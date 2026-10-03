# شرائح درس ٣-٦ «قسمة الأعداد العشرية والكسور العشرية (٢)» — الصف السابع (حصتان، كتاب الطالب ص٦٨–٦٩)
# المراجع: دليل المعلم ص٧٢ (القسمة كقسمة الأعداد الكاملة، المقسوم الكامل: نضع الفاصلة ونكمل بالأصفار؛ الأخطاء الشائعة: الفاصلة والأصفار عند وجود باقٍ؛
# النشاط: ورقة المصادر ٣-٦ «الصديق والعالِم»؛ التمرين ٣: ٦٫٢٤٢ أو ٦٫٢٤٢٥ قبل التقريب)،
# كتاب الطالب ص٦٨–٦٩ (مثال ٣-٦)، وإجابات الدليل ص٧٩ (كتاب الطالب) وص٨٣ (كتاب النشاط ص٥٠–٥١).
# python3.12 gen_powers.py div2_slides.py قسمة_الأعداد_العشرية_٢_عرض_تفاعلي.html "قسمة الأعداد العشرية والكسور العشرية (٢) — الصف السابع"
exec(open(os.path.join(HERE, 'vcol.py'), encoding='utf-8').read())
exec(open(os.path.join(HERE, 'figs.py'), encoding='utf-8').read())
from decimal import Decimal as _D, ROUND_HALF_UP as _HU

DV = '<span class="x">÷</span>'
def STP(lab, expr='', cls=''): return st(f'<div class="stp {cls}"><span class="lab">{lab}</span>{expr}</div>')
def STEPS(*rows): return '<div class="stps">' + ''.join(rows) + '</div>'
def VB(h): return f'<div class="vbox">{h}</div>'
def Q(a_, k): return f'{_ar(a_)} ÷ {_ar(k)}'
def PAD(a_, n):   # نكتب المقسوم بمنازل عشرية تزيد منزلةً على المطلوب: ٦٨ ← ٦٨٫٠٠
    i, _, d = a_.partition('.'); return i + '.' + d.ljust(n + 1, '0')
def RES(a_, k, n): return _ar(str((_D(a_) / _D(k)).quantize(_D(1).scaleb(-n), _HU)))
def RAW(a_, k, n): return _ar(str((_D(a_) / _D(k)).quantize(_D(1).scaleb(-(n + 1)), rounding='ROUND_DOWN')))
def SOL(a_, k, n):   # الحل: القسمة بمنزلةٍ زائدة ثم التقريب
    return vdiv(PAD(a_, n), k) + f'<small>{RAW(a_, k, n)} ≈ {RES(a_, k, n)}</small>'
S = []
ME = 'إعداد: أ. عيسى الحارثي'
S.append(slide(f'''<span class="tag">الصف السابع · الدرس ٣-٦</span>
<h1 class="h1s">قسمة الأعداد العشرية والكسور العشرية (٢)</h1>
<p class="lead">كتاب الطالب ص ٦٨ و ٦٩ · حصتان</p>
<p class="lead" style="font-size:clamp(26px,4.8vh,56px)">{ME}</p>''', 'cover'))
CAN = ['أقسم عدداً كاملاً أو عشرياً على عددٍ من رقمٍ واحد <b>عندما يوجد باقٍ</b>', 'أكمل القسمة <b>بإضافة أصفار</b> بعد الفاصلة', 'أقرّب الناتج إلى <b>درجة الدقّة</b> المطلوبة']
S.append(slide(f'''<h2>في نهاية هذا الدرس…</h2>
<div class="can">{''.join(f'<div><span class="can-i">✔</span><span><b>أنا أستطيع</b> أن {t}</span></div>' for t in CAN)}</div>'''))
S.append(slide(f'''<h2>مفردات الدرس</h2>
{st('<div class="vocab wide"><div><span>الباقي</span><i>remainder</i></div><div><span>درجة الدقّة</span><i>degree of accuracy</i></div><div><span>منزلة عشرية</span><i>decimal place</i></div></div>')}
<p class="lead">حصتان: <b class="c-i">أنا</b> ← <b class="c-we">نحن</b> ← <b class="c-u">أنتم</b></p>'''))

