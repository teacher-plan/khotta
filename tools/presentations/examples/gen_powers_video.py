# يبني صفحة HTML مستقلة لمشاهد فيديو «القوى والجذور» من مصدر التصميم (.dc.html)، ثم:
# node tools/presentations/video.mjs examples/فيديو_القوى_والجذور.html examples/صوت examples/فيديو_القوى_والجذور.mp4
# لدرسٍ آخر: python3 gen_powers_video.py <مصدر>.dc.html <مجلد_الصوت> <خرج>.html
import os, re, json, sys
HERE = os.path.dirname(os.path.abspath(__file__)); KIT = os.path.dirname(HERE)
DC, AUD, OUT = (sys.argv[1:4] if len(sys.argv) > 3 else ('فيديو_القوى_والجذور.dc.html', 'صوت', 'فيديو_القوى_والجذور.html'))
src = open(os.path.join(HERE, DC), encoding='utf-8').read()
H1, H2 = re.findall(r'<div style="font-size: (?:22px; font-weight: 700|18px; opacity: \.85)">(.*?)</div>', src)[:2]
css = re.search(r'<style>(.*?)</style>', src, re.S).group(1)
css = css.replace("'Readex Pro','Cairo'", "'Readex Pro','KDigits'").replace("font-family:'Cairo'", "font-family:'KDigits'")
LISTS = {'sq': [{'d': 500 + i * 60} for i in range(25)], 'layers': [{'d': 3400 + i * 300} for i in range(5)]}
def expand(m):
    items, var, body = LISTS[m.group(1)], m.group(2), m.group(3)
    return ''.join(re.sub(r'\{\{' + var + r'\.(\w+)\}\}', lambda k: str(it[k.group(1)]), body) for it in items)
scenes = []
for n, body in re.findall(r'<sc-if value="\{\{s(\d)\}\}"[^>]*>(.*?)</sc-if>', src, re.S):
    body = re.sub(r'<sc-for list="\{\{(\w+)\}\}" as="(\w+)"[^>]*>(.*?)</sc-for>', expand, body, flags=re.S)
    scenes.append(f'<section class="sc" style="display:none">{body}</section>')
durs = json.load(open(os.path.join(HERE, AUD, 'durations.json')))['durations']
dots = ''.join('<i class="dt"></i>' for _ in scenes)
html = f'''<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><title>{H1}</title><style>
{open(os.path.join(KIT, 'fonts.css'), encoding='utf-8').read()}
{css}
.sc{{flex-direction:column;align-items:center;justify-content:center}}
.dt{{width:14px;height:14px;border-radius:7px;background:#C9D6E8;display:block}}.dt.on{{background:#C7361B;width:34px}}
</style></head><body>
<div class="stage" dir="rtl" style="width:1280px;height:720px;box-sizing:border-box;position:relative;overflow:hidden;display:flex;flex-direction:column">
<div style="height:64px;flex-shrink:0;display:flex;align-items:center;justify-content:space-between;padding:0 40px;background:#14305C;color:#fff">
<div style="font-size:22px;font-weight:700">{H1}</div><div style="font-size:18px;opacity:.85">{H2}</div></div>
<div id="mid" style="flex-grow:1;min-height:0;overflow:hidden;position:relative;display:flex;align-items:center;justify-content:center;padding:24px 64px">{''.join(scenes)}</div>
<div style="height:64px;flex-shrink:0;display:flex;align-items:center;gap:24px;padding:0 40px;background:#fff;border-top:2px solid #C9D6E8">
<div style="flex-grow:1;display:flex;flex-direction:column;gap:10px"><div style="height:8px;border-radius:4px;background:#E3EAF3;overflow:hidden;display:flex"><div id="bar" style="height:8px;width:0;background:#C7361B"></div></div>
<div style="display:flex;gap:8px">{dots}</div></div><div class="m" id="cnt" style="font-size:22px;color:#3B5480"></div></div>
</div>
<script>
// مدة كل مشهد = طول تعليقه + ثانية ونصف (٧ ثوانٍ على الأقل) — مطابقة لنسخة التصميم
window.DURS = {json.dumps(durs)}.map(d => Math.max(7000, Math.round(d * 1000) + 1500));
const ar = n => String(n).replace(/\\d/g, c => '٠١٢٣٤٥٦٧٨٩'[c]);
const TOT = DURS.reduce((a, b) => a + b, 0);
let cur = -1;
window.seek = (i, t) => {{  // المشهد i عند الزمن t (ms) — لقطة ثابتة لكل إطار
  const sc = document.querySelectorAll('.sc');
  if (i !== cur) {{ sc.forEach((s, k) => s.style.display = k === i ? 'flex' : 'none'); cur = i;
    document.querySelectorAll('.dt').forEach((d, k) => d.classList.toggle('on', k === i));
    document.getElementById('cnt').textContent = ar(i + 1) + ' / ' + ar(sc.length);
    const s = sc[i], H = document.getElementById('mid').clientHeight - 32; s.style.transform = 'none';  // تصغير المشهد إن زاد عن المساحة
    if (s.scrollHeight > H) s.style.transform = 'scale(' + (H / s.scrollHeight) + ')'; }}
  sc[i].getAnimations({{subtree: true}}).forEach(a => {{ a.pause(); a.currentTime = t; }});
  const done = DURS.slice(0, i).reduce((a, b) => a + b, 0) + t;
  document.getElementById('bar').style.width = (done / TOT * 100) + '%';
}};
</script></body></html>'''
out = os.path.join(HERE, OUT)
open(out, 'w', encoding='utf-8').write(html); print(out, len(scenes), 'مشاهد')
