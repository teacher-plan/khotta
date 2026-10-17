#!/usr/bin/env python3
# استيراد ملفات المعلّم كما هي (PDF، صور، ZIP، مجلد) وتجهيزها للمهارة — guides/INDEXING.md
#
#   python3 import_files.py <ملف أو مجلد أو zip …> --out books/math-7-1            ← يتعرّف نوع كل كتاب آلياً
#   python3 import_files.py صفحات/*.jpg --as student --out books/math-7-1          ← صور صفحات ← student.pdf
#   python3 import_files.py --info books/math-7-1/guide.pdf                        ← عدد الصفحات والطبعة وجودة النص
#   python3 import_files.py --render books/math-7-1/student.pdf --pages 16-21 --dpi 110 --to pages/  ← صور للقراءة
#   python3 import_files.py --text books/math-7-1/guide.pdf --pages 20-22         ← نصّ مطبَّع للبحث
#
# الأنواع: student (كتاب الطالب) و guide (دليل المعلم) و activity (كتاب النشاط). صفحات درسٍ واحد مرفقة
# تُحفظ باسم lesson_<النوع>.pdf وتكفي لبناء الدرس دون فهرسة (SKILL.md «بيئة التشغيل»).
import argparse, os, re, sys, zipfile, tempfile, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import open_pdf, render, norm_ar, is_pdf, log, save_json

IMG = ('.jpg', '.jpeg', '.png', '.webp', '.bmp', '.tif', '.tiff')
KIND_WORDS = {  # كلمات تظهر في الصفحات الأولى بعد التطبيع
    'guide': ['دليل المعلم', 'دليل المعلم', 'teacher', 'نقاط التعلم', 'الاخطاء الشائعه'],
    'activity': ['كتاب النشاط', 'كتاب التمارين', 'workbook', 'activity'],
    'student': ['كتاب الطالب', 'learner', 'student'],
}


def natkey(p):
    return [int(t) if t.isdigit() else t for t in re.split(r'(\d+)', os.path.basename(p))]


def expand(inputs, tmp):
    files = []
    for x in inputs:
        if os.path.isdir(x):
            for r, _, fs in os.walk(x):
                files += [os.path.join(r, f) for f in fs]
        elif x.lower().endswith('.zip'):
            d = tempfile.mkdtemp(dir=tmp)
            with zipfile.ZipFile(x) as z:
                for n in z.namelist():   # حماية من مسارات خارج المجلد
                    if n.startswith('/') or '..' in n.split('/'):
                        continue
                    z.extract(n, d)
            files += expand([d], tmp)
        else:
            files.append(x)
    return sorted([f for f in files if f.lower().endswith('.pdf') or f.lower().endswith(IMG)], key=natkey)


def images_to_pdf(imgs, out):
    import pymupdf
    doc = pymupdf.open()
    for p in imgs:
        im = pymupdf.open(p)
        doc.insert_pdf(pymupdf.open('pdf', im.convert_to_pdf()))
    doc.save(out, deflate=True)
    return doc.page_count


def guess_kind(path, name_hint=''):
    n = norm_ar(name_hint or os.path.basename(path)).lower()
    for k, ws in (('guide', ['دليل', 'guide', 'teacher']), ('activity', ['نشاط', 'activity', 'workbook']), ('student', ['طالب', 'student', 'book'])):
        if any(w in n for w in ws):
            return k
    try:
        d = open_pdf(path)
        head = norm_ar(' '.join(d[i].get_text() for i in range(min(6, d.page_count)))).lower()
        for k in ('guide', 'activity', 'student'):
            if any(norm_ar(w).lower() in head for w in KIND_WORDS[k]):
                return k
    except Exception:
        pass
    return None


