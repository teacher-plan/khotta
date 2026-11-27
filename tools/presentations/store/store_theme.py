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
# ألوان منصّة خُطّة وأيقوناتها وشعارها: للملخّصات (طلب الأستاذ عيسى، ٢٧ نوفمبر). أوراق العمل والاختبارات تبقى
# أبيض وأسود لأنها تُطبع بالعشرات. KH_BRAND=1/0 يفرض أحدهما؛ والافتراض: الملخّص ملوّن.
_kb = os.environ.get('KH_BRAND')
STORE_BRAND = (_kb == '1') if _kb in ('0', '1') else ('ملخّص' in STORE_META['kind'])
import json as _json, base64 as _b64
_KI = _json.load(open(os.path.join(KIT, 'store', 'ki_icons.json'), encoding='utf-8'))
def ICON(name, cls='ic'):
    """أيقونة من أيقونات المنصّة (ki-*، مستخرجة من cycle1.html) بلون النصّ المحيط."""
    if not STORE_BRAND: return ''
    return _KI[name].replace('stroke="black"', 'stroke="currentColor"').replace('<svg ', f'<svg class="{cls}" aria-hidden="true" ', 1)
_LOGO = 'data:image/png;base64,' + _b64.b64encode(open(os.path.join(KIT, '..', '..', 'khottah_icon_192.png'), 'rb').read()).decode() if STORE_BRAND else ''

def header(code, title, unit, goal, kind=None):
    m = STORE_META
    k = kind or m['kind']
    lesson = f'الدرس {code}: {title}' if code[:1] in '٠١٢٣٤٥٦٧٨٩' else title
    logo = f'<img class="logo" src="{_LOGO}" alt="خُطّة"/>' if STORE_BRAND else ''
    return f'''<header class="st">{logo}<div class="meta"><span>المادة: <b>{m["subject"]}</b></span><span>الصف: <b>{m["grade"]}</b></span><span>الفصل الدراسي: <b>{m["semester"]}</b></span><span>العام الدراسي: <b>{m["year"]}</b></span></div>
<div class="row2"><span class="kind">{ICON('book')}{k}</span><span class="unit">{unit}</span></div><h1>{lesson}</h1></header>
<div class="goal"><b>{ICON('target')}الهدف:</b><span>{goal}</span></div>'''

FOOT = '<footer><span>جميع الحقوق محفوظة © منصّة خُطّة</span><span class="url">khotati.com</span></footer>'

# المكوّنات بلا رموزٍ تعبيرية ملوّنة: وسومٌ نصّية بحدود
def rule(t, icon=''): return f'<div class="rule"><b class="tag">{ICON('bulb')}قاعدة</b><div>{t}</div></div>'
def example(q, steps, ans=None, title='مثال محلول'):
    rows = ''.join(f'<tr><td class="n">{a(i + 1)}</td><td class="e">{e}</td><td class="r">{r}</td></tr>' for i, (e, r) in enumerate(steps))
    return f'''<div class="ex"><div class="exh"><b class="tag">{ICON('pen')}{title}</b><span>{q}</span></div><table>{rows}</table>{f'<div class="ans">الإجابة: {ans}</div>' if ans else ''}</div>'''
def warn(items):
    return f'<div class="warn"><b class="tag">{ICON("alert")}انتبه</b>' + ''.join(f'<div class="wr"><span class="bad">✗ {b}</span><span class="good">✓ {g}</span><small>{w}</small></div>' for b, g, w in items) + '</div>'
def practice(qs, ans):
    return f'<div class="pr"><b class="tag">{ICON("brain")}تدرّب</b><ol>' + ''.join(f'<li>{q}</li>' for q in qs) + '</ol><div class="pa">الإجابات: ' + '، '.join(f'({a(i + 1)}) {x}' for i, x in enumerate(ans)) + '</div></div>'

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
.tb td:first-child{font-size:12pt;width:auto}
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
# ── نسخة الملخّص بألوان المنصّة: فاتحة صالحة للطباعة (تعبئاتٌ كريمية خفيفة، ولونٌ للحدود والعناوين) ──
BRAND_CSS = r'''
:root{--k-red:#D86048;--k-red-d:#A83030;--k-deep:#7A2020;--k-olive:#487848;--k-olive-d:#35603A;--k-ink:#301800;--k-muted:#7A6350;--k-cream:#F7EEE2;--k-card:#FBF4EA;--k-border:#E3D2BD;
 --ink:#301800;--ink2:#7A6350;--v:#A83030;--line:#E3D2BD}
body{background:#EFE6DA;color:var(--k-ink)}
.ic{width:1.1em;height:1.1em;flex:none;vertical-align:-.18em;margin-inline-end:1.2mm}
header.st{background:var(--k-cream);border-bottom:2px solid var(--k-red-d);position:relative;padding-inline-end:26mm}
header.st .logo{position:absolute;left:11mm;top:50%;transform:translateY(-50%);width:16mm;height:16mm;border-radius:3.5mm;box-shadow:0 0 0 1px var(--k-border)}
header.st .meta{color:var(--k-muted);border-bottom-color:var(--k-border)}header.st .meta b{color:var(--k-ink)}
header.st .unit{color:var(--k-muted)}
header.st .kind{border-color:var(--k-red-d);color:var(--k-red-d);background:#fff;display:inline-flex;align-items:center}
header.st h1{color:var(--k-ink)}
.goal{background:#FFFDF9;border-color:var(--k-border);border-inline-start:2mm solid var(--k-red)}
.goal b{color:var(--k-red-d);display:inline-flex;align-items:center}
.tag{display:inline-flex;align-items:center;border-color:currentColor}
.sec>h2{color:var(--k-ink);border-bottom-color:var(--k-red)}
.sec>h2 i{background:var(--k-red-d)}
.rule{background:#F4F8F2;border-color:#B9D1B5;border-inline-start-color:var(--k-olive)}
.rule .tag{color:var(--k-olive-d)}
.ex{border-color:var(--k-border)}
.exh{background:var(--k-card);border-bottom-color:var(--k-border)}.exh .tag{color:var(--k-red-d)}
.ex td{border-bottom-color:#EFE3D3}.ex td.n{background:var(--k-red-d)}
.ans{background:var(--k-card);color:var(--k-deep);border-top-color:var(--k-red-d)}
.ans .op,.ans .v{color:var(--k-deep)}
.warn{background:#FFF6F3;border-color:var(--k-red)}.warn .tag{color:var(--k-red-d)}
.wr .bad{color:var(--k-red-d)}.wr .good{color:var(--k-olive-d)}
.tb th{background:var(--k-cream);color:var(--k-ink);border-bottom-color:var(--k-red-d)}
.tb td:first-child{color:var(--k-red-d)}
.tb.area td:nth-child(2){background:#F4F8F2}.tb.area td:nth-child(3){background:var(--k-card)}
.pr{background:#FFFDF9;border-color:var(--k-border)}.pr .tag{color:var(--k-olive-d)}.pa{border-top-color:var(--k-border)}
footer{color:var(--k-muted);border-top-color:var(--k-red-d)}footer .url{color:var(--k-red-d)}
.op{color:var(--k-muted)}.v{color:var(--k-red-d);text-decoration:none}
.page svg,.page img{filter:none}
'''
_store_base_build = build
def build(out, title, pages):
    global CSS
    if STORE_CSS not in CSS:
        CSS += STORE_CSS + (BRAND_CSS if STORE_BRAND else '')
    return _store_base_build(out, title, pages)
