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
 */
import { push, json } from '../../lib/relay.js';

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

export function normalize(evt) {
  const o = evt.data?.object || {};
  switch (evt.type) {
    case 'checkout.session.completed':
      if (o.payment_status !== 'paid') return null;
      return { kind: 'payment', email: o.customer_details?.email || o.customer_email || '',
               name: o.customer_details?.name || '', amount: o.amount_total, currency: o.currency, ref: o.client_reference_id || '' };
    case 'invoice.paid':
      return { kind: 'payment', email: o.customer_email || '', name: o.customer_name || '',
               amount: o.amount_paid, currency: o.currency, ref: '' };
    case 'charge.refunded':
      return { kind: 'refund', email: o.billing_details?.email || o.receipt_email || '',
               name: o.billing_details?.name || '', amount: o.amount_refunded, currency: o.currency, ref: '' };
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
  const results = await push(env, kind, {
    ...rest,
    amount: (amount || 0) / 100, // cents → dollars
    stripe_event: evt.id,
    stripe_object: evt.data?.object?.id || '',
    at: new Date((evt.created || Date.now() / 1000) * 1000).toISOString(),
  });
  const delivered = results.some((r) => r.ok);
  // a 5xx makes Stripe retry later, which is what an undelivered payment needs
  return json({ ok: delivered }, delivered ? 200 : 502);
}
