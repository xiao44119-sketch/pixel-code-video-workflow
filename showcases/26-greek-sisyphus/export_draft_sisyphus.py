#!/usr/bin/env python3
import json
import os
import sys
import time
import subprocess
from pathlib import Path

SKILL_SCRIPTS = "/Users/mlx/.gemini/config/skills/jianying-draft-export/scripts"
sys.path.insert(0, SKILL_SCRIPTS)
from draft_builder import JianyingDraft

FFMPEG = "/Users/mlx/Desktop/IP/finn-video-v2/.tools/imageio_ffmpeg/binaries/ffmpeg-macos-aarch64-v7.1"
WORK_DIR = "/Users/mlx/Desktop/IP/code-video-works/26-greek-sisyphus"
RAW_VIDEO = os.path.join(WORK_DIR, "master_clean.mp4")
AUDIO_PATH = os.path.join(WORK_DIR, "audio_fish/master_audio_48k.wav")
FINAL_VIDEO = os.path.join(WORK_DIR, "古希腊神话史诗重构_EP01_西西弗斯_对无意义的终极复仇_大片.mp4")
COVER_PATH = os.path.join(WORK_DIR, "cover.png")
SUB_PATH = os.path.join(WORK_DIR, "audio_fish/subtitles.json")

def main():
    print("=== 正在通过电影级原声母带合成成片并注入剪映草稿 ===")
    if not os.path.exists(RAW_VIDEO):
        raise FileNotFoundError(f"Raw video missing: {RAW_VIDEO}")
    if not os.path.exists(AUDIO_PATH):
        raise FileNotFoundError(f"Audio track missing: {AUDIO_PATH}")

    # 1. 音画混流合成完整母版（人声+BGM动态闪避）
    print(f"Muxing {RAW_VIDEO} + {AUDIO_PATH} -> {FINAL_VIDEO}...")
    cmd = [
        FFMPEG, "-y",
        "-i", RAW_VIDEO,
        "-i", AUDIO_PATH,
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "256k",
        "-shortest",
        FINAL_VIDEO
    ]
    subprocess.run(cmd, check=True)
    print(f"✓ Generated final master video: {FINAL_VIDEO}")

    # 2. 检查字幕与封面
    if not os.path.exists(COVER_PATH):
        raise FileNotFoundError(COVER_PATH)
    if not os.path.exists(SUB_PATH):
        raise FileNotFoundError(SUB_PATH)

    with open(SUB_PATH, "r", encoding="utf-8") as f:
        subtitles = json.load(f)

    # 先彻底退出剪映，防止缓存覆盖
    print("Pre-closing any running JianYing instances...")
    subprocess.run(["killall", "-9", "VideoFusion"], stderr=subprocess.DEVNULL)
    subprocess.run(["killall", "-9", "VideoFusion-macOS"], stderr=subprocess.DEVNULL)
    subprocess.run(["killall", "-9", "VideoFusion-macOSTrayHelper"], stderr=subprocess.DEVNULL)
    time.sleep(1.0)

    # 3. 构建剪映自包含工程草稿
    draft_name = "古希腊神话史诗重构_EP01_西西弗斯_对无意义的终极复仇_骁清Finn"
    print(f"Creating JianYing self-contained draft: {draft_name}...")
    draft = JianyingDraft(name=draft_name, width=1080, height=1920)
    draft.set_video(FINAL_VIDEO)
    draft.set_cover(COVER_PATH)

    print("Adding subtitles with dual-color highlights (#ffd76a gold + black outline)...")
    for sub in subtitles:
        draft.add_subtitle(
            text=sub["text"],
            start_sec=sub["start"],
            end_sec=sub["end"],
            highlight=sub.get("hl", "")
        )
        print(f"  + [{sub['start']:.2f}s -> {sub['end']:.2f}s] {sub['text']} (hl={sub.get('hl', '')})")

    # 4. 保存草稿
    draft_folder = draft.save_and_inject(open_app=False)

    # 5. 确保在 root_meta_info.json 中排在第 0 位（最左上角第一个）
    draft_root = Path(os.path.expanduser("~/Movies/JianyingPro/User Data/Projects/com.lveditor.draft"))
    root_meta_file = draft_root / "root_meta_info.json"
    if root_meta_file.exists():
        with open(root_meta_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        store = data.get("all_draft_store", [])
        sisy_item = None
        new_store = []
        for it in store:
            if it.get("draft_name") == draft_name:
                sisy_item = it
            else:
                new_store.append(it)
        now_us = int(time.time() * 1_000_000)
        if sisy_item:
            sisy_item["tm_draft_create"] = now_us
            sisy_item["tm_draft_modified"] = now_us
            new_store.insert(0, sisy_item)
            data["all_draft_store"] = new_store
            data["draft_ids"] = len(new_store)
            with open(root_meta_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False)
            print(f"✓ EP01 已置顶至 root_meta_info 第 0 位 (时间戳: {now_us})")

    # 6. 重新启动剪映
    print("Launching JianYing Pro...")
    subprocess.run(["open", "-a", "/Applications/VideoFusion-macOS.app"])

    print(f"\n==========================================")
    print(f"  SUCCESS: 剪映草稿已成功注入并打开！")
    print(f"  草稿名称: {draft_name}")
    print(f"  草稿路径: {draft_folder}")
    print(f"==========================================")

if __name__ == "__main__":
    main()
