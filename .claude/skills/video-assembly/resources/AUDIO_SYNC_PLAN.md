# Audio-Synced Video Production Plan

## TTS Audio Generated
All voiceover audio files are in `/tmp/remotion-test/audio/`

## Exact Frame Durations (from TTS)
| Scene | Seconds | Frames |
|-------|---------|--------|
| scene1 | 34.15 | 1024 |
| scene2 | 40.85 | 1225 |
| scene3 | 65.30 | 1959 |
| scene4 | 61.56 | 1846 |
| scene5 | 47.81 | 1434 |
| scene6 | 51.38 | 1541 |
| scene7 | 32.18 | 965 |
| scene8 | 41.98 | 1259 |
| scene9 | 35.26 | 1057 |
| scene10 | 33.55 | 1006 |
| scene11 | 55.18 | 1655 |
| scene12 | 30.31 | 909 |
| scene13 | 31.37 | 941 |
| scene14 | 34.73 | 1041 |
| scene15 | 40.54 | 1216 |
| scene16 | 41.35 | 1240 |
| endcard | 7.01 | 210 |
| **TOTAL** | **684.50** | **20535** |

## Additional Frames
- 5 ACT cards × 150 frames = 750
- ~22 transitions × 45 frames = 990
- **Grand Total: ~22275 frames = 12.4 minutes**

## TODO
1. Update ACExplainerV6.tsx TransitionSeries to use EXACT frame counts above
2. Each scene durationInFrames should match the audio duration
3. Add audio files to Remotion composition using `<Audio src={staticFile('audio/scene1.mp3')} />`
4. Copy audio files to public/ folder for Remotion

## Script Location
`/tmp/remotion-test/scripts/AC_Complete_System_Script_v2.md`

## Audio Files
`/tmp/remotion-test/audio/scene*.mp3`
