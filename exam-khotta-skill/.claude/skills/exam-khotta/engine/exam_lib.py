# مكتبة «Exam-khotta»: قراءة ملف الاختبار (JSON)، وصيغة الرياضيات المختصرة، والتحقّق من مواصفات وثيقة التقويم.
#
# صيغة النصوص (الكسور والأسس والجذور والكيمياء والآيات…) موثّقة في notation.py و guides/FORMAT.md.
import json, os, re
import arabic_check

AR = '٠١٢٣٤٥٦٧٨٩'
LETTERS = ['أ', 'ب', 'ج', 'د', 'هـ', 'و', 'ز', 'ح']
TYPE_NAMES = {'mcq': 'اختيار من متعدد', 'long': 'إجابة طويلة', 'short': 'إجابة قصيرة', 'fill': 'إكمال الفراغ',
              'tf': 'الصواب والخطأ مع التفسير', 'order': 'الترتيب والسلسلة', 'match': 'المزاوجة',
              'table': 'إكمال جدول أو شكل', 'explain': 'التفسير', 'creative': 'النوع الإبداعي'}
AO_NAMES = {'AO1': 'المعرفة', 'AO2': 'التطبيق', 'AO3': 'الاستدلال'}
LV_NAMES = {'L': 'منخفض', 'M': 'متوسط', 'H': 'مرتفع'}


from notation import ar, parse, plain, lint   # الصيغة المختصرة كلها في notation.py


def to_int(x):
    return int(str(x).translate(str.maketrans(AR, '0123456789')))


def marks_word(n):
    n = int(n)
    if n == 1:
        return 'درجة واحدة'
    if n == 2:
        return 'درجتان'
    if 3 <= n <= 10:
        return f'{ar(n)} درجات'
    return f'{ar(n)} درجة'


# ── الملفات ──
def load_json(p):
    with open(p, encoding='utf-8') as f:
        return json.load(f)


def find_config(start):
    p = os.environ.get('EXAM_KHOTTA_CONFIG')
    if p and os.path.exists(p):
        return {**load_json(p), '_dir': os.path.dirname(os.path.abspath(p))}
    d = os.path.abspath(start)
    while True:
        c = os.path.join(d, 'exam-khotta.config.json')
        if os.path.exists(c):
            return {**load_json(c), '_dir': d}   # _dir: لمسارات نسبية في الإعداد (مثل الشعار)
        if os.path.dirname(d) == d:
            return {}
        d = os.path.dirname(d)


def load_spec(skill_dir, spec_id):
    return load_json(os.path.join(skill_dir, 'specs', spec_id + '.json'))


def grade_band(grade, keys):
    for k in keys:
        a, _, b = k.partition('-')
        if int(a) <= int(grade) <= int(b or a):
            return k
    return None


def is_other(t):
    return t not in ('mcq', 'long')


# ── التحقّق ──
def item_texts(it):
    for k in ('stem', 'answer', 'guidance', 'objective', 'body', 'title'):
        if isinstance(it.get(k), str):
            yield it[k]
    for k in ('choices', 'steps', 'left', 'right', 'items'):
        for x in it.get(k, []) or []:
            yield str(x)
    for v in it.get('verses', []) or []:
        for x in v:
            yield str(x)
    for prt in it.get('parts', []):
        yield prt.get('stem', '')
    for row in (it.get('grid') or {}).get('rows', []):
        for c in row:
            yield str(c)



def fields(spec):
    """حقول التصنيف في المواصفات (بالترتيب): {الحقل: {'label': …، 'values': {رمز: اسم}}}.
    الرياضيات: ao (هدف التقويم) وlevel (الصعوبة)؛ العربية: strand (الفرع) وlevel (المستوى) وqtype (موضوعي/مقالي)…"""
    if spec.get('fields'):
        return spec['fields']
    return {'ao': {'label': 'هدف التقويم', 'values': {k: v['name'] for k, v in spec.get('ao', {}).items()}},
            'level': {'label': 'مستوى الصعوبة', 'values': {k: v['name'] for k, v in spec.get('levels', {}).items()}}}


