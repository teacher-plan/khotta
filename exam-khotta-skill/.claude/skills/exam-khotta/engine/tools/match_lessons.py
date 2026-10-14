#!/usr/bin/env python3
# مطابقة الدروس بين كتاب الطالب ودليل المعلم وكتاب النشاط، وبناء مسوّدة الفهرس آلياً — guides/INDEXING.md
#
#   python3 match_lessons.py --dir books/math-7-1 --out indexes/math-7-1.draft.json
#   python3 match_lessons.py --dir books/math-7-1 --compare <S>/indexes/math-7-1.json     ← يقارن بفهرس جاهز
#   python3 match_lessons.py --dir books/math-7-1 --sheets                                  ← لوحات مصغّرة فقط
#
# يقرأ student.pdf و guide.pdf و activity.pdf (ما وُجد منها) ويستخرج لكل صفحة:
#   • رقمها المطبوع (من تذييل InDesign «indd 15» أو رقم الصفحة في أسفلها/أعلاها) ← الفرق offset لكل كتاب؛
#   • رمز الدرس وعنوانه في رأسها (١-٧ …) ← صفحات كل درس؛
#   • في الدليل: رأس قسم الدرس («… (حصتان) ص ١٥٢-١٥٣ في كتاب الطالب») ← عدد الحصص وصفحات الكتاب للتحقّق المتبادل،
#     وصفحات «إجابات تمارين كتاب الطالب/النشاط».
# ويكتب: مسوّدة فهرس بالأرقام المطبوعة، و offsets.json، و match_report.md، ولوحات مصغّرة في <dir>/_check/
# (كل صورة مرقّمة بـ «PDF n · ط m») ليتحقّق منها الوكيل بعينه. ما لم يتأكّد منه يُعلَّم في التقرير ‹؟›.
# ⚠ النص المستخرج من كتب الوزارة قد يكون معكوس الأرقام أو مفكوك الحروف؛ لذلك يُطبَّع، وتُحسم الحالات المشكوكة بالنظر.
import argparse, os, re, sys, json, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import open_pdf, norm_ar, to_ar, save_json, log

KINDS = {'student': 'كتاب الطالب', 'guide': 'دليل المعلم', 'activity': 'كتاب النشاط'}
CODE = re.compile(r'(?<!\d)(\d{1,2})\s*[-–]\s*(\d{1,2})(?!\d)')
EXCLUDE = ['تمارين ومسايل عامه', 'تمارين ومسائل عامه', 'مراجعه الوحده', 'نهايه الوحده', 'ورقه المصادر']
ORD = {'الاولي': 1, 'الثانيه': 2, 'الثالثه': 3, 'الرابعه': 4, 'الخامسه': 5, 'السادسه': 6, 'السابعه': 7, 'الثامنه': 8,
       'التاسعه': 9, 'العاشره': 10}
_O = '|'.join(ORD)
UNIT = re.compile(r'الوحده (' + _O + r')|(' + _O + r') ?:? ?الوحده')   # بعض الملفات تقلب ترتيب الكلمات


def unit_no(top):
    m = UNIT.search(top)
    return ORD[m.group(1) or m.group(2)] if m else None


def summary_page(p):   # صفحة «ملخّص: يجب أن تعرف» في آخر الوحدة تحمل رأس آخر درس
    return p['body'][:40].lstrip(' :').startswith('ملخص')


def page_parts(page):
    """نصوص الرأس والتذييل والمتن (مطبّعة) وأرقام الصفحة المرشّحة."""
    H = page.rect.height
    top, bottom, body, nums = [], [], [], []
    for b in page.get_text('blocks'):
        x0, y0, x1, y1, t = b[0], b[1], b[2], b[3], b[4]
        n = norm_ar(t)
        if not n:
            continue
        if y1 < H * 0.13:
            top.append(n)
        elif y0 > H * 0.88:
            bottom.append(n)
        else:
            body.append(n)
        if (y1 < H * 0.09 or y0 > H * 0.90) and re.fullmatch(r'\d{1,3}', n.replace(' ', '')):
            nums.append(int(n.replace(' ', '')))
    raw = page.get_text()
    m = re.search(r'ind[bd]\s+(\d{1,3})\b', raw)
    slug = int(m.group(1)) if m else None
    return ' | '.join(top), ' | '.join(bottom), ' '.join(body), nums, slug


