# شرائح درس ٣-١ «ترتيب الأعداد العشرية والكسور العشرية» — الصف السابع (٣ حصص، كتاب الطالب ص٥٧–٥٩)
# المراجع: دليل المعلم ص٦٣–٦٤ (كتابة أصفار لتتساوى المنازل، الرموز < و >، معاملات التحويل؛ الأخطاء الشائعة: ١٣٫٢ < ١٣٫١١ …؛ النشاطان ١ و ٢)،
# كتاب الطالب ص٥٧–٥٩ (مثال ٣-١)، وإجابات الدليل ص٧٧ (كتاب الطالب) وص٨١ (كتاب النشاط ص٤٠–٤٢).
# python3.12 gen_powers.py dec_slides.py ترتيب_الأعداد_العشرية_عرض_تفاعلي.html "ترتيب الأعداد العشرية والكسور العشرية — الصف السابع"

def STP(lab, expr, cls=''): return st(f'<div class="stp {cls}"><span class="lab">{lab}</span>{expr}</div>')
def STEPS(*rows): return '<div class="stps">' + ''.join(rows) + '</div>'
DV = '<span class="x">÷</span>'
TR = str.maketrans('0123456789.', '٠١٢٣٤٥٦٧٨٩٫')
def D(x): return str(x).translate(TR)                              # «8.56» ← «٨٫٥٦»
def PV(nums, hi=None, cols=('عشرات', 'آحاد', 'أجزاء<br>من عشرة', 'أجزاء<br>من مئة', 'أجزاء<br>من ألف')):
    # جدول المنازل: الأعداد مصفوفةٌ عند الفاصلة؛ hi = رقم العمود المُبرَز (٠ عشرات … ٤ أجزاء من ألف)
    head = ''.join(f'<th class="{"hi" if i == hi else ""}">{c}</th>' + ('<th class="pt"></th>' if i == 1 else '') for i, c in enumerate(cols))
    rows = ''
    for n in nums:
        w, _, f = n.partition('.')
        w = w.rjust(2); f = f.ljust(3)
        cells = [w[0], w[1], f[0], f[1], f[2]]
        rows += '<tr>' + ''.join(f'<td class="{"hi" if i == hi else ""}{" z" if c == " " else ""}">{D(c) if c != " " else ""}</td>' + ('<td class="pt">٫</td>' if i == 1 else '') for i, c in enumerate(cells)) + '</tr>'
    return f'<table class="pv"><tr>{head}</tr>{rows}</table>'
def LADDER(units, facs, cls=''):   # سلّم التحويل: من الوحدة الكبرى (يميناً) إلى الصغرى
    out = ''
    for i, u in enumerate(units):
        out += f'<span class="lu">{u}</span>'
        if i < len(facs): out += f'<span class="lf"><b>× {D(facs[i])}</b><i>÷ {D(facs[i])}</i></span>'
    return f'<div class="ladder {cls}">{out}</div>'
S = []
ME = 'إعداد: أ. عيسى الحارثي'
S.append(slide(f'''<span class="tag">الصف السابع · الدرس ٣-١</span>
<h1 class="h1s">ترتيب الأعداد العشرية والكسور العشرية</h1>
<p class="lead">كتاب الطالب ص ٥٧ إلى ٥٩ · ثلاث حصص</p>
<p class="lead" style="font-size:clamp(26px,4.8vh,56px)">{ME}</p>''', 'cover'))
CAN = ['أرتّب الأعداد العشرية <b>تصاعدياً وتنازلياً</b> بمقارنة المنازل', 'أستخدم الرموز <b>&lt; و &gt; و = و ≠</b> للمقارنة', '<b>أحوّل</b> بين وحدات الطول والكتلة والسعة قبل المقارنة والترتيب']
S.append(slide(f'''<h2>في نهاية هذا الدرس…</h2>
<div class="can">{''.join(f'<div><span class="can-i">✔</span><span><b>أنا أستطيع</b> أن {t}</span></div>' for t in CAN)}</div>'''))
S.append(slide(f'''<h2>مفردات الدرس</h2>
{st('<div class="vocab wide"><div><span>ترتيب تصاعدي</span><i>ascending</i></div><div><span>ترتيب تنازلي</span><i>descending</i></div><div><span>المنزلة العشرية</span><i>decimal place</i></div><div><span>القياسات</span><i>measures</i></div></div>')}
<p class="lead">ثلاث حصص: <b class="c-i">أنا</b> ← <b class="c-we">نحن</b> ← <b class="c-u">أنتم</b></p>'''))

