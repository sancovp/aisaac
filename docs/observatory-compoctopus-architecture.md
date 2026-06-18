# Observatory + Compoctopus — Storage & LLM-Call Architecture

**Author:** saas-mapper · **Date:** 2026-06-06
**Method:** Full/targeted reads of source (cited `file:line`). `IS` = read from code; `UNCLEAR` =
not confirmed / not full-read. Code is source of truth.
**Paths confirmed:** compoctopus = `/home/GOD/gnosys-plugin-v2/application/compoctopus/` ✓ ;
observatory = `/home/GOD/gnosys-plugin-v2/integration/observatory-sdna/` ✓ (both where expected).

---

## A. Compoctopus

**What it IS:** a self-improving **compiler-of-agents**. A "Bandit" (`router.py`) decides, per task,
between **ChainSelect** (reuse a graduated "golden chain") and **ChainConstruct** (build a new agent
pipeline). Everything is a `CompoctopusAgent` = a **Chain of SDNA steps** (each LLM step = an SDNAC with
its own heaven agent; mechanical steps = FunctionLinks). It compiles `.🐙/.octo` specs and Claude-Code
components, and spawns "pilot"/"ralph" worker agents to do real code work.

### A.1 STORAGE — where state/data lives

| Site | What's stored | Writes / Reads | Status |
|---|---|---|---|
| **In-memory dict** `GoldenChainStore` (`golden_chains.py:46`) | graduated high-reward configs (`GoldenChainEntry`), LRU+TTL | written by `graduate()` on bandit success; read by ChainSelect | **IS in-memory only**. `sync_to_carton`/`sync_from_carton` = **`NotImplementedError`** (`golden_chains.py:182-198`) → **NOT persisted** |
| **In-memory dict** `SensorStore` (`sensors.py:37`) | per-config execution `SensorReading`s → reward signal (success·0.4+eff·0.3+human·0.3) | written after each agent run; read by the Bandit + graduation check | **IS in-memory only**; no persistence at all |
| **Registry** (`registry.py`) | MCPs/skills/domains/arms the Bandit queries | `register_*` / `find_*` | **IS in-memory** (`backend="static"` dict). `backend="carton"` is **designed-not-wired**: semantic search "not yet integrated" (`registry.py:210-214,271-274`); `sync_from/to_carton` = **`NotImplementedError`** (`registry.py:351-377`) |
| **File queue** `PILOT_QUEUE` (`agents/pilot/factory.py:58,80,95,283,300`) | starship-pilot work items as JSON in `pending/`/`response/`/`done/` (under `/tmp`) | `write_text(json.dumps(...))`; polled by glob | **IS** real file-based queue |
| **`/tmp` queues/dirs** | `COMPOCTOPUS_AUTO_QUEUE=/tmp/compoctopus_auto_queue` (`tools/tools/go_auto_tool.py:23`); `auto_daemon.py`, `mermaid_maker.py`, `tools/build_prd_tool.py`, `integration/run_octocoder.py` all use `/tmp`; `run_octohead.py` uses `HEAVEN_DATA` | auto-dev cycle queue, PRD scratch, rendered mermaid, octocoder I/O | **IS** ephemeral `/tmp` scratch/queues |
| **neo4j (indirect)** (`agents/pilot/factory.py:206-258`) | NOT written by compoctopus itself — it **configures a neo4j MCP** (`bolt://host.docker.internal:7687`, CA's `neo4j_codebase_mcp`) and hands it to the **spawned pilot agent** | the pilot agent reads the code-graph via that MCP | **IS** (config only; compoctopus owns no neo4j writes) |

**Storage bottom line (IS):** compoctopus's own durable state is **`/tmp` JSON file queues**; its
"knowledge" stores (golden chains, sensors, registry) are **in-memory and ephemeral** — every
Carton/KG persistence path is an explicit **`NotImplementedError` stub**. (Matches the verified
sanctuary-system-architecture note: "reward/emanation in-memory, exact-match, non-persistent; Carton
persistence stubbed.")

### A.2 LLM CALLS — where / how / from where / what types

- **Where (call site):** never in compoctopus source directly. Each `CompoctopusAgent` wraps a `Chain`
  of **SDNACs**; "each SDNAC has its own `HermesConfig` → its own Heaven agent (Ariadne context →
  Poimandres LLM execution via HeavenAgent)" (`agent.py:1-29,126-143`). The LLM call happens **inside the
  heaven-framework HeavenAgent**, invoked by `chain.execute(ctx)`.
- **How (client/library):** the **heaven framework** (`HermesConfig`/`BaseHeavenAgent`; local patch in
  `heaven_patch/baseheavenagent.py`). **No direct `litellm`/`anthropic`/`openai`/langchain call exists in
  compoctopus source** — confirmed: grep for those clients in `agents/ralph/core.py` + `octopus_coder.py`
  returned **nothing**. Compoctopus only *configures* (model, system prompt, tools) and runs the chain.
- **From where (trigger):** `run_*.py` entrypoints + `mcp_server.py` + `auto_daemon.py` → the Bandit
  (`router.py`) → `CompoctopusAgent.execute()` → `Chain`/`EvalChain` → SDNAC → heaven agent. Worker
  agents: the **pilot** (`agents/pilot/`) and **ralph** TDD coder (`agents/ralph/core.py`, the same module
  ralph-saas's worker invokes via `python3 -m compoctopus.agents.ralph.core`).
- **What types (models / shape):** default **`model="minimax"`** (`agent.py:83`). Call shapes by agent
  type (`agent.py:22-26`): Planner = `Chain` (sequential, no loop); OctoCoder = `EvalChain` (anneal loop
  with a verify evaluator); Bandit = `EvalChain` (SELECT→CONSTRUCT→SELECT loop). So: **agent-loop**
  (multi-turn heaven agents) with mechanical FunctionLink steps interleaved; provider = MiniMax (model
  string is configurable per agent).
- **UNCLEAR:** exact provider envelope (which client the heaven `HermesConfig` ultimately uses —
  litellm/uni-api/anthropic-compat) lives in the heaven framework, not read here; flagged, not confirmed.

---

## B. Observatory (observatory-sdna)

**What it IS:** an autonomous **research agent** that runs the **scientific method as a Chain** — a
`CompoctopusAgent` named "researcher" = Chain of **5 SDNACs (observe → hypothesize → propose →
experiment → analyze)** + a FunctionLink that **dispatches experiments to "Grug"** (a separate
experiment-runner agent). "The Chain IS the state machine — Python controls phase transitions, not the
LLM" (`agents.py:1-20`). It is literally a **domain instance of the Compoctopus `CompoctopusAgent`
pattern** (imports `compoctopus.agent.CompoctopusAgent` + `sdna.chain_ontology`).

### B.1 STORAGE — where state/data lives

| Site | What's stored | Writes / Reads | Status |
|---|---|---|---|
| **CartON (KG)** via `carton_mcp` | research observations (typed scientific-method tags → CartON concepts) | `record_observation` → `carton_mcp.server_fastmcp.observe_from_identity_pov(data, agent_identity="researcher")` (`researcher_mcp.py:249-250`); `query_knowledge` → `carton_mcp.carton_utils.CartOnUtils.query_wiki_graph(cypher)` (`researcher_mcp.py:317,338`) | **IS — real, live CartON read+write** (neo4j-backed wiki graph). Unlike compoctopus, this is wired, not stubbed |
| **File queue** `/tmp/heaven_data/observatory/` (`runner.py:23,33,39`) | the researcher investigation **queue** (`QUEUE_FILE`, JSON) — `new` vs `resume` entries, phase progress, paused-after-experiment-for-grug state | `runner.py` read/write_text(json); the runner state machine | **IS** real file-backed queue/state |
| **Memory files** (`agents.py:111-130`) | `researcher_memory.md` (read each phase) + `researcher_prior_concepts.md` (last ~100 investigation concepts, refreshed from CartON) | written by `researcher_mcp` / `_refresh_prior_concepts`; read by phase SDNACs | **IS** — markdown memory to dodge CartON queue lag |
| **Validity cache** `/tmp/heaven_data/observatory/validity/{investigation}.json` (`researcher_mcp.py:37,49-73`) | per-investigation concept validity (valid/invalid/revalidated timestamps) | `mark_valid`/`_save_validity` write_text(json) | **IS** |
| **`mcp_server.py`** | json.dump ×9 (server-side state) | — | UNCLEAR (not full-read; likely the same observatory queue surface) |

**Storage bottom line (IS):** observatory persists to **CartON (real, live)** for the knowledge graph
**plus** a `/tmp/heaven_data/observatory/` **file layer** (queue + memory + validity) used specifically to
**work around CartON ingestion queue lag** (the `TOOL_SLEEP=15s` + retry-after-30s pattern,
`researcher_mcp.py:35,340-345`).

### B.2 LLM CALLS — where / how / from where / what types

- **Where (call site):** each scientific-method phase is an **SDNAC** built in `agents.py`
  (`_make_phase_hermes` `agents.py:147-187`; `_make_phase_sdnac` `:190-207`; assembled into a
  `CompoctopusAgent` `:301-471`). The LLM call runs inside the heaven agent the `HermesConfig` builds
  (same Ariadne→Poimandres path as compoctopus).
- **How (client/library):** **heaven framework `HermesConfig` + SDNAC** (`agents.py:160,559`), with
  `sdna.chain_ontology.Chain` driving sequencing (`agents.py:37`). MCP attached to each phase agent =
  **`researcher-mcp`** only (`_get_researcher_mcp_servers` `agents.py:92-104`, resolved via
  `shutil.which("researcher-mcp")`, stdio). **No direct litellm/anthropic/openai** in observatory source.
- **From where (trigger):** `runner.py` (the queue state machine) / `mcp_server.py` / `grug_server.py` →
  builds `make_researcher_compoctopus(...)` → `ResearcherChain.execute()` (`agents.py:40-85`) → each
  SDNAC → heaven agent. The chain **pauses after EXPERIMENT** and resumes on a **Grug callback**
  (`runner.py:42-65,196-216`); Grug (`grug_agent.py`/`grug_server.py`) is the **separate experiment-runner
  agent** that actually executes proposed experiments.
- **What types (models / shape):** **`DEFAULT_MODEL = "MiniMax-M2.7-highspeed"`** — "MiniMax via
  Anthropic-compatible API" (`config.py:5-6`); every phase SDNAC is created `model=model`
  (`agents.py:165,383,397,415,432,455,471`). Call shape = **multi-phase agent-loop** (5 fresh LLM
  conversations, ≤15 turns each — `_make_phase_hermes(..., max_turns=15)` `agents.py:147`), sequenced by a
  Python Chain (not an LLM state machine), with a mechanical Grug-dispatch FunctionLink between PROPOSE
  and EXPERIMENT.
- **UNCLEAR:** Grug's own LLM client/model not read this pass (`grug_agent.py` not opened); same
  heaven-framework provider-envelope caveat as compoctopus.

---

## C. Cross-repo relationship (IS)
Observatory **is built on Compoctopus**: it imports `compoctopus.agent.CompoctopusAgent` +
`compoctopus.chain_ontology.FunctionLink` (`agents.py:216,320`) and `sdna.chain_ontology`, and realizes the
same **Chain-of-SDNACs-with-per-phase-Hermes-agents** pattern for the research domain. The decisive
**storage divergence**: compoctopus's KG persistence is **stubbed (in-memory + NotImplementedError)**,
whereas observatory does **real CartON reads/writes** via `carton_mcp` + a `/tmp/heaven_data/observatory`
file layer. **LLM-wise they are the same engine** — heaven-framework Hermes/SDNA agents, MiniMax models,
agent-loop shape, zero direct LLM-client calls in either repo's source.

### Not-full-read / flagged
- compoctopus: `heaven_patch/baseheavenagent.py` (the LLM-exec patch), `octohead.py`/`auto_daemon.py`
  internals, `agents/ralph/core.py` body — characterized from signatures/greps, not full-read.
- observatory: `grug_agent.py`/`grug_server.py` (the experiment-runner's own LLM calls), `mcp_server.py`
  body — not full-read.
- Both: the ultimate **provider envelope** (which HTTP client the heaven `HermesConfig` uses to reach
  MiniMax) lives in the heaven-framework dependency, outside these repos — UNCLEAR from here.

---

# D. heaven-bml — the ORIGINAL GitHub version (separate task; included here)

**Located (IS):** the ORIGINAL is the GitHub repo **`sancovp/heaven-bml`** ("HEAVEN BML System —
Build-Measure-Learn GitHub project management for AI agents", `gh repo view`, pushed 2025-07-26).
Local clone read: `/home/GOD/tmp/heaven-bml-public` (git remote = github.com/sancovp/heaven-bml,
tag `public-1.4.0`, 2025-07-08). Also pip-installed: **`heaven-bml` v2.6.1** (site-packages). This is a
DIFFERENT system from `/home/GOD/heaven_bml_sqlite/` (the later "treekanban" SQLite rewrite).

**What it IS:** a Build-Measure-Learn **kanban project manager whose entire datastore is GitHub itself** —
GitHub Issues + Labels (+ GitHub Actions). No database, no server. For AI agents to manage work in a repo.

## D.1 STORAGE — where state lives (IS)
- **GitHub Issues + Labels ARE the store** — there is NO DB/file store. (`heaven_bml/github_kanban.py`.)
  - **Status** = a `status-<state>` label; the 7 BML columns = `backlog → plan → build → measure → learn
    → archived` + `blocked` (`github_kanban.py:22-40`, `KanbanBoard` dataclass + `VALID_TRANSITIONS`
    state machine).
  - **Priority** = a `priority-<tree>` label in **TREE NOTATION** — `priority-1.2.3.4.5…` = infinite
    hierarchy, natural-sorted (`tree_kanban.py:parse_tree_priority/get_issue_priority`). This is the
    signature feature: arbitrary-depth ordered priorities encoded in labels.
  - **Data model:** `Issue(number,title,state,labels,assignees,url)` + `KanbanBoard(backlog,plan,build,
    measure,learn,blocked,archived)`.
- **All reads/writes via the `gh` CLI** (subprocess): `gh issue list --json …` (`github_kanban.py:42-63`),
  `gh issue create`, label edits → real-time GitHub sync.
- **GitHub Actions workflows** installed into the target repo via `setup_scripts/install_bml_workflows.py`
  (`python -m heaven_bml.setup_scripts.install_bml_workflows --repo org/repo`) = CI-side BML automation.
- Requires `GITHUB_TOKEN`; the board is the repo's Issues tab (shareable, PR-linkable).

## D.2 SURFACE / FEATURE SET (IS)
- Python API (`heaven_bml/`): `construct_kanban_from_labels(repo)`, `get_all_prioritized_issues`,
  `move_issue_above/below(issue, target, repo)`, `create_github_issue_with_status(repo, title, body,
  status)` (README + `github_kanban.py`/`tree_kanban.py`).
- **MCP server** (`mcp_server/server.py`, `python -m mcp_server --default-repo org/repo`) for Claude Code.
- `agent_wrappers.py` = agent-integration wrappers.

## D.3 What the SQLite rewrite likely DROPPED (mark UNCLEAR — inference)
The original is **GitHub-native**: the board lives in GitHub Issues/Labels, syncs in real time, is visible
in the GitHub UI, links to PRs, and ships **GitHub Actions** workflow automation. The SQLite rewrite
(`heaven_bml_sqlite`, "treekanban") moves the board into a **local SQLite DB** — gaining offline/speed/no-
token, but (by store-type) **losing the GitHub-as-shared-surface, the Issues/PR linkage, and the Actions
CI automation**. *(IS: the original's GitHub store + Actions. UNCLEAR: exact sqlite-version feature delta —
I did not full-read `heaven_bml_sqlite` this task; the "dropped" list is inferred from the store change and
should be confirmed against that repo.)*

---

# E. largechain (LARGE CHAIN)

**Located (IS):** on the box at **`/home/GOD/large-chain`** (github **`sancovp/largechain`**, "Transform
any function into conversational AI that improves itself… every pip install downloads an AI scientist",
pushed 2025-07-02). NOT in the monorepo (canonical-source-dirs lists it HOST-ONLY; it is also present
here). **Accessible — read.** Backronym (README): "Language Automating Recursive Genetic Evolution
Chaining Hierarchies through AI Networks."

**What it IS:** a heaven-framework toolkit to **turn any Python function into a self-improving
conversational AI agent** (`make_function_agentic`) and **package + publish it to PyPI**
(`make_function_agentic_and_publish_to_pypi`). **Stage = DESIGN + prototype**, not a built product:
the repo is **25 design `.md` docs + 8 `.py`** (2 top-level scripts + 6 `wip_plan/` prototypes). Despite
the README's `pip install large-chain` + `from large_chain import make_function_agentic`, there is **no
`large_chain/` package in the repo** — only standalone scripts and `wip_plan/make_function_agentic_v2.py`.
So it is **product-SHAPED (a pip library/framework) but NOT product-BUILT** → architecture only, not a row
in the publishable-systems table (could become one if the package is actually built+published).

## E.1 STORAGE — where state lives (IS)
- **No DB. No CartON/neo4j/chroma/sqlite.** Persistence = **generated Python package files written to
  disk** then **published to PyPI**.
  - `make_function_agentic_and_publish_to_pypi(...)` writes the generated library into `work_dir =
    Path(output_dir)` (default `/tmp/test_pypi_package`, `make_function_agentic_and_publish_to_pypi.py:76`;
    `pypi_docs_writer_agent.py:165`) — setup.py/README/the agentic lib module.
  - **PyPI is the "store"/distribution target**: `PackageAndPublishPypiTool`
    (`pypi_docs_writer_agent.py:17`) + twine; token from `pypi_api_key` param or `PYPI_API_KEY` env
    (`make_function_agentic_and_publish_to_pypi.py:62-67`).
  - The *temporary* `make_function_agentic` produces an **in-memory `AgenticFunction`** (no disk) — the
    publish pipeline is the persistent variant.
- Bottom line: largechain's "storage" is **filesystem-staged package artifacts → PyPI** (a publishing
  pipeline), not a knowledge store.

## E.2 LLM CALLS — where / how / from where / what types (IS)
- **How (client/lib):** the **heaven framework** — `BaseHeavenAgent` + `HeavenAgentConfig` +
  `UnifiedChat` + `ProviderEnum` (`computer_use_demo.tools.base...`), and `hermes_step` from `heaven_base`
  (`make_function_agentic_and_publish_to_pypi.py:22,330-331`; `pypi_docs_writer_agent.py:12-13`). Same
  heaven substrate as compoctopus/observatory — but here the call is `BaseHeavenAgent(config, UnifiedChat(),
  ...)` / `hermes_step(...)`.
- **What types (models / provider):** **OpenAI** — `ProviderEnum.OPENAI`, **`model="gpt-4.1"`**
  (`pypi_docs_writer_agent.py:60-61`) for the PyPI-docs agent, and **`model="gpt-4o-mini"`** ×3
  (`make_function_agentic_and_publish_to_pypi.py:350-371`: a `chat_config` / `check_config` / `fill_config`
  trio — the chat→check→fill loop that turns a function into conversational AI). **Note: this is OpenAI GPT,
  NOT the MiniMax that compoctopus/observatory default to** — a different provider on the same heaven engine.
- **Call sites / from where:** `create_pypi_publishing_agent()` (`pypi_docs_writer_agent.py:20-67`) →
  `publish_function_to_pypi()` (`:70`); and `make_function_agentic_and_publish_to_pypi()` (`:25`) →
  `_call_pypi_publishing_agent_via_hermes` → `hermes_step(...)` (`:252`). The core function-wrapping LLM
  loop lives in `wip_plan/make_function_agentic_v2.py` (the chat/check/fill configs).
- **Call shape:** **agent-loop** (heaven `BaseHeavenAgent` / `hermes_step` multi-turn), with a
  chat→check→fill structured-refinement loop for generating the agentic wrapper + PyPI docs.
- **UNCLEAR:** `wip_plan/make_function_agentic_v2.py` body + `make_heaven_tool_from_docstring*` not
  full-read; same heaven provider-envelope caveat (the actual OpenAI HTTP client lives in heaven/UnifiedChat).

## E.3 Where it fits the patterns (IS)
Same **heaven-framework LLM engine** as compoctopus/observatory — but two divergences: (1) **provider =
OpenAI GPT (gpt-4.1 / gpt-4o-mini)**, not MiniMax; (2) its "storage"/output is **PyPI package artifacts**,
not CartON/neo4j. It belongs to the **publishing/distribution** theme alongside marketplace-publishing — but
its distribution target is **PyPI** (a function→pip-package compiler) rather than a Claude-Code plugin
marketplace. It is **design/prototype-stage**, so it is architecture-mapped here, not added to the
publishable-systems table.
