# ورقة ملخّص الدرس ١-٥ «الأسس» للطالب — PDF لمجموعة الصف.
# python3.12 gen_index_summary.py ← node ../sheet.mjs ملخص_الأسس.html ملخصات
# المراجع: كتاب الطالب ص٣٠–٣١، دليل المعلم ص٢٩–٣٠، ورقة «درسي في صفحة» ١-٥.
import os
HERE = os.path.dirname(os.path.abspath(__file__)); KIT = os.path.dirname(HERE)
_src = open(os.path.join(HERE, 'gen_powers_summary.py'), encoding='utf-8').read()
exec(_src.split('HEAD = ')[0])
exec('CSS = ' + _src.split('CSS = ')[1].split('\nout = ')[0])
ME = 'إعداد: أ. عيسى الحارثي'
def S(b, e): return f'{a(b)}<sup>{a(e)}</sup>'

def tree(t):
    """شجرة عوامل من صفوف متداخلة (العدد، الفرع الأيسر، الفرع الأيمن)؛ الأعداد الأولية في نهايات الفروع داخل دوائر."""
    U, V, items, leaves = 44, 42, [], [0]
    def lay(n, d):
        if isinstance(n, tuple):
            xl, xr = lay(n[1], d + 1), lay(n[2], d + 1); x = (xl + xr) / 2
            items.append(('n', n[0], x, d)); items.append(('l', x, d, xl)); items.append(('l', x, d, xr)); return x
        x = leaves[0] * U + U / 2; leaves[0] += 1; items.append(('p', n, x, d)); return x
    lay(t, 0)
    D = max(i[3] for i in items if i[0] != 'l') + 1
    out = [f'<line x1="{x}" y1="{d * V + 26}" x2="{xc}" y2="{(d + 1) * V + 8}"/>' for k, x, d, xc in items if k == 'l']
    for k, n, x, d in (i for i in items if i[0] != 'l'):
        y = d * V + 22
        if k == 'p': out.append(f'<circle cx="{x}" cy="{y - 5}" r="13"/>')
        out.append(f'<text x="{x}" y="{y}">{a(n)}</text>')
    return f'<svg class="tree" viewBox="0 0 {leaves[0] * U} {D * V}" width="{leaves[0] * U}">{"".join(out)}</svg>'

HEAD = f'''<header><div class="hd"><b>الصف السابع</b><span>الوحدة الأولى: الأعداد الصحيحة والقوى والجذور</span>
<span>الدرس ١-٥: الأسس · {ME}</span></div><div class="logo"><span class="mm">{S(2, 3)} = ٢ × ٢ × ٢</span></div></header>
<div class="goal">🎯 أرسم شجرة العوامل، وأكتب العدد بالأسس، وأجد م م ص و ع م ك بالعوامل الأولية</div>'''

