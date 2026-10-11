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
| 1 **I need JobWorld for my business** — the owner (B2B) | the business they run and what is eating their time | each feature as the pain it ends ("do you have this?" → "JobWorld does it like this"), the list, N seats (a seat = one JobWorld per person in the org chart, `application/jobworld/DESIGN.md` §6) | JobWorld with those departments and N seats | a B2B engagement on a retainer |
| 2 **I want to start an AI-native business** — the founder | where they are starting from: an idea · a skill and no idea yet · only the will · leaving a job | JobWorld helps them make an idea it can run on its own, or helps them run the parts it cannot; one seat, the AI CEO and its departments as the team from day one | JobWorld, one seat, their new company in it | the community, free with JobWorld; done-with-you only after they buy (§4) |
| 3 **I want to learn how to use AI** — the learner | what for: their business · their work · building agents | where AI stops working for them, how they learned so far; JobWorld carries the Claude compilation skills and teaches AI by doing it with them | JobWorld | the free sign-up (law 13's consent boxes): the weekly letter — a version of the newsletter on what each change means for people using JobWorld — every framework and manual, and the community where they share and help each other |
| 4 **I want to learn to sell, market or run my operations** — the entrepreneur who wants to grow | which of the three, and where it stalls | "you need frameworks — here they are": the B2B bootcamp's frameworks (PSA · SCREENING · CLINIC · DOCTOR · LIFE · MEDICINE · OFFERS, in `/bootcamp`'s words, the whole page linked), for entrepreneurs to learn from — "and every one runs inside JobWorld too: want that?" | JobWorld, running those frameworks with them and for them | the community, free; the retainer for a business, offered after they buy (§4) |
| 5 **I want to sell JobWorld to my clients** — the agency | what they do | what is hard now (churn · delivery that does not scale · another vendor's name · custom setups · thin recurring revenue), how many clients they would put on it | the agency level = **Meta Business** (`sanctuary-revolution-alpha/application/lamai-saas/DESIGN.md` §2), on sale on the plans page: JobWorld under their own name, logo, colours, domain and email; each client its own business under them; their clients paid in their own Stripe, one monthly bill to us | tailoring their version with *USER*, offered after they buy (§4) |

**How a feature is said** (avatars 1 and 5): GoHighLevel's public funnel is the reference for its shape only — *it does
x, y, z: what you need for your business and to sell to your clients* — our positioning differs, its words are never
copied, GHL is never named. The features come from JobWorld's own design, never invented on the site.

## 4. The cart — a direct-response funnel

Every conversation ends at the same cart, and the cart is a classic direct-marketing funnel: **a visitor sees an offer
only at the stage that earns it.** Nobody is sold done-with-you before they have bought the product.

```
the CLOSER ─▶ 1 FRONT END ─▶ 2 CHECKOUT ─▶ 3 ONE-TIME OFFER ─▶ 4 NO THANKS ─▶ 5 IN
              the JobWorld    Stripe, with   after payment, only    the lighter      the dashboard,
              plan the        its order      to a buyer: this       offer, or none   the community,
              conversation    bump           avatar's done-with-                     the letter
              sold                           you
```

1. **Front end — the only offer before payment:** the JobWorld plan the conversation sold (Single Business; the agency's
   Meta Business), at `app.iwantaiformybusiness.com/pricing`. What the conversation decided rides in as the address's
   query: `from=door`, `avatar`, `seats` (the owner's answer; the founder's one), `clients` and `tier=meta` (the agency).
   **The one exception is the B2B avatar, the owner:** beside Get JobWorld it is offered the retainer (Set it up with
   Isaac, a call) — a business goes straight to done-with-you. The learner's free sign-up (the letter, the frameworks
   and manuals, the community) is a lead magnet, not done-with-you, and stays beside its cart. The community, free with
   JobWorld, may be named as part of what they get.
2. **Checkout** — Stripe, the plan in the cart, and the ORDER BUMP: one add-on ticked on the checkout itself. Which
   add-on is *USER*'s (§6).
3. **The one-time offer — only after payment.** Stripe's return lands on a page between the checkout and the dashboard
   that shows this avatar its done-with-you, once: the owner who bought on their own → set it up with Isaac on the
   retainer · the entrepreneur → the retainer, for a business · the agency → tailoring their version with Isaac · the
   founder and the learner → their own (*USER*'s, §6). It knows the avatar because the door's answers ride into the
   checkout's metadata.
4. **No thanks** → the lighter offer (the downsell), or straight on (*USER*'s, §6).
5. **In:** the dashboard, and what they bought brings with it — the community, the weekly letter.

## 5. One look for the rest

Everything past the door — the JobWorld page, the bootcamp, the accounts app (sign-in, sign-up, pricing, the dashboard) —
wears the site's Blueprint System (RULE 02); every primary button carries the arm.

| surface | state |
|---|---|
| the door, glass over the film | live |
| the five CLOSER conversations, one per avatar, each with its own words and answers (`own` · `fnd` · `lrn` · `ent` · `agc`) | live — each: why they are here → the pains they tick → what they tried, said back → (their size) → the destination drawn from their answers → (the entrepreneur: the frameworks, each opened) → their concerns, each opened → the cart, and its hand-holding beside it |
| the front end: no done-with-you before payment, except the owner's retainer | live |
| the plans page reading what the door sends (the agency's plan first for `tier=meta`, the seats) | owed |
| the door's answers carried into the checkout's metadata | owed |
| the one-time offer page after payment, and the no-thanks step | owed — its offers per avatar wait on §6 |
| the order bump | owed — its add-on waits on §6 |
| the weekly letter, and the frameworks and manuals sent on the learner's sign-up | owed — the sign-up is live; what it sends is not made |
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
- the community's home (it is free with JobWorld; where it lives comes later); the retainer's terms for the B2B engagement
- THE CART'S OFFERS (law 1 — the offers are *USER*'s): the order bump's add-on · the founder's and the learner's one-time
  offer after payment · the downsell after a no thanks

## 7. The order of work

1. the door as glass over the film — now
2. each avatar's CLOSER conversation, drafted with the skill, ending at the cart — done
3. the cart funnel (§4): the plans page reading what the door sends · the answers into the checkout · the one-time
   offer page after payment · the order bump — each offer once *USER* names it
4. the hand-holding behind the cart: the community's home, the weekly letter and what the sign-up sends, the retainer's
   terms
5. pricing and the dashboard in the theme
6. the pricing pass, and Stripe live
7. the VSLs, when the twin exists
