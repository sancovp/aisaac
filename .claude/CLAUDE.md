# AIsaac Site — TWI

Static site at sancovp.github.io/aisaac/. GitHub Pages. Mercurial Cyberglass theme.

## The Sanctuary System IS Everything

Not a product. The totality. A way to run your life so everything compounds. Every domain, page, funnel, and piece of content is a facet of the Sanctuary System.

## Domain Architecture (12 domains)

1. **PAIAB** — agent building (community PAIAB tier)
2. **SANCTUM** — life architecture (community SANCTUM tier)
3. **CAVE** — business automation (community CAVE tier + B2B)
4. **STARSYSTEM** — development workflow (part of PAIAB tier)
5. **SANCREV** — the game (contains 1-4)
6. **SANCREV: OPERA** — the open source engine (lead magnet for all funnels)
7. **Jobworld** — commercial product (B2B + B2C entrepreneur)
8. **UNICORN** — business model thesis ($1M x $1K)
9. **Story Machine** — content pipeline (CartON → JourneyBlog → blog/video/book)
10. **The Sanctuary System** — the myth, the totality (deepest funnel)
11. **Mahajalakala / CFD** — philosophical foundation (deepest funnel)
12. **Level10+** — Isaac's personal journey (personal hero funnel)

## Page Inventory (19 pages + 27 blog posts)

### Router
- `index.html` — 4-funnel survey (Sanctuary System / B2B / Wantrepreneur / PAIAB)

### B2B Family (sticky bar: "Book a Call" + qualification modal)
- `transform.html` — services + demo consent cascade
- `advertorial.html` — paid ad pre-lander, Chad Funnel pattern [PLACEHOLDER]
- `pricing.html` — hidden one-sheet, sent on calls only. NOT linked from nav.
- `phone-agent.html` — voice agent details

### Community Family (sticky bar: "Join Sanctuary Revolution")
- `join.html` — Sanctuary Revolution tiers (PAIAB/SANCTUM/CAVE/All) + waitlist
- `school.html` — Dr Capitalism MIFGE, wantrepreneur path
- `free.html` — free tools bento grid
- `agents.html` — free agent repo showcase [PLACEHOLDER]
- `jobworld-premium.html` — B2C entrepreneur, $997→$40/mo value stack [PLACEHOLDER]

### Product
- `build.html` — Jobworld
- `opera.html` — SANCREV OPERA (4 facets: PAIAB/SANCTUM/CAVE/STARSYSTEM)
- `gnosys.html` — GNOSYS
- `soma.html` — SOMA

### Deep
- `sanctuary-system.html` — the myth, the allegory [PLACEHOLDER]
- `level10.html` — Isaac's journey, Level10+ [PLACEHOLDER]

### Meta
- `learn.html` — curriculum
- `frameworks.html` — framework index
- `apply.html` — qualification fallback (JS-off)

### Blog
- `blog/` — 27 posts mapped by facet (PAIAB/SANCTUM/CAVE), level (L1-L7), and book bucket

## CTA Families

`sticky-cta.js` detects page family and shows contextual CTAs:
- **B2B pages:** "Book a Call" → qualification modal → Vapi demo cascade
- **Community pages:** "Join Sanctuary Revolution" → join.html
- **Blog posts:** auto-detected from category CTA class (transform→B2B, else→community)
- **Default/unknown:** "Find Your Path" → index.html survey
- **Hidden on:** index.html, join.html, apply.html

## Four Funnels

### B2B: "I need AI in my business"
index survey → transform.html → click any offer → demo consent → Vapi AI call
→ Close: SMS purchase link / Book Isaac / Pitch school / Nurture
→ Design doc: `docs/vapi-agent-design.md`

### Wantrepreneur: "I want to make money with AI"
index survey → school.html → Dr Capitalism MIFGE → cohort ($997) → mastermind
→ Book: "The Wantrepreneur's Guide" ($2.99 Amazon tripwire)
→ Outline: `books/wantrepreneur-guide/OUTLINE.md`

### PAIAB/Learn: "I want to build AI agents"
index survey → free.html → agents.html → individual repos → Jobworld Premium
→ Community: join.html PAIAB tier

### Sanctuary System: "The full vision"
index survey → opera.html / sanctuary-system.html → Level10+ → community All Access
→ Books: "The Sanctuary System" + "Level10+"
→ Outlines: `books/the-sanctuary-system/OUTLINE.md`, `books/level10plus/OUTLINE.md`

## Value Stack

```
Jobworld (the app)                     = free
+ Self-interpreting skill system       = the real value
+ All 27+ frameworks                   = $997 anchor
+ Marketing skills (AIDA, Hormozi)     = $500 worth
+ Lead gen + content + ad agents       = $500 worth
─────────────────────────────────────
Stack value: $2,000+
Community membership: ~$40/mo
B2B clients: included in $200/mo upkeep
```

## Content Rules

- No dollar amounts on public B2B pages. Numbers are on pricing.html only.
- Blog posts have category CTAs (transform/build/learn) before the footer.
- 81 AI-IMAGE placeholders — each must install a belief or overcome an objection.
- The joke (L1 voice agent = 10 min setup) is NEVER on the site. Structural, discovered by client.
- The site IS the case study. Never fake case studies. Point at the system itself as proof.
- Funnel depth IS initiation depth. Each level of the value ladder is a deeper level of the language world.
- Every image installs a belief or overcomes an objection.

## Auto-Content Pipeline (not yet wired)

CartON concepts → JourneyBlog AIDA fractal template → rendered HTML → blog.
- **Template**: `cave_discord_fork/templates.py` → `JourneyBlog` — AIDA within AIDA
- **Renderer**: `cave_discord_fork/renderers.py`
- **Target**: `blog/` — must match blog-style.css + include category CTA

## Design Docs (in `docs/`)

- `vapi-agent-design.md` — AI demo call cascade (5 steps, tools, data flow)
- `lead-gen-design.md` — 5-filter lead scoring, hyperpersonalized outreach
- `execution-plan.md` — Phase 1 (Claude Code only) → Phase 2 (STARSYSTEM recompile)
- `competitive-tally.md` — Puru/Rosewell/Mark/Ottley vs Isaac (brutal)
- `framework-architecture.md` — how 27 frameworks interrelate (dependency graph, layers)
- `domain-architecture.md` — 12 domains, nesting, the Sanctuary System as totality
- `blog-map.md` — all 27 posts mapped to facet/level/book/CTA/belief
- `cohort-design.md` — escape the self-sealing system, automated gamification

## Books (in `books/`)

- `wantrepreneur-guide/` — $2.99 Amazon, explains the joke, the meta-funnel
- `level10plus/` — Isaac's journey, personal hero tripwire
- `the-sanctuary-system/` — the myth, deepest layer tripwire

## Skills (in `.claude/skills/`)

36 marketing + video production skills: Hormozi (18), direct marketing (10), Expert Secrets (2), video pipeline (4), AIDA fractal (1), excalidraw render (1).

## Deploy

```bash
git add . && git commit -m "message" && git push
```
GitHub Pages deploys automatically from main branch.
