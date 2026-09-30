# شرائح درس ١-١ «الأعداد الصحيحة: العمليات الحسابية على الأعداد الصحيحة» — الصف السابع (٣ حصص، كتاب الطالب ص١٦–٢١)
# المراجع: دليل المعلم ص٢٠–٢٢ (النشاطان ١ و٢، الأخطاء الشائعة)، كتاب الطالب ص١٦–٢١، ورقة «درسي في صفحة» ١-١،
# وإجابات الدليل ص٣٤–٣٥ (كتاب الطالب) وص٤١ (كتاب النشاط ص١٣–١٤).
# python3.12 gen_powers.py int_slides.py الأعداد_الصحيحة_عرض_تفاعلي.html "الأعداد الصحيحة — الصف السابع"
# الرياضيات تُكتب من اليمين لليسار: أول ما يُقرأ هو أول ما يُمرَّر إلى M().

DV = '<span class="x">÷</span>'
MI = '<span class="x">−</span>'
def U(*p): return '<span class="now">' + ' '.join(p) + '</span>'
def BR(*p): return '<span class="brk">(' + ' '.join(p) + ')</span>'
def STP(lab, expr, cls=''): return st(f'<div class="stp {cls}"><span class="lab">{lab}</span>{expr}</div>')
def STEPS(*rows): return '<div class="stps">' + ''.join(rows) + '</div>'
def Z(v): return N(-v) if v < 0 else a(v)                 # عدد صحيح بإشارته
def ZB(v): return BR(N(-v)) if v < 0 else a(v)            # السالب بين قوسين كما في الكتاب
BOX = '<span class="blank">؟</span>'

def pyr(rows, sol=None, inv=False):
    """هرم أعداد: rows من الأعلى إلى الأسفل، وكل صفّ بترتيب القراءة (من اليمين). None = خانة فارغة.
    sol: الصفوف نفسها محلولة — الخانات التي كانت فارغة تظهر ملوّنة. inv: الهرم مقلوب (كتاب النشاط)."""
    def draw(rs, base):
        out = ''
        for i, r in enumerate(rs):
            cells = ''
            for j, v in enumerate(r):
                was_blank = base is not None and base[i][j] is None
                cells += f'<span class="{"new" if was_blank else ""}">{"" if v is None else Z(v)}</span>'
            out += f'<div class="pr">{cells}</div>'
        return f'<div class="pyr{" inv" if inv else ""}">{out}</div>'
    q = draw(rows, None)
    if sol is None: return q
    return f'<button class="flip box col pyrc"><span class="tap">👆 الحل</span>{q}<span class="hid col">{draw(sol, rows)}</span></button>'

def table(op, rows_h, cols_h, given, full=False):
    """جدول عمليات: op رمز العملية، الخانات = f(صف، عمود). given: {(r,c): v} ما يعطيه الكتاب."""
    f = {'−': lambda r, c: r - c, '×': lambda r, c: r * c}[op]
    head = f'<tr><th class="op">{op}</th>' + ''.join(f'<th>{Z(c)}</th>' for c in cols_h) + '</tr>'
    body = ''
    for r in rows_h:
        body += f'<tr><th>{Z(r)}</th>' + ''.join(
            f'<td class="{"g" if (r, c) in given else ("z" if f(r, c) == 0 else ("p" if f(r, c) > 0 else "n"))}">{Z(f(r, c)) if (full or (r, c) in given) else ""}</td>'
            for c in cols_h) + '</tr>'
    return f'<table class="otb">{head}{body}</table>'

S = []
ME = 'إعداد: أ. عيسى الحارثي'
# ═══ الغلاف والأهداف (نقاط التعلّم في دليل المعلم ص٢٠) ═══
S.append(slide(f'''<span class="tag">الصف السابع · الدرس ١-١</span>
<h1 class="h1s">الأعداد الصحيحة</h1>
<p class="lead">العمليات الحسابية على الأعداد الصحيحة · كتاب الطالب ص ١٦–٢١</p>
<p class="lead" style="font-size:clamp(26px,4.8vh,56px)">{ME}</p>''', 'cover'))
CAN = ['أمثّل الأعداد الصحيحة على <b>خط الأعداد</b> وأقارن بينها',
       'أجمع الأعداد الصحيحة <b>الموجبة والسالبة</b>',
       'أطرح بتحويل الطرح إلى <b>جمع المعكوس الجمعي</b>',
       'أضرب الأعداد الصحيحة وأقسمها وأحدّد <b>إشارة الناتج</b>']
S.append(slide(f'''<h2>في نهاية هذا الدرس…</h2>
<div class="can">{''.join(f'<div><span class="can-i">✔</span><span><b>أنا أستطيع</b> أن {t}</span></div>' for t in CAN)}</div>'''))
S.append(slide(f'''<h2>مفردات الدرس</h2>
{st('<div class="vocab wide"><div><span>العدد الصحيح</span><i>integer</i></div><div><span>المعكوس الجمعي</span><i>additive inverse</i></div><div><span>موجب</span><i>positive</i></div><div><span>سالب</span><i>negative</i></div><div><span>خط الأعداد</span><i>number line</i></div><div><span>ناتج الضرب</span><i>product</i></div></div>')}
<p class="lead">ثلاث حصص: <b class="c-i">أنا</b> ← <b class="c-we">نحن</b> ← <b class="c-u">أنتم</b></p>'''))

