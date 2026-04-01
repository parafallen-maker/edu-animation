#!/bin/bash
# Initialize a Manim educational video project
# Usage: init-project.sh <project-dir>
set -euo pipefail

DIR="${1:?Usage: init-project.sh <project-dir>}"

mkdir -p "$DIR/audio"
touch "$DIR/__init__.py"

echo "[OK] Manim project ready: $DIR"
echo "[OK] Write scenes to $DIR/<name>.py"
echo "[OK] Generate audio to $DIR/audio/scene{N}.mp3"
