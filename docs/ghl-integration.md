# GoHighLevel — what it gives us, what we keep, and how they connect

REFERENCE DETAIL — READ when anything touches GoHighLevel (GHL), the relay's writes into it, or where a piece of
business logic should live. NOT deprecated, NOT skippable. The law it serves is `.claude/rules/00-SITE-CANON.md`
§ HOSTING AND AUTOMATIONS; the payment side is `docs/stripe-payments.md`; the HOW of the Worker is the
`cloudflare-site` skill; the vendor facts (plans, prices, what the API can do) are the business-runtime project's
`research/ghl.md` (§ WHAT THE API EXPOSES).

**Status:** ① the lead and ② the payment are BUILT (`lib/ghl.js`, called by `functions/api/lead.js` and
`functions/api/stripe.js`) and proven against the real sub-account with test records, which were then deleted. ③ Cal.com
and ④ GHL's outbound events are NOT BUILT. The text to the lead and the ring-you-first call are not built: they wait on
a phone number and the A2P registration. The GHL sub-account is "Ribcage Solutions" (pipeline "TWI Sales", 8 contact
fields); the hand-built workflow "Website Lead Intake" there is not called by anything and can stay off.

## 1. The split — who is responsible for what

| GHL gives us (the CRM and the reach) | We keep ourselves (the brain and the glue) | Comes from elsewhere |
|---|---|---|
| people: contacts, notes, tags, custom fields | the website (Cloudflare Worker + static files) | **Stripe** — the money, the payment links, the payment webhook |
| deals: pipeline "TWI Sales" — New lead → Booked → Showed → Proposal → Won (Lost = a status) | **the relay** — the one server every form and payment passes through | **Cal.com** — today's booking calendar (GHL has its own; which one wins is OPEN) |
| reach: a phone number, texts, calls, email, reminders, missed-call text-back, review requests | partner attribution: `?ref=` code kept 90 days, carried to the contact and to Stripe | **the phone carrier** — through GHL; texting needs the A2P registration |
| the ring-you-first call to a new lead (a workflow step — the one thing with no API) | consent records: what a visitor agreed to, when, which wording (`consent_version`) | **ElevenLabs / YouTube** — the voice and the films |
| calendars, forms, surveys, email sequences | the offer, its prices, its copy — frozen, Isaac's only | **HighLevel affiliate program** — commission on the agencies we refer |
| GHL's own AI chat and voice (a template we can sell) | the agents and the runtime that do the work (SOMA, JobWorld) — GHL is their commodity surface | |
| SaaS Mode — sells a white-label account to a client, creates the sub-account, rebills usage at our markup | commission payouts to partners — by hand, monthly, from a task the relay creates | |
| snapshots — a configured account others can be given | the decisions: what happens when, and why | |

**The rule under it:** the visual builders (workflows, funnels, page layouts) have no write API — GHL's API can
list workflows, never create one. So **anything that must be tested, versioned and changed quickly is code in the
relay; anything that only GHL can do (the ring-you-first call, SaaS billing) is a workflow built once by hand and
started by the relay.**

## 2. The connections — what flows where

```mermaid
flowchart TB
  classDef site fill:#e3f2fd,stroke:#1565c0;
  classDef ghl fill:#ede7f6,stroke:#4527a0;
  classDef ext fill:#fff8e1,stroke:#ff8f00,stroke-dasharray:4 3;
  classDef run fill:#e8f5e9,stroke:#2e7d32;

  subgraph SITE["OUR SIDE — Cloudflare"]
    PAGE["the site — forms, ref.js, capture.js"]:::site
    RELAY["THE RELAY — /api/lead · /api/stripe · /api/cal · /api/ghl"]:::site
  end
  subgraph EXT["ELSEWHERE — ends at the seam"]
    STRIPE["Stripe — payment links + webhook"]:::ext
    CAL["Cal.com — the booking calendar"]:::ext
  end
  subgraph GHL["GOHIGHLEVEL — sub-account Ribcage Solutions"]
    CRM["contacts · deals · custom fields · tasks"]:::ghl
    REACH["phone number · texts · email · the ring-you-first call"]:::ghl
    HOOKS["GHL's outbound events"]:::ghl
  end
  subgraph RUN["THE RUNTIME — SOMA · JobWorld agents"]
    AGENTS["agents: read and write the CRM through the API"]:::run
  end

  PAGE -- "① a lead" --> RELAY
  STRIPE -- "② a payment / refund" --> RELAY
  CAL -- "③ a booking, a no-show" --> RELAY
  RELAY -- "writes through GHL's API (token)" --> CRM
  RELAY -- "sends a text / starts the call workflow" --> REACH
  HOOKS -- "④ a reply, a stage change" --> RELAY
  CRM --> HOOKS
  AGENTS -- "API" --> CRM
  RELAY -- "⑤ an event the agents act on" --> AGENTS
```

