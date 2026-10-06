# شرائح درس ٤-١ «التعرّف على وحدات القياس» — الصف السابع (حصة واحدة، كتاب الطالب ص٨٠–٨٣)
# المراجع: دليل المعلم ص٨٦–٨٧ (المفردات، نقاط التعلّم، الأخطاء الشائعة: الخلط بين الوحدة الأكبر والأصغر والخطأ في معامل التحويل؛
# النشاط: الطن و٥٠٠٠٠٠ غم، و٢ كم و٥٠٠٠٠٠ سم؛ تعليقات التمارين ٧–٩)، كتاب الطالب ص٨٠–٨٣ (مثال ٤-١)،
# وإجابات الدليل ص٩٠ (كتاب الطالب) وص٩٢ (كتاب النشاط ص٥٨–٦٠).
# python3.12 gen_powers.py meas_slides.py التعرف_على_وحدات_القياس_عرض_تفاعلي.html "التعرّف على وحدات القياس — الصف السابع"
exec(open(os.path.join(HERE, 'vcol.py'), encoding='utf-8').read())
exec(open(os.path.join(HERE, 'figs.py'), encoding='utf-8').read())

DV = '<span class="x">÷</span>'
TR = str.maketrans('0123456789.', '٠١٢٣٤٥٦٧٨٩٫')
def D(x): return str(x).translate(TR)
def STP(lab, expr='', cls=''): return st(f'<div class="stp {cls}"><span class="lab">{lab}</span>{expr}</div>')
def STEPS(*rows): return '<div class="stps">' + ''.join(rows) + '</div>'
def U(*items): return '<div class="units">' + ''.join(f'<div><b>{u}</b><span>{n}</span><i>{e}</i></div>' for u, n, e in items) + '</div>'
LEN = (['كم', 'م', 'سم', 'ملم'], [1000, 100, 10], ['كيلومتر', 'متر', 'سنتيمتر', 'مليمتر'])
MAS = (['طن', 'كغم', 'غم'], [1000, 1000], ['طن', 'كيلوغرام', 'غرام'])
CAP = (['لتر', 'مل'], [1000], ['لتر', 'مليلتر'])
S = []
ME = 'إعداد: أ. عيسى الحارثي'
S.append(slide(f'''<span class="tag">الصف السابع · الدرس ٤-١</span>
<h1 class="h1s">التعرّف على وحدات القياس</h1>
<p class="lead">كتاب الطالب ص ٨٠ إلى ٨٣ · حصة واحدة</p>
<p class="lead" style="font-size:clamp(26px,4.8vh,56px)">{ME}</p>''', 'cover'))
CAN = ['أسمّي وحدات <b>الطول والكتلة والسعة</b> وأدوات قياسها', '<b>أحوّل</b> من وحدةٍ إلى أخرى بالضرب أو القسمة على معامل التحويل', '<b>أرتّب</b> قياساتٍ بعد كتابتها بالوحدة نفسها']
S.append(slide(f'''<h2>في نهاية هذا الدرس…</h2>
<div class="can">{''.join(f'<div><span class="can-i">✔</span><span><b>أنا أستطيع</b> أن {t}</span></div>' for t in CAN)}</div>'''))
S.append(slide(f'''<h2>مفردات الدرس</h2>
<div class="voc3">{st('<div><b>الطول</b><i>length</i><span>المسافة بين طرفين أو نقطتين</span></div>')}{st('<div><b>الكتلة</b><i>mass</i><span>مقدار ما في الجسم من مادة</span></div>')}{st('<div><b>السعة</b><i>capacity</i><span>مقدار ما يتّسع له الوعاء من سائل</span></div>')}</div>
{st('<p class="lead"><b>الوحدات المترية</b> (metric units): نحوّل بينها بالضرب أو القسمة على ١٠ أو ١٠٠ أو ١٠٠٠</p>')}''' + tn('المفردات من دليل المعلم ص٨٦. التعريفات بجملةٍ واحدة من إعدادي (من خارج المرجع) لتثبيت المعنى.')))

