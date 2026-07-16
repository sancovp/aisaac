/**
 * aisaac explainer lab — web-native player entry.
 *
 * Bundles the LIVE diagram engine (video_aios studio/base, Remotion + React 19)
 * with @remotion/player into one static IIFE. The ink-stickman presenter is a
 * pre-rendered alpha-VP9 webm (studio/stick output, frames 0-1298 of the
 * video1-sevenlevels presenter pass) overlaid on the player and slaved to the
 * player clock. Both passes were compiled from the same shot list, so frame N
 * of the webm IS frame N of the composition — sync is drift-corrected, not
 * interpreted.
 *
 * Build: ./build.sh (imports resolve against the engine checkout via NODE_PATH
 * and the @engine alias — see build.sh). The committed artifact is
 * ../explainer.bundle.js; this file is provenance.
 */
import React, { useEffect, useMemo, useRef, useState } from 'react';
import { createRoot } from 'react-dom/client';
import { Player } from '@remotion/player';
import type { PlayerRef } from '@remotion/player';
import { VideoFromShotList, totalFrames } from '@engine/VideoFromShotList';
import { sevenLevelsShotList } from '@engine/video1-sevenlevels';
import type { ShotList } from '@engine/types';

const FPS = 30;

// The excerpt = the HOOK segment of VIDEO 1 (7 sentences, frames 0-1298).
// Taking the whole first segment keeps the segment's TTS mp3 and the
// pre-rendered presenter webm frame-aligned with the live composition.
const excerpt: ShotList = {
  ...sevenLevelsShotList,
  segments: [sevenLevelsShotList.segments[0]],
};
const DURATION = totalFrames(excerpt);

const GOLD = '#e8b437';
const MINT = '#4fd1a5';
const INK_DIM = '#8b93a7';
const PANEL = '#0f1520';

const fmt = (f: number) => {
  const s = Math.floor(f / FPS);
  return `${Math.floor(s / 60)}:${String(s % 60).padStart(2, '0')}`;
};

const vp9Supported = () => {
  if (typeof document === 'undefined') return false;
  const v = document.createElement('video');
  return v.canPlayType('video/webm; codecs="vp9"') !== '';
};

