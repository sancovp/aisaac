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
TITLE = 'What brings you here? — AI Transformations With Isaac'
DESC = 'Pick the one that sounds like you, and go straight to the part that is for you.'
URL = 'https://iwantaiformybusiness.com/'
V_CSS, V_ARM, V_DOOR = '2026-10-11h', '2026-10-11e', '2026-10-11b'


ICONS = {'briefcase': '<rect width="20" height="14" x="2" y="7" rx="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>', 'rocket': '<path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"/><path d="m12 15-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"/><path d="M9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0"/><path d="M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5"/>', 'cap': '<path d="M22 10 12 5 2 10l10 5 10-5z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/><path d="M22 10v6"/>', 'trend': '<polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/>', 'users': '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>', 'store': '<path d="M3 9 4.5 4h15L21 9"/><path d="M4 9v11h16V9"/><path d="M9 20v-6h6v6"/>', 'monitor': '<rect width="20" height="14" x="2" y="3" rx="2"/><path d="M8 21h8M12 17v4"/>', 'bot': '<rect width="16" height="12" x="4" y="8" rx="2"/><path d="M12 8V4H8"/><path d="M2 14h2M20 14h2M15 13v2M9 13v2"/>', 'megaphone': '<path d="m3 11 18-5v12L3 14v-3z"/><path d="M11.6 16.8a3 3 0 1 1-5.8-1.6"/>', 'compass': '<circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/>', 'code': '<polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/>', 'dots': '<circle cx="12" cy="12" r="1"/><circle cx="19" cy="12" r="1"/><circle cx="5" cy="12" r="1"/>', 'phone': '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/>', 'tag': '<path d="M12.6 2.6A2 2 0 0 0 11.2 2H4a2 2 0 0 0-2 2v7.2a2 2 0 0 0 .6 1.4l8.7 8.7a2.4 2.4 0 0 0 3.4 0l6.6-6.6a2.4 2.4 0 0 0 0-3.4z"/><circle cx="7.5" cy="7.5" r=".5"/>'}


def opt(label, sub, attrs, icon='dots', cta='Enter', cls=''):
    """one card of the survey (the June survey's shape: an icon, a title, a line, its call at the foot), pressed by the
    arm (arm.js, sized as for a button: data-arm-h), then door.js moves on"""
    return (f'<span class="arm-press" data-arm-press data-arm-h="54"><button class="door-card{cls}" type="button" {attrs}>'
            f'<span class="get-ico" aria-hidden="true"><svg viewBox="0 0 24 24">{ICONS[icon]}</svg></span>'
            f'<span class="door-card-k">{label}</span><span class="door-card-v">{sub}</span>'
            f'<span class="door-card-go">{cta} &rarr;</span></button></span>')


START = [
    opt('I need JobWorld for my business', 'An AI CEO and its departments, working your business.', f'data-go="{URL}jobworld" data-key="why" data-val="features"', 'briefcase'),
    opt('I want to start an AI-native business', 'One that runs on AI from the first day.', f'data-go="{URL}jobworld" data-key="why" data-val="ai-native"', 'rocket'),
    opt('I want to learn how to use AI', 'Tell me what for, and I send you the right material.', 'data-step="learn" data-key="why" data-val="learn"', 'cap'),
    opt('I want to learn to sell, market or run my operations', 'The B2B frameworks I use &mdash; then JobWorld does it for you.', f'data-go="{URL}bootcamp" data-key="why" data-val="operate"', 'trend'),
    opt('I want to sell JobWorld to my clients', 'Under your own name, or tailored for them by me.', 'data-step="agency" data-key="why" data-val="agency"', 'users'),
]
LEARN = [
    opt('For my business', 'Where AI goes in the business you run.', 'data-step="learn-send" data-key="for" data-val="business"', 'store', 'Next'),
    opt('For my work', 'Using AI in the job you do.', 'data-step="learn-send" data-key="for" data-val="work"', 'monitor', 'Next'),
    opt('To build my own AI agents', 'Agents, skills and the harnesses they run in.', 'data-step="learn-send" data-key="for" data-val="agents"', 'bot', 'Next'),
]
AGENCY = [
    opt('A marketing or lead-generation agency', 'You run campaigns and leads for clients.', 'data-step="tailor" data-key="do" data-val="agency"', 'megaphone', 'Next'),
    opt('Consulting or coaching', 'You advise owners on how to run the business.', 'data-step="tailor" data-key="do" data-val="consulting"', 'compass', 'Next'),
    opt('Software or IT services', 'You build or run systems for clients.', 'data-step="tailor" data-key="do" data-val="it"', 'code', 'Next'),
    opt('Something else', 'Tell me on the call.', 'data-step="tailor" data-key="do" data-val="other"', 'dots', 'Next'),
]
TAILOR = [
    opt('Yes &mdash; tailor it with me', 'We shape JobWorld around what your clients need, on a call.', 'data-buy="call" data-key="tailor" data-val="call"', 'phone', 'Book a call', ' door-card-call'),
    opt('No &mdash; the agency level', 'JobWorld under your own name, for your own clients.', f'data-go="{APP}/pricing" data-key="tailor" data-val="agency-level"', 'tag', 'See the plans'),
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
<body data-depth="0" class="door-page">
<!-- BUILT by tools/build_door.py — edit the script, then rebuild. THE DOOR: one question, five cards, every card to
     JobWorld by its own way (docs/the-door.md). The top bar carries only the wordmark: the door's exits are its cards. -->
<header class="nav nav-glass">
  <span class="logo">AI Transformations With Isaac</span>
</header>

<!-- THE FILM: the agents' loop, full screen behind everything (the door's look: glass over the film) -->
<video class="door-bg" autoplay muted loop playsinline preload="auto" data-loop
       poster="assets/hero-loop-2-poster.jpg" width="1280" height="720"
       aria-label="The owner leans back at his desk while his company of people and AI agents works on its own, wired together.">
  <source src="assets/hero-loop-2.mp4" type="video/mp4">
</video>

<main id="main" class="door-stage">
  <div class="door-glass door-survey" data-door>
    <div class="door-top">
      <button class="door-back" type="button" data-back hidden>&larr; Back</button>
      <div class="door-dots" aria-hidden="true"><span data-dot-n="1"></span><span data-dot-n="2"></span><span data-dot-n="3"></span></div>
    </div>
{step('start', 1, 'Start here', 'What brings you here?', 'Five ways in. Pick yours.', chr(10).join(START), first=True)}
{step('learn', 2, 'Learn AI', 'Learn AI &mdash; for what?', 'So what I send you fits.', chr(10).join(LEARN))}
{step('learn-send', 3, 'Learn AI', 'I&rsquo;ll send you everything.', 'Where should it go?', SEND)}
{step('agency', 2, 'Sell JobWorld', 'What do you do?', 'So I know who your clients are.', chr(10).join(AGENCY))}
{step('tailor', 3, 'Sell JobWorld', 'Do you want it tailored for your clients?', 'I shape it with you, or you take it as it is under your own name.', chr(10).join(TAILOR))}
  </div>
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