# ═══════════ الحصة الأولى: ترتيب الأعداد العشرية ═══════════
S.append(slide('''<span class="tag">الحصة الأولى · ٤٠ دقيقة</span><h2>ترتيب الأعداد العشرية</h2>
<div class="plan"><div><b>٥ د</b>تهيئة: نشاط البطاقات</div><div><b>٥ د</b>المنازل العشرية</div><div><b>٨ د</b>خطوات الترتيب</div>
<div><b>٥ د</b>نكتب أصفاراً</div><div><b>٦ د</b>نحن: مثال ٣-١ (أ)</div><div><b>٥ د</b>أنتم</div><div><b>٣ د</b>انتبه</div><div><b>٣ د</b>بطاقة الخروج</div></div>''', 'divider'))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">تهيئة 🎲</span>{ref('النشاط ١ في دليل المعلم')}</div><h2>كوّن عبارةً صحيحة بالأرقام التي أذكرها</h2>
{st('<div class="slots"><span>☐☐٫☐☐</span><b>&lt;</b><span>☐☐٫☐☐</span></div>')}
{st('<div class="note">أذكر ثمانية أرقام عشوائية من ٠ إلى ٩، وتكتبون كل رقمٍ في مربّع لتصبح العبارة صحيحة</div>')}''' + tn('النشاط ١ في الدليل بعد مناقشة مثال ٣-١: مجموعات، نقطة لكل مجموعة تكوّن عبارة صحيحة. ثم اطلب أصغر عدد ممكن وأكبر عدد ممكن (٥ نقاط لعدد صحيح و ١٠ للعددين).')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('كتاب الطالب ص ٥٧')}</div><h2>المنازل العشرية</h2>
{st(PV(['5.201', '12.37', '23.2']))}
{st('<div class="note">عدد الأرقام بعد الفاصلة العشرية هو <b>عدد المنازل العشرية</b>: ٥٫٢٠١ له ثلاث منازل</div>')}'''))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('كتاب الطالب ص ٥٧')}</div><h2>رتّب تصاعدياً: {M(D('8.56'), '،', D('7.4'), '،', D('8.518'), cls="sm")}</h2>
{box(STEPS(STP('١) نقارن العدد الكامل', M(D('7'), '&lt;', D('8'), cls="sm")), STP('٢) العدد الكامل متساوٍ، فنقارن الأجزاء من عشرة', M(D('5'), EQ, D('5'), cls="sm")), STP('٣) نقارن الأجزاء من مئة', M(D('1'), '&lt;', D('6'), cls="sm")), STP('الترتيب', M(D('7.4'), '،', D('8.518'), '،', D('8.56'), cls="sm"), 'fin')))}'''))
S.append(slide(f'''<div class="row hdr">{mode('i')}<span class="qbadge" style="background:#7048E8;box-shadow:0 4px 0 #4C2FB0">جدول المنازل</span></div><h2>نقارن عموداً عموداً من اليمين</h2>
{st(PV(['7.4', '8.56', '8.518'], hi=3))}
{st('<div class="note">في عمود الأجزاء من مئة: ١ أصغر من ٦، فـ ٨٫٥١٨ أصغر من ٨٫٥٦</div>')}''' + tn('من خارج المرجع: جدول المنازل يرتّب الأعداد عند الفاصلة، فتسهل المقارنة عموداً عموداً.')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('دليل المعلم ص ٦٣')}</div><h2>نكتب أصفاراً لتتساوى المنازل العشرية</h2>
<div class="col" style="gap:1.4vh">{st(box(f'<div class="col"><span class="hint">قبل</span>{M(D("5.682"), "،", D("5.61"), "،", D("0.95"), "،", D("5.68"), cls="sm")}</div>', style="min-width:60vw"))}{st(box(f'<div class="col"><span class="hint">بعد</span>{M(D("5.682"), "،", D("5.610"), "،", D("0.950"), "،", D("5.680"), cls="sm")}</div>', style="border-color:var(--base);min-width:60vw"))}</div>
{st('<div class="note">الصفر في آخر الجزء العشري <b>لا يغيّر</b> قيمة العدد: ٥٫٦١ = ٥٫٦١٠</div>')}''' + tn('اقتراح الدليل لمن يجد صعوبة: نعيد كتابة الأعداد بعدد المنازل نفسه بإضافة أصفار عن يمينها.')))
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('مثال ٣-١ (أ)')}</div><h2>معاً: رتّب تصاعدياً {M(D('5.682'), '،', D('5.61'), '،', D('0.95'), '،', D('5.68'), cls="sm")}</h2>
<button class="flip box col"><span class="tap">👆 الحل</span><span class="hid col">{M(D('0.95'), '،', D('5.61'), '،', D('5.68'), '،', D('5.682'), cls="sm")}<small class="hint">٠٫٩٥ أصغرها لأن عددها الكامل ٠، ثم نقارن الأجزاء من مئة، ثم من ألف</small></span></button>'''))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ١ (د)')}{timer(2)}</div>''' + quiz(f'ما أصغر عدد؟ {M(D("9.09"), "،", D("8.9"), "،", D("9.53"), "،", D("9.4"))}', [M(D('9.09')), M(D('8.9')), M(D('9.4')), M(D('9.53'))], 1, 'العدد الكامل ٨ أصغر من ٩')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ١ (و)')}</div>''' + quiz(f'ما أكبر عدد؟ {M(D("0.107"), "،", D("0.084"), "،", D("0.102"), "،", D("0.009"))}', [M(D('0.084')), M(D('0.102')), M(D('0.107')), M(D('0.009'))], 2, 'الأجزاء من عشرة: ١ في ٠٫١٠٧ و ٠٫١٠٢ ، ثم الأجزاء من ألف: ٧ أكبر من ٢')))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">انتبه ⚠️ أخطاء شائعة</span>{ref('دليل المعلم ص ٦٣')}</div><h2>أيّها صحيح؟</h2>
<div class="errs">{''.join(st(f'<button class="flip err"><span class="xq">{q}</span><span class="tap">👆</span><span class="hid xa no">{w}</span></button>') for q, w in (
  (M(D('13.2'), '&lt;', D('13.11')), '✘ عدد الأرقام لا يحدّد الأكبر: ١٣٫٢٠ &gt; ١٣٫١١'),
  (M(D('2'), '&lt;', D('11'), 'إذن', D('13.2'), '&lt;', D('13.11')), '✘ نقارن الأجزاء من عشرة: ٢ &gt; ١'),
  ('&lt; تعني «أكبر من»', '✘ &lt; تعني «أصغر من»، و &gt; تعني «أكبر من»')))}</div>''' + tn('الأخطاء الشائعة الثلاثة في الدليل: الاعتماد على عدد الأرقام، والخلط بين الرمزين، والخطأ في عامل التحويل (في الحصة الثانية).')))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ١ 🎫</span><h2>رتّب تصاعدياً</h2>
<div class="exit">{st(f'<div><b>١</b>{M(D("5.49"), "،", D("2.06"), "،", D("7.99"), "،", D("5.91"), cls="sm")}</div>')}{st(f'<div><b>٢</b>{M(D("3.09"), "،", D("2.87"), "،", D("3.11"), "،", D("2.55"), cls="sm")}</div>')}{st(f'<div><b>٣</b>{M(D("6.725"), "،", D("6.178"), "،", D("6.71"), "،", D("6.17"), cls="sm")}</div>')}</div>'''))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ١ 🎫</span><h2>الإجابات</h2>
<button class="flip box col" style="min-width:40vw"><span class="tap">👆 اضغط لإظهار الإجابات</span><span class="hid col">{M(D('2.06'), '،', D('5.49'), '،', D('5.91'), '،', D('7.99'), cls="sm")}{M(D('2.55'), '،', D('2.87'), '،', D('3.09'), '،', D('3.11'), cls="sm")}{M(D('6.17'), '،', D('6.178'), '،', D('6.71'), '،', D('6.725'), cls="sm")}</span></button>'''))

# ═══════════ الحصة الثانية: الرموز والتحويل بين الوحدات ═══════════
S.append(slide('''<span class="tag">الحصة الثانية · ٤٠ دقيقة</span><h2>المقارنة والتحويل بين الوحدات</h2>
<div class="plan"><div><b>٣ د</b>إحماء</div><div><b>٤ د</b>الرموز</div><div><b>٨ د</b>معاملات التحويل</div>
<div><b>٦ د</b>نضرب أم نقسم؟</div><div><b>٧ د</b>مثال ٣-١ (ب، ج)</div><div><b>٦ د</b>نحن ← أنتم</div><div><b>٣ د</b>انتبه</div><div><b>٣ د</b>بطاقة الخروج</div></div>''', 'divider'))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">إحماء 🔥</span>{timer(1)}</div>''' + quiz(f'أيّ رمز يجعل العبارة صحيحة؟ {M(D("6.71"), "☐", D("6.03"))}', [M('&lt;'), M('&gt;'), M('=')], 1, '٦٫٧١ أكبر من ٦٫٠٣ لأن ٧ &gt; ٠ في الأجزاء من عشرة')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('كتاب الطالب ص ٥٧')}</div><h2>رموز المقارنة</h2>
<div class="syms">{''.join(st(f'<div><b>{s}</b><span>{t}</span></div>') for s, t in (('=', 'يساوي'), ('≠', 'لا يساوي'), ('&gt;', 'أكبر من'), ('&lt;', 'أصغر من')))}</div>
{st(f'<div class="note">نقرأ من اليمين: {M(D("8.56"), "&gt;", D("8.518"))} أي «٨٫٥٦ أكبر من ٨٫٥١٨»</div>')}''' + tn('اطلب من الطلاب تذكّر الرمزين: الفتحة الواسعة نحو العدد الأكبر.')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('كتاب الطالب ص ٥٧')}</div><h2>معاملات التحويل</h2>
<div class="lads">{st('<div><span class="lt">الطول</span>' + LADDER(['كم', 'م', 'سم', 'ملم'], [1000, 100, 10]) + '</div>')}{st('<div><span class="lt">الكتلة</span>' + LADDER(['طن', 'كغم', 'غم'], [1000, 1000]) + '</div>')}{st('<div><span class="lt">السعة</span>' + LADDER(['لتر', 'مل'], [1000]) + '</div>')}</div>'''))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('دليل المعلم ص ٦٣')}</div><h2>نضرب أم نقسم؟</h2>
<div class="col" style="gap:1.4vh">{st(box(f'<div class="col"><b class="kk c-we">من الكبرى إلى الصغرى: نضرب</b>{M(D("7.5"), "م", EQ, D("7.5"), X, D("100"), EQ, D("750"), "سم", cls="sm")}</div>', style="flex:1"))}{st(box(f'<div class="col"><b class="kk c-exp">من الصغرى إلى الكبرى: نقسم</b>{M(D("450"), "غم", EQ, D("450"), DV, D("1000"), EQ, D("0.45"), "كغم", cls="sm")}</div>', style="flex:1"))}</div>''' + tn('الخطأ الشائع الثالث في الدليل: الضرب في ١٠٠٠ بدل القسمة. اسأل: هل نتوقّع عدداً أكبر أم أصغر؟ الوحدة الأصغر تحتاج عدداً أكبر.')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('مثال ٣-١ (ب)')}</div><h2>اكتب = أو ≠ : {M(D("7.5"), "م ☐", D("75"), "سم", cls="sm")}</h2>
{box(STEPS(STP('نحوّل إلى الوحدة نفسها (سم)', M(D('7.5'), X, D('100'), EQ, D('750'), 'سم', cls="sm")), STP('نقارن', M(D('750'), 'سم ≠', D('75'), 'سم', cls="sm")), STP('النتيجة', M(D('7.5'), 'م ≠', D('75'), 'سم', cls="sm"), 'fin')))}'''))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('مثال ٣-١ (ج)')}</div><h2>اكتب &lt; أو &gt; : {M(D("4.5"), "كغم ☐", D("450"), "غم", cls="sm")}</h2>
{box(STEPS(STP('نحوّل إلى غم', M(D('4.5'), X, D('1000'), EQ, D('4500'), 'غم', cls="sm")), STP('نقارن', M(D('4500'), 'غم &gt;', D('450'), 'غم', cls="sm")), STP('النتيجة', M(D('4.5'), 'كغم &gt;', D('450'), 'غم', cls="sm"), 'fin')))}'''))
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('تمرين ٣ (ز، ح)')}</div><h2>معاً: اكتب &lt; أو &gt;</h2>
<div class="row">{st(f'<button class="flip box col" style="flex:1"><span class="hint">{M(D("4.5"), "لتر ☐", D("2700"), "مل", cls="sm")}</span><span class="tap">👆</span><span class="hid col">{M(D("4500"), "مل &gt;", D("2700"), "مل", cls="sm")}</span></button>')}{st(f'<button class="flip box col" style="flex:1"><span class="hint">{M(D("0.45"), "طن ☐", D("547"), "كغم", cls="sm")}</span><span class="tap">👆</span><span class="hid col">{M(D("450"), "كغم &lt;", D("547"), "كغم", cls="sm")}</span></button>')}</div>'''))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ٤ (ج)')}{timer(2)}</div>''' + quiz(f'اكتب = أو ≠ : {M(D("0.85"), "كم ☐", D("850"), "م")}', [M('='), M('≠')], 0, '٠٫٨٥ × ١٠٠٠ = ٨٥٠ م')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ٤ (د)')}</div>''' + quiz(f'اكتب = أو ≠ : {M(D("0.985"), "م ☐", D("985"), "سم")}', [M('='), M('≠')], 1, '٠٫٩٨٥ × ١٠٠ = ٩٨٫٥ سم وليست ٩٨٥')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ٣ (ط)')}</div>''' + quiz(f'اكتب &lt; أو &gt; : {M(D("3.5"), "سم ☐", D("345"), "ملم")}', [M('&lt;'), M('&gt;')], 0, '٣٫٥ × ١٠ = ٣٥ ملم ، و ٣٥ أصغر من ٣٤٥')))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ٢ 🎫</span><h2>اكتب الرمز الصحيح</h2>
<div class="exit">{st(f'<div><b>١</b>{M(D("27.9"), "☐", D("27.85"), cls="sm")} (&lt; أو &gt;)</div>')}{st(f'<div><b>٢</b>{M(D("6.7"), "لتر ☐", D("670"), "مل", cls="sm")} (= أو ≠)</div>')}{st(f'<div><b>٣</b>{M(D("0.06"), "كغم ☐", D("550"), "غم", cls="sm")} (&lt; أو &gt;)</div>')}</div>'''))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ٢ 🎫</span><h2>الإجابات</h2>
<button class="flip box col" style="min-width:40vw"><span class="tap">👆 اضغط لإظهار الإجابات</span><span class="hid col">{M(D('27.9'), '&gt;', D('27.85'), cls="sm")}{M(D('6700'), 'مل ≠', D('670'), 'مل', cls="sm")}{M(D('60'), 'غم &lt;', D('550'), 'غم', cls="sm")}</span></button>'''))

