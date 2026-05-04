# Lead Gen System — Design Doc

Last updated: 2026-05-04

## The Advantage Over Everyone Else

Every competitor's system is INBOUND — build a site, hope people come, handle whoever shows up. Our system is OUTBOUND + INBOUND: we find them, research them, personalize the outreach, and when they respond, the AI already knows their business before the call starts.

GHL agencies ask "tell me about your business." Our agent says "I see you run [X] and you posted about [Y] last week — here's what I'd automate for you."

## Architecture

```
OUTBOUND PIPELINE:
  Prospect List → Social Scraping → Enrichment → Personalized DM/Email → Response
    → Qualification → Vapi Demo Call (pre-loaded with prospect context)

INBOUND PIPELINE:
  Site Traffic → Survey Qualification → Demo Consent → Vapi Demo Call
    → Same cascade as outbound
```

## Phase 1: Manual + Claude Code (this week)

### Step 1: Build Prospect List
- Source: Google Maps (local businesses), LinkedIn Sales Navigator, Instagram hashtags
- Filter: businesses that take phone calls (restaurants, dentists, realtors, contractors, etc.)
- Tool: Firecrawl API scrapes their website → clean markdown
- Store: CSV or Airtable (simple, no infra needed)

### Step 2: Enrich Each Prospect
Claude Code agent reads:
- Their website (via Firecrawl)
- Their Google Business profile
- Their social media (Instagram bio, recent posts, LinkedIn)
- Their reviews (pain points surface here)

Output per prospect:
```json
{
  "name": "Dr. Smith",
  "business": "Smith Family Dental",
  "website": "smithdental.com",
  "pain_points": ["missed calls during procedures", "receptionist overwhelmed"],
  "recent_posts": ["just hired a new hygienist", "open Saturdays now"],
  "reviews_mention": ["hard to reach by phone", "great once you get in"],
  "personalization_hook": "Your patients love you but can't reach you by phone"
}
```

### Step 3: Generate Personalized Outreach

**DM Template (Referral Bait — from Automate AI Consulting):**
"Hey [Name], I'm hoping you can help me out. I know [Business] takes calls from leads and I'm looking to have a couple businesses test my AI voice agent system for a month for free. It answers calls, qualifies leads, and books appointments 24/7. Would you be open to trying it? You can even call the demo line right now to hear it: [Vapi number]"

**Email Template (CAN-SPAM compliant):**
Subject: "[Business] — your patients can't reach you by phone"
Body: Personalized based on enrichment data. References specific reviews/posts.
CTA: "Reply 'yes' and I'll set up a 30-second test call"
Footer: Unsubscribe link (CAN-SPAM required)

### Step 4: Send
- Email: Gmail API or SMTP (start manual, automate later)
- DM: Instagram DM (manual first), LinkedIn InMail (manual first)
- Volume: 50/day email, 20/day DM (warm up accounts)

### Step 5: Response Handling
- "Yes" → send Vapi demo number OR direct to site survey
- "Tell me more" → send one-liner + Vapi number
- "Not interested" → log, move on
- No response → follow-up in 3 days (max 3 touches)

### Step 6: Vapi Call (Pre-Loaded)
When prospect calls the demo number, Vapi agent has their enrichment data:
- "Hi [Name], thanks for calling. I understand [Business] has been dealing with [pain_point]. Let me show you how this would work for your specific situation..."
- Agent demos itself AS their receptionist
- Runs the cascade: close → book Isaac → B2C → nurture

## Phase 2: Automated (week 2+)

### Automation Targets
| Manual Step | Automated Version | Tool |
|-------------|------------------|------|
| Build prospect list | Firecrawl scrapes Google Maps by niche+location | Firecrawl API + cron |
| Enrich prospects | Claude reads scraped data, outputs JSON | Claude API batch |
| Generate messages | Claude generates from enrichment + template | Claude API |
| Send emails | Gmail API or Instantly.ai | API + scheduler |
| Send DMs | PhantomBuster or manual | (manual stays longer — platform risk) |
| Response handling | Classify + route via Claude | Webhook + Claude |
| Follow-up | Scheduled sequences | Cron + email API |

### 3-Agent Pattern (from Stephen Pope)
Instead of one complex agent:
1. **Lead Enrichment Agent** — scrapes + researches + outputs JSON profile
2. **Outreach Agent** — generates personalized DMs/emails from profile
3. **Response Agent** — classifies responses, routes to Vapi or follow-up

Each agent has a SHORT prompt with EXAMPLES not RULES.

### Cross-Platform Session Normalization (from Stephen Pope)
All channels normalize to:
```
{ unique_id, message, platform }
```
Session ID starts as email → graduates to phone once captured → all history rewires.
Conversation never restarts across channels.

### Mid-Call Injection (from Stephen Pope)
When prospect books via Cal.com during Vapi call:
- Cal.com fires webhook
- Webhook calls Vapi control URL
- Injects "You're booked for [date]" into the live call
- Prospect hears confirmation while still on the phone

## Compliance

### CAN-SPAM (Email)
- Must include: physical address, unsubscribe link, honest subject line
- Must honor unsubscribe within 10 business days
- No deceptive headers

### FCC TCPA (Phone/SMS)
- NO outbound AI calling without prior express consent
- Inbound AI + consented callback = legal
- The demo number is INBOUND (they call us)

### Platform TOS (DMs)
- Instagram/LinkedIn have automation limits
- Start manual, automate carefully
- Risk: account suspension if too aggressive
- Mitigation: warm up accounts, personalize (not templates), low volume

## Metrics to Track

| Metric | Target |
|--------|--------|
| Emails sent/day | 50 |
| DMs sent/day | 20 |
| Open rate | >40% |
| Reply rate | >5% (cold), >15% (warm) |
| Demo calls/week | 10+ |
| Close rate (Vapi) | >10% |
| Cost per acquisition | <$200 |
| Revenue per client | $2K+ setup + $200/mo |

## What This Looks Like as a Claude Code Skill

```
ai-lead-gen/
├── .claude/
│   ├── CLAUDE.md (lead gen agent personality)
│   ├── skills/
│   │   └── lead-gen/
│   │       ├── SKILL.md
│   │       ├── reference.md
│   │       └── resources/
│   │           ├── dm-templates.md
│   │           ├── email-templates.md
│   │           ├── enrichment-schema.json
│   │           └── compliance-checklist.md
│   └── rules/
│       ├── can-spam-compliance.md
│       └── tcpa-compliance.md
├── scripts/
│   ├── scrape_prospects.py (Firecrawl)
│   ├── enrich_prospect.py (Claude API)
│   ├── generate_outreach.py (Claude API)
│   └── send_email.py (Gmail API)
├── examples/
│   └── sample_enrichment.json
└── README.md
```
