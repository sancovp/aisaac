# I Built an AI Employee That Runs My ENTIRE Business (Complete Beginner Setup)

**Channel:** Nick Puru | AI Automation (@NicholasPuru)
**Published:** 2026-04-03
**Duration:** 29:45
**Views:** ~3,900 | **Likes:** 133
**Tags:** Claude Code, Claude Co-Work, AI Employee, AI Automation, AI Business
**URL:** https://www.youtube.com/watch?v=DEHsoS9KZnE

---

## Summary

Nick Puru walks through how to turn Anthropic's Claude Co-Work (the Claude desktop app with agentic features) into a functional "AI employee" that knows your business, accesses your tools, and runs tasks on autopilot. He frames this around a 3-layer architecture and demonstrates a live content repurposing workflow.

**Core thesis:** Most people use Claude as a fancy search engine — typing prompts from scratch each time, getting generic outputs. The fix is to give Claude persistent context (role), tool access (hands), and scheduled/manual triggers (work orders). All three layers together = AI employee. Missing any one = chatbot.

---

## The 3-Layer Framework: Role + Tools + Triggers

### Layer 1: Role (The Brain)

What Claude knows and how it operates. Three components:

#### 1a. Skills (SOPs for specific tasks)
- A skill = a saved workflow as a markdown file
- Contains: **Goal**, **Steps**, **Tools** (which apps to use), **Output Format**, **Edge Cases**
- Plain text markdown — no code required, shareable across team
- Examples shown: proposal generator, pitch deck generator, content strategy, humanizer (removes AI writing patterns like em-dashes, overly formal language)
- Skills are triggered by slash commands (e.g., `/humanizer`)
- Built-in "skill creator" skill that interviews you and generates the skill file
- **Key insight:** "A skill without a connector is basically a template. Claude can write a perfect follow-up email but cannot send it."

#### 1b. CLAUDE.md (The Employee Handbook)
- General rulebook that applies to EVERYTHING Claude does (not task-specific)
- Contains: company context, tech stack, brand voice, client vs internal communication style, document formatting, file naming conventions, things Claude should NEVER do
- **Critical point:** Don't just throw in a company description — put actual conventions: "how you name files, what tools you use for what, how formal you are in client emails vs how casual on Slack"
- "The more specific and opinionated that file is, the less time you spend fixing Claude's output"
- Structure shown: Repository overview, tech stack, code conventions, Git workflows, key domain terms, environment/secrets, testing, architecture decisions

#### 1c. Projects (Memory)
- Solves the "starting from scratch every session" problem
- Inside a project, Claude remembers: decisions, preferences, context from previous tasks
- Stored as markdown files in the project folder — human-readable
- **Must work inside projects** — standalone sessions have no memory
- Equivalent to ChatGPT's projects feature

### Layer 2: Tools (The Hands)

What Claude can actually access and act on.

#### Native Connectors
- Gmail, Google Calendar, Canva, Notion, Slack, ClickUp, QuickBooks, DocuSign, Stripe, HubSpot, Asana — "thousands"
- One-click setup: click connector, click connect, log in
- Claude can READ data AND TAKE ACTION (send Slack messages, create tasks, draft emails)

#### MCPs for Everything Else
- Zapier MCP = one integration giving access to 8,000+ apps
- Set up once as custom connector