# ═══════════ الحصة الثالثة: ترتيب القياسات وحل المسائل ═══════════
S.append(slide('''<span class="tag">الحصة الثالثة · ٤٠ دقيقة</span><h2>ترتيب القياسات وحلّ المسائل</h2>
<div class="plan"><div><b>٣ د</b>إحماء</div><div><b>٨ د</b>نرتّب قياسات</div><div><b>٥ د</b>نحن</div>
<div><b>١٠ د</b>مسألة السباحة</div><div><b>٦ د</b>النشاط ٢</div><div><b>٥ د</b>أنتم</div><div><b>٣ د</b>بطاقة الخروج</div></div>''', 'divider'))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">إحماء 🔥</span>{timer(1)}</div>''' + quiz('كم غراماً في ٢٫٣ كغم؟', [M(D('23')), M(D('230')), M(D('2300')), M(D('0.0023'))], 2, 'من الكبرى إلى الصغرى نضرب: ٢٫٣ × ١٠٠٠ = ٢٣٠٠ غم')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('تمرين ٢ (أ)')}</div><h2>رتّب تنازلياً هذه الكتل</h2>
{st('<div class="note">٢٫٣ كغم ، ٧٨٠ غم ، ٢٫١٨ كغم ، ١٩٥٠ غم</div>')}
{box(STEPS(STP('نحوّل الكل إلى غم', M(D('2300'), '،', D('780'), '،', D('2180'), '،', D('1950'), cls="sm")), STP('نرتّب من الأكبر', M(D('2300'), '،', D('2180'), '،', D('1950'), '،', D('780'), cls="sm")), STP('بالوحدات الأصلية', M(D('2.3'), 'كغم ،', D('2.18'), 'كغم ،', D('1950'), 'غم ،', D('780'), 'غم', cls="sm"), 'fin')))}''' + tn('نحوّل إلى الوحدة الأصغر غالباً لنتجنّب الكسور العشرية، ثم نكتب الإجابة بالوحدات الأصلية.')))
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('تمرين ٢ (ج)')}</div><h2>معاً: رتّب تنازلياً ١٢ م ، ٦٥٠ سم ، ٠٫٥ م ، ٥٣ سم</h2>
<button class="flip box col"><span class="tap">👆 الحل</span><span class="hid col">{M(D('1200'), '،', D('650'), '،', D('50'), '،', D('53'), 'سم', cls="sm")}{M(D('12'), 'م ،', D('650'), 'سم ،', D('53'), 'سم ،', D('0.5'), 'م', cls="sm")}</span></button>'''))
SW = [('٢٥٠ م', '١٫٢ كم'), ('١٫٢٥ كم', '٢٤٠ م'), ('٠٫٥ كم', '٠٫٤ كم'), ('٢٥٠٠ م', '١٫٦٤ كم'), ('٢ كم', '٨٢٠ م'), ('١٫٧٥ كم', '٦٤٠ م'), ('٧٥٠ م', '٠٫٢ كم'), ('١٥٠٠ م', '١٫٤٢ كم'), ('٢٥ كم', '٩٦٠ م'), ('٠٫٧٥ كم', '٠٫٨٨ كم')]
S.append(slide(f'''<div class="row hdr"><span class="qbadge">فكّر 💡</span>{ref('تمرين ٥')}</div><h2>مسافات السباحة في ١٠ أيام</h2>
<table class="swim"><tr><th>سلطان</th><th>أحمد</th></tr>{''.join(f'<tr><td class="{"bad" if s == "٢٥ كم" else ""}">{s}</td><td>{h}</td></tr>' for s, h in SW)}</table>''' + tn('تعليق الدليل: شجّع الطلاب على تحويل المسافات كلها إلى الوحدة نفسها (أمتار). ولذوي التحصيل المنخفض في (ج): اكتبوا أول ثلاثة أو أربعة مضاعفات للعدد ٢٥.')))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">فكّر 💡</span>{ref('تمرين ٥')}</div><h2>مسألة السباحة: الحلول</h2>
<div class="errs">{''.join(st(f'<button class="flip err"><span class="xq">{q}</span><span class="tap">👆</span><span class="hid xa">{w}</span></button>') for q, w in (
  ('(أ) أيّ مسافةٍ لسلطان غير ممكنة؟', '٢٥ كم، لأنها أكبر بكثير من المسافات الأخرى'),
  ('(ب) أطول مسافةٍ لأحمد أكبر بثماني مرات من أقصرها؟', 'نعم: ٠٫٢ × ٨ = ١٫٦ كم، وأطولها ١٫٦٤ كم'),
  ('(ج) من يسبح في الحمّام الذي طوله ٢٥ م؟', 'سلطان: مسافاته كلها مضاعفات للعدد ٢٥')))}</div>'''))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">النشاط ٢ 🎲</span>{ref('دليل المعلم ص ٦٤')}</div><h2>تسعة أرقام وثلاثة أعداد مرتّبة</h2>
{st('<div class="slots"><span>☐☐٫☐</span><b>&lt;</b><span>☐☐٫☐</span><b>&lt;</b><span>☐☐٫☐</span></div>')}
{st('<div class="note">أذكر تسعة أرقام عشوائية، وتكتبون كل رقمٍ فور ذكره لتصبح العلاقة صحيحة</div>')}''' + tn('النشاط ٢ بعد حلّ تمارين ٣-١: نقطة لكل مجموعة تجيب إجابة صحيحة، ثم حدّد المجموعة الفائزة.')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ٢ (د)')}{timer(2)}</div>''' + quiz('أيّ هذه السعات هو الأكبر؟', [M(D('0.55'), 'لتر'), M(D('95'), 'مل'), M(D('0.9'), 'لتر'), M(D('450'), 'مل')], 2, '٠٫٩ لتر = ٩٠٠ مل، وهي الأكبر')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ٢ (و)')}</div>''' + quiz('أيّ هذه الكتل هو الأصغر؟', [M(D('0.08'), 'طن'), M(D('920'), 'كغم'), M(D('0.15'), 'طن'), M(D('50'), 'كغم')], 3, '٠٫٠٨ طن = ٨٠ كغم ، و ٠٫١٥ طن = ١٥٠ كغم ، فأصغرها ٥٠ كغم')))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ٣ 🎫</span><h2>رتّب تنازلياً (من الأكبر إلى الأصغر)</h2>
<div class="exit">{st('<div><b>١</b>٥٫٤ سم ، ١٢ ملم ، ٠٫٨ سم ، ٩ ملم</div>')}{st('<div><b>٢</b>٦٫٥٥ كم ، ٧٨٠ م ، ٦٫٤ كم ، ١٤٥٠ م</div>')}</div>'''))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ٣ 🎫</span><h2>الإجابات</h2>
<button class="flip box col" style="min-width:40vw"><span class="tap">👆 اضغط لإظهار الإجابات</span><span class="hid col"><span class="kk">٥٫٤ سم ، ١٢ ملم ، ٩ ملم ، ٠٫٨ سم</span><span class="kk">٦٫٥٥ كم ، ٦٫٤ كم ، ١٤٥٠ م ، ٧٨٠ م</span></span></button>'''))
S.append(slide('''<span class="qbadge" style="background:#0A6770;box-shadow:0 4px 0 #05393E">الواجب المنزلي 🏠</span><h2>بعد الحصص الثلاث</h2>
<div class="exit"><div class="st"><div><b>١</b>صفحة ٤٠ في كتاب النشاط (الترتيب والمقارنة)</div></div><div class="st"><div><b>٢</b>صفحتا ٤١ و ٤٢ في كتاب النشاط (القياسات والمسائل)</div></div></div>'''))
S.append(slide(f'''<h2>الخلاصة</h2>
<div class="sumg">
{st(box('<div class="col"><b class="kk c-we">الترتيب</b><span>العدد الكامل، ثم الأجزاء من عشرة، ثم من مئة</span></div>'))}
{st(box('<div class="col"><b class="kk c-exp">الأصفار</b><span>نساوي المنازل: ٥٫٦١ = ٥٫٦١٠</span></div>'))}
{st(box('<div class="col"><b class="kk c-lcm">القياسات</b><span>نحوّل إلى الوحدة نفسها أولاً</span></div>'))}</div>'''))

