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
V_CSS, V_ARM, V_DOOR = '2026-10-11k', '2026-10-11e', '2026-10-11e'


ICONS = {'briefcase': '<rect width="20" height="14" x="2" y="7" rx="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>', 'rocket': '<path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"/><path d="m12 15-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"/><path d="M9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0"/><path d="M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5"/>', 'cap': '<path d="M22 10 12 5 2 10l10 5 10-5z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/><path d="M22 10v6"/>', 'trend': '<polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/>', 'users': '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>', 'store': '<path d="M3 9 4.5 4h15L21 9"/><path d="M4 9v11h16V9"/><path d="M9 20v-6h6v6"/>', 'monitor': '<rect width="20" height="14" x="2" y="3" rx="2"/><path d="M8 21h8M12 17v4"/>', 'bot': '<rect width="16" height="12" x="4" y="8" rx="2"/><path d="M12 8V4H8"/><path d="M2 14h2M20 14h2M15 13v2M9 13v2"/>', 'megaphone': '<path d="m3 11 18-5v12L3 14v-3z"/><path d="M11.6 16.8a3 3 0 1 1-5.8-1.6"/>', 'compass': '<circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/>', 'code': '<polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/>', 'dots': '<circle cx="12" cy="12" r="1"/><circle cx="19" cy="12" r="1"/><circle cx="5" cy="12" r="1"/>', 'phone': '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/>', 'tag': '<path d="M12.6 2.6A2 2 0 0 0 11.2 2H4a2 2 0 0 0-2 2v7.2a2 2 0 0 0 .6 1.4l8.7 8.7a2.4 2.4 0 0 0 3.4 0l6.6-6.6a2.4 2.4 0 0 0 0-3.4z"/><circle cx="7.5" cy="7.5" r=".5"/>'}


# each avatar's product-offer (the full table and the lines that go in each: OFFER, below)
OFFER_NAME = {
    'own': 'JobWorld for your business',
    'fnd': 'JobWorld for your new company',
    'lrn': 'JobWorld with my AI skills',
    'ent': 'JobWorld with the frameworks',
    'agc': 'JobWorld Agency',
}


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
    opt('I want to start an AI-native business', 'One that runs on AI from the first day.', 'data-step="fnd-c" data-key="why" data-val="founder"', 'rocket'),
    opt('I want to learn how to use AI', 'For your business, your work, or your own agents.', 'data-step="lrn-c" data-key="why" data-val="learner"', 'cap'),
    opt('I want to learn to sell, market or run my operations', 'The B2B frameworks I use &mdash; and JobWorld runs them with you.', 'data-step="ent-c" data-key="why" data-val="entrepreneur"', 'trend'),
    opt('I want to sell JobWorld to my clients', 'JobWorld under your own name, for your own clients.', 'data-step="agc-c" data-key="why" data-val="agency"', 'users'),
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
OWN_R = [  # R — REINFORCE, at the cart; the B2B avatar is the one offered done-with-you (the retainer) before buying
    opt(f'Get {OFFER_NAME["own"]}', 'Your company, with an AI CEO in the chair — starting today.', f'data-go="{APP}/pricing" data-key="own_cart" data-val="get" data-cart="own"', 'rocket', 'See the plans'),
    opt('Set it up with Isaac', 'I map your business with you and we build it in, on a retainer.', 'data-buy="call" data-key="own_cart" data-val="call"', 'phone', 'Book a call', ' door-card-call'),
]


