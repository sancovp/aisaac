---
name: tts-audio-gen
description: 'WHAT: TTS audio generation with frame-accurate timing for video sync

  WHEN: Creating voiceover audio for explainer videos, tutorials, or any video content
  that needs narration'
---

# Tts Audio Gen

Generate TTS audio from script text files using edge-tts, with sentence-by-sentence timing data for frame-accurate video sync.

## Usage

```bash
python3 /tmp/heaven_data/skills/tts-audio-gen/scripts/generate_tts.py <scene_name> [--input-dir path] [--output-dir path] [--voice en-US-GuyNeural]
```

## What It Does

1. Reads script text file (one sentence per line)
2. Generates TTS MP3 per sentence via edge-tts
3. Measures exact duration via mutagen
4. Creates timing.json with frame-accurate start/end per sentence (30fps)
5. Concatenates all sentence MP3s into full scene audio via ffmpeg

## Output Structure

```
output_dir/
  scene1_hj/
    s01.mp3, s01.txt
    s02.mp3, s02.txt
    timing.json    # [{index, sentence, duration_sec, frames, start_frame, file}]
    files.txt      # ffmpeg concat list
  scene1_hj.mp3    # full concatenated audio
```

## Dependencies

```bash
pip install edge-tts mutagen
# ffmpeg must be installed
```

## Available Voices

- en-US-GuyNeural (default, male)
- en-US-JennyNeural (female)
- en-US-AriaNeural (female, expressive)

## For ElevenLabs (higher quality)

Replace edge-tts call with:
```python
from elevenlabs import generate, save
audio = generate(text=sentence, voice='Adam', model='eleven_turbo_v2_5')
save(audio, str(output_path))
```

API key in /home/GOD/system_config.sh as ELEVENLABS_API_KEY (if set).
