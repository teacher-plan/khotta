// فحص التراكب وتناسق الخط: node overlap.mjs ملف.html [ملف٢ …]
// ١) يكشف كل الخطوات في كل شريحة، ثم يبحث عن نصّين (أو نصّ وصورة) يتراكبان بصرياً، على أربع مقاسات شاشة.
// ٢) يقيس حجم العنوان h2 وحجم النصّ الغالب في كل شريحة (بنسبة ارتفاع الشاشة)، ويبلّغ عن الشرائح الشاذّة عن متوسّط العرض.
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import fs from 'fs';
const files = process.argv.slice(2);
const SIZES = [[1180, 820], [1180, 700], [820, 1000], [1280, 720]];   // iPad Air 11": ملء الشاشة، داخل منصّة «خطة»، عمودي؛ وشاشة حاسوب
const b = await chromium.launch();
for (const f of files) {
  const html = fs.readFileSync(f, 'utf8');
  const name = f.split('/').pop();
  for (const [W, H] of SIZES) {
    const p = await b.newPage({ viewport: { width: W, height: H } });
    await p.route('http://deck.local/**', r => r.fulfill({ contentType: 'text/html', body: html }));
    await p.goto('http://deck.local/x.html'); await p.waitForTimeout(1200);
    const res = await p.evaluate(async () => {
      const slides = [...document.querySelectorAll('.slide')], out = [], fonts = [];
      for (let i = 0; i < slides.length; i++) {
        const s = slides[i];
        slides.forEach(x => { x.style.transition = 'none'; x.classList.toggle('on', x === s); });
        s.querySelectorAll('.st,.st-t').forEach(e => { e.style.transition = 'none'; e.classList.add('in'); });
        s.querySelectorAll('.flip').forEach(e => e.classList.add('open'));
        if (window.__fitAll) window.__fitAll();
        await new Promise(r => setTimeout(r, 60));
        const H = innerHeight, items = [];
        const vis = e => { for (let q = e; q && q !== s.parentElement; q = q.parentElement) { const cs = getComputedStyle(q); if (cs.visibility === 'hidden' || cs.display === 'none' || +cs.opacity === 0) return false; } return !e.closest('.dz,aside,.tnote,[hidden]'); };
        const w = document.createTreeWalker(s, NodeFilter.SHOW_TEXT); let n;
        const sizes = new Map();
        while ((n = w.nextNode())) {
          if (!n.textContent.trim()) continue; const e = n.parentElement; if (!vis(e)) continue;
          const rg = document.createRange(); rg.selectNodeContents(n);
          for (const r of rg.getClientRects()) if (r.width > 2 && r.height > 2) items.push({ e, r, t: n.textContent.trim().slice(0, 18) });
          let k = 1; for (let q = e; q && q !== document.body; q = q.parentElement) { const t = getComputedStyle(q).transform; if (t && t !== 'none') { const m = new DOMMatrix(t); k *= Math.hypot(m.a, m.b); } }
          const vh = Math.round(parseFloat(getComputedStyle(e).fontSize) * k / H * 1000) / 10;
          if (!e.closest('.vcol,.vbox,svg,h2,.qbadge,.tag,.ref,.mode,.timer,.xnum,.tap,.lab,.hint,small,sup,.can-i,.kk')) sizes.set(vh, (sizes.get(vh) || 0) + n.textContent.trim().length);
        }
        s.querySelectorAll('img,svg.svgfig').forEach(e => { if (vis(e)) { const r = e.getBoundingClientRect(); if (r.width > 2) items.push({ e, r, t: '[صورة]' }); } });
        let hit = null;
        for (let a = 0; a < items.length && !hit; a++) for (let c = a + 1; c < items.length; c++) {
          const A = items[a], B = items[c]; if (A.e === B.e || A.e.contains(B.e) || B.e.contains(A.e)) continue;
          if (A.t === '[صورة]' && B.e.closest('svg') === A.e) continue;
          const ox = Math.min(A.r.right, B.r.right) - Math.max(A.r.left, B.r.left), oy = Math.min(A.r.bottom, B.r.bottom) - Math.max(A.r.top, B.r.top);
          if (ox > 4 && oy > Math.min(A.r.height, B.r.height) * 0.35) { hit = `«${A.t}» × «${B.t}»`; break; }
        }
        if (hit) out.push(`${i + 1}: ${hit}`);
        const h2 = s.querySelector('h2'); const h2vh = h2 && vis(h2) ? Math.round(parseFloat(getComputedStyle(h2).fontSize) / H * 1000) / 10 : null;
        const body = [...sizes].sort((x, y) => y[1] - x[1])[0];
        fonts.push([i + 1, h2vh, body ? body[0] : null, s.className]);
      }
      return { out, fonts };
    });
    console.log(`${name} ${W}x${H} ${res.out.length ? 'تراكب: ' + res.out.join(' | ') : 'لا تراكب'}`);
    if (W === 1180 && H === 820) {
      const ex = res.fonts.filter(x => !/cover|divider|launch|exs/.test(x[3]));
      const med = a => { const v = a.filter(x => x != null).sort((p, q) => p - q); return v[Math.floor(v.length / 2)]; };
      const mh = med(ex.map(x => x[1])), mb = med(ex.map(x => x[2]));
      const odd = ex.filter(x => (x[1] && Math.abs(x[1] - mh) / mh > 0.25) || (x[2] && Math.abs(x[2] - mb) / mb > 0.35));
      const exs = res.fonts.filter(x => /exs/.test(x[3])), mx = med(exs.map(x => x[2]));
      const oddx = exs.filter(x => x[2] && Math.abs(x[2] - mx) / mx > 0.35);
      console.log(`  الخط: العنوان ≈ ${mh}vh، النصّ ≈ ${mb}vh، تمارين الملحق ≈ ${mx}vh` +
        (odd.length ? ` · شرائح شاذّة: ${odd.map(x => `${x[0]}(${x[1]}/${x[2]})`).join(' ')}` : ' · متناسق') +
        (oddx.length ? ` · ملحق شاذّ: ${oddx.map(x => `${x[0]}(${x[2]})`).join(' ')}` : ''));
    }
    await p.close();
  }
}
await b.close();
