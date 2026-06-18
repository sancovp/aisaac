# PsychoBlood Reconciliation — ONE family, but THREE incompatible state cores + N lifecycle stages

**Investigator:** reconciler (team psychoblood-depth) · 2026-06-04
**Method:** read the actual .py for reps 1–2, the actual .md for rep 3, CartON `get_concept`/graph for rep 4. Did NOT trust markdown claims; verified each state vocabulary against source lines.

**Verdict in one line:** These are **NOT one running system**, and **NOT four clean attempts at the same thing either.** They are **one conceptual FAMILY ("psychoblood")** expressed across **two different code lineages** (sancrev monorepo vs halo-sanctuary/CIG `/tmp` bundle) that are built on **three genuinely incompatible state representations** (9-state IntEnum · 35-dim OCEAN vector · 6-dim provenance manifold), plus **two free-floating label taxonomies** (10 loops · 16 base emotions) that are operationalized *differently in every place they appear*. No conversion function exists between any pair of state cores. Only ONE rep is live code in the canonical repo (sancrev), and it implements only a fraction of the canon.

---

## The state-representation map (the core deliverable)

| # | Representation | Source (verified) | STATE model | FLOW/LOOP set | ML substrate | Reward | In canonical repo? |
|---|---|---|---|---|---|---|---|
| 1 | **sancrev event package** | `application/sanctuary-revolution/sanctuary_revolution/harness/events/psychoblood/{psychoblood,observer_psychics,berserking}.py` (Jan 16) | **9-state `IntEnum`** GROUND..DECAY (`psychoblood.py:20-29`) + a separate **4-level ObserverLevel** UNCONSCIOUS→LUCID (`observer_psychics.py:12-16`) + a separate **4-dim Wangtang** fear/arousal/compassion/logic_lattice (`berserking.py:26-31`) | **none** — no loop concept at all | **none** — `random.random()` probabilistic tick (`psychoblood.py:83-97`) | none | **YES** (only rep that is) |
| 2 | **GP/LSTM bundle** | `/tmp/psychoblood-bundle/{gp_surrogate,emotion_ml,policy}.py` | **35-dim OCEAN** float vector (5 traits × 7 facets; rubric `emotion_ml.py:530-549`) | **10 flows** as a bare string list `NONE,SATAN,MARTYR,ADDICTION,OUTRAGE,DEVOTION,HEROISM,COMPASSION,VALUE,BERSERKING` (`policy.py:142-145`) — an **untrained `flow_head`**, no detector | **GP** (sklearn, 35 indep GPs over PCA-20, Matern, `gp_surrogate.py`) → **LSTM** swap at 500 obs (`policy.py:23-127`, not active) | **EXTERNAL** journal sanctuary/wasteland → obs weights (`emotion_ml.py:397-407`) | **NO** (`/tmp`, halo-sanctuary extraction) |
| 3 | **Metahologram design** | `/tmp/psychoblood-bundle/gp-psychoblood-metahologram.md` (DESIGN, un-built) | **6-dim meta-PE PROVENANCE** MIRROR/CONTEXT_MERGE/COMPLETION/ATTRACTOR/TAIL_ECHO/NOVELTY (§2) — **OCEAN is dropped entirely**; 9 states + 16 emotions + 10 loops demoted to a "typing layer" OVER the manifold (§7) | **10 loops** redefined as **provenance autocorrelation standing-waves** (§8) | **multi-output composite-kernel GP** (gpytorch, `K_emotion × K_provenance`, §4) — different lib/kernel/IO than rep 2 | **INTRINSIC** — "reward baked into features," provenance polarity, *"no reward function needed"* (§3) — directly contradicts rep 2 | **NO** (`/tmp` design doc) |
| 4 | **CartON canonical** | `mcp__carton__get_concept`: `Psychoblood_Nine_States`, `Psychoblood_Ontology`, `Psychoblood_State_Transitions` | **9 states** Ground..Decay, each = Blood+Psyche+Wants; probabilistic transition gates | (loops/16-emotions live in the **book outline**, rep 4b) | none (conceptual) | none | conceptual canon |
| 4b | **Book outline** | `designs/PSYCHOBLOOD_BOOK_OUTLINE.md` (markdown = the artifact here) | uses the **16 BasicEmotions** (excited/embarrassed/fearful/sad/proud/loving…) | **loops as EMOTION SEQUENCES** (ch.5: SATAN=excited→embarrassed→fearful→sad, etc.) — shows only **6** of the 10 | none | PBB "golden state" is the target | conceptual canon |

**Missing source:** rep 3's entire migration premise rests on `speaking-agent-demo/src/types/psychoblood.ts`, `…/lib/psychoblood.ts`, `…/psychoblood-loops.ts` (BasicEmotion / EmotionPattern / LoopPattern / PsychobloodLoop). **`find /home/GOD /tmp` returns NOTHING** for these — the TS layer the metahologram ports from is not present on this box. Its "typing layer" source is unverifiable here.

---

