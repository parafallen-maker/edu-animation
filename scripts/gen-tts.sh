#!/bin/bash
# Generate TTS audio using Microsoft Edge TTS (free)
# Usage: gen-tts.sh <project-dir> <scene-N.txt|inline-text> [--voice <voice-id>]
# Example: gen-tts.sh /tmp/edu-video "这是旁白文本"
#   or: gen-tts.sh /tmp/edu-video scene3.txt
#   or: gen-tts.sh /tmp/edu-video "text" --voice zh-CN-XiaoxiaoNeural
set -euo pipefail

DIR="${1:?Usage: gen-tts.sh <project-dir> <text-or-file> [--voice voice]}"
INPUT="${2:?Missing text input}"
VOICE="zh-CN-YunxiNeural"  # Default: male voice

if [ "${3:-}" = "--voice" ] && [ -n "${4:-}" ]; then
  VOICE="$4"
fi

# Install edge-tts if needed
pip3 install edge-tts -q 2>&1 | tail -1

mkdir -p "$DIR/audio"

# Detect scene number or auto-increment
if [ -f "$INPUT" ]; then
  BASENAME=$(basename "$INPUT" .txt)
  TEXT=$(cat "$INPUT")
else
  # Auto-find next scene number
  N=1
  while [ -f "$DIR/audio/scene${N}.mp3" ]; do
    N=$((N + 1))
  done
  BASENAME="scene${N}"
  TEXT="$INPUT"
fi

echo "[TTS] Generating $BASENAME with voice $VOICE..."
edge-tts --voice "$VOICE" --text "$TEXT" --write-media "$DIR/audio/${BASENAME}.mp3" 2>&1 | tail -1

# Show duration
if command -v ffprobe &>/dev/null; then
  DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$DIR/audio/${BASENAME}.mp3")
  echo "[OK] $DIR/audio/${BASENAME}.mp3 (${DUR}s)"
else
  echo "[OK] $DIR/audio/${BASENAME}.mp3"
fi

# List all generated files
echo ""
echo "[AUDIO] Generated files:"
ls -lh "$DIR/audio/"
