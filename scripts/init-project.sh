#!/bin/bash
# Initialize a Motion Canvas educational video project
# Usage: init-project.sh <project-dir> [project-name]
set -euo pipefail

DIR="${1:-/tmp/edu-video}"
NAME="${2:-edu-animation}"

if [ -d "$DIR/src" ]; then
  echo "[OK] Project already exists: $DIR"
else
  echo "[SETUP] Creating Motion Canvas project: $NAME"
  mkdir -p "$DIR"
  cd "$DIR"

  # Scaffold blank Motion Canvas project
  npx --yes create-video@latest . --template blank 2>&1 | tail -3 || \
  npx --yes @motion-canvas/create@latest . 2>&1 | tail -3

  npm install 2>&1 | tail -1
fi

mkdir -p "$DIR/audio"
mkdir -p "$DIR/src/scenes"

echo "[OK] Project ready at $DIR"
