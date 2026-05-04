#!/usr/bin/env python3
"""Render .excalidraw to PNG via Playwright + Excalidraw exportToSvg.

CRITICAL: Labels on shapes (label property) are NOT rendered by exportToSvg.
Convert all labels to standalone text elements BEFORE rendering.

Usage: python3 render.py input.excalidraw output.png [width] [height]
"""
import json, sys, time, http.server, threading
from pathlib import Path
from playwright.sync_api import sync_playwright

def convert_labels_to_text(data):
    """Convert shape label properties to standalone text elements."""
    new_elements = []
    for el in data["elements"]:
        new_elements.append(el)
        label = el.get("label")
        if label:
            text = label["text"]
            fs = label.get("fontSize", 16)
            color = label.get("strokeColor", "#1e1e1e")
            ff = label.get("fontFamily", 2)
            cx = el["x"] + el["width"] / 2
            cy = el["y"] + el["height"] / 2
            lines = text.split("\n")
            max_line = max(lines, key=len)
            est_w = len(max_line) * fs * 0.5
            est_h = len(lines) * (fs + 4)
            new_elements.append({
                "type": "text", "id": f"lbl_{el['id']}",
                "x": cx - est_w / 2, "y": cy - est_h / 2,
                "width": est_w, "height": est_h,
                "text": text, "fontSize": fs, "fontFamily": ff,
                "strokeColor": color, "textAlign": "center",
            })
            del el["label"]
    data["elements"] = new_elements
    return data

def render(excalidraw_path, output_path, width=1800, height=1200):
    render_dir = Path(__file__).parent
    data = json.loads(Path(excalidraw_path).read_text())
    data = convert_labels_to_text(data)
    
    class H(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **kw): super().__init__(*a, directory=str(render_dir), **kw)
        def log_message(self, *a): pass
    
    srv = http.server.HTTPServer(("127.0.0.1", 0), H)
    port = srv.server_address[1]
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": width, "height": height}, device_scale_factor=2)
        page.goto(f"http://127.0.0.1:{port}/render_local.html")
        page.wait_for_function("window.__moduleReady === true", timeout=60000)
        page.evaluate(f"window.renderDiagram({json.dumps(data)})")
        page.wait_for_function("window.__renderComplete === true", timeout=15000)
        svg = page.query_selector("#root svg")
        if svg:
            svg.screenshot(path=str(output_path))
            print(f"OK {output_path}")
        else:
            print("ERROR: No SVG element")
            sys.exit(1)
        browser.close()
    srv.shutdown()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: render.py input.excalidraw output.png [width] [height]")
        sys.exit(1)
    w = int(sys.argv[3]) if len(sys.argv) > 3 else 1800
    h = int(sys.argv[4]) if len(sys.argv) > 4 else 1200
    render(sys.argv[1], sys.argv[2], w, h)
