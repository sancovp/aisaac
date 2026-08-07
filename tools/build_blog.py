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

ROOT = Path(__file__).resolve().parent.parent
BLOG = ROOT / "blog"
UP = "../"

# §3.2 — files that leave the corpus.
#   doctor.html                  a dead sales page squatting in the writing dir
#   *-engineering.html           near-duplicate competing versions of a claim
#                                that already has a canonical slug
DROP = {"doctor.html", "admissibility-engineering.html",
        "concentration-engineering.html", "index.html"}

# §3.2 FILTER ROW RULE — the tags a stranger sees first must be ENGINEERING
# tags. PAIAB / SANCTUM / CAVE / UNICORN are demoted out of the row entirely
# (L3: zero canon vocabulary above the door). They survive only in data-tags.
DISCIPLINES = [
    ("tool-eng", "Tools", "what the agent can reach for"),
    ("context-eng", "Context", "what it knows when it acts"),
    ("harness-eng", "Harnesses", "the loop it runs inside"),
    ("admissibility-eng", "Admissibility", "how it knows it is wrong"),
    ("concentration-eng", "Concentration", "holding one thread to the end"),
    ("emergence-eng", "Emergence", "what shows up that nobody wrote"),
]
DISC_LABEL = {k: v for k, v, _ in DISCIPLINES}
OTHER = ("other", "Everything else", "the rest of the corpus")


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
        eyebrow = clean_text(m.group(1))
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
    """Point every in-body link at a URL that still exists (tools/linkmap.py)."""
    return re.sub(r'href=(["\'])(.*?)\1',
                  lambda m: f"href={m.group(1)}{rewrite_href(m.group(2), UP)}{m.group(1)}",
                  fragment)


def note_page(post, path_url, nxt=None):
    """THE NOTE-ARTICLE TEMPLATE (§1.2 TYPE 4) — the function that belongs in
    the cave-unicorn renderer skeleton."""
    desc = esc(truncate(clean_text(post["dek"]) or post["title"], 155))
    slug = post["slug"][:-5]
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
        f'    <p class="eyebrow">{post["eyebrow"]}</p>',
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
    return [m.groupdict() for m in CARD_RE.finditer(
        (BLOG / "index.html").read_text(encoding="utf-8"))]


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

    # ---- group the corpus by discipline. NO FILTER JS: §2.4 permits only
    # nav.js sitewide, so the filter row is static in-page anchors and the
    # grid is grouped under real headings. Crawlable, and works with JS off.
    # Grouping happens BEFORE the posts are written because the grouped order
    # IS the reading order: it drives the next-note chain, and computing it
    # first is what makes one pass converge instead of two.
    groups, seen = [], set()
    for key, label, blurb in DISCIPLINES:
        members = [c for c in cards if key in c["tags"].split() and c["href"] not in seen]
        seen.update(c["href"] for c in members)
        if members:
            groups.append((key, label, blurb, members))
    rest = [c for c in cards if c["href"] not in seen]
    if rest:
        groups.append((OTHER[0], OTHER[1], OTHER[2], rest))

    # the grouped order, flattened = the canonical reading order
    ordered = [c for _, _, _, members in groups for c in members]
    for i, c in enumerate(ordered):
        post = parse_post(BLOG / c["href"])
        if not post:
            print(f"  !! unparseable {c['href']}", file=sys.stderr)
            continue
        nxt = ({"href": ordered[i + 1]["href"], "title": clean_text(ordered[i + 1]["title"])}
               if i + 1 < len(ordered) else None)
        (BLOG / c["href"]).write_text(
            note_page(post, f"/blog/{c['href']}", nxt), encoding="utf-8")

    filt = "\n".join(
        f'        <a class="rung" href="#{k}"><span class="rung-n">{len(m):02d}</span>'
        f'<span class="rung-t">{lbl}</span><span class="rung-d">{blurb}</span></a>'
        for k, lbl, blurb, m in groups)

    sections = []
    for key, label, blurb, members in groups:
        # Attribute order MUST match CARD_RE — this markup is the script's own
        # input on the next run, and that round-trip is what keeps the curated
        # titles/descriptions/tags from being lost.
        cardhtml = "\n".join(
            f'        <a href="{c["href"]}" class="card" data-tags="{c["tags"]}"'
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
        f'      <p class="lede">{len(cards)} posts, published as they were written and never '
        "cleaned up afterwards &mdash; including the ones that record a mistake.</p>",
        '      <a class="cta-primary" href="#notes">Read them &rarr;</a>',
        "    </div>",
        "  </section>",
        "",
        '  <section id="notes" style="padding-top:0">',
        '    <div class="wrap">',
        '      <nav class="ladder" aria-label="Jump to a discipline" style="max-width:none">',
        filt,
        "      </nav>",
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
    print(f"posts: {len(cards)}   groups: {[g[0] for g in groups]}   orphans listed: {orphans}")
    return cards


if __name__ == "__main__":
    build()
