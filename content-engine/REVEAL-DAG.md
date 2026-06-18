# THE REVEAL-DAG — the discovery sequence for the holographic content engine

> The sequencer (stage C) of the content super-object. It does NOT write scripts — it answers ONE
> question each day: **which framework is allowed to be "discovered" on camera next?** A framework may
> only surface after its prerequisites have surfaced. Walking this DAG, threaded across the series, IS
> the production plan. (Vision capture: global journal 2026-06-01 "CONTENT SUPER-OBJECT".)

## The premise (why this is a DAG, not a list)

We already hold ~57 named frameworks (`aisaac/free-layer`, `aisaac/video-storyboards`,
`aisaac/b2b-bootcamp`, + 18 invariants). The series make it *look like* Isaac is discovering them live
by cross-pollinating domains. That illusion only holds if the reveal order respects dependencies: you
cannot "discover" CLINIC before the pieces it orchestrates (PSA → SCREENING → DOCTOR → LIFE) have each
been discovered. So the episode order is a **topological sort of the framework dependency graph**, and
a discovery can be *triggered* by a sibling series (a Buddhist-lens video unlocks a node the business
series then uses). That cross-series triggering is the "converging if you pay attention."

## The convergence target (every series climbs toward this)

**HOLOGRAPHIC-WORK** — "a framework (how a human thinks), a skill (how an AI runs it), an automation
(code), the content (explanation), the product (package) are ONE engine at five compression levels."
Each series reveals its own domain's frameworks, then the finale reveals they were **the same shape**:
CLINIC (business) ≅ SOSEEH/Seven-Disciplines (AI) ≅ the sanctuary path (dharma) ≅ a health protocol.
Terminal nodes feeding it: `holographic-work` ← `compounds-or-rots`, `the-altitude-ladder`,
`sovereignty`, `seven-disciplines`. That convergence is the show's payoff and the funnel's top turn:
*"it's all one engine — and the compiler that makes them is the offer."*

## The series (domain lenses over ONE substrate = Isaac's day)

| series | hook ("following…") | domain corpus | role |
|---|---|---|---|
| **A — BUSINESS** | "following Alex Hormozi until $10k MRR" → *it's in my business AI-OS* | `b2b-bootcamp` (CLINIC family) | **the spike series — full depth below** |
| **B — AI SYSTEMS** | "building the ultimate compounding system" | `video-storyboards` + `free-layer` (SOSEEH, Towering, Seven Disciplines…) | the "how I build with AI" PSA |
| **C — DHARMA** | "following ancient Buddhist meditation masters" | `business-buddhism`, `completely-fake-dharma`, `sanctuary-system`, `meta-cognitive-awareness`, `thermal-dynamics` | the awareness/sanctuary lens; **triggers the CLINIC reveal in A** |
| **D — HEALTH** | "following {health authority}" | `healthworld` | the body/protocol lens |
| **(spine) SANCTUARY JOURNEY** | the meta-narrative | `holographic-work`, `altitude-ladder`, `sovereignty` | not a lens — the convergence all four climb into |

## SERIES A — full reveal sequence (the spike; prereq edges from the inventory)

Each node = one "discovery." `needs:` = what must already be revealed (the gate). `trigger:` = the lived
event / cross-series moment that makes the discovery feel organic.

```
A0  USE HORMOZI RAW            needs: —                      trigger: "I'm just running his value-equation + basic funnel."
A1  SNAKEOIL (anti-position)   needs: A0                     trigger: a competitor/tool felt worse than what I had → "everything's snake oil relative to something better."
A2  OBVIOUSNESS-PARADOX        needs: A0                     trigger: the simplest post outperformed the clever one → "why does the obvious stuff convert?" (self-demonstrating; justifies the whole free layer)
A3  PSA (broadcast)            needs: A2, anti-case-study    trigger: deciding what to publish for free → the broadcast layer falls out of A2.
A4  SCREENING (qualify)        needs: A3                     trigger: a free-content reply that needed qualifying → "how much AI do you have? zero."
A5  MEDICINE + OFFERS          needs: A1                     trigger: building the actual offer → "a regime of solutions, not one pill" (value = identity×likelihood/cost).
A6  DOCTOR (close)             needs: A4, A5                 trigger: a real close → DIAGNOSE→OBSERVE→CONSEQUENCES→TREAT→OPTIONS→RESOLVE.
A7  LIFE (post-close flywheel) needs: A6                     trigger: a client onboarding → LOVE→INTEREST→FULFILLMENT→EXCEL.
A8  CLINIC (the orchestration) needs: A3,A4,A6,A7  + C-trigger  trigger: ★ musing the Buddhist medicine/healing metaphor (Series C) on the funnel → "PSA→SCREENING→DOCTOR→LIFE is ONE patient's journey: C-L-I-N-I-C." ← THE marquee reveal, exactly your example.
A9  CAVE (world model)         needs: A8, cosmology          trigger: "the whole thing is a passage: Wasteland → CAVE → Sanctuary."
A10 UNICORN (north star)       needs: A9                     trigger: finale → "1,000,000 × $100/mo = CLINIC at scale."
A→ CONVERGE: holographic-work  needs: A8 (+ B/C/D peers)     trigger: "CLINIC is the same shape as how I build AI systems and how the dharma works — one engine, many compressions."
```

