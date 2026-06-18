# Course Map — "Claude Code Course For GTM Engineers (100x Leverage in 3 Hours)"

**Video:** https://www.youtube.com/watch?v=zmZi70uM668
**Instructor:** Mitchell Keller (Lead Grow AI)
**Length:** 2h50m / ~35,248-word transcript (`zmZi70uM668_clean.txt`, 896 lines)
**Companion repo / funnel:** `leadgrow.ai/claudecode` (open-source CLIs, starter repo, signal data published free)
**This file:** the COMPLETE reverse-engineered curriculum spine — every module in order, the repeating beat pattern, the primitive/demo/funnel mapping, the progression arc, the recurring theses. Grounded in transcript line numbers (the `_clean.txt` lines, ~1 line ≈ a spoken paragraph).

---

## 0. How To Read This Map

The course is **not** evenly chaptered — it's a single continuous screen-share that ramps from "install Cursor" to "watch me one-shot a 19-stage cold-outbound campaign." I've cut it into **17 ordered modules** along the natural seams (where he changes topic, says "now let's get into…", or switches the on-screen artifact). Within each module I note the **primitive(s)** taught, the **demo/build** (if any), and the **funnel beat** (if any).

The whole thing is structured as a **value-ladder funnel disguised as a course** (see §Beat Pattern and §Funnel Arc): free knowledge → free companion repo/tools → free signal data → "book a call if you're a $15K-LTV B2B / PLG SaaS."

---

## 1. THE ORDERED MODULE LIST (the curriculum spine)

> Every distinct segment, top to bottom, in the order he teaches it. Title + 1-3 sentence description. (Lines are `_clean.txt` references.)

### M0 — Cold-Open Thesis & Course Promise *(lines 1-5)*
The hook: "$100K+ on AI in 16 months; Launch Club record revenue 10 months straight; Foundation $512K+; two businesses acquired." Core claim: winners "haven't escaped better prompts — they've escaped the copy-paste/context-switching loop entirely" by running ONE compounding system. Promises the arc: setup → durable work → build your own integrations/skills → build a live GTM signal together → chain it into a real campaign → close with full GTM-OS structure + advanced tips. Plugs the companion repo ("everything is ready to use — just point Claude Code at it and clone it").

### M1 — Setup: Cursor + Claude Code + Models *(lines 11-30)*
Install **Cursor** as the *interface* (so you can SEE files/docs, not a bare terminal). `npm install` **Claude Code**, init with your own subscription. **DeepSeek stack** as a cost escape hatch ("30 to 100x cheaper," V4 Pro models) once usage bottlenecks. **Voice commands** to switch models ("use DeepSeek", "use Sonnet", "claude yolo" = `--dangerously-skip-permissions`). Recurring meta-claim introduced: *"almost everything can be done by Claude for you if you give it a link to context, a screenshot, and a reasonable explanation."*

### M2 — GitHub as Source of Truth + Git-as-Control *(lines 31-68)*
**GitHub CLI** synced into Claude Code. Git reframed as **"a video game / a time machine / a save-scum system"** — checkpoints so you can always revert (esp. after a YOLO mistake). The four areas: remote → clone → local → workspace; `add`(stage) → commit(local) → push(remote = multiplayer) → fetch/pull. **Issues = task handoffs** between teammates ("Claude, create an issue for Jessica") AND the bridge to autonomous agents. **Projects = a Kanban board / campaign manifest.** Money line: *"without version control you just have a bunch of toddlers with rocket launchers."*

### M3 — Mono-Repo Structure + `.env` / API Keys *(lines 69-92)*
Set up as a **mono-repo**: a parent repo that `.gitignore`s everything *except* grouped folders (CLIs, integrations), each its **own** versioned repo with its **own** CLAUDE.md and feedback loop — so systems never pollute each other ("messy feedback loop"). Create `.claude/`, run `/init`, add `.env` for API keys. First tools to add: **Fireflies** (meeting recorder) + the **session-log review tool**. Teaches what an **API key / endpoint** is in plain language; the **F12 / "map endpoints behind the scenes"** trick for tools without an API (with a not-legal-advice disclaimer; the Clay CLI was built this way).

### M4 — The Layers & "Everything Gets Replaced" *(lines 93-110)*
The conceptual spine: **terminal → files (Markdown) → agents (use tools) → output layer (code/content/campaigns/CSVs)**. "Most things get replaced" — one interface replaces note-apps, PM tools, the copy-paste analyst. **Context becomes the moat — "context is just your unique taste in the world."** Taste is programmed into: **CLAUDE.md** (who Claude is for you), **skills** (what Claude can do), **rules** (heuristics), and referenced files (voice/ICP/campaigns). Introduces **arguments** (a short token that expands to lots of context elsewhere). The master pattern: **every system exists to SAVE context** — load only the bit needed until it needs to go deeper (progressive disclosure). Ends with a **pre-flight checklist** (you should have all of this set up now).

