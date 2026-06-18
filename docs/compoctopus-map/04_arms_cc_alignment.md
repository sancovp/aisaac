# compoctopus ARMS — the Claude-Code-component alignment layer

Scope: every file under `compoctopus/arms/` read in full, plus the base contract
(`compoctopus/base.py`), `types.py:ArmKind/FeatureType`, `router.py` (how arms wire into the
pipeline), `agent.py:CompoctopusAgent`, and the three pipeline test files. CODE is truth; cites are
`file.py:line` relative to `/home/GOD/gnosys-plugin-v2/application/compoctopus/`.

## THE LOAD-BEARING FINDING: there are TWO PARALLEL ARM FAMILIES

`arms/` contains the same 6 arms expressed twice, in two different mechanisms:

- **Family A — deterministic `CompilerArm` classes** (top-level `arms/*.py`): `chain.py`, `agent.py`,
  `mcp.py`, `skill.py`, `system_prompt.py`, `input_prompt.py`. Each is a synchronous
  `class XCompiler(CompilerArm)` (`base.py:93`) that reads/writes a shared `CompilationContext` — pure
  Python decision-trees, NO LLM. These have full `compile()` + `validate()` + `get_mermaid_spec()` +
  `get_system_prompt_sections()` + `get_tool_surface()`. **These are what the pipeline tests instantiate**
  (`tests/test_full_pipeline.py:29-34`, `test_phase1.py:112-116`, `test_phase2.py`).
- **Family B — LLM-backed `make_*()` factories** (subdir `arms/<name>/factory.py` + `prompts.py`): each
  returns a `CompoctopusAgent` (`agent.py:59`, itself a `CompilerArm`) wrapping a
  `KeywordBasedStateMachine` (ANALYZE→…→DONE) + a `HermesConfig` (`model="minimax"`, ANTHROPIC) + a
  system prompt. These delegate the compile work to an actual LLM agent run.

**`arms/__init__.py` exports ONLY Family B** (`make_*` factories) + `ReviewerCompiler`
(`arms/__init__.py:13-29`). It does NOT export the Family-A classes. Verified empirically:
`from compoctopus.arms import ChainCompiler` → `ImportError` — yet `tests/test_full_pipeline.py:18-23`
imports exactly those names from `compoctopus.arms`. **So the three pipeline tests are broken at import
against the current `__init__.py`** (a real decoherence between the test suite and the package surface;
UNVERIFIED whether they pass via some conftest path — the bare import fails). The Family-A classes are
reachable only by direct module path (`from compoctopus.arms.chain import ChainCompiler`).

Both families are legitimately `CompilerArm`s and both can be `register_arm()`'d into the router's
`_arms` dict (`router.py:121-126`), which `_default_pipeline` keys by string name
(`"chain","agent","mcp","skill","system_prompt","input_prompt"` — `router.py:193`). The registry is
populated externally; neither family is wired in by default inside the package.

---

## 1. THE ARM TABLE

