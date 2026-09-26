# RULE 00 — THE SITE CANON (nobody edits this site without reading their sources)

**THE LAW: NOBODY MAY EDIT THE SITE WITHOUT BEING TOLD WHAT TO READ TO PUT THERE.** An agent editing
any page reads that page's canonical sources FIRST and puts THEIR content there — never its own
summary, never an orchestrator's paraphrase, never invented copy. If a surface's source row below is
missing or stale, that is a BLOCKER to report, not a gap to fill with judgment.

## WHAT IS PUBLIC

**One page is presented: `ai-transformation.html`.** Above it rides the glass top bar (RULE 02 §9):
the TWI wordmark and a red BOOK A CALL that never leaves the screen. The page is six things and one
action — the claim ·
the video (`assets/vsl.mp4`, full width, its runtime never stated) · what I do (the loop
`assets/what-i-do-loop.mp4` — silent, autoplaying, looping, no controls, stopped on its poster under
reduced motion; source `video-aios/draw-the-box/loop/` — and under it ONE blurb, the four levels of
your business in *USER*'s words: solo · org · automation · solo again) · what you get (STAGE ONE's
map, in *USER*'s structure: every department in priority and why · every piece of software and what AI
needs from it — his "stringly · harnessed stringly · full logic" rendered at the door as "a plain
prompt, a guided prompt, or fully built logic" · the AI teams you could run · and we also map the
business's health — website, marketing, reviews, speed to lead, after-hours support, lead
generation, lead nurture, content presence — and its SOPs, which diagnose whether rebuilds or audits
are needed; those become customizations, never stage one) · who you will be talking to ·
book a call. No prices, no checkout; the ONE scroll choreography is the pinned pair (What I do stays
while What you get slides over it — RULE 02 §10). Its wordmark is a `<span>`, never a link:
the page has exactly one exit, the booking form.

**THE HEADLINE AND SUBHEADLINE ARE *USER*'S, FROZEN LIKE THE OFFER** — the deck's slide 1, the
same pair the page's `<title>` and meta description carry: **"AI Transformation That Actually
Works."** / **"From manual processes to a more capable, efficient, and resilient business."** An
agent never rewrites them, never merges deck lines into a new subheadline, and never swaps in an
"avatar + problem" line of its own; a proposed change is asked, not shipped.

