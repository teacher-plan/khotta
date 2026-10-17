# ورقة ملخّص الدرس ٦-٦ «تحويل الكسور إلى كسور عشرية» بالقالب الجديد (summary2.py).
# python3.12 gen_fdec_summary.py ← node ../sheet.mjs ملخص_تحويل_الكسور_إلى_كسور_عشرية.html <مجلد> ← node ../sheetcheck.mjs ملخص_تحويل_الكسور_إلى_كسور_عشرية.html
import os
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'summary2.py'), encoding='utf-8').read())
CSS += '.tb.u4{table-layout:fixed}.tb.u4 th,.tb.u4 td{text-align:center}.tb.u4 td:first-child{width:auto;font-size:11.5pt}.tb.u4 td{font-size:11.5pt}'
CSS += '.dec{direction:ltr;unicode-bidi:isolate;display:inline-block}.dot{position:relative;display:inline-block}.dot::after{content:"•";position:absolute;top:-.62em;left:50%;transform:translateX(-50%);font-size:.6em;color:#DB2777}'
AR10 = '٠١٢٣٤٥٦٧٨٩'
def DEC(s):
    out, dot = [], False
    for ch in s:
        if ch == '^': dot = True; continue
        c = AR10[int(ch)] if ch.isdigit() else ('٫' if ch == '.' else ch)
        out.append(f'<span class="dot">{c}</span>' if dot else c); dot = False
    return '<span class="dec">' + ''.join(out) + '</span>'
def MF(*p): return M(*[FR(*x) if isinstance(x, tuple) else x for x in p])

HD = header('٦-٦', 'تحويل الكسور إلى كسور عشرية', 'الوحدة السادسة: الكسور (١)',
            'أحوّل الكسر إلى كسرٍ عشري بالقسمة، وأميّز المنتهي والدوري، وأقرّب لأقرب ٣ منازل')

p1 = ''.join([
 sec(1, 'المفردات',
  table(['المفردة', 'معناها', 'مثال'], [
   ['<b>كسرٌ عشري منتهٍ</b> (terminating)', 'عدد أرقامه محدّد', M(FR('٦', '٢٥'), EQ, DEC('0.24'))],
   ['<b>كسرٌ عشري دوري</b> (recurring)', 'أرقامه تتكرّر إلى ما لا نهاية', M(FR('٧١', '٩٩'), EQ, DEC('0.^7^1'))]], 'u4')),
 sec(2, 'القاعدة',
  rule('الكسر قسمة: نقسم <b>البسط على المقام</b> لنحصل على الكسر العشري.<br>'
       'نكتب الكسر العشري الدوري بثلاث نقاط (' + DEC('0.4545') + '…) أو بنقطةٍ فوق الرقم المتكرّر، ونقطتين فوق أول وآخر رقمٍ في مجموعة التكرار (' + DEC('0.^4^5') + ').<br>'
       'إذا طالت مجموعة التكرار نقرّب لأقرب ٣ منازل عشرية بالنظر إلى المنزلة الرابعة.', '÷')),
 sec(3, 'خطأٌ شائع',
  warn([(M('٣', DV, '٧', EQ, DEC('0.4285')) + ' منتهٍ', M(DEC('0.428571428')) + '… دوري', 'مجموعة التكرار قد تكون طويلة؛ نكمل القسمة حتى يتضح التكرار')])),
 sec(4, 'مثال محلول: كسرٌ منتهٍ',
  example(f'حوّل {MF(("٣", "٨"))} إلى كسرٍ عشري.', [
   (M('٣', DV, '٨', EQ, DEC('0.375')), 'نقسم البسط على المقام'),
   (M(DEC('0.375')), 'الناتج منتهٍ، فنكتب كل الأرقام')], M(DEC('0.375')))),
])
p2 = ''.join([
 sec(5, 'مثال محلول: كسرٌ دوري',
  example(f'حوّل {MF(("٥", "١١"))} إلى كسرٍ عشري.', [
   (M('٥', DV, '١١', EQ, DEC('0.4545') + '…'), 'الرقمان ٤ و ٥ يتكرّران'),
   (M(DEC('0.^4^5')), 'نقطتان فوق أول وآخر رقمٍ في مجموعة التكرار')], M(DEC('0.^4^5')))),
 sec(6, 'مثال محلول: التقريب',
  example(f'حوّل {MF(("٣", "٧"))} إلى كسرٍ عشري لأقرب ٣ منازل عشرية.', [
   (M('٣', DV, '٧', EQ, DEC('0.428571428') + '…'), 'مجموعة التكرار ٤٢٨٥٧١'),
   (M(DEC('0.4285')), 'المنزلة الرابعة ٥ فنقرّب للأعلى'),
   (M(DEC('0.429')), 'لأقرب ٣ منازل عشرية')], M(DEC('0.429')))),
 practice([f'حوّل {MF(("١٧", "٢٥"))}', f'حوّل {MF(("٢", "٣"))}', f'حوّل {MF(("٧", "١١"))}', f'حوّل {MF(("٦", "٧"))} لأقرب ٣ منازل'],
          [M(DEC('0.68')), M(DEC('0.^6')), M(DEC('0.^6^3')), M(DEC('0.857'))]),
])
build(os.path.join(HERE, 'ملخص_تحويل_الكسور_إلى_كسور_عشرية.html'), 'ملخص تحويل الكسور إلى كسور عشرية', [(HD, p1), (HD, p2)])
