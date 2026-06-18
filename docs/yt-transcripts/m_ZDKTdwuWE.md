# AI Sales Agent That Sells 24/7 (Voice + Text + RAG)

**Source:** https://www.youtube.com/watch?v=m_ZDKTdwuWE
**Channel:** Stephen G. Pope (No Code Architects)
**Upload Date:** 2024-11-09
**Duration:** 27:13
**Context:** Stephen runs a $50K/mo business selling a "Content Engine Database" product for $5,000. This video shows his AI sales agent system that he uses to scale toward $100K/mo.

---

## Executive Summary

Stephen Pope demonstrates a complete AI sales agent system built in n8n that handles leads across WhatsApp, SMS, Telegram, email, and voice (Vapi). The system maintains conversation continuity across all channels using a cross-platform session ID, qualifies leads, answers product questions from a RAG database, and books calls — all automatically. The key architectural insight is using THREE separate simple agents instead of one complex one, and normalizing all channel inputs into a unified session ID keyed on email.

---

## System Architecture

### Core Platform: n8n (Automation Orchestration)
- All workflows built in n8n (self-hosted automation platform, similar to Make/Zapier but more powerful)
- Multiple interconnected automations handling different concerns

### Cross-Platform Session Management (THE KEY INNOVATION)
1. **Input normalization**: A code node receives payloads from WhatsApp (Twilio), SMS, Telegram, email — each sends different data formats
2. **Extracts 3 fields from ANY channel**: unique identifier (phone number), chat input (message text), platform name
3. **Session ID strategy**: Starts with phone number as session ID, graduates to email once captured
4. **Airtable lookup**: Searches for existing lead by phone number, returns email if found
5. **Session rewrite**: When lead is created with email, rewrites ALL existing Supabase chat history from phone-number-keyed to email-keyed
6. **Result**: Lead can start on WhatsApp, continue on email, call the voice agent — conversation is seamless, never restarts

### Three-Agent Architecture (CRITICAL DESIGN DECISION)
Stephen explicitly recommends splitting into 3 simple agents rather than 1 complex one:

1. **Lead Creation Agent**: Asks for name, company, email. Creates lead in Airtable. Short system prompt.
2. **Goal Gathering Agent**: Asks about business goals, main blocker, dream outcome. Stores in Airtable fields.
3. **Product Questions Agent**: Answers questions using RAG database. Handles call booking.

**Why 3 agents**: "The more simple you make your agents, especially in n8n, the better they work." Complex agents with long system prompts and many edge cases break. Simple agents with lots of EXAMPLES (not rules) in the prompt perform better.

A simple switch statement routes incoming messages to the correct agent based on lead status.

### Output Routing
All three agents map back through a single output switch that routes responses to the originating platform (WhatsApp, SMS, email, etc.) based on the tracked platform variable.

---

## Tech Stack / Tools / APIs

| Component | Tool | Purpose |
|-----------|------|---------|
| Automation orchestration | **n8n** | All workflows, webhooks, routing |
| CRM / Lead database | **Airtable** | Lead records (name, email, phone, company, goals, blockers, dream outcome) |
| Chat history + RAG vectors | **Supabase** (Postgres) | Session management, vector embeddings, chat history |
| WhatsApp integration | **Twilio** | WhatsApp business messaging |
| Voice agent | **Vapi** | AI voice calls, real-time conversation |
| Call booking | **Cal.com** | Scheduling, webhook on booking confirmation |
| Email | **Gmail** | Draft creation, inbox processing, spam filtering |
| Link shortening | Custom workflow node | Converts long URLs to short links for SMS/WhatsApp |
| Video transcription | n8n workflow | Auto-transcribes uploaded YouTube videos for RAG ingestion |
| AI model | Not specified (likely OpenAI) | Powers the 3 agents |

---

## RAG Database Architecture

### Knowledge Base Management
- **Supabase** stores vector embeddings + metadata
- **Airtable** is the user-friendly management layer for products and documents
- Products defined in Airtable with: name, alternative names/abbreviations, description, price, ideal client, bad client, lead magnet URL, buy now URL, sales call link

