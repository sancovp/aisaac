"""Builds aisaac/door.html — THE DOOR, the home of iwantaiformybusiness.com (00-SITE-CANON § WHAT IS PUBLIC; docs/the-door.md).

One question, five cards; every card routes to JobWorld, each by its own way. Its logic is the survey the site had on
2026-06-10 (`git show 9b26f427:index.html`): the cards, a short flow under some of them, step dots, a back button, the
answers kept in localStorage. Every option is a button the ARM PRESSES (arm.js, RULE 02 §8b); every step slides in.
The booking dialog is lifted whole from ai-transformation.html and the consent boxes from framework.html, so every
form shares one wording (law 13). Edit this script and rebuild; never edit door.html by hand.
"""
import pathlib
import re

SITE = pathlib.Path(__file__).resolve().parent.parent
landing = (SITE / 'ai-transformation.html').read_text()
dialog = landing[landing.index('<dialog class="capture"'):landing.index('</dialog>') + len('</dialog>')]
assert 'consent_version' in dialog and 'data-consent="recording"' in dialog
fw = (SITE / 'framework.html').read_text()
fieldset = fw[fw.index('<fieldset class="consents">'):fw.index('</fieldset>', fw.index('<fieldset class="consents">')) + len('</fieldset>')]
assert fieldset.count('data-consent=') == 5 and 'phone-field' in fieldset
fieldset = re.sub(r'<p class="consents-note">.*?</p>',
                  '<p class="consents-note">What I recommend comes by email either way. Everything after it is your choice &mdash; every box below is optional: tick the ones you want.</p>',
                  fieldset, count=1, flags=re.S)

APP = 'https://app.iwantaiformybusiness.com'
TITLE = 'Why are you here? — AI Transformations With Isaac'
DESC = 'Pick the one that sounds like you, and go straight to the part that is for you.'
URL = 'https://iwantaiformybusiness.com/'
V_CSS, V_ARM, V_DOOR = '2026-10-11e', '2026-10-11c', '2026-10-11a'


def opt(label, sub, attrs):
    """one option: a button the arm presses, then door.js moves on"""
    return (f'<span class="arm-press" data-arm-press><button class="door-opt" type="button" {attrs}>'
            f'<span class="door-opt-k">{label}</span><span class="door-opt-sub">{sub}</span></button></span>')


START = [
    opt('I need JobWorld for my business', 'An AI CEO and its departments, working your business.', f'data-go="{URL}jobworld" data-key="why" data-val="features"'),
    opt('I want to start an AI-native business', 'One that runs on AI from the first day.', f'data-go="{URL}jobworld" data-key="why" data-val="ai-native"'),
    opt('I want to learn how to use AI', 'Tell me what for, and I send you the right material.', 'data-step="learn" data-key="why" data-val="learn"'),
    opt('I want to learn to sell, market or run my operations', 'The frameworks I use &mdash; then JobWorld does it for you.', f'data-go="{URL}framework" data-key="why" data-val="operate"'),
    opt('I want to sell JobWorld to my clients', 'Under your own name, or tailored for them by me.', 'data-step="agency" data-key="why" data-val="agency"'),
]
LEARN = [
    opt('For my business', 'Where AI goes in the business you run.', 'data-step="learn-send" data-key="for" data-val="business"'),
    opt('For my work', 'Using AI in the job you do.', 'data-step="learn-send" data-key="for" data-val="work"'),
    opt('To build my own AI agents', 'Agents, skills and the harnesses they run in.', 'data-step="learn-send" data-key="for" data-val="agents"'),
]
AGENCY = [
    opt('A marketing or lead-generation agency', 'You run campaigns and leads for clients.', 'data-step="tailor" data-key="do" data-val="agency"'),
    opt('Consulting or coaching', 'You advise owners on how to run the business.', 'data-step="tailor" data-key="do" data-val="consulting"'),
    opt('Software or IT services', 'You build or run systems for clients.', 'data-step="tailor" data-key="do" data-val="it"'),
    opt('Something else', 'Tell me on the call.', 'data-step="tailor" data-key="do" data-val="other"'),
]
TAILOR = [
    ('<span class="arm-press" data-arm-press><button class="door-opt door-opt-call" type="button" data-buy="call" data-key="tailor" data-val="call">'
     '<span class="door-opt-k">Yes &mdash; book a call with Isaac</span><span class="door-opt-sub">We shape JobWorld around what your clients need.</span></button></span>'),
    opt('No &mdash; get the agency level', 'JobWorld under your own name, for your own clients.', f'data-go="{APP}/pricing" data-key="tailor" data-val="agency-level"'),
]


