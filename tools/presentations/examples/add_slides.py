# شرائح درس ٣-٣ «جمع الأعداد العشرية والكسور العشرية وطرحها» — الصف السابع (حصتان، كتاب الطالب ص٦٢–٦٣)
# المراجع: دليل المعلم ص٦٧–٦٨ (الصورة الرأسية والفواصل على خطٍّ واحد، إضافة الأصفار في الطرح، التحقّق بالتقدير؛
# الأخطاء الشائعة: عدم محاذاة الفواصل، نسيان الأصفار؛ النشاطان: ورقة المصادر ٣-٣ ولعبة النرد)،
# كتاب الطالب ص٦٢–٦٣ (مثال ٣-٣)، وإجابات الدليل ص٧٨ (كتاب الطالب) وص٨٢ (كتاب النشاط ص٤٥–٤٦).
# python3.12 gen_powers.py add_slides.py جمع_الأعداد_العشرية_وطرحها_عرض_تفاعلي.html "جمع الأعداد العشرية وطرحها — الصف السابع"
exec(open(os.path.join(HERE, 'vcol.py'), encoding='utf-8').read())
exec(open(os.path.join(HERE, 'figs.py'), encoding='utf-8').read())

def STP(lab, expr='', cls=''): return st(f'<div class="stp {cls}"><span class="lab">{lab}</span>{expr}</div>')
def STEPS(*rows): return '<div class="stps">' + ''.join(rows) + '</div>'
def Q(x, op, y): return f'{_ar(x)} {"+" if op == "+" else "−"} {_ar(y)}'           # العملية أفقياً كما في الكتاب
def WRONG(*rows):   # عمليةٌ رأسية خاطئة: الأرقام محاذاةٌ إلى اليمين دون الفواصل
    TD = 'padding: 0 .1em; text-align: right'
    tr = ''.join(f'<tr><td style="{TD}{"; border-top: .07em solid currentColor; color: #C0262D" if o == "=" else ""}">{t}</td><td style="{TD}; color: #C2410C">{o if o != "=" else ""}</td></tr>' for t, o in rows)
    return f'<table class="vcol" style="border-collapse: collapse; direction: ltr; display: inline-table; font-weight: 800; line-height: 1.12; margin: 0 auto">{tr}</table>'
def VB(*p, **k): return f'<div class="vbox">{vcol(*p, **k)}</div>'
S = []
ME = 'إعداد: أ. عيسى الحارثي'
S.append(slide(f'''<span class="tag">الصف السابع · الدرس ٣-٣</span>
<h1 class="h1s">جمع الأعداد العشرية والكسور العشرية وطرحها</h1>
<p class="lead">كتاب الطالب ص ٦٢ و ٦٣ · حصتان</p>
<p class="lead" style="font-size:clamp(26px,4.8vh,56px)">{ME}</p>''', 'cover'))
CAN = ['أكتب عملية الجمع أو الطرح <b>بالصورة الرأسية</b> والفواصل العشرية على خطٍّ واحد', 'أجمع الأعداد العشرية مع <b>الحمل</b>', 'أطرح الأعداد العشرية مع <b>إضافة الأصفار</b> والاستلاف، وأتحقّق بالتقدير']
S.append(slide(f'''<h2>في نهاية هذا الدرس…</h2>
<div class="can">{''.join(f'<div><span class="can-i">✔</span><span><b>أنا أستطيع</b> أن {t}</span></div>' for t in CAN)}</div>'''))
S.append(slide(f'''<h2>مفردات الدرس</h2>
{st('<div class="vocab wide"><div><span>الفاصلة العشرية</span><i>decimal point</i></div><div><span>الصورة الرأسية</span><i>column method</i></div><div><span>الحمل</span><i>carry</i></div><div><span>الاستلاف</span><i>borrow</i></div></div>')}
<p class="lead">حصتان: <b class="c-i">أنا</b> ← <b class="c-we">نحن</b> ← <b class="c-u">أنتم</b></p>'''))