#### Skills + Tools Synergy
- Skill without connector = template (can write email but can't send it)
- Connector without skill = raw access with no process (can talk to Slack but doesn't know what/when)
- Together = real operational output

### Layer 3: Triggers (The Work Orders)

What puts Claude to work.

#### Manual: Slash Commands
- Type `/morning` and Claude runs entire morning briefing workflow
- File name = command name (morning.md = `/morning`)
- Uses skill creator to build them conversationally

#### Automatic: Scheduled Tasks
- Set frequency: hourly, daily, weekdays only, specific times
- Each scheduled task runs as its own full session with access to ALL skills and connectors
- Example: Morning email briefing — checks email for urgent items, pulls calendar, summarizes overnight Slack, gives prioritized focus list
- **Limitation:** Only runs while computer is awake and desktop app is open — NOT a cloud server
- For 24/7 automation, move to Claude Code on a VPS

### Bonus: Plugins (Packaging)

- Package skills + commands + connectors into one installable bundle
- Hand to team member or client — they install and get your entire system
- Anthropic has community GitHub plugin repo
- Pre-built plugin categories: marketing, sales, legal, productivity, design
- Each plugin contains multiple skills for common use cases

---

## Live Demo: Content Repurposing Workflow

Nick's actual production workflow using all 3 layers:

1. **Check for new YouTube uploads** (scheduled trigger — daily)
2. **Pull transcript** from new video
3. **Write platform posts** in Nick's voice (skill)
4. **Format differently per platform** — LinkedIn, X, etc. (skill with formatting rules)
5. **Post to Slack for review** (connector — Slack)
6. **Report back with confirmation** (connector — Slack)

All 3 layers at work: Skill = role, YouTube + Slack connectors = tools, daily schedule = trigger.

---

## Step-by-Step Setup Guide (Nick's recommended order)

1. **Download Claude desktop app** (Mac/Windows). Need Pro plan ($20/mo minimum, recommends Max at $100/mo — Co-Work burns quota fast)
2. **Set up working folder + write CLAUDE.md** (~20 min). Company context, tools, communication style, formatting conventions
3. **Connect top 3 apps**: email, calendar, project management/CRM
4. **Build first skill**: Pick the workflow that eats the most time (follow-up emails, recurring report, client onboarding). Use `/skill creator`
5. **Schedule first task**: Pick something daily (morning briefing recommended — immediate visible value in Slack/Discord/Teams)

---

## Key Insights for Isaac's Business

### What Nick is Actually Selling
- AI automation agency ($5M+ revenue claimed across clients)
- Free Skool community (18,000+ members) as top-of-funnel
- Paid AI Accelerator program on Skool
- "SalesDone.ai" as the service offering
- Monetization: help entrepreneurs build AI agencies + help companies implement AI

### Competitive Intelligence (vs TWI/AIsaac)
- Nick is teaching Claude Co-Work as the platform — this is L1-L2 on Isaac's complexity ladder (prompts + tools)
- His "skills" = Isaac's skills system but in Claude Co-Work consumer form
- His "CLAUDE.md" = Isaac's CLAUDE.md but without the compound intelligence layer
- His "projects" = basic memory — Isaac's CartON/starlog system is orders of magnitude deeper
- His "plugins" = packageable skill bundles — Isaac's skill crystallization loop does this automatically
- **Gap he doesn't cover:** L3-L7 (context engineering, harnesses, admissibility/logic, metacontrol, emergence engineering)
- His "scheduled tasks" limitation (must have desktop open) is exactly what Isaac's CAVE/VPS architecture solves
- **Content format:** 30-min tutorial with screen recording + Excalidraw diagrams — effective for YouTube

### Funnel Analysis
- YouTube video (free) -> Skool community (free, 18K members) -> AI Accelerator (paid Skool) -> Done-for-you services (SalesDone.ai)
- Classic: content -> community -> course -> agency pipeline
- Uses Skool for community (Isaac should note: $99/mo platform cost, Reflio replaces this)

### What Isaac Can Learn
1. **The 3-layer framing is clean** — Role/Tools/Triggers is an accessible mental model. Isaac could adopt similar simple framing for L1-L2 content while pointing to deeper levels
2. **"Employee not chatbot" positioning** resonates — Isaac's PAIA concept is the evolved version
3. **The compounding argument** is powerful: "every skill you write, every connector you add compounds over time" — this IS Isaac's thesis, Nick just doesn't have the infrastructure to actually deliver on it at scale
4. **Plugin packaging as client deliverable** — Isaac's egregore compiler does this but should have a simple "plugin" entry point for L1-L2 users
5. **Content repurposing as first demo** — universally relatable, good first-impression workflow
6. **Morning briefing as first scheduled task** — smart onboarding: daily visible value builds trust in the system

### Pricing Intelligence
- Claude Pro: $20/mo (minimum for Co-Work)
- Claude Max: $100/mo (recommended for serious use — quota burns fast)
- Nick's agency: books free calls, implied $5K+ implementations
- Skool community: free tier + paid accelerator tier

---

## Frameworks Extracted

### The "AI Employee" Test
An AI is an employee (not a chatbot) when it has all 3:
1. Knows your business (persistent context)
2. Has access to your tools (can take action)
3. Can work without you standing over it (triggers/schedules)

### The Compounding Stack
Each addition multiplies everything else:
- New skill + existing connectors = new automated workflow
- New connector + existing skills = existing workflows gain new reach
- Model upgrade + existing system = everything improves automatically

### The "Opinionated Context" Principle
Generic company description barely moves the needle. Specific conventions (file naming, tool preferences, communication formality levels per channel) dramatically reduce output editing time.