# ═══════════ الحصة الأولى ═══════════
S.append(slide('''<span class="tag">الحصة الأولى · ٤٠ دقيقة</span><h2>القسمة مع باقٍ والتقريب لمنزلة عشرية</h2>
<div class="plan"><div><b>٤ د</b>تهيئة</div><div><b>٥ د</b>القاعدة</div><div><b>٩ د</b>مثال ٣-٦ (أ)</div>
<div><b>७ د</b>نحن</div><div><b>٨ د</b>أنتم</div><div><b>٤ د</b>انتبه</div><div><b>٣ د</b>بطاقة الخروج</div></div>'''.replace('७', '٧'), 'divider'))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">تهيئة 🤔</span></div><h2>٦٨ ÷ ٧ = ٩ والباقي ٥</h2>
{st('<div class="note">هل يمكن أن نكمل القسمة بدلاً من التوقّف عند الباقي؟</div>')}
{st('<div class="note">نعم! ٦٨ = ٦٨٫٠٠ ، فنضع الفاصلة ونكمل بالأصفار</div>')}''' + tn('من الدليل: إذا كان المقسوم عدداً كاملاً ووُجد باقٍ نضع الفاصلة في النهاية ونستمر بإضافة الأصفار. الصفر بعد الفاصلة لا يغيّر قيمة العدد (درس ٣-٣).')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('كتاب الطالب ص ٦٨')}</div><h2>عند وجود باقٍ</h2>
<div class="defs">{st('<div><b class="kk c-exp">١</b><span>نكمل القسمة <b class="c-exp">بإضافة أصفار</b> بعد الفاصلة</span></div>')}{st('<div><b class="kk c-we">٢</b><span>نتوقّف عندما يكون في الناتج <b class="c-we">منزلةٌ زائدة</b> على المطلوب</span></div>')}{st('<div><b class="kk c-lcm">٣</b><span><b>نقرّب</b> الناتج إلى درجة الدقّة المطلوبة (درس ٣-٢)</span></div>')}</div>''' + tn('مثال: المطلوب منزلة عشرية واحدة ← نحسب منزلتين ثم نقرّب.')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('مثال ٣-٦ (أ)')}</div><h2>{Q('68', '7')} لأقرب منزلة عشرية واحدة</h2>
<div class="row vrow">{STEPS(STP('نكتب ٦٨ على صورة ٦٨٫٠٠ (منزلتان)'), STP('٦٨ ÷ ٧', M('٩ والباقي ٥', cls='sm')), STP('٥٠ ÷ ٧', M('٧ والباقي ١', cls='sm')), STP('١٠ ÷ ٧', M('١ ثم نتوقّف', cls='sm')), STP('الرقم يمين ٧ هو ١، فيبقى ٧', M('٩٫٧١ ≈ ٩٫٧', cls='sm'), 'fin'))}
{VB(vdiv('68.00', '7', reveal=True))}</div>''' + tn('الباقي ٥ يُكتب صغيراً يسار الصفر الأول فيصبح ٥٠، والباقي ١ يسار الصفر الثاني فيصبح ١٠ (كما في الكتاب).')))
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('تمرين ١ (أ، ب)')}</div><h2>معاً: لأقرب منزلة عشرية واحدة</h2>
<div class="row">{st(f'<button class="flip box col" style="flex:1"><span class="hint">{Q("89", "3")}</span><span class="tap">👆</span><span class="hid col vfl">{SOL("89", "3", 1)}</span></button>')}{st(f'<button class="flip box col" style="flex:1"><span class="hint">{Q("92", "7")}</span><span class="tap">👆</span><span class="hid col vfl">{SOL("92", "7", 1)}</span></button>')}</div>''' + tn('في ٨٩ ÷ ٣: ٢٩٫٦٦ والرقم يمين ٦ هو ٦، فنقرّب إلى ٢٩٫٧.')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ١ (ج)')}{timer(2)}</div>''' + quiz(f'{Q("56", "6")} لأقرب منزلة عشرية واحدة', [M('٩٫٣'), M('٩٫٤'), M('٩٫٣٣'), M('٩')], 0, '٥٦٫٠٠ ÷ ٦ = ٩٫٣٣ ≈ ٩٫٣')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ١ (د)')}</div>''' + quiz(f'{Q("65", "8")} لأقرب منزلة عشرية واحدة', [M('٨٫٢'), M('٨٫١'), M('٨٫١٢'), M('٨٫٠')], 1, '٦٥٫٠٠ ÷ ٨ = ٨٫١٢ ≈ ٨٫١')))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">انتبه ⚠️ خطأ شائع</span>{ref('دليل المعلم ص ٧٢')}</div><h2>الفاصلة والأصفار عند وجود باقٍ</h2>
<div class="row">{st(box('<div class="col"><span class="hint no">✘ توقّفنا عند الباقي</span>' + M('٦٨ ÷ ٧ = ٩٫٥') + '</div>', style="flex:1"))}{st(box('<div class="col"><span class="hint ok">✔ أكملنا بالأصفار</span>' + M('٦٨ ÷ ٧ ≈ ٩٫٧') + '</div>', style="flex:1"))}</div>
{st('<div class="note">الباقي ٥ ليس جزءاً من عشرة! نكمل: ٥٠ ÷ ٧ ، ثم ١٠ ÷ ٧</div>')}''' + tn('الخطأ الأول (كتابة الباقي بعد الفاصلة) من خارج المرجع، ويمثّل خطأ الدليل: «قد لا يضع الطلاب الفاصلة والأصفار المناسبة عند وجود باقٍ».')))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ١ 🎫</span><h2>لأقرب منزلة عشرية واحدة</h2>
<div class="exit">{st(f'<div><b>١</b>{Q("145", "9")}</div>')}{st(f'<div><b>٢</b>{Q("275", "3")}</div>')}{st(f'<div><b>٣</b>{Q("879", "7")}</div>')}</div>'''))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ١ 🎫</span><h2>الإجابات</h2>
<button class="flip box col" style="min-width:40vw"><span class="tap">👆 اضغط لإظهار الإجابات</span><span class="hid col">{M('١٦٫١', cls="sm")}{M('٩١٫٧', cls="sm")}{M('١٢٥٫٦', cls="sm")}</span></button>'''))

# ═══════════ الحصة الثانية ═══════════
S.append(slide('''<span class="tag">الحصة الثانية · ٤٠ دقيقة</span><h2>التقريب لمنزلتين عشريتين</h2>
<div class="plan"><div><b>٣ د</b>إحماء</div><div><b>٩ د</b>مثال ٣-٦ (ب)</div><div><b>٦ د</b>نحن</div>
<div><b>٦ د</b>أنتم</div><div><b>٦ د</b>تجربة العالِمة</div><div><b>٦ د</b>الصديق والعالِم</div><div><b>٤ د</b>بطاقة الخروج</div></div>''', 'divider'))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">إحماء 🔥</span>{timer(1)}</div>''' + quiz('قرّب ٠٫٥٨٧ لأقرب منزلتين عشريتين', [M('٠٫٥٨'), M('٠٫٥٩'), M('٠٫٦'), M('٠٫٥٨٧')], 1, 'الرقم يمين ٨ هو ٧، فنضيف ١: ٠٫٥٩')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('مثال ٣-٦ (ب)')}</div><h2>{Q('2.35', '4')} لأقرب منزلتين عشريتين</h2>
<div class="row vrow">{STEPS(STP('نكتب ٢٫٣٥ على صورة ٢٫٣٥٠ (ثلاث منازل)'), STP('٢ أصغر من ٤', M('٠ ثم الفاصلة', cls='sm')), STP('٢٣ ÷ ٤', M('٥ والباقي ٣', cls='sm')), STP('٣٥ ÷ ٤ ثم ٣٠ ÷ ٤', M('٨ ثم ٧', cls='sm')), STP('الرقم يمين ٨ هو ٧', M('٠٫٥٨٧ ≈ ٠٫٥٩', cls='sm'), 'fin'))}
{VB(vdiv('2.350', '4', reveal=True))}</div>'''))
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('تمرين ٢ (أ، ج)')}</div><h2>معاً: لأقرب منزلتين عشريتين</h2>
<div class="row">{st(f'<button class="flip box col" style="flex:1"><span class="hint">{Q("5.65", "3")}</span><span class="tap">👆</span><span class="hid col vfl">{SOL("5.65", "3", 2)}</span></button>')}{st(f'<button class="flip box col" style="flex:1"><span class="hint">{Q("1.98", "8")}</span><span class="tap">👆</span><span class="hid col vfl">{SOL("1.98", "8", 2)}</span></button>')}</div>'''))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ٢ (د)')}{timer(2)}</div>''' + quiz(f'{Q("0.95", "7")} لأقرب منزلتين عشريتين', [M('٠٫١٣'), M('٠٫١٤'), M('٠٫١٣٥'), M('١٫٣٥')], 1, '٠٫٩٥٠ ÷ ٧ = ٠٫١٣٥ ≈ ٠٫١٤')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ٢ (و)')}</div>''' + quiz(f'{Q("4.3", "3")} لأقرب منزلتين عشريتين', [M('١٫٤٤'), M('١٫٤'), M('١٫٤٣'), M('١٤٫٣')], 2, '٤٫٣٠٠ ÷ ٣ = ١٫٤٣٣ ≈ ١٫٤٣')))
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('تمرين ٣')}</div><h2>تجربة العالِمة: الخليط في ٤ أوانٍ</h2>
{st('<div class="note">١٨٫٤٢ غم و ٥٫٨ غم و ٠٫٧٥ غم</div>')}
<div class="row vrow">{STEPS(STP('نجمع الكتل الثلاث', M('٢٤٫٩٧ غم', cls='sm')), STP('نقسم على ٤', M('٦٫٢٤٢٥', cls='sm')), STP('لأقرب منزلتين', M('٦٫٢٤ غم', cls='sm'), 'fin'))}
{VB(vdiv('24.970', '4', reveal=True))}{FIG('3-6_scientist', 'fig sm')}</div>''' + tn('من الدليل: يجب أن يجد الطلاب ٦٫٢٤٢ أو ٦٫٢٤٢٥ قبل التقريب إلى ٦٫٢٤ غم. مسألةٌ بخطوتين: جمع (درس ٣-٣) ثم قسمة.')))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">نشاط 🧑‍🔬</span>{ref('نشاط دليل المعلم')}</div><h2>الصديق والعالِم</h2>
<div class="row">{st(box('<div class="col"><span class="hint">الصديق 🙂</span><span class="big2">إجابةٌ مقرّبة سهلة الفهم</span></div>', style="flex:1"))}{st(box('<div class="col"><span class="hint">العالِم 🔬</span><span class="big2">إجابةٌ أدقّ بمنازل أكثر</span></div>', style="flex:1"))}</div>
{st('<div class="note">في مجموعاتٍ ثنائية: نحلّ مسائل ورقة المصادر ٣-٦، ونكتب لكل مسألة إجابتين في جدول</div>')}''' + tn('نشاط الدليل بعد إنهاء تمارين ٣-٦، ويحتاج ورقة المصادر ٣-٦ (عشر مسائل). اختم بعرض كل مجموعة نتائجها ومناقشة درجة الدقّة المناسبة.')))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ٢ 🎫</span><h2>لأقرب منزلتين عشريتين</h2>
<div class="exit">{st(f'<div><b>١</b>{Q("7.29", "4")}</div>')}{st(f'<div><b>٢</b>{Q("7.6", "6")}</div>')}{st(f'<div><b>٣</b>{Q("1.9", "7")}</div>')}</div>'''))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ٢ 🎫</span><h2>الإجابات</h2>
<button class="flip box col" style="min-width:40vw"><span class="tap">👆 اضغط لإظهار الإجابات</span><span class="hid col">{M('١٫٨٢', cls="sm")}{M('١٫٢٧', cls="sm")}{M('٠٫٢٧', cls="sm")}</span></button>'''))
S.append(slide('''<span class="qbadge" style="background:#0A6770;box-shadow:0 4px 0 #05393E">الواجب المنزلي 🏠</span><h2>بعد الحصتين</h2>
<div class="exit"><div class="st"><div><b>١</b>صفحة ٥٠ في كتاب النشاط (القسمة والتقريب)</div></div><div class="st"><div><b>٢</b>صفحة ٥١ في كتاب النشاط (مسائل)</div></div></div>'''))
S.append(slide(f'''<h2>الخلاصة</h2>
<div class="sumg">
{st(box('<div class="col"><b class="kk c-exp">أصفار</b><span>نكمل القسمة بعد الفاصلة</span></div>'))}
{st(box('<div class="col"><b class="kk c-we">منزلة زائدة</b><span>نحسب منزلةً أكثر من المطلوب</span></div>'))}
{st(box('<div class="col"><b class="kk c-lcm">نقرّب</b><span>إلى درجة الدقّة المطلوبة</span></div>'))}</div>'''))

