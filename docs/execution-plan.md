# Execution Plan — Ship at Claude Code Level, Then Recompile

Last updated: 2026-05-04

## Product Sequence (THE ORDER)

```
#2 Jobworld (done)
  → #3 Premium Pack (package existing skills into Jobworld)
    → #5 Voice Agent Business template (first "buy a business")
      → #4 Course System (encode HOW we built #5 = the curriculum)
        → #1 Egregore Compiler (connects #3→#5→#4 into one system)
          → ADS: "Watch it compile what we built by hand"
```

Each step produces the next step's input. The build IS the course IS the proof IS the ad.

## Five Products (separated)

1. **Egregore Compiler** — persona + domain → full autonomous business. ENDGAME.
2. **Jobworld** — the app/dashboard. DONE (exists).
3. **Premium Jobworld Self-Mastery Pack** — Jobworld + all frameworks + self-interpreting skills. NEXT.
4. **Course System** — Claude Code config that IS the course. You talk, it teaches AND builds. AFTER #5.
5. **"Buy a Business" Templates** — pre-configured Jobworld for one business model. AFTER #3.
   - 5a. Voice Agent Business (Vapi + lead gen + closer) — FIRST TEMPLATE
   - 5b. Content Agency Business
   - 5c. Lead Gen Business
   - 5d. Ad Agency Business

## The Rule

Phase 1 CANNOT depend on STARSYSTEM, OPERA, CAVE, SOMA, or anything that might not work.
Phase 1 is JUST Claude Code + skills. If Claude Code works, Phase 1 works.

---

## PHASE 1: Finish B2B Funnel End-to-End

GATE: a prospect can go from ad → site → survey → Vapi → payment.

- [ ] Wire Vapi demo agent with cascade script (close → book → B2C → nurture)
- [ ] Stripe product + checkout link for voice agent setup
- [ ] Connect "Get a Demo" on site to Vapi widget
- [ ] Lead gen working (even manual cold email/DMs first)
- [ ] First ad running (Creatify avatar + belief chain script, $50/day)
- [ ] Test full path end-to-end

## PHASE 2: Get Clients + Finish Jobworld (parallel)

GATE: paying clients + Jobworld premium live on Patreon.

- [ ] Sell retainer / pre-built while building
- [ ] Move premium skills BEHIND Patreon (free Jobworld keeps basics)
- [ ] Set up Patreon with PAIAB / SANCTUM / CAVE tiers
- [ ] Clean up Discord (sparse, organized by tier, role-gated channels)
- [ ] Jobworld premium = self-interpreting skills + all frameworks + business models
- [ ] Free Jobworld = basics only

## PHASE 3: Find Autonomous Business Config

GATE: one configuration runs profitably without Isaac touching it daily.

- [ ] Keep selling, keep iterating
- [ ] Test which business model runs itself with least intervention
- [ ] Voice agent business? Content agency? Lead gen? Find the winner.
- [ ] Document what works (this documentation IS the course material)

## PHASE 4: B2C Content About Jobworld Models

GATE: B2C revenue from templates / courses / community.

- [ ] "Buy a Business" templates from proven Phase 3 configs
- [ ] Course system: encode HOW we built the winning config
- [ ] Content machine pumping (Hormozi 400 pieces/week model)
- [ ] Wantrepreneur book published ($2.99 Amazon)
- [ ] Community growing on Discord + Patreon

## PHASE 5: Back to SANCREV

- [ ] Fold all learnings into OPERA
- [ ] Add STARSYSTEM to every agent repo (recompile)
- [ ] Egregore Compiler from proven patterns
- [ ] The real product emerges from proven business models
- [ ] Ads showing compiler generating what was built by hand

---

## Agent Repos (built as needed across phases)

Each agent = a Claude Code skill + a branded GitHub repo.

| # | Agent | What It Does | Repo Name | Phase |
|---|-------|-------------|-----------|-------|
| 1 | Voice Agent Setup | Configures Vapi for a business in 10 min | ai-voice-agent | 1 |
| 2 | AI Demo Caller | The Vapi agent that sells (the cascade) | ai-demo-agent | 1 |
| 3 | Content Machine | CartON/prompts → blog posts, social, scripts | ai-content-machine | 1-2 |
| 4 | Lead Gen | Cold email writer + qualification + follow-up | ai-lead-gen | 1 |
| 5 | Ad Copy Generator | Angles, advertorials, belief chains | ai-ad-copy | 1-2 |
| 6 | VSL Script Writer | Video sales letter scripts from frameworks | ai-vsl-writer | 1-2 |
| 7 | Morning Briefing | Daily business summary from all systems | ai-morning-briefing | 2 |
| 8 | Project Manager | Task tracking, follow-up, blocker detection | ai-project-manager | 2 |

### Each Repo Contains

