# Compoctopus Map — 02: Router / Bandit / Pattern-Memory (Goldens)

Slice: how compoctopus chooses between REUSING a known-good chain (exploit) vs
CONSTRUCTING a new one (explore), and how it MAKES / KEEPS / SEARCHES patterns
("golden chains"). CODE is truth; every claim cites `file:line` (paths relative to
`/home/GOD/gnosys-plugin-v2/application/compoctopus/compoctopus/`). `/home/GOD/core/`
avoided. Status tags: **[IS]** = real running code, **[STUB]** = unimplemented
(`#>> STUB` octo block or `NotImplementedError`), **[VISION]** = described in
docstrings/design only.

> KEY STRUCTURAL FINDING: there are **THREE parallel, NON-INTEGRATED Bandit
> implementations** in this codebase, each a different mechanism for the same
> SELECT-vs-CONSTRUCT decision. They do not call each other. This is the single
> most important thing to understand about this slice.

---

## 0. The three Bandits (disambiguation — read this first)

| # | File | Bandit is a… | Memory of patterns | Decision driver | Status |
|---|------|--------------|--------------------|-----------------|--------|
| A | `router.py` | a `Compiler` (subclass) | `GoldenChainStore` (in-mem dict, `golden_chains.py`) | reward score from `SensorStore` (`sensors.py`) | **[IS]** runnable, classic bandit math |
| B | `bandit.py` | an LLM agent (`CompoctopusAgent`/`EvalChain`) | a bare `Dict[str,Any]` `golden_chains` + `rewards` | an LLM emits a `<SELECT>` tag | **[IS]** code present; depends on Heaven/SDNA + an LLM at runtime |
| C | `agents/bandit/factory.py` | a `FunctionLink` `Chain` | JSON files in `/tmp/bandit_history` (`request_io.py`) | tag-overlap count over past request files | **[IS]** pure-python, fully runnable & tested |
| D | `bandit.octo` | (a 4th, source-only design) | `Dict[str,GoldenChain]` + regex `task_pattern` | `re.search` pattern match + `success_count` | **[STUB]** every method body is an un-annealed `#>> STUB` |

All four agree on the SHAPE: `LOOKUP → (SELECT | CONSTRUCT) → RECORD → graduate`.
They disagree on the *mechanism* of lookup, scoring, storage, and graduation.

---

## 1. ChainSelect vs ChainConstruct vs Bandit — the explore/exploit logic

This section is the **router.py (Bandit A)** path — the one with real bandit math.

### ChainSelect(Compiler) — EXPLOIT [IS] `router.py:42-103`
- The "exploit arm." `select(task_spec)` `router.py:55-77`:
  - derives `domain = task_spec.domain_hints[0]` (else `"general"`) `router.py:61`,
  - calls `GoldenChainStore.find_for_task(domain, feature_type)` `router.py:62-65`,
  - returns the golden's `compiled_agent` or `None`.
- Async `execute()` `router.py:79-98`: pulls `_task_spec` from context, returns
  `LinkStatus.SUCCESS` with the `CompiledAgent` in `ctx["compiled"]`, or
  `LinkStatus.BLOCKED` if no golden chain exists `router.py:91-95`.

### ChainConstruct(Compiler) — EXPLORE [IS] `router.py:110-208`
- The "explore arm." Builds a FRESH agent by running a `CompilerPipeline` of
  registered arms `router.py:149-185`:
  - arm sequence = `ctx["_arm_names"]` or `_default_pipeline(feature_type)`,
  - `_default_pipeline` `router.py:187-203` = `["chain","agent","mcp","skill",
    "system_prompt","input_prompt"]` minus per-feature skips (CHAIN/SKILL skip
    `"chain"`),
  - assembles `CompilerPipeline(arms)`, runs `pipeline.compile(ctx)`, then
    `ctx.freeze()` → a `CompiledAgent` `router.py:172-176`.
- `register_arm(name, arm)` `router.py:123-126` populates `self._arms`.