# ═══════════ الحصة الأولى: الجمع ═══════════
S.append(slide('''<span class="tag">الحصة الأولى · ٤٠ دقيقة</span><h2>جمع الأعداد العشرية</h2>
<div class="plan"><div><b>٤ د</b>تهيئة</div><div><b>٦ د</b>القاعدة</div><div><b>٨ د</b>مثال ٣-٣ (أ)</div>
<div><b>٧ د</b>نحن</div><div><b>٨ د</b>أنتم</div><div><b>٤ د</b>انتبه</div><div><b>٣ د</b>بطاقة الخروج</div></div>''', 'divider'))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">تهيئة 🤔</span></div><h2>قلمٌ بسعر ٠٫٧٥ ر.ع ودفترٌ بسعر ١٫٥ ر.ع</h2>
<div class="figrow"><div class="tag"><span>✏️</span><b>٠٫٧٥ ر.ع</b></div><span class="plus">+</span><div class="tag"><span>📒</span><b>١٫٥ ر.ع</b></div></div>
{st('<div class="note">كم ندفع ثمناً للقلم والدفتر معاً؟ قدّر أولاً ثم احسب</div>')}
{st('<div class="note">التقدير: ١ + ١٫٥ ≈ ٢٫٥ ر.ع، والدقيق ٢٫٢٥ ر.ع: نجمع الأجزاء من مئة مع الأجزاء من مئة، والأجزاء من عشرة مع الأجزاء من عشرة</div>')}''' + tn('من خارج المرجع: تهيئة بالنقود. اترك الطلاب يقترحون، وتوقّع الإجابة الخاطئة ٠٫٩٠ (من جمع ٧٥ و ١٥) لتمهّد لمحاذاة الفواصل.')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('كتاب الطالب ص ٦٢')}</div><h2>عند جمع الأعداد العشرية وطرحها</h2>
<div class="defs">{st('<div><b class="kk c-exp">١</b><span>نكتب العملية <b class="c-exp">بالصورة الرأسية</b></span></div>')}{st('<div><b class="kk c-we">٢</b><span>نضع <b class="c-we">الفواصل العشرية على خطٍّ واحد</b>، فتقع كل منزلةٍ تحت مثيلتها</span></div>')}{st('<div><b class="kk c-lcm">٣</b><span>نكمل المنازل الفارغة <b>بالأصفار</b>، ثم نجمع أو نطرح من اليمين كالأعداد الكاملة</span></div>')}</div>''' + tn('من الدليل: الأفضل وضع العملية رأسياً وتذكّر الفواصل على خطٍّ واحد. الصفر المضاف لا يغيّر قيمة العدد: ١٤٫٧ = ١٤٫٧٠.')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('مثال ٣-٣ (أ)')}</div><h2>أوجد ناتج {Q('14.7', '+', '8.56')}</h2>
<div class="row vrow">{STEPS(STP('الأجزاء من مئة', M('٠', '+', '٦', EQ, '٦', cls='sm')), STP('الأجزاء من عشرة', M('٧', '+', '٥', EQ, '١٢', cls='sm')), STP('نكتب ٢ ونحمل ١ إلى الآحاد'), STP('الآحاد', M('٤', '+', '٨', '+', '١', EQ, '١٣', cls='sm')), STP('العشرات', M('١', '+', '١', EQ, '٢', cls='sm')))}
{VB('14.7', '8.56', '+', reveal=True)}</div>''' + tn('الصفر الأزرق: الفراغ يمين الرقم ٧ يعني صفراً (من الكتاب). تحقّق بالتقدير (نقطة الدليل): ١٥ + ٩ = ٢٤، والناتج ٢٣٫٢٦ قريبٌ منه.')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('دليل المعلم ص ٦٧')}</div><h2>نتحقّق بالتقدير</h2>
<div class="row">{st(box(f'<div class="col"><span class="hint">نقرّب كل عدد إلى أقرب عدد كامل</span>{M("١٥", "+", "٩", EQ, "٢٤")}</div>', style="flex:1"))}{st(box(f'<div class="col"><span class="hint">الناتج الدقيق</span>{M("٢٣٫٢٦")}</div>', style="flex:1"))}</div>
{st('<div class="note">الناتج قريبٌ من التقدير، فالفاصلة في مكانها الصحيح</div>')}'''))
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('تمرين ١ (أ، ج)')}</div><h2>معاً: أوجد الناتج</h2>
<div class="row">{st(f'<button class="flip box col" style="flex:1"><span class="hint">{Q("8.35", "+", "6.24")}</span><span class="tap">👆</span><span class="hid vfl">{vcol("8.35", "6.24", "+")}</span></button>')}{st(f'<button class="flip box col" style="flex:1"><span class="hint">{Q("8.43", "+", "4.78")}</span><span class="tap">👆</span><span class="hid vfl">{vcol("8.43", "4.78", "+")}</span></button>')}</div>''' + tn('اطلب من طالبين الحل على السبورة بالصورة الرأسية قبل قلب البطاقة.')))
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('تمرين ١ (هـ)')}</div><h2>معاً: {Q('23.3', '+', '5.42')}</h2>
<div class="row vrow">{STEPS(STP('نكتب ٢٣٫٣ على صورة ٢٣٫٣٠'), STP('نجمع كل منزلة مع مثيلتها'), STP('الناتج', M('٢٨٫٧٢', cls='sm'), 'fin'))}
{VB('23.3', '5.42', '+', reveal=True)}</div>'''))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ١ (ط)')}{timer(2)}</div>''' + quiz(f'أوجد ناتج {Q("7.8", "+", "0.48")}', [M('١٫٢٦'), M('٨٫٢٨'), M('٧٫١٢٨'), M('٨٫٢٠')], 1, '٧٫٨٠ + ٠٫٤٨ = ٨٫٢٨ (الفواصل على خطٍّ واحد)')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ١ (ل)')}</div>''' + quiz(f'أوجد ناتج {Q("12.376", "+", "7.8")}', [M('١٣٫١٥٦'), M('١٩٫١٧٦'), M('٢٠٫١٧٦'), M('٢٠٫٩٥٦')], 2, '١٢٫٣٧٦ + ٧٫٨٠٠ = ٢٠٫١٧٦')))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">انتبه ⚠️ خطأ شائع</span>{ref('دليل المعلم ص ٦٧')}</div><h2>الفواصل العشرية على خطٍّ واحد</h2>
<div class="row">{st(box(f'<div class="col"><span class="hint no">✘ الأرقام على اليمين</span>{WRONG(("٧٫٨", ""), ("٠٫٤٨", "+"), ("١٫٢٦", "="))}</div>', style="flex:1"))}{st(box(f'<div class="col"><span class="hint ok">✔ الفواصل على خطٍّ واحد</span>{vcol("7.8", "0.48", "+")}</div>', style="flex:1"))}</div>''' + tn('الخطأ الشائع في الدليل: عدم وضع الفواصل على خطٍّ واحد. اسأل: «٧٫٨ + ٠٫٤٨ تقريباً ٨، فهل يُعقل أن يكون الناتج ١٫٢٦؟»')))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ١ 🎫</span><h2>أوجد الناتج</h2>
<div class="exit">{st(f'<div><b>١</b>{Q("11.42", "+", "25.39")}</div>')}{st(f'<div><b>٢</b>{Q("16.77", "+", "9.5")}</div>')}{st(f'<div><b>٣</b>{Q("67.043", "+", "5.672")}</div>')}</div>'''))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ١ 🎫</span><h2>الإجابات</h2>
<button class="flip box col" style="min-width:40vw"><span class="tap">👆 اضغط لإظهار الإجابات</span><span class="hid col">{M('٣٦٫٨١', cls="sm")}{M('٢٦٫٢٧', cls="sm")}{M('٧٢٫٧١٥', cls="sm")}</span></button>'''))

# ═══════════ الحصة الثانية: الطرح ═══════════
S.append(slide('''<span class="tag">الحصة الثانية · ٤٠ دقيقة</span><h2>طرح الأعداد العشرية</h2>
<div class="plan"><div><b>٣ د</b>إحماء</div><div><b>٨ د</b>مثال ٣-٣ (ب)</div><div><b>٦ د</b>الطرح من عددٍ كامل</div>
<div><b>٥ د</b>نحن</div><div><b>٥ د</b>أنتم</div><div><b>٤ د</b>المئذنة</div><div><b>٥ د</b>رمي الرمح</div><div><b>٤ د</b>بطاقة الخروج</div></div>''', 'divider'))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">إحماء 🔥</span>{timer(1)}</div>''' + quiz(f'أوجد ناتج {Q("8.72", "+", "14.9")}', [M('٢٣٫٦٢'), M('٢٢٫٦٢'), M('١٦٫١٨'), M('٢٣٫٥٢')], 0, '١٤٫٩٠ + ٨٫٧٢ = ٢٣٫٦٢')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('مثال ٣-٣ (ب)')}</div><h2>أوجد ناتج {Q('13.5', '-', '1.72')}</h2>
<div class="row vrow">{STEPS(STP('نكتب ١٣٫٥ على صورة ١٣٫٥٠'), STP('الأجزاء من مئة: ٠ − ٢ لا يمكن، نستلف من ٥', M('١٠', '−', '٢', EQ, '٨', cls='sm')), STP('الأجزاء من عشرة: ٤ − ٧ لا يمكن، نستلف من ٣', M('١٤', '−', '٧', EQ, '٧', cls='sm')), STP('الآحاد ثم العشرات', M('٢', '−', '١', EQ, '١', cls='sm')))}
{VB('13.5', '1.72', '-', reveal=True)}</div>''' + tn('الأرقام البرتقالية فوق العدد هي قيم الأرقام بعد الاستلاف (كما في الكتاب): ٥ أصبحت ٤ ثم ١٤، و ٣ أصبحت ٢. تحقّق: ١٤ − ٢ = ١٢، والناتج ١١٫٧٨ قريبٌ منه.')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('تمرين ٣: طريقة هيثم')}</div><h2>الطرح من عددٍ كامل: {Q('35', '-', '4.47')}</h2>
<div class="row vrow">{STEPS(STP('نكتب ٣٥ على صورة ٣٥٫٠٠'), STP('نستلف من ٥: يصبح ٤، والصفران ٩ و ١٠'), STP('نطرح كل منزلة', M('٣٠٫٥٣', cls='sm'), 'fin'))}
{VB('35', '4.47', '-', reveal=True)}{FIG('3-3_haitham', 'fig sm')}</div>''' + tn('من الكتاب (ورقة هيثم) ومن الدليل: «يجب أن يضيف الطلاب أصفاراً في عملية الطرح».')))
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('تمرين ٢ (ج)، تمرين ٣ (أ)')}</div><h2>معاً: أوجد الناتج</h2>
<div class="row">{st(f'<button class="flip box col" style="flex:1"><span class="hint">{Q("13.73", "-", "2.44")}</span><span class="tap">👆</span><span class="hid vfl">{vcol("13.73", "2.44", "-")}</span></button>')}{st(f'<button class="flip box col" style="flex:1"><span class="hint">{Q("23", "-", "2.65")}</span><span class="tap">👆</span><span class="hid vfl">{vcol("23", "2.65", "-")}</span></button>')}</div>'''))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ٢ (ي)')}{timer(2)}</div>''' + quiz(f'أوجد ناتج {Q("11.8", "-", "4.36")}', [M('٧٫٥٦'), M('٧٫٤٤'), M('٨٫٤٤'), M('٧٫٥٤')], 1, '١١٫٨٠ − ٤٫٣٦ = ٧٫٤٤')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ٣ (هـ)')}</div>''' + quiz(f'أوجد ناتج {Q("16", "-", "0.76")}', [M('١٦٫٧٦'), M('١٥٫٣٤'), M('١٥٫٢٤'), M('٠٫٦٠')], 2, '١٦٫٠٠ − ٠٫٧٦ = ١٥٫٢٤')))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">انتبه ⚠️ خطأ شائع</span>{ref('دليل المعلم ص ٦٧')}</div><h2>لا ننسى الأصفار</h2>
<div class="errs">{''.join(st(f'<button class="flip err"><span class="xq">{q}</span><span class="tap">👆</span><span class="hid xa no">{w}</span></button>') for q, w in (
  ('٣٥ − ٤٫٤٧ = ٣١٫٤٧', '✘ أنزلنا ٤٧ دون طرح: نكتب ٣٥٫٠٠ فالناتج ٣٠٫٥٣'), ('١١٫٨ − ٤٫٣٦ = ٧٫٥٦', '✘ طرحنا ٠ من ٦: نستلف فالناتج ٧٫٤٤')))}</div>''' + tn('الخطأ الشائع في الدليل: نسيان إضافة الأصفار. الخطأ الثاني من خارج المرجع (طرح الرقم الأصغر من الأكبر في المنزلة).')))
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('تمرين ٤')}</div><h2>جامع السلطان قابوس الأكبر</h2>
<div class="row vrow">{STEPS(STP('المئذنة الرئيسية', M('٩١٫٣ م', cls='sm')), STP('كل مئذنة جانبية', M('٤٥٫٥ م', cls='sm')), STP('ترتفع الرئيسية عن الأخرى بـ', M('٤٥٫٨ م', cls='sm'), 'fin'))}
{VB('91.3', '45.5', '-', reveal=True)}{FIG('3-3_mosque')}</div>''' + tn('من الدليل: قد يجمع بعض الطلاب التواريخ (١٩٩٢ و ٢٠٠١)، فاطلب منهم قراءة السؤال بعناية: المطلوب الفرق بين الارتفاعين.')))
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('تمرين ٥')}</div><h2>رمي الرمح: هل الفرق الأول أكبر؟</h2>
<div class="row vrow">{FIG('3-3_javelin', 'fig sm')}{st(box(f'<div class="col"><span class="hint">الأول − الثاني</span>{vcol("70.20", "67.51", "-")}</div>', style="flex:1"))}{st(box(f'<div class="col"><span class="hint">الثاني − الثالث</span>{vcol("67.51", "64.84", "-")}</div>', style="flex:1"))}</div>
{st(f'<div class="note">٢٫٦٩ &gt; ٢٫٦٧: نعم، الفرق الأول أكبر</div>')}''' + tn('المسافات: الأول ٧٠٫٢٠ م، الثاني ٦٧٫٥١ م، الثالث ٦٤٫٨٤ م. عمليتا طرح ثم مقارنة (من الدليل).')))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ٢ 🎫</span><h2>أوجد الناتج</h2>
<div class="exit">{st(f'<div><b>١</b>{Q("4.72", "-", "2.51")}</div>')}{st(f'<div><b>٢</b>{Q("48.65", "-", "12.78")}</div>')}{st(f'<div><b>٣</b>{Q("245", "-", "22.49")}</div>')}</div>'''))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ٢ 🎫</span><h2>الإجابات</h2>
<button class="flip box col" style="min-width:40vw"><span class="tap">👆 اضغط لإظهار الإجابات</span><span class="hid col">{M('٢٫٢١', cls="sm")}{M('٣٥٫٨٧', cls="sm")}{M('٢٢٢٫٥١', cls="sm")}</span></button>'''))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">نشاط 🎲</span>{ref('نشاط دليل المعلم')}</div><h2>لعبة النرد: أكبر ناتج طرح</h2>
<div class="exit">{st('<div><b>١</b>نرمي النرد ونكتب الرقم في أحد مربّعات العملية ☐☐☐٫☐ − ☐☐٫☐☐</div>')}{st('<div><b>٢</b>بعد ملء المربّعات نحسب الناتج، والفائز صاحب أكبر ناتج</div>')}</div>''' + tn('نشاط ٢ في الدليل (اختياري إن بقي وقت، أو بديلٌ عن تمرين ٥). وفي النشاط ١ ورقة المصادر ٣-٣ وإجاباتها في الدليل ص ٦٨.')))
S.append(slide('''<span class="qbadge" style="background:#0A6770;box-shadow:0 4px 0 #05393E">الواجب المنزلي 🏠</span><h2>بعد الحصتين</h2>
<div class="exit"><div class="st"><div><b>١</b>صفحة ٤٥ في كتاب النشاط (الجمع والطرح)</div></div><div class="st"><div><b>٢</b>صفحة ٤٦ في كتاب النشاط (الطرح من عددٍ كامل، ومسألتان)</div></div></div>'''))
S.append(slide(f'''<h2>الخلاصة</h2>
<div class="sumg">
{st(box('<div class="col"><b class="kk c-exp">رأسياً</b><span>الفواصل على خطٍّ واحد</span></div>'))}
{st(box('<div class="col"><b class="kk c-we">أصفار</b><span>نكمل المنازل الفارغة</span></div>'))}
{st(box('<div class="col"><b class="kk c-lcm">التقدير</b><span>نتحقّق من معقولية الناتج</span></div>'))}</div>'''))

