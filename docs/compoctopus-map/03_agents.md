# Compoctopus Map — Slice 03: THE AGENTS

> Scope: the agent system-prompt BLOCKS + their factories under
> `application/compoctopus/compoctopus/`. CODE is the source of truth; every claim is
> cited `file.py:line`. IS = verified in code. STUB/BROKEN/VISION marked explicitly.
>
> Hypothesis under test: *the SET of these agent system-prompt blocks is the "attention
> chain that bootstraps compoctopus."*

---

## 0. The two layers of "agent" in this codebase (read this first)

There is a deliberate, code-confirmed split:

- **`compoctopus/agents/<x>/`** — the **product pipeline agents** (the ones this slice
  maps): planner, bandit, octopus_coder, mermaid_maker, ralph, pilot. These are the
  agents that turn a PRD into code.
- **`compoctopus.octohead`** — the **head / chat front-end** (top-level module, not under
  `agents/`). It is the conversational face you talk to; it writes PRDs and triggers builds.

Every agent is a `CompoctopusAgent` (`compoctopus/agent.py:58`), a dataclass that wraps a
**`chain`** (a `Chain`/`EvalChain`/`Link` of SDNA steps) — see fields at `agent.py:76-84`.
`execute()` just runs `self.chain.execute(ctx)` (`agent.py:126-143`). So an "agent's
identity" = its `system_prompt` PromptSection(s) **plus** the per-phase goal strings baked
into its SDNACs.

**IMPORTANT IS/BROKEN finding up front:** `CompoctopusAgent` has **no** `state_machine`,
`hermes_config`, or `ariadne_elements` fields (only `chain`, `system_prompt`,
`mermaid_spec`, `tool_manifest`, `task_spec`, `arm_kind`, `model`, `modules` —
`agent.py:76-84`). Yet `agents/mermaid_maker/factory.py:87-91` constructs
`CompoctopusAgent(..., state_machine=sm, hermes_config=hermes, ariadne_elements=...)`.
Those kwargs do not exist on the dataclass → **`make_mermaid_maker()` raises `TypeError`
on construction**. The same broken signature appears across the `arms/*` compilers
(grep: `arms/{chain_compiler,agent_config,input_prompt,skill,mcp_compiler,reviewer,
system_prompt}/factory.py` all pass `state_machine=/hermes_config=/ariadne_elements=`).
**Only `octopus_coder`, `planner`, `bandit`, `compoctopus`(top) actually build with the
real dataclass fields.** Mark mermaid_maker as **BROKEN/STUB** for this reason.

---

## 1. OctoHead — the head (chat / PRD front-end)

- **File:** `compoctopus/octohead.py`
- **ROLE (one line):** The conversational front-end of Compoctopus — guides the user
  through design → PRD → queue, and is the surface that triggers builds and one-shot
  self-improvement cycles. It does NOT build code itself; it emits PRD files and flags.
- **Factory:** `make_octohead(system_prompt="", tools=None, name="compoctopus",
  model="minimax")` → `HeavenAgentConfig` (`octohead.py:93-132`). NOT a `CompoctopusAgent`
  / not a chain — it is a plain Heaven chat agent config you load into any channel (CLI,
  Conductor, Discord). Model actually set: `MiniMax-M2.5-highspeed` (`octohead.py:119`),
  temp 0.7, `max_tokens=8000`, `skillset="octohead"`, MCP `llm-intelligence` attached
  (`octohead.py:125-131`).
- **SYSTEM-PROMPT BLOCK (`OCTOHEAD_SYSTEM_PROMPT`, `octohead.py:18-65`) — the identity:**
  > "You are OctoHead — the chat interface to Compoctopus, the self-compiling agent
  > compiler. You guide the user through building agents, prompts, and systems. You
  > operate in phases."
  6 conversational phases (prose, not a coded SM): (1) Talk about system/design,
  (2) Conceptualize PRD, (3) Refine PRD, (4) Queue PRD [call **CreatePRD** → writes a
  `.🪸` coral file, then **BuildPRD** → daemon queue], (5) Review results (`.🏄`),
  (6) "Go Auto" → **GoAuto** one autonomous self-improvement cycle (singleton).
  Behavioral assertions are stressed as "non-negotiable" — they define correctness.