# ═══════════ الحصة الأولى: الأعداد الصحيحة وجمعها ═══════════
S.append(slide('''<span class="tag">الحصة الأولى · ٤٠ دقيقة</span><h2>الأعداد الصحيحة وجمعها</h2>
<div class="plan"><div><b>٥ د</b>تهيئة: خط الأعداد</div><div><b>٥ د</b>المقارنة</div><div><b>٨ د</b>نمط الجمع وقاعدته</div>
<div><b>١٢ د</b>أنا ← نحن ← أنتم</div><div><b>٥ د</b>انتبه: خطأ شائع</div><div><b>٥ د</b>بطاقة الخروج</div></div>''', 'divider'))
NL = '<div class="nl">' + ''.join(f'<span class="t{" z" if k == 0 else (" ng2" if k < 0 else "")}"><i></i><b>{Z(k)}</b></span>' for k in range(-5, 6)) + '</div>'
S.append(slide(f'''<h2>ما الأعداد الصحيحة؟</h2>
{st('<div class="note">أعدادٌ كاملة قد تكون <b>موجبة</b> أو <b>سالبة</b> — والصفر أيضاً عددٌ صحيح</div>')}
{st(NL)}
{st('<div class="row"><span class="dirr c-we">تزداد القيمة →</span><span class="dirr c-exp">← تتناقص القيمة</span></div>')}'''))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('كتاب الطالب ص ١٦')}</div><h2>أيّهما أكبر: {M('٣')} أم {M(N(5))} ؟</h2>
{st(NL)}
{st(box(M(N(5), '<', '٣', cls="mid")))}
{st('<div class="note">−٥ تقع على <b>يسار</b> ٣ ← إذن −٥ أصغر من ٣</div>')}'''))
S.append(slide(f'''<div class="row hdr">{mode('u')}{timer(1)}</div>''' + quiz(f'أيّهما أكبر: {M(N(2))} أم {M(N(7))} ؟', [M(N(2)), M(N(7))], 0, '−٢ تقع على يمين −٧ على خط الأعداد، فهي الأكبر')))

# نمط الجمع (كتاب الطالب ص١٦)
ADD = [(2, 3), (2, 2), (2, 1), (2, 0), (2, -1), (2, -2), (2, -3), (2, -4)]
S.append(slide(f'''<div class="row hdr"><span class="qbadge">نمط 🔍</span>{ref('كتاب الطالب ص ١٦')}</div><h2>ماذا يحدث عندما نجمع عدداً سالباً؟</h2>
<div class="patt" style="--r:4">{''.join(st(f'<div>{M(Z(p), PL, ZB(q), EQ, Z(p + q))}</div>') for p, q in ADD)}</div>
{st('<div class="note">العدد المضاف يقلّ ١ في كل مرّة ← والناتج يقلّ ١ أيضاً</div>')}'''))
S.append(slide(f'''<h2>قاعدة جمع الأعداد الصحيحة</h2>
<div class="row">
{st(box(f'<div class="col"><b class="kk c-we">إشارتان متشابهتان</b><span class="hint">نجمع ونضع الإشارة نفسها</span>{M(N(2), PL, ZB(-2), EQ, N(4), cls="sm")}{M("٢", PL, "٢", EQ, "٤", cls="sm")}</div>', style="flex:1"))}
{st(box(f'<div class="col"><b class="kk c-exp">إشارتان مختلفتان</b><span class="hint">نطرح ونضع إشارة العدد الأكبر</span>{M("٣", PL, ZB(-7), EQ, N(4), cls="sm")}{M(N(3), PL, "٧", EQ, "٤", cls="sm")}</div>', style="flex:1"))}</div>'''))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('مثال ١-١أ (أ)')}</div><h2>أوجد ناتج: {M('٣', PL, ZB(-7))}</h2>
{box(STEPS(STP('الإشارتان مختلفتان', M('٧', MI, '٣', EQ, '٤', cls="sm")), STP('إشارة الأكبر (٧)', M('٣', PL, ZB(-7), EQ, N(4), cls="sm"), 'fin')))}'''))
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('تمرين ١ (ب)')}</div><h2>معاً: {M(N(3), PL, ZB(-8))}</h2><p class="ask">هل الإشارتان متشابهتان أم مختلفتان؟</p>
{box(STEPS(STP('متشابهتان (سالبتان)', M('٣', PL, '٨', EQ, '١١', cls="sm")), STP('نضع الإشارة نفسها', M(N(3), PL, ZB(-8), EQ, N(11), cls="sm"), 'fin')))}'''))
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('تمرين ١ (ج)')}</div><h2>معاً: {M(N(10), PL, '٤')}</h2>
{box(STEPS(STP('مختلفتان', M('١٠', MI, '٤', EQ, '٦', cls="sm")), STP('إشارة الأكبر (−١٠)', M(N(10), PL, '٤', EQ, N(6), cls="sm"), 'fin')))}'''))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ١ (هـ)')}{timer(2)}</div>''' + quiz(f'أوجد ناتج {M("١٢", PL, ZB(-4))}', [M('١٦'), M('٨'), M(N(8)), M(N(16))], 1, 'إشارتان مختلفتان: ١٢ − ٤ = ٨ ، وإشارة الأكبر (١٢) موجبة')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ٢ (ب)')}</div>''' + quiz(f'أوجد ناتج {M(N(100), PL, ZB(-80))}', [M(N(20)), M('١٨٠'), M(N(180)), M('٢٠')], 2, 'إشارتان متشابهتان: ١٠٠ + ٨٠ = ١٨٠ ، والإشارة سالبة')))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">انتبه ⚠️ خطأ شائع</span>{ref('دليل المعلم ص ٢٠')}</div><h2>{M(N(3), PL, ZB(-5))} = ؟</h2>
<div class="row">
{st(box(f'<div class="col"><span class="wrong">✘</span>{M(N(3), PL, ZB(-5), EQ, "٨", cls="sm")}<small class="hint">«سالب وسالب يعطي موجباً»</small></div>', style="border-color:var(--bad);background:#FFF5F5"))}
{st(box(f'<div class="col"><span class="right">✔</span>{M(N(3), PL, ZB(-5), EQ, N(8), cls="sm")}<small class="hint">في الجمع: متشابهتان ← نجمع ونُبقي الإشارة</small></div>', style="border-color:var(--good);background:#F2FBF5"))}</div>
{st('<div class="note">قاعدة «سالب × سالب = موجب» للضرب والقسمة فقط — لا للجمع!</div>')}'''))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ١ 🎫</span><h2>أجب في دفترك</h2>
<div class="exit">{st(f'<div><b>١</b>أوجد ناتج {M(N(6), PL, ZB(-4))}</div>')}{st(f'<div><b>٢</b>أوجد ناتج {M("٥", PL, ZB(-9))}</div>')}{st(f'<div><b>٣</b>أيّهما أكبر: {M(N(3))} أم {M(N(8))} ؟</div>')}</div>'''))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ١ 🎫</span><h2>الإجابات</h2>
<button class="flip box col" style="min-width:40vw"><span class="tap">👆 اضغط لإظهار الإجابات</span><span class="hid col">{M(N(10), cls="sm")}{M(N(4), cls="sm")}{M(N(3), cls="sm")}</span></button>'''))

# ═══════════ الحصة الثانية: الطرح والمعكوس الجمعي ═══════════
S.append(slide('''<span class="tag">الحصة الثانية · ٤٠ دقيقة</span><h2>طرح الأعداد الصحيحة</h2>
<div class="plan"><div><b>٥ د</b>إحماء</div><div><b>٨ د</b>نشاط ١: نمط الطرح</div><div><b>٥ د</b>المعكوس الجمعي</div>
<div><b>١٢ د</b>أنا ← نحن ← أنتم</div><div><b>٥ د</b>هرم الأعداد</div><div><b>٥ د</b>بطاقة الخروج</div></div>''', 'divider'))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">إحماء 🔥</span>{timer(1)}</div>''' + quiz(f'أوجد ناتج {M(N(7), PL, "٣")}', [M(N(10)), M(N(4)), M('٤'), M('١٠')], 1, 'مختلفتان: ٧ − ٣ = ٤ وإشارة الأكبر (−٧) سالبة')))
SUB = [(4, 5), (4, 4), (4, 3), (4, 2), (4, 1), (4, 0), (4, -1), (4, -2), (4, -3)]
S.append(slide(f'''<div class="row hdr"><span class="qbadge">نشاط ١ 🔍</span>{ref('دليل المعلم ص ٢١')}</div><h2>تابع النمط: ماذا يحدث إذا طرحنا عدداً سالباً؟</h2>
<div class="patt c3" style="--r:3">{''.join(st(f'<div class="{"hot" if q < 0 else ""}">{M("٤", MI, ZB(q), EQ, Z(4 - q))}</div>') for p, q in SUB)}</div>
{st('<div class="note">المطروح يقلّ ١ ← الناتج يزيد ١ … و ٤ − (−٣) = ٤ + ٣ = ٧</div>')}'''))
S.append(slide(f'''<h2>المعكوس الجمعي</h2>
{st('<div class="rulebox">لكل عددٍ صحيح <b class="c-we">س</b> معكوسٌ جمعي <b class="c-exp">−س</b> بحيث: <b>س + (−س) = صفر</b></div>')}
<div class="row">{st(box(M("٣", PL, ZB(-3), EQ, "٠", cls="sm")))}{st(box(M(N(18), PL, "١٨", EQ, "٠", cls="sm")))}</div>
{st('<div class="note">المعكوس الجمعي للعدد ٣ هو −٣ ، وللعدد −١٨ هو ١٨</div>')}'''))
S.append(slide(f'''<h2>الطرح = جمع المعكوس الجمعي</h2>
{st('<div class="rulebox">نبدّل إشارة <b>الطرح</b> بإشارة <b>الجمع</b> ، ونبدّل العدد الثاني <b>بمعكوسه الجمعي</b></div>')}
{st(box(M("٥", MI, ZB(-3), EQ, "٥", PL, "٣", EQ, "٨", cls="mid")))}
{st(box(M("٥", MI, "٨", EQ, "٥", PL, ZB(-8), EQ, N(3), cls="mid")))}'''))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('مثال ١-١أ (ب)')}</div><h2>أوجد ناتج: {M(N(5), MI, '٨')}</h2>
{box(STEPS(STP('معكوس ٨ هو −٨', M(N(5), MI, '٨', EQ, N(5), PL, ZB(-8), cls="sm")), STP('متشابهتان: نجمع', M(EQ, N(13), cls="sm"), 'fin')))}'''))
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('مثال ١-١أ (ج)')}</div><h2>معاً: {M(N(3), MI, ZB(-9))}</h2><p class="ask">ما المعكوس الجمعي للعدد −٩؟</p>
{box(STEPS(STP('معكوس −٩ هو ٩', M(N(3), MI, ZB(-9), EQ, N(3), PL, '٩', cls="sm")), STP('مختلفتان: نطرح', M(EQ, '٦', cls="sm"), 'fin')))}'''))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ٧ (ب)')}{timer(2)}</div>''' + quiz(f'أوجد ناتج {M(N(5), MI, ZB(-3))}', [M(N(8)), M(N(2)), M('٢'), M('٨')], 1, '−٥ − (−٣) = −٥ + ٣ = −٢')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ٤ (د)')}</div>''' + quiz(f'أوجد ناتج {M(N(6), MI, "٦")}', [M('٠'), M('١٢'), M(N(12)), M(N(36))], 2, '−٦ − ٦ = −٦ + (−٦) = −١٢')))
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('تمرين ٨ (أ)')}</div><h2>هرم الأعداد: كل خانة = مجموع الخانتين تحتها</h2>
{pyr([[None], [-2, None], [3, -5, 1]], [[-6], [-2, -4], [3, -5, 1]])}'''))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">فكّر 💡</span>{ref('تمرين ١١ (أ)')}</div><h2>أوجد العدد المفقود: {M(BOX, MI, ZB(-5), EQ, N(2))}</h2>
{st('<p class="ask">نستخدم العملية العكسية: عكس الطرح هو الجمع</p>')}
{st(box(M(N(2), PL, ZB(-5), EQ, N(7), cls="mid")))}
{st(box(M(N(7), MI, ZB(-5), EQ, N(7), PL, '٥', EQ, N(2), cls="sm"), style="border-color:var(--good)"))}'''))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ٢ 🎫</span><h2>أجب في دفترك</h2>
<div class="exit">{st(f'<div><b>١</b>أوجد ناتج {M("٤", MI, ZB(-6))}</div>')}{st(f'<div><b>٢</b>أوجد ناتج {M(N(2), MI, "١٠")}</div>')}{st(f'<div><b>٣</b>أوجد ناتج {M(N(6), MI, ZB(-6))}</div>')}</div>'''))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ٢ 🎫</span><h2>الإجابات</h2>
<button class="flip box col" style="min-width:40vw"><span class="tap">👆 اضغط لإظهار الإجابات</span><span class="hid col">{M("٤", PL, "٦", EQ, "١٠", cls="sm")}{M(N(2), PL, ZB(-10), EQ, N(12), cls="sm")}{M(N(6), PL, "٦", EQ, "٠", cls="sm")}</span></button>'''))