page = f'''<section class="page">{HEAD}
<div class="card"><h3>شجرة العوامل</h3>
<p>• كل عددٍ صحيح أكبر من ١ وليس أولياً يمكن كتابته في صورة ناتج ضرب أعدادٍ أولية: ٨٤ = ٢ × ٢ × ٣ × ٧</p>
<p>• نرسم فرعين لعددين حاصل ضربهما العدد، ونكرّر حتى تنتهي كل الفروع بأعدادٍ أولية (نضع حولها دائرة)، ثم نضرب نهايات الفروع.</p>
<div class="two trees"><div class="mini"><b>شجرة للعدد ١٢٠</b>{tree((120, (10, 5, 2), (12, (4, 2, 2), 3)))}</div>
<div class="mini"><b>شجرةٌ أخرى للعدد ١٢٠</b>{tree((120, (60, (30, (6, 3, 2), 5), 2), 2))}</div></div>
<p>• مهما رسمنا الشجرة تبقى الأعداد في النهايات نفسها: ١٢٠ = ٢ × ٢ × ٢ × ٣ × ٥ — والعدد <b>١ لا يظهر في الشجرة</b> لأنه ليس أولياً.</p></div>

<div class="card"><h3>الأُسّ</h3>
<div class="two"><div class="mini"><b>{S(2, 3)} = ٢ × ٢ × ٢ = ٨</b><span>تُقرأ: ٢ أُسّ ٣ — ٢ هو <b>الأساس</b> و ٣ هو <b>الأُسّ</b></span></div>
<div class="mini"><b>١٢٠ = {S(2, 3)} × ٣ × ٥</b><span>٤٥٠ = ٢ × {S(3, 2)} × {S(5, 2)} · ٧٢ = {S(2, 3)} × {S(3, 2)}</span></div></div>
<p>• ما العدد الذي تمثّله: {S(2, 2)} × ٣ × ٥ = ٦٠ · ٢ × {S(3, 3)} = ٥٤ · ٣ × {S(11, 2)} = ٣٦٣ · {S(2, 3)} × {S(7, 2)} = ٣٩٢</p></div>
<footer>يتبع في الصفحة الثانية ←</footer></section>
<section class="page">{HEAD}
<div class="card"><h3>م م ص و ع م ك بالعوامل الأولية (مثال ١-٥: العددان ٦٠ ، ٧٥)</h3>
<table class="tt pt"><tr><th></th><th>٢</th><th>٣</th><th>٥</th></tr>
<tr><th>٦٠</th><td>{S(2, 2)}</td><td>٣</td><td>٥</td></tr><tr><th>٧٥</th><td>—</td><td>٣</td><td>{S(5, 2)}</td></tr>
<tr class="l"><th>م م ص</th><td>{S(2, 2)}</td><td>٣</td><td>{S(5, 2)}</td></tr><tr class="h"><th>ع م ك</th><td>—</td><td>٣</td><td>٥</td></tr></table>
<div class="two"><div class="mini l"><b>م م ص: الأُسّ الأكبر لكل عامل</b><span>{S(2, 2)} × ٣ × {S(5, 2)} = ٣٠٠</span></div>
<div class="mini h"><b>ع م ك: الأُسّ الأصغر للعوامل المشتركة فقط</b><span>٣ × ٥ = ١٥</span></div></div></div>

<div class="card"><h3>أمثلة أخرى</h3>
<p>• ٤٥ = {S(3, 2)} × ٥ و ٧٥ = ٣ × {S(5, 2)} ← م م ص = {S(3, 2)} × {S(5, 2)} = ٢٢٥ ، ع م ك = ٣ × ٥ = ١٥</p>
<p>• ٩٠ = ٢ × {S(3, 2)} × ٥ و ١٤٠ = {S(2, 2)} × ٥ × ٧ ← م م ص = ١٢٦٠ ، ع م ك = ٢ × ٥ = ١٠ (٣ و ٧ ليسا مشتركين)</p>
<p>• لعددين أوّليّين مثل ٣٧ و ٤٧: ع م ك = ١ ، و م م ص = ناتج ضربهما = ١٧٣٩</p>
<p>• ⚠️ لا تخلط: <b>م م ص</b> مضاعفٌ للعددين (أكبر منهما أو يساوي أكبرهما)، و<b>ع م ك</b> عاملٌ لهما (أصغر منهما أو يساوي أصغرهما).</p></div>


<div class="card"><h3>✍️ تدرّب</h3><div class="grid g4 sm2">
<div>اكتب ٣٦ بالأسس</div><div>اكتب ٢٠٠ بالأسس</div><div>ع م ك (٢٤ ، ٣٦)</div><div>م م ص (٢٤ ، ٣٦)</div></div>
<p>• الإجابات: {S(2, 2)} × {S(3, 2)} — {S(2, 3)} × {S(5, 2)} — ١٢ — ٧٢</p></div>
<footer>📘 المرجع: كتاب الطالب ص ٣٠–٣١ ودليل المعلم — {ME} — ارجع لكتاب النشاط ص ٢٠–٢٢ لمزيد من التمارين</footer></section>'''

CSS += r'''
.mini>b{color:#1E6FD9}.mini>span{font-weight:700;font-size:11.5pt}
.trees .mini{display:flex;flex-direction:column;align-items:center;gap:1mm}
.tree{height:auto;max-height:50mm}.tree text{font:700 15px 'Readex Pro',sans-serif;text-anchor:middle;fill:#0E1B33}
.tree line{stroke:#4A5E80;stroke-width:1.6}.tree circle{fill:#FFF1D6;stroke:#C7361B;stroke-width:1.8}
sup{font-size:.7em;color:#C7361B}.mm{font-weight:800;font-size:14pt}
.pt{width:auto;margin:0 auto 2mm;border-collapse:collapse;font-size:13pt;text-align:center}
.pt th,.pt td{padding:1.2mm 5mm;border:1px solid #C9D6E8;font-weight:800}.pt tr:first-child th{background:#EAF1FF;color:#1E6FD9}
.pt tr.l td,.pt tr.l th,.mini.l b{color:#7A3FD1}.pt tr.l td{background:#F3ECFD}
.pt tr.h td,.pt tr.h th,.mini.h b{color:#C7361B}.pt tr.h td{background:#FDECE8}
.sm2 div{font-size:12pt;padding:1mm 0}
'''
out = os.path.join(HERE, 'ملخص_الأسس.html')
open(out, 'w', encoding='utf-8').write(f'<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>ملخص الأسس</title><style>{CSS}</style></head><body>{page}</body></html>')
print(out)
