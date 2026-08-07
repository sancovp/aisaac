# KILLS — the deletion work order (Builder C)

Builder C does **not** delete files. Everything below is staged for the integrator.
Every retired **URL** already has a working redirect stub committed (see
`tools/REDIRECTS.tsv`), so nothing here 404s when it goes.

Run order for the integrator:

```bash
python3 tools/build_blog.py        # 51 posts + blog/index.html   (idempotent)
python3 tools/build_notes.py       # 13 notes + notes/index.html  (idempotent)
python3 tools/build_redirects.py   # redirect stubs + 404.html    (idempotent)
bash    tools/check-site.sh        # the acceptance gate — must exit 0
```

After Builder B finishes B5 (B deletes its six merge sources), run
`python3 tools/build_redirects.py --include-b` to lay the stubs B's deletions
leave behind. Until then those nine URLs are deliberately skipped so B's salvage
sources stay readable.

---

## A. Already handled — redirect stub written, no action needed

These files still exist but now contain only a TYPE 5 redirect (instant refresh
+ a real visible link, per §1.2). They are safe to leave in place forever; leaving
them is what preserves the inbound links.

| URL | now points at | why |
|---|---|---|
| `agents.html` | `notes/` | 4-second forced meta-refresh was a WCAG 2.2.1 failure |
| `frameworks.html` | `notes/` | bounced to `blog/` — a nav item that looped to itself; **43 inbound links**, so the URL is kept and forwarded, never deleted |
| `advertorial.html` | `notes/the-ten-minute-product-priced-like-magic.html` | had no body at all; its entire argument lived inside an HTML comment. Headline merged onto the case study |
| `sanctuary-nexus.html` | `index.html` | orphaned shell, `var(--accent)` defined nowhere |
| `dharma-concierge.html` | `inside/fake-dharma.html` | dead 3-page loop that name-collided with the real property |
| `how_i.html` | `learn.html` | 1.3KB stub |
| `join.html` | `learn.html` | lore-named community door; community is a line on a rung now |
| `level10.html` | `learn.html` | origin-story stub |
| `dr-capitalism.html` | `learn.html` | competing category (agency arbitrage) |
| `jobworld-premium.html` | `run.html` | 1.4KB tombstone |
| `phone-agent.html` | `run.html` | commodity single-service page, wrong category |
| `ralph.html` | `build.html` | acronym-named internal tool page |
| `soma-start.html` | `pricing.html` | third competing price surface |
| `opera.html` | `inside/engine.html` | unlisted + rewritten |
| `gnosys.html` | `inside/gnosys.html` | unlisted |
| `sanctuary-system.html` | `inside/sanctuary-system.html` | unlisted |
| `business-buddhism.html` | `inside/why.html` | one claim salvaged |
| `vajra-value-shop.html` | `inside/why.html` | two lines salvaged |
| `completely-fake-dharma.html` | `inside/fake-dharma.html` | kept unedited, unlisted |
| `blog/admissibility-engineering.html` | `blog/admissibility.html` | duplicate-claim pair collapsed |
| `blog/concentration-engineering.html` | `blog/l6-concentration.html` | duplicate-claim pair collapsed |
| `blog/doctor.html` | `notes/` | a sales page squatting in the writing directory |

---

## B. DELETE — move out of the published repo

These are **not URLs anyone links to**; they are agent-facing corpora, production
source, and media that are publicly fetchable only because `.nojekyll` makes every
file in the repo servable. `.nojekyll` itself **stays** (underscore paths need it);
the markdown is what leaves.

### B1. Raw internal corpora — publicly readable right now (highest priority)

| path | size | why it must go |
|---|---|---|
| `b2b-bootcamp/` | 76K, 16 files | `core-pitch-script.md` publishes the closing mechanics verbatim; `SANCTUARY-WASTELAND-cosmology.md` is canon at a public URL |
| `content-engine/` | 16K | `REVEAL-DAG.md` states plainly that the series is designed to *"make it look like Isaac is discovering them live"* — it publishes the illusion it exists to protect |
| `ai-operating-system-positioning/` | 56K, 4 files | the **previous category bet, still live**, arguing "the folder is the operating system" against the current claim; also publishes the editorial mechanic from the inside |
| `docs/` | 6.8M, 111 files | superseded snapshots, `.bak` files, a `.patch`, a raw conversation dump, and `competitive-tally.md` — all world-readable |

**Extract these three before deleting `docs/`:**
- `docs/blog-map.md` → the only existing IA for `blog/`; keep privately
- `docs/course-builder/` → real source material for rung 2 (Builder B)
- `docs/scott-domain-proof/` (the non-`.bak` files only) → `ssri/papers/`

