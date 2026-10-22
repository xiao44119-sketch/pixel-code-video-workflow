#!/usr/bin/env python3
import asyncio
import edge_tts
import subprocess
import json
import os
import re

FFMPEG = '/Users/mlx/Desktop/IP/finn-video-v2/.tools/imageio_ffmpeg/binaries/ffmpeg-macos-aarch64-v7.1'
WORK_DIR = '/Users/mlx/Desktop/IP/code-video-works/18-boomerang-v1'
AUDIO_DIR = os.path.join(WORK_DIR, 'audio')
os.makedirs(AUDIO_DIR, exist_ok=True)

# 60.0s 电影级哲学大片《回旋镖》：7幕卡点口播
# 语速适中微快，既有纪录片的厚重沉思，又有卡点节奏感
segments = [
    {
        'id': 's_0',
        'scene': 0,
        'target_start': 0.30,
        'window_end': 7.60,
        'text': '四十年前，一个选择在黑箱里做出。过程没人看见，后果没人负责。现在，它飞回来了。',
        'hl': '黑箱',
        'rate': '+20%'
    },
    {
        'id': 's_1',
        'scene': 1,
        'target_start': 8.30,
        'window_end': 15.60,
        'text': '偏好、名额、B超，三线叠加。出生性别比从108，冲到121。控制了数量，也控制了性别。',
        'hl': '121',
        'rate': '+38%'
    },
    {
        'id': 's_2',
        'scene': 2,
        'target_start': 16.30,
        'window_end': 24.60,
        'text': '第一把刀，数量：男性多出1752万。当年想要儿子的家庭，如今掏空积蓄，替儿子买一张结婚门票。',
        'hl': '1752万',
        'rate': '+22%'
    },
    {
        'id': 's_3',
        'scene': 3,
        'target_start': 25.30,
        'window_end': 33.60,
        'text': '第二把刀：观念滞后。她们读了更多书，旧规则却没动。韩国性别比早已正常，生育率照样跌到0.72。',
        'hl': '观念滞后',
        'rate': '+25%'
    },
    {
        'id': 's_4',
        'scene': 4,
        'target_start': 34.30,
        'window_end': 43.40,
        'text': '第三把刀，替代：AI把孤独的代价压到接近零。他缺回应，它永远秒回；她怕打扰，它从不越界。两个人，不必再相遇。',
        'hl': '秒回',
        'rate': '+30%'
    },
    {
        'id': 's_5',
        'scene': 5,
        'target_start': 44.30,
        'window_end': 52.50,
        'text': '人人最优，集体退场。养老接力，从2.6比1，滑向1.04比1。让你不想生孩子的AI，或许就是替你交养老金的“孩子”。',
        'hl': '1.04 : 1',
        'rate': '+38%'
    },
    {
        'id': 's_6',
        'scene': 6,
        'target_start': 53.15,
        'window_end': 59.00,
        'text': '要儿子，儿子无妻；养儿防老，无儿可防；最后，自己养自己。回旋镖，落在了下一代。',
        'hl': '回旋镖',
        'rate': '+44%'
    }
]

async def save_with_retry(text, voice, rate, path, max_retries=5):
    for attempt in range(max_retries):
        try:
            comm = edge_tts.Communicate(text, voice, rate=rate)
            await comm.save(path)
            if os.path.exists(path) and os.path.getsize(path) > 1000:
                return
        except Exception as e:
            print(f'Retry {attempt+1} due to: {e}')
            if attempt == max_retries - 1:
                raise
            await asyncio.sleep(1.5 * (attempt + 1))

def get_duration(file_path):
    res = subprocess.run([FFMPEG, '-i', file_path], stderr=subprocess.PIPE, text=True)
    m = re.search(r'Duration: (\d+):(\d+):(\d+\.\d+)', res.stderr)
    if m:
        h, mn, s = m.groups()
        return int(h) * 3600 + int(mn) * 60 + float(s)
    return 0.0

async def main():
    print("=== Generating 60s Boomerang Documentary Voiceover (Precision Zero Overlap) ===")
    subtitles = []
    
    for i, seg in enumerate(segments):
        mp3 = os.path.join(AUDIO_DIR, f"{seg['id']}.mp3")
        print(f"Synthesizing [{seg['id']}]: {seg['text']}")
        await save_with_retry(seg['text'], 'zh-CN-YunyangNeural', seg['rate'], mp3)
        await asyncio.sleep(0.3)
        dur = get_duration(mp3)
        start = seg['target_start']
        end = round(start + dur, 2)
        print(f"  -> Generated {dur:.2f}s | Window: [{start:.2f}s -> {end:.2f}s] (Max: {seg['window_end']}s)")
        if end > seg['window_end']:
            print(f"  [WARNING] Exceeds window by {end - seg['window_end']:.2f}s!")
        else:
            print(f"  [OK] Clean Headroom: {seg['window_end'] - end:.2f}s")
            
        subtitles.append({
            "start": start,
            "end": end,
            "text": seg['text'],
            "hl": seg['hl']
        })

    sub_file = os.path.join(AUDIO_DIR, 'subtitles.json')
    with open(sub_file, 'w', encoding='utf-8') as f:
        json.dump(subtitles, f, ensure_ascii=False, indent=2)
    print(f"Saved subtitles to {sub_file}")

    inputs = []
    filter_parts = []
    for i, seg in enumerate(segments):
        mp3 = os.path.join(AUDIO_DIR, f"{seg['id']}.mp3")
        inputs.extend(['-i', mp3])
        delay_ms = int(seg['target_start'] * 1000)
        filter_parts.append(f"[{i}:a]adelay={delay_ms}|{delay_ms}[a{i}];")
    
    mix_inputs = "".join([f"[a{i}]" for i in range(len(segments))])
    filter_complex = "".join(filter_parts) + f"{mix_inputs}amix=inputs={len(segments)}:normalize=0[mix];[mix]apad=pad_dur=2[out]"
    
    out_wav = os.path.join(AUDIO_DIR, 'voice_full.wav')
    cmd = [
        FFMPEG, '-y',
        *inputs,
        '-filter_complex', filter_complex,
        '-map', '[out]',
        '-t', '60.00',
        '-ar', '48000',
        '-ac', '1',
        out_wav
    ]
    subprocess.run(cmd, check=True)
    full_dur = get_duration(out_wav)
    print(f"Successfully generated full audio: {out_wav} (Duration: {full_dur:.2f}s)")

if __name__ == '__main__':
    asyncio.run(main())
