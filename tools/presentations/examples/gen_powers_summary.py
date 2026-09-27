# ورقة ملخّص الدرس ١-٦ «القوى والجذور» للطالب — تُرسل في مجموعة الصف (واتساب) صوراً + PDF.
# صفحتان بمقاس A4 عمودي. نفس اصطلاحات العروض: الأس أعلى يسار الأساس، الجذر مرسوم من اليمين، أرقام عربية-هندية.
import os, re
HERE = os.path.dirname(os.path.abspath(__file__)); KIT = os.path.dirname(HERE)
AR = '٠١٢٣٤٥٦٧٨٩'
def a(n): return ''.join(s if s.startswith('<') else ''.join(AR[int(c)] if c.isdigit() else c for c in s) for s in re.split(r'(<[^>]*>)', str(n)))
def N(v): return f'<span class="ng"><i>−</i>{a(v)}</span>'
def PM(v): return f'<span class="ng"><i>±</i>{a(v)}</span>'
def P(b, e=None): return f'<span class="b">{a(b)}' + (f'<sup>{a(e)}</sup>' if e is not None else '') + '</span>'
def PN(v, e): return f'<span class="b"><span>({N(v)})</span><sup>{a(e)}</sup></span>'
X = '<span class="x">×</span>'; EQ = '<span class="x">=</span>'; PL = '<span class="x">+</span>'
def M(*p): return '<span class="m">' + ' '.join(a(x) if not str(x).startswith('<') else x for x in p) + '</span>'
def rep(b, n): return X.join(P(b) for _ in range(n))
def R(v, k=2):
    v = str(v); inner = N(v[1:]) if v.startswith('−') else a(v)
    idx = f'<i class="ri">{a(k)}</i>' if k == 3 else ''
    return (f'<span class="rt">{idx}<svg class="rsv" viewBox="0 0 32 64" preserveAspectRatio="none"><path d="M31 38 L25 34 L15 62 L1 1.5"/></svg>'
            f'<span class="ov">{inner}</span></span>')

HEAD = lambda part: f'''<header><div class="hd"><b>الصف السابع</b><span>الوحدة الأولى: الأعداد الصحيحة والقوى والجذور</span>
<span>الدرس ١-٦: القوى والجذور — {part}</span></div><div class="logo">{M(P(5,2))}{M(R(25))}</div></header>
<div class="goal">🎯 أجد قوى العدد وجذوره، وأتذكّر المربعات حتى {M(P(20,2))} ومكعبات الأعداد ١ – ١٠</div>'''
FOOT = '<footer>📘 المرجع: كتاب الطالب ص ٣٢–٣٤ — احتفظ بهذه الورقة وراجعها قبل الاختبار</footer>'

sq = ''.join(f'<div>{M(P(n,2),EQ,n*n)}</div>' for n in range(1, 21))
cu = ''.join(f'<div>{M(P(n,3),EQ,n**3)}</div>' for n in range(1, 11))

page1 = f'''<section class="page">{HEAD('القوى')}
<div class="card"><h3>قوى العدد</h3>
<p>• قوى العدد هي عدد مرات تكرار ضرب العدد في نفسه، ونستخدم <b class="ce">الأُسس</b> لإظهارها.</p>
<div class="anat">{M(P(5,3),EQ,rep(5,3),EQ,125)}<span class="lbl"><b class="cb">الأساس</b>: العدد الذي نضربه &nbsp;·&nbsp; <b class="ce">الأس</b>: كم مرّة نكتبه</span></div>
<div class="two"><div class="mini"><b>التربيع</b>{M(P(5,2),EQ,rep(5,2),EQ,25)}<small>يُقرأ: خمسة تربيع، أو مربّع العدد ٥</small></div>
<div class="mini"><b>التكعيب</b>{M(P(5,3),EQ,rep(5,3),EQ,125)}<small>يُقرأ: خمسة تكعيب، أو مكعّب العدد ٥</small></div></div>
<p>• <b>قوى العدد ١٠:</b> عدد الأصفار = الأس: {M(P(10,3),EQ,1000)} &nbsp;و&nbsp; {M(P(10,6),EQ,1000000)} (مليون)</p></div>
<div class="card warn"><h3>⚠️ انتبه: الأس ليس عدداً نضرب فيه!</h3>
<div class="two"><div class="bad">✘ {M(P(4,2),EQ,4,X,2,EQ,8)}</div><div class="good">✔ {M(P(4,2),EQ,rep(4,2),EQ,16)}</div></div></div>
<div class="card"><h3>احفظ: الأعداد المربّعة حتى ٢٠</h3><div class="grid g4">{sq}</div></div>
<div class="card"><h3>احفظ: مكعبات الأعداد ١ – ١٠</h3><div class="grid g5">{cu}</div></div>
{FOOT}</section>'''

