#!/usr/bin/env python3
"""Generate sentence-by-sentence TTS for Hero's Journey script"""
import subprocess
import json
import re
import sys
from pathlib import Path
from mutagen.mp3 import MP3

VOICE = "en-US-GuyNeural"
FPS = 30

def split_sentences(text: str) -> list[str]:
    """Split text into sentences on newlines (each line is a sentence)."""
    return [s.strip() for s in text.strip().split('\n') if s.strip()]

def generate_tts(sentence: str, output_path: Path) -> float:
    """Generate TTS for a sentence, return duration in seconds."""
    temp_txt = output_path.with_suffix('.txt')
    temp_txt.write_text(sentence)

    subprocess.run([
        'edge-tts', '--voice', VOICE,
        '--file', str(temp_txt),
        '--write-media', str(output_path)
    ], check=True, capture_output=True)

    audio = MP3(output_path)
    return audio.info.length

def process_scene(scene_name: str, input_dir: Path, output_base: Path):
    """Process a scene: split sentences, generate TTS, output timing JSON."""
    input_file = input_dir / f"{scene_name}.txt"
    output_dir = output_base / f"{scene_name}_hj"
    output_dir.mkdir(exist_ok=True)

    text = input_file.read_text()
    sentences = split_sentences(text)

    timings = []
    cumulative_frames = 0

    for i, sentence in enumerate(sentences, 1):
        mp3_path = output_dir / f"s{i:02d}.mp3"
        print(f"  [{i}/{len(sentences)}] {sentence[:60]}...")

        duration = generate_tts(sentence, mp3_path)
        frames = int(duration * FPS)

        timings.append({
            "index": i,
            "sentence": sentence,
            "duration_sec": round(duration, 3),
            "frames": frames,
            "start_frame": cumulative_frames,
            "file": mp3_path.name
        })
        cumulative_frames += frames

    # Save timing JSON
    timing_file = output_dir / "timing.json"
    timing_file.write_text(json.dumps(timings, indent=2))

    # Concatenate all into full scene audio
    list_file = output_dir / "files.txt"
    list_file.write_text("\n".join(f"file '{t['file']}'" for t in timings))

    full_mp3 = output_base / f"{scene_name}_hj.mp3"
    subprocess.run([
        'ffmpeg', '-y', '-f', 'concat', '-safe', '0',
        '-i', str(list_file), '-c', 'copy', str(full_mp3)
    ], check=True, capture_output=True)

    print(f"  Total: {cumulative_frames} frames ({cumulative_frames/FPS:.2f}s)")
    print(f"  Saved: {timing_file}")

    return timings

if __name__ == "__main__":
    # Default: generate scenes 1 and 6 (need fresh TTS)
    scenes = sys.argv[1:] if len(sys.argv) > 1 else ["scene1", "scene6"]

    input_dir = Path("/tmp/remotion-test/audio/hj_script")
    output_base = Path("/tmp/remotion-test/audio")

    for scene_name in scenes:
        print(f"\n=== {scene_name} ===")
        process_scene(scene_name, input_dir, output_base)
