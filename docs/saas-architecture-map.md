# SaaS Architecture Map — SOMA SaaS, Ralph SaaS, Crystal Ball SaaS

**Author:** saas-mapper (Task #2) · **Date:** 2026-06-06
**Method:** Full reads of source files (cited inline). Marked `IS` (read from code), `UNCLEAR`
(not found / not wired), `MARKETING` (asserted in docs/HTML but not matched by the code page).
Faithful to code as source of truth; no invented features.

---

## 0. The shared origin (all three are the SAME template fork)

All three SaaS are forks of the **`nextjs/saas-starter`** template
(`github.com/nextjs/saas-starter`). The unmodified template README is still present verbatim in
both `/home/GOD/soma-saas/README.md` and `/home/GOD/ralph-saas/README.md` (titled "Next.js SaaS
Starter"). The fork process is codified in the `make-saas` skill, which is copied identically into
all three repos (`/home/GOD/soma-saas/.claude/skills/make-saas/SKILL.md` lines 23-39 list the
exact steps and name SOMA + Ralph as the reference examples).

**Common skeleton (IS — byte-identical across all three):**
- **Framework:** Next.js 15 (app router, server components, server actions). CB pins
  `next@15.6.0-canary.59` (`crystal-ball-alpha/package.json`).
- **DB:** Postgres via **Drizzle ORM**. Tables `users`, `teams`, `team_members`, `activity_logs`,
  `invitations` are identical (`*/lib/db/schema.ts`).
- **Auth (app/browser):** email+password, **bcrypt** hash, **jose JWT** stored in a cookie;
  route protection via `middleware.ts` + `lib/auth/session.ts` + `lib/auth/middleware.ts`.
- **Payments:** **Stripe** — `lib/payments/stripe.ts` (`createCheckoutSession`,
  `createCustomerPortalSession`, `handleSubscriptionChange`, `getStripePrices/Products`) +
  `app/api/stripe/checkout/route.ts` + `app/api/stripe/webhook/route.ts`. Subscription state lands
  on the `teams`/`workspaces` row (`stripeCustomerId`, `stripeSubscriptionId`, `planName`,
  `subscriptionStatus`). 14-day trial (soma) / 7-day (CB, ralph).
- **UI:** shadcn/ui (`components/ui/*`), Tailwind.
- **Template routes shared by all:** `app/(login)/{sign-in,sign-up}`, `app/(dashboard)/dashboard/
  {general,activity,security}`, `app/api/{team,user}/route.ts`.

Everything below is the **domain layer each fork added on top** of this identical skeleton.

---

## 1. SOMA SaaS — `/home/GOD/soma-saas`

### What it is
Marketed (`/home/GOD/aisaac/soma.html`) as **"SOMA-Class AI — Self Organizing Meta Architecture"**:
observe → validate → automate. The pitch is ontology + logic-layer intelligence ("the system knows
when something is wrong and self-corrects"), sold as a high-touch quarterly engagement with Isaac.

### Architecture
- **DB schema** (`lib/db/schema.ts`): template tables **+ `partners`** (white-label: `slug`,
  `appName` default `'SOMA'`, `logoUrl`, `primaryColor`/`accentColor`, `customDomain`,
  `revenueSharePct` default 25, `platformFeeCents` default 50000, `isActive`). `teams.partnerId`
  FK ties a tenant to a partner.
- **API routes** (`app/api/`): **only** the template `stripe/`, `team/`, `user/`. **There is NO
  SOMA/observe API route.** (IS — confirmed by full file listing.)
- **The SOMA engine** lives bundled in-repo at `soma-prolog/` (Python + SWI-Prolog, the
  `add_event` / POST `/event` validator on **:8091**). It is **deployed** but **not called by the
  frontend** (see §1 verification).
- **Pages:** `app/(dashboard)/observe/page.tsx` (the product surface), `partner-admin/page.tsx`
  (white-label admin), `pricing/page.tsx`, plus template dashboard pages. Nav (`(dashboard)/
  layout.tsx`) exposes **Observe** + **Plans**.
- **Auth:** app-only (JWT cookie). **No API-key layer** (unlike Ralph and CB).
- **Pricing tiers** (`pricing/page.tsx`, hardcoded array matched to Stripe products by name):
  **Personal $17 · Pro $99 · Business $499 · Enterprise $2500** /mo + a **VIP "Isaac Personally"
  partnership** CTA → `sancovp.github.io/aisaac/apply.html`. Matches `.claude/rules/pricing-tiers.md`
  and the `$17-2500/mo` in the root `CLAUDE.md`.
- **Deploy** (`fly.toml` + `Dockerfile`): **Fly.io, single multi-process container** run by
  **supervisord** — Next.js on **:3000** AND the SOMA Python/SWI-Prolog daemon on **:8091** (both
  ports exposed in `fly.toml`; `Dockerfile` installs swi-prolog + janus-swi + owlready2 + fastmcp
  and `pip install -e`'s `soma-prolog/`). Persistent volume `soma_data` → `/data` for OWL files +
  tenant data. `SOMA_OWL_PATH=/data/owl/soma.owl`.
- **White-label layer** (IS, partial): `lib/db/partner-queries.ts` (`getPartnerBySlug`,
  `getPartnerByDomain`, `getBrandingFromHost`, `getAllPartners`, `getPartnerTeams`) +
  `components/branding-provider.tsx` (React context injecting `--brand-primary`/`--brand-accent`
  CSS vars) + `partner-admin/page.tsx` (lists partners with rev-share %). The admin page is
  **display-only** — its "Add Partner" button is not wired to a mutation (UNCLEAR/not-built).
- **Design intent** (`.claude/rules/`): `soma-engine-is-backend.md` ("all validation goes through
  SOMA's POST /event entrypoint; never put validation logic in Next.js");
  `domain-shards-from-user-observations.md` (users at $17 farm domain OWLs that become pre-trained
  Pro-tier editions — "users create the product by existing").

### Concrete user journey (IS)
Sign up → land on `/observe` → type "what your team does" into a box → see observations tagged
`processing / validated (CODE) / needs-more-detail (SOUP) / compiled & scheduled`. Pay via
`/pricing` → Stripe checkout → subscription on the `teams` row.

### ⚠ VERIFICATION OF PRIOR FINDING — **CONFIRMED: the observe page is a mock**
`app/(dashboard)/observe/page.tsx` is a **client component with hardcoded demo data and NO network
call whatsoever** (IS — full read):
- Lines 18-38: `useState` seeded with **3 hardcoded observations** ("Alice processes invoices…",
  etc.) including a fake `soupGaps` list.
- Lines 40-60: `handleSubmit` pushes the typed text locally, then a **`setTimeout(…, 2000)`**
  (line 51) flips its status to `'soup'` with a **static string** ("Observation received — SOMA is
  validating. More detail needed to compile.").
- **There is no `fetch`, no call to `:8091`, no `/api` call** anywhere in the file. The "SOMA is
  validating" text is theater.
**Conclusion:** the SOMA daemon is real and is *deployed alongside* the app (supervisord/:8091),
but the **frontend↔engine wire does not exist**. The `observe` UI is a non-functional demo. This
directly contradicts the `soma-engine-is-backend` rule's intent — that wiring is VISION, not built.

---

## 2. Ralph SaaS — `/home/GOD/ralph-saas`

### What it is
**R.A.L.P.H. = Remote Automations & Language-agent Process Hub** (`README.md`, `ralph.html`): a
hosted **remote workforce** for an agent you already run. "Make Claude Code the manager. Give it
workers." schedule → execute → report. Explicitly positioned as the **labor** half of the pair
("SOMA = intelligence, Ralph = labor; Enterprise gets both" — `README.md` lines 7-11).

### Architecture (the most genuinely-wired of the three)
- **DB schema** (`lib/db/schema.ts`) — the richest, domain-specific:
  - `workspaces` (**replaces `teams`**; adds `slug`, `ownerId`, **`apiKey`** unique, `partnerId`,
    Stripe fields, `planName` default `'starter'`).
  - `partners` (white-label; `appName` default `'Ralph'`, `revenueSharePct` 25).
  - `repoConnections` (github repo + branch + installationId).
  - `jobConfigs` (`task`, `runtimeImage` default `ralph-python-node`, `agentConfig` jsonb,
    `expectedArtifacts`, `outputPr`).
  - `schedules` (`cron`, `dependsOn` jsonb, `oneShot`, `lastFiredAt`, `nextFireAt`).
  - `runs` (`status` queued→…, `workerHost`, `prUrl`, `artifactPrefix`, `logUrl`, `finalReport`).
  - `blockages` (`reason`, `resumeOptions` jsonb, `artifactUri`, `resolvedWith`).
- **API surface** (IS, real): **`app/api/v1/{jobs,runs,schedules,blockages}/route.ts`**, every one
  authenticated by **`x-api-key` header → `workspaces.apiKey` lookup** (`jobs/route.ts` lines 6-11
  is the canonical pattern, repeated in each). GET lists by workspace; POST inserts. `blockages`
  also has PATCH (resolve).
- **Local MCP hub** (`ralph-hub/ralph_hub_mcp.py`): a **FastMCP** server installed next to Claude
  Code. 8 tools (`create_job`, `list_jobs`, `create_schedule`, `list_schedules`, `run_now`,
  `list_runs`, `list_blockages`, `resume_blockage`) that hit `RALPH_API_URL/api/v1/*` with the
  `x-api-key` header (`_api()` lines 25-37). **This is the real, primary UX surface** (rule
  `mcp-first-interface.md` + `ralph.html`: "No dashboard needed").
- **Remote worker** (`worker/ralph_worker.py`): a **disposable poller** (run by the user/agency,
  not the cloud). `poll_loop` → `claim_run` (GET `/runs`, picks `status=='queued'`) → `execute_run`
  (git clone, `git checkout -b ralph/<id>/<ts>`, runs **`python3 -m compoctopus.agents.ralph.core
  --repo … --requirements … --model …`**, `gh pr create`, files a blockage on failure/timeout).
- **Auth:** app (JWT cookie) for the dashboard + **API-key** for the `/api/v1` machine surface.
- **Pricing:**
  - **MARKETING:** **$99/mo, BYOK** model keys; private-label **$297 setup + $99/mo**
    (`README.md` lines 41-45, `ralph.html`, `.claude/rules/{private-label-for-agencies,byok-model-keys,pricing-tiers}`).
  - **IS (the actual page):** `app/(dashboard)/pricing/page.tsx` is the **UNMODIFIED template** —
    tiers **"Base" / "Plus"** at **$8 / $12 per user/month** (defaults on lines 27, 39). ⚠ The
    pricing PAGE does not match the $99/mo marketing. The customization never happened on this page.
- **BYOK:** users supply their own model keys; routing via **uni-api** (`/tmp/uni-api`, Apache 2.0)
  per `byok-model-keys.md`. (uni-api integration is design-stated; no uni-api call found in the
  worker — UNCLEAR whether wired.)
- **White-label / private-label:** `partners` table exists, but **no `partner-admin` page** in
  ralph (soma has one; ralph does not). `private-label-for-agencies.md` says "same pattern as SOMA
  SaaS, use make-saas skill" — so the admin UI is VISION here.
- **Deploy** (`fly.toml` + `Dockerfile`): **Fly.io, simple single Next.js container** (node:20,
  `next start -p 3000`, 1gb). **No daemon, no supervisord** (unlike SOMA) — the worker runs
  elsewhere, disposably.

### Concrete user journey (IS)
Install the MCP hub next to Claude Code (set `RALPH_API_KEY`/`RALPH_API_URL`) → your agent calls
`create_job("weekly-docs", …)` → `create_schedule(42, "0 3 * * 5")` → a worker (you/agency run it)
polls, clones, runs ralph, opens a PR, and on trouble files a `blockage` with `resume_options` →
agent calls `resume_blockage(87, "open_partial_pr")`. (Verbatim demo in `ralph.html`.)

### Gaps found (IS — code does not match the data-flow doc)
- **No scheduler/cron dispatcher.** `README.md` line 36 says "Cloud Scheduler → queues run", but
  **no route or daemon fires `schedules` → `runs`** (no such file in `app/`). Schedules are stored
  but nothing actuates them. (UNCLEAR/not-built.)
- **`claim_run` is not an atomic claim.** `worker/ralph_worker.py` lines 36-47: to "claim", it
  **POSTs `/runs`, which `runs/route.ts` POST *inserts a new* queued run** rather than locking the
  existing one. Two workers would both pick the same run and create duplicates; the original run is
  never marked claimed/running. (IS — bug.)
- **`resume_blockage` doesn't re-queue.** `blockages/route.ts` PATCH marks the blockage resolved but
  the comment "queue a resume run" (line 30) is **not implemented** — no new run is inserted.

---

## 3. Crystal Ball SaaS — `/home/GOD/gnosys-plugin-v2/base/crystal-ball-alpha`

### What it is
The SaaS wrapper around the **Crystal Ball engine** (`lib/crystal-ball/`, the encoding compiler /
minespace / scry — `engine.ts` is **167 KB** of real engine code). Sold as a coordinate-space
"spaces" tool: "the full Crystal Ball engine — all primitives, all orders, full superposition"
(`pricing/page.tsx`). Per `canonical-source-dirs`, CB is a **separate repo** (`sancovp/crystal-ball`,
Next.js/TS SaaS) hosted on its own.

### Architecture
- **DB schema** (`lib/db/schema.ts`): template tables **+ `api_keys`** (prefixed `cb_live_` /
  `cb_test_`, `isActive`, `lastUsedAt`, `revokedAt`) **+ `spaces`** (`data` jsonb = a **serialized
  CrystalBall**, scoped to a `teamId`). **No `partners` table — no white-label layer** (unlike SOMA
  and Ralph).
- **API surface** (IS, real — calls the actual engine, not a mock):
  - **`app/api/cb/route.ts`** — the **one authenticated MCP-facing route**: `withApiKeyAuth` →
    `cb(auth.teamId, input)` (the real engine) → publishes the result on the **SSE event bus**.
    Accepts `{input}` / `{cmd}` / `text/plain`.
  - **`app/api/spaces/route.ts`**, `spaces/[space]/{scry,mine,seed}/route.ts`, `app/api/mine`,
    `app/api/cb/{flow,spaces}`, `app/api/crystal-ball` — the **visualizer routes**. These call the
    same real `cb()` engine **but with a hardcoded `DEV_TEAM_ID = 1` and NO auth** (CORS `*`). (IS —
    `spaces/route.ts` line 12, `scry/route.ts` line 11.)
  - **`app/api/events/route.ts`** — **Server-Sent Events** stream; frontends subscribe and receive
    live `cb_result` pushes.
  - `event-bus.ts` — in-process pub/sub singleton (on `globalThis` to survive HMR) connecting
    `/api/cb` → SSE clients.
- **Auth:** app (JWT cookie) for dashboard + **API-key (Bearer)** for the MCP/engine route
  (`lib/crystal-ball/auth.ts`: `withApiKeyAuth`, `generateApiKey`, `revokeApiKey`). Note the **viz
  routes bypass auth** with the dev team id.
- **Pricing** (`pricing/page.tsx`, customized — violet/dark theme): **Explorer $8/mo · Navigator
  $24/mo** (2 tiers; falls back to product names `Explorer`/`Base`, `Navigator`/`Plus`). Different
  tier names/prices from soma and ralph.
- **Deploy:** **UNCLEAR** — there is **no `fly.toml` and no `Dockerfile` at the CB root** (verified
  by listing). Per `canonical-source-dirs`, CB is hosted separately as `sancovp/crystal-ball`; the
  deploy config is not in this tree.
- **Frontend:** `app/mine/page.tsx` (the minespace visualizer; consumes `/api/spaces` + SSE).

### Concrete user journey (IS)
Two surfaces: (a) **Machine** — an MCP client sends `Authorization: Bearer cb_live_…` to
`/api/cb` with a coordinate string ("AIDA_Tweet 1.2") → the engine resolves it → result streamed
back over SSE. (b) **Visualizer** — the `/mine` page hits the no-auth `/api/spaces` viz routes
(dev team 1) to render the space. Billing via `/pricing` → Stripe (Explorer/Navigator).

---

## 4. Comparison table

| Dimension | SOMA SaaS | Ralph SaaS | Crystal Ball SaaS |
|---|---|---|---|
| Base template | `nextjs/saas-starter` | same | same |
| Stack | Next.js 15 / Drizzle / Postgres / Stripe / shadcn | same | same (next canary) |
| Domain tables added | `partners` | `workspaces`, `partners`, `repoConnections`, `jobConfigs`, `schedules`, `runs`, `blockages` | `api_keys`, `spaces` |
| Primary product API | **none** (only stripe/team/user) | **`/api/v1/{jobs,runs,schedules,blockages}`** | **`/api/cb`** + `/api/spaces/*` + SSE `/api/events` |
| Auth (app) | JWT cookie | JWT cookie | JWT cookie |
| Auth (machine API) | — (none) | `x-api-key` → workspace | `Bearer cb_*` → team (`withApiKeyAuth`); viz routes no-auth (DEV_TEAM_ID=1) |
| Backend engine | SWI-Prolog `soma-prolog/` :8091 | `compoctopus.agents.ralph.core` (in worker) | `lib/crystal-ball/engine.ts` (167 KB, in-process) |
| **Engine wired to product?** | **NO — observe page is mock** | **YES — hub+worker hit live API** | **YES — `/api/cb` calls real `cb()`** |
| MCP surface | — | `ralph-hub/ralph_hub_mcp.py` (FastMCP, 8 tools) | `/api/cb` is MCP-compatible (`{input}`/`{cmd}`) |
| Pricing (page IS) | $17 / $99 / $499 / $2500 + VIP | **Base $8 / Plus $12 (unmodified template)** | Explorer $8 / Navigator $24 |
| Pricing (marketing) | matches page | **$99/mo BYOK + $297 private-label** (≠ page) | matches page |
| White-label | `partners` + queries + branding + admin page (display-only) | `partners` table only (no admin page) | **none** |
| Deploy | Fly.io, **multi-proc supervisord** (Next+:8091), volume | Fly.io, **single Next container** (worker disposable, external) | **UNCLEAR** (no fly/Docker in tree; separate repo) |
| Live-push | — | polling (worker/hub) | **SSE event bus** |
| State store | Postgres + OWL files on `/data` volume | Postgres + (S3/R2 for artifacts per rule, not code-verified) | Postgres (`spaces.data` jsonb = serialized engine state) |

---

## 5. Synthesis — one program or separate?

### What they ARE today (IS): three separate apps, one shared skeleton
They are **three independent Next.js applications**, each its own fork of `nextjs/saas-starter`,
each with **its own Postgres, its own Stripe products, its own auth/login, its own dashboard**, and
(for SOMA/Ralph) its own Fly app. A user **runs them separately**: separate sign-ups, separate API
keys, separate subscriptions. There is **no shared identity, no shared billing, no single dashboard,
and no code path that lets one app call another.** So: **separate, not one program.**

The strongest coupling that exists in code is **negative**: the same template skeleton is
**triplicated** (three copies of identical `lib/auth`, `lib/payments`, `lib/db` template tables,
`app/(login)`, `app/api/{stripe,team,user}`). That is duplication, not integration. A schema fork
already diverged the tenancy model: SOMA/CB use `teams`; Ralph renamed it to `workspaces` + `apiKey`.

### What they are DESIGNED to be (MARKETING/VISION): one ecosystem, two halves + a substrate
The docs frame an ecosystem, not three products:
- **SOMA = intelligence** (observe→validate→automate) and **Ralph = labor**
  (schedule→execute→report). `ralph/README.md` (7-11): *"Same ecosystem. Enterprise gets both."*
  `ralph.html`: *"SOMA observes your business and validates what's real. R.A.L.P.H. executes what
  SOMA compiled. Together: your business understands itself AND acts on that understanding."*
- The **one intended cross-product seam** is: **SOMA compiles a validated process → that becomes a
  Ralph `jobConfig`/`schedule`.** This is the only real integration the narrative implies — and it
  is **NOT wired in code** (SOMA has no automation-output API at all; its observe page is a mock).
- **Crystal Ball is a different layer**, not part of the SOMA↔Ralph labor/intelligence pair. It is
  the encoding/compiler + visualizer substrate (the engine the rest of GNOSYS reasons *with*), and
  it ships no white-label/partner layer. It shares the SaaS template but is conceptually upstream.

### Shared infra & duplication (IS)
- **Shared (by template, not by runtime):** auth model, Stripe integration, Drizzle/Postgres
  pattern, shadcn UI, the `make-saas` skill + its `white-label-pattern.md` / `deployment-checklist.md`
  / `pricing-tier-template.md` resources (copied into each repo).
- **Duplicated:** the entire base skeleton ×3; the `partners` white-label table ×2 (SOMA, Ralph,
  with slightly different columns — SOMA has `platformFeeCents`/`accentColor`, Ralph uses `boolean`
  `isActive`).
- **Not shared:** databases, Stripe accounts/products, deploys, user identity.

### What a unified UX would require (VISION — to make it "one program run simultaneously")
1. **One identity/account** across all three (today: `teams` vs `workspaces` divergence must be
   reconciled; pick one tenancy model + one API-key table).
2. **One billing surface** — a single Stripe customer with a **bundle/Enterprise plan** granting
   SOMA + Ralph (+ CB) entitlements, instead of three separate subscriptions. (The "Enterprise gets
   both" promise needs one checkout, not two.)
3. **One dashboard** with tabs: SOMA *Observe* + Ralph *Jobs/Runs/Blockages* + CB *Spaces*.
4. **The real integration wire:** SOMA's compiled/validated automations → POST a Ralph `jobConfig`
   (+ optional `schedule`). This is the single seam that turns "intelligence" into "labor" and is
   the highest-value missing code (currently pure narrative).
5. **Shared white-label/partner table** (one `partners` row brands all surfaces a tenant sees)
   rather than two divergent copies.
6. **First wire SOMA's own engine to its own UI** — the prerequisite for #4, since today SOMA's
   product surface (`observe`) is a mock that never reaches the deployed :8091 daemon.

### Bottom line
- **IS:** three separate template-fork SaaS apps. **Ralph** and **Crystal Ball** have genuinely
  working product APIs (Ralph: `/api/v1` + MCP hub + worker; CB: `/api/cb` → real engine + SSE).
  **SOMA's product UI is a mock** — its engine is deployed beside the app but not connected.
- **DESIGNED:** an ecosystem where SOMA (intelligence) feeds Ralph (labor), with CB as the
  compiler/visualizer substrate. The labor↔intelligence integration and a unified account/billing/
  dashboard are **VISION, not built.** They compose into one program only on paper today.

---

## Appendix — primary files read (citations)
- Shared template proof: `soma-saas/README.md`, `ralph-saas/README.md`, `*/lib/payments/stripe.ts`,
  `*/lib/db/schema.ts`, `soma-saas/.claude/skills/make-saas/SKILL.md`.
- SOMA: `app/(dashboard)/observe/page.tsx` (mock — lines 18-60), `app/(dashboard)/pricing/page.tsx`,
  `app/(dashboard)/partner-admin/page.tsx`, `lib/db/partner-queries.ts`,
  `components/branding-provider.tsx`, `fly.toml`, `Dockerfile`, `.claude/rules/*`.
- Ralph: `lib/db/schema.ts`, `app/api/v1/{jobs,runs,schedules,blockages}/route.ts`,
  `ralph-hub/ralph_hub_mcp.py`, `worker/ralph_worker.py`, `app/(dashboard)/pricing/page.tsx`,
  `docs/ARCHITECTURE.md` (=README), `fly.toml`, `Dockerfile`, `.claude/rules/*`.
- CB: `lib/db/schema.ts`, `lib/crystal-ball/auth.ts`, `lib/crystal-ball/event-bus.ts`,
  `app/api/cb/route.ts`, `app/api/events/route.ts`, `app/api/spaces/route.ts`,
  `app/api/spaces/[space]/scry/route.ts`, `app/(dashboard)/pricing/page.tsx`, `package.json`,
  `.env.example` (no fly/Docker present).
- User framing: `aisaac/soma.html`, `aisaac/ralph.html`.

---

## 6. Seed Publishing + the "seed" systems

**Scope note:** these were added after the original 3-SaaS pass. The headline product is
**SeedPublishing**; the other `seed*` dirs are characterized for completeness. All full-read or
listed; paths cited; IS vs unclear marked.

### 6.1 SeedPublishing — IS (built) — the PUBLISHING / gated-community content surface
**Path:** `/home/GOD/seed_publishing_public/SeedPublishing/` (latest; git HEAD 2025-09-13 "Improve
authentication session handling"). A **Replit project** (`.replit` present).

**What it IS (from code):** a public-facing **read interface for a private CMS** that displays
**"compound intelligence QA conversations" (SEED/Carton format)** + a **wiki of concept files**
(markdown). `replit.md` (the design doc): "displays authorized and **redacted** AI-human collaboration
sessions… the public-facing interface for a private content management system."

**Stack (IS — DIFFERENT from the soma/ralph/CB Next.js trio):**
- **Express.js + TypeScript** backend (`server/{index,routes,storage,db,vite}.ts`), **Vite + React 18 +
  Wouter** frontend (`client/src/`), **shadcn/ui + Tailwind**, **Drizzle ORM + Neon serverless
  Postgres**, **express-session**. Not Next.js, not the `nextjs/saas-starter` fork. (`package.json`,
  `replit.md`.)
- Pages (`client/src/pages/`): `home`, `login`, `wiki`, `not-found`.

**DB schema (IS — `shared/schema.ts`):** ONLY **`members`** (email, name, addedBy default "zapier") +
**`api_keys`** (hashed key, memberId, isActive). ⚠ The `qa_conversations` / `io_pairs` tables described
in `replit.md` are **DESIGN, not built** — they are absent from `schema.ts`; wiki content is pulled
**from a GitHub repo** at runtime (`storage.refreshFromGitHub`), not stored in those tables.

**Auth + membership (IS — `server/routes.ts`):**
- **Triple auth** via `requireAuth`: (1) **session** (express-session), (2) **admin API key** (env
  `ADMIN_API_KEY`; admin identity hardcoded `fred@bento.com` — a placeholder/test account), (3) **per-user
  password** = a SHA-256-hashed row in `api_keys`. Signup auto-generates a "system password".
- **Membership is gated by Zapier**, not Stripe: `POST /api/members/add` + `/remove` authenticate via
  `x-api-key === ZAPIER_API_KEY`. So access is provisioned by an external Zapier flow (e.g. from wherever
  payment/community signup happens).
- **Protected wiki API** (all behind `requireAuth`): `/api/concept-files` (list/get), `/api/search`
  (filename/content + sort), `/api/stats`, `/api/refresh` (pull from GitHub).

**Monetization (IS/unclear):** **NO Stripe / no billing in this repo** (unlike the Next.js trio). Access
is membership-gated via Zapier → the actual payment/checkout surface lives **elsewhere** (UNCLEAR where —
not in this codebase). So SeedPublishing is the *gated content surface*, not the *biller*.

**Deploy (IS):** **Replit** (`.replit`, `.config/`, `.local/`) + **Neon** Postgres. Not Fly.io (unlike
soma/ralph). UNCLEAR if it was promoted off Replit.

**Role in the SaaS picture / relation to mapped products:** SeedPublishing is the **publishing /
members-only content layer** — it surfaces SEED compound-intelligence QA + a concept wiki to paying/invited
members. It is **standalone**: no code link to Jobworld, soma-saas, ralph-saas, or lamai-saas (no shared
DB, auth, or API). Conceptually it's the built instance of the **"Story Machine / content pipeline"** idea
in the aisaac `CLAUDE.md` (CartON → published content), and it is adjacent in spirit to **lamai-saas**'s
interpretive/social surface — but the two share no code. Its content **source** (CartON/SEED QA exported to
a GitHub repo of markdown) is the only conceptual tie to the rest of the stack.

### 6.2 seed-mcp — IS (built, but NOT a SaaS) — the SEED unified-identity MCP
**Path (canonical):** `/home/GOD/gnosys-plugin-v2/application/seed-mcp/` (per `canonical-source-dirs`;
`/home/GOD/seed-mcp.legacy_pre_monorepo` is the old pre-monorepo copy).
**What it IS:** an **MCP server** — "SEED — Unified System Identity for Compound Intelligence… one coherent
voice that coordinates everything behind the scenes." Current built feature = **`who_am_i(context="")`**
(`README.md`). Part of **STARSYSTEM**; coordinates STARLOG/etc. `SEED_STATE_MACHINE_SPEC.md` DESIGNS a
fuller "Compound Intelligence Operating System" — a hook-driven tool-sequencing state machine
("follow the yellow brick road") — which is **VISION/spec**, not the shipped `who_am_i` tool.
**Role:** a dev/agent-coordination tool, **not a SaaS product** and unrelated to SeedPublishing despite the
shared "seed" name (different "seed": SEED-the-agent-identity vs SEED-the-published-content).

### 6.3 Other seed* dirs (characterized, not full SaaS)
- **`/home/GOD/seed_publishing_fixed/`** + **`/home/GOD/seed_publishing_replit/SeedPublishing/`** — EARLIER
  snapshots of SeedPublishing (both git HEAD 2025-09-11, same commit "Use standard markdown rendering…").
  The `_replit` copy still has `node_modules` (the actual Replit checkout); `_public` is the newer,
  auth-hardened copy. = the same app at different points; `_public` is canonical.
- **`/home/GOD/seed_v0_publishing/`** — **SPEC docs only** (no app): `SEED_V0_SPEC.md`,
  `REDACTION_SYSTEM_SPEC.md`, `AUTO_REDACTION_AGENT_SPEC.md`, `LOCAL_WEBSERVER_SPEC.md`,
  `DEPRECATED_WEBSERVER.py`. The design predecessor — notably the **redaction system** (publish authorized +
  auto-redacted QA) that `replit.md` references as "authorized and redacted… sessions." DESIGN, not built
  here.
- **`/home/GOD/seed-ui-mcp/`** — a TypeScript **MCP** (`dist/`, `src/`, `package.json`); a UI-oriented seed
  MCP. Not read in depth (no README surfaced); flagged as a seed-prefixed MCP, IS-unclear beyond "a TS MCP".
- **`/home/GOD/seed_song/`** — **content/narrative drafts** (markdown: `compound_intelligence_mantra.md`,
  `aisaac_story_draft1.md`, `high_ticket_product_draft1.md`, `giint_blueprint_system.md`). Not a system —
  marketing/story material.

### 6.4 Seed-systems bottom line
- The only **SaaS-shaped** seed product is **SeedPublishing** — a gated members-only SEED-content wiki/QA
  browser, **Express/Vite/React/Drizzle/Neon on Replit**, membership via **Zapier** (no in-repo billing),
  **standalone** from the Next.js trio + lamai. Its "published content" is the conceptual bridge to the rest
  of the stack (CartON/SEED QA → GitHub markdown → this reader).
- **seed-mcp** is the unrelated **agent-identity MCP** (dev tool, STARSYSTEM), not a SaaS.
- The rest are **older snapshots, spec docs, a UI MCP, and content drafts**.
- **Appendix citations:** `seed_publishing_public/SeedPublishing/{replit.md, package.json, shared/schema.ts,
  server/routes.ts}`, `gnosys-plugin-v2/application/seed-mcp/{README.md, SEED_STATE_MACHINE_SPEC.md}`,
  dir listings of `seed_publishing_fixed`, `seed_publishing_replit`, `seed_v0_publishing`, `seed-ui-mcp`,
  `seed_song`.

---

## 7. Publishable-systems table (pattern view)

Tabular form of everything publishable, to surface patterns at a glance. Full 15-column data (incl.
repo_path, auth_model, publishes_what, depends_on, notes) is in **`publishable-systems.csv`** next to this
file; condensed below for inline reading. Cells grounded in code/this map; UNCLEAR marked.

| system | kind | stack | status | deploy | billing | tier/price | audience | relation |
|---|---|---|---|---|---|---|---|---|
| soma-saas | saas_app | Next.js+Drizzle+Stripe (+SOMA Prolog daemon) | partial | fly | stripe | $17/$99/$499/$2500+VIP | b2b+b2c | nextjs/saas-starter fork; observe wired to real engine |
| ralph-saas | saas_app | Next.js+Drizzle+Stripe (+Py hub+worker) | built | fly | stripe | $99 BYOK mktg / page Base$8 Plus$12 | dev | same fork; Ralph=labor pair to SOMA=intelligence (not code-wired) |
| lamai-saas | saas_app | Next.js+Drizzle+Stripe | partial | unclear | stripe | unclear | b2c+social | same fork; social/interpretive (Empathy Museum) |
| crystal-ball (hosted) | saas_app | Next.js+Drizzle+Stripe (+CB engine TS) | built | unclear (sep repo) | stripe | Explorer$8 / Navigator$24 | dev | same fork; compiler/visualizer substrate |
| bangerlab-saas | saas_app | Next.js+Drizzle+Stripe+Docker | partial | fly (unclear) | stripe | unclear | b2c content | same fork; logic in slop-saas-compiler |
| primalops-saas | saas_app | Next.js+Drizzle+Stripe+Docker | partial | fly (unclear) | stripe | unclear | b2c fitness | same fork; vertical sibling of bangerlab |
| slop-saas-compiler | engine | Python compiler+templates+nextjs-wrapper | built | none (build tool) | none | none | internal/dev | emits the SaaS funnels behind bangerlab/primalops |
| SeedPublishing | content_surface | Express+Vite+React+Drizzle+Neon (Replit) | built | replit | zapier | membership (price external) | b2c+community | DIFFERENT stack; standalone content reader |
| aisaac-site | site | static HTML | built | github_pages | none | none | b2b+b2c | top-of-funnel router into every product |
| seed-mcp | mcp | Python (MCP) | partial | none (pip/MCP) | none | none | dev | NOT a SaaS; agent-identity (who_am_i) |
| seed-ui-mcp | mcp | TypeScript (MCP) | unclear | none | none | none | dev | seed-prefixed MCP sibling |
| twi-jobworld | saas_app | Python (CAVE) + CC plugin + dashboard | built | docker/marketplace | none | community tiers (external) | b2c | the ORIGINAL *World |
| twi-healthworld | saas_app | Python (CAVE) + CC plugin + dashboard | built | docker/marketplace | none | none (funnel) | b2c | git fork of twi-jobworld |
| promptworld | saas_app | Python (CAVE) + claude -p backend + chat UI | built | unclear (local) | none | none | dev | same CAVE pattern; kept separate per Isaac |
| sanctum-builder | engine (builder lib) | Python+pydantic (sanctuary-system + life_architecture_app; NOT CAVE) | partial | none (via sancrev treeshell) | none | none (SANCTUM community tier) | b2c+internal | NOT a CAVE *World; the *-builder lib family (w/ paia-/cave-builder); writes heaven_data/sanctums |
| heaven_data | engine (substrate) | filesystem + chroma + CartON stores (~8.4GB runtime) | built | mount candidate (unclear) | none | none | internal | shared RUNTIME under the Python/CAVE/sancrev side; the 6 Next forks do NOT use it |
| marketplace-publishing | content_surface (distribution) | git repos + .claude-plugin/marketplace.json + CC plugin loader | built | github (/plugin marketplace add) | none | none | dev | the distribution layer for doc-mirror/autopoiesis/ralph/*World plugins; ship-a-plugin = build→publish |
| blog-system | content_surface | Python + metastack (RenderablePiece) → HTML | partial | github_pages (aisaac/blog) | none | none | b2b+b2c | feeds the aisaac funnel; "Story Machine" arm; renderer is pure template (NO LLM); auto CartON→blog not yet wired |

**Patterns (see message to team-lead):** two stack families (Next.js/saas-starter fork ×6 vs the CAVE-Python
*Worlds ×3 vs the one-off Express/Replit SeedPublishing vs static aisaac vs Python MCPs); billing splits
stripe (the 6 Next forks) / zapier (SeedPublishing) / none (CAVE *Worlds + engine + MCPs + site); built vs
partial is ~half-half; deploy clusters fly (Next forks) / docker-marketplace (*Worlds) / replit (Seed) /
github_pages (site).
