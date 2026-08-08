# lab/ — explainer lab (unlisted test pages)

`explainer.html` — the animated diagram explainer + ink-stickman presenter,
**live and scroll-scrubbed**. Both engines run in the browser; the visitor's
scroll position is the composition clock.

Two modes (toggle bottom-right of the stage):

- **SCRUB** (default) — scroll drives the frame through a damped lerp; silent.
- **PLAY** — normal timed playback with the segment's narration mp3 through
  the composition's own `<Audio>`; scroll is suspended; exiting play syncs the
  scroll position back to the current frame. The mp3 is the only media file
  on the page.

Deep link: `?f=623` opens scrolled to that frame. Dev hook: `?p=0.42` previews
the page state at 42% scrub progress without scrolling (used for headless
screenshot verification — old-headless screenshot passes don't honor
`position:sticky`). `?bare=1` hides the chrome for the same screenshot pass.

## Three SURFACES, one file (`?embed=…`)

This page is embedded twice on the public site. Both embeds are the SAME file
under a query param — there is no second copy, no reskin, and no video. The
rule the site templates state and this file obeys: *the exhibit keeps its own
look; reskinning the artifact destroys the proof.* The host page owns the
frame, this page owns everything inside it.

| URL | chrome | clock | audio | used by |
|---|---|---|---|---|
| `explainer.html` | full — header, lede, footer, progress rail, route rail, mode toggle | **scroll is the clock** | play mode | the raw instrument; the engineer's descent rung |
| `explainer.html?embed=door` | none | **autoruns and loops** on a wall clock | never | `index.html` — the first-screen frame |
| `explainer.html?embed=room` | route rail + mode toggle only | autoruns until the visitor takes it, then wheel / drag | play mode, explicit click only | `watch.html` — the exhibit |

Behaviour the embeds add (all of it in `scrub.js`; no bundle rebuild):

- **Boot is gated on the diagram engine alone.** `boot()` no longer waits up to
  3s for the presenter; it mounts the instant `window.AisaacBackdrop` exists and
  attaches the presenter later on the `aisaac:presenter-ready` event that
  `presenter-entry.tsx` already dispatched, handing it the current frame. First
  motion costs 125 KB gz instead of 479 KB. This improves the standalone page too.
- **Off-screen and hidden-tab pause.** An `IntersectionObserver` with `root:null`
  (which intersects the top-level viewport even from inside an iframe) plus
  `document.hidden`. A homepage scrolled past the door drops the frame to idle,
  and because the elapsed delta is dropped rather than banked, the film does not
  jump when it comes back.
- **`prefers-reduced-motion` at the door does not autorun.** It renders ONE real
  frame (mid-beat 2) from the same two engines and stops. A held real frame is
  honest; a poster image pretending to be a live engine would not be.
- **Room mode releases the page at both ends.** Wheel is captured only while the
  composition has somewhere to go; at frame 0 scrolling up, and at the last frame
  scrolling down, the handler stops calling `preventDefault()` and the parent page
  scrolls normally. The exhibit is a clock you can put down, never a scroll trap.
- **`#door-enter`** is a real `<a href="../watch.html" target="_top">` in the
  markup, shown by CSS only under `?embed=door`. It is keyboard-focusable and it
  works whether or not any script ran.
- **`<noscript>`** renders a designed still on the lab's own background — one mono
  line plus a live link to the same seven sentences in prose. Deliberate, not
  missing.

Degradation ladder, each rung shipping something real: WebGL missing → the
diagram runs alone (the existing `boot()` P-null path) → JavaScript off → the
`<noscript>` still + link → the iframe blocked entirely → the host page's own
figcaption still states in prose exactly what the frame does.

## Pieces

- `explainer.bundle.js` (~403 KB, 125 KB gz) — the video_aios diagram engine
  (`studio/base`, Remotion 4.0.409 + React 19) bundled with `@remotion/player`.
  Plays the HOOK segment of the `video1-sevenlevels` shot list (7 sentences,
  frames 0–1298 @30fps) — node-network/bar visuals, GAS spine, live layout math
  including the presenter-exclusion ZONE. Beat lines are blanked in the
  composition copy: the captions are DOM text in the scroll sections.
