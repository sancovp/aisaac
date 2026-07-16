# lab/ — explainer lab (unlisted test pages)

`explainer.html` — the animated diagram explainer running web-native, with the
ink-stickman presenter overlaid. Not linked from the site nav.

How it works:

- `explainer.bundle.js` (~406 KB) — the video_aios diagram engine
  (`studio/base`, Remotion 4.0.409 + React 19) bundled with `@remotion/player`
  into one static IIFE. It plays the HOOK segment of the `video1-sevenlevels`
  shot list (7 sentences, frames 0–1298 @30fps) live in the browser: animated
  node-network/bar visuals, per-word caption build-in, the GAS spine.
- `presenter-seg1.webm` (~2.1 MB) — the ink-stickman presenter pass
  (`studio/stick`), alpha-transparent VP9, stream-copied from the full
  video1 presenter render (frames 0–1302). Overlaid as a `<video>` and
  drift-corrected against the player clock every frame update. Both passes
  were compiled from the same shot rows, so frame N of the webm is frame N
  of the composition.
- `audio/seven-levels/seg1_hook.mp3` — the segment TTS narration, played by
  the composition's own `<Audio>` tag; `window.remotion_staticBase` is set to
  the page directory so it resolves under any deployment prefix.
- `fonts/*.woff2` — Inter (converted from the Debian `fonts-inter` OTFs), so
  the page has zero external requests.

Rebuild the bundle: `cd src && ./build.sh` (needs the `~/video_aios/studio/base`
checkout with its node_modules; see `src/build.sh`).

Known limits: the presenter overlay needs VP9-alpha support (Chrome/Edge/
Firefox — not Safari; the page detects this and drops the overlay with a
note). Known upstream layout defect: leftmost diagram elements can sit where
the presenter stands (video1 zone-law finding); visible here as the stickman
brushing the L1/L7 node labels in two beats.
