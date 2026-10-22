import { createRequire } from "node:module";
import { spawn } from "node:child_process";
import path from "node:path";
import { pathToFileURL } from "node:url";

const require = createRequire(import.meta.url);
const { chromium } = require("/Users/mlx/Desktop/IP/finn-video-v2/node_modules/playwright");

const FFMPEG = "/Users/mlx/Desktop/IP/finn-video-v2/.tools/imageio_ffmpeg/binaries/ffmpeg-macos-aarch64-v7.1";
const CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const DIR = "/Users/mlx/Desktop/IP/code-video-works/18-boomerang-v1";
const HTML_FILE = path.join(DIR, "index.html");
const TEMP_VIDEO = path.join(DIR, "boomerang_master_60s.mp4");
const FINAL_VIDEO = path.join(DIR, "回旋镖_60s电影级哲学大片.mp4");
const VOICE_AUDIO = path.join(DIR, "audio/voice_full.wav");

const DURATION = 60.0;
const FPS = 30;
const WIDTH = 1080;
const HEIGHT = 1920;

async function main() {
  console.log("=== 开始流式渲染：《回旋镖》60s 电影级哲学大片 ===");
  const browser = await chromium.launch({
    executablePath: CHROME,
    headless: true,
    args: ["--allow-file-access-from-files"]
  });

  const page = await browser.newPage({
    viewport: { width: WIDTH, height: HEIGHT },
    deviceScaleFactor: 1
  });

  const fileUrl = pathToFileURL(HTML_FILE).href + "?capture=1";
  console.log("正在加载回旋镖动画引擎:", fileUrl);
  await page.goto(fileUrl);
  await page.waitForFunction(() => window.__ready === true, { timeout: 15000 });
  console.log("✨ 回旋镖确定性数学渲染引擎已完全就绪!");

  const totalFrames = Math.round(DURATION * FPS);
  console.log("🎬 总计 " + totalFrames + " 帧 (60.0s @ 30fps)...");

  const ffmpegArgs = [
    "-y",
    "-f", "image2pipe",
    "-vcodec", "mjpeg",
    "-r", String(FPS),
    "-i", "-",
    "-c:v", "libx264",
    "-pix_fmt", "yuv420p",
    "-preset", "fast",
    "-crf", "16",
    TEMP_VIDEO
  ];

  const ffmpeg = spawn(FFMPEG, ffmpegArgs, { stdio: ["pipe", "inherit", "inherit"] });

  const startTime = Date.now();
  for (let i = 0; i < totalFrames; i++) {
    const t = i / FPS;
    await page.evaluate((currTime) => window.renderFrame(currTime), t);
    const buffer = await page.screenshot({ type: "jpeg", quality: 96 });
    ffmpeg.stdin.write(buffer);

    if (i % 60 === 0 || i === totalFrames - 1) {
      const elapsed = ((Date.now() - startTime) / 1000).toFixed(1);
      const fpsReal = ((i + 1) / ((Date.now() - startTime) / 1000)).toFixed(1);
      const percent = (((i + 1) / totalFrames) * 100).toFixed(1);
      console.log("  🚀 进度: " + (i + 1) + "/" + totalFrames + " 帧 (" + percent + "%) | 动画时间: " + t.toFixed(2) + "s | 耗时: " + elapsed + "s | 渲染速度: " + fpsReal + " fps");
    }
  }

  ffmpeg.stdin.end();

  await new Promise((resolve, reject) => {
    ffmpeg.on("close", (code) => {
      if (code === 0) resolve();
      else reject(new Error("FFmpeg exited with code " + code));
    });
  });

  await browser.close();
  const renderElapsed = ((Date.now() - startTime) / 1000).toFixed(1);
  console.log("母版纯净视频流压制完成! 耗时: " + renderElapsed + "s");

  // 合成 60s 电影级深度配音音轨
  console.log("🎵 开始合成 60s 电影级深度配音音轨...");
  const muxArgs = [
    "-y",
    "-i", TEMP_VIDEO,
    "-i", VOICE_AUDIO,
    "-c:v", "copy",
    "-c:a", "aac",
    "-b:a", "256k",
    "-shortest",
    FINAL_VIDEO
  ];

  const mux = spawn(FFMPEG, muxArgs, { stdio: "inherit" });
  await new Promise((resolve, reject) => {
    mux.on("close", (code) => {
      if (code === 0) resolve();
      else reject(new Error("FFmpeg mux exited with code " + code));
    });
  });

  console.log("🎉 全部压制成功! 最终成片已输出至: " + FINAL_VIDEO);
}

main().catch((err) => {
  console.error("渲染异常中断:", err);
  process.exit(1);
});
