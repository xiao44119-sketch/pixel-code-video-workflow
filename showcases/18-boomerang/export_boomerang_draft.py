#!/usr/bin/env python3
import json
import os
import sys
from pathlib import Path

# 引入 jianying-draft-export 核心模块
SKILL_SCRIPTS = "/Users/mlx/.gemini/config/skills/jianying-draft-export/scripts"
sys.path.insert(0, SKILL_SCRIPTS)
from draft_builder import JianyingDraft

WORK_DIR = "/Users/mlx/Desktop/IP/code-video-works/18-boomerang-v1"
VIDEO_PATH = os.path.join(WORK_DIR, "回旋镖_60s电影级哲学大片.mp4")
COVER_PATH = os.path.join(WORK_DIR, "cover_60s.png")
SUB_PATH = os.path.join(WORK_DIR, "audio/subtitles.json")

def main():
    print("=== 开始构建《回旋镖》剪映 Pro 自包含原生工程草稿 ===")
    
    if not os.path.exists(VIDEO_PATH):
        raise FileNotFoundError(f"成片不存在: {VIDEO_PATH}")
    if not os.path.exists(COVER_PATH):
        raise FileNotFoundError(f"封面不存在: {COVER_PATH}")
    if not os.path.exists(SUB_PATH):
        raise FileNotFoundError(f"字幕文件不存在: {SUB_PATH}")

    with open(SUB_PATH, 'r', encoding='utf-8') as f:
        subtitles = json.load(f)

    draft = JianyingDraft(
        name="回旋镖_时代代价与代际契约_60s哲学大片",
        width=1080,
        height=1920
    )

    # 1. 注入母版视频 (自动探测时长)
    draft.set_video(VIDEO_PATH)

    # 2. 注入封面
    draft.set_cover(COVER_PATH)

    # 3. 注入 7 幕卡点字幕轨（符合 Clean Feed 规范，在剪映独立文本轨道呈现，金白双色高亮）
    for sub in subtitles:
        draft.add_subtitle(
            text=sub['text'],
            start_sec=sub['start'],
            end_sec=sub['end'],
            highlight=sub.get('hl', '')
        )
        print(f"  + 添加字幕 [{sub['start']:.2f}s -> {sub['end']:.2f}s]: {sub['text']} (高亮: {sub.get('hl', '')})")

    # 4. 保存草稿并启动剪映
    draft_folder = draft.save_and_inject(open_app=True)
    print(f"🎉 剪映草稿工程构建并注入成功: {draft_folder}")

if __name__ == '__main__':
    main()
