# MineSpace Correction Surface — readiness note + correction targets

**Prepared by:** minespace-explorer (prep task). **For:** Isaac + team-lead to start from. **Scope:** minespace's ACTUAL current-vs-canonical gaps (decode + boundary). **NOT in scope:** FLOW (freeze→recurse / generation) — the #17 build-spec was rejected wrong-premise; this surface excludes it.
**Grounding:** code read this session (file:line, paths rel. `base/crystal-ball-alpha/lib/crystal-ball/`); canonical = Isaac's own MineSpace_Epistemics findings (2026-06-05T01:10:13 + 09:46:42) + the verified #4 current-vs-canonical map.

---

## PART 1 — CA-TS readiness: is CB current+complete on CA-TS?

**Straight answer: YES, current+complete — but "on CA-TS" means the live CLI, NOT a persisted Neo4j graph.**

- The CA-TS backend (`/home/GOD/context_alignment_utils/neo4j_codebase_mcp/ts_backend/`, branch `ca-typescript-backend`, committed today 2026-06-06 11:29) is a **standalone CLI (ts-morph) that EMITS a JSON node/edge bundle — it does NOT write to Neo4j** (README "Known gaps": "No direct Neo4j write… MCP server.py not extended (standalone CLI)").
- **Consequence:** there is **no stored CA-TS graph that can be stale.** ts-morph builds a fresh `Project` from the live repo on every invocation, so a `deps`/`parse-repo` run always reflects CB's **current** source. The "#11-era parse" was a live CLI readout, not a persisted graph — nothing went stale.
- **Verified empirically just now (current CB source):**
  - `node ca_ts.mjs parse-repo "$CB/lib/crystal-ball" --name crystal-ball` → **53 files, no crash**, real module/class/attribute extraction.
  - `node ca_ts.mjs deps computeMinePlane --root "$CB" --pretty` → correctly localizes **mine.ts:63-142** + `computeSpaceHeat` (index.ts:578-589) + `isKernelComplete` (index.ts:642-660), live from current source.
- **What "closes" full graph-residency (only if you want a queryable persisted graph):** the known gap is "no direct Neo4j write." To put CB in a *persisted* CA graph you'd either (a) load the emitted `parse-repo` JSON bundle into Neo4j, or (b) extend `server.py` — **neither is built.** For the working use Isaac+team need (per-target dep readout / callgraph grounding), **run the CLI live per-target — it is current by construction.** No refresh step exists or is needed; just invoke it.

**Bottom line:** CB-on-CA-TS = **current + complete, on demand via the CLI** (verified). Not stale. If a *persisted* Neo4j graph is the requirement, that's a separate unbuilt piece (no-direct-Neo4j-write gap), not a refresh.

---

## PART 2 — The correction targets (prioritized)

### ⚠️ Premise reframe (read first — this is why #17 was wrong-premise)

Isaac's canonical (MineSpace_Epistemics 2026-06-05) **says enumeration is the CHEAP, CORRECT part**, not the bug: *"the real line already contains every configuration (they are just reals); CB DECODES the pre-existing real line through the encoding structure; enumeration = reading off what already exists, not constructing it = discover-not-invent made literal."* So the minespace correction is **NOT** "make it an infinite generative ambient space with LLM sibling-gen + freeze-recurse" (that was the #17 premise — generation/FLOW). The correction is: **CB should DECODE per-coordinate and LOCALIZE the exact dot where decode→implication** — *"the feature is not the field, it is KNOWING PRECISELY WHERE DECODE ENDS AND IMPLICATION BEGINS."* The targets below are scoped to that decode/boundary surface.

### Target list (each: gap → code (file:line) → what canonical wants → IS/VISION/OPEN)

**T1 — Decode an ARBITRARY coordinate to a foundation-ontology web (the core missing move). [VISION / NEEDS-BUILDING]**
- Now: `buildUARL(space, nodeId)` emits `is_a`/`has_part`/`produces`/`class_instance` but **reads an already-built node** (`index.ts:2393-2456`, the `space.nodes.get(nodeId)` at :2394); it lives on the `view` path, **decoupled from the MineSpace plane**. No function decodes a coordinate that wasn't built.
- Canonical: ANY coordinate flash-decodes (via the per-digit grammar) to a meaningful-or-not `is_a`/`has_part`/`produces` web (Epistemics 01:10 + 09:46).
- IS: the predicate logic (`index.ts:2407-2447`) + `parseCoordinate` (`index.ts:693-811`) + `decodeDot`/`coordToReal` (`index.ts:826-840`) all exist and are reusable.
- VISION: the `decode-arbitrary-coordinate → web` function itself (walk the kernel slot-tree along the parsed coordinate, emit the web from the *virtual* coordinate-walked node, not a stored node).

