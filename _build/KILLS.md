# KILLS — files to delete / move private (Builder C)

**Builder C does not delete files.** This is the list; the integrator executes it.
Every entry has a destination in [`REDIRECTS.md`](REDIRECTS.md) or a reason it needs none.

`_build/` itself is a coordination directory and **must not ship**. Delete it after the
merge, or add it to `.gitignore` — `.nojekyll` means anything left in the web root is
publicly fetchable, which is the exact defect §2.5 exists to close.

---

## A. Root pages — DELETE (redirect stub or 404)

Each of these has a redirect row. None has salvage left un-ported; the "salvaged into"
column says where its surviving content went.

| File | Salvaged into | Notes |
|---|---|---|
| `agents.html` | — | 4-second forced meta-refresh (WCAG 2.2.1 failure), noindex, zero inbound links, zero unique content. |
| `sanctuary-nexus.html` | the completion-triple idea → case-study skeleton | Orphaned + already noindex. Used `var(--accent)`, defined nowhere. |
| `dharma-concierge.html` | — | Dead 3-page loop; name-collided with the real 23-page `/dharma-concierge/` property and never linked to it. |
| `how_i.html` | — | 1.3KB stub. |
| `join.html` | community becomes a priced line on `learn.html` / `pricing.html` (B) | Lore-named community door. |
| `level10.html` | two lines → `learn.html` about band (B) | Origin-story stub. |
| `dr-capitalism.html` | — | Competing category (agency arbitrage). |
| `jobworld-premium.html` | — | 1.4KB tombstone. |
| `soma-start.html` | inventory → `pricing.html` (B) | Third competing price surface. |
| `phone-agent.html` | — | Commodity single-service page, wrong category. |
| `ralph.html` | — | Acronym-named internal tool page. |
| `advertorial.html` | headline → `notes/the-ten-minute-product-priced-like-magic.html` (**done**, C3) | Had **no body**: the entire six-belief argument lived inside an HTML comment. |
| `vajra-value-shop.html` | two lines → `inside/why.html` (**done**, C4) | Broken shell, no CTA, gate in front of a gate. |
| `business-buddhism.html` | the ethics-as-architecture claim → `inside/why.html` (**done**, C4) | The one mechanism-backed sentence survived; the rest was a book ad for an unpublished book. |
| `blog/doctor.html` | — | A sales page squatting in the writing directory. Never listed in the blog index. |

## B. Root pages — MOVED to `inside/` (delete the originals)

The replacements are written and live. Originals are now duplicates.

| Original | Replacement | Status |
|---|---|---|
| `opera.html` | `inside/engine.html` | written (C4) |
| `gnosys.html` | `inside/gnosys.html` | written (C4) |
| `sanctuary-system.html` | `inside/sanctuary-system.html` | written (C4) |
| `completely-fake-dharma.html` | `inside/fake-dharma.html` | written (C4), content preserved verbatim |

## C. Blog — merge duplicates (delete the loser, keep the winner)

Two pairs of near-duplicate competing versions of the same claim. Both losers were
already unlisted in `blog/index.html`; both are now redirect targets.

| Delete | Keep | Why this one wins |
|---|---|---|
| `blog/admissibility-engineering.html` | `blog/admissibility.html` | Dated (April 2026), listed in the index, better subtitle. |
| `blog/concentration-engineering.html` | `blog/l6-concentration.html` | Dated (May 2026), listed in the index; the loser led with a canon product name. |

**Kept and now LISTED** (the audit's "list-or-delete" orphans — both are real, finished
posts, so listing recovers value that deleting would burn): `blog/sovereignty.html`,
`blog/owl-to-agent.html`. Both appear in the rebuilt `blog/index.html`.

## D. Directories — MOVE PRIVATE (do not delete blindly; these are real IP)

`.nojekyll` makes every `.md` in this repo publicly fetchable. These are the leaks.
**Extract the listed keepers first, then move the directory out of the published repo.**