# THE FOUNDER'S CLOSER (avatar 2, "I want to start an AI-native business"). JobWorld helps them make an idea it can run
# on its own, or helps them run the parts it cannot; one seat; the hand-holding is the community, free with JobWorld.
FND_C = [  # C — CLARIFY: where they are starting from
    opt('I have an idea', 'I know what I want to start.', 'data-step="fnd-l" data-key="fnd_start" data-val="idea"', 'rocket', 'Next'),
    opt('I have a skill, not an idea yet', 'I know what I am good at, not what to sell.', 'data-step="fnd-l" data-key="fnd_start" data-val="skill"', 'compass', 'Next'),
    opt('I have nothing yet but the will', 'I want my own thing, and AI is the way in.', 'data-step="fnd-l" data-key="fnd_start" data-val="will"', 'trend', 'Next'),
    opt('I am leaving a job to do this', 'I need it working before the money runs out.', 'data-step="fnd-l" data-key="fnd_start" data-val="leaving"', 'briefcase', 'Next'),
]
FND_L = [  # L — LABEL
    pick('I do not know which idea will work', 'Every idea looks good until it has to sell.', 'data-val="which" data-solve="It shapes the idea with you into a business it can run on its own — or one it helps you run."', 'compass'),
    pick('I cannot afford a team', 'Everything that needs doing lands on me.', 'data-val="team" data-solve="One seat comes with an AI CEO and its departments: the team is there from the first day."', 'users'),
    pick('I do not know where to start', 'Too many first steps, none of them obvious.', 'data-val="start" data-solve="Its CEO turns what you want into the first week of work, then does it with you."', 'rocket'),
    pick('I start things and never finish them', 'The momentum runs out before the business exists.', 'data-val="finish" data-solve="Workflows on the calendar keep the work moving when you stop — it picks up where it left off."', 'tag'),
    pick('I do not know how to sell or market', 'Building is fine; getting customers is not.', 'data-val="sell" data-solve="It builds the lead list and drafts the outreach, and sends when you approve."', 'megaphone'),
    pick('I am doing it all alone', 'Nobody to think it through with.', 'data-val="alone" data-solve="You talk it through with your CEO any hour, and with the JobWorld community, free."', 'phone'),
]
FND_O = [  # O — OVERVIEW
    opt('A course or a guru', 'I learned a lot and built little.', 'data-step="fnd-s" data-key="fnd_tried" data-val="course" data-reply="A course tells you what to do. JobWorld does it with you, the same day."', 'cap', 'Next'),
    opt('ChatGPT or AI on my own', 'Good answers, still all on me.', 'data-step="fnd-s" data-key="fnd_tried" data-val="chat" data-reply="A chat answers. JobWorld is a company that works — on your own AI account."', 'bot', 'Next'),
    opt('No-code tools and apps', 'A pile of tools and no business.', 'data-step="fnd-s" data-key="fnd_tried" data-val="tools" data-reply="Tools wait for you to run them. JobWorld runs the business and asks you only what it cannot know."', 'monitor', 'Next'),
    opt('Looking for a cofounder', 'Still looking.', 'data-step="fnd-s" data-key="fnd_tried" data-val="cofounder" data-reply="Your CEO is in the chair from the first hour, and it never leaves."', 'users', 'Next'),
    opt('Nothing yet', 'This is the start.', 'data-step="fnd-s" data-key="fnd_tried" data-val="nothing" data-reply="Then you start with a company that already knows how to work."', 'rocket', 'Next'),
]
FND_E = [  # E — EXPLAIN
    pick('I do not have the idea yet', 'It helps you make one it can run on its own — or one it helps you run, where it cannot.', 'data-val="idea"', 'compass'),
    pick('I cannot pay for staff', 'You do not need to: one seat is you, and the departments are its AI.', 'data-val="staff"', 'users'),
    pick('Will it spend my money?', 'Charging, invoicing, recording a payment, selling, pricing and buying do not exist for it. It messages you instead.', 'data-val="money"', 'tag'),
    pick('I am not technical', 'You talk to it. When something needs running, you get a button that runs it for you.', 'data-val="tech"', 'monitor'),
    pick('Whose AI is it?', 'Its seat is signed in with your own AI account. What it makes is kept in your own private repository.', 'data-val="whose"', 'bot'),
]
FND_R = [  # R — REINFORCE, at the cart; the hand-holding for an individual is the community, free with JobWorld
    opt(f'Get {OFFER_NAME["fnd"]}', 'Your new company, with an AI CEO in the chair from day one. The community comes with it, free.', f'data-go="{APP}/pricing" data-key="fnd_cart" data-val="get" data-cart="fnd"', 'rocket', 'See the plans'),
]

