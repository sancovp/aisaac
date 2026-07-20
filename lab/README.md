# lab/ — explainer lab (unlisted test pages)

`explainer.html` — the animated diagram explainer + ink-stickman presenter,
**live and scroll-scrubbed**. Both engines run in the browser; the visitor's
scroll position is the composition clock. Not linked from the site nav.

Two modes (toggle bottom-right of the stage):

- **SCRUB** (default) — scroll drives the frame through a damped lerp; silent.
- **PLAY** — normal timed playback with the segment's narration mp3 through
  the composition's own `<Audio>`; scroll is suspended; exiting play syncs the
  scroll position back to the current frame. The mp3 is the only media file
  on the page.

Deep link: `?f=623` opens scrolled to that frame. Dev hook: `?p=0.42` previews
the page state at 42% scrub progress without scrolling (used for headless
screenshot verification — old-headless screenshot passes don't honor
`position:sticky`).

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
scrub.js proceeds backdrop-only after a 3s grace. Scroll feel (LERP_K=0.16,
VH_PER_BEAT=1.35, LINGER=0.35 — one-line constants in scrub.js) and mobile
need a human browser pass.