| # | event | who sends it | what the relay does | what lands in GHL |
|---|---|---|---|---|
| ① BUILT | a visitor submits a form | the site → `/api/lead` | drops bots and bad emails, labels the lead (form, page, partner), keeps the consent record | **upsert contact** (partner code, form, revenue, focus, page, consent record + version) · **create the deal** at New lead · a note · a task "Call new lead now" for Isaac, due in 2 minutes · *(not built yet: **the text and the ring-you-first call, only if a consent record and a phone are present**)* |
| ② BUILT | a payment or a refund | Stripe → `/api/stripe` (signed, 5-minute window) | reads `payment_id`, `billing_reason`, `ref` | **find the contact by email** (none → a task "unmatched payment") · skip if `last_payment_id` already equals this `payment_id` · save it · **deal → Won** · a partner code present and it is the first payment (`subscription_create` / `checkout`, never `subscription_cycle`) → a task "pay <partner> $1,000" · a refund → a task to cancel an unpaid commission |
| ③ | a call is booked, or missed | Cal.com webhook → `/api/cal` — **NOT BUILT** | maps booking → the contact by email | deal → **Booked**; after the call **Showed**; a no-show starts the no-show follow-up |
| ④ | the lead replies, or a deal moves | GHL's outbound events → `/api/ghl` — **NOT BUILT; whether GHL charges for these is unverified** (`research/ghl.md` Q9) | verifies the call is GHL's, routes it | tells the agents, or updates the site's own records |
| ⑤ | anything the agents should act on | the relay → the runtime | forwards the event | the agents write back through the API |

**What each form is** (`intent`, labelled `form` on the contact): `call` and `partner-referral` — a business that may buy: contact, a deal at New lead, a note, the call task · `partner-apply` — an agency applying: contact tagged `partner`, a note, a "Review partner application" task, no deal, and the code it typed is not stored as an attribution · `framework` and `community-waitlist` — a free opt-in: contact with a tag and a note, no deal, no task.

**The keys that tie the systems together** (a missing key is a broken link, never a guess):

| key | joins | rule |
|---|---|---|
| the contact's **email** | a payer, a booker and a lead are the same person | the only match; no email → a task for Isaac, never a duplicate contact |
| **`payment_id`** | a checkout and its invoice — one sale arrives twice | saved on the contact as `last_payment_id`; a second arrival stops |
| the **partner code** (`ref`) | the lead → the contact → Stripe's `client_reference_id` → the commission | stored on the contact as `partner_code`; empty means no partner |
| the **consent record + version** | a text or a call → the wording the visitor saw | no record, no text and no call |

## 3. What GHL's API can and cannot do (the boundary the design is drawn around)

VERIFIED 2026-09-28 · GHL's official OpenAPI specs (576 operations, 41 areas — full list in `research/ghl.md`).
**Writable:** contacts, notes, tags, tasks (with a full due timestamp), deals and their Won/Lost status, custom
fields, texts and email, phone-number purchase, sub-accounts, SaaS, users, blog posts, media, custom menu links,
redirects. **Not writable:** workflows (list only), funnel and website pages (list only), snapshots (a share link
only — loading one is done in the app). A hand-built workflow can be started for a contact:
`POST /contacts/{contactId}/workflow/{workflowId}`.

