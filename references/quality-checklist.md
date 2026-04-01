# 质量检查清单

Phase 5 QA 自动化工作流。

## Step 1: 代码扫描

```bash
source /tmp/manim-env/bin/activate
python3 scripts/style-scan.py <project-dir> --output /tmp/style-report.md
```

脚本自动检查：

| 检查项 | 提取方式 | 严重级别 |
|--------|---------|---------|
| 硬编码颜色 | 正则 `#hex` 不在 T 类中 | 🟡重要 |
| 非标准字号 | `font_size=` 不在标准集 | 🟢轻微 |
| 字号过小 | `font_size < 13` | 🔴严重 |
| 缺少 design_system 导入 | grep import | 🔴严重 |
| corner_radius 非标准 | 不在 T.RADIUS | 🟢轻微 |
| stroke_width 非标准 | 不在 T.STROKE | 🟢轻微 |
| wait(0) | 正则 | 🟡重要 |
| wait 过长 | `> 15s` | 🟡重要 |

> ✅ **Checkpoint**: 更新 PROGRESS.md — 标记 `[x] Round 1: style-scan` 并记录问题数量。

## Step 2: 关键帧截图审查

渲染关键帧截图，然后用 image tool 分析：

```bash
bash scripts/render-keyframes.sh <project-dir> <scene_file.py> --output-dir /tmp/keyframes
```

然后对每张截图用 `image` tool 检查：

| 检查项 | 检查内容 | 严重级别 |
|--------|---------|---------|
| 整体美观 | 画面干净、专业、符合教育视频风格 | 🔴严重 |
| 视觉平衡 | 构图平衡、留白合理、元素分布均匀 | 🔴严重 |
| 色彩协调 | 色彩方案统一、不刺眼 | 🔴严重 |
| 视觉层级 | 主体突出、信息层级清晰 | 🔴严重 |
| 文字可读性 | 文字清晰、字号足够、对比度充分 | 🔴严重 |
| 元素重叠 | 文字被遮挡、元素不当重叠 | 🔴严重 |
| **视觉丰富度** | **场景是否有非文本视觉内容？纯文本彩框 = PPT 风格，必须重设计** | 🔴严重 |
| **插图质量** | **是否使用渐变、圆角、分层形状？纯色填充矩形不可接受** | 🔴严重 |
| 安全区 | 关键内容是否被裁切 | 🟡重要 |
| **元素尺寸** | **内容占画布 ≤30% = "缩略图综合征"** | 🔴严重 |
| **视觉-旁白同步** | **视觉元素是否与旁白同时出现？差异 >0.3s = 不同步** | 🔴严重 |
| 环境效果 | 是否有背景纹理/粒子/光晕？纯色背景太单调 | 🟡重要 |

> ✅ **Checkpoint**: 更新 PROGRESS.md — 标记 `[x] Round 1: screenshots rendered and reviewed`

## Step 3: 自动修复

1. **按优先级**：先修 🔴严重，再修 🟡重要，🟢轻微可跳过
2. **每条问题**：定位源码，根据修复策略修改
3. **回归验证**：修复后重新运行 Step 1 + Step 2
4. **循环条件**：仍有 🔴严重则继续，最多 3 轮

> ✅ **Checkpoint**: 更新 PROGRESS.md — 标记 `[x] Round 1: fixes applied`

## Step 4: 最终渲染

```bash
bash scripts/render.sh <project-dir> --output <final.mp4> -qh
```

## 报告格式

每条问题包含：
- 严重级别：🔴严重 / 🟡重要 / 🟢轻微
- 来源：[Code Scan] 或 [Screenshot Review]
- 文件:行号 或 截图:帧号
- 当前值 vs 规则要求
- 具体修复建议

---

## 附录：Style Check Rules

### 1. 字号规则（1080p 画布）
| 元素类型 | 最低值 | 推荐值 |
|---------|--------|--------|
| 场景主标题 | 36 | 56 (T.H1) |
| 章节标题 | 24 | 36 (T.H2) |
| 正文/标签 | 13 | 16-24 (T.H3/H4) |
| 字幕 | 13 | 24 (T.H3) |
| **绝对最低** | **13** | — |

**修复**：`font_size < 13` → 改为 13；低于推荐值 → 改为推荐值。

### 2. 调色板
动态从 `design_system.py` 的 `T` 类提取。`rgba()` 和黑白豁免。

**修复**：非批准颜色 → 用 `T` 类中最接近的颜色替换。

### 3. 安全区（Manim 坐标）
- x ∈ [-6.4, 6.4], y ∈ [-3.5, 3.5]
- `.move_to()` 或 `.to_edge()` 超出此范围 → 🔴严重

**修复**：使用 `.to_edge(UP/LEFT/etc, buff=...)` 控制在安全区内。

### 4. 间距规范
合法值（对应 T 的 buff）：0.1, 0.2, 0.3, 0.5, 0.8

### 5. 圆角
标准值：T.RADIUS = [0.05, 0.1, 0.2, 0.3, 0.5]

### 6. 描边
标准值：T.STROKE = [1, 2, 3, 4]

### 7. 布局区域
| 区域 | Y 范围 | 用途 |
|------|--------|------|
| 标题区 | y > 2.5 | 场景标题 |
| 内容区 | y ∈ [-1.0, 2.5] | 核心内容 |
| 信息区 | y ∈ [-2.5, -1.0] | 补充信息 |
| 字幕区 | y < -3.2 | 旁白字幕 |

### 8. 禁用模式
| 禁止做法 | 正确做法 |
|---------|---------|
| 直接 `mobject.shift()` | `self.play(mobject.animate.shift(...))` |
| 直接 `mobject.set_opacity(0)` | `self.play(FadeOut(mobject))` |
| 硬编码 `"#FF0000"` | 从 `T` 类导入 |