### Bandit(Compiler) — THE HEAD [IS] `router.py:215-377`
Holds one `ChainSelect`, one `ChainConstruct`, one `GoldenChainStore`, one
`SensorStore` `router.py:238-241`. Two entry points:

- **async `execute()`** `router.py:248-282` — the live decision:
  1. try `chain_select.execute(ctx)`; on SUCCESS set `ctx["_bandit_chose"]="select"`
     and return (REUSE the golden) `router.py:260-268`;
  2. on miss, fall through to `chain_construct.execute(ctx)`, set
     `_bandit_chose="construct"` (BUILD new) `router.py:270-282`.
  > NOTE: `execute()` SELECTs on ANY golden hit — `find_for_task` already gates on
  > `reward_mean >= 0.8` `golden_chains.py:81,93`.

- **sync `compile(task_spec)`** `router.py:284-308` — the documented main entry:
  - looks up a golden, and only exploits **if `golden.reward_count >= 5`**
    `router.py:296`; otherwise CONSTRUCTs. (So `compile()` adds a hard count gate
    *on top of* the reward gate; `execute()` does not.)

### The selection / scoring mechanism (router.py path) [IS]
Scoring lives in `sensors.py`, not the bandit. `SensorStore.get_reward(config_hash)`
`sensors.py:57-90` computes:

```
reward = success_rate*0.4 + efficiency*0.3 + human_feedback*0.3
  success_rate = (# readings with success) / (# readings)
  efficiency   = max(0, 1 - avg_turns/25)          # 25 = SDNA max_turns
  human_feedback = avg(human_feedback) or 0.5 default
```
A config **graduates** to a golden when
`meets_graduation_threshold(hash, min_count=5, min_reward=0.8)` `sensors.py:102-125`
— i.e. ≥5 recorded runs AND mean reward ≥0.8.

**So the explore/exploit policy is NOT epsilon-greedy or UCB** — it is a deterministic
threshold gate: "exploit iff a golden exists for (domain, feature_type) with mean
reward ≥0.8 (and, via `compile()`, ≥5 runs); else explore." The class is *named*
Bandit but implements a graduation-gated cache, not a multi-armed-bandit sampler.
**[IS]** for the gate; classic bandit sampling is **[VISION]** only (the name + the
"bandit problem" docstring `sensors.py:1-12`).

### The LLM path (bandit.py — Bandit B) [IS code / runtime-dependent]
`bandit.py` is a *different* SELECT/CONSTRUCT realized as an LLM state machine:
- `make_bandit()` `bandit.py:140-258` builds an `EvalChain` with one SELECT `SDNAC`
  (an LLM step, model `"minimax"`) + a `FunctionLink` evaluator, `max_cycles=5`.
- The LLM is given `BanditTools` `bandit.py:39-83` (`query_registry`,
  `list_golden_chains`, `list_arm_kinds`) and a system prompt telling it to output
  `<SELECT>arm_name</SELECT>` or `<SELECT>CONSTRUCT</SELECT>` `bandit.py:90-114`.
- `BanditRuntime.run()` `bandit.py:287-341`: runs the CA, extracts the `<SELECT>` tag
  `bandit.py:343-361`, and on `CONSTRUCT` calls `_construct()` `bandit.py:363-390`
  which picks the highest-`reward` candidate arm (`max(... key=rewards.get)`
  `bandit.py:370`), runs it, then runs a Reviewer arm `bandit.py:405-419`; pass → 
  `rewards[arm]+=1`, fail → `-1`. The constructed result is cached into the plain
  `golden_chains` dict under key `f"{kind}:{task[:80]}"` `bandit.py:317-318`.
- Here scoring is integer reward tallies per arm name (`+1`/`-1`), and the
  explore/exploit *choice itself is delegated to the LLM*. This is a genuinely
  different mechanism from router.py's reward formula.

---

## 2. golden_chains.py + registry.py — make / keep / search patterns

This is the "make/keep/search patterns" capability. Precise behavior:

