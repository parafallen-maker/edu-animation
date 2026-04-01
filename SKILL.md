---
name: edu-animation
description: "Generate educational explainer videos from text scripts using Manim + Edge TTS + FFmpeg. Triggers when user asks to create an educational video, explainer animation, tutorial video, 科普视频, 科普动画, 教学视频, or 视频制作 from a script/topic. Supports Chinese and English narration."
---

# Educational Animation Generator (Manim)

Generate short educational videos (1-10 min) using Manim, Edge TTS, and FFmpeg.

## Prerequisites

- Python 3.10+ with Manim (`pip install manim`)
- System Cairo library (`brew install cairo` on macOS)
- `edge-tts` (`pip install edge-tts`)
- FFmpeg (`brew install ffmpeg`)
- Chinese font: PingFang SC (macOS built-in) or Source Han Sans SC

**Quick environment setup:**
```bash
mkdir -p <project-dir>/audio
[ -f /tmp/manim-env/bin/activate ] && source /tmp/manim-env/bin/activate
python3 -m ensurepip -q 2>/dev/null
python3 -m pip install manim edge-tts -q 2>&1 | tail -1
```

## ⚠️ Context Recovery Protocol

Every conversation turn may follow a context loss (compaction, new session). **Before doing ANY work:**

1. **Check** if `PROGRESS.md` exists in the project directory
   - If YES → Read it completely to determine current phase and last completed step
   - If NO → This is a new project, proceed to Phase 1
2. **Read supporting files** referenced in PROGRESS.md (only if that phase is marked complete)
3. **Verify** files listed in "Files Created" section actually exist on disk
4. **Resume** from the first unchecked item in the current phase

> Skipping this protocol causes repeated work or file corruption. Always run it first.

## Progress Tracking — Mandatory Protocol

⚠️ **This protocol is NON-NEGOTIABLE. Skipping updates causes context loss and repeated work.**

Maintain `PROGRESS.md` using [progress-template.md](assets/progress-template.md). Create it at Phase 1 start.

### Checkpoint Rule

**Every time you complete a checkbox item in PROGRESS.md, you MUST immediately:**
1. Mark the item `[x]` and add brief notes
2. Update the "Current State" section
3. Then — and only then — proceed to the next item

### Phase Transition Gate

**Before starting any new Phase, you MUST:**
1. Read `PROGRESS.md` and verify ALL items in the previous phase are `[x]`
2. Update "Current Phase" to the new phase
3. If any previous item is unchecked, complete it first

## References

- [style-guide.md](references/style-guide.md) — Visual standards, color system, typography
- [animation-guide.md](references/animation-guide.md) — Animation patterns, timing, spring presets
- [visual-principles.md](references/visual-principles.md) — Composition, layout, information density
- [mobject-patterns.md](references/mobject-patterns.md) — Reusable Mobject component recipes
- [quality-checklist.md](references/quality-checklist.md) — QA workflow and style check rules
- [storyboard-template.md](references/storyboard-template.md) — Storyboard format
- [script-and-narration.md](references/script-and-narration.md) — Script writing and TTS notes
- [requirements-guide.md](references/requirements-guide.md) — Requirements gathering questionnaire

## Workflow

### Phase 1: Requirements Gathering

Confirm with user:
- **Topic**: What concept/subject to explain?
- **Audience**: Who is watching? (children/adults, beginners/experts)
- **Language**: Chinese/English/other?
- **Duration**: Short (1-3min), Medium (3-5min), or Long (5-10min)?
- **Key points**: What must the viewer learn?

Create `PROGRESS.md` from [progress-template.md](assets/progress-template.md).

For detailed question templates, see [requirements-guide.md](references/requirements-guide.md).

### Phase 1.5: Script Writing

> ⚠️ **Checkpoint Rule active**: Update PROGRESS.md after EACH item.

Write a complete narrative script before designing the storyboard.

**IMPORTANT**: Write the FULL narration text — every word that will be spoken. Do NOT write summaries, bullet points, or placeholders.

The script must include:
1. **Core message** — one-line summary, learning objectives
2. **Narrative strategy** — entry angle, core metaphor, knowledge scaffolding, emotional curve
3. **Full narration text** — word-for-word with emphasis markers (`**bold**` for stress, `*italic*` for softer tone) and pause markers (`[.]` short, `[..]` medium, `[...,` long, `[PAUSE]` dramatic)
4. **Pacing notes** — where to speed up, slow down, and pause
5. **Visual intents** — 1-2 sentences per chapter describing what viewers should see
6. **Self-review** — run through checklist in [script-and-narration.md](references/script-and-narration.md)