| Arm (kind) | INPUT spec → OUTPUT artifact | `CompilerArm` subclass? | IS vs STUB | State machine (Family B) |
|---|---|---|---|---|
| **chain** (`ArmKind.CHAIN`) | `ctx.task_spec` (TaskSpec) → `ctx.chain_plan` (ChainPlan = DAG of ChainNodes) | A: `ChainCompiler(CompilerArm)` `chain.py:33`. B: `CompoctopusAgent` `chain_compiler/factory.py:16` | **IS** (A: full polymorphic decompose+validate `chain.py:54-213`; B: real SM+Hermes). Compiles a **CHAIN** (sequence-of-agent-steps), the chain-ontology unit. | ANALYZE→DECOMPOSE→DONE `chain_compiler/factory.py:26-34` |
| **agent** (`ArmKind.AGENT`) | `ctx.task_spec` + `ctx.chain_plan` → `ctx.agent_profile` (AgentProfile: model/provider/temp/max_turns/permission_mode) | A: `AgentConfigCompiler(CompilerArm)` `agent.py:33`. B: factory `agent_config/factory.py:18` | **IS** (A: full trust→permission/model/temp decision tree + Trust-Boundary validate `agent.py:51-171`). Compiles a **CC subagent / agent config** (HermesConfig-compatible profile). | ANALYZE→CONFIGURE→DONE `agent_config/factory.py:26-35` |
| **mcp** (`ArmKind.MCP`) | `ctx.task_spec`+`ctx.chain_plan`+`ctx.agent_profile` → `ctx.tool_manifest` (ToolManifest = MCPConfig dict) | A: `MCPCompiler(CompilerArm)` `mcp.py:32`. B: factory `mcp_compiler/factory.py:18` | **IS** (A: full hint-gather + registry-or-mock build + Capability-Surface validate `mcp.py:54-152`). Compiles a **CC MCP tool surface**. THE arm that prevents Error 2013. | ANALYZE→SELECT→DONE `mcp_compiler/factory.py:26-35` |
| **skill** (`ArmKind.SKILL`) | `ctx.task_spec`+`ctx.chain_plan` → `ctx.skill_bundle` (SkillBundle = SkillSpecs + injected_context) | A: `SkillCompiler(CompilerArm)` `skill.py:33`. B: factory `skill/factory.py:16` | **IS** (A: full hint→registry/fallback skill select + concat injected context + dup-name validate `skill.py:55-152`). Compiles **CC skills** (SKILL.md bundles). | ANALYZE→SELECT→DONE `skill/factory.py:24-33` |
| **system_prompt** (`ArmKind.SYSTEM_PROMPT`) | `ctx.task_spec`+`agent_profile`+`tool_manifest`+`skill_bundle` → `ctx.system_prompt` (XML IDENTITY/WORKFLOW/CAPABILITY/CONSTRAINTS) | A: `SystemPromptCompiler(CompilerArm)` `system_prompt.py:34`. B: factory `system_prompt/factory.py:25` | **IS** (A: full 4-section compose + mandatory-section/Dual-Description validate `system_prompt.py:58-186`). Compiles a **CC system prompt**. | IDENTITY→WORKFLOW→CAPABILITY→CONSTRAINTS→DONE `system_prompt/factory.py:36-53` |
| **input_prompt** (`ArmKind.INPUT_PROMPT`) | `ctx.task_spec`+`tool_manifest`+`system_prompt`+`skill_bundle` → `ctx.input_prompt` (goal string + mermaid + template_vars) | A: `InputPromptCompiler(CompilerArm)` `input_prompt.py:34`. B: factory `input_prompt/factory.py:19` | **IS** (A: full mermaid-aligned-to-manifest build + goal assembly + Capability-Surface validate `input_prompt.py:58-152`). Compiles a **CC input/user prompt** (the `agent.run()` goal). | ANALYZE→MERMAID→ASSEMBLE→DONE `input_prompt/factory.py:27-42` |
| **reviewer** (`ArmKind.REVIEWER`) | dict `{arm_output, original_task, arm_kind, attempt, feedback}` → `ReviewResult(passed, feedback, invariant_violations)` | `ReviewerCompiler` is a **thin wrapper, NOT a `CompilerArm`** (`reviewer/factory.py:142`, plain class). Its inner `make_reviewer()` returns a `CompoctopusAgent` (which IS a CompilerArm). | **IS as quality-gate** (real SM + Hermes + PASS/FAIL parse `reviewer/factory.py:154-178`). Reviews ALL arm outputs; it is the validator, not a component-compiler. | REVIEW→DONE `reviewer/factory.py:39-69` |

Notes on IS vs STUB: **no arm is a `NotImplementedError`/pseudocode stub** — every Family-A `compile()`
has real logic and every Family-B factory builds a real SM+Hermes. The only "not built" gaps are
explicit TODOs: MCP/Chain `get_tool_surface()` carry `# TODO Phase 2: add carton MCP`
(`mcp.py:225-227`, `chain.py:277`), and Family-B `_build_ariadne` degrades to `{}` if `sdna`/`heaven_base`
absent (`*/factory.py` `except ImportError`). The headline "stub" is structural, not per-arm: **the
Family-A classes the tests use are not exported by `arms/__init__.py`** (decoherence above).

---

## 2. THE `CompilerArm` BASE CONTRACT (`base.py:93-233`)

`CompilerArm(Link, ABC)` — **every arm IS a `Link`** in the chain-ontology (`base.py:89,93`), so an arm
composes into any `Chain`; `CompilerPipeline(Chain)` (`base.py:410`) IS a chain of arms.

Every arm MUST implement (all `@abstractmethod`):
- `kind -> ArmKind` (`base.py:112-115`) — which arm this is (the registry/dispatch key).
- `compile(ctx: CompilationContext) -> None` (`base.py:123`) — read inputs from `ctx`, do work, write
  output back to `ctx`. The arms communicate ONLY through the shared mutable `CompilationContext`
  (blackboard pattern) — each reads what upstream arms wrote, writes its one facet.
- `validate(ctx) -> GeometricAlignmentReport` (`base.py:136`) — check the geometric invariant(s) this
  arm is responsible for (not all arms check all 5).
- `get_mermaid_spec() -> MermaidSpec` (`base.py:146`) — the arm's OWN operating diagram (for D:D→D).
- `get_system_prompt_sections() -> List[PromptSection]` (`base.py:155`) — the arm's identity AS an agent.
- `get_tool_surface() -> ToolManifest` (`base.py:164`) — tools the arm needs when it runs as an agent.

