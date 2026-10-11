"""Builds aisaac/jobworld.html — the JobWorld product page in the Blueprint System.

Every sentence on the page comes from a canonical source (00-SITE-CANON § THE SOURCE MAP, the
jobworld.html row): the walkthrough's site section and VSL script, the demo recordings' own
description, and the JobWorld architecture's fences. The booking dialog is lifted whole from
ai-transformation.html, so every page shares one form and one consent wording (law 13).
Edit this script and rebuild; never edit jobworld.html by hand.
"""
import pathlib

SITE = pathlib.Path(__file__).resolve().parent.parent
src = (SITE / 'ai-transformation.html').read_text()
dialog = src[src.index('<dialog class="capture"'):src.index('</dialog>') + len('</dialog>')]
assert 'consent_version' in dialog and 'data-consent="recording"' in dialog

TITLE = 'JobWorld — your company, with an AI CEO in the chair'
DESC = ('A JobWorld is your company with an AI CEO in the chair. You sign in to it with your own AI account, '
        'and nothing in it reaches the world until you say so.')
URL = 'https://iwantaiformybusiness.com/jobworld'

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
<meta property="og:image" content="https://iwantaiformybusiness.com/assets/og/twi-jobworld.png">
<meta property="og:url" content="{URL}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="assets/favicon.svg">
<link rel="stylesheet" href="style.css?v=2026-10-11e">
</head>
<body data-depth="0">
<!-- BUILT by tools/build_jobworld.py — edit the script, then rebuild. The JobWorld product page:
     what a JobWorld is, three real recordings of one running, where it stops, and one action, Book a
     call. Its sources: 00-SITE-CANON § THE SOURCE MAP, the jobworld.html row. No price, no name of
     anything behind the door, no client named. -->

<div class="bp-parcels" aria-hidden="true">
  <div class="lane"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div>
  <div class="lane"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div>
</div>

<a class="skip-link" href="#book">Skip to booking</a>

<!-- THE TOP BAR: the product's name, the ink Sign in for owners who already have one, the ink Get JobWorld (the plans and
     the checkout), and the red Book a call that never leaves the screen. -->
<header class="nav nav-glass">
  <span class="logo">JobWorld</span>
  <a class="nav-get" href="https://app.iwantaiformybusiness.com/sign-in">Sign in</a>
  <span class="arm-press" data-arm-press="down"><a class="nav-get" href="https://app.iwantaiformybusiness.com/pricing">Get JobWorld</a></span>
  <span class="arm-press" data-arm-press="down"><button class="nav-book" type="button" data-buy="call">Book a call</button></span>
</header>

