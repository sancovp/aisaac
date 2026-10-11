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
- **Every conversation SHOWS that avatar its own CLOSER process** (the `hormozi-closer` skill). A visitor comes because
  they want something and do not yet know how to get it: **Clarify** sets out that avatar's options for what they are
  after, and they pick · **Label** sets out what must be going on, and they name themselves in it · **Overview** what they
  have tried, said back · **Sell the vacation**, drawn from their answers · **Explain** each concern · **Reinforce** at the
  cart, where their offer is. This is the shape of each conversation; the words on each screen are written for that
  avatar. **The survey only asks which one they are** (the SCREENING, `b2b-bootcamp/SCREENING-framework.md`), and each
  conversation opens on the choice they made. **Two moves from the bootcamp carry the close:** where it ends if nothing
  changes — each pain they ticked, carried to its end and left with them (DOCTOR's Consequences,
  `b2b-bootcamp/DOCTOR-framework.md`) — and **the trick**: the expectation set ("you expect another AI tool"), then the
  literal thing — the real JobWorld working on screen — so the meaning snaps into place (`b2b-bootcamp/JOKE-MEDICINE-structure.md`).
  Then where they will be, their doubts answered, and the offer. Nothing on any screen is false: no invented number, no
  invented scarcity. **The door TELLS them; it never asks.** Every screen is a statement in the second person that presupposes
  where they are and where they are going, and the visitor only recognises themselves in it — a hypnotic experience,
  never a questionnaire.
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
| 1 **I need AI for my business** — the owner (B2B) | the business they run and what is eating their time | each feature as the pain it ends ("do you have this?" → "JobWorld does it like this"), the list, N seats (a seat = one JobWorld per person in the org chart, `application/jobworld/DESIGN.md` §6) | JobWorld with those departments and N seats | a B2B engagement on a retainer |
| 2 **I want to start an AI-native business** — the founder | where they are starting from: an idea · a skill and no idea yet · only the will · leaving a job | JobWorld helps them make an idea it can run on its own, or helps them run the parts it cannot; one seat, the AI CEO and its departments as the team from day one | JobWorld, one seat, their new company in it | the community, free with JobWorld |
| 3 **I want to learn how to use AI** — the learner | what for: their business · their work · building agents | where AI stops working for them, how they learned so far; JobWorld carries the Claude compilation skills and teaches AI by doing it with them | JobWorld | the free sign-up (law 13's consent boxes): the weekly letter — a version of the newsletter on what each change means for people using JobWorld — every framework and manual, and the community where they share and help each other |
| 4 **I want to learn to sell, market or run my operations** — the entrepreneur who wants to grow | which of the three, and where it stalls | "you need frameworks — here they are": the B2B bootcamp's frameworks (PSA · SCREENING · CLINIC · DOCTOR · LIFE · MEDICINE · OFFERS, in `/bootcamp`'s words, the whole page linked), for entrepreneurs to learn from — "and every one runs inside JobWorld too: want that?" | JobWorld, running those frameworks with them and for them | the community, free with JobWorld |
| 5 **I want to sell AI to my clients** — the agency | what they do | what is hard now (churn · delivery that does not scale · another vendor's name · custom setups · thin recurring revenue), how many clients they would put on it | the agency level = **Meta Business** (`sanctuary-revolution-alpha/application/lamai-saas/DESIGN.md` §2), on sale on the plans page: JobWorld under their own name, logo, colours, domain and email; each client its own business under them; their clients paid in their own Stripe, one monthly bill to us | the community, free with JobWorld |

**How a feature is said** (avatars 1 and 5): GoHighLevel's public funnel is the reference for its shape only — *it does
x, y, z: what you need for your business and to sell to your clients* — our positioning differs, its words are never
copied, GHL is never named. The features come from JobWorld's own design, never invented on the site.

**THE OFFERS — one per avatar, and JobWorld is the main product of every one** (no other product is offered; HealthWorld
and PromptWorld are not part of the offers). Each is a Grand Slam offer built from the marketing skills: a MAGIC name, its
core (the avatar's JobWorld — the client JobWorld, or for the agency the agency JobWorld, `application/jobworld/DESIGN.md`
§2), and bonuses named for their benefit, each answering an objection its CLOSER labelled. Prices, a guarantee and
scarcity are added when they exist. The words are the `OFFERS` table in `tools/build_door.py`.

| avatar | the offer |
|---|---|
| owner | The AI CEO Install for Business Owners |
| founder | The AI-Native Company Launch |
| learner | The Learn-AI-by-Doing Fast Track |
| entrepreneur | The Sell, Market &amp; Operate Accelerator |
| agency | The White-Label AI Agency Launch |

## 4. The cart — a direct-response funnel, and everything in it is JobWorld

**EVERY OFFER IS JOBWORLD, OR MORE ON JOBWORLD.** The front end is a JobWorld plan; the order bump, the one-time offer and
the downsell can only put more on JobWorld (more seats, the agency level) — never a separate product, a course, a
session or a service bundled in. **The one exception is the B2B start:** a business may begin with the retainer — *USER*
works inside the business — and is sold into JobWorld from inside. A visitor sees an offer only at the stage that earns
it.

```
the CLOSER ─▶ 1 FRONT END ─▶ 2 CHECKOUT ─▶ 3 ONE-TIME OFFER ─▶ 4 NO THANKS ─▶ 5 IN
              a JobWorld      Stripe, its    after payment:         a smaller step   the dashboard,
              plan            order bump:    more on JobWorld       on JobWorld,     the community
              (B2B: or the    more on                               or none
              retainer)       JobWorld
```

1. **Front end:** the JobWorld plan the conversation sold (Single Business; the agency's Meta Business), at
   `app.iwantaiformybusiness.com/pricing`, the conversation's answers riding in as the query (`from=door`, `avatar`,
   `seats`, `clients`, `tier=meta`). **The B2B owner** may start with the retainer instead (Set it up with Isaac, a
   call) — and is sold into JobWorld from inside the business. The learner's free sign-up is the lead magnet beside its
   cart; the community is free with JobWorld.
2. **Checkout and its order bump:** more on JobWorld, ticked on the checkout.
3. **The one-time offer, after payment:** more on JobWorld, shown once, on a page between the checkout's return and the
   dashboard; it knows the avatar because the door's answers ride into the checkout's metadata.
4. **No thanks** → a smaller step on JobWorld, or straight in.
5. **In:** the dashboard and the community.

**Each cart shows its offer:** under the cards, *What you get* — the lines known to go in that avatar's JobWorld (the
`OFFER` table in `tools/build_door.py`), then the size their answers chose. Lines are added as each offer is built up.