Quality gate: **Present the complete script to the user for approval. Do NOT proceed to Phase 2 until the user explicitly approves.**

Why script first: Separates "what to tell" from "how to show" — LLM produces better narratives when not simultaneously calculating animation specs.

**Output**: Save approved script as `script.md`

### Phase 2: Storyboard Design

> ⚠️ **Checkpoint Rule active**: Update PROGRESS.md after EACH item.

Convert the approved script into a production-ready storyboard.

Tasks:
1. Break script into visual scenes (5-15 scenes)
2. Assign narration text to each scene
3. Design visual layers (background / midground / foreground / UI)
4. Add frame-level animation specifications
5. Define visual-narration sync points
6. Plan asset inventory (shared Mobjects, colors, typography)

Use [storyboard-template.md](references/storyboard-template.md) for format.

**Output**: Save as `storyboard.md`

### Phase 3: Visual Design

> ⚠️ **Checkpoint Rule active**: Update PROGRESS.md after EACH item.

1. **Choose color palette** — Select from [design_system.py](assets/design_system.py) `T` class, or extend it with topic-appropriate colors
2. **Copy design_system.py** — Copy to project directory for local import
3. **Create shared Mobject components** — Build reusable visual elements following [mobject-patterns.md](references/mobject-patterns.md)
4. **Design scene layouts** — Plan visual layers per scene following [visual-principles.md](references/visual-principles.md)

See [style-guide.md](references/style-guide.md) for complete visual standards.

### Phase 4: Animation Implementation

> ⚠️ **Checkpoint Rule active**: Update PROGRESS.md after EACH item.

1. **Initialize project**: `bash scripts/init-project.sh <project-dir>`
2. **Generate TTS audio** for each scene: `bash scripts/gen-tts.sh <project-dir> "旁白文本"`
3. **Write Manim scene code** following [scene_template.py](assets/scene_template.py)
4. **Match `self.wait()` to audio durations** exactly

**Critical rules:**
- Import colors/fonts from `design_system.py` — NO hardcoded color hex strings
- Use `T.FONT` for all Chinese text
- Every element has exact coordinates — no ambiguity
- See [animation-guide.md](references/animation-guide.md) for animation patterns

### Phase 5: QA & Review

#### Step 1: Code Scanning

```bash
source /tmp/manim-env/bin/activate
python3 scripts/style-scan.py <project-dir> --output /tmp/style-report.md
```

Checks: hardcoded colors, invalid font sizes, missing imports, unsafe zone violations, layout conflicts.

> ✅ **Checkpoint**: Update PROGRESS.md — mark `[x] Round 1: style-scan`

#### Step 2: Keyframe Screenshot Review

```bash
bash scripts/render-keyframes.sh <project-dir> <scene_file.py> --output-dir /tmp/keyframes
```

Then use the `image` tool to analyze each screenshot for:
- Overall aesthetics, visual balance, color harmony
- Text readability, element overlap
- **Visual richness** — scenes with only text are PPT-like and must be redesigned
- **Illustration quality** — must use gradients, rounded corners, layered shapes
- **Content fill ratio** — content occupying ≤30% of canvas = "Thumbnail Syndrome"
- **Visual-narration sync** — elements should appear with their narration

> ✅ **Checkpoint**: Update PROGRESS.md — mark `[x] Round 1: screenshots rendered and reviewed`

#### Step 3: Auto-Fix

Fix 🔴Critical first, then 🟡Important. Re-run scan after fixes.
Maximum 3 rounds. See [quality-checklist.md](references/quality-checklist.md) for detailed rules.

> ✅ **Checkpoint**: Update PROGRESS.md — mark `[x] Round 1: fixes applied`

#### Step 4: Final Render

```bash
bash scripts/render.sh <project-dir> --output <final.mp4> -qh
```

## Quality Checklist

- [ ] All scenes have narration matching TTS audio duration
- [ ] `self.wait()` durations match scene audio lengths
- [ ] Font set to `"PingFang SC"` for Chinese (via `T.FONT`)
- [ ] `camera.background_color` is dark (`T.BG`)
- [ ] Visual hierarchy is clear (size + color + position)
- [ ] All diagrams have labels and annotations
- [ ] No text overlap or truncation
- [ ] Animations use easing (`rate_func`), not abrupt cuts
- [ ] No hardcoded color hex strings outside `design_system.py`
- [ ] Final MP4 has both video + audio tracks synced