# ═══════════ ملحق: تمارين كتاب الطالب ص٦٢–٦٣ (الإجابات من دليل المعلم ص٧٨) ═══════════
S.append(launch('sb', '٦٢ و ٦٣', note=f'المراجع: كتاب الطالب ص٦٢ و ٦٣، ودليل المعلم ص٦٧ و ٦٨ وإجاباته ص٧٨ · {ME}'))
H = ['أ', 'ب', 'ج', 'د', 'هـ', 'و', 'ز', 'ح', 'ط', 'ي', 'ك', 'ل']
def EX(lst, op): return [(f'({h}) {Q(x, op, y)}', vcol(x, y, op)) for h, (x, y) in zip(H, lst)]
RA, RS = 'الفواصل العشرية على خطٍّ واحد، ثم نجمع من اليمين', 'نكمل المنازل بالأصفار، ثم نطرح من اليمين ونستلف عند الحاجة'
B1 = [('6.24', '8.35'), ('11.42', '25.39'), ('4.78', '8.43'), ('19.45', '9.83'), ('23.3', '5.42'), ('16.77', '9.5'), ('8.72', '14.9'), ('123.8', '9.37'), ('0.48', '7.8'), ('67.043', '5.672'), ('9.95', '0.478'), ('12.376', '7.8')]
S.append(ex(1, 'أوجد ناتج الجمع', RA, EX(B1, '+'), cols=2))
B2 = [('4.72', '2.51'), ('23.78', '9.35'), ('13.73', '2.44'), ('19.38', '6.65'), ('48.65', '12.78'), ('32.27', '1.49'), ('82.77', '25.93'), ('45.42', '7.35'), ('74.9', '3.67'), ('11.8', '4.36'), ('34.9', '8.77'), ('1.75', '0.688')]
S.append(ex(2, 'أوجد ناتج الطرح', RS, EX(B2, '-'), cols=2))
B3 = [('23', '2.65'), ('46', '1.76'), ('87', '13.45'), ('245', '22.49'), ('16', '0.76'), ('42', '4.66'), ('58', '9.06'), ('235', '18.18')]
S.append(ex(3, 'أوجد ناتج الطرح بطريقة هيثم', 'نكتب العدد الكامل بفاصلةٍ وأصفار: ٢٣ = ٢٣٫٠٠', EX(B3, '-'), cols=2))
S.append(ex(4, 'جامع السلطان قابوس الأكبر', 'المطلوب الفرق بين الارتفاعين (لا نجمع التواريخ)', [(FIG('3-3_mosque') + 'المئذنة الرئيسية ٩١٫٣ م، والجانبية ٤٥٫٥ م: بكم ترتفع الرئيسية عن الأخرى؟', vcol('91.3', '45.5', '-') + '<small>ترتفع ٤٥٫٨ م</small>')], cols=1))
S.append(ex(5, 'رمي الرمح', 'عمليتا طرح ثم نقارن', [(FIG('3-3_javelin') + 'الفرق بين الأول والثاني', vcol('70.20', '67.51', '-')), (FIG('3-3_javelin') + 'الفرق بين الثاني والثالث', vcol('67.51', '64.84', '-') + '<small>٢٫٦٩ &gt; ٢٫٦٧: نعم، الفرق الأول أكبر</small>')], cols=2))

