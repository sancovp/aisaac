# CHANGELOG — the site

What changed, what it replaced or corrected, and why. Appended, never edited; never served (`.assetsignore`).



## 2026-10-11 — the survey only asks which one they are; each funnel opens on the choice

- Isaac ruled: the survey asks which one they are and nothing else; every funnel then starts with the thing they chose.
  The first screen is now "Which one are you?" and the five choices, with no pill, no line and no sub-line on the cards;
  each funnel's first screen is headed with the visitor's own choice ("I need JobWorld for my business." …).
- Files: `tools/build_door.py` → `door.html`.

## 2026-10-11 — the door's first screen says plainly why they came

- Isaac could not follow "Five kinds of people walk through this door. One of them is you." Replaced with "You came here
  to get something done with AI. Start from where you are."; the learner's "And this is where you want it." with "Start
  with where you want it working." Every screen's text was then read in order as a visitor.
- Files: `tools/build_door.py` → `door.html`.

## 2026-10-11 — the door tells; it never asks

- Isaac ruled: the door is a hypnotic experience — it tells the visitor, and never asks the human. Every screen heading
  was a question ("What do you want most right now?", "Anything holding you back?" …); all are now second-person
  statements that presuppose where they are ("You built a business, and it still runs through you.", "Every owner has
  the same few doubts.") and the visitor recognises themselves in the cards. §1 states it.
- Files: `tools/build_door.py` → `door.html` · `docs/the-door.md`.

## 2026-10-11 — Clarify and Label put back: the ruling was the process, not the copy

- Isaac's ruling describes why a visitor comes (they want something and do not yet know how) and what Clarify and Label
  do; it was an instruction at the level of the process, and the entry above printed it on the screens as copy
  ("I don't know how to…", "Here is what must be happening"). Reverted to the screens before it. The door doc and the
  `hormozi-closer` skill now state the process and say the words are written per avatar.
- Files: `tools/build_door.py` → `door.html` · `docs/the-door.md` · `.claude/skills/hormozi-closer/SKILL.md` (+ copy).

## 2026-10-11 — Clarify opens on "I don't know how to…"; Label shows what must be happening

- Isaac ruled: each self-selected avatar is shown its exact CLOSER process — they come because they do not know how to
  get what they want; Clarify sets out the options, and they label themselves.
- All five Clarify screens now read "I don't know how to…" with that avatar's options (the owner's time back, growth
  without hiring…; the founder's idea into a business…; the learner's AI in business, work, agents; the entrepreneur's
  sell, market, run, all three; the agency's deliver AI, scale delivery, own product, keep clients). All five Label
  screens read "Here is what must be happening. Which is you?". Replaced: Clarify asked what they want most, where they
  start, what for, what to get better at, or what they do.
- Files: `tools/build_door.py` → `door.html` · `docs/the-door.md` · `.claude/skills/hormozi-closer/SKILL.md` (and its
  copy in `~/.claude/skills`).

## 2026-10-11 — five offers built from the marketing skills, JobWorld the main product of each

- Isaac ruled: JobWorld is the main product that appears in every offer; HealthWorld and PromptWorld are not part of the
  offers; offers are built from the marketing skills (every Hormozi and Expert Secrets skill read whole).
- Each cart now carries a Grand Slam offer: a MAGIC name (avatar + goal + container), a core that leads with JobWorld,
  and bonuses named for their benefit, each answering an objection the conversation labelled — all things JobWorld does
  or comes with. Replaced: the product-label names ("JobWorld for your business" …) and a plain checklist.
- Files: `tools/build_door.py` → `door.html` · `style.css` · `docs/the-door.md`.

## 2026-10-11 — the five offer names taken back down

- Isaac ruled the names were wrong: offers are named and built from the marketing skills (every Hormozi and Expert
  Secrets skill), not as product labels. The carts say "Get JobWorld" again and §3's offers table is removed until each
  avatar's product is confirmed and its offer is built (MAGIC name, stack, guarantee).
- Files: `tools/build_door.py` → `door.html` · `docs/the-door.md`.

## 2026-10-11 — one product-offer per avatar; no vendor name in the public code

- Isaac ruled: the products made are each for a specific avatar — put them together into offers accordingly, so each
  conversation is the CLOSER that sells its avatar's offer; and no comment in the public code names the CRM vendor.
- The door's carts now name five offers, each a JobWorld (the client tier loaded per avatar; the agency tier for the
  agency): JobWorld for your business · for your new company · with my AI skills · with the frameworks · JobWorld Agency.
  Before, every cart said "Get JobWorld" (the agency's "Get the agency level"). §3 carries the table.
- `lib/ghl.js` → `lib/crm.js` (`CrmError`), its importers and log labels, and the comments in it, the two relay functions,
  `lib/relay.js` and `framework.html` no longer name the vendor. The Worker secret keeps its name (renaming it needs its
  value set again).
- Files: `tools/build_door.py` → `door.html` · `docs/the-door.md` · `lib/crm.js` · `functions/api/{lead,stripe}.js` ·
  `lib/relay.js` · `framework.html`.

## 2026-10-11 — the cart's steps filled from the rule: seats and the agency level

- Isaac ruled the cart's offers are already decided by the rule (every offer is JobWorld or more on it) and are not to
  be asked for one by one. §4 now carries each avatar's front end, order bump, one-time offer and downsell, built only
  from seats and the agency level; the seat sells in Stripe test mode at the ~$20 direction until the pricing pass.
  Before, those steps were listed as open questions for Isaac.
- Files: `docs/the-door.md`.

## 2026-10-11 — each cart shows its offer

- Isaac ruled: put the base of each offer into every place it is known to go, now — he builds every offer up
  iteratively, all at once; what he says goes into the website as he says it, never held back until the whole is known.
- Each avatar's cart screen now carries *What you get*: the lines known to go in its JobWorld (the owner's departments
  and seats; the founder's one seat and the idea shaped with it; the learner's compilation skills, letter, frameworks and
  manuals; the entrepreneur's frameworks running inside; the agency's white label, clients under them and own Stripe;
  the community free for all), then the size their answers chose. Before, the cart showed only a one-line summary.