# THE LEARNER'S CLOSER (avatar 3, "I want to learn how to use AI"). JobWorld carries the Claude compilation skills and
# teaches AI by doing it with them; the free sign-up is the hand-holding: the weekly letter (what it means for people
# using JobWorld), every framework and manual, and the community where they share and help each other.
LRN_C = [  # C — CLARIFY: what for
    opt('For my business', 'Where AI goes in the business you run.', 'data-step="lrn-l" data-key="lrn_for" data-val="business"', 'store', 'Next'),
    opt('For my work', 'Using AI in the job you do.', 'data-step="lrn-l" data-key="lrn_for" data-val="work"', 'monitor', 'Next'),
    opt('To build my own AI agents', 'Agents, skills and the harnesses they run in.', 'data-step="lrn-l" data-key="lrn_for" data-val="agents"', 'bot', 'Next'),
]
LRN_L = [  # L — LABEL
    pick('I use it like a search box', 'Questions in, answers out, nothing more.', 'data-val="search" data-solve="You watch it work — departments, workflows, pages — and ask why at every step."', 'monitor'),
    pick('Every tutorial is out of date by next week', 'The tools move faster than the lessons.', 'data-val="dated" data-solve="The weekly letter says what each change means for you, in JobWorld, that week."', 'cap'),
    pick('I do not know what is possible', 'Everyone says AI can do anything; nobody shows what.', 'data-val="possible" data-solve="It shows you, running: a company of agents doing real work while you watch."', 'compass'),
    pick('I learn it and never use it', 'It does not stick because it is not tied to real work.', 'data-val="stick" data-solve="You learn on your own work: it does the job with you, and you keep what it built."', 'tag'),
    pick('Agents break when I build them', 'They work once and fall over.', 'data-val="agents" data-solve="It carries my Claude compilation skills — the way I build agents that hold up — and builds with you."', 'code'),
]
LRN_O = [  # O — OVERVIEW
    opt('YouTube and free tutorials', 'A lot of watching.', 'data-step="lrn-s" data-key="lrn_tried" data-val="youtube" data-reply="Watching shows you someone else doing it. JobWorld does it with you, on yours."', 'monitor', 'Next'),
    opt('A paid course', 'Finished it, or meant to.', 'data-step="lrn-s" data-key="lrn_tried" data-val="course" data-reply="A course ends. JobWorld keeps teaching, because it keeps working with you."', 'cap', 'Next'),
    opt('Using ChatGPT or Claude', 'Every day, but only so far.', 'data-step="lrn-s" data-key="lrn_tried" data-val="chat" data-reply="That is the right start. JobWorld is what comes next: the same AI, running a company."', 'bot', 'Next'),
    opt('Nothing yet', 'Starting from zero.', 'data-step="lrn-s" data-key="lrn_tried" data-val="nothing" data-reply="Then you start on the real thing, not a toy."', 'rocket', 'Next'),
]
LRN_E = [  # E — EXPLAIN
    pick('I am not technical', 'You talk to it. When something needs running, you get a button that runs it for you.', 'data-val="tech"', 'monitor'),
    pick('Is it just another course?', 'No — it is the AI system itself, working. The letter, the frameworks and the manuals sit beside it.', 'data-val="course"', 'cap'),
    pick('What does the free part give me?', 'Every week, the letter on what is new and what it means in JobWorld; every framework and manual; and the community, where people using it help each other.', 'data-val="free"', 'users'),
    pick('Whose AI is it?', 'Its seat is signed in with your own AI account. You learn on the account you will keep using.', 'data-val="whose"', 'bot'),
]
LRN_R = [  # R — REINFORCE, at the cart; then the free hand-holding
    opt(f'Get {OFFER_NAME["lrn"]}', 'Learn AI by running it — it does the work with you and shows you how.', f'data-go="{APP}/pricing" data-key="lrn_cart" data-val="get" data-cart="lrn"', 'rocket', 'See the plans'),
    opt('Start free', 'The weekly letter, every framework and manual, and the community.', 'data-step="lrn-send" data-key="lrn_cart" data-val="free"', 'cap', 'Sign me up'),
]