## 4. What is needed to build it

| need | who | state |
|---|---|---|
| a Private Integration Token for the sub-account | Isaac created it (all scopes — narrow it to contacts, opportunities, conversations messages, custom fields once things settle); it lives only in the Worker's secret `GHL_TOKEN` and `.dev.vars` | ✅ |
| a phone number in the sub-account | Isaac buys it | ⏸ |
| the A2P registration (IRS CP 575 emailed to GHL's team) | Isaac | ⏸ |
| the ring-you-first call workflow, built once | Isaac by hand, or with GHL's assistant | ⏸ |
| the relay's GHL module (`lib/ghl.js`) + the payment and lead handlers | an agent | ✅ |
| Cal.com → relay | an agent, after the calendar question below | ⏸ |

**Open for Isaac:** keep Cal.com or move booking into GHL's calendar · whether the hand-built workflow "Website
Lead Intake" is switched off once the relay writes to GHL directly.

## 6. The plan — how an AI reaches everything in GHL, and the order of work

**The goal (Isaac's):** an AI agent has ACCESS to everything in GHL, so nothing waits on him clicking. GHL splits into three
layers with three different doors:

| layer | the door | state |
|---|---|---|
| **DATA** — contacts, deals, tasks, texts, email, fields, calendars, invoices, products (≈570 API operations) | the public API with a sub-account token (`GHL_TOKEN`) | ✅ open; the relay uses it |
| **AGENCY** — sub-accounts, SaaS plans, snapshots, users | the public API with an agency token (`GHL_AGENCY_TOKEN`, `.dev.vars` only) | ✅ token in place; nothing built on it yet |
| **THE BUILDERS** — workflows, funnels, forms, page layouts | NOT the API (workflows are read-only there). The real screens, driven by a browser; GHL's own builder AI as a helper; or our own code as a GHL Marketplace app whose custom steps a workflow can call | ⏸ decision below |

**The recommended door for the builders (not yet decided by Isaac):** a SEPARATE GHL user for the AI (Settings → My Staff,
a limited role), signed in once in a browser tool that drives GHL's real screens — so anything the AI does appears in the audit
log under its own name, can be removed in one click, and never runs as Isaac. Rejected: the reverse-engineered internal API
(`research/ghl-workflow-builder-repo-map.md` — it logs in as a user, its evidence does not hold up, and it leaks secrets).

**The order of work** (each row is a board row in the business-runtime project; the HOW is its `ghl-api` skill):

| # | work | who | needs |
|---|---|---|---|
| 1 | ✅ the relay writes leads and payments into the CRM, per form (`lib/ghl.js`) | agent | done and live |
| 2 | ✅ the `ghl-api` skill — ONE skill, a folder per GHL domain (32 domains, 402 operations) generated from GHL's own MCP with MCPorter, `call.sh` to run any operation, and `house-rules/` (tokens, IDs, traps); a read, a write and a delete proven through it (`business-runtime/.claude/skills/ghl-api/`) | agent | done |
| 3 | the AI user in GHL + the browser tool that drives GHL as that user | Isaac creates the user and signs in once; an agent builds the tool | Isaac's go |
| 4 | Cal.com → the relay (a booking moves the deal to Booked; a no-show is flagged) | agent | Isaac: keep Cal.com or use GHL's calendar (recommended: keep Cal.com for now) |
| 5 | narrow the sub-account token from all scopes to contacts, opportunities, conversations messages, custom fields | agent walks Isaac through it | — |
| 6 | speed to lead: an instant text and the ring-you-first call, only for a lead with a consent record and a phone | agent | a phone number in the sub-account and the A2P registration (Isaac's setup, already on his list) |
| 7 | GHL's outbound events → the relay (a reply, a stage change), if GHL does not charge for them (`research/ghl.md` Q9) | agent | Q9 answered |
| 8 | SaaS Mode: the three tiers as plans, the first snapshot | agent + Isaac | the tier prices (Isaac's) |
| 9 | the framework's real PDF, its skills repo, an honest placeholder on the skills button meanwhile | agent | Isaac's word on which frameworks ship |

## 7. JobWorld ↔ GHL — GHL is the CEO's world

**The design** is `business-runtime/DESIGN.md` § 8a "GHL IS THE CEO'S WORLD"; this is its build list. JobWorld is a `CAVEHTTPServer`
subclass (`JobworldHTTPServer` in `twi-jobworld/server/jobworld_server.py`, its agent `JobworldAgent(CAVEAgent)`), so it already has
the doors used below: `/api/emit-event` and `/api/events` (the event bus) · `/api/automations` (the cave calendar) ·
`/api/tasks` + `/api/ceo-review` (the review gate) · `/api/sop-patterns` + `.../harvest` (emergent SOPs → skills) ·
`/api/departments` + `/api/agents` (make an employee or a department).

| # | build | how | state |
|---|---|---|---|
| 1 | **THE FENCE** — ✅ BUILT (`business-runtime/.claude/skills/ghl-api/fence/SKILL.md`). The one hard block is MONEY: `call.sh` and both clients refuse any write that charges, invoices, records a payment, sells, prices or buys (48 operations; `tools/fence_rules.py`) with "message your human user"; `--full` removes it, for a person or a builder. Everything else is INSTRUCTION, written for the agent in that skill: send only on one of the three bases (they contacted us · they consented · cold email to a US business), check the contact's do-not-disturb flags and the `suppressed` tag first, say it is automated on chat channels, never a cold text or AI call, leave a note when it sends. Cold email waits on the company's postal address (the board's OPEN list). What it does not do: a process holding the raw token and a shell can call GHL directly, and the instructions are not enforced in code — a model told the rule correctly follows it | ✅ built |
| 2 | the relay pushes every lead, payment, booking and reply to JobWorld's `/api/emit-event`, labeled with an `observation.process` | a destination in the relay's list, or a cave automation that reads it | ⏸ |
| 3 | GHL (through the safe profile) is a default tool in every JobWorld box | one entry in `render.py`, the key in the box's `.secrets/`, like Instantly and Apollo | ⏸ |
| 4 | patterns are harvested automatically | a nightly cave-calendar entry harvests any pattern with enough events; each new SOP goes through the review gate before it is kept | ⏸ |
| 5 | outcomes attach to patterns | a reply, a booking or a payment in GHL is recorded on the pattern that produced it, so what worked harvests first | ⏸ — the pipes exist, the plumbing is not done |
| 6 | **the test lane** — our own inbound lead handled by the CEO for a week | steps 1–3 first; then read the patterns that emerged and harvest one | ⏸ |
| 7 | **the human as the CEO's employee** — what only a person may do (a LinkedIn or Instagram message from a person's own account) becomes a task the CEO assigns to a human seat, with the drafted message and the link prepared; the human carries it out in GHL's staff app; the reply lands in GHL and the CEO reads it | a GHL task with `assignedTo` the human (built: `lib/ghl.js` already creates tasks) · the fence binds a directive to a human as it binds the CEO's own actions | ⏸ |

⛔ **Not proven:** the CEO designing a business from a ping. B6's departments came from a setup and kiki's from defaults; what the
data shows is the mechanism (B6: 5 patterns, 2 harvested skills; HealthWorld: 4 patterns, 0 harvested). The test lane is what
would prove it.

## 5. Proof and undo

PROOF (done 2026-09-28 against the real sub-account, records deleted after): one lead → a contact with its 7 fields, a deal at New lead, a note and a task; the same sale sent as an invoice then a checkout, twice each → one deal Won at the first payment's amount, one "Pay partner" task; a renewal changed nothing about the deal; a refund → a task; an unknown payer → a contact tagged `unmatched-payment` and a task. UNDO: remove `GHL_TOKEN` from the Worker — the relay falls
back to the webhook destinations it has today.