# ═══════════ الحصة: الوحدات والتحويل ═══════════
S.append(slide('''<span class="tag">الحصة · ٤٠ دقيقة</span><h2>وحدات القياس والتحويل بينها</h2>
<div class="plan"><div><b>٤ د</b>تهيئة</div><div><b>٦ د</b>الوحدات وأدواتها</div><div><b>٦ د</b>سلّم التحويل</div>
<div><b>٧ د</b>مثال ٤-١ (١)</div><div><b>٥ د</b>مثال ٤-١ (٢)</div><div><b>٧ د</b>نحن ← أنتم</div><div><b>٢ د</b>انتبه</div><div><b>٣ د</b>بطاقة الخروج</div></div>''', 'divider'))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">تهيئة 🤔</span>{ref('النشاط في دليل المعلم')}</div><h2>أيّهما أثقل؟</h2>
<div class="vs">{st('<div>طن واحد</div>')}<b>أم</b>{st('<div>٥٠٠٠٠٠ غم</div>')}</div>
{st('<div class="note">خمّنوا الآن… وسنعود إلى السؤال في آخر الحصة</div>')}''' + tn('النشاط في الدليل: ناقش أفكار الطلاب دون أن تكشف الإجابة، ثم نحلّه بعد تعلّم التحويل (الطن أثقل: ٥٠٠٠٠٠ غم = ٥٠٠ كغم = ٠٫٥ طن).')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('كتاب الطالب ص ٨٠')}</div><h2>وحدات الطول 📏</h2>
{st(U(('ملم', 'مليمتر', 'mm'), ('سم', 'سنتيمتر', 'cm'), ('م', 'متر', 'm'), ('كم', 'كيلومتر', 'km')))}
{st('<div class="note">نقيس الطول بالمسطرة أو شريط القياس</div>')}''' + tn('الدليل: تأكّد أن الطلاب يدركون طول السنتيمتر بأشياء مألوفة. من إعدادي: ١ سم ≈ عرض إصبع، ١ م ≈ خطوة كبيرة، ١ كم ≈ مشي ١٠ إلى ١٥ دقيقة.')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('كتاب الطالب ص ٨٠')}</div><h2>وحدات الكتلة ⚖️ والسعة 🧪</h2>
<div class="row vrow">{st(FIG('4-1_tools', 'fig sm'))}<div class="col" style="gap:1.4vh">{st(U(('غم', 'غرام', 'g'), ('كغم', 'كيلوغرام', 'kg'), ('طن', 'طن', 'tonne')))}{st(U(('مل', 'مليلتر', 'ml'), ('لتر', 'لتر', 'litre')))}</div></div>
{st('<div class="note">الكتلة بالميزان، والسعة بالمخبار</div>')}''' + tn('الموازين: الزنبركي، وذو الكفّتين، وذو المؤشّر، والرقمي (كتاب الطالب ص٨٠). من إعدادي: ١ كغم ≈ كيس سكّر، ١ لتر ≈ قنّينة ماءٍ كبيرة.')))
S.append(slide(f'''<div class="row hdr">{mode('i')}<span class="qbadge" style="background:#7048E8;box-shadow:0 4px 0 #4C2FB0">سلّم التحويل</span></div><h2>وحدات الطول على درج</h2>
{st(STAIR(*LEN))}''' + tn('من إعدادي (بديلٌ لمخطّط الكتاب ص٨٠): ننزل الدرج إلى وحدةٍ أصغر فنضرب، ونصعد إلى وحدةٍ أكبر فنقسم. الرقم في الدائرة معامل التحويل.')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('جدول كتاب الطالب ص ٨٠')}</div><h2>سلّما الكتلة والسعة</h2>
<div class="row stairs2">{st(STAIR(*MAS))}{st(STAIR(*CAP))}</div>'''))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('كتاب الطالب ص ٨٠')}</div><h2>نضرب أم نقسم؟</h2>
<div class="col" style="gap:1.4vh">{st(box('<div class="col"><b class="kk c-we">⬇ من وحدةٍ كبيرة إلى أصغر: نضرب</b><span class="why">لأن الوحدة الأصغر نحتاج منها عدداً أكبر</span></div>', style="min-width:70vw"))}{st(box('<div class="col"><b class="kk c-exp">⬆ من وحدةٍ صغيرة إلى أكبر: نقسم</b><span class="why">لأن الوحدة الأكبر نحتاج منها عدداً أقل</span></div>', style="min-width:70vw"))}</div>''' + tn('قبل الحل اسأل دائماً: هل نتوقّع عدداً أكبر أم أصغر؟')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('مثال ٤-١ (١ أ)')}</div><h2>حوّل {M(D('3.2'), 'كم', cls="sm")} إلى متر</h2>
{box(STEPS(STP('١) معامل التحويل', M('١ كم', EQ, D('1000'), 'م', cls="sm")), STP('٢) من كبيرة إلى أصغر: نضرب', M(D('3.2'), X, D('1000'), cls="sm")), STP('٣) الناتج', M(D('3200'), 'م', cls="sm"), 'fin')))}'''))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('مثال ٤-١ (١ ب)')}</div><h2>حوّل {M(D('750'), 'غم', cls="sm")} إلى كيلوغرام</h2>
{box(STEPS(STP('١) معامل التحويل', M(D('1000'), 'غم', EQ, '١ كغم', cls="sm")), STP('٢) من صغيرة إلى أكبر: نقسم', M(D('750'), DV, D('1000'), cls="sm")), STP('٣) الناتج', M(D('0.75'), 'كغم', cls="sm"), 'fin')))}'''))
S.append(slide(f'''<div class="row hdr">{mode('i')}<span class="qbadge" style="background:#7048E8;box-shadow:0 4px 0 #4C2FB0">لماذا؟</span></div><h2>تنتقل الأرقام بين المنازل</h2>
<div class="row vrow">{st(valign([('3.2', 'كم'), ('3200', 'م')], fs='clamp(40px,8vh,92px)'))}{st(valign([('750', 'غم'), ('0.75', 'كغم')], fs='clamp(40px,8vh,92px)'))}</div>
{st('<div class="note">× ١٠٠٠ : الأرقام ثلاث منازل إلى اليسار · ÷ ١٠٠٠ : ثلاث منازل إلى اليمين</div>')}''' + tn('من إعدادي: ربطٌ بدرس ٣-٧ (الضرب والقسمة على ١٠ و١٠٠ و١٠٠٠).')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('مثال ٤-١ (٢)')}</div><h2>رتّب تصاعدياً: ٥٠ سم ، ٠٫٤ م ، ٣٤٥ ملم</h2>
{box(STEPS(STP('١) نحوّل الكل إلى سم', M(D('50'), '،', D('40'), '،', D('34.5'), 'سم', cls="sm")), STP('٢) نرتّب', M(D('34.5'), '،', D('40'), '،', D('50'), cls="sm")), STP('٣) بالوحدات الأصلية', '<span class="kk">٣٤٥ ملم ، ٠٫٤ م ، ٥٠ سم</span>', 'fin')))}''' + tn('الكتاب: ٠٫٤ م = ٤٠ سم، و٣٤٥ ملم = ٣٤٫٥ سم. نكتب الإجابة النهائية بالوحدات الأصلية كما في السؤال.')))
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('تمرين ٢ و ٣')}</div><h2>معاً: حوّل</h2>
<div class="row">{''.join(st(f'<button class="flip box col" style="flex:1"><span class="hint">{q}</span><span class="tap">👆</span><span class="hid col">{M(*a_, cls="sm")}</span></button>') for q, a_ in (
  ('٥٦٠ سم = ☐ م', (D('5.6'), 'م')), ('٤٫٣ كم = ☐ م', (D('4300'), 'م')), ('٥٤٠٠ غم = ☐ كغم', (D('5.4'), 'كغم'))))}</div>''' + tn('اسأل في كل بطاقة: ننزل أم نصعد؟ ثم ما المعامل؟')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ١ (أ)')}{timer(2)}</div>''' + quiz('للتحويل من (م) إلى (سم):', [M(X, D('100')), M(DV, D('100')), M(X, D('1000')), M(DV, D('1000'))], 0, 'المتر أكبر من السنتيمتر بمئة مرة، فننزل ونضرب في ١٠٠')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ١ (ب)')}</div>''' + quiz('للتحويل من (مل) إلى (لتر):', [M(X, D('100')), M(DV, D('100')), M(X, D('1000')), M(DV, D('1000'))], 3, 'اللتر أكبر: نصعد ونقسم على ١٠٠٠')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ٤ (و)')}</div>''' + quiz('٦٨٠ مل = ☐ لتر', [M(D('68')), M(D('6.8')), M(D('0.68')), M(D('680000'))], 2, '٦٨٠ ÷ ١٠٠٠ = ٠٫٦٨ لتر')))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">تهيئة: الحل 💡</span>{ref('النشاط في دليل المعلم')}</div><h2>نعود إلى السؤال</h2>
