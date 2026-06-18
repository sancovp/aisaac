# PsychoBlood "prompts" — extraction

## Path / name found
- **`/tmp/psychoblood-bundle/psychoblood-session-prompts.md`** (42 KB, mtime 2026-06-04 07:51 — the newest file in the bundle; the rest of the psychoblood files are 06:36).
- A matching **`/tmp/psychoblood-session-prompts.zip`** also exists in `/tmp`.
- These are the only `*psychoblood*prompt*` hits anywhere under `/tmp` and `/home/GOD` (excluding `/home/GOD/core`).

## 1. WHAT IT IS — concretely

It is **NOT a designed prompt library.** It is a **raw transcript of Isaac's 180 verbatim USER prompts** from one Claude Code session, scraped straight out of `~/.claude/history.jsonl`. The header states it exactly:

```
# Session 42aa7dae-4657-4b28-968d-88711df9eb58
# 180 user prompts
# Date range: 2026-02-05 19:42:52 to 2026-02-08 05:31:20
# Project: /Users/isaacwr/Desktop/claude_code
# Source: ~/.claude/history.jsonl
```

**Structure:** 180 numbered sections. Each item has the shape:
```
## [N] YYYY-MM-DD HH:MM:SS

<the literal text Isaac typed>
```
The fields are: index `[N]`, an ISO timestamp, and the verbatim user message. Nothing else — no model replies, no per-flow mapping, no rubrics, no few-shot pairs. It is the **human half of the conversation only**, in chronological order. Several entries are duplicates (Isaac re-sent edited versions), and many are throwaway control lines (`/compact`, `/exit`, `/model`, `sitrep`, `yeah`).

So: it is the **DESIGN-SESSION TRANSCRIPT** in which Isaac and an agent verbally architected the PsychoBlood / HALO_SANCTUARY emotion-ML system over ~2.5 days. It is the *origin record of the intent*, not the runtime artifact.

## 2. Per-flow / per-state mapping?

**No.** There is no flow→prompt table and no 9-state→strategy mapping in this file. It does not map psychoblood loops or states to response strategies. What it DOES contain is Isaac *describing* the mechanism he wants built, in his own words. The relevant design statements (verbatim):

**The single tool + returned ICL primer (item [18]/[20]):**
> "there is one tool which is `report_user_state` and it *returns* a prompt to the LLM that guides it ICL to adjust its persona style emotional tone to flow with the user properly even if they are angry instead of being sycophantic. this creates space to actually output the correct tokens and not get fucked up by the emotion bullshit. It's a game: User says X and the hook injects 'Call sanctuary_system_mcp.report_user_state() then continue' and it returns '{{the persona rubric that MEANS the emotional values of the psychblood counterpart flow}}'"

**The short/mid/long loop (item [33]):**
> "the LLM has a tool that lets it put keywords that are a DSL that maps to vectors in R^3 ... our ML system just logs that ... and responds. Then, the MCP sees the response of the ML system and gives it back to the AI. The AI *doesnt classify what it is explicitly, it just responds from the priming* ... The mid loop is that they do daily/2x daily journaling ... the long loop is that there's some way to edit the ML system."

**Emergent psychoblood-loop detection (item [36]):**
> "the ML system doesnt compute psychoblood -- it computes NEXT BASE EMOTION until it has bootstrapped psychoblood flows and stuff and they become selectable base emotions. It builds up predictive power until it can ... *resolve* conflicts between human and ai ... by INJECTING the next emotion to the AI, making it respond a certain way, which creates ICL lift over time."

**The transmutation example, stated literally (item [172]):**
> "base emotions should not be changing the reasoning output. The fact that anger makes the output different actually shows why LLMs are so frustrating ... they lock ICL in anger, you have to transition to sadness 'i dont understand why you are nt understanding me! lets get clarity PLEASE. lets chill and figure out what representation bindings are missing here...'"

That last one is the *closest thing in the file to an actual per-flow primer* — but it is Isaac giving an example of the desired transition (anger→sadness) inside a sentence, not a stored prompt keyed to a flow.

## 3. Is this the "primer" / transmutation layer (the missing link)?

**No — but it is the SPEC for that layer, stated verbatim by Isaac.** The actual primer/transmutation layer (detect emotion/flow → inject a transmuting strategy) would be **the string that `report_user_state()` RETURNS** — "the persona rubric that MEANS the emotional values of the psychoblood counterpart flow." That returned-rubric artifact is **described** here but **not contained** here. This file is the design intent; the runtime primer mapping is a thing Isaac repeatedly says the system should *produce/return*, and it is not present as data in this bundle.

What the bundle DOES contain alongside it (the built ML side, mtime 06:36): `gp_surrogate.py` (GP that predicts next 35-dim OCEAN state from human+agent OCEAN), `policy.py` (`EmotionPolicy` LSTM — "LLM is both user AND labeler"), `train_policy.py`, `emotion_ml.py`, plus `gp-ml.md`, `spiral-typology.md`, and the big `gp-psychoblood-metahologram.md`. So the **OCEAN-vector prediction engine exists in code**, but the **emotion→persona-rubric primer text that flows back to the LLM is the piece these prompts call for and that I do not see materialized as a per-flow prompt set.**

## 4. How it would be USED at runtime

Per Isaac's own description in the transcript, the runtime loop is:
1. **Hook (UserPromptSubmit):** user says X → hook injects "Call `sanctuary_system_mcp.report_user_state()` then continue."
2. **LLM** scores the current emotional state as OCEAN floats (35-place vector via the DSL/tool) for the human + agent channels and labels it.
3. **MCP / ML system** (GP now, LSTM later) logs it and **predicts the next OCEAN state**, returns it to the MCP.
4. **MCP returns a primer** to the LLM — the persona rubric for the predicted next emotion — so the LLM **responds FROM the priming** without explicitly classifying, "creating space to output the correct tokens and not get fucked up by the emotion."
5. **Reward:** emergent per-turn LLM self-scoring of the last prediction + a daily HITL Sanctuary(+1)/Wasteland(−2) journal score.

So the consumer of the (yet-to-be-materialized) primer is **the LLM, via a hook that forces the MCP tool call**; the OP/emotion detector is the LLM itself filling the OCEAN vector.

## Honesty notes
- This file **references** things not present in it: the returned persona-rubric prompts, the `report_user_state` MCP, the sanctuary journal, the "meta-PE guide," "towering v2" in the CIG project, the "3-pass autonomous research system," and `gp-psychoblood-metahologram.md` (the last is in the same bundle).
- The "9 states" framing from the investigation prompt does **not** appear in this file; it speaks of base emotions, OCEAN's ~35 facets, and emergent psychoblood "loops/flows," plus HUMAN/AGENT/ZERO/SYSTEM channel states (item [18]).
