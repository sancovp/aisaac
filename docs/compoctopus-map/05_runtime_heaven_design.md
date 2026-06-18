# Compoctopus Map 05 — Runtime / Daemon / Heaven-Integration + Design Narrative

Scope: how compoctopus RUNS autonomously, how it sits on **heaven**, and the
self-compilation **bootstrap** narrative from `DESIGN.md`.

Convention used throughout:
- **IS** — verified by reading the actual code (cited `file:line`).
- **VISION** — stated in `DESIGN.md` only; not (or not yet) in code. `DESIGN.md`
  self-labels `Status: ASPIRATIONAL` at `DESIGN.md:4`.

All code paths are under
`/home/GOD/gnosys-plugin-v2/application/compoctopus/`. The package root holds
`auto_dev.py` and `heaven_patch/`; the importable package is `compoctopus/`.

---

## 1. How it runs autonomously (IS — code)

There are **two independent run loops** plus a manual one-shot entrypoint. Both
loops are dumb directory-pollers over emoji-suffixed files.

### 1a. Build daemon — `compoctopus/daemon.py` (the `.🪸 → .🏄` loop)

The build daemon (`daemon.py:67` `daemon_loop`) polls a queue dir
(default `/tmp/compoctopus_daemon_queue`, `daemon.py:26`) every `interval` seconds
(default 5, `daemon.py:27`) for `*.🪸` (coral / PRD) files:

```
daemon_loop (daemon.py:77):
  while True:
    corals = sorted(queue.glob("*.🪸"))         # daemon.py:78
    for coral in corals: await process_coral(coral)
    await asyncio.sleep(interval)
```

`process_coral` (`daemon.py:30`):
1. `from compoctopus.run import run_from_prd` and `await run_from_prd(coral)` (`daemon.py:32,37`).
2. On success logs `🏄 Build complete` (`daemon.py:38`); on exception writes an
   error `.🏄` report (`daemon.py:50-57`).
3. Moves the processed coral into a `done/` subdir (`daemon.py:59-63`).

`run_from_prd` (`run.py:23`) is the actual pipeline driver — IS:
- loads the `.🪸` JSON → `PRD.from_dict` (`run.py:41-43`);
- builds a workspace dir (`run.py:48-51`);
- `agent = make_compoctopus(prd, workspace)` then `await agent.execute({...})`
  (`run.py:54-59`);
- walks the workspace, writes a `.🏄` report next to the PRD (`run.py:62-90`).

`run_from_prd_sync` (`run.py:104`) is a sync wrapper. `run_autonomously()`
(`run.py:109`) — the "no-PRD meta mode" — is **`raise NotImplementedError`**
(`run.py:111-114`). So the autonomous "compile yourself with no input" entry is
VISION, not built.

The build daemon is auto-started on demand by `BuildPRDTool._ensure_daemon_running`
(`tools/build_prd_tool.py:23`), which `pgrep`s for `python -m compoctopus.daemon`
and `Popen`s it if absent (`build_prd_tool.py:26-47`).

### 1b. Auto-dev daemon — `compoctopus/auto_daemon.py` (the `.🤖` loop)

This is the self-improvement loop. `daemon_loop` (`auto_daemon.py:238`) polls
`AUTO_QUEUE` (default `/tmp/compoctopus_auto_queue`, `auto_daemon.py:40`) for
`*.🤖` flag files, **processing only the first and deleting extras**
(`auto_daemon.py:248-258` — "Only one .🤖 at a time").

`process_flag` (`auto_daemon.py:182`) reads `{focus, rules}` from the flag JSON
(`auto_daemon.py:190-192`) and runs one cycle:
1. `git_pull_latest()` — clone or `git reset --hard origin/develop` into
   `/tmp/compoctopus_autodev_workspace` (`auto_daemon.py:56-68`, `:198`).
2. `reinstall()` — `pip install -e . --quiet` from fresh source
   (`auto_daemon.py:71-74`, `:201`). (NOTE: this `-e` editable install
   contradicts the global `pip-install-our-packages-no-deps` rule, but it is what
   the code does.)