<div class="row">{st(f'<button class="flip box col" style="flex:1"><span class="hint">طن أم ٥٠٠٠٠٠ غم؟</span><span class="tap">👆</span><span class="hid col"><span class="kk">٥٠٠٠٠٠ ÷ ١٠٠٠ = ٥٠٠ كغم</span><span class="kk c-we">الطن أثقل (١٠٠٠ كغم)</span></span></button>')}{st(f'<button class="flip box col" style="flex:1"><span class="hint">٢ كم أم ٥٠٠٠٠٠ سم؟</span><span class="tap">👆</span><span class="hid col"><span class="kk">٥٠٠٠٠٠ ÷ ١٠٠ = ٥٠٠٠ م</span><span class="kk c-we">٥٠٠٠٠٠ سم أطول (٥ كم)</span></span></button>')}</div>''' + tn('السؤال الثاني من النشاط في الدليل أيضاً. ناقش أفكار الطلاب قبل الكشف.')))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">انتبه ⚠️ أخطاء شائعة</span>{ref('دليل المعلم ص ٨٦')}</div><h2>أيّها صحيح؟</h2>
<div class="errs">{''.join(st(f'<button class="flip err"><span class="xq">{q}</span><span class="tap">👆</span><span class="hid xa no">{w}</span></button>') for q, w in (
  ('المليمتر أكبر من السنتيمتر', '✘ السنتيمتر أكبر: ١ سم = ١٠ ملم'),
  ('٣ م = ٣٠ سم', '✘ المعامل ١٠٠: ٣ × ١٠٠ = ٣٠٠ سم'),
  ('٤٥٠ غم = ٤٥٠٠٠٠ كغم', '✘ إلى وحدة أكبر نقسم: ٤٥٠ ÷ ١٠٠٠ = ٠٫٤٥ كغم')))}</div>''' + tn('الخطآن الشائعان في الدليل: الخلط بين الوحدة الأكبر والأصغر، والخطأ في معامل التحويل.')))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج 🎫</span><h2>حوّل، ثم رتّب</h2>