# ═══════════ ملحق: تمارين كتاب الطالب ص٦٩ (الإجابات من دليل المعلم ص٧٩) ═══════════
S.append(launch('sb', '٦٩', note=f'المراجع: كتاب الطالب ص٦٨ و ٦٩، ودليل المعلم ص٧٢ وإجاباته ص٧٩ · {ME}'))
H = ['أ', 'ب', 'ج', 'د', 'هـ', 'و', 'ز', 'ح', 'ط']
R1, R2 = 'نحسب منزلتين عشريتين ثم نقرّب إلى منزلة واحدة', 'نحسب ثلاث منازل عشرية ثم نقرّب إلى منزلتين'
def RX(lst, n): return [(f'({h}) {Q(x, k)}', SOL(x, k, n)) for h, (x, k) in zip(H, lst)]
S.append(ex(1, 'لأقرب منزلة عشرية واحدة', R1, RX([('89', '3'), ('92', '7'), ('56', '6'), ('65', '8'), ('879', '7'), ('592', '3'), ('145', '9'), ('275', '3')], 1), cols=2))
S.append(ex(2, 'لأقرب منزلتين عشريتين', R2, RX([('5.65', '3'), ('7.29', '4'), ('1.98', '8'), ('0.95', '7'), ('7.6', '6'), ('4.3', '3'), ('1.9', '7'), ('0.7', '3')], 2), cols=2))
S.append(ex(3, 'تجربة العالِمة', 'نجمع الكتل ثم نقسم على ٤ ونقرّب لمنزلتين', [(FIG('3-6_scientist', 'fig side') + '١٨٫٤٢ غم و ٥٫٨ غم و ٠٫٧٥ غم قُسمت بالتساوي في ٤ أوانٍ: ما كتلة الخليط في كل إناء؟', vdiv('24.970', '4') + '<small>٢٤٫٩٧ ÷ ٤ = ٦٫٢٤٢٥ ≈ ٦٫٢٤ غم</small>')], cols=1))