### MAKE (graduate) [IS] `golden_chains.py:106-133`
`GoldenChainStore.graduate(compiled_agent, reward_mean, reward_count, domain)`:
- `config_hash = compiled_agent.compile_id` or a `hash(system_prompt+tool_manifest)`
  fallback `golden_chains.py:117-119`,
- wraps into a `GoldenChainEntry(config_hash, reward_mean, reward_count, domain,
  feature_type, compiled_agent)` `golden_chains.py:120-127` (type def
  `types.py:711-723`),
- `store()`s it. Called from `Bandit.record_execution()` `router.py:322-370` —
  i.e. graduation happens *after* an execution outcome is recorded AND the sensor
  graduation threshold is met `router.py:358-366`.

### KEEP (store) [IS] `golden_chains.py:29-178`
- Backing store: an **in-memory `Dict[str, GoldenChainEntry]`** keyed by
  `config_hash` `golden_chains.py:46`. Thread-safe via `RLock`.
- Shape kept per entry: `{config_hash, compiled_agent, reward_mean, reward_count,
  domain, feature_type}` `types.py:711-723`.
- Lifecycle management **[IS]**: LRU eviction over `max_chains=500`
  `golden_chains.py:164-172`, and TTL expiry `ttl=30 days` (lazy, on access)
  `golden_chains.py:151-162`.
- **Persistence is [STUB].** `sync_to_carton()` / `sync_from_carton()`
  `golden_chains.py:182-198` both `raise NotImplementedError`. So goldens DIE with
  the process — there is no durable golden store yet. The intent (persist each as a
  `Golden_Chain` Carton concept) is **[VISION]** in those docstrings.

### SEARCH / retrieve [IS] `golden_chains.py:66-104`
- Primary search = `find_for_task(domain, feature_type, min_reward=0.8)`
  `golden_chains.py:77-104`: linear scan filtering by **exact** `domain` AND
  **exact** `feature_type` AND `reward_mean >= min_reward`, then `max(... key=
  reward_mean)` picks the best `golden_chains.py:90-98`.
- `get(config_hash)` `golden_chains.py:66-75` = direct hash lookup (with TTL check).
- **There is NO similarity index, NO embedding, NO fuzzy match here.** Retrieval is
  exact (domain, feature_type) bucketing + reward argmax. A "similarity index" is
  **[VISION]** (the Carton/chroma hooks that would provide it are unimplemented).

### registry.py — the OTHER searchable store (arms/MCPs/skills/domains) [IS, with VISION edges]
`registry.py` is the catalog the bandit/arms query for "what exists?" `registry.py:1-21`.
- Stores `RegisteredMCP / RegisteredSkill / RegisteredDomain / RegisteredArm`
  dataclasses `registry.py:38-108` in plain dicts (backend `"static"`; `"carton"`
  backend declared but its semantic path is deferred) `registry.py:115-134`.
- Arm lookup the bandit uses: `get_arms_for_kind(ArmKind)` `registry.py:315-324`,
  `list_arms()` `registry.py:326-334`, `get_ca_recipe(arm_name)` `registry.py:336-345`.
- Pattern SEARCH here is **keyword/tag overlap**, not semantic:
  - `find_skills_for_behavior(tags)` `registry.py:188-225`: lowercase tag-set
    intersection, sorted by overlap count. Carton semantic search is an explicit
    `if backend=="carton" and not scored` **[STUB/VISION]** branch that only logs
    `registry.py:209-216`.
  - `resolve_domain_stack(task)` `registry.py:247-288`: word-overlap against domain
    descriptions/names/subdomains, argmax; same deferred-carton branch
    `registry.py:270-276`; falls back to a `general` domain `registry.py:281-282`.
- `sync_to_carton()` / `sync_from_carton()` `registry.py:351-378` = **[STUB]**
  `NotImplementedError`. So the registry, like the golden store, is process-local.

### The third pattern memory — agents/bandit (Bandit C) [IS, fully runnable]
`agents/bandit/factory.py` + `request_io.py` is a self-contained, LLM-free
make/keep/search:
- KEEP: every request is a JSON file in `/tmp/bandit_history`
  (`write_request` `request_io.py:20-29`), updated with outcome+duration on RECORD
  (`update_outcome` `request_io.py:38-45`).