# ═══════════ ملحق: تمارين كتاب الطالب ص٥٨–٥٩ (الإجابات من دليل المعلم ص٧٧) ═══════════
S.append(launch('sb', '٥٨ و ٥٩', note=f'المراجع: كتاب الطالب ص٥٧ إلى ٥٩، ودليل المعلم ص٦٣ و ٦٤ وإجاباته ص٧٧ · {ME}'))
H = ['أ', 'ب', 'ج', 'د', 'هـ', 'و', 'ز', 'ح', 'ط', 'ي', 'ك', 'ل']
def L(*xs): return ' ، '.join(D(x) for x in xs)
B1 = [(('5.49', '2.06', '7.99', '5.91'), ('2.06', '5.49', '5.91', '7.99')), (('3.09', '2.87', '3.11', '2.55'), ('2.55', '2.87', '3.09', '3.11')),
      (('12.1', '11.88', '12.01', '11.82'), ('11.82', '11.88', '12.01', '12.1')), (('9.09', '8.9', '9.53', '9.4'), ('8.9', '9.09', '9.4', '9.53')),
      (('23.661', '23.592', '23.659', '23.665'), ('23.592', '23.659', '23.661', '23.665')), (('0.107', '0.084', '0.102', '0.009'), ('0.009', '0.084', '0.102', '0.107')),
      (('6.725', '6.178', '6.71', '6.17'), ('6.17', '6.178', '6.71', '6.725')), (('11.302', '11.032', '11.02', '11.1'), ('11.02', '11.032', '11.1', '11.302'))]
