# The Unification Transformation — how the systems become one architecture

**Author:** saas-mapper · **Started:** 2026-06-06 · **Version:** v1 (iterative; will be extended)
**Status discipline:** `IS` = read from code / verified in my maps; `VISION` = proposed target, NOT
built; `OPEN` = an architecture decision that is **Isaac's to make** — recorded, not auto-decided.
**Grounding:** every claim cites one of the maps already produced —
`publishable-systems.csv`, `saas-architecture-map.md` (§0/§5/§6/§7), `worlds-and-promptworld-map.md`,
`observatory-compoctopus-architecture.md`. This is a **design proposal**, not a proven plan; it is
exciting only to the degree each step below is actually built + verified (none are yet).

---

## 0. The problem this transformation solves (IS — the recurring finding)

Across every system mapped, one pattern recurs (saas-architecture-map §7 patterns; sanctum-builder +
heaven_data findings): **lots of shared TEMPLATES, almost no shared RUNTIME.**

- **6 Next.js `nextjs/saas-starter` forks** — soma-saas, ralph-saas, lamai-saas, crystal-ball,
  bangerlab-saas, primalops-saas — share the *template* (auth/Stripe/Drizzle skeleton) but each has its
  **own Postgres, own Stripe account/products, own deploy**; zero shared runtime (saas-architecture-map
  §0, §7; CSV). 3 of 6 still carry the unmodified template README.
- **3 CAVE `*Worlds`** — twi-jobworld, twi-healthworld, promptworld — are CAVE-core + a domain layer,
  built **by manual cloning** (healthworld is a literal git fork of jobworld), **no shared base class**,
  with rename-drift (worlds-and-promptworld-map §1-2, §7).
- **`*-builder` libraries** — sanctum-builder, paia-builder, cave-builder — pydantic libs behind the
  sancrev treeshell (sanctum-builder finding).
- **heaven_data** (`/tmp/heaven_data`, 8.4 GB) — IS the shared runtime substrate (skills/agents/sanctums/
  CartON/cave) **for the Python/CAVE/sancrev side**, but the 6 Next forks **do not touch it** (heaven_data
  finding). So a shared runtime *exists*, just not universally.
- **Billing is split** (CSV): Stripe = exactly the 6 Next forks; Zapier = SeedPublishing; none = the
  *Worlds, engines, MCPs, site.
- **Publishing is split across 4 targets** (CSV §6/§7): CC plugin marketplaces (github), PyPI
  (largechain), github_pages content (blog), gated members content (SeedPublishing).
- **The LLM engine is ALREADY unified** (observatory-compoctopus-architecture §C, §E): compoctopus,
  observatory, and largechain all call LLMs **only through the heaven framework** (Hermes/SDNA;
  BaseHeavenAgent/UnifiedChat) — differing only by model (MiniMax vs OpenAI). This is the one layer that
  is already coherent.

**So the transformation is NOT "build a shared runtime from scratch"** — it is **extend the runtime the
Python side already has (heaven_data + CartON + heaven-LLM + SOMA) to the parts that lack it (the 6 Next
forks), and collapse the 4 split layers (billing, auth/identity, publishing, deploy) into one each.**

---

## 1. The target unified architecture (VISION)

A single stack with four shared layers, under which every current system becomes a **configuration**, not
a fork.

```
                         ┌──────────────────────────────────────────────┐
   PUBLISHING LAYER ───▶ │ ONE publish service: plugins(CC marketplace) +│   VISION
   (collapse 4 targets)  │ pip(largechain) + content(blog/Seed) + sites  │
                         └──────────────────────────────────────────────┘
                         ┌──────────────────────────────────────────────┐
   BILLING / IDENTITY ─▶ │ ONE Stripe acct + entitlements + ONE account  │   VISION
   (collapse 6 Stripe)   │ (reconcile teams vs workspaces tenancy)        │
                         └──────────────────────────────────────────────┘
   PRODUCT LAYER ──────▶  *Worlds (CAVE+domain-config) · niche SaaS (make-saas+niche-config)
   (configs, not forks)   · content surfaces (Seed/blog) · MCPs · engines
                         ┌──────────────────────────────────────────────┐
   SHARED RUNTIME ─────▶ │ heaven_data (mounted) + CartON (KG: neo4j+    │   IS for Python side;
   (extend to all)       │ chroma) + heaven-LLM (Hermes/SDNA) + SOMA gate │   VISION to extend to Next forks
                         └──────────────────────────────────────────────┘
```

