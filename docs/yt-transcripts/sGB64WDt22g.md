# Build an API in 2026 & Make SERIOUS Money

**Video:** https://www.youtube.com/watch?v=sGB64WDt22g
**Channel:** Olly Rosewell (@OBRosewell)
**Duration:** 16:13
**Upload Date:** 2026-03-17
**Views:** ~89,000
**Extracted:** 2026-05-04

---

## Core Thesis

**In 2026, the most profitable solo-founder SaaS model is building APIs — not apps with UIs — because AI agents consume APIs, not dashboards.** The entire agentic AI ecosystem (Cursor, Claude tool use, OpenAI function calling, n8n, Zapier, Make, Pipedream) resolves to the same thing: making HTTP requests to API endpoints. If your product is callable via API, you become a building block that agents recommend and developers embed.

---

## Key Arguments

### 1. AI Agents Don't Browse — They Call APIs
- Agents can't click buttons, navigate onboarding flows, or drag-and-drop
- They can only query structured endpoints
- Every AI agent framework (Claude tool use, OpenAI, etc.) resolves to API calls
- Being an API means you're a tool agents can autonomously select and use

### 2. API Stickiness > SaaS Stickiness
- **SaaS stickiness** = workflow/UI habit lock-in (fragile — better UI comes along, users switch)
- **API stickiness** = code-level lock-in (structural — ripping out an API means rewriting code, retesting, redeploying)
- Your customer isn't a person clicking a dashboard — it's a line of code in a system
- That line of code doesn't churn because it saw a competitor's ad
- Multiply by thousands of codebases = massive structural moat

### 3. Revenue Scales With Usage, Not Seats
- More users of the app that uses your API = more API calls = more revenue
- Every time a workflow runs, it calls your endpoint
- Per-credit / per-call pricing model (not per-seat)

### 4. Distribution Is Automatic
- Every new automation platform (Zapier, Make, n8n, Pipedream) = another distribution channel
- You don't build integrations — the API IS the integration
- AI coding tools (Cursor, Lovable) recommend your API when developers describe tasks

---

## Real Examples Cited

| Company | What It Does | Revenue/Status |
|---------|-------------|----------------|
| **ScreenshotOne** | Send URL, get screenshot image back | Solo founder, tens of thousands MRR |
| **Postie** | Open-source social media posting API | $60,000/month |
| **Resend** | Email sending API for developers | Used daily, growing with every developer |
| **ZoomInfo** | Send company domain, get employee emails | Billions (NASDAQ listed) |

---

## API Product Ideas for Solo Founders

1. **PDF Generation API** — Send data, get styled PDF back. Reports, invoices, receipts, proposals. Price per document.
2. **Social Proof Screenshot API** — Send tweet/LinkedIn URL, get beautiful screenshot image. Price per screenshot.
3. **Website Change Monitoring API** — Send URL, API checks periodically, returns diffs. Competitor research, price monitoring, compliance. Price per monitored URL.
4. **Text-to-Audio API** — Send text, get MP3. Content repurposing, podcasting tools. Price per minute of audio.
5. **Email Verification API** — Send email address, get deliverability status. Every outreach/cold email agent needs this. Very easy to build.
6. **Email Retrieval/Enrichment API** — Send company domain, get employee list + emails. Companies making millions with this exact model.

---

## Technical Build Process (for non-coders)

### Stack: Cursor + Supabase + Vercel
- **Total cost to production:** $0-20
- **Total time:** Less than 1 day

### Steps:
1. **Set up accounts** on Cursor, Supabase, Vercel
2. **Scaffold in Cursor** (~1 hour) — Use the PRD prompt (see below) to define architecture. Push back on over-complexity. Minimum files.
3. **Set up Supabase tables** — API keys table (id, key, email, created_at, requests_used, requests_limit) + usage_logs table. Use SQL editor.
4. **Build endpoint logic** — Tell Cursor exactly what input/output you want. Test locally with curl. Paste errors back into Cursor for fixes. This back-and-forth IS the vibe coding workflow.
5. **Deploy to Vercel** (~15 min) — Push to GitHub, import to Vercel, add env vars, click deploy. Live API with public URL.
6. **Build landing page** — What the API does, pricing (per-credit), sign up. Style with Tailwind/shadcn. One page.
7. **Add auth + billing** — Supabase auth for login, Stripe checkout for payment. Webhook upgrades request limits on payment success.
8. **Write documentation** — This matters MORE than you think because agents need docs to discover and use your API. Ask Cursor to generate docs explaining API keys, endpoints, and functionality.

### Validation Before Polish:
- Post landing page in relevant communities
- Offer 500 free API calls to first 50 signups
- **Signal to look for:** Are developers actually integrating your API into their workflows?
- If they sign up but never call the endpoint = product doesn't solve a real problem

---

## Key Prompts from Description

### PRD Scaffold Prompt:
```
I want to build a simple API product using Next.js and Vercel.
The API does one thing: [describe your API function here].
Tech stack: Next.js with App Router, TypeScript, Vercel, Supabase.
I need:
1. API route at /api/v1/[your-endpoint]
2. API key auth via x-api-key header
3. Supabase "api_keys" table
4. Supabase "usage_logs" table
5. Middleware for key check + usage + rate limiting
6. Endpoint logic
7. Simple landing page
Do NOT write any code yet. First, outline the file structure and database schema.
```

### Supabase SQL Prompt:
```
Generate the SQL CREATE TABLE statements for the api_keys and
usage_logs tables. Include Row Level Security policies that allow
the service role to read and write but block public access.
```

---

## Frameworks / Mental Models

### The API-as-Default-Tool Framework
1. Build a simple API that does ONE thing well
2. Make it reliable + write clean docs
3. Get embedded inside AI coding flows (Cursor, Lovable recommend you)
4. Every new automation platform = free distribution channel
5. Code-level lock-in compounds over time

### The Validation Signal
- People signing up = vanity metric
- People calling your endpoint from their code = real signal
- If no API calls after signups, pivot the product

---

## Relevance to Isaac's Business

### Direct Parallels:
- **OPERA/GNOSYS as API:** Isaac's system IS an API-first architecture. MCP tools ARE APIs. The thesis validates building tools that agents call rather than UIs humans click.
- **Egregore Compiler output:** Each compiled business system exposes APIs that other agents/systems can call. The compiler produces API-first businesses.
- **Stickiness model:** Once a PAIA integrates OPERA tools into workflows, switching cost is structural (code-level), not emotional. This is exactly the moat Isaac is building.
- **Pricing model:** Per-usage pricing (like the API examples) maps to Isaac's $200/mo usage model for voice agents and tools.

### Differences / Where Isaac Goes Further:
- Olly is teaching solo founders to build single-endpoint APIs. Isaac is building the COMPILER that generates these.
- Olly's APIs are stateless utilities. Isaac's system is stateful compound intelligence (CartON, starlogs, GIINT hierarchies).
- Olly's distribution is "hope Cursor recommends you." Isaac's distribution is the cohort/community/mastermind funnel where every participant gets a PAIA that uses OPERA APIs.
- L7 (emergence engineering) is the moat Olly can't touch — the human-AI team that builds human-AI teams.

### Actionable for Phase 1:
- The "500 free API calls to first 50 signups" validation pattern could work for TWI voice agent leads
- Clean docs matter for agent discovery — ensure OPERA/Jobworld APIs have excellent documentation
- The per-credit pricing model validates Isaac's per-usage pricing structure
