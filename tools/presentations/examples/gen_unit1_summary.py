# ورقة «ملخّص الوحدة الأولى: الأعداد الصحيحة والقوى والجذور» — كل قاعدة ومعها مثالٌ محلول (صفحتان A4).
# python3.12 gen_unit1_summary.py ← node ../sheet.mjs ملخص_الوحدة_الأولى.html ملخصات
# المرجع: صفحة ملخّص الوحدة في كتاب الطالب.
import os
HERE = os.path.dirname(os.path.abspath(__file__)); KIT = os.path.dirname(HERE)
_src = open(os.path.join(HERE, 'gen_powers_summary.py'), encoding='utf-8').read()
exec(_src.split('HEAD = ')[0])
exec('CSS = ' + _src.split('CSS = ')[1].split('\nout = ')[0])
DV = '<span class="x">÷</span>'; MI = '<span class="x">−</span>'
def BR(*p): return '<span class="brk">(' + ' '.join(a(x) if not str(x).startswith('<') else x for x in p) + ')</span>'

def rule(n, text, ex, wide=False):
    return (f'<div class="rc{" wide" if wide else ""}"><div class="rt2"><b>{a(n)}</b><span>{text}</span></div>'
            f'<div class="ex"><span class="el">مثال</span>{ex}</div></div>')
def sec(title, cards): return f'<div class="sec"><h3>{title}</h3><div class="rg">{cards}</div></div>'

HEAD = f'''<header><div class="hd"><b>الصف السابع</b><span>ملخّص الوحدة الأولى</span>
<span>الأعداد الصحيحة والقوى والجذور</span></div><div class="logo">{M(P(2,2),X,P(5,3))}{M(EQ,'٥٠٠')}</div></header>'''
FOOT = '<footer>📘 المرجع: كتاب الطالب — صفحة ملخّص الوحدة الأولى · راجع هذه الورقة قبل اختبار الوحدة</footer>'

TESTS = [('٢', 'الآحاد زوجي'), ('٣', 'مجموع الأرقام يقبل ٣'), ('٤', 'آخر رقمين يقبلان ٤'), ('٥', 'الآحاد ٠ أو ٥'), ('٦', 'يقبل ٢ و ٣ معاً'),
         ('٨', 'آخر ثلاثة أرقام تقبل ٨'), ('٩', 'مجموع الأرقام يقبل ٩'), ('١٠', 'الآحاد ٠'), ('١٠٠', 'آخر رقمين ٠٠')]
dtab = '<div class="dt">' + ''.join(f'<div><b>{n}</b><span>{t}</span></div>' for n, t in TESTS) + '</div>'

p1 = f'''<section class="page">{HEAD}
{sec('١) الأعداد الصحيحة',
  rule(1, 'يمكنك طرح عددٍ سالب بإضافة العدد الموجب المقابل له.', M('٥', MI, BR(N(3)), EQ, '٥', PL, '٣', EQ, '٨')) +
  rule(2, 'عند ضرب عددين صحيحين أو قسمتهما: إشارتان <b class="g2">متشابهتان ← موجب</b>، و<b class="r2">مختلفتان ← سالب</b>.',
       '<span class="col2">' + M(N(5), X, N(2), EQ, '١٠') + M(N(5), X, '٢', EQ, N(10)) + M(N(20), DV, N(4), EQ, '٥') + '</span>'))}
{sec('٢) المضاعفات والعوامل',
  rule(3, 'تجد مضاعفات عددٍ بالضرب في ١، ٢، ٣، وهكذا.', 'مضاعفات ٦: ' + M('٦ ، ١٢ ، ١٨ ، ٢٤ ، …')) +
  rule(4, 'كلّ عددٍ صحيحٍ موجب له مضاعفات وعوامل، والعوامل تأتي أزواجاً.', 'عوامل ١٢: ' + M('١ ، ٢ ، ٣ ، ٤ ، ٦ ، ١٢') + '<small>(١ × ١٢ ، ٢ × ٦ ، ٣ × ٤)</small>') +
  rule(5, 'من الممكن أن تكون هناك عوامل مشتركة بين عددين صحيحين.', 'المشتركة بين ١٢ و ١٨: ' + M('١ ، ٢ ، ٣ ، ٦') + '<small>أكبرها ٦ = العامل المشترك الأكبر</small>', True))}
{sec('٣) اختبارات قابلية القسمة',
  rule(6, 'هناك اختباراتٌ بسيطة لقابلية القسمة على ٢، ٣، ٤، ٥، ٦، ٨، ٩، ١٠، ١٠٠:' + dtab,
       'العدد ٣٧٢ يقبل القسمة على ٢ و ٣ (٣ + ٧ + ٢ = ١٢) و ٤ (٧٢) و ٦، ولا يقبلها على ٥ و ٨ و ٩ و ١٠ و ١٠٠', True))}
{FOOT}</section>'''

