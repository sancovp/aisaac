# THE DOOR — the site's front: the survey, its five ways in, the JobWorld pipeline, one theme

The design of everything a visitor meets before they are a customer: the home (a survey), the part each answer opens,
the sales pipeline inside the JobWorld part, the loop between the product and the service, and the one look all of it
wears. The site canon (`.claude/rules/00-SITE-CANON.md` § WHAT IS PUBLIC, law 9, the source map's door row) states the
rulings as law; this document holds the whole design in one place. History: `CHANGELOG.md`.

## 1. What it is

**The home is a door, not a page that explains.** One short, very good-looking survey asks *why are you here* — in effect,
*which avatar are you* — and lets the visitor into the part they choose. It is the router back to everything, and every
way in ends at **JobWorld**, each by its own path.

## 2. The survey

- **One question, five cards — CARDS, as the June survey had them:** the question centered over a row of cards, each an
  icon, a title, one line and its call at the foot ("Enter →"); the sub-steps are cards too. The door stays short;
  anything longer belongs to the part a card opens.
- **Every transition is animated** with the site's own cast: THE ROBOT ARM (`arm.js`, source `docs/arm-press/`) and THE
  AGENTS of the films (the owner with the gold orb, the cyan agents, the black wires — `~/claude_code/video-aios/draw-the-box/`).
- **Its logic is the survey the site already had** — `git show 9b26f427:index.html` (2026-06-10): the cards in a modal, a
  qualification flow under one card (monthly revenue · what's eating your time · how soon), step dots and a back button,
  the answers kept in `localStorage` (`twi_qualify`), each result routing to its page, an email capture on the learning
  path. It has everything except the animations; it is re-drawn, not reinvented.
- **The way out is the same door** (law 9): its exits are the five parts and nothing else.

## 3. The five ways in — every one ends in JobWorld

| # | the card | where it goes |
|---|---|---|
| 1 | **I need [JobWorld's features] for my business** | the JobWorld part, by THE PIPELINE (§4) |
| 2 | **I want to start an AI-native business** | JobWorld |
| 3 | **I want to learn how to use AI** | "for…" → matched to the material and recommended → "I'll send you everything by email — sign up here" (a form with law 13's five consent boxes, posted to the relay) → JobWorld, which carries the Claude compilation skills and teaches AI itself |
| 4 | **I want to learn how to sell, market, or run my business operations** | THE B2B FRAMEWORKS PAGE — `/bootcamp` (the B2B bootcamp: PSA · SCREENING · CLINIC · DOCTOR · LIFE and the tools behind them; built by `tools/build_bootcamp.py`) → back to JobWorld, which does it for them. Never `framework.html`, the DIY funnel |
| 5 | **I want to sell JobWorld to my clients** | what do you do (the business, who its clients are) → do you want it tailored for you? → **book a call**, or **buy the agency level** — LAMAI's Meta Business, the white label (their own name, mark and colours on JobWorld for their clients; `sanctuary-revolution-alpha/application/lamai-saas/DESIGN.md` §2) |

## 4. The pipeline — the JobWorld part's own flow (card 1, and card 5's agency version)

A sales pipeline that asks, qualifies, and walks every feature **socratically**:

1. **What do you need?** — qualify the business (the old survey's questions are the start: revenue · what is eating the
   time · how soon).
2. **Each feature, as the problem it solves** — *"so, do you have this problem?"* → *"JobWorld solves it like this."*
3. **The list** — *"do you have any of these? select them"* → *"JobWorld solves all of those."*
4. **The size** — *"you need N seats"* — a seat is a JobWorld (one per person in the org chart: CEO · Manager · Worker;
   `sanctuary-revolution-alpha/application/jobworld/DESIGN.md` §6), so N is counted from their answers, never a slogan.
5. **The help** — *"do you want help integrating it with your business?"* → the CONCIERGE PAGE (§5). For card 5 the same
   step is *"do you want it tailored for you?"* → book a call or the agency level.

**THE FEATURES ARE WALKED IN THIS FORMAT** — problem → "JobWorld solves it like this" — for an owner's own business and
for an agency selling to its clients. Each feature is one row in the shape the site already uses for a leak tree:
*the numbers · but · before · so we · after* (RULE 02 §11) — *but* and *before* are the problem, *so we* is "JobWorld
solves it like this", *after* is the dream.

**WHERE THE FEATURES COME FROM:** JobWorld's own design (`application/jobworld/DESIGN.md`) — the console, the CEO and its
departments, the workflows on the calendar, the hot pages, the repository, the seats, the white label — never invented
on the site.

**HOW A FEATURE IS SAID — the reference:** GoHighLevel's own public funnel (its sales pages: *it does x, y, z — what you
need for your business, and to sell to your clients*). Read for its SHAPE only:
- its positioning sells GHL's SaaS; ours is a company with an AI CEO in the chair, signed in with the owner's own AI,
  nothing reaching the world until the owner says so;
- its words are never copied, and GHL is never named on a page;
- what it sells agencies, we have too: the white label (Meta Business).

## 5. The loop between the product and the service

- **THE FUNNEL PAGE** — the JobWorld page (`jobworld.html`, built by `tools/build_jobworld.py`), the main page of
  `app.iwantaiformybusiness.com` (live at its root). It is a funnel: a visitor can BUY from it. Its exits: Get JobWorld (the
  plans and the Stripe checkout, `app.iwantaiformybusiness.com/pricing`) · Sign in · Book a call · the concierge page.
- **THE CONCIERGE PAGE** — the coaching / done-with-you service: the business worked with *USER*. Advertised from the
  pipeline's help step and from the funnel page. Its exits: Book a call · the funnel page · sign-up.
- **THE ACCOUNTS APP** (LAMAI — sign-in, sign-up, pricing, the dashboard) leads back to the funnel page and nowhere else.
- A visitor can only move between these pages and their buttons.

## 6. One theme

Everything a visitor or owner sees wears the site's Blueprint System (RULE 02): white paper, black ink, Geist and Geist
Mono, outlined cards with nodes on their dividers, the glass top bar, red only for Book a call. Every primary button —
Book a call, Get JobWorld, the door's cards — carries THE ARM PRESS (RULE 02 §8b). The accounts app is
served the site's own `style.css`; it never has a look of its own.

| surface | in the theme |
|---|---|
| the JobWorld page at the app's root | live |
| the sign-in and sign-up | built, in review (PR #1599), deployed by hand after it merges |
| pricing and the dashboard | owed |
| the door, the parts, the concierge page | owed — built in the theme from the start |

## 7. The VSLs

Each part opens with a VSL played by *USER*'s AVATAR DIGITAL TWIN, with the door's animations. ASPIRATIONAL until the twin
exists; until then a part opens on its page as it is.

## 8. Open — *USER*'s

- the twin, and the VSL of each part
- the concierge page's source: the existing service page reframed, or a new offer (the nearest frozen one is
  `pricing.html`'s "Retainer — Your AI CTO") — and its address
- THE PRICING PASS, later: the seat's price and the plans' — the direction is down, toward something like $297/mo plus about $20
  a seat, once a seat's cost and the SaaS's cost are measured (`sanctuary-revolution-alpha/application/lamai-saas` board § OPEN);
  until then the plans in Stripe stand, and the shape and the words are built without waiting on the numbers
- the recommendations card 3 matches people to

## 9. The order of work

1. the themed sign-in lands and is deployed — DONE
2. THE DOOR — DONE as the home (`door.html`, `tools/build_door.py`, `door.js`): five cards, the two flows, the arm on every
   option, every step sliding in, the films' agents beside it; the agents' own animations on each transition come next
3. THE PIPELINE in the JobWorld part — JobWorld's feature list in the leak-tree format, GHL's funnel read for its shape
4. the concierge page and the buttons that close the loop
5. card 3's email sign-up and card 4's route through the frameworks
6. card 5's tailoring flow and the agency level's checkout
7. pricing and the dashboard in the theme
8. the VSLs, when the twin exists
