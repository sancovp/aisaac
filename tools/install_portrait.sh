#!/usr/bin/env bash
# install_portrait.sh — put Isaac's photo in the hero slot that isaac.html has
# been holding open since 2026-08-07 ("the page about him must have HIS PHOTO").
#
#   bash tools/install_portrait.sh ~/Downloads/isaac.jpg
#
# Does three things and nothing else:
#   1. centre-crops the source to 4:5 and writes assets/isaac-portrait.jpg
#      (960x1200 — .portrait-frame is aspect-ratio 4/5, so any other ratio
#      gets cropped by object-fit anyway; doing it here means the browser
#      downloads the pixels that actually get shown)
#   2. replaces the ISAAC-PHOTO comment block in isaac.html with the real
#      <figure>, width and height inline because style_qa G5 requires them
#   3. runs the gates
#
# Idempotent: re-run it with a different source to swap the photo.
# Uses sips, which ships with macOS. No dependencies.

set -euo pipefail
cd "$(dirname "$0")/.."

SRC="${1:-}"
if [ -z "$SRC" ] || [ ! -f "$SRC" ]; then
  echo "usage: bash tools/install_portrait.sh <path-to-photo>"
  echo "  e.g. bash tools/install_portrait.sh ~/Downloads/isaac.jpg"
  [ -n "$SRC" ] && echo "  (no file at: $SRC)"
  exit 1
fi

OUT="assets/isaac-portrait.jpg"
W=960; H=1200

mkdir -p assets
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
cp "$SRC" "$TMP/in"

# Scale so the SHORT edge covers the target, then centre-crop to exactly 4:5.
sips -s format jpeg "$TMP/in" --out "$TMP/a.jpg" >/dev/null
read -r SW SH < <(sips -g pixelWidth -g pixelHeight "$TMP/a.jpg" \
  | awk '/pixelWidth/{w=$2} /pixelHeight/{h=$2} END{print w, h}')
# cover: scale up whichever axis falls short of the 4:5 box
if [ "$((SW * H))" -gt "$((SH * W))" ]; then
  sips -Z "$H" --resampleHeightWidthMax "$H" "$TMP/a.jpg" --out "$TMP/b.jpg" >/dev/null || \
    sips --resampleHeight "$H" "$TMP/a.jpg" --out "$TMP/b.jpg" >/dev/null
else
  sips --resampleWidth "$W" "$TMP/a.jpg" --out "$TMP/b.jpg" >/dev/null
fi
sips -c "$H" "$W" "$TMP/b.jpg" --out "$OUT" >/dev/null   # -c is centre-crop: height width
echo "  wrote $OUT ($(sips -g pixelWidth -g pixelHeight "$OUT" | awk '/pixelWidth/{w=$2}/pixelHeight/{h=$2}END{print w"x"h}'), $(du -h "$OUT" | cut -f1))"

# Swap the placeholder comment for the real figure.
python3 - "$OUT" <<'PY'
import re, sys
out = sys.argv[1]
p = "isaac.html"
s = open(p, encoding="utf8").read()
fig = (
'      <figure class="portrait">\n'
'        <div class="portrait-frame">\n'
f'          <img src="{out}" alt="Isaac" width="960" height="1200">\n'
'        </div>\n'
'        <figcaption>Isaac &middot; sancovp</figcaption>\n'
'      </figure>\n'
)
placeholder = re.compile(r'[ \t]*<!-- ISAAC-PHOTO:.*?-->\n', re.S)
existing = re.compile(r'[ \t]*<figure class="portrait">.*?</figure>\n', re.S)
if placeholder.search(s):
    s = placeholder.sub(fig, s, count=1); print("  isaac.html: placeholder -> <figure>")
elif existing.search(s):
    s = existing.sub(fig, s, count=1); print("  isaac.html: portrait refreshed")
else:
    print("  !! neither the ISAAC-PHOTO comment nor an existing <figure> was found."); sys.exit(1)
open(p, "w", encoding="utf8").write(s)
PY

echo
echo "── gates ──"
python3 tools/style_qa.py | tail -3