<main id="main">

  <section class="bp-hero">
    <div class="wrap">
      <div class="bp-card">
        <div class="hero-split">
          <div class="hero-copy">
            <p class="eyebrow"><span class="pill">Business Owners:</span></p>
            <h1>Your company, <span>with an AI CEO in the chair.</span></h1>
            <p class="lede">{DESC}</p>
            <div class="solo-cta" id="book">
              <span class="arm-press" data-arm-press><a class="cta-primary" href="https://app.iwantaiformybusiness.com/pricing">Get JobWorld &rarr;</a></span>
              <span class="arm-press" data-arm-press><button class="cta-primary" type="button" data-buy="call">Book a call &rarr;</button></span>
              <div class="hero-who">
                <img src="assets/isaac-headshot-sm.jpg" alt="" width="240" height="240">
                <p class="booker-who"><strong>Isaac Wostrel-Rubin</strong><span>Founder of TWI</span></p>
              </div>
              <p class="door-fine">Bring one part of your business. We map it on the call, and I show you what its CEO does with it on day one.</p>
            </div>
          </div>
          <div class="hero-art">
            <video autoplay muted loop playsinline preload="auto" data-loop
                   poster="assets/hero-loop-2-poster.jpg" width="1280" height="720"
                   aria-label="The owner leans back at his desk, hands behind his head, while his company works on its own: people and AI agents at their desks, wired together — signals run along the wires, documents and messages pass between the desks, and the money flows back down the one line to him.">
              <source src="assets/hero-loop-2.mp4" type="video/mp4">
            </video>
          </div>
        </div>
        <div class="bp-rule"></div>
        <div class="bp-pad">
          <p class="hero-for"><span class="hero-for-k">Who it&rsquo;s for</span>Owners of established businesses who are still the one who knows how everything runs &mdash; and franchisors and multi-location operators whose model runs in many places.</p>
        </div>
      </div>
    </div>
  </section>

  <!-- THE FIRST NIGHT — library/marketing/jobworld-walkthrough/site-section.md, verbatim. The recording
       is the owner's own JobWorld, redacted; silent, looping, no controls. -->
  <section class="bp-sec bp-band">
    <div class="wrap">
      <p class="eyebrow"><span class="pill">What it looks like running</span></p>
      <h2>Your AI CEO, on its first night</h2>
      <div class="bp-card">
        <div class="bp-pad">
          <div class="artifact-frame what-loop">
            <video autoplay muted loop playsinline preload="metadata" data-loop
                   poster="assets/jobworld-walkthrough-poster.jpg" width="1008" height="530"
                   aria-label="The CEO's terminal in a JobWorld: it lists five questions, takes the answers from the owner's other agent, reports two lines of its own draft it cut, checks the email tool's documentation, and spawns a researcher that builds a 25-company lead list across five cities">
              <source src="assets/jobworld-walkthrough-loop.mp4" type="video/mp4">
            </video>
          </div>
        </div>
        <div class="bp-rule"></div>
        <div class="bp-pad">
          <p class="lede">This is a JobWorld &mdash; your company with an AI CEO in the chair, signed in with your own AI account. On its first night it drafted your cold outreach, asked you five questions, took the answers from your other agent reading your own documents, rewrote its own draft where it couldn&rsquo;t back a line up, checked the email tool&rsquo;s docs instead of guessing, and built a 25-company lead list across five cities for free. Then it stopped, at the one line it may not cross without you: sending.</p>
        </div>
        <div class="bp-rule"></div>
        <div class="bp-split get-top">
          <div class="bp-cell">
            <p class="get-k">It asks before it acts</p>
            <p class="get-v">Five questions before a word went out. Nothing reaches the world until you say so.</p>
          </div>
          <div class="bp-cell">
            <p class="get-k">It checks what it isn&rsquo;t sure of</p>
            <p class="get-v">It read the email tool&rsquo;s help center rather than guess a merge tag that would have broken every unsubscribe link.</p>
          </div>
          <div class="bp-cell">
            <p class="get-k">It builds, it doesn&rsquo;t buy</p>
            <p class="get-v">The lead list came from a map search &times; the company&rsquo;s page &times; the company&rsquo;s own site &mdash; a source on every fact.</p>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- THE DASHBOARD — clients/aht/demo/console-tour.mp4 and its CLAUDE.md; the one frontend
       (application/jobworld DESIGN §9 · business-runtime DESIGN §8a). A demo business, labelled so. -->
  <section class="bp-sec">
    <div class="wrap">
      <p class="eyebrow"><span class="pill">The dashboard</span></p>
      <h2>The business runs from one dashboard.</h2>
      <div class="bp-card">
        <div class="bp-pad">
          <div class="artifact-frame what-loop">
            <video autoplay muted loop playsinline preload="metadata" data-loop
                   poster="assets/jobworld-console-tour-poster.jpg" width="1440" height="900"
                   aria-label="A JobWorld's dashboard, page by page: the CEO's terminal, Today, Pipeline, Contacts with one opened, Conversations with one thread opened, Calendar, and Activity">
              <source src="assets/jobworld-console-tour.mp4" type="video/mp4">
            </video>
          </div>
        </div>
        <div class="bp-rule"></div>
        <div class="bp-pad">
          <p class="lede">Your CEO&rsquo;s terminal, then Today, Pipeline, Contacts, Conversations, Calendar and Activity. The agents do the work here; you handle the settings and hand them files and notes.</p>
          <p class="door-fine">Shown on a demo business: its records are made up, its CEO is real.</p>
        </div>
      </div>
    </div>
  </section>

  <!-- IT WORKS WHILE YOU WATCH — clients/aht/demo/agent-at-work.mp4 and its CLAUDE.md. -->
  <section class="bp-sec bp-band">
    <div class="wrap">
      <p class="eyebrow"><span class="pill">It works while you watch</span></p>
      <h2>You ask in its terminal. The pipeline changes as it works.</h2>
      <div class="bp-card">
        <div class="bp-pad">
          <div class="artifact-frame what-loop">
            <video autoplay muted loop playsinline preload="metadata" data-loop
                   poster="assets/jobworld-agent-at-work-poster.jpg" width="1440" height="900"
                   aria-label="The CEO is asked in its terminal to do four things: it closes and wins one deal, adds a new contact and her deal, adds a note on a third, and refuses the refund; the Pipeline and Activity pages show each change as it lands">
              <source src="assets/jobworld-agent-at-work.mp4" type="video/mp4">
            </video>
          </div>
        </div>
        <div class="bp-rule"></div>
        <div class="bp-pad">
          <p class="lede">Four things asked of the CEO, in its terminal: it closes and wins one deal, adds a new contact and her deal, writes a note on a third &mdash; and refuses the refund, because money waits for the owner. Pipeline and Activity show each change as it lands.</p>
          <p class="door-fine">Shown on the same demo business.</p>
        </div>
      </div>
    </div>
  </section>

  <!-- WHERE IT STOPS — the fences of business-runtime DESIGN §8a (the hard blocks: money, and contact
       without a basis) and §8e (the model account is the business's own). -->
  <section class="bp-sec">
    <div class="wrap">
      <p class="eyebrow"><span class="pill">Where it stops</span></p>
      <h2>It asks before it acts, and it stops at the line you draw.</h2>
      <div class="bp-card">
        <div class="bp-split get-top">
          <div class="bp-cell">
            <p class="get-k">Money waits for you</p>
            <p class="get-v">Charging, invoicing, recording a payment, selling, pricing and buying do not exist for it. It messages you instead.</p>
          </div>
          <div class="bp-cell">
            <p class="get-k">Nobody is contacted without a basis</p>
            <p class="get-v">It reaches a person only when they contacted you, or consented to that channel, or for a cold email to a US business &mdash; and it checks do-not-disturb before every send.</p>
          </div>
          <div class="bp-cell">
            <p class="get-k">Your AI, your account</p>
            <p class="get-v">Its seat is signed in with your own AI account, and it runs your company in your own words from the first hour.</p>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- HOW IT GROWS — vsl-your-ai-ceo.md § the_arc, as one sequence. -->
  <section class="bp-sec bp-band">
    <div class="wrap">
      <p class="eyebrow"><span class="pill">How it grows</span></p>
      <h2>First it drafts and asks. Then it runs the department.</h2>
      <div class="bp-card">
        <div class="bp-split get-top becomes-steps">
          <div class="bp-cell cell-tint tint-gold">
            <p class="get-k">1 &middot; It drafts and asks</p>
            <p class="becomes-result">It writes the work, then stops and asks what it cannot know.</p>
          </div>
          <div class="bp-cell cell-tint tint-cyan">
            <span class="step-arrow" aria-hidden="true">&rarr;</span>
            <p class="get-k">2 &middot; You approve, and it sends</p>
            <p class="becomes-result">Nothing reaches the world until you say so.</p>
          </div>
          <div class="bp-cell cell-tint tint-violet">
            <span class="step-arrow" aria-hidden="true">&rarr;</span>
            <p class="get-k">3 &middot; It answers and books</p>
            <p class="becomes-result">It answers the replies you tell it to, and books the calls.</p>
          </div>
        </div>
        <div class="bp-rule"></div>
        <div class="bp-pad becomes-terminus">
          <p>That is a department, and you did not hire anyone. Every department you add starts the same way.</p>
        </div>
      </div>
    </div>
  </section>

  <section class="bp-sec who-sec">
    <div class="wrap">
      <p class="eyebrow"><span class="pill">Who helps you</span></p>
      <div class="bp-card about-card">
        <div class="bp-split about-split">
          <div class="bp-cell">
            <div class="portrait-frame">
              <img src="assets/isaac-headshot.jpg" alt="Isaac Wostrel-Rubin" width="960" height="1200">
            </div>
          </div>
          <div class="bp-cell">
            <p class="booker-who"><strong>Isaac Wostrel-Rubin</strong><span>Founder of TWI</span></p>
            <p class="lede">Book a call and bring me one part of your business. We will map it together on the call, and I will show you what its CEO does with it on day one. <strong>You cannot automate a box you cannot draw.</strong></p>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="bp-sec bp-ink bp-close">
    <div class="wrap">
      <h2>A tool does what you click. A JobWorld runs your business the way you would.</h2>
      <div class="solo-cta">
        <span class="arm-press" data-arm-press><a class="cta-primary" href="https://app.iwantaiformybusiness.com/pricing">Get JobWorld &rarr;</a></span>
        <span class="arm-press" data-arm-press><button class="cta-primary" type="button" data-buy="call">Book a call &rarr;</button></span>
      </div>
      <p class="door-fine">Subscribe and sign in today, or book a call first — if the answer for your business is to do nothing, I will tell you that.</p>
    </div>
  </section>

</main>

<footer class="footer">
  <span>&copy; 2026 AI Transformations With Isaac</span>
</footer>

{dialog}

<script src="vsl.js?v=2026-09-28h"></script>
<script src="ref.js?v=2026-09-28a"></script>
<script src="capture.js?v=2026-10-08"></script>
<script src="arm.js?v=2026-10-11c"></script>
</body>
</html>
'''

(SITE / 'jobworld.html').write_text(page)
print('wrote', SITE / 'jobworld.html', len(page), 'bytes')