def step(sid, n, pill, h, sub, body, first=False):
    return f'''        <div class="door-step{' is-on' if first else ''}" data-step-id="{sid}" data-dot="{n}">
          <p class="eyebrow"><span class="pill">{pill}</span></p>
          <h{'1' if first else '2'} class="door-q">{h}</h{'1' if first else '2'}>
          <p class="lede">{sub}</p>
          <div class="door-opts">
            {body}
          </div>
        </div>'''


SEND = f'''<form class="lead-form door-form" method="POST" action="https://iwantaiformybusiness.com/api/lead">
              <input type="hidden" name="intent" value="learn">
              <input type="hidden" name="learn_for" value="">
              <input type="hidden" name="_next" value="{URL}jobworld">
              <div class="lead-row">
                <label class="lead-field"><span>Your name</span>
                  <input type="text" name="name" autocomplete="name" required placeholder="Your name">
                </label>
                <label class="lead-field"><span>Email</span>
                  <input type="email" name="email" autocomplete="email" required placeholder="you@company.com">
                </label>
              </div>
              {fieldset}
              <input type="hidden" name="consent_version" value="2026-10-08">
              <input type="hidden" name="consent_record" value="">
              <span class="arm-press" data-arm-press><button class="cta-primary" type="submit">Send it to me &rarr;</button></span>
              <p class="door-fine">Free. Then you meet JobWorld &mdash; it teaches AI too.</p>
            </form>'''

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
<link rel="stylesheet" href="style.css?v={V_CSS}">
</head>
<body data-depth="0">
<!-- BUILT by tools/build_door.py — edit the script, then rebuild. THE DOOR: one question, five cards, every card to
     JobWorld by its own way (docs/the-door.md). The top bar carries only the wordmark: the door's exits are its cards. -->
<header class="nav nav-glass">
  <span class="logo">AI Transformations With Isaac</span>
</header>

<main id="main">
  <section class="bp-hero">
    <div class="wrap">
      <div class="bp-card">
        <div class="hero-split">
          <div class="hero-copy door-survey" data-door>
            <div class="door-top">
              <button class="door-back" type="button" data-back hidden>&larr; Back</button>
              <div class="door-dots" aria-hidden="true"><span data-dot-n="1"></span><span data-dot-n="2"></span><span data-dot-n="3"></span></div>
            </div>
{step('start', 1, 'Start here', 'Why are you here?', 'Pick the one that sounds most like you.', chr(10).join(START), first=True)}
{step('learn', 2, 'Learn AI', 'Learn AI &mdash; for what?', 'So what I send you fits.', chr(10).join(LEARN))}
{step('learn-send', 3, 'Learn AI', 'I&rsquo;ll send you everything.', 'Where should it go?', SEND)}
{step('agency', 2, 'Sell JobWorld', 'What do you do?', 'So I know who your clients are.', chr(10).join(AGENCY))}
{step('tailor', 3, 'Sell JobWorld', 'Do you want it tailored for your clients?', 'I shape it with you, or you take it as it is under your own name.', chr(10).join(TAILOR))}
          </div>
          <div class="hero-art">
            <video autoplay muted loop playsinline preload="auto" data-loop
                   poster="assets/hero-loop-2-poster.jpg" width="1280" height="720"
                   aria-label="The owner leans back at his desk while his company of people and AI agents works on its own, wired together.">
              <source src="assets/hero-loop-2.mp4" type="video/mp4">
            </video>
          </div>
        </div>
      </div>
    </div>
  </section>
</main>

{dialog}

<script src="vsl.js?v=2026-09-28h"></script>
<script src="ref.js?v=2026-09-28a"></script>
<script src="capture.js?v=2026-10-08"></script>
<script src="consent.js?v=2026-10-08"></script>
<script src="arm.js?v={V_ARM}"></script>
<script src="door.js?v={V_DOOR}"></script>
</body>
</html>
'''
(SITE / 'door.html').write_text(page)
print(f'wrote {SITE / "door.html"} {len(page)} bytes')
