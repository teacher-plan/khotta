# ورقة ملخّص الدرس ١-٢ «المضاعفات» للطالب — PDF لمجموعة الصف.
# python3.12 gen_mult_summary.py ← node ../sheet.mjs ملخص_المضاعفات.html ملخصات
# المراجع: كتاب الطالب ص٢٢–٢٣، دليل المعلم ص٢٣–٢٤، ورقة «درسي في صفحة» ١-٢.
import os
HERE = os.path.dirname(os.path.abspath(__file__)); KIT = os.path.dirname(HERE)
_src = open(os.path.join(HERE, 'gen_powers_summary.py'), encoding='utf-8').read()
exec(_src.split('HEAD = ')[0])
exec('CSS = ' + _src.split('CSS = ')[1].split('\nout = ')[0])
MI = '<span class="x">−</span>'
ME = 'إعداد: أ. عيسى الحارثي'
def L(*xs, hot=()): return '<span class="lst">' + '، '.join(f'<b class="{"cm" if x in hot else ""}">{a(x)}</b>' for x in xs) + '، …</span>'

HEAD = f'''<header><div class="hd"><b>الصف السابع</b><span>الوحدة الأولى: الأعداد الصحيحة والقوى والجذور</span>
<span>الدرس ١-٢: المضاعفات · {ME}</span></div><div class="logo">{M('م م ص')}{M('٤ ، ٦', '←', '١٢')}</div></header>
<div class="goal">🎯 أكتب مضاعفات العدد، وأجد المضاعفات المشتركة والمضاعف المشترك الأصغر (م م ص)</div>'''

page = f'''<section class="page">{HEAD}
<div class="card"><h3>المضاعفات</h3>
<p>• مضاعفات العدد: نبدأ <b>بالعدد نفسه</b>، ثم نضيفه في كل مرّة (أو نضربه في ١ ، ٢ ، ٣ ، …). النقاط تعني أن النمط يستمر.</p>
<div class="three"><div class="mini"><b>مضاعفات ٣</b>{L(3, 6, 9, 12, 15)}</div><div class="mini"><b>مضاعفات ٧</b>{L(7, 14, 21, 28, 35)}</div><div class="mini"><b>مضاعفات ٢٥</b>{L(25, 50, 75, 100, 125)}</div></div>
<p>• <b>المضاعف رقم ن = العدد × ن</b>: المضاعف الرابع للعدد ١٢ = {M('١٢', X, '٤', EQ, '٤٨')} ، والسابع للعدد ٦ = {M('٦', X, '٧', EQ, '٤٢')}</p>
<p>• إذا عرفت مضاعفاً: التالي = نضيف العدد، والسابق = نطرحه. السابع عشر للعدد ٨ هو ١٣٦ ← الثامن عشر {M('١٣٦', PL, '٨', EQ, '١٤٤')} ، والسادس عشر {M('١٣٦', MI, '٨', EQ, '١٢٨')}</p></div>

<div class="card"><h3>المضاعفات المشتركة والمضاعف المشترك الأصغر (م م ص)</h3>
<div class="two"><div class="mini"><b>مضاعفات ٦</b>{L(6, 12, 18, 24, 30, 36, 42, 48, hot=(24, 48))}</div><div class="mini"><b>مضاعفات ٨</b>{L(8, 16, 24, 32, 40, 48, hot=(24, 48))}</div></div>
<p>• المضاعفات المشتركة للعددين ٦ و ٨ الأصغر من ١٠٠: ٢٤ ، ٤٨ ، ٧٢ ، ٩٦ — وكلها مضاعفات للعدد ٢٤</p>
<p>• <b>م م ص</b> = أصغر مضاعفٍ مشترك: م م ص (٦ ، ٨) = <b>٢٤</b> · م م ص (٤ ، ٦) = ١٢ · م م ص (٩ ، ١١) = ٩٩</p></div>

<footer>يتبع في الصفحة الثانية ←</footer></section>
<section class="page">{HEAD}
<div class="card warn"><h3>⚠️ لا تخلط بين المضاعفات والعوامل</h3>
<div class="two"><div class="good">مضاعفات ٦: ٦ ، ١٢ ، ١٨ ، ٢٤ ، … (لا تنتهي)</div><div class="bad">عوامل ٦: ١ ، ٢ ، ٣ ، ٦ (محدودة)</div></div></div>

<div class="card info"><h3>💡 مسألة محلولة (تمرين ٨)</h3>
<p>• ضيوف سارة بين ٥٠ و ١٠٠ ويجلسون ٨ أو ١٢ على كل مائدة دون مقعدٍ فارغ ← نبحث عن مضاعفات مشتركة للعددين ٨ و ١٢ بين ٥٠ و ١٠٠: <b>٧٢ أو ٩٦</b></p></div>

<div class="card"><h3>✍️ تدرّب</h3><div class="grid g4 sm2">
<div>أوّل ٤ مضاعفات للعدد ٩</div><div>المضاعف الرابع للعدد ٢١</div><div>م م ص (٥ ، ٦)</div><div>م م ص (٤ ، ١٠)</div></div>
<p>• الإجابات: ٩ ، ١٨ ، ٢٧ ، ٣٦ — ٨٤ — ٣٠ — ٢٠</p></div>
<footer>📘 المرجع: كتاب الطالب ص ٢٢–٢٣ ودليل المعلم — {ME} — ارجع لكتاب النشاط ص ١٥ لمزيد من التمارين</footer></section>'''

CSS += r'''
.lst{font-size:12.5pt;font-weight:700}.lst b.cm{border:1.5px solid #C7361B;border-radius:50%;padding:0 1mm;color:#C7361B}
.three{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:3mm}
.mini>b{color:#1E6FD9}
.sm2 div{font-size:12pt;padding:1mm 0}
'''
out = os.path.join(HERE, 'ملخص_المضاعفات.html')
open(out, 'w', encoding='utf-8').write(f'<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>ملخص المضاعفات</title><style>{CSS}</style></head><body>{page}</body></html>')
print(out)
