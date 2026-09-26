# RULE 02 — THE STYLE (the Blueprint System)

**The ruling (*USER*):** the site is drawn like a diagram on a drafting sheet — the reference is
bugster.dev, taken in **white and black** instead of its off-white and lime, with the stark
black bands Palantir uses. Nothing here is decoration; every visual choice serves RULE 01's
deducibility mechanics: the page looks like an engineer's working drawing of a running system.

## The language

1. **Palette — paper and ink, nothing else.** `--paper #fff` · `--ink #000` (true black, never a
   tinted near-black) · `--text-2 #3d3d3d` · `--text-3 #6b6b6b` (the lightest text allowed, 5.3:1)
   · `--line #e6e6e6` (the blueprint columns). Every legacy accent token name (`--mercury-*`,
   `--amber`) resolves to ink or a grey, so no page can carry a colour. Colour enters in exactly
   two places, both *USER*'s rulings:
   - **`--signal #e10600` = BOOK A CALL, everywhere** — the top bar's button and every
     `.cta-primary[data-buy="call"]`, on paper and on the ink band alike (paper text on it =
     4.97:1; hover `--signal-deep #b30500`). Nothing else is red, except the leak tree's two warning labels (below).
   - **the loop's own palette as the level separators** — `--loop-gold #ff8c1f` (the CEO's orb:
     Solo and Solo again), `--loop-cyan #1abfff` (Org), `--loop-violet #9e6bff` (Automation), as
     3px bars between the four levels only, so the list and the film beside it share one colour
     code. Bars, never text.
   - **the parcels' yellows** (`--pkg`, drawn inside the token: ink outline, three yellow faces,
     a strip of tape) — the only other colour, and it lives only on the parcels (§3).
   - **the leak tree's branch labels** (§11), each wearing its meaning on the LABEL and its tick,
     never on the sentence: *but* and *instead of* in `--signal` (the problem, the old way) · *so we*
     in `--leak-act #b45309` (amber — yellow text is unreadable on white; 5.0:1) · *so that you* in
     `--leak-good #15803d` (green, 5.0:1). The numbers stay ink.
   Every other colour on a page comes from media (the films, the portrait).
   **No new colours, ever, without editing THIS rule.**
2. **Type — Geist + Geist Mono**, one family, self-hosted (`assets/fonts/geist-var.woff2`,
   `geist-mono-var.woff2`, SIL OFL 1.1, licence beside them). **Geist Mono 700** carries every
   claim (h1), every number, every button and every label; **Geist** carries the prose and the h2
   section heads (600). No other face on a presented page.
