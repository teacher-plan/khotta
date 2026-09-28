# ورقة ملخّص الدرس ١-٧ «ترتيب العمليات الحسابية» للطالب — صور + PDF لمجموعة الصف.
# python3.12 gen_order_summary.py ← node ../sheet.mjs ملخص_ترتيب_العمليات.html ملخصات
# المراجع: كتاب الطالب ص٣٥، دليل المعلم ص٣٣، ورقة «درسي في صفحة» ١-٧ (إعداد أ. أرخية السعدي).
import os
HERE = os.path.dirname(os.path.abspath(__file__)); KIT = os.path.dirname(HERE)
_src = open(os.path.join(HERE, 'gen_powers_summary.py'), encoding='utf-8').read()
exec(_src.split('HEAD = ')[0])                               # a, N, P, M, X, EQ, PL, R …
exec('CSS = ' + _src.split('CSS = ')[1].split('\nout = ')[0])  # نفس هوية ورقة «القوى والجذور»

exec(open(os.path.join(HERE, 'order_building.py'), encoding='utf-8').read())
DV = '<span class="x">÷</span>'; MI = '<span class="x">−</span>'
def U(*p): return '<span class="now">' + ' '.join(a(x) if not str(x).startswith('<') else x for x in p) + '</span>'
def BR(*p): return '<span class="brk">(' + ' '.join(a(x) if not str(x).startswith('<') else x for x in p) + ')</span>'
def PW(inner, e): return f'<span class="b"><span>{a(inner)}</span><sup>{a(e)}</sup></span>'
def row(lab, expr): return f'<div class="sr"><span class="sl">{lab}</span>{expr}</div>'

HEAD = f'''<header><div class="hd"><b>الصف السابع</b><span>الوحدة الأولى: الأعداد الصحيحة والقوى والجذور</span>
<span>الدرس ١-٧: ترتيب العمليات الحسابية</span></div><div class="logo">{M('٣',PL,'٤',X,'٥')}{M(EQ,'٢٣')}</div></header>
<div class="goal">🎯 أحلّ مسألةً فيها أكثر من عملية حسابية بالترتيب الصحيح، وأضع الأقواس في مكانها المناسب</div>'''
FOOT = '<footer>📘 المرجع: كتاب الطالب ص ٣٥ ودليل المعلم — عن ورقة «درسي في صفحة» إعداد أ. أرخية السعدي — ارجع لكتاب النشاط ص ٢٥ لمزيد من التمارين</footer>'


page = f'''<section class="page">{HEAD}
<div class="card"><h3>ترتيب العمليات الحسابية</h3>
<div class="two ordw"><div class="bld">{building()}</div>
<div class="mini chant"><b>🎵 نردّدها معاً</b>{''.join(f'<span>{l}</span>' for l in CHANT)}</div></div>
<p>• يتّفق علماء الرياضيات في كل العالم على هذا الترتيب، فتُحلّ المسألة بالطريقة نفسها ونحصل على <b>الناتج نفسه</b>.</p></div>

<div class="card"><h3>أمثلة محلولة (مثال ١-٧)</h3><div class="three">
<div class="mini"><b>(أ)</b>{row('الضرب', M('٣',PL,U('٤',X,'٥'),EQ,'٣',PL,'٢٠'))}{row('الجمع', M(EQ,'٢٣'))}</div>
<div class="mini"><b>(ب)</b>{row('الأقواس', M('٣٠',DV,U(BR('٨',MI,'٣')),EQ,'٣٠',DV,'٥'))}{row('القسمة', M(EQ,'٦'))}</div>
<div class="mini"><b>(ج)</b>{row('الأقواس', M(P(3,2),X,'٥',MI,U(BR('١٩',MI,'٨'))))}{row('الأسس', M(EQ,U(P(3,2)),X,'٥',MI,'١١'))}{row('الضرب', M(EQ,U('٩',X,'٥'),MI,'١١'))}{row('الطرح', M(EQ,'٤٥',MI,'١١',EQ,'٣٤'))}</div>
</div></div>

<div class="card warn"><h3>⚠️ اقرأ المسألة كاملةً قبل أن تبدأ</h3>
<div class="two"><div class="bad">✘ {M(U('١٢',MI,'٤'),X,'٣',EQ,'٨',X,'٣',EQ,'٢٤')}</div><div class="good">✔ {M('١٢',MI,U('٤',X,'٣'),EQ,'١٢',MI,'١٢',EQ,'٠')}</div></div>
<p>• <b>سناء وخديجة</b> (تمرين ٢): {M(P(6,2),PL,'٨',DV,'٢')} — الصحيح <b>خديجة</b>: {M('٣٦',PL,'٤',EQ,'٤٠')}، أمّا سناء فجمعت قبل القسمة: {M(BR('٣٦',PL,'٨'),DV,'٢',EQ,'٢٢')}</p></div>

<footer>يتبع في الصفحة الثانية ←</footer></section>
<section class="page">{HEAD}
<div class="card"><h3>العمليات المتساوية: من اليمين إلى اليسار</h3>
<div class="two"><div class="mini">{M(U('٢٠',MI,'٧'),MI,'٢',EQ,'١٣',MI,'٢',EQ,'١١')}<small>بدون أقواس: نبدأ من اليمين</small></div>
<div class="mini">{M('٢٠',MI,U(BR('٧',MI,'٢')),EQ,'٢٠',MI,'٥',EQ,'١٥')}<small>الأقواس تغيّر الناتج</small></div></div></div>

<div class="card"><h3>ضع الأقواس ليكون الناتج صحيحاً (تمرين ٣)</h3><div class="grid g4 sm2">
<div>{M('٣',X,BR('٢',PL,'١'),EQ,'٩')}</div><div>{M(BR('٨',MI,'٣'),X,'٢',EQ,'١٠')}</div><div>{M('٢٠',MI,BR('٧',MI,'٢'),EQ,'١٥')}</div><div>{M(PW('(٥ + ٢)',2),EQ,'٤٩')}</div></div>
<p>• حدِّد العملية التي يجب أن تحدث أولاً، ضعها بين قوسين، ثم <b>تأكّد بالحساب</b>.</p></div>

<div class="card"><h3>✍️ تدرّب: أوجد الناتج (من تمرين ١)</h3><div class="grid g4 sm2">
<div>(ب) {M(BR('٢',MI,'٧'),X,'٥')}</div><div>(د) {M(BR('١٢',MI,'٤'),X,'٣')}</div><div>(هـ) {M('٤',X,'٢',PL,'٥',X,'٣')}</div><div>(و) {M('٤',X,BR('٢',PL,'٥'),X,'٣')}</div>
<div>(ح) {M('٢٠',DV,BR('٢',PL,'٨'))}</div><div>(ط) {M('٣٥',MI,'١٥',DV,'٣')}</div><div>(ك) {M('١٥',X,'٣',DV,PW('(٧ − ٤)',2))}</div><div>(س) {M('١٠٠',MI,PW('(٢٥ − ١٧)',2))}</div></div>
<p>• حلّها في دفترك خطوةً خطوة، ثم قارن إجاباتك مع معلّمك.</p></div>

<div class="card info"><h3>💡 لاحظ</h3>
<p>• داخل الأقواس نطبّق الترتيب نفسه: {M(f'<span class="b">٣<sup>(١٠ − ٤ × ٢)</sup></span>',EQ,f'<span class="b">٣<sup>(١٠ − ٨)</sup></span>',EQ,P(3,2),EQ,'٩')}</p>
<p>• يمكن إجراء عمليتين معاً إذا كانتا منفصلتين: {M(P(6,2),DV,BR('١١',MI,'٢'),EQ,'٣٦',DV,'٩',EQ,'٤')}</p></div>
{FOOT}</section>'''