# THE ENTREPRENEUR'S CLOSER (avatar 4, "I want to learn to sell, market or run my operations"). Need frameworks? Here they
# are (the B2B bootcamp, /bootcamp, for entrepreneurs to learn from) — and they are inside JobWorld too: want that?
ENT_C = [  # C — CLARIFY: which of the three
    opt('Sell', 'Turn conversations into customers.', 'data-step="ent-l" data-key="ent_want" data-val="sell"', 'phone', 'Next'),
    opt('Market', 'Get noticed by the right people.', 'data-step="ent-l" data-key="ent_want" data-val="market"', 'megaphone', 'Next'),
    opt('Run my operations', 'Deliver without it all running through me.', 'data-step="ent-l" data-key="ent_want" data-val="run"', 'store', 'Next'),
    opt('All three', 'The whole machine.', 'data-step="ent-l" data-key="ent_want" data-val="all"', 'trend', 'Next'),
]
ENT_L = [  # L — LABEL; each pain carries the framework that answers it
    pick('Nobody notices me', 'I post and nothing comes back.', 'data-val="noticed" data-solve="PSA: the broadcast that names a condition they did not know they had."', 'megaphone'),
    pick('I talk to the wrong people', 'Calls with people who were never going to buy.', 'data-val="wrong" data-solve="SCREENING: a five-minute check that routes them — in, nurture, or not your client."', 'users'),
    pick('My close feels like a pitch', 'They go cold the moment I mention price.', 'data-val="close" data-solve="CLINIC · DOCTOR: they see the leak themselves, and yes feels like being treated."', 'phone'),
    pick('Clients leave after the first result', 'Nothing keeps them past the sale.', 'data-val="churn" data-solve="LIFE: the systems keep working, and they refer and ask what else you do."', 'tag'),
    pick('My offer is hard to explain', 'People nod and do not buy.', 'data-val="offer" data-solve="MEDICINE and OFFERS: one bundle that overcomes every obstacle, laid out as a treatment plan."', 'store'),
    pick('Delivery runs through me', 'I am the bottleneck of my own business.', 'data-val="delivery" data-solve="JobWorld runs the path for you — its CEO and departments do the selling, the marketing and the operations."', 'briefcase'),
]
ENT_O = [  # O — OVERVIEW
    opt('Books and courses', 'I know the theory.', 'data-step="ent-s" data-key="ent_tried" data-val="course" data-reply="You know the theory. Here it is as frameworks you run — and a system that runs them with you."', 'cap', 'Next'),
    opt('A coach or a mastermind', 'Good advice, still my job to do it.', 'data-step="ent-s" data-key="ent_tried" data-val="coach" data-reply="Advice still leaves the work to you. JobWorld does the work, in the frameworks."', 'compass', 'Next'),
    opt('Hiring a salesperson or marketer', 'It did not stick.', 'data-step="ent-s" data-key="ent_tried" data-val="hire" data-reply="People need a playbook first. These are the playbook — and JobWorld runs it."', 'users', 'Next'),
    opt('Doing it all myself', 'Every night.', 'data-step="ent-s" data-key="ent_tried" data-val="self" data-reply="Then the frameworks give you the shape, and JobWorld takes the hours."', 'briefcase', 'Next'),
]
ENT_F = [  # the frameworks, here — each opens what it is (the bootcamp's own words)
    pick('PSA — get noticed', 'The broadcast — an ad, a post, a cold email — that names a condition they did not know they had, and invites them to get screened.', 'data-val="psa"', 'megaphone'),
    pick('SCREENING — qualify', 'A five-minute check. Then route them: in, nurture, or not your client.', 'data-val="screening"', 'users'),
    pick('CLINIC · DOCTOR — diagnose and close', 'Diagnose · Observe · Consequences · Treat · Options · Resolve. They see the leak themselves, and saying yes feels like being treated.', 'data-val="doctor"', 'phone'),
    pick('LIFE — keep them', 'Love · Interest · Fulfillment · Excel. They leave reviews, refer others, and ask what else you can do.', 'data-val="life"', 'tag'),
    pick('MEDICINE · OFFERS — build the offer', 'One bundle that overcomes every obstacle on the client&rsquo;s journey, laid out as a treatment plan in tiers.', 'data-val="offer"', 'store'),
]
ENT_E = [  # E — EXPLAIN
    pick('Can I just use the frameworks?', 'Yes — they are free on the bootcamp page. JobWorld is for when you want them run with you and for you.', 'data-val="free"', 'cap'),
    pick('Will it sell for me without asking?', 'Nothing reaches the world until you say so. It drafts, asks, and stops at the line you draw.', 'data-val="ask"', 'compass'),
    pick('Will it bother my customers?', 'It reaches a person only when they contacted you or consented to that channel — and it checks do-not-disturb before every send.', 'data-val="contact"', 'phone'),
    pick('Will it touch my money?', 'Charging, invoicing, recording a payment, selling, pricing and buying do not exist for it. It messages you instead.', 'data-val="money"', 'tag'),
]
ENT_R = [  # R — REINFORCE, at the cart (the front end only: done-with-you is offered after they buy, docs/the-door.md §4)
    opt(f'Get {OFFER_NAME["ent"]}', 'The frameworks, run with you and for you. The community comes with it, free.', f'data-go="{APP}/pricing" data-key="ent_cart" data-val="get" data-cart="ent"', 'rocket', 'See the plans'),
]

