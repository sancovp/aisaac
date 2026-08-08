#!/usr/bin/env python3
"""C1 + C2 — put every blog post on the NOTE-ARTICLE template and rebuild
blog/index.html on NOTE-INDEX. Idempotent: safe to re-run after every render.

WHY THIS SCRIPT EXISTS (spec §5, C1). The posts are machine-fed nightly by the
cave-unicorn renderer, which emits a FRAGMENT — no doctype, no <title>, no
viewport, no og/twitter (50 of 55 files) — so every post renders in quirks mode
with a raw URL in the tab and shares as a bare blue link. The spec's fix is
"patch the renderer, not the posts". The cave-unicorn repo is NOT reachable
from this container (checked: /home/ceo/repo has no clone), so this script is
that same patch expressed as a POST-RENDER step the pipeline can call. When the
renderer repo is reachable, port `note_page()` into its skeleton verbatim and
delete this file.

Run:  python3 tools/build_blog.py
"""
import html
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from skeleton import (head, nav, ladder, receipts, receipts_compact,  # noqa: E402
                      final_cta, footer)
from linkmap import rewrite_href  # noqa: E402
import tags as TAGS  # noqa: E402  — the brand tag vocabulary + the assignments

ROOT = Path(__file__).resolve().parent.parent
BLOG = ROOT / "blog"
NOTES = ROOT / "notes"
UP = "../"

# §3.2 — files that leave the corpus.
#   doctor.html                  a dead sales page squatting in the writing dir
#   *-engineering.html           near-duplicate competing versions of a claim
#                                that already has a canonical slug
DROP = {"doctor.html", "admissibility-engineering.html",
        "concentration-engineering.html", "index.html"}

# §3.2 FILTER ROW RULE — the tags a stranger sees first must be ENGINEERING
# tags. PAIAB / SANCTUM / CAVE / UNICORN are demoted out of the row entirely
# (L3: zero canon vocabulary above the door).
#
# The row itself now comes from tools/tags.py: the seven levels of agent
# engineering in order, then the cross-cutting concepts. The six generic
# discipline keys that used to live here matched NOTHING — all 51 cards shipped
# `data-tags=""` and the whole corpus collapsed under one "Everything else"
# heading. That is the defect tags.py was written to close; the vocabulary and
# the per-post assignments both live there so the two generators cannot drift.


def clean_text(s):
    s = re.sub(r"<[^>]+>", "", s)
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


def truncate(s, n):
    if len(s) <= n:
        return s
    return s[:n].rsplit(" ", 1)[0].rstrip(" ,;:.—-") + "…"


def esc(s):
    return html.escape(s, quote=True)


def extract_article(raw):
    """Pull the article innards out of a post in EITHER shipped shape: the
    fragment shape (#isaac-site > article) or the 5 full-page posts."""
    m = re.search(r"<article[^>]*>(.*?)</article>", raw, re.S)
    if m:
        return m.group(1)
    m = re.search(r"<body[^>]*>(.*?)</body>", raw, re.S)
    if not m:
        return None
    body = m.group(1)
    body = re.sub(r'<div class="header">.*?</div>\s*</div>', "", body, flags=re.S)
    body = re.sub(r'<div class="footer">.*?</div>', "", body, flags=re.S)
    body = re.sub(r"<script\b.*?</script>", "", body, flags=re.S)
    return body


