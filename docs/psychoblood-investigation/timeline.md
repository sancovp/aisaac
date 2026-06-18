# PsychoBlood — Timeline Archaeology (deconfabulated + self-verified)

**Investigator:** archaeologist (team psychoblood-depth) · **Date:** 2026-06-04
**Method:** heaven timeline-archaeologist (deconfabulate skill, verbatim runner `/tmp/run_pb_deconfab.py`,
history `/tmp/heaven_data/agents/deconfabulator/memories/histories/2026_06_04/2026_06_04_07_07_14_deconfabulator.json`)
+ independent `query_wiki_graph` verification of every load-bearing fact + on-disk code reads.

**Timeline freshness horizon (checked FIRST):** newest `User_Message` = `2026_06_04T04_23_10` →
ingestion is ALIVE and fully covers the Jan–Mar 2026 period in question. Absences below are real, not pipeline gaps.

---

## TIMELINE OF WORK (when psychoblood was actually touched)

| Date | What happened | Evidence type |
|------|---------------|---------------|
| **2026-01-16 01:53:51** | The psychoblood module files written to disk: `psychoblood.py` (9-state machine), `berserking.py` (wangtang), `observer_psychics.py` — AND a separate `psyche/module.py`. All four share an **identical-to-the-nanosecond mtime** → written/imported as one batch. | filesystem mtime (monorepo) |
| **2026-01-23 15:23–15:24** | Architecture defined as CartON concepts: `Psychoblood_Nine_States`, `Psychoblood_State_Transitions`, `Psychoblood_Heros_Journey_Mapping`, `Psychoblood_Ontology`. | CartON nodes (deconfab) |
| **2026-02-23 / 02-25** | psychoblood discussed as a **cognitive-architecture concept** ("pump antibodies through psychoblood / cognitive flow"). Discussion only. | Iteration_Summary |
| **2026-03-03** | Auto-created stub nodes (`Psychoblood`, `Psychoblood_Missing`, `Psychoblood_Sidechaining`) — empty stubs, not work. | CartON stubs |
| **2026-03-04** | `Sancrev_Psychoblood_Events` concept notes files at `/tmp/sanctuary-revolution/.../events/psychoblood/`, "Unique to sancrev - not in CAVE." | CartON node |
| **2026-03-09** | "Psychoblood GP" added to project list as **HOST-ONLY**, marked "?" (uncertain). | Iteration_Summary |
| **2026-03-16 05:44** | Agent **READ** all three psychoblood `.py` files. `USES_TOOL → Read` (NOT Edit/Write). No code changed. | Tool_Call (verified USES_TOOL) |
| **2026-03-17** | Last active day. Isaac wrestling with HOW psychoblood gets coded; creates `Psychoblood_Mechanics`, `Psychoblood_Implementation`, `Psychoblood_Implementation_Planning`, `Skill_Understand_Psychoblood_As_Code`. Whole day's thrust = designing the **autoresearch / researcher / observatory / grug / compoctopus** stack. | Iteration_Summary + User_Message |
| **2026-05-22 / 05-24** | psychoblood resurfaces ONLY as a "spirituality/fringe **CONTENT** channel." Never coded again. | User_Message + Iteration_Summary |

Last code-touch in the ingested timeline = **2026-03-16 (a Read)**. Last active design/impl-planning = **2026-03-17**.

---

## ACTION EVIDENCE — real impl vs discussion

**REAL ARTIFACTS THAT EXIST (built, on disk, verified by reading):**
- `application/sanctuary-revolution/sanctuary_revolution/harness/events/psychoblood/psychoblood.py` —
  `PsychobloodMachine`: the **9-state machine** (IntEnum GROUND…DECAY) + probabilistic `StateTransition`s +
  `tick()`/`force_state()`. Docstring: *"From PSYCHO BLOOD 1 conversation."*
- `berserking.py` — `BerserkingModule`/`WangtangState` (fear/arousal/compassion/logic_lattice → wangtang_score; the "berserking" keyword).
- `observer_psychics.py` — `ObserverPsychics` meta-awareness (Unconscious→Noticing→Witnessing→Lucid; the "observer psychics" keyword).
- Built ~Jan 16, designed in CartON Jan 23. **This is the real `IS`.**

