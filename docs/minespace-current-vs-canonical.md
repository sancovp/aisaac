# CB Current mineSpace vs THE Canonical mineSpace — The Diff

**Task #4 (minespace-explorer).** Premise: CB's current code "mineSpace" is NOT the real mineSpace; find the precise gap.
**Method:** full-read of the code (code is source of truth, not the doc-comments inside it). Every claim is cited `file:line`.
**Canonical source read:** `/home/GOD/gnosys-plugin-v2/base/crystal-ball-alpha/lib/crystal-ball/` (newer copy, git `1d951db` 2026-05-12; `mine.ts`, `mine-view.ts`, `engine.ts` are byte-identical to the `/tmp/crystal-ball-alpha` clone — only `index.ts` differs, and the differing lines are not mine/lock related, so this is THE current code).
**Canonical def source:** the carton MCP tools (`mcp__carton__get_concept` / `query_wiki_graph`) were **NOT available** in this worker's toolset (errored: "No such tool available"). The canonical definition used here is the verbatim spec carried in the Task #4 description (the rollup `Doc_Mirror_System_Gnosys_Session_Rollup_2026_06_06T05_04_13` / `Minespace_Epistemics`). UNVERIFIED-against-graph; verify the canonical text against CartON when the MCP is reachable.

---

## 0. THE CANONICAL mineSpace (the target shape, verbatim from the spec)

> lock a kernel (a tree of arbitrary strings = a declared ontology shape; its EWS = the domain chain)
> → enter its mineSpace = a **PLAIN coordinate space, infinite + totally ordered**; **ANY point flash-decodes** (via the alphabet)
> to a **meaningful-or-not foundation-ontology instance** (an is_a/has_part/produces web, decodable to English);
> **mine it** (heatmap of **generation preferences** + **LLM swarms make sibling options**);
> **freeze a chosen config** → its **sub-mineSpace** = the instance-specific configs of THAT class → **recurse** (the Y1–Y6 tower / Instance-as-Class recursion);
> **a point = z = x+iy ADDRESS of a semantic web, not a bare number.**

Six load-bearing claims to check against the code: (C1) plain/infinite/total-order space; (C2) ANY point flash-decodes to a foundation-ontology web; (C3) decodable to English (is_a/has_part/produces); (C4) heatmap = generation preferences + LLM-swarm sibling generation; (C5) freeze→sub-mineSpace→recurse (Y1–Y6); (C6) point = z=x+iy address-of-a-semantic-web, not a bare number.

---

## 1. WHAT THE CURRENT mineSpace ACTUALLY DOES (IS — cited)

There are **three distinct things in the code that all carry the name "mine/mineSpace"** — they are not one coherent object. This is itself part of the gap.

### 1a. `computeMinePlane` — a finite ENUMERATION of already-built nodes (`mine.ts:63-142`)
- Walks the **existing** child tree of one locked space (`enumeratePaths`, `mine.ts:159-258`), recording every existing node as a `ValidPath` (`mine.ts:206-217`). It reads `space.nodes` — **only nodes that have already been constructed exist as points.** Nothing is decoded from a coordinate that wasn't already built.
- **Bounded, not infinite:** hard cap `maxPaths = 2000` (`mine.ts:67,170,177`).
- A "point" is a `MinedPoint { x, y, heat, label, coordinate, depth }` (`mine.ts:37-45`) whose `(x,y)` come from a **radial/grid layout for visualization** (`projectPathsToPlane`, `mine.ts:262-357`; `x = cos(angle)*radius`, `y = depth*2`, `mine.ts:297-316`) — i.e. a heat-map plot, **NOT** the encoding address.
- `heat` (`mine.ts:318-338`) is **proof/sorry state**: `frozen→0.0` (proven/cold), `locked→0.1`, else base `0.4–0.7` scaled down by the fraction of frozen siblings. It is a *coherence/anneal* signal, **not** "generation preference."
- Ш-detection: `frozenRatio === 1.0 ⇒ shaDetected` (100% coherence) (`mine.ts:112-128`).

