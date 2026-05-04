---
name: video-assembly
description: 'WHAT: FFmpeg video assembly pipeline combining Remotion segments with
  TTS audio

  WHEN: Assembling final explainer videos from rendered segments and voiceover audio'
---

# Video Assembly

Assemble video from Remotion segments + audio using FFmpeg.

## Pipeline

```
1. Remotion renders visual segments → MP4 files
2. TTS generates audio → MP3 + timing.json (use tts-audio-gen skill)
3. FFmpeg stitches segments + overlays audio
```

## Commands

### Render Remotion composition
```bash
cd /tmp/remotion-test && npx remotion render src/index.ts CompositionName --output output.mp4
```

### Stitch multiple segments
```bash
ffmpeg -i intro.mp4 -i demo.mp4 -i outro.mp4 \
  -filter_complex '[0:v][1:v][2:v]concat=n=3:v=1:a=0[outv]' \
  -map '[outv]' final.mp4
```

### Add voiceover to video
```bash
ffmpeg -i final.mp4 -i voiceover.mp3 -c:v copy -c:a aac output_with_audio.mp4
```

### Replace placeholder segment
```bash
# Split at timestamp, insert replacement, rejoin
ffmpeg -i main.mp4 -t 30 -c copy part1.mp4
ffmpeg -i main.mp4 -ss 45 -c copy part2.mp4
ffmpeg -i part1.mp4 -i replacement.mp4 -i part2.mp4 \
  -filter_complex '[0:v][1:v][2:v]concat=n=3:v=1:a=0[outv]' \
  -map '[outv]' final.mp4
```

## Remotion Composition Types

- **DiagramExplainer** — Animated flowcharts (use Excalidraw PNGs as source)
- **InsightCard** — Key quotes/concepts with animation
- **SectionHeader** — Act/scene transitions
- **DemoPlaceholder** — Blank segments to replace with OBS captures

## Audio Sync

Use timing.json from tts-audio-gen to set exact frame durations:
```tsx
<Series>
  <Series.Sequence durationInFrames={timing[0].frames}>
    <Scene1 />
    <Audio src={staticFile('audio/scene1.mp3')} />
  </Series.Sequence>
</Series>
```

## File Structure
```
remotionproject/
  src/compositions/   # React components
  src/content/         # JSON content data
  audio/               # TTS MP3s + timing.json
  public/              # Static assets (images, audio for Remotion)
```
