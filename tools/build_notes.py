#!/usr/bin/env python3
"""C3 — conform notes/ to Builder A's shipped skeleton, and build notes/index.html.

The 13 note bodies were rendered from free-layer/*.md by another pass and the
PROSE IS GOOD — this script does not rewrite content. It fixes three classes of
structural defect that make the pages render wrong against A's `style.css`:

  1. ROOT-ABSOLUTE PATHS (href="/style.css", "/watch.html", "/blog/…").
     The deploy is a GitHub Pages PROJECT SUBPATH, so these resolve above the
     project and 404 — every one of these pages was loading with NO stylesheet.
     A's _templates/_head.html sets the opposite law: relative in-page, absolute
     only for canonical/og.
  2. CLASSES THAT DO NOT EXIST IN style.css — .receipt-kind/.receipt-claim
     (A ships .receipt-k + h3 + p + .receipt-go), .rung-num/.rung-name/.rung-note
     (A ships .rung-n/.rung-t/.rung-d), .note-grid/.note-card/.read-link/
     .note-filters/.filter-btn (A ships .cards/.card/.receipt-go/.ladder/.rung).
  3. MISSING SKELETON — no skip-link, no <main id="main">, no .wrap containers,
     footer without .tagline, no nav.js include.

Idempotent: re-running parses its own output and produces byte-identical files.
Run:  python3 tools/build_notes.py
"""
import html
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from skeleton import (head, nav, ladder, receipts, receipts_compact,  # noqa: E402
                      final_cta, footer)

ROOT = Path(__file__).resolve().parent.parent
NOTES = ROOT / "notes"
UP = "../"
MARK = "<!-- RECONFORMED:C -->"

# The two families, from the free-layer/ source tree they were rendered out of.
FRAMEWORKS = ["compounds-or-rots", "the-altitude-ladder", "the-four-slots",
              "build-in-verified-layers", "drift-is-the-default",
              "right-is-not-fluent", "forge-your-own-vocabulary"]
CASE_STUDIES = ["the-ten-minute-product-priced-like-magic",
                "the-repo-that-repaired-its-own-blind-spots",
                "the-validator-that-refuses-to-be-wrong",
                "the-missing-slot-found-in-an-afternoon",
                "the-compiler-that-resolves-the-ordinary",
                "the-agent-that-only-sees-the-next-turn"]
ORDER = FRAMEWORKS + CASE_STUDIES