### M5 — CLAUDE.md (the Business Brain) + Rules *(lines 111-129)*
**CLAUDE.md** = "the business brain," kept **LEAN** ("literally the shorter the better"). Use **Karpathy's 4 rules** + a **workspace map** (your OS/runtime/languages); steal his CLAUDE.md verbatim + **"caveman mode"** to save tokens. **Only add to it when you hit consistent issues found via session-log review** (the feedback loop). **His 6 standing rules:** (1) give clickable full file paths; (2) everything has a place (temp vs not); (3) tell me what you're thinking THEN default to action; (4) **never delete, only archive**. Closes on the **daily rhythm** — run GTM through GitHub issues as the "what to do next" source of truth, which is also the on-ramp to autonomous agents (Hermes / OpenClaw).

### M6 — Skills: Anatomy & Authoring *(lines 130-144, 213-214)*
**A skill = "a prompt with front matter" = one SOP.** Front matter (name, model, description, tools) is what the AI reads *before* entering — must carry **trigger words** ("write outbound copy", "build sequences") so plain language invokes it; `model sonnet` in front matter picks the sub-agent model. Body = a **workflow** + **quality gates** + **anti-patterns** (with examples). **Best way to build a complex/unique skill: record yourself doing the task, narrate step-by-step, feed the recording** (this is *why* the first build is the transcript fetcher). **Skill chaining:** output of skill 1 is pre-curated to be the input of skill 2; point new skills at **GSD** (Get-Stuff-Done plugin) so they're built with UX in mind (use the `ask_user_question` tool).

