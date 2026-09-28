#!/usr/bin/env python3
"""C5 — write a redirect stub for every retired URL, plus 404.html.

WHY META-REFRESH AND NOT A REAL 301: GitHub Pages serves static files and has
no redirect config, so a host-level 301 is not available on this deploy. The
spec (§1.2 TYPE 5) allows a meta-refresh ONLY at content="0" AND only with a
real visible link — a timed refresh is a WCAG 2.2.1 failure, which is exactly
why the old `agents.html` (content="4") dies. Both conditions are met here.
If the site ever moves behind a host that CAN do 301s, tools/REDIRECTS.tsv is
the table to feed it — that is why the table is emitted as data, not prose.

OWNERSHIP GUARD: six retired URLs (build/transform/soma/promptworld/school/
free/apply/sancrev/soma-start) are Builder B's merge SOURCES. B still needs to
read them and deletes them itself at step B5. Writing a stub over them now
would destroy B's salvage material, so they are skipped unless --include-b is
passed. The integrator runs `--include-b` AFTER B5.

Run:  python3 tools/build_redirects.py [--include-b]
"""
import posixpath
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from linkmap import REDIRECTS  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent

# Builder B's merge sources — B deletes these at B5 and hands C the list.
B_OWNED = {"build.html", "transform.html", "soma.html", "promptworld.html",
           "school.html", "free.html", "apply.html", "sancrev.html",
           "soma-start.html"}

# Why each URL retired — shown to the human who lands on the stub.
REASON = {
    "agents.html": "The free agents live on the Learn rung now.",
    "frameworks.html": "The frameworks are the notes. They moved to one index.",
    "advertorial.html": "This argument became a case study.",
    "sanctuary-nexus.html": "This page was a shell that never got written.",
    "dharma-concierge.html": "That project moved to its own site.",
    "how_i.html": "This stub folded into the Learn rung.",
    "join.html": "The community is a line on the Learn rung now, not a page.",
    "level10.html": "The origin story folded into the Learn rung.",
    "dr-capitalism.html": "Retired — a different business than this one.",
    "jobworld-premium.html": "It lives inside the Run rung now.",
    "phone-agent.html": "Single-service pages retired; this is part of Run.",
    "ralph.html": "Internal tooling — it lives inside the Build rung now.",
    "opera.html": "The platform page moved inside, and lost its lore.",
    "gnosys.html": "Moved inside.",
    "sanctuary-system.html": "Moved inside.",
    "business-buddhism.html": "One idea survived; it is on the Why page.",
    "vajra-value-shop.html": "One idea survived; it is on the Why page.",
    "completely-fake-dharma.html": "Kept, unedited, but unlisted.",
    "soma-start.html": "Every price is on one page now.",
    "build.html": "This page is now the Run rung.",
    "transform.html": "Merged into the Run rung.",
    "soma.html": "Became a tier on the Run rung.",
    "promptworld.html": "This page is now the Build rung.",
    "school.html": "Merged into the Learn rung.",
    "free.html": "Merged into the Learn rung and the notes.",
    "apply.html": "Booking and prices are on one page now.",
    "sancrev.html": "The price stack moved to the pricing page.",
    "blog/admissibility-engineering.html": "Two versions of one claim; this is the other one.",
    "blog/concentration-engineering.html": "Two versions of one claim; this is the other one.",
    "blog/doctor.html": "A sales page that was sitting in the writing folder.",
}

NAMES = {"index.html": "the homepage", "notes/": "the notes", "learn.html": "Learn",
         "run.html": "Run", "build.html": "Build", "pricing.html": "Pricing",
         "watch.html": "Watch"}


def stub(old, target):
    """A TYPE 5 redirect: instant refresh AND a real visible link."""
    up = "../" if "/" in old else ""
    # "/" means the homepage; relpath needs a real path to work with
    key = target.lstrip("/") or "index.html"
    # relative path from the stub's OWN directory to the target
    dest = posixpath.relpath(key, posixpath.dirname(old) or ".")
    if key.endswith("/"):
        dest += "/"
    label = NAMES.get(key, dest.rstrip("/").split("/")[-1].replace(".html", ""))
    reason = REASON.get(old, "This page moved.")
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="refresh" content="0; url={dest}">
<meta name="robots" content="noindex">
<title>Moved — Isaac</title>
<link rel="canonical" href="https://sancovp.github.io/aisaac/{key}">
<link rel="icon" href="{up}assets/favicon.svg">
<link rel="stylesheet" href="{up}style.css">
</head>
<body>
<main id="main">
  <section class="claim">
    <div class="wrap">
      <p class="eyebrow">This page moved</p>
      <h1>{reason}</h1>
      <p class="lede">You are being sent to {label}. If nothing happens, use the link.</p>
      <a class="cta-primary" href="{dest}">Go to {label} &rarr;</a>
    </div>
  </section>