### Document Ingestion Pipeline
1. Upload video (YouTube or file) to Airtable via form
2. Provide: source URL, source ID, context description, product association
3. n8n automation auto-transcribes the video
4. Transcription stored back in Airtable as attachment
5. Automatically indexed into Supabase vector database
6. Can refresh/re-index at any time by toggling checkboxes in Airtable

### RAG Query Flow
- User asks product question via any channel
- Agent searches vector database with the question
- Returns answers with source URLs (testimonials, product pages, demos)
- Links auto-shortened for SMS/WhatsApp delivery

---

## Lead Qualification Flow

1. **Initial contact** (any channel) → Lead Creation Agent
   - Collects: name, company, email (won't proceed without all three)
   - Creates lead in Airtable
   - Rewrites session ID from phone to email

2. **Goal gathering** → Goal Gathering Agent
   - Asks: business goals, main blocker, dream outcome
   - Stores all in Airtable lead record
   - Won't answer product questions until goals are captured

3. **Product engagement** → Product Questions Agent
   - Answers from RAG database
   - Provides testimonials with links
   - Handles call booking flow

4. **Call booking** (text flow):
   - Confirms price first ("$5,000 — does that fit your budget?")
   - Asks if ready to start this week or next (filters tire-kickers)
   - Looks for times in next 2 days (urgency)
   - Asks timezone
   - Books on Cal.com, sends Zoom link

5. **Call booking** (voice flow — different UX):
   - Voice agent sends booking link via SMS to phone on file
   - Stays on the line: "Pick your date and time, I'll wait here"
   - Cal.com webhook fires on booking → n8n → Vapi API (control URL) → injects confirmation into live call
   - Voice agent confirms: "Your call is set for Friday at 1pm"

---

## Email Processing / Spam Filter

- Incoming emails classified: product question vs. spam
- If sender is NOT in contacts AND message is NOT product-related → auto-move out of inbox
- Product questions → routed through same AI agent pipeline
- Responses created as Gmail drafts for review (not auto-sent)

---

## Key Engineering Patterns for Our System

### What to replicate:
1. **Cross-platform session ID normalization** — phone number → email graduation. This is the core pattern for multi-channel lead tracking.
2. **Three simple agents > one complex agent** — decompose by lead lifecycle stage. Each agent has a short prompt with EXAMPLES not RULES.
3. **Airtable as friendly CRM + Supabase as vector/session store** — manage in Airtable, compute in Supabase. For us: Airtable → our CRM equivalent, Supabase → CartON/CAVE.
4. **Link shortening for mobile channels** — critical UX detail.
5. **Voice agent mid-conversation injection via API** — Cal.com webhook → Vapi control URL. This is how the voice agent "knows" about events that happen outside the call.
6. **Video transcription → RAG pipeline** — upload video, auto-transcribe, auto-index. Knowledge base grows from content.
7. **Draft-first email responses** — don't auto-send, create drafts for review. Safety net.
8. **Budget + readiness qualification before booking** — reduces no-shows and tire-kickers.

### What to improve on:
1. **No social media scraping / hyperpersonalization** — Stephen's system is reactive (waits for inbound). Our system should be PROACTIVE (scrape socials, personalize outreach).
2. **No cold outreach** — no DM automation, no cold email sequences. This is a gap we fill.
3. **n8n dependency** — we can build this natively in CAVE/SDNA without n8n.
4. **No lead scoring** — no automated prioritization of leads. We can add this.
5. **Manual product setup** — we can auto-generate product knowledge from website scraping.

---

## Relevance to Our Hyperpersonalized Lead Gen System

This video provides a solid INBOUND sales agent reference architecture. Our system needs to ADD:
- **Outbound**: Social media scraping (LinkedIn, Twitter/X, Instagram) → lead enrichment → personalized DM/email sequences
- **Hyperpersonalization**: Use scraped social data to customize every message
- **Cold outreach automation**: Automated DM sending, cold email sequences (CAN-SPAM compliant)
- **Lead scoring**: AI-driven prioritization based on engagement signals
- **Multi-touch sequences**: Not just respond to inbound, but initiate outbound campaigns

The cross-platform session management and three-agent architecture from this video are directly applicable patterns.
