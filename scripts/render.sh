#!/bin/bash
# Render Manim project to final MP4 with audio
# Usage: render.sh <project-dir> [--output <path>] [-ql|-qm|-qh|-qk]
set -euo pipefail

DIR="${1:?Usage: render.sh <project-dir> [--output path] [-ql|-qm|-qh|-qk]}"
OUTPUT=""
QUALITY="-qh"
shift

while [ $# -gt 0 ]; do
  case "$1" in
    --output) OUTPUT="${2:?--output requires a path}"; shift ;;
    -ql|-qm|-qh|-qk) QUALITY="$1" ;;
  esac
  shift
done

MAIN_PY=$(find "$DIR" -maxdepth 1 -name "*.py" ! -name "__init__.py" | head -1)
if [ -z "$MAIN_PY" ]; then echo "[ERROR] No .py in $DIR"; exit 1; fi

SCENE_CLASS=$(grep -oP 'class \w+\(Scene\)' "$MAIN_PY" | head -1 | sed 's/class //;s/(Scene)//')
if [ -z "$SCENE_CLASS" ]; then echo "[ERROR] No Scene class in $MAIN_PY"; exit 1; fi

echo "[RENDER] $MAIN_PY :: $SCENE_CLASS (quality $QUALITY)"

[ -f /tmp/manim-env/bin/activate ] && source /tmp/manim-env/bin/activate

cd "$DIR"
manim render $QUALITY --disable_caching -a -o raw "$MAIN_PY" "$SCENE_CLASS" 2>&1 | tail -5

# Find rendered video
RAW_MP4=""
for qdir in "480p15" "720p30" "1080p60" "2160p60"; do
  [ -f "$DIR/output/$qdir/raw.mp4" ] && RAW_MP4="$DIR/output/$qdir/raw.mp4" && break
done
if [ -z "$RAW_MP4" ]; then
  RAW_MP4=$(find "$DIR/media" -name "*.mp4" -not -path "*/partial*" | head -1)
fi
if [ -z "$RAW_MP4" ]; then echo "[ERROR] No rendered MP4"; exit 1; fi

echo "[OK] Raw: $RAW_MP4"

# Merge audio
if [ -d "$DIR/audio" ] && [ "$(ls "$DIR/audio"/scene*.mp3 2>/dev/null | wc -l)" -gt 0 ]; then
  CL=$(mktemp)
  for f in $(ls "$DIR/audio/scene"*.mp3 | sort -V); do echo "file '$f'"; done > "$CL"

  MA=$(mktemp /tmp/manim-merge-XXXXX.mp3)
  ffmpeg -y -f concat -safe 0 -i "$CL" -c copy "$MA" 2>/dev/null

  [ -z "$OUTPUT" ] && OUTPUT="$DIR/output/final.mp4"

  ffmpeg -y -i "$RAW_MP4" -i "$MA" \
    -c:v copy -c:a aac -b:a 128k -shortest -movflags +faststart \
    "$OUTPUT" 2>&1 | tail -2

  rm -f "$CL" "$MA"
  echo "[OK] $OUTPUT"
  ls -lh "$OUTPUT"
else
  echo "[OK] Raw video (no audio): $RAW_MP4"
fi
