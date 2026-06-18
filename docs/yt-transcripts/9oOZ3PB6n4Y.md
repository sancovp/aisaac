# Competitive Intelligence Synthesis

## Video: "Hermes Agent /Go Feature: The Most Important Command of 2026"
**Channel:** David (AI agent/automation YouTuber, likely "David Ondrej" or similar — promotes "New Society" community)
**Duration:** ~20 minutes (31,718 chars transcript)
**Topic:** How to set up Hermes Agent on a VPS, activate the /go (goal) feature, and use it for autonomous long-running tasks including business automation and multi-agent orchestration with Codex CLI.

---

### Key Claims

- /go is "the single most important command of 2026" — allows tasks that take 10-20 hours to complete autonomously
- Hermes Agent overtook OpenClaw as the #1 app globally on OpenRouter token rankings
- /go originated from the "Ralph Wiggum loop" concept (January 2026) but adds a judge model, sub-goals, and token budgets
- OpenAI released /goal in Codex CLI on April 30, 2026; Hermes followed days later with an "arguably more powerful" version
- You can use your existing ChatGPT subscription (Plus or Pro) to power Hermes Agent for free via OpenAI Codex authentication
- Hermes can now use Codex CLI as its runtime for tool execution when using OpenAI models
- /go can run 6, 12, 18, 24+ hours until the defined end state is achieved
- A woman used Codex /goal to sell excess farm produce by having it message potential customers autonomously

---

### Technical Details

**How /go works according to the video:**
1. You define a clear, measurable end goal (e.g., "tests passing", "10 new customers", "all slides generated")
2. A separate **judge model** evaluates progress — it sees the goal text, last 4KB of agent response, and system prompt
3. The judge checks whether execution is headed in the right direction and whether the task is complete
4. The loop runs until: goal achieved, you pause it, or token budget exhausted
5. Sub-goals can be injected mid-run via `/sub goal` without restarting
6. Survives crashes and restarts — persistence across sessions
7. You can interact with it mid-run

**Hermes /go advantages over raw Ralph loops (as claimed):**
- Built-in judge model (separate, unbiased from execution)
- Lives inside full Hermes harness (checkpoints, V2, rollback, LSP, skills, MCP tools)
- Crash/restart survival with session persistence
- Mid-run interaction and sub-goal injection
- Built-in slash command vs. external setup

**Features/tools discussed:**
- Hermes Agent skills system (82 pre-built skills)
- Skill creation from learned experiences (CDN/Cloudflare workaround became a skill)
- OpenRouter for image generation (GPT Images 2 model)
- Codex CLI as sub-agent runtime controlled by Hermes
- CEO/CTO pattern: Hermes as orchestrator, Codex CLI agents as workers
- VPS setup on Hostinger for persistent agent hosting
- SSH access and SCP for file transfer
- `/fast` toggle for priority processing

**Specific prompts/skills mentioned:**
- Image generation skill using OpenRouter + GPT Images 2
- Presentation/slide deck generation skill (PowerPoint-quality output)
- "Autonomous AI agents" pre-built skill for launching Codex CLI sub-agents
- CEO prompt: "You are the CEO. Spawn two sub agents via the autonomous agents skill. CTO build X. CMO build Y. Goal criteria: both repos committed with all required deliverables."

---

### Actionable Tactics

1. **Set up Hermes on a VPS** (Hostinger recommended, 24-month plan for discount)
2. **Use ChatGPT subscription auth** instead of API keys to run Hermes for free
3. **Store API keys via `hermes config set`** — keeps keys out of context window (security)
4. **Define measurable end states** — "tests passing", "10 customers contacted", "all slides generated" — not vague goals like "build a great app"
5. **Use CEO/CTO pattern** — Hermes orchestrates, Codex CLI sub-agents execute
6. **Create skills from failures** — when Hermes hits an error and solves it, have it save the solution as a skill
7. **Use `/sub goal`** to steer mid-run without restarting
8. **Use `/fast` toggle** for priority processing (burns credits faster but much faster execution)
9. **Use Midjourney for style references** and GPT Images 2 for actual generation
10. **Give Hermes all possible tools, APIs, skills, MCPs** so /go doesn't get stuck

---

### Relevance to AIsaac/TWI

**Direct competitive overlap:**
- This is EXACTLY what Isaac's system does but with SOMA as the validation/judge layer instead of Hermes's simple judge model
- The "Ralph Wiggum loop" is literally named after Isaac's pattern — the video credits it as the origin of /go
- The CEO/CTO multi-agent orchestration is what Isaac's conductor/GNOSYS/ralph hierarchy does, but with proper ontological validation

