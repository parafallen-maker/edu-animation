---
name: edu-animation
description: Generate educational explainer videos from text scripts using Motion Canvas + Edge TTS + FFmpeg. Triggers when user asks to create an educational video, explainer animation, tutorial video, 科普视频, 科普动画, 教学视频, or 视频制作 from a script/topic. Supports Chinese and English narration with Kurzgesagt/3Blue1Brown-style flat design visuals.
---

# Educational Animation Generator

Generate short educational videos (1-5 min) from text scripts using Motion Canvas, Edge TTS, and FFmpeg.

## Prerequisites

- Node.js 16+, npm
- Python 3 + `edge-tts` (`pip3 install edge-tts`)
- Google Chrome (macOS/Linux)
- FFmpeg (`brew install ffmpeg`)

## Workflow

### 1. Gather Requirements

Confirm with user:
- **Topic** and key points to cover
- **Audience** (beginners / practitioners / general)
- **Language** (default: Chinese)
- **Duration** (default: ~2 min)
- **Style** (default: dark theme, Kurzgesagt/3Blue1Brown flat design)

### 2. Write Script & Storyboard

Split into 6-10 scenes. Each scene needs:
- Title + subtitle (shown at top)
- Narration text (read aloud by TTS)
- Visual concept (what shapes/figures/diagrams to show)
- Duration estimate (based on narration length ~4 chars/sec for Chinese)

Save as markdown. Each scene = one section.

### 3. Generate TTS Audio

For each scene's narration text:
```bash
bash scripts/gen-tts.sh <project-dir> "旁白文本" [--voice zh-CN-XiaoxiaoNeural]
```

Available Chinese voices (edge-tts):
- `zh-CN-YunxiNeural` — male, energetic (default)
- `zh-CN-XiaoxiaoNeural` — female, warm
- `zh-CN-YunjianNeural` — male, narrative

Repeat for each scene. Files output to `<project-dir>/audio/scene{N}.mp3`.

### 4. Build Motion Canvas Project

Initialize project:
```bash
bash scripts/init-project.sh <project-dir> [<project-name>]
```

Create scene files in `src/scenes/scene{N}.tsx`. Follow patterns in `references/motion-canvas-patterns.md`.

**Critical project.ts rules:**
- Do NOT set `audio` in `makeProject()` — audio is merged separately
- Import all scenes with `?scene` suffix
- Scenes play sequentially

**Rendering caveats:** See `references/troubleshooting.md`.

### 5. Render & Merge

Render to MP4 (no audio, audio merged separately to avoid Motion Canvas path issues):
```bash
bash scripts/render.sh <project-dir> --no-audio --output <final-output.mp4>
```

Or render without merging:
```bash
bash scripts/render.sh <project-dir> --no-audio
# Raw video at <project-dir>/output/<name>.mp4
```

## Scene Structure Template

```tsx
import { Layout, Node, Rect, Txt, makeScene2D } from '@motion-canvas/2d';
import { all, createRef, waitFor } from '@motion-canvas/core';
import { BG, BLUE, backgroundPattern, centeredTitle } from '../lib';

export default makeScene2D(function* (view) {
  view.fill(BG);
  const root = createRef<Node>();
  view.add(<Node ref={root} opacity={0} scale={0.92}>
    {backgroundPattern()}
    {centeredTitle('Scene Title', 'Subtitle')}
  </Node>);

  // Add visual content to root...

  // Animate in
  yield* all(root().opacity(1, 1.2), root().scale(1, 1.2));
  // Hold
  yield* waitFor(7);
});
```

## Quality Checklist

- [ ] All scenes have Chinese/English narration
- [ ] Scene durations match TTS audio lengths
- [ ] `project.ts` has NO `audio` field
- [ ] Visual hierarchy: title > subtitle > narration > decoration
- [ ] Color consistency with palette (see references)
- [ ] Animations use spring easing, not linear
- [ ] Final MP4 has both video + audio tracks

## Tips

- Keep each scene component under 60 lines
- Use `waitFor()` for static holds between animations
- Test render with 1-2 scenes first before building all
- Motion Canvas rendering takes ~1-3 min for a 2-min video
- If rendering hangs, check `references/troubleshooting.md`