- **STATE MACHINE:** **None** in code. The "phases" are prose in the system prompt; the
  only enforcement is the tools it can call. (IS)
- **TOOLS** (`OCTOHEAD_TOOLS`, `octohead.py:69-90`, all built via
  `make_heaven_tool_from_docstring`):
  - **CreatePRD** (`tools/create_prd_tool.py`) — writes a typed `PRD` to the build queue;
    refuses if `behavioral_assertions` is empty (`create_prd_tool.py:81-86`).
  - **BuildPRD** (`tools/build_prd_tool.py`) — sends a `.🪸` to the daemon queue.
  - **GoAuto** (`tools/go_auto_tool.py`) — writes a `.🤖` flag to `COMPOCTOPUS_AUTO_QUEUE`;
    singleton (refuses if a flag already exists, `go_auto_tool.py:65-72`).

---

## 2. Planner — PRD → GIINT hierarchy

- **Files:** `agents/planner/factory.py`, `agents/planner/prompts.py`
- **ROLE:** Decomposes a PRD into the GIINT work hierarchy
  Project → Feature → Component → Deliverable → Task, persisted via the
  `llm-intelligence` MCP (`factory.py:1-14`). It is a sequential `Chain` (no loops).
- **SYSTEM-PROMPT BLOCK — note there are TWO, and the factory uses its OWN inline one:**
  - The one actually wired into the built agent is the **inline** `PLANNER_SYSTEM_PROMPT`
    in `factory.py:32-50`:
    > "You are the Planner — the task decomposition arm of Compoctopus. Your job: take a
    > PRD … and decompose it into the GIINT hierarchy using the llm-intelligence MCP
    > tools … You MUST call these tools to persist the hierarchy. You MUST NOT just
    > describe the hierarchy in text."
  - A *second*, mermaid-driven `PLANNER_SYSTEM_PROMPT` lives in `prompts.py:74-98` (wraps
    a full `PLANNER_MERMAID` sequenceDiagram as `<EVOLUTION_WORKFLOW>` with strict rules
    and `complete_task=...` / `GOAL ACCOMPLISHED` keywords). **`factory.py` does NOT import
    or use the prompts.py version** — it defines its own. So the mermaid identity is
    **dormant/VISION** for the planner as currently assembled. (IS: factory's inline
    prompt is the live one; `factory.py:18` imports only `SystemPrompt, PromptSection`,
    not the prompts module.)
- **STATE MACHINE:** **None.** It is a `Chain` of 5 SDNACs, one per phase, run in order
  (`factory.py:166-175`): `project → features → components → deliverables → tasks`. Each
  phase's instructions come from `PHASE_INSTRUCTIONS` (`factory.py:52-78`), baked into the
  SDNAC goal (`factory.py:86-97`). No KeywordBasedStateMachine, no cycles.
- **TOOLS:** `BashTool`, `NetworkEditTool` (`factory.py:114,161-162`) + `llm-intelligence`
  MCP (`LLM_INTELLIGENCE_MCP`, `factory.py:24-30`) wired into each SDNAC's `HermesConfig`
  (`factory.py:130-146`, model `minimax`, `max_turns=30`, `bypassPermissions`).
  Fallback when SDNA isn't importable → a `ConfigLink` (test-mode, `factory.py:104-111`).

---

## 3. Bandit — worker selector (TWO distinct implementations)

There are **two** "Bandit"s in the codebase. Both are real code; they are different things.

### 3a. `agents/bandit/factory.py` — the pipeline Bandit (mechanical, NO LLM)
- **ROLE:** Pick which worker handles a task, using tag-similarity history; the
  "multi-armed bandit" exploit step in the pipeline. Currently always resolves to
  `"octopus_coder"` unless a prior successful request with matching tags exists.