- `explainer.presenter.bundle.js` (~1.24 MB, 354 KB gz) — the ink-stickman
  engine (`studio/stick`, React 18 + @react-three/fiber 8 + three) with the
  video1 presenter spec, transparent variant (WebGL canvas clears to alpha 0),
  in its own `@remotion/player`. A separate bundle because R3F 8's reconciler
  crashes under React 19 (`ReactCurrentBatchConfig` — verified crash). Two
  mount roots, two Reacts, no conflict. Both passes compile from the same shot
  rows, so frame N here is frame N of the backdrop — the composite coordinate
  contract holds live, layered at the same 1920×1080.
- `scrub.js` — the scroll driver; see the attribution ledger below.
- `audio/seven-levels/seg1_hook.mp3` — the segment TTS narration (play mode).
- `fonts/*.woff2` — Inter (from the Debian `fonts-inter` OTFs); zero external
  requests beyond the page's own files.

## Provenance / reproducibility

Bundles built from the `~/video_aios` checkout at commit
**`afd48414bc99b717b0929c65bb2b0d8ac28ce57e`** (studio/base + studio/stick,
2026-07-17; includes the zone-law fix moving the diagram ZONE off the
presenter corner). Rebuild: `cd src && ./build.sh` (needs both engine
checkouts with their node_modules).

## scroll-world attribution + pattern ledger

Scroll mechanics adapted from
[oso95/scroll-world](https://github.com/oso95/scroll-world)
`references/scrub-engine.js` (MIT, © 2026 cyw), after a full read of the
skill (`SKILL.md` + all references).

**Adopted:** scroll→time scrubbing on a sticky stage over a tall runway
(+1vh tail so the last beat completes); damped rAF lerp toward the scrub
target; per-section copy with the smoothstep opacity curves (first greets on
landing, last holds, middle peaks mid-range); `lingerEase` per-section dwell
(time settles mid-sentence where the copy peaks; boundary frames untouched);
route rail with dots + hover/active labels; top scrollbar progress; the
mouse-wheel scroll hint; width-gated resize on touch (URL-bar collapse must
not yank the scroll); `prefers-reduced-motion` (lerp snaps; hint stops).

**Adapted:** `<video>.currentTime` → `seekTo()` on two live `@remotion/player`
mounts (no media video); section scroll ranges are proportional to each
sentence's real TTS frame count instead of a uniform `diveScroll`; the copy
card is num + eyebrow + the full narration sentence (the narration IS the
copy — no separate title/body); the route rail sits left (our film's caption
column owns the right); copy scrim mirrored to the right edge for the same
reason.

**Dropped (with why):** Higgsfield generation, stills/posters and blob video
loading, seek-coalescing and iOS video priming (no video element to harden);
the seam/connector discipline and crossfades (structurally unnecessary — the
excerpt is ONE continuous composition, which is the live-engine advantage);
mobile clip variants (no clips); drifting particles (scroll-world itself
drops them alongside scrubbing cost — our scrub cost is React renders);
brand topbar/nav/CTA chrome (lab page, not a landing page).

## Known limits

The presenter needs WebGL (virtually universal); if its bundle fails to boot,
scrub.js proceeds backdrop-only. Scroll feel (LERP_K=0.16, VH_PER_BEAT=1.35,
LINGER=0.35 — one-line constants in scrub.js) and mobile need a human browser
pass. Two more constants belong to the embeds and want the same pass:
`EMBED_FPP=0.5` (frames per px of wheel/drag in room mode) and `HELD_FRAME=240`
(the frame the reduced-motion door holds).

**Coarse pointers in room mode scrub on HORIZONTAL drag only.** Vertical touch
is left to the page on purpose (`touch-action: pan-y` on the stage), because a
frame that eats vertical swipes on a phone is a trap, and the end-release rule
that saves the mouse wheel has no clean touch equivalent. A phone visitor gets
the autorun, the route dots and the play toggle; taking the clock by hand is a
sideways gesture. This is a stated limit, not an oversight.

**Not measured yet:** cold-load time to first engine frame on throttled mobile.
The door is on every homepage visit, so this is the number that decides whether
the `defer` order above is sufficient or the diagram engine needs splitting.
