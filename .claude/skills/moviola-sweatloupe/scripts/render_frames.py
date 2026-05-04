#!/usr/bin/env python3
"""Moviola Sweatloupe — render Remotion frames via Playwright for review.

Usage:
    python3 render_frames.py --port 3000 --composition MyComp --start 0 --end 900 --interval 30 --output-dir /tmp/sweatloupe_frames/
"""
import argparse, json, sys
from pathlib import Path

def render_frames(port=3000, composition="MyComposition", start_frame=0, end_frame=900, interval=30, output_dir="/tmp/sweatloupe_frames/", width=1920, height=1080):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("ERROR: pip install playwright && playwright install chromium", file=sys.stderr); sys.exit(1)
    out = Path(output_dir); out.mkdir(parents=True, exist_ok=True)
    frames = list(range(start_frame, end_frame + 1, interval))
    print(f"Capturing {len(frames)} frames (interval={interval}) to {output_dir}")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": width, "height": height}, device_scale_factor=2)
        for i, frame in enumerate(frames):
            page.goto(f"http://localhost:{port}/preview?composition={composition}&frame={frame}", wait_until="networkidle")
            page.wait_for_timeout(500)
            fn = f"frame_{frame:06d}.png"; page.screenshot(path=str(out / fn))
            print(f"  [{i+1}/{len(frames)}] frame {frame} -> {fn}")
        browser.close()
    manifest = {"composition": composition, "start_frame": start_frame, "end_frame": end_frame, "interval": interval, "total_frames": len(frames), "frames": [f"frame_{f:06d}.png" for f in frames]}
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2))
    print(f"Done. {len(frames)} frames. Manifest: {out / 'manifest.json'}")

if __name__ == "__main__":
    pa = argparse.ArgumentParser(description="Moviola Sweatloupe")
    pa.add_argument("--port", type=int, default=3000); pa.add_argument("--composition", default="MyComposition")
    pa.add_argument("--start", type=int, default=0); pa.add_argument("--end", type=int, default=900)
    pa.add_argument("--interval", type=int, default=30); pa.add_argument("--output-dir", default="/tmp/sweatloupe_frames/")
    pa.add_argument("--width", type=int, default=1920); pa.add_argument("--height", type=int, default=1080)
    a = pa.parse_args()
    render_frames(a.port, a.composition, a.start, a.end, a.interval, a.output_dir, a.width, a.height)