# ═══════════ ملحق: حلول كتاب النشاط ص٤٥–٤٦ (الإجابات من دليل المعلم ص٨٢) ═══════════
S.append(launch('ab', '٤٥ و ٤٦', note='الإجابات النهائية من دليل المعلم ص ٨٢'))
NA, NB = 'نشاط ص ٤٥ · تمرين', 'نشاط ص ٤٦ · تمرين'
A1 = [('7.36', '7.36'), ('38.38', '27.27'), ('4.78', '8.74'), ('18.96', '2.14'), ('0.77', '5.38'), ('76.767', '9.5'), ('32.22', '0.977'), ('13.809', '8.37')]
S.append(ex(1, 'أوجد ناتج الجمع', RA, EX(A1, '+'), cols=2, src=NA))
A2 = [('7.45', '4.33'), ('27.58', '8.36'), ('44.73', '3.55'), ('21.66', '6.67'), ('8.75', '2.85'), ('45.6', '5.49'), ('57.37', '45.6'), ('12.42', '8.765')]
S.append(ex(2, 'أوجد ناتج الطرح', RS, EX(A2, '-'), cols=2, src=NA))
A3 = [('36', '4.3'), ('43', '8.3'), ('58', '9.55'), ('106', '68.22')]
S.append(ex(3, 'أوجد ناتج الطرح', 'نكتب العدد الكامل بفاصلةٍ وأصفار', EX(A3, '-'), cols=2, src=NB))
S.append(ex(4, 'طول البرج', 'نجمع الأطوال الثلاثة والفواصل على خطٍّ واحد', [(FIG('3-3_tower', 'fig side') + 'الأساس ١٩٫٨١ م، والقاعدة ٢٧٫١٣ م، والسارية ٤٦٫٣ م: ما طول البرج؟', '<span class="vr2">' + vcol('19.81', '27.13', '+') + vcol('46.94', '46.3', '+') + '</span><small>طول البرج ٩٣٫٢٤ م</small>')], cols=1, src=NB))
S.append(ex(5, 'الوثب العالي', 'عمليتا طرح ثم نقارن', [(FIG('3-3_highjump') + 'الفرق بين ١٩٦٠ و ١٩٣٠', vcol('1.86', '1.605', '-')), (FIG('3-3_highjump') + 'الفرق بين ١٩٩٠ و ١٩٦٠', vcol('2.09', '1.86', '-') + '<small>٠٫٢٥٥ &gt; ٠٫٢٣: نعم، الفرق الأول أكبر</small>')], cols=2, src=NB))

