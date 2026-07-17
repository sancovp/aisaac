/**
 * Build-time shim aliased over 'remotion' in the BACKDROP bundle only.
 *
 * The engine's SegmentView unconditionally mounts <Audio src={staticFile(seg.audio)}>
 * for the segment's TTS track. The scroll-scrubbed lab page has no timeline
 * playback and ships no media files, so Audio is stubbed to render nothing.
 * Everything else re-exports from the real remotion module (single instance —
 * @remotion/player resolves through this same alias, so contexts stay shared).
 */
export * from 'remotion-original';

export const Audio: React.FC<Record<string, unknown>> = () => null;

import type React from 'react';