def tool_cfg(spec, kind, grade, number=None):
    """مواصفات الأداة للصف: إعدادات الأداة العامة تغلبها إعدادات نطاق الصف (bands) إن وُجدت."""
    tool = spec['tools'].get(kind)
    if not tool:
        return None
    cfg = {k: v for k, v in tool.items() if k != 'bands'}
    bands = tool.get('bands') or {}
    band = grade_band(grade, bands) if bands else None
    if bands and not band:
        return {**cfg, '_no_band': True}
    if band:
        cfg.update(bands[band]); cfg['_band'] = band
    if cfg.get('variants'):   # الأول والثاني يختلفان (مثل توزيع فروع العربية بين الاختبارين)
        vs = cfg.pop('variants')
        v = vs.get(str(number or 1)) or vs.get('1')
        cfg.update(v); cfg['_variant'] = str(number or 1)
    # توافق مع الشكل الأول (ao وlevel على مستوى الأداة، by_grade للأنواع)
    dist = dict(cfg.get('dist') or {})
    for f in ('ao', 'level'):
        if cfg.get(f) and f not in dist:
            dist[f] = cfg[f]
    cfg['dist'] = dist
    if cfg.get('by_grade') and not cfg.get('types_rule'):
        b2 = grade_band(grade, cfg['by_grade'])
        cfg['types_rule'] = cfg['by_grade'].get(b2) if b2 else None
    if isinstance(cfg.get('calculator'), dict):
        b3 = grade_band(grade, cfg['calculator'])
        cfg['calculator'] = cfg['calculator'].get(b3) if b3 else None
    if isinstance(cfg.get('grids'), dict) and cfg['grids'] and all('-' in k or k.isdigit() for k in cfg['grids']):
        b4 = grade_band(grade, cfg['grids'])
        cfg['grids'] = cfg['grids'].get(b4, {}) if b4 else {}
    return cfg


def _in(n, rng):
    if rng is None:
        return True
    if isinstance(rng, int):
        return n == rng
    return rng[0] <= n <= rng[1]


def _rng(r):
    return f'{ar(r)}' if isinstance(r, int) else f'{ar(r[0])}–{ar(r[1])}'


