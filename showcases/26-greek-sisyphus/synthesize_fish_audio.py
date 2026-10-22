#!/usr/bin/env python3
import json, asyncio, os, subprocess, re, time
from pathlib import Path
import edge_tts

WORK_DIR = Path("/Users/mlx/Desktop/IP/code-video-works/26-greek-sisyphus")
AUDIO_DIR = WORK_DIR / "audio_fish"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)
FFMPEG = "/Users/mlx/Desktop/IP/finn-video-v2/.tools/imageio_ffmpeg/binaries/ffmpeg-macos-aarch64-v7.1"
VOICE = "zh-CN-YunxiNeural"

segments = [
    # Act 1: 荒谬循环 (0.0 ~ 11.0s)
    {"id": "p0", "text": "巨石，又一次滚落山脚。", "hl": "又一次", "act": 1},
    {"id": "p1", "text": "诸神在云端俯视，以为这是剥夺希望的终极折磨。", "hl": "终极折磨", "act": 1},

    # Act 2: 现实投射 (11.0 ~ 23.0s)
    {"id": "p2", "text": "像极了你日复一日的打卡、搬砖、归零、再来。", "hl": "归零", "act": 2},
    {"id": "p3", "text": "你以为你在赎罪，其实你只是在被无意义吞噬。", "hl": "无意义", "act": 2},

    # Act 3: 觉醒对决 (23.0 ~ 36.0s)
    {"id": "p4", "text": "但所有人都看错了西西弗斯。", "hl": "看错了", "act": 3},
    {"id": "p5", "text": "当他转身走向巨石那一刻，他不再祈求怜悯。", "hl": "不再祈求", "act": 3},
    {"id": "p6", "text": "巨石上的每一道裂痕，都成了他对抗虚无的勋章。", "hl": "勋章", "act": 3},

    # Act 4: 终极复仇 (36.0 ~ 50.0s)
    {"id": "p7", "text": "当你把向上的挣扎本身，当成全部的意义——", "hl": "向上的挣扎", "act": 4},
    {"id": "p8", "text": "诸神的诅咒，就在你面前彻底失效。", "hl": "彻底失效", "act": 4},
    {"id": "p9", "text": "我是骁清Finn，想清楚了，评论区聊聊。", "hl": "骁清Finn", "act": 4}
]

def get_duration(audio_path: Path) -> float:
    cmd = [FFMPEG, "-i", str(audio_path)]
    res = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    m = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.\d+)", res.stderr)
    if m:
        h, mn, s = float(m.group(1)), float(m.group(2)), float(m.group(3))
        return round(h * 3600 + mn * 60 + s, 2)
    return 0.0

async def synth_with_retry(text: str, out_file: Path, retries=5):
    for attempt in range(retries):
        try:
            comm = edge_tts.Communicate(text, VOICE, rate="-4%", pitch="+0Hz")
            await comm.save(str(out_file))
            if out_file.exists() and out_file.stat().st_size > 1000:
                return
        except Exception as e:
            print(f"    [Retry {attempt+1}/{retries}] error: {e}")
            await asyncio.sleep(1.5)
    raise RuntimeError(f"Failed to synthesize: {text}")

async def main_async():
    print(f"=== 开始合成《西西弗斯：对无意义的终极复仇》原声大片音频 ({len(segments)} 句, 音色: {VOICE}) ===")
    durations = {}
    for seg in segments:
        sid = seg["id"]
        out_file = AUDIO_DIR / f"{sid}.mp3"
        if not out_file.exists() or out_file.stat().st_size < 1000:
            print(f"Synthesizing [{sid}] ({seg['text']})...")
            await synth_with_retry(seg["text"], out_file)
            await asyncio.sleep(0.5)
        else:
            print(f"Using cached [{sid}]...")
            
        dur = get_duration(out_file)
        durations[sid] = {
            "text": seg["text"],
            "hl": seg["hl"],
            "act": seg["act"],
            "duration": dur
        }
        print(f"  -> Ready: {out_file.name} (时长: {dur}s)")

    dur_path = AUDIO_DIR / "durations.json"
    dur_path.write_text(json.dumps(durations, ensure_ascii=False, indent=2))
    print(f"\n✓ 全部音频合成完毕，时长映射已保存至: {dur_path}")

if __name__ == "__main__":
    asyncio.run(main_async())
