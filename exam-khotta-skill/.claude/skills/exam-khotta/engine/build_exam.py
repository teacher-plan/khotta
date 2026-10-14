#!/usr/bin/env python3
# يبني من ملف الاختبار (JSON) — guides/FORMAT.md:
#   <العنوان>_نموذج_أ.pdf/.docx، <العنوان>_نموذج_ب.pdf/.docx، <العنوان>_دليل_التصحيح.pdf/.docx (فيه شبكة المفردات)
# بعد التحقّق من مواصفات وثيقة التقويم (exam_lib.validate). لا يبني إن وُجد خطأ إلا بـ --force.
#
#   python3 <S>/engine/build_exam.py exam.json [--out مجلد] [--no-pdf] [--no-docx] [--check] [--log <P>/exams/log.json]
import argparse, base64, html, json, os, re, shutil, subprocess, sys, datetime
HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import notation
from exam_lib import (plain, ar, marks_word, load_json, find_config, load_spec, validate, grade_band,
                      LETTERS, TYPE_NAMES, tool_cfg, fields, key_columns, field_value, grid_model,
                      summary_model, KEY_WIDTHS, item_labels)

GRADE_AR = {5: 'الخامس', 6: 'السادس', 7: 'السابع', 8: 'الثامن', 9: 'التاسع', 10: 'العاشر', 11: 'الحادي عشر', 12: 'الثاني عشر'}
SEM_AR = {1: 'الأول', 2: 'الثاني'}
SUBJ_AR = {'math': 'الرياضيات', 'science': 'العلوم', 'arabic': 'اللغة العربية', 'english': 'اللغة الإنجليزية',
           'social': 'الدراسات الاجتماعية', 'islamic': 'التربية الإسلامية', 'it': 'تقنية المعلومات',
           'chemistry': 'الكيمياء', 'physics': 'الفيزياء', 'biology': 'الأحياء'}


# ═════════════ HTML ═════════════
def h(text, dg):
    return notation.html(text, dg)


def img_tag(path, base, width):
    p = path if os.path.isabs(path) else os.path.join(base, path)
    ext = os.path.splitext(p)[1].lower().strip('.').replace('jpg', 'jpeg')
    data = base64.b64encode(open(p, 'rb').read()).decode()
    return f'<div class="fig"><img src="data:image/{ext};base64,{data}" style="width:{width}%"></div>'


def lines_html(n):
    return '<div class="lines">' + '<div></div>' * n + '</div>' if n else ''