- SEARCH: `find_similar_requests(history_dir, tags)` `request_io.py:48-66` = count of
  shared tags, sorted desc, top-5.
- SELECT: `_select_worker_link` `factory.py:39-65` reuses a past request's
  `selected_worker` only if a similar request had `outcome=="success"`; else defaults
  to `"octopus_coder"` (the implicit CONSTRUCT).
- This is the only pattern-memory that actually **persists to disk** today (flat JSON).

---

## 3. The `.octo` format — what it IS and how it's used

**`.octo` is NOT a DSL and NOT a serialized chain.** It is **ordinary target-language
source code annotated with three comment-style "annealing markers."** Definitive spec:
`annealer.py:1-84` and `agents/octopus_coder/prompts.py:7-90`.

The three markers (Python flavor) `annealer.py:19-24`:
```
#>> STUB            opens a stub block (an un-filled method body)
#| actual_code      a wrapped code line (the "pipe" state)
#<< STUB            closes the stub block
```
Rules `prompts.py:26-32`: imports / class decls / signatures / docstrings stay
OUTSIDE stub blocks; only method BODIES go inside, each `#|` line being valid code
once the `#|` prefix is stripped.

**Use = the ANNEAL step:** `compoctopus.annealer.anneal('<file>.octo')` mechanically
strips `#>> STUB` / `#| ` / `#<< STUB` → emits executable code `annealer.py:86+`,
`prompts.py:212-223`. It is language-agnostic (`#` for Python/Ruby, `//` for JS/Rust/C)
`annealer.py:66-73`. The `.🐙` emoji extension is canonical; `.octo` is the ASCII alias
`annealer.py:11-13`.

**Why it exists:** it's the substrate of the self-compiling loop — the OctoCoder agent
writes `.octo` STUBS (architecture-as-structure), fills `#|` pseudocode, ANNEALs, then
pytest-VERIFYs, looping on failure (the `STUB→TESTS→PSEUDO→ANNEAL→VERIFY` cycle
`prompts.py:92-118`). The bootstrap sequence (`annealer.py:75-84`) is the D:D→D
fixed-point: a hand-written kernel compiles `.octo` agents that compile more agents.

**The two in-scope `.octo` files are STUB-state design sources, not running code:**
- `bandit.octo` — a 4th Bandit design: `Bandit` class with `lookup/select/construct/
  record/graduate/transition` over a `KeywordBasedStateMachine`
  (`LOOKUP→SELECT|CONSTRUCT→RECORD→DONE`) `bandit.octo:42-199`. EVERY body is an
  un-annealed `#>> STUB` `bandit.octo:57-60,90-97,...` — i.e. the intended logic sits
  *inside `#|` comments* and is **[STUB]** (not executable until annealed). This is
  where the regex-`task_pattern` golden-chain idea lives `bandit.octo:81-97,161-182`.
- `agent.octo` — the `CompoctopusAgent` base type as `.octo`; all `CompilerArm`
  abstract methods are empty `#>> STUB`/`#<< STUB` blocks `agent.octo:88-153`
  (the *running* `CompoctopusAgent` is the annealed `agent.py`).

---

## 4. How router / bandit are themselves `Compiler`s (D:D→D)

The type spine (router.py docstring `router.py:9-12`, re-exported from SDNA
`chain_ontology.py:18-27`):
```
Link  →  Chain(Link)  →  Compiler(Chain)  →  { Bandit, ChainSelect, ChainConstruct }
```
- A `Compiler` is a `Chain` that takes a **`TaskSpec` (a description, D) in** and
  produces a **`CompiledAgent` (also a runnable description, D) out** — i.e. `D → D`.
  `Bandit.compile(task_spec) -> CompiledAgent` `router.py:284-308` is literally that
  signature.
