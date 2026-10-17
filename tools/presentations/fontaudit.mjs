// تدقيق وضوح الخط: لكل شريحة (مكشوفة الخطوات) أصغر خطٍّ ظاهر بنسبة ارتفاع الشاشة (vh).
// node fontaudit.mjs ملف.html [الحدّ الأدنى بالـvh، الافتراضي 4]
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import fs from 'fs';
const [f, minArg] = process.argv.slice(2); const MIN = +(minArg || 4);
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 1180, height: 820 } });
await p.setContent(fs.readFileSync(f, 'utf8')); await p.waitForTimeout(500);
const r = await p.evaluate((MIN) => {
  const H = innerHeight, out = []; let worst = 99;
  document.querySelectorAll('.slide').forEach((s, i) => {
    document.querySelectorAll('.slide').forEach(x => { x.style.transition = 'none'; x.classList.toggle('on', x === s); });
    s.querySelectorAll('.st,.st-t').forEach(e => { e.style.transition = 'none'; e.classList.add('in'); });
    s.querySelectorAll('.flip,.sq').forEach(e => e.classList.add('open'));
    const small = new Map();
    const w = document.createTreeWalker(s, NodeFilter.SHOW_TEXT);
    let n; while ((n = w.nextNode())) {
      if (!n.textContent.trim()) continue;
      const e = n.parentElement; const cs = getComputedStyle(e);
      if (cs.visibility === 'hidden' || e.closest('[hidden],.bar,.cnt,.dz,[aria-hidden="true"]') ) continue;
      const rg = document.createRange(); rg.selectNodeContents(n); const rc = rg.getBoundingClientRect(); if (!rc.width) continue;
      // الحجم الفعلي بعد أي تصغير (transform): النسبة بين العرض المرسوم والعرض المنطقي
      let k = 1, q = e; while (q && q !== document.body) { const t = getComputedStyle(q).transform; if (t && t !== 'none') { const m = new DOMMatrix(t); k *= Math.hypot(m.a, m.b); } q = q.parentElement; }
      const vh = parseFloat(cs.fontSize) * k / H * 100;
      if (vh < MIN - 0.05) { const key = n.textContent.trim().slice(0, 30); small.set(key, Math.min(small.get(key) || 99, vh)); }
      worst = Math.min(worst, vh);
    }
    if (small.size) out.push((i + 1) + ': ' + [...small].sort((a, b) => a[1] - b[1]).slice(0, 6).map(([t, v]) => v.toFixed(1) + '«' + t + '»').join('  '));
  });
  return { out, worst: worst.toFixed(2) };
}, MIN);
console.log(f.split('/').pop(), 'أصغر خط:', r.worst + 'vh'); r.out.forEach(l => console.log('  ' + l));
await b.close();