# THE AGENCY'S CLOSER (avatar 5, "I want to sell JobWorld to my clients"). The cart is the agency level — Meta Business
# (lamai-saas DESIGN §2): JobWorld under their own brand, each client its own business under them, paid in their own
# Stripe; tailoring it with Isaac is offered once they have bought (docs/the-door.md §4).
AGC_C = [  # C — CLARIFY: what they do
    opt('A marketing or lead-generation agency', 'You run campaigns and leads for clients.', 'data-step="agc-l" data-key="agc_do" data-val="agency"', 'megaphone', 'Next'),
    opt('Consulting or coaching', 'You advise owners on how to run the business.', 'data-step="agc-l" data-key="agc_do" data-val="consulting"', 'compass', 'Next'),
    opt('Software or IT services', 'You build or run systems for clients.', 'data-step="agc-l" data-key="agc_do" data-val="it"', 'code', 'Next'),
    opt('Something else', 'You serve businesses another way.', 'data-step="agc-l" data-key="agc_do" data-val="other"', 'dots', 'Next'),
]
AGC_L = [  # L — LABEL
    pick('Clients leave when results stall', 'Month three is when they start asking.', 'data-val="churn" data-solve="Each client gets a JobWorld working their business every day — results that do not wait on your team."', 'tag'),
    pick('Delivery does not scale past my team', 'Every new client means another hire.', 'data-val="scale" data-solve="Each client is its own business under you, with its own login and its own AI departments."', 'users'),
    pick('I resell tools under someone else&rsquo;s name', 'My clients see the vendor, not me.', 'data-val="brand" data-solve="Your name, logo, colours, domain and email — our mark never shows."', 'store'),
    pick('Every client needs a custom setup', 'Onboarding eats the margin.', 'data-val="setup" data-solve="Set your version up once, and every client starts from it."', 'code'),
    pick('My recurring revenue is thin', 'Projects end; retainers wobble.', 'data-val="mrr" data-solve="Your clients pay you in your own Stripe, every month; you pay us one monthly bill."', 'trend'),
]
AGC_O = [  # O — OVERVIEW
    opt('A white-label software', 'It is theirs, with my sticker on it.', 'data-step="agc-n" data-key="agc_tried" data-val="whitelabel" data-reply="A sticker on someone else&rsquo;s tool. This is a company of AI working each client&rsquo;s business, under your brand."', 'tag', 'Next'),
    opt('Building my own tools', 'It works until I have to maintain it.', 'data-step="agc-n" data-key="agc_tried" data-val="build" data-reply="You keep the client; we keep the system running."', 'code', 'Next'),
    opt('Hiring more delivery staff', 'Margins went with them.', 'data-step="agc-n" data-key="agc_tried" data-val="hire" data-reply="The delivery is the AI&rsquo;s. Your team does what only people can."', 'users', 'Next'),
    opt('Nothing yet', 'This would be new.', 'data-step="agc-n" data-key="agc_tried" data-val="nothing" data-reply="Then you start with a product that already runs, under your own name."', 'rocket', 'Next'),
]
AGC_N = [  # the size: how many clients they would put on it
    opt('1 to 5 clients', 'Start with the ones who need it most.', 'data-step="agc-s" data-key="agc_clients" data-val="1-5"', 'briefcase', 'Next'),
    opt('6 to 20 clients', 'A book of business.', 'data-step="agc-s" data-key="agc_clients" data-val="6-20"', 'users', 'Next'),
    opt('21 to 100 clients', 'An agency at scale.', 'data-step="agc-s" data-key="agc_clients" data-val="21-100"', 'store', 'Next'),
    opt('More than 100', 'A platform of your own.', 'data-step="agc-s" data-key="agc_clients" data-val="100+"', 'trend', 'Next'),
]
AGC_E = [  # E — EXPLAIN
    pick('Do my clients see your name?', 'No. Under your brand the header, the tab and the sign-up carry your name and mark; ours never shows.', 'data-val="brand"', 'store'),
    pick('Who bills my clients?', 'You do, through your own Stripe. You pay us one monthly bill.', 'data-val="bill"', 'tag'),
    pick('Can each client be set up differently?', 'Each client is its own business with its own setup, started from your version.', 'data-val="setup"', 'code'),
    pick('Will it act for my clients without asking?', 'Nothing reaches the world until they say so. It drafts, asks, and stops at the line they draw.', 'data-val="ask"', 'compass'),
    pick('Will it touch their money?', 'Charging, invoicing, recording a payment, selling, pricing and buying do not exist for it.', 'data-val="money"', 'tag'),
]
AGC_R = [  # R — REINFORCE, at the cart (JobWorld Agency); tailoring with Isaac is offered after they buy (docs/the-door.md §4)
    opt(f'Get {OFFER_NAME["agc"]}', 'JobWorld under your own name, for your own clients &mdash; starting today.', f'data-go="{APP}/pricing" data-key="agc_cart" data-val="get" data-cart="agc" data-tier="meta"', 'rocket', 'See the plans'),
]