def validate(exam, spec, log=None, dg=None):
    """يعيد (أخطاء، تنبيهات). الأخطاء تمنع البناء؛ التنبيهات تُعرض للمعلّم."""
    E, W = [], []
    dg = dg or exam.get('digits') or spec.get('digits') or 'ar'
    kind = exam.get('kind')
    grade = int(exam.get('grade', 0))
    tool = tool_cfg(spec, kind, grade, exam.get('number'))
    if tool and tool.get('graded') is False:
        W.append(f'{tool["name"]} في هذه المادّة تكويني لا يُرصد درجةً (الوثيقة ص {tool.get("page", "")})')
    if not tool:
        return [f'الأداة «{kind}» غير موجودة في مواصفات {spec["id"]} (المتاح: {"، ".join(spec["tools"])})'], W
    if tool.get('_no_band'):
        return [f'لا مواصفات لـ{tool["name"]} للصف {grade} في {spec["id"]}'], W
    if spec.get('grades') and grade not in spec['grades']:
        E.append(f'الصف {grade} خارج نطاق المواصفات {spec["id"]}')
    page = tool.get('page', '')
    F = fields(spec)
    lessons = exam.get('lessons', [])
    if tool.get('lessons') and not _in(len(lessons), tool['lessons']):
        E.append(f'عدد الدروس {len(lessons)}، والمطلوب {_rng(tool["lessons"])} ({tool["name"]}، الوثيقة ص {page})')
    forms = exam.get('forms') or {}
    if not forms:
        return E + ['لا توجد نماذج (forms)'], W
    lesson_codes = {l['code'] if isinstance(l, dict) else l for l in lessons}
    grid_fields = tool.get('grid_fields') or (['type'] + list(F) + ['marks'])
    grids = {}
    forbid = set(tool.get('forbid_types') or [])
    forms = {f: [i for i in its if i.get('type') != 'passage'] for f, its in forms.items()}   # النص القرائي بلا درجة
    for fname, items in forms.items():
        tag = f'النموذج ({fname})'
        if tool.get('items') and not _in(len(items), tool['items']):
            E.append(f'{tag}: عدد المفردات {len(items)}، والمطلوب {_rng(tool["items"])}')
        total = 0
        sums = {f: {} for f in F}
        objectives = []
        for k, it in enumerate(items, 1):
            q = f'{tag} المفردة {k}'
            t = it.get('type')
            if t not in TYPE_NAMES:
                E.append(f'{q}: نوع غير معروف «{t}»'); continue
            if t in forbid:
                E.append(f'{q}: نوع «{TYPE_NAMES[t]}» غير مسموح في {tool["name"]} لهذه المادّة (الوثيقة ص {page})')
            m = it.get('marks')
            if not isinstance(m, int) or m < 1:
                E.append(f'{q}: الدرجة يجب أن تكون عدداً صحيحاً موجباً'); m = 0
            total += m
            for f, fd in F.items():
                v = it.get(f)
                if fd.get('optional') and v is None:
                    continue
                if v not in fd['values']:
                    E.append(f'{q}: «{fd["label"]}» ({f}) يجب أن يكون أحد: {"، ".join(fd["values"])}')
                else:
                    sums[f][v] = sums[f].get(v, 0) + m
            for fld, name in (('objective', 'الهدف التعليمي'), ('lesson', 'الدرس'), ('page', 'رقم الصفحة'), ('stem', 'نص السؤال')):
                if not str(it.get(fld, '')).strip():
                    E.append(f'{q}: ينقصه {name} ({fld})')
            if it.get('lesson') and lesson_codes and it['lesson'] not in lesson_codes:
                E.append(f'{q}: الدرس «{it["lesson"]}» ليس من دروس الاختبار')
            if it.get('answer') in (None, '') and not it.get('steps') and not (t == 'match' and it.get('pairs')):
                E.append(f'{q}: ينقصه الإجابة (answer أو steps) لدليل التصحيح')
            mg = tool.get('max_guess')
            if t == 'mcq':
                ch = it.get('choices', [])
                need = 4 if (mg is None or mg <= 0.25) else 3
                if len(ch) < need:
                    E.append(f'{q}: الاختيار من متعدد يحتاج {ar(need)} بدائل على الأقل (التخمين ≤ ٢٥٪)')
                if len({plain(c) for c in ch}) != len(ch):
                    E.append(f'{q}: بدائل مكرّرة')
                ans = it.get('answer')
                if not (isinstance(ans, int) and 0 <= ans < len(ch)):
                    E.append(f'{q}: الإجابة (answer) رقم البديل الصحيح بدءاً من ٠')
            if t == 'tf' and not it.get('explain', True) and (mg is not None and mg < 0.5):
                E.append(f'{q}: الصواب والخطأ بلا تفسير نسبة تخمينه ٥٠٪ (> ٢٥٪): اجعل explain = true')
            if t == 'match':
                L, R = it.get('left', []), it.get('right', [])
                if len(R) < max(4, len(L) + 1):
                    E.append(f'{q}: المزاوجة تحتاج بدائل أكثر من البنود بواحد على الأقل، و٤ على الأقل (التخمين ≤ ٢٥٪)')
            if t == 'order' and len(it.get('items', [])) < 3:
                E.append(f'{q}: الترتيب يحتاج ٣ عناصر على الأقل')
            objectives.append(str(it.get('objective', '')).strip())
        if tool.get('total') is not None and total != tool['total']:
            E.append(f'{tag}: مجموع الدرجات {total}، والمطلوب {tool["total"]}')
        for f, want in (tool.get('dist') or {}).items():
            if f not in F:
                continue
            for v, n in want.items():
                got = sums[f].get(v, 0)
                if got != n:
                    E.append(f'{tag}: درجات «{F[f]["values"].get(v, v)}» ({F[f]["label"]}) = {got}، والمطلوب {n}')
            extra = [v for v in sums[f] if v not in want and sums[f][v]]
            if extra:
                E.append(f'{tag}: {F[f]["label"]}: «{"، ".join(F[f]["values"].get(v, v) for v in extra)}» ليس ضمن توزيع الوثيقة لهذه الأداة')
        tr = tool.get('types_rule')
        if tr:
            mcq = [i for i in items if i.get('type') == 'mcq']; lng = [i for i in items if i.get('type') == 'long']
            oth = [i for i in items if is_other(i.get('type'))]
            if tr.get('mcq'):
                if not _in(len(mcq), tr['mcq']['count']):
                    E.append(f'{tag}: مفردات الاختيار من متعدد {len(mcq)}، والمطلوب {_rng(tr["mcq"]["count"])}')
                if tr['mcq'].get('each') and any(not _in(i.get('marks', 0), tr['mcq']['each']) for i in mcq):
                    E.append(f'{tag}: درجة مفردة الاختيار من متعدد {_rng(tr["mcq"]["each"])}')
                for f, vals in (tr['mcq'].get('covers') or {}).items():
                    if not set(vals) <= {i.get(f) for i in mcq}:
                        E.append(f'{tag}: مفردات الاختيار من متعدد تغطي: {"، ".join(F[f]["values"][v] for v in vals)}')
            elif tr.get('mcq') is None and 'mcq' in tr and mcq:
                E.append(f'{tag}: لا اختيار من متعدد في هذه الأداة')
            if tr.get('long'):
                lc = tr['long'].get('count', 1)
                if not _in(len(lng), lc):
                    E.append(f'{tag}: مفردات الإجابة الطويلة {len(lng)}، والمطلوب {_rng(lc)}')
                if tr['long'].get('marks') is not None and any(not _in(i.get('marks', 0), tr['long']['marks']) for i in lng):
                    E.append(f'{tag}: درجة الإجابة الطويلة {_rng(tr["long"]["marks"])}')
            elif 'long' in tr and lng:
                E.append(f'{tag}: الإجابة الطويلة ليست ضمن مواصفات هذا الصف: اجعلها من الأنواع الأخرى')
            if tr.get('other'):
                o = tr['other']
                if o.get('count') is not None and not _in(len(oth), o['count']):
                    E.append(f'{tag}: مفردات الأنواع الأخرى {len(oth)}، والمطلوب {_rng(o["count"])}')
                if o.get('marks') is not None and not _in(sum(i.get('marks', 0) for i in oth), o['marks']):
                    E.append(f'{tag}: درجات الأنواع الأخرى {sum(i.get("marks", 0) for i in oth)}، والمطلوب {_rng(o["marks"])}')
                if o.get('each') and any(not _in(i.get('marks', 0), o['each']) for i in oth):
                    E.append(f'{tag}: درجة كل مفردة من الأنواع الأخرى {_rng(o["each"])}')
        if tool.get('slots'):   # بنية ثابتة (مثل التربية الإسلامية: السؤال الأول نص قرآني وحديث…)
            want = sorted(tuple(sorted(sl.items())) for sl in tool['slots'])
            got = []
            for it in items:
                keys = {k for sl in tool['slots'] for k in sl}
                got.append(tuple(sorted((k, it.get(k)) for k in keys if k in it or k == 'marks')))
            if sorted(got) != want:
                E.append(f'{tag}: لا يطابق بنية {tool["name"]} في الوثيقة (ص {page}): '
                         + '؛ '.join(' '.join(str(v) for _, v in sl) for sl in want))
        if len(set(objectives)) != len(objectives):
            W.append(f'{tag}: هدف تعليمي مكرّر في أكثر من مفردة (يجوز بهدف تقويم وصعوبة مختلفين، تأكّد)')
        if kind == 'short_test' and not forbid and len({it.get('type') for it in items if is_other(it.get('type'))}) < 2 and len(items) > 3:
            W.append(f'{tag}: نوّع أنواع المفردات')
        missing = lesson_codes - {it.get('lesson') for it in items}
        if missing:
            W.append(f'{tag}: دروس بلا مفردة: {"، ".join(sorted(missing))}')
        grids[fname] = [tuple(('other' if f == 'type' and is_other(it.get('type')) else it.get(f)) for f in grid_fields) for it in items]
        if log and kind == 'short_test':
            same = lambda e: e.get('subject', exam.get('subject')) == exam.get('subject') and e.get('grade', exam.get('grade')) == exam.get('grade') and e.get('semester', exam.get('semester')) == exam.get('semester')
            quiz_obj = {o for e in log if e.get('kind') == 'quiz' and same(e) for o in e.get('objectives', [])}
            rep = [o for o in objectives if o in quiz_obj]
            if rep:
                W.append(f'{tag}: أهداف قِيست في سؤال قصير سابق (الوثيقة تمنع تكرارها): {"؛ ".join(rep)}')
    # كتابة الصيغ والتشكيل في كل النصوص
    for fname, items in forms.items():
        for k, it in enumerate(items, 1):
            for t in item_texts(it):
                e2, w2 = lint(t, dg)
                bare = re.sub(r' ?(quran|ce|ltr)\{[^{}]*\}', '', t)
                for kind_, msg in arabic_check.check(bare, punctuation=True):
                    (e2 if kind_ == 'E' else w2).append(msg)
                E += [f'النموذج ({fname}) المفردة {k}: {x}' for x in e2]
                W += [f'النموذج ({fname}) المفردة {k}: {x}' for x in w2]
    names = list(grids)
    for f2 in names[1:]:
        if sorted(grids[f2], key=str) != sorted(grids[names[0]], key=str):
            E.append(f'النموذج ({f2}) لا يطابق شبكة النموذج ({names[0]}) في: {"، ".join(grid_fields)}')
        stems = {plain(i.get('stem', '')) for i in forms[names[0]]}
        same = [k for k, i in enumerate(forms[f2], 1) if plain(i.get('stem', '')) in stems]
        if same:
            W.append(f'النموذج ({f2}): مفردات بنصّ مطابق للنموذج ({names[0]}): {"، ".join(map(str, same))}')
    return E, W