# ═══════════ ملحق: حلول كتاب النشاط ص٥٠–٥١ (الإجابات من دليل المعلم ص٨٣) ═══════════
S.append(launch('ab', '٥٠ و ٥١', note='الإجابات النهائية من دليل المعلم ص ٨٣ (مع تصحيح التمرينين ٧ و ٨)'))
NA, NB = 'نشاط ص ٥٠ · تمرين', 'نشاط ص ٥١ · تمرين'
S.append(ex(1, 'لأقرب منزلة عشرية واحدة', R1, RX([('33', '2'), ('44', '3'), ('55', '4'), ('66', '9'), ('911', '6'), ('911', '7'), ('911', '8'), ('911', '9'), ('119', '9')], 1), cols=2, src=NA))
S.append(ex(2, 'لأقرب منزلتين عشريتين', R2, RX([('10.98', '10'), ('98.7', '9'), ('8.76', '8'), ('76.5', '7'), ('0.654', '6'), ('5.43', '5'), ('4.32', '4'), ('0.321', '3'), ('2.19', '2')], 2), cols=2, src=NA))
S.append(ex(3, 'مسائل القسمة', 'نحدّد المقسوم والمقسوم عليه، ثم نقرّب كما يطلب السؤال', [
  ('(٣) ١٥٫٦ م قُطعت ٨ قطعٍ متساوية: ما طول القطعة؟', vdiv('15.60', '8') + '<small>١٫٩٥ م</small>'),
  ('(٤) ٢٫٦ كغم في ٦ حاويات (لمنزلتين): ما كتلة كل حاوية؟', SOL('2.6', '6', 2) + '<small>كغم</small>')], cols=1, src=NA))
