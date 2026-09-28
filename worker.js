/* worker.js — THE SITE ON CLOUDFLARE (00-SITE-CANON § HOSTING AND AUTOMATIONS): a Worker with static assets.
 * It runs first on every request, then hands the rest to the site's files:
 *
 *   one address   every other domain we own (and www) → https://iwantaiformybusiness.com, same path, 301
 *   the relay     POST /api/lead   (every form)  · POST /api/stripe (Stripe's payment webhook)
 *   the home      /  →  the presented page, ai-transformation.html
 *   the files     everything else, from the repo (.assetsignore keeps the rules, docs and tooling out)
 *
 * The relay's handlers live in functions/api/*.js and lib/relay.js; secrets (DESTINATIONS,
 * STRIPE_WEBHOOK_SECRET) live in the Worker's settings, never in a file.
 */
import { onRequestPost as lead } from './functions/api/lead.js';
import { onRequestPost as stripe } from './functions/api/stripe.js';

const PRIMARY = 'iwantaiformybusiness.com';
const REDIRECT_HOSTS = [
  'www.iwantaiformybusiness.com',
  'runmybusinessonai.com', 'www.runmybusinessonai.com',
  'iwantaiinmybusiness.com', 'www.iwantaiinmybusiness.com',
];

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (REDIRECT_HOSTS.includes(url.hostname)) {
      return Response.redirect(`https://${PRIMARY}${url.pathname}${url.search}`, 301);
    }

    if (url.pathname === '/api/lead' || url.pathname === '/api/stripe') {
      if (request.method !== 'POST') return new Response('POST only', { status: 405, headers: { Allow: 'POST' } });
      return url.pathname === '/api/lead' ? lead({ request, env }) : stripe({ request, env });
    }

    if (url.pathname === '/') {
      return env.ASSETS.fetch(new Request(new URL('/ai-transformation', url), request));
    }

    return ranged(request, await env.ASSETS.fetch(request));
  },
};

/** VIDEO NEEDS BYTE RANGES: Safari will not play a <video> whose server answers a Range request with the
 *  whole file (200) instead of the slice (206), and the assets binding answers 200 when the Worker runs
 *  first. So a Range request for a whole-file answer is cut here: `bytes=a-b`, `bytes=a-`, `bytes=-n`.
 *  Files are ≤ 25 MB (Cloudflare's per-asset limit), so the slice is taken in memory. */
async function ranged(request, res) {
  const range = request.headers.get('Range');
  if (!range || res.status !== 200 || request.method !== 'GET') return res;
  const m = /^bytes=(\d*)-(\d*)$/.exec(range.trim());
  if (!m || (m[1] === '' && m[2] === '')) return res;
  const buf = await res.arrayBuffer();
  const size = buf.byteLength;
  let start, end;
  if (m[1] === '') { start = Math.max(0, size - Number(m[2])); end = size - 1; }
  else { start = Number(m[1]); end = m[2] === '' ? size - 1 : Math.min(Number(m[2]), size - 1); }
  const headers = new Headers(res.headers);
  headers.set('Accept-Ranges', 'bytes');
  if (start >= size || start > end) {
    headers.set('Content-Range', `bytes */${size}`);
    return new Response(null, { status: 416, headers });
  }
  headers.set('Content-Range', `bytes ${start}-${end}/${size}`);
  headers.set('Content-Length', String(end - start + 1));
  return new Response(buf.slice(start, end + 1), { status: 206, headers });
}
