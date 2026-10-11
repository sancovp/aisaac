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
V_CSS, V_ARM, V_DOOR = '2026-10-11i', '2026-10-11e', '2026-10-11c'


ICONS = {'briefcase': '<rect width="20" height="14" x="2" y="7" rx="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>', 'rocket': '<path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"/><path d="m12 15-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"/><path d="M9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0"/><path d="M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5"/>', 'cap': '<path d="M22 10 12 5 2 10l10 5 10-5z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/><path d="M22 10v6"/>', 'trend': '<polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/>', 'users': '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>', 'store': '<path d="M3 9 4.5 4h15L21 9"/><path d="M4 9v11h16V9"/><path d="M9 20v-6h6v6"/>', 'monitor': '<rect width="20" height="14" x="2" y="3" rx="2"/><path d="M8 21h8M12 17v4"/>', 'bot': '<rect width="16" height="12" x="4" y="8" rx="2"/><path d="M12 8V4H8"/><path d="M2 14h2M20 14h2M15 13v2M9 13v2"/>', 'megaphone': '<path d="m3 11 18-5v12L3 14v-3z"/><path d="M11.6 16.8a3 3 0 1 1-5.8-1.6"/>', 'compass': '<circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/>', 'code': '<polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/>', 'dots': '<circle cx="12" cy="12" r="1"/><circle cx="19" cy="12" r="1"/><circle cx="5" cy="12" r="1"/>', 'phone': '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/>', 'tag': '<path d="M12.6 2.6A2 2 0 0 0 11.2 2H4a2 2 0 0 0-2 2v7.2a2 2 0 0 0 .6 1.4l8.7 8.7a2.4 2.4 0 0 0 3.4 0l6.6-6.6a2.4 2.4 0 0 0 0-3.4z"/><circle cx="7.5" cy="7.5" r=".5"/>'}


def opt(label, sub, attrs, icon='dots', cta='Enter', cls=''):
    """one card of the survey (the June survey's shape: an icon, a title, a line, its call at the foot), pressed by the
    arm (arm.js, sized as for a button: data-arm-h), then door.js moves on"""
    return (f'<span class="arm-press" data-arm-press data-arm-h="54"><button class="door-card{cls}" type="button" {attrs}>'
            f'<span class="get-ico" aria-hidden="true"><svg viewBox="0 0 24 24">{ICONS[icon]}</svg></span>'
            f'<span class="door-card-k">{label}</span><span class="door-card-v">{sub}</span>'
            f'<span class="door-card-go">{cta} &rarr;</span></button></span>')


def pick(label, sub, attrs, icon='dots'):
    """a card the visitor TICKS (one of many) or OPENS (a concern and its answer): no arm, no Enter — the arm presses Next"""
    return (f'<button class="door-card door-pick" type="button" {attrs}>'
            f'<span class="get-ico" aria-hidden="true"><svg viewBox="0 0 24 24">{ICONS[icon]}</svg></span>'
            f'<span class="door-card-k">{label}</span><span class="door-card-v">{sub}</span></button>')


def nxt(label, to, cls='cta-primary'):
    return f'<div class="door-next-row"><span class="arm-press" data-arm-press><button class="{cls} door-next" type="button" data-step="{to}">{label} &rarr;</button></span></div>'


