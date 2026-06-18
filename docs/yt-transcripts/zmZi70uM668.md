# Claude Code Course For GTM Engineers - 100x Leverage in 3 hours

**Video:** https://www.youtube.com/watch?v=zmZi70uM668
**Channel:** Mitchell Keller (Lead Grow AI)
**Published:** 2026-05-26
**Duration:** 2 hours 50 minutes
**Last updated:** 2026-06-04

---

## Summary

A full beginner-to-advanced course on running an entire go-to-market (GTM) operation from inside Claude Code, taught by Mitchell Keller (Lead Grow AI), who claims $100K+ spent on AI over 16 months helping Launch Club hit record revenue and Foundation generate $512K+. The core thesis: the operators winning in GTM right now aren't using better tools or better prompts — they've **escaped the copy-paste / context-switching loop entirely** by running a single durable system (Claude Code) that compounds and works *around* them. The course takes you from setup (Cursor + Claude Code + GitHub) through the Claude Code primitives (CLAUDE.md, skills, hooks, agents, sub-agents, plugins), the deliberate choice of **CLIs over MCPs** (to avoid context-flooding), building your own tool integrations live (Fireflies transcript fetcher, an Apify CLI fork), the **Karpathy auto-research loop** as a self-improving optimization engine, and culminates in a real multi-segment "permissionless-value" cold outbound campaign built end-to-end with a 19-stage GTM orchestrator backed by Supabase + Trigger.dev + Clay. The recurring meta-lesson: **context is the moat**, every system exists to *save context* (progressive disclosure), and the difference between a tool and a *system* is the feedback loop.

---

## The Core Worldview (why this matters)

