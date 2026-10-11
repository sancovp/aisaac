# THE DOOR — five avatars, five sales conversations, one cart

The design of everything a visitor meets before they are a customer: the home (the avatar picks itself), each avatar's own
sales conversation, the one cart they all end at, the hand-holding on top of it, and the look. The site canon
(`.claude/rules/00-SITE-CANON.md` § WHAT IS PUBLIC, law 9, the source map's door row) states the rulings as law; this
document holds the whole design in one place. History: `CHANGELOG.md`.

## 1. The model

```
the visitor ─▶ THE DOOR: the avatar picks itself
                 │
                 ├─▶ avatar 1 ─▶ its own CLOSER ─┐
                 ├─▶ avatar 2 ─▶ its own CLOSER ─┤
                 ├─▶ avatar 3 ─▶ its own CLOSER ─┼─▶ THE CART: exactly what this avatar needs INSIDE JobWorld
                 ├─▶ avatar 4 ─▶ its own CLOSER ─┤        (the AI system they do it in, with them and for them)
                 └─▶ avatar 5 ─▶ its own CLOSER ─┘                     │
                                                                       ▼
                                          THE HAND-HOLDING, by who they are:
                                          the community (individuals) · a B2B engagement on a retainer (businesses)
```

- **The avatar self-selects.** The door asks one question and the visitor picks the card that is them.
- **Each avatar gets ITS OWN sales conversation, attuned to it** — never one script for all, never avatars mashed together.
- **Every conversation is the CLOSER process** (the `hormozi-closer` skill): Clarify why they are here · Label the pain ·
  Overview what they have tried · Sell the vacation · Explain away their concerns · Reinforce the decision.
- **Every conversation ends at the same cart: JobWorld**, set up with exactly what that avatar needs — they do it
  themselves (DIY) inside an AI system that does it with them and for them.
- **Then the hand-holding, by who they are:** the community for individuals; a B2B engagement on a retainer for businesses.
- **It is not selling AI transformation.** It is getting each person, in their own terms, to the JobWorld they need.

## 2. The door — the look

- **Full screen, the film behind everything:** the agents' loop (`assets/hero-loop-2.mp4`) fills the screen; over it sits
  only the top bar and ONE GLASS PANEL — the survey, frosted over the film. Nothing else on the screen. The glass is the
  door's own look, not the Blueprint drafting sheet.
- **Cards, as the June survey had them** (`git show 9b26f427:index.html`): the question centered over a row of cards —
  an icon, a title, one line, its call at the foot. Sub-steps are cards too.
- **The arm presses every card** (`arm.js`, RULE 02 §8b), and every step slides in. The agents' own animations on each
  transition come next; each avatar's part opens with a VSL by *USER*'s digital twin when it exists.

## 3. The five avatars — each one's conversation, and its cart

Each row is a CLOSER, written in that avatar's terms. The words of each step are drafted with the `hormozi-closer` skill and
are *USER*'s to strike.

| avatar (the card) | Clarify — why they are here | where the conversation goes | the cart: what they need inside JobWorld | hand-holding |
|---|---|---|---|---|
| 1 **I need JobWorld for my business** — the owner | the business they run and what is eating their time | each feature as the pain it ends ("do you have this?" → "JobWorld does it like this"), the list, N seats (a seat = one JobWorld per person in the org chart, `application/jobworld/DESIGN.md` §6) | JobWorld with those departments and N seats | a B2B engagement on a retainer |
| 2 **I want to start an AI-native business** — the founder | what they want to start | the business they picture, run from day one by an AI CEO | JobWorld, their new company in it | the community |
| 3 **I want to learn how to use AI** — the learner | what for: their business · their work · building agents | what they tried, where they got stuck; "I'll send you the right material" (an email sign-up, law 13's consent boxes) | JobWorld — it carries the Claude compilation skills and teaches AI by doing it with them | the community |
| 4 **I want to learn to sell, market or run my operations** — the entrepreneur who wants to grow | which of the three, and where it stalls | "need frameworks? here they are" — the B2B bootcamp (`/bootcamp`: PSA · SCREENING · CLINIC · DOCTOR · LIFE and the tools), for entrepreneurs to learn from — "and they are inside JobWorld too: want that?" | JobWorld, running those frameworks with them and for them | the community, or the retainer for a business |
| 5 **I want to sell JobWorld to my clients** — the agency | what they do and who their clients are | "do you want it tailored for you?" | the agency level — LAMAI's Meta Business, the white label (their name, mark and colours on JobWorld for their clients; `sanctuary-revolution-alpha/application/lamai-saas/DESIGN.md` §2) | tailoring on a call with *USER* |

**How a feature is said** (avatars 1 and 5): GoHighLevel's public funnel is the reference for its shape only — *it does
x, y, z: what you need for your business and to sell to your clients* — our positioning differs, its words are never
copied, GHL is never named. The features come from JobWorld's own design, never invented on the site.

## 4. The cart

One cart for everyone: **Get JobWorld** → the plans and the Stripe checkout (`app.iwantaiformybusiness.com/pricing`). What
each avatar's conversation decided (which departments, how many seats, the agency level) rides into it. The JobWorld page
(`jobworld.html`, the app's root) is a funnel to the same cart: Get JobWorld · Sign in · Book a call.

## 5. One look for the rest

Everything past the door — the JobWorld page, the bootcamp, the accounts app (sign-in, sign-up, pricing, the dashboard) —
wears the site's Blueprint System (RULE 02); every primary button carries the arm.

| surface | state |
|---|---|
| the door, glass over the film | being built |
| each avatar's CLOSER conversation | owed — next |
| the JobWorld page at the app's root, with Get JobWorld | live |
| the bootcamp at `/bootcamp` | live |
| the sign-in and sign-up | live |
| pricing and the dashboard in the theme | owed |

## 6. Open — *USER*'s

- the twin, and each avatar's VSL
- the words of each CLOSER (drafted with the skill, struck by *USER*)
- THE PRICING PASS, later: the seat's price and the plans' — the direction is down, toward something like $297/mo plus about
  $20 a seat, once a seat's cost and the SaaS's cost are measured (`sanctuary-revolution-alpha/application/lamai-saas` board
  § OPEN); Stripe goes live with it
- the community's home and terms; the retainer's terms for the B2B engagement

## 7. The order of work

1. the door as glass over the film — now
2. each avatar's CLOSER conversation, drafted with the skill, ending at the cart
3. the hand-holding offers on the far side of the cart (community · retainer)
4. pricing and the dashboard in the theme
5. the pricing pass, and Stripe live
6. the VSLs, when the twin exists
