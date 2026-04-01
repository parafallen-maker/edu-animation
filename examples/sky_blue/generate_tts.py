"""
预生成 TTS 旁白 — 用 edge-tts 生成每段旁白音频，并用 ffprobe 记录时长
"""
import asyncio
import json
import subprocess
import os
import edge_tts

VOICE = "zh-CN-XiaoxiaoNeural"
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "audio", "narration")

SEGMENTS = [
    ("hook_1",    "天空为什么是蓝色的？"),
    ("hook_2",    "不是因为大海的倒影。"),
    ("setup_1",   "太阳光看起来是白色的。"),
    ("setup_2",   "但它其实是各种颜色混在一起。"),
    ("core_1",    "现在想象一下，大气层是一个巨大的弹球台。"),
    ("core_2",    "空气中的分子，就是上面密密麻麻的小钉子。"),
    ("core_3",    "蓝光的波长短，就像一个小弹球。碰到钉子就被弹得到处都是。"),
    ("core_4",    "而红光的波长长，就像一个大弹球。钉子根本挡不住它，直接穿过去了。"),
    ("aha_1",     "所以你抬头看到的蓝色。"),
    ("aha_2",     "就是被弹得满天都是的蓝光。"),
    ("ending",    "天空的颜色，是光的弹球游戏。"),
]


def get_duration(path: str) -> float:
    result = subprocess.run(
        ["ffprobe", "-v", "quiet", "-print_format", "json",
         "-show_format", path],
        capture_output=True, text=True
    )
    info = json.loads(result.stdout)
    return float(info["format"]["duration"])


async def generate_all():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    timeline = {}

    for seg_id, text in SEGMENTS:
        path = os.path.join(OUTPUT_DIR, f"{seg_id}.mp3")
        comm = edge_tts.Communicate(text, VOICE)
        await comm.save(path)
        dur = get_duration(path)
        timeline[seg_id] = {"text": text, "duration": dur, "path": path}
        print(f"  {seg_id}: {dur:.2f}s — {text}")

    timeline_path = os.path.join(OUTPUT_DIR, "timeline.json")
    with open(timeline_path, "w", encoding="utf-8") as f:
        json.dump(timeline, f, ensure_ascii=False, indent=2)
    print(f"\nTimeline saved to {timeline_path}")
    return timeline


if __name__ == "__main__":
    asyncio.run(generate_all())