**T2 — Localize the boundary DOT-BY-DOT (decode→implication phase change). [VISION / NEEDS-BUILDING — the load-bearing feature]**
- Now: boundary is computed at the **node/config level**, not per-dot. `ews.computeBoundary` gives interior/frontier/`canExpand` (`ews.ts:225-291`); `mine.PointStatus` is `'valid'|'adjacent'|'invalid'` (`mine.ts:468`). Nothing walks a coordinate dot-by-dot to flag the **first unassigned/non-resolving dot**.
- Canonical (09:46, the sharp version): the boundary is hit DOT-BY-DOT; the instant you reach an **unassigned dot** (a segment that doesn't resolve in this domain ontology = SOMA SOUP/undefined ref), **direct decoding dies and degrades to implication-only**; CB's special feature is telling you **EXACTLY WHICH DOT** — the precise coordinate position where decode flips to implication.
- IS: the per-digit enrichment that makes this detectable (`0`=class, `1-7`=instance, `8`=drill) exists in the grammar (`index.ts:656-811`).
- VISION: the function that returns `{ decodesThrough: <coord prefix>, diesAtDot: <position>, reason: 'unassigned/SOUP' }`.

**T3 — Compute the BEYOND / "melt" zone (it is DECLARED but never COMPUTED). [IS-gap → VISION]**
- Now: `PointStatus` includes `'invalid'` (`mine.ts:468`) but **nothing ever produces it** — `projectKernel` only pushes `'valid'` (`mine.ts:550`) and `'adjacent'` (`mine.ts:585`); `mineConfigurations` only pushes `'valid'` (`mine.ts:753`) and `'adjacent'` (`mine.ts:780`); `ews.computeBoundary` only reads valid/adjacent (`ews.ts:231-237`). So the third zone is a dead enum value.
- Canonical (01:10): three zones — INTERIOR (valid, decodes here), FRONTIER (adjacent, known-unknowns), **BEYOND (invalid: different dot-structure, encrypted, the numbers STOP MEANING ANYTHING here = it MELTS INTO ANOTHER DOMAIN)** — with the melt-boundary located exactly + the reason given.
- IS: the zone names + the morphism into the next domain (`drill`/`producedSpace`, `index.ts:498-527`) exist.
- VISION: actually computing/emitting `'invalid'`/BEYOND points (a coordinate that parses but doesn't resolve in THIS kernel ontology) so the melt-boundary is real, not a declared-only enum.

**T4 — A point must be the ADDRESS of a web, not a bare label. [IS partial → VISION small]**
- Now: `realToPlane`/`planeToReal` (`mine.ts:381-416`) is the genuine ℝ↔ℝ² address bijection — **the one canonical piece already realized** — but a `KnownPoint` carries only a single node `label` (`mine.ts:470-480, 545-551`), not the decoded web.
- Canonical: a point = z=x+iy ADDRESS of a semantic web.
- VISION (small): attach T1's decoded web to the point (recommend keeping the (x,y) address as-is and hanging the web off it; no new complex `z` type needed).

**T5 — The decode→implication handoff to SOMA d-chains (past the boundary). [OPEN / DESIGN-FOR-ISAAC]**
- Now: **no wiring** from the decode-boundary to any implication engine.
- Canonical (09:46): past the unassigned dot, knowledge degrades to **implication-only via D-CHAINS** (forced implication cascades = SOMA deduction); *"the unassigned dot = SOMA SOUP/undefined-reference; the implication structures past it = SOMA deduction chains; CB localizes the boundary, SOMA does the implication past it = same boundary, two engines."*
- OPEN: this is a **cross-engine (CB↔SOMA) design** — the decode-boundary localizer (T2) is the CB half; the implication past it is SOMA's. Flag for Isaac: is the implication handoff in-scope for the minespace correction, or a follow-on once T1–T3 land? (T2 is the precondition either way.)

### Explicitly OUT OF SCOPE (FLOW — do not change, per team-lead)
- freeze→sub-mineSpace→recurse / the Y1–Y6 Instance-as-Class tower; LLM-swarm generation of sibling configs. (These were #4-C5 + the rejected #17 spec.) The `drill`/`producedSpace` morphism (`index.ts:498-527`) is the *crossing* into the next domain — minespace's job (T3) is to **detect the melt-boundary**; the crossing/recursion itself is FLOW and untouched here.

### Priority order
1. **T2** (dot-by-dot boundary localizer) — the load-bearing canonical feature ("knowing where decode ends").
2. **T1** (decode-arbitrary-coordinate → web) — the precondition for T2/T3/T4; reuses buildUARL+parseCoordinate.
3. **T3** (compute the BEYOND/melt zone) — make the declared-only `'invalid'` real.
4. **T4** (attach web to the address) — small, completes "point = address of a web."
5. **T5** (SOMA implication handoff) — OPEN, cross-engine, likely follow-on.

---

## Honesty markers
- **IS (verified this session):** Part 1 (CA-TS is live-CLI, no-Neo4j-write, parses current CB — empirically run); every "Now:" line in T1–T5 (cited, read). The `'invalid'`-never-produced finding (T3) confirmed in mine.ts.
- **VISION / NEEDS-BUILDING:** the decode-arbitrary fn (T1), the dot-localizer (T2), computing BEYOND (T3), attaching the web (T4).
- **OPEN / DESIGN-FOR-ISAAC:** the CB→SOMA implication handoff (T5); whether a persisted CA-TS Neo4j graph is wanted (Part 1 known gap).
- **Premise correction surfaced:** enumeration is canonical-correct (decode, not generate); the minespace fix is decode + boundary-localization, NOT generative/FLOW — this is the corrected premise Isaac+lead should start from.