<div class="exit">{st('<div><b>١</b>٣٫٥ كغم = ☐ غم</div>')}{st('<div><b>٢</b>٤٥٠ سم = ☐ م</div>')}{st('<div><b>٣</b>رتّب تصاعدياً: ٦٠ سم ، ٠٫٥٨ م ، ٥٩٥ ملم</div>')}</div>''' + tn('من إعدادي (غير موجودة في الكتابين).')))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج 🎫</span><h2>الإجابات</h2>
<button class="flip box col" style="min-width:40vw"><span class="tap">👆 اضغط لإظهار الإجابات</span><span class="hid col"><span class="kk">١) ٣٫٥ × ١٠٠٠ = ٣٥٠٠ غم</span><span class="kk">٢) ٤٥٠ ÷ ١٠٠ = ٤٫٥ م</span><span class="kk">٣) ٠٫٥٨ م ، ٥٩٥ ملم ، ٦٠ سم</span></span></button>''' + tn('(٣) بالسنتيمتر: ٥٨ ، ٥٩٫٥ ، ٦٠.')))
S.append(slide('''<span class="qbadge" style="background:#0A6770;box-shadow:0 4px 0 #05393E">الواجب المنزلي 🏠</span><h2>كتاب النشاط</h2>
<div class="exit"><div class="st"><div><b>١</b>الصفحات ٥٨ و ٥٩ و ٦٠ في كتاب النشاط</div></div></div>'''))
S.append(slide(f'''<h2>الخلاصة</h2>
<div class="sumg">
{st(box('<div class="col"><b class="kk c-b">الوحدات</b><span>الطول: ملم، سم، م، كم<br>الكتلة: غم، كغم، طن<br>السعة: مل، لتر</span></div>'))}
{st(box('<div class="col"><b class="kk c-we">⬇ إلى أصغر</b><span>نضرب في المعامل<br>١٠ أو ١٠٠ أو ١٠٠٠</span></div>'))}
{st(box('<div class="col"><b class="kk c-exp">⬆ إلى أكبر</b><span>نقسم على المعامل<br>وللترتيب: الوحدة نفسها أولاً</span></div>'))}</div>'''))