- Files: `tools/build_door.py` → `door.html` · `style.css` · `docs/the-door.md`.

## 2026-10-11 — every offer in the cart is JobWorld, or more on JobWorld

- Isaac: "i just told you the offers earlier in this conversation. They are all jobworld. you can ONLY put more things on
  jobworld. the only thing that is not ONLY jobworld plus more stuff is when they start b2b and i can sell them into
  jobworld after getting inside".
- Corrected: §4 said the one-time offer after payment was "this avatar's done-with-you" (the retainer, tailoring), and a
  draft money model in the conversation filled the bump, upsell and downsell from `pricing.html`'s older lineup (the
  Strategy Session, the School, Pre-built Automations, Custom Integrations). Now §4 states the bump, the one-time offer
  and the downsell can only put more on JobWorld (today: seats, the agency level); the B2B owner alone may start with
  the retainer and is sold into JobWorld from inside.
- Files: `docs/the-door.md` · `.claude/rules/00-SITE-CANON.md`.

## 2026-10-11 — the newsletter is another agent's lane

- Isaac: "another agent will handle the newsletter stuff btw". `docs/the-door.md` §5 and §7: the weekly letter and what
  the learner's sign-up sends leave the door's owed work; the door owns only the sign-up.

## 2026-10-11 — the cart is a direct-response funnel: no done-with-you before payment, except for the B2B owner

- Isaac: "i think the carts need to be figured out. there are some things they shouldnt see unless theyve already got a
  plan in their cart, already paid, etc. you know? classic direct marketing funnels. why sell them into a done with you
  before they buy it, etc. only the b2b goes straight to DWY (the retainer)".
- Replaced: every conversation's last screen offered done-with-you beside Get JobWorld (the entrepreneur's retainer
  call, the agency's tailoring call). Now only the owner (B2B) keeps the retainer there; the entrepreneur's and the
  agency's done-with-you move to the one-time offer after payment. `docs/the-door.md` §4 is the funnel: front end →
  checkout with its order bump → the one-time offer → no thanks → in. The offers at the bump, the founder's and learner's
  one-time offer, and the downsell are Isaac's (law 1), listed open.
- Files: `tools/build_door.py` → `door.html` · `docs/the-door.md` · `.claude/rules/00-SITE-CANON.md`.

## 2026-10-11 — the door's other four conversations: founder, learner, entrepreneur, agency