page2 = f'''<section class="page">{HEAD('الجذور')}
<div class="card"><h3>الجذر التربيعي {M(R('؟'))} : عكس التربيع</h3>
<p>• لأن {M(P(5,2),EQ,25)} و {M(PN(5,2),EQ,25)} فإن للعدد ٢٥ <b>جذرين تربيعيين</b>:</p>
<div class="big">{M(R(25),EQ,PM(5))}</div>
<p>• أمثلة: {M(R(9),EQ,PM(3))} &nbsp; {M(R(81),EQ,PM(9))} &nbsp; {M(R(196),EQ,PM(14))}</p></div>
<div class="card"><h3>الجذر التكعيبي {M(R('؟',3))} : عكس التكعيب</h3>
<p>• لأن {M(P(5,3),EQ,125)} فإن:</p><div class="big">{M(R(125,3),EQ,5)}</div>
<p>• للعدد ١٢٥ <b>جذرٌ تكعيبيٌّ صحيحٌ واحد</b> فقط، و(−٥) ليس جذراً تكعيبياً له لأن {M(PN(5,3),EQ,N(125))}</p>
<p>• أمثلة: {M(R(27,3),EQ,3)} &nbsp; {M(R(1000,3),EQ,10)}</p></div>
<div class="card"><h3>قواعد مهمّة</h3>
<p>١) نُكمل العملية داخل الجذر أولاً: {M(R('100 − 36'),EQ,R(64),EQ,PM(8))}</p>
<p>٢) لا نوزّع الجذر على الجمع: {M(R('9 + 16'),EQ,R(25),EQ,5)} بينما {M(R(9),PL,R(16),EQ,7)}</p>
<p>٣) التربيع يلغي الجذر التربيعي: <span class="m">({R(36)})<sup class="e2">{a(2)}</sup> {EQ} {a(36)}</span></p>
<p>٤) آحاد العدد المربّع: ٠ أو ١ أو ٤ أو ٥ أو ٦ أو ٩ فقط (لا ينتهي بـ ٢ أو ٣ أو ٧ أو ٨)</p>
<p>٥) للعدد المربّع عددٌ <b>فرديّ</b> من العوامل: ١٦ ← ١، ٢، ٤، ٨، ١٦</p></div>
<div class="card info"><h3>💡 معلومة إثرائية (للاطّلاع فقط)</h3>
<p>• لا يوجد جذر تربيعي لعددٍ سالب، أما الجذر التكعيبي فممكن: {M(R('−125',3),EQ,N(5))}</p></div>
{FOOT}</section>'''

