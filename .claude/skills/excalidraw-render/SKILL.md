---
name: excalidraw-render
description: "WHAT: Render Excalidraw JSON diagrams to PNG via Playwright + headless Chromium\nWHEN: Creating diagrams for blog posts, documentation, or any visual content"
category: single_turn_process
---

# Excalidraw Render Pipeline

Renders `.excalidraw` JSON files to PNG images using Playwright + headless Chromium + jsdelivr CDN.

## Critical Rules

1. **Labels MUST be standalone text elements.** The `label` property on shapes is NOT rendered by `exportToSvg`. Convert every shape label to a separate `text` element positioned at the shape's center.

2. **Use jsdelivr CDN only.** esm.sh does NOT work in headless Chromium (module loading times out).

3. **Screenshot the SVG element**, not the full page, for clean output without extra whitespace.

## Usage

```bash
python3 /tmp/heaven_data/skills/excalidraw-render/scripts/render_excalidraw.py input.excalidraw --output output.png
```

## Setup (first time only)

```bash
pip install playwright && playwright install chromium
```

## Creating Diagrams

When designing Excalidraw JSON:

1. Create shapes (rectangle, ellipse, diamond) with colors and styles
2. For EVERY label, create a SEPARATE text element at the shape's center coordinates:
   ```json
   {"type": "text", "x": shape_x + shape_width/2, "y": shape_y + shape_height/2,
    "text": "Label Text", "textAlign": "center", "verticalAlign": "middle",
    "fontSize": 20, "fontFamily": 1}
   ```
3. Use arrows with `startBinding`/`endBinding` to connect shapes
4. Group related elements with colored backgrounds (use `backgroundColor` on rectangles)
5. Set `"type": "excalidraw"` at the top level of the JSON

## Color Palette (Excalidraw)

- Blue: `#1e90ff` (stroke), `#1864ab` (fill)
- Green: `#2f9e44` (stroke/fill)
- Orange: `#e8a120` (stroke), `#f08c00` (fill)
- Red: `#e03131` (stroke/fill)
- Purple: `#7950f2` (stroke/fill)
- Teal: `#0c8599` (stroke/fill)
- Background: `#ffffff` (light) or `#1e1e2e` (dark)

## Files

- `scripts/render_excalidraw.py` — Main render script (Playwright + Chromium)
- `scripts/render_local.html` — HTML template with jsdelivr CDN exportToSvg
