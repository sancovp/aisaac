# Context-Alignment TypeScript Backend — Report

**Task #3 (`ca-ts`).** Add a TypeScript backend to context-alignment (CA) so it
can ingest TS codebases like Crystal Ball (CB), using **ts-morph** (the TS
compiler-API wrapper) — **without refactoring the Python**. Tested on
`/home/GOD/gnosys-plugin-v2/base/crystal-ball-alpha/lib/crystal-ball/`.

- **Branch:** `ca-typescript-backend` in `/home/GOD/context_alignment_utils`
  (reversible; the pre-existing uncommitted Python edits were carried along
  untouched — I added only `neo4j_codebase_mcp/ts_backend/`).
- **Code:** `neo4j_codebase_mcp/ts_backend/` — `project.mjs`, `extractor.mjs`,
  `deps.mjs`, `ca_ts.mjs` (CLI), `README.md`, `package.json` (+ `node_modules/`
  with ts-morph). Plain ESM, runs on `node` — no build step.

---

## STEP 1 — The Python extraction contract (what I must reproduce)

The Python CA backend has **two output layers**, both reproduced by the TS backend:

### Layer A — bulk repo → graph (`parsers/parse_repo_into_neo4j.py`)
Per file, `Neo4jCodeAnalyzer.analyze_python_file()` returns:

```
{ module_name, file_path, line_count,
  classes:   [{ name, full_name, methods:[…], attributes:[…] }],
  functions: [{ name, full_name, params, params_detailed, params_list, return_type, args }],
  imports:   [internal-module-name, …] }       # internal imports only
```

`method`/`function` shape: `params=[{name,type,kind,optional,default}]`,
`params_detailed=["name:type=default", "[kind] name:type"]`, `return_type`, `args`.

`DirectNeo4jExtractor._create_graph()` writes the **graph schema**:
- **Nodes:** `Repository{name,source_url}`, `File{name,path,module_name,line_count}`,
  `Class{name,full_name}`, `Method{method_id,name,full_name,args,params_list,params_detailed,return_type}`,
  `Function{func_id,…}`, `Attribute{attr_id,name,full_name,type}`.
- **Edges:** `(Repo)-[:CONTAINS]->(File)`, `(File)-[:DEFINES]->(Class|Function)`,
  `(Class)-[:HAS_METHOD]->(Method)`, `(Class)-[:HAS_ATTRIBUTE]->(Attribute)`,
  `(File)-[:IMPORTS]->(File)` (resolved by `module_name` prefix match).

### Layer B — per-target dependency readout (`dependency_analyzer.py`)
`CrossFileDependencyAnalyzer.analyze()` returns the "what's required to
comprehend this target" structure:

```
{ status, target, file, line_range,
  dependencies:           [{ name, type(function|class|reference), file, line_range,
                             symbol_origin(internal|external), confidence, why, why_details,
                             resolution, evidence:[{line,expr}], source_line, source_expr }],
  file_dependencies:      [{ path, operation, pattern, line, confidence, why }],
  inferred_dependencies:  [{ name, kind, line, confidence, why, expression, candidates, source_file }],
  config_lineage:         [{ kind, variable, key_path, line, confidence, why, source }],
  analysis_options:       { target_scoped, include_same_file, include_external_packages, … } }
```

Key Python behaviors I matched: **target-scoped** (analyze only the target node's
body) by default; **same-file deps omitted** by default; builtins +
`COMMON_OBJECT_METHODS` filtered as noise; `analyze_recursive()` drills
dependencies that are **`**kwargs`/`*args` passthroughs**.

MCP tool surface (`server.py`): `parse_repository_to_neo4j`,
`get_dependency_context` (Layer B, contextualizer=False), `analyze_dependencies_and_merge_to_graph`, `query_codebase_graph`.

---

## STEP 2 — The TS implementation (ts-morph)

| File | Role |
|---|---|
| `project.mjs` | Builds a ts-morph `Project`. Loads the repo's own **`tsconfig.json`** so `paths` aliases (`@/*`), `moduleResolution:bundler`, and relative imports resolve exactly as the repo compiles. Helpers for project-vs-external (package boundary) classification. |
| `extractor.mjs` | **Layer A.** `analyzeSourceFile()` → the per-file dict; `analyzeRepo()` → all files + a `{nodes,edges}` graph bundle in the Python schema shape. |
| `deps.mjs` | **Layer B.** `analyzeTargetDependencies()` + `analyzeRecursive()` → the `analyze()` structure. |
| `ca_ts.mjs` | CLI: `parse-file`, `parse-repo`, `deps` (`--whole-file --include-same-file --no-external --recursive --depth --pretty`). |