| Directory | Extract first | Why it must leave |
|---|---|---|
| `docs/` (~24 `.md` + 7 subdirs, ~400KB) | `docs/blog-map.md` (only existing IA for `blog/`), `docs/course-builder/` (real source for rung 2 → B), `docs/scott-domain-proof/` **non-`.bak` files** → `ssri/papers/` | Superseded snapshots, `.bak` files, a `.patch`, a raw conversation dump, and `competitive-tally.md` + `market-research-synthesis.md` — all publicly readable. |
| `b2b-bootcamp/` (16 `.md`) | — | `core-pitch-script.md` publishes the closing mechanics verbatim; the cosmology file is canon at a public URL. |
| `content-engine/` | the DAG pattern (re-aim to the world-loop claim) | `REVEAL-DAG.md` states plainly that the series should "make it *look like* Isaac is discovering them live" — it publishes the illusion it exists to protect. |
| `ai-operating-system-positioning/` | the "advertise the world, not the features" discipline; invariants I1 and I15; `new-blogs.md` as a backlog | **The previous category bet, still live at a public URL**, arguing against the current claim — plus the editorial mechanic described from the inside. |
| `books/` (3 `OUTLINE.md`) | two ideas → `inside/` material only | Two of three have no content at all, only a TODO. |
| `video-storyboards/`, `scripts/` | — | Production source, not site content. |
| `dharma-concierge/` (30 files, 67MB) | `CONTENT_MAP.md`'s post-chain pattern | A complete separate brand selling $250 ingestible pills with longevity framing, on the same domain as a B2B AI funnel. Health-claims liability surface. **Strong standalone site — give it its own repo and domain.** |
| `builds/edwards-heating-air/` | the head block + its 14-breakpoint responsive discipline (port INTO the site) | Broken as committed (every image `src` is page-relative but assets live in `assets/`; `edwards-hero-video.mp4` does not exist) **and** it publishes a live third party's name, address, license, phone and verbatim reviews on a domain they have not agreed to. |
| `free-layer/` (`README.md`, `ASCEND-MAP.md`, `INVARIANTS.md`) | the 13 content files are **already rendered** into `notes/` (C3) | RULE 1: agent-facing docs in a web root. `README.md` also publishes the funnel mechanic in full. **Keep the 13 source `.md` only if they move private too** — otherwise the rendered `notes/` are now the source of truth. |

## E. Loose media in the web root — MOVE OUT (~29MB)

Nothing links to these after the rebuild; they are the plumber shoot's working files.
`cinematic-plumbing.html` is Builder A's and references its own assets — **confirm with A
before removing any file A's exhibit still points at.**

```
plumber-emergency-final.png      6.0M      plumbing-emergency-v2.png       7.6M
plumber-hero-ref.png             7.7M      plumbing-emergency.png          1.5M
plumber-hero-video.mp4           3.6M      plumbing-hero-v2.png            6.4M
plumber-portrait-final.png       5.9M      plumbing-portrait-v2.png        6.6M
plumber-tools-final.png          5.0M      plumbing-services.png           1.5M
cinematic-plumbing-hero.png      1.4M      plumbing-tools-v2.png           6.7M
cinematic-hvac-coR.md            6.8K   ← also a stray .md
```

## F. Scripts — DELETE (Builder A owns these files; listed for completeness)

`exit-popup.js`, `sticky-cta.js`, and `newsletter.js` (§2.4). **All `<script>` tags
referencing them are already gone from every file Builder C owns** — 54 blog notes, the
blog index, the 13 notes, the notes index, `inside/*`, `404.html`, `frameworks.html`.

## G. Fonts in the web root

`Cascadia.woff2` and `Virgil.woff2` sit in the root and are referenced by no stylesheet
in the rebuild. Builder A is self-hosting Inter + JetBrains Mono into `assets/fonts/`;
if A does not adopt these two, they go.
