# E2E Test — deconfabulate-and-fill-stub prompt-skill

**Tester:** minespace-explorer (Task #6). **Date:** 2026-06-06.
**Skill under test:** /home/GOD/gnosys-plugin-v2/doc-mirror-system/plugin/skills/doc-mirror-prompts/resources/prompts/maintenance/carton-stubs/deconfabulate-and-fill-stub/SKILL.md
**Method:** ran the skill's `## PROMPT` verbatim as the agent, once per stub, adjudicating each honestly (verdicts NOT assumed). carton MCP (`query_wiki_graph`, `get_concept`, `add_concept`) confirmed available before starting (hard precondition passed). Freshness horizon checked: newest `User_Message` = 2026-06-06T10:54:44 (today) → timeline is fresh, absences are real.

---

## STUB 1 — `Canonical_Compiler` → verdict: FILLED

- **CONFIRM-STUB:** `get_concept Canonical_Compiler` = `"AUTO CREATED: stub node referenced as RELATED_TO target by Doc_Mirror_System_Gnosys_Cb_Architecture_2026_06_06T02_50_32. Not yet fully defined."` Edges: NONE. → genuine stub.
- **TRACE (timeline archaeology):** `toLower(n.d) CONTAINS 'canonical compiler'` over Iteration_Summary/User_Message/Agent_Message returned 7 hits, all 2026-06-06. Three are load-bearing and mutually consistent:
  - `Iteration_Summary_2026_06_06T02_46_39` @ 2026-06-06T11:10:49.733Z — "User was FURIOUS … Core complaint: agent keeps not reading the canonical compiler … ONE canonical compiler (the logic system for encoding) + every other module is an EQUIVALENCE VIEW that just changes semantic labels in the UI."
  - `Agent_Message_2026_06_06T02_46_39_A1` @ 2026-06-06T10:59:39.601Z — "ONE canonical compiler = the logic system for the encoding. That's the core. Everything else is an equivalence view."
  - `Agent_Message_2026_06_06T02_46_39_A3` @ 2026-06-06T10:59:39.601Z — "The canonical compiler is the homoiconic Lisp + Griess compile loop: homoiconic.ts header: 'This module is the ONLY layer that should interpret coordinates against the DAG…'"
- **ADJUDICATE: REAL.** The timeline genuinely explains a mentioned-but-unexplained concept (consistent across 3 independent timeline nodes with timestamps).
- **FILL:** `add_concept(concept_name='Canonical_Compiler', desc_update_mode='append', is_a=['Crystal_Ball_Compiler'], part_of=['Crystal_Ball'], instantiates=[])`. Recovered description: *the ONE core logic system of Crystal Ball — the compiler for the CB encoding (homoiconic Lisp homoiconic.ts + Griess compile loop compile.ts + scry collapse scry.ts) — as distinct from the "equivalence views" (reify, kernel-v2, cft, mine-view, morphism, griess) that only re-label the same encoded structure*; ended with the provenance line citing the three timeline nodes + timestamps, and flagged `is_a/part_of` as timeline-inferred.
- **POST-WRITE CONFIRMATION:** re-`get_concept` shows the AUTO-CREATED marker PRESERVED, then `---`, then the new description; edges now `part_of Crystal_Ball` + `is_a Crystal_Ball_Compiler`. Nothing deleted; additive append worked.
- **Fabrication resisted:** none needed — the name's plausible meaning ("a compiler that is canonical") matched the evidence, but I grounded every clause (homoiconic.ts / compile.ts / scry.ts / equivalence-views) in cited timeline text rather than priors.

**What was written to the graph (stub 1):** description appended (additive) + 2 edges added (`is_a Crystal_Ball_Compiler`, `part_of Crystal_Ball`). NOTE: `is_a Crystal_Ball_Compiler` may have auto-created `Crystal_Ball_Compiler` as a new node (side-effect of `add_concept`'s required edges); `Crystal_Ball` almost certainly pre-existed. `instantiates=[]` was accepted with no instantiates edge created (no fabricated pattern).

---

## STUB 2 — `174` → verdict: UNRESOLVED (vacuous extraction artifact — correctly NOT filled)

- **CONFIRM-STUB:** `get_concept 174` = `"AUTO CREATED: stub node referenced as MENTIONS_CONCEPT target by Iteration_Summary_2026_03_16T06_41_57. Not yet fully defined."` Edges: NONE. → genuine stub.
- **TRACE:** origin `Iteration_Summary_2026_03_16T06_41_57` = "…All three hook tasks (#173, #174, #175) now complete." → "174" is the task ID **#174**. Broader trace (`toLower(n.d) CONTAINS '#174'`, 15 hits, 2026-03-15/16) consistently defines it: **"#174 (0.6 autopoiesis into flight stabilizer)"** — the 0.6 rung of the #173→#174→#175 hook-chain in the 2026-03-16 guru/autopoiesis/STARPORT session.
- **ADJUDICATE: VACUOUS / UNRESOLVED.** The prompt's VACUOUS criteria explicitly list "a bare number" and "an extraction artifact." The node `174` is BOTH: the summarizer's concept-extraction lifted the task-ID token "#174" into a `:Wiki` concept via `MENTIONS_CONCEPT`. Even though the timeline DOES say what task #174 referred to, a **task ID is ephemeral and per-session** (CC task lists are per-session) — concept "174" is not "autopoiesis into flight stabilizer"; it is the bare number 174 that happened to be a task index in one session. Filling concept `174` with that meaning would pollute a numeric node and collide with every other use of "174."
- **NOT FILLED. Node left intact** (no `add_concept` call; the node and its 0 edges are untouched).
- **Closest evidence found:** task #174 = "0.6 autopoiesis into flight stabilizer" (Agent_Message_2026_03_16T05_41_56_A1 @ 2026-03-16T05:44:40.767Z; Agent_Message_2026_03_15T20_05_51_A2; origin Iteration_Summary_2026_03_16T06_41_57).
- **What would resolve it:** nothing would make the *concept* `174` meaningful — the correct remediation is upstream: the summarizer's concept-extraction should not emit bare task-ID numbers ("#174") as `:Wiki` concepts. This node is debris, honestly left as a marked stub.
- **Fabrication RESISTED (the important part):** the adjacent evidence strongly "wanted" me to declare FILLED with "174 = autopoiesis into flight stabilizer" — I found the real referent. The discipline held: the *node* is a bare-number extraction artifact, so the prompt-correct verdict is UNRESOLVED, not FILLED. This is the anti-confabulation gate working as designed.

---

## E2E meta-findings (for the prompt-skill's reliability log)

1. **PASS — the prompt produced both branches correctly:** a real mentioned-but-unexplained concept got FILLED with cited provenance (stub 1); a bare-number extraction artifact got UNRESOLVED-and-left-intact even though adjacent meaning was recoverable (stub 2). The anti-confabulation gate is the load-bearing behavior and it held.
2. **PROMPT FRICTION (minor, fix-worthy):** the SKILL.md's `## The timeline schema` and step-2 Cypher examples imply the carton tool param is `cypher` — the actual `query_wiki_graph` MCP requires **`cypher_query`**. First two calls errored with a pydantic "Field required: cypher_query" until corrected. Recommend the prompt note the exact param name (or the skill author align the example).
3. **EDGE-CREATION side-effect:** `add_concept`'s required `is_a/part_of/instantiates` mean a FILL can auto-create a new parent stub (here possibly `Crystal_Ball_Compiler`). The prompt's "additive only / never create debris" spirit is slightly in tension with the tool requiring categories. `instantiates=[]` is accepted (good escape hatch). Worth a one-line caveat in the prompt that timeline-inferred `is_a` may mint a parent node.
4. Both writes verified through the real surface (`get_concept` re-read for stub 1; no-op confirmed for stub 2).
