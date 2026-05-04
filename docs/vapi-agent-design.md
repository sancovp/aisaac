# Vapi AI Demo Agent — Design Doc

Last updated: 2026-05-04

## Purpose
The AI demo agent is the FIRST touchpoint for qualified B2B leads. It replaces the "book a call" step with a live AI conversation that can close deals, book Isaac, pitch B2C, or nurture — in that order.

## Trigger
- Qualified lead clicks "Get a Demo" / "Yes — show me a demo" on the site
- Lead has already self-qualified via the index survey (business owner, $10K+/mo revenue)
- Context from survey answers is passed to the agent (revenue tier, bottleneck, timeline, selected offer)

## Agent Cascade (5 steps, in order)

### Step 1: Demo + Close
- Agent greets, references their selected offer and survey answers
- Walks them through what the automation does for THEIR business (personalized)
- Pitches the grand slam: $1,200/mo first month ($1,000 retainer + $200 voice agent usage)
- If they say yes → Step 2 (SMS close)
- If they hesitate or say no → Step 3 (book Isaac)

### Step 2: SMS Purchase Link
- "Great — I can text you a secure link right now. What's your number?"
- Agent triggers SMS via Twilio/Vapi webhook → Stripe checkout link
- Lead completes purchase on phone while on the call
- Agent confirms, explains next steps (onboarding email, first meeting scheduling)
- DONE — they're a client

### Step 3: Book Isaac
- "No problem. Let me set you up with Isaac directly — he'll answer anything I couldn't."
- Agent uses SETTER TOOL: cal.com API to book a discovery call
  - Needs: cal.com API key, available slots query, booking creation
  - Pre-fills: name, email, selected offer, survey answers (Isaac sees context before the call)
- "You're booked for [date/time]. You'll get a confirmation email. Isaac will have your info."
- If they don't want a meeting either → Step 4

### Step 4: Pitch B2C
- "Got it. There's actually a really good option for learning this yourself."
- Pitches the cohort ($997/$1997) — "It teaches the exact system Isaac uses, all 7 levels"
- Mentions the free blog content and learn path
- If they're interested → sends link to learn.html or cohort signup (when live)
- If not → Step 5

### Step 5: Nurture
- "Totally fine. Can I get your email? I'll send you useful stuff — no spam, unsubscribe anytime."
- Captures email → adds to nurture list
- Nurture sequence (email automation, TBD):
  - Day 0: "Here's the blog posts most relevant to [their bottleneck]"
  - Day 3: Framework PDF related to their industry
  - Day 7: Case study / testimonial
  - Day 14: "Still thinking about it? Here's what changed for [similar business]"
  - Day 30: "Spots are open again — want to revisit?"
- Agent signs off warmly

## Tools the Agent Needs (Vapi function calling)

| Tool | Purpose | Integration |
|------|---------|-------------|
| `book_isaac` | Query cal.com slots, create booking | cal.com API v2 |
| `send_sms` | Send Stripe checkout link | Twilio SMS API |
| `capture_lead` | Store email + context to CRM/list | Formspree or custom endpoint |
| `get_survey_context` | Read lead's survey answers | localStorage → passed via webhook |
| `transfer_to_isaac` | Live transfer if Isaac is available | Vapi transfer action |

## Vapi Configuration

```
Platform: Vapi (vapi.ai)
Model: GPT-4o or Claude (Vapi supports both)
Voice: Professional male or female (TBD — test both)
First message: Dynamic based on survey context
Cost: ~$0.13-0.31/min (Vapi pricing)
Max call duration: 10 minutes
Silence timeout: 30 seconds
```

## Data Flow

```
Site survey → localStorage
  → "Get a Demo" click
    → Vapi widget loads with context payload:
      {
        selected_offer: "AI Phone Agent",
        revenue: "20-50k",
        bottleneck: "leads",
        timeline: "now"
      }
    → Agent personalizes conversation from payload
    → Agent actions write to:
      - cal.com (bookings)
      - Twilio (SMS)
      - Email list (nurture)
      - Stripe (purchases)
```

## Nurture System (separate from Vapi, triggered by it)

### Email sequences needed:
1. **Post-demo-no-buy** — they liked the demo but didn't purchase
2. **Post-demo-no-meeting** — they didn't want Isaac either
3. **Post-demo-b2c** — they went to the school path
4. **Post-demo-nurture** — just gave email, lowest intent

### Lead magnet assets to create:
- "The 30-Day System Audit" (already a blog post → make it a PDF)
- "7 Engineering Disciplines" cheat sheet
- "AI Automation ROI Calculator" (simple spreadsheet)
- Framework PDFs from existing blog posts

## What Isaac Sees (pre-call context)

When a lead books through the AI agent, Isaac's cal.com booking includes:
- Lead name + email + phone
- Selected offer
- Revenue tier
- Bottleneck
- Timeline urgency
- Whether they heard the $1,200/mo offer and declined
- Agent's notes on objections/hesitations

This means Isaac NEVER goes into a call blind. He knows exactly what was pitched and why they said no.

## Implementation Order

1. [ ] Create Vapi account + configure agent
2. [ ] Write agent system prompt with cascade logic
3. [ ] Set up cal.com API integration (book_isaac tool)
4. [ ] Set up Twilio SMS (send_sms tool)
5. [ ] Create Stripe checkout link for grand slam offer
6. [ ] Wire site "Get a Demo" button to Vapi widget
7. [ ] Set up email list + nurture sequences
8. [ ] Create lead magnet PDFs from blog content
9. [ ] Test full cascade end-to-end
10. [ ] Go live
