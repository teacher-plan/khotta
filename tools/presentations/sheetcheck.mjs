// فحص ورقة الملخّص قبل التسليم: node sheetcheck.mjs ملخص.html
// ١) تراكب: نصّان (أو نصّ وجدول) يتقاطعان بصرياً في الصفحة نفسها.
// ٢) رصّ: سطرٌ متعدّد الأسطر تباعده أقلّ من ١٫٥ من حجم خطّه، أو فقرةٌ نثرية أطول من سطرين.
// ٣) خروج: محتوى أطول من الصفحة.
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import path from 'path';
const b = await chromium.launch();
for (const f of process.argv.slice(2)) {
  const p = await b.newPage({ viewport: { width: 900, height: 1200 } });
  await p.goto('file://' + path.resolve(f));
  await p.evaluate(() => document.fonts.ready);
  const res = await p.evaluate(() => {
    const out = [];
    document.querySelectorAll('.page').forEach((pg, pi) => {
      const P = pi + 1;
      if (pg.scrollHeight > pg.clientHeight + 1) out.push(`ص${P}: المحتوى أطول من الصفحة`);
      const items = [], w = document.createTreeWalker(pg, NodeFilter.SHOW_TEXT); let n;
      while ((n = w.nextNode())) {
        if (!n.textContent.trim()) continue;
        const rg = document.createRange(); rg.selectNodeContents(n);
        for (const r of rg.getClientRects()) if (r.width > 2 && r.height > 2) items.push({ e: n.parentElement, r, t: n.textContent.trim().slice(0, 16) });
      }
      for (let a = 0; a < items.length; a++) for (let c = a + 1; c < items.length; c++) {
        const A = items[a], B = items[c]; if (A.e === B.e || A.e.contains(B.e) || B.e.contains(A.e)) continue;
        const ox = Math.min(A.r.right, B.r.right) - Math.max(A.r.left, B.r.left), oy = Math.min(A.r.bottom, B.r.bottom) - Math.max(A.r.top, B.r.top);
        if (ox > 3 && oy > Math.min(A.r.height, B.r.height) * 0.35) { out.push(`ص${P}: تراكب «${A.t}» × «${B.t}»`); a = items.length; break; }
      }
      const seen = new Set(), paras = new Map();
      const w2 = document.createTreeWalker(pg, NodeFilter.SHOW_TEXT); let m;
      while ((m = w2.nextNode())) {
        if (!m.textContent.trim()) continue;
        const e = m.parentElement, rg = document.createRange(); rg.selectNodeContents(m);
        const tops = new Set([...rg.getClientRects()].filter(r => r.width > 2).map(r => Math.round(r.top)));
        if (tops.size < 2) continue;
        const cs = getComputedStyle(e), fs = parseFloat(cs.fontSize), lh = cs.lineHeight === 'normal' ? fs * 1.2 : parseFloat(cs.lineHeight);
        if (lh / fs < 1.5 && !seen.has(P)) { seen.add(P); out.push(`ص${P}: تباعد أسطر ضيّق (${(lh / fs).toFixed(2)}) في «${m.textContent.trim().slice(0, 20)}»`); }
        const blk = e.closest('p,li,td'); if (blk) paras.set(blk, Math.max(paras.get(blk) || 0, tops.size));
      }
      for (const [blk, k] of paras) if (blk.tagName === 'P' && k > 2) out.push(`ص${P}: فقرة من ${k} أسطر «${blk.textContent.trim().slice(0, 20)}…»`);
    });
    return out;
  });
  console.log(path.basename(f), res.length ? '\n  ' + res.join('\n  ') : 'نظيف');
  await p.close();
}
await b.close();