# ═══════════ ملحق: تمارين كتاب الطالب ص٨١–٨٣ (الإجابات من دليل المعلم ص٩٠) ═══════════
S.append(launch('sb', '٨١ إلى ٨٣', note=f'المراجع: كتاب الطالب ص٨٠ إلى ٨٣، ودليل المعلم ص٨٦ و ٨٧ وإجاباته ص٩٠ · {ME}'))
H = ['أ', 'ب', 'ج', 'د', 'هـ', 'و', 'ز', 'ح', 'ط']
RC = 'إلى وحدة أصغر نضرب، وإلى وحدة أكبر نقسم'
S.append(ex(1, 'اختر الطريقة الصحيحة للتحويل', RC, [('(أ) من (م) إلى (سم)', '× ١٠٠'), ('(ب) من (مل) إلى (لتر)', '÷ ١٠٠٠'), ('(ج) من (كغم) إلى (غم)', '× ١٠٠٠'), ('(د) من (كغم) إلى (طن)', '÷ ١٠٠٠')], cols=2))
S.append(ex(2, 'حوّل الأطوال', RC, [(f'({h}) {q}', a_) for h, (q, a_) in zip(H, [
  ('٨٠ ملم = ☐ سم', '٨ سم'), ('١٢ سم = ☐ ملم', '١٢٠ ملم'), ('٣ م = ☐ سم', '٣٠٠ سم'), ('٥٠٠٠ م = ☐ كم', '٥ كم'), ('٥٦٠ سم = ☐ م', '٥٫٦ م'),
  ('٤٥ ملم = ☐ سم', '٤٫٥ سم'), ('٤٫٣ كم = ☐ م', '٤٣٠٠ م'), ('١٫٨ م = ☐ سم', '١٨٠ سم'), ('٨٩٥ م = ☐ كم', '٠٫٨٩٥ كم')])], cols=2))
S.append(ex(3, 'حوّل الكتل', RC, [(f'({h}) {q}', a_) for h, (q, a_) in zip(H, [
  ('٨٠٠٠ كغم = ☐ طن', '٨ طن'), ('٢ كغم = ☐ غم', '٢٠٠٠ غم'), ('٣٫٤ طن = ☐ كغم', '٣٤٠٠ كغم'), ('٥٤٠٠ غم = ☐ كغم', '٥٫٤ كغم'), ('٠٫٨ كغم = ☐ طن', '٠٫٠٠٠٨ طن'), ('٤٢٥ غم = ☐ كغم', '٠٫٤٢٥ كغم')])], cols=2))
S.append(ex(4, 'حوّل السعات', RC, [(f'({h}) {q}', a_) for h, (q, a_) in zip(H, [
  ('٩٠٠٠ مل = ☐ لتر', '٩ لتر'), ('٤ لتر = ☐ مل', '٤٠٠٠ مل'), ('٥٫٢ لتر = ☐ مل', '٥٢٠٠ مل'), ('٣٢٠٠ مل = ☐ لتر', '٣٫٢ لتر'), ('٠٫٥ لتر = ☐ مل', '٥٠٠ مل'), ('٦٨٠ مل = ☐ لتر', '٠٫٦٨ لتر')])], cols=2))
S.append(ex(5, 'أكمل من الإطار', 'الإطار: ٤٣ ، كغم ، ٣٢ ، سم ، ٦٧٠ ، غم ، × ، ÷ ، ١٠ ، ١٠٠٠ ، ٣٢٠', [(f'({D(i)}) {q}', a_) for i, (q, a_) in enumerate([
  ('٤٫٣ طن × ☐ = ٤٣٠٠ كغم', '١٠٠٠'), ('٨٫٥ ☐ × ١٠ = ٨٥ ملم', 'سم'), ('٦٧ ملم ☐ ١٠ = ٦٫٧ سم', '÷'), ('٠٫٤٣ م × ١٠٠ = ☐ سم', '٤٣'),
  ('☐ مل ÷ ١٠٠٠ = ٠٫٦٧ لتر', '٦٧٠'), ('٨٥٠ ☐ ÷ ١٠٠٠ = ٠٫٨٥ ☐', 'غم ، كغم'), ('(ب) بالأربعة المتبقية', '٣٢ × ١٠ = ٣٢٠')], 1)], cols=2))