- Each of the five cards now opens its own CLOSER conversation (the `hormozi-closer` skill), every one ending at Get
  JobWorld. Before, cards 2 and 4 left for `/jobworld` and `/bootcamp`, and cards 3 and 5 ran short flows (what for →
  email; what do you do → tailored?).
- Isaac's answers, in his words: the community — "doesnt matter right now will be obvious later. sure could be included
  with jobworld/free"; the founder — "jobworld helps them make an idea that jobworld can do autonomously, or help them
  otherwise"; the learner — "they receive a version of the newsletter every week tailored to what it means for people
  using jobworld imo, and they receive all our frameworks and manuals and its a community for sharing and helping each
  other"; the agency level — "why dont you know what this is": it is LAMAI's Meta Business plan, already on sale.
- `door.js` keeps each conversation's answers under its own prefix and draws each destination and cart line from them;
  the cart carries `seats`, `clients`, `tier=meta`. Fixed on the way: an opened concern card turned its answer white on
  white under the pointer (hover inverted it); the door's backdrop film got player controls under reduced motion
  (`vsl.js` now skips a `data-backdrop` loop).
- Files: `tools/build_door.py` → `door.html` · `door.js` · `style.css` · `vsl.js` · `docs/the-door.md` ·
  `.claude/rules/00-SITE-CANON.md`.

## 2026-10-11 — the owner's CLOSER conversation (avatar 1), live in the door

What changed: card 1 ("I need JobWorld for my business") opens its own conversation in the glass panel, built with the
`hormozi-closer` skill: Clarify (what they want most) → Label (the pains they tick; each one something JobWorld does, from
its design) → Overview (what they tried, said back to them) → their team size (seats, one JobWorld per person) → Sell the
vacation (a screen drawn from their answers: each pain crossed out beside how JobWorld ends it, their seats) → Explain (five
concerns, each opening its answer — the JobWorld page's own "Where it stops") → Reinforce at the cart (Get JobWorld, carrying
the avatar and seats to the plans page; or set it up with Isaac on a retainer). `door.js` gains pick-many lists, concerns
that open in place, the destination and cart summaries, and dots sized to each conversation. Every word is a draft for the
owner to strike. Seen locally at 1440 and 390, every screen; the cart lands on `/pricing?from=door&avatar=owner&seats=…`.
Why — the owner's "ok go" to building each avatar's CLOSER, starting with the owner.
Files: `tools/build_door.py` · `door.html` · `door.js` · `style.css` · `docs/the-door.md` · the pages whose stylesheet version moved · this file.

## 2026-10-11 — the door is glass over the film; the model is self-select → each avatar's own CLOSER → one cart → hand-holding

