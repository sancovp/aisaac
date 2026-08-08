"""THE BRAND TAG VOCABULARY — the one table both corpus generators read.

WHY THIS FILE EXISTS (Isaac's defect report, 2026-08-08, verbatim): "in the blog
search, we have by tags, but those tags are not by extremely important concept in
my system so it doesn't feel as branded as it could... shouldn't you be able to
search for like the 7 levels of agent engineering itself as a filter? ... this
kind of unbrandedness is rampant."

The state that produced that report: every one of the 51 blog cards carried
`data-tags=""`, so build_blog.py's discipline grouping collapsed to a single
"Everything else" heading. The corpus filed itself under nothing.

THE FIX, and its laws:

  1. THE SPINE IS THE SEVEN LEVELS. The ladder from lab/explainer.html ->
     blog/levels-overview.html (L1 Prompts, L2 Tools, L3 Context, L4 Harnesses,
     L5 Admissibility, L6 Concentration, L7 Emergence) is the flagship framework,
     so it is the first seven filters, IN ORDER, numbered. A visitor who reads
     nothing but the filter row has met the framework.
  2. DOOR REGISTER ONLY (RULE 00 law 2 — the lore firewall). Every tag is
     decodable by a stranger with no canon vocabulary. No myth names, no PAIAB /
     SANCTUM / CAVE / UNICORN / SOMA / GNOSYS. Those survive only inside post
     bodies, which are not being rewritten.
  3. NO ORPHANS. Every tag holds >= 2 posts corpus-wide; every post holds 1-3
     tags. Both are asserted by check() and both generators call it, so the
     vocabulary cannot rot silently.
  4. ONE CORPUS, ONE INDEX. blog/index.html carries the tag sections over BOTH
     blog posts and notes (64 items) — a tag filter that only reached half the
     writing would be the same defect in a new costume. notes/index.html carries
     the identical row, pointing into those sections.

The cross-cutting tags after the ladder are NOT invented here: they are the
regions the posts themselves fall into, named in the register of
~/repo/garage-lab/INDEX.md's door-safe branches (evidence discipline, the
code/instruction boundary, worlds & causal ladders, type-system moves).

The first tag in a post's tuple is its PRIMARY: it decides where the post sits in
the canonical reading order (and therefore the next-note chain). The rest are
cross-listings.
"""

# key, row label, the blurb a stranger reads to decode the tag
TAGS = [
    ("the-ladder", "The ladder itself",
     "the seven levels, and where the industry actually is"),
    ("l1-prompts", "Level 1 &middot; Prompts",
     "text in, text out &mdash; the floor most agencies sell as the ceiling"),
    ("l2-tools", "Level 2 &middot; Tools",
     "the agent can call things now; it still does not know what it is doing"),
    ("l3-context", "Level 3 &middot; Context",
     "what it knows when it acts, and why more of it is not better"),
    ("l4-harnesses", "Level 4 &middot; Harnesses",
     "runtime control over what the agent sees, runs and returns"),
    ("l5-admissibility", "Level 5 &middot; Admissibility",
     "outputs that have to compose from validated parts or not ship"),
    ("l6-concentration", "Level 6 &middot; Concentration",
     "holding one thread to the end without drifting off it"),
    ("l7-emergence", "Level 7 &middot; Emergence",
     "the system starts extending itself instead of being maintained"),
    ("skills", "Skills",
     "packaged capability an agent loads &mdash; and how it loads it"),
    ("composition", "Composition",
     "working pieces do not add up to a working whole by themselves"),
    ("drift-repair", "Drift &amp; repair",
     "everything that generates drifts; this is the returning"),
    ("vocabulary", "Naming &amp; vocabulary",
     "you cannot build what you cannot name, so forge the name first"),
    ("worlds-loops", "Worlds &amp; loops",
     "systems with laws and rounds, not scripts with steps"),
    ("the-operator", "The operator",
     "the human at the top of the stack: attention, judgment, not falling over"),
    ("the-market", "The market",
     "what is actually being sold, what it costs, what it is worth"),
]

