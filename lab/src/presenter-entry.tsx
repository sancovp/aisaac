/**
 * aisaac explainer lab — PRESENTER bundle (React 18).
 *
 * Mounts the LIVE ink-stickman engine (video_aios studio/stick: ExplainerVideo
 * with the video1 presenter spec, transparent variant — WebGL canvas clears to
 * alpha 0) in its own @remotion/player, carrying its OWN React 18 + R3F 8 +
 * three. This bundle is separate from the backdrop bundle because
 * @react-three/fiber 8 does not run under React 19 (its reconciler reads
 * ReactCurrentBatchConfig, removed in 19 — verified crash). Two mount roots,
 * two Reacts, zero conflict; scrub.js drives both from one scroll clock.
 *
 * The presenter spec and the backdrop shot list compile from the same shot
 * rows, so frame N here IS frame N of the backdrop — layered at the same
 * 1920x1080, the composite coordinate contract holds live in the page.
 */
import React, { useEffect, useRef } from 'react';
import { createRoot } from 'react-dom/client';
import { Player } from '@remotion/player';
import type { PlayerRef } from '@remotion/player';
import { ExplainerVideo } from '@stick/spec/render';
import { compile } from '@stick/spec/compile';
import spec from '@stick-demo/video1-presenter.spec.json';

const FPS = 30;
const DURATION = 1299; // the HOOK excerpt: frames 0-1298 of the video1 timing

const compiled = compile(spec as Parameters<typeof compile>[0]);

const PresenterComp: React.FC = () => (
  <ExplainerVideo compiled={compiled} transparent />
);

export interface PresenterAPI {
  setFrame: (f: number) => void;
}

const App: React.FC = () => {
  const playerRef = useRef<PlayerRef>(null);
  const lastFrame = useRef(-1);

  useEffect(() => {
    const api: PresenterAPI = {
      setFrame: (f: number) => {
        const clamped = Math.max(0, Math.min(DURATION - 1, Math.round(f)));
        if (clamped === lastFrame.current) return;
        lastFrame.current = clamped;
        playerRef.current?.seekTo(clamped);
      },
    };
    (window as unknown as { AisaacPresenter?: PresenterAPI }).AisaacPresenter = api;
    window.dispatchEvent(new Event('aisaac:presenter-ready'));
  }, []);

  return (
    <Player
      ref={playerRef}
      component={PresenterComp}
      durationInFrames={DURATION}
      fps={FPS}
      compositionWidth={1920}
      compositionHeight={1080}
      controls={false}
      clickToPlay={false}
      doubleClickToFullscreen={false}
      spaceKeyToPlayOrPause={false}
      style={{ width: '100%', height: '100%' }}
    />
  );
};

const rootEl = document.getElementById('presenter-root');
if (rootEl) createRoot(rootEl).render(<App />);
