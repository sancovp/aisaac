# Stripe payments — the design

REFERENCE DETAIL — READ when anything touches Stripe, the payment links, the `/api/stripe` relay, or the
commission trigger. NOT deprecated, NOT skippable. The law it serves is `.claude/rules/00-SITE-CANON.md`
§ HOSTING AND AUTOMATIONS (REFERRAL PARTNERS); the HOW of the Worker and its secrets is the
`cloudflare-site` skill.

## 1. What it is for

Sales close on a call and are PAID THROUGH STRIPE. Stripe is the ledger; the payment is the TRIGGER — the
deal is won, and a referred client's first payment records the partner's $1,000. Stripe's webhook reaches
the relay (`functions/api/stripe.js`), which proves the call came from Stripe and pushes one plain event to
every destination on its list (`DESTINATIONS`); the destination (GoHighLevel's workflow) does the rest. The
relay keeps no state and never calls Stripe back.

## 2. The account

`Meetovp` — `acct_1OtdePC3GAOTArnD`, LIVE mode (the legal entity's account; the name is not shown on the site).
What was already there is kept untouched:

| product | price | link |
|---|---|---|
| AI Transformation Advisory (AHT's founding rate) | $1,000 / month | `plink_1UG2rE…` — buy.stripe.com/fZueVc7f58IW8673ce3wQ00 |
| AI Transformation Map A La Carte | $1,000 one-time | `plink_1UH44h…` — buy.stripe.com/fZu5kCfLB5wKbij9AC3wQ01 (automatic tax, invoice created) |
| Custom Dev Work 1 mo | $500 one-time | — |

## 3. The offer, as Stripe objects

The frozen offer (business-runtime `CLAUDE.md` § THE OFFER IS FROZEN): **THE FOUNDING DEAL $3,000 = 90 days,
then $2,000/mo · THE RETAINER $2,000/mo.** Prices and names are *USER*'s; these objects carry his words.

| object | what it is |
|---|---|
| **P1** product "AI Transformation Partnership — Founding 90 Days" | one-time price **$3,000** |
| **P2** product "AI Transformation Partnership — Monthly Retainer" | recurring price **$2,000 / month** |
| **L1 THE FOUNDING LINK** | subscription mode · line items P1 ×1 + P2 ×1 · `trial_period_days` **90** ⇒ the customer pays **$3,000 today**, and **$2,000/mo from day 91** until cancelled — the whole founding deal in one checkout |
| **L2 THE RETAINER LINK** | P2 ×1 ⇒ **$2,000 today and monthly** |

Both links: automatic tax ON (as the most recent existing link), billing address `auto`, the phone number
collected, Stripe's hosted confirmation page after payment. Both products take the à-la-carte product's tax code (`txcd_20060048`).
The IDs and URLs, once made, are recorded in §8.

## 4. The webhook

One endpoint: `https://iwantaiformybusiness.com/api/stripe`, events **`checkout.session.completed` ·
`invoice.paid` · `charge.refunded`**. Its signing secret (`whsec_…`) lives ONLY in the Worker's secret
`STRIPE_WEBHOOK_SECRET` and in the local `.dev.vars` (git-ignored) — never in a file in git, never in chat.
The relay rejects an unsigned or stale (> 5 min) call with 400.

## 5. What the relay sends — the contract every destination can rely on

One event per Stripe event that means money moved, JSON, pushed to every destination whose `events` list
names it:

| field | meaning |
|---|---|
| `event` | `payment` or `refund` |
| `payment_id` | **THE DEDUPE KEY** — the Stripe invoice id when the payment has an invoice, else the PaymentIntent id (a refund: the PaymentIntent id, else the charge id) |
| `source` | `checkout` (a Checkout Session, i.e. a payment link) · `invoice` · `charge` |
| `billing_reason` | on invoice payments: `subscription_create` (a subscription's first payment) · `subscription_cycle` (a renewal) · `manual` (a one-off invoice) · … ; `checkout` on a checkout payment |
| `email` · `name` | the payer, as Stripe has them |
| `amount` · `currency` | dollars (not cents) · `usd` |
| `ref` | the partner code, when the checkout started on the site (`client_reference_id`); empty otherwise |
| `stripe_event` · `stripe_object` · `at` | the Stripe event id, the object id, when |

⛔ **ONE PAYMENT CAN ARRIVE TWICE, AND THAT IS BY STRIPE'S DESIGN**: a payment-link checkout that creates an
invoice (every subscription link, and a one-time link with invoice creation on) fires BOTH
`checkout.session.completed` and `invoice.paid` for the same money. Both carry the SAME `payment_id` (the
invoice id). ⇒ **A DESTINATION DEDUPES ON `payment_id`.** The relay does not drop either one itself: the
checkout event is the one carrying the partner `ref`, and the invoice event is the only one for a
subscription made outside a payment link — dropping either loses something real. A payment of $0 (a trial's
empty first invoice) is not sent.

## 6. Which events each link produces

| link | at purchase | later |
|---|---|---|
| L1 founding | `checkout` $3,000 (ref) + `invoice` $3,000 `subscription_create` — one `payment_id` | day 91 and monthly: `invoice` $2,000 `subscription_cycle` |
| L2 retainer | `checkout` $2,000 (ref) + `invoice` $2,000 `subscription_create` — one `payment_id` | monthly: `invoice` $2,000 `subscription_cycle` |
| à la carte (existing) | `checkout` $1,000 + `invoice` $1,000 `manual` — one `payment_id` | — |
| AHT's advisory (existing) | as L2, at $1,000 | monthly `subscription_cycle` |
| a refund | `refund` with the refunded amount | — |

## 7. The destination's side — the GoHighLevel workflow (`ASPIRATIONAL:` until GHL joins the list)

On `payment`: if the contact's last `payment_id` equals this one → stop (the duplicate) · find the contact by
`email` (none → flag for *USER*) · mark the deal won · if the contact carries a partner and no commission is
recorded yet → record "pay <partner> $1,000" and tag it · store `payment_id` on the contact. On `refund`:
cancel an unpaid commission. A renewal (`subscription_cycle`) never records a commission. Until GHL is on
the list, the stand-in destination receives the same events (a duplicate there is only a second email).

## 8. What exists now

| object | id | url / state |
|---|---|---|
| P1 "AI Transformation Partnership — Founding 90 Days" / $3,000 one-time | `prod_VLW9irRKLRXZTB` / `price_1UKp79C3GAOTArnDbwcwaLv0` | live |
| P2 "AI Transformation Partnership — Monthly Retainer" / $2,000 a month | `prod_VLW9NOieOAjOfb` / `price_1UKp7FC3GAOTArnDJoOwrwge` | live |
| L1 founding link | `plink_1UKpEtC3GAOTArnDZFn9YiAy` | live · https://buy.stripe.com/bJe3cu7f54sG7237su3wQ02 · P1 + P2, trial 90 days, automatic tax, phone collected |
| L2 retainer link | `plink_1UKpEyC3GAOTArnDowO5738K` | live · https://buy.stripe.com/fZu4gy7f5aR40DF6oq3wQ03 · P2, automatic tax, phone collected |
| webhook endpoint | `we_1UKp8BC3GAOTArnDQDgUVTF3` | enabled · `https://iwantaiformybusiness.com/api/stripe` · its secret in the Worker (`STRIPE_WEBHOOK_SECRET`) and `.dev.vars` |

**PROVEN LIVE** (§10): an unsigned call → 400 · a correctly signed event of an ignored type → 200 `ignored` ·
a wrong signature → 400. ⚠ A test request must send a browser-like or Stripe's own user-agent
(`Stripe/1.0 (+https://stripe.com/docs/webhooks)`): Cloudflare answers a script's default one
(`Python-urllib`) with 403 error 1010 before the Worker runs — Stripe's own calls pass.

## 9. The site's hand-off

`capture.js` `DEST.founding` → L1's URL, `DEST.retainer` → L2's URL; it appends `prefilled_email` and
`client_reference_id` (the partner code). The presented page offers only the call — the links are what
*USER* sends after the call, and what the preserved full funnel page's checkout doors use.

## 10. Proving it, and undoing it

PROOF: a signed event of a type the relay ignores returns 200 `ignored`; an unsigned one returns 400; after
the first real payment, the endpoint's deliveries in the Stripe dashboard show 200. UNDO: disable the
webhook endpoint; deactivate the links (a payment link cannot be deleted, only deactivated).
