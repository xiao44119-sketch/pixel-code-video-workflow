import { createRequire } from 'node:module';
import { spawn, execFileSync } from 'node:child_process';
import { mkdir } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const root = path.dirname(fileURLToPath(import.meta.url));
const require = createRequire(import.meta.url);
const { chromium } = require('/Users/mlx/Desktop/IP/finn-video-v2/node_modules/playwright');

const FFMPEG = '/Users/mlx/Desktop/IP/finn-video-v2/.tools/imageio_ffmpeg/binaries/ffmpeg-macos-aarch64-v7.1';
const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';

const HTML_FILE = path.join(root, '01-dark-finance', 'index_full.html');
const AUDIO_FILE = path.join(root, '01-dark-finance', 'audio_full.wav');
const OUT_DIR = path.join(root, 'output');
const DURATION = 43.0;
const FPS = 30;
const WIDTH = 1920;
const HEIGHT = 1080;

const KEY_TIMES = [
  { t: 2.0, name: "scene01-consensus" },
  { t: 6.0, name: "scene02-seashell" },
  { t: 9.8, name: "scene03-prison-cigarette" },
  { t: 13.5, name: "scene04-fiat-banknotes" },
  { t: 17.5, name: "scene05-mobile-digits" },
  { t: 21.5, name: "scene06-keyboard-code" },
  { t: 25.5, name: "scene07-exchange-medium" },
  { t: 30.0, name: "scene08-resources-products-services" },
  { t: 35.0, name: "scene09-labor-production" },
  { t: 40.0, name: "scene10-income-consumption-circuit" }
];

async function main() {
  await mkdir(OUT_DIR, { recursive: true });
  console.log("Launching Chromium for full 43-second masterwork render...");
  const browser = await chromium.launch({
    executablePath: CHROME,
    headless: true
  });

  const page = await browser.newPage({
    viewport: { width: WIDTH, height: HEIGHT },
    deviceScaleFactor: 1
  });

  await page.goto(pathToFileURL(HTML_FILE).href);
  await page.waitForTimeout(600);

  // Hide UI controls for rendering and stop interactive animation loop
  await page.evaluate(() => {
    if (window.stopAnimation) window.stopAnimation();
    const c = document.getElementById('controls');
    if (c) c.style.display = 'none';
  });

  // 1. Capture All 10 Keyframes Contact Sheet
  console.log("Capturing 10 Scenes Keyframe Contact Sheets...");
  for (const item of KEY_TIMES) {
    await page.evaluate((t) => window.renderFrame(t), item.t);
    const kfPath = path.join(OUT_DIR, `full-${item.name}-${item.t.toFixed(1)}s.png`);
    await page.screenshot({ path: kfPath, type: 'png' });
    console.log(`  Saved: ${path.basename(kfPath)}`);
  }

  // 2. Render Full Video with image2pipe to H.264
  const totalFrames = Math.round(DURATION * FPS);
  const rawVideo = path.join(OUT_DIR, '01-dark-finance-temp.mp4');
  const finalVideo = path.join(OUT_DIR, '01-dark-finance-FULL.mp4');

  console.log(`\nEncoding 43s Video (${totalFrames} frames @ ${FPS}fps)...`);
  const enc = spawn(FFMPEG, [
    '-y',
    '-hide_banner',
    '-loglevel', 'error',
    '-f', 'image2pipe',
    '-framerate', String(FPS),
    '-vcodec', 'png',
    '-i', 'pipe:0',
    '-c:v', 'libx264',
    '-preset', 'fast',
    '-crf', '18',
    '-pix_fmt', 'yuv420p',
    rawVideo
  ], { stdio: ['pipe', 'ignore', 'inherit'] });

  for (let f = 0; f < totalFrames; f++) {
    const curT = f / FPS;
    await page.evaluate((t) => window.renderFrame(t), curT);
    const imgBuffer = await page.screenshot({ type: 'png' });
    enc.stdin.write(imgBuffer);
    if (f % 60 === 0 || f === totalFrames - 1) {
      process.stdout.write(`  Rendered ${f}/${totalFrames} frames (${((f/totalFrames)*100).toFixed(0)}%)\r`);
    }
  }
  enc.stdin.end();

  await new Promise((resolve, reject) => {
    enc.on('close', (code) => {
      if (code === 0) resolve();
      else reject(new Error(`FFmpeg exited with code ${code}`));
    });
  });

  console.log(`\nVideo track rendered: ${rawVideo}`);

  // 3. Merge Audio Track with High Fidelity
  console.log("Multiplexing audio soundtrack with final video...");
  execFileSync(FFMPEG, [
    '-y',
    '-hide_banner',
    '-loglevel', 'error',
    '-i', rawVideo,
    '-i', AUDIO_FILE,
    '-c:v', 'copy',
    '-c:a', 'aac',
    '-b:a', '192k',
    '-t', String(DURATION),
    '-movflags', '+faststart',
    finalVideo
  ]);

  console.log(`\n>>> MASTERPIECE RENDER COMPLETE: ${finalVideo} <<<`);
  await page.close();
  await browser.close();
}

main().catch(err => {
  console.error("Masterwork render failed:", err);
  process.exit(1);
});