CSS += r'''
.now{display:inline-flex;gap:.22em;border-bottom:2.5px solid var(--exp)}
.brk{display:inline-flex;gap:.2em;direction:rtl;unicode-bidi:isolate}
.ordw{align-items:center}.ord{display:flex;flex-direction:column;gap:1.6mm;flex:2.2}
.ord>div{display:flex;align-items:center;gap:2mm;border:2px solid;border-radius:3mm;padding:1.2mm 3mm;font-size:13pt}
.ord>div>b:first-child{color:#fff;border-radius:50%;width:7mm;height:7mm;display:flex;align-items:center;justify-content:center;flex:none}
.o1{border-color:#2563EB}.o1>b:first-child{background:#2563EB}.o2{border-color:#C7361B}.o2>b:first-child{background:#C7361B}
.o3{border-color:#7A3FD1}.o3>b:first-child{background:#7A3FD1}.o4{border-color:#1B7A3E}.o4>b:first-child{background:#1B7A3E}
.mancol{flex:1;display:flex;flex-direction:column;align-items:center;gap:1mm}.mancol small{font-size:10pt;color:#4A5E80}
.man{width:30mm;height:auto}.man circle,.man line,.man path{fill:none;stroke-width:8;stroke-linecap:round;stroke-linejoin:round}
.man .mt{font-family:'Readex Pro',sans-serif;font-weight:700;font-size:34px;text-anchor:middle}.man .mt2{font-family:'Readex Pro',sans-serif;font-weight:600;font-size:20px;text-anchor:middle}
.bld{font-size:12.5pt;flex:1.5;display:flex;justify-content:center}.chant{flex:1;gap:2mm;justify-content:center}.chant b{font-size:12pt;color:#4A5E80}.chant span{font-weight:700;font-size:12.5pt;line-height:1.6;text-align:center}
.three{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:3mm}
.three .mini{align-items:stretch;gap:1mm}.three .mini>b{align-self:center}
.sr{display:flex;align-items:center;justify-content:space-between;gap:2mm;font-size:12pt}
.sl{font-size:9pt;font-weight:600;color:#1E6FD9;background:#EAF1FF;border-radius:2mm;padding:0 2mm;flex:none}
.sm2 div{font-size:13pt;padding:1mm 0}
.mini .m{font-size:13pt}
'''
out = os.path.join(HERE, 'ملخص_ترتيب_العمليات.html')
open(out, 'w', encoding='utf-8').write(f'<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>ملخص ترتيب العمليات</title><style>{CSS}</style></head><body>{page}</body></html>')
print(out)