### Node-kind mapping (TS → Python concept)
- `FunctionDeclaration` → **function**
- `const X = (..)=>..` / function-expression → **function** (the TS idiom for a top-level fn; Python has no analog but this is the faithful equivalent)
- `ClassDeclaration` → **class**; its public `MethodDeclaration` → **method**; public `PropertyDeclaration` → **attribute**
- `InterfaceDeclaration` / `TypeAliasDeclaration` / `EnumDeclaration` → **Class-like node** tagged `kind:"interface"|"type_alias"|"class"` (TS extension — these are first-class "things to comprehend"; flagged so a consumer can distinguish)
- `ImportDeclaration` → **IMPORTS edge** (internal targets only)
- `CallExpression` / `NewExpression` / heritage (`extends`/`implements`) → **dependency edges** (Layer B)

### Import resolution (the hard part — handled, not hand-rolled)
ts-morph drives the **real TS language service**:
- **Relative imports** + **tsconfig `paths` aliases** (`@/*`) — resolved by loading
  the repo tsconfig into the `Project`.
- **Barrel re-exports** — CB's `lib/crystal-ball/index.ts` is a ~96 KB barrel
  imported by ~38 files. `resolveDeclarations()` uses
  `identifier.getDefinitionNodes()` (go-to-definition, follows imports) and, when
  that lands on an `ImportSpecifier`/`ExportSpecifier`, follows the
  **aliased-symbol chain** (`getAliasedSymbol().getDeclarations()`) to the
  *original* defining file + line.
- **CB-cognition rule — stop at the package boundary:** anything resolving into
  `node_modules` or a `.d.ts` is tagged `symbol_origin:"external"` and **never
  drilled**; TS builtin libs (`node_modules/typescript/lib/*.d.ts`) are dropped
  entirely as boundary noise; `COMMON_OBJECT_METHODS` (`.push`/`.get`/`.map`/…)
  are filtered (mirrors the Python filter — without it the checker resolves
  `arr.push` into `lib.es5.d.ts`).

---

## STEP 3 — Test output on Crystal Ball (verified by reading the source myself)