LABEL = {k: lbl for k, lbl, _ in TAGS}
ORDER = [k for k, _, _ in TAGS]

# ── the corpus, tagged. slug (with extension for blog, .html for notes too) ──
# Assigned by reading every post's title, dek and section headings. Primary
# first. Keep this list ALPHABETICAL within each corpus so a new post is
# obviously missing rather than quietly untagged.

BLOG_TAGS = {
    "admissibility.html": ("l5-admissibility", "l3-context"),
    "allegorization-compiler.html": ("vocabulary", "l1-prompts"),
    "blanket.html": ("l4-harnesses", "composition"),
    "calibration.html": ("the-operator", "l6-concentration"),
    "cave-unicorn-how-it-works-deep-dive.html": ("worlds-loops", "l7-emergence"),
    "cave-unicorn-the-story.html": ("worlds-loops", "l7-emergence"),
    "composition.html": ("composition",),
    "crowning.html": ("l7-emergence", "the-operator"),
    "docmagic-stack.html": ("l5-admissibility", "drift-repair"),
    "externalization.html": ("the-operator", "l3-context"),
    "flat-vs-tree.html": ("skills", "l3-context"),
    "flow.html": ("the-operator", "l6-concentration"),
    "gas-httyd.html": ("l5-admissibility", "worlds-loops"),
    "halo.html": ("drift-repair", "the-operator"),
    "helming.html": ("the-operator", "composition"),
    "hiel.html": ("l6-concentration", "the-operator"),
    "holographic-work.html": ("composition", "l7-emergence"),
    "innout-configuration-mining.html": ("the-market", "composition"),
    "interaction-loop.html": ("composition", "drift-repair"),
    "l1-l2-prompts-tools.html": ("l1-prompts", "l2-tools", "the-ladder"),
    "l3-context.html": ("l3-context", "the-ladder", "skills"),
    "l4-fork.html": ("l4-harnesses", "the-ladder"),
    "l4-harnesses.html": ("l4-harnesses", "the-ladder"),
    "l5-admissibility.html": ("l5-admissibility", "the-ladder"),
    "l6-concentration.html": ("l6-concentration", "the-ladder"),
    "l7-emergence.html": ("l7-emergence", "the-ladder"),
    "levels-overview.html": ("the-ladder",),
    "meta-cognitive-awareness.html": ("the-operator", "l6-concentration"),
    "mission-control.html": ("drift-repair", "l6-concentration"),
    "ok-stable-signal.html": ("composition", "l5-admissibility"),
    "owl-to-agent.html": ("l5-admissibility", "vocabulary"),
    "preparing-for-stronger-models.html": ("l4-harnesses", "l7-emergence"),
    "progressive-disclosure-harness.html": ("l4-harnesses", "skills", "l2-tools"),
    "reach.html": ("the-operator", "vocabulary"),
    "sanctot-example.html": ("l5-admissibility", "vocabulary"),
    "seam-repair.html": ("drift-repair", "composition"),
    "seven-disciplines.html": ("the-ladder",),
    "shell.html": ("l2-tools", "worlds-loops", "l4-harnesses"),
    "single-biggest-trick-part-3.html": ("worlds-loops", "vocabulary"),
    "single-biggest-trick-reflection.html": ("worlds-loops", "vocabulary"),
    "single-biggest-trick.html": ("vocabulary", "l1-prompts", "worlds-loops"),
    "skilltree-how-it-works-deep-dive.html": ("skills", "l3-context"),
    "skilltree-the-story.html": ("skills", "l3-context"),
    "soseeh.html": ("vocabulary", "the-operator"),
    "sovereignty.html": ("l7-emergence", "worlds-loops"),
    "the-fair-game.html": ("the-market", "the-ladder"),
    "the-system-audit.html": ("the-market", "composition"),
    "the-thread-never-breaks-aida.html": ("drift-repair", "l3-context"),
    "the-thread-never-breaks-doc-mirror.html": ("drift-repair", "l3-context"),
    "thermal-dynamics.html": ("the-operator", "l6-concentration"),
    "towering.html": ("composition", "the-operator"),
}

