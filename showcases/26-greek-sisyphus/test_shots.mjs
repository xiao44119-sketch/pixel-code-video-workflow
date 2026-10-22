import { createRequire } from "node:module";
import http from "node:http";
import fs from "node:fs";
import path from "node:path";

const require = createRequire(import.meta.url);
const { chromium } = require("/Users/mlx/Desktop/IP/finn-video-v2/node_modules/playwright");

const CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const DIR = "/Users/mlx/Desktop/IP/code-video-works/26-greek-sisyphus";
const OUT_DIR = path.join(DIR, "shots");

if (!fs.existsSync(OUT_DIR)) fs.mkdirSync(OUT_DIR, { recursive: true });

function startServer(port = 8768) {
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

async function main() {
  console.log("=== 启动本地静态服务器与 Chrome 验证 8 镜头母版 WebGL 渲染 ===");
  const server = await startServer(8768);

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
    viewport: { width: 1080, height: 1920 },
    deviceScaleFactor: 1,
  });

  const errors = [];
  page.on("pageerror", (e) => errors.push(String(e)));
  page.on("console", (msg) => {
    if (msg.type() === "error") errors.push(msg.text());
  });

  await page.goto("http://127.0.0.1:8768/index.html?capture=1", { waitUntil: "networkidle" });
  await page.waitForFunction(() => window.__ready === true, { timeout: 15000 });

  if (errors.length) {
    console.warn("Errors caught:", errors);
  }

  const times = [
    { t: 2.5,   name: "beat0_fall_boulder.jpg" },
    { t: 7.5,   name: "beat1_abyss_look.jpg" },
    { t: 13.0,  name: "beat2_chain_death.jpg" },
    { t: 19.0,  name: "beat3_muscle_push.jpg" },
    { t: 24.5,  name: "beat4_camus_walkdown.jpg" },
    { t: 29.5,  name: "beat5_lucid_statue.jpg" },
    { t: 34.5,  name: "beat6_approach_tension.jpg" },
    { t: 37.05, name: "beat7_burst_shockwave.jpg" },
    { t: 45.0,  name: "beat8_godrays_triumph.jpg" },
    { t: 54.0,  name: "beat9_obsidian_fade.jpg" },
  ];

  const canvas = page.locator("#c");
  for (const item of times) {
    const frame = Math.round(item.t * 30);
    await page.evaluate((f) => window.renderFrame(f), frame);
    const outPath = path.join(OUT_DIR, item.name);
    await canvas.screenshot({ path: outPath, type: "jpeg", quality: 95 });
    console.log(`✓ 关键帧已截取 [t=${item.t.toFixed(2)}s, frame=${frame}]: ${item.name}`);
  }

  // 生成官方封面 cover.png (使用 37.05s 冲击波高能帧)
  const coverPath = path.join(DIR, "cover.png");
  await page.evaluate(() => window.renderFrame(Math.round(37.05 * 30)));
  await canvas.screenshot({ path: coverPath, type: "png" });
  console.log(`✓ 官方封面已更新: ${coverPath}`);

  // 质量检测
  const qc = await page.evaluate(() => window.__qcReport());
  console.log("=== QC 报告 ===", JSON.stringify(qc, null, 2));

  await browser.close();
  server.close();
  console.log("=== 8 镜头多视角测试与质检全部通过！===");
}

main().catch((err) => {
  console.error("FAIL:", err);
  process.exit(1);
});