### 1b. `mine()` / `projectKernel` / `MineSpace` — a real (x,y) plane keyed to a deliverable (`mine.ts:454-611`)
- `MineSpace { deliverable, origin:{0,0}, known: KnownPoint[], projectedKernels }` (`mine.ts:486-491`). This is the object the doc-comment calls "what mineSpace actually IS … a flat 2D plane equipped with a CB coordinate encoder" (`mine.ts:454-466`).
- Here the `(x,y)` ARE the encoding: for each enumerated valid path, `encoded = encodeDot(coordinate)` then `{x,y} = realToPlane(encoded)` (`mine.ts:538-539`). `realToPlane` (`mine.ts:381-399`) is a genuine **ℝ→ℝ² digit-interleaving bijection** (odd digits→x, even→y), reversible via `planeToReal` (`mine.ts:408-416`). **This is the only place the canonical "z=x+iy address" idea is literally realized** — and even here x and y are two separate `number`s, never a complex `z`.
- `projectKernel` (`mine.ts:515-593`) marks enumerated paths `status:'valid'` (`mine.ts:550`) and **synthesizes `'adjacent'` points** by ±N integer perturbation of each coordinate segment (`mine.ts:556-592`). Adjacency = arithmetic neighbors of EXISTING coordinates, capped by `adjacentDepth=2`. No decoding-to-semantics happens; the only "meaning" carried is the original node's `label` (`mine.ts:545-551`).

### 1c. `mineConfigurations` — the cartesian config tuple space (the user-facing `mine` command) (`mine.ts:718-794`)
- This is what the `mine` REPL command actually runs (`engine.ts:684-717`). `extractDimensions` (`mine.ts:646-672`) takes **depth-1 nodes as dimensions** and **depth-2 nodes as their children** — i.e. exactly TWO levels, flat.
- `totalConfigs = product of dimension child counts` (`mine.ts:733`) — a Cartesian product count.
- It emits **only the current config + one-dimension-at-a-time neighbors** (`mine.ts:743-791`): one `'valid'` current point (`mine.ts:748-761`) and, for each dim, the configs that differ in exactly that one dim (`mine.ts:764-790`). It does **not** enumerate the full product, and does **not** recurse.
- `heat` here is **cosmetic/color-by-dimension**: current `=0.0`, neighbor `=0.3+(dimIdx/dims.length)*0.4` (`mine.ts:756,784`). Not a preference signal.

### 1d. Decoding-to-semantics exists, but on a SEPARATE path (`mine-view.ts` + `buildUARL`)
- `buildUARL(space, nodeId)` (`index.ts:2393-2456`) is the closest thing to "decode a point to an is_a/has_part/produces web": it emits `subject is_a parent, has_part children…, produces producedSpace…` (`index.ts:2407-2453`). **BUT** it reads an **existing node** (`space.nodes.get(nodeId)`, `index.ts:2394`); it derives predicate/object from the node's **already-present** label, parent, and children. It cannot take an arbitrary coordinate/point and synthesize a web — the node must already exist.
- `computeMineView` (`mine-view.ts:160-267`) is the `view` command (`engine.ts:766-772`), not the `mine` command. It builds the LLM prompt (`renderPromptView`, `mine-view.ts:271-376`) from existing self/parent/sibling/child nodes + UARL + kernel matrix. This is where the foundation-ontology semantics live — but keyed to **built** nodes, decoupled from the `MineSpace` (x,y) plane.

### 1e. The lock flow (IS — cited)
- `lockKernel(registry, globalId)` (`index.ts:242-290`): a kernel locks **iff** every node with a `kernelRef` has a locked sub-kernel (`index.ts:251-258`) AND every non-terminal node with children has ≥2 children (the "spectrum needs a high and a low" check, `index.ts:260-282`). Recursive over sub-kernels via the `kernelRef→subKernel.locked` chain. This realizes the canonical "lock a kernel" precondition.
- `isKernelComplete(space)` (`index.ts:636-654`): `complete` iff every slotted node (`slotCount>0`) is `locked`. Used by `computeMinePlane` (`mine.ts:87`) only to set the origin's heat — **completeness does NOT gate entry into a mineSpace.**
- The encoding alphabet is real and present: digit semantics `0=superposition, 1-7=select, 8=drill, 88=close-drill, 9=wrap(+7)` (`index.ts:656-811`), structural delimiters `DOT=8988, KERNEL_OPEN=90, KERNEL_CLOSE=900` (`index.ts:819-823`), `encodeDot/decodeDot/coordToReal` (`index.ts:826-840`). EWS/domain-chain is modeled (`Space.ewsRef`, `Space.isEWS`, `index.ts:149-150`).

