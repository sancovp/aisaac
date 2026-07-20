/**
 * aisaac explainer lab — BACKDROP bundle (React 19).
 *
 * Mounts the LIVE diagram engine (video_aios studio/base: VideoFromShotList,
 * the Visual menu, the real layout math) in @remotion/player — no rendered
 * video anywhere. The player never plays; the page's scroll driver (scrub.js)
 * owns the clock and drives frames through window.AisaacBackdrop.setFrame().
 *
 * The excerpt is the HOOK segment of the video1-sevenlevels shot list
 * (7 sentences, frames 0-1298 @30fps). Beat LINES are blanked in the copy
 * passed to the composition — on this page the captions are real DOM text in
 * the scroll sections (one authored source, three surfaces: film, page, spec);
 * the real lines are exported on the API for scrub.js to render.
 *
 * PLAY mode support: the composition's own <Audio> stays real — the page sets
 * window.remotion_staticBase to its directory so the segment's narration mp3
 * (lab/audio/…) resolves under any deployment prefix. While scrubbing the
 * player is paused, so the audio never sounds; scrub.js's play toggle calls
 * play()/pause() here for normal timed playback with the voice.
 * Build: ./build.sh.
 */
import React, { useEffect, useRef } from 'react';
import { createRoot } from 'react-dom/client';
import { Player } from '@remotion/player';
import type { PlayerRef } from '@remotion/player';
import { VideoFromShotList, totalFrames } from '@engine/VideoFromShotList';
import { sevenLevelsShotList } from '@engine/video1-sevenlevels';
import type { ShotList, Beat } from '@engine/types';

const FPS = 30;

const hookSeg = sevenLevelsShotList.segments[0];

// The composition gets the beats with blank lines (DOM owns the captions);
// visuals, timing, spine all stay live.
const excerpt: ShotList = {
  ...sevenLevelsShotList,
  segments: [
    {
      ...hookSeg,
      beats: hookSeg.beats.map((b: Beat): Beat => ({ ...b, line: '', eyebrow: undefined })),
    },
  ],
};
const DURATION = totalFrames(excerpt);

export interface BackdropAPI {
  fps: number;
  duration: number;
  beats: { start: number; frames: number; line: string; eyebrow?: string }[];
  setFrame: (f: number) => void;
  play: () => void;
  pause: () => void;
  on: (event: 'frameupdate' | 'ended' | 'play' | 'pause', cb: (frame: number) => void) => void;
}

const App: React.FC = () => {
  const playerRef = useRef<PlayerRef>(null);
  const lastFrame = useRef(-1);

  useEffect(() => {
    const api: BackdropAPI = {
      fps: FPS,
      duration: DURATION,
      beats: hookSeg.beats.map((b: Beat) => ({
        start: b.startFrame,
        frames: b.frames,
        line: b.line,
        eyebrow: b.eyebrow,
      })),
      setFrame: (f: number) => {
        const clamped = Math.max(0, Math.min(DURATION - 1, Math.round(f)));
        if (clamped === lastFrame.current) return;
        lastFrame.current = clamped;
        playerRef.current?.seekTo(clamped);
      },
      play: () => playerRef.current?.play(),
      pause: () => playerRef.current?.pause(),
      on: (event, cb) => {
        const p = playerRef.current;
        if (!p) return;
        if (event === 'frameupdate') {
          p.addEventListener('frameupdate', ((e: { detail: { frame: number } }) => {
            lastFrame.current = e.detail.frame;
            cb(e.detail.frame);
          }) as never);
        } else {
          p.addEventListener(event, (() => cb(lastFrame.current)) as never);
        }
      },
    };
    (window as unknown as { AisaacBackdrop?: BackdropAPI }).AisaacBackdrop = api;
    window.dispatchEvent(new Event('aisaac:backdrop-ready'));
  }, []);

  return (
    <Player
      ref={playerRef}
      component={VideoFromShotList as React.FC<{ shotList: ShotList }>}
      inputProps={{ shotList: excerpt }}
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

const rootEl = document.getElementById('backdrop-root');
if (rootEl) createRoot(rootEl).render(<App />);