S.append(ex(6, 'رتّب تصاعدياً', 'نحوّل إلى الوحدة نفسها، ثم نرتّب، ثم نكتب بالوحدات الأصلية', [(f'({h}) {q}', a_) for h, (q, a_) in zip(H, [
  ('٣٥ سم ، ٠٫٣٨ م ، ٢٧٠ ملم', '٢٧٠ ملم ، ٣٥ سم ، ٠٫٣٨ م'), ('٤٫٢ لتر ، ٧٩٥ مل ، ٠٫٨ لتر', '٧٩٥ مل ، ٠٫٨ لتر ، ٤٫٢ لتر'),
  ('٠٫١٢٥ كغم ، ٨ كغم ، ٩٥ غم', '٩٥ غم ، ٠٫١٢٥ كغم ، ٨ كغم'), ('٦٢٥٠ م ، ٦٫٢ كم ، ٦٫٠٥ كم', '٦٫٠٥ كم ، ٦٫٢ كم ، ٦٢٥٠ م')])], cols=1, per=2))
S.append(ex(7, 'واجب عائشة', 'المتر أكبر من المليمتر، فنضرب', [(FIG('4-1_aisha', 'fig side') + 'هل إجابة عائشة صحيحة؟ اشرح', 'نعم<small>في المتر ١٠٠٠ ملم، ومن وحدةٍ أكبر إلى أصغر نضرب: ٢٫٣ × ١٠٠٠ = ٢٣٠٠ ملم</small>')], cols=1, note='تعليق الدليل: شجّع الطلاب على شرحٍ يوضّح فهمهم للعملية.'))
S.append(ex(8, 'زجاجات سعيد', 'نحوّل السعات إلى الوحدة نفسها (مل)', [(FIG('4-1_bottles', 'fig side') + 'أ: ٦٥٠ مل · ب: ٠٫٣٨ لتر · ج: ٥٠٢٠ مل · د: ٠٫٠٤٥ لتر<br>أيّها أقرب إلى نصف لتر (٥٠٠ مل)؟', 'الزجاجة ب<small>أ: ٦٥٠ − ٥٠٠ = ١٥٠ مل · ب: ٥٠٠ − ٣٨٠ = ١٢٠ مل · ج: أكثر من ٥ لترات · د: ٤٥ مل فقط</small>')], cols=1, note='تعليق الدليل: يحوّل الطلاب بعض القياسات لتصبح كلها بالوحدة نفسها.'))
S.append(ex(9, 'شاشة سارة', 'نحوّل الطولين إلى سنتيمتر', [(FIG('4-1_sara') + 'عددٌ كامل بالسنتيمتر، أصغر من ٣٢٫٨ سم وأكبر من ٣١٥ ملم<br>ما طول الشاشة؟', '٣٢ سم<small>٣١٥ ملم = ٣١٫٥ سم، والعدد الكامل بين ٣١٫٥ و ٣٢٫٨ هو ٣٢</small>')], cols=1, note='تعليق الدليل: وجّه الطلاب إلى تحويل الطولين إلى سنتيمتر، وناقش أهمية ذلك.'))

# ═══════════ ملحق: حلول كتاب النشاط ص٥٨–٦٠ (الإجابات من دليل المعلم ص٩٢) ═══════════
S.append(launch('ab', '٥٨ إلى ٦٠', note='الإجابات النهائية من دليل المعلم ص ٩٢'))
NA, NB, NC = 'نشاط ص ٥٨ · تمرين', 'نشاط ص ٥٩ · تمرين', 'نشاط ص ٦٠ · تمرين'
S.append(ex(1, 'اختر الإجابة الصحيحة', RC, [('(١) من كم إلى م', '× ١٠٠٠'), ('(٢) من غم إلى كغم', '÷ ١٠٠٠'), ('(٣) من ملم إلى م', '÷ ١٠٠٠'), ('(٤) من سم إلى م', '÷ ١٠٠')], cols=2, src=NA))
S.append(ex(2, 'حوّل الأطوال', RC, [(f'({h}) {q}', a_) for h, (q, a_) in zip(H, [
  ('٩ م = ☐ سم', '٩٠٠ سم'), ('٨٫١ كم = ☐ م', '٨١٠٠ م'), ('٥٠ ملم = ☐ سم', '٥ سم'), ('٧٠٠٠ م = ☐ كم', '٧ كم'), ('٢٢٠ سم = ☐ م', '٢٫٢ م'),
  ('٧٥ ملم = ☐ سم', '٧٫٥ سم'), ('٨٦ سم = ☐ ملم', '٨٦٠ ملم'), ('٦٫٦ م = ☐ سم', '٦٦٠ سم'), ('٤٥٥ م = ☐ كم', '٠٫٤٥٥ كم')])], cols=2, src=NA))
