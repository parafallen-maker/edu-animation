# Motion Canvas Scene Patterns

Reusable component patterns and animation templates for Motion Canvas v3 educational videos.

## Color System

```
BG:      #0B1120  (deep navy)
PANEL:   #132040  (panel bg)
BORDER:  rgba(255,255,255,0.08)
BLUE:    #4A9EFF  (primary accent)
RED:     #FF6B6B  (danger/contrast)
GREEN:   #4ADE80  (success)
YELLOW:  #FBBF24  (highlight)
WHITE:   #FFFFFF
BODY:    #CBD5E1  (body text)
MUTED:   #64748B  (secondary text)
```

## Font Stack

```
PingFang SC, Hiragino Sans GB, Microsoft YaHei, Noto Sans CJK SC, sans-serif
```

## Component Templates

### TitleBlock
Fade in + slide up with spring. Title (64px, weight 800) + subtitle (30px, body color).

### NarrationBox
Bottom-anchored semi-transparent panel: `rgba(9,18,34,0.88)`, border-radius 32px, padding 28px 34px, fontSize 29, lineHeight 1.5.

### MetricChip
Vertical layout: label (24px, body color) + value (34px, accent color, weight 800). Panel: 260×110, radius 24.

### SceneCard
Wide panel (420×240): accent color left strip (8px, radius 8), title (34px, weight 700), subtitle (22px, body).

### Grid/Dot Background
- Dots every 120px, size 4, fill rgba(255,255,255,0.05)
- Vertical lines every 240px, stroke rgba(255,255,255,0.03)
- Horizontal lines every 180px, stroke rgba(255,255,255,0.02)
- Decorative circles: large blurred (r=200-260, opacity 0.12-0.16)

## Scene Types

### Comparison Scene (A vs B)
Split screen with left/right panels. Animate elements sequentially.
- Phase 1: Left panel content appears (1.2s)
- Phase 2: Right panel content appears (1.2s)
- Phase 3: Connection/contrast element (1.0s)

### Timeline/Sequence Scene
Horizontal or vertical progression of steps.
- Each step slides in from the direction of flow
- Active step highlighted with accent glow

### Data/Metric Scene
Key figures displayed prominently with animated counters.
- Numbers count up from 0
- Color-coded by category

### Card Cascade Scene
Multiple info cards appear sequentially (staggered 0.3-0.5s).
- Cards slide up + fade in
- Earlier cards dim slightly when later ones appear

## Animation Guidelines

- Use `all()` for parallel animations
- Use `spring()` for natural motion (damping 10-15)
- Use `waitFor()` for static holds
- Target scene duration: 10-25 seconds
- Keep scene components under 60 lines each