# ── نموذج دليل التصحيح (مشترك بين PDF وWord) ──
DEFAULT_KEY = [['رقم المفردة', 'n'], ['عنصر التقويم', 'ao'], ['الهدف التعليمي', 'objective'], ['رقم الصفحة', 'page'],
               ['الإجابة', 'answer'], ['الدرجة', 'marks'], ['الإرشادات', 'guidance']]
KEY_WIDTHS = {'n': 5, 'marks': 5, 'ao': 9, 'level': 9, 'strand': 9, 'qtype': 7, 'element': 10, 'page': 8, 'unit': 9,
              'objective': 19, 'answer': 29, 'guidance': 20}


def key_columns(spec, tool):
    """أعمدة جدول التصحيح كما تشترطها وثيقة المادّة: [(العنوان، الحقل)]."""
    cols = tool.get('answer_key')
    if not cols and tool.get('answer_key_columns'):   # الشكل الأول: أسماء فقط بترتيب الافتراضي
        cols = [[h, f] for h, (_, f) in zip(tool['answer_key_columns'], DEFAULT_KEY)]
    return [tuple(c) for c in (cols or DEFAULT_KEY)]


def field_value(spec, it, f, exam=None):
    F = fields(spec)
    if f in F:
        v = it.get(f)
        return F[f]['values'].get(v, v or '')
    if f == 'unit' and exam:
        for l in exam.get('lessons', []):
            if isinstance(l, dict) and l.get('code') == it.get('lesson'):
                return l.get('unit', '')
        return ''
    return it.get(f, '')