p2 = f'''<section class="page">{HEAD}
{sec('٤) الأعداد الأولية',
  rule(7, 'الأعداد الأوليّة لها عاملان فقط: ١ والعدد نفسه. (العدد ١ ليس أولياً)', '٧ أولي (١ ، ٧) — ٩ ليس أولياً (١ ، ٣ ، ٩)') +
  rule(9, 'يمكنك كتابة كلّ عددٍ صحيحٍ موجب في صورة ناتج ضرب أعدادٍ أوليّة.', M('٥٠٠', EQ, '٢', X, '٢', X, '٥', X, '٥', X, '٥', EQ, P(2, 2), X, P(5, 3))) +
  rule(10, 'نستخدم نواتج ضرب العوامل الأوليّة لإيجاد العامل المشترك الأكبر (المشترك بالأس الأصغر) والمضاعف المشترك الأصغر (الكل بالأس الأكبر).',
       '<span class="col2">' + M('١٢', EQ, P(2, 2), X, '٣') + M('١٨', EQ, '٢', X, P(3, 2)) + '<span>ع.م.أ = ' + M('٢', X, '٣', EQ, '٦') + ' ، م.م.أ = ' + M(P(2, 2), X, P(3, 2), EQ, '٣٦') + '</span></span>', True) +
  rule(8, 'يمكن استخدام طريقة غربال إراتوستينس لإيجاد الأعداد الأوليّة: نحذف مضاعفات ٢ ثم ٣ ثم ٥ ثم ٧.', '<span>الأوليّة حتى ٥٠: <b>٢ ، ٣ ، ٥ ، ٧ ، ١١ ، ١٣ ، ١٧ ، ١٩ ، ٢٣ ، ٢٩ ، ٣١ ، ٣٧ ، ٤١ ، ٤٣ ، ٤٧</b></span>', True))}
{sec('٥) القوى والجذور',
  rule(11, f'{M(P(7, 2))} تُقرأ «مربّع العدد ٧»، و {M(R(49))} تُقرأ «الجذر التربيعي للعدد ٤٩». للأعداد الصحيحة الموجبة جذران تربيعيان.',
       M(P(7, 2), EQ, '٤٩') + ' ، ' + M(PN(7, 2), EQ, '٤٩') + ' ، ' + M(R(49), EQ, PM(7))) +
  rule(12, f'{M(P(4, 3))} تُقرأ «مكعّب العدد ٤»، و {M(R(64, 3))} تُقرأ «الجذر التكعيبي للعدد ٦٤».', M(P(4, 3), EQ, '٤', X, '٤', X, '٤', EQ, '٦٤') + ' ، ' + M(R(64, 3), EQ, '٤')) +
  rule(13, f'{M(P(5, 4))} يعني {M("٥", X, "٥", X, "٥", X, "٥")} — الأس يخبرنا كم مرّةً نكتب الأساس.', M(P(5, 4), EQ, '٢٥', X, '٢٥', EQ, '٦٢٥'), True))}
{FOOT}</section>'''

CSS += r'''
.brk{display:inline-flex;gap:.2em;direction:rtl;unicode-bidi:isolate}
.sec{display:flex;flex-direction:column;gap:2mm}
.sec h3{background:var(--ink);color:#fff;border-radius:3mm;padding:1.2mm 4mm;font-size:13.5pt;align-self:flex-start}
.rg{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:2.5mm}
.rc{background:#fff;border:2px solid var(--line);border-radius:4mm;padding:2.4mm 3.5mm;display:flex;flex-direction:column;gap:1.8mm;font-size:11.5pt;line-height:1.6}
.rc.wide{grid-column:1/-1}
.rt2{display:flex;gap:2mm;align-items:flex-start;font-weight:600}
.rt2>b{flex:none;background:var(--acc);color:#fff;border-radius:50%;width:6.5mm;height:6.5mm;display:flex;align-items:center;justify-content:center;font-size:10pt}
.ex{display:flex;gap:2mm;align-items:center;flex-wrap:wrap;background:#F2F6FB;border-radius:2.5mm;padding:1.4mm 2.5mm}
.ex small{font-size:9.5pt;color:#4A5E80;width:100%}
.el{flex:none;background:#1B7A3E;color:#fff;border-radius:2mm;padding:0 2mm;font-size:9pt;font-weight:700}
.col2{display:flex;flex-direction:column;gap:.5mm}
.g2{color:#1B7A3E}.r2{color:#B3261E}
.dt{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1.2mm;margin-top:1.5mm}
.dt div{display:flex;gap:1.5mm;align-items:center;background:#FFF6E3;border-radius:2mm;padding:.6mm 2mm;font-size:10.5pt;font-weight:500}
.dt b{color:#C7361B;font-size:12pt;min-width:7mm;text-align:center}
.rc .m{font-size:12pt}
'''
out = os.path.join(HERE, 'ملخص_الوحدة_الأولى.html')
open(out, 'w', encoding='utf-8').write(f'<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>ملخص الوحدة الأولى</title><style>{CSS}</style></head><body>{p1}{p2}</body></html>')
print(out)
