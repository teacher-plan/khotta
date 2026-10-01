# قالب ورقة الملخّص الجديد (من الوحدة الثانية، تعليمات الأستاذ عيسى):
# • لا شَرطة فاصلة بين الجمل (الفاصلة «،» بدلاً منها)، والشَّرطة لا تظهر إلا علامة طرح داخل الرياضيات.
# • عبارات دقيقة كاملة، ومثال محلول من إعدادي لكل فكرة، وبجانب كل خطوة سببها.
# • تذييل كل صفحة: يميناً «عمل: أ. عيسى الحارثي»، ويساراً «تحت إشراف: أ. أحمد الحارثي (معلّم أول رياضيات)»، ولا شيء غيرهما.
# الاستخدام: exec(open('summary2.py').read()) ثم build(out_html, title, [page1, page2]) — الصفحة = header(...) + أقسام.
import os, re
HERE = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else os.getcwd()
KIT = os.path.dirname(HERE)
AR = '٠١٢٣٤٥٦٧٨٩'
def a(s): return ''.join(AR[int(c)] if c.isdigit() else c for c in str(s))
MI = '<span class="op">−</span>'; PL = '<span class="op">+</span>'; X = '<span class="op">×</span>'; DV = '<span class="op">÷</span>'; EQ = '<span class="op">=</span>'
def V(t): return f'<b class="v">{t}</b>'
def FR(n, d): return f'<span class="fr"><span>{n}</span><span>{d}</span></span>'
def G(*p): return '<span class="grp">(' + ' '.join(p) + ')</span>'
def M(*p): return '<span class="m">' + ' '.join(p) + '</span>'

def header(code, title, unit, goal):
    return f'''<header><div class="hl"><span class="code">{"الدرس " + code if code[:1] in "٠١٢٣٤٥٦٧٨٩" else code}</span><h1>{title}</h1><span class="unit">الصف السابع · {unit}</span></div></header>
<div class="goal"><b>🎯 هدف الدرس</b><span>{goal}</span></div>'''
def sec(n, title, *body): return f'<section class="sec"><h2><i>{a(n)}</i>{title}</h2>{"".join(body)}</section>'
def rule(t, icon='📌'): return f'<div class="rule"><b>{icon}</b><div>{t}</div></div>'
def p(t): return f'<p class="tx">{t}</p>'
def example(q, steps, ans=None, title='مثال محلول'):
    rows = ''.join(f'<tr><td class="n">{a(i + 1)}</td><td class="e">{e}</td><td class="r">{r}</td></tr>' for i, (e, r) in enumerate(steps))
    return f'''<div class="ex"><div class="exh"><b>✍️ {title}</b><span>{q}</span></div><table>{rows}</table>{f'<div class="ans">الإجابة: {ans}</div>' if ans else ''}</div>'''
def warn(items):
    return '<div class="warn"><b class="wt">⚠️ انتبه</b>' + ''.join(f'<div class="wr"><span class="bad">✘ {b}</span><span class="good">✔ {g}</span><small>{w}</small></div>' for b, g, w in items) + '</div>'
def table(head, rows, cls=''):
    return f'<table class="tb {cls}"><tr>' + ''.join(f'<th>{h}</th>' for h in head) + '</tr>' + ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows) + '</table>'
def practice(qs, ans):
    return '<div class="pr"><b>🧠 تدرّب</b><ol>' + ''.join(f'<li>{q}</li>' for q in qs) + '</ol><div class="pa">الإجابات: ' + '، '.join(f'({a(i + 1)}) {x}' for i, x in enumerate(ans)) + '</div></div>'
FOOT = '<footer><span>عمل: أ. عيسى الحارثي</span><span>تحت إشراف: أ. أحمد الحارثي (معلّم أول رياضيات)</span></footer>'

