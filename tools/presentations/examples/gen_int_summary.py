# ورقة ملخّص الدرس ١-١ «الأعداد الصحيحة» للطالب — PDF واحد لمجموعة الصف.
# python3.12 gen_int_summary.py ← node ../sheet.mjs ملخص_الأعداد_الصحيحة.html ملخصات
# المراجع: كتاب الطالب ص١٦–٢١، دليل المعلم ص٢٠–٢٢، ورقة «درسي في صفحة» ١-١.
import os
HERE = os.path.dirname(os.path.abspath(__file__)); KIT = os.path.dirname(HERE)
_src = open(os.path.join(HERE, 'gen_powers_summary.py'), encoding='utf-8').read()
exec(_src.split('HEAD = ')[0])                               # a, N, P, M, X, EQ, PL …
exec('CSS = ' + _src.split('CSS = ')[1].split('\nout = ')[0])  # نفس هوية أوراق الوحدة

DV = '<span class="x">÷</span>'; MI = '<span class="x">−</span>'
def Z(v): return N(-v) if v < 0 else a(v)
def ZB(v): return f'<span class="brk">({N(-v)})</span>' if v < 0 else a(v)
def row(lab, expr): return f'<div class="sr"><span class="sl">{lab}</span>{expr}</div>'
ME = 'إعداد: أ. عيسى الحارثي'

HEAD = f'''<header><div class="hd"><b>الصف السابع</b><span>الوحدة الأولى: الأعداد الصحيحة والقوى والجذور</span>
<span>الدرس ١-١: الأعداد الصحيحة · {ME}</span></div><div class="logo">{M(N(3), X, ZB(-5))}{M(EQ, '١٥')}</div></header>
<div class="goal">🎯 أجمع الأعداد الصحيحة وأطرحها وأضربها وأقسمها، وأحدّد إشارة الناتج</div>'''
FOOT = f'<footer>📘 المرجع: كتاب الطالب ص ١٦–٢١ ودليل المعلم — {ME} — ارجع لكتاب النشاط ص ١٣–١٤ لمزيد من التمارين</footer>'
NL = '<div class="nl">' + ''.join(f'<span class="{"n" if k < 0 else ""}"><i></i><b>{Z(k)}</b></span>' for k in range(-5, 6)) + '</div>'