def info(path):
    d = open_pdf(path)
    txt = ''.join(d[i].get_text() for i in range(min(10, d.page_count)))
    ar = len(re.findall('[؀-ۿ]', txt))
    broken = txt.count('اإل') + txt.count('األ')
    ed = re.findall(r'(الطبعة[^\n]{0,40}|1[34]\d\d ?هـ|20[12]\d ?م)', txt)
    return {'pages': d.page_count, 'text_layer': ar > 200, 'arabic_text_reversed_ligatures': broken > 0,
            'edition_hints': ed[:4], 'kind_guess': guess_kind(path),
            'advice': ('النص قابلٌ للاستخراج' if ar > 200 else 'صفحات مصوّرة بلا نص: اقرأها صوراً (--render)')
                      + ('، وفيه لام-ألف مفكوكة: استعمل --text (يطبّعها) لا النص الخام' if broken else '')}


def parse_pages(spec, n):
    out = []
    for part in (spec or f'1-{n}').split(','):
        a, _, b = part.partition('-')
        out += list(range(int(a), int(b or a) + 1))
    return [p for p in out if 1 <= p <= n]


def main():
    ap = argparse.ArgumentParser(description='استيراد ملفات الكتب وتجهيزها')
    ap.add_argument('inputs', nargs='*'); ap.add_argument('--out', default='books')
    ap.add_argument('--as', dest='as_kind', choices=['student', 'guide', 'activity'])
    ap.add_argument('--lesson', action='store_true', help='الملفات صفحات درسٍ واحد فقط ← lesson_<النوع>.pdf')
    ap.add_argument('--info'); ap.add_argument('--render'); ap.add_argument('--text')
    ap.add_argument('--pages', help='أرقام صفحات PDF: 16-21,24'); ap.add_argument('--dpi', type=int, default=110)
    ap.add_argument('--to', default='pages')
    a = ap.parse_args()

    if a.info:
        import json; print(json.dumps(info(a.info), ensure_ascii=False, indent=1)); return
    if a.render:
        d = open_pdf(a.render); os.makedirs(a.to, exist_ok=True)
        for p in parse_pages(a.pages, d.page_count):
            print(render(d[p - 1], os.path.join(a.to, f'p{p:03d}.png'), dpi=a.dpi))
        return
    if a.text:
        d = open_pdf(a.text)
        for p in parse_pages(a.pages, d.page_count):
            print(f'── صفحة PDF {p} ──\n{norm_ar(d[p - 1].get_text())}')
        return
    if not a.inputs:
        ap.error('أعطِ ملفات أو مجلداً أو zip')

    os.makedirs(a.out, exist_ok=True)
    tmp = tempfile.mkdtemp()
    try:
        files = expand(a.inputs, tmp)
        pdfs = [f for f in files if f.lower().endswith('.pdf')]
        imgs = [f for f in files if f.lower().endswith(IMG)]
        report = {}
        if imgs:   # صور الصفحات تُضمّ بترتيب أسمائها في PDF واحد
            kind = a.as_kind or guess_kind(imgs[0]) or 'student'
            name = f'lesson_{kind}.pdf' if a.lesson or len(imgs) < 25 else f'{kind}.pdf'
            dest = os.path.join(a.out, name)
            n = images_to_pdf(imgs, dest)
            report[name] = {'from_images': len(imgs), 'pages': n}
            log(f'✔ {len(imgs)} صورة ← {dest}')
        for f in pdfs:
            if not is_pdf(f):
                log(f'✘ ليس PDF سليماً: {f}'); continue
            kind = a.as_kind or guess_kind(f)
            if not kind:
                log(f'? لم أتعرّف نوع {f} — أعد بـ --as student|guide|activity'); continue
            d = open_pdf(f)
            name = f'lesson_{kind}.pdf' if a.lesson or d.page_count < 25 else f'{kind}.pdf'
            dest = os.path.join(a.out, name)
            if os.path.abspath(f) != os.path.abspath(dest):
                shutil.copyfile(f, dest)
            report[name] = info(dest)
            log(f'✔ {os.path.basename(f)} ← {dest} ({kind}، {report[name]["pages"]} صفحة)')
        save_json(report, os.path.join(a.out, 'import_report.json'))
        print(f'تقرير الاستيراد: {os.path.join(a.out, "import_report.json")}')
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == '__main__':
    main()