3. `clean_daemon_queue()` (`auto_daemon.py:170`, `:204`).
4. `run_octohead_introspection(focus, rules)` (`auto_daemon.py:77`, `:207`) — the
   introspection step (see below).
5. `wait_for_builds()` — block until the **build daemon** drains the `.🪸`s it
   produced and `.🏄` reports appear (`auto_daemon.py:114`, `:213`).
6. `commit_and_pr(focus)` — new `auto-dev/<ts>` branch, `git add -A`, commit, push,
   `gh pr create --base develop` (`auto_daemon.py:130-167`, `:216`).
7. `finally:` always `flag_path.unlink()` and delete any extra flags
   (`auto_daemon.py:226-235`).

The `.🤖` trigger is written by `GoAuto` (`tools/go_auto_tool.py:40` `go_auto`):
it refuses if a `.🤖` already exists (`go_auto_tool.py:66-72` — singleton, gated by
PR acceptance), else writes `auto_dev_<ts>.🤖` with `{timestamp, focus, rules}`
(`go_auto_tool.py:74-84`).

**Introspection** (`run_octohead_introspection`, `auto_daemon.py:77`): force-reimports
all `compoctopus.*` modules (`auto_daemon.py:81-83`), `find`s the `.py` tree
(`auto_daemon.py:88`), builds a prompt embedding the tree + focus + improvement
rules (`auto_daemon.py:90-97`), then `config = make_octohead()` and
`await exec_completion_style(prompt, agent=config)` (`auto_daemon.py:99-100`). The
instruction is "identify the single most impactful improvement … only ONE per
cycle." OctoHead is expected to call `CreatePRD`/`BuildPRD` to enqueue corals for
the build daemon. The `IMPROVEMENT_RULES` (`auto_daemon.py:39-59`) are the
dogfooding invariants (behavioral assertions, alignment reflects all patterns,
no orphaned code, respect the `.🪸→.🐙→.🏄` lifecycle, one focused PRD).

`auto_dev.py` (package root) is an **older, standalone variant** of the same loop
(`auto_dev.py:176` `single_cycle`, `:207` `main` with `--loop`/`--interval`). It
duplicates pull → introspect → wait → commit/PR → clean. It imports
`run_from_prd`, `make_octohead`, `CreatePRDTool`, `BuildPRDTool` (`auto_dev.py:87-91`).
Functionally the same as `auto_daemon.py` minus the per-flag git-reset/reinstall and
single-flag gating. (IS: both exist; `auto_daemon.py` is the flag-driven daemon,
`auto_dev.py` is the cron-style standalone.)

### 1c. `sensors.py` — what it senses (IS)

`SensorStore` (`sensors.py:26`) is a **thread-safe in-memory reward store** keyed by
`config_hash`. It does NOT poll anything — it RECORDS `SensorReading`s from
executions (`sensors.py:41` `record`) and computes a reward (`sensors.py:57`
`get_reward`):

```
reward = success_rate*0.4 + efficiency*0.3 + human_feedback*0.3   # sensors.py:85
  success_rate = goal_accomplished / runs                          # :71
  efficiency   = 1 - avg_turns/25                                   # :72-74
  human_feedback = avg(scores) or 0.5                              # :77-83
```

It feeds the **Construct-vs-Select bandit**: `meets_graduation_threshold`
(`sensors.py:102`) returns True when a config has `>=5` runs at `>=0.8` mean reward
— the signal to graduate a config into a "golden chain" (cache it for SELECT).
Per the module docstring (`sensors.py:8-12`), this realizes the DESIGN's "Sensors =
metrics derived from execution outcomes." NOTE: this is a library object; nothing in
the runtime loop (`daemon.py`/`run.py`) is shown wiring `SensorStore.record` into
`run_from_prd`, so the bandit reward path is built-but-not-obviously-fed in the
poller loops.

### 1d. `alignment.py` — what it aligns (IS)

