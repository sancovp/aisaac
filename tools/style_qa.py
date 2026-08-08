#!/usr/bin/env python3
"""style_qa.py — the mechanical quality gates of RULE 02 (Mercury Glass).

Run before any style commit:

    python3 tools/style_qa.py                # canon pages, summary
    python3 tools/style_qa.py --all          # canon + legacy + stubs
    python3 tools/style_qa.py -v             # every violation, with locations
    python3 tools/style_qa.py --bucket legacy -v

Exit status is 1 if any CANON page fails a gate, 0 otherwise. Legacy pages are
counted and reported but never fail the build: they predate the rebuild, and
silently churning them is how a style pass turns into a content pass.

THE GATES (RULE 02, "Mechanical quality gates"), one function each:

  G1 contrast     WCAG AA, computed from the ACTUAL token values in style.css
                  — not from a hand-kept table that drifts the first time a
                  token moves. Alpha tokens are composited over --void first.
  G2 inline       zero style="" attributes (the block vocabulary is closed;
                  style.css carries .mt-s/.mt-l/.flush-top for layout nudges)
  G3 pagestyle    zero page <style> over 20 lines
  G4 h1           exactly one <h1> per page
  G5 imgdim       every <img> carries width and height (no layout shift)
  G6 ogimage      an og:image per page-type
  G7 fontfamily   no font-family declaration outside style.css
  G8 hex          no hex colour outside style.css

Gates 7 and 8 are the ones that actually keep the site one designed object:
the moment a page can name its own colour or its own typeface, the stylesheet
stops being the single source of truth and "high-end" becomes unenforceable.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from collections import defaultdict
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STYLESHEET = os.path.join(ROOT, "style.css")

# ── Scope ────────────────────────────────────────────────────────────────────
# CANON  — the rebuilt site. These must pass; a failure here is a ship blocker.
# LEGACY — pre-rebuild pages still served. Reported, never fatal.
# STUB   — meta-refresh redirects. Only the gates that can apply to them do.
# EXEMPT — the deliberately-foreign artifact islands and the separate
#          sub-brands, named as exempt by style.css's own header. Reskinning
#          an artifact destroys the proof it exists to carry, so the artifact
#          is allowed its own look and is not measured against this rule.

CANON_FILES = {
    "index.html", "watch.html", "system.html", "isaac.html",
    "learn.html", "build.html", "run.html", "404.html",
}
# FROZEN — pricing.html is restored verbatim from main by Isaac's order of
# 2026-08-07 ("STOP CHANGING MY OFFERS"). RULE 00 law 1 makes it his file
# alone, so it is measured and REPORTED but never edited to satisfy a gate.
# Its violations are evidence for a FOR ISAAC block, not a to-do list.
FROZEN_FILES = {"pricing.html"}
# UTILITY — TYPE 5 (_templates/util.html) ships no og tags by design: a
# noindex 404 has no page-type in the share graph, so G6 does not apply.
UTILITY_FILES = {"404.html"}
CANON_DIRS = ("blog/", "notes/", "inside/")
EXEMPT_DIRS = ("lab/", "ssri/", "builds/", ".claude/", "_build/", "_templates/",
               "dharma-concierge/", "healthworld/", "docs/", "books/",
               "free-layer/", "content-engine/", "b2b-bootcamp/",
               "ai-operating-system-positioning/", "video-storyboards/",
               "scripts/", ".git/")
EXEMPT_FILES = {"cinematic-plumbing.html"}


def bucket_of(rel: str, text: str) -> str:
    if rel in EXEMPT_FILES or rel.startswith(EXEMPT_DIRS):
        return "exempt"
    if re.search(r'http-equiv=["\']refresh', text, re.I):
        return "stub"
    if rel in FROZEN_FILES:
        return "frozen"
    if rel in CANON_FILES or rel.startswith(CANON_DIRS):
        return "canon"
    return "legacy"


def html_files():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in {".git", "node_modules"}]
        for fn in sorted(filenames):
            if fn.endswith(".html"):
                yield os.path.relpath(os.path.join(dirpath, fn), ROOT)


# ── G1: contrast, computed from the token block ──────────────────────────────

HEX = re.compile(r"^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")
RGBA = re.compile(r"^rgba?\(\s*([\d.]+)\s*,\s*([\d.]+)\s*,\s*([\d.]+)\s*(?:,\s*([\d.]+)\s*)?\)$")


def parse_tokens(css: str) -> dict[str, str]:
    """Pull --name: value pairs out of the :root block only."""
    m = re.search(r":root\s*\{(.*?)\n\}", css, re.S)
    if not m:
        return {}
    return {
        name: val.strip()
        for name, val in re.findall(r"(--[\w-]+)\s*:\s*([^;]+);", m.group(1))
    }


def to_rgba(value: str):
    """→ (r, g, b, a) in 0-255 / 0-1, or None if it is not a literal colour."""
    v = value.split("/*")[0].strip()
    if HEX.match(v):
        h = v[1:]
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 1.0
    m = RGBA.match(v)
    if m:
        a = float(m.group(4)) if m.group(4) is not None else 1.0
        return float(m.group(1)), float(m.group(2)), float(m.group(3)), a
    return None


def composite(fg, bg):
    """Flatten a translucent colour onto an opaque one."""
    r, g, b, a = fg
    return (r * a + bg[0] * (1 - a), g * a + bg[1] * (1 - a), b * a + bg[2] * (1 - a), 1.0)


def luminance(c):
    def ch(v):
        v /= 255.0
        return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
    return 0.2126 * ch(c[0]) + 0.7152 * ch(c[1]) + 0.0722 * ch(c[2])


def ratio(fg, bg):
    l1, l2 = luminance(fg), luminance(bg)
    lo, hi = sorted((l1, l2))
    return (hi + 0.05) / (lo + 0.05)


# What each text token is actually SET AT in style.css decides its threshold.
# WCAG "large" = >=24px, or >=18.66px bold. Everything else needs 4.5:1.
# Keep this table honest against the stylesheet — a token demoted to "large"
# to dodge a failure is the gate lying to you.
TEXT_ROLES = {
    "--text-1": ("body copy, headings", 4.5),
    "--text-2": ("lede, card copy, prose", 4.5),
    "--text-3": ("fineprint, rung-d, footer, provenance", 4.5),
    "--mercury-blue": ("eyebrows, links, receipt-go, step-num", 4.5),
    "--mercury-violet": ("loop separators, honest eyebrow", 4.5),
    "--mercury-teal": ("h1 accent span, receipt-k, tier-note", 4.5),
    "--mercury-chrome": ("h1 gradient stop", 3.0),
    "--mercury-rose": ("unused today; kept as a token", 4.5),
    "--ok": ("status positives", 4.5),
    "--amber": ("DEPRECATED dead theme", 4.5),
}


def gate_contrast(css: str, verbose: bool):
    tokens = parse_tokens(css)
    void = to_rgba(tokens.get("--void", "#04040e"))
    glass = to_rgba(tokens.get("--glass-bg", "rgba(255,255,255,0.035)"))
    backgrounds = [("--void", void)]
    if glass:
        backgrounds.append(("--glass-bg over --void", composite(glass, void)))

    rows, failures = [], []
    for tok, (role, threshold) in TEXT_ROLES.items():
        col = to_rgba(tokens.get(tok, ""))
        if col is None:
            continue
        for bg_name, bg in backgrounds:
            r = ratio(col, bg)
            ok = r >= threshold
            rows.append((tok, bg_name, r, threshold, ok, role))
            if not ok:
                failures.append((tok, bg_name, r, threshold, role))

    print(f"\nG1 contrast — {len(rows)} token/background pairs, "
          f"{len(failures)} below AA")
    if verbose or failures:
        for tok, bg, r, th, ok, role in rows:
            if verbose or not ok:
                mark = "ok  " if ok else "FAIL"
                print(f"   {mark} {r:5.2f}:1 (needs {th}) {tok:<18} on {bg:<24} — {role}")
    return failures


# ── G2-G8: per-page HTML gates ───────────────────────────────────────────────

class PageScan(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.inline_styles = []      # (line, tag)
        self.h1s = []                # line numbers
        self.imgs_no_dim = []        # (line, src)
        self.og_image = False
        self.style_blocks = []       # (line, n_lines)
        self._style_open = None

    def handle_starttag(self, tag, attrs):
        line = self.getpos()[0]
        d = dict(attrs)
        if "style" in d:
            self.inline_styles.append((line, tag))
        if tag == "h1":
            self.h1s.append(line)
        if tag == "img":
            if not (d.get("width") and d.get("height")):
                self.imgs_no_dim.append((line, d.get("src", "?")))
        if tag == "meta" and d.get("property") == "og:image" and d.get("content"):
            self.og_image = True
        if tag == "style":
            self._style_open = line

    def handle_endtag(self, tag):
        if tag == "style" and self._style_open is not None:
            self.style_blocks.append((self._style_open, self.getpos()[0] - self._style_open))
            self._style_open = None


# Hex outside style.css. Skip SVG-safe places? No — the rule is absolute: all
# colour lives in style.css and diagrams use .diagram classes. But a hex inside
# a data: URI or an href fragment is not a colour, so anchor the match to a
# colour-ish context.
HEX_IN_HTML = re.compile(r"#[0-9a-fA-F]{3}(?:[0-9a-fA-F]{3})?\b(?![\w-])")
# A hex inside <pre>/<code> is CONTENT, not styling — a post quoting the
# mermaid source of its own diagram is a receipt, and blanking it out to
# please the linter would delete the receipt. Masked before G7/G8 run.
CODE_BLOCK = re.compile(r"<(pre|code)\b.*?</\1>", re.S | re.I)


def mask_code(text: str) -> str:
    """Blank code spans, preserving line numbering so file:line stays true."""
    return CODE_BLOCK.sub(lambda m: re.sub(r"[^\n]", " ", m.group(0)), text)
HEX_SKIP_CTX = re.compile(r'(?:href|id|xlink:href|url\(#|content=")')
FONT_FAMILY = re.compile(r"font-family\s*[:=]", re.I)


def scan_page(path, rel):
    text = open(path, encoding="utf-8", errors="replace").read()
    p = PageScan()
    try:
        p.feed(text)
    except Exception:
        pass

    v = defaultdict(list)
    for line, tag in p.inline_styles:
        v["G2_inline"].append(f"{rel}:{line} <{tag} style=…>")
    for line, n in p.style_blocks:
        if n > 20:
            v["G3_pagestyle"].append(f"{rel}:{line} <style> is {n} lines (max 20)")
    if len(p.h1s) != 1:
        v["G4_h1"].append(f"{rel}: {len(p.h1s)} <h1> (need exactly 1)"
                          + (f" at lines {p.h1s}" if p.h1s else ""))
    for line, src in p.imgs_no_dim:
        v["G5_imgdim"].append(f"{rel}:{line} <img src={src}> has no width/height")
    if not p.og_image:
        v["G6_ogimage"].append(f"{rel}: no og:image")
    for i, line in enumerate(mask_code(text).splitlines(), 1):
        if FONT_FAMILY.search(line):
            v["G7_fontfamily"].append(f"{rel}:{i} {line.strip()[:90]}")
        for m in HEX_IN_HTML.finditer(line):
            ctx = line[max(0, m.start() - 40):m.start()]
            if HEX_SKIP_CTX.search(ctx):
                continue
            v["G8_hex"].append(f"{rel}:{i} {m.group(0)} — {line.strip()[:80]}")
    return text, v


GATE_ORDER = ["G2_inline", "G3_pagestyle", "G4_h1", "G5_imgdim",
              "G6_ogimage", "G7_fontfamily", "G8_hex"]
# Gates that cannot meaningfully apply to a meta-refresh stub.
STUB_SKIP = {"G6_ogimage"}


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("-v", "--verbose", action="store_true",
                    help="list every violation with its file:line")
    ap.add_argument("--all", action="store_true",
                    help="report legacy and stub buckets too")
    ap.add_argument("--bucket", choices=["canon", "frozen", "legacy", "stub", "exempt"],
                    help="report only this bucket")
    args = ap.parse_args()

    css = open(STYLESHEET, encoding="utf-8").read()
    contrast_failures = gate_contrast(css, args.verbose)

    per_bucket = defaultdict(lambda: defaultdict(list))
    counts = defaultdict(int)
    for rel in html_files():
        path = os.path.join(ROOT, rel)
        text = open(path, encoding="utf-8", errors="replace").read()
        b = bucket_of(rel.replace(os.sep, "/"), text)
        counts[b] += 1
        if b == "exempt":
            continue
        _, v = scan_page(path, rel)
        for gate, items in v.items():
            if gate in STUB_SKIP and (b == "stub" or rel in UTILITY_FILES):
                continue
            per_bucket[b][gate].extend(items)

    show = [args.bucket] if args.bucket else (
        ["canon", "frozen", "legacy", "stub"] if args.all else ["canon", "frozen"])

    print(f"\npages scanned: " + " · ".join(
        f"{b} {counts[b]}" for b in ("canon", "frozen", "legacy", "stub", "exempt")))

    canon_fail = 0
    for b in show:
        gates = per_bucket[b]
        total = sum(len(gates[g]) for g in GATE_ORDER)
        flag = ""
        if b == "canon":
            flag = "  ← must be 0" if total else "  ← clean"
        elif b == "frozen":
            flag = "  ← REPORT ONLY: Isaac's file, offers frozen (RULE 00 law 1)"
        print(f"\n{b.upper()} — {total} violations{flag}")
        for g in GATE_ORDER:
            items = gates[g]
            print(f"   {g:<16} {len(items)}")
            if args.verbose:
                for it in items:
                    print(f"        {it}")
        if b == "canon":
            canon_fail = total

    if not args.verbose and (canon_fail or contrast_failures):
        print("\n(run with -v for the file:line of every violation)")

    bad = canon_fail + len(contrast_failures)
    print(f"\nRESULT: {'FAIL' if bad else 'PASS'} "
          f"({canon_fail} canon violations, {len(contrast_failures)} contrast failures)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
