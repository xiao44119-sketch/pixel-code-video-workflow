import { createRequire } from "node:module";
import path from "node:path";
import { pathToFileURL } from "node:url";

const require = createRequire(import.meta.url);
const { chromium } = require("/Users/mlx/Desktop/IP/finn-video-v2/node_modules/playwright");

const CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const DIR = "/Users/mlx/Desktop/IP/code-video-works/18-boomerang-v1";
const HTML_FILE = path.join(DIR, "index.html");

async function main() {
  const browser = await chromium.launch({
    executablePath: CHROME,
    headless: true,
    args: ["--allow-file-access-from-files"]
  });

  const page = await browser.newPage({
    viewport: { width: 1080, height: 1920 },
    deviceScaleFactor: 1
  });

  await page.goto(pathToFileURL(HTML_FILE).href + "?capture=1");
  await page.waitForFunction(() => window.__ready === true);

  const shots = [
    { t: 4.5, name: "shot_01_blackbox.png" },
    { t: 12.5, name: "shot_02_ratio121.png" },
    { t: 20.5, name: "shot_03_scale1752w.png" },
    { t: 30.5, name: "shot_04_ideology_gear.png" },
    { t: 39.0, name: "shot_05_ai_islands.png" },
    { t: 49.0, name: "shot_06_pension_gears.png" },
    { t: 57.5, name: "shot_07_boomerang_close.png" }
  ];

  for (const s of shots) {
    await page.evaluate((time) => window.renderFrame(time), s.t);
    const out = path.join(DIR, s.name);
    await page.screenshot({ path: out, type: "png" });
    console.log("Saved shot:", out);
  }

  await browser.close();
}

main().catch(console.error);