RO = 'نقارن العدد الكامل، ثم الأجزاء من عشرة، ثم من مئة، ثم من ألف'
S.append(ex(1, 'رتّب تصاعدياً (من الأصغر إلى الأكبر)', RO, [(f'({h}) {L(*q)}', L(*a_)) for h, (q, a_) in zip(H, B1)], cols=2))
B2 = [('٢٫٣ كغم ، ٧٨٠ غم ، ٢٫١٨ كغم ، ١٩٥٠ غم', '٢٫٣ كغم ، ٢٫١٨ كغم ، ١٩٥٠ غم ، ٧٨٠ غم'), ('٥٫٤ سم ، ١٢ ملم ، ٠٫٨ سم ، ٩ ملم', '٥٫٤ سم ، ١٢ ملم ، ٩ ملم ، ٠٫٨ سم'),
      ('١٢ م ، ٦٥٠ سم ، ٠٫٥ م ، ٥٣ سم', '١٢ م ، ٦٥٠ سم ، ٥٣ سم ، ٠٫٥ م'), ('٠٫٥٥ لتر ، ٩٥ مل ، ٠٫٩ لتر ، ٤٥٠ مل', '٠٫٩ لتر ، ٠٫٥٥ لتر ، ٤٥٠ مل ، ٩٥ مل'),
      ('٦٫٥٥ كم ، ٧٨٠ م ، ٦٫٤ كم ، ١٤٥٠ م', '٦٫٥٥ كم ، ٦٫٤ كم ، ١٤٥٠ م ، ٧٨٠ م'), ('٠٫٠٨ طن ، ٩٢٠ كغم ، ٠٫١٥ طن ، ٥٠ كغم', '٩٢٠ كغم ، ٠٫١٥ طن ، ٠٫٠٨ طن ، ٥٠ كغم'),
      ('٩٥٠٠٠ سم ، ٩٢٠ م ، ٩٨٠٠ ملم ، ٠٫٨٥ كم ، ٠٫٠٠٩ كم', '٩٥٠٠٠ سم ، ٩٢٠ م ، ٠٫٨٥ كم ، ٩٨٠٠ ملم ، ٠٫٠٠٩ كم')]