def scan(path):
    d = open_pdf(path)
    pages = []
    for i in range(d.page_count):
        top, bottom, body, nums, slug = page_parts(d[i])
        pages.append({'pdf': i + 1, 'top': top, 'bottom': bottom, 'body': body[:3000], 'nums': nums, 'slug': slug})
    return d, pages


def offsets(pages):
    """الفرق offset = رقم PDF − الرقم المطبوع، بالأغلبية، مع نطاقات إن تغيّر."""
    votes = []
    for p in pages:
        cands = ([p['slug']] if p['slug'] else []) + p['nums']
        for c in cands:
            if 0 < c <= len(pages) + 20:
                votes.append((p['pdf'], p['pdf'] - c))
    if not votes:
        return None, [], 0
    cnt = collections.Counter(o for _, o in votes)
    main, k = cnt.most_common(1)[0]
    # نطاقات: تتبّع تغيّر الفرق الأغلب في نوافذ من ١٥ صفحة
    ranges, cur, start = [], None, 1
    for w in range(1, len(pages) + 1, 15):
        c = collections.Counter(o for pg, o in votes if w <= pg < w + 15)
        o, n = c.most_common(1)[0] if c else (cur, 0)
        if n < 3 or n < 0.6 * sum(c.values()):   # نافذة ضعيفة الدلالة (أرقام داخل التمارين): لا تغيّر الفرق
            o = cur if cur is not None else main
        if o != cur:
            if cur is not None:
                ranges.append({'from_pdf': start, 'to_pdf': w - 1, 'offset': cur})
            cur, start = o, w
    ranges.append({'from_pdf': start, 'to_pdf': len(pages), 'offset': cur})
    conf = round(k / max(1, len(votes)), 2)
    return main, (ranges if len(ranges) > 1 else []), conf


def printed(pdf_no, main, ranges):
    for r in ranges:
        if r['from_pdf'] <= pdf_no <= r['to_pdf']:
            return pdf_no - r['offset']
    return pdf_no - (main or 0)


def codes_in(text):
    return [(int(a), int(b)) for a, b in CODE.findall(text)]


def orient(all_pairs, ref=None):
    """الاستخراج قد يقلب «٧-١» إلى «1-7». إن وُجدت رموز كتاب الطالب (ref) نختار الاتجاه الأكثر تطابقاً معها،
    وإلا فالاتجاه الذي تتزايد فيه أرقام الوحدات عبر الصفحات (رقم الدرس يعود إلى ١ مع كل وحدة)."""
    if not all_pairs:
        return lambda a, b: (a, b)
    keep_f, swap_f = (lambda a, b: (a, b)), (lambda a, b: (b, a))
    if ref:
        k = sum(1 for x in set(all_pairs) if x in ref); w = sum(1 for x in set(all_pairs) if x[::-1] in ref)
        if k != w:
            return keep_f if k > w else swap_f
    seq = [x for i, x in enumerate(all_pairs) if i == 0 or x != all_pairs[i - 1]]
    mono1 = sum(1 for x, y in zip(seq, seq[1:]) if y[0] >= x[0])
    mono2 = sum(1 for x, y in zip(seq, seq[1:]) if y[1] >= x[1])
    u1 = len({a for a, _ in seq}); u2 = len({b for _, b in seq})
    return keep_f if (-mono1, u1) <= (-mono2, u2) else swap_f


def code_str(u, l):
    return f'{to_ar(u)}-{to_ar(l)}'