3. **The drafting sheet:** four faint vertical BLUEPRINT COLUMNS run the height of the page at
   the container's edges and its thirds (`body::before`); a band with its own ground covers them.
   **THE PARCELS** (`.bp-parcels`, *USER*'s ruling — a little easter egg, candy): isometric
   yellow packages on the two INNER columns only — never the outer columns beside the cards. Ten
   per column: the page is cut into ten equal stretches and each parcel shuttles back and forth
   inside its OWN stretch (12 s / 14.5 s a pass, eased, staggered phases), so two parcels can never
   meet anywhere and one is always somewhere to catch. They live IN THE PAGE, not the viewport:
   scrolling passes them, they never follow it. The layer sits behind everything, so a parcel only
   shows crossing a gap between cards. Drawn, never the 📦 emoji. Off on phones (the inner columns
   sit at the screen edge there) and under reduced motion.
4. **The card** (`.bp-card`): paper, a 1px ink outline, radius `--r-bp` 28px. Inside it,
   **hairline dividers** (`.bp-rule` across, `.bp-split` down) — and a small square **NODE**
   (11px, paper fill, ink outline) wherever a divider meets the card's edge, like the handles a
   diagram editor shows on a selected shape. Nodes appear ONLY at those junctions — and, where the
   cells are the STEPS OF ONE SEQUENCE (What it becomes: 1 · Foundation → 2 · Hardening → 3 ·
   Closure), as a larger node carrying an arrow (`.step-arrow`) at the middle of each divider
   between steps, turned to point down when the steps stack on a phone. A sequence's two ends sit
   on a RAIL under it (`.becomes-rail`): where it starts, one long ink arrow, where it ends.
5. **The label:** `.eyebrow` = a square node, a short ink connector, then the text; on the
   presented page the text sits in a hairline **pill** (`.eyebrow > .pill`). Sentence case, never
   all caps. One per section, never above every heading.
6. **The bands alternate:** plain paper (columns show) · **grain** (`.bp-band`: paper with the
   `--grain` noise tooth, ink rules top and bottom) · **ink** (`.bp-ink`: the one black band,
   reserved for the final action).
7. **The button** (`.cta-primary`): paper, 1px ink outline, radius 14px, Geist Mono 600; it
   INVERTS on hover (ink fill, paper text). On the ink band it is the same button inverted.
   **Any button that books the call is red instead** (§1).
8. **Frames** (`.artifact-frame`, `.portrait-frame`): paper, 1px ink outline, radius 22px, no glass,
   no glow, no shadow. A film's own controls sit ON the film and stay light-on-dark. **The VSL
   starts WITH SOUND** wherever the browser allows it. Where the browser refuses sound before the
   visitor's first click (Chrome's and Safari's autoplay policy), it plays silently while on screen
   (paused when scrolled away), its controls hidden and ONE paper button on its centre,
   `Watch with sound` (`.vsl-sound`, inverts to ink on hover) — and the visitor's first click, tap or
   key press ANYWHERE on the page (except one that opens the booking form) turns the sound on and
   restarts the film. From then the visitor owns it. Reduced motion: no autoplay.
8b. **The hero** (`.hero-split`, bugster.dev's shape): one card; the copy on the left — pill, the h1
   in Geist Mono 700 at up to 3.7rem with its second clause in `--text-3`, the lede, the red Book a
   call; the drawing on the right with NO divider between them, bleeding off the card's right edge
   (the cell clips it to the card's corner). The drawing sits on the card's exact white (#fff,
   measured at its corners) and carries the characters of the site's own films (the owner with the
   gold orb, the cyan agents, the black wires), never stock art. Under a hairline, the film's sheet: the WHO IT'S FOR
   block first (`.hero-for`, a mono key over the avatar in prose), then the VSL at the card's full
   width. On a phone it stacks: copy, drawing, who it's for, film.
9. **The top bar** (`.nav-glass`): the ONE glass surface — paper at 55% under a 16px blur, a
   hairline beneath, **sticky, so it never leaves the screen**. It carries exactly two things: the
   wordmark `Transformations With Isaac` on the left (a `<span>`, never a link) and
   the red **BOOK A CALL** button (`.nav-book`, `--signal`, inverts to ink on hover) on the right —
   the visitor can never not see the button. On a phone the wordmark wraps; the button never
   leaves the screen.
10. **The pinned stack** (`.pin-stack`, `stack.js`, *USER*'s ruling): What I do → What you get →
   What it becomes → Who helps you. Each `.pin` scrolls fully into view and STAYS while the next `.sheet` slides up
   over it like a sheet laid on top — opaque paper carrying its own blueprint columns, an ink edge
   on top, at least a screen tall. Each pin point is MEASURED (`min(nav height, viewport − section
   height)`), so a section taller than the screen pins only once its bottom is visible and nothing
   is covered unread. A pinned section that changes height (a reader opening a leak tree) is
   re-measured on the spot (`ResizeObserver`). The wrapper ends every pin with the stack, so no
   pinned section shows through later ones. JS off: normal scroll.
11. **The leak tree** (`.leak`, a native `<details>`): closed, one row — the item in mono and its
   one hook number in grey, a `+` at the right; open, an ink TRUNK down the left with a tick to
   each branch — the numbers (with its source in small mono beneath) · but · so we · instead of · so that
   you (in ink, the dream) — it ENDS on the dream. Labels coloured per §1. No JS; keyboard-operable; the open is a 180ms fade that
   reduced motion drops. The FIRST tree ships open, so the visitor sees what a row holds; the rest
   stay closed, and nothing opens on scroll — an opening tree pushes the pinned section's bottom
   away while the reader is mid-section.
12. **Icon tiles** (`.get-ico`): a line icon (Lucide shapes, ISC licence) in ink, in a 38px
   outlined square beside a card label — never an emoji (they render differently per device).
13. **Restraint:** no gradients, no glass blur outside the top bar, no glow, no shadows · motion
   only in the films (the VSL's silent autoplay included), the parcels, the pinned stack (driven by the reader's own scroll), and
   ≤200ms colour flips that answer a hover · `prefers-reduced-motion` respected everywhere
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
- ⛔ The presented page links `style.css`, `vsl.js` and `stack.js` with a `?v=` version: bump it in
  the SAME commit as any change to those files, or returning visitors — and the verification
  browser — keep the old file and the change looks unmade. A replaced image gets a NEW filename
  for the same reason. Before judging a change on screen, check the computed value, not the
  screenshot.

## What "high-end" means here, testably

A stranger screenshots any presented page: it reads as one drafted object — white sheet, black
ink, mono claims, outlined cards with nodes on their dividers. It could not be mistaken for a
template default, a Notion export, or a generic SaaS landing page.
