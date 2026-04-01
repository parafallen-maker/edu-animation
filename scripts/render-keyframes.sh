#!/bin/bash
# render-keyframes.sh — Render keyframe screenshots from Manim scenes
# Usage: bash render-keyframes.sh <project-dir> <scene_file.py> [--output-dir /tmp/keyframes]
set -euo pipefail

DIR="${1:?Usage: render-keyframes.sh <project-dir> <scene_file.py> [--output-dir path]}"
SCENE_FILE="${2:?Missing scene file}"
OUT_DIR="/tmp/keyframes"

if [ "${3:-}" = "--output-dir" ] && [ -n "${4:-}" ]; then
  OUT_DIR="$4"
fi

[ -f /tmp/manim-env/bin/activate ] && source /tmp/manim-env/bin/activate

SCENE_BASE=$(basename "$SCENE_FILE" .py)

# Extract all Scene class names
CLASSES=$(grep -E 'class \w+\(Scene\)' "$DIR/$SCENE_FILE" | sed 's/class //;s/(Scene).*//' | tr '\n' ' ')

if [ -z "$CLASSES" ]; then
  echo "[ERROR] No Scene classes found in $SCENE_FILE"
  exit 1
fi

mkdir -p "$OUT_DIR"
echo "[INFO] Rendering keyframes from: $SCENE_FILE"
echo "[INFO] Scenes: $CLASSES"
echo "[INFO] Output: $OUT_DIR"
echo ""

for cls in $CLASSES; do
  echo "[RENDER] $cls → ${OUT_DIR}/scene-${cls}-keyframe.png"
  cd "$DIR"
  manim render --format png -o keyframe "$SCENE_FILE" "$cls" 2>&1 | tail -3

  # Find the rendered PNG
  PNG=$(find "$DIR/media" -name "${cls}.png" 2>/dev/null | head -1)
  if [ -z "$PNG" ]; then
    PNG=$(find "$DIR" -name "keyframe.png" 2>/dev/null | head -1)
  fi

  if [ -n "$PNG" ] && [ -f "$PNG" ]; then
    cp "$PNG" "${OUT_DIR}/scene-${cls}-keyframe.png"
    echo "[OK] ${OUT_DIR}/scene-${cls}-keyframe.png"
  else
    echo "[WARN] Could not find rendered PNG for $cls"
  fi
  echo ""
done

echo "---"
echo "[DONE] Keyframes saved to $OUT_DIR"
ls -lh "$OUT_DIR"/*.png 2>/dev/null || echo "[WARN] No PNG files found"
