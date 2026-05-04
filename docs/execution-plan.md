# Execution Plan — Ship at Claude Code Level, Then Recompile

Last updated: 2026-05-04

## The Rule

Phase 1 CANNOT depend on STARSYSTEM, OPERA, CAVE, SOMA, or anything that might not work.
Phase 1 is JUST Claude Code + skills. If Claude Code works, Phase 1 works.

---

## PHASE 1: Claude Code Level (Target: 3-5 days)

### What We Build

Each agent = a Claude Code skill + a branded GitHub repo.

| # | Agent | What It Does | Repo Name | Priority |
|---|-------|-------------|-----------|----------|
| 1 | Voice Agent Setup | Configures Vapi for a business in 10 min | ai-voice-agent | DAY 1 |
| 2 | AI Demo Caller | The Vapi agent that sells (the cascade) | ai-demo-agent | DAY 1 |
| 3 | Content Machine | CartON/prompts → blog posts, social, scripts | ai-content-machine | DAY 2 |
| 4 | Lead Gen | Cold email writer + qualification + follow-up | ai-lead-gen | DAY 2 |
| 5 | Ad Copy Generator | Angles, advertorials, belief chains | ai-ad-copy | DAY 3 |
| 6 | VSL Script Writer | Video sales letter scripts from frameworks | ai-vsl-writer | DAY 3 |
| 7 | Morning Briefing | Daily business summary from all systems | ai-morning-briefing | DAY 3 |
| 8 | Project Manager | Task tracking, follow-up, blocker detection | ai-project-manager | DAY 4 |

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
