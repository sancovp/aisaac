# Build & Sell Claude Code Operating Systems (2+ Hour Course)

**Channel:** Nate Herk | AI Automation
**Duration:** 2:33:21
**URL:** https://www.youtube.com/watch?v=bCljOfCH8Ms

---

## Summary

Nate Herk presents a 2.5-hour "course" on building a personal AI Operating System (AIOS) inside Claude Code, framed as a gift from someone who scaled an AI agency to $100K/month and sold it. The core thesis is that Claude Code becomes your "layer between you and your computer" — a persistent, context-rich agent that knows your business, connects to your tools, and can act autonomously via scheduled routines. The system is built from: a CLAUDE.md master prompt, a context folder, skills (markdown SOPs), API connections, and Claude's native routines/loop features for cadence. The "operating system" framing is marketing — technically it is CLAUDE.md + skills + API connections + scheduled tasks — but it is well-packaged and genuinely useful for the target audience. The course is free, with upsell into a paid community where he drops more skills.

---

## Key Sections

### 1. Introduction & Framing (0:00–10:00)
- Positions himself as authority: $100K/month AI agency, sold it, 350K community members
- Defines "AI OS" as the intelligence layer on top of Claude Code — sees files, communicates with tools, remembers everything
- Promises tool-agnostic foundation ("I moved this to Codex in 2 minutes")
- Teases free setup guide + GitHub repo in his School community