S.append(ex(3, 'حوّل الكتل', RC, [(f'({h}) {q}', a_) for h, (q, a_) in zip(H, [
  ('٧٫٥ طن = ☐ كغم', '٧٥٠٠ كغم'), ('٩٧٥ غم = ☐ كغم', '٠٫٩٧٥ كغم'), ('٣٠٠٠ كغم = ☐ طن', '٣ طن'), ('٩٩٠٠ غم = ☐ كغم', '٩٫٩ كغم'), ('٠٫٢ كغم = ☐ طن', '٠٫٠٠٠٢ طن'), ('٦ كغم = ☐ غم', '٦٠٠٠ غم')])], cols=2, src=NA))
S.append(ex(4, 'حوّل السعات', RC, [(f'({h}) {q}', a_) for h, (q, a_) in zip(H, [
  ('٢٠٠٠ مل = ☐ لتر', '٢ لتر'), ('٦ لتر = ☐ مل', '٦٠٠٠ مل'), ('٨٫٨ لتر = ☐ مل', '٨٨٠٠ مل'), ('٥٥٠٠ مل = ☐ لتر', '٥٫٥ لتر'), ('٠٫٢ لتر = ☐ مل', '٢٠٠ مل'), ('٩٩٠ مل = ☐ لتر', '٠٫٩٩ لتر')])], cols=2, src=NA))
S.append(ex(5, 'أكمل من الإطار', 'الإطار: ÷ ، ٥٥ ، ٥٥٠ ، ١٠٠٠ ، ملم ، سم ، م ، ×', [(f'({h}) {q}', a_) for h, (q, a_) in zip(H, [
  ('٥٫٥ طن × ☐ = ٥٥٠٠ كغم', '١٠٠٠'), ('٥٫٥ ☐ × ١٠ = ٥٥ ملم', 'سم'), ('٥٥ ملم ☐ ١٠ = ٥٫٥ سم', '÷'), ('٠٫٥٥ م × ١٠٠ = ☐ سم', '٥٥'), ('☐ مل ÷ ١٠٠٠ = ٠٫٥٥ لتر', '٥٥٠'), ('٨٥٠ ☐ ÷ ١٠٠٠ = ٠٫٨٥ ☐', 'ملم ، م')])], cols=2, src=NB))
S.append(ex(6, 'رتّب من الأصغر إلى الأكبر', 'نحوّل إلى الوحدة نفسها، ثم نرتّب، ثم نكتب بالوحدات الأصلية', [(f'({h}) {q}', a_) for h, (q, a_) in zip(H, [
  ('٢٧ سم ، ٠٫٣ م ، ٢٨٠ ملم', '٢٧ سم ، ٢٨٠ ملم ، ٠٫٣ م'), ('٧٫٢ لتر ، ٦٣٥ مل ، ٠٫٦ لتر', '٠٫٦ لتر ، ٦٣٥ مل ، ٧٫٢ لتر'),
  ('٠٫٥٥٥ كغم ، ٨٨ غم ، ٠٫٠٦ كغم', '٠٫٠٦ كغم ، ٨٨ غم ، ٠٫٥٥٥ كغم'), ('٣٫١ كم ، ٣٫٠٩٥ كم ، ٣٢٥٠ م', '٣٫٠٩٥ كم ، ٣٫١ كم ، ٣٢٥٠ م')])], cols=1, per=2, src=NB))
S.append(ex(7, 'واجب أحمد', 'من وحدة أكبر (كم) إلى أصغر (م) نضرب', [(FIG('4-1_ahmed', 'fig side') + 'هل أحمد على صواب؟ اشرح', 'لا<small>يجب أن يضرب: ٦٥ × ١٠٠٠ = ٦٥٠٠٠ م، لا أن يقسم</small>')], cols=1, src=NB, note='في إجابات الدليل ص٩٢ ورد اسم «علي» بدل «أحمد» (خطأ في الاسم فقط، والإجابة صحيحة).'))
S.append(ex(8, 'دلاء راشد', 'نحوّل السعات إلى لتر', [(FIG('4-1_buckets') + '٤٧٠٠ مل · ٤٫٨ لتر · ٣٨٨٠ مل · ٤٫٧٥ لتر<br>أيّ دلوٍ سعته أقرب إلى ٥ لترات؟', '٤٫٨ لتر<small>٤٧٠٠ مل = ٤٫٧ لتر · ٣٨٨٠ مل = ٣٫٨٨ لتر · ٤٫٧٥ لتر · والأقرب ٤٫٨ (ينقص ٠٫٢ فقط)</small>')], cols=1, src=NB))
S.append(ex(9, 'قياسا عائشة', 'نحوّل الطولين إلى سنتيمتر', [(FIG('4-1_aisha2') + 'عددٌ كامل بالسنتيمتر، أصغر من ٠٫٦٧٣ م وأكبر من ٦٥٩ ملم<br>ما القياسان المحتملان؟', '٦٦ سم أو ٦٧ سم<small>٦٥٩ ملم = ٦٥٫٩ سم ، ٠٫٦٧٣ م = ٦٧٫٣ سم</small>')], cols=1, src=NC))

