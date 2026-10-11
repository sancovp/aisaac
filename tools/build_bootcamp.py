"""Builds aisaac/bootcamp.html — THE B2B FRAMEWORKS PAGE (the B2B bootcamp: PSA · SCREENING · CLINIC · DOCTOR · LIFE and
the tools behind them), where THE DOOR's fourth card lands ("I want to learn to sell, market or run my operations") and
from which the visitor goes back to JobWorld, which does it for them (docs/the-door.md §3).

The bootcamp is lifted WHOLE and verbatim from framework.html's `#bootcamp` section (its sources: b2b-bootcamp/), so it has
one wording; its section heading becomes the page's h1, and its placeholder call becomes the way back to JobWorld.
Edit framework.html's section or this script, then rebuild; never edit bootcamp.html by hand.
"""
import pathlib

SITE = pathlib.Path(__file__).resolve().parent.parent
fw = (SITE / 'framework.html').read_text()
i = fw.index('  <!-- THE B2B BOOTCAMP'); j = fw.index('</section>', fw.index('id="bootcamp"')) + len('</section>')
sec = fw[i:j]
H2 = '<h2>How to sell and deliver AI transformation &mdash; run like a clinic.</h2>'
assert H2 in sec
sec = sec.replace(H2, '<h1 class="sec-h1">How to sell and deliver AI transformation &mdash; run like a clinic.</h1>')
a = sec.index('      <div class="solo-cta fw-again">'); b = sec.index('</div>', sec.index('</p>', a)) + len('</div>')
sec = sec[:a] + '''      <div class="solo-cta fw-again">
        <span class="arm-press" data-arm-press><a class="cta-primary" href="https://iwantaiformybusiness.com/jobworld">Or let JobWorld do it for you &rarr;</a></span>
        <p class="door-fine">Every framework on this page runs in JobWorld &mdash; its CEO and departments do the selling, the marketing and the operations.</p>
      </div>''' + sec[b:]

APP = 'https://app.iwantaiformybusiness.com'
TITLE = 'The B2B bootcamp — how to sell and deliver AI transformation'
DESC = 'For operators: diagnose before you prescribe, close like care, and keep the care going after the sale.'
URL = 'https://iwantaiformybusiness.com/bootcamp'

page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{TITLE}</title>
<meta name="description" content="{DESC}">
<link rel="canonical" href="{URL}">
<meta property="og:type" content="website">
<meta property="og:title" content="{TITLE}">
<meta property="og:description" content="{DESC}">
<meta property="og:image" content="https://iwantaiformybusiness.com/assets/og/twi-framework.png">
<meta property="og:url" content="{URL}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="assets/favicon.svg">
<link rel="stylesheet" href="style.css?v=2026-10-11h">
</head>
<body data-depth="0">
<!-- BUILT by tools/build_bootcamp.py — the B2B bootcamp, lifted from framework.html's #bootcamp. THE DOOR's fourth card
     lands here; the one way on is JobWorld. -->
<header class="nav nav-glass">
  <span class="logo">AI Transformations With Isaac</span>
  <span class="arm-press" data-arm-press="down"><a class="nav-get" href="https://iwantaiformybusiness.com/jobworld">JobWorld</a></span>
</header>

<main id="main">
{sec}
</main>

<script src="arm.js?v=2026-10-11e"></script>
</body>
</html>
'''
(SITE / 'bootcamp.html').write_text(page)
print(f'wrote {SITE / "bootcamp.html"} {len(page)} bytes')