def item_html(k, it, dg, base):
    t = it['type']
    body = [f'<div class="stem">{h(it["stem"], dg)}</div>']
    if it.get('fig'):
        body.append(img_tag(it['fig'], base, it.get('fig_width', 45)))
    if t == 'mcq':
        cols = it.get('choice_cols', 4 if max(len(plain(c)) for c in it['choices']) < 14 else 2)
        rows = [it['choices'][i:i + cols] for i in range(0, len(it['choices']), cols)]
        tr = ''
        for r0, row in enumerate(rows):
            tr += '<tr>' + ''.join(f'<td><span class="circ">{LETTERS[r0 * cols + i]}</span> {h(c, dg)}</td>' for i, c in enumerate(row)) + '</tr>'
        body.append(f'<table class="choices">{tr}</table>')
    elif t == 'tf':
        body.append('<div class="tf">( &nbsp; صواب &nbsp; / &nbsp; خطأ &nbsp; )</div>')
        if it.get('explain', True):
            body.append('<div class="sub">فسّر إجابتك:</div>' + lines_html(it.get('lines', 2)))
    elif t == 'match':
        L, R = it['left'], it['right']
        rows = ''
        for i in range(max(len(L), len(R))):
            l = f'<td class="mn">{ar(i + 1)}</td><td>{h(L[i], dg)}</td><td class="mbox"></td>' if i < len(L) else '<td></td><td></td><td></td>'
            r = f'<td class="mn">{LETTERS[i]}</td><td>{h(R[i], dg)}</td>' if i < len(R) else '<td></td><td></td>'
            rows += f'<tr>{l}<td class="gap"></td>{r}</tr>'
        body.append(f'<table class="match"><tr><th colspan="3">{h(it.get("left_title", "العمود الأول"), dg)}</th><th class="gap"></th><th colspan="2">{h(it.get("right_title", "العمود الثاني"), dg)}</th></tr>{rows}</table>')
    elif t == 'order':
        cells = ''.join(f'<span class="ord">{h(x, dg)}</span>' for x in it['items'])
        body.append(f'<div class="ords">{cells}</div><div class="sub">الترتيب:</div>' + lines_html(it.get('lines', 1)))
    elif t == 'table':
        g = it['grid']
        tr = ''.join('<tr>' + ''.join(f'<{"th" if r == 0 and g.get("header", True) else "td"}>{h(c, dg) if c else "&nbsp;"}</{"th" if r == 0 and g.get("header", True) else "td"}>' for c in row) + '</tr>' for r, row in enumerate(g['rows']))
        body.append(f'<table class="grid">{tr}</table>' + lines_html(it.get('lines', 0)))
    else:
        default = 0 if it.get('parts') else {'long': 6, 'explain': 3, 'creative': 4, 'short': 1, 'fill': 0}.get(t, 2)
        body.append(lines_html(it.get('lines', default)))
    for p in it.get('parts', []):
        body.append(f'<div class="part"><b>({p["label"]})</b> {h(p["stem"], dg)}</div>' + lines_html(p.get('lines', 2)))
    return (f'<section class="item"><div class="qhead"><span class="qn">{k}</span></div>'
            f'<div class="qbody">{"".join(body)}</div><div class="mk">{marks_word(it["marks"])}</div></section>')


def header_html(exam, cfg, form, dg, key=False):
    g = int(exam['grade'])
    right = [cfg.get('country', 'سلطنة عُمان'), cfg.get('ministry', 'وزارة التربية والتعليم')]
    if cfg.get('directorate'):
        right.append(cfg['directorate'])
    if cfg.get('school'):
        right.append(cfg['school'])
    subj = SUBJ_AR.get(exam.get('subject'), exam.get('subject', ''))
    mid = [f'<b class="ttl">{html.escape(exam["title"])}</b>', f'مادة {subj} · الصف {GRADE_AR.get(g, g)}',
           f'الفصل الدراسي {SEM_AR.get(int(exam.get("semester", 1)), "")}']
    if key:
        mid.insert(1, '<b>دليل التصحيح وشبكة المفردات</b>')
    left = [f'العام الدراسي: {ar(cfg.get("year", exam.get("year", "")), dg)}', f'الزمن: {html.escape(exam.get("duration_short") or exam.get("duration", ""))}',
            f'الدرجة الكلية: {ar(exam["total"])}']
    if form:
        left.append(f'<b>النموذج ({form})</b>')
    col = lambda xs, c: f'<div class="{c}">' + '<br>'.join(xs) + '</div>'
    return f'<header>{col(right, "hr")}{col(mid, "hm")}{col(left, "hl")}</header>'


