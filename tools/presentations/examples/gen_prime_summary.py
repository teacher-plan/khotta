# ورقة ملخّص الدرس ١-٤ «الأعداد الأولية» للطالب — PDF لمجموعة الصف.
# python3.12 gen_prime_summary.py ← node ../sheet.mjs ملخص_الأعداد_الأولية.html ملخصات
# المراجع: كتاب الطالب ص٢٨–٢٩، دليل المعلم ص٢٧–٢٨، ورقة «درسي في صفحة» ١-٤.
import os
HERE = os.path.dirname(os.path.abspath(__file__)); KIT = os.path.dirname(HERE)
_src = open(os.path.join(HERE, 'gen_powers_summary.py'), encoding='utf-8').read()
exec(_src.split('HEAD = ')[0])
exec('CSS = ' + _src.split('CSS = ')[1].split('\nout = ')[0])
ME = 'إعداد: أ. عيسى الحارثي'
PRIMES = [p for p in range(2, 101) if all(p % d for d in range(2, int(p ** .5) + 1))]

def tree(n, steps):
    """شجرة العوامل: في كل مستوى n = p × m ، العامل الأولي p يُحاط بدائرة (يميناً) ونكمل مع m (يساراً)."""
    W, dy, x, y, out = 60 * (len(steps) + 1), 46, 60 * len(steps) + 20, 22, []
    out.append(f'<text x="{x}" y="{y}">{a(n)}</text>')
    for p, m in steps:
        xl, xr, y2 = x - 34, x + 30, y + dy
        out.append(f'<line x1="{x}" y1="{y + 6}" x2="{xl}" y2="{y2 - 16}"/><line x1="{x}" y1="{y + 6}" x2="{xr}" y2="{y2 - 16}"/>')
        out.append(f'<circle cx="{xr}" cy="{y2 - 6}" r="14"/><text x="{xr}" y="{y2}">{a(p)}</text>')
        last = m in PRIMES
        out.append((f'<circle cx="{xl}" cy="{y2 - 6}" r="14"/>' if last else '') + f'<text x="{xl}" y="{y2}">{a(m)}</text>')
        x, y = xl, y2
    return f'<svg class="tree" viewBox="0 0 {W + 20} {y + 14}" width="{W + 20}">{"".join(out)}</svg>'

HEAD = f'''<header><div class="hd"><b>الصف السابع</b><span>الوحدة الأولى: الأعداد الصحيحة والقوى والجذور</span>
<span>الدرس ١-٤: الأعداد الأولية · {ME}</span></div><div class="logo">{M('٢ ، ٣ ، ٥ ، ٧')}{M('١١ ، ١٣ …')}</div></header>
<div class="goal">🎯 أتعرّف العدد الأولي، وأستخدم غربال إراتوستينس، وأجد العوامل الأولية للعدد</div>'''