What goes on JobWorld: **seats** (one JobWorld per person in the org chart, `application/jobworld/DESIGN.md` §6) and **the
agency level** (Meta Business — the white label, each client its own business under them). Each step, per avatar:

| avatar | front end | order bump | one-time offer, after payment | no thanks → |
|---|---|---|---|---|
| owner (B2B) | JobWorld with the seats they chose · or the retainer first | +1 seat — for whoever runs the busiest department | a seat for everyone on the team they told the door about | +1 seat instead of the whole team |
| founder | JobWorld, one seat | +1 seat — for a partner | the agency level — start the business as a JobWorld agency | straight in |
| learner | JobWorld | — | — | straight in |
| entrepreneur | JobWorld | +1 seat — for whoever sells or delivers | the agency level — sell what the frameworks do, running in JobWorld, to clients | +1 seat |
| agency | JobWorld Agency | +1 seat — on their own business | — | JobWorld for your business — run it in their own business first |

A seat's price comes with the pricing pass (§6); until then the seat is sold in Stripe's test mode at the direction's
~$20 a month.

## 5. One look for the rest

Everything past the door — the JobWorld page, the bootcamp, the accounts app (sign-in, sign-up, pricing, the dashboard) —
wears the site's Blueprint System (RULE 02); every primary button carries the arm.

| surface | state |
|---|---|
| the door, glass over the film | live |
| the five CLOSER conversations, one per avatar, each with its own words and answers (`own` · `fnd` · `lrn` · `ent` · `agc`) | live — each: why they are here → the pains they tick → what they tried, said back → (their size) → the destination drawn from their answers → (the entrepreneur: the frameworks, each opened) → their concerns, each opened → the cart, and its hand-holding beside it |
| the front end: JobWorld only; the owner may start with the retainer | live |
| the plans page reading what the door sends (the agency's plan first for `tier=meta`, the seats) | owed |
| the door's answers carried into the checkout's metadata | owed |
| the one-time offer page after payment, and the no-thanks step (§4's table) | owed — next |
| the order bump (§4's table) | owed — next |
| the weekly letter, and the frameworks and manuals sent on the learner's sign-up | another agent's lane — the door owns only the sign-up, which is live |
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
- whether anything beyond seats and the agency level goes on JobWorld

## 7. The order of work

1. the door as glass over the film — now
2. each avatar's CLOSER conversation, drafted with the skill, ending at the cart — done
3. the cart funnel (§4): the plans page reading what the door sends · the answers into the checkout · the one-time
   offer page after payment · the order bump — each offer once *USER* names it
4. the hand-holding behind the cart: the community's home, the retainer's terms (the weekly letter and what the
   sign-up sends are another agent's lane)
5. pricing and the dashboard in the theme
6. the pricing pass, and Stripe live
7. the VSLs, when the twin exists