def clean(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", s))).strip()


def truncate(s, n):
    return s if len(s) <= n else s[:n].rsplit(" ", 1)[0].rstrip(" ,;:.—-") + "…"


def relativise(fragment):
    """Root-absolute -> relative-from-notes/. The core defect fix."""
    def sub(m):
        q, href = m.group(1), m.group(2)
        if not href.startswith("/"):
            return m.group(0)
        p = href[1:]
        if p == "":                       # "/"        -> ../index.html
            p = "index.html"
        if p.startswith("notes/"):        # sibling note, stays in this dir
            p = p[len("notes/"):] or "index.html"
            return f"href={q}{p}{q}"
        return f"href={q}{UP}{p}{q}"
    return re.sub(r'href=(["\'])(.*?)\1', sub, fragment)


def parse(path):
    raw = path.read_text(encoding="utf-8")
    m = re.search(r'<article class="note">(.*?)</article>', raw, re.S)
    if not m:
        return None
    art = m.group(1)
    eyebrow, title, dek = "", "", ""
    mm = re.search(r'<p class="eyebrow">(.*?)</p>', art, re.S)
    if mm:
        eyebrow = clean(mm.group(1))
        art = art[:mm.start()] + art[mm.end():]
    mm = re.search(r"<h1[^>]*>(.*?)</h1>", art, re.S)
    if not mm:
        return None
    title = mm.group(1).strip()
    art = art[:mm.start()] + art[mm.end():]
    mm = re.search(r'<p class="dek">(.*?)</p>', art, re.S)
    if mm:
        dek = mm.group(1).strip()
        art = art[:mm.start()] + art[mm.end():]

    # receipts: accept the old (.receipt-kind/.receipt-claim) and new shapes
    rec = []
    for r in re.finditer(r'<a class="receipt" href="([^"]+)">(.*?)</a>', raw, re.S):
        href, inner = r.group(1), r.group(2)
        k = re.search(r'class="receipt-(?:kind|k)"[^>]*>(.*?)<', inner, re.S)
        c = re.search(r'class="receipt-claim"[^>]*>(.*?)<', inner, re.S)
        h3 = re.search(r"<h3>(.*?)</h3>", inner, re.S)
        p = re.search(r"<p>(.*?)</p>", inner, re.S)
        rec.append((clean(k.group(1)) if k else "Receipt",
                    clean((h3 or c).group(1)) if (h3 or c) else "",
                    clean(p.group(1)) if p else "",
                    "Open"))
    return {"slug": path.stem, "eyebrow": eyebrow or "Field note",
            "title_html": title, "title": clean(title), "dek": dek,
            "body": relativise(art).strip(), "receipts": rec}


def render(note, nxt):
    desc = html.escape(truncate(clean(note["dek"]) or note["title"], 155), quote=True)
    dek = f'\n    <p class="dek">{note["dek"]}</p>' if note["dek"] else ""
    rec = [(k, h3, p or "Open the artifact and check the claim yourself.", go, href)
           for (k, h3, p, go), href in zip(note["receipts"], _hrefs(note))] \
        if note["receipts"] else []
    if not rec:
        rec = [("Open source", "The engine this came out of",
                "Public repos, MIT, full commit history.", "github.com/sancovp",
                "https://github.com/sancovp")]
    nxt_html = ""
    if nxt:
        nxt_html = (f'\n  <a class="note-next" href="{nxt["slug"]}.html">Next note: '
                    f'<b>{html.escape(nxt["title"])} &rarr;</b></a>')
    return _mark("\n".join([
        head(html.escape(note["title"], quote=True), desc,
             f'/notes/{note["slug"]}.html', note["slug"], up=UP),
        nav(up=UP, current="notes/"),
        "",
        '  <article class="note">',
        f'    <p class="eyebrow">{note["eyebrow"]}</p>',
        f'    <h1>{note["title_html"]}</h1>{dek}',
        "",
        note["body"],
        "  </article>",
        "",
        receipts_compact(rec) + nxt_html,
        "",
        final_cta(up=UP),
        footer(up=UP),
    ]))


def _mark(page):
    """Stamp the reconform marker INSIDE <head>. A comment before <!doctype>
    is invalid and puts legacy engines into quirks mode."""
    return page.replace("<head>\n", "<head>\n" + MARK + "\n", 1)


def _hrefs(note):
    """The hrefs belonging to the parsed receipts, already relativised."""
    return note.setdefault("_rhrefs", [])


def build():
    parsed = {}
    for path in sorted(NOTES.glob("*.html")):
        if path.stem == "index":
            continue
        n = parse(path)
        if not n:
            print(f"  !! unparseable {path.name}", file=sys.stderr)
            continue
        raw = path.read_text(encoding="utf-8")
        n["_rhrefs"] = [relativise(f'href="{h}"').split('"')[1]
                        for h in re.findall(r'<a class="receipt" href="([^"]+)"', raw)]
        parsed[path.stem] = n

    order = [s for s in ORDER if s in parsed] + \
            [s for s in sorted(parsed) if s not in ORDER]
    for i, slug in enumerate(order):
        nxt = ({"slug": order[i + 1], "title": parsed[order[i + 1]]["title"]}
               if i + 1 < len(order) else None)
        (NOTES / f"{slug}.html").write_text(render(parsed[slug], nxt), encoding="utf-8")

    def cards(slugs):
        return "\n".join(
            f'        <a class="card" href="{s}.html"><h3>{html.escape(parsed[s]["title"])}</h3>'
            f'<p>{truncate(clean(parsed[s]["dek"]), 190)}</p>'
            f'<span class="receipt-go">Read &rarr;</span></a>'
            for s in slugs if s in parsed)

    fw, cs = [s for s in FRAMEWORKS if s in parsed], [s for s in CASE_STUDIES if s in parsed]
    index = _mark("\n".join([
        head("The patterns, written plainly",
             "Short pieces on how these systems actually work, plus the long field-note "
             "feed behind them. Free, no email, no strings.", "/notes/", "notes", up=UP),
        nav(up=UP, current="notes/"),
        "",
        '  <section class="claim">',
        '    <div class="wrap">',
        '      <p class="eyebrow">Free &mdash; no email, no strings</p>',
        "      <h1>The patterns, written plainly.</h1>",
        f'      <p class="lede">{len(fw) + len(cs)} short pieces on how these systems '
        "actually work, and the long field-note feed behind them. Take what you need.</p>",
        '      <a class="cta-primary" href="#patterns">Start reading &rarr;</a>',
        "    </div>",
        "  </section>",
        "",
        '  <section id="patterns" class="flush-top">',
        '    <div class="wrap">',
        '      <nav class="ladder measure-none" aria-label="Jump to a section">',
        f'        <a class="rung" href="#frameworks"><span class="rung-n">{len(fw):02d}</span>'
        '<span class="rung-t">Frameworks</span><span class="rung-d">ways to think about the '
        "problem &mdash; the shape, not the build</span></a>",
        f'        <a class="rung" href="#case-studies"><span class="rung-n">{len(cs):02d}</span>'
        '<span class="rung-t">Case studies</span><span class="rung-d">one real thing that '
        "happened, and what it cost</span></a>",
        '        <a class="rung" href="../blog/"><span class="rung-n">51</span>'
        '<span class="rung-t">Field notes</span><span class="rung-d">the long feed, published '
        "as the work happened</span></a>",
        "      </nav>",
        "",
        '      <h2 id="frameworks">Frameworks</h2>',
        '      <p class="receipts-lede">A way to think about the problem. These hand you the '
        "shape, not the build.</p>",
        f'      <div class="cards">\n{cards(fw)}\n      </div>',
        "",
        '      <h2 id="case-studies">Case studies</h2>',
        '      <p class="receipts-lede">One real thing that happened, what it cost, and what '
        "was actually learned.</p>",
        f'      <div class="cards">\n{cards(cs)}\n      </div>',
        "",
        '      <h2 id="field-notes">Field notes</h2>',
        '      <p class="receipts-lede">The long feed &mdash; 51 notes published as the work '
        "happened, grouped by discipline.</p>",
        '      <div class="cards">',
        '        <a class="card" href="../blog/"><h3>The whole feed</h3><p>Every field note on '
        "agent engineering, grouped by discipline &mdash; tools, context, harnesses, "
        'admissibility, concentration, emergence.</p><span class="receipt-go">Browse 51 notes '
        "&rarr;</span></a>",
        '        <a class="card" href="../blog/flat-vs-tree.html"><h3>Flat vs Tree</h3><p>A bug '
        "hiding in every AI &ldquo;skills&rdquo; folder &mdash; and the paper about it. They "
        "named it &ldquo;progressive disclosure,&rdquo; then shipped it unable to disclose.</p>"
        '<span class="receipt-go">Read &rarr;</span></a>',
        # The last hop of the reader's descent. isaac.html is deliberately NOT
        # in the nav (the nav is single-source and a seventh item forces a
        # re-paste across every page), so the maker is reached from the door
        # and from the end of the reading chain. This is that end.
        '        <a class="card" href="../isaac.html"><h3>Who writes these</h3><p>Seven things '
        "he believes, each with the receipt attached &mdash; and, at the bottom, the debts he "
        "names before anyone else gets to.</p>"
        '<span class="receipt-go">Meet the maker &rarr;</span></a>',
        "      </div>",
        "    </div>",
        "  </section>",
        "",
        receipts(up=UP),
        ladder(up=UP, heading="Reading is rung zero. Here is the rest of the ladder."),
        footer(up=UP),
    ]))
    (NOTES / "index.html").write_text(index, encoding="utf-8")
    print(f"notes conformed: {len(order)}  (frameworks {len(fw)}, case studies {len(cs)}) + index")


if __name__ == "__main__":
    build()