`GeometricAlignmentValidator` (`alignment.py:40`) checks the **5 geometric
invariants** that every compilation output must satisfy (the "laws of the algebra,"
the core safety mechanism that prevents "compound garbage"):

1. `check_dual_description` (`alignment.py:59`) — system prompt (WORKFLOW prose) and
   input prompt (mermaid) describe the same program; cross-checks mermaid task_list
   ↔ WORKFLOW text and mermaid tool_references ↔ CAPABILITY text.
2. `check_capability_surface` (`alignment.py:148`) — every referenced tool exists
   (no PHANTOM) and every equipped tool is referenced (no ORPHAN). This is the check
   that targets the "tool call and result not match" / MiniMax 2013 error.
3. `check_trust_boundary` (`alignment.py:239`) — tool COUNT and tool CAPABILITY are
   within the trust level's limits (`TRUST_MAX_TOOLS`: ORCHESTRATOR 50 / BUILDER 20 /
   EXECUTOR 3 / OBSERVER 10, `alignment.py:232-237`); CONSTRAINTS section present.
4. `check_phase_template` (`alignment.py:319`) — every SM phase maps to a real prompt
   template.
5. `check_polymorphic_dispatch` (`alignment.py:364`) — feature type maps to a valid
   compilation path.

`validate_all` (`alignment.py:412`) runs all 5 and returns a
`GeometricAlignmentReport`. Each violation message is a long remediation string. This
is library machinery; like the sensors it is not shown being invoked inside the
poller loop — it is the validation primitive the arms/pipeline are meant to call.

---

## 2. Heaven integration — the KeywordBasedStateMachine (IS)

### 2a. KeywordBasedStateMachine — `heaven_patch/keyword_state_machine.py`

A standalone SM object you attach to a heaven agent (`keyword_state_machine.py:88`).
It is NOT a heaven subclass — it's a plain object passed via config.

- `__init__` (`:103`) validates states/initial/terminal, builds a transition map
  (explicit `transitions` dict or "all transitions allowed," `:151-170`).
- `state_keywords` (`:194`) — **the state NAMES become `additional_kws`**.
- `transition(new, reason)` (`:202`) — validates against the transition map, swaps
  `current_state`, appends history, raises on invalid/terminal-source.
- `process_kvs(extracted_content)` (`:252`) — given the agent's extracted-keyword
  dict, if a key matches a VALID next state it executes the transition and returns
  the consumed keys; logs a warning on an invalid-transition attempt
  (`:291-300`). **Only one transition per call** (`:288-289`).
- `build_transition_prompt()` (`:341`) → `build_kw_instructions()` (`:308`) — emits
  the `<STATE_MACHINE>` system-prompt block listing states, CURRENT/TERMINAL markers,
  valid next states, cycles completed, and the instruction to emit the next-state as
  an XML tag (e.g. `<ANNEAL>reason</ANNEAL>`).
- Persistence: `save_state`/`load_state` write
  `heaven_data/agents/<agent_name>/sm_<name>.json` (`:352-407`). **Refuses unnamed
  agents** (`UNNAMED_AGENTS = {None,"","default","unnamed","agent"}`, `:101`,
  `:361-367`) because persistence needs a unique dir.
- `reset()` (`:242`) increments `cycles_completed` and returns to the initial state.
- `to_mermaid()` (`:499`) renders the SM as a `stateDiagram-v2`.

### 2b. How it attaches to a heaven agent — `heaven_patch/baseheavenagent.py`

Config fields on `HeavenAgentConfig` (IS, `baseheavenagent.py:364-365`):
```
state_machine: Optional[Any] = None   # a KeywordBasedStateMachine
min_sm_cycles: Optional[int] = None   # min complete cycles before the agent may stop
```

Wiring in `BaseHeavenAgent.__init__` (`baseheavenagent.py:868-880`):
1. `self.state_machine = config.state_machine; self.min_sm_cycles = config.min_sm_cycles`.
2. If an SM is set: `self.state_machine.load_state(self.name)` (crash-resilient
   resume).