# ═══════════ الحصة الثالثة: الضرب والقسمة ═══════════
S.append(slide('''<span class="tag">الحصة الثالثة · ٤٠ دقيقة</span><h2>ضرب الأعداد الصحيحة وقسمتها</h2>
<div class="plan"><div><b>٥ د</b>إحماء</div><div><b>٨ د</b>نشاط ٢: نمط الضرب</div><div><b>٥ د</b>قاعدة الإشارات</div>
<div><b>١٢ د</b>أنا ← نحن ← أنتم</div><div><b>٥ د</b>فكّر</div><div><b>٥ د</b>بطاقة الخروج</div></div>''', 'divider'))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">إحماء 🔥</span>{timer(1)}</div>''' + quiz(f'أوجد ناتج {M(N(4), MI, ZB(-9))}', [M(N(13)), M('٥'), M(N(5)), M('١٣')], 1, '−٤ − (−٩) = −٤ + ٩ = ٥')))
MUL1 = [3, 2, 1, 0, -1, -2, -3, -4]
S.append(slide(f'''<div class="row hdr"><span class="qbadge">نشاط ٢ 🔍</span>{ref('كتاب الطالب ص ١٩')}</div><h2>تابع النمط: {M(BOX, X, '٥')}</h2>
<div class="patt c2" style="--r:4">{''.join(st(f'<div class="{"hot" if k < 0 else ""}">{M(Z(k), X, "٥", EQ, Z(k * 5))}</div>') for k in MUL1)}</div>
{st('<div class="note">سالب × موجب = <b class="c-exp">سالب</b></div>')}'''))
MUL2 = [4, 3, 2, 1, 0, -1, -2, -3, -4]
S.append(slide(f'''<div class="row hdr"><span class="qbadge">نشاط ٢ 🔍</span>{ref('كتاب الطالب ص ١٩')}</div><h2>تابع النمط: {M(BOX, X, ZB(-3))}</h2>
<div class="patt c3" style="--r:3">{''.join(st(f'<div class="{"hot" if k < 0 else ""}">{M(Z(k), X, ZB(-3), EQ, Z(k * -3))}</div>') for k in MUL2)}</div>
{st('<div class="note">سالب × سالب = <b class="c-we">موجب</b></div>')}'''))
SG = [('+', '+', '+'), ('−', '−', '+'), ('+', '−', '−'), ('−', '+', '−')]
S.append(slide(f'''<h2>قاعدة الإشارات في الضرب والقسمة</h2>
<div class="row" style="align-items:center">
<div class="sgt">{''.join(st(f'<div class="{"p" if r == "+" else "n"}"><b>{x}</b><i>×</i><b>{y}</b><i>=</i><b>{r}</b></div>') for x, y, r in SG)}</div>
{st('<div class="col"><div class="rulebox">إشارتان <b class="c-we">متشابهتان</b> ← الناتج <b class="c-we">موجب</b></div><div class="rulebox">إشارتان <b class="c-exp">مختلفتان</b> ← الناتج <b class="c-exp">سالب</b></div></div>')}</div>
{st('<div class="note">والقاعدة نفسها للقسمة — ولا تنطبق على الجمع والطرح</div>')}'''))
S.append(slide(f'''<h2>القسمة عمليةٌ عكسية للضرب</h2>
{st(box(M(ZB(-3), X, '٤', EQ, N(12), cls="mid")))}
<div class="row">{st(box(M(N(12), DV, '٤', EQ, N(3), cls="sm")))}{st(box(M(N(12), DV, ZB(-3), EQ, '٤', cls="sm")))}</div>
{st('<div class="note">كل عملية ضرب تعطينا عمليتي قسمة</div>')}'''))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('مثال ١-١ب (أ) و (ب)')}</div><h2>أوجد: {M('١٢', X, ZB(-3))} و {M(N(8), X, ZB(-5))}</h2>
{box(STEPS(STP('مختلفتان ← سالب', M('١٢', X, ZB(-3), EQ, N(36), cls="sm")), STP('متشابهتان ← موجب', M(N(8), X, ZB(-5), EQ, '٤٠', cls="sm"), 'fin')))}'''))
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('مثال ١-١ب (ج) و (د)')}</div><h2>معاً: {M(N(20), DV, '٤')} و {M(N(24), DV, ZB(-6))}</h2><p class="ask">الإشارتان أولاً… ثم العدد</p>
{box(STEPS(STP('مختلفتان ← سالب', M(N(20), DV, '٤', EQ, N(5), cls="sm")), STP('متشابهتان ← موجب', M(N(24), DV, ZB(-6), EQ, '٤', cls="sm"), 'fin')))}'''))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ١ (ج)')}{timer(2)}</div>''' + quiz(f'أوجد ناتج {M(N(4), X, ZB(-5))}', [M(N(20)), M('٢٠'), M(N(9)), M('٩')], 1, 'إشارتان متشابهتان ← موجب: ٤ × ٥ = ٢٠')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ٢ (ب)')}</div>''' + quiz(f'أوجد ناتج {M(N(30), DV, "٦")}', [M('٥'), M(N(5)), M(N(24)), M('٣٦')], 1, 'إشارتان مختلفتان ← سالب: ٣٠ ÷ ٦ = ٥')))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">انتبه ⚠️ خطأ شائع</span>{ref('دليل المعلم ص ٢٠')}</div><h2>قواعد الجمع غير قواعد الضرب!</h2>
<div class="row">
{st(box(f'<div class="col"><b class="kk">جمع</b>{M(N(3), PL, ZB(-5), EQ, N(8), cls="mid")}<small class="hint">متشابهتان ← نجمع ونُبقي الإشارة</small></div>', style="flex:1"))}
{st(box(f'<div class="col"><b class="kk">ضرب</b>{M(N(3), X, ZB(-5), EQ, "١٥", cls="mid")}<small class="hint">متشابهتان ← الناتج موجب</small></div>', style="flex:1;border-color:var(--exp)"))}</div>'''))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">فكّر 💡</span>{ref('تمرين ٧')}</div><h2>ما العددان الصحيحان؟ {M('○', X, '△', EQ, N(12))}</h2>
<button class="flip box col"><span class="tap">👆 اضغط لإظهار الأزواج الستة</span><span class="hid col">{M('١', X, ZB(-12), '، ', N(1), X, '١٢', cls="sm")}{M('٢', X, ZB(-6), '، ', N(2), X, '٦', cls="sm")}{M('٣', X, ZB(-4), '، ', N(3), X, '٤', cls="sm")}<small class="hint">إشارتان مختلفتان دائماً لأن الناتج سالب</small></span></button>'''))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ٣ 🎫</span><h2>أجب في دفترك</h2>
<div class="exit">{st(f'<div><b>١</b>أوجد ناتج {M("٥", X, ZB(-4))}</div>')}{st(f'<div><b>٢</b>أوجد ناتج {M(N(50), DV, ZB(-5))}</div>')}{st(f'<div><b>٣</b>أوجد ناتج {M("١٦", DV, ZB(-4))}</div>')}</div>'''))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ٣ 🎫</span><h2>الإجابات</h2>
<button class="flip box col" style="min-width:40vw"><span class="tap">👆 اضغط لإظهار الإجابات</span><span class="hid col">{M(N(20), cls="sm")}{M("١٠", cls="sm")}{M(N(4), cls="sm")}</span></button>'''))
S.append(slide('''<span class="qbadge" style="background:#0A6770;box-shadow:0 4px 0 #05393E">الواجب المنزلي 🏠</span><h2>بعد كل حصة</h2>
<div class="exit"><div class="st"><div><b>١</b>بعد الحصتين الأولى والثانية: صفحة ١٣ في كتاب النشاط</div></div><div class="st"><div><b>٢</b>بعد الحصة الثالثة: صفحة ١٤ في كتاب النشاط</div></div></div>'''))
S.append(slide(f'''<h2>الخلاصة</h2>
<div class="sumg">
{st(box('<div class="col"><b class="kk c-we">الجمع</b><span>متشابهتان: نجمع ونُبقي الإشارة</span><span>مختلفتان: نطرح ونضع إشارة الأكبر</span></div>'))}
{st(box('<div class="col"><b class="kk c-exp">الطرح</b><span>نجمع المعكوس الجمعي</span>' + M("٥", MI, ZB(-3), EQ, "٥", PL, "٣") + '</div>'))}
{st(box('<div class="col"><b class="kk c-lcm">الضرب والقسمة</b><span>متشابهتان ← موجب</span><span>مختلفتان ← سالب</span></div>'))}</div>'''))

