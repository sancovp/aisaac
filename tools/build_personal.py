"""Builds aisaac/isaac-wostrel-rubin.html — Isaac's personal page in the Blueprint System.

The book passages are pulled from the manuscript BY LINE RANGE at build time, so every quoted
word is the manuscript's own; the booking dialog is lifted whole from ai-transformation.html so
the two pages share one form.
"""
import html, re, pathlib

SITE = pathlib.Path('/Users/isaacwr/claude_code/aisaac')
MS = pathlib.Path('/Users/isaacwr/claude_code/sanctuary-revolution-alpha/research/ssri/ship/arrow-book/MANUSCRIPT.md')
ms = MS.read_text().split('\n')

def md_inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'\*(.+?)\*', r'<em>\1</em>', t)
    return t

def passage(a, b):
    """manuscript lines a..b (1-indexed, inclusive) → <p> per non-empty source paragraph."""
    paras = [l for l in ms[a - 1:b] if l.strip()]
    return '\n'.join(f'            <p>{md_inline(p)}</p>' for p in paras)

# the five passages — each a CONTIGUOUS run of Chapter One, never stitched
EXCERPTS = [(136, 136), (146, 148), (220, 238), (298, 306), (312, 324)]
assert ms[131].startswith('# CHAPTER ONE'), ms[131]
excerpts = '\n          </blockquote>\n          <blockquote class="book-excerpt">\n'.join(passage(a, b) for a, b in EXCERPTS)

src = (SITE / 'ai-transformation.html').read_text()
dialog = src[src.index('<dialog class="capture"'):src.index('</dialog>') + len('</dialog>')]

BELIEFS = [
 ("Iteration doesn’t compound. Worlds do.",
  "Running the same loop more times plateaus. The step change comes from injecting a bigger space to search in and an instrument to see the results with — capability, not repetition. A world is the thing that holds both: the space persists between runs, and the instruments accumulate. That is the difference between a loop that spins and a system that climbs.",
  "I ran roughly a hundred flat cycles of a generative loop with no meaningful gain, then added a combinatorial kernel and one observation instrument and the output jumped in a single step. The same shape is visible in the published numbers of the multi-agent loops that went viral this summer: their parallel rounds gained less than their sequential ones, and the real lift came from a harness someone bolted on, not from more rounds. My own footage of that run is not published yet. Until it is, treat this as the thesis I am about to have to prove."),
 ("A thing is code only if it must execute.",
  "Something is a function only when it has to touch the outside world — a mail server, an HTTP API, a database, a file. Everything else is an instruction you hand a language model. Most agent codebases are enormous because they wrote hundreds of functions for work a sentence would have done, and every one of those functions is now a thing that can break.",
  "The outreach engine I run is twelve connector verbs of real code — send, track, host, serve, pull — and everything else in it is an instruction: the copywriting, the qualification, the checking. I learned this by building the wrong thing first. I wrote a linter that checked strings for style violations, which is exactly the function a sentence replaces. The law is the scar."),
 ("Receipts, or it isn’t a pattern.",
  "A pattern is not something you noticed. It is something that appears more than once in code you actually shipped, at line numbers you can open. Without that it is a preference with good branding — and the field is drowning in preferences with good branding.",
  "My pattern catalog runs to fifty-seven entries and every one carries file-and-line ranges from real repositories. The most recent sweep produced twenty-two new entries, merged four into existing ones, and killed one outright for failing its own evidence test. The whole catalog is on this site — every entry, what it does, and the repository it runs in."),
 ("Nothing gets to accept itself.",
  "A system may never mint its own acceptance. The check has to come from outside the thing being checked, and it has to run the artifact rather than have an opinion about it. A model grading its own output is a mirror with a rubric taped to it.",
  "The test I use: a fresh agent with none of the build context runs the artifact against the outcome the maker declared in advance. It is falsifiable, it cannot be flattered, and it doubles as a transferability test — if it only works in the room where it was made, it does not work. I shipped that in February 2026. The same idea surfaced in the multi-agent discourse about five months later."),
 ("A claim you can’t lose is worthless.",
  "Every claim needs a branch where it dies, with a cause, on the record. Not a disclaimer at the bottom — an actual path in the structure where the thing turns out to be wrong and that outcome gets published like any other. If your framework has no way to fail, you did not build a framework, you built a story.",
  "I put my own headline claim in front of an adversarial panel and let it grade me: thirteen requirements, eight met, three partial, two open. The two open ones are the two that matter — nobody outside me has deployed it, and nobody outside me has witnessed it run. They are still open. They are restated further down this page instead of being quietly retired."),
 ("Publish the process, not the polish.",
  "The record of how a thing was actually made is the only artifact that is not a rendering of something else. Every write-up, every talk, every case study is a compression of that record, chosen to flatter. The record itself is the one document that cannot be spun, which is exactly why almost nobody publishes it.",
  "Fifty-plus field notes, published the night the work happened, dead ends left in. Some are polished and some are a working note with the failed approach still sitting in the middle of it. That is the trade for getting them at all — the tidy version arrives a year later, or never."),
 ("Every artifact is both a story and a manual.",
  "Written in the past tense, a piece of work is a biography: this happened, then this, and here is what changed. Written in the imperative, the identical structure is a manual: do this, then this, and this will change. They are the same object in two moods, which is why a thing built properly teaches by existing and does not need a separate course written about it afterwards.",
  "It is why this site is shaped the way it is. The notes are the build log and the curriculum at once, the patterns render as installable process and as lessons from one source, and the marketing is the work’s own exhaust rather than a second job bolted onto it. You are reading a worked example of the claim."),
]