def student_lessons(pages, main, ranges):
    pairs = [c for p in pages for c in codes_in(p['top'])[:1]]
    o = orient(pairs)
    les = collections.OrderedDict(); notes = []
    for p in pages:
        if any(w in p['top'] + ' ' + p['body'][:300] for w in EXCLUDE) or summary_page(p) or UNIT.search(p['top']):
            continue   # صفحات المراجعة والملخّص وافتتاح الوحدة ليست من الدرس
        cs = codes_in(p['top'])
        if not cs:
            continue
        u, l = o(*cs[0])
        if les and (l, u) == next(reversed(les)):   # صفحة بخطٍّ تالف قلبت الرمز: تتبع الدرس السابق
            u, l = l, u
        title = re.sub(CODE, '', p['top'].split('|')[0]).strip(' -–|')[:60]
        e = les.setdefault((u, l), {'code': code_str(u, l), 'title': title, 'book_pages': [], 'book_pdf_pages': []})
        e['book_pages'].append(printed(p['pdf'], main, ranges)); e['book_pdf_pages'].append(p['pdf'])
    return les, notes


# رأس قسم الدرس في الدليل: «X-Y عنوان (حصتان) ص N-M في كتاب الطالب … نقاط التعلم الرئيسية».
# ترتيب أجزائه في النص المستخرج مضطرب، فنلتقط كل جزءٍ بنمطٍ مستقل.
G_CODE = re.compile(r'(?<!\d)(\d{1,2})\s*[-–]\s*(\d{1,2})\s*نقاط التعلم')
G_BOOK = re.compile(r'كتاب الطالب\s*(\d{1,3})(?:\s*[-–]\s*(\d{1,3}))?')
G_SESS = re.compile(r'حصه واحده|حصتان|\(\s*(\d)\s*حصص|حصص\s*\)\s*ص?\s*(\d)\s*\(')


def guide_head(txt):
    if 'نقاط التعلم' not in txt or 'كتاب الطالب' not in txt:
        return None
    c = G_CODE.search(txt); bk = G_BOOK.search(txt); se = G_SESS.search(txt)
    if not c:
        return None
    sessions = None
    if se:
        g = se.group(0)
        sessions = 1 if 'واحده' in g else 2 if 'حصتان' in g else int(se.group(1) or se.group(2))
    pages = sorted({int(x) for x in bk.groups() if x}) if bk else []
    title = txt[max(0, c.start() - 70):c.start()].split('ص')[-1].strip(' ()0123456789-–')[-60:]
    return (int(c.group(1)), int(c.group(2))), sessions, pages, title


def guide_sections(pages, main, ranges, ref=None):
    """أقسام الدروس في الدليل وصفحات الإجابات."""
    heads = []
    for p in pages:
        h = guide_head(p['top'] + ' ' + p['body'][:700])
        if h and not any(h[0] == x[1][0] for x in heads):
            heads.append((p['pdf'], h))
    o = orient([h[0] for _, h in heads], ref)
    sec = collections.OrderedDict()
    for k, (pdf, (code, sessions, bp, title)) in enumerate(heads):
        u, l = o(*code)
        end = heads[k + 1][0] - 1 if k + 1 < len(heads) else pdf
        sec[(u, l)] = {'guide_pdf_start': pdf, 'guide_pdf_end': end, 'sessions': sessions,
                       'book_pages_from_guide': bp, 'title_guide': title}
    answers = {'student': [], 'activity': []}
    for p in pages:
        t = p['top'] + ' ' + p['body'][:400]
        if 'اجابات تمارين كتاب الطالب' in t:
            answers['student'].append(p['pdf'])
        if 'اجابات تمارين كتاب النشاط' in t:
            answers['activity'].append(p['pdf'])
    # آخر قسمٍ في كل وحدة ينتهي قبل صفحات الإجابات
    ans_all = sorted(answers['student'] + answers['activity'])
    for v in sec.values():
        later = [a for a in ans_all if a > v['guide_pdf_start']]
        if later and later[0] <= v['guide_pdf_end']:
            v['guide_pdf_end'] = later[0] - 1
        v['guide_pages'] = [printed(x, main, ranges) for x in range(v['guide_pdf_start'], v['guide_pdf_end'] + 1)]
    return sec, answers