All runs are through the real CLI surface; each was cross-checked against the
actual `.ts` source (not against the tool's own claims).

### `reify.ts` → `reifyMineSpace` (target-scoped, default)
```
$ node ca_ts.mjs deps reifyMineSpace --root <CB> --pretty
Found reifyMineSpace in lib/crystal-ball/reify.ts (lines 79-189)
Cross-file dependencies required to understand reifyMineSpace:
  1. createKernel (function, internal, conf=0.95) — index.ts lines 186-219
  2. getKernel   (function, internal, conf=0.95) — index.ts lines 224-228
  3. lockKernel  (function, internal, conf=0.95) — index.ts lines 242-290
  4. addDot      (function, internal, conf=0.95) — index.ts lines 377-383
  5. addNode     (function, internal, conf=0.95) — index.ts lines 448-478
  6. computeSpaceSlotSignature (function, internal, conf=0.95) — kernel-v2.ts lines 420-476
```
**Ground truth (my read of reify.ts:33-47 imports + grep of index.ts/kernel-v2.ts):**
reify imports `{createKernel, addNode, addDot, lockKernel, getKernel}` from `./index`
and `{computeSpaceSlotSignature}` from `./kernel-v2`; `reifyMineSpace`'s body calls
exactly those 6. Defining lines: `createKernel`@index:186, `getKernel`@224,
`lockKernel`@242, `addDot`@377, `addNode`@448, `computeSpaceSlotSignature`@kernel-v2:420.
**✅ Exact match — and the 6 resolved THROUGH the `./index` barrel to their true defining files/lines.**
(Before the `COMMON_OBJECT_METHODS` filter, 3 noise deps `get`/`set`/`push` leaked
in from `Map`/`Array` — filter added → gone.)

### `reify.ts` → `buildFutamuraTower` (same-file handling)
- Default: **"No cross-file dependencies"** — correct: its only callees,
  `reifyMineSpace` (79-189) and `detectCatastrophes` (228-294), are **same-file**
  (and `detectCatastrophes` is non-exported), so they're omitted by default.
- `--include-same-file`: lists both with correct line ranges. ✅

### `reify.ts` structural extraction (`parse-file`)
- functions: `reifyMineSpace` L79-189, `detectCatastrophes` L228-294, `buildFutamuraTower` L305-363 (the nested `addOrbitUnder` is correctly NOT top-level)
- classes/types: `interface:ReifyResult`, `interface:CatastropheEvent`, `interface:TowerResult`, `type_alias:CatastropheClass`
- imports: `lib.crystal-ball.index`, `lib.crystal-ball.kernel-v2`
- params: `reifyMineSpace` → `["registry:Registry","sourceKernelId:number","level:number=0"]`, return `ReifyResult` (default value + return type captured). ✅

### `mine.ts` → `mine` and `computeMinePlane`
- `mine` → found `mine.ts:601-611`; default = no cross-file deps; `--include-same-file`
  = `declareMineSpace`@497 + `projectKernel`@515 — matches the body (`mine` calls both). ✅
  - **Caught a real gotcha:** a `const mine = computeMinePlane(...)` in
    `demo-orbits.ts:74` initially shadowed the `mine` function (first-by-path). Fixed:
    `findTarget` now prefers real definitions (function/class/interface) over plain
    value-consts, matching Python (which only indexes functions/classes as targets).
- `computeMinePlane` → `computeSpaceHeat`@index:572 + `isKernelComplete`@index:636.
  Verified: `computeMinePlane`'s body (lines 63-142) calls **exactly** those two
  (grep confirms 1 each; the other `./index` imports — `coordToReal`, `getViewChildren`,
  `encodeDot`, `decodeDot` — are used in *other* functions, correctly excluded by
  target-scoping). ✅

### Scale (`parse-repo lib/crystal-ball`)
53 files in **<1 s**: 156 classes/interfaces/types, 342 functions, 107 internal
imports → **1273 graph nodes, 1379 edges**. Full Layer-B contract keys + every
per-dep field present and matching Python's. ✅

---

## What works vs. gaps (honest)

### Works (verified E2E)
- Layer A per-file dict + repo graph bundle in the Python schema shape.
- Layer B dependency readout with the **full** Python field set
  (`symbol_origin/confidence/why/why_details/resolution/evidence/source_line/source_expr`).
- **Import resolution through relative + tsconfig-`paths` aliases + barrel
  re-exports** — the headline requirement — exact on reify/mine.
- Target-scoping, same-file omission, builtin/object-method noise filtering,
  package-boundary stop, recursive rest-param drill, contextualizer-style pretty readout.
- Parameter extraction incl. optional/default/rest + return types.

### Gaps / deliberate differences (do NOT treat as done where noted)
1. **No direct Neo4j write.** `parse-repo` emits a `{nodes,edges}` JSON bundle in
   the exact schema shape; it does **not** run the Cypher `MERGE`s that Python's
   `_create_graph` does. Wiring is mechanical (a thin Python adapter, or a JS
   neo4j-driver writer) but intentionally not done — keeps the backend
   self-contained and avoids refactoring the Python per the task constraint. **VISION.**
2. **MCP server not extended.** `server.py` still only routes Python. The TS
   backend is a standalone CLI; a future `server.py` change could `subprocess` to
   `ca_ts.mjs` for `.ts/.tsx` repos. Not done (would edit Python). **VISION.**
3. **`file_dependencies` / `config_lineage` are best-effort**, lighter than
   Python's. Detected: `fs.read*/write*` + dynamic `import('lit')` (file deps);
   `JSON.parse` + `process.env.X` (config). Python additionally tracks
   config-variable **propagation** through assignments/subscripts/dispatch — not
   ported. **PARTIAL.**
4. **`inferred_dependencies`** covers computed/element-access calls + unresolved
   names (with name-index candidates). Python's `getattr`/dynamic-subscript/config-
   dispatch lineage is richer. **PARTIAL.**
5. **Name ambiguity:** `findTarget` picks the first real definition by
   (path, line). No file-qualified target yet — identical to the Python
   limitation. For an ambiguous name, the first match wins. **KNOWN LIMITATION.**
6. **Interfaces/type-aliases/enums** are emitted as Class-like nodes (`kind` tag).
   This is a TS extension with no Python analog; documented so consumers can filter.
7. **External resolution** lands in `.d.ts` type stubs (not real impl, unlike
   Python's site-packages source), so it's marked `external` and not drilled.
   `--no-external` gives a pure in-package readout.

### How to run
```
cd neo4j_codebase_mcp/ts_backend
node ca_ts.mjs deps <Target> --root <repo> --pretty
node ca_ts.mjs parse-file <file.ts> --root <repo>
node ca_ts.mjs parse-repo <repo> [--name <repoName>]
```
