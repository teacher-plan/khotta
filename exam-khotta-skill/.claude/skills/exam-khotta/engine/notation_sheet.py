#!/usr/bin/env python3
# صفحة اختبار الرموز: يعرض كل صيغة كما ستظهر في PDF وفي Word، لتتحقّق بعينك قبل استعمالها في اختبار.
#   python3 <S>/engine/notation_sheet.py [samples.json] --out <مجلد>
# samples.json: [["الوصف", "الصيغة بالكتابة المختصرة"], …]؛ بدونه تُعرض العيّنات المضمّنة أدناه (كل الرموز).
import argparse, html, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import notation
import build_exam
from build_exam import page, to_pdf, make_snipper, resolve_quran

SAMPLES = [
    ['— الرياضيات —', ''],
    ['جمع وطرح وضرب وقسمة', '٣٤ + ١٢ − ٨ × ٢ ÷ ٤ = ٤٢'],
    ['أعداد سالبة بين قوسين', '(−٦) × (−٤) = ٢٤ ، ٥ − (−٣) = ٨'],
    ['عدد عشري ونسبة مئوية', '٣.٤ + ٠.٦ = ٤ ، ٢٥% من ٨٠ = ٢٠'],
    ['كسر', '{٣/٤} + {١/٤} = ١'],
    ['عدد كسري', '{٢ ١/٣} − {١ ٢/٣} = {٢/٣}'],
    ['كسر فيه عملية', '{٣ + ٥/٢ × ٤} = {٨/٨} = ١'],
    ['أسّ (أعلى يسار الأساس)', '٥^{٢} = ٥ × ٥ = ٢٥ ، ١٠^{٣} = ١٠٠٠'],
    ['أسّ على سالب بين قوسين', '(−٣)^{٢} = ٩'],
    ['متغيّر بأسّ ومعامل', '٣س^{٢} + ٢س − ٥ = ٠'],
    ['جذر تربيعي (علامة معكوسة)', '√{٣٦} = ٦ ، √{٨١} + √{١٦} = ١٣'],
    ['جذر تكعيبي', '√[٣]{١٢٥} = ٥'],
    ['جذر فوق عملية', '√{٢٥ + ١٤٤} = √{١٦٩} = ١٣'],
    ['كسر تحت جذر', '√{{٩/١٦}} = {٣/٤}'],
    ['عشري دوري', '{١/٣} = ٠.‾{٣}'],
    ['متباينات', '٣ < ٥ ، ٧ > ٢ ، س ≤ ٤ ، ص ≥ −١ ، ٤ ≠ ٥'],
    ['معادلة بمتغيّر', '٢س + ٣ = ١١ ← س = ٤'],
    ['زوايا', 'ق∠أ ب ج = ٩٠° ، ٣٠° + ٦٠° = ٩٠°'],
    ['هندسة', 'أب ∥ جد ، م ن ⊥ ل ك ، △ أ ب ج'],
    ['زوج مرتّب', 'النقطة (٢، ٣)'],
    ['ط ومساحة الدائرة', 'م = ط نق^{٢} ≈ ٣.١٤ × ٥^{٢}'],
    ['ترميز علمي', '٣ × ١٠^{٨} م/ث'],
    ['وحدات مربعة ومكعبة', '٢٥ سم^{٢} ، ٨ م^{٣}'],
    ['فراغ للإجابة', '٧ × ___ = ٥٦'],
    ['— العلوم —', ''],
    ['صيغة كيميائية', 'الماء ce{H2O} وحمض الكبريتيك ce{H2SO4}'],
    ['أيونات بشحنات', 'ce{Na^+} و ce{SO4^{2-}} و ce{Fe^{3+}}'],
    ['معادلة موزونة', 'ce{2H2 + O2 -> 2H2O}'],
    ['تفاعل انعكاسي', 'ce{N2 + 3H2 <=> 2NH3}'],
    ['حالات المادة', 'ce{NaCl(aq) + AgNO3(aq) -> AgCl(s) + NaNO3(aq)}'],
    ['قانون فيزيائي بالعربية', 'ق = ك × ت ، ع = {ف/ز}'],
    ['قانون بالرموز اللاتينية', 'ltr{F = ma} و ltr{v = d/t}'],
    ['رموز يونانية ووحدات', 'المقاومة ٢٠ Ω ، الطول الموجي λ = ٥٠٠ nm ، Δ ط'],
    ['تسارع', '٩.٨ م/ث^{٢}'],
    ['— اللغة العربية —', ''],
    ['نص مشكول', 'ذَهَبَ الطَّالِبُ إِلَى المَدْرَسَةِ مُبَكِّرًا.'],
    ['تنوين وشدّة', 'قَرَأَ مُحَمَّدٌ كِتَابًا مُفِيدًا.'],
    ['آية بالمرجع (تُجلب آلياً)', 'quran[112:1-4]'],
]


