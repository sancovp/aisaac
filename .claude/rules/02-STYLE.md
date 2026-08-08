# RULE 02 — THE STYLE (Mercury Glass // Living Instrument)

**The ruling (2026-08-07, CEO-decided per Isaac's delegation "come up with whatever
style this should be"):** the site keeps and ELEVATES Builder A's Mercurial-cyberglass
base. The look is **a living instrument, not a brochure** — the visual register of an
observatory reading a running world. Nothing here is decoration; every visual choice
serves RULE 01's deducibility mechanics.

## The language

1. **Base (KEEP, already law in style.css):** `--void` near-black · glass panels ·
   ONE accent (`--mercury-blue`) · JetBrains Mono for receipts/labels · Inter for UI ·
   self-hosted fonts, zero external requests · three breakpoints declared once.
2. **Display voice (ADD):** one OFL display serif (Fraunces preferred; Spectral
   acceptable), self-hosted woff2, used ONLY for: h1/h2 claims, the myth-register
   lines, pull-quotes. Everything else stays Inter/Mono. This is the single biggest
   de-generic move; it separates the voice of the claims from the voice of the chrome.
3. **The density gradient (ADD — depth made visible):** the DOOR is spacious (huge
   type, few elements, one action); each descent level gets visually denser (tighter
   leading, more mono, more hairline rules, data-table energy at the code-adjacent
   depths). A visitor FEELS the descent. Implement as a per-page `data-depth="0|1|2|3"`
   attribute on <body> with token overrides — no per-page CSS.
4. **Instrument details:** hairline rules (`--glass-border`) as the structural line
   language · mono micro-labels (already in use: "THE RECEIPT") · live-data styling
   (pulse/glow) is RESERVED for genuinely live/running things — a static element
   styled as live is the fake-dashboard sin in CSS form.
5. **Restraint laws:** no new colors, ever, without editing THIS rule · no gradients
   beyond the existing glass shine · no stock imagery, no emoji in chrome · motion
   ONLY inside the world engine + micro-transitions ≤200ms; `prefers-reduced-motion`
   respected everywhere · diagrams are inline SVG in token colors only.

## Mechanical quality gates (tools/style_qa.py — run before any style commit)

- WCAG AA contrast computed from the actual token values for every text/bg pair.
- Zero inline `style=` attributes; zero page `<style>` over 20 lines (existing law).
- Single h1 per page; every `<img>` has width/height; og:image exists per page-type.
- No font-family declarations outside style.css; no hex colors outside the token block.

## Implementation record (2026-08-07 — what shipped against this rule)

- **Display serif = Fraunces**, SIL OFL 1.1, self-hosted at
  `assets/fonts/fraunces-latin-var.woff2` (67 KB; licence beside it). SOFT and
  WONK axes pinned flat; `wght` + `opsz` left variable so optical sizing tracks
  the type size from one file. Applied to `h1`, `h2`, `.note blockquote`
  (pull-quotes) and `.myth`. Nothing else.
- **Density gradient** = `body[data-depth="0|1|2|3"]` overriding
  `--sec-y --claim-y --h1-size --h1-measure --h2-size --lede-size --lh-lede
  --lh-prose --rule-a --micro --r-card`. Depth 1 IS the `:root` default, so a
  page with no attribute renders as before. The gradient survives the 900px
  breakpoint rather than flattening. Applied: 0 = door (index/watch) ·
  1 = system/isaac/rungs · 2 = blog + notes · 3 = inside/.
- **`--text-3` corrected `#64748b` → `#6c7c92`.** The §"mechanical quality
  gates" contrast check found the old value at 4.29:1 on `--void` and 4.07:1 on
  glass — under AA, on the token that carries fineprint, the footer and every
  provenance line. Moved the smallest step along the existing slate ramp to
  clear AA on both (4.80 / 4.55). Same ramp, corrected — logged here because
  the restraint law requires any palette change to edit this rule.
- **The brand tag pills (2026-08-08).** `.eyebrow a` + `.eyebrow { flex-wrap }`.
  ZERO new colours and zero new block vocabulary: the eyebrow is already the mono
  uppercase label voice, so a pill is that voice plus a `--glass-border` hairline
  at `--r-sm`, and the hover border reuses `.rung:hover`'s existing rgba —
  deliberately, because the filter row and the pills are the same control and
  must light up the same way. Nothing else in the file gained a selector.
- **`.receipts-lede` unscoped (2026-08-08).** It existed only as
  `.receipts .receipts-lede`, so the identical class on the corpus-index section
  blurbs rendered as unstyled body copy. Added the unscoped base; the `.receipts`
  variant is untouched.
- **Not a colour change but worth knowing:** `--black`, `--grey`,
  `--grey-light` and `--accent` were referenced across the posts and defined
  NOWHERE, and `.post-nav` was used 40 times and defined nowhere. Retiring the
  inline styles resolved all of them onto real tokens and real classes.

## What "high-end" means here, testably

A stranger screenshots any page: it reads as one designed object with the door's
signature (void + glass + serif claims + mono receipts). No page could be mistaken for
a template default, a Notion export, or a generic SaaS landing page. The door's first
viewport contains: the running world, one serif claim, one Enter. Nothing else.
