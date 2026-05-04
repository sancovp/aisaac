# Video Production Pipeline

## Overview

Modular video production system combining programmatic rendering with live capture.

## Components

### 1. Remotion (Scripted Visuals)
- **DiagramExplainer** - Animated flowcharts (AC loop, SOSEEH structure)
- **InsightCard** - Key quotes, terms, concepts with animation
- **SectionHeader** - Transitions between video parts
- **DemoPlaceholder** - Blank segments to swap with OBS captures

### 2. OBS (Live Capture)
- Live demos of Claude using frameworks
- Screen recordings
- Voiceover via OBS voiceover system

### 3. FFmpeg (Assembly)
- Stitch Remotion segments + OBS demos
- Replace placeholder sections with actual content
- Final render with audio

## Workflow

```
1. Write Remotion composition for visual segments
2. Render to video files
3. Capture OBS demos separately
4. Record voiceover
5. FFmpeg assembly: stitch all pieces
6. Export final video
```

## Content Types

### Framework Explainer Video
```
[SectionHeader: "The Allegorization Compiler"]
[DiagramExplainer: AC flowchart animating step by step]
[InsightCard: "Heat triggers reach"]
[DemoPlaceholder → OBS: Live demo of catching a reach]
[InsightCard: "Stack 3+ analogies from different domains"]
[DiagramExplainer: Domain variance visualization]
[SectionHeader: "Try it yourself"]
```

### Quick Tutorial (30-60 sec)
```
[SectionHeader: "SOSEEH in 30 seconds"]
[DiagramExplainer: Pilot/Vehicle/MissionControl/Loops]
[InsightCard: "Fill the blanks. Weird blanks = bugs."]
```

### Insight Clip (Social)
```
[InsightCard: Single key insight, full screen, animated]
```

## File Structure

```
src/
├── compositions/
│   ├── DiagramExplainer.tsx
│   ├── InsightCard.tsx
│   ├── SectionHeader.tsx
│   └── DemoPlaceholder.tsx
├── content/
│   ├── ac-explainer.json      # Content for AC video
│   ├── soseeh-tutorial.json   # Content for SOSEEH video
│   └── reach-explainer.json   # Content for REACH video
└── Root.tsx                   # Register all compositions
```

## Assembly Script (FFmpeg)

```bash
# Example: Stitch intro + demo + outro
ffmpeg -i intro.mp4 -i demo.mp4 -i outro.mp4 \
  -filter_complex "[0:v][1:v][2:v]concat=n=3:v=1:a=0[outv]" \
  -map "[outv]" final.mp4

# Add voiceover
ffmpeg -i final.mp4 -i voiceover.mp3 \
  -c:v copy -c:a aac output_with_audio.mp4
```