What changed: `door.html` is the agents' film full screen with only the top bar and one glass panel holding the survey
cards (RULE 02 §13 names the door's own look). `docs/the-door.md` is rewritten to the model and the canon's door passage
with it: the avatar self-selects; each avatar gets its own sales conversation, the CLOSER process (the new
`hormozi-closer` skill); every one ends at the same cart — what that avatar needs inside JobWorld, the AI system that does
it with them and for them; then the hand-holding — the community for individuals, a B2B retainer for businesses. The
bootcamp is for entrepreneurs to learn from, inside avatar 4's conversation.
What it replaced: the door as a Blueprint card with the film beneath; a door doc and canon that read the cards as routes to
pages and the bootcamp as a sales-transformation page.
Why — the owner's words: "imo make the survey glass morphic over *just* the video you ahve there. nothing else on the
screen besides the top bar, the hero as glass morphic"; and: the avatars are never to be mashed together — each one
eventually leads to the same cart process, and the sales process is attuned to each … have the avatar self select.
THEN, for each one, clarify why they are there, label the pains, etc the CLOSER process … IT IS NOT ABOUT SELLING AI
TRANSFORMATION HERE. The b2b bootcamp is FOR ENTREPRENEURS to learn from."
Files: `tools/build_door.py` · `door.html` · `style.css` · `.claude/rules/02-STYLE.md` · `.claude/rules/00-SITE-CANON.md` ·
`docs/the-door.md` · `ai-transformation.html` · `jobworld.html` · `bootcamp.html` · the build scripts · this file.

## 2026-10-11 — the door as cards (the June survey's shape); card 4 to the B2B frameworks page, built at /bootcamp

What changed: the door is the question centered over a row of cards — an icon, a title, a line, "Enter →" — and every
sub-step is cards; the arm presses a card at its top edge (`arm.js`'s `data-arm-h`). Card 4 now lands on `bootcamp.html`
(`/bootcamp`), the B2B frameworks lifted whole from `framework.html`'s `#bootcamp` by `tools/build_bootcamp.py`, whose one
way on is JobWorld. The canon and `docs/the-door.md` say so, and that card 4 never goes to `framework.html`.
What it replaced: a list of buttons beside the film; card 4 pointing at `framework.html` — the DIY funnel — because no B2B
frameworks page existed and the one with "framework" in its name was taken without checking.
Why — the owner's words: "the survey should be different. should be cards. look how we had it on aisaac"; "why did you link
the *frameowkrs page* which is the DIY page instead of the b2b frameworks page?"
Files: `tools/build_door.py` · `door.html` · `door.js` · `tools/build_bootcamp.py` · `bootcamp.html` · `arm.js` · `style.css` ·
`worker.js` · `tools/style_qa.py` · `ai-transformation.html` · `tools/build_jobworld.py` · `jobworld.html` ·
`.claude/rules/00-SITE-CANON.md` · `docs/the-door.md` · this file.

## 2026-10-11 — THE DOOR is built and is the home

What changed: `tools/build_door.py` writes `door.html`; `door.js` runs it — one question ("Why are you here?"), five cards,
the learn-AI flow (what for → the email sign-up with the five consent boxes, the choice carried as `learn_for` → JobWorld),
the sell-JobWorld flow (what do you do → tailored? → Book a call, or the agency level at the app's pricing), step dots and
Back, the answers in `localStorage` (`twi_door`). Every option is pressed by the arm; each step slides in; the hero loop of
the films' agents sits beside it. The worker serves it at `/` (the landing page stays at `/ai-transformation`); the style
gate counts it as canon. `arm.js`'s link variant now stacks above its arm like a button does; each door card is its own
stack so the arm rises over the cards above. Seen locally at 1440 and 390 (no sideways scroll); style gate PASS.
What it replaced: the landing page at the home.
Why — the owner's words: "i was asking because im still not seeing the survey btw".
Files: `tools/build_door.py` · `door.html` · `door.js` · `style.css` · `worker.js` · `tools/style_qa.py` · `ai-transformation.html` ·
`tools/build_jobworld.py` · `jobworld.html` · `.claude/rules/00-SITE-CANON.md` · `docs/the-door.md` · this file.

## 2026-10-11 — every primary button carries the arm press: Get JobWorld and the funnel page's Book a call too

What changed: `arm.js` presses a link as well as a button (the replayed click follows it); `tools/build_jobworld.py` wraps
the funnel page's six primary buttons (Get JobWorld and Book a call in the top bar — mirrored — the hero and the close) and
loads `arm.js`; the landing page's `arm.js` version bumped. RULE 02 §8b: every primary button carries the arm, the door's
included; `docs/the-door.md` says so. Seen locally: the arm comes up, presses Get JobWorld, and the plans page opens.
Why — the owner's words: "dont miss the robot arm buttons."
Files: `arm.js` · `tools/build_jobworld.py` · `jobworld.html` · `ai-transformation.html` · `.claude/rules/02-STYLE.md` · `docs/the-door.md` · this file.

## 2026-10-11 — the JobWorld page is a funnel: Get JobWorld (the plans and the checkout) in the top bar, the hero and the close

What changed: `tools/build_jobworld.py` puts an ink Get JobWorld, to `app.iwantaiformybusiness.com/pricing` (the plans and
the Stripe checkout), in the top bar, the hero and the closing band, beside Book a call; the closing line no longer says
"No purchase". The canon's JobWorld paragraph, law 9's loop and `docs/the-door.md` say the page is a funnel a visitor buys
from. Prices stay in Stripe, never on the page.
What it replaced: a product page whose only actions were Book a call and Sign in — the canon had given it the landing
page's one-exit law, so nobody could subscribe from it.
Why — the owner's ruling: the funnel page was not a funnel — it led only to Sign in and Book a call; people must be able to
buy the application and subscribe from it.
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
