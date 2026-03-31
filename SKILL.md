---
name: edu-animation
description: Generate educational explainer videos from text scripts using Manim + Edge TTS + FFmpeg. Supports precise vector-based information design with exact coordinate control, architecture diagrams, flow charts, comparison tables, radial graphs, and data visualizations. Triggers when user asks to create an educational video, explainer animation, tutorial video, 科普视频, 科普动画, 教学视频, or 视频制作 from a script/topic. Supports Chinese and English narration.
---

# Educational Animation Generator

Generate short educational videos (1-5 min) using Manim, Edge TTS, and FFmpeg.

## Prerequisites

- Python 3.10+ with Manim (`pip install manim`)
- System Cairo library (`brew install cairo` on macOS)
- `edge-tts` (`pip install edge-tts`)
- FFmpeg (`brew install ffmpeg`)
- Chinese font: PingFang SC (macOS built-in) or Source Han Sans SC

## Workflow

### 1. Gather Requirements

Confirm with user:
- **Topic** and key points
- **Audience** (beginners / practitioners / general)
- **Language** (default: Chinese)
- **Duration** (default: ~2 min)

### 2. Write Script & Storyboard

Split into 6-10 scenes. Each scene:
- Title + subtitle
- Narration text (TTS reads this)
- **Visual spec** (shapes, positions, data — Manim requires precision)
- Duration estimate (~4 chars/sec for Chinese)

Save as markdown.

### 3. Generate TTS Audio

```bash
bash scripts/gen-tts.sh <project-dir> "旁白文本" [--voice zh-CN-YunxiNeural]
```

Voices: `zh-CN-YunxiNeural` (male), `zh-CN-XiaoxiaoNeural` (female), `zh-CN-YunjianNeural` (narrative).

Output: `<project-dir>/audio/scene{N}.mp3`

### 4. Build Manim Scene Code

```bash
bash scripts/init-project.sh <project-dir>
```

Use design system from `references/design-system.py` for consistent components.

**Manim design principles:**
- Every element has exact coordinates — no CSS ambiguity
- Use `SurroundingRectangle` / `BackgroundRectangle` for emphasis
- Use `Arrow` with `max_tip_length_to_length_ratio` for annotations
- Text hierarchy: Title > Subtitle > Body > Caption
- Use `Axes` / `NumberPlane` for data visualization
- See `references/manim-patterns.md` for reusable scene patterns

### 5. Render & Merge

```bash
bash scripts/render.sh <project-dir> --output <final.mp4> [-ql|-qm|-qh|-qk]
```

Quality: `-ql` (480p), `-qm` (720p, default), `-qh` (1080p), `-qk` (4K)

### 6. Visual Review (when image model available)

After rendering, capture key frames for visual inspection:

```bash
source /tmp/manim-env/bin/activate
manim render --format png -o review <script.py> SceneName
```

Then use the `image` tool to analyze: alignment, overlap, readability, color consistency. Fix issues in Manim code and re-render.

## Quality Checklist

- [ ] All scenes have narration matching TTS audio duration
- [ ] `self.wait()` durations match scene audio lengths
- [ ] Font set to `"PingFang SC"` for Chinese
- [ ] `camera.background_color` is dark (#0B1120)
- [ ] Visual hierarchy is clear (size + color + position)
- [ ] All diagrams have labels and annotations
- [ ] No text overlap or truncation
- [ ] Animations use easing (default spring), not abrupt cuts
- [ ] Final MP4 has both video + audio tracks synced