page = f'''<section class="page">{HEAD}
<div class="card"><h3>الأعداد الصحيحة وخط الأعداد</h3>
<p>• <b>الأعداد الصحيحة</b> أعدادٌ كاملة قد تكون موجبة أو سالبة، والصفر أيضاً عددٌ صحيح.</p>
{NL}
<div class="two"><div class="mini"><b>تزداد القيمة كلما اتجهنا يميناً →</b></div><div class="mini"><b>← تتناقص القيمة كلما اتجهنا يساراً</b></div></div>
<p>• −٥ تقع على يسار ٣ ، إذن {M(N(5), '<', '٣')} &nbsp;·&nbsp; و −٢ أكبر من −٧</p></div>

<div class="card"><h3>جمع الأعداد الصحيحة</h3>
<div class="two">
<div class="mini good2"><b>إشارتان متشابهتان</b><small>نجمع ونضع الإشارة نفسها</small>{M(N(6), PL, ZB(-4), EQ, N(10))}{M('٥', PL, '٣', EQ, '٨')}</div>
<div class="mini bad2"><b>إشارتان مختلفتان</b><small>نطرح ونضع إشارة العدد الأكبر</small>{M('٣', PL, ZB(-7), EQ, N(4))}{M(N(3), PL, '٧', EQ, '٤')}</div></div>
<p>• مثال: {M('١٢', PL, ZB(-4), EQ, '٨')} &nbsp;·&nbsp; {M(N(100), PL, ZB(-80), EQ, N(180))} &nbsp;·&nbsp; {M(N(5), PL, '٥', EQ, '٠')}</p></div>

<div class="card"><h3>طرح الأعداد الصحيحة = جمع المعكوس الجمعي</h3>
<p>• لكل عددٍ صحيح <b>س</b> معكوسٌ جمعي <b>−س</b> بحيث: <b>س + (−س) = صفر</b> — معكوس ٣ هو −٣ ، ومعكوس −١٨ هو ١٨</p>
<p>• نبدّل إشارة الطرح بإشارة الجمع، ونبدّل العدد الثاني بمعكوسه الجمعي:</p>
<div class="three">
<div class="mini">{row('معكوس −٣ هو ٣', M('٥', MI, ZB(-3)))}{M(EQ, '٥', PL, '٣', EQ, '٨')}</div>
<div class="mini">{row('معكوس ٨ هو −٨', M(N(5), MI, '٨'))}{M(EQ, N(5), PL, ZB(-8), EQ, N(13))}</div>
<div class="mini">{row('معكوس −٩ هو ٩', M(N(3), MI, ZB(-9)))}{M(EQ, N(3), PL, '٩', EQ, '٦')}</div></div>
<p>• العدد المفقود بالعملية العكسية: {M('؟', MI, ZB(-5), EQ, N(2))} ← {M(N(2), PL, ZB(-5), EQ, N(7))}</p></div>

<footer>يتبع في الصفحة الثانية ←</footer></section>
<section class="page">{HEAD}
<div class="card"><h3>ضرب الأعداد الصحيحة وقسمتها</h3>
<div class="two">
<div class="mini good2"><b>إشارتان متشابهتان ← الناتج موجب</b>{M(N(8), X, ZB(-5), EQ, '٤٠')}{M(N(24), DV, ZB(-6), EQ, '٤')}</div>
<div class="mini bad2"><b>إشارتان مختلفتان ← الناتج سالب</b>{M('١٢', X, ZB(-3), EQ, N(36))}{M(N(20), DV, '٤', EQ, N(5))}</div></div>
<div class="grid g4 sm2"><div>{M('+', X, '+', EQ, '+')}</div><div>{M('−', X, '−', EQ, '+')}</div><div>{M('+', X, '−', EQ, '−')}</div><div>{M('−', X, '+', EQ, '−')}</div></div>
<p>• <b>القسمة عمليةٌ عكسية للضرب:</b> {M(ZB(-3), X, '٤', EQ, N(12))} ← {M(N(12), DV, '٤', EQ, N(3))} و {M(N(12), DV, ZB(-3), EQ, '٤')}</p></div>

<div class="card warn"><h3>⚠️ لا تخلط بين قواعد الجمع وقواعد الضرب</h3>
<div class="two"><div class="bad">✘ {M(N(3), PL, ZB(-5), EQ, '٨')}</div><div class="good">✔ {M(N(3), PL, ZB(-5), EQ, N(8))}</div></div>
<p>• قاعدة «سالب × سالب = موجب» للضرب والقسمة فقط: {M(N(3), X, ZB(-5), EQ, '١٥')}</p></div>

<div class="card"><h3>✍️ تدرّب (من كتاب الطالب)</h3><div class="grid g4 sm2">
<div>{M(N(3), PL, ZB(-8))}</div><div>{M(N(10), PL, '٤')}</div><div>{M('٧', MI, ZB(-2))}</div><div>{M(N(6), MI, ZB(-6))}</div>
<div>{M('٥', X, ZB(-4))}</div><div>{M(N(4), X, ZB(-5))}</div><div>{M('٢٠', DV, ZB(-10))}</div><div>{M(N(12), DV, ZB(-4))}</div></div>
<p>• حلّها في دفترك، ثم قارن إجاباتك: −١١ ، −٦ ، ٩ ، ٠ ، −٢٠ ، ٢٠ ، −٢ ، ٣</p></div>

<div class="card info"><h3>💡 لاحظ</h3>
<p>• الأعداد التي ناتج ضربها −١٢ إشارتاها مختلفتان: ١ و −١٢ ، −١ و ١٢ ، ٢ و −٦ ، −٢ و ٦ ، ٣ و −٤ ، −٣ و ٤</p></div>
{FOOT}</section>'''

CSS += r'''
.brk{display:inline-flex;gap:.2em;direction:rtl;unicode-bidi:isolate}
.nl{display:flex;direction:ltr;border-top:2.5px solid #14305C;margin:3mm 2mm 1mm}
.nl>span{flex:1;display:flex;flex-direction:column;align-items:center}
.nl>span>i{width:2px;height:3mm;background:#14305C;margin-top:-1.6mm}
.nl>span>b{font-size:14pt;direction:rtl;unicode-bidi:isolate}.nl>span.n>b{color:#C7361B}
.three{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:3mm}
.three .mini{align-items:stretch;gap:1mm}
.sr{display:flex;align-items:center;justify-content:space-between;gap:2mm;font-size:12pt}
.sl{font-size:9pt;font-weight:600;color:#1E6FD9;background:#EAF1FF;border-radius:2mm;padding:0 2mm;flex:none}
.good2{border-color:#1B7A3E}.good2>b{color:#1B7A3E}.bad2{border-color:#C7361B}.bad2>b{color:#C7361B}
.mini small{font-size:10pt;color:#4A5E80}
.sm2 div{font-size:13pt;padding:1mm 0}
.mini .m{font-size:13pt}
'''
out = os.path.join(HERE, 'ملخص_الأعداد_الصحيحة.html')
open(out, 'w', encoding='utf-8').write(f'<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>ملخص الأعداد الصحيحة</title><style>{CSS}</style></head><body>{page}</body></html>')
print(out)