CSS = '''
@page { size: A4 %(orient)s; margin: 12mm 13mm 14mm; }
* { box-sizing: border-box; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { margin: 0; font-family: %(ff)s; font-weight: 500; font-size: %(fs)spt; line-height: %(lh)s; color: #111; direction: rtl; background: #fff; }
header { display: grid; grid-template-columns: 1fr 1.3fr 1fr; gap: 8px; border: 1.6px solid #222; border-radius: 6px; padding: 6px 10px; font-size: 10.5pt; line-height: 1.55; }
.hm { text-align: center; } .hl { text-align: left; } .ttl { font-size: 13.5pt; }
.student { display: flex; gap: 10px; align-items: stretch; margin: 8px 0 6px; font-size: 11pt; }
.student .nm { flex: 1; border: 1.2px solid #222; border-radius: 6px; padding: 6px 10px; }
.student .sc { width: 34mm; border: 1.6px solid #222; border-radius: 6px; text-align: center; padding: 4px; }
.student .sc b { display: block; font-size: 15pt; letter-spacing: 1px; }
.inst { font-size: 10.5pt; background: #f2f2f2; border-radius: 5px; padding: 4px 10px; margin-bottom: 4px; }
.item { display: grid; grid-template-columns: 9mm 1fr auto; gap: 6px; padding: 8px 0 6px; border-bottom: 1px dashed #bbb; break-inside: avoid; }
.qhead { display: flex; flex-direction: column; align-items: center; gap: 2px; }
.qn { display: inline-grid; place-items: center; min-width: 8mm; height: 8mm; padding: 0 1.5mm; border-radius: 4mm; background: #222; color: #fff; font-weight: 700; font-size: 11.5pt; }
.mk { font-size: 9pt; color: #222; white-space: nowrap; border: 1px solid #888; border-radius: 4px; padding: 0 6px; align-self: start; margin-top: 3px; }
.stem { font-weight: 600; }
.sub { margin-top: 4px; }
.part { margin-top: 6px; }
.lines div { height: 9mm; border-bottom: 1.2px dotted #666; }
.choices { width: 100%%; border-collapse: separate; border-spacing: 6px 4px; margin-top: 2px; }
.choices td { border: 1px solid #999; border-radius: 6px; padding: 3px 8px; vertical-align: middle; }
.circ { display: inline-grid; place-items: center; width: 6.5mm; height: 6.5mm; border: 1.3px solid #222; border-radius: 50%%; font-weight: 700; font-size: 10pt; margin-left: 4px; }
.tf { font-weight: 700; margin: 4px 0; }
table.match, table.grid { border-collapse: collapse; margin: 6px auto 2px; }
table.match td, table.match th, table.grid td, table.grid th { border: 1.2px solid #333; padding: 3px 10px; text-align: center; min-width: 14mm; }
table.match th, table.grid th { background: #ececec; }
table.match .gap { border: none; width: 10mm; min-width: 10mm; background: none; }
table.match .mbox { width: 12mm; }
table.grid td { height: 10mm; }
.ords { display: flex; flex-wrap: wrap; gap: 8px; margin: 4px 0; }
.ord { border: 1.2px solid #333; border-radius: 6px; padding: 1px 12px; }
.fig { text-align: center; margin: 4px 0; } .fig img { max-height: 70mm; object-fit: contain; }
.end { text-align: center; font-weight: 700; margin-top: 10px; }
.pt { text-align: center; font-weight: 700; margin-bottom: 4px; }
.psrc { text-align: left; font-size: .85em; margin-top: 4px; }
table.verses { margin: 0 auto; border-collapse: collapse; } table.verses td { padding: 1px 6px; text-align: justify; text-align-last: justify; min-width: 45mm; } table.verses td.gap { min-width: 12mm; }
.passage { border: 1.3px solid #444; border-radius: 6px; padding: 8px 12px; margin: 8px 0; line-height: 2; text-align: justify; break-inside: avoid; }
h3.grp { font-size: 12.5pt; margin: 10px 0 0; padding: 2px 10px; background: #ececec; border-radius: 5px; }
.foot { display: flex; justify-content: space-between; font-size: 9.5pt; color: #333; margin-top: 8px; }
/* دليل التصحيح */
h2 { font-size: 13pt; margin: 10px 0 4px; break-after: avoid; }
thead { display: table-header-group; }
table.key, table.spec, table.sum { width: 100%%; border-collapse: collapse; font-size: 10pt; line-height: 1.5; }
table.key th, table.key td, table.spec th, table.spec td, table.sum th, table.sum td { border: 1.1px solid #333; padding: 3px 6px; vertical-align: top; }
table.key th, table.spec th, table.sum th { background: #e6e6e6; }
table.key td.c, table.spec td, table.sum td { text-align: center; }
table.key tr, table.spec tr { break-inside: avoid; }
.ok { color: #0a6b2a; font-weight: 700; } .bad { color: #b00020; font-weight: 700; }
.sign { display: flex; justify-content: space-between; margin-top: 14px; font-size: 11pt; }
.formbreak { break-before: page; }
'''


