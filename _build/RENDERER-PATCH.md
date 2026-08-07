# RENDERER-PATCH — what `cave-unicorn` must emit from now on

**Status: the 54 rendered notes in `blog/` are already fixed in-place.** This file is the
patch that has to land in the *renderer* so the fix survives the next nightly run.

## Why this is a spec and not a commit

`cave-unicorn` has **no local checkout** in this container. It lives in the monorepo at
`sra-git/application/cave-unicorn/` (`cave_unicorn/site.py` is the file that owns the
skeleton — it and `tests/test_unicorn.py` are the only places the `isaac-site` wrapper
string appears). Per the build rails, Builder C pushes to `aisaac@ceo` and to nothing
else, so the renderer change is written here and handed to whoever owns that repo.

**Until this lands, every new nightly post regresses.** The in-place fix covers the 54
posts that existed on 2026-08-07 and nothing after.

## What was wrong (measured, not asserted)

| Defect | Count before |
|---|---|
| No `<!doctype>` → quirks mode | 50 of 55 |
| No `<title>` → raw URL in the tab and in every search result | 50 of 55 |
| No `<meta viewport>` → no mobile response at any width | 50 of 55 |
| No `og:`/`twitter:` tags → every share is a bare blue link | 54 of 55 |
| Nav variants across the corpus | 5 |
| `<script>` tags for `sticky-cta.js` / `exit-popup.js` / `newsletter.js` | 53 |

## The patch

### 1. Emit a real document

The renderer currently emits a fragment that opens with
`<link rel="stylesheet" href="blog-style.css">` and wraps everything in
`<div id="isaac-site">`. Replace that wrapper with a full document:

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{TITLE_60} — Isaac</title>
<meta name="description" content="{DESC_155}">
<link rel="canonical" href="{SITE_ORIGIN}/blog/{slug}.html">
<meta property="og:type" content="article">
<meta property="og:title" content="{TITLE_60} — Isaac">
<meta property="og:description" content="{DESC_155}">
<meta property="og:image" content="{SITE_ORIGIN}/assets/og/{slug}.png">
<meta property="og:url" content="{SITE_ORIGIN}/blog/{slug}.html">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{REL}/assets/favicon.svg">
<link rel="stylesheet" href="{REL}/style.css">
</head>
<body>
{NAV}
<main id="main">
  <article class="note"> … </article>
  {RECEIPTS_COMPACT}
  {FINAL_CTA}
</main>
{FOOTER}
</body>
</html>
```

- `TITLE_60` / `DESC_155` — clamp on a **word boundary**, then append `…`. A hard slice
  produces `…saw the next tu` in the browser tab, which reads as a bug.
- `REL` — `..` for `blog/*.html`. Paths are depth-relative, not root-absolute: the site
  is served from a project Pages subdirectory (`/aisaac/`), where `/style.css` 404s.
- `{NAV}` / `{FOOTER}` — the shared blocks, byte-identical to every other page.

### 2. Drop `blog-style.css` and `#isaac-site`

One stylesheet ships site-wide (§2.1). Map the old classes onto the shared vocabulary:

| Old | New |
|---|---|
| `<div id="isaac-site">` | *(removed)* |
| `<div class="site-header">…</div>` | the canonical `<header class="nav">` block |
| `<article>` | `<article class="note">` |
| `<div class="post-tag">X</div>` | `<p class="eyebrow">X</p>` |
| `<p class="post-subtitle">` | `<p class="dek">` |
| `<div class="site-footer">…</div>` | the canonical `<footer class="footer">` block |
| `<div class="blog-cta…">` (2 links) | one `<section class="final-cta">`, one link |

### 3. Emit no `<script>` at all

`sticky-cta.js` and `exit-popup.js` are deleted from the repo (§2.4). `newsletter.js`
goes too unless a live backend exists — an email field that writes to `localStorage` and
says "we'll be in touch" is silent data loss, which is the bug `apply.html` died for.
The only script the pages load is the shared `nav.js`, emitted by the shared footer block.

### 4. Rewrite links to killed surfaces

The renderer emits `../apply.html`, `../frameworks.html`, `../transform.html` etc. Those
surfaces no longer exist. Apply the map in `_build/REDIRECTS.md`; the notable ones:

```
../apply.html      → ../pricing.html      ../frameworks.html → ../notes/
../transform.html  → ../run.html          ../promptworld.html→ ../build.html
../school.html     → ../learn.html        ../free.html       → ../learn.html
../soma.html       → ../run.html          ../opera.html      → ../inside/engine.html
../build.html      → ../run.html   (build.html changed meaning: it is rung 3 now)
```

### 5. Keep the canon vocabulary in the body — deliberately

Law L3 bans `SANCREV / SANCTUM / CAVE / UNICORN / PAIAB / SOMA / …` **above the door**.
It is *not* applied to the body of an already-opened note, and the renderer must not
start stripping it: the corpus is the highest-value asset on the site and rewriting 54
posts' prose to satisfy a door rule would damage it for no reader benefit. "Lore is the
inside, never the door" — a note you have clicked into *is* the inside.

Where the rule **is** enforced: the door surfaces, and the blog index's filter row (the
canon tags used to be the first four choices a stranger saw, one click from the homepage;
they are gone from the filter row entirely now).

15 of the 54 notes carry canon terms in their prose. That is intended, and the in-place
patch preserved every one.

## Reference implementation

The in-place patch that produced the current 54 files is a single idempotent script
(re-running it on a patched file is a no-op). It is not committed to this repo — it is a
one-shot migration, and the durable form of it is the renderer change above. The
integrator can find it in the build scratchpad as `patch_notes.py` if the exact
transformations need re-reading.

## Files intentionally left unpatched

`admissibility-engineering.html`, `concentration-engineering.html`, `doctor.html` — all
three are on the kill/merge list and ship as redirect stubs, so patching them was work
thrown away. See `_build/KILLS.md` §C.

## Acceptance (run after any future render)

```bash
cd blog
grep -Li '<!doctype' *.html   # empty
grep -Li '<title>'   *.html   # empty
grep -Li 'viewport'  *.html   # empty
grep -Li 'og:image'  *.html   # empty
grep -l  '<script'   *.html | grep -v nav.js   # empty
grep -l  'blog-style' *.html  # empty
# exactly one nav block across the corpus:
for f in *.html; do grep -A9 '<header class="nav">' "$f" | md5sum; done | sort -u | wc -l   # 1
```