def grid_model(spec, items):
    """شبكة المفردات: (العناوين، الصفوف) — النمط ثم حقول المادّة ثم الدرجة والدرس."""
    F = fields(spec)
    heads = ['رقم المفردة', 'نمط المفردة'] + [fd['label'] for fd in F.values()] + ['الدرجة', 'الدرس']
    rows = []
    for (_, lab), it in zip(item_labels(items), items):
        r = [lab, TYPE_NAMES.get(it.get('type'), it.get('type'))]
        for f, fd in F.items():
            v = it.get(f)
            # الرموز الرسمية (AO1، L) تُعرض مع اسمها؛ والرموز الداخلية (obj، recall) يُعرض اسمها فقط
            official = v in fd['values'] and re.fullmatch(r'[A-Z]{1,3}\d?', str(v))
            r.append(f'{v} · {fd["values"][v]}' if official else fd['values'].get(v, v or '—'))
        r += [ar(it.get('marks', 0)), str(it.get('lesson', ''))]
        rows.append(r)
    return heads, rows


def summary_model(spec, tool, items):
    """ملخّص التوزيع: [(العنوان، الحاصل، المطلوب أو None)] لكل قيمة في حقول المادّة، ثم عدد المفردات والمجموع."""
    F = fields(spec)
    out = []
    dist = tool.get('dist') or {}
    for f, fd in F.items():
        want = dist.get(f)
        vals = list(want) if want else [v for v in fd['values'] if any(i.get(f) == v for i in items)]
        for v in vals:
            out.append((fd['values'].get(v, v), sum(i.get('marks', 0) for i in items if i.get(f) == v), want.get(v) if want else None))
    out.append(('المفردات', len(items), None))
    out.append(('المجموع', sum(i.get('marks', 0) for i in items), tool.get('total')))
    return out


GROUP_NO = {'الأول': 1, 'الثاني': 2, 'الثالث': 3, 'الرابع': 4, 'الخامس': 5, 'السادس': 6}


def item_labels(items):
    """تسميات المفردات (بلا النصوص): بلا مجموعات ← ١، ٢، ٣…؛ وبمجموعات «السؤال الأول» ← أ، ب، ج… داخل كل سؤال.
    يعيد قائمة (تسمية الورقة، تسمية الدليل)."""
    out, gi, k, prev = [], 0, 0, object()
    groups = []
    for it in items:
        if it.get('type') == 'passage':
            continue
        g = it.get('group')
        if g is None:
            k += 1; lab = it.get('label') or ar(k); out.append((lab, lab)); continue
        if g != prev:
            prev = g; gi = GROUP_NO.get(g, gi + 1); k = 0
        lab = it.get('label') or LETTERS[k]   # تسمية صريحة مثل «ب-١» كما في بنية الوثيقة
        out.append((lab, f'{ar(gi)} ({lab})')); k += 1
    return out
