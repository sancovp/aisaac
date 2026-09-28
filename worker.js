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

    return env.ASSETS.fetch(request);
  },
};