# ═══════════ ملحق: تمارين كتاب الطالب ص١٧–٢١ ═══════════
S.append(launch('sb', '١٧ إلى ٢١', note=f'المراجع: كتاب الطالب ص١٦–٢١ ودليل المعلم ص٢٠–٢٢ وإجاباته ص٣٤–٣٥ — {ME}'))
RA = 'متشابهتان: نجمع ونُبقي الإشارة · مختلفتان: نطرح ونضع إشارة الأكبر'
RS = 'الطرح = جمع المعكوس الجمعي'
RM = 'متشابهتان ← موجب · مختلفتان ← سالب'
def OPQ(x, op, y):  # سؤال + حل
    if op == '+': return M(Z(x), PL, ZB(y)), M(Z(x), PL, ZB(y), EQ, Z(x + y))
    if op == '-': return M(Z(x), MI, ZB(y)), M(Z(x), PL, ZB(-y), EQ, Z(x - y))
    if op == '*': return M(Z(x), X, ZB(y)), M(EQ, Z(x * y))
    if op == '/': return M(Z(x), DV, ZB(y)), M(EQ, Z(x // y))
L5 = ['(أ)', '(ب)', '(ج)', '(د)', '(هـ)', '(و)']
def parts(items):
    out = []
    for k, (x, op, y) in enumerate(items):
        q, s = OPQ(x, op, y); out.append((L5[k] + ' ' + q, s))
    return out
S.append(ex(1, 'أوجد ناتج عمليات الجمع', RA, parts([(3, '+', -6), (-3, '+', -8), (-10, '+', 4), (-10, '+', -7), (12, '+', -4)]), cols=2, src='تمرين ١-١أ'))
S.append(ex(2, 'أوجد ناتج الجمع', RA, parts([(30, '+', -20), (-100, '+', -80), (-20, '+', 5), (-30, '+', -70), (45, '+', -40)]), cols=2, src='تمرين ١-١أ'))
S.append(ex(3, M(N(1132), PL, ZB(-471), EQ, N(1603)) + ' ، فأوجد ' + M(N(1132), PL, ZB(-472)), 'العدد الثاني أصغر بواحد ← الناتج أصغر بواحد', [('الناتج', M(N(1603), MI, '١', EQ, N(1604)))], cols=1, src='تمرين ١-١أ'))
S.append(ex(4, 'أوجد ناتج الطرح', RS, parts([(4, '-', 6), (-4, '-', 6), (6, '-', 4), (-6, '-', 6), (-2, '-', 10)]), cols=2, src='تمرين ١-١أ'))
S.append(ex(5, M('٤١٩', MI, ZB(-283), EQ, '٧٠٢') + ' ، فأوجد ' + M('٤١٩', MI, ZB(-284)), 'نطرح عدداً أصغر بواحد (−٢٨٤) ← الناتج أكبر بواحد', [('الناتج', M('٤١٩', PL, '٢٨٤', EQ, '٧٠٣'))], cols=1, src='تمرين ١-١أ'))
S.append(ex(6, 'أوجد ناتج كلٍّ مما يلي', RS, parts([(4, '-', -6), (-4, '-', -6), (8, '-', -2), (12, '-', -10)]), cols=2, src='تمرين ١-١أ'))
S.append(ex(7, 'أوجد ناتج الطرح', RS, parts([(7, '-', -2), (-5, '-', -3), (12, '-', -4), (-6, '-', -6), (-2, '-', -10)]), cols=2, src='تمرين ١-١أ'))
PY8 = [([[None], [-2, None], [3, -5, 1]], [[-6], [-2, -4], [3, -5, 1]]),
       ([[None], [None, None], [-2, -3, 5]], [[-3], [-5, 2], [-2, -3, 5]]),
       ([[None], [None, None], [2, -4, -6]], [[-12], [-2, -10], [2, -4, -6]]),
       ([[3], [2, None], [-3, None, None]], [[3], [2, 1], [-3, 5, -4]]),
       ([[-7], [None, -6], [None, None, 2]], [[-7], [-1, -6], [7, -8, 2]])]
for k0 in (0, 3):
    S.append(slide(f'''<div class="xhead"><span class="xnum">📘 تمرين ٨</span><h2>هرم الأعداد: كل خانة = مجموع الخانتين تحتها</h2></div>
<div class="row">{''.join(f'<div class="col"><b class="kk">{L5[k]}</b>{pyr(q, s)}</div>' for k, (q, s) in enumerate(PY8) if k0 <= k < k0 + 3)}</div>'''))
T9 = dict(rows=[4, 2, 0, -2, -4], cols=[-4, -2, 0, 2, 4])
S.append(slide(f'''<div class="xhead"><span class="xnum">📘 تمرين ٩</span><h2>أكمل الجدول: العدد الأوّل − العدد الثاني</h2></div>
<button class="flip box col tbc"><span class="tap">👆 الحل</span>{table('−', T9['rows'], T9['cols'], {(4, -4): 8, (-4, 2): -6})}<span class="hid col">{table('−', T9['rows'], T9['cols'], {(4, -4): 8, (-4, 2): -6}, full=True)}</span></button>'''))
S.append(ex(10, 'أوجد ناتج ما يلي', 'حدّد العملية أولاً، ثم طبّق قاعدتها', parts([(5, '+', -3), (-4, '-', -5), (-2, '+', 18), (-10, '-', 4)]), cols=2, src='تمرين ١-١أ'))
S.append(ex(11, 'أوجد العدد المفقود', 'نستخدم العملية العكسية ثم نتحقّق', [
  ('(أ) ' + M(BOX, MI, ZB(-5), EQ, N(2)), M(N(2), PL, ZB(-5), EQ, N(7))), ('(ب) ' + M(N(2), PL, BOX, EQ, '٢'), M('٢', MI, ZB(-2), EQ, '٤')),
  ('(ج) ' + M(BOX, MI, '٤', EQ, N(3)), M(N(3), PL, '٤', EQ, '١'))], cols=2, src='تمرين ١-١أ'))
S.append(ex(1, 'أوجد ناتج الضرب', RM, parts([(5, '*', -4), (-8, '*', 6), (-4, '*', -5), (-6, '*', -10), (-2, '*', 20)]), cols=2, src='تمرين ١-١ب'))
S.append(ex(2, 'أوجد ناتج القسمة', RM, parts([(20, '/', -10), (-30, '/', 6), (-12, '/', -4), (-50, '/', -5), (16, '/', -4)]), cols=2, src='تمرين ١-١ب'))
S.append(ex(3, 'أوجد ناتج كلٍّ مما يلي', RM, parts([(4, '*', -10), (-20, '/', 5), (-20, '*', 5), (-40, '/', -8), (-12, '*', -4)]), cols=2, src='تمرين ١-١ب'))
S.append(ex(4, 'اكتب عبارتي قسمة لكل عبارة ضرب', 'كل عملية ضرب تعطي عمليتي قسمة', [
  ('(أ) ' + M('٥', X, ZB(-3), EQ, N(15)), M(N(15), DV, '٥', EQ, N(3)) + M(N(15), DV, ZB(-3), EQ, '٥')),
  ('(ب) ' + M(N(8), X, ZB(-4), EQ, '٣٢'), M('٣٢', DV, ZB(-8), EQ, N(4)) + M('٣٢', DV, ZB(-4), EQ, N(8))),
  ('(ج) ' + M(N(6), X, '٧', EQ, N(42)), M(N(42), DV, ZB(-6), EQ, '٧') + M(N(42), DV, '٧', EQ, N(6)))], cols=2, src='تمرين ١-١ب'))
T5 = [3, 2, 1, 0, -1, -2, -3]
S.append(slide(f'''<div class="xhead"><span class="xnum">📘 تمرين ١-١ب ٥</span><h2>أكمل جدول الضرب</h2></div>
<button class="flip box col tbc sm7"><span class="tap">👆 الحل (أخضر: صفر · أزرق: موجب · أحمر: سالب)</span>{table('×', T5, [-3, -2, -1, 0, 1, 2, 3], {(3, 2): 6, (1, -2): -2, (-1, -3): 3})}<span class="hid col">{table('×', T5, [-3, -2, -1, 0, 1, 2, 3], {(3, 2): 6, (1, -2): -2, (-1, -3): 3}, full=True)}</span></button>'''))
PY6 = [([[None], [-6, None], [2, -3, -2]], [[-36], [-6, 6], [2, -3, -2]]),
       ([[None], [None, None], [-4, 5, -1]], [[100], [-20, -5], [-4, 5, -1]]),
       ([[48], [-12, None], [-3, None, None]], [[48], [-12, -4], [-3, 4, -1]]),
       ([[64], [None, -16], [None, 2, None]], [[64], [-4, -16], [-2, 2, -8]])]
for k0 in (0, 2):
    S.append(slide(f'''<div class="xhead"><span class="xnum">📘 تمرين ١-١ب ٦</span><h2>كل خانة = ناتج ضرب الخانتين تحتها</h2></div>
<div class="row">{''.join(f'<div class="col"><b class="kk">{L5[k]}</b>{pyr(q, s)}</div>' for k, (q, s) in enumerate(PY6) if k0 <= k < k0 + 2)}</div>'''))
S.append(ex(7, M('○', X, '△', EQ, N(12)), 'الناتج سالب ← الإشارتان مختلفتان', [
  ('(أ) الأعداد', M('١', X, ZB(-12)) + M('٢', X, ZB(-6)) + M('٣', X, ZB(-4))), ('…', M(N(1), X, '١٢') + M(N(2), X, '٦') + M(N(3), X, '٤')),
  ('(ب) عدد الأزواج', M('٦') + '<small>ستة أزواج مختلفة</small>')], cols=2, src='تمرين ١-١ب'))
S.append(ex(8, 'أوجد ناتج كلٍّ مما يلي', RM, parts([(5, '*', -3), (-6, '*', 2), (-3, '*', -3), (-60, '/', -10), (20, '/', -5), (-18, '/', 6)]), cols=2, src='تمرين ١-١ب'))
S.append(ex(9, 'اكتب الأعداد المفقودة', 'نستخدم العملية العكسية', [
  ('(أ) ' + M('٤', X, BOX, EQ, N(20)), M(N(20), DV, '٤', EQ, N(5))), ('(ب) ' + M(BOX, DV, ZB(-2), EQ, N(6)), M(N(6), X, ZB(-2), EQ, '١٢')),
  ('(ج) ' + M('٤', X, BOX, EQ, '١٢'), M('١٢', DV, '٤', EQ, '٣')), ('(د) ' + M(BOX, X, ZB(-3), EQ, '١٢'), M('١٢', DV, ZB(-3), EQ, N(4))),
  ('(هـ) ' + M(N(30), MI, BOX, EQ, '٥'), M(N(30), MI, '٥', EQ, N(35))), ('(و) ' + M(BOX, DV, ZB(-3), EQ, '٧'), M('٧', X, ZB(-3), EQ, N(21)))], cols=2, src='تمرين ١-١ب'))

# ═══════════ ملحق: حلول كتاب النشاط ص١٣–١٤ (الإجابات من دليل المعلم ص٤١) ═══════════
S.append(launch('ab', '١٣ و ١٤', note='الإجابات النهائية من دليل المعلم ص ٤١'))
NA, NB = 'نشاط ص ١٣ · تمرين', 'نشاط ص ١٤ · تمرين'
S.append(ex(1, 'أوجد ناتج كلٍّ مما يلي', RA, parts([(6, '+', -3), (-6, '+', -4), (-2, '+', -8), (-1, '+', 6), (-10, '+', 4)]), cols=2, src=NA))
S.append(ex(2, 'أوجد العدد الصحيح المفقود', 'العدد المفقود = الناتج − العدد المعلوم', [
  ('(أ) ' + M('٥', PL, BOX, EQ, '٢'), M('٢', MI, '٥', EQ, N(3))), ('(ب) ' + M('٤', PL, BOX, EQ, N(6)), M(N(6), MI, '٤', EQ, N(10))),
  ('(ج) ' + M(N(3), PL, BOX, EQ, '٣'), M('٣', MI, ZB(-3), EQ, '٦')), ('(د) ' + M(N(12), PL, BOX, EQ, N(8)), M(N(8), MI, ZB(-12), EQ, '٤')),
  ('(هـ) ' + M('٧', PL, BOX, EQ, N(6)), M(N(6), MI, '٧', EQ, N(13)))], cols=2, src=NA))
S.append(ex(3, 'أوجد ناتج الطرح', RS, parts([(3, '-', 7), (-3, '-', 7), (-20, '-', 30), (5, '-', 15), (-9, '-', 4)]), cols=2, src=NA))
S.append(ex(4, 'أوجد ناتج الطرح', RS, parts([(4, '-', -6), (10, '-', -3), (-10, '-', -5), (-6, '-', -12), (15, '-', -10)]), cols=2, src=NA))
PA5 = [([[3, -5, 4], [-2, None], [None]], [[3, -5, 4], [-2, -1], [-3]]),
       ([[-4, 2, -1], [None, None], [None]], [[-4, 2, -1], [-2, 1], [-1]]),
       ([[-1, 4, -6], [None, None], [None]], [[-1, 4, -6], [3, -2], [1]])]
S.append(slide(f'''<div class="xhead"><span class="xnum">📘 {NA} ٥</span><h2>كل خانة = مجموع الخانتين فوقها</h2></div>
<div class="row">{''.join(f'<div class="col"><b class="kk">{L5[k]}</b>{pyr(q, s, inv=True)}</div>' for k, (q, s) in enumerate(PA5))}</div>'''))
S.append(slide(f'''<div class="xhead"><span class="xnum">📘 {NB} ١</span><h2>أكمل جدول الضرب</h2></div>
<button class="flip box col tbc"><span class="tap">👆 الحل</span>{table('×', [-3, -1, 2, 5], [-3, -1, 2, 5], {(5, 5): 25})}<span class="hid col">{table('×', [-3, -1, 2, 5], [-3, -1, 2, 5], {(5, 5): 25}, full=True)}</span></button>'''))
S.append(ex(2, 'أكمل عمليات القسمة', RM, parts([(20, '/', -2), (-24, '/', 3), (-44, '/', -4), (28, '/', -4), (-12, '/', -6)]), cols=2, src=NB))
S.append(ex(3, 'اكتب عمليتي قسمة من ' + M(N(5), X, '٦', EQ, N(30)), 'كل عملية ضرب تعطي عمليتي قسمة', [
  ('القسمة الأولى', M(N(30), DV, '٦', EQ, N(5))), ('القسمة الثانية', M(N(30), DV, ZB(-5), EQ, '٦'))], cols=2, src=NB))
S.append(ex(4, 'راشد: «٥ × ٥ = ٢٥ ، إذن −٥ × (−٥) = −٢٥» — هل هو على صواب؟', RM, [
  ('الإجابة', '<b>لا</b>' + M(N(5), X, ZB(-5), EQ, '٢٥') + '<small>إشارتان متشابهتان ← الناتج موجب</small>')], cols=1, src=NB))
S.append(ex(5, 'ناتج ضرب عددين صحيحين مختلفين = −١٦ ، فما العددان؟', 'الناتج سالب ← إشارتان مختلفتان', [
  ('الأزواج الممكنة', M('١', X, ZB(-16)) + M(N(1), X, '١٦') + M('٢', X, ZB(-8))), ('و', M(N(2), X, '٨') + M(N(4), X, '٤') + '<small>أيّ زوجٍ منها</small>')], cols=2, src=NB))
S.append(ex(6, 'أوجد الأعداد المفقودة', 'نستخدم القسمة (العملية العكسية)', [
  ('(أ) ' + M(N(2), X, BOX, EQ, '٢٠'), M('٢٠', DV, ZB(-2), EQ, N(10))), ('(ب) ' + M('٤', X, BOX, EQ, N(12)), M(N(12), DV, '٤', EQ, N(3))),
  ('(ج) ' + M(BOX, X, '٩', EQ, N(45)), M(N(45), DV, '٩', EQ, N(5))), ('(د) ' + M(BOX, X, ZB(-5), EQ, N(35)), M(N(35), DV, ZB(-5), EQ, '٧'))], cols=2, src=NB))

EXTRA_CSS_OWN = '''
.now{display:inline-flex;gap:.28em;align-items:baseline;border-bottom:.09em solid var(--exp);padding-bottom:.02em}
.brk{display:inline-flex;gap:.2em;align-items:baseline;direction:rtl;unicode-bidi:isolate}
.stps{display:flex;flex-direction:column;gap:1.6vh;align-items:stretch}
.stp{display:flex;align-items:center;gap:1.4vw;justify-content:space-between}
.stp .lab{flex:none;font-family:var(--fh);font-weight:800;color:#2563EB;background:#EAF1FF;border-radius:12px;padding:.2em .8em;text-align:center}
.stp.fin .lab{background:var(--good);color:#fff}.stp.fin .m{color:var(--good)}
.nl{display:flex;direction:ltr;align-items:flex-start;width:min(1500px,92vw);border-top:.5vh solid var(--ink);position:relative;margin-top:2vh}
.nl::before,.nl::after{content:'';position:absolute;top:-1.6vh;border:1.4vh solid transparent}
.nl::before{left:-1.6vh;border-right-color:var(--ink);border-left:0}.nl::after{right:-1.6vh;border-left-color:var(--ink);border-right:0}
.nl .t{flex:1;display:flex;flex-direction:column;align-items:center}
.nl .t>i{width:.5vh;height:2.4vh;background:var(--ink);margin-top:-1.4vh}
.nl .t b{font-family:var(--fh);font-size:clamp(34px,7vh,84px);font-weight:800;color:var(--ink)}
.nl .t.ng2 b{color:var(--exp)}.nl .t.z b{color:var(--ink2)}
.dirr{font-family:var(--fh);font-weight:800;font-size:clamp(28px,5.4vh,62px);padding:0 2vw}
.patt{display:grid;grid-auto-flow:column;grid-template-rows:repeat(var(--r,4),auto);grid-template-columns:repeat(2,minmax(0,1fr));gap:1.2vh 4vw;font-size:clamp(34px,6.4vh,76px)}
.patt.c3{grid-template-columns:repeat(3,minmax(0,1fr));font-size:clamp(30px,5.6vh,66px)}
.patt.c2{grid-template-columns:repeat(2,minmax(0,1fr))}
.patt>div>div{display:flex;justify-content:center}.patt .hot .m{color:var(--exp)}
.rulebox{font-weight:800;font-size:clamp(30px,5.8vh,68px);background:#EAF7F8;border:4px solid var(--base);border-radius:20px;padding:1.4vh 2vw;text-align:center;line-height:1.5}
.pyr{display:flex;flex-direction:column;align-items:center;font-family:var(--fh);font-weight:800;font-size:clamp(34px,7.4vh,86px)}
.pyr .pr{display:flex;direction:rtl}
.pyr .pr>span{width:2.3em;height:1.5em;border:.06em solid var(--ink);margin:-.03em;display:flex;align-items:center;justify-content:center;background:#fff;color:var(--ink)}
.pyr .pr>span.new{background:#D9F2E3 !important;color:var(--good) !important}.pyr .pr>span.new *{color:var(--good) !important}
.pyrc{padding:1vh 1.4vw}.pyrc .tap{order:3}.pyrc.open>.pyr{display:none}
.nl .t b{direction:rtl;unicode-bidi:isolate}
.otb{border-collapse:collapse;font-family:var(--fh);font-weight:800;font-size:clamp(34px,7vh,84px);direction:rtl}
.otb th,.otb td{border:.05em solid var(--ink);min-width:2.3em;height:1.35em;text-align:center;padding:0 .2em}
.otb th{background:#FFF3C4}.otb th.op{background:var(--ink);color:#fff}
.otb td.g{background:#fff;color:var(--ink)}.otb td.p{color:#2563EB}.otb td.n{color:var(--bad)}.otb td.z{color:var(--good);background:#E6F6EC}
.tbc{padding:1.2vh 1.4vw}.tbc>.otb{display:table}
.tbc .hid .otb{margin-top:0}.tbc.open>.otb{display:none}
.sm7 .otb{font-size:clamp(30px,5.8vh,68px)}
.sgt{display:flex;flex-direction:column;gap:1vh;font-family:var(--fh);font-weight:900;font-size:clamp(40px,8vh,96px)}
.sgt .st>div,.sgt>div{display:flex;gap:.5em;align-items:center;justify-content:center;background:#fff;border:4px solid;border-radius:18px;padding:.1em .6em}
.sgt .p{border-color:var(--good)}.sgt .p b:last-child{color:var(--good)}.sgt .n{border-color:var(--bad)}.sgt .n b:last-child{color:var(--bad)}
.sgt i{font-style:normal;color:var(--ink2)}
.sumg{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:2vw;width:min(1600px,94vw)}
.sumg .col span{font-weight:700;font-size:clamp(28px,5.4vh,64px);line-height:1.4}
.sumg .kk{font-size:clamp(36px,7vh,84px)}
'''
