---
name: remotion-video-production
description: "WHAT: Remotion video production system \u2014 React-based programmatic\
  \ video creation with audio sync\nWHEN: Building explainer videos, tutorials, or\
  \ any programmatic video content"
---

# Remotion Video Production

Remotion is a React framework for programmatic video creation. Videos are React components rendered frame-by-frame.

## Core Concepts

- **Composition** — A registered video with fixed dimensions, FPS, and duration
- **Sequence** — Time-offset child components within a composition
- **Series** — Sequential scenes with TransitionSeries for transitions
- **useCurrentFrame()** — Hook returning current frame number for animation
- **interpolate()** — Map frame ranges to value ranges (opacity, position, scale)
- **spring()** — Physics-based easing for natural motion
- **staticFile()** — Reference files in public/ directory

## Project Location

`/tmp/remotion-test/` — Full project with node_modules, 16 scenes of audio, shot lists

## Key Files

- `src/Composition.tsx` — Main composition (currently empty, build here)
- `audio/` — Generated TTS MP3s + timing.json per scene
- `AUDIO_SYNC_PLAN.md` — Frame-accurate duration mapping for all scenes
- `VIDEO_PIPELINE.md` — Assembly workflow (Remotion + OBS + FFmpeg)
- `SHOT_LIST.md` — Shot-by-shot breakdown
- `SCRIPT_HJ.md` — Full Hero's Journey script
- `.claude/skills/remotion-best-practices/` — 30+ rule files for Remotion patterns

## Composition Types for Explainer Videos

1. **DiagramExplainer** — Animated flowcharts using Excalidraw PNGs (use excalidraw-render skill)
2. **InsightCard** — Key quotes/terms/concepts with text animation
3. **SectionHeader** — Act/scene transitions with title cards
4. **DemoPlaceholder** — Blank segments to swap with screen recordings

## Audio-Synced Pattern

```tsx
import { Audio, Series, useCurrentFrame, interpolate, staticFile } from 'remotion';
import timing from '../audio/scene1_hj/timing.json';

const Scene1: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Series>
      {timing.map((t, i) => (
        <Series.Sequence key={i} durationInFrames={t.frames}>
          <div style={{opacity: interpolate(frame, [0, 15], [0, 1])}}>
            {t.sentence}
          </div>
          <Audio src={staticFile(`audio/scene1_hj/${t.file}`)} />
        </Series.Sequence>
      ))}
    </Series>
  );
};
```

## Related Skills

- **tts-audio-gen** — Generate TTS audio with frame-accurate timing
- **video-assembly** — FFmpeg stitching + audio overlay
- **excalidraw-render** — Render diagrams for DiagramExplainer scenes
- **remotion-best-practices** — Detailed rule files at /tmp/remotion-test/.claude/skills/remotion-best-practices/