- Because the OUTPUT `CompiledAgent` can itself be registered as an arm and re-entered
  into `ChainConstruct`'s pipeline (`register_arm`, `compile_with_pipeline`
  `router.py:123-126,149-185`), a compiled thing becomes a new compiler-arm — the
  output feeds back as a new arm. That self-application is the **D:(D→D)** fixed point
  (`ArmKind.COMPOCTOPUS = "compoctopus"  # D:D→D — needs self-DI to exist`
  `types.py:108`). **[IS]** for the type structure & single-hop; the full recursive
  self-improvement (auto_daemon introspecting its own repo → PRs) is wired through
  OctoHead/daemon and is **[VISION]/partly built**, not exercised in this slice.
- `ChainSelect` / `ChainConstruct` are the two `Compiler` arms the head dispatches
  between; the `Bandit` is a `Compiler` whose "compilation" is *choosing which sub-
  Compiler compiles* — a compiler over compilers.

---

## 5. ASCII diagram — PRD → Bandit{Select | Construct} → (golden store ↔)

```
                       TaskSpec  (D: a description / PRD-derived spec)
                          │
                          ▼
            ┌─────────────────────────────┐
            │   Bandit (Compiler, D→D)     │   router.py:215
            │   "the head of the octopus"  │
            └──────────────┬──────────────┘
                           │ 1. LOOKUP
              ┌────────────┴─────────────┐
              ▼ EXPLOIT                  ▼ EXPLORE (on miss / low reward·count)
   ┌────────────────────┐      ┌──────────────────────────┐
   │ ChainSelect         │      │ ChainConstruct            │  router.py:110
   │ (Compiler)          │      │ (Compiler)                │
   │ router.py:42        │      │ CompilerPipeline of arms: │
   └─────────┬──────────┘      │ chain→agent→mcp→skill→     │
             │ find_for_task    │ system_prompt→input_prompt│
             │ (domain,         │ → ctx.freeze()            │
             │  feature_type,   └────────────┬──────────────┘
             │  reward≥0.8)                  │ produces a NEW
             ▼                               ▼ CompiledAgent (D)
   ╔═══════════════════════════════════════════════════╗
   ║  GoldenChainStore   (golden_chains.py:29)          ║
   ║  in-mem Dict[config_hash → GoldenChainEntry]       ║
   ║  • find_for_task = exact(domain,feature)+reward    ║   ◄── SELECT reads
   ║    argmax  (NO similarity index)                   ║
   ║  • LRU(500) + TTL(30d)                             ║
   ║  • graduate() ◄────────────────────────────┐      ║   ◄── graduation writes
   ║  • sync_to/from_carton = NotImplemented[STUB]│      ║
   ╚══════════════════════════════════════════════│═════╝
                           │ 2. run CompiledAgent  │
                           ▼ (execute the agent)   │
                  record_execution(success,turns,  │
                     human_feedback) router.py:322  │
                           │                        │
                           ▼                        │
              ┌─────────────────────────┐           │
              │ SensorStore (sensors.py) │           │
              │ reward = .4·success +    │           │
              │  .3·eff + .3·human       │           │
              │ meets_graduation_thresh? │───yes─────┘
              │ (count≥5 AND reward≥0.8) │   → graduate to golden
              └─────────────────────────┘
```

---

## Provenance / status summary
- **[IS] (runnable):** router.py decision logic, GoldenChainStore (make/keep/search,
  LRU+TTL), SensorStore reward math + graduation gate, Registry static catalog +
  keyword/tag search, the annealer `.octo` strip, agents/bandit JSON-file memory.
- **[STUB] (NotImplementedError / un-annealed octo):** all Carton persistence
  (`sync_to_carton`/`sync_from_carton` in both golden_chains.py and registry.py),
  the entire `bandit.octo` / `agent.octo` bodies, the carton-semantic-search branches.
- **[VISION] (docstring/design only):** true multi-armed-bandit sampling (it's a
  threshold cache today), similarity/embedding retrieval of patterns, the full D:D→D
  self-improvement loop, durable cross-process golden memory.