Provided (non-abstract): `name` (`base.py:118`), `get_state_machine()` default
ANALYZING→COMPILING→VALIDATING→COMPLETE (`base.py:173`), the `Link.execute()` async bridge over the sync
`compile()`/`validate()` (`base.py:183-208`), `get_system_prompt()`/`get_input_prompt()`
(`base.py:215-233`), and `self_compile()` — the **D:D→D** check where the arm validates its own
self-description against the same invariants it enforces on others (`base.py:237-309`).

**How an arm plugs into the pipeline:** `CompilerPipeline.compile(ctx)` threads ONE `ctx` through
`self.arms` in order; after each `arm.compile(ctx)` it runs `arm.validate(ctx)` and STOPS on the first
misalignment (`base.py:484-518`). `compile_partial()` is the bootstrap mode: it tolerates
`NotImplementedError` per arm and returns a `PartialCompilationReport` (the "gradient" — which arm to
fill next, `base.py:536-596`). The **router** (`ChainConstruct`) owns the `_arms` registry and picks the
arm-name sequence via `_default_pipeline(feature_type)` (`router.py:187-203`), then builds a
`CompilerPipeline(arms)` (`router.py:172-176`) and `ctx.freeze()`s to a `CompiledAgent`.

---

## 3. THE `reviewer` ARM — the quality gate

The Reviewer is **not** a component-compiler; it is the **validator that gates every CONSTRUCT**. The
Bandit calls it after any construct (`bandit.py:407-408`; reviewer docstring `reviewer/factory.py:1-5`).

- `make_reviewer()` builds a `CompoctopusAgent` with SM `REVIEW→DONE` (`reviewer/factory.py:39-69`),
  `HermesConfig(model="minimax", tools=[])` — "pure evaluation, no tools" (`reviewer/factory.py:97`),
  and `REVIEWER_SYSTEM_PROMPT`.
- **What it validates:** the 5 geometric alignment invariants, enumerated verbatim in the prompt
  (`reviewer/prompts.py:9-15`): (1) Dual Description — system prompt ⇔ mermaid describe the same program;
  (2) Capability Surface — every referenced tool exists & every tool is referenced; (3) Trust Boundary —
  agent scope matches permission scope; (4) Phase↔Template — SM phase determines prompt / output class
  determines next phase; (5) Polymorphic Dispatch — feature_type determines the compile path. PLUS the
  arm output vs the original task requirements.
- **Gate output:** the agent emits `PASS`/`FAIL` + specific actionable feedback; `ReviewerCompiler.compile()`
  parses it — `passed = "PASS" in text and "FAIL" not in text` (`reviewer/factory.py:172`) — and returns
  `ReviewResult(passed, feedback, invariant_violations)` where violations are scraped by name
  (`_extract_violations`, `reviewer/factory.py:181-195`). It is the retry/feedback loop's judge: failed
  reviews carry `feedback`+`attempt` back into the next construct.

These same 5 invariants are also checked *deterministically* by each Family-A arm's `validate()` (e.g.
Trust Boundary in `agent.py:110-171`, Capability Surface in `mcp.py:98-152`) and by `alignment.py`. So
Compoctopus has BOTH a code-level gate (per-arm `validate`) and an LLM-level gate (the Reviewer).

---

## 4. CRUX — do the arms cover the Claude Code component set?

