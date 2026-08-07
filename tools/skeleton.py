"""The shared skeleton, conformed to Builder A's shipped `_templates/` + `style.css`.

EVERY string here is pasted from A's templates, not invented. If A changes a
template, change it here and re-run the generators — never hand-edit a page.

A's PATH LAW (_templates/_head.html): the site deploys to a GitHub Pages PROJECT
SUBPATH (https://sancovp.github.io/aisaac/), so in-page href/src are RELATIVE and
only canonical/og URLs are absolute. `up` is "" at the repo root and "../" one
level down. Root-absolute paths are forbidden sitewide.

A's class vocabulary (verified against style.css):
  .note .dek .caveat .note-meta .note-next  |  .receipt > .receipt-k h3 p .receipt-go
  .ladder > .rung > .rung-n .rung-t .rung-d |  .cards > .card  |  .wrap .eyebrow .lede
"""

SITE_ORIGIN = "https://sancovp.github.io/aisaac"


def head(title, description, path, og_slug, up="", noindex=False):
    """B0 — A's _templates/_head.html, placeholders filled."""
    robots = '\n<meta name="robots" content="noindex">' if noindex else ""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} — Isaac</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{SITE_ORIGIN}{path}">
<meta property="og:type" content="website">
<meta property="og:title" content="{title} — Isaac">
<meta property="og:description" content="{description}">
<meta property="og:image" content="{SITE_ORIGIN}/assets/og/{og_slug}.png">
<meta property="og:url" content="{SITE_ORIGIN}{path}">
<meta name="twitter:card" content="summary_large_image">{robots}
<link rel="icon" href="{up}assets/favicon.svg">
<link rel="stylesheet" href="{up}style.css">
</head>
<body data-depth="2">
<a class="skip-link" href="#main">Skip to content</a>"""


def nav(up="", current=None):
    """B1 — A's _templates/_nav.html. PASTED VERBATIM. Never edited locally;
    the only variable is A's documented ROOT vs DEPTH-1 variant."""
    items = [("watch.html", "Watch"), ("learn.html", "Learn"),
             ("build.html", "Build"), ("run.html", "Run"),
             ("notes/", "Notes"), ("pricing.html", "Pricing")]
    out = ['<header class="nav">',
           f'  <a href="{up}isaac.html" class="logo">Isaac</a>',  # ratchet law: brand slot -> the hub, never the one-way door
           '  <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="navlinks">Menu</button>',
           '  <nav id="navlinks" class="nav-links" aria-label="The ladder">']
    for href, label in items:
        cls = ' class="nav-cta"' if href == "pricing.html" else ""
        aria = ' aria-current="page"' if href == current else ""
        out.append(f'    <a href="{up}{href}"{cls}{aria}>{label}</a>')
    out += ["  </nav>", "</header>", "", '<main id="main">']
    return "\n".join(out)


# OFFER FREEZE (Isaac, direct order): these rung descriptions carry NO price,
# tier, or paid-CTA wording. Rung 05 is the ONLY pointer to money, and it names
# no number — pricing.html is the single offer surface and the single source of
# truth for every figure. Do not reintroduce prices here: a price in shared
# navigation chrome silently contradicts the offer page on every page at once.
_RUNGS = [
    ("01", "watch.html", "Watch a world run", "the engine, live, in your browser"),
    ("02", "learn.html", "Learn to build them", "the patterns, the notes, and the community"),
    ("03", "build.html", "Run your work inside one", "open source — install it today"),
    ("04", "run.html", "Have one run your business", "built with you, then handed over"),
    ("05", "pricing.html", "What it costs", "every price on one page"),
]


def ladder(up="", heading="Where this sits"):
    """B6 — the IA spine rendered as content."""
    rows = "\n".join(
        f'        <a class="rung" href="{up}{href}"><span class="rung-n">{n}</span>'
        f'<span class="rung-t">{t}</span><span class="rung-d">{d}</span></a>'
        for n, href, t, d in _RUNGS)
    return f"""  <section>
    <div class="wrap">
      <p class="eyebrow">Where this sits</p>
      <h2>{heading}</h2>
      <nav class="ladder" aria-label="Where this sits">
{rows}
      </nav>
    </div>
  </section>"""


def receipts(up=""):
    """B4 — the site-canonical four. Every claim opens an artifact."""
    return f"""  <section class="receipts dark">
    <div class="wrap">
      <p class="eyebrow">Receipts, not testimonials</p>
      <h2>Don't take my word for it &mdash; take the code.</h2>
      <p class="receipts-lede">No logo wall, no invented case studies. Four things you can open right now.</p>
      <div class="receipts-grid">
        <a class="receipt" href="https://github.com/sancovp"><div class="receipt-k">Open source</div><h3>The engine, on GitHub</h3><p><b>heaven-framework</b>, <b>chaincompiler</b>, <b>carton-mcp</b>, <b>skilltree</b> &mdash; MIT, full commit history.</p><span class="receipt-go">github.com/sancovp &rarr;</span></a>
        <a class="receipt" href="{up}watch.html"><div class="receipt-k">Running now</div><h3>A world running in your browser</h3><p>The engine drawing its own explainer. Your scroll is the clock.</p><span class="receipt-go">Watch it &rarr;</span></a>
        <a class="receipt" href="{up}cinematic-plumbing.html"><div class="receipt-k">One run's output</div><h3>What one run produced</h3><p>A live local-business site, built end to end by the engine. Not a mockup.</p><span class="receipt-go">Open it &rarr;</span></a>
        <a class="receipt" href="{up}notes/"><div class="receipt-k">Open notes</div><h3>The field notes</h3><p>Published as they were written &mdash; including the ones that record a mistake.</p><span class="receipt-go">Read them &rarr;</span></a>
      </div>
    </div>
  </section>"""


def receipts_compact(items):
    """B4 compact — 2 MAX, inside a NOTE-ARTICLE. `items` = [(kind, h3, p, go, href)]"""
    rows = "\n".join(
        f'        <a class="receipt" href="{href}"><div class="receipt-k">{k}</div>'
        f"<h3>{h3}</h3><p>{p}</p><span class=\"receipt-go\">{go} &rarr;</span></a>"
        for k, h3, p, go, href in items[:2])
    return f"""  <section class="receipts compact">
    <div class="wrap measure">
      <p class="eyebrow">Receipts</p>
      <div class="receipts-grid">
{rows}
      </div>
    </div>
  </section>"""


def final_cta(up="", h2="See one actually run.",
              p="The fastest way to judge any of this is to watch the engine do it.",
              label="Watch a world run", href="watch.html"):
    """B9 — ONE link, ONE destination."""
    return f"""  <section class="final-cta">
    <div class="wrap">
      <h2>{h2}</h2>
      <p>{p}</p>
      <a class="cta-primary" href="{up}{href}">{label} &rarr;</a>
    </div>
  </section>"""


def footer(up=""):
    """B10 — A's _templates/_footer.html."""
    return f"""</main>

<footer class="footer">
  <span>&copy; 2026 Isaac</span>
  <span class="tagline">Built by the engine it sells. That is the whole proof.</span>
</footer>
<script src="{up}nav.js"></script>
</body>
</html>"""