- **SYSTEM-PROMPT BLOCK:** trivial, two tiny PromptSections (`factory.py:93`):
  > IDENTITY: "You are the Bandit." / WORKFLOW: "1.SETUP 2.TAG 3.SELECT 4.DISPATCH
  > 5.RECORD"
  — but **no LLM ever reads it**: every link is a `FunctionLink` (pure Python). The
  prompt is decorative. (IS)
- **STATE MACHINE:** **None.** A `Chain` of 6 `FunctionLink`s (`factory.py:92`):
  `setup → extract_tags → pass_through → select → dispatch → record`. Tag extraction =
  first 3 words >3 chars (`factory.py:21-23`); selection reads JSON history via
  `request_io.py` (`find_similar_requests`, `request_io.py:48-66`); default worker hard-
  coded `octopus_coder` (`factory.py:56`).
- **TOOLS:** none (mechanical file I/O only, via `bandit.request_io`).

### 3b. `compoctopus/bandit.py` + `router.py` — the explore/exploit Compiler Bandit (VISION-ish)
- **ROLE:** The "head of the octopus": `Bandit(Compiler)` chooses **ChainSelect** (exploit
  a proven *golden chain*) vs **ChainConstruct** (explore: assemble a new pipeline of
  compiler *arms*), records reward, and graduates configs to golden chains
  (`router.py:215-377`). This is the richer design described in the module docstrings.
- **SYSTEM-PROMPT BLOCK:** none — it is a Python `Compiler` class, not a chat agent.
- **STATE MACHINE:** none here; decision logic is `select-then-construct` Python
  (`router.py:248-282`). Graduation threshold logic in `record_execution`
  (`router.py:322-370`).
- **STATUS:** **Not wired into the live PRD pipeline.** `make_compoctopus` (§7) dispatches
  every task straight to `octopus_coder` and only *mentions* the Bandit in comments
  ("In full Compoctopus, the Bandit routes each task", `compoctopus.py:83`). So 3b is
  **VISION / not-on-the-happy-path**. (IS, by reading `compoctopus.py:82-106`.)

---

## 4. OctoCoder (🐙 Coder) — the bootstrap kernel coding agent

- **Files:** `agents/octopus_coder/factory.py`, `.../prompts.py`, `.../reference_tests.py`
- **ROLE:** The core code-compiler. Takes a `spec`+`workspace`, runs the **Annealing
  Cycle** to produce tested, working code. Called "the Compoctopus bootstrap kernel."
