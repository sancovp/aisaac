# Crystal Ball — System Architecture Map

**Scope:** `/home/GOD/gnosys-plugin-v2/base/crystal-ball-alpha` — engine modules in
`lib/crystal-ball/` (~50 .ts files: ~24 library modules + 14 demo drivers + 8 tests +
a `needs-rework/` dir excluded by tsconfig) and the `app/api` routes that wire the
engine into the SaaS. Read on `main` (the `cb-recohere-youknow-strata` branch is
meaning-only, so the wiring/callgraph here is identical; strata are now the canonical
youknow names foundation/domain/instance/instance_subtype_generator/domain_generator/
instance_generator).

**Method:** dependency graph grounded in the **CA-TypeScript backend** (the ts-morph
tool built in task #3: `node ca_ts.mjs parse-repo <root>` over the whole repo = 108
files, + `deps <symbol>` readouts), NOT grep. Importer counts below are real
import-edge counts (app + lib) from the tool. Code is the source of truth.

---

## 1. What this system IS (one paragraph)

Crystal Ball is a **coordinate-ontology compiler**: a Space is a DAG of nodes where
children ARE the spectrum, a coordinate is a dot-path selecting nodes, `0` means
superposition (unfilled / class-slot) and `1-7` mean a filled selection (instance).
The core loop is **scry → resolve → bloom → lock → freeze**: a perturbation daemon
(`scry.ts`) finds superposition `0`-slots, calls an LLM swarm (`swarm-agent.ts`) to
collapse them, grows/blooms the space, and checks a catastrophe surface (`reify.ts`'s
Futamura tower, the `Ш` count) — reverting any fill that raises `Ш`, converging toward
"crowning" (`Ш = 0`). On **freeze**, a node's context is rendered to a **UARL** statement
(`buildUARL`) and validated through **youknow()/SOMA** (`youknow-bridge.ts`, via
`docker exec mind_of_god`) — the one seam where CB hands a claim to the foundation
validator. Everything else (`kernel-v2`, `mine`, `cft`, `morphism`, `griess`, `algebra`,
`chirality`, `fractran`, `ews`, `mine-view`, `kernel-function`) is an **equivalence view**:
a different mathematical lens (RKHS, mineSpace, CFT, category theory, Griess/Monster,
FRACTRAN) computed over the *same* DAG. The whole math core is wrapped by **`engine.ts`**,
the SaaS facade that persists Spaces to a Postgres `spaces` table (drizzle) and is called
by 8 `app/api` routes; `auth.ts` (API keys) and `event-bus.ts` (SSE) are the other live
SaaS pieces. The youknow / Y-strata layer tags each node with a stratum → Y-level →
UARL claim; that tagging feeds the freeze→youknow validation.

---

## 2. Module table (role / live-dead / importers / purpose)

Importers = total static import edges (app+lib) per the CA-TS tool.