def activity_lessons(pages, main, ranges, ref=None):
    pairs = []
    for p in pages:
        t = p['top'] + ' ' + p['body'][:200]
        if 'تمارين' in t:
            pairs += codes_in(t)[:1]
    o = orient(pairs, ref)
    les = collections.OrderedDict(); cur = None
    for p in pages:
        t = p['top'] + ' ' + p['body'][:200]
        cs = codes_in(t) if 'تمارين' in t else []
        if ref:   # أرقامٌ داخل التمارين مثل «8-16» ليست رموز دروس
            cs = [c for c in cs if o(*c) in ref]
        if p['body'].count('.....') >= 3:   # صفحة المحتويات (نقاط الدليل)
            continue
        un = unit_no(p['top'])
        if cs:
            cur = o(*cs[0])
        elif un and (not cur or un != cur[0]):   # بداية وحدة جديدة رأسها صورة: أول دروسها
            cur = (un, 1) if not ref or (un, 1) in ref else None
        elif any(w in t for w in ['ورقه المصادر', 'اوراق المصادر', 'اجابات تمارين', 'ملخص :']) or not (p['top'] + p['body']).strip():
            cur = None
        if cur:
            e = les.setdefault(cur, {'activity_printed_pages': [], 'activity_pdf_pages': []})
            e['activity_printed_pages'].append(printed(p['pdf'], main, ranges)); e['activity_pdf_pages'].append(p['pdf'])
    return les


