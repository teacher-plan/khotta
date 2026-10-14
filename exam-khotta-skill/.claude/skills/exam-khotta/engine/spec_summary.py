#!/usr/bin/env python3
# ملخّص مقروء لمواصفات مادّة (من ملف specs/*.json نفسه الذي يفحص به المحرّك، فلا يختلفان):
#   python3 spec_summary.py arabic-5-12                 ← كل الأدوات والصفوف
#   python3 spec_summary.py islamic-5-12 --grade 7      ← ما يخصّ الصف السابع فقط
#   python3 spec_summary.py --all --md <S>/specs        ← يكتب <المعرّف>.md لكل مواصفات (للمحادثات وللقراءة)
import argparse, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); SKILL = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from exam_lib import load_spec, fields, tool_cfg, TYPE_NAMES, ar


def rng(r):
    if r is None:
        return '—'
    return ar(r) if isinstance(r, int) else f'{ar(r[0])}–{ar(r[1])}'


def band_lines(spec, tool_id, tool, grade, number=None):
    F = fields(spec)
    c = tool_cfg(spec, tool_id, grade, number)
    out = []
    if c.get('total') is not None:
        out.append(f'- الدرجة: **{ar(c["total"])}**')
    elif c.get('graded') is False:
        out.append('- **تكويني لا يُرصد درجةً**')
    if c.get('items'):
        out.append(f'- المفردات: {rng(c["items"])}')
    if c.get('lessons'):
        out.append(f'- الدروس: {rng(c["lessons"])}')
    for f, want in (c.get('dist') or {}).items():
        if f in F:
            out.append(f'- حسب {F[f]["label"]}: ' + '، '.join(f'{F[f]["values"].get(v, v)} {ar(n)}' for v, n in want.items()))
    tr = c.get('types_rule')
    if tr:
        parts = []
        if tr.get('mcq'):
            parts.append(f'اختيار من متعدد: {rng(tr["mcq"]["count"])} (درجة كلٍّ {rng(tr["mcq"].get("each"))})')
        if tr.get('long'):
            parts.append(f'إجابة طويلة: {rng(tr["long"].get("count", 1))} بدرجة {rng(tr["long"].get("marks"))}')
        elif 'long' in tr:
            parts.append('بلا إجابة طويلة')
        if tr.get('other'):
            o = tr['other']
            parts.append('أنواع أخرى' + (f': {rng(o.get("count"))} مفردات' if o.get('count') else '') + (f'، مجموعها {rng(o.get("marks"))}' if o.get('marks') else '') + (f'، كلٌّ {rng(o.get("each"))}' if o.get('each') else ''))
        out.append('- الأنواع: ' + '؛ '.join(parts))
    if c.get('forbid_types'):
        out.append('- **ممنوع:** ' + '، '.join(TYPE_NAMES.get(t, t) for t in c['forbid_types']))
    if c.get('slots'):
        out.append('- **البنية الثابتة:**')
        for sl in c['slots']:
            out.append('  - ' + '، '.join(F[k]['values'].get(v, v) for k, v in sl.items() if k in F) + f' — {ar(sl.get("marks", 0))}')
    if c.get('calculator') is not None:
        out.append(f'- الآلة الحاسبة: {"مسموحة" if c["calculator"] else "ممنوعة"}')
    if c.get('grids'):
        out.append('- شبكات مقترحة في الوثيقة: ' + '، '.join(c['grids']))
    return out


def summary(spec, grade=None):
    d = spec['document']
    L = [f'# مواصفات {spec["id"]}', '', f'> **{d["title"]}** — {d["edition"]}', f'> {d.get("url", "")}', f'> {d.get("pages_note", "")}',
         '> هذا الملف مولَّد من `' + spec['id'] + '.json` بـ `engine/spec_summary.py` (الملف نفسه الذي يفحص به المحرّك).', '']
    F = fields(spec)
    L.append('## حقول التصنيف لكل مفردة')
    for f, fd in F.items():
        L.append(f'- `{f}` — {fd["label"]}: ' + '، '.join(f'`{k}` {v}' for k, v in fd['values'].items()) + (' (اختياري)' if fd.get('optional') else ''))
    L.append(f'- أرقام المحتوى: `{spec.get("digits", "ar")}`، والخط: `{spec.get("font", "readex")}`')
    L.append('')
    grades = [grade] if grade else spec.get('grades', [])
    for tid, tool in spec['tools'].items():
        L.append(f'## {tool["name"]} (`{tid}`)' + (f' — الوثيقة ص {ar(tool["page"])}' if tool.get('page') else ''))
        if tool.get('duration_text'):
            L.append(f'- الزمن: {tool["duration_text"]}')
        seen = {}
        for g in grades:
            cfg = tool_cfg(spec, tid, g)
            if cfg.get('_no_band'):
                continue
            vs = None
            raw_band = (tool.get('bands') or {})
            from exam_lib import grade_band
            b = grade_band(g, raw_band) if raw_band else None
            src = dict(tool); src.update(raw_band.get(b, {}) if b else {})
            vs = list((src.get('variants') or {}).keys()) or [None]
            for v in vs:
                lines = band_lines(spec, tid, tool, g, v)
                key = json.dumps(lines, ensure_ascii=False)
                seen.setdefault(key, []).append((g, v))
        for key, gs in seen.items():
            glist = sorted({g for g, _ in gs}); vlist = sorted({v for _, v in gs if v})
            head = f'### الصف {ar(glist[0])}' if len(glist) == 1 else f'### الصفوف {ar(glist[0])}–{ar(glist[-1])}'
            if vlist:
                head += ' — ' + '، '.join({'1': 'الأول', '2': 'الثاني'}.get(v, v) for v in vlist)
            L.append(head)
            L += json.loads(key)
        if tool.get('answer_key'):
            L.append('- أعمدة دليل التصحيح: ' + '، '.join(h for h, _ in tool['answer_key']))
        if tool.get('rules'):
            L.append('- **قواعد الوثيقة:**')
            L += [f'  - {r}' for r in tool['rules']]
        L.append('')
    if spec.get('marking'):
        L.append('## ضوابط التصحيح')
        for k, rows in spec['marking'].items():
            L.append(f'### {"النص القرآني" if k == "quran" else "الحديث الشريف" if k == "hadith" else k}')
            L.append('| البند | الضابط | مقدار الخصم |'); L.append('|---|---|---|')
            L += [f'| {a} | {b or "—"} | {c} |' for a, b, c in rows]
        L.append('')
    return '\n'.join(L)


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('spec', nargs='?'); ap.add_argument('--grade', type=int)
    ap.add_argument('--all', action='store_true'); ap.add_argument('--md')
    a = ap.parse_args()
    ids = [f[:-5] for f in sorted(os.listdir(os.path.join(SKILL, 'specs'))) if f.endswith('.json')] if a.all else [a.spec]
    for sid in ids:
        txt = summary(load_spec(SKILL, sid), a.grade)
        if a.md:
            p = os.path.join(a.md, f'{sid}.summary.md'); open(p, 'w', encoding='utf-8').write(txt + '\n'); print(p)
        else:
            print(txt)