# THE OFFERS — one product per avatar, each a JobWorld (docs/the-door.md §3–§4; the tiers are application/jobworld/DESIGN.md
# §2): the owner's, founder's, learner's and entrepreneur's are the client JobWorld, each loaded for that avatar; the
# agency's is the agency JobWorld, which makes client JobWorlds its own way. No prices here (the plans page holds them).
# Each line is what is known to go in it now; lines are added as each offer is built up.
OFFER = {
    'own': ['JobWorld for your business: an AI CEO in the chair, and its departments',
            'A seat for each person who runs part of the business',
            'Workflows on the calendar, the dashboard, and pages built on request',
            'Everything it makes kept in your own private repository',
            'Nothing goes out without your say; your money never moves',
            'The JobWorld community, free'],
    'fnd': ['JobWorld, one seat: an AI CEO and its departments from day one',
            'An idea shaped with you into a business it can run on its own &mdash; or one it helps you run',
            'Outreach drafted and lead lists built, sent when you approve',
            'Everything it makes kept in your own private repository',
            'The JobWorld community, free'],
    'lrn': ['JobWorld: it does the work with you and shows you how',
            'My Claude compilation skills, inside it',
            'The weekly letter, every framework and manual',
            'The JobWorld community, free'],
    'ent': ['JobWorld, running the frameworks with you and for you',
            'PSA &middot; SCREENING &middot; CLINIC &middot; DOCTOR &middot; LIFE &middot; MEDICINE &middot; OFFERS, inside it',
            'Its CEO and departments doing the selling, the marketing and the operations',
            'Nothing goes out without your say; your money never moves',
            'The JobWorld community, free'],
    'agc': ['A JobWorld that makes your clients&rsquo; JobWorlds &mdash; your way, under your own name',
            'Your name, logo, colours, domain and email &mdash; ours never shows',
            'Each client its own JobWorld, with its own login, under you',
            'Your clients pay you in your own Stripe; one monthly bill to us',
            'The JobWorld community, free'],
}


