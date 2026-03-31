# Troubleshooting

## Cairo / pycairo Build Error

**Error**: `Dependency "cairo" not found`

**Fix**: Install system Cairo library, then reinstall Manim:
```bash
brew install cairo pkg-config
pip install manim
```

## No Manim Virtual Environment

**Error**: `ModuleNotFoundError: No module named 'manim'`

**Fix**: Create venv with Python 3.10+:
```bash
uv venv /tmp/manim-env --python 3.12
source /tmp/manim-env/bin/activate
uv pip install manim
```

## Interactive Scene Selection

**Error**: Manim prompts "Choose number" and hangs in non-TTY.

**Fix**: Use `-a` flag to render all scenes:
```bash
manim render -qh -a -o output script.py SceneName
```

## Video Shorter Than Audio

**Cause**: `self.wait()` duration doesn't match TTS audio length.

**Fix**: Check audio durations, adjust `self.wait()` in each Scene:
```bash
for i in audio/scene*.mp3; do
  ffprobe -v error -show_entries format=duration -of csv=p=0 "$i"
done
```

## Chinese Font Not Rendering

**Symptom**: Boxes or missing characters in rendered video.

**Fix**: Explicitly set font in every `Text()` call:
```python
Text("中文", font="PingFang SC", font_size=24)
```

## Scene Concatenation Order Wrong

**Fix**: Manim renders Scene classes in file definition order. Ensure classes are defined top to bottom in the correct sequence.

## High Quality Slow

`-qk` (4K) is 4x slower than `-qh` (1080p). Use `-ql` (480p) for fast previews during development, `-qh` for final output.