3. `from .tools.state_machine_tool import create_sm_tool; sm_tool =
   create_sm_tool(self.state_machine, self.name)` and append to `self.tools`.
4. `sm_prompt = self.state_machine.build_transition_prompt()` and **append it to the
   system prompt** (`baseheavenagent.py:880`).

**The transition is tool-driven, not parse-driven.** The actual transition path is
the `StateMachineTool` (`heaven_patch/state_machine_tool.py`):
- `create_sm_tool(sm, agent_name)` (`state_machine_tool.py:15`) builds a LangChain
  `Tool` named `StateMachineTool` with args `transition_to` + `reason`
  (`:40-57`, `:122-128`).
- Its coroutine `sm_transition_func` (`:60`) calls
  `sm.process_kvs({transition_to: reason})` (`:71`), and on success
  `sm.save_state(agent_name)` (`:75`) and returns the NEW phase's goal/prompt_suffix +
  valid next transitions as the tool result IMMEDIATELY in the same turn (`:77-98`).
- So the agent **calls a tool** to transition; the `<STATE>` XML keyword in the prompt
  is the human-readable convention, but the transition is executed by the tool call.
  (`_process_agent_response` at `baseheavenagent.py:3377` extracts `additional_kws`
  into `_current_extracted_content` (`:3449-3491`) but does NOT itself call
  `process_kvs` — confirming the tool is the driver.)

### 2c. The `min_sm_cycles` STOP-gating (the re-prompt-until-N-cycles mechanism)

In `BaseHeavenAgent.run` (`baseheavenagent.py:1556`), the outer body is
`while True:` (`:1574`). After a run completes (`:1601-1609`), the SM cycle
enforcement block (`baseheavenagent.py:1611-1623`) fires:

```python
if (self.state_machine is not None
        and self.min_sm_cycles is not None
        and self.state_machine.cycles_completed < self.min_sm_cycles):   # :1612-1614
    if self.state_machine.is_terminal:                                   # :1616
        self.state_machine.reset()                                       # :1617  → cycles_completed++
        self.state_machine.save_state(self.name)                         # :1618
    prompt = f"SM cycle {cycles+1}/{min_sm_cycles} — continue from {current_state}"  # :1620
    self.completed = False                                               # :1621
    self.goal = self.config.system_prompt                                # :1622
    continue                                                             # :1623 → loops run() again
return result                                                            # :1625
```

So: **the agent cannot truly stop until it has completed `min_sm_cycles` full
state-machine cycles.** When the agent reaches a terminal state with too few cycles
done, the SM is `reset()` (incrementing the counter), the agent is un-completed, a
continuation prompt is injected, and `run()` loops. This is the STOP-gate that forces
N complete passes (e.g. WRITE→ANNEAL→TEST→DONE, repeated) before the agent is allowed
to return.

### 2d. compoctopus-`heaven_patch` vs canonical heaven — FINDING

**The SM machinery is NOT compoctopus-only — it is identical in canonical
heaven-framework.** I diffed `heaven_patch/baseheavenagent.py` against the monorepo
canonical
`base/heaven-framework/heaven_base/baseheavenagent.py`: the canonical file has the
SAME `state_machine`/`min_sm_cycles` fields (canonical `:363-364`), the SAME
`create_sm_tool` wiring (canonical `:869-879`), and the SAME cycle-enforcement block
(canonical `:1825-1833`). So `heaven_patch/` is a **vendored snapshot of heaven**
(its imports use `from .tools...`, `from ..state_machine`, `from ..baseheaventool`),
not a unique compoctopus mechanism. The KeywordBasedStateMachine + StateMachineTool +
`min_sm_cycles` gating are a canonical heaven capability that compoctopus consumes
(e.g. `mermaid_maker.py:99` imports `from heaven_base.state_machine import
KeywordBasedStateMachine, StateConfig`). What is compoctopus-specific is only the SM
CONTENT (the state graphs the arms define), not the engine.