</main>
</body>
</html>
"""


NOT_FOUND = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Not found — Isaac</title>
<meta name="description" content="That page does not exist. Here is the ladder instead.">
<meta name="robots" content="noindex">
<link rel="icon" href="assets/favicon.svg">
<link rel="stylesheet" href="style.css">
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>

<header class="nav">
  <a href="index.html" class="logo">Isaac</a>
  <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="navlinks">Menu</button>
  <nav id="navlinks" class="nav-links" aria-label="The ladder">
    <a href="watch.html">Watch</a>
    <a href="learn.html">Learn</a>
    <a href="build.html">Build</a>
    <a href="run.html">Run</a>
    <a href="notes/">Notes</a>
    <a href="pricing.html" class="nav-cta">Pricing</a>
  </nav>
</header>

<main id="main">
  <section class="claim">
    <div class="wrap">
      <p class="eyebrow">404</p>
      <h1>That page isn't here.</h1>
      <p class="lede">A lot of pages were retired in a rebuild &mdash; most of them redirect, but this one didn't survive with a forwarding address. The ladder below goes everywhere that still exists.</p>
      <a class="cta-primary" href="watch.html">Watch a world run &rarr;</a>
    </div>
  </section>

  <section>
    <div class="wrap">
      <p class="eyebrow">Where this sits</p>
      <h2>Everything on the site, in order.</h2>
      <nav class="ladder" aria-label="Where this sits">
        <a class="rung" href="watch.html"><span class="rung-n">01</span><span class="rung-t">Watch a world run</span><span class="rung-d">the engine, live, in your browser</span></a>
        <a class="rung" href="learn.html"><span class="rung-n">02</span><span class="rung-t">Learn to build them</span><span class="rung-d">the patterns, the notes, and the community</span></a>
        <a class="rung" href="build.html"><span class="rung-n">03</span><span class="rung-t">Run your work inside one</span><span class="rung-d">open source &mdash; install it today</span></a>
        <a class="rung" href="run.html"><span class="rung-n">04</span><span class="rung-t">Have one run your business</span><span class="rung-d">built with you, then handed over</span></a>
        <a class="rung" href="pricing.html"><span class="rung-n">05</span><span class="rung-t">What it costs</span><span class="rung-d">every price on one page</span></a>
      </nav>
    </div>
  </section>

  <section>
    <div class="wrap">
      <div class="cards">
        <a class="card" href="notes/"><h3>The notes</h3><p>The patterns written plainly, plus 51 field notes behind them.</p><span class="receipt-go">Read &rarr;</span></a>
        <a class="card" href="system.html"><h3>How the engine works</h3><p>One engine, many worlds, and the loop that compounds.</p><span class="receipt-go">See the map &rarr;</span></a>
      </div>
    </div>
  </section>
</main>

<footer class="footer">
  <span>&copy; 2026 Isaac</span>
  <span class="tagline">Built by the engine it sells. That is the whole proof.</span>
</footer>
<script src="nav.js"></script>
</body>
</html>
"""


def build(include_b=False):
    written, skipped, rows = [], [], []
    for old, target in sorted(REDIRECTS.items()):
        rows.append(f"{old}\t{target}\t{REASON.get(old, '')}")
        if old in B_OWNED and not include_b:
            skipped.append(old)
            continue
        path = ROOT / old
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(stub(old, target), encoding="utf-8")
        written.append(old)

    (ROOT / "404.html").write_text(NOT_FOUND, encoding="utf-8")
    written.append("404.html")
    (ROOT / "tools" / "REDIRECTS.tsv").write_text(
        "# old\tnew\twhy — feed this to a host that supports real 301s\n"
        + "\n".join(rows) + "\n", encoding="utf-8")
    print(f"stubs written: {len(written)}")
    if skipped:
        print(f"SKIPPED (Builder B still owns these; re-run --include-b after B5): "
              f"{', '.join(skipped)}")
    return written


if __name__ == "__main__":
    build(include_b="--include-b" in sys.argv)