def parse_post(path):
    """Read a post in either the legacy vocabulary (.post-tag/.post-subtitle)
    or the one this script emits (.eyebrow/.dek). Matching BOTH is what makes
    a re-run lossless instead of silently dropping the dek."""
    art = extract_article(path.read_text(encoding="utf-8"))
    if art is None:
        return None
    eyebrow = ""
    m = re.search(r'<(?:div|p|span)[^>]*class="[^"]*\b(?:post-tag|tag|eyebrow)\b[^"]*"'
                  r"[^>]*>(.*?)</(?:div|p|span)>", art, re.S)
    if m:
        # drop the tag pills before reading the eyebrow back — they are
        # REGENERATED from tools/tags.py every run, and parsing them as part of
        # the eyebrow text is how a re-run would silently concatenate them
        eyebrow = clean_text(re.sub(r"<a\b.*?</a>", "", m.group(1), flags=re.S))
        art = art[:m.start()] + art[m.end():]
    m = re.search(r"<h1[^>]*>(.*?)</h1>", art, re.S)
    if not m:
        return None
    title_html = m.group(1).strip()
    art = art[:m.start()] + art[m.end():]
    dek = ""
    m = re.search(r'<p[^>]*class="[^"]*\b(?:post-subtitle|sub|dek|lede)\b[^"]*"[^>]*>(.*?)</p>',
                  art, re.S)
    if m:
        dek = m.group(1).strip()
        art = art[:m.start()] + art[m.end():]
    return {"slug": path.name, "eyebrow": eyebrow or "Field note",
            "title": clean_text(title_html), "title_html": title_html,
            "dek": dek, "body": art.strip()}


def fix_links(fragment):
    """Point every in-body link at a URL that still exists (tools/linkmap.py).

    `index.html` is exempt. Inside a post body that href means THIS DIRECTORY's
    index — the "All posts" link at the foot of ~16 salvaged posts — but
    linkmap reads a bare `index.html` as the site root and rewrote it to
    `../index.html`. That sent readers back to the door, which the ratchet law
    of navigation forbids (RULE 00 decision log, 2026-08-07: index.html is the
    ENTRYPOINT ONLY, one-way, no nav routes back to it), and it made the build
    non-idempotent besides."""
    return re.sub(
        r'href=(["\'])(.*?)\1',
        lambda m: m.group(0) if m.group(2) == "index.html" else
        f"href={m.group(1)}{rewrite_href(m.group(2), UP)}{m.group(1)}",
        fragment)


def note_page(post, path_url, nxt=None):
    """THE NOTE-ARTICLE TEMPLATE (§1.2 TYPE 4) — the function that belongs in
    the cave-unicorn renderer skeleton."""
    desc = esc(truncate(clean_text(post["dek"]) or post["title"], 155))
    slug = post["slug"][:-5]
    # the post declares its framework concepts and each pill jumps to that
    # concept's section on the corpus index (tools/tags.py, law 4)
    pills = TAGS.pills(TAGS.tags_for(post["slug"], "blog"),
                       lambda k: f"index.html#{k}")
    dek = f'\n    <p class="dek">{post["dek"]}</p>' if post["dek"] else ""
    nxt_html = ""
    if nxt:
        nxt_html = (f'\n  <p class="note-next">Next note: '
                    f'<a href="{nxt["href"]}"><b>{esc(nxt["title"])} &rarr;</b></a></p>')
    return "\n".join([
        head(esc(post["title"]), desc, path_url, slug, up=UP),
        nav(up=UP, current="notes/"),
        "",
        '  <article class="note">',
        f'    <p class="eyebrow">{post["eyebrow"]}{pills}</p>',
        f'    <h1>{post["title_html"]}</h1>{dek}',
        "",
        fix_links(post["body"]),
        "  </article>",
        "",
        receipts_compact([
            ("Open source", "The engine this came out of",
             "Public repos, MIT, full commit history — this note describes code you can read.",
             "github.com/sancovp", "https://github.com/sancovp"),
            ("Running now", "See it actually run",
             "The engine drawing its own explainer, live in the browser.",
             "Watch a world run", f"{UP}watch.html"),
        ]) + nxt_html,
        "",
        final_cta(up=UP),
        footer(up=UP),
    ])


# ---------------------------------------------------------------- the index --

CARD_RE = re.compile(
    r'<a href="(?P<href>[^"]+)" class="(?:blog-card|card)" data-tags="(?P<tags>[^"]*)"'
    r' data-search="(?P<search>[^"]*)"><h3>(?P<title>.*?)</h3><p>(?P<desc>.*?)</p>', re.S)