---

## 3. The bootstrap (DESIGN.md) — D:D→D self-compilation

`DESIGN.md` is the design artifact; `Status: ASPIRATIONAL` (`DESIGN.md:4`). This
section reports it AS design/vision and marks what the code actually backs.

### 3a. The D:D→D fixed point (the central claim)

> "The pipeline is a fixed-point endomorphism **D:D→D**. The compiler can compile
> itself. The agents it produces can produce more agents through the same pipeline."
> — `DESIGN.md:28`

> "**CompoctopusCompiler**: calls a list of AgentCompilerPipelines to produce a
> specialized version of Compoctopus itself. THIS is the D:D→D endomorphism."
> — `DESIGN.md:95`

The fixed point is later restated concretely (`DESIGN.md:1370-1387`):
> "The fixed point is: a CompoctopusAgent whose inner pipeline IS Compoctopus
> itself." with the loop `CompoctopusAgent → *Compiler → Compoctopus →
> CompoctopusAgent ─ fixed point: D(D)=D`.

### 3b. The self-compilation bootstrap of the HEAD (`DESIGN.md:109-147`)

The "head" (OctoHead) is bootstrapped by compiling better versions of itself:
```
Step 0: Generic OctoHead → writes PRD for "Prompt Engineer agent"
Step 1: PE agent (compiled by the system) → put in OctoHead → PE-powered head
        → PE-powered OctoHead writes PRD for "OctoHead Specialist"
