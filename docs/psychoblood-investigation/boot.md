# PsychoBlood — Boot / Runtime Investigation (mechanic)

**Question:** How is PsychoBlood SUPPOSED to boot and run live, and is there ANY working wiring —
or did the prior implementation never actually boot? Isaac's hypothesis: the prior AI
misunderstood how to boot it.

**VERDICT (grounded in code): CONFIRMED — it was never bootable/live as a PsychoBlood loop.**
The cognitive pieces exist as standalone libraries. The *boot/integration layer* (registration +
per-turn trigger + tool exposure + caller) was **never written**. There is ZERO live wiring on any
path. Two disconnected lineages exist; neither is fired by anything.

---

## There are TWO disconnected PsychoBlood lineages (they do not reference each other)

### Lineage A — the hand-coded state machine (`harness/events/psychoblood/`)
Files: `psychoblood.py`, `observer_psychics.py`, `berserking.py`
(`/home/GOD/gnosys-plugin-v2/application/sanctuary-revolution/sanctuary_revolution/harness/events/psychoblood/`)

- `psychoblood.py:41` `PsychobloodMachine` — a 9-state `IntEnum` (GROUND…DECAY) with `tick(delta_time)`
  doing **probabilistic random-walk** transitions (`psychoblood.py:83-97`, uses `random.random()`).
- `observer_psychics.py:26` `ObserverPsychics` — meta-awareness levels (UNCONSCIOUS→LUCID);
  `check_awareness()` returns an `[OBSERVER] …` injection string (`observer_psychics.py:37-53`).

**Wiring status: NOT wired anywhere.**
- `events/__init__.py` imports **only `gear_events`** (lines 2-14) — psychoblood is NOT imported.
- harness `__init__.py` exports **only** `PersonaControl`, `PERSONA_FLAG`, and the GEAR events
  (lines 8-22) — psychoblood is NOT exported.
- Repo-wide grep for `PsychobloodMachine`/`ObserverPsychics`/`from .psychoblood`/`from events.psychoblood`
  (excluding `/home/GOD/core/`, the defining files, and `.soma-worktrees` vault copies): **only hits are
  docs/continuity notes and vision(m) files** — NO executable import, NO instantiation, NO caller.

### Lineage B — the OCEAN ML predictor bundle (`/tmp/psychoblood-bundle/emotion_ml.py`)
- `report_emotion(...)` (`emotion_ml.py:441`) labeled **"THE ONE TOOL … (MCP-exposed)"**, with a
  module-level singleton `_emotion_system = EmotionMLSystem()` (`emotion_ml.py:438`).
- Pipeline: report OCEAN[35] → GP surrogate predicts next OCEAN + `icl_prompt` guidance → returns it
  (`emotion_ml.py:207-309`, `_predict_next_state` 311-365, `_generate_icl_prompt` 367-387).
- Self-contained library only: imports `policy`/`gp_surrogate` siblings; persists GP obs to
  `../data/gp_observations.json`.

**Wiring status: NOT wired anywhere.**
- Repo-wide grep for `emotion_ml` / `report_emotion` / `EmotionMLSystem` importers (monorepo, excl
  vault): **ZERO hits.** The only `report_emotion` occurrence in the box is inside `/tmp/brainhook.log`
  — i.e. a transcript of a *conversation about* it, not a caller.
