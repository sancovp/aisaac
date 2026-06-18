# The "Worlds" + Legacy Autobattler + PromptWorld Status Map

**Author:** saas-mapper (Task #8) · **Date:** 2026-06-06
**Method:** Full reads of source + on-disk doc-mirror journals (cited inline). Marked `IS` (read from
code/file), `NOT FOUND` (searched, absent), `DESIGN-ONLY` (docs exist, no code), `MARKETING`
(asserted in site/README), `UNCLEAR`. Faithful to code/files; nothing invented.
**Provenance limitation:** I did **not** query the CartON `:Wiki` timeline MCP for historical data —
I used the **on-disk doc-mirror journal** (`promptworld/context/journal/2026-06.md`, the durable layer
that survives even when the ingestion pipeline is down) + repo code + the aisaac site. Where history
is cited it is from that journal, not the live timeline.

---

## Summary table

| # | World / thing | Status | Where | What it is (one line) |
|---|---|---|---|---|
| 1 | **Jobworld** | **IS** (built) | `/home/GOD/twi-jobworld` (+ monorepo `application/cave-jobworld`) | CAVE-fork plugin: "zero-employee AI company" (5 dept agents + CEO + dashboard) |
| 2 | **HealthWorld** | **IS** (built, 2 forms) | `/home/GOD/twi-healthworld` (plugin) + `/home/GOD/aisaac/healthworld` (15 HTML pages) | Jobworld fork: "your body is a company" — OSMOSYS + 14 body-system depts + CLINIC |
| 3 | **gameworld** | **NOT FOUND** (as built repo) | only `/tmp/agent_world_game` = DESIGN-ONLY docs | No code; an "Agent World RPG" concept exists in docs; journal says it's "a totally different pattern" |
| 4 | **World of Skillcraft** | **NOT a world — it's a PATTERN** | `understand-teams` skill | One of two agent-team coordination patterns (shared-state), not a `*World` repo |
| 5 | **World of Workers** | **NOT FOUND in container** | listed HOST-ONLY in `canonical-source-dirs.md:126` | Not in Docker; lives on host only per the canonical rule |
| 6 | **Legacy Autobattler** | **IS** (built, legacy) | `/home/GOD/core/computer_use_demo/codebase_analyzer_system/autobattler/` | Runnable TFT-style "Agent Arena" — recruit agent units, deploy team, battle "project" enemies |
| 7 | **PromptWorld** | **IS** (v1+v2 built+verified) | monorepo `application/promptworld` | 3rd CAVE `*World` fork; engineer-CEO over `claude -p`; PROMPTS dept live; doc-mirror registered |

---

## 1. Jobworld — `/home/GOD/twi-jobworld` (IS, built)

### What it is
A **Claude Code plugin** (`.claude-plugin/` present) that instantiates an **AI-run company**:
"Zero employees. A full company. All AI." (`README.md`). You are the CEO; 5 agent roles (Content,
Growth, Revenue, Research, Engineering) execute. It ships a web dashboard, a Projects→Milestones→
Goals→Tasks hierarchy, an org chart, an event log, a "Ralph Loop" persistent-prompt toggle, and a
day-simulation.

### Architecture (IS — from dir structure + README)
- `server/` — the company-simulation engine + dashboard (REST API; "all agents expose their work via
  a REST API").
- `skills/` (21 skill dirs) — incl. `instantiate-jobworld` (the **instance maker**), `understand-*`
  (plugins/agents/hooks/mcps), and `compile-claude-code-component` (the component-compiler seed —
  see PromptWorld below).
- `ink-ceo/`, `kiki-ops/`, `sop-engine/`, `agents/`, `template/` (per-instance scaffold), `docker/`.
- **Futamura framing** (README, MARKETING/design): the plugin is "P1 in the Futamura tower" —
  P0 = Jobworld source, P1 = this plugin interprets source → new plugin instances.

### Related (IS)
- **`/home/GOD/gnosys-plugin-v2/application/cave-jobworld/`** — a **separate Python package**
  (`cave_jobworld`, `pyproject.toml`) — the CAVE-integrated package form, distinct from the
  `twi-jobworld` plugin. (Also forks/copies at `/tmp/jobworld`, `/tmp/cave-jobworld`, `/tmp/jobworld-test`.)
- On the aisaac site, the Jobworld funnel page (`jobworld-premium.html`) is a **PLACEHOLDER** (per
  the promptworld journal entry, 2026-06-01).

### State (IS)
Built and structured (last touched ~May 19). It is the **original `*World`** that HealthWorld and
PromptWorld were forked from.

---

## 2. HealthWorld — EXISTS in two forms (IS, built)

### Form A — the plugin: `/home/GOD/twi-healthworld` (IS)
A **direct fork of twi-jobworld** (the promptworld journal entry 2026-06-01T14:44 proves it: "healthworld's
git origin IS github.com/sancovp/twi-jobworld.git, first commit = 'Initial twi-jobworld plugin', shares
jobworld's whole history"). Domain swapped to **personal health**:
- **OSMOSYS** = the health-operations agent ("mirrors GNOSYS"); **D.O.C.T.O.R.** = bedside-manner
  protocol; **CLINIC** = the chain (PSA → SCREENING → D.O.C.T.O.R. → LIFE). (`README.md`, `CLAUDE.md`)
- **14 body-system departments** (Dental, Sleep, Cardio, Gut, Musculoskeletal, Mental, Skin, Vision,
  Hormonal, Nutrition, Substance, Environment, Social, Financial).
- `server/healthworld_agent.py` = `HealthworldAgent(CAVEAgent)`; `healthworld_server.py` =
  REST+WebSocket+`/api/health-import` (Apple Health via Health Auto Export $3/mo) + `/api/department-status`.
- Skills: `hw-osmosys-bootstrap`, `osmosis-pwns` (full-body CLINIC sim), `hw-psa`, `hw-screening`,
  `hw-doctor-protocol`, `hw-life`, `generate-monitor`, `instantiate-healthworld`, `run-dept-{14}`.
- **Known drift (IS, journal-flagged):** the fork was a manual clone+rename — `docker/` still says
  `Dockerfile.jobworld`, and ~277 lines of domain are tangled INTO the core agent.
- **State:** "freshly built last week as a CAVE fork" (journal 2026-06-01T14:12) — verified-working
  enough that it was used as the proof that CAVE boots cleanly for PromptWorld.

### Form B — the site funnel: `/home/GOD/aisaac/healthworld/` (IS)
**15 static HTML pages** (`index.html` + 14 body-system pages: cardio, dental, gut, hormonal, mental,
musculoskeletal, nutrition, skin, sleep, social, substance, vision, environment, financial). This is
the **funnel entry-set** ("Osmosis Jones the Jobworld"; recent git commit `ab4e1e6` "Add HealthWorld
dashboard"). The promptworld journal notes the index says "Same engine. Different world." (the
holographic-work convergence, live in the funnel). (Also `/tmp/heaven_data/healthworld` runtime data.)

---

## 3. gameworld — NOT FOUND as a built repo (DESIGN-ONLY concept exists)

- **No `gameworld` / `game-world` directory or repo** anywhere under `/home/GOD` or `/tmp` (searched,
  empty).
- The closest artifact is **`/tmp/agent_world_game/`** — **DESIGN DOCS ONLY** (4 markdown files:
  `README.md`, `CONCEPT_ART.md`, `NPC_DIALOGUE.md`, `TECHNICAL_IMPLEMENTATION.md`, Apr 2025). It
  describes **"Agent World: The AI Engineering RPG"** — a meta-RPG where you build AI agents to battle
  "task-monsters" and expand a "domain empire," with a HEAVEN hub. **No code.** This is a *different*
  thing from the autobattler (#6), though thematically adjacent.
- **Corroborating history (IS, journal 2026-06-01T14:59):** Isaac, verbatim — "gameworld is a TOTALLY
  DIFFERENT pattern (different team pattern)… jobworld + healthworld have NO shared class… i think
  maybe `*World` doesnt even exist maybe im making that up."
- **Verdict:** `gameworld` is **NOT a built system** — it is a design concept (the RPG docs) + an open
  question in Isaac's own framing. NOT FOUND as code.

---

## 4. World of Skillcraft — NOT a world; it is a TEAM PATTERN (IS)

`World of Skillcraft` is **one of the two agent-team coordination patterns** documented in the
`understand-teams` skill (`/tmp/heaven_data/skills/understand-teams/`), **not a `*World` repo**:
- Skill metadata (`_metadata.json:5`): "two patterns: **Metacog Shell** (peer messaging,
  self-improving) and **World of Skillcraft** (shared state, persistent agents)."
- `resources/overview.md`: **Metacog Shell** = agents message each other **directly**; **World of
  Skillcraft** = agents coordinate **indirectly via shared state (files/JSON)**, persistent agents.
- Also referenced by the `compile-claude-code-component` skill.
- **Verdict:** exists as a **named pattern/concept** (a way to run agent teams), **not a domain world**.
  No `*World` repo by this name. (This matches Isaac's "if it exists" hedge in the task.)

---

## 5. World of Workers — NOT FOUND in container (HOST-ONLY per the rule)

- **No `world-of-workers` directory** under `/home/GOD` or `/tmp` (searched, empty).
- **`canonical-source-dirs.md:126`** explicitly lists `world-of-workers` under the
  **"💻 HOST ONLY (not in Docker)"** bucket (alongside `story-graph-system`, `landing-page-game`,
  `sancrev-frontend`, `crystal-ball (hosted)`, `CIG`, `psychoblood-gp`, `brain-agent`, `largechain`).
- **Verdict:** **NOT FOUND in this container — by design.** It lives on the host only; I cannot map
  its architecture from here. (Honest limitation, not an absence of the project.)

---

## 6. Legacy Autobattler — IS (built, runnable, legacy) — "Agent Arena"

**Location** (authorized for this item only): `/home/GOD/core/computer_use_demo/codebase_analyzer_system/autobattler/`
(files dated **May 23 2025** — legacy core). Files: `game.py` (25 KB, the engine), `arena_tool.py`
(HEAVEN tool wrapper), `cli.py` (renderer), `entities.py` (Agent/Enemy/Task/Tool/AgentShopItem),
`example.py`, `__init__.py` + `../product_philosophy/game_loop_design.md`.

### What it is (IS — full read of `game.py` + `arena_tool.py`)
A **complete, runnable Team-Fight-Tactics-style auto-battler** where the units are **AI agents** and
the enemies are **software projects**. It is NOT a stub — it has full game logic, save/load, and a
HEAVEN tool interface. `AgentArenaTool.description` = **"Play the Agent Arena auto-battler game to
build workflows"** — i.e. the metaphor is *building an agent workflow by playing a shop-and-battle game*.

### How it works (IS)
- **`AgentArenaGame`** (`game.py:109`): gold economy (start 50), rounds (`max_rounds=8`), a **shop**
  of recruitable agents, a **bench** + deployed **team**, a **tool bench**, and one **enemy** per
  campaign.
- **Agent pool** (`_initialize_agent_pool`): 8 typed agents — Designer, Coder, Tester, DevOps,
  Content, Security, Database, Frontend — each with `base_skills` (coding/design/testing/…),
  `cost`, and `synergies`.
- **Tool pool**: CodeEditor, Debugger, Designer, Deployment, Documentation, Database, Testing,
  Security — each tagged; buying a tool for an agent boosts task success when tags match.
- **Enemy = a project/goal** (`_create_enemy_from_goal`): named from the goal string, given generated
  **tasks**; each task has `required_skills`, `tags`, `required_steps`, `difficulty`.
- **Battle** (`run_battle` + `AgentFlow.execute`): the deployed team is run as a **sequential flow**
  against each task; per-agent **success_chance** = base 0.5 + skill-over-requirement bonus + tool
  bonus(0.2) + level bonus − difficulty, clamped [0.1, 0.9], rolled with `random.random()`. Completing
  a task damages the enemy; defeating the enemy + completing tasks award gold; agents gain XP and
  level up. Game ends at victory or round 8.
- **Shop mechanics:** weighted refresh (favoring agents useful vs current enemy tasks), lock slots,
  recruit, free between-round refresh + round gold (`10 + round*2`).
- **Tool interface** (`arena_tool.py`): `AgentArenaTool(BaseHeavenTool)` with actions
  `new_game / render / shop_action / tool_action / team_action / battle / next_round / view_agent /
  view_task / save_game / load_game / help`. State persists to `~/.agent_arena/<game_id>.json`
  (`save_game`/`from_state`/`load_game` — full serialization).
- **Design intent** (`product_philosophy/game_loop_design.md`): a dual-loop "infinite game" —
  inner loop Play→Learn (minutes/hours), outer loop Measure→Improve (days/weeks), with a "magic
  layer" (effortless NL input → agents execute → transparent scoring → social/leaderboards). i.e. the
  autobattler is the gamified surface for the build→measure→learn loop over agent workflows.

### State (IS)
**Self-contained and runnable** (depends on `entities.py` + `cli.py` + HEAVEN's `BaseHeavenTool`).
Legacy (May 2025, in `/home/GOD/core`). Note: `_create_enemy_from_goal` and `_initialize_agent_pool`
have inline comments "would use LLM / be much more extensive in a full implementation" — so task/enemy
generation is **deterministic/simplified**, not LLM-backed, in this version. It is a working prototype,
not wired into any current system.

---

## 7. PromptWorld — "where are we": v1 + v2 BUILT & SELF-VERIFIED (IS)

**Location:** `/home/GOD/gnosys-plugin-v2/application/promptworld` (doc-mirror registered — `.promptworld/`
cursor dir present). **History source:** `context/journal/2026-06.md` (35 entries, 2026-06-01 →
2026-06-02; the on-disk durable layer).

### What it is (IS — settled identity, journal)
PromptWorld = **the 3rd CAVE `*World` fork** (after twi-jobworld + twi-healthworld), domain =
**compiling agents / claude-code components**. It is **PURE-CLAUDE** (no SDNA, no minimax; opus/sonnet
workers). The CEO is an **"engineer-CEO."**

### Architecture (IS — code present)
- `p_main_agent.py` → **`ClaudePMainAgent`**: a `claude -p --resume`-backed drop-in for CAVE's tmux
  `main_agent` (no tmux). Public surface mirrors CAVE's CodeAgent (`session_exists`, `create_session`/
  `spawn_agent`, `send_keys` [str=prompt chunk, 'Enter'=flush turn], `capture_pane`, `send_and_wait`).
- `convo_registry.py` → **`ConvoRegistry`**: alias↔session_id JSON map (`~/.promptworld/convos.json`)
  = **named, save/resumable conversations** (the convo-management tmux lacks).
- `server/` → `PromptWorldHTTPServer(CAVEHTTPServer)` + `/api/chat` (talk to engineer-CEO),
  `/api/convos`, `/api/department/prompt`, `/api/health`.
- `index.html` → minimal dark chat UI ("talk to your engineer-CEO", POSTs `/api/chat`).
- `agents/` → personas (`engineer-ceo`, `prompt-engineer`); `compiled/prompts/` → output artifacts;
  `prompts/`, `skills/` (incl. `start-promptworld`), `docs/`, `context/journal/`.
- **Load-bearing fix (IS, journal 2026-06-01T14:31–14:36):** `claude -p` bills depleted **API credit**
  if `ANTHROPIC_API_KEY` is in env; `_run_turn` scrubs it from the subprocess env → uses the OAuth
  **subscription**. This applies to **every** `claude -p` `*World` agent.

### Where we are (IS — verified milestones, journal)
- **v1 DONE + self-verified E2E** (commit `b914f32`, merged `0792127`, 2026-06-01T16:22): the CAVE-fork
  boots; chat the engineer-CEO over `claude -p` (subscription). Agent verified live himself: `python -m
  server --port 3858` clean; `/api/health` main_agent=`ClaudePMainAgent`; `/api/chat` → real reply.
- **v2 DONE + self-verified E2E** (2026-06-02T01:38): **first department = PROMPTS** — a `prompt-engineer`
  (2nd `claude -p` convo) compiles real prompt artifacts to `compiled/prompts/` via
  `POST /api/department/prompt`. Verified with a commit-msg request producing a real artifact.

### Open / deferred (IS — journal)
- **Persona-not-wired gap** (flagged v2): the engineer-CEO `/api/chat` convo does **not** inject
  `agents/engineer-ceo.md` — it replies from generic knowledge. Works for `prompt-engineer` only
  because the persona is prepended each compile turn. Fix (v2.1): inject persona once at session
  creation.
- **Deferred to v2+:** the other 6 departments (MCPs/Skills/Harnesses/Operating-Systems/Teams/
  Workflows-Chains — a complexity ladder Prompt→…→AIOS), CEO auto-dispatch, the assemble→project→
  publish→install product loop, GEAR scoring, paia-hook lean settings.
- **Strategic decision (IS, Isaac verbatim 2026-06-01T14:59):** **KEEP PROMPTWORLD SEPARATE** — build
  standalone, do NOT wire it to jobworld/healthworld/starsystem CEOs yet. Apparent duplication across
  packages is accepted for now; the unification question (the "`*World` compiler", "compiler-compilers")
  is **deferred to Isaac, not auto-decided.**

---

## Cross-cutting: is "`*World`" even a real shared abstraction? (IS — honest)

The journal (2026-06-01T14:44 + 14:59) records the empirical truth, not a tidy story:
- **Jobworld + HealthWorld + PromptWorld ARE the same pattern** = **CAVE-core + a domain layer**
  (`{World}Agent(CAVEAgent)` + `{World}HTTPServer(CAVEHTTPServer)` + dashboard + dept agents +
  SOP-harvest). HealthWorld was a literal git clone of Jobworld; PromptWorld is the same fork swapping
  the tmux main_agent for `claude -p`.
- **But there is NO shared `*World` base class**, the forks carry rename-drift, and there is **no
  `*World` compiler** (each was a manual clone+rename+domain-swap). Isaac: "i think maybe `*World`
  doesnt even exist maybe im making that up… see im trying to cohere stuff because im scared."
- **gameworld is explicitly a different pattern** (a team pattern / RPG concept, not a CAVE fork).
- The unifying idea floated (NOT decided): a **`*World` compiler is a special case of PromptWorld**
  (PromptWorld compiles claude-code components → it could compile `*World`s, including itself). This
  is **VISION**, parked behind the "keep separate" decision.

**Net:** three real CAVE-fork worlds (Jobworld/HealthWorld/PromptWorld) that look alike by manual
copying, not by a shared compiler; "gameworld"/"World of Workers" are not built here; "World of
Skillcraft" is a team pattern, not a world.

---

## Appendix — files/dirs read (citations)
- Jobworld: `/home/GOD/twi-jobworld/README.md` + dir tree; monorepo `application/cave-jobworld/`.
- HealthWorld: `/home/GOD/twi-healthworld/{README.md,CLAUDE.md}` + tree; `/home/GOD/aisaac/healthworld/` (15 pages).
- gameworld: searched `/home/GOD`+`/tmp` (none); `/tmp/agent_world_game/README.md` (design-only).
- World of Skillcraft: `/tmp/heaven_data/skills/understand-teams/{_metadata.json,resources/overview.md}`.
- World of Workers: `/home/GOD/.claude/rules/canonical-source-dirs.md:126` (HOST-ONLY); disk search (none).
- Autobattler: `/home/GOD/core/computer_use_demo/codebase_analyzer_system/autobattler/{game.py,arena_tool.py}` +
  `product_philosophy/game_loop_design.md` (authorized for this item only; did not wander elsewhere in core).
- PromptWorld: `application/promptworld/{context/journal/2026-06.md, index.html}` + dir tree
  (p_main_agent.py, convo_registry.py, server/, agents/, compiled/, docs/, skills/).

---

## GAMEWORLD SKILLS (Task #9 — searched all skill dirs, not just repos)

**Question:** #8 found no gameworld *repo* (only `/tmp/agent_world_game` design docs). Isaac said there
may be gameworld *skills*. I searched **all** skill locations by dir-name AND by content:
`/tmp/heaven_data/skills/` (856 dirs), `/home/GOD/.claude/skills/` (103 dirs),
`/home/GOD/aisaac/.claude/skills/` (37 dirs), the monorepo, `_quarantine/`, and `_defaults.json`.

### Verdict: NO gameworld skill directory exists on disk (live or quarantined) — but there are 3 real references
A dir-name + content search for `gameworld | game-world | agent-arena | autobattler | auto-battler |
agent-world | task-monster | domain-empire | skillcraft | skill-refinery` returned **zero skill
directories** in any location (`find … -type d` empty, including `_quarantine/`). The terms appear
only as *references inside other skills*:

1. **`gameworld-generator` — CLAIMED but NOT ON DISK (the key finding).**
   `understand-bangerlab/reference.md:16` lists: `| Gameworld generator | ~/.claude/skills/gameworld-generator/ | WORKS — Isaac built during quota |`.
   **That path is EMPTY** — `/home/GOD/.claude/skills/gameworld-generator/` does not exist, nor does any
   `*gameworld*` dir anywhere (`/home/GOD`, `/tmp`, monorepo, quarantine — all searched). This is an
   **encoded-certainty claim ("WORKS") that does not match disk reality now** (the exact stale-marker
   failure mode the global rules warn about). Either it was never committed to a skills dir, lived in a
   since-reset `~/.claude/skills`, or the claim is aspirational. **As of 2026-06-06: NOT FOUND.**

2. **"Gameworld (WoS)" = identified with World of Skillcraft.**
   `understand-bangerlab/SKILL.md:74` (Strategic Vision): *"Gameworld (WoS) as L6 skill refinery."*
   So **Gameworld ≡ WoS = the World of Skillcraft team pattern** (the same pattern #8 found). And
   `understand-teams/resources/overview.md:88+` describes WoS as a **literally game-shaped** system:
   multiple Claude instances coordinating through a shared **`game.json`** ("gold, trade board, quest
   log"), with **`execute.sh`** holding "ALL game logic" and a dumb **WebSocket `ServerAgent.js`**.
   → The closest thing to a "gameworld skill" that ACTUALLY EXISTS is **`understand-teams`** (the WoS
   pattern), which is a real, equipped skill — but it is a *team-coordination* skill, not a
   gameworld/RPG product skill.

3. **`understand-gear` — adjacent gamification, NOT gameworld.**
   `/tmp/heaven_data/skills/understand-gear/` — "GEAR = Gear, Experience, Achievements (wrt) Reality —
   gamified PAIA progression with goldenization spectrum and achievement tiers." A real skill; it
   supplies the RPG-stat/science-dashboard metaphor used across the `*World`s (the "GEAR scoring"
   PromptWorld deferred). Related framing, but not a gameworld game.

### Also checked
- **`/tmp/agent_world_game/`** has **NO `SKILL.md` and NO skillset** — just 4 design `.md` files
  (`README`, `CONCEPT_ART`, `NPC_DIALOGUE`, `TECHNICAL_IMPLEMENTATION`). Confirmed: design-only, no skill.
- **`_defaults.json`** (the equipped-skillset manifest) has **no** game/arena/battle/rpg/gameworld
  entries.
- The only other content hits (`compile-claude-code-component`, `understand-cb-dsl`) match on incidental
  words (WoS mention / "battle" / "arena" in unrelated prose), not gameworld skills.

### Honest bottom line
**There are NO gameworld / agent-arena / autobattler skills on disk.** The one named skill
(`gameworld-generator`) is referenced as "WORKS" in `understand-bangerlab` but its path is empty
(stale/aspirational — flag for Isaac: did it ever get committed, or was it lost in a `~/.claude/skills`
reset?). "Gameworld" in the live skill corpus means **World of Skillcraft** (the shared-`game.json`
team pattern in `understand-teams`) used as an "L6 skill refinery" — consistent with #8's finding that
gameworld is "a different pattern," and with WoS being a *team-coordination* mechanism rather than a
built domain world. `understand-gear` is the adjacent gamification skill, not a gameworld.

**Search citations:** `understand-bangerlab/{SKILL.md:74,reference.md:16}`,
`understand-teams/{_metadata.json:5, resources/overview.md:88+}`, `understand-gear/SKILL.md`,
`/tmp/agent_world_game/` (no SKILL.md), `_defaults.json` (no matches),
`find … -type d -iname '*gameworld*'` (empty in `/home/GOD`, `/tmp`, monorepo, `_quarantine`).
