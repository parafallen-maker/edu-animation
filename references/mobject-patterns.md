# Mobject 组件模式

Manim 中可复用的视觉组件食谱。每个组件直接使用 `design_system.py` 的 `T` token。

## 箭头组件

### 标注箭头
```python
def annotate_arrow(start, end, label="", color=None):
    """带标签的标注箭头"""
    if color is None:
        color = T.WHITE
    ar = Arrow(start, end, stroke_width=3, color=color,
               max_tip_length_to_length_ratio=0.15, buff=0.1)
    if label:
        mid = (np.array(start) + np.array(end)) / 2
        lbl = Z(label, font_size=T.CAP, color=T.BODY).next_to(mid, UP, buff=T.SM)
        return VGroup(ar, lbl)
    return ar
```

### 力箭头（Kurzgesagt 风格）
```python
FORCE_COLORS = {
    "lift":    T.BLUE,
    "gravity": T.RED,
    "thrust":  T.GREEN,
    "drag":    T.ROSE,
}

FORCE_DIRS = {
    "lift":    UP,
    "gravity": DOWN,
    "thrust":  RIGHT,
    "drag":    LEFT,
}

def force_arrow(force_type, length=1.5, show_label=True):
    """力的示意箭头"""
    color = FORCE_COLORS[force_type]
    direction = FORCE_DIRS[force_type]
    ar = Arrow(ORIGIN, direction * length, stroke_width=4, color=color,
               max_tip_length_to_length_ratio=0.2)
    if show_label:
        labels = {"lift": "升力", "gravity": "重力", "thrust": "推力", "drag": "阻力"}
        lbl = Z(labels[force_type], font_size=T.H4, color=color, weight=BOLD)
        lbl.next_to(ar, direction, buff=T.SM)
        return VGroup(ar, lbl)
    return ar
```

## 图标组件
```python
def icon_container(emoji, label="", color=None, size=0.6):
    """图标 + 可选标签的容器"""
    if color is None:
        color = T.BLUE
    circle = Circle(radius=size, fill_color=color, fill_opacity=0.12,
                     stroke_color=color, stroke_width=2)
    icon = Z(emoji, font_size=28).move_to(circle)
    group = VGroup(circle, icon)
    if label:
        lbl = Z(label, font_size=T.H4, color=T.BODY, weight=BOLD)
        lbl.next_to(circle, DOWN, buff=T.SM)
        group.add(lbl)
    return group
```

## 信息卡片
```python
def styled_card(title, body_lines, accent_color=None, width=3.5, height=2.5):
    """带标题和内容列表的卡片"""
    if accent_color is None:
        accent_color = T.BLUE
    bg = RoundedRectangle(
        width=width, height=height, corner_radius=0.2,
        fill_color=T.BG_MEDIUM, stroke_color=accent_color, stroke_width=2
    )
    # 顶部强调线
    accent_line = Line(
        bg.get_corner(UL) + DOWN * 0.1 + RIGHT * 0.3,
        bg.get_corner(UR) + DOWN * 0.1 + LEFT * 0.3,
        color=accent_color, stroke_width=3
    )
    title_text = Z(title, font_size=T.H3, color=accent_color, weight=BOLD)
    title_text.next_to(accent_line, DOWN, buff=T.SM).align_to(bg, LEFT).shift(RIGHT * 0.3)
    items = VGroup(*[Z(f"• {line}", font_size=T.BODY_S, color=T.BODY) for line in body_lines])
    items.arrange(DOWN, aligned_edge=LEFT, buff=0.08)
    items.next_to(title_text, DOWN, buff=T.SM).align_to(bg, LEFT).shift(RIGHT * 0.3)
    return VGroup(bg, accent_line, title_text, items)
```

## 动画文本

### 淡入
```python
self.play(FadeIn(text, shift=UP * 0.2), run_time=0.5)
```

### 缩放入场
```python
self.play(GrowFromCenter(text), run_time=0.6)
```

### 逐字显示（打字机效果）
```python
def typewriter_reveal(text_mobject, scene, char_rate=0.05):
    """逐字显示文字"""
    full_text = text_mobject.text
    chars = list(full_text)
    result = Z("", font_size=text_mobject.font_size, color=text_mobject.color)
    for i, char in enumerate(chars):
        new_text = Z("".join(chars[:i + 1]), font_size=text_mobject.font_size, color=text_mobject.color)
        new_text.move_to(text_mobject)
        scene.play(Transform(result, new_text), run_time=char_rate)
    return result
```

