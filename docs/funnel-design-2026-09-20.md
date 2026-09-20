# THE FUNNEL — the landing page, the two purchases, and what happens after they buy

**Status: DESIGN, not built.** *USER*, 2026-09-20: *"ok start writing this down. Because we have to
plan what happens after they buy as well."*

**Scope:** ONE page. It is a standalone funnel that will be **deployed on its own domain**. It is
not part of the GitHub site — *USER*, 2026-09-20: *"we are using github to store what we are working
on, and it is publicly available as a set up github site, but it is not intended to be a github
site."* Measured: no page on that site links to `ai-transformation.html`, and it links out to
nothing but itself. The other 39 pages are a separate, older property and are out of scope here.

---

## 0. THE OFFER — *USER*'s words, 2026-09-20, and the only place it is written

> *"Its $3k upfront for **three months of AI transformation partnership** and then $2000/mo after
> 90 days."*

**⛔ OFFERS ARE FROZEN (`00-SITE-CANON` hard law 1). The three lines below are *USER*'s and no agent
edits them.** Everything else in this document is mechanism and is arguable.

| SKU | what it is |
|---|---|
| **THE FOUNDING DEAL** | **$3,000 up front = three months of AI transformation partnership.** At day 90 it continues at **$2,000/month**. |
| **THE RETAINER** | **$2,000/month**, month to month. |
| **THE CALL** | free discovery call. No purchase. |

