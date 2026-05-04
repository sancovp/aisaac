---
name: moviola-sweatloupe
description: "WHAT: Automated video QC \u2014 render frames via Playwright, review\
  \ screenshots for errors, fix and re-render until clean\nWHEN: After writing a Remotion\
  \ composition, before publishing video content"
---

# Moviola Sweatloupe

Automated video QC pipeline: render Remotion compositions via Playwright, screenshot at configurable frame intervals, review screenshots for errors, fix, re-render until clean.

## The Loop

```
1. Render: Playwright opens Remotion preview, navigates to frame N
2. Screenshot: capture frame as PNG at interval (every 30 frames = 1/sec default)
3. Review: second agent reads all PNGs sequentially, checks for:
   - Text readability and overlap
   - Missing assets (blank frames, broken images)
   - Layout issues (elements off-screen, overlapping)
   - Timing problems (wrong content at wrong frame)
   - Visual quality (artifacts, rendering glitches)
4. Error list: [{frame: N, error: 'description'}]
5. Fix: edit Remotion composition code to resolve errors
6. Re-render affected frames only
7. Re-review until error list is empty
```

## Usage

```bash
# Render all frames at 1fps granularity
python3 /tmp/heaven_data/skills/moviola-sweatloupe/scripts/render_frames.py --composition MyComp --interval 30 --output-dir /tmp/sweatloupe_frames/

# Review frames (launches reviewer agent)
# Reviewer reads each PNG and returns error JSON
```

## Remotion Preview URL

Remotion dev server runs at localhost:3000. Playwright navigates to:
```
http://localhost:3000/preview?composition=MyComp&frame=N
```

Screenshot the preview viewport at each frame interval.

## Frame Granularity

- Structure review: scene transitions only (every 150-300 frames)
- Rough cut: every 30 frames (1 screenshot per second)
- Fine QC: every 5 frames
- Pixel-perfect: every frame (slow, use for final pass only)

## Two-Agent Pattern

- Agent 1 (editor): writes Remotion code, renders, screenshots
- Agent 2 (reviewer): reads screenshots, returns error list
- Agent 1 fixes, re-renders, re-sends
- Loop until Agent 2 returns zero errors

The Moviola is the render+scrub. The Sweatloupe is the magnified review.
