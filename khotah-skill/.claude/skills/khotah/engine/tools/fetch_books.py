#!/usr/bin/env python3
# تنزيل كتب المنهج العُماني آلياً مع التحقّق — guides/SOURCES.md
#
#   python3 fetch_books.py --subject math --grade 7 --semester 2 --out books/math-7-2
#   python3 fetch_books.py --subject math --grade 7 --semester 2 --list          ← يعرض ما وُجد دون تنزيل
#   python3 fetch_books.py --url <رابط PDF أو Drive أو صفحة أفدني> --as guide --out books/math-7-2
#
# كتاب الطالب وكتاب النشاط: من بوابة الوزارة (رسمية). دليل المعلم: من أفدني (غير رسمي) بعد التحقّق من الطبعة.
# الناتج: student.pdf و activity.pdf و guide.pdf في مجلد --out، و sources.json، وصورة الغلاف وصفحة البيانات
# في <out>/_check/ ليطّلع عليها الوكيل (الطبعة والعام). إن فشل مصدر انتقل للتالي، وفي النهاية يطبع ما على
# المعلّم تنزيله بنفسه (الخطة البديلة) — لا يتوقّف أبداً بخطأٍ غامض.
import argparse, os, re, sys, html, urllib.parse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import http_get, download, is_pdf, open_pdf, render, save_json, log

MOE = 'https://home.moe.gov.om'
AFEDNE = 'https://om.afedne.com'
GRADE_AR = {1: 'الأول', 2: 'الثاني', 3: 'الثالث', 4: 'الرابع', 5: 'الخامس', 6: 'السادس', 7: 'السابع', 8: 'الثامن',
            9: 'التاسع', 10: 'العاشر', 11: 'الحادي عشر', 12: 'الثاني عشر'}
GRADE_SHORT = {1: 'أول', 2: 'ثاني', 3: 'ثالث', 4: 'رابع', 5: 'خامس', 6: 'سادس', 7: 'سابع', 8: 'ثامن', 9: 'تاسع', 10: 'عاشر',
               11: 'حادي عشر', 12: 'ثاني عشر'}
SUBJECTS = {  # الرمز ← كلمات اسم المادّة في البوابة وأفدني
    'math': ['الرياضيات'], 'science': ['العلوم'], 'arabic': ['لغتي الجميلة', 'اللغة العربية'],
    'english': ['اللغة الانجليزية', 'اللغة الإنجليزية'], 'social': ['الدراسات الاجتماعية'],
    'islamic': ['ديني قيمي', 'التربية الإسلامية'], 'it': ['تقنية المعلومات'], 'life': ['المهارات الحياتية'],
    'physics': ['الفيزياء'], 'chemistry': ['الكيمياء'], 'biology': ['الأحياء'],
}
SEM_AR = {1: ['الفصل الأول', 'الفصل الاول'], 2: ['الفصل الثاني']}
SEM_SHORT = {1: ['أول', 'الأول', 'الاول'], 2: ['ثاني', 'الثاني']}
SKIP = ['الإعاقة', 'الاعاقة', 'كتيب', 'برايل']


