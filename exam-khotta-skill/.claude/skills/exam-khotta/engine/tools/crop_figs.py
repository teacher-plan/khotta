#!/usr/bin/env python3
# تقطيع صور أسئلة الكتاب وأشكاله بحدودها فقط — rules/GENERAL.md (صور أسئلة الكتاب بجانب أسئلتها)
#
#   python3 crop_figs.py books/math-7-1/student.pdf --page 37 --auto --out lessons/١-٧/figs --prefix ١-٧
#       ← يكتشف الأشكال والصور تلقائياً، ويحفظ كل مرشّح، ومعاينةً مرقّمة preview_p37.jpg لتختار منها
#   python3 crop_figs.py books/math-7-1/student.pdf --page 37 --grid --out lessons/١-٧/figs
#       ← صورة الصفحة بشبكة مئوية مرقّمة (٠–١٠٠) لتحدّد بها حدود سؤالٍ بعينه
#   python3 crop_figs.py books/math-7-1/student.pdf --page 37 --box 8,22,60,48 --name ١-٧_تمرين٣ --out lessons/١-٧/figs
#       ← قصّ مستطيل بالنسب المئوية (يسار، أعلى، يمين، أسفل) بدقّة ٢٠٠ نقطة/بوصة
#   --printed 36 بدل --page: الرقم المطبوع، ويُحوَّل بـ offsets.json الموجود بجانب الكتاب (أو --offset).
# الطريقة الموصى بها: --auto أولاً؛ إن لم يلتقط السؤال كاملاً (نصّ السؤال مع شكله) استعمل --grid ثم --box.
import argparse, os, re, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import open_pdf, log


def pdf_page(a, doc):
    if a.page:
        return a.page
    off = a.offset
    if off is None:
        f = os.path.join(os.path.dirname(os.path.abspath(a.pdf)), 'offsets.json')
        kind = os.path.splitext(os.path.basename(a.pdf))[0]
        j = json.load(open(f, encoding='utf-8')) if os.path.exists(f) else {}
        alias = {'student': 'student_book', 'guide': 'teacher_guide', 'activity': 'activity_book'}   # الشكل القديم
        off = j.get(kind, j.get(alias.get(kind, ''), 0))
    return a.printed + (off or 0)


def merge(rects, gap):
    """يدمج المستطيلات المتقاربة (أجزاء شكلٍ واحد) حتى لا تتغيّر."""
    import pymupdf
    rs = [pymupdf.Rect(r) for r in rects]
    changed = True
    while changed:
        changed = False
        out = []
        while rs:
            r = rs.pop()
            for i, q in enumerate(out):
                if (r + (-gap, -gap, gap, gap)).intersects(q):
                    out[i] = q | r; changed = True; break
            else:
                out.append(r)
        rs = out
    return rs


def auto_regions(page):
    import pymupdf
    R = page.rect; area = R.width * R.height; m = min(R.width, R.height)
    cands = []; imgs = []
    def add_img(bb):   # صور قد تكون مقسّمة بلاطاتٍ صغيرة؛ نقبل الصالح منها بأي حجم ثم ندمجها
        x0, y0, x1, y1 = bb
        if x1 > x0 and y1 > y0:
            b = pymupdf.Rect(bb) & R
            if not b.is_empty and b.width * b.height < 0.85 * area:
                imgs.append(b)
    for im in page.get_image_info():
        add_img(im['bbox'])
    for blk in page.get_text('dict')['blocks']:   # صور داخل كائنات Form لا تظهر في get_image_info
        if blk.get('type') == 1:
            add_img(blk['bbox'])
    for d in page.get_drawings():
        b = d['rect']
        if not R.contains(b):   # رسوم خارج حدود الصفحة المرئية (صفحات مزدوجة، أطر القصّ)
            continue
        if b.width * b.height < 0.0005 * area or b.width > 0.97 * R.width and b.height > 0.9 * R.height:
            continue
        cands.append(b)
    # بلاطات الصورة الواحدة تُدمج بفجوة أوسع، والرسوم بفجوة أضيق حتى لا تلتصق بخطوط الإجابة؛
    # ويُصفّى كلٌّ منهما قبل الجمع حتى لا يبتلع إطارٌ عريض صورةً داخله
    def ok(r):   # أطر الصفحة والزخارف الطويلة الرفيعة تُستبعد، والصغير جداً يُتجاهل
        return (r.width * r.height > 0.006 * area and r.width < 0.95 * R.width and r.height < 0.9 * R.height
                and not (r.height < 0.03 * R.height or r.width < 0.03 * R.width) and r.y0 > R.height * 0.06)
    regs = merge([r for r in merge(imgs, gap=m * 0.035) + merge(cands, gap=m * 0.01) if ok(r)], gap=0)
    regs.sort(key=lambda r: (round(r.y0 / (R.height * 0.05)), -r.x1))   # من أعلى، ثم من اليمين (عربي)
    return regs