page = f'''<section class="page">{HEAD}
<div class="card"><h3>العدد الأولي</h3>
<p>• <b>العدد الأولي</b>: عددٌ له <b>عاملان فقط</b> هما ١ والعدد نفسه، مثل ١١ (عاملاه ١ و ١١) و ٢٣.</p>
<p>• إذا كان للعدد عوامل أخرى فهو <b>ليس أولياً</b>: ٩ = ٣ × ٣ ، ١٥ = ٣ × ٥ ، ٢١ ، ٢٧ ، ٤٩ ليست أعداداً أولية.</p>
<p>• كل الأعداد الأولية <b>فردية</b> ما عدا العدد <b>٢</b> (العدد الأولي الزوجي الوحيد).</p></div>

<div class="card warn"><h3>⚠️ خطآن شائعان</h3>
<div class="two"><div class="bad">✘ العدد ١ عددٌ أولي</div><div class="good">✔ ١ ليس أولياً: له عاملٌ واحد فقط</div></div>
<div class="two"><div class="bad">✘ العدد ٩١ عددٌ أولي</div><div class="good">✔ ٩١ = ٧ × ١٣ ليس أولياً</div></div></div>

<div class="card"><h3>غربال إراتوستينس · الأعداد الأولية حتى ١٠٠ (٢٥ عدداً)</h3>
<p>• اكتب الأعداد حتى ١٠٠ واشطب ١ ، ثم ضع مربّعاً حول ٢ واشطب مضاعفاته، ثم ٣ ثم ٥ ثم ٧ — ما يبقى أعدادٌ أولية.</p>
<div class="pgrid">{''.join(f'<b>{a(p)}</b>' for p in PRIMES)}</div>
<p>• بين ٢٠ و ٣٠: ٢٣ ، ٢٩ — وبين ٩٠ و ١٠٠: عددٌ واحد هو ٩٧ — ومثال لخمسة أعداد متتالية غير أولية: ٢٤ ، ٢٥ ، ٢٦ ، ٢٧ ، ٢٨</p></div>
<footer>يتبع في الصفحة الثانية ←</footer></section>
<section class="page">{HEAD}
<div class="card"><h3>العوامل الأولية للعدد</h3>
<p>• نختبر القسمة على الأعداد الأولية فقط: ٢ ، ٣ ، ٥ ، ٧ …</p>
<p>• مثال ١-٤: ٣٠ = ٢ × ١٥ = ٣ × ١٠ = ٥ × ٦ ، إذن العوامل الأولية للعدد ٣٠ هي <b>٢ ، ٣ ، ٥</b></p>
<div class="two trees"><div class="mini"><b>شجرة العوامل للعدد ٢٤</b>{tree(24, [(2, 12), (2, 6), (2, 3)])}<span>العوامل الأولية: ٢ ، ٣</span></div>
<div class="mini"><b>شجرة العوامل للعدد ٨٠</b>{tree(80, [(2, 40), (2, 20), (2, 10), (2, 5)])}<span>العوامل الأولية: ٢ ، ٥</span></div></div>
<p>• العوامل الأولية للعدد ١٥: ٣ ، ٥ — وللعدد ٢٥: ٥ فقط</p></div>

<div class="card"><h3>ناتج ضرب ومجموع عددين أوّليّين</h3>
<p>• ٣٥ = ٥ × ٧ ، ٢٢٦ = ٢ × ١١٣ (زوجي، فنقسم على ٢) ، ٣٠٥ = ٥ × ٦١</p>
<p>• ١٨ = ٥ + ١٣ = ٧ + ١١ ، ٣٠ = ٧ + ٢٣ = ١١ + ١٩ = ١٣ + ١٧</p>
<p>• <b>طريقة حسن</b>: ١١ ثم نضيف ٢ ، ٤ ، ٦ … فنحصل على ١٣ ، ١٧ ، ٢٣ ، ٣١ ، ٤١ ، ٥٣ ، ٦٧ ، ٨٣ ، ١٠١ ثم <b>١٢١ = ١١ × ١١</b> ليس أولياً — لا نعمّم من أمثلةٍ قليلة!</p></div>

<div class="card"><h3>✍️ تدرّب</h3><div class="grid g4 sm2">
<div>هل ٥١ أولي؟</div><div>العوامل الأولية للعدد ٧٠</div><div>اكتب ١٣٣ ناتجَ ضرب أوّليّين</div><div>اكتب ٢٦ مجموعَ أوّليّين</div></div>
<p>• الإجابات: لا (٥١ = ٣ × ١٧) — ٢ ، ٥ ، ٧ — ٧ × ١٩ — ٣ + ٢٣ أو ٧ + ١٩</p></div>
<footer>📘 المرجع: كتاب الطالب ص ٢٨–٢٩ ودليل المعلم — {ME} — ارجع لكتاب النشاط ص ١٨–١٩ لمزيد من التمارين</footer></section>'''

CSS += r'''
.pgrid{display:grid;grid-template-columns:repeat(13,1fr);gap:1.2mm;direction:rtl;margin:1.5mm 0}
.pgrid b{background:#1B7A3E;color:#fff;border-radius:2mm;text-align:center;font-size:12.5pt;padding:.6mm 0}
.mini>b{color:#1E6FD9}.mini>span{font-weight:700;font-size:11.5pt}
.trees .mini{display:flex;flex-direction:column;align-items:center;gap:1mm}
.tree{height:auto;max-height:52mm}.tree text{font:700 15px 'Readex Pro',sans-serif;text-anchor:middle;fill:#0E1B33}
.tree line{stroke:#4A5E80;stroke-width:1.6}.tree circle{fill:#FFF1D6;stroke:#C7361B;stroke-width:1.8}
.sm2 div{font-size:12pt;padding:1mm 0}
'''
out = os.path.join(HERE, 'ملخص_الأعداد_الأولية.html')
open(out, 'w', encoding='utf-8').write(f'<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>ملخص الأعداد الأولية</title><style>{CSS}</style></head><body>{page}</body></html>')
print(out)