| Module | Role | Live? | Importers (app+lib) | Purpose |
|---|---|---|---|---|
| `index.ts` | **canonical-core** (foundation) | LIVE | 46 (2 app, 42 lib) | Encoding/DAG engine: Space/CBNode, createKernel/addNode/bloom/lockKernel/freezeNode, coordToReal/encodeDot, Born weights/superposition, Stratum + STRATUM_TO_Y + Y_LAYER_SEMANTICS, buildUARL/buildSpaceUARL, **freezeWithYouknow**, serialize/deserialize. Everything imports it. |
| `engine.ts` | **SaaS facade / orchestrator** | LIVE | 8 (8 app) | `cb(teamId,input)` interaction entrypoint; loadCb/saveCb to the drizzle `spaces` table; getSession; imports the entire math core + `execSync` docker for youknow. THE app-facing entry. |
| `kernel-v2.ts` | equivalence-view (RKHS) | LIVE | 15 (lib) | Slot/spectrum signatures, kernel temperature, slot orbits, tensor/gram. Most-used view. |
| `mine.ts` | equivalence-view (mineSpace) | LIVE | 11 (1 app,10 lib) | Configuration mineSpace: computeMinePlane, mine, mineConfigurations, realToPlane. |
| `reify.ts` | canonical-core (tower) | LIVE | 6 (lib) | The T operator: reifyMineSpace, buildFutamuraTower, catastrophe classes A–E, `Ш`, crowning. |
| `kernel-function.ts` | equivalence-view (RKHS) | LIVE | 4 (lib) | RKHS kernel function, eigenvalues, hybridKernel, foundationSignature. |
| `youknow-bridge.ts` | **bridge (SOMA seam)** | LIVE | 4 (lib) | callYouknow() via `docker exec mind_of_god`; feedSpaceToYouknow, buildStatementsFromSpace, queryLabel. The youknow()/SOMA validation seam. |
| `griess.ts` | equivalence-view / phase | LIVE | 3 (lib) | Griess constructor, κ_user, verifyKappa, griess-phase state machine, tryAdvanceFromCB. |
| `morphism.ts` | equivalence-view (category) | live-peripheral | 3 (lib: cft, chirality, test) | Category-theoretic foundation (functors/associativity). Consumed by cft/chirality/tests. |
| `swarm-agent.ts` | **canonical-core (LLM gen)** | LIVE | 3 (lib: engine, gmr, scry) | The LLM measurement: runSwarm/runBatchSwarm/execSwarmViaDocker, computeAlgebraNeighborhoods. The generator. |
| `algebra.ts` | equivalence-view | LIVE | 2 (lib: cft, engine) | CB algebra "the missing multiplication", analyzeAlgebra. |
| `cft.ts` | equivalence-view (CFT) | live-peripheral | 2 (lib: test-cft, test-cft-alpha-sweep) | 2D CFT consistency analysis. Only test importers → NOT in the live compile path. |
| `gmr.ts` | canonical-core (support) | LIVE | 2 (lib: engine, scry) | Geometric Manifold Rectification — cleans Born support before the swarm. |
| `scry.ts` | **canonical-core (daemon)** | LIVE | 2 (lib: compile, engine) | The perturbation daemon / generation loop (see flow §4). |
| `uarl-aligner.ts` | bridge (Monster-demo) | demo-only | 2 (lib: populate-monster-cb, test-uarl-aligner) | ANY ontology→UARL→CB; PREDICATE_ALIGNMENTS predicate→Y table. **Monster-demo-only** (FOCUS#1). |
| `chirality.ts` | equivalence-view | live-peripheral | 1 (lib: test-cft) | Chirality analysis of spaces. |
| `compile.ts` | **canonical-core (compiler)** | LIVE | 1 (lib: engine) | Griess single-pass compiler: DERIVE→COMPUTE→BUILD(scry)→VERIFY(verifyKappa+youknow)→ONT/SOUP; kappaToUARL, applyYouknowCorrections, meta_compile. |
| `fractran.ts` | equivalence-view | demo-only | 1 (lib: demo-fractran) | FRACTRAN lens. Only a demo imports it. |
| `homoiconic.ts` | **canonical-core (Lisp)** | LIVE | 1 (lib: engine) | The CB Lisp: cbEval(=scry)/cbQuote/cbApply/cbWalk; "the ONLY layer that interprets coordinates against the DAG." |
| `lean-export.ts` | bridge (Lean4) | peripheral | 1 (lib: monster-bridge) | Export spaces to Lean 4 theorem scaffolds (frozen→theorem, unfrozen→sorry). |
| `mine-view.ts` | equivalence-view | LIVE | 1 (lib: engine) | "Full mathematical view from any position" — composes UARL + Y-layer + Born/amplitude. |
| `monster-youknow-adapter.ts` | bridge (Monster) | demo-only | 1 (lib: test-monster-adapter) | Monster ontology → CB/UARL types (MONSTER_TYPES). |
| `auth.ts` | SaaS infra | LIVE | 4 (4 app) | API-key auth (withApiKeyAuth) for the routes. |
| `event-bus.ts` | SaaS infra | LIVE | 2 (2 app) | In-process pub/sub (cbEventBus) for SSE → frontend push. |
| `ews.ts` | equivalence-view | **DEAD** | 0 | EWS (Emergent Web Structure) computation — **0 importers per the tool**. Orphaned/leaf. |
| `space-data.ts` | infra/helper | **DEAD** | 0 | "Space Data Helper" — 0 importers. Orphaned. |
| `monster-bridge.ts` | bridge/script | DEAD (script) | 0 | meta-introspector/monster ↔ CB bridge; runnable, nothing imports it. |
| `encode-monster.ts` | script | DEAD (script) | 0 | Feeds the Monster ontology into youknow(). Runnable entrypoint. |
| `populate-monster-cb.ts` | script | DEAD (script) | 0 | Full Monster→UARL→CB pipeline. The one real consumer of uarl-aligner. |
| `demo-*.ts` (14) | driver | entrypoint | 0 each | Runnable demos (foundation, superposition, tower, tower-v2, orbits, kernelspace, kernel-v2, kernel-hs, futamura, fractran, funnel-kernel, tweet-kernel, mine-comprehensive, attractor-tests). 0 importers is expected. |
| `test-*.ts` (8) | test-only | entrypoint | 0 each | cft, cft-alpha-sweep, kernel-coupling, monster-adapter, morphism, regression, uarl-aligner, views. |
| `needs-rework/` | excluded | — | — | demo-attractor-tests, demo-tower (dup copies); tsconfig `exclude`s this dir. |

---

## 3. SaaS → engine wiring (the app surface)

```
HTTP client / frontend
   │
   ▼  (API key)
app/api/**/route.ts  ──auth──> auth.ts: withApiKeyAuth
   │  cb/route.ts, spaces/route.ts, spaces/[space]/scry/route.ts,
   │  mine/route.ts, crystal-ball/route.ts, cb/flow|spaces/route.ts,
   │  spaces/[space]/route.ts                      (8 routes import engine)
   ▼
engine.ts:  cb(teamId, input)            [engine.ts:421]
   ├── loadCb(teamId, space)  ◄────► Postgres `spaces` table (drizzle)   [engine.ts:309/351]
   ├── getSession(teamId)                                                [engine.ts:211]
   └── orchestrates the math core (index/homoiconic/scry/swarm/mine/reify/griess/compile/...)
app/api/events/route.ts ──► event-bus.ts: cbEventBus  (SSE push to frontend)
app/api/spaces/[space]/seed|mine/route.ts ──► index.ts / mine.ts directly
```

---

## 4. CORE FLOW (the compile/scry path, with file:line)

```
DECLARE        engine.cb()                              engine.ts:421
   │           κ_user / space declared; createKernel    index.ts:186 (createKernel)
   ▼
BLOOM/GROW     addNode / bloom → 0-slots (superposition)  index.ts:448 (addNode); 0 = unfilled
   ▼
SCRY (daemon)  scry(registry, space, maxIter)            scry.ts:131
   │  1. findSuperpositions (Born weight>0)              scry.ts:70
   │  2. computeAlgebraNeighborhoods                     swarm-agent.ts (via scry.ts:165)
   │  3. GMR rectify Born support                        gmr.ts rectifySpace (scry.ts:221)
   │  4. runBatchSwarm  ── LLM measurement ──►           swarm-agent.ts (scry.ts:224)
   │        execSwarmViaDocker (the LLM call)            swarm-agent.ts
   │  5. catastrophe check: buildFutamuraTower → Ш       reify.ts:305 (scry.ts:149/298)
   │  6. if Ш increased → setAmplitude 0 (REVERT)        index.ts (scry.ts:242)
   │  7. tryAdvanceFromCB (griess phase)                 griess.ts (scry.ts:293)
   │  8. repeat until collapsed / crowned / critical
   ▼
RESOLVE/EVAL   cbEval = scry a coordinate against DAG    homoiconic.ts:84 (cbEval)
   ▼
LOCK           lockKernel / lockNode (instantiation done) index.ts:242 (lockKernel)
   ▼
FREEZE+VALIDATE  freezeWithYouknow(space,node,youknowFn) index.ts:2491
   │  buildUARL(node) → UARL statement                   index.ts:2393
   │  youknowFn(uarl.raw) ── docker exec ──►             youknow-bridge.ts:62 callYouknow
   │        `docker exec mind_of_god python3 … youknow()` youknow-bridge.ts:169
   │  accepted → freezeNode('youknow'); rejected → no freeze, return reason  index.ts
   ▼
COMPILE wrap   compile(): DERIVE→COMPUTE→BUILD(scry)→VERIFY(verifyKappa+youknow)→ONT|SOUP  compile.ts:196
```

`freezeWithYouknow` (index.ts:2491) is, by its own docstring, "the ONLY CB operation
that triggers YOUKNOW validation."

---

## 5. FOCUS answers

**#1 — Where is `uarl-aligner` used? (lead: only populate-monster-cb)**
CONFIRMED by the CA-TS tool + grep cross-check: `uarl-aligner.ts` is imported by exactly
two files — `populate-monster-cb.ts` (the Monster-ontology→UARL→CB script) and
`test-uarl-aligner.ts`. Both have **0 importers themselves** (a script + a test), and
neither is reached from `engine.ts` or any `app/api` route. So the aligner — and its
`PREDICATE_ALIGNMENTS` predicate→Y table — is **Monster-demo-only and low-stakes**: it is
NOT in the live SaaS compile/scry path. (This is why the recohere task left the
predicate→Y mapping intact and merely flagged it — nothing live depends on it.)

**#2 — Canonical compiler core vs equivalence views vs bridges**
- **CANONICAL CORE (the compiler itself):** `index.ts` (the DAG/encoding foundation),
  `homoiconic.ts` (eval/quote/apply Lisp), `scry.ts` (the perturbation/generation daemon),
  `swarm-agent.ts` (the LLM measurement/generator), `compile.ts` (the Griess single-pass
  compiler), `reify.ts` (the Futamura tower / Ш / crowning), `gmr.ts` (Born-support
  rectification). All wired into `engine.cb()` and the scry loop.
- **EQUIVALENCE VIEWS (math lenses on the same DAG):** `kernel-v2` (RKHS, the most-used),
  `kernel-function` (RKHS kernel/eigenvalues), `mine` + `mine-view` (mineSpace), `griess`
  (Griess/κ phase), `algebra` (multiplication), `cft` (2D CFT consistency — **test-only
  consumers**), `morphism` (category theory — view-of-views), `chirality` (test-only),
  `fractran` (demo-only), `ews` (**0 importers — dead**).
- **BRIDGES (to external systems):** `youknow-bridge` (→ youknow()/SOMA via docker — LIVE,
  the validation seam), `uarl-aligner` (ANY→UARL→CB — Monster-demo-only), `monster-youknow-adapter`
  (Monster types — test-only), `monster-bridge` + `encode-monster` + `populate-monster-cb`
  (Monster pipeline scripts — 0-importer entrypoints), `lean-export` (→ Lean4 scaffolds —
  reached only from monster-bridge).
- **SaaS INFRA:** `engine` (facade), `auth` (API keys), `event-bus` (SSE).

**#3 — How youknow / Y-strata flows now**
The Stratum tag (now canonical `foundation`/`domain`/`instance`/`instance_subtype_generator`/
`domain_generator`/`instance_generator`) lives on each `CBNode` (index.ts:102). On any node,
`buildUARL` (index.ts:2393) maps `node.stratum → STRATUM_TO_Y` (index.ts:2262) → a `y_layer`
+ `griess_phase` + the `Y_LAYER_SEMANTICS` meaning (index.ts:2300), producing the UARL claim
string. The generation flow: an LLM (the swarm) fills `0`-slots (superposition) during
`scry` → the space grows (resolve/bloom) → on **freeze**, `freezeWithYouknow` (index.ts:2491)
renders `buildUARL`/`buildSpaceUARL` (index.ts:2462) and calls the injected `youknowFn`,
which in the live path is `youknow-bridge.callYouknow` (youknow-bridge.ts:62) running
`docker exec mind_of_god python3 … print(youknow(stmt))` (youknow-bridge.ts:169) — i.e. the
claim is validated by youknow()/SOMA and persisted to ONT (or rejected with feedback).
`compile.ts` closes the loop: `applyYouknowCorrections` feeds youknow's verdict back as
amplitude changes (compile.ts:129). The Y-strata are thus the *labels* the validator reads;
the recohere corrected what those labels MEAN (Y1=foundation is SOMA-provided; flow starts
at Y2; Y4/Y5/Y6 are the level-typed generators) without touching this mechanical flow.

---

## 6. LIVE vs DEAD summary

- **LIVE compiler core (in the engine/scry path):** index, homoiconic, scry, swarm-agent,
  compile, reify, gmr + the views the core pulls: kernel-v2, kernel-function, mine,
  mine-view, griess, algebra.
- **LIVE SaaS:** engine (8 routes), auth, event-bus, + the 15 `app/api` routes.
- **LIVE bridge:** youknow-bridge (the SOMA seam).
- **LIVE-but-peripheral (only test/demo/view consumers, NOT the SaaS path):** cft &
  chirality (test-only), morphism (cft/chirality/tests), fractran (demo-only),
  uarl-aligner + monster-youknow-adapter (Monster-demo/test-only), lean-export (monster-bridge only).
- **DEAD (0 importers, not a demo/test/script):** **`ews.ts`** and **`space-data.ts`** — nothing
  imports them per the tool. (ews.ts is notable: the Emergent-Web-Structure computation is
  NOT statically wired into the live engine.)
- **Scripts (0-importer runnable entrypoints, Monster pipeline):** monster-bridge,
  encode-monster, populate-monster-cb.
- **Drivers / tests (0 importers, expected):** 14 `demo-*`, 8 `test-*`.

---

## 7. UNCLEAR / could-not-determine

1. **RESOLVED (was UNCLEAR): `engine.cb()` is a COMMAND ROUTER**, not a single fixed path.
   It dispatches on the `input` string to whichever operation the user/route names:
   `"scry [N]"` → the full scry daemon (engine.ts:1073); `"compile"` → griessCompile
   (engine.ts:1031); a freeze command → `freezeWithYouknow(crystal, node.id, session.youknowFn)`
   (engine.ts:1271 & 1378 — the live youknow seam uses an INJECTED `session.youknowFn`);
   direct fills via `applySwarmActions` (engine.ts:1518) / `execSwarmViaDocker` (engine.ts:1824,
   tower context); mine via `computeMinePlane`/`computeMineSpace` (686/1471). So BOTH the scry
   loop and a direct swarm fill are reachable, selected by command — confirmed by reading the dispatch.
2. **`ews.ts` truly dead vs dynamically/planned-used.** 0 static importers per the tool ⇒
   DEAD as wired. If something invokes it via a non-import path (string eval, planned route)
   the tool wouldn't see it — but no such path was found. Flag for confirmation.
3. **`cft.ts` live status.** Only test files import it ⇒ the CFT-consistency analysis is not
   in the live compile path (consistent with the architecture decision to route CB toward
   Scott-domain semantics, not CFT). Stated as test-only; not a defect.
4. **Importer counts are STATIC import edges**, not runtime call frequency; a module with 1
   importer (e.g. `compile.ts` ← engine) can still be central. Counts indicate wiring, not
   importance — role column disambiguates.

---

*Map generated read-only; dependency graph grounded in the CA-TypeScript backend
(ca_ts.mjs parse-repo/deps over 108 files), cross-checked against full reads of
index.ts/scry.ts/compile.ts/homoiconic.ts/reify.ts/youknow-bridge.ts and the api routes.
Code is the source of truth.*
