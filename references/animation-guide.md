# 动画设计指南

Manim 教育视频的动画模式、时间标准和最佳实践。

## 核心规则

**所有动画必须通过 `self.play()` 驱动**

```python
# ✓ 正确：通过 Animation 包装
self.play(FadeIn(title), run_time=0.8)
self.play(mobject.animate.shift(RIGHT * 2), run_time=1.0)

# ❌ 错误：直接修改属性
mobject.shift(RIGHT * 2)  # 无动画过渡
mobject.set_opacity(0)     # 瞬间消失
```

## 时间标准

### 常用 run_time 值

| 类型 | run_time | 用途 |
|------|----------|------|
| 微交互 | 0.1-0.2s | 徽章、切换 |
| 快速 | 0.3-0.5s | 图标入场 |
| 标准 | 0.5-0.8s | 卡片、面板 |
| 慢速 | 1.0-1.5s | 全屏元素 |
| 戏剧性 | 1.5-2.5s | 场景转换 |

### 与音频时长的匹配

```python
# 场景总时长 = 动画预算 + hold 时间
# hold 时间 = 音频时长 - 动画预算
audio_duration = 10.6  # 秒
animation_budget = 3.5  # 入场动画总时长
self.wait(audio_duration - animation_budget)  # self.wait(7.1)
```

## 缓动函数（rate_func）

Manim 内建缓动，推荐使用：

```python
from manim import *

# ── 推荐的缓动 ──
smooth      # 平滑减速，最常用
linear      # 匀速，适合数据动画
rush_into   # 快速进入，适合强调
rush_from   # 快速离开
slow_into   # 缓慢进入，适合大元素
there_and_back  # 去回，适合脉冲效果

# ── 不推荐 ──
# bouncing — 弹跳过多，教育视频显得不专业
# wiggle — 除非特别需要抖动效果
```

## 入场动画模式

### FadeIn — 淡入
```python
self.play(FadeIn(mobject, shift=UP * 0.3), run_time=0.5)
# shift 参数：入场方向
```

### GrowFromCenter — 从中心生长
```python
self.play(GrowFromCenter(circle), run_time=0.8)
# 适合圆形、放射图中心
```

### Create — 路径绘制
```python
self.play(Create(arrow), run_time=0.6)
self.play(Create(diagram_line), run_time=0.4)
# 适合箭头、连接线、流程线
```

### DrawBorderThenFill — 先轮廓后填充
```python
self.play(DrawBorderThenFill(card_bg), run_time=0.8)
# 适合卡片、面板等有填充的元素
```

### ScaleIn / GrowFromPoint
```python
self.play(GrowFromPoint(icon, ORIGIN), run_time=0.5)
self.play(ScaleInPlace(title, scale_factor=0), run_time=0.3)
# 适合弹出式强调
```

## 退场动画模式

### FadeOut — 淡出
```python
self.play(FadeOut(mobject, shift=DOWN * 0.3), run_time=0.3)
```

### FadeOutAndShift — 淡出+移位
```python
self.play(FadeOutAndShift(elements, direction=UP), run_time=0.5)
# 适合场景转场
```

### Uncreate — 路径消融
```python
self.play(Uncreate(arrow), run_time=0.3)
```

## 注意力动画

### 聚焦高亮
```python
# 用 SurroundingRectangle 聚焦某个元素
highlight = SurroundingRectangle(target, color=T.BLUE, fill_opacity=0.08)
self.play(Create(highlight), run_time=0.3)
# 移除聚焦
self.play(FadeOut(highlight), run_time=0.2)
```

### 脉冲
```python
# 用 .animate 做脉冲效果
self.play(
    circle.animate.set_stroke_width(4).set_stroke_color(T.YELLOW),
    run_time=0.3
)
self.play(
    circle.animate.set_stroke_width(2).set_stroke_color(T.BLUE),
    run_time=0.3
)
```

### 闪烁高亮
```python
flash = SurroundingRectangle(target, color=T.YELLOW, fill_opacity=0.3)
self.play(FadeIn(flash), run_time=0.15)
self.play(FadeOut(flash), run_time=0.15)
```

## 错落动画（Staggered）

```python
# 方法 1：LaggedStart
self.play(
    LaggedStart(
        *[FadeIn(item) for item in items],
        lag_ratio=0.3,  # 每个元素间隔 30% 的动画时长
    ),
    run_time=2.0,
)

# 方法 2：Succession — 顺序播放
self.play(
    Succession(
        *[FadeIn(item, run_time=0.3) for item in items],
    ),
    run_time=len(items) * 0.3,
)
```

## 场景转场

```python
# 标准转场：淡出当前内容 → 淡入新内容
self.play(FadeOut(old_content), run_time=0.5)
self.remove(old_content)
self.play(FadeIn(new_content), run_time=0.5)

# 或一次性完成
self.play(
    FadeOut(old_content),
    FadeIn(new_content),
    run_time=0.8,
)
```

## 禁止的做法

| ❌ 禁止 | ✓ 正确做法 |
|---------|-----------|
| 直接 `mobject.shift()` | `self.play(mobject.animate.shift(...))` |
| 直接 `mobject.set_opacity(0)` | `self.play(FadeOut(mobject))` |
| 硬编码颜色 `"#FF0000"` | 从 `T` 类导入：`T.RED` |
| `self.wait(0)` | 设置合适的等待时长或删除 |
| `self.wait(30)` 无理由 | 确认匹配音频时长 |
| 一次 play 超过 10 个动画 | 拆分为多个 play 调用 |

## 性能提示

1. **减少重建**：用 `mobject.animate` 而非每次创建新 Mobject
2. **使用 VGroup**：批量操作相关元素
3. **`rate_func=smooth`** 是最常用的，避免复杂缓动
4. **`--disable_caching`** 开发时使用，最终渲染去掉
5. **1080p60 (`-qh`)** 是推荐的最终渲染质量