START = [
    opt('I need JobWorld for my business', 'An AI CEO and its departments, working your business.', 'data-step="own-c" data-key="why" data-val="owner"', 'briefcase'),
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



# THE OWNER'S CLOSER (avatar 1, "I need JobWorld for my business"; the hormozi-closer skill). Every pain below is something
# JobWorld does (sanctuary-revolution-alpha/application/jobworld/DESIGN.md: the CEO and departments, the workflows on the
# calendar, the console, the hot pages, the drafts it asks before sending, the repository, the seats); every concern's
# answer is the JobWorld page's own "Where it stops" (jobworld.html) or what the console does (the RUN buttons).
OWN_C = [  # C — CLARIFY: why they are here
    opt('My time back', 'The business stops waiting on me for every decision.', 'data-step="own-l" data-key="own_want" data-val="time"', 'compass', 'Next'),
    opt('Growth without hiring', 'More gets done with the people I have.', 'data-step="own-l" data-key="own_want" data-val="grow"', 'trend', 'Next'),
    opt('Nothing falling through the cracks', 'Every lead and every task followed up.', 'data-step="own-l" data-key="own_want" data-val="cracks"', 'tag', 'Next'),
    opt('AI that actually does the work', 'Not another chat window — work done.', 'data-step="own-l" data-key="own_want" data-val="ai"', 'bot', 'Next'),
]
OWN_L = [  # L — LABEL: they name the pains themselves (pick many); each carries how JobWorld ends it
    pick('Everything waits on me', 'I am the one who knows how it all runs.', 'data-val="bottleneck" data-solve="An AI CEO runs your departments and asks you only what it cannot know."', 'users'),
    pick('Leads go cold before anyone follows up', 'By the time someone gets to them, they have moved on.', 'data-val="leads" data-solve="Workflows fire the moment a lead arrives or changes — the follow-up goes to the right department on time, every time."', 'phone'),
    pick('My business lives in five apps and my head', 'Pipeline, contacts, messages, calendar — scattered.', 'data-val="scattered" data-solve="One dashboard: your pipeline, contacts, conversations, calendar, and every action the agents took."', 'monitor'),
    pick('Outreach and marketing never get done', 'There is always something more urgent.', 'data-val="outreach" data-solve="It drafts the outreach, builds the lead list, and sends when you approve."', 'megaphone'),
    pick('I wait weeks for a report or a page', 'Every small thing needs someone to build it.', 'data-val="pages" data-solve="Ask for a page or a dashboard in one sentence — it is built while you watch."', 'code'),
    pick('When someone leaves, what they knew leaves too', 'The how-we-do-it lives in people.', 'data-val="knowhow" data-solve="Everything it makes is kept in your own private repository, and it loads itself back from it."', 'store'),
]
OWN_O = [  # O — OVERVIEW: what they already tried, said back to them
    opt('Hiring people', 'More hands, more to manage.', 'data-step="own-n" data-key="own_tried" data-val="hire" data-reply="People were the answer until managing them became the job. JobWorld is a company that does not need you to manage it."', 'users', 'Next'),
    opt('Buying software', 'Another tool, another login.', 'data-step="own-n" data-key="own_tried" data-val="software" data-reply="Software does what you click. JobWorld does the work and asks you only what it cannot know."', 'monitor', 'Next'),
    opt('ChatGPT or AI on my own', 'Useful answers, no work done.', 'data-step="own-n" data-key="own_tried" data-val="chat" data-reply="A chat answers a question. JobWorld runs departments — on your own AI account."', 'bot', 'Next'),
    opt('An agency or a consultant', 'They did it, then they left.', 'data-step="own-n" data-key="own_tried" data-val="agency" data-reply="An agency does it and leaves. JobWorld keeps doing it, and everything it makes stays yours."', 'compass', 'Next'),
    opt('Nothing yet', 'This is the first real try.', 'data-step="own-n" data-key="own_tried" data-val="nothing" data-reply="Then you start with a company that already knows how to work."', 'rocket', 'Next'),
]
OWN_N = [  # the size: a seat is one JobWorld for one person in the org chart (jobworld DESIGN §6)
    opt('Just me', 'One JobWorld, with me in the chair.', 'data-step="own-s" data-key="own_seats" data-val="1"', 'briefcase', 'Next'),
    opt('2 to 5 people', 'A seat for each person who runs a part.', 'data-step="own-s" data-key="own_seats" data-val="2-5"', 'users', 'Next'),
    opt('6 to 20 people', 'Departments with their own leads.', 'data-step="own-s" data-key="own_seats" data-val="6-20"', 'store', 'Next'),
    opt('More than 20', 'A whole org chart.', 'data-step="own-s" data-key="own_seats" data-val="21+"', 'trend', 'Next'),
]
OWN_E = [  # E — EXPLAIN: each concern opens its answer
    pick('Will it do things without asking me?', 'Nothing reaches the world until you say so. It drafts, asks, and stops at the line you draw.', 'data-val="ask"', 'compass'),
    pick('Will it touch my money?', 'Charging, invoicing, recording a payment, selling, pricing and buying do not exist for it. It messages you instead.', 'data-val="money"', 'tag'),
    pick('Will it bother my customers?', 'It reaches a person only when they contacted you or consented to that channel — and it checks do-not-disturb before every send.', 'data-val="contact"', 'phone'),
    pick('Whose AI is it?', 'Its seat is signed in with your own AI account, and it runs your company in your own words from the first hour.', 'data-val="whose"', 'bot'),
    pick('I am not technical', 'You talk to it. When something needs running, you get a button that runs it for you.', 'data-val="tech"', 'monitor'),
]
OWN_R = [  # R — REINFORCE, at the cart; then the hand-holding (a business: the retainer, on a call)
    opt('Get JobWorld', 'Your company, with an AI CEO in the chair — starting today.', f'data-go="{APP}/pricing" data-key="own_cart" data-val="get" data-cart', 'rocket', 'See the plans'),
    opt('Set it up with Isaac', 'I map your business with you and we build it in, on a retainer.', 'data-buy="call" data-key="own_cart" data-val="call"', 'phone', 'Book a call', ' door-card-call'),
]


def step(sid, n, pill, h, sub, body, first=False, of=3, mode='', after=''):
    """one screen of the door: its place in its flow (n of `of`, the dots), a question, and its cards; `mode` marks a
    pick-many list (`data-multi`) or a list of concerns (`data-concerns`); `after` follows the cards (a Next, a summary)"""
    return f'''        <div class="door-step{' is-on' if first else ''}" data-step-id="{sid}" data-dot="{n}" data-of="{of}">
          <p class="eyebrow"><span class="pill">{pill}</span></p>
          <h{'1' if first else '2'} class="door-q">{h}</h{'1' if first else '2'}>
          <p class="lede">{sub}</p>
          <div class="door-opts" {mode}>
            {body}
          </div>
          {after}
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
      <div class="door-dots" aria-hidden="true" data-dots></div>
    </div>
{step('start', 1, 'Start here', 'What brings you here?', 'Five ways in. Pick yours.', chr(10).join(START), first=True)}
{step('own-c', 2, 'For your business', 'What do you want most right now?', 'Pick the one that matters most.', chr(10).join(OWN_C), of=8)}
{step('own-l', 3, 'For your business', 'Which of these is happening to you?', 'Tick every one that is true.', chr(10).join(OWN_L), of=8, mode='data-multi="own_pains"', after=nxt('That&rsquo;s me', 'own-o'))}
{step('own-o', 4, 'For your business', 'What have you tried so far?', 'So I do not sell you what already failed you.', chr(10).join(OWN_O), of=8)}
{step('own-n', 5, 'For your business', 'How many people run the business with you?', 'Each of them gets their own JobWorld seat.', chr(10).join(OWN_N), of=8)}
{step('own-s', 6, 'For your business', 'Here is where you will be.', '', '', of=8, after='<div class="door-vac" data-vacation></div>' + nxt('That&rsquo;s what I want', 'own-e'))}
{step('own-e', 7, 'For your business', 'Anything holding you back?', 'Open any one and read the answer.', chr(10).join(OWN_E), of=8, mode='data-concerns', after=nxt('No &mdash; I&rsquo;m in', 'own-r'))}
{step('own-r', 8, 'For your business', 'You are making the right call.', 'Your departments run without waiting on you, nothing goes out without your say, and everything they make stays yours.', chr(10).join(OWN_R), of=8, after='<div class="door-vac door-cart-sum" data-cart-sum></div>')}
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
