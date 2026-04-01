#!/bin/bash
# Initialize a Manim educational video project
# Usage: init-project.sh <project-dir>
set -euo pipefail

DIR="${1:?Usage: init-project.sh <project-dir>}"

mkdir -p "$DIR/audio"
touch "$DIR/__init__.py"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ASSETS_DIR="$(dirname "$SCRIPT_DIR")/assets"

if [ -f "$ASSETS_DIR/design_system.py" ]; then
  cp "$ASSETS_DIR/design_system.py" "$DIR/design_system.py"
  echo "[OK] Copied design_system.py to $DIR"
fi

echo "[OK] Manim project ready: $DIR"
echo "[OK] Write scenes to $DIR/<name>.py"
echo "[OK] Generate audio to $DIR/audio/scene{N}.mp3"
