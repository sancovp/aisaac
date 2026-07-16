#!/usr/bin/env bash
# Build lab/explainer.bundle.js from entry.tsx against the video_aios diagram
# engine checkout. Run from this directory. The engine and its node_modules
# (Remotion 4.0.409, React 19.2.3, @remotion/player) are NOT vendored into this
# repo — the committed bundle is the artifact; this script is how it was made.
set -euo pipefail

ENGINE_BASE="${ENGINE_BASE:-$HOME/video_aios/studio/base}"
ESBUILD="$ENGINE_BASE/node_modules/.bin/esbuild"

NODE_PATH="$ENGINE_BASE/node_modules" "$ESBUILD" entry.tsx \
  --bundle \
  --minify \
  --format=iife \
  --target=es2019 \
  --jsx=automatic \
  --define:process.env.NODE_ENV='"production"' \
  --alias:@engine="$ENGINE_BASE/src/base" \
  --outfile=../explainer.bundle.js

ls -la ../explainer.bundle.js