Step 2: OctoHead Specialist (compiled by the PE-powered system) → the fixed point
Step 3: DONE — "The system eats itself into existence" (DESIGN.md:139)
```
"What you need to run this" (`DESIGN.md:141-146`) is self-marked: OctoHead wrapper ✅
(`make_octohead`), CreatePRD ✅, Planner→Bandit→OctoCoder pipeline ✅, plus two PRDs
(Step 1 / Step 2 inputs) — which are NOT marked done. **IS**: `make_octohead`
(`octohead.py:93`), `CreatePRD` (`tools/create_prd_tool.py`), and a
Planner→dispatch→OctoCoder pipeline (`compoctopus.py:26`) all exist in code.
**VISION**: the head actually re-compiling itself to a fixed point (running Steps
0→3) is described, not demonstrated in code.

### 3c. The file lifecycle (`DESIGN.md:150-157`) — IS (the daemons use exactly these)

| Ext | Name | Stage | Code that handles it |
|-----|------|-------|----------------------|
| `.🪸` | Coral | PRD file | written by `CreatePRD`→`PRD.save_to_queue`; consumed by `daemon.py:78` |
| `.🐙` | Octopus | file being compiled / the `.octo` source format | `annealer.py` + `*.octo` (e.g. `bandit.octo`) |
| `.🏄` | Surf | results report | written by `run.py:89`, `daemon.py:56` |
| `.🤖` | Robot | auto-dev trigger flag (singleton) | written by `go_auto_tool.py:83`; consumed by `auto_daemon.py:249` |

The lifecycle is real and load-bearing in the runtime — the two pollers are literally
glob loops over `.🪸` and `.🤖`.

### 3d. The filling sequence (`DESIGN.md:721-937`) — the 6-step MVP

```
Step 1: 🐙 Coder        (hand-written bootstrap kernel — "gcc stage 1")
Step 2: Bandit          (🐙 Coder codes it — "gcc stage 2, compiles itself")
Step 3: Planner         (Bandit constructs it)
Step 4: Self-atomization (Bandit feeds itself to the Planner — "gcc stage 3")
Step 5: Self-compilation (make itself, diff vs original, verify D:D→D fixed point)
Step 6: Evolve chain     (specialize into "the Compoctopus that updates Compoctopus")
```
> "After step 6, the Evolve chain IS the golden chain for self-modification. The
> system never needs us again." — `DESIGN.md:734-735`

The analogy throughout is the **GCC triple-bootstrap**: gcc-1 compiles gcc-2, gcc-2
compiles gcc-3, gcc-2 == gcc-3 (`DESIGN.md:877-878`).

### 3e. What is BUILT vs DESIGN-only — the implementation-status checklists

`DESIGN.md` carries multiple dated status checklists. The MOST RECENT (latest
evolution section, `DESIGN.md:1905-1917`) reads:
```
[x] Step 0: CompoctopusAgent type (agent.py)
[x] Step 1: 🐙 Coder — make_octopus_coder()
[x] Step 1.5: CodeCompiler Link wrapping OctoCoder
[x] Step 2: Bandit — generated by OctoCoder, 15/15 tests passing
[ ] Step 2.1: Fix OctoCoder prompts for correct annealing semantics ← NOW
[ ] Step 2.6: Bandit architecture — DECIDE → EXECUTE → REVIEW
[ ] Step 2.7: Reviewer arm
[ ] Step 3: Planner — uses GIINT MCP tools for decomposition
[ ] Step 4: Self-atomization
[ ] Step 5: Self-compilation (D:D→D verification)
[ ] Step 6: Evolve chain
```
The "Code-First Bootstrap Proof (2026-03-05)" section (`DESIGN.md:1327-1349`) records
the one concrete demonstration: OctoCoder ran on MiniMax via SDNA→Heaven, drove
`WRITE → ANNEAL → TEST → REWRITE → ANNEAL → TEST → DONE`, compiled
`bandit.octo → bandit.py` in 2 iterations, **15/15 tests passing**.

**Code cross-check (IS):**
- `agents/{bandit,octopus_coder,planner,mermaid_maker,pilot,ralph}/` all exist with
  `factory.py` + `tests/` (verified on disk). `bandit.octo`/`bandit.py` exist at the
  package root.
- `agents/bandit/tests/test_bandit.py` exists (backing the "15/15 tests" claim — I did
  not re-run it, so the PASS count is UNVERIFIED here; the artifact exists).
- `make_compoctopus` (`compoctopus.py:26`) wires Planner → dispatch → OctoCoder for
  real. **But** the dispatch link sends every task straight to the default worker —
  `"In full Compoctopus, the Bandit routes each task"` (`compoctopus.py:82-84`). So the
  **Bandit is built as an arm but is NOT routing in the live pipeline**; the runtime
  bypasses it.

**Verdict on each filling-sequence step:**
- Steps 0, 1, 1.5, 2, 2.5 → **IS** (built; arm packages + factories + the 2026-03-05
  OctoCoder→Bandit proof).
- Step 3 (Planner via GIINT MCP) → **PARTIAL** — a `make_planner` factory + planner
  package exist and `make_compoctopus` calls it, but DESIGN's own latest checklist
  marks Step 3 `[ ]` and `ProjectCompiler` is labeled "(stub)" (`DESIGN.md:1706`).
- Steps 4, 5, 6 (self-atomization, **self-compilation / D:D→D verification**, Evolve)
  → **VISION** — all unchecked `[ ]` in every status block; no code demonstrates the
  diff-against-self verification.

---

## 4. `giint_bridge.py` — connection to GIINT (IS)

`giint_bridge.py` is now a **thin re-export + one Link** (it was "gutted" from 398
lines of mirror types, `DESIGN.md:1410-1418`):
- Lines `15-49` `from llm_intelligence.projects import (...)` — re-exports the REAL
  GIINT hierarchy: enums (`TaskStatus`, `AssigneeType`, `ProjectType`), models
  (`Task`, `Deliverable`, `Component`, `Feature`, `Project`), spec models, the
  registry (`get_registry`), and the top-level mutators (`create_project`,
  `add_feature_to_project`, `add_component_to_feature`,
  `add_deliverable_to_component`, `add_task_to_deliverable`, `update_task_status`, …).
  No mirrors, no duplicates (`giint_bridge.py:5-9`).
- `ProjectCompiler(Link)` (`giint_bridge.py:91`) — a chain Link whose `execute()`
  (`:114`) reads `_goal` from context, lazily builds the Planner
  (`from compoctopus.octopus_coder import make_planner`, `:128`) and runs it
  (`:131`). Context in: `_goal` → context out: `_project_id`. The module docstring
  states the Planner agent **uses the `giint-llm-intelligence` MCP tools directly** to
  create/query the hierarchy; this Python module is only for Python-side type access
  (reading a Project after the Planner builds it) (`giint_bridge.py:5-10`).

So GIINT decomposition = "Planner agent calls the GIINT MCP" (the persistence path),
and `giint_bridge` = typed Python access + the `ProjectCompiler` wrapper that runs the
Planner inside a compoctopus chain. The runtime reads the resulting project via
`from llm_intelligence.projects import get_project` in `compoctopus.py:68`, then
`_extract_tasks` walks Feature→Component→Deliverable→Task (`compoctopus.py:143`).

---

## 5. ASCII — the autonomous run loop (IS)

```
  ┌─────────────────────────────── BRAIN (user-facing) ───────────────────────────────┐
  │  User ↔ OctoHead chat agent  (make_octohead, octohead.py:93)                       │
  │     │  CreatePRD ─────────────► writes prd_*.🪸 to working queue                    │
  │     │  BuildPRD  ─────────────► moves .🪸 → /tmp/compoctopus_daemon_queue            │
  │     │                            (+ auto-starts build daemon, build_prd_tool.py:23) │
  │     └  GoAuto    ─────────────► writes ONE auto_dev_<ts>.🤖 to /tmp/..._auto_queue  │
  └────────────────────────────────────┬───────────────────────────┬──────────────────┘
                shared volume (.🪸,.🤖) │                           │
  ┌──────── BUILD DAEMON ──────────────▼────────┐   ┌──────── AUTO-DEV DAEMON ─────────▼─────────┐
  │ daemon.py:67  poll *.🪸 every 5s             │   │ auto_daemon.py:238  poll *.🤖 (first only)  │
  │   process_coral (daemon.py:30):              │   │   process_flag (auto_daemon.py:182):        │
  │     run_from_prd(coral)  (run.py:23)         │   │     1 git reset --hard origin/develop       │
  │       PRD.from_dict                          │   │     2 pip install -e .                       │
  │       make_compoctopus (compoctopus.py:26)   │   │     3 clean_daemon_queue                      │
  │         Planner ──(GIINT MCP)──► project_id  │   │     4 OctoHead introspection (make_octohead) │
  │         dispatch_tasks: get_project          │   │         → identify 1 improvement             │
  │           → OctoCoder per task               │   │         → CreatePRD/BuildPRD → .🪸 ──────────┼──► (build daemon builds it)
  │             SM: WRITE→ANNEAL→TEST→DONE        │   │     5 wait_for_builds (.🏄 appear)            │
  │             min_sm_cycles STOP-gate          │   │     6 commit → push → gh pr create develop   │
  │       write .🏄 report (run.py:89)           │   │     finally: delete the .🤖 flag             │
  │     move coral → done/                        │   │   (singleton: one cycle until PR resolved)  │
  └───────────────────────────────────────────────┘   └─────────────────────────────────────────────┘

  Inside any heaven agent with a state_machine (baseheavenagent.py:1611):
     run() ─► [agent works, calls StateMachineTool to transition] ─► reached terminal?
        └─ if cycles_completed < min_sm_cycles: reset()(cycles++), un-complete, re-prompt, LOOP
        └─ else: return result
```

---

## Provenance / honesty notes
- All `file:line` citations are from reading the actual code in
  `application/compoctopus/`. DESIGN.md quotes are marked as design.
- `/home/GOD/core/` was excluded from all searches.
- UNVERIFIED in this pass: the "15/15 tests passing" count (the test file exists; I did
  not execute it). The DESIGN's own checklists are the authority for what its authors
  consider built vs not, and they agree with the code: arms exist; self-compilation
  (Step 5, D:D→D) and Evolve (Step 6) do not.