def fonts_css():
    out = ''
    for f in ('fonts.css', 'fonts_ar.css'):
        p = os.path.join(HERE, 'assets', f)
        if os.path.exists(p):
            out += open(p, encoding='utf-8').read()
    return out


# خطّ المتن: readex (الرياضيات والعلوم، أرقام واضحة) أو amiri (نسخ للعربية والتربية الإسلامية: تشكيل كامل)
FONTS = {'readex': ("'KDigits', 'Readex Pro', sans-serif", 1.75, 0),
         'amiri': ("'Amiri', 'KDigits', serif", 2.0, 1.5)}
BODY_FONT = 'readex'


def page(body, orient='portrait', fs=12.5):
    ff, lh, extra = FONTS.get(BODY_FONT, FONTS['readex'])
    return (f'<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><style>{fonts_css()}{CSS % {"orient": orient, "fs": fs + extra, "ff": ff, "lh": lh}}</style></head>'
            f'<body>{body}</body></html>').replace('</style>', notation.CSS + '</style>', 1)


def paper_html(exam, cfg, form, items, dg, base):
    calc = calc_note(exam)
    inst = '؛ '.join(x for x in [exam.get('instructions', 'أجب عن جميع الأسئلة في الورقة نفسها'), calc] if x)
    stu = (f'<div class="student"><div class="nm">اسم الطالب: ...................................................................'
           f' &nbsp; الصف: ............</div><div class="sc">الدرجة<b>&nbsp;&nbsp;&nbsp; / {ar(exam["total"])}</b></div></div>')
    body = header_html(exam, cfg, form, dg) + stu + f'<div class="inst">{html.escape(inst)}.</div>'
    labels = iter(item_labels(items)); grp = None
    for it in items:
        if it.get('group') and it['group'] != grp:   # «السؤال الأول» ثم مفرداته (أ، ب، ج)
            grp = it['group']; body += f'<h3 class="grp">السؤال {html.escape(grp)}</h3>'
        if it.get('type') == 'passage':   # نص القراءة أو الأبيات: بلا رقم ولا درجة
            t = f'<div class="pt">{h(it["title"], dg)}</div>' if it.get('title') else ''
            v = ''
            if it.get('verses'):   # أبيات: الصدر والعجز في عمودين
                v = '<table class="verses">' + ''.join(f'<tr><td>{h(a_, dg)}</td><td class="gap"></td><td>{h(b_, dg)}</td></tr>' for a_, b_ in it['verses']) + '</table>'
            src = f'<div class="psrc">{h(it["source"], dg)}</div>' if it.get('source') else ''
            body += f'<div class="passage">{t}{h(it.get("body", ""), dg)}{v}{src}</div>'
            continue
        body += item_html(next(labels)[0], it, dg, base)
    body += f'<div class="end">انتهت الأسئلة، مع تمنياتنا لكم بالتوفيق</div>'
    tname = cfg.get('teacher_name', '')
    if tname:
        body += f'<div class="foot"><span>معلّم المادّة: {html.escape(tname)}</span><span></span></div>'
    return page(body)


def answer_html(it, dg):
    t = it['type']
    if t == 'mcq':
        a = it['answer']
        return f'<b>({LETTERS[a]})</b> {h(it["choices"][a], dg)}'
    if t == 'match' and it.get('pairs'):
        return '، '.join(f'{ar(i + 1)} ← {LETTERS[j]}' for i, j in enumerate(it['pairs']))
    parts = []
    if it.get('answer') not in (None, ''):
        parts.append(h(it['answer'], dg))
    if it.get('steps'):
        parts.append('<br>'.join(h(s, dg) for s in it['steps']))
    return '<br>'.join(parts)


def key_cell(exam, spec, it, f, k, dg):
    if f == 'n':
        return k
    if f == 'marks':
        return ar(it.get('marks', 0))
    if f == 'answer':
        return answer_html(it, dg)
    if f in ('objective', 'page', 'guidance'):
        return h(it.get(f, ''), dg)
    return html.escape(str(field_value(spec, it, f, exam)))


