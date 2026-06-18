# I Let AI Run Experiments All Night. It Made My Prompt 2x Better (Auto Research Explained)

**Video:** https://www.youtube.com/watch?v=8T3lMCfZHQM
**Channel:** Nick Puru | AI Automation (@NicholasPuru)
**Published:** 2026-03-31
**Duration:** 19 minutes
**Last updated:** 2026-05-04

---

## Summary

Nick Puru breaks down Andrej Karpathy's open-source "Auto Research" project (42,000+ GitHub stars) and explains its significance for business operators, not just ML engineers. The core thesis: the Auto Research pattern — automated trial-and-error with a measurable score — applies far beyond ML model training. It works for anything where you have (1) something to change, (2) a number to track, and (3) a way to test it via API/CLI.

---

## The Auto Research Pattern (The Core Loop)

```
1. READ the thing you want to improve
2. MAKE ONE CHANGE (just one)
3. RUN A TEST → get a SCORE
4. Did the score improve?
   YES → COMMIT the change, LOG what happened, LOOP back to 1
   NO  → REVERT the change, try something different, LOOP back to 1
5. NEVER STOP. "The human might be asleep."
```

**Why it works:** Not because the AI is smarter at any single decision — it works because it does not stop. Over 50, 100, 500 runs, it finds optimizations a human would miss because humans get tired or distracted after ~10 iterations.

**Three requirements for any Auto Research target:**
1. Something you can CHANGE (copy, code, prompt, config)
2. A NUMBER you can TRACK (reply rate, conversion rate, accuracy score, execution time)
3. A way to TEST IT (API, CLI, file system — some programmatic feedback mechanism)

---

## Key Evidence / Case Studies

### Karpathy's Original Run
- Ran for ~2 days on a small language model
- Agent found ~20 stacked improvements
- One was a bug Karpathy himself missed for months (missing scalar multiplier making attention mechanism too diffuse)
- The repo is just 3 files: `prepare.py`, `train.py`, `program.md`

### Shopify CEO (Tobi Lutke)
- Ran Auto Research on Liquid (Shopify's 20-year-old Ruby template engine)
- ~120 automated experiments over ~2 days
- Result: **53% faster, 61% fewer memory allocations**
- On code that engineers had been manually optimizing for two decades
- Lutke acknowledged possible overfitting but said "absolutely amazing ideas in the results"

### Nick's Live Demo (Prompt Optimization)
- Task: Extract structured JSON from customer inquiry emails
- Mediocre starter prompt scored **7/15** on test suite
- Let Claude Code run the Auto Research loop autonomously
- 5 experiments later: **15/15 perfect score**
- Total cost: **$0.24**
- Each experiment logged: hypothesis, score before/after, keep/revert status, remaining failures

---

## Business Use Cases Identified

| Domain | What Changes | What You Track | API/Tool |
|--------|-------------|----------------|----------|
| **Cold Email** | Copy/subject lines | Reply rates | Instantly, SmartLead API |
| **Landing Pages** | Headline, CTA, layout | Conversion rate | Webflow, Framer API |
| **Ad Creatives** | Copy, image, audience | CTR, CPA | Meta Ads API, Google Ads |
| **Code Performance** | The code itself | Execution time | CLI benchmarks |
| **Prompt Engineering** | The prompt | Accuracy score | Claude Code / any LLM API |
| **Chatbot Scripts** | Conversation flows | Resolution rate | Chatbot platform API |
| **Newsletter Subject Lines** | Subject line text | Open rate | Email platform API |
| **Voice Agent Prompts** | Agent script | Call success rate | Voice platform API |
| **YouTube Thumbnails** | Thumbnail design | CTR | YouTube Analytics API |
| **Pricing Pages** | Price points, layout | Conversion rate | Site builder API |

---

## Competitive Advantage Framing

> "Your competitor who runs 30 tests on their landing page per year — you run 30 per day because you've got a loop running in the background. Who has the better landing page by December? It's not even close."

This is the key business argument: Auto Research turns optimization from a human-bottlenecked activity (1-2 tests/week) into a machine-speed activity (100+ tests/night). The compound effect over months is massive.

---

## Honest Limitations (Nick's Own Caveats)

1. **Fast feedback required** — if a test takes a week to get data, the loop is slow. Start with whatever gives you data fastest.
2. **Need a real number** — "not just vibes." Must be a countable metric: pass/fail, percentage, response time, reply rate.
3. **Agent needs programmatic access** — API, file, CLI. Something it can change and test without human intervention.
4. **Not for big-picture strategy** — the agent won't tell you which market to go after. It optimizes execution (copy, targeting, prompt engineering, micro-optimizations that compound).

---

## Actionable Frameworks for Isaac's Business

### Immediate Application: Voice Agent Prompt Optimization
- Isaac's voice agent qualifies leads and books meetings
- Auto Research loop: change the voice agent prompt, track booking rate / qualification accuracy, iterate via voice platform API
- Could run overnight, wake up to a measurably better voice agent

### Immediate Application: Cold Email Optimization
- Phase 1 of TWI roadmap is cold email → voice agent → meeting
- Auto Research on cold email copy: change subject/body, track reply rate via Instantly/SmartLead, iterate
- People reporting 2% → 8-12% reply rates with this pattern

### Immediate Application: Landing Page CTA Optimization
- sancovp.github.io/aisaac/ has 9 pages
- Auto Research on headlines and CTAs: change copy, track conversion, iterate via site builder

### The Experiment Log as Content
- Each Auto Research run produces a detailed experiment log (hypothesis, score, keep/revert)
- This log IS content: "I let AI optimize my cold email overnight. Here's what it learned."
- Operational self-disclosure = the system showing itself working = marketing

### The Pattern IS the Product (L4 Harness)
- Auto Research pattern maps to Isaac's L4 (Harnesses — systems AROUND the AI for reliability)
- Could be packaged as a cohort lesson: "Here's how to set up automated optimization for your business"
- The loop is simple enough to teach, powerful enough to differentiate

---

## Technical Setup (From Demo)

1. Clone Karpathy's Auto Research repo for context
2. Create custom version with:
   - `program.md` — instructions for the agent (the loop protocol)
   - `prompt.md` — the thing being optimized (starter prompt)
   - `eval.py` — scoring script (runs against test cases, returns score)
   - `test_cases.json` — ground truth for evaluation
   - `experiment_log.md` — auto-populated record of all runs
3. Tools needed: Claude Code (or any code-capable AI) + relevant API key
4. Cost: ~$0.24 for 5 optimization rounds on 15 test cases

---

## Nick Puru Context

- Runs AI automation agency, claims $5M+ in bottom-line revenue across clients
- Has 18,000+ member Skool community (free tier)
- Offers: free community, weekly AI newsletter, team training/implementation audits
- Website: salesdone.ai
- His business model mirrors part of Isaac's value ladder (community → training → done-for-you)
- Uses the "free community + paid implementation" funnel structure
