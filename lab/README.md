# lab/ — explainer lab (unlisted test pages)

`explainer.html` — the animated diagram explainer + ink-stickman presenter,
**live and scroll-scrubbed**. No media files: both engines run in the browser
and the visitor's scroll position is the composition clock. Not linked from
the site nav.

How it works:

- `explainer.bundle.js` (~403 KB, 125 KB gz) — the video_aios diagram engine
  (`studio/base`, Remotion 4.0.409 + React 19) bundled with `@remotion/player`.
  Plays the HOOK segment of the `video1-sevenlevels` shot list (7 sentences,
  frames 0–1298 @30fps) — node-network/bar visuals, GAS spine, live layout
  math. Beat lines are blanked in the composition copy: on this page the
  captions are DOM text (below). `remotion` is aliased to `src/remotion-shim.ts`
  (Audio → null) since the page has no timeline playback.
- `explainer.presenter.bundle.js` (~1.24 MB, 354 KB gz) — the ink-stickman
  engine (`studio/stick`, React 18 + @react-three/fiber 8 + three) with the
  video1 presenter spec, transparent variant (WebGL canvas clears to alpha 0),
  in its own `@remotion/player`. A separate bundle because R3F 8's reconciler
  crashes under React 19 (`ReactCurrentBatchConfig` — verified). Two mount
  roots, two Reacts, no conflict. Both passes compile from the same shot rows,
  so frame N here is frame N of the backdrop — the composite coordinate
  contract holds live, layered at the same 1920×1080.
- `scrub.js` — the scroll driver. Scroll mechanics adapted from
  [oso95/scroll-world](https://github.com/oso95/scroll-world)
  `references/scrub-engine.js` (MIT, © 2026 cyw): segment layout, smoothstep
  copy curves, damped lerp toward the scrub target, route dots,
  reduced-motion. The `<video>.currentTime` core is replaced by `seekTo()` on
  the two live players. Each sentence beat is one scroll section (~1.35
  viewport-heights); its caption card fades in per the scroll-world curves,
  built from the real beat lines exported by the backdrop bundle — one
  authored source, three surfaces (film, page copy, timing).
- `fonts/*.woff2` — Inter (from the Debian `fonts-inter` OTFs); zero external
  requests.

Rebuild the bundles: `cd src && ./build.sh` (needs the `~/video_aios/studio/
{base,stick}` checkouts with their node_modules; see `src/build.sh`).

Dev hook: `?p=0.42` scrolls to 42% of the scrub range and snaps the damping —
used for headless screenshot verification.

Known limits: the presenter needs WebGL (virtually universal); if its bundle
fails to boot, scrub.js proceeds backdrop-only after a 3s grace. Scroll feel /
mobile need a human browser pass.