def offer(p):
    """the offer box at a cart: what they get, then the size their answers chose (door.js fills data-cart-sum)"""
    items = ''.join(f'<li>{x}</li>' for x in OFFER[p])
    return (f'<div class="door-offer"><p class="door-offer-k">{OFFER_NAME[p]} &mdash; what you get</p><ul class="door-offer-list">{items}</ul>'
            f'<div class="door-cart-sum" data-cart-sum="{p}"></div></div>')


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
              <p class="door-fine">Free: the weekly letter, every framework and manual, and the community. Then you meet JobWorld.</p>
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
       poster="assets/hero-loop-2-poster.jpg" width="1280" height="720" data-backdrop
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
{step('own-s', 6, 'For your business', 'Here is where you will be.', '', '', of=8, after='<div class="door-vac" data-vacation="own"></div>' + nxt('That&rsquo;s what I want', 'own-e'))}
{step('own-e', 7, 'For your business', 'Anything holding you back?', 'Open any one and read the answer.', chr(10).join(OWN_E), of=8, mode='data-concerns="own_concerns"', after=nxt('No &mdash; I&rsquo;m in', 'own-r'))}
{step('own-r', 8, 'For your business', 'You are making the right call.', 'Your departments run without waiting on you, nothing goes out without your say, and everything they make stays yours.', chr(10).join(OWN_R), of=8, after=offer('own'))}
{step('fnd-c', 2, 'Start a business', 'Where are you starting from?', 'Pick the one that is closest.', chr(10).join(FND_C), of=7)}
{step('fnd-l', 3, 'Start a business', 'What is in the way?', 'Tick every one that is true.', chr(10).join(FND_L), of=7, mode='data-multi="fnd_pains"', after=nxt('That&rsquo;s me', 'fnd-o'))}
{step('fnd-o', 4, 'Start a business', 'What have you tried so far?', 'So I do not sell you what already failed you.', chr(10).join(FND_O), of=7)}
{step('fnd-s', 5, 'Start a business', 'Here is where you will be.', '', '', of=7, after='<div class="door-vac" data-vacation="fnd"></div>' + nxt('That&rsquo;s what I want', 'fnd-e'))}
{step('fnd-e', 6, 'Start a business', 'Anything holding you back?', 'Open any one and read the answer.', chr(10).join(FND_E), of=7, mode='data-concerns="fnd_concerns"', after=nxt('No &mdash; I&rsquo;m in', 'fnd-r'))}
{step('fnd-r', 7, 'Start a business', 'You are making the right call.', 'You start with a company that already knows how to work, it asks before anything goes out, and everything it makes is yours.', chr(10).join(FND_R), of=7, after=offer('fnd'))}
{step('lrn-c', 2, 'Learn AI', 'Learn AI &mdash; for what?', 'So what you learn fits.', chr(10).join(LRN_C), of=8)}
{step('lrn-l', 3, 'Learn AI', 'Where does it stop working for you?', 'Tick every one that is true.', chr(10).join(LRN_L), of=8, mode='data-multi="lrn_pains"', after=nxt('That&rsquo;s me', 'lrn-o'))}
{step('lrn-o', 4, 'Learn AI', 'How have you learned so far?', 'So I do not sell you what already failed you.', chr(10).join(LRN_O), of=8)}
{step('lrn-s', 5, 'Learn AI', 'Here is where you will be.', '', '', of=8, after='<div class="door-vac" data-vacation="lrn"></div>' + nxt('That&rsquo;s what I want', 'lrn-e'))}
{step('lrn-e', 6, 'Learn AI', 'Anything holding you back?', 'Open any one and read the answer.', chr(10).join(LRN_E), of=8, mode='data-concerns="lrn_concerns"', after=nxt('No &mdash; I&rsquo;m in', 'lrn-r'))}
{step('lrn-r', 7, 'Learn AI', 'You are making the right call.', 'You learn AI by using it on real work, and you are never learning it alone.', chr(10).join(LRN_R), of=8, after=offer('lrn'))}
{step('lrn-send', 8, 'Learn AI', 'Where should it go?', 'The weekly letter, the frameworks and manuals, and the way into the community.', SEND, of=8)}
{step('ent-c', 2, 'Grow your business', 'What do you want to get better at?', 'Pick the one that matters most.', chr(10).join(ENT_C), of=8)}
{step('ent-l', 3, 'Grow your business', 'Where does it stall?', 'Tick every one that is true.', chr(10).join(ENT_L), of=8, mode='data-multi="ent_pains"', after=nxt('That&rsquo;s me', 'ent-o'))}
{step('ent-o', 4, 'Grow your business', 'What have you tried so far?', 'So I do not sell you what already failed you.', chr(10).join(ENT_O), of=8)}
{step('ent-s', 5, 'Grow your business', 'Here is where you will be.', '', '', of=8, after='<div class="door-vac" data-vacation="ent"></div>' + nxt('Show me how', 'ent-f'))}
{step('ent-f', 6, 'Grow your business', 'You need frameworks. Here they are.', 'Open any one. All of them, free, are on <a href="bootcamp" target="_blank" rel="noopener">the bootcamp page</a> &mdash; and every one runs inside JobWorld too.', chr(10).join(ENT_F), of=8, mode='data-concerns="ent_frameworks"', after=nxt('I want them run for me', 'ent-e'))}
{step('ent-e', 7, 'Grow your business', 'Anything holding you back?', 'Open any one and read the answer.', chr(10).join(ENT_E), of=8, mode='data-concerns="ent_concerns"', after=nxt('No &mdash; I&rsquo;m in', 'ent-r'))}
{step('ent-r', 8, 'Grow your business', 'You are making the right call.', 'You have the frameworks, and a system that runs them with you and for you.', chr(10).join(ENT_R), of=8, after=offer('ent'))}
{step('agc-c', 2, 'Sell JobWorld', 'What do you do?', 'So I know who your clients are.', chr(10).join(AGC_C), of=8)}
{step('agc-l', 3, 'Sell JobWorld', 'What is hard about it now?', 'Tick every one that is true.', chr(10).join(AGC_L), of=8, mode='data-multi="agc_pains"', after=nxt('That&rsquo;s me', 'agc-o'))}
{step('agc-o', 4, 'Sell JobWorld', 'What have you tried so far?', 'So I do not sell you what already failed you.', chr(10).join(AGC_O), of=8)}
{step('agc-n', 5, 'Sell JobWorld', 'How many clients would you put on it?', 'Each one gets its own JobWorld, under your name.', chr(10).join(AGC_N), of=8)}
{step('agc-s', 6, 'Sell JobWorld', 'Here is where you will be.', '', '', of=8, after='<div class="door-vac" data-vacation="agc"></div>' + nxt('That&rsquo;s what I want', 'agc-e'))}
{step('agc-e', 7, 'Sell JobWorld', 'Anything holding you back?', 'Open any one and read the answer.', chr(10).join(AGC_E), of=8, mode='data-concerns="agc_concerns"', after=nxt('No &mdash; I&rsquo;m in', 'agc-r'))}
{step('agc-r', 8, 'Sell JobWorld', 'You are making the right call.', 'Your clients get a company of AI working their business, under your name, billed by you.', chr(10).join(AGC_R), of=8, after=offer('agc'))}
  </div>
</main>

{dialog}

<script src="vsl.js?v=2026-10-11d"></script>
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
