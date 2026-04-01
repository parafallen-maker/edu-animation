# Example: 天空为什么是蓝色的

46 秒通识科普视频。

## 核心隐喻

**弹球台** — 大气层是弹球台，空气分子是钉子。

| 隐喻域 | 目标域 |
|--------|--------|
| 弹球台 | 大气层 |
| 钉子 | 空气分子 |
| 小弹球 (被弹得到处都是) | 蓝光 (波长短，被散射) |
| 大弹球 (直接穿过) | 红光 (波长长，穿透) |

## 视频结构

| Beat | 时长 | 内容 | 叙事模式 |
|------|------|------|----------|
| Hook | 5s | 提问 + 否定错误答案 | Misconception Correction |
| Setup | 6s | 白光通过棱镜分解为彩虹 | Before and After |
| Core | 22s | 弹球台隐喻：蓝球 zigzag vs 红球直线 | Compare and Contrast |
| Aha | 6s | 小人仰望，蓝色散射点汇聚为蓝天 | Build Up and Reveal |
| Linger | 4s | "天空的颜色，是光的弹球游戏" | — |

## 运行

```bash
# 1. 安装依赖
pip install manim edge-tts

# 2. 生成 TTS 旁白
cd examples/sky_blue
python3 generate_tts.py

# 3. 低质量预览
manim render main.py WhySkyIsBlue -ql

# 4. 高质量渲染
manim render main.py WhySkyIsBlue -qh --fps 30
```

输出文件：`media/videos/main/1080p30/WhySkyIsBlue.mp4`

## 文件说明

- `main.py` — 主场景代码 (5 段叙事方法)
- `config.py` — 颜色/字体配置
- `generate_tts.py` — TTS 旁白生成 (11 段)
