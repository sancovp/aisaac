# RULE 02 — THE STYLE (the Blueprint System)

**The ruling (*USER*):** the site is drawn like a diagram on a drafting sheet — the reference is
bugster.dev, taken in **white and black** instead of its off-white and lime, with the stark
black bands Palantir uses. Nothing here is decoration; every visual choice serves RULE 01's
deducibility mechanics: the page looks like an engineer's working drawing of a running system.

## The language

1. **Palette — paper and ink, nothing else.** `--paper #fff` · `--ink #000` (true black, never a
   tinted near-black) · `--text-2 #3d3d3d` · `--text-3 #6b6b6b` (the lightest text allowed, 5.3:1)
   · `--line #e6e6e6` (the blueprint columns). Every legacy accent token name (`--mercury-*`,
   `--amber`) resolves to ink or a grey, so no page can carry a colour. **THE ONE COLOUR is
   `--signal #e10600`, and it belongs to the top bar's BOOK A CALL button alone** (paper text on
   it = 4.97:1). Every other colour on a page comes from media (the films, the portrait).
   **No new colours, ever, without editing THIS rule.**
2. **Type — Geist + Geist Mono**, one family, self-hosted (`assets/fonts/geist-var.woff2`,
   `geist-mono-var.woff2`, SIL OFL 1.1, licence beside them). **Geist Mono 700** carries every
   claim (h1), every number, every button and every label; **Geist** carries the prose and the h2
   section heads (600). No other face on a presented page.
3. **The drafting sheet:** four faint vertical BLUEPRINT COLUMNS run the height of the page at
   the container's edges and its thirds (`body::before`); a band with its own ground covers them.
4. **The card** (`.bp-card`): paper, a 1px ink outline, radius `--r-bp` 28px. Inside it,
   **hairline dividers** (`.bp-rule` across, `.bp-split` down) — and a small square **NODE**
   (11px, paper fill, ink outline) wherever a divider meets the card's edge, like the handles a
   diagram editor shows on a selected shape. Nodes appear ONLY at those junctions.
5. **The label:** `.eyebrow` = a square node, a short ink connector, then the text; on the
   presented page the text sits in a hairline **pill** (`.eyebrow > .pill`). Sentence case, never
   all caps. One per section, never above every heading.
6. **The bands alternate:** plain paper (columns show) · **grain** (`.bp-band`: paper with the
   `--grain` noise tooth, ink rules top and bottom) · **ink** (`.bp-ink`: the one black band,
   reserved for the final action).
7. **The button** (`.cta-primary`): paper, 1px ink outline, radius 14px, Geist Mono 600; it
   INVERTS on hover (ink fill, paper text). On the ink band it is the same button inverted.
8. **Frames** (`.artifact-frame`, `.portrait-frame`): paper, 1px ink outline, radius 22px, no glass,
   no glow, no shadow. A film's own controls sit ON the film and stay light-on-dark.
9. **The top bar** (`.nav-glass`): the ONE glass surface — paper at 55% under a 16px blur, a
   hairline beneath, **sticky, so it never leaves the screen**. It carries exactly two things: the
   wordmark `TWI: Transforming the World, Incorporated` on the left (a `<span>`, never a link) and
   the red **BOOK A CALL** button (`.nav-book`, `--signal`, inverts to ink on hover) on the right —
   the visitor can never not see the button. On a phone the wordmark wraps; the button never
   leaves the screen.
10. **Restraint:** no gradients, no glass blur outside the top bar, no glow, no shadows · motion only in the films and
   in ≤200ms colour flips that answer a hover · `prefers-reduced-motion` respected everywhere
   (the silent loops stop on their poster) · diagrams the site draws are inline SVG in ink.

## The density gradient (still law)

`body[data-depth="0|1|2|3"]` overrides `--sec-y --claim-y --h1-size --h1-measure --h2-size
--lede-size --lh-lede --lh-prose --rule-a --micro --r-card`: the door (0) is spacious, each descent
denser, depth 3 (inside/ and patterns.html) tightest. `--rule-a` is the hairline alpha on paper
(0.12 → 0.22 as you descend). No per-page CSS.

## The closed vocabulary (still law)

A page is built from the classes `style.css` already declares; doubling the content must cost
the stylesheet nothing. `.data-table a` carries the link colour; `.data-table td:last-child` takes
`--micro`. The architecture entry (`.arch` · `.arch-what` · `.arch-dia` · `.arch-moves` ·
`.arch-runs`) holds patterns.html: a repository's own diagram ships unaltered as an `<img>`, and
an `.arch-dia` structure diagram is **PURE ASCII, 0x20–0x7E only** — one glyph that falls back to
a system face breaks the monospace grid.

## Mechanical quality gates (`tools/style_qa.py` — run before any style commit, read its output)

- WCAG AA contrast computed from the actual token values for every text/background pair.
- Zero inline `style=` attributes; zero page `<style>` over 20 lines.
- Single h1 per page; every `<img>` has width/height; og:image exists per page type.
- No font-family declarations outside style.css; no hex colours outside the token block.
- ⛔ The gate does NOT see: a rule that loses the cascade to a later one of equal specificity
  (the About card kept its desktop grid on phones this way — measure `scrollWidth` at 390px), or
  a hard-coded background that ignores the tokens (the booking dialog did). Look at the page at
  1440 and at 390, and open the dialog, before calling a style change done.

## What "high-end" means here, testably

A stranger screenshots any presented page: it reads as one drafted object — white sheet, black
ink, mono claims, outlined cards with nodes on their dividers. It could not be mistaken for a
template default, a Notion export, or a generic SaaS landing page.