**PRESUPPOSE THE CALL.** Page copy speaks as if the visitor is already booking: "who you'll be
talking to", never the conditional "who you'd be talking to" — the conditional keeps the call
hypothetical (the marketing register's presupposition and future-pacing).

**The full funnel is preserved, not presented:** `ai-transformation-full.html` (the thirteen deck
slides, the driven diagrams, the cost anchor, the ledger, the price cascade, both checkout doors, the
FAQ), linked from nothing. It comes back by swapping the two filenames. Every other page exists and is
not being presented; the laws below govern each page whenever it is.

## HARD LAWS (every page, before any source)

1. **OFFERS ARE FROZEN.** Prices, products, tiers, session lengths, guarantees, paid-CTA wording:
   Isaac only. Source of truth = `main:pricing.html` verbatim. Discrepancies (arithmetic, collisions)
   are EVIDENCE for a `FOR ISAAC` report block — never resolved by an agent.
2. **LORE FIREWALL AT THE DOOR.** Top-of-funnel pages: zero canon-internal vocabulary. The inner
   register lives in `inside/` only (reachable from system.html, never from the door). Isaac's
   PERSONAL pages may carry his real register — plain statement first, flavor after, never as
   prerequisite vocabulary.
3. **NO UNCASHED CLAIMS.** A claim ships with its receipt or ships as a labeled IOU. No fabricated
   numbers, no uptime claims nobody verified, no fake dashboards (world-slots stay empty until real
   footage exists).
4. **VOICE:** scoreboard readings, not verdicts ("is losing", never "is a loser") · shown, never
   claimed · punch at the discourse, never at names · the arrogance budget equals the receipt balance.
5. **LAYOUT** = the `_templates/` + `style.css` skeleton · relative in-page paths · the absolute
   SITE_ORIGIN (`https://sancovp.github.io/aisaac`) only in canonical/og.
6. **THE NAMES: TWI in the chrome, Isaac in person.** The top bar's wordmark is
   `Transformations With Isaac` — the company's name (TWI), and the only name in the chrome; the
   hero's pill reads just `TWI`. The person the visitor will talk to is **Isaac Wostrel-Rubin, Founder of TWI**: the
   about card names him so, and the footer and the prose say Isaac. His background ("How I got
   here") states only facts he gave: AI since 2023, agents for a film production company,
   philosophy and ontologies, what he has built, the Digital Twin of an Organization he is building. The legal entity (Ribcage Solutions, Inc.) never appears on the site; it lives in
   `docs/`, the contracts and the Stripe statement. `AIsaac` is the repository and the URL path,
   never a brand on a page.
7. **EVERY SURFACE ANSWERS ITS OWN OF THE BUYER'S FIVE QUESTIONS.** Marketing is mostly organization:
   the organized thing should feel like finding a treasure trove. (a) does it LOOK LIKE the
   information is real, useful, what I need · (b) is there a lot, is it organized, will I get
   everything I need even without knowing what that is · (c) what should I expect, and is this what I
   expected · (d) what are the guarantees · (e) can I afford this relative to how the guarantees
   change my life. (a)(b)(c) are the free surfaces' job — the door, blog/tags, repos, notes; (d)(e)
   are the offer layer — pricing, Isaac-authored, frozen.
8. **SAFE, THEN WHERE-NEXT.** Every page tests against one recognition: the information here is safe,
   and I want the next part. A visitor does not go back and read it all unless an offer makes them
   pause; they convert, or pause and then convert or leave.
9. **THE RATCHET LAW OF NAVIGATION.** A funnel is a series of ratcheted options: the visitor can find
   no move except the sanctioned ones. Every page's visible exits ARE its sanctioned moves — design each
   exit set deliberately. On the full site: the brand button → `isaac.html` (the hub) · `index.html`
   is the entrypoint only, one-way, with no nav route back to it (browser-back only). On the public
   page: the booking form is the one exit.
10. **THE BRANDED-FILTER LAW.** Every browse or filter surface filters by Isaac's framework concepts,
    never by generic categories. The corpus index files every piece under the seven levels of agent
    engineering (the flagship: `lab/explainer.html` → `blog/levels-overview.html`) plus the
    cross-cutting concepts. The vocabulary and every assignment live in `tools/tags.py`, whose four
    laws bind: the seven levels are the spine · door register only (law 2) · no orphan tags and 1–3
    tags per post, both checked at build time · ONE corpus, ONE tag index. When a surface sorts, it
    sorts by the framework.
11. **THE ENGINEER DESCENT (full site).** It is a landing for cave-teams and dark-factory and ends at
    dark-factory's README, which ends in a clone command. `build.html` reuses the dark-factory and
    cave-teams README copy — the best zero-lore public text in the ecosystem — and never paraphrases
    over it. dark-factory's one-liner: *"no human is in the loop; what stops it shipping garbage is
    three independent gates ending in a controlled experiment."*
12. **HERO FIRST (full site).** The site is about Isaac and what he thinks; the funnel sits
    downstream. Funnel category = simulations-and-world-loops. The h1 scoreboard line returns only
    when a scoreboard page is published.

## THE SOURCE MAP — per surface, what you READ to know what goes there

⛔ **SOURCES NOT ON THIS MACHINE.** `~/aios-research/`, `~/repo/garage-lab/`, `~/repo/dark-factory/`
and `/agent/` exist neither on this host nor in its containers. A surface whose sources are only
there is BLOCKED: report it and edit nothing on it (law above). Where they live is ⏸ OPEN, *USER*'s.
Paths below marked ✓ resolve here.

| surface | canonical sources (READ THESE, in order) |
|---|---|
| **the whole funnel** (IA, what sells, the ladder) | `~/aios-research/FLYWHEEL.md` (THE SPINE) · `~/aios-research/THE-CLINIC-MAP.md` (the operating-structure ruling) · ✓ `~/claude_code/video-aios/references/content-plan/THE-OFFER-AND-FUNNEL.md` (the concrete money offer) · `~/aios-research/ME2C-FUNNEL.md` (creator side) |
| **positioning / category** | `~/aios-research/GARAGE-LAB-LAUNCH-STRATEGY.md` §0 (simulations and world loops: iteration does not compound; worlds compound), §1 (legibility grammar), §1b (content pipeline), §1c (voice — law 4) |
| **index.html / the door** | the two rows above + `~/aios-research/SITE-CEO-BRANCH-REVIEW.md` (live decisions, incl. hero-first) |
| **isaac.html (the hero site)** | `GARAGE-LAB-LAUNCH-STRATEGY.md` §1c · `~/aios-research/HJ-GAUGE-SPEC.md` (the theses) · `~/repo/garage-lab/CATALOG.md` + `INDEX.md` (the receipts) · `~/repo/garage-lab/CLAIM-AUDIT.md` (the honest claim board) · myth flavor ONLY from ✓ `~/claude_code/sanctuary-revolution-alpha/research/ssri/SANCTUARY-MYTH-ORIGIN.md` Part V |
| **pricing.html** | `main:pricing.html` VERBATIM + Isaac. No other source exists. |
| **rung pages (learn/build/run)** | the funnel row for what each rung IS; product truth for jobworld surfaces from `~/aios-research/SYSTEM-ROLLUP.md` + the avi-jw rules (`/agent/.claude/rules/00,05,07`) — honest grades only |
| **watch.html / world demos** | real run receipts ONLY: cave-teams live tests (`test_live_skillcraft.py` runs), future footage per `GARAGE-LAB-LAUNCH-STRATEGY.md` §1b. Never generated numbers. |
| **blog/ + notes/ (field notes)** | the posts' own content (conform layout only) · new notes draw from `~/repo/garage-lab/CATALOG.md` entries (receipted patterns) · **the tag vocabulary and every post's tags = `tools/tags.py`, the single source both generators read — a new post is TAGGED THERE or the build fails** |
| **inside/ (the lored register)** | ✓ `SANCTUARY-MYTH-ORIGIN.md` · `HJ-GAUGE-SPEC.md` · the top-level design — the ONE place the inner register ships |
| **patterns.html (the architectures)** | the page shows named SYSTEM STRUCTURES, not working disciplines. READ, in order: cave-teams' topology diagrams with their run receipts · ✓ `~/claude_code/cave-teams/cave_teams/*.py` MODULE HEADERS (`blackboard · season · gameworld · gauntlet · skillcraft · darkfactory · evolve · npc · agentdir` — each docstring states its structure; those statements are what the entries render) · `~/repo/dark-factory/README.md` + `docs/*.svg` · ✓ the `compile-claude-code-component` skill's `reference.md` (the 7 primitives + control levels) · `~/repo/garage-lab/CATALOG.md` **architectural entries only** · the public READMEs of any repo linked. **THE COMPILER WING:** ✓ `~/claude_code/sanctuary-revolution-alpha/base/chaincompiler/` — `README.md` (§Why · §the one idea · §the loop · §the stack · §SkillTree · §the formal spec) · `REBUILD-SPEC.md` · `FEDERATION.md` · the package READMEs and MODULE HEADERS for `rulecatcher · honeyc · accc · corcc · sccc · chainaios (bandit·gba·hba·cog·construct) · glyphsteer · si · framework · skillchain-compiler` · `chains/skill2framework.chain` · `.claude/skills/bandit-chain-system`. **THE COMPOSITION SUBSTRATE** — `sancovp/universal-chain-ontology` (`uco/core.py`) + `sancovp/sdna` (`sdna/{sdna,ariadne,poimandres,chain_ontology}.py`) + `cave-teams/cave_teams/{sdna_bridge,links,concurrent,chain_ontology}.py`; **THE AGENT HARNESS** — `sancovp/cave` (`cave/core/{cave_agent,state_reader,hooks,channel,automation,calendar,config_snapshots,dna}.py`, `core/mixins/{hook_router,anatomy}.py`, `core/loops/base.py`, `HOOK_ARCHITECTURE.md`); **THE EDIT SIDECAR** — `sancovp/codenose` (`hooks/`, `codenose/util_deps/*`) plus its receiving-end rule; **THE CONCEPT STORE** — `sancovp/carton-mcp` (`add_concept_tool.py`, `sm_gate.py`, `observation_worker_daemon.py`, `carton_kv.py`, `network_gateway.py`, `carton_quota.py`, `aut_deducer.py`, `server_fastmcp.py`, `UARL_SPEC.md`); **THE TREE ENGINE** — `sancovp/skilltree` (`src/skilltree/{cohere,federation,tome}.py`); and the PRIVATE **symbolic reasoner** + **structure engine** in the canonical home's `base/`, whose entries say "the lab". **Runs-in links ship only for repos AND PATHS that return 200 UNAUTHENTICATED** — `dark-factory`, `world-of-skillcraft` and `garage-lab` are private, so their entries say "the lab"; `personacc`, `personapack` and `goldenreq` exist in the monorepo but NOT in the public `chaincompiler` repo, so nothing on the page may be built on them. The monorepo's own four SVGs are LIGHT-themed and never go on the void; the self-maintaining repository's are dark and ship unaltered. Branch names differ per repo (`master` for cave · codenose · skilltree · sdna; `main` for chaincompiler · carton-mcp · uco · cave-teams) — every deep link uses the right one and is re-verified, never assumed. |
| **audience/market claims** | `~/aios-research/WAVE-STATE-BRIEF.md` · `~/aios-research/reports/` — cite or omit |
| **archetype/rung strategy** (why the site is shaped this way) | ✓ `~/claude_code/sanctuary-revolution-alpha/research/ssri/ship/SANCTUARY-WASTELAND-BATTLESPACE.md` §7m / §7m-bis (the Dudjom → Hormozi transition; Mipham-with-a-door = free-the-WHAT / paid-the-how-I) |

## OPEN — *USER*'s

- where the sources marked absent above live
- the custom domain · the repo-name L3 exception · the watch.html build · merge-source deletions

## MAINTENANCE

This rule is the unification point. A ruling about site content REWRITES this rule the same session —
into the law, the source-map row or the OPEN item it touches, stated as current truth, never appended
as a dated entry. An edit made without reading this file's sources is a defect regardless of how good
it looks.