⚠ **SUPERSEDED, KEPT:** every offer surface on the old site says **$1,000/mo**, and the sales deck's
slide 13 says `$1,000 / month`. **$2,000 is canonical as of 2026-09-20** (*USER*, verbatim: *"yeah
its $2000 now canonically"*). The deck is now stale on its last slide and the film is built to never
say a price at all, so neither needs re-cutting when this moves again.

### THE SINGLE-MONTH SKU IS DELIBERATELY NOT BUILT

*USER* raised it and questioned it in the same breath (*"single month or recurring purchase for some
reason (lol?)"*). It is not built, for three reasons: month-to-month **already is** the single-month
purchase (subscribe, cancel after one); every option on a checkout costs conversion; and one month
of mapping produces a partial map, which is the one version of this that cannot deliver its own
outcome. The offer's own mechanism — *stop when the next cycle isn't worth it* — already contains
the exit.

---

## 1. THE PAGE

```
HEADLINE / SUBHEADLINE
VIDEO                     the full sell, start to finish
THE STACK                 the six value lines again in text, because people scroll past video
THE OFFER                 the three doors
     [ $3,000 — three months ]        PRIMARY
     [ $2,000 / month ]               secondary
       rather talk first? book a call   the exit
ABOUT ME / PHOTO
```

**THE FOUNDING DEAL IS THE PRIMARY BUTTON, AND THE RETAINER'S JOB IS TO PRICE IT.** $3,000 for 90
days against $6,000 at the monthly rate is legible only when both are on screen. The expensive
option exists so the cheap one can be read.

**THE CALL IS THE EXIT, NOT A PEER.** Smaller, below, lower contrast, worded *"rather talk first?"*
⛔ **Never the word FREE next to a price** — a free thing beside a $2,000 thing is not a downsell,
it is the obvious choice, and it takes the price with it.

### ⚠ THE UNRESOLVED TENSION, AND IT IS *USER*'S TO RULE ON

`business-context-2026-09-15-first-client.md` settled the opposite five days ago:

> *"The B2B content endpoint is settled: `CONTENT → TALK TO ISAAC`. No lead magnets, no nurture
> sequences, no community infrastructure until the service is verified. The site should not grow
> funnel machinery yet."*

and

> *"**The sales call is the smallest demonstration of the product** — sales mechanism and service
> mechanism are the same mechanism."*

If the call IS the demonstration, a checkout that skips the call skips the thing that sells it. And
the qualifier was **"until the service is verified"** — there are zero clients, so it is not.

**The reading that reconciles them:** build the buttons, keep the call primary in emphasis, and
treat the checkout as the PRICE ANCHOR it is. Someone who books after seeing $3,000 on a button
arrives pre-qualified and pre-framed, and the price reveal never has to happen on the call. The
button does work even when nobody clicks it. ⏸ **Whether the call or the checkout gets top billing
is NOT decided.**

---

## 2. THE STRIPE MECHANICS — this is native, no custom program is needed

*USER*: *"So you sign up for that exact process somehow through stripe... or we have a program that
makes it happen on stripe or something. or idk. idk if we can."*

**You can. It is one Checkout Session.**

```
line item 1   one-time        $3,000
subscription  $2,000 / month  with  trial_period_days: 90
```

They are charged **$3,000 today**. The subscription bills **nothing** for 90 days. On day 91 it
starts at **$2,000/month**, automatically. Cancelling inside the 90 days means they are never
charged again — which IS the de-risk, without a second sale.

⚠ **VERIFY THE EXACT LINE-ITEM RULES AGAINST CURRENT STRIPE DOCS BEFORE BUILDING.** Mixing a
one-time price with a trialling subscription in one Session is supported; the precise field shape
changes between API versions and is not worth trusting from memory.

### THE TWO SHAPES, AND WHY A IS RECOMMENDED

| | A — trial-continuation *(recommended)* | B — *USER*'s de-risk variant |
|---|---|---|
| mechanism | $3k now, subscription auto-starts day 91 | $3k now, nothing else. They come back and buy $2k/mo |
| continuation | **by default** | by re-sale |
| risk | must be disclosed plainly or it is a dark pattern | zero |
| cost | — | you re-sell every client at day 90, forever |

*USER* floated B as the de-risk (*"3k for 90 days then OPTION if you continue its normal price so
they just come back and buy the $2k"*). **A gets the same de-risk from cancel-anytime while keeping
continuation as the default**, and it is not deceptive as long as the button says what happens.
**THE DISCLOSURE IS NOT OPTIONAL AND IT GOES ON THE BUTTON, NOT IN THE TERMS:**
*"$3,000 today for three months. Continues at $2,000/month after. Cancel any time."*

### NOT SHOWING THE FOUNDING DEAL TO SOMEONE WHO TOOK IT

*USER*: *"we make it cookie so that they cant see the $3k after they buy it."*

A cookie is the weak version — it clears, and it does not survive a second device. **The mechanism
that actually holds is a redemption cap on the price itself:** Stripe Payment Links support a
maximum number of redemptions, so the founding SKU is capped at its real number and simply stops
being purchasable. That also closes the leak a cookie does not: an existing client buying a SECOND
founding term at day 91 instead of the retainer.

---

## 3. SCARCITY — what is legal, stated plainly

*USER*: *"maybe we put scarcity like it fake fills up every 30 days and re-opens 2 weeks later with
a different number of max clients. Whatever is actually legal that-wise."*

**I am not a lawyer and this is not legal advice.** The line, as it is actually enforced:

| | |
|---|---|
| ✅ **Real cap, truthfully stated** | *"I take N clients at a time."* True, enforced, closes when full. |
| ✅ **Real enrollment windows** | Open and closed on a schedule you actually honour. |
| ⛔ **A counter that fills on a timer regardless of sales** | Deceptive. This is the specific pattern regulators pursue — FTC Act §5 in the US, the Unfair Commercial Practices Directive in the EU. False "limited time" and fake stock counters are named examples. |

### ⭐ THE DECLINING ADMISSION SCHEDULE (*USER*, 2026-09-20) — the honest version, and it works

> *"its the next 3 for the first 2 weeks of the month, the next 2 for the 3rd week, the next 1 for
> the 4th week... so it looks like it fills but it doesnt. it isnt fake, either, its just how it
> works."*

**He is right, and the thing that makes it true is the WORDING, not the schedule.**

| | |
|---|---|
| ⛔ *"1 spot left"* | a claim about **DEMAND** — it implies two were taken. False if they were not. |
| ✅ *"Taking 1 more client this month"* | a claim about **CAPACITY** — true whether or not anyone bought. |

Identical urgency, identical declining number. One is an unverifiable statement about the world; the
other is a published operating policy, which is *USER*'s to declare and is true the moment it is
honoured. **And it has a real service rationale underneath it:** a client admitted on the 28th gets
a worse first 90 days, because their onboarding lands in the seam between months. Admitting fewer
people late in the cycle is an operating choice, not a device.

**THE SCHEDULE IS A CEILING, NEVER A FLOOR — it must also fall on real sales:**

```
shown = min( schedule_for_this_week , monthly_cap − sold_this_month )

  weeks 1–2  →  3        if 3 sell in week one it reads 0 for the rest of the
  week 3     →  2        month, NOT 3 → 2 → 1. Otherwise the number is announcing
  week 4     →  1        availability that is already gone, which is the deceptive
                         direction and the easiest one to fall into by accident.
```

At 0 the founding button genuinely closes. The serverless function reads this month's founding-SKU
count from Stripe, takes the min, renders the number — no bookkeeping, and it cannot drift from
reality because reality is its input.

⛔ **THE ONLY THING THAT MAKES ANY OF THIS FALSE IS NOT HONOURING IT.** If a second buyer appears on
the 26th and is admitted, the representation was untrue and every prior month's was retroactively a
performance. **The price of this mechanism being real is being willing to refuse money you could
have taken** — that cost is the mechanism, and it should be known before it goes on the page.

⇒ **MAKE THE CAP REAL AND IT DOES EVERYTHING THE FAKE ONE WOULD.** The truthful version is already
strong here and costs nothing, because the scarcity is genuinely real: *USER* needs three clients
and can only serve so many at once. **"The first three companies" is a fact.** When the seats fill,
the founding price closes until one opens — and it closes *because it is closed*, which is the whole
difference.

This is also the same law as `.claude/rules/anti-case-study.md` — *"Never fake case studies. The
system IS the proof."* A fake counter is that sin relocated to the checkout.

---

## 4. ⭐ AFTER THEY BUY — the part *USER* asked for, and the part nobody has written

`Stripe success` → redirect → **the onboarding page** (unlisted URL; no auth needed at three clients)

| # | what happens | built with |
|---|---|---|
| 1 | **Book the first two sessions.** A DIFFERENT cal.com link than the discovery one — this is a client scheduling link, not a sales one. | cal.com |
| 2 | **The intake.** Departments, roles, systems, and what they already have written down. This is the raw material for the map, and it is the thing that makes session one productive instead of introductory. | a form |
| 3 | **Pre-recorded: what happens in the first 90 days.** The arc — foundation, then hardening, then closure — as it applies to them. | video |
| 4 | **Pre-recorded: what to bring to session one.** Org chart, any SOPs that exist, last month's numbers by line. | video |
| 5 | **Pre-recorded: how the mapping works.** DISCOVER → MAP → ANALYZE → RESEARCH → DECIDE, and what a decision looks like — including that STOP is a real answer. | video |

⏸ **OPEN:** whether those three videos are made in `video-aios` like the VSL, or recorded plainly by
*USER*. They are client-facing, not prospect-facing, so the bar is different and plain is likely
right. **Not decided.**

⏸ **OPEN:** what happens at **day 75** — the trial-ending moment. Stripe can send its own
notification; whether *USER* wants that, or a personal message, or a session on the calendar to
decide continuation, is unsettled. **This is the single highest-leverage unbuilt thing in the
document**, because it is where a founding client becomes a retained one.

---

## 5. WHAT IS ALREADY TRUE (no decisions needed)

- **The video never states a price.** The cascade runs $38,000 → *not even that* → *not even half*
  → *not even half that* → *and I'm still not charging that* → **and lands on the button.** The two
  dollar figures it keeps ($38,000 market rate, $29K–$220K DIY exposure) are facts about the MARKET,
  not about *USER*'s offer, so they do not move when the price does.
- **The video fits in the repo.** 130 MB → **54.5 MB** at CRF 24, PSNR 41 dB, visually identical
  (checked, not assumed). No R2, no YouTube, no new hosting needed for the file itself.
- **A real cart needs one serverless function.** A static page cannot create a Stripe Checkout
  Session — the secret key cannot be in the browser. Payment Links and the Pricing Table embed are
  static and need nothing; the assembled cart does. This is the one thing that decides the host.

## 6. STILL NEEDED FROM *USER*

1. **The domain.**
2. **Call primary or checkout primary** (§1's tension).
3. **The real cap number** — how many clients at once, which is what makes the scarcity true.
4. Whether `draw-the-box` **replaces** the climb video currently on the page, or both live there.
5. Trial-continuation (A) or re-sale (B) in §2.