The ★ on **A8** is the load-bearing cross-series edge: **C (dharma) must have surfaced the
medicine/healing metaphor before A8 can fire.** So the staggered schedule has to place a C-episode on
that metaphor *before* the A8 episode — that's why the DAG threads across series, not within one.

## SERIES B / C / D — sketch (deepen when each spins up)

- **B (AI systems):** foundational first — `meta-cognitive-awareness` → `composition` → `towering`/`build-in-verified-layers` → `SOSEEH`/`the-four-slots` → `drift-is-the-default` → `right-is-not-fluent` → `admissibility`/`concentration`/`emergence` → **`seven-disciplines`** → converge `holographic-work`.
- **C (dharma):** `meta-cognitive-awareness` (shared root with B) → `thermal-dynamics`/`HIEL` → the medicine/healing metaphor ★ (feeds A8) → `sanctuary-system` → converge.
- **D (health):** TBD from `healthworld` corpus → a protocol/regime framework that rhymes with MEDICINE → converge.

Shared root: **`meta-cognitive-awareness`** sits under B and C both — a natural early reveal that pays off in two series at once.

## The reveal-cursor (stage C state)

A tiny persisted record (same idea as the doc-mirror cursor): `{revealed: [A0,A1,...], pending_triggers: [...]}`.
Each day: `eligible = nodes whose needs ⊆ revealed AND whose trigger has lived-event support in today's
cohered log`. The compiler (stage D) may only script discoveries from `eligible`. When a node is shipped,
add it to `revealed`. This is what makes "report day → today's allowed reveals → scripts" mechanical.

## How it drives the daily compile

```
cohered day-log (CartON events, tagged by series/framework)
   → reveal-cursor: which eligible nodes have support today?
   → for each due series (staggered): lens × day-events × eligible-node → SCRIPT
   → the discovered framework graduates: held → "born on camera" (add to revealed)
```

## FUNNEL ENTRY POINTS (the site layer — already partly built)

Each series lands on the public site (`sancovp.github.io/aisaac`) as a set of **domain entry pages** → the
CLINIC funnel (PSA → SCREENING → DOCTOR via `apply.html`/`join.html`). The *World's per-domain page set
IS the PSA broadcast layer (one entry point per avatar). Build status:

| series | entry-page set | status |
|---|---|---|
| **D — Health** | `healthworld/` = 14 body-system dept pages + index ("Pick one department. Make it green." → `apply`/`join`) | **BUILT** — 14 PSA entry points, one per health avatar |
| **C — Dharma** | `dharma-concierge/` (23 pages) + `completely-fake-dharma.html` + `dharma-concierge.html` | **BUILT** (substantial) |
| **A — Business** | `jobworld-premium.html` | **PLACEHOLDER** ("being built right now") — the parallel business-department entry set is NOT built |
| **B — AI systems** | `frameworks.html` + `free.html` + `free-layer/` + `agents.html` | content exists; framework index live |

**Key:** the HealthWorld index literally says **"Same engine. Different world."** — that's the
`holographic-work` convergence *already live in the funnel*: each *World is the same engine, different
domain. So the per-*World **funnel template** is proven: *N domain pages → "pick one, make it green" →
apply/join.* PromptWorld would get its own set: *N component pages (skill/mcp/hook/persona/plugin) →
"build one" → apply/join.* The reveal-DAG's on-camera "discoveries" drive viewers TO these entry pages;
the pages are the landing surface the series funnels into.

— v1, Series A deep. Refine the edges/triggers, then this drives the single-video spike (episode = A0/A1).