- **The winning move is not better prompts — it's escaping the loop.** Operators lose to copy-paste and context-switching. One interface (Claude Code) that integrates everything replaces note-taking apps, project management, and the analyst-with-a-CSV workflow.
- **Everything gets replaced; context becomes the moat.** "Context is just your unique taste in the world." That taste gets programmed into CLAUDE.md (who Claude is for you), skills (what Claude can do), and rules (heuristics).
- **Every Claude Code primitive exists to SAVE context.** "Claude code only has so big of a brain." Systems load context *sequentially*, only the little bit needed until it needs to go deeper. (This is the same progressive-disclosure principle Isaac's system rests on.)
- **Tool vs. system:** "Without the feedback loop, it's just a tool; with feedback loops, it's a system." An agent = AI + skill + tools + the ability to improve itself.

---

## Layer 1 — Setup (the prerequisites)

1. **Cursor** as the interface (so you can SEE files/docs, not just a bare terminal).
2. **Claude Code** via npm install; initialize with your own subscription. Voice commands to switch models ("use DeepSeek", "use Sonnet", "claude yolo" = `--dangerously-skip-permissions`).
3. **DeepSeek stack** as a cost escape hatch — run Claude Code on DeepSeek V4 models, claimed "30 to 100x cheaper." Recommended once usage gets bottlenecked.
4. **GitHub + GitHub CLI** = the source of truth / "file system in the cloud" / save-scum system.
5. **`.env`** in `.claude/` for API keys; first tools to add: Fireflies (meeting recorder) + a session-log review tool.

### Git as control (the framing)
Git = "a video game / a time machine" — checkpoints so you can always revert. Four areas: remote repo → clone → local repo → workspace; `add` (stage) → commit (local) → push (remote = multiplayer) → fetch/pull. **Without version control, "you just have a bunch of toddlers with rocket launchers."** Git **issues** = task handoffs between team members (and the bridge to autonomous agents). Git **projects** = a Kanban board / campaign manifest.

### Mono-repo structure
A parent repo with everything `.gitignore`'d *except* grouped folders (CLIs, integrations), each of which is its **own** versioned repo with its own CLAUDE.md and feedback loop — so systems never pollute each other.

---

## Layer 2 — The Claude Code Primitives (the architecture)

| Primitive | What it is | Key teaching |
|-----------|-----------|--------------|
| **CLAUDE.md** | "Who Claude is for you" — the business brain | Keep it LEAN ("the shorter the better"). Stolen verbatim from Karpathy + "caveman mode" to save tokens. Each project/folder gets its own; Claude reads the *closest* one, walking up to the top if none. Only add to it when you hit consistent issues found via session-log review. |
| **Skills** | "A prompt with front matter" = one SOP | Front matter (name, model, description, tools) is what the AI reads *before* entering — must have **trigger words** ("write outbound copy", "build sequences") so plain language invokes it. Best way to build a complex/unique skill: **record yourself doing the task**, narrate step-by-step, feed the recording. Include a **workflow**, **quality gates**, and **anti-patterns**. |
| **Rules** | Heuristics (words to the LLM, breakable) | His 6 standing rules: give clickable file paths; everything has a place (temp vs. not); tell me what you're thinking THEN default to action; **never delete, only archive**. |
| **Hooks** | Code injected before/after a tool use (deterministic, *unbreakable*) | Unlike rules, hooks are code — "they can't be broken." Uses: protect `.env` (block reads of API keys), ping Slack/play a sound on task completion, trigger cron jobs. The one to set up first: a sound ping when a task finishes/needs you. |
| **Arguments** | A short reference token that expands to a lot of context elsewhere | E.g. `company-pain-points` or `bison-api-key` — lets you UNITE separated systems on demand and keeps Claude from ever leaking/seeing raw keys. |
| **Agents / Sub-agents** | An org chart inside Claude | Orchestrator (big model, Opus) spawns specialist sub-agents (search, write, check) **in parallel, each with its own context window** (~29-30K each) so the orchestrator's window stays clean on the goal. Controls **spend** (weak model for search/deterministic tool runs, Sonnet 4.5 for *writing*). His advice: mostly ignore agents, focus on skills; just keep a codebase-searcher and a writing agent. |
| **Plugins** | Packages of skills/agents/hooks in one installable box | Install in one line; the path to **multiplayer**. |
| **Marketplaces** | "Costco for skills" — version-controlled, permissioned skill sets | Per-department visibility/controls. Claude's official marketplace = 174 plugins. |

---

## Layer 3 — CLIs over MCPs (the load-bearing architectural choice)

- **An MCP is "a USB port for your AI"** — out-of-the-box toolkits ("training wheels"). The fatal flaw: **MCPs flood the model with ALL their tools, ALL the time** → context rot → mistakes. (Vivid analogy: MCP is "Omni-Man grilling Mark on the stairs in Invincible" — life lessons you didn't ask for.)
- **A CLI is your own custom command-line interface** — invoked only when needed, run via code (which is why coding agents are uniquely valuable). For small businesses (not SOC2/enterprise), **you almost always want a CLI, not an MCP.**
- **The integration element is what makes Claude Code useful for GTM** — without it, it's "just an analyst that picks apart a CSV."
- **Building one:** check if the tool has a CLI or MCP → if MCP only, map the endpoints off it → use the open-source **"CLI anything"** repo (leadgrow.ai/claudecode) as the build path → feed the API docs (copy page as markdown / screenshots — "screenshots are your best friend") → architect in plain language → wrap actors/endpoints as skills.

---

## Layer 4 — The Karpathy Auto-Research Loop (the most powerful GTM system)

> "Without the feedback loop, it's just a tool; with feedback loops, it's a system."

**The loop:** Pick **one data point** → create a **ground truth** to measure against → the AI spawns split-test **challengers** against the current winner → challengers compete to beat the benchmark → keep/revert → run 5-10 self-improving passes ("anneal"). Document each pass as a git version so you can roll back if it regresses.

**The critical caveat (the part everyone misses):** Karpathy's loop was built for *algorithmic/research* problems. For GTM you must **bend it to your needs and inject your taste + rules**:
- A clear **goal** (e.g. reply rate) anchored to ONE bastion of truth (e.g. deliverability).
- **Rules around what can beat a challenger** (e.g. must be ≥20% better, because deliverability decays naturally).
- A **time horizon** matched to feedback speed (a 5-minute loop won't work for cold email; loop every 500-1000 sends instead).
- **Guardrails / human-controlled variables** (the offer/CTA stays fixed; "you can't just say I'll give you a million dollars").
- A **trigger** (only loop when the winner starts trending down — "fingerprinting," like ads going stale).

**Where to apply it:** reply rate (cold email), click-through / conversion rate (landing page homepage = ground truth), ad copy (hold creative, vary copy per value-prop). Related: "auto-context" (a different loop, mentioned but not used by him).

**Demonstrated live:** a Product Hunt new-release **GTM signal scraper** — annealed a discovery prompt against a ground truth (Google search + SERP + Product Hunt), classified new-product vs. new-feature vs. is-AI, pushed to Supabase, deployed on Trigger.dev as a daily cron job (~$2/month for ~60 launches/day), published free on the website.

---

## Layer 5 — When to Automate vs. Agentic vs. Run Yourself (the deployment hierarchy)

- **Agent = AI + skill + tools + ability to improve itself.** For workflows needing **decision-making that's different each time** (e.g. diagnosing a "red alert" cold-email campaign — 100 branching considerations: other campaigns' health, bounce vs. deliverability, Outlook vs. Google, which inboxes still deliver). "That is a freaking nightmare scenario to build in n8n."
- **Automation = a Merkle tree of if-then logic.** Deterministic. Easy to build well. n8n excels here at scale/volume.
- **Agentic automation** = LLM calls a tool, becomes deterministic again. Hard to build well.

**The graduation ladder:**
1. **Run in Claude Code** (you control it; you can course-correct).
2. **Graduate to the cloud** — **Trigger.dev** (chosen over n8n because it deploys directly from Claude Code via its CLI, is completely malleable, and gives durability/retriability/observability out of the box for agentic flows). n8n stays for deterministic high-volume flows.
3. **Cloud-managed agents** — when it needs on-the-fly access to more knowledge (past clients, databases).
4. **Hermes agent (the top level)** — a dedicated autonomous agent on a cron, with a **self-improving harness built in** (like the Karpathy loop), able to spawn its own sub-agents, orchestrate an org chart from Slack, run any model, work 24/7 as an "AI co-worker." (OpenClaw also mentioned as an alternative.)

**The `/goal` (Ralph loop) feature:** give the AI a goal + budget; it runs many turns until done. Used to attempt one-shotting a complex campaign (it failed and had to be stopped/course-corrected — a deliberately shown realistic failure). With a 1M context window + sub-agents, a goal "could run for like 10 hours."

---

## Layer 6 — The Live Build: GTM Orchestrator + Permissionless-Value Campaign

The capstone: building a real multi-segment cold-outbound campaign end-to-end. Inspiration credited to **Eric Noasoski** (cold-outbound skills — ~50% of the orchestrator's skills are adaptations of his) and **Jordan Crawford** (permissionless-value / "Cannonball" research process). The **GTM Orchestrator** is a Lead Grow plugin (hooks + skills + tools, git-versioned, transferable to the team).

### The campaign logic ("a mini-campaign for every single prospect")
- **Signals** (the buying-state detectors): funding, new leadership hires (last 90 days), actively-hiring-for-leadership, product launches, SEC/government records, G2 reviews. Built by a Hermes agent overnight as scrapers, segment-scored.
- **Permissionless value email** (Jordan Crawford style): "3 company types just hired a CRO this week — here are the decision-makers, here's the sequencing we'd run." Deliver full **decision-maker cards** upfront (contact info broken up so no links trigger spam).
- **Matching logic** (the hard part): match each prospect to signal-companies where target-market overlaps → top 3 by fit score → pull contacts → generate 3 PVP emails. Result shown: ~2,953 prospects → tripled matches via Discolike prospect-expansion → 618 qualified leads at 70% email-hit.

### The 19-stage pipeline architecture
discover → Clay format → Clay enrich (via a **Cloudflare "fire-and-wait" worker that turns Clay into an API**: fire to a webhook, wait, pull back via callback URL into Supabase) → qualify ICP (auto-context + auto-research loops) → enrichments (run through Trigger.dev for concurrency/durability — "hundreds of thousands of processes for ~$12/month") → find-people waterfall (AI Arc → custom agents) → email waterfall (MillionVerifier, Kit, ICPs, Lead Magic) → MX pre-filter (block bad domains) → segment → apply copy → personalize (1:1 AI copy, "a real AI SDR, not a template") → QA-check → launch (create campaigns, upload copy, select inboxes, route leads) into Bison.

### The state model (the durability insight)
- **Git = the Kanban board** (campaign position between sessions) + a **"manifest doc"** that tracks everything done (this is what let him replay the whole build on a dashboard).
- **Supabase / Postgres = the source of truth for DATA** — "if you do campaign data in just git, it will completely implode." Every LLM output must write back to a table or you lose data. Google Sheets is too fragile/unscalable.
- **SQLite** = a convenient local mirror of Supabase.
- Watchwords for any pipeline: **observability, durability, stateful** (durable = resumes after failure; stateful = pauses and remembers).

---

## Layer 7 — Advanced: Security, Plugins-as-Multiplayer, and the Knowledge Graph

### Security
- Hooks to protect `.env` PLUS a **hard deny in `settings.json`** on any direct env-var access ("Claude, implement a hard deny… it'll build it for you in one shot").
- At team scale: run env vars through a password manager; run LLM calls through a **gateway** (LiteLLM / OpenRouter) for security, rate limits, and observability (**Langfuse** to diagnose where context injection goes wrong).

### The Context/Knowledge Graph (called "probably the most important thing in the whole video")
- Recommends **Jacob Deal's `context-os`** (github.com/jacob-dedle/contextos) — a **knowledge graph that updates over time**, maintained by agents.
- **Why a graph beats grep:** a prompt fed by *specific knowledge nodes* gives **traceable** output (you know exactly what produced it). Without it, the model "shakes it all around" and you get a question-mark output you can't debug.
- The graph gives **direct pathways between related contexts** (ICP → persona), so an agent navigates straight there instead of fanning out grep-searches that "burn tokens and fill your context with garbage."
- **Layers of context:** concrete (your business) / emergent (a campaign result you're still testing) / research-driven (might be valuable, unverified). The metaphor: **gardening** — plant good context, trace and pull the "weeds" of bad info before they spread, without pesticide-spraying the whole thing.
- **"Claude Code blew up not because of the best model, but because of the best HARNESS"** — everything surrounding the model (tools, system prompt, baseline prompt). Your job is to set the rest of the direction.

---

## Notable Claims & Numbers

- $100K+ spent on AI over 16 months; Foundation generated $512K+; two businesses acquired.
- DeepSeek can run Claude Code "30 to 100x cheaper."
- Trigger.dev: hundreds of thousands of processes/month for ~$12; the PH signal scraper ~$2/month for ~60 launches/day.
- Claude's official plugin marketplace: 174 plugins (he runs 3).
- Sub-agent context windows ~29-30K each, independent of the orchestrator's.
- Campaign result: ~2,953 prospects → 618 qualified leads, 70% email hit.
- Spend 80% of your time planning ("a perfect plan creates a perfect output").

---

## Concrete Takeaways (the operating playbook)

1. **Escape the copy-paste loop** — run GTM from ONE interface (Claude Code), not a stack of tabs.
2. **Lean CLAUDE.md, trigger-word-rich skills** — record yourself doing a task to build the skill; improve skills via session-log review until you can run them in YOLO mode.
3. **Prefer CLIs over MCPs** — MCPs flood context; CLIs load only what's needed (progressive disclosure).
4. **Let the model prompt YOU** — use a "grill me" skill so the AI surfaces gaps in your plan; always plan-mode + verify between executions; **make a mermaid diagram** before any build to confirm how things chain.
5. **Skill chaining** — the output of skill 1 is pre-curated to be the input of skill 2; gate transitions with hooks.
6. **The Karpathy loop is the highest-leverage GTM system** — one data point + ground truth + challengers + your rules/guardrails; deploy to Trigger.dev as a cron once >90% accurate.
7. **Graduate deployment:** Claude Code (control) → Trigger.dev/cloud agents → Hermes (autonomous, self-improving harness).
8. **Persistence:** Git = Kanban + manifest; Supabase = the data source of truth (never campaign data in git alone); write every LLM output to a table.
9. **Context is the moat** — build a knowledge graph (context-os) so outputs are *traceable* and contexts are reusable across skills.
10. **Multiplayer = plugins + marketplaces with permissions** — "if no one else can use it, you're cooked."

---

## Why This Might Matter (for the Sanctuary System / TWI)

This is an independent, commercially-successful operator arriving — from the GTM-agency angle — at nearly every pillar Isaac's system already encodes: **context-as-moat + progressive disclosure** (load only what's needed), **skills = SOPs with trigger words**, **the self-improving feedback loop** (Karpathy/Ralph ≈ doc-mirror's anneal + the autorealization climb), **a graduation ladder of mechanism** (Claude Code → cloud → autonomous harness ≈ Isaac's complexity ladder rule → skill → harness → OS), **state-what-is via traceable knowledge graphs** (his "trace the weeds" ≈ CartON/journal provenance), and **multiplayer via plugins** (≈ shipping doc-mirror as a plugin). It is strong external corroboration that the architecture is correct, and a competitive datapoint: he sells this exact GTM-orchestrator build to B2B firms (25K+ company market, $15K+ LTV) — directly adjacent to Isaac's B2B funnel and the cold-email → voice-agent → meeting motion in the TWI roadmap. The "permissionless-value" PVP campaign and the CLI-anything / context-os patterns are immediately liftable into the lead-gen design.
