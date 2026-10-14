# كتابة ورقة الاختبار ودليل التصحيح بصيغة Word (.docx) من اليمين لليسار، مع كسور حقيقية (معادلات Word).
# تحتاج: pip install python-docx
import os
from docx import Document
from docx.enum.section import WD_ORIENT
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Mm, Pt, RGBColor
from exam_lib import parse, plain, ar, marks_word, LETTERS, TYPE_NAMES, AO_NAMES, LV_NAMES

M_NS = 'http://schemas.openxmlformats.org/officeDocument/2006/math'

# ترتيب العناصر كما في مواصفة OOXML (Word قد يرفض الملف إن خالفه)
SEQ = {
    'w:pPr': 'pStyle keepNext keepLines pageBreakBefore framePr widowControl numPr suppressLineNumbers pBdr shd tabs '
             'suppressAutoHyphens kinsoku wordWrap overflowPunct topLinePunct autoSpaceDE autoSpaceDN bidi adjustRightInd '
             'snapToGrid spacing ind contextualSpacing mirrorIndents suppressOverlap jc textDirection textAlignment '
             'textboxTightWrap outlineLvl divId cnfStyle rPr sectPr pPrChange',
    'w:rPr': 'rStyle rFonts b bCs i iCs caps smallCaps strike dstrike outline shadow emboss imprint noProof snapToGrid '
             'vanish webHidden color spacing w kern position sz szCs highlight u effect bdr shd fitText vertAlign rtl cs em '
             'lang eastAsianLayout specVanish oMath',
    'w:tblPr': 'tblStyle tblpPr tblOverlap bidiVisual tblStyleRowBandSize tblStyleColBandSize tblW jc tblCellSpacing '
               'tblInd tblBorders shd tblLayout tblCellMar tblLook tblCaption tblDescription',
    'w:tcPr': 'cnfStyle tcW gridSpan hMerge vMerge tcBorders shd noWrap tcMar textDirection tcFitText vAlign hideMark',
    'w:sectPr': 'headerReference footerReference footnotePr endnotePr type pgSz pgMar paperSrc pgBorders lnNumType '
                'pgNumType cols formProt vAlign noEndnote titlePg textDirection bidi rtlGutter docGrid printerSettings sectPrChange',
}


def fix_order(root):
    for tag, seq in SEQ.items():
        order = {qn('w:' + n): i for i, n in enumerate(seq.split())}
        for el in root.iter(qn(tag)):
            kids = list(el)
            seen = set(); uniq = []
            for k in kids:   # عنصر مفرد مكرّر (مثل szCs) يبقى آخره
                if k.tag in seen and k.tag != qn('w:headerReference') and k.tag != qn('w:footerReference'):
                    uniq = [u for u in uniq if u.tag != k.tag]
                seen.add(k.tag); uniq.append(k)
            for k in kids:
                el.remove(k)
            for k in sorted(uniq, key=lambda k: order.get(k.tag, 999)):
                el.append(k)


def _el(tag, **attrs):
    e = OxmlElement(tag)
    for k, v in attrs.items():
        e.set(qn(k), str(v))
    return e