def read_index_order():
    """The curated title/description for each post, in its current order.

    DEDUPED BY HREF, and that is load-bearing: the index is no longer a
    partition — a post is listed under every concept it carries — so the same
    card is legitimately in the markup two or three times. Reading them all
    back is how one run turned 51 posts into 233 and the next into 495."""
    seen, out = set(), []
    for m in CARD_RE.finditer((BLOG / "index.html").read_text(encoding="utf-8")):
        c = m.groupdict()
        if c["href"] in seen:
            continue
        seen.add(c["href"])
        out.append(c)
    return out


def note_cards():
    """The 13 short pieces, as cards for the corpus index.

    Law 4 of tools/tags.py: ONE corpus, ONE tag index. A filter that reached the
    51 field notes but not the 13 notes/ pieces would be the same unbrandedness
    in a new costume — and every note page's pills link into these sections, so
    the note has to be listed in them. notes/index.html keeps its own
    Frameworks / Case-studies curation; this is the concept view over the same
    files, not a second home for them."""
    from build_notes import ORDER as NOTE_ORDER, parse as parse_note
    out = []
    for slug in NOTE_ORDER:
        path = NOTES / f"{slug}.html"
        if not path.exists():
            continue
        n = parse_note(path)
        if not n:
            print(f"  !! unparseable note {slug}", file=sys.stderr)
            continue
        out.append({"href": f"../notes/{slug}.html", "slug": f"{slug}.html",
                    "corpus": "notes", "title": esc(n["title"]),
                    "search": esc(n["title"].lower()),
                    "desc": esc(truncate(clean_text(n["dek"]), 180))})
    return out


