/* /api/stripe — Stripe calls this when money moves (00-SITE-CANON § REFERRAL PARTNERS).
 *
 * Sales close on a call and are paid through Stripe, so a payment is the commission's
 * trigger. The relay proves the call came from Stripe (the signing secret), turns it into
 * one plain event — `payment` or `refund`, with the payer's email and the amount — and
 * pushes it. The destination (GoHighLevel's workflow) finds the contact by that email and
 * does the rest: a referred client's first payment → "pay <partner> $1,000"; a refund →
 * cancel an unpaid one; no contact → flagged for a person.
 *
 * Stripe events it listens for: checkout.session.completed (a payment link was paid) ·
 * invoice.paid (an invoice or a subscription month) · charge.refunded.
 *
 * ⛔ ONE PAYMENT CAN ARRIVE TWICE: a link checkout that creates an invoice (every subscription link) fires
 * BOTH checkout.session.completed and invoice.paid for the same money. Both carry the same `payment_id`
 * (the invoice id), and a destination dedupes on it — the relay keeps both, because the checkout event is
 * the one with the partner `ref` and the invoice event is the only one for a subscription made outside a
 * link. The whole contract: docs/stripe-payments.md §5.
 */
import { push, json } from '../../lib/relay.js';
import { recordPayment } from '../../lib/ghl.js';

const TOLERANCE_S = 300;
const enc = new TextEncoder();

async function hmacHex(secret, message) {
  const key = await crypto.subtle.importKey('raw', enc.encode(secret), { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);
  const sig = await crypto.subtle.sign('HMAC', key, enc.encode(message));
  return [...new Uint8Array(sig)].map((b) => b.toString(16).padStart(2, '0')).join('');
}

function sameText(a, b) {
  if (a.length !== b.length) return false;
  let d = 0;
  for (let i = 0; i < a.length; i++) d |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return d === 0;
}

// Stripe-Signature: t=<unix>,v1=<hex>[,v1=<hex>…] — signed over "<t>.<raw body>"
export async function verify(header, body, secret, now = Date.now() / 1000) {
  if (!header || !secret) return false;
  const parts = header.split(',').map((p) => p.split('='));
  const t = parts.find(([k]) => k === 't')?.[1];
  const sigs = parts.filter(([k]) => k === 'v1').map(([, v]) => v);
  if (!t || !sigs.length || Math.abs(now - Number(t)) > TOLERANCE_S) return false;
  const expected = await hmacHex(secret, `${t}.${body}`);
  return sigs.some((s) => sameText(s, expected));
}

const idOf = (v) => (v && typeof v === 'object' ? v.id : v) || '';

export function normalize(evt) {
  const o = evt.data?.object || {};
  switch (evt.type) {
    case 'checkout.session.completed':
      if (o.payment_status !== 'paid' || !o.amount_total) return null;
      return { kind: 'payment', email: o.customer_details?.email || o.customer_email || '',
               name: o.customer_details?.name || '', amount: o.amount_total, currency: o.currency, ref: o.client_reference_id || '',
               payment_id: idOf(o.invoice) || idOf(o.payment_intent) || o.id, source: 'checkout', billing_reason: 'checkout' };
    case 'invoice.paid':
      if (!o.amount_paid) return null; // a trial's empty invoice is not a payment
      return { kind: 'payment', email: o.customer_email || '', name: o.customer_name || '',
               amount: o.amount_paid, currency: o.currency, ref: '',
               payment_id: o.id, source: 'invoice', billing_reason: o.billing_reason || '' };
    case 'charge.refunded':
      return { kind: 'refund', email: o.billing_details?.email || o.receipt_email || '',
               name: o.billing_details?.name || '', amount: o.amount_refunded, currency: o.currency, ref: '',
               payment_id: idOf(o.payment_intent) || o.id, source: 'charge', billing_reason: '' };
    default:
      return null;
  }
}

export async function onRequestPost({ request, env }) {
  const body = await request.text();
  if (!(await verify(request.headers.get('Stripe-Signature'), body, env.STRIPE_WEBHOOK_SECRET))) {
    return json({ ok: false, error: 'bad signature' }, 400);
  }
  const evt = JSON.parse(body);
  const n = normalize(evt);
  if (!n) return json({ ok: true, ignored: evt.type }); // answered, so Stripe stops retrying

  const { kind, amount, ...rest } = n;
  const event = {
    ...rest,
    amount: (amount || 0) / 100, // cents → dollars
    stripe_event: evt.id,
    stripe_object: evt.data?.object?.id || '',
    at: new Date((evt.created || Date.now() / 1000) * 1000).toISOString(),
  };
  const [results, crm] = await Promise.all([
    push(env, kind, event),
    recordPayment(env, { event: kind, ...event }).catch((e) => {
      console.error('ghl payment', e.message);
      return { ok: false };
    }),
  ]);
  const delivered = results.some((r) => r.ok) || crm.ok === true;
  // a 5xx makes Stripe retry later, which is what an undelivered payment needs — and a CRM write that FAILED
  // (a token is set and the call errored) must retry too, since recordPayment is safe to run twice
  const crmFailed = crm.ok === false;
  return json({ ok: delivered && !crmFailed, crm: crm.ok === true }, delivered && !crmFailed ? 200 : 502);
}