S.append(ex(5, 'طيّ الورق', 'نقسم ثم نقرّب لمنزلتين', [
  (FIG('3-6_a4', 'fig side') + 'طول ورقة A4 ٢٩٫٧ سم طُويت أربعة أرباع: ما طول الربع؟', vdiv('29.700', '4') + '<small>٧٫٤٢٥ ≈ ٧٫٤٣ سم</small>')], cols=1, src=NB))
S.append(ex(6, 'طيّ الورق', 'نقسم ثم نقرّب لمنزلة واحدة', [
  (FIG('3-6_strip', 'fig side') + 'عرض ١٤٫٨ سم طُوي سبعة أقسام: ما عرض القسم؟', SOL('14.8', '7', 1) + '<small>سم</small>')], cols=1, src=NB))
S.append(ex(7, 'مسائل من خطوتين', 'نجمع أولاً ثم نقسم', [
  ('(٧) ١٢٫٢٥٠ و ٢٠٫٤٩٠ و ١٨٫١٨٠ ريالاً قُسمت على ٤ أصدقاء: كم دفع كلٌّ منهم؟', '٥٠٫٩٢٠ ÷ ٤ = ١٢٫٧٣٠ ريالاً<small>الدليل كتب ١٦٫٩٧٣ (قسم على ٣)</small>'),
  ('(٨) ٢٫٧ و ٣٫٥ و ١٫٢٥ و ٠٫٢٧٥ كغم لست حاويات (لمنزلتين): ما كتلة الحاوية؟', '٧٫٧٢٥ ÷ ٦ ≈ ١٫٢٩ كغم<small>الدليل كتب ٢٫٣٤ (كأنها ٧٫٢ و ٥٫٣)</small>')], cols=1, src=NB,
  note='في إجابات الدليل ص ٨٣ خطآن: التمرين ٧ قُسم على ٣ بدل ٤ أصدقاء، والتمرين ٨ يوافق ٧٫٢ و ٥٫٣ كغم لا ٢٫٧ و ٣٫٥ المطبوعتين في كتاب النشاط.'))