def links(page_html):
    for m in re.finditer(r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', page_html, re.S):
        yield m.group(1), re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', m.group(2)))).strip()


def find_link(page_html, words, pattern=r'manaheg/\d+$'):
    for href, text in links(page_html):
        if re.search(pattern, href) and any(w in text for w in words):
            return urllib.parse.urljoin(MOE + '/', href)
    return None


def moe_books(subject, grade, sem):
    """يعيد {'student': url, 'activity': url} من بوابة الوزارة."""
    names = SUBJECTS.get(subject, [subject])
    home = http_get(MOE + '/ar/manaheg')
    g = None
    for href, text in links(home):
        if re.search(r'manaheg/\d+$', href) and text.replace('الصف ', '').strip() == GRADE_AR[grade]:
            g = urllib.parse.urljoin(MOE + '/', href)
    if not g:
        raise RuntimeError(f'لم أجد الصف {GRADE_AR[grade]} في البوابة')
    s = find_link(http_get(g), names)
    if not s:
        raise RuntimeError(f'لم أجد مادّة {names[0]} للصف {GRADE_AR[grade]}')
    p = find_link(http_get(s), SEM_AR[sem])
    if not p:
        raise RuntimeError(f'لم أجد {SEM_AR[sem][0]}')
    page = http_get(p)
    out = {}
    unnamed = []
    # كل كتاب: نصّ العنوان قبل رابط Book…pdf
    for m in re.finditer(r"(.{0,500}?)(/images/manaheg/file/Book\d+\.pdf)", page, re.S):
        title = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', m.group(1)))).strip()[-120:]
        url = MOE + m.group(2)
        if any(w in title for w in SKIP):
            continue
        kind = 'activity' if 'النشاط' in title else ('student' if 'الطالب' in title else None)
        if kind and kind not in out:
            out[kind] = url
            log(f'البوابة: {kind} ← {url} ({title[-50:]})')
        elif not kind:
            unnamed.append((url, title))
    if 'student' not in out and len(unnamed) >= 1:   # كتاب واحد بلا «كتاب الطالب» في عنوانه (مثل «ديني قيمي»)
        out['student'] = unnamed[0][0]
        log(f'البوابة: student ← {unnamed[0][0]} (بلا تسمية؛ تحقّق من الغلاف)')
    return out


def afedne_guide(subject, grade, sem):
    """يبحث في أفدني عن دليل المعلم ويعيد قائمة مرشّحين [(العنوان، رابط الصفحة)] مرتّبة."""
    names = SUBJECTS.get(subject, [subject])
    found = []
    for q in [f'دليل المعلم {names[0]} {GRADE_AR[grade]}', f'دليل المعلم {names[0]}']:
        for pg in (1, 2, 3):
            try:
                s = http_get(f'{AFEDNE}/library?search={urllib.parse.quote(q)}&page={pg}')
            except RuntimeError as e:
                log(e); break
            for href, text in links(s):
                if '/library/file/' in href and 'دليل' in text and (href, text) not in found:
                    found.append((text, href))
    def score(t):
        g = (GRADE_AR[grade] in t or GRADE_SHORT[grade] in t)
        sm = any(w in t for w in SEM_SHORT[sem])
        other = any(w in t for w in SEM_SHORT[3 - sem])
        subj = any(n.replace('ال', '', 1) in t for n in names)
        return (g and subj) * 4 + sm * 2 - other * 3
    found = [f for f in found if score(f[0]) >= 4]
    found.sort(key=lambda f: -score(f[0]))
    return found


def drive_id(text):
    m = re.search(r'drive\.google\.com/(?:file/d/|u/\d/uc\?id=|uc\?id=|open\?id=)([A-Za-z0-9_-]{20,})', text)
    return m.group(1) if m else None


def resolve(url):
    """يحوّل رابط صفحة أفدني أو Drive إلى رابط تنزيل مباشر."""
    u = urllib.parse.urlparse(url)
    host = (u.hostname or '').lower()
    if (host in ('afedne.com', 'www.afedne.com') and u.path.startswith('/library/file/')) or host == 'afidni.com' or host.endswith('.afidni.com'):
        did = drive_id(http_get(url))
        if not did:
            raise RuntimeError('لم أجد رابط Drive في صفحة الملف')
        url = f'https://drive.google.com/file/d/{did}/view'
    did = drive_id(url)
    if did:
        return f'https://drive.usercontent.google.com/download?id={did}&export=download&confirm=t'
    return url


def verify(path, kind, out):
    """يتحقّق أنه PDF سليم ويحفظ الغلاف وصفحة البيانات صوراً، ويعيد ملخّصاً."""
    if not is_pdf(path):
        raise RuntimeError('الملف المنزَّل ليس PDF (غالباً صفحة HTML أو تحذير Drive)')
    d = open_pdf(path)
    chk = os.path.join(out, '_check'); os.makedirs(chk, exist_ok=True)
    for i in range(min(3, d.page_count)):
        render(d[i], os.path.join(chk, f'{kind}_p{i + 1}.png'), dpi=60)
    head = ' '.join(d[i].get_text()[:400] for i in range(min(4, d.page_count)))
    ed = re.findall(r'(الطبعة[^\n]{0,40}|1[34]\d\d ?هـ|20[12]\d ?م)', head)
    return {'pages': d.page_count, 'size_mb': round(os.path.getsize(path) / 1e6, 1), 'edition_hints': ed[:4],
            'check_images': f'_check/{kind}_p1..3.png'}


def main():
    ap = argparse.ArgumentParser(description='تنزيل كتب المنهج العُماني')
    ap.add_argument('--subject', default='math'); ap.add_argument('--grade', type=int); ap.add_argument('--semester', type=int)
    ap.add_argument('--out', default='books'); ap.add_argument('--kinds', default='student,activity,guide')
    ap.add_argument('--list', action='store_true', help='اعرض ما وُجد دون تنزيل')
    ap.add_argument('--url', help='رابط مباشر (PDF أو Drive أو صفحة أفدني)'); ap.add_argument('--as', dest='as_kind', default='guide')
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    srcp = os.path.join(a.out, 'sources.json')
    sources = __import__('json').load(open(srcp, encoding='utf-8')) if os.path.exists(srcp) else {}
    todo = {}
    if a.url:
        todo[a.as_kind] = [a.url]
    else:
        if not (a.grade and a.semester):
            ap.error('حدّد --grade و --semester (أو --url)')
        kinds = a.kinds.split(',')
        if {'student', 'activity'} & set(kinds):
            try:
                for k, u in moe_books(a.subject, a.grade, a.semester).items():
                    if k in kinds:
                        todo[k] = [u]
            except RuntimeError as e:
                log('البوابة:', e)
        if 'guide' in kinds:
            cands = afedne_guide(a.subject, a.grade, a.semester)
            for t, h in cands[:5]:
                log(f'أفدني (مرشّح): {t} ← {h}')
            if cands:
                todo['guide'] = [h for _, h in cands[:3]]
    if a.list:
        print(__import__('json').dumps(todo, ensure_ascii=False, indent=1)); return
    missing = []
    for kind in a.kinds.split(',') if not a.url else [a.as_kind]:
        dest = os.path.join(a.out, f'{kind}.pdf')
        if os.path.exists(dest) and is_pdf(dest):
            log(f'{kind}: موجود مسبقاً ← {dest}'); continue
        ok = False
        for u in todo.get(kind, []):
            try:
                du = resolve(u)
                log(f'{kind}: تنزيل {du}')
                download(du, dest)
                info = verify(dest, kind, a.out)
                sources[kind] = {'url': u, 'download': du, **info}
                log(f'{kind}: ✔ {info["pages"]} صفحة، {info["size_mb"]} م.ب، الطبعة: {info["edition_hints"] or "اقرأها من صور _check"}')
                ok = True; break
            except Exception as e:
                log(f'{kind}: ✘ {e}')
                if os.path.exists(dest) and not is_pdf(dest):
                    os.remove(dest)
        if not ok:
            missing.append(kind)
    save_json(sources, srcp)
    if missing:
        names = {'student': 'كتاب الطالب', 'activity': 'كتاب النشاط', 'guide': 'دليل المعلم'}
        print('\nالخطة البديلة — اطلب من المعلّم وضع هذه الملفات بنفسه في ' + a.out + ':')
        for k in missing:
            print(f'  - {names.get(k, k)} ← {k}.pdf (أو أرفق صفحات الدرس فقط)')
    print('\nتحقّق الآن من الطبعة والعام في صور ' + os.path.join(a.out, '_check') + ' وفق guides/SOURCES.md.')


if __name__ == '__main__':
    main()
