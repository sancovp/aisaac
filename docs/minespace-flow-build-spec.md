# Canonical mineSpace / FLOW — Build Spec (for review before any core build)

**Owner:** minespace-explorer (Task #17). **Status:** DESIGN/BUILD SPEC — review before touching the CB core.
**Premise (from #4 diff + system map + youknow recohere, all merged):** current `mineSpace` is three fragmented objects; the canonical defining move is MISSING (an infinite ambient coordinate space where ANY address flash-decodes to a foundation-ontology `is_a`/`has_part`/`produces` web); and `freeze → sub-mineSpace → recurse` (the Y1–6 tower) is NOT wired into the mine flow.
**Method:** every claim grounded in code, cited `file:line` (paths relative to `base/crystal-ball-alpha/lib/crystal-ball/`). Each piece tagged **[EXISTS]** / **[NEEDS-BUILDING]** / **[DECISION-FOR-ISAAC]**. This is **wiring + one decode function**, not a rewrite — the cycling mechanics stay intact.

---

## 0. Index

- §1 — What exists today (the substrate the build sits on), grounded.
- §2 — **Part 1: Canonical mineSpace** = make `mine` an addressable ambient space; the one new decode function.
- §3 — **Part 2: FLOW** = `freeze → sub-mineSpace → recurse`, wiring Y4/Y5/Y6 onto `bloom`/`producedSpace`/`freeze`.
- §4 — **Part 3: Unified-EWS wiring** = where `computeEWS` plugs into the engine/FLOW beyond all_math.
- §5 — The cycling mechanics to keep INTACT.
- §6 — EXISTS / NEEDS-BUILDING / DECISION-FOR-ISAAC table (the build checklist).
- §7 — The key DESIGN-DECISIONS-FOR-ISAAC (the forks to settle before building).

---

## 1. What exists today (the substrate) — grounded

**The encoding alphabet [EXISTS].** Digit grammar `0=superposition, 1-7=select, 8=drill, 88=close-drill, 9=wrap(+7)` (`index.ts:656-811`); delimiters `DOT=8988, KERNEL_OPEN=90, KERNEL_CLOSE=900` (`index.ts:819-823`); `encodeDot`/`decodeDot`/`coordToReal` (`index.ts:826-840`); `realToPlane`/`planeToReal` = a genuine ℝ↔ℝ² bijection (`mine.ts:381-416`). So an address *can* be parsed/placed; what's missing is decode-to-web (§2).

**The kernel ID = EWS backward chain, Y-strata-coupled [EXISTS].** `computeSpaceSlotSignature(...).canonical` IS the kernel ID (`kernel-v2.ts:431,478,485`; doc-comment 425-426). It is built from `subtreeFingerprint`, which tags each node with `s:${node.stratum}` (`kernel-v2.ts:323`) — so the youknow Y-strata is coupled INTO the kernel identity (`kernel-v2.ts:312-316`).

**The Y-strata generators (canonical) [EXISTS as data, NOT as a driver].** `STRATUM_TO_Y` (`index.ts:2288-2295`): foundation→Y1, domain→Y2, instance→Y3, instance_subtype_generator→Y4, domain_generator→Y5, instance_generator→Y6. `Y_LAYER_SEMANTICS` (`index.ts:2328-2382`) states the **REQUIRED FLOW: 2→3→4, then 4→5→6, then re-enter any (free cycling)** and "CB does NOT generate; the LLM IS the generator; CB only ORGANIZES the levels and REQUIRES the flow." **But these are consumed only as prompt text** by `buildUARL`/`describeYLayer` (`index.ts:2388-2392,2426-2428`) and `computeMineView` (`mine-view.ts:113-117`). **No code drives the 2→3→4 / 4→5→6 recursion.**

**Decode-to-web [EXISTS but node-bound].** `buildUARL(space, nodeId)` emits `subject is_a parent, has_part children…, produces producedSpace…, class_instance…` (`index.ts:2393-2456`); `buildSpaceUARL(space)` does the whole space (`index.ts:2462-2470`), surfaced via a `uarl` command (`engine.ts:1091,1202`). **It reads an EXISTING node** (`index.ts:2394`) — it cannot decode an un-built coordinate.

**The three "mineSpace" objects [EXISTS, fragmented]** (from #4): `computeMinePlane` = finite enumeration of built nodes for a heatmap, cap 2000 (`mine.ts:63-142`); `mine()`/`MineSpace`/`projectKernel` = the (x,y)-address plane keyed to a deliverable (`mine.ts:454-611`); `mineConfigurations` = flat 2-level cartesian tuple, the user-facing `mine` command (`mine.ts:718-794`, `engine.ts:684-717`).

**The generator + the Griess loop [EXISTS].** `scry()` = the perturbation daemon: find 0-superpositions → `runBatchSwarm` (LLM) collapses → Sha/catastrophe check → revert-or-keep → crown (`scry.ts:131-309`; surfaced `engine.ts:1075`). `compile()` = DERIVE(declareKappa)→BUILD(scry)→VERIFY(`verifyKappa` + `kappaToUARL`→`callYouknow`)→corrections→ONT/SOUP/crowned (`compile.ts:196-309`; surfaced `engine.ts:1033`).

**The bloom/freeze machinery [EXISTS].** `bloom(registry, space, nodeId, childSpaceName?)` sets `node.producedSpace` and creates/links a child space (`index.ts:498-527`) — **this is the sub-mineSpace primitive.** `freezeNode`/`lockNode` (`index.ts:1655-1685`); `setSlotCount` (class/instance, `index.ts:1644-1648`); `getBornWeight` (`index.ts:1731`). FlowPhase = `idle|create|bloom|fill|lock|mine|compose` (`engine.ts:118`) — a BUILD-phase machine, NOT the Y-tower recursion.

**The unified EWS [EXISTS, wired only to all_math].** `computeEWS` = forward(structure)+backward(kernel-id symmetry)+boundary(interior/frontier from `mine()`)+production(domain chain via `ewsRef`) (`ews.ts:127-141`). The **production chain** (`ews.ts:387-482`) walks the EWS space's dots → ordered `DomainLink`s, each `typed` (has `kernelRef` → a sub-kernel space) or `untyped` (`0` = LLM fills), with `loops` (self-sustaining cycle) — **this IS the domain chain a FLOW would walk.** Called ONLY at `engine.ts:2818` (all_math); never in the mine/FLOW path.

---

## 2. PART 1 — Canonical mineSpace: an addressable ambient space

**Canonical (target):** lock a kernel → enter its mineSpace = a plain coordinate space, infinite + totally ordered; ANY point flash-decodes (via the alphabet) to a meaningful-or-not foundation-ontology instance (`is_a`/`has_part`/`produces` web, decodable to English); a point = z=x+iy ADDRESS of a semantic web, not a bare number.

**Current (gap):** `mine` materializes a finite list of already-built nodes (`mine.ts:530,541` push existing/adjacent; cap 2000 `mine.ts:67`). Decode-to-web only on built nodes (`index.ts:2394`). So "ANY address decodes" is absent.

**The smallest change — one new pure function [NEEDS-BUILDING]:**

> `decodeAddressToWeb(registry, kernelSpaceName, realOrXY) → UARLWeb | { meaningful:false }`

Pipeline, reusing what EXISTS:
1. `planeToReal(xDigits,yDigits)` or take the real directly → encoded digit string (`mine.ts:408-416` EXISTS).
2. `decodeDot(encoded)` → dotted coordinate (`index.ts:831` EXISTS).
3. **Parse the coordinate against the kernel grammar** to a *virtual* node-path (`parseCoordinate`, `index.ts:693-811` EXISTS) — selections `1-7`, drills `8`, wraps `9`, superpositions `0`.
4. **Synthesize the web from the coordinate + the kernel's slot structure**, NOT from a pre-existing node: walk the locked kernel's slot tree along the parsed selections; at each step emit `is_a` (slot's parent kind), `has_part` (the slot's children kinds), `produces` (if the slot blooms), `class_instance` (`0`=class vs `1-7`=instance) — i.e. the SAME predicate logic as `buildUARL` (`index.ts:2407-2447`) but driven by the *coordinate-walked virtual node*, not `space.nodes.get(nodeId)`. Where the coordinate addresses a slot that exists in the kernel → bind the real label; where it addresses an un-built region → emit a structurally-valid-but-unlabeled web (`meaningful` iff the walk stays inside the kernel's slot grammar; otherwise `{meaningful:false}` — the "meaningful-or-not" the canonical names).

**This is the load-bearing new piece.** It converts mine from "list of built nodes" to "address → decode" — the kernel becomes the *codec*, the coordinate space stays ambient/infinite, and enumeration (`computeMinePlane`) becomes a *windowed view* into it rather than the space itself.

**Smallest wiring change [NEEDS-BUILDING, small]:** the `mine` command (`engine.ts:684-717`) gains an addressable read: given a coordinate/real, return `decodeAddressToWeb(...)` instead of only the materialized `mineConfigurations` tuple list. Keep `computeMinePlane`/`mineConfigurations` as the *render window* (cap 2000 becomes a view bound, not the space's extent — `mine.ts:67`).

**[DECISION-FOR-ISAAC #1]:** the canonical says "a point = z=x+iy". Today x,y are two reals (`mine.ts:393-398`). Do we (a) keep (x,y) but attach the decoded web to the point (minimal), or (b) introduce a complex `z` type? (b) is a bigger surface. Recommend (a): the address is already the ℝ↔ℝ² bijection; "z=x+iy" is satisfied by treating the (x,y) pair AS the complex address — no new numeric type needed, just attach the web.

---

## 3. PART 2 — FLOW: freeze → sub-mineSpace → recurse (the Y-tower)

**Canonical (target):** freeze a chosen config → its sub-mineSpace = the instance-specific configs of THAT class → recurse (Instance-as-Class: 2→3→4, then 4→5→6, then free re-enter). The LLM is the generator; CB organizes + requires the flow.

**Current (gap):** the recursion machinery EXISTS in pieces but is NOT driven as a loop. `bloom` opens a `producedSpace` (`index.ts:498-527`); `scry` fills 0-superpositions in ONE space (`scry.ts:131`); `freezeNode` commits a node (`index.ts:1673`); the Y-strata semantics are prompt-text only (`index.ts:2328-2382`). Nothing chains freeze → open-next-order-space → re-enter.

**The wiring — a FLOW driver over EXISTING primitives [NEEDS-BUILDING]:**

> `flowStep(registry, space, nodeId) → { nextSpace, nextStratum }`

Per step, composing primitives that EXIST:
1. The LLM (via `scry`, `scry.ts:131`) fills the current level's 0-superpositions → a chosen config.
2. **Freeze the chosen config** (`freezeNode`, `index.ts:1673` EXISTS).
3. **Open its sub-mineSpace** = `bloom(registry, space, chosenNodeId)` → sets `producedSpace`, the next-order space (`index.ts:498-527` EXISTS). This is the Instance-as-Class move: the frozen instance node becomes the class-root of the produced space.
4. **Advance the stratum** along the canonical ladder: set the produced space's root `stratum` to the next Y-level per the REQUIRED FLOW `2→3→4, 4→5→6, re-enter` (`index.ts:2324`). The stratum is **level-typed** (`index.ts:2310-2311`): Y4 consumes a Y3 instance, Y5 consumes any Y4-output, Y6 consumes any Y5-output → then feeds a fresh Y4. Because `subtreeFingerprint` already tags `s:${stratum}` (`kernel-v2.ts:323`), advancing the stratum automatically re-keys the sub-mineSpace's kernel ID.
5. **Re-enter** at the produced space → recurse `flowStep`.

So FLOW = `scry`(fill) → `freezeNode`(commit) → `bloom`(open sub-space) → set next `stratum` → recurse. **The four verbs all EXIST; the driver that sequences them per the Y-ladder is the new piece**, and it is a sequencer, not new math.

**[DECISION-FOR-ISAAC #2]:** Y4/Y5/Y6 are "level-typed, source-irrelevant, freely composable" (`index.ts:2310-2311,2370-2379`). The strict ladder is `2→3→4 / 4→5→6 / re-enter any`. Does FLOW (a) enforce the strict ladder as the default with free re-entry only on explicit request, or (b) let the generator pick any level-valid next operator each step (fully free)? This determines whether `flowStep` hard-codes the `2→3→4→5→6` order or reads an allowed-next-set from the current stratum. Recommend (a) default ladder + (b) as an override — matches "REQUIRED FLOW" + "free cycling."

**[DECISION-FOR-ISAAC #3]:** the existing `FlowPhase` machine (`engine.ts:118`: idle/create/bloom/fill/lock/mine/compose) is the BUILD-phase axis. The Y-tower is the ONTOLOGICAL-LEVEL axis. Are these two axes (build-phase × Y-level) kept orthogonal (a build runs at one Y-level; FLOW moves Y-levels), or merged? Recommend orthogonal: don't overload `FlowPhase`; add a `stratum` cursor alongside it.

---

## 4. PART 3 — Unified-EWS wiring (the production chain IS the domain chain FLOW walks)

**Current:** `computeEWS` is invoked ONLY in all_math (`engine.ts:2818`); its `production` field (the domain chain) is computed but never drives anything (`ews.ts:137,387-482`).

**The wiring [NEEDS-BUILDING]:** plug `computeEWS(...).production` into the FLOW driver of §3 as the **chain the recursion walks**:
- A kernel's `ewsRef` space holds the production chain (`ews.ts:475-481`); each `DomainLink` is `typed` (has a sub-kernel) or `untyped` (`0`, LLM fills) (`ews.ts:433-451`).
- FLOW's "open the next-order space" (§3 step 3) should consult `production.domains`: the next domain in the chain is the next FLOW target; a `typed` link → re-enter its existing sub-kernel; an `untyped` link → `bloom` + `scry` to fill it. `loops:true` (`ews.ts:456`) = the self-sustaining cycle = the free re-enter (§3 step 5).
- `computeEWS(...).boundary` (interior/frontier/`canExpand`, `ews.ts:225-291`) gives FLOW its **stop/continue signal per level**: `canExpand` nodes are the open frontier to fill; a level with no expandable nodes + kernel-complete is where that level's mineSpace closes and FLOW descends.

So: **EWS.production = the domain chain FLOW walks; EWS.boundary = the per-level stop/continue gate; EWS.backward.canonical = the kernel ID that re-keys on each descent.** The wiring is: call `computeEWS` inside `flowStep` (not only all_math) and route on `production` + `boundary`.

**[DECISION-FOR-ISAAC #4]:** `computeEWS.boundary` currently derives interior/frontier from `mine()` (the materialized enumeration, `ews.ts:229-237`). Once §2 makes mine addressable, should `boundary` switch to the ambient decode (interior = decodable-and-built, frontier = decodable-not-yet-built), or keep the materialized definition? Recommend switching after §2 lands, so EWS boundary reflects the ambient space, not the enumeration.

---

## 5. Keep these MECHANICS intact (this is wiring, not a rewrite)

- The encoding alphabet + bijections (`index.ts:656-840`, `mine.ts:381-416`) — UNCHANGED; §2 consumes them.
- `scry` collapse loop + Born/Sha/revert/crown (`scry.ts:131-309`) — UNCHANGED; FLOW calls it per level.
- `compile` Griess loop + `verifyKappa` + youknow corrections (`compile.ts:196-309`) — UNCHANGED.
- `bloom`/`freezeNode`/`lockNode`/`setSlotCount` (`index.ts:498-527,1644-1685`) — UNCHANGED; FLOW sequences them.
- `computeSpaceSlotSignature`/`subtreeFingerprint` kernel-ID + `s:${stratum}` coupling (`kernel-v2.ts:317-485`) — UNCHANGED; it re-keys automatically as FLOW advances stratum.
- `buildUARL`/`buildSpaceUARL` predicate logic (`index.ts:2393-2470`) — REUSED by the new `decodeAddressToWeb` (§2), not replaced.

---

## 6. Build checklist — EXISTS / NEEDS-BUILDING / DECISION

| Piece | Status | Cite / Note |
|---|---|---|
| Encoding alphabet + `encodeDot`/`decodeDot`/`coordToReal` | EXISTS | `index.ts:656-840` |
| ℝ↔ℝ² bijection `realToPlane`/`planeToReal` | EXISTS | `mine.ts:381-416` |
| `parseCoordinate` (coordinate → tokens) | EXISTS | `index.ts:693-811` |
| `buildUARL`/`buildSpaceUARL` (node→is_a/has_part/produces) | EXISTS (node-bound) | `index.ts:2393-2470` |
| **`decodeAddressToWeb` (arbitrary coordinate → web)** | **NEEDS-BUILDING** | §2; reuses the four rows above |
| mine made addressable (enumeration → render window) | NEEDS-BUILDING (small) | `engine.ts:684-717`, `mine.ts:67` |
| `bloom` (open producedSpace = sub-mineSpace) | EXISTS | `index.ts:498-527` |
| `freezeNode`/`lockNode`/`setSlotCount` | EXISTS | `index.ts:1644-1685` |
| `scry` (LLM generator fills 0-superpositions) | EXISTS | `scry.ts:131-309` |
| Y-strata tables + REQUIRED FLOW (data) | EXISTS | `index.ts:2288-2382` |
| stratum coupled into kernel ID (`s:${stratum}`) | EXISTS | `kernel-v2.ts:323` |
| **`flowStep` driver (scry→freeze→bloom→advance-stratum→recurse)** | **NEEDS-BUILDING** | §3; sequences existing verbs |
| `computeEWS` (forward/backward/boundary/production) | EXISTS | `ews.ts:127-141` |
| EWS production chain (typed/untyped/loops) | EXISTS | `ews.ts:387-482` |
| **EWS wired into FLOW (not only all_math)** | **NEEDS-BUILDING** | §4; call in `flowStep` |
| convergence measurable: `buildSpaceUARL` → external reasoner pass-rate | NEEDS-BUILDING | compile uses `kappaToUARL` property-claims (`compile.ts:53-85`), NOT per-node web; the re-aim's measurable needs `buildSpaceUARL`→`callYouknow` pass-rate vs resolved-arity |
| z=x+iy point type vs (x,y)+web | DECISION #1 | §2 |
| strict Y-ladder vs free level-valid next | DECISION #2 | §3 |
| build-phase axis vs Y-level axis (orthogonal?) | DECISION #3 | §3 |
| EWS boundary: ambient vs materialized | DECISION #4 | §4 |

---

## 7. DESIGN-DECISIONS-FOR-ISAAC (settle before building)

1. **z=x+iy point.** Attach the decoded web to the existing (x,y) address (minimal, recommended) vs introduce a complex `z` numeric type (bigger surface). §2.
2. **Y-ladder enforcement.** Default strict `2→3→4 / 4→5→6 / re-enter` with explicit free-cycle override (recommended), vs fully free level-valid next each step. Determines `flowStep`'s next-operator logic. §3.
3. **Two axes.** Keep build-phase (`FlowPhase`) and Y-level (`stratum`) orthogonal — a build runs at one Y-level, FLOW moves levels (recommended) — vs merge them into one machine. §3.
4. **EWS boundary source.** After mine becomes addressable, switch `computeEWS.boundary` interior/frontier to the ambient decode (recommended) vs keep the materialized `mine()` enumeration. §4.
5. **The convergence measurable (the re-aim's load-bearing claim).** The proof's measurable is "external mereology pass-rate of the decoded `buildSpaceUARL` web vs resolved arity." Today `compile` validates `kappaToUARL` property-claims, not the per-node web (`compile.ts:53-85,264-265`). Building the measurable = wire `buildSpaceUARL` → `callYouknow` (or the external reasoner) and record pass-rate per FLOW step. **DECISION: is the convergence measurable in-scope for THIS build, or a separate follow-on?** (It is what makes FLOW falsifiable; recommend at least stubbing the measurement hook in `flowStep`.)

**Honesty:** §2–§4 designs are VISION/NEEDS-BUILDING (not built); every EXISTS row is cited and was read this session. The convergence claim itself stays VISION/claim-to-prove per the proof — this spec builds the apparatus that would let it be measured, it does not assert it.