def key_html(exam, cfg, spec, dg):
    tool = tool_cfg(spec, exam['kind'], exam['grade'], exam.get('number'))
    body = header_html(exam, cfg, None, dg, key=True)
    lessons = '، '.join(f'{l["code"]} {l.get("title", "")}' if isinstance(l, dict) else l for l in exam['lessons'])
    body += f'<div class="inst">الدروس: {html.escape(lessons)} · المرجع: {html.escape(spec["document"]["title"])}، {html.escape(spec["document"]["edition"])}</div>'
    cols = key_columns(spec, tool)
    tw = sum(KEY_WIDTHS.get(f, 9) for _, f in cols)
    for n, (form, items) in enumerate(exam['forms'].items()):
        items = [i for i in items if i.get('type') != 'passage']
        cls = ' class="formbreak"' if n else ''
        body += f'<h2{cls}>شبكة مفردات النموذج ({form})</h2>'
        heads, rows = grid_model(spec, items)
        body += ('<table class="spec"><tr>' + ''.join(f'<th>{x}</th>' for x in heads) + '</tr>'
                 + ''.join('<tr>' + ''.join(f'<td>{html.escape(x)}</td>' for x in r) + '</tr>' for r in rows) + '</table>')
        body += summary_table(spec, tool, items)
        body += f'<h2>دليل التصحيح — النموذج ({form})</h2>'
        th = ''.join(f'<th style="width:{KEY_WIDTHS.get(f, 9) * 100 / tw:.0f}%">{c}</th>' for c, f in cols)
        rows = ''.join('<tr>' + ''.join(f'<td class="{"c" if f not in ("objective", "answer", "guidance") else ""}">{key_cell(exam, spec, it, f, lab[1], dg)}</td>'
                                        for _, f in cols) + '</tr>' for lab, it in zip(item_labels(items), items))
        mi = [f for _, f in cols].index('marks') if 'marks' in [f for _, f in cols] else None
        tot = ''
        if mi is not None:
            tot = (f'<tr><th colspan="{mi}">المجموع</th><th>{ar(sum(i["marks"] for i in items))}</th>'
                   + (f'<th colspan="{len(cols) - mi - 1}"></th>' if len(cols) - mi - 1 else '') + '</tr>')
        body += f'<table class="key"><thead><tr>{th}</tr></thead><tbody>{rows}{tot}</tbody></table>'
    sup = cfg.get('reviewer_title', 'المعلّم الأول')
    body += (f'<div class="sign"><span>إعداد: {html.escape(cfg.get("teacher_name", "........................"))}</span>'
             f'<span>مراجعة {html.escape(sup)}: ........................ التوقيع: ............</span></div>')
    return page(body, 'landscape', 11)


def summary_table(spec, tool, items):
    sm = summary_model(spec, tool, items)
    def cell(v, want):
        if want is None:
            return f'<td>{ar(v)}</td>'
        return f'<td class="{"ok" if v == want else "bad"}">{ar(v)} / {ar(want)}</td>'
    head = ''.join(f'<th>{html.escape(l)}</th>' for l, _, _ in sm)
    row = ''.join(cell(v, w) for _, v, w in sm)
    return f'<table class="sum" style="margin-top:6px"><tr>{head}</tr><tr>{row}</tr></table>'


def calc_note(exam):
    if exam.get('calculator') is not None:
        return 'يُسمح باستخدام الآلة الحاسبة' if exam['calculator'] else 'لا يُسمح باستخدام الآلة الحاسبة'
    return ''


# ═════════════ PDF (Chromium) ═════════════
def to_pdf(html_path, pdf_path):
    js = os.path.join(HERE, 'pdf.mjs')
    env = dict(os.environ)
    if not env.get('CHROMIUM_PATH') and os.path.exists('/opt/pw-browsers/chromium'):
        env['CHROMIUM_PATH'] = '/opt/pw-browsers/chromium'
    r = subprocess.run(['node', js, html_path, pdf_path], capture_output=True, text=True, env=env)
    if r.returncode != 0:
        raise RuntimeError((r.stderr or r.stdout).strip()[-400:])