EXTRA_CSS_OWN = '''
.stps{display:flex;flex-direction:column;gap:1.2vh;align-items:stretch}
.stp{display:flex;align-items:center;gap:1.4vw;justify-content:space-between}
.stp .lab{flex:0 1 auto;max-width:60%;font-family:var(--fh);font-weight:800;color:#2563EB;background:#EAF1FF;border-radius:12px;padding:.2em .8em;text-align:center;line-height:1.4;font-size:clamp(20px,3.6vh,42px)}
.stp.fin .lab{background:var(--good);color:#fff}
.slide .vrow{align-items:center;justify-content:center;gap:2vh 3vw;flex-wrap:wrap}
.box .col>.m:not(.mid):not(.sm):not(.big),.hid.col>.m:not(.mid):not(.sm):not(.big){font-size:clamp(32px,6vh,70px)}
.voc3{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1.6vw;width:min(1500px,94vw)}
.voc3 .st>div{display:flex;flex-direction:column;align-items:center;gap:.6vh;background:#fff;border:3px solid var(--line);border-radius:18px;padding:1.6vh 1vw;text-align:center}
.voc3 b{font-family:var(--fh);font-size:clamp(34px,6.4vh,76px);color:var(--base)}.voc3 i{font-style:normal;font-weight:700;color:var(--ink2);font-size:clamp(20px,3.4vh,38px)}
.voc3 span{font-weight:700;font-size:clamp(22px,3.8vh,44px);line-height:1.5}
.units{display:flex;gap:1.4vw;flex-wrap:wrap;justify-content:center}
.units>div{display:flex;flex-direction:column;align-items:center;background:#fff;border:3px solid var(--base);border-radius:16px;padding:.8vh 1.4vw;min-width:9em}
.units b{font-family:var(--fh);font-size:clamp(36px,7vh,82px);color:var(--base);line-height:1.15}.units span{font-weight:800;font-size:clamp(20px,3.4vh,38px)}.units i{font-style:normal;color:var(--ink2);font-weight:700;font-size:clamp(18px,3vh,32px);direction:ltr}
.slide .svgfig.stair{width:auto;height:min(60vh,600px);max-width:92vw;max-height:none}
.stairs2{gap:2vw}.slide .stairs2 .svgfig.stair{height:min(50vh,480px);max-width:46vw}
.vs{display:flex;align-items:center;gap:3vw;font-family:var(--fh);font-weight:900}
.vs .st>div{background:#fff;border:3px solid var(--line);border-radius:18px;padding:1.6vh 2.4vw;font-size:clamp(40px,8vh,92px)}
.vs>b{font-size:clamp(30px,5.4vh,62px);color:var(--exp)}
.why{font-weight:700;color:var(--ink2);font-size:clamp(22px,3.8vh,44px)}
.errs{display:flex;flex-direction:column;gap:1.4vh;width:min(1400px,92vw)}
.errs .err{display:flex;flex-direction:column;align-items:center;gap:.6vh;background:#fff;border:3px solid var(--line);border-radius:16px;padding:.8vh 1.6vw;font-size:clamp(26px,5vh,58px);font-weight:700}
.errs .err .xa{font-size:clamp(24px,4.4vh,50px)}
.sumg{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:2vw;width:min(1600px,94vw)}
.sumg .col span{font-weight:700;font-size:clamp(22px,4vh,46px);line-height:1.5}
.sumg .kk{font-size:clamp(30px,5.6vh,66px)}
.hid.col .kk{font-size:clamp(28px,5.2vh,60px)}
.xa small{display:block}
@media (max-aspect-ratio:1/1){.voc3,.sumg{grid-template-columns:1fr}.stairs2{flex-direction:column}.slide .stairs2 .svgfig.stair{max-width:90vw;height:min(32vh,400px)}}
''' + FIG_CSS