class DocxExam:
    def __init__(self, font='Arial', digits='ar'):
        self.font, self.dg = font, digits

    @staticmethod
    def save(d, path):
        fix_order(d.element)
        fix_order(d.styles.element)
        d.save(path)

    # ── أساسيات ──
    def new_doc(self, landscape=False):
        d = Document()
        s = d.sections[0]
        s.page_width, s.page_height = (Mm(297), Mm(210)) if landscape else (Mm(210), Mm(297))
        if landscape:
            s.orientation = WD_ORIENT.LANDSCAPE
        s.left_margin = s.right_margin = Mm(13); s.top_margin = Mm(12); s.bottom_margin = Mm(12)
        s._sectPr.append(_el('w:bidi'))
        st = d.styles['Normal']
        st.font.name = self.font; st.font.size = Pt(12.5)
        rpr = st.element.get_or_add_rPr()
        rf = rpr.find(qn('w:rFonts'))
        if rf is None:
            rf = _el('w:rFonts'); rpr.append(rf)
        for k in ('w:ascii', 'w:hAnsi', 'w:cs', 'w:eastAsia'):
            rf.set(qn(k), self.font)
        rpr.append(_el('w:szCs', **{'w:val': 25}))
        rpr.append(_el('w:lang', **{'w:bidi': 'ar-OM'}))
        st.paragraph_format.space_after = Pt(2)
        return d

    def para(self, cont, align='right', space_before=0, space_after=2, keep=False):
        p = cont.add_paragraph()
        pf = p.paragraph_format
        pf.space_before, pf.space_after = Pt(space_before), Pt(space_after)
        if keep:
            pf.keep_with_next = True
        p._p.get_or_add_pPr().insert(0, _el('w:bidi'))
        p.alignment = {'right': WD_ALIGN_PARAGRAPH.RIGHT, 'center': WD_ALIGN_PARAGRAPH.CENTER, 'left': WD_ALIGN_PARAGRAPH.LEFT}[align]
        return p

    def run(self, p, text, bold=False, size=None, color=None, sup=False):
        r = p.add_run(text)
        rpr = r._r.get_or_add_rPr()
        rpr.append(_el('w:rtl'))
        if bold:
            r.bold = True; rpr.append(_el('w:bCs'))
        if size:
            r.font.size = Pt(size); rpr.append(_el('w:szCs', **{'w:val': int(size * 2)}))
        if color:
            r.font.color.rgb = RGBColor.from_string(color)
        if sup:
            r.font.superscript = True
        return r

    def _mrun(self, text, bold=False):
        r = OxmlElement('m:r')
        rp = OxmlElement('m:rPr'); rp.append(_el('m:sty', **{'m:val': 'b' if bold else 'p'})); r.append(rp)
        w = OxmlElement('w:rPr'); w.append(_el('w:rFonts', **{'w:ascii': self.font, 'w:hAnsi': self.font, 'w:cs': self.font}))
        r.append(w)
        t = OxmlElement('m:t'); t.text = text; t.set(qn('xml:space'), 'preserve'); r.append(t)
        return r

    def frac(self, p, whole, num, den, bold=False):
        om = OxmlElement('m:oMath')
        if whole:
            om.append(self._mrun(whole + ' ', bold))
        f = OxmlElement('m:f')
        for tag, val in (('m:num', num), ('m:den', den)):
            e = OxmlElement(tag); e.append(self._mrun(val, bold)); f.append(e)
        om.append(f)
        p._p.append(om)

    def sqrt(self, p, val):
        om = OxmlElement('m:oMath'); rad = OxmlElement('m:rad')
        pr = OxmlElement('m:radPr'); pr.append(_el('m:degHide', **{'m:val': 1})); rad.append(pr)
        rad.append(OxmlElement('m:deg'))
        e = OxmlElement('m:e'); e.append(self._mrun(val)); rad.append(e)
        om.append(rad); p._p.append(om)

    def rich(self, p, text, bold=False, size=None):
        for part in parse(text, self.dg):
            k = part[0]
            if k == 't':
                self.run(p, part[1], bold, size)
            elif k == 'b':
                self.run(p, part[1], True, size)
            elif k == 'f':
                self.frac(p, part[1], part[2], part[3], bold)
            elif k == 'sup':
                self.run(p, part[1], bold, size, sup=True)
            elif k == 'sqrt':
                self.sqrt(p, part[1])
            elif k == 'blank':
                self.run(p, ' .................... ', False, size)
            elif k == 'br':
                p.add_run().add_break()
        return p

    def table(self, cont, rows, cols, widths=None, border=True, center=True):
        t = cont.add_table(rows=rows, cols=cols)
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        tpr = t._tbl.tblPr
        tpr.append(_el('w:bidiVisual'))
        if border:
            b = OxmlElement('w:tblBorders')
            for side in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
                b.append(_el(f'w:{side}', **{'w:val': 'single', 'w:sz': 8, 'w:color': '333333'}))
            tpr.append(b)
        if widths:   # عرض ثابت للأعمدة (Word و LibreOffice يقرآن tblGrid)
            t.autofit = False
            tpr.append(_el('w:tblLayout', **{'w:type': 'fixed'}))
            for gc, w in zip(t._tbl.tblGrid.findall(qn('w:gridCol')), widths):
                gc.set(qn('w:w'), str(int(w * 56.7)))
            for row in t.rows:
                for c, w in zip(row.cells, widths):
                    c.width = Mm(w)
        return t

    def cell(self, c, text, bold=False, size=None, align='center', shade=None):
        c.paragraphs[0]._p.getparent().remove(c.paragraphs[0]._p)
        for k, line in enumerate(str(text).split('\n')):
            p = self.para(c, align, 0, 0)
            self.rich(p, line, bold, size)
        if shade:
            tcpr = c._tc.get_or_add_tcPr(); tcpr.append(_el('w:shd', **{'w:val': 'clear', 'w:color': 'auto', 'w:fill': shade}))

    def lines(self, cont, n, width_mm=182):
        # سطر إجابة: علامة جدولة بخطٍّ منقّط حتى نهاية السطر (لا تُدمج كما تُدمج حدود الفقرات)
        for _ in range(n):
            p = self.para(cont, 'right', 9, 0)
            tabs = OxmlElement('w:tabs')
            tabs.append(_el('w:tab', **{'w:val': 'left', 'w:leader': 'dot', 'w:pos': int(width_mm * 56.7)}))
            p._p.get_or_add_pPr().append(tabs)
            r = self.run(p, '	', size=11, color='777777')

    def header(self, d, hl, landscape=False):
        right, mid, left = hl
        w = (86, 99, 86) if landscape else (60, 64, 60)
        t = self.table(d, 1, 3, w, border=True)
        cells = t.rows[0].cells
        for c, xs, al in ((cells[0], right, 'right'), (cells[1], mid, 'center'), (cells[2], left, 'left')):
            c.paragraphs[0]._p.getparent().remove(c.paragraphs[0]._p)
            for i, x in enumerate(xs):
                p = self.para(c, al, 0, 0)
                self.rich(p, x, bold=(c is cells[1] and i == 0) or x.startswith('النموذج'), size=14 if (c is cells[1] and i == 0) else 10.5)

    # ── ورقة الأسئلة ──
    def paper(self, exam, cfg, form, items, base, hl, calc):
        d = self.new_doc()
        self.header(d, hl)
        self.para(d, 'right', 0, 0).paragraph_format.line_spacing = Pt(6)
        t = self.table(d, 1, 2, (150, 34))
        c0, c1 = t.rows[0].cells
        self.cell(c0, 'اسم الطالب: ..............................................   الصف: ........', align='right', size=11.5)
        self.cell(c1, f'الدرجة\n      / {ar(exam["total"], self.dg)}', bold=True, size=12)
        inst = '؛ '.join(x for x in [exam.get('instructions', 'أجب عن جميع الأسئلة في الورقة نفسها'), calc] if x) + '.'
        p = self.para(d, 'right', 4, 4); self.run(p, inst, size=11)
        for k, it in enumerate(items, 1):
            self.item(d, k, it, base)
        p = self.para(d, 'center', 4, 0); self.run(p, 'انتهت الأسئلة، مع تمنياتنا لكم بالتوفيق', True, 11.5)
        if cfg.get('teacher_name'):
            self.run(p, f'          معلّم المادّة: {cfg["teacher_name"]}', size=10)
        return d

    def item(self, d, k, it, base):
        t = it['type']
        p = self.para(d, 'right', 4, 2, keep=True)
        self.run(p, f'{ar(k, self.dg)}) ', True, 13.5)
        self.rich(p, it['stem'], bold=True)
        self.run(p, f'   ({marks_word(it["marks"])})', size=10, color='444444')
        if it.get('fig'):
            path = it['fig'] if os.path.isabs(it['fig']) else os.path.join(base, it['fig'])
            pp = self.para(d, 'center', 2, 2)
            pp.add_run().add_picture(path, width=Mm(1.7 * it.get('fig_width', 45)))
        if t == 'mcq':
            ch = it['choices']
            cols = it.get('choice_cols', 4 if max(len(plain(c)) for c in ch) < 14 else 2)
            rows = (len(ch) + cols - 1) // cols
            tb = self.table(d, rows, cols, [184 / cols] * cols)
            for i, c in enumerate(ch):
                self.cell(tb.rows[i // cols].cells[i % cols], f'({LETTERS[i]})  {c}', align='right')
        elif t == 'tf':
            p = self.para(d, 'right', 2, 2); self.run(p, '(  صواب  /  خطأ  )', True)
            if it.get('explain', True):
                p = self.para(d, 'right', 2, 0); self.run(p, 'فسّر إجابتك:')
                self.lines(d, it.get('lines', 2))
        elif t == 'match':
            L, R = it['left'], it['right']
            n = max(len(L), len(R))
            tb = self.table(d, n + 1, 5, (12, 62, 16, 12, 62))
            hdr = tb.rows[0].cells
            self.cell(hdr[0], ''); self.cell(hdr[1], it.get('left_title', 'العمود الأول'), True, shade='E6E6E6')
            self.cell(hdr[2], 'الحرف', True, shade='E6E6E6'); self.cell(hdr[3], '')
            self.cell(hdr[4], it.get('right_title', 'العمود الثاني'), True, shade='E6E6E6')
            for i in range(n):
                r = tb.rows[i + 1].cells
                if i < len(L):
                    self.cell(r[0], ar(i + 1, self.dg)); self.cell(r[1], L[i]); self.cell(r[2], '')
                if i < len(R):
                    self.cell(r[3], LETTERS[i]); self.cell(r[4], R[i])
        elif t == 'order':
            p = self.para(d, 'right', 2, 2)
            self.rich(p, '     |     '.join(it['items']))
            p = self.para(d, 'right', 2, 0); self.run(p, 'الترتيب:')
            self.lines(d, it.get('lines', 1))
        elif t == 'table':
            rows = it['grid']['rows']
            tb = self.table(d, len(rows), len(rows[0]))
            for r, row in enumerate(rows):
                for c, v in enumerate(row):
                    hd = r == 0 and it['grid'].get('header', True)
                    self.cell(tb.rows[r].cells[c], v or ' ', hd, shade='E6E6E6' if hd else None)
            self.lines(d, it.get('lines', 0))
        else:
            default = 0 if it.get('parts') else {'long': 6, 'explain': 3, 'creative': 4, 'short': 1, 'fill': 0}.get(t, 2)
            self.lines(d, it.get('lines', default))
        for prt in it.get('parts', []):
            p = self.para(d, 'right', 4, 0); self.run(p, f'({prt["label"]}) ', True); self.rich(p, prt['stem'])
            self.lines(d, prt.get('lines', 2))

    # ── دليل التصحيح ──
    def key(self, exam, cfg, spec, hl):
        tool = spec['tools'][exam['kind']]
        d = self.new_doc(landscape=True)
        self.header(d, hl, landscape=True)
        lessons = '، '.join(f'{l["code"]} {l.get("title", "")}' if isinstance(l, dict) else l for l in exam['lessons'])
        p = self.para(d, 'right', 4, 4)
        self.run(p, f'الدروس: {lessons} · المرجع: {spec["document"]["title"]}، {spec["document"]["edition"]}', size=10)
        cols = tool.get('answer_key_columns') or ['رقم المفردة', 'عنصر التقويم', 'الهدف التعليمي', 'رقم الصفحة', 'الإجابة', 'الدرجة', 'الإرشادات']
        for n, (form, items) in enumerate(exam['forms'].items()):
            if n:
                d.add_page_break()
            p = self.para(d, 'right', 6, 2); self.run(p, f'شبكة مفردات النموذج ({form})', True, 13)
            tb = self.table(d, len(items) + 1, 6, (22, 50, 45, 40, 20, 30))
            for c, v in zip(tb.rows[0].cells, ['رقم المفردة', 'نمط المفردة', 'هدف التقويم', 'مستوى الصعوبة', 'الدرجة', 'الدرس']):
                self.cell(c, v, True, 10.5, shade='E6E6E6')
            for k, it in enumerate(items, 1):
                vals = [ar(k, self.dg), TYPE_NAMES[it['type']], f'{it["ao"]} · {AO_NAMES[it["ao"]]}', f'{it["level"]} · {LV_NAMES[it["level"]]}', ar(it['marks'], self.dg), it['lesson']]
                for c, v in zip(tb.rows[k].cells, vals):
                    self.cell(c, v, size=10.5)
            # ملخّص التوزيع
            ao = {k: sum(i['marks'] for i in items if i['ao'] == k) for k in AO_NAMES}
            lv = {k: sum(i['marks'] for i in items if i['level'] == k) for k in LV_NAMES}
            wa, wl = tool.get('ao') or {}, tool.get('level') or {}
            heads = [AO_NAMES[k] for k in AO_NAMES] + [LV_NAMES[k] for k in LV_NAMES] + ['المجموع']
            vals = [f'{ar(ao[k], self.dg)}' + (f' / {ar(wa[k], self.dg)}' if k in wa else '') for k in AO_NAMES] + \
                   [f'{ar(lv[k], self.dg)}' + (f' / {ar(wl[k], self.dg)}' if k in wl else '') for k in LV_NAMES] + \
                   [f'{ar(sum(i["marks"] for i in items), self.dg)} / {ar(tool["total"], self.dg)}']
            p = self.para(d, 'right', 4, 0)
            tb = self.table(d, 2, len(heads))
            for c, v in zip(tb.rows[0].cells, heads):
                self.cell(c, v, True, 10, shade='E6E6E6')
            for c, v in zip(tb.rows[1].cells, vals):
                self.cell(c, v, size=10)
            p = self.para(d, 'right', 8, 2); self.run(p, f'دليل التصحيح — النموذج ({form})', True, 13)
            widths = (16, 22, 52, 22, 78, 14, 66)
            tb = self.table(d, len(items) + 2, 7, widths)
            for c, v in zip(tb.rows[0].cells, cols):
                self.cell(c, v, True, 10.5, shade='E6E6E6')
            for k, it in enumerate(items, 1):
                r = tb.rows[k].cells
                self.cell(r[0], ar(k, self.dg), size=10.5); self.cell(r[1], AO_NAMES[it['ao']], size=10.5)
                self.cell(r[2], it['objective'], size=10.5, align='right'); self.cell(r[3], it['page'], size=10.5)
                self.cell(r[4], self.answer_text(it), size=10.5, align='right'); self.cell(r[5], ar(it['marks'], self.dg), size=10.5)
                self.cell(r[6], it.get('guidance', ''), size=10.5, align='right')
            last = tb.rows[-1].cells
            m = last[0].merge(last[4]); self.cell(m, 'المجموع', True, 10.5, shade='E6E6E6')
            self.cell(last[5], ar(sum(i['marks'] for i in items), self.dg), True, 10.5); self.cell(last[6], '')
        p = self.para(d, 'right', 14, 0)
        self.run(p, f'إعداد: {cfg.get("teacher_name", "........................")}          '
                    f'مراجعة {cfg.get("reviewer_title", "المعلّم الأول")}: ........................   التوقيع: ............', size=11)
        return d

    def answer_text(self, it):
        if it['type'] == 'mcq':
            a = it['answer']; return f'({LETTERS[a]}) {it["choices"][a]}'
        if it['type'] == 'match' and it.get('pairs'):
            return '، '.join(f'{ar(i + 1, self.dg)} ← {LETTERS[j]}' for i, j in enumerate(it['pairs']))
        parts = [str(it['answer'])] if it.get('answer') not in (None, '') else []
        parts += it.get('steps', [])
        return '\n'.join(parts)
