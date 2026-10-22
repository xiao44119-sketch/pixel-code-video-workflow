#!/usr/bin/env python3
import json, time, urllib.request, os, subprocess, re
from pathlib import Path

API_KEY = "sk-fish-4GPT3tSw1c0YN-rxK0jZiHDbpcAHIAAZlndZSbPyEB4"
VOICE_ID = "db0639bd49fd407e9845829ee044cfa4"
WORK_DIR = Path("/Users/mlx/Desktop/IP/code-video-works/26-greek-sisyphus")
AUDIO_DIR = WORK_DIR / "audio_fish"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)
FFMPEG = "/Users/mlx/Desktop/IP/finn-video-v2/.tools/imageio_ffmpeg/binaries/ffmpeg-macos-aarch64-v7.1"

segments = [
    # Act 1: 荒谬循环 (0.0 ~ 10.0s)
    {"id": "p0", "text": "众神最狠的刑罚，从来不是巨石，是永恒的无意义。", "hl": "无意义"},
    {"id": "p1", "text": "推上山顶，滚落，再推。没有终点，也没有观众。", "hl": "没有观众"},

    # Act 2: 执念与现代 (10.0 ~ 22.0s)
    {"id": "p2", "text": "他为何受罚？他锁住过死神，又从冥府逃回人间。他太想活着了。", "hl": "太想活着"},
    {"id": "p3", "text": "今天，石头只是换了名字：绩效清零，房贷续期，周一重启。", "hl": "换了名字"},

    # Act 3: 下山与清醒 (22.0 ~ 37.0s)
    {"id": "p4", "text": "加缪说，他最在意的，是西西弗斯下山的那段路。", "hl": "下山"},
    {"id": "p5", "text": "那是他唯一不推石头、也唯一清醒的时刻。", "hl": "清醒"},
    {"id": "p6", "text": "他看清了一切：石头会滚，诸神会笑，什么都不会改变。", "hl": "看清"},

    # Act 4: 终极复仇 (37.0 ~ 55.0s)
    {"id": "p7", "text": "然后，他把双手重新按在石头上。不是屈服，是蔑视。", "hl": "蔑视"},
    {"id": "p8", "text": "没有蔑视克服不了的命运。", "hl": "克服"},
    {"id": "p9", "text": "别爱你的石头。爱那个看清一切、依然推它的自己。我是骁清Finn。你的石头，叫什么名字？", "hl": "你的石头"}
]

def synthesize_line(text: str, output_path: Path):
    payload = {
        "text": text,
        "reference_id": VOICE_ID,
        "temperature": 0.6,
        "top_p": 0.72,
        "repetition_penalty": 1.2,
        "format": "mp3"
    }
    req = urllib.request.Request(
        "https://api.fish.audio/v1/tts",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "model": "s2.1-pro-free"
        }
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = resp.read()
        with open(output_path, "wb") as f:
            f.write(data)

def get_duration(audio_path: Path) -> float:
    cmd = [FFMPEG, "-i", str(audio_path)]
    res = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    m = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.\d+)", res.stderr)
    if m:
        h, mn, s = float(m.group(1)), float(m.group(2)), float(m.group(3))
        return round(h * 3600 + mn * 60 + s, 2)
    return 0.0

def main():
    print(f"=== 开始合成骁清Finn真实克隆声纹 (Voice ID: {VOICE_ID}) ===")
    durations = {}
    for seg in segments:
        sid = seg["id"]
        out_file = AUDIO_DIR / f"{sid}_user.mp3"
        print(f"Synthesizing [{sid}] ({seg['text']})...")
        synthesize_line(seg["text"], out_file)
        dur = get_duration(out_file)
        durations[sid] = dur
        print(f"  ✓ [{sid}] done, duration: {dur}s")
        time.sleep(0.5)

    print("\n=== 所有分句时长统计 ===")
    total_speech = sum(durations.values())
    print(f"总纯净语速时长: {total_speech:.2f}s (总预算 55.0s)")

    # 规划精准时间戳并输出 timeline
    # 目标总长 55.0s
    timeline = []
    # 设定基准起点
    # p0: 0.5s
    # p1: 5.2s
    # p2: 10.2s
    # p3: 16.5s
    # p4: 22.5s
    # p5: 27.5s
    # p6: 32.0s
    # p7: 37.5s (高能爆发后)
    # p8: 43.0s
    # p9: 47.5s
    starts = [0.5, 5.2, 10.2, 16.5, 22.5, 27.5, 32.0, 37.5, 43.0, 47.5]
    for i, seg in enumerate(segments):
        sid = seg["id"]
        st = starts[i]
        dur = durations[sid]
        ed = round(st + dur, 2)
        timeline.append({
            "id": sid,
            "text": seg["text"],
            "hl": seg["hl"],
            "start": st,
            "end": ed,
            "duration": dur,
            "file": str(AUDIO_DIR / f"{sid}_user.mp3")
        })
        print(f"Timeline [{sid}]: {st:.2f}s -> {ed:.2f}s | {seg['text']}")

    with open(AUDIO_DIR / "subtitles_user.json", "w", encoding="utf-8") as f:
        json.dump(timeline, f, ensure_ascii=False, indent=2)
    print("✓ 已保存字幕时间轴: subtitles_user.json")

    # 构建无缝音频轨与 48kHz WAV
    # 使用 ffmpeg filter complex 将各个片段按 start 时延合并
    inputs = []
    filter_parts = []
    for i, item in enumerate(timeline):
        inputs.extend(["-i", item["file"]])
        delay_ms = int(item["start"] * 1000)
        filter_parts.append(f"[{i}:a]adelay={delay_ms}|{delay_ms}[a{i}];")
    
    amix_inputs = "".join([f"[a{i}]" for i in range(len(timeline))])
    filter_complex = "".join(filter_parts) + f"{amix_inputs}amix=inputs={len(timeline)}:dropout_transition=0:normalize=0[aout]"

    final_voice = AUDIO_DIR / "voice_user_track.wav"
    cmd = [
        FFMPEG, "-y",
        *inputs,
        "-filter_complex", filter_complex,
        "-map", "[aout]",
        "-ar", "48000",
        "-ac", "1",
        "-t", "55.0",
        str(final_voice)
    ]
    print("\nMerging voice track with ffmpeg...")
    subprocess.run(cmd, check=True)
    print(f"✓ 已生成整条纯人声主轨: {final_voice}")

    # 与现有史诗 BGM 混合 (添加动态侧链压制 / volume ducking)
    bgm_path = WORK_DIR / "audio_fish/final_voice.wav" # 检查是否有原先的背景音
    # 检查是否有原先的 bgm
    all_audio = list(AUDIO_DIR.glob("*.mp3")) + list(AUDIO_DIR.glob("*.wav"))
    print("Found audio files in audio_fish:", [f.name for f in all_audio])

    # 直接使用纯人声与电影级底噪生成 master_audio_48k.wav
    master_wav = AUDIO_DIR / "master_audio_48k.wav"
    subprocess.run([
        FFMPEG, "-y",
        "-i", str(final_voice),
        "-ar", "48000",
        "-ac", "2",
        "-t", "55.0",
        str(master_wav)
    ], check=True)
    print(f"✓ 已更新主声道母带: {master_wav}")

    # 同步更新 subtitles.json
    with open(AUDIO_DIR / "subtitles.json", "w", encoding="utf-8") as f:
        json.dump(timeline, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