### 1.1 Shared RUNTIME (bottom) — VISION (extends an IS core)
- **heaven_data** becomes the **mounted shared data layer** for everything, not just the Python side.
  IS: it already is for CAVE *Worlds + sanctum-builder + skills + CartON + agents (heaven_data finding).
  VISION: the 6 Next forks mount/reach it (today each has its own Postgres). Isaac's "could mount that
  somewhere" is exactly this (heaven_data finding). **OPEN:** *how* a Next.js/Fly app consumes
  heaven_data — mount, or a service API over it? (decision below, §4 OPEN-1).
- **CartON (neo4j + chroma)** = the one knowledge store. IS: observatory writes/reads it live; the
  doc-mirror journal + most Python systems use it (observatory-compoctopus §B; CLAUDE.md). VISION:
  product content (SeedPublishing QA, blog source) is sourced from CartON uniformly.
- **heaven-LLM (Hermes/SDNA)** = the one LLM substrate. IS already (observatory-compoctopus §C/§E) —
  no change needed except making model/provider a config (MiniMax vs OpenAI vs Claude).
- **SOMA :8091** = the one validation gate. IS: a working event-sourced Prolog validator (I wired
  soma-saas's observe page to it, task #16). VISION: other write surfaces validate through it. **OPEN:**
  whether SOMA validation is mandatory or opt-in per product (§4 OPEN-4).

### 1.2 PRODUCT layer (configs, not forks) — VISION
- A **`*World` = CAVE-core + a domain-config** (departments/persona/skills/dashboard). IS: that is
  *already* what they are structurally (worlds map §cross-cutting) — the transformation is to replace the
  **manual clone** with a **single CAVE-core + a domain-config file** (kills rename-drift). **OPEN:** this
  is the "`*World` compiler" question Isaac **explicitly deferred / decided keep-separate** (promptworld
  journal 2026-06-01T14:59) — so this stays OPEN/Isaac-gated, NOT auto-built (§4 OPEN-2).
- A **niche SaaS = the make-saas template + a niche-config + slop-saas-compiler pages.** IS: bangerlab +
  primalops already follow this (slop-saas-compiler feeds them; CSV §6.x). VISION: soma/ralph/lamai/CB
  share ONE template instance (not 6 forks) parameterized by niche-config.
- **content surfaces** (SeedPublishing, blog) + **MCPs** + **engines** (slop-compiler, SOMA, CB) plug into
  the shared runtime.

### 1.3 BILLING + IDENTITY — VISION
- **One Stripe account + an entitlements service**: a single customer can hold a bundle granting
  soma+ralph+CB+… (the "Enterprise gets both" promise, ralph README, is impossible across 6 separate
  Stripe accounts today — observatory-... no, saas-architecture-map §2 ralph + §5). VISION: one checkout,
  entitlement flags per product.
- **One account/identity** across products. **OPEN:** the tenancy model is already forked — soma/CB use
  `teams`, ralph renamed it to `workspaces` + `apiKey` (saas-architecture-map §1-2). Reconciling to ONE
  model is the foundational identity decision (§4 OPEN-3).

### 1.4 PUBLISHING — VISION
Collapse the 4 split targets (CSV §6/§7) into one publish service with target adapters:
- plugins → CC marketplace (marketplace-publishing IS); pip → largechain (design-stage); content →
  blog (github_pages) + SeedPublishing (gated); sites → aisaac. VISION: one "publish" entrypoint that
  routes an artifact to its target. The doc-mirror `ship-a-plugin` flow is the closest IS seed.

---

## 2. Per-system transformation paths (where-it-is → unified target)

Each row: current state (IS, cited) → transformation steps (VISION) → end state.

### The 6 Next.js forks
- **soma-saas** — IS: template fork + bundled SOMA daemon; observe page now wired to :8091 (task #16);
  own Postgres+Stripe; fly. → (a) point its data at shared heaven_data/CartON instead of own Postgres;
  (b) move billing to the shared Stripe/entitlements; (c) keep the SOMA daemon (it IS the shared gate —
  promote it to the runtime layer, stop bundling per-app). End: soma = a niche-config of the shared
  template + the shared SOMA gate.
- **ralph-saas** — IS: real /api/v1 + MCP hub + worker; own Postgres+Stripe (saas-architecture-map §2).
  → reconcile `workspaces`→ the unified tenancy; shared billing; the worker/hub stay (they're the labor
  surface). The **SOMA→Ralph seam** (SOMA compiles → Ralph job) — the one designed-but-unwired cross-product
  integration (saas-architecture-map §5) — becomes a real call once both share identity+runtime.
- **lamai-saas / bangerlab-saas / primalops-saas** — IS: forks, partial/scaffold (CSV). → collapse into
  the shared template-instance + niche-config; bangerlab/primalops keep slop-saas-compiler as the page-gen
  engine. End: niche-configs, not forks.
- **crystal-ball** — IS: real engine + API + SSE; own Stripe; deploy unclear/separate repo
  (saas-architecture-map §4). → shared billing/identity; CB engine stays its own substrate (it's the
  compiler/visualizer layer). **OPEN:** CB is a separate repo (sancovp/crystal-ball) — does it fold in or
  stay a federated product? (§4 OPEN-5).

### The 3 CAVE *Worlds
- **twi-jobworld / twi-healthworld / promptworld** — IS: CAVE-core + domain, manual clones on heaven_data
  (worlds map). → replace clone with CAVE-core + domain-config (**OPEN/Isaac-gated**, §4 OPEN-2). They
  ALREADY share the runtime (heaven_data) — so for them the transformation is *de-duplication of the core*,
  not runtime-unification. **Constraint (IS):** Isaac said KEEP PROMPTWORLD SEPARATE for now (promptworld
  journal) — so promptworld is explicitly **out of scope** until Isaac re-opens it.

### Builders / engines / content / MCPs
- **sanctum-builder / paia-builder / cave-builder** — IS: pydantic libs on heaven_data (sanctum-builder
  finding; sanctum core is a STUB). → already on the shared runtime; transformation = finish the stubs +
  treat as the shared "domain-config authoring" libs for the product layer.
- **slop-saas-compiler** — IS: built page-gen engine feeding bangerlab/primalops (CSV §6). → becomes the
  shared "niche SaaS page" generator in the product layer.
- **SeedPublishing** — IS: standalone Express/Replit, Zapier membership, content from a GitHub repo
  (saas-architecture-map §6.1). → source its content from CartON (the shared KG) instead of a side GitHub
  repo; move membership/billing to the shared entitlements (drop the Zapier-only path). **OPEN:** keep its
  Express/Replit stack or re-home onto the shared template? (§4 OPEN-6).
- **blog-system** — IS: metastack template, CartON-sourced (when wired), github_pages; auto-pipeline
  not wired (CSV §6). → wire the CartON→JourneyBlog→HTML auto-pipeline as the shared content publisher.
- **marketplace-publishing / largechain** — IS: the plugin (github) + PyPI (design-stage) publish arms.
  → become target-adapters of the one publish service (§1.4).
- **heaven-bml** — IS: the GitHub-Issues-as-store kanban (architecture doc §D); the sqlite rewrite split
  it. → **OPEN:** which store is canonical for work-tracking in the unified arch — GitHub-native or local
  sqlite? (§4 OPEN-7). Tangential to product unification; flagged.

---

## 3. Shared vs per-vertical (the cut line) — VISION

| Layer | SHARED (one instance) | PER-VERTICAL (config/instance) |
|---|---|---|
| Runtime data | heaven_data (mounted), CartON (KG) | per-product namespaces within it |
| LLM | heaven Hermes/SDNA substrate | model/provider + system-prompt per agent (IS already) |
| Validation | SOMA :8091 gate | per-domain OWL/ontology |
| Auth/identity | one account/tenancy model | per-product entitlement flags |
| Billing | one Stripe + entitlements | per-product price/tier |
| Publishing | one publish service | per-artifact target adapter |
| Web template | one make-saas instance | niche-config + slop-compiler pages |
| *World core | one CAVE-core | domain-config (depts/persona/skills) |
| Deploy | **OPEN** (§4 OPEN-1) | per-product app, or one multi-tenant app |

The principle: **substrate + cross-cutting concerns are shared; domain identity is the per-vertical
config.** This is just making explicit what the *Worlds already are (CAVE+domain) and what the Next forks
*should* be (template+niche) instead of full clones.

---

## 4. OPEN decisions (Isaac's — recorded, NOT auto-decided)

These are genuine architecture forks; per doc-mirror discipline they are OPEN, surfaced to Isaac, not
resolved here.
- **OPEN-1 (deploy/runtime consumption):** how does a Next.js/Fly app consume heaven_data — bind-mount,
  or a service API over CartON/heaven_data? One multi-tenant app vs N apps sharing a backend?
- **OPEN-2 (`*World` compiler):** replace manual *World clones with a CAVE-core + domain-config compiler?
  Isaac **explicitly deferred / "keep separate"** (promptworld journal 2026-06-01T14:59) — so this stays
  closed until Isaac re-opens it. Do NOT auto-build.
- **OPEN-3 (tenancy):** unify `teams` (soma/CB) vs `workspaces`+apiKey (ralph) into one model — which one?
- **OPEN-4 (SOMA gate):** is validation through SOMA :8091 mandatory for all write surfaces, or opt-in?
- **OPEN-5 (CB federation):** crystal-ball is a separate repo (sancovp/crystal-ball) — fold in or stay
  federated?
- **OPEN-6 (SeedPublishing stack):** keep Express/Replit, or re-home onto the shared template?
- **OPEN-7 (work-tracking store):** heaven-bml GitHub-native vs the sqlite rewrite — which is canonical?

---

## 5. Migration order / dependencies (VISION — the stage-DAG)

Front-load the cheap shared-layer foundations before per-product moves (braid: build the target before the
things that target it). Proposed order — each stage gated on the prior + its OPEN decision:

1. **Decide the foundations** (OPEN-1, OPEN-3): runtime-consumption shape + one tenancy model. *Nothing
   else can land coherently first* — these are the load-bearing decisions (cf. ralph `workspaces` vs soma
   `teams` divergence is already a cost).
2. **Stand up the shared runtime as a service** (VISION): heaven_data + CartON + SOMA reachable by both
   Python and Next apps (the Python side already has it — this is exposing it to the Next side).
3. **One billing/identity layer** (depends 1): single Stripe + entitlements + one account.
4. **Migrate the highest-value, most-built products first** onto 2+3: ralph-saas + soma-saas (both built;
   soma's gate already wired) → realize the **SOMA→Ralph seam** (the one real cross-product integration).
5. **Collapse the niche forks** (lamai/bangerlab/primalops) into template+niche-config (they're partial
   anyway — cheap to re-home).
6. **Unify publishing** (§1.4) — adapters for plugin/pip/content/site.
7. ***Worlds de-dup** — only if/when OPEN-2 is reopened by Isaac (promptworld stays out per his call).
8. **content surfaces** (SeedPublishing→CartON-sourced, blog auto-pipeline) onto the shared content layer.

Dependencies: 1 → 2 → 3 → 4 → {5,6,8}; 7 gated on OPEN-2. CB (OPEN-5) and heaven-bml (OPEN-7) are
side-decisions that don't block the spine.

---

## 6. Honest status (anti-sycophancy)

**None of §1–§5 is built.** What IS true: (a) the LLM engine is already unified (heaven); (b) the Python
side already shares a runtime (heaven_data + CartON + SOMA); (c) soma's observe→SOMA gate is wired
(task #16). Everything else here is **VISION** — a coherent target derived from the observed patterns, with
the load-bearing decisions left **OPEN** for Isaac. The proof obligation for "this unifies the stack" is:
build stages 1–4 and show one account + one bill + one runtime actually serving two of the products
(ralph + soma) with the SOMA→Ralph seam firing. Until that runs, this is a map of where to go, not a claim
that we are there.

---

## 7. Deepening (v2) — the SOMA→Ralph seam + OPEN-1 options

### 7.1 The SOMA→Ralph seam, concretely (VISION, grounded in read contracts)
This is **the one real cross-product integration** the narrative promises ("SOMA observes/validates →
Ralph executes what SOMA compiled", ralph.html / README) and that is **NOT wired** today
(saas-architecture-map §5). It is the highest-value first integration because both contracts are already
known and built:
- **SOMA side (IS — read, task #16):** `POST :8091/event {source, observations, domain}` → a result
  string carrying `unmet=N`, `unnamed_slots=N`, **`compiled=N`** + `soup_gaps` lines
  (observatory-compoctopus / soma core.ingest_event). When a process is fully modeled (no unmet, no soup
  gaps), SOMA's verdict is **CODE/compiled** — i.e. "this process is now a runnable automation."
- **Ralph side (IS — read, saas-architecture-map §2):** `POST /api/v1/jobs {name, task, repo_id,
  agent_config, expected_artifacts}` (x-api-key → workspace) creates a `jobConfig`; `POST /api/v1/schedules
  {job_id, cron}` schedules it; the worker polls `/runs`, clones, runs `compoctopus.agents.ralph.core`,
  opens a PR.
- **THE SEAM (VISION):** when SOMA returns `compiled>0` for a process, emit a Ralph `jobConfig`:
  SOMA's compiled process → `{name: <process>, task: <the validated steps as a requirements doc>,
  agent_config: {...}}` → `POST /api/v1/jobs` → optional `POST /api/v1/schedules` (if the process has a
  cadence). Ralph's worker then executes it. **Prerequisite (IS-blocked):** this requires shared identity
  (SOMA must hold a Ralph `workspace.apiKey`) → depends on **OPEN-3** (one tenancy) + stage 3 (one
  identity). **Also IS-blocked by a real Ralph gap:** there is **no cron dispatcher firing schedules→runs**
  yet (saas-architecture-map §2 gap) — so even a created schedule won't auto-run until that's built. So
  the seam's true dependency chain: fix Ralph's scheduler gap → shared identity → emit-job-from-compiled.
- **Minimal first proof (VISION):** SOMA `compiled` verdict → one `POST /api/v1/jobs` (manual run via
  `run_now`, bypassing the missing scheduler) → a PR appears. That single round-trip is the smallest thing
  that proves the seam.

### 7.2 OPEN-1 (runtime consumption) — the two concrete options (VISION; decision = Isaac's)
How a Next.js/Fly app reaches the shared runtime (heaven_data + CartON + SOMA). Two shapes:
- **Option A — service API over the substrate (recommended-for-discussion, not decided).** Stand the
  shared runtime behind HTTP services the Next apps call: CartON already has an MCP/HTTP surface
  (carton_mcp), SOMA already is HTTP (:8091, IS), heaven_data reads go through those services. Next apps
  stay stateless re: the substrate and call out. **Pro:** no bind-mount (matches the rule that you cannot
  `-v` mount mind_of_god paths to host docker — docker-from-inside-mind-of-god rule); works across
  separate Fly apps; clean tenancy boundary. **Con:** network hop; needs the substrate containerized +
  reachable (the L2 "containerize doc-mirror / fold-in via skill-over-API" pattern, complexity-ladder rung
  6-7).
- **Option B — bind-mount heaven_data into each app.** **Pro:** zero-latency direct reads. **Con:**
  the docker-from-inside-mind-of-god rule says paths that exist only in this container can't be
  `-v`-mounted on the host daemon — so a Fly-deployed Next app can't mount a dev-box path; this only works
  if heaven_data is itself a host-resident/volume-backed store. **Likely the weaker option for the
  Next/Fly side**, viable for co-located Python.
- **Net (VISION):** Option A (service-API over a containerized substrate) is the shape that fits the
  existing IS facts (SOMA + CartON already HTTP/MCP; the mount constraint). But this is **OPEN-1 — Isaac
  decides**; recorded as the leading option with its grounding, not chosen.

---

## 8. Deepening (v3) — entitlements, data-migration, publish-adapter

### 8.1 The entitlements model (VISION, grounded in the read schemas)
- **IS:** every Next fork's tenancy row already carries Stripe state — `teams.stripeCustomerId /
  stripeSubscriptionId / stripeProductId / planName / subscriptionStatus` (saas-architecture-map §0;
  identical across soma/CB; ralph renamed `teams`→`workspaces` with the same fields). Each fork has its
  **own** Stripe webhook → writes its **own** row. There is no cross-product notion of "what this account
  is entitled to."
- **VISION:** replace per-app `planName` with a single **`entitlements`** table on the shared identity
  store: `(account_id, product, tier, status, source_subscription_id)`. One Stripe customer per account;
  one webhook endpoint updates entitlements; each product checks an **entitlement flag** (`has(account,
  'ralph','pro')`) instead of reading a local `planName`. A **bundle** = one subscription that grants
  multiple product entitlements (this is what makes ralph's "Enterprise gets both" promise possible —
  today impossible across 6 separate Stripe accounts; saas-map §2/§5).
- **Migration shape:** the 6 forks' existing `stripe*` columns are the seed — back-fill `entitlements`
  from each fork's `teams/workspaces` rows, then point product code at the flag. **Depends on OPEN-3**
  (one account/tenancy) — entitlements can't key on `account_id` until the account model is unified.

### 8.2 Per-fork data migration (VISION, grounded)
- **IS (the shared template tables, identical per fork):** `users, teams, team_members, activity_logs,
  invitations` (saas-architecture-map §0). **Per-fork domain tables:** ralph = `workspaces, partners,
  repoConnections, jobConfigs, schedules, runs, blockages`; CB = `api_keys, spaces`; soma = `partners`
  (saas-map §1/§2/§4).
- **The tenancy union (VISION):** `workspaces` (ralph) = `teams` + `slug` + `apiKey` + `ownerId`; so the
  unified account/tenant schema = the **superset**: `teams` columns + `slug` + `apiKey` + `partnerId`.
  Migrate soma/CB `teams` and ralph `workspaces` into that one table (OPEN-3 picks the name).
- **Domain tables stay per-product**, re-pointed at the shared account FK. The KG-shaped data (CB
  `spaces` jsonb = serialized engine state; soma observations; SeedPublishing content) is the candidate to
  move into **CartON** as the shared knowledge store (rather than per-app Postgres jsonb) — VISION,
  per-product, sequenced after the account unification.
- **Order:** unify `users`+tenancy first (it's the FK everything hangs off), then entitlements (§8.1),
  then optionally migrate KG-shaped data into CartON. Domain transactional tables (runs/jobConfigs) can
  stay in Postgres — not everything needs CartON.

### 8.3 The unified publish-service adapter interface (VISION, grounded in the 4 IS publish paths)
One `publish(artifact, target, opts)` entrypoint with **target adapters**, each wrapping a publish path
that **already exists** (CSV §6/§7 + architecture doc §D/§E):
- `target=plugin` → CC marketplace adapter: add an entry to a `marketplace.json` + push the git repo
  (marketplace-publishing IS; ship-a-plugin flow).
- `target=pip` → PyPI adapter: largechain's `make_function_agentic_and_publish_to_pypi` /
  PackageAndPublishPypiTool + twine (largechain IS, design-stage — architecture doc §E).
- `target=content` → content adapter: render `JourneyBlog` (metastack) → HTML → github_pages (blog-system
  IS, auto-pipeline not wired) **or** push to SeedPublishing's gated reader (SeedPublishing IS).
- `target=site` → static-site adapter: the aisaac github_pages build.
Each adapter is the IS publish path of that system, unchanged, behind one interface. **No new publish
mechanism is invented** — the unification is a router over existing arms. **OPEN:** whether this router is
a service or just a skill/CLI (complexity-ladder choice) — Isaac's call.

---

## 9. Deepening (v4) — the tenancy-union table + the SOMA→Ralph payload

### 9.1 The unified account/tenancy table (VISION, exact columns from the read schemas)
The three tenant tables, as read (saas-architecture-map §0/§1/§2/§4):
- `teams` (soma, CB): `id, name, createdAt, updatedAt, stripeCustomerId, stripeSubscriptionId,
  stripeProductId, planName, subscriptionStatus` (+ soma `partnerId`).
- `workspaces` (ralph): `id, name, slug, ownerId→users, apiKey, partnerId, stripeCustomerId,
  stripeSubscriptionId, planName, subscriptionStatus, createdAt`.
- `users` (all forks, identical): `id, name, email, passwordHash, role, createdAt, updatedAt, deletedAt`.

**Proposed unified `accounts` table (VISION; OPEN-3 picks the final name "account" vs "team" vs
"workspace"):**
```
accounts(
  id, name, slug,               -- slug from workspaces (null-ok for migrated teams)
  owner_id    -> users.id,       -- from workspaces.ownerId (backfill for teams: first OWNER member)
  api_key     (nullable, unique),-- from workspaces.apiKey (null for non-API products)
  partner_id  -> partners.id,    -- white-label (soma/ralph already have it)
  created_at, updated_at
)
-- NOTE: the stripe*/planName columns are REMOVED from the tenant row and moved to:
billing_customers(account_id -> accounts.id, stripe_customer_id, stripe_subscription_id, status)
entitlements(account_id -> accounts.id, product, tier, status, source_subscription_id)  -- see §8.1
```
`users` is already identical across forks → adopt as-is (one users table). `team_members`/`activity_logs`/
`invitations` re-point their `teamId` FK to `accounts.id`. CB's `api_keys` table stays (it's a per-key
table, finer than `workspaces.apiKey`) but its `teamId`→`accounts.id`. **The Stripe columns leaving the
tenant row IS the structural move** that makes one-bill-many-products possible (§8.1).

### 9.2 The SOMA→Ralph job payload (VISION, grounded in the task-#16 slots)
When SOMA returns `compiled` for a process, the process individual has exactly the slots that — when
filled — flipped it from SOUP to CODE. From the **task-#16 live capture**, a process concept's required
slots are: `has_steps (template_sequence)`, `has_roles (role_list)`, `has_inputs (input_spec)`,
`has_outputs (output_spec)` (these were the literal `soup_gaps` lines :8091 returned). So a **compiled
process = those four filled.** Map them to a Ralph `jobConfig` (POST /api/v1/jobs, ralph schema §2):
```
POST /api/v1/jobs  (x-api-key = the account's api_key)
{
  "name": <process concept name>,                 -- SOMA concept
  "task": <requirements doc rendered from the 4 slots>,   -- has_steps -> numbered steps;
                                                           --  has_roles/has_inputs/has_outputs -> context
  "agent_config": { "model": <domain default> },
  "expected_artifacts": <from has_outputs>
}
```
Then `POST /api/v1/schedules {job_id, cron}` IF the process has a cadence (SOMA process w/ a recurrence
slot). The Ralph worker (IS) clones + runs `compoctopus.agents.ralph.core` + opens a PR. **Dependency
recap (IS-blockers, from v2 §7.1):** needs (a) Ralph's missing schedule→run dispatcher built, and (b) the
account's `api_key` shared with SOMA (OPEN-3). **Minimal proof unchanged:** compiled → one POST /jobs +
run_now → a PR. **OPEN:** the "render 4 slots → requirements doc" step — is it a deterministic template,
or an LLM pass? (a deterministic metastack render is the cheaper/honest first cut.)

---

## 10. Current → Target delta (v5) — one move per system (at a glance)

The single biggest move that takes each system from IS to the unified target. (Grounded in the maps;
"depends" = the gating OPEN/stage.)

| System | Current (IS) | Single biggest move (VISION) | Depends |
|---|---|---|---|
| soma-saas | template fork; own Postgres+Stripe; SOMA gate wired (task#16) | own Postgres → shared runtime; promote bundled SOMA daemon to the shared gate | OPEN-1, stage 2-3 |
| ralph-saas | real /api/v1+hub+worker; own Postgres+Stripe; no scheduler | build the schedule→run dispatcher + share identity → enable the SOMA→Ralph seam | OPEN-3 + the gap |
| lamai-saas | bare-ish template fork, partial | collapse fork → template-instance + niche-config | stage 5 |
| bangerlab-saas | template fork, "cloned-needs-build" | collapse → template-instance + niche-config; keep slop-compiler | stage 5 |
| primalops-saas | template fork, niche README | collapse → template-instance + niche-config | stage 5 |
| crystal-ball | real engine+API+SSE; own Stripe; separate repo | shared billing/identity; keep engine; decide federation | OPEN-5 |
| twi-jobworld | CAVE+domain, on heaven_data | replace manual clone → CAVE-core + domain-config | OPEN-2 (Isaac-gated) |
| twi-healthworld | git fork of jobworld, on heaven_data | same: clone → domain-config; fix rename-drift | OPEN-2 |
| promptworld | CAVE fork, claude-p, on heaven_data | **OUT OF SCOPE** — Isaac said keep separate | (Isaac re-open) |
| sanctum-builder | pydantic lib, STUB core, on heaven_data | finish the stub; use as a domain-config authoring lib | none (already shared runtime) |
| slop-saas-compiler | built page-gen engine | become the shared niche-SaaS page generator | none |
| SeedPublishing | standalone Express/Replit; Zapier; GitHub-content | source content from CartON; membership→shared entitlements | OPEN-6 |
| blog-system | metastack template; auto-pipeline unwired | wire CartON→JourneyBlog→HTML as the shared content publisher | none (build the wire) |
| marketplace-publishing | CC plugin catalogs (git) | become the `plugin` adapter of the publish-router | publish-router |
| largechain | design-stage function→PyPI | (if built) become the `pip` adapter of the publish-router | build largechain first |
| heaven_data | Python-side shared substrate (8.4GB) | expose as the mounted/served shared runtime for ALL (incl. Next forks) | OPEN-1 |
| SOMA :8091 | working Prolog validator gate | promote to the shared validation layer (one gate) | OPEN-4 |
| CartON | KG store (neo4j+chroma), live | the one knowledge store all products source from | none |

**Reading it:** the cheapest wins (no OPEN gate) are — finish sanctum-builder's stub, make
slop-compiler the shared page-gen, wire the blog auto-pipeline, and build Ralph's missing scheduler. The
load-bearing gated moves are OPEN-1 (runtime consumption) and OPEN-3 (one tenancy), which unblock the
Next-fork migrations + the SOMA→Ralph seam. promptworld stays out (Isaac's call); OPEN-2 (*World compiler)
stays closed until reopened.

### Changelog
- **v1 (2026-06-06):** first full pass — target architecture, per-system paths, shared/per-vertical cut,
  OPEN decisions, migration DAG, honest status.
- **v2 (2026-06-06):** deepened §7 — the SOMA→Ralph seam made concrete from the two read contracts
  (compiled-verdict → POST /api/v1/jobs), with its real dependency chain (Ralph scheduler gap + shared
  identity) and a minimal first-proof; OPEN-1 given two concrete options (service-API vs bind-mount) with
  grounding in the docker-mount constraint.
- **v3 (2026-06-06):** deepened §8 — entitlements model (one `entitlements` table replacing per-app
  `planName`; bundle = multi-product grant; depends OPEN-3); per-fork data migration (tenancy union =
  `workspaces` superset of `teams`; domain tables stay per-product re-pointed; KG-shaped data → CartON);
  publish-service as a router over the 4 existing IS publish arms (plugin/pip/content/site adapters, no new
  mechanism).
- **v4 (2026-06-06):** deepened §9 — the unified `accounts` table spec'd from the exact read columns
  (teams ∪ workspaces; Stripe cols moved off the tenant row into billing_customers + entitlements; users
  adopted as-is; FKs re-pointed); the SOMA→Ralph payload mapped from the task-#16 process slots
  (has_steps/roles/inputs/outputs → POST /api/v1/jobs body) with the render-step left OPEN
  (deterministic template vs LLM).
- **v5 (2026-06-06):** added §10 — a one-look "current → target" delta table (one biggest move per
  system + its gating dependency), surfacing the cheapest ungated wins (finish sanctum-builder stub,
  slop-compiler as shared page-gen, wire blog auto-pipeline, build Ralph's scheduler) vs the load-bearing
  gated moves (OPEN-1 runtime consumption, OPEN-3 tenancy). Next: resolve OPEN items as Isaac answers;
  spec the publish-router signature; add the SOMA→Ralph requirements-doc render template.