def belief(i, t, claim, receipt):
    op = ' open' if i == 0 else ''
    return f'''              <details class="leak"{op}>
                <summary><span class="leak-name">{html.escape(t)}</span></summary>
                <div class="leak-tree">
                  <p><span>The claim</span>{html.escape(claim)}</p>
                  <p class="leak-dream"><span>The receipt</span>{html.escape(receipt)}</p>
                </div>
              </details>'''

beliefs = '\n'.join(belief(i, *b) for i, b in enumerate(BELIEFS))

# GitHub's own one-line description for each repo (gh api repos/sancovp/<r> .description)
REPOS = [
 ("skilltree", "A navigable, coordinate-addressed tree over flat skill directories — progressive disclosure for Claude Code skills.", "The code behind the paper."),
 ("cave-teams", "Connect AI agents like code. A provider-agnostic multi-agent orchestration library + Claude Code plugin — compose any agents (Claude, Codex, MiniMax) into teams with a tiny DSL, every topology, a programmable control flow, and a proven-team library.", None),
 ("dark-factory", "A repository that maintains and improves itself: AI agents play a game economy, develop skills, apply them to the repo, and ship through causally-gated CI/CD. Watch the PR list — merged PRs are proven improvements, closed PRs are the graveyard.", None),
 ("chaincompiler", "A compiler-compiler for cognition — a closed algebra over the skill dir (SKILL.md).", None),
 ("cave", "CAVE — Code Agent Virtualization Environment.", "The agent runtime: agents as HTTP services."),
 ("heaven-framework", "Foundation framework for HEAVEN ecosystem — AI agent infrastructure with unified context engineering.", None),
 ("carton-mcp", "CartOn MCP — Knowledge graph mapping for concept networks with Neo4j backend.", None),
 ("codenose", "Configurable code smell detection for LLMs — JSON-driven theming, rules, and custom hooks.", None),
 ("sdna", "Sanctuary DNA — Gnostic agent workflow DSL.", None),
 ("universal-chain-ontology", "Universal Chain Ontology (UCO): standalone, zero-dependency Link/Chain homoiconic composition primitives.", None),
]
def repo(name, desc, note):
    n = f'\n                <p class="repo-note">{html.escape(note)}</p>' if note else ''
    return f'''              <a class="repo" href="https://github.com/sancovp/{name}">
                <p class="repo-name">{name}</p>
                <p class="repo-desc">{html.escape(desc)}</p>{n}
                <p class="repo-go">github.com/sancovp/{name} &rarr;</p>
              </a>'''