---

## 2. THE PRECISE GAP (canonical vs current)

| # | Canonical claim | Current code | Verdict |
|---|---|---|---|
| C1 | mineSpace = a **plain coordinate space, infinite + totally ordered** | `computeMinePlane`/`mineConfigurations` **enumerate finite sets of already-built nodes** (cap 2000, `mine.ts:67`; or current+1-dim neighbors, `mine.ts:743-791`). `MineSpace.known` is a list you push existing/adjacent points into (`mine.ts:489,541,579`). | **DECOHERED.** The plane object exists (`mine.ts:486-491`) and the encoding gives a total order in principle (`coordToReal`, `index.ts:836`), but the runtime "mineSpace" is a **finite materialized point list of what was already constructed**, not an infinite ambient space you address into. |
| C2 | **ANY point flash-decodes** to a (meaningful-or-not) foundation-ontology instance | Decoding-to-web (`buildUARL`, `index.ts:2393`) requires the **node to already exist** in the space. An arbitrary coordinate that wasn't built has no label/parent/children → no web. `decodeDot` (`index.ts:831`) only recovers the dotted coordinate string, not a semantic web. | **MISSING.** There is no "given (x,y)/real, flash-decode to an is_a/has_part/produces instance" function. The points that decode are exactly the ones already enumerated; there is no decode of the *empty* ambient space. |
| C3 | decodable to **English** (is_a / has_part / produces web) | `buildUARL` DOES produce `is_a/has_part/produces` English-ish UARL (`index.ts:2407-2453`). | **PRESENT-BUT-DIFFERENT / decoupled.** The capability exists, but on the `view`/`buildUARL` path over **built** nodes — it is not the decode-of-an-arbitrary-mineSpace-point the canonical means, and it is not attached to `MineSpace` points (those carry only `label`, `mine.ts:545-551`). |
| C4 | mine = **heatmap of generation preferences** + **LLM swarms make sibling options** | `heat` everywhere is **proof/sorry/anneal state** (`frozen=cold`, `mine.ts:324-338`) or **cosmetic color-by-dimension** (`mine.ts:756,784`). Sibling generation is **not** in the mine path: `'adjacent'` points are ±N **arithmetic** perturbations (`mine.ts:556-592`) and config neighbors are existing children (`mine.ts:764-790`). LLM generation lives on the separate `0`-superposition/`view` path (`mine-view.ts`, `index.ts:842+`), not invoked by `mine`. | **DECOHERED (heat) + MISSING (preference + swarm).** Heat measures the wrong axis (coherence, not preference). No LLM-swarm produces sibling options inside mineSpace. |
| C5 | freeze a config → its **sub-mineSpace** = instance-specific configs of THAT class → **recurse** (Y1–Y6 / Instance-as-Class) | `mineConfigurations` is **flat, 2 levels** (`extractDimensions` depth-1 dims / depth-2 children, `mine.ts:651-652`) and does not recurse. Recursion machinery exists but ELSEWHERE: drill `8`/`producedSpace` (`mine.ts:236-256`, `index.ts:601-620`), `Stratum` Y1–Y6 (`index.ts:50-65`), `reifyMineSpace`/`buildFutamuraTower` (imported `engine.ts:58`). Freezing a config does **not** spawn a sub-mineSpace of instance configs. | **PRESENT-BUT-DIFFERENT.** The Y1–Y6 tower + drill exist as separate operations; the canonical "freeze→sub-mineSpace→recurse" loop is **not wired into the mine flow.** |
| C6 | a point = **z = x+iy ADDRESS of a semantic web**, not a bare number | `realToPlane` gives a true (x,y) **address** that round-trips to the encoded real (`mine.ts:381-416`) — but x and y are two `number`s, never a complex `z`, and the "semantic web" at that address is only the single node `label` (`mine.ts:545-551`), not a web. Meanwhile `computeMinePlane`'s `(x,y)` are a **layout artifact** (`mine.ts:297-316`), not the address at all. | **PARTIAL / DECOHERED.** The address-bijection is the one canonical piece genuinely realized (`mine.ts:381-416`). But (a) it's not a complex `z`, (b) the address points at a label not a web, and (c) the *user-facing* `mine` plot uses non-address (x,y). |

