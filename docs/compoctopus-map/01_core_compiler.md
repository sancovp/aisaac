# Compoctopus — Core Compiler Map (01)

Slice mapped: the chain-ontology spine + base pipeline + top orchestrator + meta/onion/anneal + shared data model.
All file:line citations are against `/home/GOD/gnosys-plugin-v2/application/compoctopus/compoctopus/`.
SDNA citations are against `/home/GOD/gnosys-plugin-v2/base/sdna/sdna/`.

Marking convention: **IS** = verified by reading the code; **STUB/VISION** = declared-but-unimplemented (NotImplementedError / TODO / placeholder / docstring-only).

---

## 1. The chain_ontology type ladder

`chain_ontology.py` is a **re-export module**, not a definition module. **IS**: it imports `Link, Chain, EvalChain, ConfigLink, LinkConfig, LinkResult, LinkStatus, Compiler` from `sdna.chain_ontology` (`chain_ontology.py:18-27`) and `DovetailModel, HermesConfigInput` from `sdna.config` (`chain_ontology.py:30`). The only thing compoctopus *defines* in this file is `FunctionLink` (`chain_ontology.py:37`). So the canonical ladder lives in `sdna/sdna/chain_ontology.py`.

The ladder (all in SDNA):

- **`LinkStatus`** (`sdna:35-39`) **IS** a str-enum: `SUCCESS / BLOCKED / ERROR / AWAITING_INPUT`.
- **`LinkResult`** (`sdna:43-49`) **IS** a dataclass: `status`, `context: Dict`, `error`, `resume_path: List[int]`. This is the universal return value of every `execute()`.
- **`Link`** (`sdna:55-131`) **IS** the ABC root: "atomic unit of execution." Abstract method `async execute(context) -> LinkResult` (`sdna:77-89`). `name` is a plain attribute OR a `@property` (both satisfy the contract, `sdna:73-75`). `describe(depth)` (`sdna:91-116`) returns an LLM-readable static string; `__str__` delegates to `describe` (`sdna:118-131`).
  - **VISION** (explicitly): the docstring says `describe()`/`__str__` will *eventually* send the object's AST to ontologization (Carton/YOUKNOW), query the ontology, and return a paginated live CLI session (`sdna:98-114, 120-130`). **Current behavior IS** a static format string — the ontology-backed self-description is NOT implemented.
- **`Chain(Link)`** (`sdna:138-191`) — **the homoiconic property**. **IS**: `Chain` *subclasses* `Link`, so a Chain IS a Link and can be a member of another Chain (`Chain([Link, Chain([...]), Link])`, `sdna:144`). `__init__(chain_name, links)` (`sdna:150-152`); `name` is a `@property` over `_name` (`sdna:154-156`); `add()` is fluent (`sdna:158-161`). `execute()` (`sdna:163-175`) **IS** sequential: copies context, runs each `link.execute(ctx)`, threads `ctx = result.context` forward, and **stops on first non-SUCCESS**, prepending its index to `resume_path` (`sdna:171-174`). `__len__`/`__getitem__` make it list-like (`sdna:177-181`). `describe()` (`sdna:183-191`) recurses into children with tree connectors.
- **`EvalChain(Chain)`** (`sdna:198-264`) **IS** a Chain + an `evaluator: Link` in a loop (SDNAFlowchain / OVP pattern). `__init__` adds `evaluator`, `max_cycles=3`, `approval_key="approved"` (`sdna:207-218`). `execute()` (`sdna:220-252`): per cycle — run inner chain via `super().execute()`, then run the evaluator; if `ctx[approval_key]` is truthy → SUCCESS; if max cycles hit → **BLOCKED** with "Max cycles reached" (`sdna:248-252`). If no evaluator, single pass (`sdna:235-236`).
- **`Compiler(Chain)`** (`sdna:271-310`) **IS** the D:D→D type: "a Chain whose output is a Link or Chain." It does NOT override `execute()` — it inherits Chain's sequential execution. What it adds is the **output convention**: `__init__(chain_name, links, output_key="compiled")` (`sdna:289-295`) and `get_compiled(context)` which returns `context.get(self.output_key)` (`sdna:298-300`). So **the "compiled" key IS just a dict slot** in the threaded context where a Compiler's links deposit the produced Link/Chain; `get_compiled` reads it back. `describe()` appends `→ produces Link via 'compiled'` (`sdna:309`).
- **`LinkConfig`** (`sdna:317-348`) **IS** the serializable config dataclass a compiler produces: `name, goal, system_prompt, model, provider, temperature, max_turns, permission_mode, allowed_tools, mcp_servers, skills, passthrough`. Docstring maps each field to a HermesConfig field.
- **`ConfigLink(Link)`** (`sdna:351-391`) **IS** the leaf node wrapping a `LinkConfig`. `name` proxies `config.name` (`sdna:362-364`). **STUB-ish / placeholder**: `execute()` (`sdna:366-375`) is explicitly a *passthrough* — it only writes `ctx["_link_config"]` and `ctx["_link_name"]` and returns SUCCESS. The docstring states real execution (instantiate an SDNAC, run it) happens "in production"; this file does NOT do that — it is dry-run only (`sdna:367-371`).

