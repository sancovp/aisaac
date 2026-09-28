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
     never on the sentence: *but* and *before* in `--signal` (the problem, where you are) · *so we*
     in `--leak-act #b45309` (amber — yellow text is unreadable on white; 5.0:1) · *after* in
     `--leak-good #15803d` (green, 5.0:1). The numbers stay ink.
   - **the SECTION TINTS** (*USER*'s ruling: the sections must be told apart by colour) — a
     section's hue says what it is about: **red** the problem · **gold** the framework · **violet**
     the theory · **cyan** what you build · **green** growth and community. A tinted section
     (`.bp-sec.tinted.tint-<hue>`) gets a soft ground (`--tint-<hue>-bg`), a 4px top edge in its
     accent (`--tint-<hue>`, ≥5.4:1 on its ground), and the accent on its label, its card headings,
     its numerals, its icons and its card nodes — the section's tab (the square at the head of its
     label) is FILLED in the accent, and so are the nodes where its cards' dividers meet their edges; the white cards sit on the tint, and that contrast is what separates the
     sections. Utility sections (how it works · who it's for · questions · the story) stay plain or
     grain, so a colour always means something. Used on `framework.html`, `framework-worksheet.html`
     and `isaac-wostrel-rubin.html`. ⛔ **`ai-transformation.html` has NO tinted SECTIONS** (*USER*'s
     ruling) — its sections stay black and white; the hue there lives only in TINTED CELLS
     (`.bp-cell.cell-tint.tint-<hue>`: the cell on its hue's soft ground, its heading and icon in the
     accent, a corner cell taking the card's radius), in exactly two places — What you get's cards
     (every department gold · every piece of software cyan · the AI teams violet · your SOPs green)
     and What it becomes' stages (Foundation gold → Hardening cyan → Closure violet).
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
6. **The bands:** plain paper (columns show) · **grain** (`.bp-band`: paper with the
   `--grain` noise tooth, ink rules top and bottom) · **tinted** (§1's section tints, which
   replace the grain wherever a section has a meaning to colour) · **ink** (`.bp-ink`: the one
   black band, reserved for the final action). Two sections of the same kind are never adjacent.
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
   call; the HERO LOOP on the right (a silent looping `video[data-loop]`, styled exactly as the
   drawing was) with NO divider between them, bleeding off the card's right edge (the cell clips it
   to the card's corner). It sits on the card's exact white (#fff — video luma 235, the legal white)
   and carries the characters of the site's own films (the owner with the gold orb, the cyan agents,
   the black wires), never stock art. Under a hairline, the film's sheet: the WHO IT'S FOR
   block first (`.hero-for`, a mono key over the avatar in prose), then the VSL at the card's full
   width. On a phone it stacks: copy, the loop, who it's for, film.
9. **The top bar** (`.nav-glass`): the ONE glass surface — paper at 55% under a 16px blur, a
   hairline beneath, **sticky, so it never leaves the screen**. It carries exactly two things: the
   wordmark `Transformations With Isaac` on the left (a `<span>`, never a link) and
   the red **BOOK A CALL** button (`.nav-book`, `--signal`, inverts to ink on hover) on the right —
   the visitor can never not see the button. On a phone the wordmark wraps; the button never
   leaves the screen.
10. **The pinned stack** (`.pin-stack`, `stack.js`, *USER*'s ruling): What I do → What you get →
   What it becomes → Who helps you. **THE HOLD IS WHILE YOU READ, NEVER AFTER.** Each `.pin` sticks
   under the nav the moment its top reaches it; from then the reader's scroll moves its content at
   HALF SPEED until its last line is on screen, so a section cannot be flicked past. The next `.sheet`
   (opaque paper carrying its own blueprint columns, an ink edge on top, at least a screen tall) is
   timed to arrive exactly then — its top margin is the extra scroll the slowdown costs — and slides
   up over a section that has just been read; nothing ever sits frozen waiting to be covered. A
   section that fits the screen has nothing to slow, so the next sheet simply slides over it. A pinned
   section that changes height (a reader opening a leak tree) is re-measured on the spot
   (`ResizeObserver`). The slow read moves the STICKY POINT itself (`--pin-top` rises from the nav to
   nav − the overflow), never a transform — the browser releases a sticky section by its real box, so a
   transformed one lets go while the sheet meant to cover it is still below it, and the section under
   it shows through the gap. The wrapper ends every pin with the stack, so no pinned section shows
   through later ones. The pins go sticky only once `stack.js` runs (`.is-live`): JS off, normal scroll.
   **THE SCROLL SPEED HAS A CEILING** (*USER*'s ruling, the landing page only): a wheel or trackpad moves
   the page at most 2,200 px a second (`stack.js`); below that it is the reader's own scroll, above it
   the travel is spread out and never more than ~0.6 s of it is banked, so nothing coasts on after the
   hand stops; a reversal turns at once. Touch keeps the phone's own scrolling; pinch-zoom, sideways
   scroll and an open dialog are untouched.
11. **The leak tree** (`.leak`, a native `<details>`): closed, one row — the item in mono and its
   one hook number in grey, a `+` at the right; open, an ink TRUNK down the left with a tick to
   each branch — the numbers (with its source in small mono beneath) · but · *Before, you're* · so we · *After,
   you* (in ink, the dream) — BEFORE and AFTER frame the fix, and it ENDS on the dream. Each label is
   the opening words of its sentence. Labels coloured per §1. Keyboard-operable; reduced motion drops the
   grow and shrink. The FIRST tree ships open, so the visitor sees what a row holds; the rest
   stay closed, and nothing opens on scroll — an opening tree pushes the pinned section's bottom
   away while the reader is mid-section. Every open GROWS (its height, ~360ms eased; `stack.js`), and
   UNHURRIED hover is the rule: a tree opens only when the pointer RESTS on its row (~260ms) — a cursor
   passing over the list opens nothing — and a hover-opened tree closes ~320ms after the pointer leaves,
   shrinking shut, so crossing the gap between rows never snaps it. With a MOUSE a tree OPENS ON HOVER (*USER*'s ruling;
   `stack.js`): pointing at a row opens it, leaving closes a tree hover opened, a click pins it open
   and a second click closes it; a tree already open is never closed by hover; touch keeps the tap.
12. **Icon tiles** (`.get-ico`): a line icon (Lucide shapes, ISC licence) in ink, in a 38px
   outlined square beside a card label — never an emoji (they render differently per device). Every
   card, step and group on `framework.html` carries one naming what it IS (a megaphone for PSA, a
   stethoscope for SCREENING…), so a grid of cards reads as distinct things, not a jumble; a ladder
   row carries a small inline one (`.fw-ico`) inheriting its label's colour. In a tinted section
   the icons take the accent.
13. **Restraint:** no gradients, no glass blur outside the top bar, no glow, no shadows · motion
   only in the films (the VSL's silent autoplay included), the parcels, the pinned stack (driven by the reader's own scroll), and
   ≤200ms colour flips that answer a hover · `prefers-reduced-motion` respected everywhere
   (the silent loops stop on their poster) · diagrams the site draws are inline SVG in ink.

14. **The personal page's own pieces** (`isaac-wostrel-rubin.html`, `.me-*` · `.paper-*` · `.book-*`
   · `.repo*`): the paper card (its abstract's sentences left, status right) · the BOOK COVER — the
   one card that ink FILLS, because it is the book's own object, like a film, carrying the book's
   mark in its own colours · the contents list set in mono by the chapters' glyphs · the passages
   as quotations with an ink rule, inside a card (on the bare sheet the parcels cross them) · one
   outlined card per repository, the whole card the link, two to a row (ten repos, five even rows).
   The seven beliefs reuse the leak tree: *The claim* in ink, *The receipt* in green.

15. **The framework funnel's own pieces** (`framework.html`, `.fw-*` · `.nav-get`): its top-bar
   button is INK (`.nav-get`), because red means Book a call and this page's action is the opt-in ·
   the hero is ONE column, one card cut by hairlines: the headline and the sub · the Top film at
   the card's full width · the opt-in as ONE row (name · email · the button; stacked on a phone) · `partners.html` takes the same hero with its IMAGE
   (`.fw-art`: full width, no frame, on the card's exact white) where the film would be · the 7 steps (the first section under the hero) as outlined cards
   with a big grey numeral, the seventh (the question) full width · the FAQ reuses the leak tree ·
   the three steps reuse the arrow nodes (§4) · the AUTONOMY LADDER: the three roles across a split,
   then the grades as rows (grade · its state in mono · what it means) · the bootcamp frameworks as
   the same outlined cards. THE WORKSHEET (`framework-worksheet.html`, `.ws-*`): fill-in tables with
   ink rules, writing lines, square tick boxes — and it PRINTS (the chrome drops out under print).

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
