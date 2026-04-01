#!/usr/bin/env python3
"""
TTS narration generator — generates per-segment mp3 files + timeline.json

Usage:
  python3 scripts/generate_tts.py --segments segments.json --output-dir project/audio/narration
  python3 scripts/generate_tts.py --inline '{"hook_1":"天空为什么是蓝色的？","setup_1":"太阳光看起来是白色的。"}'

segments.json format:
  [
    {"id": "hook_1",  "text": "天空为什么是蓝色的？"},
    {"id": "setup_1", "text": "太阳光看起来是白色的。"}
  ]

  or dict format:
  {"hook_1": "天空为什么是蓝色的？", "setup_1": "太阳光看起来是白色的。"}

Output: <output-dir>/
  ├── hook_1.mp3
  ├── setup_1.mp3
  └── timeline.json   ← {"hook_1": {"text": "...", "duration": 2.3, "path": "..."}, ...}
"""
import asyncio
import argparse
import json
import subprocess
import os
import sys

try:
    import edge_tts
except ImportError:
    print("Error: edge-tts not installed. Run: pip install edge-tts", file=sys.stderr)
    sys.exit(1)


DEFAULT_VOICE = "zh-CN-XiaoxiaoNeural"


def get_duration(path: str) -> float:
    """Get audio duration in seconds via ffprobe."""
    result = subprocess.run(
        ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", path],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        raise RuntimeError(f"ffprobe failed on {path}: {result.stderr}")
    info = json.loads(result.stdout)
    return float(info["format"]["duration"])


async def generate_all(segments: list[tuple[str, str]], output_dir: str,
                       voice: str) -> dict:
    os.makedirs(output_dir, exist_ok=True)
    timeline = {}

    for seg_id, text in segments:
        path = os.path.join(output_dir, f"{seg_id}.mp3")
        comm = edge_tts.Communicate(text, voice)
        await comm.save(path)
        dur = get_duration(path)
        timeline[seg_id] = {"text": text, "duration": dur, "path": path}
        print(f"  {seg_id}: {dur:.2f}s — {text}")

    timeline_path = os.path.join(output_dir, "timeline.json")
    with open(timeline_path, "w", encoding="utf-8") as f:
        json.dump(timeline, f, ensure_ascii=False, indent=2)
    print(f"\nTimeline saved to {timeline_path}")
    total = sum(v["duration"] for v in timeline.values())
    print(f"Total narration: {total:.1f}s ({len(segments)} segments)")
    return timeline


def parse_segments(source: str) -> list[tuple[str, str]]:
    """Parse segments from file path or inline JSON string."""
    if os.path.isfile(source):
        with open(source, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = json.loads(source)

    if isinstance(data, list):
        return [(item["id"], item["text"]) for item in data]
    elif isinstance(data, dict):
        return list(data.items())
    else:
        raise ValueError("Segments must be a list of {id, text} or a dict of {id: text}")


def main():
    parser = argparse.ArgumentParser(description="Generate TTS narration segments")
    parser.add_argument("--segments", type=str,
                        help="Path to segments.json or inline JSON string")
    parser.add_argument("--inline", type=str,
                        help="Inline JSON dict: {\"id\": \"text\", ...}")
    parser.add_argument("--output-dir", type=str, default="audio/narration",
                        help="Output directory (default: audio/narration)")
    parser.add_argument("--voice", type=str, default=DEFAULT_VOICE,
                        help=f"Edge TTS voice (default: {DEFAULT_VOICE})")
    args = parser.parse_args()

    source = args.segments or args.inline
    if not source:
        parser.error("Provide --segments <file.json> or --inline '{...}'")

    segments = parse_segments(source)
    asyncio.run(generate_all(segments, args.output_dir, args.voice))


if __name__ == "__main__":
    main()