def build():
    cards = read_index_order()
    listed = {c["href"] for c in cards}
    on_disk = {p.name for p in BLOG.glob("*.html")} - DROP

    # §3.2 "list-or-delete the two remaining orphans" -> LIST them, so the
    # index is provably the complete corpus rather than a hand-kept subset.
    orphans = sorted(on_disk - listed)
    for slug in orphans:
        post = parse_post(BLOG / slug)
        if not post:
            print(f"  !! unparseable orphan {slug}", file=sys.stderr)
            continue
        cards.append({"href": slug, "tags": "", "search": post["title"].lower(),
                      "title": esc(post["title"]),
                      "desc": esc(truncate(clean_text(post["dek"]), 180))})
    cards = [c for c in cards if c["href"] in on_disk]

    # ---- THE TAG INDEX. NO FILTER JS: §2.4 permits only nav.js sitewide, so
    # the filter row is static in-page anchors and the grid is grouped under
    # real headings. Crawlable, and works with JS off.
    #
    # Unlike the old discipline grouping this is NOT a partition: a post is
    # listed under EVERY tag it carries. A filter that only showed you the
    # posts whose FIRST concept matched would be lying about the corpus — ask
    # for Level 5 and you must get all eleven, not the four that happen to be
    # filed there first.
    notes = note_cards()
    for c in cards:
        c["corpus"], c["slug"] = "blog", c["href"]
        c["tags"] = " ".join(TAGS.tags_for(c["href"], "blog"))

    # The base order comes from tools/tags.py, NOT from the markup. Sorting on
    # the markup's order was a feedback loop: cross-listing changed where each
    # card FIRST appears, that changed the order read back, and the reading
    # chain oscillated between two states forever. The index may be re-derived
    # from the tag table; it may not be derived from itself.
    base = {slug: i for i, slug in enumerate(TAGS.BLOG_TAGS)}
    cards.sort(key=lambda c: base.get(c["slug"], len(base)))

    violations = TAGS.check({c["slug"] for c in cards}, {n["slug"] for n in notes})
    if violations:
        for v in violations:
            print(f"  !! TAG {v}", file=sys.stderr)
        sys.exit(1)

    # Reading order (the next-note chain) stays a partition and stays inside
    # blog/: each post sits with its PRIMARY concept, concepts in ladder order.
    # It is computed BEFORE the posts are written because that order IS the
    # chain — computing it first is what makes one pass converge instead of two.
    ordered = [c for key in TAGS.ORDER for c in cards
               if TAGS.tags_for(c["slug"], "blog")[:1] == (key,)]

    corpus_order = {c["href"]: i for i, c in enumerate(ordered + notes)}
    groups = []
    for key, label, blurb in TAGS.TAGS:
        members = sorted(
            (c for c in cards + notes if key in TAGS.tags_for(c["slug"], c["corpus"])),
            key=lambda c: corpus_order[c["href"]])
        if members:
            groups.append((key, label, blurb, members))
    for i, c in enumerate(ordered):
        post = parse_post(BLOG / c["href"])
        if not post:
            print(f"  !! unparseable {c['href']}", file=sys.stderr)
            continue
        nxt = ({"href": ordered[i + 1]["href"], "title": clean_text(ordered[i + 1]["title"])}
               if i + 1 < len(ordered) else None)
        (BLOG / c["href"]).write_text(
            note_page(post, f"/blog/{c['href']}", nxt), encoding="utf-8")

    filt = TAGS.tag_row({k: f"#{k}" for k in TAGS.ORDER},
                        {k: len(m) for k, _, _, m in groups})

    sections = []
    for key, label, blurb, members in groups:
        # Attribute order MUST match CARD_RE — this markup is the script's own
        # input on the next run, and that round-trip is what keeps the curated
        # titles and descriptions from being lost. (data-tags is now WRITTEN
        # from tools/tags.py rather than read back, so the markup can no longer
        # be the place a tag silently disappears.)
        cardhtml = "\n".join(
            f'        <a href="{c["href"]}" class="card"'
            f' data-tags="{" ".join(TAGS.tags_for(c["slug"], c["corpus"]))}"'
            f' data-search="{c["search"]}"><h3>{c["title"]}</h3><p>{c["desc"]}</p>'
            f'<span class="receipt-go">Read &rarr;</span></a>' for c in members)
        sections.append(
            f'      <h2 id="{key}">{label}</h2>\n'
            f'      <p class="receipts-lede">{blurb}</p>\n'
            f'      <div class="cards">\n{cardhtml}\n      </div>')

    index = "\n".join([
        head("The field notes",
             "Engineering notes published as they were written — agent architecture, "
             "context, harnesses, admissibility, and the ones that record a mistake.",
             "/blog/", "blog", up=UP),
        nav(up=UP, current="notes/"),
        "",
        '  <section class="claim">',
        '    <div class="wrap">',
        '      <p class="eyebrow">Open notes</p>',
        "      <h1>The notes written while the thing was being built.</h1>",
        f'      <p class="lede">{len(cards) + len(notes)} posts, published as they were '
        "written and never cleaned up afterwards &mdash; including the ones that record a "
        "mistake. Filed under the seven levels of agent engineering and the concepts that "
        "cut across them.</p>",
        '      <a class="cta-primary" href="#notes">Read them &rarr;</a>',
        "    </div>",
        "  </section>",
        "",
        '  <section id="notes" class="flush-top">',
        '    <div class="wrap">',
        '      <p class="eyebrow">Filter by concept</p>',
        filt,
        "",
        "\n\n".join(sections),
        "    </div>",
        "  </section>",
        "",
        receipts(up=UP),
        ladder(up=UP, heading="Reading is rung zero. Here is the rest of the ladder."),
        footer(up=UP),
    ])
    (BLOG / "index.html").write_text(index, encoding="utf-8")
    print(f"corpus: {len(cards)} blog + {len(notes)} notes   orphans listed: {orphans}")
    for k, lbl, _, m in groups:
        print(f"  {len(m):3d}  {k:<18} {clean_text(lbl)}")
    return cards


if __name__ == "__main__":
    build()