### One-line summary of the gap
The current code has the **encoding alphabet** (real), the **address bijection ℝ↔ℝ²** (real, `mine.ts:381-416`), the **lock precondition** (real, `index.ts:242-290`), and **decode-to-UARL** (real but on a separate path, `index.ts:2393`). What it does **not** have is the canonical mineSpace's defining move: an **infinite ambient coordinate space where ANY address flash-decodes to a foundation-ontology web** and where **mining = preference-heat + LLM-swarm sibling generation** that **recurses freeze→sub-mineSpace** through Y1–Y6. Today "mineSpace" = a **finite enumeration/cartesian-tuple list of already-built nodes for visualization + DB persistence** (`engine.ts:684-717`), with the semantic-decode and the Y-tower recursion living on adjacent, unconnected code paths.

---

## 3. WHAT WOULD HAVE TO CHANGE (a diff, not a rewrite — direction only; UNVERIFIED designs)

These are deltas implied by §2, expressed as the smallest moves that close each gap. Each is VISION until built/tested.

1. **C2/C3 — add an address→web decoder.** Introduce `decodeAddressToWeb(real | {x,y})`: `planeToReal`→`decodeDot`→parse coordinate→**synthesize** (not look up) an `is_a/has_part/produces` instance via the alphabet, returning a web even for un-built coordinates ("meaningful-or-not"). Today `buildUARL` (`index.ts:2393`) only reads built nodes; the new function must produce a web from the coordinate grammar alone, then optionally bind labels where nodes exist.
2. **C1 — make mineSpace ambient, not materialized.** Treat `MineSpace` (`mine.ts:486`) as an addressable function over the totally-ordered encoding, with enumeration as a *windowed view* into it; drop/relativize the `maxPaths=2000` cap (`mine.ts:67`) as a render window, not the space's extent.
3. **C4 — split the two heats and add the swarm.** Keep the proof/anneal heat (`mine.ts:324-338`) but add a distinct **generation-preference** weight, and route the **LLM-swarm sibling generation** (currently on the `0`/`view` path) INTO `mine` so mining produces sibling options, not ±N arithmetic neighbors (`mine.ts:556-592`).
4. **C5 — wire freeze→sub-mineSpace→recurse.** On freeze of a config, spawn the chosen node's `producedSpace`/sub-kernel as the next mineSpace and recurse, walking `Stratum` Y1→Y6 (`index.ts:50-65`) — i.e. connect the already-present drill/reify/tower machinery (`mine.ts:236-256`, `engine.ts:58`) to the `mineConfigurations` flow.
5. **C6 — make the point a z-address-of-a-web.** Represent a mined point as `z=x+iy` (or keep (x,y) but) **carrying the decoded web** from move (1), so a point IS the address of a semantic web, and make the user-facing `mine` plot use the **address** (x,y) (`mine.ts:381`) rather than the layout artifact (`mine.ts:297-316`).

---

## 4. Honesty markers
- **IS (read from code, cited):** §1 in full; §2 verdicts; the encoding alphabet, the ℝ↔ℝ² bijection, the lock precondition, `buildUARL`'s is_a/has_part/produces, the three-named-mineSpace fragmentation.
- **UNVERIFIED:** the canonical text itself (carton MCP unavailable this run — taken verbatim from the Task #4 spec; re-verify against `Doc_Mirror_System_Gnosys_Session_Rollup_2026_06_06T05_04_13` / `Minespace_Epistemics` when reachable).
- **VISION (not built):** all of §3.
- **Scope note:** read the monorepo copy (`base/crystal-ball-alpha`, the newer one) as current; `mine.ts`/`mine-view.ts`/`engine.ts` identical across both clones, so the diff holds for both. Did not exhaustively read all 2632 lines of `index.ts` / 3246 of `engine.ts` — read the complete operational boundary of mine/lock/encode/decode (the cited ranges) per the task's named entrypoints.