S.append(ex(2, 'رتّب القياسات تنازلياً (من الأكبر إلى الأصغر)', 'نحوّل إلى الوحدة نفسها أولاً، ثم نرتّب', [(f'({h}) {q}', a_) for h, (q, a_) in zip(H, B2)], cols=1, per=2))
B3 = [('٤٫٢٣ ☐ ٤٫٥٤', '&lt;'), ('٦٫٧١ ☐ ٦٫٠٣', '&gt;'), ('٠٫٢٧ ☐ ٠٫٠٣', '&gt;'), ('٢٧٫٩ ☐ ٢٧٫٨٥', '&gt;'), ('٨٫٥٥ ☐ ٨٫٥٠٨', '&gt;'), ('٥٫٠٥٥ ☐ ٥٫٥٠٥', '&lt;'),
      ('٤٫٥ لتر ☐ ٢٧٠٠ مل', '&gt;<small>٤٥٠٠ مل</small>'), ('٠٫٤٥ طن ☐ ٥٤٧ كغم', '&lt;<small>٤٥٠ كغم</small>'), ('٣٫٥ سم ☐ ٣٤٥ ملم', '&lt;<small>٣٥ ملم</small>'),
      ('٠٫٠٦ كغم ☐ ٥٥٠ غم', '&lt;<small>٦٠ غم</small>'), ('٧٨٠٠ م ☐ ٠٫٨ كم', '&gt;<small>٨٠٠ م</small>'), ('٠٫٠٦٥ م ☐ ٦٫٧ سم', '&lt;<small>٦٫٥ سم</small>')]
S.append(ex(3, 'اكتب &lt; أو &gt;', 'نحوّل إلى الوحدة نفسها، ثم نقارن المنازل', [(f'({h}) {q}', a_) for h, (q, a_) in zip(H, B3)], cols=2))
B4 = [('٦٫٧ لتر ☐ ٦٧٠ مل', '≠<small>٦٧٠٠ مل</small>'), ('٤٫٠٥ طن ☐ ٤٥٠٠ كغم', '≠<small>٤٠٥٠ كغم</small>'), ('٠٫٨٥ كم ☐ ٨٥٠ م', '='), ('٠٫٩٨٥ م ☐ ٩٨٥ سم', '≠<small>٩٨٫٥ سم</small>'),
      ('١٤٫٥ سم ☐ ١٤٥ ملم', '='), ('٢٣٠٠ غم ☐ ٠٫٢٣ كغم', '≠<small>٢٫٣ كغم</small>'), ('٠٫٠٧٢ لتر ☐ ٧٢٠ مل', '≠<small>٧٢ مل</small>'), ('٠٫٥٢ م ☐ ٥٢٠ ملم', '='), ('٠٫٨٥ كغم ☐ ٨٥٠ غم', '=')]
S.append(ex(4, 'اكتب = أو ≠', 'نحوّل إلى الوحدة نفسها ثم نقارن', [(f'({h}) {q}', a_) for h, (q, a_) in zip(H, B4)], cols=2))
S.append(ex(5, 'مسافات السباحة لأحمد وسلطان', 'نحوّل كل المسافات إلى أمتار', [('(أ) مسافة غير ممكنة لسلطان', '٢٥ كم<small>أكبر بكثير من المسافات الأخرى</small>'),
  ('(ب) أطول مسافة لأحمد أكبر بثماني مرات من أقصرها؟', 'نعم<small>٠٫٢ × ٨ = ١٫٦ كم، وأطولها ١٫٦٤ كم</small>'), ('(ج) من يسبح في حمّام طوله ٢٥ م؟', 'سلطان<small>مسافاته كلها مضاعفات للعدد ٢٥</small>')], cols=1, per=2))