## Are they ONE system expressed 4 ways, or 4 incompatible designs?

**Neither cleanly — they are ONE CONCEPT, TWO LINEAGES, THREE STATE CORES.**

- **Conceptually** the canon (rep 4 + 4b) is coherent and layered: **9 STATES = vertical altitude/trajectory** (where you are), **10 LOOPS = behavioral attractor patterns** (what's running you), **16 EMOTIONS = primaries** the states/loops are built from. States and loops are *orthogonal layers*, not rivals. So at the idea level it is one family.
- **At the code/runtime level they do NOT compose.** Lineage A (sancrev, monorepo) implements ONLY the 9-state enum + two bespoke side-modules (observer, wangtang) — no loops, no OCEAN, no provenance, no ML. Lineage B (`/tmp` halo-sanctuary/CIG bundle) implements ONLY 35-OCEAN regression + an untrained 10-flow head, and its design successor (metahologram) throws OCEAN away for a 6-dim provenance manifold. The two lineages share **only the word "psychoblood" and the loop NAMES** — no shared types, no shared files, no shared runtime, no import path between them.

## Which is live/canonical?

- **Live code in the canonical tree: ONLY rep 1 (sancrev).** It is real importable Python in `application/sanctuary-revolution/…`, mirrored in CA, and registered in CartON as `Sancrev_Psychoblood_Events` ("unique to sancrev, not in CAVE"). **Caveat (unverified):** I traced no caller — I did NOT confirm anything actually *invokes* `PsychobloodMachine.tick()` in a running harness. It is "canonical-resident code," not proven "executing."
- **Conceptual canon: rep 4 / 4b** (CartON 9-state ontology + book). The CartON 9 states match rep 1's enum **exactly** (one cosmetic label diff: `Nine_States` says "Fear (terror/edge)", `Ontology` says "Fear/Edge"; code uses `FEAR`).
- **Reps 2 & 3 are a SEPARATE, non-canonical lineage** living only in `/tmp` (halo-sanctuary / CIG). Rep 2 is working ML code but not in the monorepo; rep 3 is an un-built design (references `cig/cig/gp_psychoblood.py` "new" and the missing `.ts` files).

---

## Precise incoherences a unifier WILL hit

1. **Three incompatible state cores, zero converters.** `IntEnum`(9) ↔ `List[float]`(35 OCEAN) ↔ `Dict`(6 provenance). No function maps any pair. The metahologram only gestures at it with **color analogies** (§2 table: "AROUSAL = orange = neutral→excited") — no executable state↔state mapping — and it **deletes OCEAN**, the one core that rep 2 actually runs on.
2. **The 10-loop taxonomy is defined three different ways under the same names:** rep 2 = bare string list + untrained head (no semantics); rep 3 §8 = provenance-autocorrelation signatures; rep 4b ch.5 = emotion SEQUENCES. Unifying requires picking ONE operationalization and rebuilding the others.
3. **Loop-set membership disagrees.** The 10-list has OUTRAGE/DEVOTION/VALUE; the book shows only 6 (SATAN/MARTYR/ADDICTION/HEROISM/COMPASSION/BERSERKING). Partial overlap, not a superset.
4. **Name collisions across orthogonal layers.** `COMPASSION` is BOTH 9-state #7 AND a 10-loop. `BERSERKING` is a 10-loop (rep 2) AND a standalone 4-dim Wangtang module (rep 1 `berserking.py`) AND the book's PBB "golden state" — three operationalizations of one word.
5. **`psychoblood_loop` is a literal stub in rep 2.** `emotion_ml.py:99` → `psychoblood_loop: str = "NONE"  # TODO: integrate detector`. The bridge between OCEAN and loops was never built — the flow_head exists but nothing trains or reads it as state.
6. **Contradictory reward philosophies.** Rep 2 = EXTERNAL journal reward reweighting observations (`apply_journal_reward`). Rep 3 = INTRINSIC, "no reward function needed." These are mutually exclusive design commitments.
7. **Different ML substrates.** Rep 2: sklearn, 35 independent single-output GPs, single Matern kernel, OCEAN→OCEAN regression. Rep 3: gpytorch, one multi-output GP, ProductKernel(emotion×provenance), emotion→provenance. Shared only the "GP bootstrap → LSTM at 500 obs" motif.
8. **rep 1's observer (4-level meta-awareness) and wangtang (4-dim) layers exist NOWHERE else.** Reps 2/3 have no awareness/observer concept at all.

---

## Bottom line for the team
Unifying is not "merge 4 files." It is **a re-derivation**: pick the canonical STATE core (the 9-state ontology is the only one that is both live code AND conceptual canon), decide whether OCEAN and provenance are (a) the *measurement substrate* under the 9 states or (b) competing cores to drop, and **build the missing converters + the never-built loop detector** (rep 2's `# TODO: integrate detector`). The metahologram is the most ambitious unification *attempt* but it (i) is un-built, (ii) discards OCEAN, and (iii) depends on `.ts` source files absent from this box — so it cannot be the integration target as-is.