### B2. Not this site's content

| path | size | why |
|---|---|---|
| `dharma-concierge/` | 66M, 45 files | a complete separate brand selling $250 ingestible pills with longevity framing, on the same domain as a B2B AI funnel. Breaks one-claim-per-domain and attaches a health-claims liability surface. It is a strong standalone site — **move it to its own repo + domain, do not destroy it**. Steal one pattern first: `CONTENT_MAP.md`'s post-N→post-N+1 chain that closes into a circle |
| `builds/edwards-heating-air/` | 16M, 9 files | broken as committed (every image `src` is page-relative but assets live in `assets/`; `edwards-hero-video.mp4` does not exist) **and** it publishes a live third party's name, address, licence number, phone and verbatim reviews on a domain they have not agreed to. Move to the outreach engine's repo. **Port its head block and 14-breakpoint responsive discipline into the site first** — that is exactly what the blog posts lacked |
| `books/` | 28K, 3 files | two of the three `OUTLINE.md` files have no content at all, only a TODO. Salvage two lines: *"the funnel IS the product IS the content IS the proof"*, and "the myth predicted the architecture" (inside material only) |
| `video-storyboards/`, `scripts/` | 168K, 32 files | production source, not site content |

### B3. Loose media at the repo root

**12 files, 57.2 MB** — `plumber-*.png`, `plumbing-*.png`, `plumber-hero-video.mp4`,
`cinematic-plumbing-hero.png`. These are source frames for the Dickinson exhibit and
belong with it, not at the web root. Builder A owns `cinematic-plumbing.html` and its
media compression pass (spec A5); coordinate so the exhibit keeps the assets it
actually references.

### B4. Superseded by the rebuild

| path | why |
|---|---|
| `blog/blog-style.css` | the parallel design system. Zero files reference it now (verified) — every post falls through to `style.css` |
| `exit-popup.js`, `sticky-cta.js` | Builder A owns the deletion (§2.4). **No file in C's scope references either any more** — verified 0 script tags remaining across `blog/`, `notes/`, `inside/` |
| `newsletter.js` | A's audit call. Every `<script src="../newsletter.js">` has already been stripped from all 51 posts |
| `free-layer/*.md` (13 content files) | superseded — already rendered into `notes/`. `README.md`, `ASCEND-MAP.md`, `INVARIANTS.md` are agent-facing docs sitting in a web root and must go regardless |

---

## C. KEEP — explicitly not killed

| path | status |
|---|---|
| `.nojekyll` | **keep** — underscore paths need it. Removing the markdown is the fix, not removing this |
| `ssri/` | keep, unlisted. Own stylesheet, own sub-brand identity; `alignment.html` is cited as a real receipt |
| `blog/diagrams/` | keep — referenced by the posts |
| `inside/` | keep, all five pages `noindex` |
| `cinematic-plumbing.html`, `lab/` | Builder A's, untouched by C |

---

## FOR ISAAC: unresolved discrepancies found (evidence only, nothing changed)

Per the offer freeze, C made **no** choices about any of these.

1. **C asserts no offer content anywhere.** The shared ladder that appears on every
   C page previously carried `$65/mo` and `from $1,000/mo` in its rung descriptions.
   Both figures do exist verbatim in `main` (`join.html`, `pricing.html`), but a
   price in shared navigation chrome contradicts the pricing page on every page at
   once, so the rung descriptions now carry **no numbers at all** and rung 05 points
   to `pricing.html` as the single offer surface. No price was changed — prices were
   removed from navigation, not edited.
2. **Prices inside note and blog prose are untouched** (`$5,000`, `$10,000`, `$5K-35K`
   etc.). Those are editorial content from the corpus, verbatim from `main`.
3. **`opera.html`'s Discord claim was cut, not reworded.** *"GNOSYS and Conductor are
   always running. Talk to them on Discord"* is the site's most concretely falsifiable
   claim and it could not be verified from this container. `inside/engine.html` makes
   no uptime claim; the Discord link is simply absent. **If Isaac can confirm it is
   true, it can go straight back in.**
4. **Unverifiable counts were dropped rather than restated** on `inside/engine.html`
   and `inside/gnosys.html`: "300K+ lines of backend", "190K+ knowledge concepts",
   "26 framework blog posts". The last one was also factually wrong — there are 51.
5. **`blog/cave-unicorn-how-it-works-deep-dive.html`** contains an ASCII site-structure
   diagram inside a `<pre>` block that still names `frameworks.html` and `apply.html`.
   It is prose inside a code block, not a link, so C did not rewrite it. It is now
   slightly out of date.
