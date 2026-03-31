#!/bin/bash
# Render Motion Canvas project to MP4 via Puppeteer + headed Chrome
# Usage: render.sh <project-dir> [--no-audio] [--output <path>]
set -euo pipefail

DIR="${1:?Usage: render.sh <project-dir> [--no-audio] [--output path]}"
NO_AUDIO=false
OUTPUT=""

shift
while [ $# -gt 0 ]; do
  case "$1" in
    --no-audio) NO_AUDIO=true ;;
    --output) OUTPUT="${2:?--output requires a path}"; shift ;;
  esac
  shift
done

# Find Chrome
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
if [ ! -f "$CHROME" ]; then
  CHROME="/usr/bin/google-chrome"
fi
if [ ! -f "$CHROME" ]; then
  echo "[ERROR] Chrome not found. Install Google Chrome first."
  exit 1
fi

# Ensure puppeteer-core is available
cd "$DIR"
npm ls puppeteer-core &>/dev/null || npm install puppeteer-core --save-dev 2>&1 | tail -1

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "[RENDER] Project: $DIR"
echo "[RENDER] Chrome:  $CHROME"

node "$SCRIPT_DIR/render.mjs" "$DIR" "$CHROME"

# Merge audio
if [ "$NO_AUDIO" = false ] && [ -d "$DIR/audio" ]; then
  MP4=$(ls "$DIR/output/"*.mp4 2>/dev/null | head -1)
  if [ -z "$MP4" ]; then
    echo "[WARN] No MP4 found in output/"
    exit 1
  fi

  if [ -z "$OUTPUT" ]; then
    echo "[INFO] Raw video: $MP4"
    exit 0
  fi

  echo "[MERGE] Combining video + audio → $OUTPUT"
  CONCATLIST=$(mktemp)
  for f in $(ls "$DIR/audio/scene"*.mp3 2>/dev/null | sort -V); do
    echo "file '$f'" >> "$CONCATLIST"
  done

  MERGED_AUDIO=$(mktemp /tmp/edu-merge-XXXXX.mp3)
  ffmpeg -y -f concat -safe 0 -i "$CONCATLIST" -c copy "$MERGED_AUDIO" 2>/dev/null
  ffmpeg -y -i "$MP4" -i "$MERGED_AUDIO" -c:v copy -c:a aac -b:a 128k -shortest "$OUTPUT" 2>&1 | tail -1

  rm -f "$CONCATLIST" "$MERGED_AUDIO"
  echo "[OK] $OUTPUT"
fi
