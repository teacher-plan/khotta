# مكتبة «Exam-khotta»: قراءة ملف الاختبار (JSON)، وصيغة الرياضيات المختصرة، والتحقّق من مواصفات وثيقة التقويم.
#
# صيغة النصوص في ملف الاختبار (تعمل في الورقة ودليل التصحيح، في PDF وWord):
#   {٣/٤}  كسر          {١ ٢/٣}  عدد كسري          س^{٢}  أُسّ          √{١٦}  جذر
#   ___    فراغ للإجابة  □  مربّع فارغ             **نص**  غامق          سطر جديد: \n
#   الأرقام اللاتينية تُحوَّل إلى عربية (٠–٩)، والفاصلة العشرية بين رقمين («.» أو «،») إلى «٫» (U+066B، تبقي العدد متّصلاً من اليسار لليمين)، و« - » إلى «−» و« * » إلى «×».
import json, os, re

AR = '٠١٢٣٤٥٦٧٨٩'
LETTERS = ['أ', 'ب', 'ج', 'د', 'هـ', 'و', 'ز', 'ح']
TYPE_NAMES = {'mcq': 'اختيار من متعدد', 'long': 'إجابة طويلة', 'short': 'إجابة قصيرة', 'fill': 'إكمال الفراغ',
              'tf': 'الصواب والخطأ مع التفسير', 'order': 'الترتيب والسلسلة', 'match': 'المزاوجة',
              'table': 'إكمال جدول أو شكل', 'explain': 'التفسير', 'creative': 'النوع الإبداعي'}
AO_NAMES = {'AO1': 'المعرفة', 'AO2': 'التطبيق', 'AO3': 'الاستدلال'}
LV_NAMES = {'L': 'منخفض', 'M': 'متوسط', 'H': 'مرتفع'}


def ar(s, digits='ar'):
    s = str(s)
    if digits != 'ar':
        return s
    # رموز لاتينية فيها أرقام (7Ni1، AO2، 7:30 لا) تبقى كما هي
    parts = re.split(r'([A-Za-z][A-Za-z0-9]*|\d+[A-Za-z][A-Za-z0-9]*)', s)
    for i in range(0, len(parts), 2):
        parts[i] = re.sub(r'(?<=\d)[.،,](?=\d)', '٫', parts[i]).translate(str.maketrans('0123456789', AR))
    return ''.join(parts)


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


# ── صيغة الرياضيات ──
TOK = re.compile(r'\{(?:([0-9٠-٩]+)\s+)?([^{}/]+)/([^{}]+)\}|\^\{([^{}]+)\}|√\{([^{}]+)\}|\*\*(.+?)\*\*|(_{3,})|(\n)')


def parse(text, digits='ar'):
    """يحوّل نصاً بالصيغة المختصرة إلى قائمة أجزاء: ('t', نص) ('f', عدد_صحيح، بسط، مقام) ('sup', نص)
    ('sqrt', نص) ('b', نص) ('blank',) ('br',)."""
    text = str(text if text is not None else '')
    text = re.sub(r'(?<=\S) - (?=\S)', ' − ', text).replace(' * ', ' × ')
    out, i = [], 0
    for m in TOK.finditer(text):
        if m.start() > i:
            out.append(('t', ar(text[i:m.start()], digits)))
        if m.group(3) is not None:
            out.append(('f', ar(m.group(1), digits) if m.group(1) else '', ar(m.group(2).strip(), digits), ar(m.group(3).strip(), digits)))
        elif m.group(4):
            out.append(('sup', ar(m.group(4), digits)))
        elif m.group(5):
            out.append(('sqrt', ar(m.group(5), digits)))
        elif m.group(6):
            out.append(('b', ar(m.group(6), digits)))
        elif m.group(7):
            out.append(('blank',))
        else:
            out.append(('br',))
        i = m.end()
    if i < len(text):
        out.append(('t', ar(text[i:], digits)))
    return out


def plain(text, digits='ar'):
    """نصّ بلا تنسيق (للفحص والطول)."""
    r = []
    for p in parse(text, digits):
        if p[0] == 't' or p[0] in ('b', 'sup', 'sqrt'):
            r.append(p[1])
        elif p[0] == 'f':
            r.append(f'{p[1]} {p[2]}/{p[3]}'.strip())
    return ''.join(r)


# ── الملفات ──
def load_json(p):
    with open(p, encoding='utf-8') as f:
        return json.load(f)


