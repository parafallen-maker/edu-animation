# 分镜模板

```
# Storyboard: {Project Title}

## Scene {N}: {Scene Title}

**Duration**: {seconds} (must match audio)
**Layout**: Center Stage / Split Comparison / Diagram / Steps / Timeline / Radial

### Narration
> (word-for-word from approved script)

### Visual Layers

**Background:**
- Color: {T.BG / T.BG_MEDIUM / custom}
- Effect: {none / gradient / pattern / particles}

**Midground:**
- Main element: {description}
- Position: {Manim coordinates, e.g., ORIGIN, UP*2+LEFT*3}
- Components: {design_system components used}

**Foreground:**
- Labels: {description}
- Annotations: {description}
- Callouts: {description}

### Animation Specs

| Element | Animation | Start | Duration | Notes |
|---------|-----------|-------|----------|-------|
| {element} | FadeIn / GrowFromCenter / Create | 0s | 0.5s | shift UP*0.2 |
| {element} | LaggedStart(FadeIn) | 0.5s | 1.5s | lag_ratio=0.3 |
| {element} | FadeIn | 2.0s | 0.3s | subtitle |

### Sync Point
Visual "{element}" appears when narrator says: "{keyword}"

### Design System References
- Colors: {T.BLUE, T.GREEN, ...}
- Font sizes: {T.H1 for title, T.H3 for body}
- Components: {radial_graph, arch_layer, subtitle_bar, ...}
```

## 完整示例

```
# Storyboard: 什么是 IoT

## Scene 1: 什么是物联网？

**Duration**: 10.6s
**Layout**: Center Stage + Radial

### Narration
> 物联网，英文 Internet of Things，简称 IoT。简单来说，就是把日常物品连接到互联网，让它们能够互相通信。

### Visual Layers

**Background:**
- Color: T.BG (#0B1120)
- Effect: none

**Midground:**
- 中心：☁️ 云图标 (Circle + Z("☁️"))
- 位置：UP * 2
- 周围：📱手机、💡灯泡、📡传感器、⌚手表 (icon_container)
- 位置：DOWN * 1.5, 均匀分布
- 连线：DashedLine 从设备到云

**Foreground:**
- 标签：无（Scene 2 再加细节）

### Animation Specs

| Element | Animation | Start | Duration | Notes |
|---------|-----------|-------|----------|-------|
| title_block | FadeIn | 0s | 0.8s | "什么是 IoT？" |
| cloud | FadeIn + scale | 0.8s | 0.5s | UP*2 |
| phone | FadeIn + Create(line) | 1.3s | 0.4s | LEFT*3 |
| bulb | FadeIn + Create(line) | 1.7s | 0.4s | LEFT*1 |
| sensor | FadeIn + Create(line) | 2.1s | 0.4s | RIGHT*1 |
| watch | FadeIn + Create(line) | 2.5s | 0.4s | RIGHT*3 |
| (hold) | wait | 3.0s | 7.6s | match audio 10.6s |

### Sync Point
Cloud appears when narrator says: "互联网"
```