# ═════════════ Word (python-docx) ═════════════
def all_texts(exam):
    keys = ('stem', 'answer', 'guidance', 'objective', 'page', 'body', 'title')
    for items in exam['forms'].values():
        for it in items:
            for k in keys:
                if isinstance(it.get(k), str):
                    yield it[k]
            for k in ('choices', 'steps', 'left', 'right', 'items'):
                for x in it.get(k, []) or []:
                    yield str(x)
            for prt in it.get('parts', []):
                yield prt.get('stem', '')
            for row in (it.get('grid') or {}).get('rows', []):
                for c in row:
                    yield str(c)


def make_snipper(exam, dg, workdir):
    """يرسم كل جذر في الاختبار صورةً (Chromium) لـ Word، ويعيد دالة: عقدة ← (مسار، العرض pt، الارتفاع pt) أو None."""
    import hashlib
    found = {}
    def walk(ns):
        for n in ns:
            if n[0] == 'root':
                hh = notation.to_html([n]); found[hashlib.md5(hh.encode()).hexdigest()[:12]] = hh
            for x in n[1:]:
                if isinstance(x, list):
                    walk(x)
    for t in all_texts(exam):
        walk(notation.parse(t, dg))
    if not found:
        return None
    os.makedirs(workdir, exist_ok=True)
    items = [{'id': k, 'html': v, 'out': os.path.join(workdir, k + '.png')} for k, v in found.items()]
    jobs = os.path.join(workdir, 'jobs.json')
    json.dump({'css': fonts_css() + notation.CSS, 'items': items}, open(jobs, 'w', encoding='utf-8'), ensure_ascii=False)
    env = dict(os.environ)
    if not env.get('CHROMIUM_PATH') and os.path.exists('/opt/pw-browsers/chromium'):
        env['CHROMIUM_PATH'] = '/opt/pw-browsers/chromium'
    r = subprocess.run(['node', os.path.join(HERE, 'snips.mjs'), jobs], capture_output=True, text=True, env=env)
    if r.returncode != 0:
        print('⚠ تعذّر رسم الجذور صوراً لـ Word (تظهر بعلامة غير معكوسة):', (r.stderr or '')[-200:])
        return None
    sizes = {}
    from PIL import Image
    for it in items:   # قصّ الهوامش الشفافة؛ المقاس بالنقاط = البكسل ÷ ٥ (دقّة الرسم) × ٠٫٧٥
        im = Image.open(it['out']); bb = im.getbbox()
        if bb:
            im = im.crop((max(0, bb[0] - 4), 0, min(im.width, bb[2] + 4), im.height)); im.save(it['out'])
        sizes[it['id']] = (im.width / 5 * 0.75, im.height / 5 * 0.75)
    def snip(node):
        k = hashlib.md5(notation.to_html([node]).encode()).hexdigest()[:12]
        if k in sizes:
            return (os.path.join(workdir, k + '.png'),) + tuple(sizes[k])
        return None
    return snip


def docx_build(exam, cfg, spec, dg, base, out_base):
    from docx_writer import DocxExam
    snip = make_snipper(exam, dg, out_base + '_صور')
    default_font = 'Traditional Arabic' if BODY_FONT == 'amiri' else 'Arial'
    W = DocxExam(exam.get('docx_font') or spec.get('docx_font') or cfg.get('docx_font', default_font), dg, snip,
                 cfg.get('quran_font', 'Traditional Arabic'))
    files = []
    for form, items in exam['forms'].items():
        d = W.paper(exam, cfg, form, items, base, header_lines(exam, cfg, form, dg), calc_note(exam))
        f = f'{out_base}_نموذج_{form}.docx'; W.save(d, f); files.append(f)
    d = W.key(exam, cfg, spec, header_lines(exam, cfg, None, dg, key=True))
    f = f'{out_base}_دليل_التصحيح.docx'; W.save(d, f); files.append(f)
    return files


