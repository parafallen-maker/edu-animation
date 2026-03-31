#!/bin/bash
# Generate TTS audio using Microsoft Edge TTS (free)
# Usage: gen-tts.sh <project-dir> <text-or-file> [--voice <voice>]
set -euo pipefail

DIR="${1:?Usage: gen-tts.sh <project-dir> <text-or-file> [--voice voice]}"
INPUT="${2:?Missing text input}"
VOICE="zh-CN-YunxiNeural"

if [ "${3:-}" = "--voice" ] && [ -n "${4:-}" ]; then
  VOICE="$4"
fi

pip3 install edge-tts -q 2>&1 | tail -1
mkdir -p "$DIR/audio"

if [ -f "$INPUT" ]; then
  TEXT=$(cat "$INPUT")
else
  N=1
  while [ -f "$DIR/audio/scene${N}.mp3" ]; do N=$((N + 1)); done
  BASENAME="scene${N}"
  TEXT="$INPUT"
fi

edge-tts --voice "$VOICE" --text "$TEXT" --write-media "$DIR/audio/${BASENAME}.mp3" 2>&1 | tail -1

if command -v ffprobe &>/dev/null; then
  DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$DIR/audio/${BASENAME}.mp3")
  echo "[OK] $DIR/audio/${BASENAME}.mp3 (${DUR}s)"
else
  echo "[OK] $DIR/audio/${BASENAME}.mp3"
fi
