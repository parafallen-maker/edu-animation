# edu-animation

Manim + Edge TTS + FFmpeg 教育科普视频 Skill。

针对**通识科普**场景优化：用视觉隐喻把一个概念讲清楚。

## 特性

- **视觉隐喻设计系统**：8 种可复用隐喻模式（流动、容器、天平、弹球、缩放……），每个概念都有日常物品类比
- **叙事级动画模式**：7 种场景级动画模式（铺垫揭示、因果链、左右对比、聚焦放大、错误纠正……）
- **画面密度控制**：5-Beat 短视频结构（Hook→Setup→Core→Aha→Linger），每段有密度上限
- **画面驱动工作流**：先设计视觉叙事，后写旁白 — 画面本身能讲故事
- **信息设计组件库**：架构图、流程图、对比表、星型拓扑、数据可视化
- **中文 TTS**：Edge TTS 免费语音合成，自动 timeline 对齐
- **1080p30 输出**：支持 480p / 720p / 1080p / 4K

## 快速开始

```bash
# 安装依赖
brew install cairo ffmpeg sox pkg-config
pip install manim edge-tts

# 初始化项目
bash scripts/init-project.sh my-video

# 生成旁白音频
python3 scripts/generate_tts.py \
  --inline '{"hook":"天空为什么是蓝色的？","setup":"太阳光其实是彩虹色混在一起。"}' \
  --output-dir my-video/audio/narration

# 编写 Manim 场景代码，使用设计系统组件
# 见 assets/design_system.py, references/narrative-patterns.md

# 渲染
bash scripts/render.sh my-video --output final.mp4 -qh
```

## 项目结构

```
edu-animation/
├── SKILL.md                          # Skill 定义 (6-phase workflow)
├── assets/
│   ├── design_system.py              # 设计令牌 + 可复用组件
│   ├── scene_template.py             # 场景代码模板
│   └── progress-template.md          # 进度跟踪模板
├── references/
│   ├── metaphor-patterns.md      ★   # 视觉隐喻模式库
│   ├── narrative-patterns.md     ★   # 叙事级动画模式
│   ├── popscience-structure.md   ★   # 短视频结构 + 密度控制
│   ├── style-guide.md                # 视觉规范
│   ├── animation-guide.md            # 动画模式参考
│   ├── visual-principles.md          # 构图/排版原则
│   ├── mobject-patterns.md           # Mobject 组件食谱
│   ├── script-and-narration.md       # 脚本撰写指南
│   ├── storyboard-template.md        # 分镜格式
│   ├── quality-checklist.md          # QA 清单
│   └── requirements-guide.md         # 需求收集问卷
├── scripts/
│   ├── generate_tts.py           ★   # TTS 旁白生成 + timeline
│   ├── init-project.sh               # 初始化项目
│   ├── render.sh                      # 渲染 + 音频合并
│   ├── render-keyframes.sh           # 关键帧截图
│   └── style-scan.py                 # 代码风格扫描
└── examples/
    └── sky_blue/                 ★   # 示例: "天空为什么是蓝色的"
        ├── main.py                    # 完整场景代码
        ├── config.py                  # 项目配置
        ├── generate_tts.py            # TTS 生成
        └── README.md                  # 示例说明
```

★ = 本次新增的通识科普优化模块

## 工作流概览

```
Phase 1:   需求确认 — 主题/受众/时长/核心收获
Phase 1.5: 核心隐喻设计 ★ — 每个概念找视觉隐喻
Phase 2:   画面叙事设计 ★ — 画面优先，选叙事模式
Phase 2.5: 旁白撰写 ★ — 配合画面写旁白
Phase 3:   视觉设计 — 配色/组件/布局
Phase 4:   动画实现 — Manim 编码 + TTS 对齐
Phase 5:   QA & 渲染 — 风格扫描 + 关键帧审查
```

## 示例: 天空为什么是蓝色的

46 秒科普视频，核心隐喻 **"弹球台"**：
- 大气分子 = 钉子
- 蓝光 = 小弹球（被弹得到处都是）
- 红光 = 大弹球（直接穿过）

1080p30，11 段 TTS 旁白自动对齐。完整代码见 [examples/sky_blue/](examples/sky_blue/)。

## 与其他方案的对比

| 方案 | 控制力 | 中文 | 教育隐喻 | 科普优化 |
| --- | --- | --- | --- | --- |
| **Manim (本 skill)** | ⭐⭐⭐⭐⭐ | ✅ | ⭐⭐⭐⭐⭐ | ✅ |
| Remotion | ⭐⭐⭐ | ⚠️ | ⭐⭐ | ❌ |
| Motion Canvas | ⭐⭐⭐ | ⚠️ | ⭐⭐ | ❌ |
| HTML + SVG | ⭐⭐⭐ | ✅ | ⭐⭐ | ❌ |

## License

MIT
