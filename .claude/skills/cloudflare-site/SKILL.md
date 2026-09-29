---
name: cloudflare-site
description: Deploy, check, and change the business site on Cloudflare — the `aisaac` Worker behind iwantaiformybusiness.com and its lead relay. Use whenever you push a site change and need to know it is live, add a page or a domain to the business site, add or change where leads go (GoHighLevel, any webhook), set the Stripe webhook secret, run the site locally with its relay, or anything in the site fails to show up after a push.
---

# The business site on Cloudflare

The law is `00-SITE-CANON.md` § HOSTING AND AUTOMATIONS (what is served where, and why). This is the HOW.

## What runs

- ONE **Cloudflare Worker with static assets**, named `aisaac`, connected to this repo's `main`: every push
  builds and deploys it (≈1 minute). No build step, no GitHub workflow. GitHub Pages deploys the same push to
  `sancovp.github.io/aisaac` (the rest of the old site).
- `wrangler.jsonc` — its settings: the two routes (`iwantaiformybusiness.com`, `www.`), assets = the repo.
- `worker.js` — runs FIRST on every request: other domains + `www` → 301 to `iwantaiformybusiness.com` ·
  `POST /api/lead`, `POST /api/stripe` → the relay · `/` → `ai-transformation` · only the pages in `PAGES`,
  the files in `FILES` and `assets/` are served · anything else → 302 home · byte ranges for Safari video.
- `.assetsignore` — what is never served: every dot-file (the rules), `docs/`, `tools/`, `functions/`,
  `lib/`, the Worker's own source. **No served file may exceed 25 MiB** (Cloudflare's per-asset limit).
- THE RELAY — `functions/api/lead.js` (every form) · `functions/api/stripe.js` (Stripe's payment webhook) ·
  `lib/relay.js` (the destination list and the push). It pushes; it never stores and never sends mail.
- SECRETS live in the Worker's settings, never in a file in git: `DESTINATIONS` and `STRIPE_WEBHOOK_SECRET`.
  Locally they are in `.dev.vars` (git-ignored). **Secrets are write-only on Cloudflare** — they cannot be
  read back — so `.dev.vars` is the copy you edit and re-put from.

## Did my push go live?

```bash
npx wrangler deployments list | tail -8          # the newest version and when it was made
curl -s "https://iwantaiformybusiness.com/?cb=$RANDOM" | grep -o 'stack.js?v=[^"]*'   # the live page's stamps
```
The first request after a push can still get the old page while the new version rolls out — wait a minute
and ask again. A returning browser keeps an old `style.css`/`*.js` unless its `?v=` stamp changed: bump the
stamp in every page that links the file, in the same commit (RULE 02 § quality gates).

## Add a page to the business domain

Add its path (no `.html`) to `PAGES` in `worker.js` (a new script or stylesheet goes in `FILES`); its media
goes under `assets/`. Canonical/og URLs on business pages use `https://iwantaiformybusiness.com` with clean
paths (canon law 5). Push.

## Add a domain

1. *USER* buys it at Cloudflare's registrar (an account action — never an agent's).
2. Add its hostname to `REDIRECT_HOSTS` in `worker.js` (so it 301s to the address) and a
   `{ "pattern": "<domain>", "custom_domain": true }` route in `wrangler.jsonc`, plus its `www.`.
3. Push. If the domain does not answer after the build, apply the routes directly:
   `npx wrangler triggers deploy`. A route for a domain the account does not own fails ("can't infer zone").

## Where leads go — the destination list

`DESTINATIONS` is a JSON list; each destination takes the events it names:

```json
[{"name": "formspree", "url": "https://formspree.io/f/…", "events": ["lead"]},
 {"name": "ghl", "url": "<GHL inbound-webhook URL>", "events": ["lead", "payment", "refund"],
  "headers": {"Authorization": "Bearer …"}, "rename": {"email": "contact_email"}}]
```
`headers` and `rename` are optional. To add GoHighLevel (or any webhook): edit the list in `.dev.vars`, then

```bash
npx wrangler secret put DESTINATIONS        # paste the WHOLE list — a put replaces it
npx wrangler secret list                    # names only; confirms it is set
```
No page and no code change. A destination that fails never stops the others.

## Stripe — the payment trigger

In Stripe, add a webhook endpoint `https://iwantaiformybusiness.com/api/stripe` for
`checkout.session.completed`, `invoice.paid` and `charge.refunded`; copy its signing secret (`whsec_…`)
into `.dev.vars` and `npx wrangler secret put STRIPE_WEBHOOK_SECRET`. The relay checks the signature
(5-minute window) and pushes one plain `payment` or `refund` event, with the partner code when Stripe
carried it. Creating the Payment Links and the endpoint is *USER*'s (live payment objects on his account).

## Run it locally

```bash
npx wrangler dev --port 8788                 # the Worker + relay, reading .dev.vars
curl -s -o /dev/null -w '%{http_code}\n' -X POST http://127.0.0.1:8788/api/lead \
  -d 'email=test@example.com&name=Test&form=test&_gotcha='     # 303 = accepted and forwarded
```
A local run pushes to the REAL destinations in `.dev.vars` — a test lead lands in the real inbox/CRM.

## Log in

`npx wrangler whoami` shows the account. If it is logged out, *USER* runs `npx wrangler login` once
(a browser OAuth on his account); it persists on this machine.
