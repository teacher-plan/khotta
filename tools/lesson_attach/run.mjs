// رفع ملخّصات الدروس وعروضها التفاعلية إلى مرفقات بطاقات الدروس (تشغيلٌ يدوي من GitHub Actions).
// يبني كل ملخّص PDF من مولّده في المستودع (tools/presentations/examples/gen_*_summary.py) ثم يرفعه
// مع العروض إلى user-files بمفتاح الخدمة، ويطبع سطر JSON لكل ملف (المسار والحجم) لتُسجَّل في البطاقات.
import { chromium } from 'playwright';
import { execFileSync } from 'child_process';
import fs from 'fs'; import path from 'path';
const EX = 'tools/presentations/examples';
const items = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const { SUPABASE_URL, SERVICE_KEY } = process.env;
const out = fs.mkdtempSync('/tmp/la-');
const b = await chromium.launch();
let fail = 0;
for (const it of items) {
  try {
    let file;
    if (it.kind === 'pdf') {
      execFileSync('python3', [it.gen], { cwd: EX, stdio: 'pipe' });
      const p = await b.newPage({ deviceScaleFactor: 2, viewport: { width: 900, height: 1200 } });
      await p.goto('file://' + path.resolve(EX, it.html));
      await p.evaluate(() => document.fonts.ready);
      file = path.join(out, it.dest.split('/').pop());
      await p.pdf({ path: file, format: 'A4', printBackground: true, preferCSSPageSize: true });
      await p.close();
    } else file = it.src;
    const body = fs.readFileSync(file);
    const r = await fetch(`${SUPABASE_URL}/storage/v1/object/user-files/${it.dest}`, {
      method: 'POST', body, headers: { Authorization: 'Bearer ' + SERVICE_KEY, apikey: SERVICE_KEY, 'Content-Type': it.ct, 'x-upsert': 'true' } });
    if (!r.ok) throw new Error('upload ' + r.status + ' ' + (await r.text()).slice(0, 200));
    console.log('OK ' + JSON.stringify({ lid: it.lid, kind: it.kind, name: it.name, path: it.dest, size: body.length }));
  } catch (e) { fail++; console.log('FAIL ' + it.lid + ' ' + it.name + ' ' + e.message); }
}
await b.close();
if (fail) process.exit(1);