def build(samples, out, dg='ar', font='readex'):
    os.makedirs(out, exist_ok=True)
    build_exam.BODY_FONT = font
    samples = resolve_quran({'s': samples}, out)['s']
    rows = []
    for d, t in samples:
        if not t:
            rows.append(f'<tr><th colspan="3" class="sec">{html.escape(d)}</th></tr>')
        else:
            rows.append(f'<tr><td class="d">{html.escape(d)}</td><td class="src" dir="ltr">{html.escape(t)}</td><td class="r">{notation.html(t, dg)}</td></tr>')
    body = ('<h1 style="font-size:15pt;margin:0 0 6px">صفحة اختبار الرموز — PDF</h1>'
            '<style>table.t{width:100%;border-collapse:collapse;font-size:12.5pt} table.t td,table.t th{border:1px solid #999;padding:5px 8px;vertical-align:middle}'
            ' .src{font-family:DejaVu Sans Mono,monospace;font-size:8.5pt;color:#555;text-align:left;width:34%} .d{width:22%;font-size:10pt} .sec{background:#e8e8e8}</style>'
            f'<table class="t"><tr><th>الحالة</th><th>المكتوب في ملف الاختبار</th><th>الناتج</th></tr>{"".join(rows)}</table>')
    hp = os.path.join(out, 'رموز.html'); open(hp, 'w', encoding='utf-8').write(page(body))
    try:
        to_pdf(hp, hp[:-5] + '.pdf'); print(hp[:-5] + '.pdf')
    except Exception as e:
        print('⚠ PDF:', e)
    # Word
    from docx_writer import DocxExam
    fake = {'forms': {'x': [{'stem': t} for _, t in samples if t]}}
    W = DocxExam('Traditional Arabic' if font == 'amiri' else 'Arial', dg, make_snipper(fake, dg, os.path.join(out, 'رموز_صور')))
    doc = W.new_doc()
    p = W.para(doc, 'right', 0, 6); W.run(p, 'صفحة اختبار الرموز — Word', True, 15)
    tb = W.table(doc, len(samples) + 1, 2, (60, 124))
    W.cell(tb.rows[0].cells[0], 'الحالة', True, shade='E6E6E6'); W.cell(tb.rows[0].cells[1], 'الناتج', True, shade='E6E6E6')
    for i, (d, t) in enumerate(samples, 1):
        W.cell(tb.rows[i].cells[0], d, bold=not t, size=10, align='right', shade='E8E8E8' if not t else None)
        W.cell(tb.rows[i].cells[1], t or ' ', align='right')
    f = os.path.join(out, 'رموز.docx'); W.save(doc, f); print(f)


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('samples', nargs='?'); ap.add_argument('--out', default='notation_test')
    ap.add_argument('--font', choices=['readex', 'amiri'], default='readex')
    ap.add_argument('--digits', choices=['ar', 'latin'], default='ar', help='أرقام المحتوى: عربية (الرياضيات) أو لاتينية (العلوم)')
    a = ap.parse_args()
    build(json.load(open(a.samples, encoding='utf-8')) if a.samples else SAMPLES, a.out, dg=a.digits, font=a.font)