The hypothesis ("each arm compiles a different Claude Code component, i.e. the arms ARE the
align-all-CC-components-to-the-chain-ontology layer") is **PARTIALLY TRUE, with material gaps.** The arms
map to CC concepts but they do NOT emit on-disk CC artifacts (`.claude/agents/*.md`, `.mcp.json`,
`skills/<n>/SKILL.md`, slash-command files, `plugin.json`) — they emit in-memory `CompilationContext`
facets (`SystemPrompt`, `InputPrompt`, `ToolManifest`, `SkillBundle`, `AgentProfile`, `ChainPlan`) that
`freeze()` into a `CompiledAgent` (an SDNA/Heaven runtime agent), not Claude-Code files. The "components"
are SDNA-agent facets that *correspond to* CC components, not CC files. With that caveat:

**COVERED by an arm:**
- **System prompt** → `system_prompt` arm. (IS)
- **Input / user prompt** (the `agent.run()` goal + mermaid) → `input_prompt` arm. (IS) — this is the
  closest thing to a CC "slash-command body / user-message template," but it is NOT a `.claude/commands/*`
  slash command.
- **MCP (tool surface)** → `mcp` arm produces a `ToolManifest`/`MCPConfig`. (IS) — corresponds to MCP
  config, but it is an SDNA ToolManifest, not a `.mcp.json` file.
- **Skill** → `skill` arm produces a `SkillBundle`. (IS) — corresponds to CC skills; injects SKILL.md-style
  context, does not write a `SKILL.md` package dir.
- **Agent / subagent config** → `agent` arm produces an `AgentProfile` (model/provider/permissions/turns).
  (IS) — corresponds to a CC subagent's frontmatter (model, permissions), not a `.claude/agents/*.md`.
- **Chain** → `chain` arm produces a `ChainPlan`. (IS) — this is the chain-ontology unit itself, NOT a
  standard Claude Code component (CC has no "chain" primitive). This is Compoctopus's own addition.
- **Reviewer** → cross-cutting quality gate, not a CC component at all.

**MISSING — no arm exists for these CC components:**
- **Hooks** — NO arm. There is no `HookCompiler`/`ArmKind.HOOK`. CC hooks (PreToolUse, PostToolUse, Stop,
  SessionStart, PreCompact, …) are entirely uncovered.
- **Slash commands** — NO arm. `input_prompt` makes a goal string, but there is no compiler that emits a
  `.claude/commands/<name>.md` slash-command (with frontmatter, `$ARGUMENTS`, `!`-bash, `@`-file refs).
- **Plugins / marketplace** — NO arm. No compiler assembles `plugin.json` / `marketplace.json` / a plugin
  dir bundling the other components. (`COMPOCTOPUS_AGENT`/`COMPOCTOPUS` higher-order kinds exist in
  `ArmKind` `types.py:106-108` but those CHAIN the base arms into a CA / do D:D→D — they are not a plugin
  compiler.)
- **Settings / permissions file** (`.claude/settings.json`) — NO standalone arm; permission *mode* is set
  inside `agent` (AgentProfile.permission_mode), but no arm emits a settings artifact.

**So the arm set ≈ {system_prompt, input_prompt, mcp, skill, agent} of the CC component set, PLUS a
non-CC `chain` primitive, MINUS {hooks, slash-commands, plugins, settings}.** The arms align *agent
construction* (SDNA/Heaven runtime agents) to the chain ontology; they are NOT yet a complete
"compile every Claude-Code component to disk" layer. Closing the gap would mean adding `HookCompiler`,
`SlashCommandCompiler`, `PluginCompiler` arms (and an artifact-emit step that writes the CC files).

---

## 5. ASCII — one arm = (spec → SM-wrapped LLM compile → validated artifact)

```
        CompilationContext (shared blackboard — upstream arms' outputs live here)
                                     │  read inputs
                                     ▼
   ┌───────────────────────────── ARM (kind: ArmKind) ──────────────────────────────┐
   │                                                                                 │
   │   FAMILY A (deterministic class, e.g. ChainCompiler)                            │
   │      compile(ctx):  pure-python decision tree  ──►  writes ctx.<facet>          │
   │      validate(ctx): checks ITS geometric invariant  ──►  GeometricAlignmentReport│
   │                                                                                 │
   │   FAMILY B (CompoctopusAgent via make_*()):  SM-WRAPPED LLM COMPILE             │
   │      KeywordBasedStateMachine:   S0 ──► S1 ──► … ──► DONE                       │
   │              (each state's goal injected via Ariadne → HermesConfig → LLM run)  │
   │              e.g. ANALYZE → DECOMPOSE → DONE   /   IDENTITY→WORKFLOW→…→DONE      │
   │                                          │ emits the facet text                 │
   └──────────────────────────────────────────┼─────────────────────────────────────┘
                                               ▼  writes ctx.<facet>
        CompilationContext (now carries this arm's output: chain_plan / agent_profile /
                            tool_manifest / skill_bundle / system_prompt / input_prompt)
                                               │
                                               ▼   ─── REVIEWER arm (LLM PASS/FAIL gate,
                                                        checks the 5 invariants) ───┐
                                               │   ◄── retry w/ feedback if FAIL ◄──┘
                                               ▼  (per-arm validate() also gates here)
                                        VALIDATED ARTIFACT (this facet)

   Pipeline = chain of arms, ONE ctx threaded through (router._default_pipeline order):
     chain ─► agent ─► mcp ─► skill ─► system_prompt ─► input_prompt
       │       │        │      │            │                │
   ChainPlan AgentProf ToolMan SkillBund SystemPrompt   InputPrompt
                                               │
                                               ▼
                                    ctx.freeze() ► CompiledAgent (SDNA/Heaven runtime agent)
```

Each arm is the autorealization of one facet: a SPEC (TaskSpec slice / upstream facets) climbs through an
SM-wrapped compile to a VALIDATED artifact, gated by both a deterministic `validate()` and the LLM
Reviewer. The pipeline composes the six facets into one runnable agent.