def find_config(start):
    p = os.environ.get('EXAM_KHOTTA_CONFIG')
    if p and os.path.exists(p):
        return load_json(p)
    d = os.path.abspath(start)
    while True:
        c = os.path.join(d, 'exam-khotta.config.json')
        if os.path.exists(c):
            return load_json(c)
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
def validate(exam, spec, log=None):
    """يعيد (أخطاء، تنبيهات). الأخطاء تمنع البناء؛ التنبيهات تُعرض للمعلّم."""
    E, W = [], []
    kind = exam.get('kind')
    tool = spec['tools'].get(kind)
    if not tool:
        return [f'نوع الأداة «{kind}» غير موجود في المواصفات (المتاح: {", ".join(spec["tools"])})'], W
    grade = int(exam.get('grade', 0))
    if spec.get('grades') and grade not in spec['grades']:
        E.append(f'الصف {grade} خارج نطاق المواصفات {spec["id"]}')
    lessons = exam.get('lessons', [])
    lo, hi = tool['lessons']
    if not (lo <= len(lessons) <= hi):
        E.append(f'عدد الدروس {len(lessons)}، والمطلوب {lo}–{hi} ({tool["name"]}، الوثيقة ص {tool["page"]})')
    forms = exam.get('forms') or {}
    if not forms:
        return E + ['لا توجد نماذج (forms)'], W
    lesson_codes = {l['code'] if isinstance(l, dict) else l for l in lessons}
    grids = {}
    for fname, items in forms.items():
        tag = f'النموذج ({fname})'
        n = len(items)
        a, b = tool['items']
        if not (a <= n <= b):
            E.append(f'{tag}: عدد المفردات {n}، والمطلوب {a}–{b}')
        total = 0
        ao = {'AO1': 0, 'AO2': 0, 'AO3': 0}; lv = {'L': 0, 'M': 0, 'H': 0}
        mcq = [it for it in items if it.get('type') == 'mcq']; lng = [it for it in items if it.get('type') == 'long']
        others = [it for it in items if is_other(it.get('type'))]
        objectives = []
        for k, it in enumerate(items, 1):
            q = f'{tag} المفردة {k}'
            t = it.get('type')
            if t not in TYPE_NAMES:
                E.append(f'{q}: نوع غير معروف «{t}»'); continue
            m = it.get('marks')
            if not isinstance(m, int) or m < 1:
                E.append(f'{q}: الدرجة يجب أن تكون عدداً صحيحاً موجباً (لا أنصاف)')
                m = 0
            total += m
            if it.get('ao') not in ao:
                E.append(f'{q}: هدف التقويم يجب أن يكون AO1 أو AO2 أو AO3')
            else:
                ao[it['ao']] += m
            if it.get('level') not in lv:
                E.append(f'{q}: الصعوبة يجب أن تكون L أو M أو H')
            else:
                lv[it['level']] += m
            for fld, name in (('objective', 'الهدف التعليمي'), ('lesson', 'الدرس'), ('page', 'رقم الصفحة'), ('stem', 'نص السؤال')):
                if not str(it.get(fld, '')).strip():
                    E.append(f'{q}: ينقصه {name} ({fld})')
            if it.get('lesson') and lesson_codes and it['lesson'] not in lesson_codes:
                E.append(f'{q}: الدرس «{it["lesson"]}» ليس من دروس الاختبار')
            if it.get('answer') in (None, '') and not it.get('steps') and not (t == 'match' and it.get('pairs')):
                E.append(f'{q}: ينقصه الإجابة (answer أو steps) لدليل التصحيح')
            if t == 'mcq':
                ch = it.get('choices', [])
                if len(ch) < 4:
                    E.append(f'{q}: الاختيار من متعدد يحتاج ٤ بدائل على الأقل (التخمين ≤ ٢٥٪)')
                if len({plain(c) for c in ch}) != len(ch):
                    E.append(f'{q}: بدائل مكرّرة')
                ans = it.get('answer')
                if not (isinstance(ans, int) and 0 <= ans < len(ch)):
                    E.append(f'{q}: الإجابة (answer) رقم البديل الصحيح بدءاً من ٠')
                if m != 1 and kind == 'short_test':
                    E.append(f'{q}: مفردة الاختيار من متعدد درجتها ١')
            if t == 'tf' and not it.get('explain', True):
                if tool.get('max_guess') and tool['max_guess'] < 0.5:
                    E.append(f'{q}: الصواب والخطأ بلا تفسير نسبة تخمينه ٥٠٪ (> ٢٥٪): اجعل explain = true')
            if t == 'match':
                L, R = it.get('left', []), it.get('right', [])
                if len(R) < max(4, len(L) + 1):
                    E.append(f'{q}: المزاوجة تحتاج بدائل أكثر من البنود بواحد على الأقل، و٤ على الأقل (التخمين ≤ ٢٥٪)')
            if t == 'order' and len(it.get('items', [])) < 3:
                E.append(f'{q}: الترتيب يحتاج ٣ عناصر على الأقل')
            if kind == 'short_test' and is_other(t) and m > 2:
                E.append(f'{q}: مفردات الأنواع الأخرى درجتها ١–٢')
            objectives.append(str(it.get('objective', '')).strip())
        if total != tool['total']:
            E.append(f'{tag}: مجموع الدرجات {total}، والمطلوب {tool["total"]}')
        if tool.get('ao'):
            for k2, v in tool['ao'].items():
                if ao[k2] != v:
                    E.append(f'{tag}: درجات {AO_NAMES[k2]} ({k2}) = {ao[k2]}، والمطلوب {v}')
        if tool.get('level'):
            for k2, v in tool['level'].items():
                if lv[k2] != v:
                    E.append(f'{tag}: درجات الصعوبة {LV_NAMES[k2]} ({k2}) = {lv[k2]}، والمطلوب {v}')
        if tool.get('by_grade'):
            band = grade_band(grade, tool['by_grade'])
            g = tool['by_grade'].get(band) if band else None
            if g:
                if len(mcq) != g['mcq']['count']:
                    E.append(f'{tag}: مفردات الاختيار من متعدد {len(mcq)}، والمطلوب {g["mcq"]["count"]} (الصفوف {band})')
                if g.get('long'):
                    if len(lng) != g['long']['count'] or sum(i.get('marks', 0) for i in lng) != g['long']['marks']:
                        E.append(f'{tag}: يلزم {g["long"]["count"]} مفردة إجابة طويلة بـ {g["long"]["marks"]} درجات (الصفوف {band})')
                elif lng:
                    E.append(f'{tag}: الإجابة الطويلة ليست ضمن مواصفات الصفوف {band}: اجعلها من الأنواع الأخرى')
                oa, ob = g['other']['count']
                if not (oa <= len(others) <= ob):
                    E.append(f'{tag}: مفردات الأنواع الأخرى {len(others)}، والمطلوب {oa}–{ob}')
                if sum(i.get('marks', 0) for i in others) != g['other']['marks']:
                    E.append(f'{tag}: درجات الأنواع الأخرى {sum(i.get("marks", 0) for i in others)}، والمطلوب {g["other"]["marks"]}')
        if len(set(objectives)) != len(objectives):
            W.append(f'{tag}: هدف تعليمي مكرّر في أكثر من مفردة (يجوز بهدف تقويم وصعوبة مختلفين، تأكّد)')
        types = {it.get('type') for it in others}
        if kind == 'short_test' and len(types) < 2:
            W.append(f'{tag}: نوّع أنواع المفردات الأخرى (الوثيقة: «تُطبَّق أنواع مختلفة من المفردات»)')
        covered = {it.get('lesson') for it in items}
        missing = lesson_codes - covered
        if missing:
            W.append(f'{tag}: دروس بلا مفردة: {"، ".join(sorted(missing))}')
        grids[fname] = [(it.get('type') if not is_other(it.get('type')) else 'other', it.get('ao'), it.get('level'), it.get('marks')) for it in items]
        if log and kind == 'short_test':
            quiz_obj = {o for e in log if e.get('kind') == 'quiz' for o in e.get('objectives', [])}
            rep = [o for o in objectives if o in quiz_obj]
            if rep:
                W.append(f'{tag}: أهداف قِيست في سؤال قصير سابق (الوثيقة تمنع تكرارها): {"؛ ".join(rep)}')
    names = list(grids)
    for f2 in names[1:]:
        if sorted(grids[f2], key=str) != sorted(grids[names[0]], key=str):
            E.append(f'النموذج ({f2}) لا يطابق شبكة النموذج ({names[0]}) في الأنماط والأهداف والصعوبة والدرجات')
        stems = {plain(i.get('stem', '')) for i in forms[names[0]]}
        same = [k for k, i in enumerate(forms[f2], 1) if plain(i.get('stem', '')) in stems]
        if same:
            W.append(f'النموذج ({f2}): مفردات بنصّ مطابق للنموذج ({names[0]}): {"، ".join(map(str, same))}')
    return E, W