NOTE_TAGS = {
    "build-in-verified-layers.html": ("composition", "l5-admissibility"),
    "compounds-or-rots.html": ("l7-emergence", "worlds-loops"),
    "drift-is-the-default.html": ("drift-repair", "l6-concentration"),
    "forge-your-own-vocabulary.html": ("vocabulary",),
    "right-is-not-fluent.html": ("l5-admissibility", "l3-context"),
    "the-agent-that-only-sees-the-next-turn.html": ("l4-harnesses", "l2-tools", "skills"),
    "the-altitude-ladder.html": ("the-ladder", "composition"),
    "the-compiler-that-resolves-the-ordinary.html": ("vocabulary", "l5-admissibility"),
    "the-four-slots.html": ("composition", "vocabulary"),
    "the-missing-slot-found-in-an-afternoon.html": ("vocabulary", "composition"),
    "the-repo-that-repaired-its-own-blind-spots.html": ("drift-repair", "l7-emergence"),
    "the-ten-minute-product-priced-like-magic.html": ("the-market", "l1-prompts"),
    "the-validator-that-refuses-to-be-wrong.html": ("l5-admissibility", "drift-repair"),
}


def tags_for(slug, corpus):
    """corpus is 'blog' or 'notes'. Unknown slug -> () (and check() will say so)."""
    return (BLOG_TAGS if corpus == "blog" else NOTE_TAGS).get(slug, ())


def corpus_counts():
    """tag key -> how many pieces carry it, across BOTH corpora. This is the
    number the row shows on either index, because there is one corpus."""
    counts = {k: 0 for k in ORDER}
    for table in (BLOG_TAGS, NOTE_TAGS):
        for t in table.values():
            for k in t:
                counts[k] += 1
    return counts


def check(blog_slugs, note_slugs):
    """Laws 3 and 4, mechanically. Returns a list of violation strings."""
    bad = []
    known = set(ORDER)
    counts = {k: 0 for k in ORDER}
    for slugs, table, name in ((blog_slugs, BLOG_TAGS, "blog"),
                               (note_slugs, NOTE_TAGS, "notes")):
        for s in slugs:
            t = table.get(s)
            if not t:
                bad.append(f"{name}/{s}: untagged")
                continue
            if not 1 <= len(t) <= 3:
                bad.append(f"{name}/{s}: {len(t)} tags (must be 1-3)")
            for k in t:
                if k not in known:
                    bad.append(f"{name}/{s}: unknown tag {k!r}")
                else:
                    counts[k] += 1
        for s in table:
            if s not in slugs:
                bad.append(f"{name}/{s}: tagged but not in the corpus")
    for k, n in counts.items():
        if n < 2:
            bad.append(f"tag {k!r}: {n} post(s) — orphan tags are banned")
    return bad


def tag_row(hrefs, counts, aria="Filter the corpus by concept"):
    """The filter row. JS-free: `.ladder`/`.rung` anchors, the same component
    Builder C shipped, because nav.js is the only script this site permits.
    `hrefs` maps tag key -> href; `counts` maps tag key -> post count."""
    rows = "\n".join(
        f'        <a class="rung" href="{hrefs[k]}">'
        f'<span class="rung-n">{counts.get(k, 0):02d}</span>'
        f'<span class="rung-t">{lbl}</span>'
        f'<span class="rung-d">{blurb}</span></a>'
        for k, lbl, blurb in TAGS if counts.get(k, 0))
    return (f'      <nav class="ladder measure-none" aria-label="{aria}">\n'
            f"{rows}\n      </nav>")


def pills(keys, href_for):
    """The per-post tag pills. They live INSIDE the .eyebrow row (mono, uppercase,
    already the label voice) so no new block vocabulary is introduced — style.css
    gives `.eyebrow a` the hairline pill chrome out of existing tokens."""
    if not keys:
        return ""
    return "".join(f'<a href="{href_for(k)}">{LABEL[k]}</a>'
                   for k in sorted(keys, key=ORDER.index))