**The "Made Hermes Actually Smart" angle:**
- Hermes's judge is a simple AI model that sees "last 4KB + goal text" — it has NO ontological grounding, NO domain validation, NO deduction chains
- SOMA provides what Hermes's judge CANNOT: structured observation chains, pattern validation, semantic guarantees that the goal criteria actually map to reality
- A SOMA plugin for Hermes would replace the naive judge with an actual validation layer (L5 logic)
- The video literally shows a failure mode: the presentation had "slightly misaligned" elements, the blog post was "way too congested text" — these are quality failures the judge missed because it only checks "is it done?" not "is it good?"

**Gap/opportunity for a SOMA plugin:**
- Hermes has 82 skills but NO validation that skills produce correct output
- The skill-creation-from-failure pattern is ad-hoc — SOMA would formalize this as observation chains
- /go's judge has no memory of WHY something failed before — SOMA's accumulated observations would prevent repeated failures
- Sub-goal injection is manual — SOMA could auto-generate corrective sub-goals from observation data

**Content pipeline opportunity:**
- This video has 31K chars of transcript = this creator produces long-form content about Hermes
- Isaac's "Made Hermes Actually Smart with SOMA" angle directly targets this audience
- The video's audience already uses Hermes — they're pre-qualified for a SOMA plugin
- Isaac can make content showing SOMA catching the failures this video's demos produced

---

### Competitive Position

**What this creator gets RIGHT about Hermes:**
- Clear explanation of the judge model architecture (separate from execution, sees limited context)
- Correct identification that measurable end states are the key differentiator vs. raw loops
- Good understanding of the CEO/CTO multi-agent pattern
- Accurate claim about crash persistence and mid-run interaction
- Smart use of Codex CLI as runtime to leverage existing ChatGPT subscriptions
- Correctly identifies skills-from-failures as a competitive advantage

**What they MISS (that SOMA/observation chains cover):**
- **No quality validation** — the judge checks "is it done?" never "is it correct/good?" The presentation had alignment issues, the blog was unreadable. A naive judge said "goal achieved" when the output was mediocre.
- **No accumulated learning across goals** — each /go starts fresh. SOMA's observation chains would carry learned patterns (e.g., "GPT 5.5 produces bad frontend design" would become a routing rule after one observation)
- **No ontological grounding for goal criteria** — "both repos committed with all deliverables" is a string the judge pattern-matches against. SOMA would decompose this into verifiable structural claims.
- **No deduction about WHAT to measure** — the user must manually define success criteria. SOMA could auto-generate measurement criteria from domain knowledge (L5 logic vs. L1 prompt-level goal definition)
- **No observation of failure modes** — when the CDN blocking happened, it was solved ad-hoc. SOMA would classify this failure, store the pattern, and prevent it system-wide across all future goals.
- **Skills are black boxes** — Hermes creates skills but has no way to validate they'll work in new contexts. SOMA validates skill applicability via type checking.
- **The "CEO/CTO" pattern has no accountability layer** — Hermes fires off Codex agents and checks "did files get committed?" but has no way to verify the QUALITY of what was committed. SOMA provides the semantic audit layer.

**Where Isaac's content would differentiate:**
1. **"Your /go judge is blind" video** — show a Hermes /go completing with mediocre output, then show SOMA catching the quality failures the judge missed
2. **"Hermes skills are just prompts, mine are validated"** — demonstrate a Hermes skill failing in a new context vs. SOMA-validated skills that carry applicability constraints
3. **"The Ralph Loop grew up"** — Isaac can claim legitimate origin credit for the pattern and show how GNOSYS is the mature version (proper ontology, not just "run again and check")
4. **"L1 goals vs. L5 goals"** — demonstrate that "build an app" is L1, "build an app where all routes return valid schemas and the auth flow completes in under 2 seconds" is L5, and SOMA auto-generates L5 criteria from L1 descriptions
5. **Price angle** — this creator sells a $X/month community ("New Society") for Hermes setup guides. Isaac's SOMA plugin would be the actual product that makes Hermes smarter, not just a tutorial community

---

### Summary

This video represents the mainstream AI agent audience (non-technical, business-focused, wants autonomous money-making). The creator is essentially selling "how to set up Hermes" as a course. Isaac's angle is fundamentally different: not "how to set it up" but "how to make it actually reliable" via SOMA as a validation/observation layer. The entire gap between "goal achieved" (what Hermes reports) and "goal actually achieved correctly" (what SOMA verifies) is Isaac's product territory. L1-L3 is what this creator teaches. L4-L7 is what Isaac builds.