repos = '\n'.join(repo(*r) for r in REPOS)

TOC = [("1", "→"), ("2", "A → B"), ("3", "A → 1 → 2 → 3 → B"), ("4", "⊆"), ("5", "+1"),
       ("6", "F(x) = x"), ("7", "⊢ | ⊬"), ("8", "⊨"), ("9", "X ≅ X"), ("10", "E(you) = you"),
       ("11", "+1 → 1"), ("12", "⌜X⌝"), ("", "Interlude"), ("13", "⊢ D∞ · 12 + 1"),
       ("", "Afterword: the status report"), ("", "The map")]
toc = '\n'.join(f'                <li><span class="toc-n">{n}</span><span class="toc-t">{html.escape(t)}</span></li>' for n, t in TOC)

V = '2026-09-26t'
page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Isaac Wostrel-Rubin — papers, a book, and the code</title>
<meta name="description" content="I build agent systems that run as worlds. My paper, a preview of my book, what I believe and the receipts, and the public repositories.">
<link rel="canonical" href="https://sancovp.github.io/aisaac/isaac-wostrel-rubin.html">
<meta property="og:type" content="profile">
<meta property="og:title" content="Isaac Wostrel-Rubin">
<meta property="og:description" content="I build agent systems that run as worlds. My paper, a preview of my book, what I believe and the receipts, and the public repositories.">
<meta property="og:image" content="https://sancovp.github.io/aisaac/assets/og/home.png">
<meta property="og:url" content="https://sancovp.github.io/aisaac/isaac-wostrel-rubin.html">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="assets/favicon.svg">
<link rel="stylesheet" href="style.css?v={V}">
</head>
<body data-depth="0">
<!-- ══════════════════════════════════════════════════════════════════════
     THE PERSONAL PAGE (*USER*'s ruling): the business page is TWI's; this one is Isaac's. Same
     Blueprint System, different job — it highlights his PAPER, his BOOK and his THEORIES first,
     then the code. Its content starts from `isaac.html` (the older personal page, left untouched),
     WITHOUT that page's price ladder: offers are frozen and live on the call.
     Unlike the business page it links OUT — to the paper, the repos, the notes — because those are
     the point. The one action it asks for is still Book a call.
     Built by a script (book passages pulled from the manuscript by line range, the booking dialog
     lifted whole from ai-transformation.html) — see 00-SITE-CANON § WHAT IS PUBLIC.
     ══════════════════════════════════════════════════════════════════════ -->

<div class="bp-parcels" aria-hidden="true">
  <div class="lane"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div>
  <div class="lane"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div>
</div>

<a class="skip-link" href="#paper">Skip to the paper</a>

<header class="nav nav-glass">
  <span class="logo">Isaac Wostrel-Rubin</span>
  <button class="nav-book" type="button" data-buy="call">Book a call</button>
</header>

<main id="main">

  <section class="bp-hero">
    <div class="wrap">
      <div class="bp-card bp-split me-hero">
        <div class="bp-cell">
          <p class="eyebrow"><span class="pill">Isaac Wostrel-Rubin</span></p>
          <h1>Nobody is keeping score. <span>So I grade myself in public.</span></h1>
          <p class="lede">I build agent systems that run as worlds &mdash; a business, a body, a codebase, each with its own departments, its own economy and its own record of what it actually did. No computer-science degree, no lab, no team. A hundred-plus public repositories and a lot of nights.</p>
          <div class="me-jump">
            <a class="cta-primary" href="#paper">The paper &darr;</a>
            <a class="me-link" href="#book">The book</a>
            <a class="me-link" href="#think">What I think</a>
            <a class="me-link" href="#code">The code</a>
          </div>
        </div>
        <div class="bp-cell me-portrait">
          <div class="portrait-frame">
            <img src="assets/isaac-portrait.jpg" alt="Isaac Wostrel-Rubin" width="960" height="1200">
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- THE PAPER — its own abstract's words, its own status line; linked, never re-hosted here -->
  <section class="bp-sec tinted tint-cyan" id="paper">
    <div class="wrap">
      <p class="eyebrow"><span class="pill">The paper</span></p>
      <h2>Flat versus Tree: Why Agent Skills Need a Graph</h2>
      <div class="bp-card bp-split paper-card">
        <div class="bp-cell">
          <p class="paper-abs">Practitioners building tool-using agents report a counterintuitive failure: connecting an agent to more tools can make its selection <em>worse</em>, not better.</p>
          <p class="paper-abs">skilltree makes that structure explicit: a coordinate-addressed tree (in general, a graph) the agent navigates instead of reassembling, demonstrated with tools that install in one command.</p>
          <div class="me-jump">
            <a class="cta-primary" href="ssri/papers/flat-vs-tree.html">Read the paper &rarr;</a>
            <a class="me-link" href="https://github.com/sancovp/skilltree">The code (MIT)</a>
          </div>
        </div>
        <div class="bp-cell paper-meta">
          <p class="get-k">Status</p>
          <p class="get-v">Working paper, June&ndash;July 2026. Not peer-reviewed.</p>
          <p class="get-k">Author</p>
          <p class="get-v">Isaac Wostrel-Rubin &middot; independent researcher &middot; ORCID 0009-0003-0219-0506</p>
          <p class="get-k">What it claims</p>
          <p class="get-v">A correction to the substrate &mdash; the structure a skill library already has, made explicit &mdash; not a new performance record. The agent-task benchmark is specified as future work.</p>
        </div>
      </div>
    </div>
  </section>

  <!-- THE BOOK — a PREVIEW: the title page, the contents, five passages of Chapter One. The book is
       in its final draft; nothing from the sealed part, no practice text, nothing from the raw
       autobiography corpus (the book's own gates, research/ssri/ship/arrow-book). -->
  <section class="bp-sec tinted tint-violet" id="book">
    <div class="wrap">
      <p class="eyebrow"><span class="pill">The book</span></p>
      <h2>The Sanctuary System &mdash; a preview</h2>
      <div class="bp-card bp-split book-card">
        <div class="bp-cell">
          <div class="book-cover">
            <p class="book-title">The Sanctuary System</p>
            <p class="book-sub">The Infinite Story</p>
            <img src="assets/sanc-mark-white.png" alt="The mark: three circles sharing a relationship to the centre" width="480" height="480">
            <p class="book-quote">&ldquo;I can&rsquo;t get out of my head&rdquo;</p>
            <p class="book-author">Isaac Wostrel-Rubin</p>
          </div>
        </div>
        <div class="bp-cell">
          <p class="get-k">Contents</p>
          <ol class="book-toc">
{toc}
          </ol>
          <p class="book-note">Thirteen chapters, each titled by one step of a single construction, and thirteen volumes that open each chapter all the way down. In its final draft.</p>
        </div>
      </div>

      <div class="bp-card book-read">
        <div class="bp-pad">
          <p class="get-k">From Chapter One: &ldquo;&rarr;&rdquo;</p>
          <blockquote class="book-excerpt">
{excerpts}
          </blockquote>
        </div>
      </div>
    </div>
  </section>

  <!-- WHAT I THINK — the seven beliefs from isaac.html, each opening to its receipt (the leak-tree
       component: the claim in ink, the receipt in green) -->
  <section class="bp-sec tinted tint-gold" id="think">
    <div class="wrap">
      <p class="eyebrow"><span class="pill">What I think</span></p>
      <h2>Seven things I believe, and what makes each one more than an opinion.</h2>
      <div class="bp-card">
        <div class="bp-pad">
          <p class="me-intro">These are the load-bearing ones &mdash; the beliefs the code is actually shaped by. Every one gets a receipt. Where the receipt is not public yet, it says so in the same breath, because a claim with a missing receipt is a debt, not a discovery.</p>
          <div class="leaks">
{beliefs}
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- THE CODE — every repo here answered 200 unauthenticated when this page was built; each
       description is the repository's own GitHub description -->
  <section class="bp-sec tinted tint-green" id="code">
    <div class="wrap">
      <p class="eyebrow"><span class="pill">The code</span></p>
      <h2>A hundred-plus public repositories. Ten to start with.</h2>
      <div class="repo-grid">
{repos}
      </div>
      <div class="me-more">
        <a class="me-link" href="https://github.com/sancovp">Every repository &rarr;</a>
        <a class="me-link" href="blog/">Fifty-plus field notes &rarr;</a>
        <a class="me-link" href="patterns.html">Fifty-seven patterns, with the file and line they run at &rarr;</a>
      </div>
    </div>
  </section>

  <section class="bp-sec bp-band">
    <div class="wrap">
      <p class="eyebrow"><span class="pill">Who I am</span></p>
      <div class="bp-card bp-split me-story">
        <div class="bp-cell">
          <h2>The outsider who kept building anyway.</h2>
          <p class="lede">I came at this sideways. I could always describe a system better than I could write one, so I spent years describing systems to a model until the descriptions started compiling &mdash; and that is genuinely the whole method. I talk to the machine in metaphors and advanced infrastructure falls out the other end. The oldest piece of this system is a prompt I wrote three years ago, before I could have implemented any of it in code.</p>
          <p class="lede">What came out is not a product with a roadmap. It is an engine that stands up a self-running world for a domain, plus about a hundred repositories of the parts, plus fifty-odd field notes written on the nights the work happened. I did it alone, in the gaps, without permission from anyone. That is the garage.</p>
        </div>
        <div class="bp-cell">
          <h2>The short version, told straight.</h2>
          <p class="lede">For a long time I had a hundred repositories and an audience of about five people. I used to think those two numbers contradicted each other. They don&rsquo;t. One is a fact about the work and the other is a fact about how I was presenting it, and I had spent years assuming that being honest was the same thing as being legible.</p>
          <p class="lede">What I actually want is boring to say and hard to do. I want the making of a thing and the record of making it to be one artifact, so the work teaches, the teaching brings people, and the people fund the next build &mdash; and none of it is a second job. I was never trying to ship a product. I was trying to build a place, and then it turned out the place could work for a living.</p>
        </div>
      </div>
    </div>
  </section>

  <section class="bp-sec tinted tint-red">
    <div class="wrap">
      <p class="eyebrow"><span class="pill">What I owe</span></p>
      <h2>The open rows, stated by me before anyone else gets to.</h2>
      <div class="bp-card">
        <div class="bp-pad me-owe">
          <p class="lede">Nobody outside me has deployed the core of this, and nobody outside me has witnessed it run. Those are the two ungraded requirements on my own audit. They are also the only two that cannot be closed by writing better &mdash; they need someone else&rsquo;s hands. Everything I say about the engine should be read against that fact, permanently, until it changes.</p>
          <p class="lede">The scoreboard isn&rsquo;t published. Cost per verified task, defects carried between rounds, what actually compounds and what only looks like it &mdash; the field has none of these, which is why nobody can tell who is winning. I am building that measurement and I do not have it yet.</p>
          <p class="lede">One receipt above is still an IOU and is marked as such: the hundred-cycle footage. It exists and it is not cut. It is named here so that if it never appears, this page is the evidence against me. None of this is modesty. A claim without a receipt is a debt, and a debt you announce is cheaper than one somebody finds.</p>
        </div>
      </div>
    </div>
  </section>

  <section class="bp-sec bp-ink bp-close">
    <div class="wrap">
      <h2>Want this running in your business?</h2>
      <div class="solo-cta">
        <button class="cta-primary" type="button" data-buy="call">Book a call &rarr;</button>
      </div>
      <p class="door-fine">Or read what the work looks like for a company: <a href="ai-transformation.html">AI Transformations With Isaac &rarr;</a></p>
    </div>
  </section>

</main>

<footer class="footer">
  <span>&copy; 2026 Isaac Wostrel-Rubin</span>
</footer>

{dialog}

<script src="vsl.js?v={V}"></script>
<script src="capture.js"></script>
</body>
</html>
'''
(SITE / 'isaac-wostrel-rubin.html').write_text(page)
print('wrote', len(page), 'bytes;', len(EXCERPTS), 'passages;', len(BELIEFS), 'beliefs;', len(REPOS), 'repos')
