// يحوّل ورقة الملخّص إلى صور PNG (صفحة لكل صورة، مناسبة لواتساب) + ملف PDF.
// node tools/presentations/sheet.mjs ملف.html مجلد_الإخراج
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import path from 'path';
const [, , file, out] = process.argv;
const b = await chromium.launch();
const p = await b.newPage({ deviceScaleFactor: 2, viewport: { width: 900, height: 1200 } });
await p.goto('file://' + path.resolve(file));
await p.evaluate(() => document.fonts.ready);
const pages = await p.$$('.page');
const base = path.basename(file, '.html');
for (let i = 0; i < pages.length; i++) {
  const over = await pages[i].evaluate(e => e.scrollHeight > e.clientHeight + 1);
  if (over) console.log('OVERFLOW page', i + 1);
  await pages[i].screenshot({ path: path.join(out, `${base}_${i + 1}.png`) });
}
await p.pdf({ path: path.join(out, `${base}.pdf`), format: 'A4', printBackground: true, preferCSSPageSize: true });
await b.close();
console.log('done', pages.length);
