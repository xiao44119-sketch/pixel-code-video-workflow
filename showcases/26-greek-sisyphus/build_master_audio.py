#!/usr/bin/env python3
import json, subprocess, os
from pathlib import Path

WORK_DIR = Path("/Users/mlx/Desktop/IP/code-video-works/26-greek-sisyphus")
AUDIO_DIR = WORK_DIR / "audio_fish"
BGM_PATH = Path("/Users/mlx/Desktop/IP/assets/audio/bgm_score_v4.wav")
FFMPEG = "/Users/mlx/Desktop/IP/finn-video-v2/.tools/imageio_ffmpeg/binaries/ffmpeg-macos-aarch64-v7.1"

durations = json.loads((AUDIO_DIR / "durations.json").read_text())

# 精准电影级时间轴编排 (总长 55.0 秒)
timeline = [
    # Act 1: 荒谬循环 (0.0 ~ 11.0s)
    {"id": "p0", "start": 0.6},
    {"id": "p1", "start": 4.5},

    # Act 2: 现实打脸 (11.0 ~ 23.0s)
    {"id": "p2", "start": 10.8},
    {"id": "p3", "start": 17.2},

    # Act 3: 觉醒对决 (23.0 ~ 38.0s)
    {"id": "p4", "start": 23.2},
    {"id": "p5", "start": 27.2},
    {"id": "p6", "start": 32.8},

    # Act 4: 终极复仇 (38.0 ~ 55.0s)
    {"id": "p7", "start": 38.8},
    {"id": "p8", "start": 44.0},
    {"id": "p9", "start": 49.0}
]

TOTAL_DURATION = 55.0

def main():
    print(f"=== 开始编排《西西弗斯：对无意义的终极复仇》电影级原声母带 ({TOTAL_DURATION}s) ===")
    
    # 1. 生成字幕与校验卡点
    subtitles = []
    for item in timeline:
        sid = item["id"]
        info = durations[sid]
        start = item["start"]
        dur = info["duration"]
        end = round(start + dur, 2)
        subtitles.append({
            "id": sid,
            "start": start,
            "end": end,
            "text": info["text"],
            "hl": info["hl"],
            "act": info["act"]
        })
        print(f"[{sid}] Act {info['act']} | {start:5.1f}s -> {end:5.1f}s ({dur:4.2f}s) | HL: {info['hl']:6s} | {info['text']}")

    (AUDIO_DIR / "subtitles.json").write_text(json.dumps(subtitles, ensure_ascii=False, indent=2))
    print(f"✓ 字幕时间线已保存: {AUDIO_DIR / 'subtitles.json'}")

    # 2. 合成单声道纯人声轨 (用 adelay + amix 混合)
    filter_complex = []
    inputs = []
    for i, item in enumerate(timeline):
        sid = item["id"]
        inputs.extend(["-i", str(AUDIO_DIR / f"{sid}.mp3")])
        delay_ms = int(item["start"] * 1000)
        filter_complex.append(f"[{i}:a]adelay={delay_ms}|{delay_ms}[a{i}]")
    
    mix_inputs = "".join(f"[a{i}]" for i in range(len(timeline)))
    filter_complex.append(f"{mix_inputs}amix=inputs={len(timeline)}:dropout_transition=0:normalize=0[voice]")
    filter_complex.append(f"[voice]apad=whole_dur={TOTAL_DURATION}[voice_padded]")

    padded_voice = AUDIO_DIR / "voice_padded.wav"
    cmd_voice = [FFMPEG, "-y"] + inputs + [
        "-filter_complex", ";".join(filter_complex),
        "-map", "[voice_padded]",
        "-ar", "48000",
        str(padded_voice)
    ]
    subprocess.run(cmd_voice, check=True)
    print("✓ 拼接全片人声音轨完成:", padded_voice)

    # 3. 人声响度标准化 (I=-16 LUFS)
    norm_voice = AUDIO_DIR / "voice_norm.wav"
    cmd_norm = [
        FFMPEG, "-y",
        "-i", str(padded_voice),
        "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
        "-ar", "48000",
        str(norm_voice)
    ]
    subprocess.run(cmd_norm, check=True)
    print("✓ 人声响度标准化完成 (-16 LUFS):", norm_voice)

    # 4. 终混母带 (混入 BGM，音量 0.15，淡入 1s，淡出 3s)
    master_audio = AUDIO_DIR / "master_audio_48k.wav"
    fade_out_start = TOTAL_DURATION - 3.0
    bgm_filter = f"[1:a]aloop=loop=-1:size=2e+09,volume=0.15,afade=t=in:ss=0:d=1.0,afade=t=out:st={fade_out_start}:d=3.0[bgm];[0:a][bgm]amix=inputs=2:duration=first:dropout_transition=0[master]"
    
    cmd_master = [
        FFMPEG, "-y",
        "-i", str(norm_voice),
        "-i", str(BGM_PATH),
        "-filter_complex", bgm_filter,
        "-map", "[master]",
        "-t", str(TOTAL_DURATION),
        "-ar", "48000",
        str(master_audio)
    ]
    subprocess.run(cmd_master, check=True)
    print(f"\n🏆 48kHz 终混音频母带输出完毕: {master_audio} (时长: {TOTAL_DURATION}s)")

if __name__ == "__main__":
    main()
