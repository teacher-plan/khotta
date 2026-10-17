// يرسم صيغاً قصيرة (مثل الجذر بعلامته المعكوسة) صوراً PNG عالية الدقة لإدراجها في Word.
//   node snips.mjs jobs.json   (jobs: {css, items: [{id, html, out}]}) ← يكتب sizes.json بجانب jobs.json
import { chromium } from './pw.mjs';
import fs from 'fs';
import path from 'path';
const jobsPath = process.argv[2];
const jobs = JSON.parse(fs.readFileSync(jobsPath, 'utf8'));
const b = await chromium.launch(process.env.CHROMIUM_PATH ? { executablePath: process.env.CHROMIUM_PATH } : {});
const p = await b.newPage({ deviceScaleFactor: 5 });
await p.setContent(`<!doctype html><html dir="rtl"><head><meta charset="utf-8"><style>${jobs.css}
body{margin:0;background:transparent;font-family:'KDigits','Readex Pro',sans-serif;font-weight:500;font-size:12.5pt;color:#000}
#s{display:inline-block;padding:0 1px;line-height:1.1}</style></head><body><span id="s"></span></body></html>`);
await p.evaluate(() => document.fonts.ready);
const sizes = {};
for (const it of jobs.items) {
  await p.evaluate((h) => { document.getElementById('s').innerHTML = h; }, it.html);
  await p.evaluate(() => document.fonts.ready);
  const el = await p.$('#s');
  const box = await el.boundingBox();
  await el.screenshot({ path: it.out, omitBackground: true });
  sizes[it.id] = [box.width, box.height];
}
fs.writeFileSync(path.join(path.dirname(jobsPath), 'sizes.json'), JSON.stringify(sizes));
await b.close();
