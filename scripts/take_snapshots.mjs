import { createRequire } from 'node:module';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const root = path.dirname(fileURLToPath(import.meta.url));
const require = createRequire(import.meta.url);
const { chromium } = require('/Users/mlx/Desktop/IP/finn-video-v2/node_modules/playwright');

const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const HTML_FILE = path.join(root, '03-geo-monopoly', 'index.html');
const OUT_DIR = path.join(root, 'output');

async function run() {
  const browser = await chromium.launch({ executablePath: CHROME, headless: true });
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  await page.goto(pathToFileURL(HTML_FILE).href);
  await page.waitForFunction(() => window.__assetsLoaded === true, { timeout: 15000 }).catch(() => {});
  await page.waitForTimeout(500);

  await page.evaluate(() => {
    if (window.stopAnimation) window.stopAnimation();
    const c = document.getElementById('controls');
    if (c) c.style.display = 'none';
  });

  const testTimes = [
    { t: 3.5, name: 's01_chaos' },
    { t: 6.2, name: 's01_laser' },
    { t: 10.5, name: 's01_orb' },
    { t: 16.5, name: 's02_grid' },
    { t: 24.5, name: 's02_probe' },
    { t: 33.5, name: 's02_void' },
    { t: 41.5, name: 's03_slash' },
    { t: 47.5, name: 's03_docking' },
    { t: 54.5, name: 's03_shields' },
    { t: 61.5, name: 's04_aerial' },
    { t: 68.5, name: 's04_vortex' },
    { t: 74.5, name: 's04_certainty' }
  ];

  for (const item of testTimes) {
    await page.evaluate((t) => window.renderFrame(t), item.t);
    const p = path.join(OUT_DIR, `snap_${item.name}.png`);
    await page.screenshot({ path: p, type: 'png' });
    console.log(`Saved: snap_${item.name}.png`);
  }

  await browser.close();
}

run().catch(console.error);