# ═══════════ ملحق: حلول كتاب النشاط ص٤٠–٤٢ (الإجابات من دليل المعلم ص٨١) ═══════════
S.append(launch('ab', '٤٠ إلى ٤٢', note='الإجابات النهائية من دليل المعلم ص ٨١'))
NA, NB, NC = 'نشاط ص ٤٠ · تمرين', 'نشاط ص ٤١ · تمرين', 'نشاط ص ٤٢ · تمرين'
A1 = [(('7.36', '3.76', '6.07', '7.63'), ('3.76', '6.07', '7.36', '7.63')), (('8.03', '3.08', '8.11', '5.99'), ('3.08', '5.99', '8.03', '8.11')),
      (('23.4', '19.44', '23.05', '19.42'), ('19.42', '19.44', '23.05', '23.4')), (('1.08', '1.3', '2.11', '1.18'), ('1.08', '1.18', '1.3', '2.11')),
      (('45.454', '45.545', '45.399', '45.933'), ('45.399', '45.454', '45.545', '45.933')), (('5.183', '5.077', '50.44', '5.009'), ('5.009', '5.077', '5.183', '50.44')),
      (('31.425', '31.148', '31.41', '31.14'), ('31.14', '31.148', '31.41', '31.425')), (('7.502', '7.052', '7.02', '7.2'), ('7.02', '7.052', '7.2', '7.502'))]
S.append(ex(1, 'رتّب تصاعدياً', RO, [(f'({h}) {L(*q)}', L(*a_)) for h, (q, a_) in zip(H, A1)], cols=2, src=NA))
A2 = [('٤٫٣ سم ، ٢٧ ملم ، ٠٫٢ سم ، ٧ ملم', '٠٫٢ سم ، ٧ ملم ، ٢٧ ملم ، ٤٫٣ سم'), ('٣٤٫٥ سم ، ٥٠٠ ملم ، ٢٩ سم ، ١٩٫٥ ملم', '١٩٫٥ ملم ، ٢٩ سم ، ٣٤٫٥ سم ، ٥٠٠ ملم'),
      ('٢٠٠٠ غم ، ٧٥٫٧٥ كغم ، ٥٥٥٠ غم ، ٣ كغم', '٢٠٠٠ غم ، ٣ كغم ، ٥٥٥٠ غم ، ٧٥٫٧٥ كغم'), ('١٫٧٥ كغم ، ١٩٧٥ غم ، ٠٫٩ كغم ، ١٨٠٠ غم', '٠٫٩ كغم ، ١٫٧٥ كغم ، ١٨٠٠ غم ، ١٩٧٥ غم'),
      ('٠٫١٢٥ لتر ، ١٠٠ مل ، ٠٫٢ لتر ، ١٥٠ مل', '١٠٠ مل ، ٠٫١٢٥ لتر ، ١٥٠ مل ، ٠٫٢ لتر'), ('٢٥ كم ، ٢٧٥٠ م ، ٠٫٠٥ كم ، ٩٩٩ م', '٠٫٠٥ كم ، ٩٩٩ م ، ٢٧٥٠ م ، ٢٥ كم'),
      ('٥٠٠٠٠ غم ، ٠٫٧٥ طن ، ٣٥٩٩٩٩ غم ، ٥٧٫٧٢٥ كغم ، ١٫٠٠١ طن ، ٥٠٠ كغم ، ٢٠٠ غم', '٢٠٠ غم ، ٥٠٠٠٠ غم ، ٥٧٫٧٢٥ كغم ، ٣٥٩٩٩٩ غم ، ٥٠٠ كغم ، ٠٫٧٥ طن ، ١٫٠٠١ طن')]
S.append(ex(2, 'رتّب القياسات تصاعدياً', 'نحوّل إلى الوحدة نفسها أولاً، ثم نرتّب', [(f'({h}) {q}', a_) for h, (q, a_) in zip(H, A2)], cols=1, per=2, src=NA))
A3 = [('٧٫٢٨ ☐ ٧٫٣٤', '&lt;'), ('٩٫١ ☐ ٩٫٠٣', '&gt;'), ('٠٫٣٣ ☐ ٠٫٠٤', '&gt;'), ('٥٦٫٤ ☐ ٥٦٫٣٥', '&gt;'), ('٠٫٦٦ ☐ ٠٫٦٠٦', '&gt;'), ('٣٫٥٠٥ ☐ ٣٫٧', '&lt;'),
      ('٠٫٧٧ طن ☐ ٨٠٦ كغم', '&lt;<small>٧٧٠ كغم</small>'), ('٧٨٠٠ م ☐ ٠٫٨ كم', '&gt;<small>٨٠٠ م</small>'), ('٣٫٥ كغم ☐ ٣٧٥ غم', '&gt;<small>٣٥٠٠ غم</small>'),
      ('٠٫١٢٥ م ☐ ١٥ سم', '&lt;<small>١٢٫٥ سم</small>'), ('١٥٦٫٣ سم ☐ ١٢٣٤ ملم', '&gt;<small>١٥٦٣ ملم</small>'), ('٠٫٥ لتر ☐ ٧٠٠ مل', '&lt;<small>٥٠٠ مل</small>')]
S.append(ex(3, 'اكتب &lt; أو &gt;', 'نحوّل إلى الوحدة نفسها، ثم نقارن المنازل', [(f'({h}) {q}', a_) for h, (q, a_) in zip(H, A3)], cols=2, src=NA))
A4 = [('٢٠٥٫٥ سم ☐ ٢٥٥ ملم', '≠<small>٢٠٥٥ ملم</small>'), ('٠٫١٢٥ لتر ☐ ١٢٥ مل', '='), ('٥٠٠ غم ☐ ٠٫٠٥ كغم', '≠<small>٥٠ غم</small>'), ('٢٫٧ لتر ☐ ٢٧ مل', '≠<small>٢٧٠٠ مل</small>'),
      ('٠٫٠٥ م ☐ ٥٠ ملم', '='), ('١٠٫٥ طن ☐ ١٠٥٠ كغم', '≠<small>١٠٥٠٠ كغم</small>'), ('٠٫٢٢ كغم ☐ ٢٢٠ غم', '='), ('١٫٧٥ كغم ☐ ١٧٥ متر', '≠<small>كتلة وطول: وحدتان مختلفتان</small>'), ('٠٫١٢٥ م ☐ ١٢٥ سم', '≠<small>١٢٫٥ سم</small>')]