def main():
    ap = argparse.ArgumentParser(description='تقطيع صور الأسئلة والأشكال')
    ap.add_argument('pdf'); ap.add_argument('--page', type=int); ap.add_argument('--printed', type=int); ap.add_argument('--offset', type=int)
    ap.add_argument('--auto', action='store_true'); ap.add_argument('--grid', action='store_true')
    ap.add_argument('--box', help='يسار,أعلى,يمين,أسفل بالنسب المئوية'); ap.add_argument('--name')
    ap.add_argument('--out', default='figs'); ap.add_argument('--prefix', default='fig'); ap.add_argument('--dpi', type=int, default=200)
    ap.add_argument('--pad', type=float, default=1.2, help='هامش حول القصّ بالنسبة المئوية')
    a = ap.parse_args()
    if not (a.page or a.printed):
        ap.error('حدّد --page (رقم PDF) أو --printed (الرقم المطبوع)')
    import pymupdf
    from PIL import Image, ImageDraw
    doc = open_pdf(a.pdf); pn = pdf_page(a, doc); page = doc[pn - 1]; R = page.rect
    os.makedirs(a.out, exist_ok=True)

    def save(rect, name):
        p = a.pad / 100
        rect = pymupdf.Rect(rect.x0 - p * R.width, rect.y0 - p * R.height, rect.x1 + p * R.width, rect.y1 + p * R.height) & R
        if rect.is_empty or rect.width < 5 or rect.height < 5:
            return None
        f = os.path.join(a.out, name + '.jpg')
        pix = page.get_pixmap(dpi=a.dpi, clip=rect)
        if pix.width < 2 or pix.height < 2:
            return None
        Image.frombytes('RGB', (pix.width, pix.height), pix.samples).save(f, quality=90)
        return f

    if a.grid:
        pix = page.get_pixmap(dpi=110); im = Image.frombytes('RGB', (pix.width, pix.height), pix.samples); dr = ImageDraw.Draw(im)
        for k in range(0, 101, 5):
            x, y = im.width * k / 100, im.height * k / 100
            c = (220, 30, 30) if k % 10 == 0 else (255, 170, 170)
            dr.line([(x, 0), (x, im.height)], fill=c, width=1); dr.line([(0, y), (im.width, y)], fill=c, width=1)
            if k % 10 == 0:
                dr.text((x + 2, 2), str(k), fill=(200, 0, 0)); dr.text((2, y + 2), str(k), fill=(200, 0, 0))
        f = os.path.join(a.out, f'grid_p{pn}.jpg'); im.save(f, quality=85); print(f); return

    if a.box:
        x0, y0, x1, y1 = [float(v) / 100 for v in a.box.split(',')]
        rect = pymupdf.Rect(R.width * x0, R.height * y0, R.width * x1, R.height * y1)
        print(save(rect, a.name or f'{a.prefix}_p{pn}')); return

    if a.auto:
        regs = auto_regions(page)
        pix = page.get_pixmap(dpi=80); im = Image.frombytes('RGB', (pix.width, pix.height), pix.samples); dr = ImageDraw.Draw(im)
        s = im.width / R.width; made = []
        regs = [r & R for r in regs if not (r & R).is_empty]
        for i, r in enumerate(regs, 1):
            f = save(r, f'{a.prefix}_p{pn}_{i:02d}')
            if not f:
                continue
            made.append(f)
            dr.rectangle([r.x0 * s, r.y0 * s, r.x1 * s, r.y1 * s], outline=(220, 30, 30), width=3)
            dr.rectangle([r.x1 * s - 26, r.y0 * s, r.x1 * s, r.y0 * s + 20], fill=(220, 30, 30)); dr.text((r.x1 * s - 22, r.y0 * s + 3), f'{i}', fill='white')
        pv = os.path.join(a.out, f'preview_p{pn}.jpg'); im.save(pv, quality=80)
        print(f'{len(made)} مرشّح على صفحة PDF {pn}؛ المعاينة: {pv}')
        for f in made:
            print(' ', f)
        print('انظر في المعاينة، واحذف ما لا يلزم، وأعد تسمية ما يلزم بالشكل <رمز الدرس>_<وصف>.jpg؛'
              ' وإن لم يلتقط سؤالاً كاملاً فاستعمل --grid ثم --box.')
        return
    ap.error('اختر --auto أو --grid أو --box')


if __name__ == '__main__':
    main()