## 进度条
```python
def progress_bar(value=0.75, width=6, color=None):
    """水平进度条"""
    if color is None:
        color = T.BLUE
    bg_bar = RoundedRectangle(
        width=width, height=0.3, corner_radius=0.15,
        fill_color=T.BG_LIGHT, fill_opacity=0.5, stroke_width=0
    )
    fill_width = width * value
    fill_bar = RoundedRectangle(
        width=fill_width, height=0.3, corner_radius=0.15,
        fill_color=color, fill_opacity=0.8, stroke_width=0
    )
    fill_bar.align_to(bg_bar, LEFT)
    pct = Z(f"{int(value * 100)}%", font_size=T.H4, color=T.WHITE, weight=BOLD)
    pct.move_to(fill_bar)
    return VGroup(bg_bar, fill_bar, pct)
```

## 数据可视化

### 柱状图
```python
def bar_chart(data, max_height=3):
    """简单柱状图。data: [(label, value, color)]"""
    bars = VGroup()
    max_val = max(d[1] for d in data)
    bar_width = 0.6
    gap = 0.3

    for i, (label, value, color) in enumerate(data):
        height = (value / max_val) * max_height
        bar = RoundedRectangle(
            width=bar_width, height=height, corner_radius=0.1,
            fill_color=color, fill_opacity=0.8, stroke_width=0
        )
        bar.move_to(DOWN * (max_height / 2 - height / 2))
        bar.shift(RIGHT * (i * (bar_width + gap) - len(data) * (bar_width + gap) / 2))
        lbl = Z(label, font_size=T.CAP, color=T.BODY).next_to(bar, DOWN, buff=T.SM)
        val = Z(str(value), font_size=T.H4, color=color, weight=BOLD).next_to(bar, UP, buff=T.SM)
        bars.add(VGroup(bar, lbl, val))

    return bars
```

### 环形图
```python
def donut_chart(segments, radius=1.5, inner_radius=0.8):
    """环形图。segments: [(label, percentage, color)]"""
    arcs = VGroup()
    start_angle = 0

    for label, pct, color in segments:
        angle = pct / 100 * 360
        arc = AnnularSector(
            inner_radius=inner_radius, outer_radius=radius,
            start_angle=start_angle, angle=angle,
            fill_color=color, fill_opacity=0.8, stroke_width=0
        )
        arcs.add(arc)
        start_angle += angle

    arcs.move_to(ORIGIN)
    return arcs
```

## 架构图组件

### 四层堆叠架构
```python
def four_layer_arch(layers_data):
    """四层架构图。layers_data: [(label, items, color)]"""
    layer_mobjects = []
    for label, items, color in layers_data:
        layer = arch_layer(label, items, color)
        layer_mobjects.append(layer)

    stack = VGroup(*layer_mobjects).arrange(DOWN, buff=0.4)

    # 层间箭头
    arrows = VGroup()
    for i in range(len(stack) - 1):
        ar = Arrow(stack[i], stack[i + 1], buff=0.15, stroke_width=2,
                   color=T.WHITE, max_tip_length_to_length_ratio=0.15).set_opacity(0.3)
        arrows.add(ar)

    return VGroup(stack, arrows)
```

## 组合动画模式

### 动画图表（中心 + 周围）
```python
def animated_radial(scene, center_label, satellites, radius=2.5):
    """逐步展示放射图"""
    center_node = Circle(radius=0.8, color=T.ORANGE, fill_opacity=0.15, stroke_width=3)
    center_text = Z(center_label, font_size=T.H3, color=T.ORANGE, weight=BOLD)
    center_group = VGroup(center_node, center_text)

    scene.play(FadeIn(center_group, scale=1.1), run_time=0.5)

    sat_groups = []
    for i, (label, color) in enumerate(satellites):
        angle = (i / len(satellites)) * TAU - PI / 2
        pos = np.array([radius * np.cos(angle), radius * np.sin(angle), 0])
        node = Circle(radius=0.5, color=color, fill_opacity=0.08, stroke_width=1.5).move_to(pos)
        lbl = Z(label, font_size=T.H4, color=T.BODY, weight=BOLD).move_to(pos)
        ar = Arrow(center_group, node, buff=0.15, stroke_width=1.5, color=T.WHITE,
                   max_tip_length_to_length_ratio=0.15).set_opacity(0.2)
        g = VGroup(node, lbl, ar)
        sat_groups.append(g)
        scene.play(FadeIn(g), run_time=0.35)

    return VGroup(center_group, *sat_groups)
```

### 错落列表
```python
def staggered_list(scene, items, animation_class=FadeIn, lag_ratio=0.3):
    """错落显示列表"""
    for item in items:
        scene.play(animation_class(item), run_time=0.4)
    # 或使用 LaggedStart 一次性编排
    # scene.play(LaggedStart(*[animation_class(i) for i in items], lag_ratio=lag_ratio), run_time=2)
```
