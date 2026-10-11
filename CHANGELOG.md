# CHANGELOG — the site

What changed, what it replaced or corrected, and why. Appended, never edited; never served (`.assetsignore`).

## 2026-10-11 — the JobWorld page is a funnel: Get JobWorld (the plans and the checkout) in the top bar, the hero and the close

What changed: `tools/build_jobworld.py` puts an ink Get JobWorld, to `app.iwantaiformybusiness.com/pricing` (the plans and
the Stripe checkout), in the top bar, the hero and the closing band, beside Book a call; the closing line no longer says
"No purchase". The canon's JobWorld paragraph, law 9's loop and `docs/the-door.md` say the page is a funnel a visitor buys
from. Prices stay in Stripe, never on the page.
What it replaced: a product page whose only actions were Book a call and Sign in — the canon had given it the landing
page's one-exit law, so nobody could subscribe from it.
Why — the owner's words: "the funnel page somehow is not a funnel, somehow goes to SIGN IN and BOOK A CALL … why doesnt it
go to SIGN IN or let people fucking BUY THE FUCKING APPLICATION!?!!? … why cant they subscribe!?"
Files: `tools/build_jobworld.py` · `jobworld.html` · `.claude/rules/00-SITE-CANON.md` · `docs/the-door.md` · this file.

## 2026-10-11 — `docs/the-door.md`: the door's whole design in one document

What changed: the survey, its five ways in, the JobWorld pipeline (features walked socratically in the leak-tree shape, GHL's funnel as the reference for its shape only), the loop between the product and the service, the one theme, the VSLs, what is open and the order of work — gathered into `docs/the-door.md`; the source map's door row points at it.
Why — the owner asked for the information gathered into a doc.
Files: `docs/the-door.md` · `.claude/rules/00-SITE-CANON.md` · this file.

## 2026-10-11 — THE DOOR's fifth card (sell JobWorld to my clients → tailor → book or the agency level); the features walked in the pipeline's format

What changed: § WHAT IS PUBLIC adds the fifth card — "I want to sell JobWorld to my clients" → what do you do → do you want
me to tailor it → book a call or buy the agency level (LAMAI's Meta Business, the white label) — and states that JobWorld's
features are walked in the same socratic format (problem → "JobWorld solves it like this"), for the owner and for the
agency, with GoHighLevel's public funnel as the reference for how a feature is said, its shape only: our positioning
differs, its words are never copied, GHL is never named.
Why — the owner's words: "we also will need to do the SAME format for the jobworld features themselves. you can reference
the GHL funnel itself (ghl's funnel) even though that is about selling THEIR SAAS … Just understand our positioning is
different. But we *DO* have white label. We do also need to ask "I want to sell JobWorld to my clients" -> what do you do
etc -> do you want me to tailor it for you? -> book with me or buy agency level."
Files: `.claude/rules/00-SITE-CANON.md` · this file.

## 2026-10-11 — THE DOOR's cards: four ways in, every one routing to JobWorld; the sales pipeline lives in the JobWorld part

What changed: § WHAT IS PUBLIC names the door's four cards in the owner's words and each route — the features card into a
socratic sales pipeline (features as the problems they solve, the list, N seats, "help integrating?" where the concierge
page is advertised), the AI-native-business card, the learn-AI card (matched, emailed, signed up — JobWorld teaches AI
with the owner's Claude compilation skills), the sell/market/run card (the frameworks, then back to JobWorld). The door stays
one question and one card; the pipeline is the part's own flow. OPEN narrowed to the twin, the VSLs, the feature→problem
list (JobWorld's) and the seat's price.
Why — the owner's words: "the questions can just be: I need [jobworld's features] for my business (goes to JW but a special
way where we ask them questions, qualify what they need, lead them thru all the features, essentially a sales pipeline …),
I want to start an AI native business (goes to JW), I want to learn how to use AI (then goes "for..." and matches them to
my stuff and recommends it, i will send you an email with everything just sign up here…) … jobworld has my claude
compilation skills, it can teahc them AI too … so yeah, all these route to JW in different ways, and another one is "i
want to learn how to sell, market, or run my business operations" and that goes to the frameworks (DOCTOR etc) and goes
back to JW (it does it for you)".
Files: `.claude/rules/00-SITE-CANON.md` · this file.

## 2026-10-11 — THE DOOR: the home is a short, beautiful survey — why are you here, which avatar — animated with the arm and the films' agents, each part opening with a VSL

What changed: `00-SITE-CANON.md` § WHAT IS PUBLIC states the home as THE DOOR — a survey in the Blueprint System, every
transition animated with the robot arm and the films' characters, its logic taken from the survey the site had on
2026-06-10 (`9b26f427`), each self-selected part opening with a VSL played by the owner's digital twin (aspirational
until the twin exists); law 9 names the door's exits; the source map has the door's row. The presented page stands at
the home until the door is built.
What it replaced: the "engine door" at `index.html` (two rendering engines, "three ways down") and the landing page as the
home.
Why — the owner's words: "the home should just be literally a short very nice looking survey that uses our agent guys from
the video and the robot arm we put in, and it should just be an awesome little survey that is like: why are you here,
which avatar are you (essentially). We made one of these for the aisaac site a while ago, its logic probably could be
looked at here for reference it probably has everything already except the cool animations. So, then we should animate
each transition of the survey and with robot arms and agent anims, and then let them in to the part they self-select for,
each one opens with a VSL (in the final version) and has great animations... etc. using my avatar digital twin which
we're gonna have done soon but isnt ready yet."
Files: `.claude/rules/00-SITE-CANON.md` · this file.

## 2026-10-11 — THE FRONT LOOP: one theme, the funnel on the main page, a concierge page advertised from it, the SaaS advertised back

What changed: `00-SITE-CANON.md` § WHAT IS PUBLIC states the front loop — the funnel page (`jobworld.html`, the main page
of `app.iwantaiformybusiness.com`) advertises the concierge page (the coaching, done-with-you service), the concierge
page advertises the SaaS back, and a visitor moves only between them; every page the accounts app shows wears this
site's Blueprint System; law 9 names the loop's exits. The concierge page's offer source is OPEN (none is written; the
candidate is `pricing.html`'s "Retainer — Your AI CTO").
What it replaced: the accounts app's pages in the Next.js starter's look; the JobWorld page as the app's root with
nothing advertised beside it.
Why — the owner's words: "if both are ours the styles/theme needs to be unified to ours pls and funnel site goes up on
the main (funnel) page, the coaching/DWY concierge service page gets made something that gets *advertised* on the
funnel page, and the SaaS gets cross-advertised on the coaching page, so that they can only go back and forth between
those and their buttons".
Files: `.claude/rules/00-SITE-CANON.md` · this file · `.assetsignore`.