EXTRA_CSS_OWN = '''
.stps{display:flex;flex-direction:column;gap:1.1vh;align-items:stretch}
.stp{display:flex;align-items:center;gap:1.4vw;justify-content:space-between}
.stp .lab{flex:0 1 auto;max-width:70%;font-family:var(--fh);font-weight:800;color:#2563EB;background:#EAF1FF;border-radius:12px;padding:.2em .8em;text-align:center;line-height:1.4;font-size:clamp(20px,3.5vh,40px)}
.stp.fin .lab{background:var(--good);color:#fff}
.slide .vrow{align-items:center;justify-content:center;gap:2vh 3vw;flex-wrap:wrap}
.slide .vrow>.stps{flex:0 1 auto;max-width:min(1000px,62vw)}
@media (max-aspect-ratio:1/1){.slide .vrow{flex-direction:column}.slide .vrow>.stps{max-width:92vw}}
.vbox{flex:none;background:#fff;border:3px solid var(--line);border-radius:18px;padding:1vh 2vw;font-family:var(--fh);font-size:clamp(44px,8.8vh,100px)}
.hid.vfl{font-family:var(--fh);font-size:clamp(34px,6.4vh,74px)}
.hid.vfl small{font-size:.6em;color:var(--good)}
.box .col>.m:not(.mid):not(.sm):not(.big),.hid.col>.m:not(.mid):not(.sm):not(.big){font-size:clamp(32px,6vh,70px)}
.big2{font-weight:700;font-size:clamp(24px,4.4vh,50px);line-height:1.4}
.hint.no{color:var(--bad)}.hint.ok{color:var(--good)}
.defs{display:flex;flex-direction:column;gap:1.6vh;width:min(1400px,92vw)}
.defs .st>div{display:flex;align-items:center;gap:1.6vw;background:#fff;border:3px solid var(--line);border-radius:18px;padding:1.2vh 1.6vw}
.defs .kk{flex:none;font-size:clamp(36px,6.8vh,80px)}.defs span{font-weight:700;font-size:clamp(26px,4.8vh,56px);line-height:1.45}
.sumg{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:2vw;width:min(1600px,94vw)}
.sumg .col span{font-weight:700;font-size:clamp(26px,4.6vh,56px);line-height:1.4}
.sumg .kk{font-size:clamp(30px,5.6vh,66px)}
.xa .vcol{font-family:var(--fh);font-size:1.05em;margin:0 .3em;color:var(--ink)}
.xa small{display:block}
'''+FIG_CSS
