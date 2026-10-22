import { createRequire } from "node:module";
import { spawn } from "node:child_process";
import http from "node:http";
import fs from "node:fs";
import path from "node:path";

const require = createRequire(import.meta.url);
const { chromium } = require("/Users/mlx/Desktop/IP/finn-video-v2/node_modules/playwright");

const FFMPEG = "/Users/mlx/Desktop/IP/finn-video-v2/.tools/imageio_ffmpeg/binaries/ffmpeg-macos-aarch64-v7.1";
const CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const DIR = "/Users/mlx/Desktop/IP/code-video-works/26-greek-sisyphus";
const MASTER_VIDEO = path.join(DIR, "master_clean.mp4");

const DURATION = 55.0;
const FPS = 30;
const WIDTH = 1080;
const HEIGHT = 1920;
const LOG = path.join(DIR, "render.log");

function log(line) {
  const text = line + "\n";
  fs.appendFileSync(LOG, text);
  process.stdout.write(text);
}

function startServer(port = 8766) {
  const mimeTypes = {
    ".html": "text/html",
    ".js": "text/javascript",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".json": "application/json",
  };
  const server = http.createServer((req, res) => {
    const urlPath = req.url.split("?")[0];
    let filePath = path.join(DIR, urlPath === "/" ? "index.html" : urlPath);
    if (!fs.existsSync(filePath)) {
      res.writeHead(404);
      res.end("Not found");
      return;
    }
    const ext = path.extname(filePath);
    res.writeHead(200, {
      "Content-Type": mimeTypes[ext] || "application/octet-stream",
      "Access-Control-Allow-Origin": "*",
    });
    fs.createReadStream(filePath).pipe(res);
  });
  return new Promise((resolve) => {
    server.listen(port, "127.0.0.1", () => resolve(server));
  });
}

function writeOrWait(stream, buffer) {
  if (stream.write(buffer)) return Promise.resolve();
  return new Promise((resolve, reject) => {
    stream.once("drain", resolve);
    stream.once("error", reject);
  });
}

async function main() {
  fs.writeFileSync(LOG, "");
  log("=== 开始流式渲染：《古希腊神话史诗重构》EP.01 西西弗斯 55s 电影级母版 ===");

  const server = await startServer(8766);
  log("✓ 本地渲染服务器已启动: http://127.0.0.1:8766");

  const browser = await chromium.launch({
    executablePath: CHROME,
    headless: true,
    args: [
      "--use-gl=angle",
      "--use-angle=metal",
      "--enable-webgl",
      "--ignore-gpu-blocklist",
    ],
  });
  const page = await browser.newPage({
    viewport: { width: WIDTH, height: HEIGHT },
    deviceScaleFactor: 1,
  });

  const errors = [];
  page.on("pageerror", (e) => errors.push(String(e)));
  page.on("console", (msg) => {
    if (msg.type() === "error") errors.push(msg.text());
  });

  await page.goto("http://127.0.0.1:8766/index.html?capture=1", { waitUntil: "networkidle" });
  await page.waitForFunction(() => window.__ready === true, { timeout: 15000 });

  if (errors.length) {
    log("WARN: " + errors.join(" | "));
  }

  const totalFrames = Math.round(DURATION * FPS);
  log(`引擎就绪，开始渲染 ${totalFrames} 帧 (1080x1920 @ 30fps)...`);

  const ffmpeg = spawn(FFMPEG, [
    "-y",
    "-f", "image2pipe",
    "-vcodec", "mjpeg",
    "-r", String(FPS),
    "-i", "-",
    "-c:v", "libx264",
    "-pix_fmt", "yuv420p",
    "-preset", "fast",
    "-crf", "16",
    MASTER_VIDEO,
  ], { stdio: ["pipe", "inherit", "inherit"] });

  const canvas = page.locator("#c");
  const startTime = Date.now();
  for (let i = 0; i < totalFrames; i++) {
    const t = i / FPS;
    await page.evaluate((currFrame) => window.renderFrame(currFrame), i);
    const buffer = await canvas.screenshot({ type: "jpeg", quality: 96 });
    await writeOrWait(ffmpeg.stdin, buffer);
    if (i % 60 === 0 || i === totalFrames - 1) {
      const elapsed = (Date.now() - startTime) / 1000;
      const fpsReal = (i + 1) / elapsed;
      const remainingSec = (totalFrames - (i + 1)) / (fpsReal || 1);
      log(`FRAME ${i + 1}/${totalFrames} t=${t.toFixed(2)}s fps=${fpsReal.toFixed(2)} eta=${remainingSec.toFixed(0)}s`);
    }
  }
  ffmpeg.stdin.end();
  await new Promise((resolve, reject) => {
    ffmpeg.on("close", (code) => {
      if (code === 0) resolve();
      else reject(new Error("FFmpeg exited with code " + code));
    });
  });

  const qc = await page.evaluate(() => window.__qcReport());
  log("=== QC 报告 === " + JSON.stringify(qc));

  await browser.close();
  server.close();
  log("MASTER_DONE " + MASTER_VIDEO + " elapsed=" + ((Date.now() - startTime) / 1000).toFixed(1) + "s");
}

main().catch((err) => {
  log("RENDER_FAILED " + (err && err.stack ? err.stack : err));
  process.exit(1);
});