def header_lines(exam, cfg, form, dg, key=False):
    g = int(exam['grade'])
    right = [cfg.get('country', 'سلطنة عُمان'), cfg.get('ministry', 'وزارة التربية والتعليم')] + [x for x in (cfg.get('directorate'), cfg.get('school')) if x]
    subj = SUBJ_AR.get(exam.get('subject'), exam.get('subject', ''))
    mid = [exam['title']] + (['دليل التصحيح وشبكة المفردات'] if key else []) + [f'مادة {subj} · الصف {GRADE_AR.get(g, g)}', f'الفصل الدراسي {SEM_AR.get(int(exam.get("semester", 1)), "")}']
    left = [f'العام الدراسي: {ar(cfg.get("year", exam.get("year", "")), dg)}', f'الزمن: {exam.get("duration_short") or exam.get("duration", "")}', f'الدرجة الكلية: {ar(exam["total"])}'] + ([f'النموذج ({form})'] if form else [])
    return right, mid, left


# ═════════════ الآيات: quran[112:1-4] ← النص الموثّق ═════════════
QREF = re.compile(r'quran\[(\d{1,3}(?::\d{1,3}(?:-\d{1,3})?)?)(?:\|(uthmani|imlaei))?\](?:\{([^{}]*)\})?')


def resolve_quran(exam, base):
    """يستبدل quran[المرجع] بنصّ الآيات من quran.com (مع ذاكرة مؤقتة بجانب الملف)، ويتحقّق من quran[المرجع]{نص}."""
    raw = json.dumps(exam, ensure_ascii=False)
    if 'quran[' not in raw:
        return exam
    sys.path.insert(0, os.path.join(HERE, 'tools'))
    import quran as Q
    cache_p = os.path.join(base, '.quran_cache.json')
    cache = load_json(cache_p) if os.path.exists(cache_p) else {}
    errs = []
    def rep(m):
        ref, script, given = m.group(1), m.group(2) or 'uthmani', m.group(3)
        key = f'{ref}|{script}'
        if key not in cache:
            try:
                s_, x, y, name = Q.parse_ref(ref)
                vs = Q.fetch(s_, x, y, script)
                cache[key] = {'text': ' '.join(f'{t} ({Q.num(n)})' if y != x else t for n, t in vs),
                              'label': f'[{name}: {Q.num(x)}{"–" + Q.num(y) if y != x else ""}]'}
            except BaseException as e:
                errs.append(f'تعذّر جلب الآية {ref} ({e})؛ الصق نصّها من كتاب الطالب داخل quran{{…}}')
                return m.group(0)
        c = cache[key]
        if given is not None:   # اقتباس: يجب أن يكون جزءاً متّصلاً من الآية (أو الآيات) حرفاً حرفاً
            g = Q.strip_marks(re.sub(r'\s*\([٠-٩]+\)', '', given))
            w = Q.strip_marks(re.sub(r'\s*\([٠-٩]+\)', '', c['text']))
            if not g or g not in w:
                errs.append(f'الاقتباس من الآية {ref} لا يطابق المصدر «{given}»؛ نصّ الآية: {c["text"]}')
            return 'quran{' + given.replace('"', '\\"') + '}'
        return 'quran{' + c['text'].replace('"', '\\"') + '} ' + c['label']
    raw = QREF.sub(rep, raw)
    json.dump(cache, open(cache_p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    if errs:
        for e in errs:
            print('  ✘', e)
        sys.exit(1)
    return json.loads(raw)


# ═════════════ main ═════════════
def safe(s):
    return re.sub(r'[\\/:*?"<>|]+', '-', s).replace(' ', '_')


def main():
    ap = argparse.ArgumentParser(description='بناء الاختبار القصير أو السؤال القصير')
    ap.add_argument('exam'); ap.add_argument('--out'); ap.add_argument('--no-pdf', action='store_true'); ap.add_argument('--no-docx', action='store_true')
    ap.add_argument('--check', action='store_true', help='تحقّق فقط'); ap.add_argument('--force', action='store_true')
    ap.add_argument('--log', help='سجلّ الاختبارات <P>/exams/log.json (لمنع تكرار أهداف السؤال القصير)')
    a = ap.parse_args()
    exam = load_json(a.exam); base = os.path.dirname(os.path.abspath(a.exam))
    exam = resolve_quran(exam, base)
    cfg = {**find_config(base), **exam.get('header', {})}
    spec = load_spec(SKILL, exam.get('spec') or f'{exam.get("subject", "math")}-5-10')
    tool = tool_cfg(spec, exam['kind'], exam['grade'], exam.get('number')) or {}
    if not tool or tool.get('_no_band'):
        print(f'✘ لا مواصفات لـ«{exam["kind"]}» للصف {exam["grade"]} في {spec["id"]}'); sys.exit(1)
    exam.setdefault('total', tool.get('total'))
    exam.setdefault('duration', tool.get('duration_text', ''))
    exam.setdefault('duration_short', tool.get('duration_short', ''))
    if exam.get('calculator') is None and tool.get('calculator') is not None:
        exam['calculator'] = tool['calculator']
    dg = exam.get('digits') or spec.get('digits') or cfg.get('digits', 'ar')
    global BODY_FONT
    BODY_FONT = exam.get('font') or spec.get('font') or cfg.get('font') or 'readex'
    log = load_json(a.log) if a.log and os.path.exists(a.log) else []
    errs, warns = validate(exam, spec, log, dg)
    print(f'التحقّق من مواصفات {spec["document"]["title"]} ({spec["document"]["edition"]}) — {tool["name"]}:')
    for e in errs:
        print('  ✘', e)
    for w in warns:
        print('  ⚠', w)
    if not errs:
        print('  ✔ مطابق للمواصفات' + (' (مع تنبيهات)' if warns else ''))
    if a.check:
        sys.exit(1 if errs else 0)
    if errs and not a.force:
        print('لم يُبنَ شيء: صحّح الأخطاء أعلاه (أو --force للمعاينة فقط).'); sys.exit(1)
    out = a.out or base; os.makedirs(out, exist_ok=True)
    ob = os.path.join(out, safe(exam['title']))
    made = []
    htmls = []
    for form, items in exam['forms'].items():
        p = f'{ob}_نموذج_{form}.html'; open(p, 'w', encoding='utf-8').write(paper_html(exam, cfg, form, items, dg, base)); htmls.append(p)
    p = f'{ob}_دليل_التصحيح.html'; open(p, 'w', encoding='utf-8').write(key_html(exam, cfg, spec, dg)); htmls.append(p)
    if not a.no_pdf:
        try:
            for p in htmls:
                to_pdf(p, p[:-5] + '.pdf'); made.append(p[:-5] + '.pdf')
        except Exception as e:
            print('⚠ تعذّر إنشاء PDF (Playwright/Chromium):', e, '— اطبع ملفات HTML إلى PDF من المتصفّح.')
            made += htmls
    if not a.no_docx:
        try:
            made += docx_build(exam, cfg, spec, dg, base, ob)
        except ImportError:
            print('⚠ python-docx غير مثبّت: pip install python-docx')
    if log is not None and a.log and not errs:
        objs = sorted({it['objective'] for items in exam['forms'].values() for it in items if it.get('type') != 'passage' and it.get('objective')})
        ident = lambda e: (e.get('subject'), e.get('grade'), e.get('semester'), e.get('kind'), e.get('title'))
        me = {'subject': exam.get('subject'), 'grade': exam.get('grade'), 'semester': exam.get('semester'), 'kind': exam['kind'], 'title': exam['title']}
        log = [e for e in log if ident(e) != ident(me)] + [{**me, 'date': str(datetime.date.today()),
               'lessons': [l['code'] if isinstance(l, dict) else l for l in exam['lessons']], 'objectives': objs}]
        os.makedirs(os.path.dirname(os.path.abspath(a.log)), exist_ok=True)
        json.dump(log, open(a.log, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('الملفات:')
    for f in made:
        print(' ', f)


if __name__ == '__main__':
    main()