CSS = open(os.path.join(KIT, 'fonts.css'), encoding='utf-8').read() + r'''
:root{--ink:#0E1B33;--ink2:#3B4F72;--nav:#123A6B;--teal:#0B7A83;--rule:#1E5FB8;--rulebg:#EEF4FD;--ex:#157347;--exbg:#EFF8F2;--w:#B3261E;--wbg:#FDF1EF;--v:#C2410C;--line:#D5DEEA}
*{box-sizing:border-box}
body{margin:0;background:#DDE5EF;font-family:'Readex Pro','KDigits',sans-serif;color:var(--ink)}
.m,.m *,.tb td,.e{font-family:'KDigits','Readex Pro',sans-serif}
.page{width:210mm;height:297mm;margin:0 auto 10mm;background:#fff;padding:0 0 0;display:flex;flex-direction:column;direction:rtl;overflow:hidden;position:relative}
.body{flex:1;min-height:0;display:flex;flex-direction:column;gap:2.6mm;padding:3mm 11mm 0}
header{flex:none;background:linear-gradient(120deg,var(--nav),var(--teal));color:#fff;padding:4.5mm 11mm 3.5mm;position:relative;overflow:hidden}
header::after{content:'س  ع  ل  +  ×  ÷';position:absolute;left:8mm;top:3mm;font-size:30pt;font-weight:800;opacity:.12;letter-spacing:3mm;direction:ltr}
.hl{display:flex;flex-direction:column;gap:1mm}
.code{align-self:flex-start;background:rgba(255,255,255,.18);border-radius:99px;padding:.6mm 4mm;font-weight:700;font-size:10.5pt}
h1{margin:0;font-size:21pt;font-weight:800;line-height:1.25}
.unit{font-size:10.5pt;font-weight:600;color:#DCEBFA}
.goal{flex:none;display:flex;gap:3mm;align-items:center;margin:3mm 11mm 0;background:#FFF7E6;border:1px solid #F1C66B;border-radius:3mm;padding:2mm 4mm;font-size:11pt;font-weight:600}
.goal b{color:#9A5B00;white-space:nowrap}
.sec{display:flex;flex-direction:column;gap:1.8mm}
.sec>h2{margin:0;display:flex;align-items:center;gap:2.5mm;font-size:14pt;color:var(--nav)}
.sec>h2 i{font-style:normal;width:7.5mm;height:7.5mm;border-radius:50%;background:var(--nav);color:#fff;display:inline-flex;align-items:center;justify-content:center;font-size:11pt}
.tx{margin:0;font-size:11pt;line-height:1.65}
.rule{display:flex;gap:3mm;align-items:flex-start;background:var(--rulebg);border-inline-start:2mm solid var(--rule);border-radius:2.5mm;padding:2mm 4mm;font-size:11.3pt;line-height:1.7;font-weight:600}
.rule>b{font-size:13pt}
.m{display:inline-flex;align-items:center;gap:1.2mm;direction:rtl;unicode-bidi:isolate;font-weight:700;font-size:1.08em;white-space:nowrap}
.op{color:var(--ink2);font-weight:700}
.v{color:var(--v);font-weight:800}
.fr{display:inline-flex;flex-direction:column;align-items:center;line-height:1.05;vertical-align:middle}
.fr>span:first-child{border-bottom:.5mm solid currentColor;padding:0 1mm .3mm;align-self:stretch;text-align:center}
.grp{display:inline-flex;gap:1mm;align-items:center;direction:rtl;unicode-bidi:isolate}
.ex{border:1.2px solid #A9D8BC;border-radius:3mm;overflow:hidden;background:#fff}
.exh{display:flex;gap:3mm;align-items:baseline;background:var(--exbg);padding:2mm 4mm;font-size:11.5pt;font-weight:600;border-bottom:1px solid #CDEBD9}
.exh b{color:var(--ex);white-space:nowrap}
.ex table{width:100%;border-collapse:collapse}
.ex td{padding:1.1mm 3mm;border-bottom:1px dashed #DCEFE3;vertical-align:middle}
.ex tr:last-child td{border-bottom:0}
.ex td.n{width:8mm;text-align:center;color:#fff;font-weight:800;font-size:10pt}
.ex td.n{background:var(--ex);border-bottom:1px solid #fff}
.ex td.e{font-size:12.5pt;font-weight:700;white-space:nowrap;width:1%}
.ex td.r{font-size:10.5pt;color:var(--ink2);font-weight:600}
.ans{background:var(--ex);color:#fff;font-weight:800;padding:1.6mm 4mm;font-size:11.5pt}
.ans .op{color:#fff}.ans .v{color:#FFE08A}
.warn{background:var(--wbg);border:1.2px solid #F2B8B2;border-radius:3mm;padding:2.5mm 4mm;display:flex;flex-direction:column;gap:1.6mm}
.wt{color:var(--w);font-size:12pt}
.wr{display:grid;grid-template-columns:1fr 1fr;gap:1mm 4mm;font-size:11pt;font-weight:700;align-items:center}
.wr .bad{color:var(--w)}.wr .good{color:var(--ex)}.wr small{grid-column:1/-1;color:var(--ink2);font-weight:600;font-size:10pt}
.tb{width:100%;border-collapse:separate;border-spacing:0;border:1.2px solid var(--line);border-radius:3mm;overflow:hidden;font-size:11pt}
.tb.area{width:auto;margin:0 auto}.tb.inv td,.tb.inv th{padding:.6mm 3mm;white-space:nowrap}.tb.area td,.tb.area th{text-align:center;min-width:22mm;font-size:13pt}.tb.area td:nth-child(2){background:#E7F0FF}.tb.area td:nth-child(3){background:#FFF1E6}
.tb th{background:var(--nav);color:#fff;padding:1.2mm 3mm;font-weight:700;text-align:right}
.tb td{padding:1.1mm 3mm;border-top:1px solid var(--line);font-weight:600;line-height:1.6}
.tb tr:nth-child(odd) td{background:#F7FAFD}
.tb td:first-child{font-size:15pt;text-align:center;font-weight:800;color:var(--nav);width:14mm}
.pr{background:#F4F1FD;border:1.2px solid #CFC4F4;border-radius:3mm;padding:2.5mm 4mm;font-size:11.3pt}
.pr>b{color:#5B3CC4}.pr ol{list-style:arabic-indic;margin:1.5mm 0;padding-inline-start:6mm;display:grid;grid-template-columns:1fr 1fr;gap:1mm 6mm;font-weight:600}
.pa{font-size:10.5pt;color:var(--ink2);font-weight:600;border-top:1px dashed #CFC4F4;padding-top:1.5mm}
.two{display:grid;grid-template-columns:1fr 1fr;gap:3mm}
footer{flex:none;display:flex;justify-content:space-between;align-items:center;margin:auto 11mm 0;padding:2mm 0 4.5mm;border-top:1.2px solid var(--line);font-size:10.5pt;font-weight:700;color:var(--nav)}
@page{size:A4;margin:0}
@media print{body{background:#fff}.page{margin:0;page-break-after:always}}
'''
BAD_DASH = re.compile(r'(?<![٠-٩0-9])\s[—–-]\s(?![٠-٩0-9])')
def build(out, title, pages):
    html = ''.join(f'<section class="page">{hd}<div class="body">{body}</div>{FOOT}</section>' for hd, body in pages)
    text = re.sub(r'<[^>]+>', ' ', html)
    bad = [m.group(0) for m in BAD_DASH.finditer(text)]
    assert not bad, f'شَرطة فاصلة في الملخّص: {bad[:3]}'
    open(out, 'w', encoding='utf-8').write(f'<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><title>{title}</title><style>{CSS}</style></head><body>{html}</body></html>')
    print(out)
