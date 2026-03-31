# edu-animation

Manim + Edge TTS + FFmpeg 教育科普视频生成器。

## 特性

- **精确矢量渲染**：Manim 像素级坐标控制，零歧义
- **信息设计组件库**：架构图、流程图、对比表、星型拓扑、数据可视化
- **中文 TTS**：Edge TTS 免费语音合成，男声/女声/旁白
- **视觉反馈循环**：渲染 PNG 帧 → 视觉模型审查 → 自动修复
- **1080p60 输出**：支持 480p / 720p / 1080p / 4K

## 快速开始

```bash
# 安装依赖
brew install cairo ffmpeg
pip install manim edge-tts

# 初始化项目
bash scripts/init-project.sh my-video

# 生成旁白音频
bash scripts/gen-tts.sh my-video "你的旁白文本"

# 编写 Manim 场景代码，使用设计系统组件
# 见 references/design-system.py

# 渲染并合并音频
bash scripts/render.sh my-video --output final.mp4 -qh
```

## 项目结构

```
edu-animation/
├── SKILL.md                          # OpenClaw skill 定义
├── scripts/
│   ├── init-project.sh               # 初始化项目
│   ├── gen-tts.sh                    # TTS 音频生成
│   └── render.sh                     # 渲染 + 音频合并
└── references/
    ├── design-system.py              # 可复用组件库
    ├── manim-patterns.md             # 场景模式参考
    └── troubleshooting.md            # 常见问题
```

## 产出示例

OpenClaw 产品科普视频（8 场景，2:15，1080p60）：

[🎬 openclaw-edu-manim.mp4](https://github.com/parafallen-maker/edu-animation/releases)

## 与其他方案的对比

| 方案 | 控制力 | 中文 | headless | 信息设计精度 |
|------|--------|------|----------|-------------|
| **Manim (本 skill)** | ⭐⭐⭐⭐⭐ | ✅ | ✅ | ⭐⭐⭐⭐⭐ |
| Motion Canvas | ⭐⭐⭐ | ⚠️ | ❌ | ⭐⭐⭐ |
| HTML + SVG | ⭐⭐⭐ | ✅ | ✅ | ⭐⭐⭐ |
| Remotion | ⭐⭐⭐ | ⚠️ | ✅ | ⭐⭐ |

## License

MIT
