# قالب «مخزن خُطّة» للطباعة — يُنفَّذ بعد summary2.py (exec) فيستبدل رأس الصفحة وتذييلها وألوانها.
# المواصفات الملزمة: .claude/skills/khotta-store/ (SKILL.md و references/).
#
# • أبيض وأسود: لا خلفيات ملوّنة ولا نصّ ملوّن ولا رموز تعبيرية ملوّنة، والتعبئة رماديةٌ فاتحة (≤ ١٢٪) فقط.
# • الرأس: المادة · الصف · الفصل الدراسي · العام الدراسي، ثم نوع الملف والوحدة، ثم «الدرس <رمزه>: <اسمه>».
# • التذييل: «جميع الحقوق محفوظة © منصّة خُطّة» يميناً و khotati.com يساراً، ولا شيء غيرهما.
#
# بيانات الرأس من STORE_META (يضبطها المولِّد) أو من متغيّرات البيئة KH_SUBJECT/KH_GRADE/KH_SEM/KH_YEAR.
import os
STORE_META = {
    'subject': os.environ.get('KH_SUBJECT', 'الرياضيات'),
    'grade': os.environ.get('KH_GRADE', 'السابع'),
    'semester': os.environ.get('KH_SEM', 'الأول'),
    'year': os.environ.get('KH_YEAR', '٢٠٢٦ / ٢٠٢٧'),
    'kind': os.environ.get('KH_KIND', 'ملخّص الدرس'),
}

def header(code, title, unit, goal, kind=None):
    m = STORE_META
    k = kind or m['kind']
    lesson = f'الدرس {code}: {title}' if code[:1] in '٠١٢٣٤٥٦٧٨٩' else title
    return f'''<header class="st"><div class="meta"><span>المادة: <b>{m["subject"]}</b></span><span>الصف: <b>{m["grade"]}</b></span><span>الفصل الدراسي: <b>{m["semester"]}</b></span><span>العام الدراسي: <b>{m["year"]}</b></span></div>
<div class="row2"><span class="kind">{k}</span><span class="unit">{unit}</span></div><h1>{lesson}</h1></header>
<div class="goal"><b>الهدف:</b><span>{goal}</span></div>'''

FOOT = '<footer><span>جميع الحقوق محفوظة © منصّة خُطّة</span><span class="url">khotati.com</span></footer>'

# المكوّنات بلا رموزٍ تعبيرية ملوّنة: وسومٌ نصّية بحدود
def rule(t, icon=''): return f'<div class="rule"><b class="tag">قاعدة</b><div>{t}</div></div>'
def example(q, steps, ans=None, title='مثال محلول'):
    rows = ''.join(f'<tr><td class="n">{a(i + 1)}</td><td class="e">{e}</td><td class="r">{r}</td></tr>' for i, (e, r) in enumerate(steps))
    return f'''<div class="ex"><div class="exh"><b class="tag">{title}</b><span>{q}</span></div><table>{rows}</table>{f'<div class="ans">الإجابة: {ans}</div>' if ans else ''}</div>'''
def warn(items):
    return '<div class="warn"><b class="tag">انتبه</b>' + ''.join(f'<div class="wr"><span class="bad">✗ {b}</span><span class="good">✓ {g}</span><small>{w}</small></div>' for b, g, w in items) + '</div>'
def practice(qs, ans):
    return '<div class="pr"><b class="tag">تدرّب</b><ol>' + ''.join(f'<li>{q}</li>' for q in qs) + '</ol><div class="pa">الإجابات: ' + '، '.join(f'({a(i + 1)}) {x}' for i, x in enumerate(ans)) + '</div></div>'

STORE_CSS = r'''
:root{--ink:#111;--ink2:#444;--nav:#111;--teal:#111;--rule:#111;--rulebg:#fff;--ex:#111;--exbg:#F1F1F1;--w:#111;--wbg:#fff;--v:#111;--line:#9A9A9A}
body{background:#E9E9E9}
header.st{background:#fff;color:#111;padding:3mm 11mm 2mm;border-bottom:1.6px solid #111}
header.st::after{content:none}
header.st .meta{display:flex;flex-wrap:wrap;gap:1mm 6mm;font-size:10pt;font-weight:600;color:#333;border-bottom:1px solid #BDBDBD;padding-bottom:1.2mm;margin-bottom:1.2mm}
header.st .meta b{color:#111;font-weight:800}
header.st .row2{display:flex;gap:3mm;align-items:center;font-size:10.5pt;font-weight:700;color:#333}
header.st .unit{color:#333;font-size:10.5pt}
.page .body{gap:2mm}.sec{gap:1.4mm}
header.st .kind{border:1.4px solid #111;border-radius:1.5mm;padding:.3mm 3mm;color:#111;font-weight:800}
header.st h1{margin:.8mm 0 0;font-size:17pt;color:#111}
.goal{background:#fff;border:1px solid #9A9A9A;border-radius:1.5mm;color:#111}
.goal b{color:#111}
.tag{display:inline-block;border:1.3px solid #111;border-radius:1.2mm;padding:0 2.2mm;font-size:10pt;font-weight:800;color:#111;background:#fff;white-space:nowrap;line-height:1.7}
.sec>h2{color:#111;border-bottom:1.2px solid #111;padding-bottom:.8mm}
.sec>h2 i{background:#111}
.rule{background:#fff;border:1.2px solid #111;border-inline-start:2.2mm solid #111}
.ex{border:1.2px solid #777}
.exh{background:#F1F1F1;border-bottom:1px solid #BDBDBD}
.ex td{border-bottom:1px dashed #C8C8C8}
.ex td.n{background:#111}
.ans{background:#F1F1F1;color:#111;border-top:1.2px solid #111}
.ans .op,.ans .v{color:#111}
.warn{background:#fff;border:1.2px dashed #111}
.wr .bad,.wr .good{color:#111}.wr .bad{text-decoration:line-through;text-decoration-thickness:1px}
.tb th{background:#E3E3E3;color:#111;border-bottom:1.2px solid #111}
.tb tr:nth-child(odd) td{background:#fff}.tb td:first-child{color:#111}
.tb.area td:nth-child(2),.tb.area td:nth-child(3){background:#F1F1F1}
.pr{background:#fff;border:1.2px solid #777}.pr>b{color:#111}.pa{border-top:1px dashed #9A9A9A}
footer{color:#333;border-top:1.2px solid #111;font-weight:600}
footer .url{direction:ltr;font-weight:800;color:#111;letter-spacing:.3px}
.op{color:#333}.v{color:#111;text-decoration:underline;text-decoration-thickness:1px;text-underline-offset:2px}
/* شبكة الأمان: أي لونٍ بقي في رسمٍ أو رمز يُطبع رمادياً */
.page svg,.page img{filter:grayscale(1)}
.lvl{background:#fff!important;color:#111!important;border:1.2px solid #111}
.lvl b{display:none}
.mk{background:#fff;border:1.2px solid #111;color:#111}
.kh{background:#fff;border:1.2px solid #111;color:#111}
.ka{background:#F1F1F1;color:#111;border:1px solid #777}
.qn{background:#111}
.gt th{background:#E3E3E3;color:#111;border-bottom:1.2px solid #111}
.score span{border-color:#111}.score{color:#111}
.sbar{color:#111}
@media print{body{background:#fff}}
'''
_store_base_build = build
def build(out, title, pages):
    global CSS
    if STORE_CSS not in CSS:
        CSS += STORE_CSS
    return _store_base_build(out, title, pages)
