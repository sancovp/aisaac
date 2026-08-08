#!/usr/bin/env bash
# Build the two lab bundles from the video_aios engine checkouts. Run from this
# directory. Neither engine nor its node_modules is vendored into this repo —
# the committed bundles are the artifacts; this script is how they were made.
#
# TWO bundles because the two engines need two Reacts:
#   explainer.bundle.js           studio/base + @remotion/player  (React 19)
#   explainer.presenter.bundle.js studio/stick + @remotion/player (React 18 —
#                                 @react-three/fiber 8 crashes under React 19)
# Each bundle carries its own React; two mount roots, no conflict.
set -euo pipefail

BASE="${ENGINE_BASE:-$HOME/video_aios/studio/base}"
STICK="${ENGINE_STICK:-$HOME/video_aios/studio/stick}"
ESBUILD="$BASE/node_modules/.bin/esbuild"

# Backdrop. The composition's <Audio> stays real (PLAY mode narration); the
# page sets window.remotion_staticBase so the mp3 resolves relative to lab/.
NODE_PATH="$BASE/node_modules" "$ESBUILD" entry.tsx \
  --bundle --minify --format=iife --target=es2019 --jsx=automatic \
  --define:process.env.NODE_ENV='"production"' \
  --alias:@engine="$BASE/src/base" \
  --outfile=../explainer.bundle.js

# Presenter: everything resolves from the stick checkout (React 18 tree).
NODE_PATH="$STICK/node_modules" "$ESBUILD" presenter-entry.tsx \
  --bundle --minify --format=iife --target=es2019 --jsx=automatic \
  --define:process.env.NODE_ENV='"production"' \
  --alias:@stick="$STICK/src" \
  --alias:@stick-demo="$STICK/demo" \
  --outfile=../explainer.presenter.bundle.js

ls -la ../explainer.bundle.js ../explainer.presenter.bundle.js
gzip -k -9 -c ../explainer.bundle.js | wc -c
gzip -k -9 -c ../explainer.presenter.bundle.js | wc -c