### 2. The 3 M's Framework (10:00–25:00)
- **Mindset**: Default shift (always ask "how could AI do 30% of this?"), function breakdown (job = tree of tasks), curiosity rule (ask why, don't treat AI like a vending machine)
- **Method**: How to decide what's worth automating
- **Machine**: The technical setup
- Key insight: "Productivity drops before it climbs" — expects 20% dip, promises 50% gain

### 3. The 4 C's Framework (25:00–40:00)
- **Context**: What the AI knows about you, your business, your voice
- **Connections**: What data it can reach (MCPs, APIs, CLIs)
- **Capabilities**: What it can produce (skills/SOPs)
- **Cadence**: When it acts autonomously while you sleep
- These build on each other in order — can't have cadence without connections
- Tier-1 buckets: revenue, customer, calendar, comms, tasks, meetings, knowledge

### 4. Setup Walk-Through (40:00–60:00)
- Clone his GitHub repo into a local AIOS folder
- CLAUDE.md = master prompt with placeholders, skills directory reference, folder structure
- Run the `/onboard` skill — 7-question interview that creates: `about-me.md`, `about-business.md`, `priorities.md` in a `context/` folder
- Demonstrates the AI answering "what should I focus on this week?" using those context files

### 5. Connections — ClickUp API (60:00–85:00)
- Prefers API endpoints over MCP servers ("token efficient, more control")
- Pattern: ask Claude to research the API docs, build a markdown reference file locally, create a `.env` for the key
- Created a dedicated API account ("UpAI") for the AIOS — per-account permissions and cost tracking
- Demonstrated: team workload snapshot, DM to ClickUp (created a task instead of DM — acknowledged the miss)
- `/audit` skill: grades your AIOS 0–100 on the 4 C's
- `/level-up` skill: asks 5 questions to find your next automation opportunity

### 6. Google Workspace CLI (85:00–110:00)
- Open-source Google CLI (community project, not officially supported) — one tool gives Claude access to Gmail, Drive, Docs, Sheets, Slides, Calendar
- Connects via Google Cloud Console OAuth (desktop app)
- Demoed: organizing Drive, auto-populating YouTube video database in Sheets, creating Google Slides with brand assets + visual validation via Chrome DevTools screenshots
- 100+ pre-built "recipes" (multi-step workflows)
- Preferred over MCP: single tool, lower token overhead

### 7. Skills Deep-Dive (110:00–145:00)
- Skills = markdown SOPs in `.claude/skills/` — YAML front matter (name, description), step-by-step instructions, optional reference files and scripts
- Progressive context loading: Claude reads only name+description (~100 tokens) until it decides to invoke, then reads full skill, then loads supporting files only if needed
- Live build: infographic builder skill using Fal.ai Nano Banana + logo overlay
- Six-step skill building framework: name/trigger, goal, step-by-step process, reference files, rules/guardrails, self-improvement loop
- Feedback cycle: run skill → watch → give feedback → skill updates itself
- Global vs project-scoped skills (tilde directory for global)
- Skill marketplace emerging; skills are transferable across Claude Code, Cursor, Codex

### 8. Cadence — Routines & Loop (145:00–185:00)
- **Claude Routines** (cloud-based scheduled tasks): runs on Anthropic infrastructure, no laptop needed. Requires GitHub repo (no .env — API keys go in cloud environment variables). Limits: 5/day (Pro), 15/day (Max $200/mo), 25/day (Team/Enterprise). Minimum interval: 1 hour. Trusted vs Full network access.
- **Desktop Scheduled Tasks**: local, laptop must be on, longer-lived, has catch-up
- **Loop skill** (`/loop`): per-session recurring prompts, up to 3 days, minimum every few minutes, session must stay open. Good for "help me now" scenarios (watching deploys, checking emails, sprint monitoring)
- Routines are "oneshot prompts" — must be self-sufficient, no user interaction
- Demonstrated: wins engagement skill auto-posting to School community, YouTube comment analysis

### 9. Knowledge System — LLM Wiki (Karpathy Method) (185:00–210:00)
- Based on Andrej Karpathy's LLM knowledge base post
- Architecture: `raw/` folder (input documents) → Claude processes → `wiki/` folder (indexed, linked markdown pages)
- Visualized with Obsidian (free, optional)
- Hot cache (500-char summary of most recent context) for executive assistant use case
- Compared to RAG: better for 100s of pages, cheaper (markdown only), no embeddings infra; RAG wins at millions of documents
- One user dropped token usage 95% by converting 383 scattered files + 100 meeting transcripts into a wiki
- 36 YouTube transcripts → 14-minute batch ingest → full node graph with relationships

### 10. Artifacts, Dashboards & Daily Loop (210:00–153:21)
- Claude Artifacts / Co-work tab: quick dashboards pulling live data (QuickBooks, ClickUp, Fireflies) — proof-of-concept before building custom
- Daily loop: morning plan → end-of-day review → patch gaps
- Weekly: run `/audit`, identify daily-use skills to automate further
- KPIs: (1) team reaches out to AIOS instead of you, (2) you stop opening new tabs, (3) knowledge leaves your head
- Closing sell: voice OS future (Glido sponsorship), directs to context management video

---

## What They Actually Build (Technical Assessment)

**Complexity Ladder: L2–L3 (Tools + Context). Touches L4 (Cadence/Harnesses) at the edges.**

The actual technical stack:

| Component | What It Is |
|---|---|
| CLAUDE.md | A master system prompt with folder structure map |
| `context/` folder | Markdown files: about-me, about-business, priorities |
| `.claude/skills/` | Markdown SOPs with YAML front matter = L2 tools |
| `.env` | API keys |
| API reference .md files | Locally cached API docs (reduces token usage) |
| Claude Routines | Scheduled prompt injection via Anthropic cloud |
| `/loop` skill | Built-in Claude Code cron scheduler |
| LLM Wiki | Karpathy-method markdown knowledge base in Obsidian |
| GWS CLI | Open-source Google Workspace CLI bash integration |

There is NO:
- Persistent memory store beyond markdown files and GitHub repo
- Graph database or knowledge graph with typed relationships
- Hook system or autonomous feedback loop beyond "skill gets updated when it fails"
- Ontology or validation layer
- Multi-agent orchestration beyond "open 4 tabs in parallel"
- Programmatic self-improvement — all "iteration" is manual human-in-the-loop

**The "operating system" is CLAUDE.md + a well-organized folder structure + skills as SOPs + Claude's native scheduled tasks.** It is genuinely L2-L3 competence with good packaging and very clear onboarding.

The most technically sophisticated parts are:
1. The progressive context loading insight (name+desc first, full skill second, references only if needed)
2. The LLM Wiki / Karpathy method for knowledge compression
3. The API-over-MCP preference for token efficiency
4. The sub-agent delegation pattern within skills (ClickUp searcher agent)

---

## Pricing & Sales Model

**Nate's model: free course → free community → paid community → skill marketplace + sponsorships**

- Claude Code requires paid Anthropic subscription: $17–$20/month (Pro) or $200/month (Max)
- His School community: **free tier** gets the course resources, GitHub repo, skill drops
- **Paid community**: not explicitly priced in this video, but referenced multiple times
- **Skill marketplace**: mentioned as emerging monetization — "skills are having a big moment" — but explicitly says not to bank on it as a primary business model
- **Sponsorships**: Glido (voice tool), mentioned as official team member
- Revenue model: audience → community → upsells. This video is pure top-of-funnel.

**What he sells:**
1. Free: the course + GitHub repo + skills in School community
2. Paid community (monthly membership, price unspecified in transcript)
3. Implicit: his agency clients (referenced but not pitched here)

**The offer framing**: "I give you everything for free, join my community, it's 350K members." Classic Hormozi-style free value → community → paid tiers.

---

## Competitive Intelligence (for Isaac)

### What They Have vs What We Have

| Dimension | Nate Herk AIOS | Isaac / GNOSYS |
|---|---|---|
| **Core architecture** | CLAUDE.md + skills + markdown files | CAVE + SOMA + CartON + YOUKNOW + flight configs + hooks |
| **Memory** | Markdown files + GitHub repo | Neo4j graph database + ChromaDB embeddings + ontology |
| **Skills** | Markdown SOPs, manually iterated | Dragonbones-compiled from ontology, OWL-validated |
| **Agent identity** | "AIOS" persona per CLAUDE.md | Full PAIA with persona + Starsystem pilot + Ralph + Conductor |
| **Autonomy** | Routines (15/day max, 1hr min interval) | OMNISANC loop + CAVE automations (no platform limits) |
| **Knowledge** | LLM Wiki / Karpathy method | CartON typed concept graph + ChromaDB + Starlog sessions |
| **Validation** | None — skills just fail and get manually fixed | YOUKNOW OWL validation, SOMA Prolog deduction chains |
| **Self-improvement** | Human watches skill run, manually prompts update | Dragonbones emits EC → hook compiles → CartON persists |
| **Complexity level** | L2-L3 (Tools + Context) | L4-L6 (Harnesses + Admissibility + Compound Intelligence) |
| **Pricing** | Free course + paid community | $2K+ setup + $200/mo per system (agency model) |
| **Target** | Individual knowledge workers, content creators | Businesses needing full AI integration (B2B) |

### Where Isaac Wins Technically
- CartON is not markdown files — it's a typed, queryable, self-healing knowledge graph. The LLM Wiki Nate builds is L1 compared to CartON
- YOUKNOW provides actual schema validation — his skills "get better" only through manual human feedback loops
- SOMA/Prolog deduction means the system reasons correctly, not just fluently (L5 vs L2)
- CAVE automations run truly 24/7 with no Anthropic platform limits (15/day for Nate)
- OMNISANC is a stateful loop — Nate's "cadence" is stateless oneshot prompts
- GNOSYS builds agents that build themselves (Starsystem game) — Nate builds a personal productivity tool

### Where Nate Wins on Marketing/Positioning
- **"Operating System" framing** is sticky and aspirational — immediately understood
- **Four C's framework** (Context, Connections, Capabilities, Cadence) is clean, memorable, teachable
- **Three M's** (Mindset, Method, Machine) lowers the intimidation barrier
- **Free course as funnel** — 350K community members is enormous top-of-funnel
- **"Proof of concept first"** mindset — explicitly tells people to build artifacts before custom dashboards
- He **shows the productivity gain viscerally**: 4 parallel agents doing 4 tasks in 30 seconds
- **Boring is beautiful** framing — validates deterministic automations over AI agents, builds trust
- His onboarding is genuinely good UX: 7 questions → 3 files → "what should I focus on this week?" works immediately on Day 1

### What Language Resonates That Isaac Should Use
- "AI Operating System" / "AIOS" — better than "PAIA" or "compound intelligence" for cold audiences
- "It never sleeps, it has perfect memory" — concrete benefit statement
- "4 agents running in parallel doing 4 tasks while I spent 30 seconds asking" — vivid ROI demonstration
- "Your job is a tree of tasks — automate one chunk at a time" — actionable, not overwhelming
- "Knowledge leaves your head" — emotional pain point resolution
- "Boring is beautiful — deterministic beats agentic 9 times out of 10" — trust-builder, counter-hype
- "Proof of concept first" — reduces commitment anxiety
- "Productivity drops before it climbs" — pre-empts the 20% dip objection

---

## Actionable Takeaways

1. **Steal the "4 C's" framing** for positioning GNOSYS/Jobworld: Context → Connections → Capabilities → Cadence. It maps exactly to what GNOSYS does at L1-L6 but in language a non-technical buyer understands. Use it in sales calls and on the site.

2. **Create a Day 1 onboarding flow** like his `/onboard` skill. The 7-question interview → 3 context files → "what should I focus on this week?" pattern creates immediate felt value. Isaac's system needs an equivalent that works in 10 minutes for a new client.

3. **Position the LLM Wiki / Karpathy method** as a stepping stone to CartON in the curriculum. Teach it at L3, then show how CartON is what happens when you make the wiki typed, queryable, and self-healing. The upgrade path is obvious and defensible.

4. **Demo 4 agents in parallel** — Nate's best moment is opening 4 Claude Code windows and running 4 skills simultaneously. Isaac's demo equivalent should show CAVE automations + Starsystem doing equivalent work autonomously without human prompting. The contrast would be devastating.

5. **Steal the audit skill concept** for the Jobworld dashboard. An "AIOS audit" that grades your AI integration on 4 C's and surfaces gaps is a natural product feature for Jobworld — it drives engagement, surfaces upsells, and gives clients a score to improve.

6. **Use "boring is beautiful"** explicitly in content to position Isaac's L4-L7 work as the inevitable next step after the boring automations are done. Nate's audience is at L2-L3; when they hit the ceiling, Isaac's offer should be the natural upgrade.

7. **API-over-MCP preference** is worth teaching in Isaac's cohort. The pattern (research docs → local markdown reference file → .env key) is solid token management practice. The insight that MCPs load all endpoints and eat context is real and teachable.

8. **Build a "skill builder" skill for Jobworld clients** — his skill builder that asks 6 questions and generates the SKILL.md is a genuinely good product. Isaac's compiler should produce these automatically from the persona-seed spec.

9. **Address the 15/day routine limit** as a competitive wedge. Nate's "cadence" is bottlenecked by Anthropic platform limits (15 routines/day, 1hr minimum, stateless). CAVE has none of these constraints. Use this directly in sales: "When your business needs more than 15 automations a day, that's when you need OPERA."

10. **Replicate his free community → paid tier funnel structure** but compress the L1-L3 content into the free tier (blog + videos + Discord) and position the cohort as where you learn L4+. His free course is literally the L1-L3 curriculum for the TWI cohort — Isaac should give away the same depth for free and make L4 the gate.
