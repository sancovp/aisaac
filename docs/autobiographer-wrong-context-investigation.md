# Autobiographer (MOV) Fires With the WRONG Context — Investigation + Fix Design

**Investigator:** autobiographer-investigator (Task #5)
**Date:** 2026-06-06
**Method:** grep-to-locate → FULL-READ of every file entrypoint → fire. Code is source of truth.
**Status of claims below:** `IS` = read in code this session (file:line cited). `DESIGN` = stated intent
from `designs/AUTOBIOGRAPHER_DESIGN.md`. `FIX` = proposed, not yet built.

---

## 0. TL;DR — the exact mechanism

> The **night-journal (evening) ritual fires the autobiographer agent in MORNING mode.**

`autobiographer_journal` is a **single, persistent** agent whose system prompt is built **exactly once at
server boot**, frozen to `mode="journal_morning"`. Both the morning ritual and the evening ritual route to
this same agent. The ritual-trigger table *declares* the intended mode for each ritual
(`journal_morning` / `journal_evening`), but the routing code **never reads that field and never switches
the agent's mode** — and even if it did, `JournalAgent` builds its system prompt only at init, so a later
mode change has no effect. Result: the **evening journal greets the user as morning, runs the opening flow,
and persists the entry as `entry_type='opening'` instead of `'closing'`** — the day-review and night-mode
handoff never run.

There is a second, lesser decoherence: the system prompt's "Current Sanctuary Scores" and "Missing Days"
blocks are **also frozen at boot**, so every journal fires with boot-time scores, not fire-time scores.

---

## 1. The two layers (intent → code) and where each lives

### Intent (DESIGN §2, §3)
- Morning and evening journals are the **same agent in different modes** (DESIGN §2: "THREE agents…each
  runs differently"; morning/evening are the JOURNAL agent in two modes).
- Journal cron flow (DESIGN §3 "Journal cron flow", steps 1–5): cron fires → NIGHT agent contextualizes →
  creates `Journal_Autocontext_{Morning|Evening}_{date}` → **inject that context into the JOURNAL agent's
  system prompt** → fresh fire in the correct (morning/evening) mode.

### Code (what actually runs)
The pieces all EXIST — the **wire that switches mode at fire time was never built**.

---

## 2. The fire path, traced (entrypoint → firing)

### 2a. Trigger table — declares the intended mode (and it's correct)
`application/cave/cave/core/sanctum_automations.py:429-433`
```python
_RITUAL_TRIGGERS = {
    "morning-journal": {"agent": "autobiographer_journal", "mode": "journal_morning", "period": "morning"},
    "night-journal":   {"agent": "autobiographer_journal", "mode": "journal_evening", "period": "evening"},
    "friendship-saturday": {"agent": "autobiographer_night", "job_type": "friendship"},
}
```
- IS: **Both journals target the SAME agent** `autobiographer_journal`.
- IS: The intended modes differ (`journal_morning` vs `journal_evening`) — the **`mode` field encodes the
  correct intent.**

### 2b. The router — reads `agent` and `period`, **NEVER reads `mode`**
`application/cave/cave/core/sanctum_automations.py:436-481` (`_route_trigger`)
- IS line 445: `agent_name = trigger.get("agent", "autobiographer")`
- IS line 450: `period = trigger.get("period", "morning")`
- IS lines 451-467: assembles `content` (the **user message**) — embeds the autocontext text if
  `journal_autocontext_{period}.txt` exists & >300 chars, else a fallback prompt that tells the agent to
  fetch `Journal_Autocontext_{period_cap}_{today}` from CartON.
- IS lines 471-475: `httpx.post("…/agents/{agent_name}/message", json={"content": content, …})`
- **`trigger["mode"]` is never referenced anywhere in this function.** No `set_mode`, no mode in the POST
  body. (Grep confirms `set_mode` is called in exactly one place in the whole tree — see 2d.)

### 2c. The HTTP route — just enqueues; no mode parameter
`application/sanctuary-revolution/sanctuary_revolution/harness/server/sancrev_routes.py:1511-1549`
- IS: builds a `UserPromptMessage(content=…)`, `agent.enqueue(msg)`, `asyncio.create_task(agent.check_inbox())`.
- IS: the body schema is `{"content","source","priority"}` only — **no `mode`.** The content becomes a
  normal inbox message processed under the agent's existing (frozen) system prompt.

### 2d. The agent — system prompt built ONCE at boot, frozen forever
`application/sanctuary-revolution/sanctuary_revolution/agents/journal_agent.py`
- IS line 73-82 (`init_runtime`): `agent_config = HeavenAgentConfig(… system_prompt=self._build_system_prompt() …)`
  — **`_build_system_prompt()` is called exactly once** (grep: only call site is line 75).
- IS line 93: `self._agent_config = agent_config` (stored once).
- IS line 105: every `journal_run()` reuses `journal_ref._agent_config` unchanged → **the system prompt is
  the boot-time string on every fire.**
- IS line 206-214: the `journal_morning` block — *"It's morning… Walk me through your 6 dimensions…
  journal_entry(entry_type='opening', …)"*.
- IS line 215-224: the `journal_evening` block — *"It's evening… Review the day… ritual completions…
  journal_entry(entry_type='closing', …)… announce that night mode is starting."* — **never reached for
  `autobiographer_journal`.**
- IS line 336-343 (`set_mode`): sets `self._mode` only — it does **NOT** rebuild the system prompt. So even
  a correctly-plumbed `set_mode("journal_evening")` would change nothing about behavior, because the prompt
  is already frozen into `_agent_config`.

### 2e. The wiring — the agent is pinned to morning at boot
`application/sanctuary-revolution/sanctuary_revolution/harness/server/waking_dreamer.py`
- IS line 96: `self._wire_journal_runtime(agent_name="autobiographer_journal", default_mode="journal_morning")`
- IS line 208 (`_wire_journal_runtime`): `journal_agent.set_mode(default_mode)` **— the ONLY `set_mode` call
  in the entire codebase**, at wire time, with `journal_morning`.
- → `autobiographer_journal` boots in `journal_morning` and **stays there for the life of the process.**

---

## 3. The bug chain → the EXACT observed symptom

```
step 1  Server boots. waking_dreamer.py:96 wires `autobiographer_journal` with default_mode="journal_morning".
step 2  waking_dreamer.py:208 → journal_agent.set_mode("journal_morning"); self._mode="journal_morning".
step 3  init_runtime (journal_agent.py:75) calls _build_system_prompt() ONCE → emits the MORNING block
        (lines 206-214: "It's morning… entry_type='opening'"). Frozen into _agent_config.system_prompt (line 93).
step 4  ~10 PM: night-journal ritual fires. fire_ritual_notification → _route_trigger("night-journal").
step 5  _route_trigger (sanctum_automations.py:436) reads agent="autobiographer_journal", period="evening".
        It IGNORES trigger["mode"]="journal_evening" (the field is never read).
step 6  It POSTs a user-message ("…request my evening journal now…") to /agents/autobiographer_journal/message.
step 7  The route (sancrev_routes.py:1511) enqueues the message; check_inbox → run_with_content → journal_run.
step 8  journal_run (journal_agent.py:96) runs BaseHeavenAgent with the FROZEN _agent_config — system prompt
        still says MORNING / "Walk me through your 6 dimensions" / entry_type='opening'.
step 9  SYMPTOM: the evening journal greets the user as morning, runs the OPENING flow, and (following its
        system prompt) calls journal_entry(entry_type='opening') — NOT 'closing'. The evening "review the day /
        ritual completions / announce night mode" flow (journal_agent.py:215-224) never executes.
        The user message says "evening" while the system prompt says "morning" → contradictory context;
        the frozen system prompt governs tone + the entry_type instruction.
```

This reproduces the reported symptom **exactly**: the autobiographer "fires with the wrong context" — the
**evening fire carries the morning system-prompt context.** The `mode` field present in the trigger table
(step 5) is the fingerprint that the *intent* was correct and only the *wiring* is missing.

### Secondary symptom (same root family — frozen prompt)
Because `_build_system_prompt()` runs only at boot (step 3), the **"Current Sanctuary Scores"
(journal_agent.py:182-185, read from `sanctum_status.txt`) and "Missing Days" (lines 188-196)** blocks are
snapshotted at server-start and never refreshed. Every journal — morning included — fires with **boot-time
scores/gaps**, not the state at fire time. (The night agent's `missing_days_queue.json` and current sanctum
scores update on disk, but the journal never re-reads them after boot.)

### What is NOT the bug (ruled out)
- The night agent's autocontext **does** reach the model — `_route_trigger` (sanctum_automations.py:451-458)
  embeds `journal_autocontext_{period}.txt` into the **user message**. (DESIGN §3 step 4 wanted it injected
  into the *system prompt*; current code delivers it via the user message. That is a design-alignment gap,
  not a correctness bug — the content arrives either way. It is, however, period-correct, so it is not the
  source of the wrong-context symptom.)
- The autocontext concept name is consistent across producer/consumer: night agent writes
  `Journal_Autocontext_{period_cap}_{today}` with `today=strftime("%Y_%m_%d")` (night_agent.py:307-309);
  the fallback prompt references the same name with `clock.today().replace("-","_")` (sanctum_automations.py:460-464).
  Matches — not a bug.

---

## 4. Fix design (do NOT implement yet — design only)

The root cause is two coupled defects; **both must be fixed** or the symptom persists:

- **D1 — mode never switched at fire time:** `_route_trigger` ignores `trigger["mode"]` and there is no
  plumbing (route or call) to switch the target agent's mode.
- **D2 — system prompt frozen at boot:** `JournalAgent` builds its system prompt once; `set_mode` does not
  rebuild it. So even fixing D1 alone (calling `set_mode`) would not change behavior.

### Recommended fix (minimal, fixes D1 + D2 + the secondary staleness for free)

**Part A — rebuild the system prompt at every fire (fixes D2 + stale scores/missing-days).**
In `journal_agent.py`, inside `journal_run` (the async closure starting at line ~96), **rebuild the system
prompt from the current mode before constructing the agent** each call:
```python
# at top of journal_run, before agent_kwargs:
journal_ref._agent_config.system_prompt = journal_ref._build_system_prompt()
```
This makes the prompt reflect the **current** `self._mode`, sanctuary scores, and missing-days on every
fire. (Alternatively, make `set_mode` rebuild `self._agent_config.system_prompt`; rebuilding in `journal_run`
is strictly safer because it also refreshes scores/missing-days, addressing the secondary symptom.)

**Part B — actually switch the mode for the firing (fixes D1).** Plumb `trigger["mode"]` to the agent
before the message is processed. Two options:

- **B1 (preferred — explicit mode in the envelope):** extend the `/agents/{agent_name}/message` route
  (`sancrev_routes.py:1511`) to accept an optional `"mode"` in the body; when present and the agent has
  `set_mode`, call `agent.set_mode(mode)` **before** `check_inbox()`. Then in `_route_trigger`
  (`sanctum_automations.py:471-475`), include `"mode": trigger["mode"]` in the POST body for journal
  triggers. With Part A in place, the rebuilt prompt then carries the evening block.

- **B2 (alternative — dedicated mode route):** add `POST /agents/{name}/mode {"mode": …}` that calls
  `set_mode`, and have `_route_trigger` POST the mode first, then the message. More round-trips; B1 is cleaner.

**Ordering matters:** the mode must be set **before** `check_inbox()`/`journal_run` rebuilds the prompt
(Part A). In B1 this is naturally ordered inside the single route handler (set_mode → create_task(check_inbox)).

### Concurrency note (single shared agent)
`autobiographer_journal` is a process-singleton serving both periods. Morning and evening fire ~16h apart,
so a mode race is not practically reachable today — but the design is fragile. If a future change can fire
both near-simultaneously, prefer passing the mode **per-message** (carry it on the `UserPromptMessage` and
have `journal_run` build the prompt for that message's mode) rather than mutating shared `self._mode`.
Lowest-risk now: B1 + Part A; revisit per-message mode if concurrent firing becomes possible.

### Optional (DESIGN-alignment, not required for correctness)
To match DESIGN §3 step 4 ("inject context into the JOURNAL agent's **system prompt**"), `_build_system_prompt`
could read `journal_autocontext_{period}.txt` / `get_concept('Journal_Autocontext_{period_cap}_{today}')` and
add it as a system-prompt block. With Part A this becomes natural (prompt rebuilt per fire). Lower priority —
the autocontext already reaches the model via the user message today.

---

## 5. File:line index (every cited fact)

| Fact | Location |
|---|---|
| Both journals → same agent; `mode` field declared but unused | `cave/core/sanctum_automations.py:429-433` |
| Router reads agent/period, never `mode`, never `set_mode` | `cave/core/sanctum_automations.py:436-481` |
| Autocontext delivered as USER MESSAGE (not system prompt) | `cave/core/sanctum_automations.py:451-458` |
| `/agents/{name}/message` enqueues content; no `mode` param | `sanctuary-revolution/.../server/sancrev_routes.py:1511-1549` |
| System prompt built ONCE at init | `sanctuary-revolution/.../agents/journal_agent.py:73-82` (call site line 75) |
| `_agent_config` stored once + reused every fire | `journal_agent.py:93, 105` |
| MORNING block (opening) vs EVENING block (closing) | `journal_agent.py:206-214` / `215-224` |
| `set_mode` sets `_mode` only; does NOT rebuild prompt | `journal_agent.py:336-343` |
| Scores/missing-days read only at build time (frozen) | `journal_agent.py:182-196` |
| Journal agent wired to `journal_morning` permanently | `waking_dreamer.py:96` |
| The ONLY `set_mode` call in the tree (boot, morning) | `waking_dreamer.py:208` |
| Night agent produces autocontext (concept + file) | `sanctuary-revolution/.../agents/night_agent.py:297-395` |

---

## 6. FIX IMPLEMENTED (Task #14, 2026-06-06) — `IS` (E2E-verified against edited monorepo source)

Both coupled defects fixed with three surgical edits. Diff: `/tmp/autobiographer_evening_fix.patch`.

**Edit 1 — D2, per-fire prompt rebuild** — `journal_agent.py`, top of the `journal_run` closure
(after the heaven imports, before `agent_kwargs`):
```python
journal_ref._agent_config.system_prompt = journal_ref._build_system_prompt()
```
Rebuilds the system prompt on every fire from the CURRENT `self._mode` (+ fresh scores/missing-days),
undoing the boot-freeze. Required — without it, switching mode has no effect (prompt stays frozen-morning).

**Edit 2 — D1, route applies the mode** — `sancrev_routes.py`, `/agents/{agent_name}/message` handler,
after the content check and BEFORE `enqueue`/`check_inbox`:
```python
mode = body.get("mode")
if mode and hasattr(agent, "set_mode"):
    agent.set_mode(mode)
```
Guarded — only `JournalAgent` has `set_mode`; all other agents (incl. `autobiographer_night`) are untouched.

**Edit 3 — D1, trigger sends the mode** — `sanctum_automations.py`, `_route_trigger`, the journal POST:
```python
payload = {"content": content, "source": "sanctum", "priority": 8}
if "mode" in trigger:
    payload["mode"] = trigger["mode"]
```
`_RITUAL_TRIGGERS` already declared the right mode per ritual (`journal_morning`/`journal_evening`); this
finally consumes it. Friendship trigger has no `mode` key → no change to that path.

`waking_dreamer.py` — **no change** (the per-fire mode override supersedes the boot default).

### E2E evidence (in-process, monorepo source pinned ahead of site-packages)
Test: `/tmp/autobiographer_fix_e2e.py` — **RESULT: PASS**. Exercised the real edited functions:
- **D2:** boot(morning) prompt = MORNING block (`entry_type='opening'`); after `set_mode('journal_evening')`
  + rebuild = EVENING block (`entry_type='closing'` + "night mode is starting"), and the morning opening
  instruction is GONE. The two prompts differ by mode → the rebuild changes context per fire (the frozen
  behavior was the bug).
- **D1:** `_route_trigger("night-journal")` → POST to `…/agents/autobiographer_journal/message` with
  `payload["mode"]=="journal_evening"`; `morning-journal` → `"journal_morning"`; `friendship-saturday` →
  no `mode` key, routed to `autobiographer_night`.

### NOT yet verified live (needs deploy + restart — flagged, NOT done on shared infra)
- Runtime is the **pip-installed** package (`/home/GOD/.pyenv/.../site-packages/{cave,sanctuary_revolution}`),
  NOT the monorepo. To go live: `pip install --no-deps /home/GOD/gnosys-plugin-v2/application/cave` and
  `… /application/sanctuary-revolution`, then RESTART the sancrev WakingDreamer server.
- The full WakingDreamer harness with `autobiographer_journal` is **not currently running** (`:8080`
  `/agents` shows only `main`). A true live-Discord E2E (fire the night-journal ritual, observe MOV greet
  as evening + persist `entry_type='closing'`) requires that server up — deferred to a safe window so
  concurrent agents sharing this box are not disrupted.
- The route-handler glue (Edit 2) is verified by `py_compile` + the producer/consumer E2E (trigger sends
  `mode`; agent applies `mode`+rebuilds); the 3-line guarded block is the verified-by-inspection conduit
  between those two tested ends.

### Reversibility
The 3 target files were clean before this change → `git checkout -- <the 3 files>` fully reverts; patch
backup at `/tmp/autobiographer_evening_fix.patch`. NOT branched/committed: the monorepo working dir is
shared with concurrently-running agents (a `git checkout -b` would move every agent's HEAD), so changes are
left as scoped uncommitted edits for team-lead to commit on a chosen branch.

---

## 7. DEV-FLOW NOTE — editing the autobiographer journal-firing path

**When you touch the autobiographer journal mode/fire path, edit ALL THREE in lockstep (they are one
contract):**
1. `cave/core/sanctum_automations.py` — `_RITUAL_TRIGGERS` (declares per-ritual `agent`/`mode`/`period`/
   `job_type`) and `_route_trigger` (assembles the user-message `content` + the POST `payload`, incl. `mode`).
2. `sanctuary-revolution/.../harness/server/sancrev_routes.py` — `/agents/{agent_name}/message` (reads
   `body["mode"]`, applies `set_mode` before `check_inbox`). If you add a new per-fire field, plumb it here.
3. `sanctuary-revolution/.../agents/journal_agent.py` — `set_mode` (the valid-mode set), `_build_system_prompt`
   (the mode→prompt mapping, incl. the morning/evening/chat/friendship blocks), and the `journal_run` rebuild
   line (the per-fire prompt refresh). New mode ⇒ add a valid-mode entry AND a prompt block.

**Invariant to preserve:** the system prompt is rebuilt per fire (`journal_run`), and the firing mode is set
*before* `check_inbox`. Break either and the evening journal silently regresses to morning. There is ONE
persistent `autobiographer_journal` serving both periods — mode is per-fire, not per-agent.

**How to test (no live server needed):** run `/tmp/autobiographer_fix_e2e.py` (pins monorepo source via
sys.path; asserts D1 payload mode + D2 evening prompt). For a real live check: deploy (`pip install
--no-deps` both packages) + restart WakingDreamer, then fire the `night-journal` ritual and confirm MOV
greets as evening and calls `journal_entry(entry_type='closing')`.

**Deploy:** monorepo is canonical source; runtime is the pip-installed copy → always `pip install --no-deps`
both packages + restart the server for changes to take effect (per `canonical-source-dirs` +
`pip-install-our-packages-no-deps`).

*(This note is the lightweight dev-flow per the task. It can be promoted to a full dev-flow skill +
use-rule if this path is touched often.)*