- The bundle contains **no MCP server**: no `FastMCP`, no `@mcp.tool`, no `mcp.run` anywhere in
  `/tmp/psychoblood-bundle/`. The "MCP-exposed" docstring is aspirational/**false** — nothing exposes it.
- Even *inside* the bundle, the psychoblood detector is a stub: `TurnRecord.psychoblood_loop: str =
  "NONE"  # TODO: integrate detector` (`emotion_ml.py:99-100`). So Lineage A's state machine was never
  wired into Lineage B either.

---

## What "live boot" infrastructure actually exists (and what it really runs)

The only thing that ever claimed "psychoblood simulation" is the **DEPRECATED** harness:
`/home/GOD/gnosys-plugin-v2/base/sanctuary-system/game_wrapper_DEPRECATED/core/harness.py`
- `PAIAHarness` (`harness.py:67`) docstring: *"wraps code agents with psychoblood simulation."*
- Its `run_daemon()` loop (`harness.py:370-387`): `watch_output()` + `tick()` + `inject()`.
- **But `tick()` (harness.py:275-287) only calls `PsycheModule`/`WorldModule`/`SystemModule`**, guarded
  by `try: from events.psyche.module import PsycheModule … except ImportError: HAS_MODULES=False`
  (`harness.py:29-35`). It **never** imports or instantiates `PsychobloodMachine` or `ObserverPsychics`.
- `PsycheModule` (`harness/events/psyche/module.py:1`) is just an **RNG nudge emitter**: it references
  the psychoblood *ontology* as canned strings (`STATES = [...]`) and emits fixed messages like
  `"[PSYCHE] THERE IS SOMETHING HERE. I KNOW IT."` on a probability roll. It does NOT run the state
  machine, has no OCEAN, no ML, no observer.
- `inject()` (`harness.py:289-312`) writes `/tmp/paia_injection.txt`, read by `paia_*` hooks. This is the
  one real injection mechanism — but it carries PsycheModule's canned RNG strings, never `report_emotion`'s
  prediction or the observer's awareness string.
- `PAIAHarness` / `run_daemon` is in a `game_wrapper_DEPRECATED/` dir; no live (non-deprecated, non-vault)
  entrypoint invokes it. The *live* sancrev harness `__init__.py` states runtime control **moved to
  cave-harness (`cave.core`)** and sancrev keeps only PersonaControl + GEAR.

---

## The INTENDED live loop (reconstructed from code + the vision doc)

From `emotion_ml.py`'s own header (lines 1-15) + DEPRECATED harness `inject()` + the design vision
(`docs/vision/_psychoblood.md`, `_observer_psychics.md`, `_hiel.md` — all tagged **STATUS = VISION, not
built**; Isaac 2026-06-03: a "live cockpit HUD … HIEL metrics visible on EVERY message"):

```
UserPromptSubmit (per turn)
  → detect/estimate OCEAN[35] + emotion label
  → report_emotion(...)            # GP predicts next OCEAN + icl_prompt + confidence
  → inject icl_prompt as primer    # /tmp/paia_injection.txt -> paia_* hook  (mechanism EXISTS)
  → persist GP observation         # ../data/gp_observations.json
  → (observer_psychics: emit [OBSERVER] awareness string at NOTICING+)
```

### Which links exist as CODE vs are ABSENT
| Link | Status | Evidence |
|------|--------|----------|
| State machine logic | EXISTS (lib) | `psychoblood.py:41-103` |
| Observer levels logic | EXISTS (lib) | `observer_psychics.py:26-67` |
| OCEAN predictor + icl_prompt | EXISTS (lib) | `emotion_ml.py:207-387` |
| Injection mechanism (file→hook) | EXISTS (deprecated) | `harness.py:289-312` |
| **Per-turn trigger calling report_emotion** | **ABSENT** | no hook/caller found anywhere |
| **MCP server exposing report_emotion** | **ABSENT** | no FastMCP/@mcp.tool in bundle |
| **events/psychoblood registered in event registry** | **ABSENT** | `events/__init__.py:2-14` (gear only) |
| **OCEAN detector feeding report_emotion** | **ABSENT** | nothing computes the OCEAN[35] input |
| **psychoblood_loop detector → emotion_ml** | **ABSENT** | `emotion_ml.py:100` `# TODO` |
| **A boot entrypoint** | **ABSENT** | no live `run_daemon`/MCP/hook ties any of it together |

---

## Conclusion

**Isaac's hypothesis is CONFIRMED.** The prior implementation never booted as a live PsychoBlood loop —
not because the cognitive code is broken (the GP bootstrap and the state machine are runnable libraries),
but because **the entire boot/integration layer is missing**: there is no per-turn trigger, no MCP
exposure, no event registration, no OCEAN detector, and no entrypoint wiring the pieces into the live
harness. The two lineages (hand-coded state machine vs OCEAN ML predictor) were never connected to each
other, and neither was connected to a runtime. The one real injection path (PsycheModule →
`/tmp/paia_injection.txt`) lives in a DEPRECATED harness and only ships canned RNG strings.

**The single missing link that blocks boot:** a live caller/trigger. Concretely, the minimum to make it
bootable is (1) an OCEAN/emotion detector at a UserPromptSubmit hook, (2) that hook (or an MCP tool)
calling `report_emotion`, and (3) routing the returned `icl_prompt` into the existing injection
mechanism. None of (1)–(3) exists in code today.