S.append(ex(4, 'اكتب = أو ≠', 'نحوّل إلى الوحدة نفسها ثم نقارن', [(f'({h}) {q}', a_) for h, (q, a_) in zip(H, A4)], cols=2, src=NB))
S.append(ex(5, 'مسافات الركض لفوزي وأمجد', 'نحوّل كل المسافات إلى أمتار', [('(أ) مسافة كتبها فوزي خطأً', '٣٢ كم أو ١٫٦ م<small>٣٢ كم أبعد بكثير، و ١٫٦ م خطوتان فقط</small>'),
  ('(ب) أطول مسافة لأمجد أكبر بعشر مرات من أقصرها؟', 'لا<small>٠٫٥ × ١٠ = ٥ كم، وأطولها ٤ كم فقط</small>'), ('(ج) من يركض حول الحديقة التي طولها ٢٥٠ م؟', 'أمجد<small>مسافاته كلها مضاعفات للعدد ٢٥٠</small>')], cols=1, per=2, src=NB))
S.append(ex(6, 'أعداد من البطاقات ١ و ٢ و ٣', 'نكوّن الأعداد بالفاصلة ونرتّبها تصاعدياً من العدد الكامل الأصغر', [('الأعداد الاثنا عشر', L('1.23', '1.32', '2.13', '2.31', '3.12', '3.21') + '<br>' + L('12.3', '13.2', '21.3', '23.1', '31.2', '32.1') + '<small>أكبر عدد: ٣٢٫١</small>')], cols=1, src=NC))

EXTRA_CSS_OWN = '''
.stps{display:flex;flex-direction:column;gap:1.5vh;align-items:stretch}
.stp{display:flex;align-items:center;gap:1.6vw;justify-content:space-between}
.stp .lab{flex:none;max-width:50%;font-family:var(--fh);font-weight:800;color:#2563EB;background:#EAF1FF;border-radius:12px;padding:.2em .8em;text-align:center;line-height:1.4}
.stp.fin .lab{background:var(--good);color:#fff}
.box .col>.m:not(.mid):not(.sm):not(.big),.hid.col>.m:not(.mid):not(.sm):not(.big){font-size:clamp(34px,6.4vh,76px)}
.pv{border-collapse:separate;border-spacing:0;direction:rtl;font-family:var(--fh);background:#fff;border:3px solid var(--ink);border-radius:14px;overflow:hidden}
.pv th{background:var(--ink);color:#fff;font-weight:800;font-size:clamp(22px,4.3vh,48px);padding:.4em .7em;line-height:1.3}
.pv td{font-weight:900;font-size:clamp(34px,6.4vh,74px);text-align:center;padding:.05em .5em;border-top:2px solid var(--line);min-width:1.4em}
.pv .pt{padding:0 .1em;min-width:0;color:var(--bad);background:#fff}.pv th.pt{background:var(--ink)}
.pv .hi{background:#FFF1D6}.pv th.hi{background:#C77700}
.slots{display:flex;align-items:center;gap:1.6vw;font-family:var(--fh);font-weight:900;font-size:clamp(40px,8vh,96px);direction:rtl}
.slots b{color:var(--bad)}
.errs{display:flex;flex-direction:column;gap:1.4vh;width:min(1400px,92vw)}
.errs .err{display:flex;flex-direction:column;align-items:center;gap:.6vh;background:#fff;border:3px solid var(--line);border-radius:16px;padding:.8vh 1.6vw;font-size:clamp(26px,5vh,58px);font-weight:700}
.errs .err .xq{font-size:inherit}.errs .err .xa{font-size:clamp(24px,4.4vh,50px)}
.syms{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:1.6vw;width:min(1300px,90vw)}
.syms .st>div{display:flex;flex-direction:column;align-items:center;gap:.6vh;background:#fff;border:3px solid var(--line);border-radius:18px;padding:1.4vh .6vw}
.syms b{font-family:var(--fh);font-size:clamp(48px,9vh,104px);color:var(--exp);line-height:1.1}.syms span{font-weight:800;font-size:clamp(24px,4.4vh,50px)}
.lads{display:flex;flex-direction:column;gap:1.6vh;width:min(1400px,92vw)}
.lads .st>div{display:flex;align-items:center;gap:1.6vw;background:#fff;border:3px solid var(--line);border-radius:16px;padding:1vh 1.4vw}
.lads .lt{flex:none;font-weight:900;font-size:clamp(26px,4.8vh,56px);min-width:3.4em;color:var(--base)}
.ladder{display:flex;align-items:center;gap:.6vw;direction:rtl;flex-wrap:wrap}
.lu{font-family:var(--fh);font-weight:900;font-size:clamp(28px,5.4vh,62px);background:#EAF7F8;border:3px solid var(--base);border-radius:12px;padding:.05em .5em}
.lf{display:flex;flex-direction:column;align-items:center;font-family:var(--fh);font-weight:800;font-size:clamp(26px,5.2vh,58px);line-height:1.15}
.lf b{color:var(--good)}.lf i{font-style:normal;color:var(--bad)}
.swim{border-collapse:separate;border-spacing:0;font-weight:800;font-size:clamp(20px,3.6vh,40px);background:#fff;border:3px solid var(--ink);border-radius:12px;overflow:hidden;width:min(900px,62vw)}
.swim th{background:#FBE36B;padding:.2em;}.swim td{text-align:center;padding:.05em;border-top:2px solid var(--line)}.swim td+td,.swim th+th{border-inline-start:2px solid var(--line)}
.swim td.bad{background:#FFF0F0;color:var(--bad)}
.sumg{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:2vw;width:min(1600px,94vw)}
.sumg .col span{font-weight:700;font-size:clamp(26px,4.6vh,56px);line-height:1.4}
.sumg .kk{font-size:clamp(34px,6.4vh,76px)}
.hid.col .kk{font-size:clamp(28px,5.2vh,60px)}
'''