EXTRA_CSS_OWN = '''
.stps{display:flex;flex-direction:column;gap:1.2vh;align-items:stretch}
.stp{display:flex;align-items:center;gap:1.4vw;justify-content:space-between}
.stp .lab{flex:0 1 auto;max-width:70%;font-family:var(--fh);font-weight:800;color:#2563EB;background:#EAF1FF;border-radius:12px;padding:.2em .8em;text-align:center;line-height:1.4;font-size:clamp(20px,3.6vh,40px)}
.stp.fin .lab{background:var(--good);color:#fff}
.slide .vrow{align-items:center;justify-content:center;gap:2vh 3vw;flex-wrap:wrap}
.slide .vrow>.stps{flex:0 1 auto;max-width:min(900px,60vw)}
@media (max-aspect-ratio:1/1){.slide .vrow{flex-direction:column}.slide .vrow>.stps{max-width:92vw}}
.vbox{flex:none;background:#fff;border:3px solid var(--line);border-radius:18px;padding:1vh 2vw;font-family:var(--fh);font-size:clamp(48px,9.6vh,110px)}
.slide .vrow .box .vcol{font-size:clamp(36px,6.6vh,78px)}
.hid.vfl{font-family:var(--fh);font-size:clamp(36px,6.8vh,80px)}
.box .col>.m:not(.mid):not(.sm):not(.big),.hid.col>.m:not(.mid):not(.sm):not(.big){font-size:clamp(34px,6.4vh,76px)}
.box .col .vcol{font-family:var(--fh);font-size:clamp(34px,6.2vh,72px)}
.hint.no{color:var(--bad)}.hint.ok{color:var(--good)}
.defs{display:flex;flex-direction:column;gap:1.6vh;width:min(1400px,92vw)}
.defs .st>div{display:flex;align-items:center;gap:1.6vw;background:#fff;border:3px solid var(--line);border-radius:18px;padding:1.2vh 1.6vw}
.defs .kk{flex:none;font-size:clamp(36px,6.8vh,80px)}.defs span{font-weight:700;font-size:clamp(26px,4.8vh,56px);line-height:1.45}
.errs{display:flex;flex-direction:column;gap:1.4vh;width:min(1400px,92vw)}
.errs .err{display:flex;flex-direction:column;align-items:center;gap:.6vh;background:#fff;border:3px solid var(--line);border-radius:16px;padding:.8vh 1.6vw;font-size:clamp(26px,5vh,58px);font-weight:700}
.errs .err .xq{font-size:inherit}.errs .err .xa{font-size:clamp(24px,4.4vh,50px)}
.sumg{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:2vw;width:min(1600px,94vw)}
.sumg .col span{font-weight:700;font-size:clamp(26px,4.6vh,56px);line-height:1.4}
.sumg .kk{font-size:clamp(34px,6.4vh,76px)}
.xa .vcol{font-family:var(--fh);font-size:1.1em;margin:0 .3em;color:var(--ink)}
.xa small{display:block}
.vr2{display:flex;gap:3vw;justify-content:center;align-items:center}
.tag{display:flex;flex-direction:column;align-items:center;background:#FFF6E3;border:3px solid #E9A23B;border-radius:18px 18px 18px 4px;padding:1vh 2vw;font-family:var(--fh)}
.tag span{font-size:clamp(40px,8vh,90px)}.tag b{font-size:clamp(26px,5vh,58px)}.tag.q{background:#EAF1FF;border-color:#2563EB}
.plus{font-family:var(--fh);font-weight:900;font-size:clamp(40px,8vh,90px);color:#C2410C}
'''+FIG_CSS

# صفحات تمارين كتاب الطالب لشارة «كتاب الطالب ص … · تمرين …» (common_slides.py)
PG = {'تمرين': [(1, '٦٢'), (2, '٦٣')]}