```
repo-name/
├── README.md          (branded, install instructions, demo GIF/screenshot)
├── .claude/
│   ├── CLAUDE.md      (agent personality + domain knowledge)
│   ├── skills/
│   │   └── the-skill/ (SKILL.md + reference.md + resources/)
│   └── rules/         (behavioral rules for this agent)
├── examples/          (example configs, sample outputs)
└── LICENSE            (MIT)
```

### Template Script

One script generates all repos from the same template:
```bash
./create-agent-repo.sh "ai-voice-agent" "Voice Agent Setup" "Configures Vapi..."
```
Outputs a branded repo ready to push to GitHub.

### Day-by-Day

**Day 1: Vapi + Demo Agent**
- [ ] Create Vapi account
- [ ] Configure voice agent with cascade script (close → book → B2C → nurture)
- [ ] Wire "Get a Demo" button on site to Vapi widget
- [ ] Create ai-voice-agent repo (the skill that sets up Vapi for others)
- [ ] Create ai-demo-agent repo (the Vapi cascade as a template)
- [ ] Test end-to-end: site survey → demo consent → Vapi call → booking

**Day 2: Content + Lead Gen**
- [ ] Create ai-content-machine repo (JourneyBlog template + AIDA fractal + 36 marketing skills)
- [ ] Create ai-lead-gen repo (cold email + qualification + follow-up sequences)
- [ ] Test: generate 5 blog posts, generate 10 cold emails
- [ ] Start posting content (7 pieces minimum)

**Day 3: Ads + VSL + Utilities**
- [ ] Create ai-ad-copy repo (belief chains, angles, advertorials from Mark's framework)
- [ ] Create ai-vsl-writer repo (video script generation)
- [ ] Create ai-morning-briefing repo
- [ ] Isaac records first VSL (avatar or screen recording — imperfect is fine)
- [ ] Run first $50 ad test

**Day 4: Package + Launch**
- [ ] Create template script for consistent branding across all repos
- [ ] Write READMEs with install instructions + demo content
- [ ] Push all repos to GitHub
- [ ] Update free.html with links to all repos
- [ ] Update site: each "What I Build" item links to its repo
- [ ] Announce on Discord
- [ ] Create ai-project-manager repo

**Day 5: Sell**
- [ ] First cold emails go out (using ai-lead-gen)
- [ ] First ads running (using ai-ad-copy output)
- [ ] Content pipeline running (using ai-content-machine)
- [ ] Vapi demo live on site
- [ ] Everything documented as operational self-disclosure content

### Jobworld at Phase 1

Jobworld is just another Claude Code config that loads ALL the agent skills:
```
jobworld/
├── .claude/
│   ├── CLAUDE.md    (CEO agent — sees all departments)
│   └── skills/
│       ├── voice-agent/     (from ai-voice-agent)
│       ├── content-machine/ (from ai-content-machine)
│       ├── lead-gen/        (from ai-lead-gen)
│       ├── ad-copy/         (from ai-ad-copy)
│       └── ...
```
"Launch Jobworld" = `claude --profile jobworld`. That's it.

---

## PHASE 2: Recompile with STARSYSTEM (Target: Week 2)

### What Changes

Fork every Phase 1 repo. Add:
- `starlog.init_project()` — tracking
- Flight configs for each agent's workflows
- Skills that auto-evolve via STARSYSTEM
- YOUKNOW validation for agent outputs
- CartON knowledge graph integration

### The Upgrade Path

```
Phase 1 repo (Claude Code only)
  → fork
  → add .claude/starsystem/ config
  → add flight configs for workflows
  → add starlog session tracking
  → push as v2
```

Each agent goes from "Claude Code skill that works" to "autonomous evolving agent on STARSYSTEM."

### Jobworld at Phase 2

Jobworld loads STARSYSTEM-enhanced agents. Dashboard shows:
- Which agents are running
- Starlog sessions (what they've done)
- GEAR scores (structural quality)
- Knowledge graph (what they've learned)

This is the Paperclip layer — agent orchestration with visibility.

### SANCREV OPERA at Phase 2

OPERA = Jobworld + STARSYSTEM + CartON + Paperclip.
Hide everything that doesn't work. Show everything that does.
The transition from Phase 1 → Phase 2 IS the proof the compiler works.

---

## What We're NOT Doing

- NOT building STARSYSTEM infrastructure (Phase 2)
- NOT building CAVE automations (Phase 2)
- NOT building SOMA/Prolog enforcement (Phase 2)
- NOT building the WakingDreamer (Phase 3+)
- NOT building the full compiler (Phase 3+)
- NOT building Electron apps (not needed)
- NOT building multi-tenant hosting (not needed)
- NOT perfecting anything (ship ugly, iterate)

## The Only Question That Matters

"Does the Vapi agent answer the phone and sell voice agents?"

If yes → everything else follows.
If no → nothing else matters.