CSS = open(os.path.join(KIT, 'fonts.css'), encoding='utf-8').read() + r'''
:root{--ink:#14305C;--base:#0A6770;--exp:#C7361B;--line:#C9D6E8;--soft:#F2F6FB;--acc:#1E6FD9}
*{box-sizing:border-box;margin:0}
body{background:#DDE5EF;font-family:'Readex Pro','KDigits',sans-serif;color:var(--ink)}
.m,.m *{font-family:'KDigits','Readex Pro',sans-serif}
.page{width:210mm;height:297mm;margin:0 auto 10mm;background:#fff;padding:9mm 10mm;display:flex;flex-direction:column;gap:3.2mm;direction:rtl;overflow:hidden;
  background-image:linear-gradient(#EEF3F9 1px,transparent 1px),linear-gradient(90deg,#EEF3F9 1px,transparent 1px);background-size:6mm 6mm}
header{display:flex;justify-content:space-between;align-items:center;background:var(--ink);color:#fff;border-radius:5mm;padding:4mm 6mm}
.hd{display:flex;flex-direction:column;gap:1mm;font-size:13pt}.hd b{font-size:17pt}
.logo{background:#fff;border-radius:4mm;padding:2mm 4mm;font-size:18pt;display:flex;flex-direction:column;align-items:center;gap:1mm;color:var(--ink)}
.goal{background:#FFF4D6;border:2px solid #F2C94C;border-radius:3mm;padding:2.4mm 4mm;font-weight:600;font-size:12pt}
.card{background:#fff;border:2px solid var(--line);border-radius:5mm;padding:3.2mm 5mm;display:flex;flex-direction:column;gap:1.8mm;font-size:12.5pt;line-height:1.6}
.card h3{align-self:center;background:var(--soft);border:2px solid var(--line);border-radius:10mm;padding:.6mm 7mm;font-size:14pt;color:var(--ink)}
.card.warn{border-color:#E7A39A;background:#FFF8F6}.card.warn h3{background:#FDE7E3;border-color:#E7A39A;color:#8E2A18}
.card.info{border-color:#C8B3EE;background:#FAF7FF}.card.info h3{background:#EFE6FD;border-color:#C8B3EE;color:#4B1F9A}
.two{display:flex;gap:4mm}.two>*{flex:1}
.mini{background:var(--soft);border-radius:3mm;padding:2mm 3mm;display:flex;flex-direction:column;align-items:center;gap:.5mm}
.mini small{font-size:10pt;color:#4A5E80}
.bad,.good{border-radius:3mm;padding:1.5mm 3mm;text-align:center;font-weight:700;font-size:14pt}
.bad{background:#FDE7E3;color:#B3261E}.good{background:#E3F6EA;color:#1B7A3E}
.anat{display:flex;flex-direction:column;align-items:center;font-size:18pt;position:relative}
.lbl{font-size:10.5pt;font-weight:600}
.cb{color:var(--base)}.ce{color:var(--exp)}
.big{text-align:center;font-size:24pt}
.grid{display:grid;gap:1.5mm}.g4{grid-template-columns:repeat(4,1fr)}.g5{grid-template-columns:repeat(5,1fr)}
.grid div{background:var(--soft);border-radius:2mm;text-align:center;font-size:12.5pt;padding:0}
footer{margin-top:auto;text-align:center;font-size:10pt;color:#4A5E80}
.m{display:inline-flex;align-items:center;gap:.22em;direction:rtl;unicode-bidi:isolate;white-space:nowrap}
.x{color:#5A6F92}
.b{color:var(--base);display:inline-flex;align-items:flex-start;direction:rtl;unicode-bidi:isolate;font-weight:700}
.b sup{color:var(--exp);font-size:.55em;margin-inline-start:.04em;line-height:1}
sup.e2{color:var(--exp);font-size:.55em;align-self:flex-start;line-height:1}
.ng{display:inline-flex;direction:rtl;unicode-bidi:isolate}.ng i{font-style:normal}
.rt{display:inline-flex;align-items:stretch;direction:rtl;unicode-bidi:isolate;position:relative}
.rt .rsv{width:.5em;flex:none;overflow:visible}
.rt .rsv path{fill:none;stroke:currentColor;stroke-width:.075em;stroke-linejoin:round;stroke-linecap:round;vector-effect:non-scaling-stroke}
.rt .ov{border-top:.075em solid currentColor;padding:.06em .12em 0;display:inline-flex;direction:rtl;line-height:1.1}
.rt .ri{font-style:normal;font-size:.42em;font-weight:700;color:var(--exp);position:absolute;right:0;top:.05em;line-height:1}
@page{size:A4;margin:0}
@media print{body{background:#fff}.page{margin:0;page-break-after:always}}
'''
out = os.path.join(HERE, 'ملخص_القوى_والجذور.html')
open(out, 'w', encoding='utf-8').write(f'<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>ملخص القوى والجذور</title><style>{CSS}</style></head><body>{page1}{page2}</body></html>')
print(out)