### M7 — MCPs vs CLIs (the load-bearing choice) *(lines 145-182)*
**MCP = "out-of-the-box toolkits / training wheels / a USB port for your AI."** Fatal flaw: **MCPs flood ALL their tools into the model ALL the time → context rot → mistakes.** (Signature analogy: MCP is *"Omni-Man grilling Mark on the stairs in Invincible"* — life lessons you didn't ask for.) **CLI = your own custom command-line interface**, invoked only when needed, run via code (which is *why coding agents are uniquely valuable*). For small businesses (not SOC2/enterprise) **you almost always want a CLI, not an MCP.** The integration element is what makes Claude Code useful for GTM — without it it's "just an analyst that picks apart a CSV." Live aside: shows real skill front matter (Reddit-find list-builder) and critiques it as a "weak skill"; demonstrates the **handoff → `/clear` → resume** workflow (clear context above ~80% or the model gets confused like an overloaded MCP).

### M8 — Arguments + Hooks (deep) *(lines 183-214)*
Re-teaches the **context architecture** (skills / context / file system → organized into projects: a building repo, a company-info repo, projects+integrations, client work). **Control over context = no cross-system pollution** (sales copy never bleeds into marketing copy). **Arguments unite separated systems on demand** — `company-pain-points`, `bison-api-key` (named env vars Claude *can't see*, esp. with a hook). **Hooks = code injected before/after a tool use → deterministic, UNBREAKABLE** (unlike rules, which are just words to the LLM). Uses: **protect `.env`** (block reads of keys), ping Slack / play a 16-bit sound on completion, trigger cron jobs. **The first hook to set up: a sound ping when a task finishes/needs you.**

### M9 — Agents / Sub-Agents (the org chart) *(lines 215-247, 341-358)*
**An agent = an org chart inside Claude.** Orchestrator (big model, Opus) spawns specialist **sub-agents in parallel, each with its OWN context window (~29-30K)** so the orchestrator's window stays clean on the goal/vision. **Controls spend** (weak model — Haiku / DeepSeek flash — for search & deterministic tool runs; **Sonnet 4.5 for writing**). His advice: **mostly ignore agents, focus on skills** — just keep a **codebase-searcher** agent and a **writing** agent. Re-teaches **CLAUDE.md resolution** (uses the *closest* one walking up to the top). Live: spawns 3 sub-agents for a final check (shows the 3 independent windows).

### M10 — LIVE BUILD #1: Fireflies Transcript-Fetcher Skill → Sales-Coach *(lines 248-450)*
The first hands-on build, in **explanatory mode** + caveman-off. Grab the **Fireflies GraphQL API docs** ("copy page as markdown" / screenshots are your best friend). Architect in plain language → a **mermaid diagram**. Make it a **multi-vector skill**: classify each call as **internal-team / sales / content**, route to the right reference files (content always runs; the other two optional). Sales path becomes a **Hermozi-style sales coach** — fetches Alex Hormozi YouTube transcripts (via the YouTube-fetch skill, sub-agent per video), builds reference files with **Hormozi example + B2B equivalent + anti-patterns (Matt Pacock skill)**, plus an **SQLite memory** to cross-reference discovery↔proposal calls. Uses the **`grill me` skill** (let the model prompt YOU) to close plan gaps, then **anneals the skill** over ~12 iterations against a real (anonymized) call (scored himself 3.5/10). Proves: skill creation = feed raw inputs → distill around relevant areas → version it → run on a loop / graduate to managed agents / Trigger.dev / n8n.

### M11 — LIVE BUILD #2: The Apify CLI (fork "CLI-anything") *(lines 451-541)*
Build your **own tool integration** from scratch. **MCP = a USB port; a CLI is the same thing run via code.** Method: check if the tool has a CLI or MCP → if MCP-only, **map the endpoints off it** → use the open-source **"CLI-anything"** repo (`leadgrow.ai/claudecode`) as the build path → feed API docs (markdown/screenshots) → architect in plain language → **wrap actors/endpoints as skills**. Forks the existing **Apify** CLI (because a generic CLI doesn't wrap tools the way *you* use them); strips actor-building, keeps **run/monitor/get-data**; wraps the **LinkedIn-hiring-data actor** and **LinkedIn-ad-library scraper** as distinct skills (signal vs enrichment pathways). Mentions the **Vercel agent browser** (better than Claude-for-Chrome) and a **"Nexus"** (a web of all your systems so an agent can suggest the next one to build). Result: live LinkedIn Boolean search, ~199 jobs → 150 deduped companies → pushed to **Supabase** + a **Google Sheet** for visibility. Recaps the full 7-8-prompt integration process.

### M12 — The Karpathy Auto-Research Loop (the highest-leverage system) *(lines 542-563)*
**"Without the feedback loop it's just a tool; with feedback loops it's a system."** Karpathy's loop: pick **ONE data point** → create a **ground truth** → AI spawns split-test **challengers** vs the current winner → compete to beat the benchmark → keep/revert → run **5-10 self-improving passes ("anneal")**, each documented as a git version for rollback. **The critical caveat everyone misses:** the loop was built for *algorithmic/research* problems — **you must bend it to GTM by injecting your taste + rules:** a clear **goal** anchored to ONE bastion of truth (e.g. deliverability), **rules on what beats a challenger** (≥20% better, because deliverability decays), a **time horizon** matched to feedback speed (loop per 500-1000 sends, not 5 min), **guardrails/human-controlled variables** (offer/CTA fixed — "you can't just say I'll give you a million dollars"), and a **trigger** (only loop when the winner trends down — "fingerprinting," like ads going stale). Where to apply: reply rate, click-through/conversion (homepage = ground truth), ad copy (hold creative, vary copy per value-prop). Mentions **"auto-context"** as a separate loop he doesn't use.

### M13 — LIVE BUILD #3: Product-Hunt GTM Signal Scraper (the loop applied) *(lines 564-590, 619-634)*
Builds a real GTM signal using the **auto-research-process-builder** (`leadgrow.ai/cloudcode`). Scrapes **Product Hunt** daily leaderboard (UTM-param paging logic) + a second company-info page; sends an **Opus** sub-agent to build a **ground truth** for launches *not* on PH (news/TechCrunch); **classifies new-product vs new-feature vs is-AI**; anneals the discovery prompt against ground truth toward **>90% accuracy** (DeepSeek shown driving it: direct page-scrape hit 100% recall vs 25% for SERP-only → hybrid architecture). Then a **quality gate** for the last 10%, **upsert to Supabase** (28-table schema, "double-check destructive SQL with a blank-context model"), **deploy on Trigger.dev** as a daily cron (~$2/month for ~60 launches/day), and **publish free on the website.**

### M14 — When to Automate vs Agentic vs Run-Yourself (the deployment ladder) *(lines 591-619, 654-670)*
The graduation hierarchy. **Agent = AI + skill + tools + ability to improve itself** — for workflows needing **decision-making that's different each time** (the "red-alert cold-email campaign" example: ~100 branching considerations — other campaigns' health, bounce vs deliverability, Outlook vs Google, which inboxes still deliver — *"a freaking nightmare in n8n"*). **Automation = a Merkle tree of if-then logic** (deterministic; n8n excels at scale/volume). **Agentic automation** = LLM calls a tool, becomes deterministic again (hard to build well). **The ladder:** (1) run **in Claude Code** (you control it); (2) graduate to the **cloud — Trigger.dev** (chosen over n8n: deploys directly from Claude Code via its CLI, fully malleable, durability/retriability/observability out of the box); (3) **cloud-managed agents** (on-the-fly access to more knowledge — past clients, DBs); (4) **Hermes agent** — a dedicated autonomous agent on a cron with a **self-improving harness built in** (like the Karpathy loop), spawns its own sub-agents, orchestrates an org chart from Slack, any model, 24/7 "AI co-worker" (OpenClaw an alternative). Teaches the **`/goal` (Ralph loop)** feature: give AI a goal + budget, it runs many turns until done; with 1M context + sub-agents *"could run for like 10 hours."* (Used later to attempt one-shotting the campaign — shown failing and being course-corrected.)

### M15 — LIVE BUILD #4 (the capstone): GTM Orchestrator + Permissionless-Value Campaign *(lines 671-755, 695-756)*
The real multi-segment cold-outbound campaign, end-to-end. Credits **Eric Noasoski** (~50% of the orchestrator's skills are adapted from his cold-outbound skills) and **Jordan Crawford** (permissionless-value / "Cannonball" 11-step research). **Campaign logic = "a mini-campaign for every single prospect":** detect **signals** (funding, new-leadership-hires-last-90-days, actively-hiring-for-leadership, product launches, SEC/govt records, G2 reviews — built overnight by a **Hermes** agent as per-signal scrapers, segment-scored); craft a **PVP email** ("3 company types just hired a CRO this week — here are the decision-makers + the sequencing we'd run") with **full decision-maker cards** upfront (contact info broken up so no links trigger spam); the hard part is the **matching logic** — match each prospect to signal-companies where target-market overlaps → top 3 by fit score → pull contacts → generate 3 PVP emails. Uses **`/goal`** to attempt a one-shot (fails, gets stopped, course-corrected via handoff + mermaid + an HTML diagram + switch to **Opus** with max sub-agents). Result: **~2,953 prospects → tripled matches via Discolike prospect-expansion → 618 qualified leads at 70% email-hit.**

### M16 — The GTM-OS Architecture: 19 Stages, State Model, Multiplayer *(lines 756-831)*
The full anatomy of the orchestrator (a **Lead Grow plugin** = hooks + skills + tools, git-versioned, transferable). **The 19-stage pipeline:** discover → Clay format → Clay enrich (via a **Cloudflare "fire-and-wait" worker that turns Clay into an API** — fire to webhook, wait, pull back via callback URL into Supabase) → qualify ICP (auto-context + auto-research loops) → enrichments (through **Trigger.dev** for concurrency/durability — "hundreds of thousands of processes for ~$12/month") → find-people waterfall (AI Arc → custom agents) → email waterfall (MillionVerifier, Kit, ICPs, Lead Magic) → MX pre-filter → segment → apply copy → personalize (1:1 AI copy — "a real AI SDR, not a template") → QA-check → launch (create campaigns, upload copy, select inboxes, route leads) into **Bison**. **The state model:** **Git = Kanban + a "manifest doc"** (lets you replay the whole build on a dashboard); **Supabase/Postgres = the source of truth for DATA** ("campaign data in just git will completely implode"; every LLM output must write to a table; Google Sheets too fragile/unscalable); **SQLite = a local mirror**. Watchwords: **observability, durability (resumes after failure), stateful (pauses & remembers)**. **Skill-chaining gated by hooks** (a pre-check between stages 2→3 blocks a list missing core context). **28 skills** across categories. Funnel beat: the explicit **"book a call"** pitch (B2B w/ 25K+ company market & $15K+ LTV, or PLG SaaS) lands here.

### M17 — Advanced: Plugins/Marketplaces, Security, the Knowledge Graph *(lines 832-896)*
The advanced close. **Automation-recommender** (`/claude` setup plugin) scans your whole codebase and recommends changes (but over-recommends MCPs — ignore those, it doesn't detect CLIs). **Plugins = packages of skills/agents/hooks installable in one line = the path to multiplayer.** **Marketplaces = "Costco for skills"** — version-controlled, **permissioned** skill sets (per-department visibility); Claude's official marketplace = **174 plugins** (he runs 3). **Security:** hooks to protect `.env` PLUS a **hard deny in `settings.json`** on any direct env-var access ("Claude, implement a hard deny — it'll build it in one shot"); at team scale run env vars through a password manager and LLM calls through a **gateway** (LiteLLM / OpenRouter) for rate limits + observability (**Langfuse** to diagnose where context injection goes wrong). **The Knowledge/Context Graph** (he calls it *"probably the most important thing in the whole video"*): recommends **Jacob Deal's `context-os`** (`github.com/jacob-dedle/contextos`) — a knowledge graph that updates over time, maintained by agents. **Why a graph beats grep:** a prompt fed by *specific knowledge nodes* gives **traceable** output (you know exactly what produced it) vs the model "shaking it all around" into a question-mark output; **direct pathways between related contexts** (ICP → persona) so agents navigate straight there instead of fanning out grep-searches that "burn tokens and fill context with garbage." **Layers of context:** concrete (your business) / emergent (a campaign result still being tested) / research-driven (unverified). The **gardening metaphor** — plant good context, trace & pull the "weeds" of bad info before they spread, without pesticide-spraying everything. Closes on *"Claude Code blew up not because of the best model but because of the best HARNESS,"* and a final bonus: a **Richard Feynman explainer skill** (skill = "armed context window that persists across all the skills it uses").

---

## 2. THE PER-SECTION STRUCTURE (the named beat pattern)

His sections are **NOT** a rigid identical template — but there IS a dominant repeating beat, especially in the conceptual modules (M4-M9, M12, M14, M17). I'll name it:

### **The "PRIMITIVE → PLAIN-WORD ANALOGY → HOW I USE IT → THE BENEFIT (→ the funnel nudge)" beat.**

Almost every concept lands in this order:

1. **Name the primitive** in jargon, then immediately disclaim the jargon ("this is just a lot of jargon, so let's be super clear").
2. **Re-explain it with a vivid everyday analogy** (MCP = Omni-Man grilling Mark; Git = a video game / time machine / my wife remembering everything; sub-agents = an org chart; context-graph = gardening; argument = a movie one-liner / Fight Club description).
3. **"Here's how I actually do it in my system"** — cuts to the real Lead Grow artifact on screen (a real skill's front matter, the GTM orchestrator, a real campaign).
4. **State the benefit / the underlying thesis** it serves — almost always *"to SAVE context"* / *"context is the moat"* / *"that's the feedback loop."*
5. **(Often) a funnel nudge** — "you'll find this in the companion repo," "it's free on the website," "Eric/Jordan/Jacob built X, check them out," or the "book a call" beat.

The **live-build modules (M10, M11, M13, M15)** follow a different, also-repeating beat:

### **The "DOCS → PLAIN-LANGUAGE ARCHITECTURE → MERMAID DIAGRAM → GRILL-ME/PLAN-MODE → ANNEAL → VERSION/DEPLOY" build beat.**

Every live build runs: **grab the API docs (markdown/screenshots)** → **architect out loud in plain language** → **make a mermaid diagram to confirm chaining** → **plan-mode + `grill me` (let the model prompt you)** → **execute (often via cheap model/sub-agents), verify between executions** → **anneal against a ground truth / iterate** → **version in git + deploy (loop / Trigger.dev / plugin).** He repeats "spend 80% of your time planning" and "always verify between executions; never go fully buck-wild."

### Two sections rendered in the dominant (concept) beat

**M7 — MCPs vs CLIs:**
- *Primitive:* "All an MCP is is a way for AI to use something… a USB port for your AI."
- *Analogy:* "MCP is Omni-Man grilling Mark on the stairs in Invincible — life lessons you didn't ask for" → context rot.
- *How I do it:* "If you look at the companion, there's almost no MCP servers… you're almost always going to want to use a CLI" (`leadgrow.ai/cloudcode`, open-source).
- *Benefit/thesis:* CLIs load only what's needed → save context → "the integration element is what makes Claude Code useful for GTM."
- *Funnel nudge:* the free CLI-anything repo on the website.

**M8 — Hooks:**
- *Primitive:* "A hook lets you inject a prompt/words/tokens before or after a tool use."
- *Analogy/contrast:* "Unlike rules, which are just words to an LLM, these are code — they can't be broken."
- *How I do it:* protect `.env`, ping Slack / play a Pokémon-heal sound on completion, fire a cron job.
- *Benefit/thesis:* deterministic & unbreakable; "the first hook to set up is a sound ping when a task finishes."
- *Funnel nudge:* "use the cloud-code-setup skill to make your own hooks."

### One section rendered in the build beat

**M13 — Product-Hunt signal scraper:**
- *Docs:* Product Hunt leaderboard + UTM paging + second company-info page.
- *Architecture (plain language):* scrape PH daily + Opus ground-truth for non-PH launches + classify product/feature/is-AI.
- *Mermaid/diagram:* implied; he flags steps to add (comparative analysis, AI-flag column).
- *Grill-me/plan-mode:* "make sure we use GSD in the planning process."
- *Anneal:* DeepSeek drives 5-10 passes vs ground truth → hybrid scrape+SERP → >90% accuracy → quality gate for last 10%.
- *Version/deploy:* upsert Supabase → Trigger.dev daily cron (~$2/mo) → publish free on website.

---

## 3. CLAUDE CODE PRIMITIVES — COVERAGE MAP

| Primitive | Where covered | One-line teaching |
|---|---|---|
| **Cursor (interface)** | M1 | The IDE so you can SEE files/docs, not a bare terminal. |
| **Claude Code install / models / voice cmds** | M1 | `npm install`; voice-switch models; "claude yolo" = `--dangerously-skip-permissions`. |
| **DeepSeek stack** | M1, M11 (used), M13 (used) | Cost escape hatch, "30-100x cheaper"; use for deterministic/cheap work. |
| **Git / GitHub / GH CLI** | M2 | Source of truth, save-scum/time-machine; issues = handoffs; projects = Kanban. |
| **Mono-repo + `.gitignore`** | M3 | Parent repo, each system its own versioned repo + own CLAUDE.md → no pollution. |
| **`.env` / API keys / endpoints** | M3, M8 | Keys as named env vars; F12 endpoint-mapping trick for API-less tools. |
| **CLAUDE.md** | M4, M5, M9 | "Who Claude is for you," lean, Karpathy-verbatim + caveman mode; closest-one-wins resolution. |
| **Rules** | M4, M5 | Breakable heuristics; his 6 standing rules (paths, a-place-for-everything, think-then-act, never-delete-only-archive). |
| **Skills** | M4, M6, M10 (built), M17 | "A prompt with front matter" = one SOP; trigger words; record-yourself; workflow + quality gates + anti-patterns. |
| **Arguments** | M4, M8 | A short token expanding to lots of context elsewhere; unites separated systems; hides API keys. |
| **Hooks** | M8, M16 (gating), M17 (security) | Code injected before/after a tool → deterministic & unbreakable; protect `.env`, sounds, crons, stage-gates. |
| **Agents / sub-agents** | M9, M10 (used), M15 (used) | Org chart; parallel independent ~29-30K windows; spend control; "mostly ignore agents, focus on skills." |
| **MCPs** | M7, M17 | Out-of-the-box toolkits / training wheels; flood context → rot; use sparingly (Supabase MCP an OK starting case). |
| **CLIs (vs MCPs)** | M7, M11 (built) | Your own command line; loaded only when needed; "almost always want a CLI." |
| **Plugins** | M6 (mention), M16 (orchestrator IS one), M17 | Packages of skills/agents/hooks, one-line install; path to multiplayer. |
| **Marketplaces** | M17 | "Costco for skills"; version-controlled, permissioned (per-department); official = 174 plugins. |
| **`/goal` (Ralph loop)** | M14, M15 (used) | Goal + budget → many autonomous turns; with 1M ctx + sub-agents could run ~10h. |
| **`settings.json` hard-deny** | M17 | Security: hard-deny direct env-var access ("it'll build it in one shot"). |
| **Explanatory mode / caveman / `/clear` / handoff** | M7, M10 | Learning aids + context hygiene (clear above ~80%; handoff to resume). |
| **GSD / Matt Pacock / grill-me skills (3rd-party)** | M6, M10, M16, M17 | GSD = UX-aware workflow builder; grill-me = "let the model prompt you"; Pacock = skill-library/anti-patterns. |

---

## 4. THE DEMOS / LIVE BUILDS

| # | Module | What he builds/demos | Tools used | What it PROVES |
|---|---|---|---|---|
| D1 | M9 | Spawns 3 parallel sub-agents for a final check | Claude Code agents | Independent ~29-30K windows keep the orchestrator's context clean. |
| D2 | M10 | **Fireflies transcript-fetcher → Hormozi sales-coach skill** | Fireflies GraphQL, YouTube-fetch skill, SQLite, grill-me, GSD, Matt Pacock | Skill creation = feed raw inputs → distill → version → anneal; recording-yourself + expert-cloning method; let-the-model-prompt-you. |
| D3 | M11 | **Apify CLI** (fork of "CLI-anything") wrapping LinkedIn-hiring + ad-library actors | CLI-anything repo, Apify API, Vercel agent browser, Supabase, Google Sheets, DeepSeek | You can build a custom integration for ANY tool with an API in ~7-8 prompts; actors-as-skills; signal vs enrichment pathways. |
| D4 | M13 | **Product-Hunt GTM signal scraper** | Product Hunt, SERP/Google, Opus (ground truth), DeepSeek (anneal), Supabase, Trigger.dev cron | The Karpathy loop applied to GTM: ground truth → challengers → anneal to >90% → quality gate → cheap cloud cron → free public data. |
| D5 | M15-16 | **GTM Orchestrator + permissionless-value campaign** (capstone) | Apify, Disco­like, Clay (+ Cloudflare fire-and-wait), Supabase, Trigger.dev, AI Arc, MillionVerifier/Kit/Lead Magic, Bison, `/goal`, Opus + sub-agents | A real multi-segment "mini-campaign-per-prospect" runs end-to-end; 2,953 prospects → 618 qualified leads @ 70% hit; git+Supabase state model; plugin = multiplayer. |
| D6 | M14/M15 | **`/goal` one-shot attempt (shown FAILING)** | `/goal` Ralph loop | A deliberately-shown realistic failure: complex campaigns can't be one-shot; you stop, course-correct, hand off. |
| D7 | M17 | **Automation-recommender scan** + **Feynman explainer skill** (bonus) | `/claude` setup plugin; a custom skill | Codebase-aware recommendations (ignore the MCP ones); skills can encode an expert's *style*, not just a task. |

Background demos he flashes (not full builds): bulk **lead-magnet generation** for a client, a **YouTube video edited with whiteboard illustrations inside the terminal**, government-data → company-domains → lead-lists pipelines running in parallel shells (M10, lines 321-325).

---

## 5. THE PROGRESSION ARC (beginner → advanced + the funnel beats)

**Ramp shape (mechanism complexity climbs the whole time):**

```
SETUP            PRIMITIVES              HIS SYSTEM (live)        THE BIG BUILD            ADVANCED / SCALE
M1-M3            M4-M9                   M10-M13                  M14-M16                  M17
Cursor+CC+Git    CLAUDE.md, skills,      build a skill,          deployment ladder,       plugins/marketplaces,
+mono-repo+env   rules, hooks, args,     build a CLI, the        the 19-stage GTM-OS,     security, the knowledge
                 agents, MCP-vs-CLI      Karpathy loop, a        the PVP campaign         graph (context-os)
                                         signal scraper
"complete        "the architecture"      "watch me prompt        "watch me ship a         "go multiplayer +
 beginner"                                in real time"           real campaign"            make outputs traceable"
```

**The funnel beats inside the course (the value ladder, AIDA-fractal):**

- **Attention/Interest (M0):** the $100K / $512K / acquired-businesses proof + "escape the loop" promise.
- **Free value #1 — the companion repo (M0, M1, M3, M7, M11):** "everything is ready to use — clone it"; the open-source **CLI-anything** repo + starter repo + baseline skills (`leadgrow.ai/cloudcode`). *(This is the lead magnet — Hormozi-style permissionless value, the same move he teaches in the campaign.)*
- **Free value #2 — free signal data (M13):** the Product-Hunt signal scraper's output published free on the site.
- **Authority borrowing (recurring):** credits **Karpathy** (godfather of AI), **Eric Noasoski** (cold-outbound skills), **Jordan Crawford** (PVP/Cannonball), **Jacob Deal** (context-os), **Hormozi** (sales frameworks), **Feynman** — positions himself inside a trusted lineage.
- **The CTA (M16, lines 831):** the one hard pitch — *"If you're a B2B business with a market of 25,000+ companies and a $15K+ LTV offer, or a PLG SaaS with a big market — book a call and we'll build out a big beautiful strategy."*
- **The upsell tease (M14, M15, M17):** **Hermes agent** ("I'll do an entirely separate video"), the **1:1 AI-copy SDR** ("a video coming out very shortly"), per-client **knowledge graphs shipped with every client** — the next products in the ladder.
- **The "don't just copy it" gate (M16, lines 757, 826):** "build it yourself or it's a black box you won't understand" — which simultaneously justifies the course AND the done-for-you service (the meta-funnel: the people who *won't* DIY are the ones who book the call).

---

## 6. TEACHING PHILOSOPHY / RECURRING THESES (and how they thread through)

| Thesis | Verbatim/near-verbatim | Threads through |
|---|---|---|
| **Escape the loop, run a system** | "winners… escaped the copy-paste/context-switching loop entirely… a system that compounds and works around them" | M0 framing → every module ("everything gets replaced," M4) → the GTM-OS (M16). |
| **Context is the moat** | "context is just your unique taste in the world" | M4 (definition) → arguments/CLAUDE.md/skills as taste-programming → M17 (the knowledge graph as the ultimate context store). |
| **Every system exists to SAVE context (progressive disclosure)** | "Claude Code only has so big of a brain… systems exist so it only gets the little bit it needs until it needs to go deeper" | M4 (the master pattern) → MCP-vs-CLI (M7) → sub-agents' separate windows (M9) → `/clear`/handoff (M7) → skills as "progressive disclosure" (M17, explicit). |
| **Tool vs system = the feedback loop** | "without the feedback loop it's just a tool; with feedback loops it's a system" | M5 (session-log loop improves CLAUDE.md) → M6 (annealing skills) → M12 (Karpathy loop) → M14 (agent = AI+skill+tools+ability to improve itself). |
| **CLIs over MCPs** | "you're almost always going to want a CLI, not an MCP" | M7 (thesis) → M11 (build one) → M17 (ignore the recommender's MCP suggestions). |
| **Let the model prompt YOU / plan 80%** | "a perfect plan creates a perfect output… spend 80% of your time planning"; the **grill-me** skill | M6, M10, M11, M15 — every build front-loads planning, mermaid diagrams, grill-me, verify-between-executions. |
| **Anneal everything against a ground truth** | "anneal, self-improving, getting better over time… one data point, one bastion of truth" | M6 (skills), M12 (the loop), M13 (signal scraper), M16 (spintax self-anneal). |
| **State: git + a database, never git alone** | "campaign data in just git will completely implode… every LLM output must go to a table" | M2 (git = Kanban/manifest) → M13 (Supabase upsert) → M16 (the full state model + observability/durability/stateful). |
| **Traceability via a knowledge graph (gardening)** | "you know exactly what produced this output… trace and pull the weeds" | M17 (the climax thesis); retro-justifies why skills/arguments/context-layers exist. |
| **The harness beats the model** | "Claude Code blew up not because of the best model but because of the best HARNESS" | M0 (implicit) → M17 (stated outright); the whole course is "build your harness." |
| **Multiplayer or you're cooked** | "if no one else can use it, you're cooked" | M2 (push = multiplayer) → M16 (plugin = transferable) → M17 (marketplaces + permissions). |
| **Control = leverage** | "without control you just have toddlers with rocket launchers" | M2 (git) → M9 (orchestrator validates against the goal) → M14 (run-local-first, graduate carefully). |

---

## 7. NOTABLE NUMBERS & CLAIMS (for modeling our own course)

- $100K+ on AI / 16 months; Foundation $512K+; Launch Club record revenue 10 months straight; 2 businesses acquired.
- DeepSeek runs Claude Code "30 to 100x cheaper."
- Sub-agent windows ~29-30K each, independent of orchestrator.
- PH signal scraper ~$2/month (~60 launches/day); Trigger.dev "hundreds of thousands of processes for ~$12/month."
- Official plugin marketplace = 174 plugins (he runs 3).
- Capstone campaign: 2,953 prospects → tripled via Discolike expansion → **618 qualified leads @ 70% email hit**.
- The orchestrator = **19 stages, 28 skills**, ~50% adapted from Eric Noasoski's cold-outbound skills.
- Target buyer: B2B w/ 25,000+ company TAM & $15K+ LTV, or PLG SaaS.
- "Spend 80% of your time planning."

---

## 8. THE COURSE SHAPE IN ONE PARAGRAPH (for our model)

A continuous, screen-shared, build-along course shaped as a **value-ladder funnel**: hook with proof → give away a companion repo + free CLIs + free signal data (permissionless value, the exact tactic he later teaches) → teach the primitives bottom-up, each via *primitive → folksy analogy → "here's how I do it" → "to save context"* → then **show, don't tell** with four escalating live builds (a skill → a CLI → a self-annealing signal → a full 19-stage campaign), each via *docs → plain-language architecture → mermaid → grill-me/plan → anneal → version/deploy* → ramp the deployment mechanism (Claude Code → Trigger.dev → managed agents → Hermes) → land the single hard CTA at the capstone → close on the advanced "your real moat is a traceable knowledge graph + a transferable plugin" thesis, teasing the next products (Hermes, 1:1 AI SDR, per-client knowledge graphs). Every thread returns to one drumbeat: **context is the moat; every system exists to save it; the feedback loop is what turns a tool into a system.**