const App: React.FC = () => {
  const playerRef = useRef<PlayerRef>(null);
  const videoRef = useRef<HTMLVideoElement>(null);
  const [playing, setPlaying] = useState(false);
  const [muted, setMuted] = useState(false);
  const alphaOk = useMemo(vp9Supported, []);

  const initialFrame = useMemo(() => {
    const f = Number(new URLSearchParams(location.search).get('f'));
    return Number.isFinite(f) && f > 0 ? Math.min(f, DURATION - 1) : 0;
  }, []);
  const [frame, setFrame] = useState(initialFrame);

  // Wire the presenter <video> to the player clock. The player is the master:
  // on every frame update the overlay is drift-corrected against frame/FPS.
  useEffect(() => {
    const p = playerRef.current;
    const v = videoRef.current;
    if (!p) return;
    const onFrame = (e: { detail: { frame: number } }) => {
      setFrame(e.detail.frame);
      if (v) {
        const t = e.detail.frame / FPS;
        if (Math.abs(v.currentTime - t) > 0.15) v.currentTime = t;
      }
    };
    const onPlay = () => {
      setPlaying(true);
      v?.play().catch(() => {});
    };
    const onPause = () => {
      setPlaying(false);
      v?.pause();
    };
    p.addEventListener('frameupdate', onFrame as never);
    p.addEventListener('play', onPlay);
    p.addEventListener('pause', onPause);
    if (v && initialFrame) v.currentTime = initialFrame / FPS;
    return () => {
      p.removeEventListener('frameupdate', onFrame as never);
      p.removeEventListener('play', onPlay);
      p.removeEventListener('pause', onPause);
    };
  }, [initialFrame]);

  const toggle = () => {
    const p = playerRef.current;
    if (!p) return;
    if (p.isPlaying()) p.pause();
    else p.play();
  };

  const seek = (f: number) => {
    playerRef.current?.seekTo(f);
    const v = videoRef.current;
    if (v) v.currentTime = f / FPS;
  };

  const beats = excerpt.segments[0].beats;
  const activeBeat = beats.findIndex(
    (b) => frame >= b.startFrame && frame < b.startFrame + b.frames,
  );

  return (
    <div>
      <div
        style={{
          position: 'relative',
          aspectRatio: '16 / 9',
          background: '#000',
          borderRadius: 10,
          overflow: 'hidden',
          border: '1px solid rgba(255,255,255,0.08)',
        }}
      >
        <Player
          ref={playerRef}
          component={VideoFromShotList as React.FC<{ shotList: ShotList }>}
          inputProps={{ shotList: excerpt }}
          durationInFrames={DURATION}
          fps={FPS}
          compositionWidth={1920}
          compositionHeight={1080}
          initialFrame={initialFrame}
          loop
          clickToPlay
          controls={false}
          style={{ width: '100%', height: '100%' }}
        />
        {alphaOk && (
          <video
            ref={videoRef}
            src="presenter-seg1.webm"
            muted
            playsInline
            preload="auto"
            style={{
              position: 'absolute',
              inset: 0,
              width: '100%',
              height: '100%',
              pointerEvents: 'none',
            }}
          />
        )}
      </div>

      {!alphaOk && (
        <p style={{ color: INK_DIM, fontSize: 13, marginTop: 8 }}>
          The ink-presenter overlay needs a browser that plays VP9-alpha webm
          (Chrome, Edge, Firefox). The diagram player below it still runs.
        </p>
      )}

      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: 12,
          marginTop: 14,
        }}
      >
        <button className="lab-btn" onClick={toggle}>
          {playing ? 'Pause' : 'Play'}
        </button>
        <button className="lab-btn" onClick={() => seek(0)}>
          Restart
        </button>
        <input
          type="range"
          min={0}
          max={DURATION - 1}
          value={frame}
          onChange={(e) => seek(Number(e.target.value))}
          style={{ flex: 1, accentColor: GOLD }}
          aria-label="timeline"
        />
        <span style={{ color: INK_DIM, fontVariantNumeric: 'tabular-nums', fontSize: 14 }}>
          {fmt(frame)} / {fmt(DURATION)}
        </span>
        <button
          className="lab-btn"
          onClick={() => {
            const p = playerRef.current;
            if (!p) return;
            if (p.isMuted()) {
              p.unmute();
              setMuted(false);
            } else {
              p.mute();
              setMuted(true);
            }
          }}
        >
          {muted ? 'Unmute' : 'Mute'}
        </button>
      </div>

      <ol style={{ listStyle: 'none', padding: 0, margin: '26px 0 0' }}>
        {beats.map((b, i) => (
          <li
            key={i}
            onClick={() => seek(b.startFrame)}
            style={{
              padding: '10px 14px',
              marginBottom: 6,
              borderRadius: 8,
              cursor: 'pointer',
              background: i === activeBeat ? PANEL : 'transparent',
              borderLeft: `3px solid ${i === activeBeat ? GOLD : 'rgba(255,255,255,0.08)'}`,
              transition: 'background 120ms, border-color 120ms',
            }}
          >
            {b.eyebrow && (
              <span
                style={{
                  color: i === activeBeat ? GOLD : INK_DIM,
                  fontWeight: 800,
                  fontSize: 11,
                  letterSpacing: 2,
                  textTransform: 'uppercase',
                  marginRight: 10,
                }}
              >
                {b.eyebrow}
              </span>
            )}
            <span
              style={{
                color: i === activeBeat ? '#f4f6fb' : INK_DIM,
                fontSize: 15,
                lineHeight: 1.5,
              }}
            >
              {b.line}
            </span>
            {i === activeBeat && (
              <span style={{ color: MINT, fontSize: 12, marginLeft: 10 }}>●</span>
            )}
          </li>
        ))}
      </ol>
    </div>
  );
};

const rootEl = document.getElementById('explainer-root');
if (rootEl) createRoot(rootEl).render(<App />);
