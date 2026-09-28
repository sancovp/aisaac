/* /api/lead — every form on the site posts here (DIRECTION ①, the world → GoHighLevel).
 *
 * It takes the same fields the forms send today (so moving a form here changes only its
 * `action`), drops bots, labels the submission (which form, which page, which partner),
 * pushes it to every destination, then sends the visitor on to the form's `_next` — or,
 * for a script, answers JSON.
 */
import { push, json } from '../../lib/relay.js';

// where a form may send the visitor afterwards: this site, the booking calendar, Stripe checkout
const NEXT_HOSTS = ['iwantaiformybusiness.com', 'sancovp.github.io', 'cal.com', 'buy.stripe.com', 'checkout.stripe.com'];
const REF = /^[a-z0-9_-]{1,40}$/i;
const EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

async function fields(request) {
  const type = request.headers.get('Content-Type') || '';
  if (type.includes('application/json')) return await request.json();
  const form = await request.formData();
  const out = {};
  for (const [k, v] of form.entries()) out[k] = typeof v === 'string' ? v.trim() : '';
  return out;
}

function safeNext(next, origin) {
  if (!next) return null;
  try {
    const u = new URL(next, origin);
    const host = u.hostname.replace(/^www\./, '');
    if (u.protocol === 'https:' && NEXT_HOSTS.includes(host)) return u.toString();
    if (u.origin === origin) return u.toString();
  } catch {}
  return null;
}

export async function onRequestPost({ request, env }) {
  let f;
  try {
    f = await fields(request);
  } catch {
    return json({ ok: false, error: 'unreadable form' }, 400);
  }

  const origin = new URL(request.url).origin;
  const next = safeNext(f._next, origin);

  // the bot trap: a hidden field no person fills in — answer as if it worked, push nothing
  if (f._gotcha) return next ? Response.redirect(next, 303) : json({ ok: true });

  if (!EMAIL.test(f.email || '')) return json({ ok: false, error: 'a valid email is required' }, 400);

  const payload = {};
  for (const [k, v] of Object.entries(f)) if (!k.startsWith('_')) payload[k] = v;
  payload.form = f.intent || 'unknown';
  payload.ref = REF.test(f.ref || '') ? f.ref.toLowerCase() : '';
  payload.page = f.page || new URL(request.headers.get('Referer') || origin).pathname;
  payload.submitted_at = new Date().toISOString();
  payload.country = request.cf?.country || '';

  const results = await push(env, 'lead', payload);
  const delivered = results.some((r) => r.ok);
  if (!delivered) console.error('lead not delivered', JSON.stringify(results));

  if (next) return Response.redirect(next, 303);
  return json({ ok: delivered, results: results.map((r) => ({ name: r.name, ok: r.ok })) }, delivered ? 200 : 502);
}
