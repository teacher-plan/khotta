# ورقة ملخّص الدرس ١-٣ «العوامل وقابلية القسمة» للطالب — PDF لمجموعة الصف.
# python3.12 gen_fac_summary.py ← node ../sheet.mjs ملخص_العوامل_وقابلية_القسمة.html ملخصات
# المراجع: كتاب الطالب ص٢٤–٢٧، دليل المعلم ص٢٥–٢٦، ورقة «درسي في صفحة» ١-٣.
import os
HERE = os.path.dirname(os.path.abspath(__file__)); KIT = os.path.dirname(HERE)
_src = open(os.path.join(HERE, 'gen_powers_summary.py'), encoding='utf-8').read()
exec(_src.split('HEAD = ')[0])
exec('CSS = ' + _src.split('CSS = ')[1].split('\nout = ')[0])
DV = '<span class="x">÷</span>'
ME = 'إعداد: أ. عيسى الحارثي'
def L(*xs, hot=()): return '<span class="lst">' + '، '.join(f'<b class="{"cm" if x in hot else ""}">{a(x)}</b>' for x in xs) + '</span>'

HEAD = f'''<header><div class="hd"><b>الصف السابع</b><span>الوحدة الأولى: الأعداد الصحيحة والقوى والجذور</span>
<span>الدرس ١-٣: العوامل وقابلية القسمة · {ME}</span></div><div class="logo">{M('ع م ك')}{M('٢٤ ، ٤٠', '←', '٨')}</div></header>
<div class="goal">🎯 أجد عوامل العدد والعامل المشترك الأكبر (ع م ك)، وأستخدم اختبارات قابلية القسمة</div>'''
TESTS = [('٢', 'الآحاد ٠ أو ٢ أو ٤ أو ٦ أو ٨'), ('٣', 'مجموع الأرقام يقبل القسمة على ٣'), ('٤', 'آخر رقمين يكوّنان عدداً يقبل القسمة على ٤'),
         ('٥', 'الآحاد ٠ أو ٥'), ('٦', 'يقبل القسمة على ٢ وعلى ٣ معاً'), ('٧', 'لا يوجد اختبارٌ بسيط'),
         ('٨', 'آخر ثلاثة أرقام تكوّن عدداً يقبل القسمة على ٨'), ('٩', 'مجموع الأرقام يقبل القسمة على ٩'), ('١٠ و ١٠٠', 'الآحاد ٠ — وآخر رقمين ٠٠')]

page = f'''<section class="page">{HEAD}
<div class="card"><h3>العوامل</h3>
<p>• <b>العامل</b>: العدد الصحيح الذي يقسم عدداً صحيحاً آخر <b>بدون باقٍ</b>. العدد ١ عاملٌ لكل عدد، وكل عددٍ عاملٌ لنفسه.</p>
<p>• ٣ × ٨ = ٢٤ تعني: ٣ عاملٌ للعدد ٢٤ ، و ٢٤ مضاعفٌ للعدد ٣.</p>
<div class="two"><div class="mini"><b>عوامل ٤٠ في أزواج</b><span>١ × ٤٠ · ٢ × ٢٠ · ٤ × ١٠ · ٥ × ٨</span><small>(٣ و ٦ و ٧ ليست عوامل — نتوقّف عند تكرار الأزواج)</small></div>
<div class="mini"><b>عوامل ٤٠</b>{L(1, 2, 4, 5, 8, 10, 20, 40)}</div></div></div>

<div class="card"><h3>العوامل المشتركة والعامل المشترك الأكبر (ع م ك)</h3>
<div class="two"><div class="mini"><b>عوامل ٢٤</b>{L(1, 2, 3, 4, 6, 8, 12, 24, hot=(1, 2, 4, 8))}</div><div class="mini"><b>عوامل ٤٠</b>{L(1, 2, 4, 5, 8, 10, 20, 40, hot=(1, 2, 4, 8))}</div></div>
<p>• العوامل المشتركة: ١ ، ٢ ، ٤ ، ٨ — وأكبرها <b>ع م ك = ٨</b>. وقد يكون ع م ك هو ١ (مثل ٨ و ١٥).</p></div>

<div class="card warn"><h3>⚠️ خطأ شائع</h3>
<div class="two"><div class="bad">✘ عوامل ١٨: ٢ ، ٣ ، ٦ ، ٩</div><div class="good">✔ عوامل ١٨: ١ ، ٢ ، ٣ ، ٦ ، ٩ ، ١٨</div></div></div>
<footer>يتبع في الصفحة الثانية ←</footer></section>
<section class="page">{HEAD}
<div class="card"><h3>اختبارات قابلية القسمة</h3>
<table class="tt">{''.join(f'<tr><th>على {n}</th><td>{t}</td></tr>' for n, t in TESTS)}</table>
<p>• مثال: ٦٧٨٦ ← ٦ + ٧ + ٨ + ٦ = ٢٧ ، إذن يقبل القسمة على ٣ وعلى ٩ · و ١٧٨١٦ يقبل القسمة على ٨ لأن ٨١٦ ÷ ٨ = ١٠٢</p></div>

<div class="card"><h3>✍️ تدرّب</h3><div class="grid g4 sm2">
<div>عوامل ٢٨</div><div>عوامل ٢٧</div><div>ع م ك (١٢ ، ١٨)</div><div>هل ٥٩٤ يقبل القسمة على ٦؟</div></div>
<p>• الإجابات: ١،٢،٤،٧،١٤،٢٨ — ١،٣،٩،٢٧ — ٦ — نعم (زوجي ومجموع أرقامه ١٨)</p></div>
<footer>📘 المرجع: كتاب الطالب ص ٢٤–٢٧ ودليل المعلم — {ME} — ارجع لكتاب النشاط ص ١٦–١٧ لمزيد من التمارين</footer></section>'''

CSS += r'''
.lst{font-size:12.5pt;font-weight:700}.lst b.cm{border:1.5px solid #C7361B;border-radius:50%;padding:0 1mm;color:#C7361B}
.mini>b{color:#1E6FD9}.mini small{font-size:9.5pt;color:#4A5E80}
.tt{width:100%;border-collapse:collapse;font-size:11.5pt}.tt th{background:#EAF1FF;color:#1E6FD9;padding:1.4mm 3mm;white-space:nowrap;text-align:right;border:1px solid #C9D6E8}
.tt td{padding:1.4mm 3mm;border:1px solid #C9D6E8;font-weight:600}
.sm2 div{font-size:12pt;padding:1mm 0}
'''
out = os.path.join(HERE, 'ملخص_العوامل_وقابلية_القسمة.html')
open(out, 'w', encoding='utf-8').write(f'<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>ملخص العوامل وقابلية القسمة</title><style>{CSS}</style></head><body>{page}</body></html>')
print(out)
