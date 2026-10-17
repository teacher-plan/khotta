// يرسم صفحات youtube_art.py إلى PNG بالمقاس الدقيق: node snap_art.mjs jobs.json
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import fs from 'fs';
const jobs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const b = await chromium.launch();
for (const [html, png, w, h] of jobs) {
  const p = await b.newPage({ viewport: { width: w, height: h } });
  await p.goto('file://' + html); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(400);
  await p.screenshot({ path: png }); await p.close(); console.log(png.split('/').pop());
}
await b.close();