**How the Compiler's output feeds back (the self-compiling loop) — IS, by convention not by force:** a `Compiler` runs its links (Chain semantics), the links write a produced `Link` into `context["compiled"]`, and `get_compiled()` reads it out. Because the produced thing is itself a `Link`, it can be placed into another `Chain`/registered as another arm. In compoctopus's router this convention is honored: `ChainSelect`/`ChainConstruct`/`Bandit` all `ctx[self.output_key] = compiled` (a `CompiledAgent`), see §3.

**FunctionLink (compoctopus's only chain_ontology addition)** (`chain_ontology.py:37-91`) **IS** a `Link` that wraps a plain Python `fn(ctx) -> ctx|None`. `execute()` (`chain_ontology.py:61-84`): copies context, awaits `fn` if it's a coroutine else calls it; if `fn` returns non-None it replaces ctx; returns SUCCESS, or ERROR on any exception. Used for mechanical no-LLM steps (anneal, verify, dispatch). This is the homoiconic bridge for "code, not an agent."

---

## 2. base.py — CompilerArm and CompilerPipeline

**`CompilerArm(Link, ABC)`** (`base.py:93-309`) **IS** the abstract base for every compiler arm, and **IS a Link** (so arms compose into any Chain topology). The arm contract (all `@abstractmethod`, `base.py:112-171`):
- `kind -> ArmKind` (which arm).
- `compile(ctx: CompilationContext) -> None` — read inputs from ctx, do work, write output back into ctx (`base.py:123-134`). **Note: synchronous, returns None, mutates the context** — this is the arm's real work surface.
- `validate(ctx) -> GeometricAlignmentReport` (`base.py:136-144`).
- `get_mermaid_spec() -> MermaidSpec`, `get_system_prompt_sections() -> List[PromptSection]`, `get_tool_surface() -> ToolManifest` (`base.py:146-171`) — the arm's self-description AS an agent (for meta-compilation).
- `get_state_machine()` (`base.py:173-179`) has a default: `make_compiler_sm()`.

The **Link bridge** `async execute()` (`base.py:183-208`) **IS** an async wrapper over the synchronous `compile()`: it pulls/creates a `CompilationContext` from `ctx_dict["_compilation_ctx"]`, calls `self.compile()` then `self.validate()`, and maps `alignment.aligned` → SUCCESS/ERROR. So an arm works both standalone-as-a-Link and inside a pipeline.

**D:D→D self-compilation** `self_compile()` (`base.py:237-309`) **IS** implemented (not a stub): it treats the arm AS an agent and checks (1) mermaid structural validity via `MermaidValidator`, (2) required IDENTITY+WORKFLOW prompt sections, (3) tool surface vs mermaid tool refs, (4) dual-description + capability-surface via `GeometricAlignmentValidator`. Returns `SelfCompilationResult` (`base.py:312-332`). "The design IS the test."

**`CompilerPipeline(Chain)`** (`base.py:410-619`) — **IS a Chain** (`super().__init__(chain_name="compiler_pipeline", links=arms)`, `base.py:434`). So the pipeline IS a Link and can nest into larger chains. `self.arms` is a backward-compat alias for `self.links` (`base.py:435`). It composes arms by threading ONE shared `CompilationContext` through them:
- `compile(ctx)` (`base.py:472-534`) **IS** strict mode: for each arm, `begin_step` → `arm.compile(ctx)` → `arm.validate(ctx)` → `end_step`; **stops on first exception or first alignment failure** and returns ctx with the failing alignment. Fires `on_arm_start/complete/error/pipeline_complete` hooks (`base.py:444-470`). Catches only `(ValueError, TypeError, KeyError, AttributeError, RuntimeError)` (`base.py:431`) — system errors propagate.
- `compile_partial(ctx)` (`base.py:536-596`) **IS** the bootstrap/gradient mode: runs every arm, catching `NotImplementedError` → status `"not_implemented"`, other catch-errors → `"failed"`, success → `"completed"`; returns a `PartialCompilationReport`. **This is the annealing gradient as runtime telemetry** — `report.next_to_fill` (`base.py:381-389`) names the next arm to implement.
- `self_compile_all()` (`base.py:598-607`) runs `self_compile()` on every arm = the bootstrap test suite.

**The arm contract an arm satisfies (summary):** subclass `CompilerArm`, implement `kind`, `compile(ctx)` (mutate the shared `CompilationContext`), `validate(ctx)`, and the three self-description getters (`get_mermaid_spec`, `get_system_prompt_sections`, `get_tool_surface`). That makes the arm simultaneously (a) a pipeline step, (b) a standalone Link, and (c) a self-describable agent that can be meta-compiled.

The standard 6 arms named everywhere: `chain, agent, mcp, skill, system_prompt, input_prompt` (`router.py:193`, `meta.py:216`) — their factories live in `arms.py` (`make_chain_compiler` … `ReviewerCompiler`, out of this slice but cited in `__init__.py:197-205`).

---

## 3. The two orchestration paths (KEY DIVERGENCE)

There are **two separate "top" orchestrators** in this codebase, and they do NOT call each other. This is the most important structural finding and is documented in §"DIVERGENCE" below. Both are grounded by `grep` of instantiation sites.

### Path A — the chain-ontology compiler (router.py; the one the type ladder/__init__.py describe)
`router.py` builds the homoiconic compiler stack `Link → Chain → Compiler → {ChainSelect, ChainConstruct, Bandit}`:
- **`Bandit(Compiler)`** (`router.py:215-377`) **IS** "the head of the octopus." Holds a `ChainSelect` and a `ChainConstruct` (`router.py:240-241`). The real entry point is the **synchronous** `compile(task_spec) -> CompiledAgent` (`router.py:284-308`): try golden-chain lookup (SELECT, only if `reward_count >= 5`), else `chain_construct.compile_with_pipeline(task_spec)` (CONSTRUCT). `record_execution()` (`router.py:322-370`) feeds a `SensorReading` back and graduates a config to a golden chain when the threshold is met — **this is the learning/feedback loop**.
- **`ChainConstruct(Compiler)`** (`router.py:110-208`): `compile_with_pipeline()` (`router.py:149-185`) **IS** where the §2 pipeline actually runs: `arms = [self._arms[name] ...]` → `pipeline = CompilerPipeline(arms)` → `ctx = pipeline.compile(CompilationContext(task_spec))` → `compiled = ctx.freeze()`. `_default_pipeline()` (`router.py:187-203`) picks the arm sequence by `FeatureType` (CHAIN/SKILL skip the `chain` arm).
- **`ChainSelect(Compiler)`** (`router.py:42-103`): golden-chain exploit lookup; writes `ctx["compiled"]`.

End-to-end (Path A): `TaskSpec` → `Bandit.compile` → (SELECT golden | CONSTRUCT) → `ChainConstruct.compile_with_pipeline` → `CompilerPipeline.compile` threads `CompilationContext` through the 6 arms → `ctx.freeze()` → **`CompiledAgent`**, whose `.to_link()/.to_chain()` (`types.py:628-645`) convert it back into a `ConfigLink`/`Chain` = the output-is-a-Link feedback.

### Path B — the agent-factory orchestrator (compoctopus.py + compile.py; the "PRD in" story)
- **`make_compoctopus(prd, workspace, workers)`** (`compoctopus.py:26-140`) **IS** the top agent builder per its docstring "PRD → Planner → Bandit → Workers." But what it actually wires (`compoctopus.py:42-140`): `make_planner()` + default worker `make_octopus_coder()`; a `dispatch_tasks` `FunctionLink` (`compoctopus.py:60-116`) that reads GIINT tasks (via `llm_intelligence.projects.get_project`, fallback to PRD spec) and **directly dispatches each task to the default `octopus_coder` worker** — NOT through the Bandit. It returns a `CompoctopusAgent` wrapping `Chain([planner, dispatch_link])` with model `"minimax"` (`compoctopus.py:119-140`).
- **`compile(request, project_id)`** (`compile.py:8-60`) **IS** a small async router with **explicit TODOs**: `project_id` set → run `make_planner()`, mark `_planner_ran`, then for each created task it builds a `task_ctx` and appends it — but **`# TODO: Bandit.execute(task_ctx) once Bandit is wired as agent`** (`compile.py:52`); no `project_id` → **`# TODO: Bandit.execute(ctx) once Bandit is wired`** (`compile.py:59`) and just returns `{"status":"direct",...}`. So `compile.py` is **VISION/STUB for the Bandit hop** — the Planner runs but the Bandit is not actually invoked from here. `compile.py` is imported by `octopus_coder.py:18` (out of slice).

---

## 4. meta.py / onionmorph.py / annealer.py — where each sits

- **`MetaCompiler(Link)`** (`meta.py:28-267`) **IS the compiler-compiler level (D:D→D)**, intended as "Phase 6, depends on all other arms" (`meta.py:14`). It is a `Link` that takes a `router` (a Bandit) + optional `onionmorph` (`meta.py:45-55`). Implemented methods:
  - `compile_domain(desc)` (`meta.py:80-144`) **IS** real: compiles 1 orchestrator + N managers + N workers by building `TaskSpec`s and calling `self._router.compile(spec)` for each. Requires a router or raises ValueError.
  - `compile_arm(arm_name)` (`meta.py:146-201`) **IS** the literal D:D→D fixed point: pull the arm from `router.chain_construct._arms`, take its self-description (`arm.self_compile()`, `get_mermaid_spec/get_system_prompt/get_tool_surface`), feed THAT as a `TaskSpec` back into `router.compile()` to compile the arm itself.
  - `bootstrap()` (`meta.py:203-255`) compiles all 6 arms via `compile_arm` and does a **structural** (length-ratio) fixed-point check — explicitly *not semantic* ("that needs LLM", `meta.py:238`). **Partial-verification / heuristic**, not a real equivalence proof.
  - `_detect_subdomains` (`meta.py:257-267`) delegates to onionmorph or returns `["default"]`.
  - Sits ABOVE the pipeline: it USES a Bandit (Path A) recursively. Not instantiated anywhere in this package except its own class def (grep: only `meta.py`).
- **`OnionmorphRouter(Link)`** (`onionmorph.py:33-182`) **IS** a hierarchical domain router: `Domain → Subdomain → Worker`. `route(task_spec)` (`onionmorph.py:76-100`) returns a `RoutingTree`; `detect_cross_domain` (`onionmorph.py:148-181`) uses `task_spec.domain_hints` first, else registry keyword-overlap scoring, else `["general"]`; `route_single_domain` (`onionmorph.py:102-146`) matches subdomains by word-overlap. It produces a routing PLAN (a `RoutingTree` of `RoutingNode`s) — it does NOT itself compile agents; `MetaCompiler` consumes its subdomain list. Only instantiated as its own class def (grep). So onionmorph = **the layered routing front-end / subdomain detector** feeding the meta-compiler.
- **`Annealer`** (`annealer.py:230-476`) **IS** the syntactic code-generator: it compiles `.🐙`/`.octo` files to a target language by unwrapping STUB blocks. `scan()` (`annealer.py:250-330`) finds `#>> STUB / #| code / #<< STUB` blocks and classifies each as EMPTY/PSEUDO/ANNEALED (`StubPhase`, `annealer.py:184-189`); `anneal_source()` (`annealer.py:332-378`) processes stubs in reverse line order — PSEUDO → unwrap pipe lines (strip `#|`, dedent), EMPTY → replace with `raise NotImplementedError("Stub not yet filled")` (`annealer.py:366-375`). `anneal()`/`anneal_directory()` do file I/O; `SyntaxMatcher`s exist for Python/JS/TS/Rust (`annealer.py:118-159`).
  - **This is the literal mechanism behind the "Annealing Protocol" docstring in base.py** (`base.py:16-67`): NotImplementedError-with-pseudocode IS the intermediate representation; unwrapping IS the anneal; it is a **SYNTACTIC operation, not semantic** (`base.py:41-42`). The annealer is meant to be wrapped as a `FunctionLink` for the ANNEAL step (`chain_ontology.py:41,48`). **IS implemented** as a standalone util; grep shows it is **NOT yet wired** into any live pipeline arm in this slice (used only in its own module + docstrings). So annealer = the **iterate-toward-implementation ground-truth loop at the SOURCE-FILE level** (stub→pseudo→annealed→verify), distinct from the Bandit's reward loop (runtime config level) and the EvalChain loop (execution level).

Three different "loops" — keep them straight: **Annealer** = source-file stub-filling (syntactic); **EvalChain** = run→evaluate→repeat (execution); **Bandit.record_execution→graduate** = reward-driven select/construct (config selection). The annealer is the one that matches "iterate-against-ground-truth" at compile time.

---

## 5. context.py / types.py / errors.py — the shared data model

- **`CompilationContext`** (`context.py:51-158`) **IS** the mutable "wire" threaded through every arm. Holds the input `task_spec` and progressive optional outputs filled by arms in order: `chain_plan, agent_profile, tool_manifest, skill_bundle, system_prompt, input_prompt, alignment` (`context.py:65-74`) + a `steps: List[CompilationStep]` trace. `begin_step/end_step` (`context.py:81-102`) time each arm. `freeze()` (`context.py:104-128`) snapshots the context into an immutable-by-convention `CompiledAgent` with a `compile_id` (uuid) and `pipeline_arms`. `config_hash` (`context.py:130-148`) is a cached sha256 over (task desc, model, tools) used by the bandit to identify configs.
- **`types.py` — the closed type algebra**, "ONLY dataclass/enum definitions, no logic" (`types.py:13`). The pipeline transform (`types.py:6-7`): `TaskSpec → ChainPlan → AgentProfile → ToolManifest → SkillBundle → SystemPrompt → InputPrompt → CompiledAgent`.
  - **`CompilationPhase`** (`types.py:28-42`) **IS** the per-arm state-machine enum: `ANALYZING, COMPILING, VALIDATING, COMPLETE, BLOCKED, DEBUG` (the dev→complete / dev→debug→complete pattern from EvolutionFlow).
  - `GeometricInvariant` (`types.py:45-59`): the 5 invariants — DUAL_DESCRIPTION, CAPABILITY_SURFACE, TRUST_BOUNDARY, PHASE_TEMPLATE, POLYMORPHIC_DISPATCH.
  - `FeatureType` (TOOL/AGENT/CHAIN/DOMAIN/SKILL — polymorphic dispatch key, `types.py:62-73`); `TrustLevel` (ORCHESTRATOR/BUILDER/EXECUTOR/OBSERVER, `types.py:75-87`); `ArmKind` (the 6 base arms + REVIEWER + higher-order COMPOCTOPUS_AGENT/COMPOCTOPUS, `types.py:89-108`); `PermissionMode` (`types.py:111-119`).
  - IRs: `TaskSpec` (`types.py:382-399`, the pipeline input), `ChainPlan/ChainNode`, `AgentProfile` (default model `"minimax"`/provider `"openrouter"`, `types.py:424-443`), `ToolManifest` (with `all_tool_names`), `SkillBundle`, `SystemPrompt`(renders XML sections), `InputPrompt`(carries a `MermaidSpec`), `GeometricAlignmentReport` (`aligned = all(r.passed)`).
  - **`MermaidSpec`** (`types.py:209-375`) **IS** a graph-first builder: structured participants/messages/alts/loops with the rendered `.diagram` text as a *computed property* ("the structure IS the source of truth, the text is a view", `types.py:215-216`). This is the dual of a system prompt's WORKFLOW section.
  - **`CompiledAgent`** (`types.py:555-689`) **IS** the frozen output + the homoiconic bridge back to the chain ontology: `to_link_config()` (`types.py:601-626`) maps every compiled field into a `LinkConfig`; `to_link()` → `ConfigLink` (`types.py:628-635`); `to_chain()` → single-link `Chain` (`types.py:637-645`). `is_complete`/`is_aligned` properties; `to_dict()` for persistence. **This is exactly how a Compiler's `CompiledAgent` output becomes a Link that feeds back as a new arm/chain member.**
- **`errors.py`** (`errors.py:1-228`) **IS** the typed error hierarchy: `CompoctopusError` → `CompilationError`(per-arm subclasses keyed to `ArmKind`) / `AlignmentError`(per-invariant subclasses keyed to `GeometricInvariant`) / `RegistryError` / `RoutingError` / `BridgeError`. Pure exception classes; each docstring states which invariant/arm it maps to and a fix hint. (Note: the live pipeline in `base.py`/`router.py` actually catches plain `(ValueError, TypeError, KeyError, AttributeError, RuntimeError)` and `NotImplementedError`, NOT these typed errors — these typed errors are defined but not raised in this slice.)

---

## 6. ASCII composition diagram

```
                         THE HOMOIONIC SPINE (sdna/chain_ontology.py)
   Link ("I execute")  ── execute(ctx)->LinkResult ; describe()
     │  (Chain IS a Link → homoiconic nesting)
     ├── Chain(Link)            run links in sequence, thread ctx, stop on non-SUCCESS
     │     ├── EvalChain(Chain)        chain → evaluator → loop (max_cycles) ; BLOCKED if exceeded
     │     └── Compiler(Chain)         output convention: links write ctx["compiled"]; get_compiled() reads it
     ├── ConfigLink(Link)       leaf: wraps LinkConfig (dry-run passthrough; SDNAC at runtime = VISION)
     └── FunctionLink(Link)     compoctopus-added: wraps a plain fn (mechanical, no LLM)

   COMPILE STEP (compoctopus/base.py)
   CompilerArm(Link, ABC):  compile(ctx)->None  (mutates the shared CompilationContext)
                            validate(ctx)->GeometricAlignmentReport
                            + self-desc getters (mermaid / prompt sections / tools)  → self_compile() = D:D->D
   CompilerPipeline(Chain): threads ONE CompilationContext through [arm,arm,...]
                            .compile()=strict   .compile_partial()=gradient(report.next_to_fill)

   PATH A — the chain-ontology compiler (compoctopus/router.py)            [the type ladder's own story]
   ┌────────────────────────────────────────────────────────────────────────────────────┐
   │ Bandit(Compiler) .compile(TaskSpec) -> CompiledAgent                                   │
   │   ├── ChainSelect(Compiler)     golden-chain lookup (EXPLOIT)                          │
   │   └── ChainConstruct(Compiler)  build CompilerPipeline(arms) and run it (EXPLORE)      │
   │           arms = [chain, agent, mcp, skill, system_prompt, input_prompt]               │
   │              │ pipeline.compile(CompilationContext(task_spec))                          │
   │              ▼                                                                          │
   │           ctx.freeze() ──▶ CompiledAgent ──.to_link()/.to_chain()──▶ ConfigLink/Chain  │
   │                                  │  record_execution()→graduate→GoldenChain (FEEDBACK)  │
   └──────────────────────────────────┼─────────────────────────────────────────────────────┘
                                       ▼  (output IS a Link → register as a new arm → grow)
   META LEVEL (compoctopus/meta.py)            ONION FRONT-END (compoctopus/onionmorph.py)
   MetaCompiler(Link) USES a Bandit:           OnionmorphRouter(Link): TaskSpec → RoutingTree
     compile_domain → orch+managers+workers      (Domain→Subdomain→Worker)  feeds subdomains→MetaCompiler
     compile_arm    → D:D->D (arm self-desc → router.compile → the arm)
     bootstrap      → compile all 6 arms, length-ratio fixed-point check (heuristic)

   SOURCE-FILE ANNEAL LOOP (compoctopus/annealer.py)   [syntactic, separate from Path A]
   .🐙/.octo  ──scan(STUB blocks)──▶ EMPTY→NotImplementedError ; PSEUDO→unwrap #| ──▶ .py

   PATH B — the agent-factory orchestrator (compoctopus/compoctopus.py + compile.py)   [PRD story]
   make_compoctopus(PRD) ─▶ CompoctopusAgent( Chain[ make_planner(), dispatch FunctionLink ] )
        dispatch reads GIINT tasks ─▶ directly runs default worker make_octopus_coder()  (Bandit NOT called)
   compile(request, project_id): Planner runs; Bandit hop = TODO (compile.py:52, :59)  ◀── STUB/VISION
```

---

## DIVERGENCE from the self-compiling-compiler story (explicit)

1. **Two non-connected orchestrators.** The clean homoiconic story (`__init__.py` docstring, `router.py`) is Path A: `Bandit → ChainConstruct → CompilerPipeline → 6 arms → CompiledAgent → back to a Link`. But the file named `compoctopus.py` (Path B) is a *different* orchestrator that wires `Planner → dispatch → OctoCoder worker` and **does not call the Bandit at all** (`compoctopus.py:82-106` dispatches straight to the default worker). The "PRD → Planner → Bandit → Workers" docstring (`compoctopus.py:1-9`) overstates what the code wires — the Bandit step is absent.
2. **`compile.py`'s Bandit hop is a TODO.** The documented routing "planner already ran → Bandit for each task" is not implemented: `# TODO: Bandit.execute(...) once Bandit is wired` appears twice (`compile.py:52, :59`); it returns `{"status":"planned"/"direct"}` without ever invoking the Bandit. So the headline "self-compiling" loop is real in Path A's *library* surface but NOT reached through `compile.py`'s entrypoint.
3. **`ConfigLink.execute` is a dry-run passthrough** (`sdna chain_ontology.py:366-375`) — the produced Link does not actually instantiate/run an SDNAC here; the "becomes SDNAC at runtime" half of homoiconicity is VISION (deferred to an SDNABridge outside this slice).
4. **`Link.describe()/__str__` ontology-backed self-description is VISION** (`sdna chain_ontology.py:98-114`) — currently a static string.
5. **`MetaCompiler.bootstrap` fixed-point check is heuristic** (length ratio, explicitly not semantic, `meta.py:238-248`) — it does NOT prove `compile(compoctopus) ≈ compoctopus`; the QUINE claim in `__init__.py:71-89` is asserted, not verified by code.
6. **Annealer is built but unwired** — the "Annealing Protocol IS the compilation strategy, reified into the code" (`base.py:20-22`) is true as a standalone util but is not invoked by any live arm/pipeline in this slice.
7. **Typed errors in `errors.py` are defined but not raised** by the live pipeline (which catches generic Python exceptions) — the rich diagnostic taxonomy is aspirational at the orchestration layer.
```