def contact_sheets(doc, kind, out, main, ranges, per=24, cols=6):
    from PIL import Image, ImageDraw
    os.makedirs(out, exist_ok=True)
    W, Hh = 220, 300; files = []
    for s in range(0, doc.page_count, per):
        n = min(per, doc.page_count - s); rows = (n + cols - 1) // cols
        sheet = Image.new('RGB', (cols * W, rows * (Hh + 26)), 'white'); dr = ImageDraw.Draw(sheet)
        for k in range(n):
            i = s + k
            pix = doc[i].get_pixmap(dpi=28)
            im = Image.frombytes('RGB', (pix.width, pix.height), pix.samples); im.thumbnail((W - 8, Hh))
            x, y = (k % cols) * W, (k // cols) * (Hh + 26)
            sheet.paste(im, (x + 4, y + 22))
            dr.text((x + 6, y + 4), f'PDF {i + 1}  |  p{printed(i + 1, main, ranges)}', fill=(200, 30, 30))
        f = os.path.join(out, f'{kind}_sheet_{s // per + 1:02d}.jpg'); sheet.save(f, quality=72); files.append(f)
    return files


def main():
    ap = argparse.ArgumentParser(description='مطابقة دروس الكتب الثلاثة وبناء مسوّدة الفهرس')
    ap.add_argument('--dir', required=True); ap.add_argument('--out')
    ap.add_argument('--compare'); ap.add_argument('--sheets', action='store_true'); ap.add_argument('--no-sheets', action='store_true')
    a = ap.parse_args()
    docs, info = {}, {}
    for k in KINDS:
        f = os.path.join(a.dir, f'{k}.pdf')
        if os.path.exists(f):
            d, pages = scan(f); m, r, c = offsets(pages)
            docs[k] = (d, pages); info[k] = {'offset': m, 'offset_ranges': r, 'offset_confidence': c, 'pages': d.page_count}
            log(f'{KINDS[k]}: {d.page_count} صفحة، الفرق {m} (ثقة {c}){" ونطاقات " + str(r) if r else ""}')
    if not docs:
        sys.exit('لا يوجد student.pdf ولا guide.pdf ولا activity.pdf في ' + a.dir)
    chk = os.path.join(a.dir, '_check')
    if not a.no_sheets:
        for k, (d, _) in docs.items():
            fs = contact_sheets(d, k, chk, info[k]['offset'], info[k]['offset_ranges'])
            log(f'لوحات {KINDS[k]}: {len(fs)} في {chk}')
    if a.sheets:
        return
    save_json({k: v['offset'] for k, v in info.items()} | {'_ranges': {k: v['offset_ranges'] for k, v in info.items() if v['offset_ranges']}},
              os.path.join(a.dir, 'offsets.json'))

    st = student_lessons(docs['student'][1], info['student']['offset'], info['student']['offset_ranges'])[0] if 'student' in docs else {}
    gd, ans = guide_sections(docs['guide'][1], info['guide']['offset'], info['guide']['offset_ranges'], set(st)) if 'guide' in docs else ({}, {})
    ac = activity_lessons(docs['activity'][1], info['activity']['offset'], info['activity']['offset_ranges'], set(st)) if 'activity' in docs else {}

    keys = sorted(set(st) | set(gd) | set(ac))
    lessons, report = [], ['# تقرير المطابقة', '', '| الدرس | كتاب الطالب | الدليل (الحصص) | النشاط | ملاحظات |', '|---|---|---|---|---|']
    for key in keys:
        e = {'code': code_str(*key)}
        s, g, t = st.get(key, {}), gd.get(key, {}), ac.get(key, {})
        e['title'] = s.get('title') or g.get('title_guide', '')
        if s: e['book_pages'] = s['book_pages']
        if g: e['guide_pages'] = g['guide_pages']; e['sessions'] = g['sessions']
        if t: e.update(t)
        flags = []
        if s and g and g.get('book_pages_from_guide') and not set(g['book_pages_from_guide']) & set(s['book_pages']):
            flags.append(f'؟ الدليل يقول ص {g["book_pages_from_guide"]}')
        if g and s and g.get('book_pages_from_guide') and set(g['book_pages_from_guide']) - set(s['book_pages']):
            e.setdefault('note', ''); flags.append('؟ صفحات من الدليل غير مرصودة في رأس الكتاب')
        for need, have in (('كتاب الطالب', s), ('الدليل', g), ('النشاط', t)):
            if need == 'الدليل' and 'guide' not in docs or need == 'النشاط' and 'activity' not in docs or need == 'كتاب الطالب' and 'student' not in docs:
                continue
            if not have:
                flags.append(f'؟ لم يُعثر عليه في {need}')
        e['confidence'] = 'high' if not flags else 'check'
        lessons.append(e)
        rng = lambda v: f'{v[0]}–{v[-1]}' if v else '—'
        report.append(f'| {e["code"]} {e["title"][:28]} | {rng(e.get("book_pages", []))} | {rng(e.get("guide_pages", []))} ({e.get("sessions", "—")}) | {rng(e.get("activity_printed_pages", []))} | {"، ".join(flags)} |')
    idx = {'page_numbers': 'أرقام مطبوعة', 'pdf_offsets_reference': {k: v['offset'] for k, v in info.items()},
           'answers_in_guide_pdf': ans, 'lessons': lessons, '_generated_by': 'match_lessons.py — مسوّدة تُراجَع بالنظر قبل اعتمادها'}
    out = a.out or os.path.join(a.dir, 'index.draft.json')
    save_json(idx, out)
    report += ['', f'الفروق: ' + '، '.join(f'{KINDS[k]} {v["offset"]} (ثقة {v["offset_confidence"]})' for k, v in info.items()),
               f'صفحات الإجابات في الدليل (PDF): الطالب {ans.get("student")}، النشاط {ans.get("activity")}',
               '', 'راجع كل سطرٍ فيه ‹؟› بالنظر في اللوحات (_check/*_sheet_*.jpg) أو بصور الصفحات، ثم اعرض أول درس على المعلّم.']
    if a.compare:
        ref = {l['code']: l for l in json.load(open(a.compare, encoding='utf-8'))['lessons']}
        ok = bad = 0; diffs = []
        for l in lessons:
            r = ref.get(l['code'])
            if not r:
                continue
            for f in ('book_pages', 'guide_pages', 'activity_printed_pages'):
                if f in l and f in r:
                    if l[f] == r[f]: ok += 1
                    else: bad += 1; diffs.append(f'{l["code"]} {f}: آلي {l[f]} ≠ مرجع {r[f]}')
        report += ['', f'## مقارنة بـ {os.path.basename(a.compare)}: تطابق {ok}، اختلاف {bad}'] + [f'- {x}' for x in diffs[:60]]
        log(f'مقارنة: تطابق {ok}، اختلاف {bad}')
    rp = os.path.join(a.dir, 'match_report.md')
    open(rp, 'w', encoding='utf-8').write('\n'.join(report) + '\n')
    print(f'مسوّدة الفهرس: {out}\nالتقرير: {rp}\nاللوحات: {chk}')


if __name__ == '__main__':
    main()