- **SYSTEM-PROMPT BLOCK — the identity (two copies, both used):**
  - Per-SDNAC shared prompt `_CODER_SYSTEM_PROMPT` (`factory.py:43-76`):
    > "You are the 🐙 Coder — the Compoctopus bootstrap kernel. You compile understanding
    > into code. You explore, learn, stub, fill, test, and iterate until the code works."
    Then container context (`antigravity_python_dev`, absolute `/tmp` paths, BashTool for
    all I/O) + **MANDATORY TESTING RULES**: BOTH *structural* and *behavioral* tests are
    required; a behavioral test must `await agent.execute(ctx)` for real (real MiniMax
    calls, "a test that passes in under 5 seconds … is FAKE"). Appends
    `REFERENCE_TESTS_PROMPT` (`reference_tests.py:99-156`, good vs bad test patterns) +
    `OCTO_SYNTAX_REFERENCE`.
  - Agent-level `system_prompt` PromptSections (`factory.py:222-267`): IDENTITY (the
    Annealing Cycle `STUB → TESTS → PSEUDO → ANNEAL → VERIFY → (cycle)` — "You never start
    over. You refine."), OCTO_SYNTAX, TOOLS ("You have one tool: BashTool"), SANDBOX
    (workspace-only safety).
  - **`.🐙`/`.octo` annealing-syntax reference** (`prompts.py:7-90`): `#>> STUB / #| code /
    #<< STUB` markers stripped at anneal to produce real target-language code. This syntax
    is the heart of OctoCoder's identity.
- **STATE MACHINE:** **EvalChain, NOT a KeywordBasedStateMachine.** Built in
  `make_octopus_coder` (`factory.py:211-217`):
  - flow = `Chain([stub, tests, pseudo, anneal])` (4 SDNACs)
  - evaluator = `verify` SDNAC
  - `max_cycles=5`, `approval_key="approved"`
  - **States/transitions:** STUB → TESTS → PSEUDO → ANNEAL → VERIFY; on VERIFY failure the
    EvalChain loops back to STUB **on top of existing work** (failure feeds
    `IMPLEMENTATION_PLAN.md`, `prompts.py:224-246`), up to 5 cycles. Terminal = verify
    approves. (`min_sm_cycles` does not apply — this is an EvalChain; the analogous knob is
    `max_cycles=5`.) Per-phase instructions in `CODER_STATE_INSTRUCTIONS`
    (`prompts.py:120-247`). Each phase is a fresh SDNAC (fresh LLM conversation).
  - **Self-referential bootstrap detail (IS):** the STUB phase literally tells the agent to
    `cat /tmp/compoctopus/compoctopus/agents/octopus_coder/factory.py` and "READ THE CODE
    THAT BUILT YOU … The agent you produce MUST follow this same pattern" (`prompts.py:
    139-144`). OctoCoder is instructed to reproduce its own construction pattern.
- **TOOLS:** `BashTool` (+ `NetworkEditTool`) for ALL file ops (`factory.py:128-130,
  197-200`); SDNAC `HermesConfig` model `minimax`, `max_turns=30`, `bypassPermissions`
  (`factory.py:151-166`). Test-mode fallback → `ConfigLink` (`factory.py:115-125`).
- **`CodeCompiler(Link)`** (`factory.py:276-310`): a Link wrapper whose `execute()` builds
  and runs an OctoCoder from `ctx["spec"]`.

---

## 5. MermaidMaker — writes the executable sequence-diagram programs

- **Files:** `agents/mermaid_maker/factory.py`, `.../prompts.py`
- **ROLE:** Generates evolution-system-style mermaid `sequenceDiagram`s that *other* agents
  follow as executable programs ("The mermaid you write IS the program the agent will
  follow", `prompts.py:53`). It validates its own output with the mermaid CLI and loops
  until VALID.
- **SYSTEM-PROMPT BLOCK (`MERMAID_MAKER_SYSTEM_PROMPT`, `prompts.py:21-60`):**
  > "You are the MermaidMaker — you generate evolution-system-style mermaid sequence
  > diagrams that LLM agents follow as executable programs."
  Injects 3 spec files (`mermaid_rules.md`, two example mermaids — read from `../specs`,
  `prompts.py:8-19`), a WORKFLOW (write → `python3 -m compoctopus.mermaid.cli` → fix →
  loop until "VALID:") and CRITICAL rules (every `update_task_list` task needs a matching
  `complete_task`; always end `GOAL ACCOMPLISHED`).
- **STATE MACHINE:** **YES — the only agent in this slice that defines a real
  `KeywordBasedStateMachine`** (`factory.py:24-52`):
  - states: **GENERATE → DONE**
  - `initial_state="GENERATE"`, `terminal_states={"DONE"}`, transitions
    `{"GENERATE": ["DONE"]}`
  - `min_sm_cycles`: **not set** (the KeywordBasedStateMachine call passes no
    `min_sm_cycles`; `factory.py:24-52`).
  - GENERATE goal = write mermaid for `{agent_name}`/`{tool_list}`/`{workflow_description}`,
    validate via CLI, loop until VALID, output `DONE`.
- **TOOLS:** `BashTool` only (`factory.py:80`), `HermesConfig` model `minimax`,
  `max_turns=15`.
- **STATUS = BROKEN/STUB:** as noted in §0, the factory returns
  `CompoctopusAgent(..., state_machine=sm, hermes_config=hermes, ariadne_elements=...)`
  (`factory.py:87-91`) — **none of those are fields of `CompoctopusAgent`** (`agent.py:
  76-84`) → construction raises `TypeError`. So the SM is *defined* but the agent cannot
  currently be built. (IS, by reading both files.)

---

## 6. Ralph — the TDD coding arm (N fresh runs, MoE lottery)

- **Files:** `agents/ralph/factory.py`, `.../prompts.py`, `.../core.py`
- **ROLE:** A TDD coding agent that runs **N independent fresh SDNAC conversations** over a
  shared git worktree, given a pre-built implementation plan (callgraph + requirements).
  "Fold-over-fold erases pattern violations" (`factory.py:1-18`). Each run writes tests,
  codes to green, runs codenose, and on success commits + opens a PR.
- **SYSTEM-PROMPT BLOCK (`RALPH_SYSTEM_PROMPT`, `prompts.py:3-41`):**
  > "You are Ralph — a TDD coding agent. You receive an implementation plan that contains:
  > 1. Requirements 2. Complete callgraph … Your job is Test-Driven Development …"
  Rules: tests before impl; use ONLY patterns in the callgraph ("Do NOT invent new
  patterns"); "Do NOT search for code — everything you need is in the plan"; run
  `python3 -m codenose`; finish by commit → push → `gh pr create` → say DONE. **Emanations
  section:** after coding, create `add_skill_to_target_starsystem` /
  `add_rule_to_target_starsystem` via the dragonbones MCP.
- **STATE MACHINE:** **None — explicitly NOT a loop/EvalChain.** Architecture is a Python
  `for i in range(N): fresh_sdnac.execute({})` (`factory.py:257-268`); each `_make_fresh_
  sdnac` is a brand-new conversation with an INVARIANT prompt (`factory.py:130-205`). Disk
  state is what changes between runs. Default `n_runs=8`. There is **no `make_ralph()` →
  `CompoctopusAgent`**; the entry points are `run_ralph(...)` (`factory.py:212`) and
  `launch_ralph_compoctopus(...)` (`core.py:142`), which first calls context-alignment
  `analyze_dependencies` to build the plan (`core.py:27-39, 81-139`).
- **TOOLS:** `BashTool`, `NetworkEditTool` (`factory.py:166-168`) + `dragonbones` MCP for
  emanations (`DEFAULT_AGENT_CONFIG`, `factory.py:40-53`). Model `minimax` (m2.7-highspeed),
  `max_turns=99`, `bypassPermissions`. Git worktree isolation (`factory.py:94-114`).

---

## 7. Pilot — the starship-pilot launcher (writes reqs, dispatches Ralph; never codes)

- **Files:** `agents/pilot/factory.py`, `.../prompts.py`, `.../tools.py`, `.../core.py`
- **ROLE:** A queue-driven orchestrator that evolves a *starsystem*: it manages a
  pending/processing/done/response queue, and for each item launches a pilot agent whose
  logic lives in the **`starship_pilot_flight_config` waypoint flight**, not in Python
  (`factory.py:1-14`). The pilot writes a requirements doc and dispatches **Ralph**; it
  NEVER writes code itself (enforced by a hook).
- **SYSTEM-PROMPT BLOCK (`PILOT_SYSTEM_PROMPT`, `prompts.py:7-39`, templated per
  starsystem via `build_pilot_system_prompt`, `prompts.py:84-93`):**
  > "You are the Starship Pilot for starsystem: {starsystem_name}. You NEVER write code.
  > You write task lists and requirements docs. Ralph writes code."
  Workflow: (1) `get_dependency_context` via context-alignment MCP, (2) write
  `/tmp/pilot_reqs/reqs.md`, (3) dispatch ralph via `run_ralph.sh` (BLOCKS), (4) check the
  PR via `gh`, (5) merge or re-dispatch. Plus an Emanations section (dragonbones
  skills/rules) and an injected **CartON starsystem knowledge graph** (English triplets,
  `prompts.py:42-82`).
- **STATE MACHINE:** **None in Python** — the pilot's control flow is the external
  `starship_pilot_flight_config` waypoint flight (`PILOT_FLIGHT_CONFIG`, `factory.py:33`).
  The factory just runs ONE SDNAC with `max_turns=10` (`factory.py:216-274`). State is
  carried by the on-disk queue (`submit_deliverable/submit_task/submit_ovp_response/
  process_queue/resume_from_ovp`, `factory.py:45-107, 311-388`) and the OVP approve/reject
  flow.
- **TOOLS:** `BashTool` only, but with a **BEFORE_TOOL_CALL write-blocking hook**
  (`tools.py:38-77`): every bash write op is blocked except an allowlist (run_ralph.sh,
  `gh pr`, writes to `/tmp/pilot_reqs/`, `/tmp/heaven_data/`, the done-signal). Rich MCP
  surface (`factory.py:233-268`): `context-alignment`, `starlog`, `starship`, `waypoint`,
  `carton`, `dragonbones`. `skillset="starship-pilot"`,
  `carton_identity="{starsystem}_Starship_Pilot"`, model `MiniMax-M2.7-highspeed`.

---

## 8. How OctoHead is the "head," and how the self-compilation bootstrap works

**OctoHead = the chat head; the pipeline = the body.** You talk to OctoHead
(`make_octohead`, a Heaven chat config, §1). Through conversation it fills a typed PRD and
calls **CreatePRD** → a `.🪸` coral file, then **BuildPRD** → drops it in the daemon queue.

**The build pipeline (daemon side):**
`compoctopus/daemon.py` polls for `.🪸` files (`daemon.py:77-83`) → calls
`run_from_prd(coral)` (`run.py:23`) → `make_compoctopus(prd, workspace)`
(`compoctopus.py:26`) → `agent.execute({prd, workspace, spec})` (`run.py:54-59`) → writes a
`.🏄` surf report (`run.py:78-90`). File lifecycle `.🪸 → .🐙 → .🏄` matches OctoHead's
prompt (`octohead.py:57-63`).

**What `make_compoctopus` actually assembles (IS, `compoctopus.py:118-122`):**
`Chain([ planner, dispatch_link ])` — i.e. **Planner → dispatch → OctoCoder**. The
`dispatch_tasks` function reads the GIINT tasks the Planner persisted and sends **each task
straight to `workers["octopus_coder"]`** (`compoctopus.py:82-106`). The **Bandit is only a
comment** here ("In full Compoctopus, the Bandit routes each task", `compoctopus.py:83`) —
so the documented `Planner → Bandit → OctoCoder` is **partly VISION**: Planner and OctoCoder
are live; Bandit routing is not wired into this path. MermaidMaker and Ralph/Pilot are not
in `make_compoctopus` at all — they are separate agents/entry points.

**The self-compilation loop (`GoAuto`, `auto_daemon.py`):** OctoHead's **GoAuto** tool
writes a `.🤖` flag (`go_auto_tool.py:74-83`). `compoctopus/auto_daemon.py` watches the auto
queue and, per flag: git-pulls latest develop, **reinstalls compoctopus from fresh source**
(`auto_daemon.py:71-74`), force-reimports all `compoctopus*` modules (`auto_daemon.py:
81-83`), then runs **OctoHead in introspection mode** over its own source tree
(`auto_daemon.py:85-90`, `find …/compoctopus -name '*.py'`) → generates PRDs → runs the
build daemon on them → commits to a feature branch → opens a PR to develop (`auto_daemon.py:
1-17`). **This is the "result goes back into OctoHead's identity":** OctoHead reads its own
codebase, writes PRDs to improve it, the pipeline builds them, the PR (once accepted) becomes
the new source that the *next* reinstall loads — OctoHead literally recompiles the system it
is the head of. IMPROVEMENT_RULES (`go_auto_tool.py:25-37`) constrain this introspection.

---

## 9. ASCII — the agent pipeline (who hands what to whom)

```
                          ┌─────────────────────────────────────────────┐
   user  <───chat───>     │  OCTOHEAD  (head; HeavenAgentConfig)          │
                          │  phases: design→PRD→refine→queue→review→auto  │
                          │  tools: CreatePRD · BuildPRD · GoAuto         │
                          └───────┬───────────────────────┬──────────────┘
                  CreatePRD .🪸   │                        │  GoAuto .🤖
                  + BuildPRD      │                        │  (singleton)
                                  v                        v
                       ┌──────────────────┐     ┌────────────────────────┐
                       │ daemon.py polls  │     │ auto_daemon.py polls    │
                       │ .🪸 coral queue  │     │ .🤖 flag queue          │
                       └────────┬─────────┘     │ git pull → reinstall →  │
                                │               │ OctoHead introspects    │
                                │               │ its OWN source → PRDs ──┼──┐
                                │               │ → PR to develop         │  │  (loop:
                                │               └────────────────────────-┘  │  new source
                                v                                            │  feeds next
                  run_from_prd → make_compoctopus()                          │  reinstall)
                                │                                            │
              CompoctopusAgent.chain = Chain([ PLANNER , dispatch_link ])    │
                                │                                            │
            ┌───────────────────┘                                           │
            v                                                               │
   ┌──────────────────┐   GIINT hierarchy (Project→Feature→Component→        │
   │  PLANNER (Chain) │   Deliverable→Task) persisted via llm-intelligence   │
   │  5 SDNACs        │   MCP                                                │
   └────────┬─────────┘                                                     │
            │  dispatch_tasks() reads tasks                                  │
            v                                                                │
   ┌──────────────────┐   [ BANDIT route = comment-only / VISION here;       │
   │  dispatch_link   │─ ─ ┐  agents/bandit (FunctionLinks, no LLM) and       │
   └────────┬─────────┘    └─ router.Bandit (Compiler explore/exploit) exist │
            │  each task →      but are NOT wired into make_compoctopus ]     │
            v                                                                │
   ┌──────────────────────────────────────────┐                             │
   │  OCTOCODER (EvalChain, max_cycles=5)       │  produces tested code ──────┘
   │  STUB → TESTS → PSEUDO → ANNEAL → VERIFY   │  (→ .🏄 report)
   │            ^___________________| (fail)    │
   └──────────────────────────────────────────┘

   SEPARATE / ADJACENT agents (not in make_compoctopus' chain):
     MERMAIDMAKER (KeywordBasedStateMachine GENERATE→DONE) — BROKEN ctor (TypeError)
     PILOT (waypoint flight; queue-driven; never codes) ──dispatches──> RALPH
     RALPH (N fresh SDNAC runs; TDD; codenose; opens PR) — the coding arm Pilot drives
```

---

## 10. Quick reference table

| Agent | File | Returns | State machine | LLM? | Tools |
|---|---|---|---|---|---|
| OctoHead | `octohead.py` | `HeavenAgentConfig` | none (prose phases) | yes (chat) | CreatePRD, BuildPRD, GoAuto + llm-intelligence MCP |
| Planner | `agents/planner/factory.py` | `CompoctopusAgent` | none (Chain, 5 SDNACs) | yes | Bash, NetworkEdit + llm-intelligence MCP |
| Bandit (pipeline) | `agents/bandit/factory.py` | `CompoctopusAgent` | none (Chain, 6 FunctionLinks) | **no** | none (mechanical) |
| Bandit (compiler) | `bandit.py`/`router.py` | `Bandit(Compiler)` | none (select/construct) | no | (VISION; not wired) |
| OctoCoder | `agents/octopus_coder/factory.py` | `CompoctopusAgent` | **EvalChain** (5 phases, max_cycles=5) | yes | BashTool (+NetworkEdit) |
| MermaidMaker | `agents/mermaid_maker/factory.py` | `CompoctopusAgent` (**TypeError**) | **KeywordBasedStateMachine** GENERATE→DONE | yes | BashTool |
| Ralph | `agents/ralph/factory.py` | `run_ralph()` dict | none (N fresh runs) | yes | Bash, NetworkEdit + dragonbones MCP |
| Pilot | `agents/pilot/factory.py` | queue ops + SDNAC | none (external waypoint flight) | yes | BashTool(+write-block hook) + 6 MCPs |
