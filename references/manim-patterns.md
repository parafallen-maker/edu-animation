# Manim Scene Patterns

Reusable patterns for educational video scenes.

## Architecture Diagram

```python
# Three-layer stack with flow arrows
layers = VGroup(
    arch_layer("🤖 大模型层", ["GPT", "Claude", "GLM", "Gemini"], BLUE),
    arch_layer("⚙️ 核心层", ["工具调度", "上下文", "Agent编排", "记忆"], GREEN),
    arch_layer("🔌 插件层", ["Telegram", "Discord", "飞书", "GitHub"], YELLOW),
)
layers.arrange(DOWN, buff=0.35).shift(DOWN * 0.5)
for layer in reversed(layers):
    self.play(FadeIn(layer, shift=UP * 0.2), run_time=0.6)
for i in range(len(layers) - 1):
    arrow = Arrow(layers[i], layers[i+1], buff=0.15, stroke_width=2,
                  color=WHITE, max_tip_length_to_length_ratio=0.2).set_opacity(0.4)
    self.play(Create(arrow), run_time=0.3)
```

## Agent Flow (Dispatch → Execute → Merge)

```python
main = RoundedRectangle(width=3, height=1, corner_radius=0.25,
                         fill_color=PURPLE, fill_opacity=0.15, stroke_color=PURPLE, stroke_width=2.5)
subs = VGroup(*[RoundedRectangle(...) for _ in range(3)])
# Dispatch arrows down
dispatch = VGroup(*[Arrow(main, s, buff=0.1, stroke_width=2, max_tip_length_to_length_ratio=0.15)
                    for s in subs]).set_opacity(0.4)
# Merge arrows up to result
result = RoundedRectangle(...)
merge = VGroup(*[Arrow(s, result, ...) for s in subs]).set_opacity(0.3)
```

## Comparison Table (N columns)

```python
cols = comparison_table([
    ("短期上下文", BLUE, "当前对话窗口",
     ["对话历史", "指令+回复", "窗口大小有限", "会话结束即遗忘"]),
    ("工作记忆", GREEN, "跨会话任务状态",
     ["当前任务进度", "文件/变量状态", "上下文切换保持", "Agent协作共享"]),
    ("长期记忆", YELLOW, "向量数据库",
     ["用户偏好习惯", "历史设计决策", "关键领域知识", "跨天/跨周持久"]),
])
cols.arrange(RIGHT, buff=0.3)
self.play(*[FadeIn(c, scale=0.95) for c in cols], run_time=0.8)
```

## Radial Topology (channels, capabilities)

```python
center = Circle(radius=1.2, color=ORANGE, fill_opacity=0.15, stroke_width=3)
graph = radial_graph(center, [
    ("💬 Telegram", BLUE), ("🎮 Discord", BLUE),
    ("🐦 飞书", BLUE), ("🔒 Signal", GREEN),
    ("🌐 Web", ORANGE), ("📱 iMessage", PURPLE),
])
for i, (g, a) in enumerate(zip(graph[0], graph[1])):
    self.play(FadeIn(g), Create(a), run_time=0.2)
```

## Tool Grid (2×3 or 3×3)

```python
tools = [("📁 文件读写", "read/write/edit", BLUE), ...]
cards = VGroup()
for icon, api, color in tools:
    card = RoundedRectangle(width=4.5, height=1.1, corner_radius=0.2,
                             fill_color=T.PANEL, stroke_color=T.BORDER, stroke_width=1.5)
    ic = Z(icon, font_size=22, color=T.WHITE, weight=BOLD).shift(LEFT * 0.3)
    ap = Z(api, font_size=14, color=T.MUTED).next_to(ic, RIGHT, buff=0.6)
    cards.add(VGroup(card, ic, ap))
cards.arrange_in_grid(rows=2, cols=3, buff=0.35)
```

## Timing Tips

- Chinese narration: ~4 chars/sec → a 60-char narration ≈ 15s scene
- Animation budget: use 5-8s for entrance animations, rest is `self.wait()`
- Match `self.wait()` to audio duration exactly
- Use `manim render --format png` to check final frame before full render