**NOT FOUND / not built in anything visible here:**
- **GP surrogate** — REAL but as *host-only research*, not in the monorepo/timeline. Isaac (verbatim, 2026-03-17T17:36):
  *"we have a GP that is starting to detect this actually i was doing the research. Psychoblood is about detection
  and response. We detect it, the GP responds with the prompt that counter injects the AI against the user emotions…
  and interrupts the psychoblood loops by changing their neurotransmitter cocktail."* → lives in the **HOST-ONLY
  `psychoblood-gp`** project (per canonical-source-dirs; not present in this container — `ls` confirms absent).
- **LSTM policy + OCEAN states** — **ZERO evidence in the entire ingested timeline** (query for psychoblood∧(ocean∨lstm) = none).
  Psychoblood uses its **own 9-state ontology (Ground…Decay), NOT the OCEAN/Big-Five traits.** The "LSTM policy over
  OCEAN" framing in the claim appears to be a **CONFLATION** — treat as unverified.

---

## THE BOOT/WIRE GAP (strong evidence for the "never booted live" hypothesis)

The rich psychoblood object model (`PsychobloodMachine` + `BerserkingModule` + `ObserverPsychics`) is
**never imported anywhere** — `grep` for imports of those classes across the whole monorepo = nothing outside
its own dir. Instead the harness wires a **separate, thin `psyche/module.py` `PsycheModule(RNGModule)`** — same 9
state *names* as strings, but only fixed RNG "nudge" messages, no probabilistic machine, no wangtang, no observer.

→ **Two parallel implementations co-existed from day one (identical mtime); only the thin RNG stub got wired into
the running harness; the real system was built standalone and never connected to a live loop.** That IS a
boot/runtime gap. Reinforced by Isaac's own 2026-03-17 words: *"im just trying to like… understand how this stuff
gets **coded**"* and *"We know psychoblood flows from monitoring the user's psychology per turn… hmm…"* — an
explicit struggle with how to wire/run it live, not a logic problem.

---

## WHERE & WHY IT STOPPED

**When:** active work ended **2026-03-17, 2026**. After that: deferred, then content-only (May).

**Why (verified):** psychoblood's implementation got **SUBSUMED INTO the autoresearch/researcher/observatory
effort** Isaac was architecting all day on 2026-03-17 — the plan shifted to *"the researcher will build/evolve
it"* rather than coding it directly. The blocker shape was **how-to-code/wire-it-live** (the boot gap above),
combined with the system being big enough that Isaac routed it through the not-yet-built autoresearch pipeline.

**Correction to the deconfab agent's verdict:** the archaeologist concluded *"Isaac explicitly abandoned it on
Mar 17 citing complexity, planning to resume via the autoresearch system."* I verified the dates and the
autoresearch-deferral (TRUE), but found **no verbatim "too complex, abandoning" statement** — what is on the
record is a how-to-code-it struggle + deferral into autoresearch. So "explicitly abandoned citing complexity"
is **slightly overstated**; the accurate version is **"deferred/subsumed into the autoresearch system; never
resumed (autoresearch itself was never finished); resurfaced only as content."**

---

## VERDICT: **PARTIAL — built, designed, but never wired/booted; then deferred & abandoned-by-drift**

- 9-state machine + berserking + observer psychics: **REAL CODE** (Jan 16), **REAL DESIGN** (CartON Jan 23). ✅
- Wired into a running surface / booted live: **NO** — standalone, unimported; harness uses a thin RNG stub. ❌
- GP surrogate: **REAL but host-only research** (`psychoblood-gp`), invisible here. ⚠️
- LSTM policy over OCEAN: **UNVERIFIED / likely conflation** (no timeline evidence; psychoblood ≠ OCEAN). ❌
- Stopped: **2026-03-17**, subsumed into autoresearch (never finished) → content channel by May. The blocker has
  a real boot/runtime face: the best system was built but never connected to a live loop.
