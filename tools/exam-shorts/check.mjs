// فحص الجودة البصرية قبل التصيير (إلزامي): لا تراكب، لا خروج عن المنطقة الآمنة، لا نصّ يفيض عن إطاره.
// node check.mjs حلقة.html [مجلد_اللقطات]   ← يطبع كل مشكلة، ويخرج برمز 1 إن وُجدت. ويحفظ لقطة نهاية كل مشهد إن أُعطي مجلد.
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import fs from 'fs';
const [f, shots] = process.argv.slice(2);
const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 540, height: 960 } });
const html = fs.readFileSync(f, 'utf8');
await p.route('http://deck.local/**', r => r.fulfill({ contentType: 'text/html', body: html }));
await p.goto('http://deck.local/x.html'); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(400);
await p.evaluate(() => window.relayout && window.relayout());
const D = await p.evaluate(() => window.DURS);
let bad = 0;
for (let i = 0; i < D.length; i++) {
  // نهاية المشهد: كل العناصر ظاهرة في أماكنها النهائية
  await p.evaluate(([i, t]) => window.seek(i, t), [i, D[i] - 30]);
  const probs = await p.evaluate(() => {
    const SAFE = { l: 14, r: 526, t: 70, b: 800 };
    const sc = document.querySelector('.scene.on');
    const sel = '.card,.row,.steprow,.pill,.ans,.title,.mark,.pvbox,.pvlab,.pvsep,.note,img,.math,[data-t],[data-check]';
    const els = [...sc.querySelectorAll(sel)].filter(e => {
      let x = e; while (x && x !== sc) { const cs = getComputedStyle(x); if (cs.display === 'none' || +cs.opacity === 0) return false; x = x.parentElement; }
      if (e.closest('[data-deco]')) return false; // زينة مقصودة (خطّ تحت عنوان)
      const r = e.getBoundingClientRect(); return r.width > 2 && r.height > 2;
    });
    const name = e => (e.className && typeof e.className === 'string' ? '.' + e.className.split(' ')[0] : e.tagName) + ' «' + (e.textContent || '').trim().slice(0, 24) + '»';
    const out = [];
    const R = els.map(e => e.getBoundingClientRect());
    els.forEach((e, k) => {
      const r = R[k];
      if (r.left < SAFE.l - 0.5 || r.right > SAFE.r + 0.5 || r.top < SAFE.t - 0.5 || r.bottom > SAFE.b + 0.5)
        out.push(`خارج المنطقة الآمنة: ${name(e)} [${Math.round(r.left)},${Math.round(r.top)} – ${Math.round(r.right)},${Math.round(r.bottom)}]`);
      if (e.scrollWidth > e.clientWidth + 1 && getComputedStyle(e).overflow !== 'visible' || (e.matches('.pill,.mark,.pvlab,.pvbox') && e.scrollWidth > e.clientWidth + 1))
        out.push(`نصّ يفيض عن إطاره: ${name(e)}`);
    });
    // سطرٌ واحد: رؤوس الأسئلة والشارات وخطوات الحل لا تلتفّ (الكسور العمودية مستثناة)
    sc.querySelectorAll('.qhd b,.mark,.steprow>span:last-child,.nw,.ans,.wrongbox,.pill').forEach(e => {
      if (e.querySelector('.frac')) return;
      const rg = document.createRange(); rg.selectNodeContents(e);
      const fs = parseFloat(getComputedStyle(e).fontSize);
      const tops = [...rg.getClientRects()].filter(q => q.width > 1).map(q => q.top);
      const lines = tops.sort((x, y) => x - y).reduce((n, t, k, a) => n + (k && t - a[k - 1] > fs * 0.8 ? 1 : 0), tops.length ? 1 : 0);
      if (lines > 1) out.push(`نصّ التفّ على سطرين: ${name(e)}`);
    });
    // رأس السؤال: بين العنوان وشارة الدرجة ١٢ بكسل على الأقل
    sc.querySelectorAll('.qhd').forEach(h => { const b = h.querySelector('b'), m = h.querySelector('.mark'); if (!b || !m) return;
      const gap = b.getBoundingClientRect().left - m.getBoundingClientRect().right;
      if (gap < 12) out.push(`رأس مزدحم: ${name(b)} (${Math.round(gap)} بكسل)`); });
    // الزينة (الدفاتر والأقلام والدوائر) لا تلمس المحتوى ولا الشارة العلوية
    const deco = [...document.querySelectorAll('.doodle,.blob,.ring')];
    const tag = document.querySelector('#top .tag');
    deco.forEach(d => { const q = d.getBoundingClientRect();
      [...els, tag].forEach(e => { const r = e.getBoundingClientRect();
        const w = Math.min(r.right, q.right) - Math.max(r.left, q.left), h = Math.min(r.bottom, q.bottom) - Math.max(r.top, q.top);
        if (w > 1.5 && h > 1.5) out.push(`زينة فوق المحتوى: ${d.className.baseVal || d.className} ✕ ${name(e)}`); }); });
    for (let a = 0; a < els.length; a++) for (let c = a + 1; c < els.length; c++) {
      const x = els[a], y = els[c];
      if (x.contains(y) || y.contains(x)) continue;
      const r = R[a], s = R[c];
      const w = Math.min(r.right, s.right) - Math.max(r.left, s.left), h = Math.min(r.bottom, s.bottom) - Math.max(r.top, s.top);
      if (w > 1.5 && h > 1.5) out.push(`تراكب: ${name(x)} ✕ ${name(y)} (${Math.round(w)}×${Math.round(h)})`);
    }
    return out;
  });
  if (shots) await p.screenshot({ path: `${shots}/s${i + 1}.png` });
  probs.forEach(m => { bad++; console.log(`مشهد ${i + 1}: ${m}`); });
}
await b.close();
console.log(bad ? `✗ ${bad} مشكلة` : '✓ لا تراكب ولا خروج ولا فيض في كل المشاهد');
process.exit(bad ? 1 : 0);
