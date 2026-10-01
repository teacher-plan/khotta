# شرائح درس ٢-٣ «فكّ الأقواس» — الصف السابع (حصتان، كتاب الطالب ص٤٦–٤٧)
# المراجع: دليل المعلم ص٤٩ (نقاط التعلّم، الأخطاء الشائعة: ٤(س + ٣) = ٤س + ٣ …، النشاط: كتابة عبارات بأقواس)، كتاب الطالب ص٤٦–٤٧ (مثال ٢-٣)،
# وإجابات الدليل ص٥٥ (كتاب الطالب) وص٥٩ (كتاب النشاط ص٣٢–٣٣).
# python3.12 gen_powers.py br_slides.py فك_الأقواس_عرض_تفاعلي.html "فكّ الأقواس — الصف السابع"

def STP(lab, expr, cls=''): return st(f'<div class="stp {cls}"><span class="lab">{lab}</span>{expr}</div>')
def STEPS(*rows): return '<div class="stps">' + ''.join(rows) + '</div>'
MI = '<span class="x">−</span>'
def G(*p): return '<span class="grp">(' + ' '.join(p) + ')</span>'      # قوسان حول عبارة
def V(t): return f'<span class="var">{t}</span>'                                   # المتغيّر بلونٍ مميّز
def T(k, v): return f'<span class="term">{k}{V(v)}</span>'                        # حدّ: المعامل ثم المتغيّر
def K(k): return f'<span class="km">{k}</span>'                                    # الحدّ خارج الأقواس
def BR(k, t1, op, t2, arr=False, cls=''):   # k(t1 op t2)، ومع arr تظهر «×k» فوق كل حدٍّ داخل القوسين
    if arr: t1, t2 = (f'<span class="mt"><i>×{k}</i>{t}</span>' for t in (t1, t2))
    return M(K(k), G(t1, op, t2), cls=cls)
def AREA(k, t1, t2, p1, p2, flip=True):     # نموذج المساحة: العرض k والطول t1 + t2
    c = lambda p, n: (f'<button class="flip ac a{n}"><span class="tap">👆</span><span class="hid">{p}</span></button>' if flip else f'<span class="ac a{n}">{p}</span>')
    return f'<div class="area"><span class="a0"></span><span class="ah">{t1}</span><span class="ah">{t2}</span><span class="ak">{k}</span>{c(p1, 1)}{c(p2, 2)}</div>'
S = []
ME = 'إعداد: أ. عيسى الحارثي'
S.append(slide(f'''<span class="tag">الصف السابع · الدرس ٢-٣</span>
<h1 class="h1s">فكّ الأقواس</h1>
<p class="lead">كتاب الطالب ص ٤٦ و ٤٧ · حصتان</p>
<p class="lead" style="font-size:clamp(26px,4.8vh,56px)">{ME}</p>''', 'cover'))
CAN = ['أفهم أنّ <b>٤(س + ٣)</b> تعني ٤ × (س + ٣)', '<b>أفكّ الأقواس</b> بضرب الحدّ الذي خارجها في كل حدٍّ بداخلها', 'أكتشف <b>الأخطاء الشائعة</b> في فكّ الأقواس وأصحّحها']
S.append(slide(f'''<h2>في نهاية هذا الدرس…</h2>
<div class="can">{''.join(f'<div><span class="can-i">✔</span><span><b>أنا أستطيع</b> أن {t}</span></div>' for t in CAN)}</div>'''))
S.append(slide(f'''<h2>مفردات الدرس</h2>
{st('<div class="vocab wide"><div><span>الأقواس</span><i>brackets</i></div><div><span>فكّ الأقواس</span><i>expand</i></div><div><span>الضرب خارج الأقواس</span><i>multiply out</i></div></div>')}
<p class="lead">حصتان: <b class="c-i">أنا</b> ← <b class="c-we">نحن</b> ← <b class="c-u">أنتم</b></p>'''))

# ═══════════ الحصة الأولى: معنى فكّ الأقواس ═══════════
S.append(slide('''<span class="tag">الحصة الأولى · ٤٠ دقيقة</span><h2>معنى فكّ الأقواس</h2>
<div class="plan"><div><b>٥ د</b>تهيئة: ضربٌ ذهني</div><div><b>٥ د</b>معنى القوسين</div><div><b>١٠ د</b>مثال ٢-٣ (أ، ب)</div>
<div><b>٥ د</b>نموذج المساحة</div><div><b>٨ د</b>نحن ← أنتم</div><div><b>٤ د</b>انتبه</div><div><b>٣ د</b>بطاقة الخروج</div></div>''', 'divider'))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">تهيئة 🤔</span></div><h2>احسب ذهنياً: {M('٤', X, '١٣', cls="sm")}</h2>
{box(STEPS(STP('نجزّئ ١٣', M('٤', X, G('١٠', PL, '٣'), cls="sm")), STP('نضرب ٤ في كلٍّ منهما', M('٤', X, '١٠', PL, '٤', X, '٣', cls="sm")), STP('نجمع', M('٤٠', PL, '١٢', EQ, '٥٢', cls="sm"), 'fin')))}''' + tn('من خارج المرجع: تهيئة تمهّد لفكرة الدرس، فنضرب العدد في كل جزءٍ داخل القوسين ثم نجمع. اسأل الطلاب كيف حسبوها قبل كشف الخطوات.')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('كتاب الطالب ص ٤٦')}</div><h2>ماذا تعني {BR('٤', V('ع'), PL, '٣', cls="sm")} ؟</h2>
<div class="row">{st(box(f'<div class="col"><span class="hint">نكتبها عادةً هكذا</span>{BR("٤", V("ع"), PL, "٣")}</div>', style="flex:1;border-color:var(--base)"))}{st(box(f'<div class="col"><span class="hint">ومعناها</span>{M("٤", X, G(V("ع"), PL, "٣"))}</div>', style="flex:1"))}</div>
{st('<div class="note">العدد الملاصق للقوس يعني <b>الضرب</b>، فلا نكتب علامة ×</div>')}'''))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('كتاب الطالب ص ٤٦')}</div><h2>القاعدة</h2>
{st('<div class="rulebox">لفكّ الأقواس نضرب <b class="c-exp">الحدّ الموجود خارج الأقواس</b> في <b>كل حدٍّ</b> بداخلها</div>')}
{st(box(BR('٤', V('ع'), PL, '٣', arr=True, cls="big arrw")))}''' + tn('أشِر بإصبعك من ٤ إلى ع ثم من ٤ إلى ٣: الحدّ خارج القوسين «يزور» كل حدٍّ بداخلهما.')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('مثال ٢-٣ (أ)')}</div><h2>فكّ الأقواس: {BR('٤', V('ع'), PL, '٣', cls="sm")}</h2>
{box(STEPS(STP('نضرب ٤ في ع ثم ٤ في ٣', M('٤', X, V('ع'), PL, '٤', X, '٣', cls="sm")), STP('نبسّط كل حاصل ضرب', M(T('٤', 'ع'), PL, '١٢', cls="sm"), 'fin')))}
{st('<div class="note">٤ × ع نكتبها <b>٤ع</b>، و ٤ × ٣ = <b>١٢</b></div>')}'''))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('مثال ٢-٣ (ب)')}</div><h2>فكّ الأقواس: {BR('٢', V('س'), MI, '٥', cls="sm")}</h2>
{box(STEPS(STP('نضرب ٢ في س ثم ٢ في ٥', M('٢', X, V('س'), MI, '٢', X, '٥', cls="sm")), STP('نبسّط', M(T('٢', 'س'), MI, '١٠', cls="sm"), 'fin')))}
{st('<div class="note">الإشارة بين الحدّين داخل القوسين <b>تبقى كما هي</b></div>')}'''))
S.append(slide(f'''<div class="row hdr">{mode('i')}<span class="qbadge" style="background:#7048E8;box-shadow:0 4px 0 #4C2FB0">نموذج المساحة</span></div><h2>مستطيلٌ عرضه ٤ وطوله ع + ٣</h2>
{st(AREA('٤', V('ع'), '٣', T('٤', 'ع'), '١٢'))}
{st(f'<div class="note">المساحة = {BR("٤", V("ع"), PL, "٣", cls="sm")} = {M(T("٤", "ع"), PL, "١٢", cls="sm")}</div>')}''' + tn('من خارج المرجع: نموذجٌ بصري يوضّح لماذا نضرب ٤ في الحدّين معاً. اضغط كل جزء لتظهر مساحته.')))
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('تمرين ١ (أ)')}</div><h2>معاً: فكّ الأقواس {BR('٢', V('س'), PL, '٥', cls="sm")}</h2>
<button class="flip box col"><span class="tap">👆 الحل</span><span class="hid col">{M('٢', X, V('س'), PL, '٢', X, '٥', cls="sm")}{M(EQ, T('٢', 'س'), PL, '١٠', cls="sm")}</span></button>'''))
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('تمرين ١ (ط)')}</div><h2>معاً: فكّ الأقواس {BR('٦', '٢', PL, V('و'), cls="sm")}</h2>
<button class="flip box col"><span class="tap">👆 الحل</span><span class="hid col">{M('٦', X, '٢', PL, '٦', X, V('و'), cls="sm")}{M(EQ, '١٢', PL, T('٦', 'و'), cls="sm")}</span></button>''' + tn('العدد يأتي أولاً داخل القوسين هنا، فنحافظ على ترتيب الحدّين في الناتج: ١٢ + ٦و.')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ١ (هـ)')}{timer(2)}</div>''' + quiz(f'فكّ الأقواس: {BR("٣", V("ل"), MI, "١")}', [M(T('٣', 'ل'), MI, '٣'), M(T('٣', 'ل'), MI, '١'), M(T('٣', 'ل'), PL, '٣'), M(T('٢', 'ل'))], 0, '٣ × ل = ٣ل ، و ٣ × ١ = ٣ ، والإشارة − تبقى')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ١ (م)')}</div>''' + quiz(f'فكّ الأقواس: {BR("٦", "٢", MI, V("س"))}', [M('١٢', MI, V('س')), M('١٢', MI, T('٦', 'س')), M('٨', MI, T('٦', 'س')), M(T('٦', 'س'))], 1, '٦ × ٢ = ١٢ ، و ٦ × س = ٦س')))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">انتبه ⚠️ أخطاء شائعة</span>{ref('دليل المعلم ص ٤٩')}</div><h2>أيّها صحيح؟</h2>
<div class="errs">{''.join(st(f'<button class="flip err"><span class="xq">{M(*q)}</span><span class="tap">👆</span><span class="hid xa no">{w}</span></button>') for q, w in (
  ([K('٤'), G(V('س'), PL, '٣'), EQ, T('٤', 'س'), PL, '٣'], '✘ لم يضرب ٤ في ٣، والصحيح ٤س + ١٢'),
  ([K('٤'), G(V('س'), PL, '٣'), EQ, T('٤', 'س'), PL, '٧'], '✘ جمع ٤ + ٣ بدل ٤ × ٣، والصحيح ٤س + ١٢'),
  ([K('٣'), G(V('ص'), MI, '١'), EQ, T('٣', 'ص'), PL, '٢'], '✘ طرح ٣ − ١ بدل ٣ × ١، والصحيح ٣ص − ٣')))}</div>''' + tn('الأخطاء الثلاثة من دليل المعلم. اطلب من الطلاب تحديد الخطأ بالكلام قبل الضغط.')))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ١ 🎫</span><h2>فكّ الأقواس</h2>
<div class="exit">{st(f'<div><b>١</b>{BR("٥", V("ك"), PL, "٢", cls="sm")}</div>')}{st(f'<div><b>٢</b>{BR("٧", V("و"), MI, "٣", cls="sm")}</div>')}{st(f'<div><b>٣</b>{BR("٤", "٦", MI, V("د"), cls="sm")}</div>')}</div>'''))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ١ 🎫</span><h2>الإجابات</h2>
<button class="flip box col" style="min-width:40vw"><span class="tap">👆 اضغط لإظهار الإجابات</span><span class="hid col">{M(T('٥', 'ك'), PL, '١٠', cls="sm")}{M(T('٧', 'و'), MI, '٢١', cls="sm")}{M('٢٤', MI, T('٤', 'د'), cls="sm")}</span></button>'''))

# ═══════════ الحصة الثانية: حدودٌ بمعاملات، والأخطاء ═══════════
S.append(slide('''<span class="tag">الحصة الثانية · ٤٠ دقيقة</span><h2>الضرب خارج الأقواس</h2>
<div class="plan"><div><b>٤ د</b>إحماء</div><div><b>٨ د</b>مثال ٢-٣ (ج)</div><div><b>٩ د</b>نحن ← أنتم</div>
<div><b>٦ د</b>اكتشف خطأ سلطان</div><div><b>٥ د</b>أيّها مختلف؟</div><div><b>٥ د</b>تحدٍّ: نكتب الأقواس</div><div><b>٣ د</b>بطاقة الخروج</div></div>''', 'divider'))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">إحماء 🔥</span>{timer(1)}</div>''' + quiz(f'فكّ الأقواس: {BR("٣", V("س"), PL, "٤")}', [M(T('٣', 'س'), PL, '٤'), M(T('٣', 'س'), PL, '١٢'), M(T('٣', 'س'), PL, '٧'), M(T('١٢', 'س'))], 1, '٣ × س = ٣س ، و ٣ × ٤ = ١٢')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('مثال ٢-٣ (ج)')}</div><h2>فكّ الأقواس: {BR('٣', T('٢', 'م'), PL, V('ح'), cls="sm")}</h2>
{box(STEPS(STP('نضرب ٣ في ٢م ثم ٣ في ح', M('٣', X, T('٢', 'م'), PL, '٣', X, V('ح'), cls="sm")), STP('نبسّط', M(T('٦', 'م'), PL, T('٣', 'ح'), cls="sm"), 'fin')))}
{st('<div class="note">٣ × ٢م: نضرب <b>العددين</b> ٣ × ٢ = ٦ ونُبقي المتغيّر، فتصبح <b>٦م</b></div>')}'''))
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('تمرين ٢ (ج)')}</div><h2>معاً بنموذج المساحة: {BR('٥', T('٢', 'و'), PL, '٣', cls="sm")}</h2>
{st(AREA('٥', T('٢', 'و'), '٣', T('١٠', 'و'), '١٥'))}
<button class="flip box col"><span class="tap">👆 الناتج</span><span class="hid">{M(T('١٠', 'و'), PL, '١٥', cls="sm")}</span></button>'''))
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('تمرين ٢ (ح)')}</div><h2>معاً: اضرب خارج الأقواس {BR('٨', T('٣', 'هـ'), MI, '٦', cls="sm")}</h2>
<button class="flip box col"><span class="tap">👆 الحل</span><span class="hid col">{M('٨', X, T('٣', 'هـ'), MI, '٨', X, '٦', cls="sm")}{M(EQ, T('٢٤', 'هـ'), MI, '٤٨', cls="sm")}</span></button>'''))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ٢ (أ)')}{timer(2)}</div>''' + quiz(f'اضرب خارج الأقواس: {BR("٣", T("٢", "س"), PL, "١")}', [M(T('٦', 'س'), PL, '١'), M(T('٥', 'س'), PL, '٤'), M(T('٦', 'س'), PL, '٣'), M(T('٢', 'س'), PL, '٣')], 2, '٣ × ٢س = ٦س ، و ٣ × ١ = ٣')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ٢ (م)')}</div>''' + quiz(f'اضرب خارج الأقواس: {BR("٨", "٣", MI, T("٥", "س"))}', [M('٢٤', MI, T('٥', 'س')), M('١١', MI, T('١٣', 'س')), M('٢٤', PL, T('٤٠', 'س')), M('٢٤', MI, T('٤٠', 'س'))], 3, '٨ × ٣ = ٢٤ ، و ٨ × ٥س = ٤٠س ، والإشارة − تبقى')))
SUL = [((BR('٤', V('س'), PL, '٤')), M(T('٤', 'س'), PL, '٨'), 'جمع ٤ + ٤ بدل ٤ × ٤، والصحيح ٤س + ١٦'),
       ((BR('٢', T('٦', 'س'), MI, '٣')), M(T('١٢', 'س'), MI, '٣'), 'لم يضرب ٢ في ٣، والصحيح ١٢س − ٦'),
       ((BR('٣', '٢', MI, T('٥', 'س'))), M('٦', PL, T('١٥', 'س')), 'غيّر الإشارة − إلى +، والصحيح ٦ − ١٥س'),
       ((BR('٦', '٢', MI, V('س'))), M('١٢', MI, T('٦', 'س'), EQ, T('٦', 'س')), '١٢ و ٦س غير متشابهين، فالناتج ١٢ − ٦س')]
S.append(slide(f'''<div class="row hdr"><span class="qbadge">اكتشف الخطأ 🔍</span>{ref('تمرين ٣')}</div><h2>واجب سلطان: هل إجابته صحيحة؟</h2>
<div class="errs g2">{''.join(st(f'<button class="flip err"><span class="xq">({h}) {q} = {w}</span><span class="tap">👆</span><span class="hid xa no">✘ {why.replace("، ", "،<br>")}</span></button>') for h, (q, w, why) in zip(('أ', 'ب', 'ج', 'د'), SUL))}</div>''' + tn('تعليق الدليل: إذا اتّبع الطلاب طريقةً منهجية في التمرينين ١ و ٢ فسيطبّقونها على حلّ سلطان ويقارنون. الإجابات الأربع كلها خاطئة.')))
DIF = [(BR('٢', T('١٢', 'س'), PL, '١٥'), M(T('٢٤', 'س'), PL, '٣٠')), (BR('٦', '٥', PL, T('٤', 'س')), M('٣٠', PL, T('٢٤', 'س'))),
       (BR('٣', '١٠', PL, T('٨', 'س')), M('٣٠', PL, T('٢٤', 'س'))), (BR('٤', T('٦', 'س'), PL, '٢٦'), M(T('٢٤', 'س'), PL, '١٠٤'))]
S.append(slide(f'''<div class="row hdr"><span class="qbadge">فكّر 💡</span>{ref('تمرين ٤')}</div><h2>أيّ العبارات تختلف عن الأخرى؟</h2>
<div class="difg">{''.join(st(f'<button class="flip box col dif{" odd" if k == 3 else ""}"><span>{q}</span><span class="tap">👆 فكّ</span><span class="hid">{w}</span></button>') for k, (q, w) in enumerate(DIF))}</div>''' + tn('تعليق الدليل: يفكّ الطلاب الأقواس الأربعة أولاً، ثم يقارنون. المختلفة ٤(٦س + ٢٦) = ٢٤س + ١٠٤، والباقي كلها ٢٤س + ٣٠.')))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">تحدٍّ 🧩</span>{ref('نشاط دليل المعلم')}</div><h2>اكتب عبارةً بأقواس ناتج فكّها…</h2>
<div class="errs">{''.join(st(f'<button class="flip err"><span class="xq">{M(*q)}</span><span class="tap">👆</span><span class="hid xa">{w}</span></button>') for q, w in (
  (['١٢', PL, T('٤', 'س')], BR('٤', '٣', PL, V('س'))), ([T('١٨', 'ص'), MI, '٦'], BR('٦', T('٣', 'ص'), MI, '١')), (['٢٠', PL, T('١٠', 'س')], BR('١٠', '٢', PL, V('س')))))}</div>''' + tn('نشاط الدليل: عكس فكّ الأقواس. تُقبل إجاباتٌ أخرى صحيحة، مثل ٢(٦ + ٢س) للأولى. تحقّق من كل إجابة بفكّ أقواسها.')))
S.append(slide(f'''<span class="tag" style="background:#7048E8">للاطّلاع فقط</span><h2>حدٌّ سالب خارج الأقواس: {M(MI + '٣', G(T('٣', 'س'), PL, '٦'), cls="sm")}</h2>
{box(STEPS(STP('سالب × موجب = سالب', M(MI + '٣', X, T('٣', 'س'), EQ, MI + T('٩', 'س'), cls="sm")), STP('سالب × موجب = سالب', M(MI + '٣', X, '٦', EQ, MI + '١٨', cls="sm")), STP('الناتج', M(MI + T('٩', 'س'), MI, '١٨', cls="sm"), 'fin')))}''' + tn('من ورقة «درسي في صفحة» وليس في كتاب الطالب: معلومة إثرائية لا تدخل في زمن الحصة.')))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ٢ 🎫</span><h2>اضرب خارج الأقواس</h2>
<div class="exit">{st(f'<div><b>١</b>{BR("٤", T("٢", "ر"), PL, "٥", cls="sm")}</div>')}{st(f'<div><b>٢</b>{BR("٦", "٣", MI, T("٢", "ك"), cls="sm")}</div>')}{st(f'<div><b>٣</b>{BR("٧", T("٢", "ح"), MI, "٣", cls="sm")}</div>')}</div>'''))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ٢ 🎫</span><h2>الإجابات</h2>
<button class="flip box col" style="min-width:40vw"><span class="tap">👆 اضغط لإظهار الإجابات</span><span class="hid col">{M(T('٨', 'ر'), PL, '٢٠', cls="sm")}{M('١٨', MI, T('١٢', 'ك'), cls="sm")}{M(T('١٤', 'ح'), MI, '٢١', cls="sm")}</span></button>'''))
S.append(slide('''<span class="qbadge" style="background:#0A6770;box-shadow:0 4px 0 #05393E">الواجب المنزلي 🏠</span><h2>بعد الحصتين</h2>
<div class="exit"><div class="st"><div><b>١</b>صفحة ٣٢ في كتاب النشاط (فكّ الأقواس)</div></div><div class="st"><div><b>٢</b>صفحة ٣٣ في كتاب النشاط (خطأ بدر، والعبارة المختلفة)</div></div></div>'''))
S.append(slide(f'''<h2>الخلاصة</h2>
<div class="sumg">
{st(box('<div class="col"><b class="kk c-we">المعنى</b><span>العدد الملاصق للقوس يعني الضرب</span>' + M('٤', X, G(V('س'), PL, '٣')) + '</div>'))}
{st(box('<div class="col"><b class="kk c-exp">القاعدة</b><span>نضرب ما خارج القوس في كل حدّ</span>' + M(T('٤', 'س'), PL, '١٢') + '</div>'))}
{st(box('<div class="col"><b class="kk c-lcm">الإشارة</b><span>تبقى كما هي داخل القوسين</span>' + M(T('٢', 'س'), MI, '١٠') + '</div>'))}</div>'''))

# ═══════════ ملحق: تمارين كتاب الطالب ص٤٦–٤٧ (الإجابات من دليل المعلم ص٥٥) ═══════════
S.append(launch('sb', '٤٦ و ٤٧', note=f'المراجع: كتاب الطالب ص٤٦ و ٤٧، ودليل المعلم ص٤٩ وإجاباته ص٥٥ · {ME}'))
H = ['أ', 'ب', 'ج', 'د', 'هـ', 'و', 'ز', 'ح', 'ط', 'ي', 'ك', 'ل', 'م', 'ن', 'س', 'ع']
RL = 'نضرب الحدّ خارج الأقواس في كل حدٍّ بداخلها، والإشارة تبقى كما هي'
def Q(k, a1, op, a2):   # «ك(أ op ب)» → (السؤال، الخطوة، الناتج)؛ a1 و a2 إمّا عدد وإمّا (معامل، متغيّر)
    f = lambda t: T(*t) if isinstance(t, tuple) else (V(t) if t in VARS else t)
    def mul(t):
        if isinstance(t, tuple): return T(str(int(D(t[0])) * int(D(k))).translate(ARD), t[1]) if t[0] else T(k, t[1])
        return T(k, t) if t in VARS else str(int(D(t)) * int(D(k))).translate(ARD)
    o = PL if op == '+' else MI
    return BR(k, f(a1), o, f(a2)), M(mul(a1), o, mul(a2)), M(K(k), X, f(a1), o, K(k), X, f(a2))
ARD = str.maketrans('0123456789', '٠١٢٣٤٥٦٧٨٩'); D = lambda s: s.translate(str.maketrans('٠١٢٣٤٥٦٧٨٩', '0123456789'))
VARS = set('سصعدوحلطرمكهـ') | {'هـ'}
def EXP(spec): return [(f'({h}) {q}', f'{ans}<small>{stp}</small>') for h, (q, ans, stp) in zip(H, (Q(*s) for s in spec))]
B1 = [('٢', 'س', '+', '٥'), ('٣', 'د', '+', '٦'), ('٤', 'و', '+', '٢'), ('٥', 'ص', '+', '٥'), ('٣', 'ل', '-', '١'), ('٧', 'ح', '-', '٤'), ('٦', 'د', '-', '٩'), ('٢', 'هـ', '-', '٨'),
      ('٦', '٢', '+', 'و'), ('٢', '١', '+', 'ر'), ('٥', '٧', '+', 'ح'), ('٩', '٣', '+', 'ط'), ('٦', '٢', '-', 'س'), ('٢', '١', '-', 'د'), ('٥', '٧', '-', 'ع'), ('٩', '٣', '-', 'ك')]
S.append(ex(1, 'فكّ الأقواس', RL, EXP(B1), cols=2))
B2 = [('٣', ('٢', 'س'), '+', '١'), ('٤', ('٣', 'د'), '+', '٥'), ('٥', ('٢', 'و'), '+', '٣'), ('٦', ('٤', 'ص'), '+', '٧'), ('٢', ('٣', 'ل'), '-', '٤'), ('٤', ('٢', 'ح'), '-', '٣'), ('٦', ('٥', 'د'), '-', '١'), ('٨', ('٣', 'هـ'), '-', '٦'),
      ('٣', '١', '+', ('٢', 'و')), ('٥', '٣', '+', ('٤', 'ر')), ('٧', '٦', '+', ('٧', 'ح')), ('٩', '٥', '+', ('٤', 'ط')), ('٨', '٣', '-', ('٥', 'س')), ('١٢', '٢', '-', ('٣', 'ص')), ('٦', '٥', '-', ('٨', 'ع')), ('٢', '١٣', '-', ('٤', 'ك'))]
S.append(ex(2, 'اضرب خارج الأقواس', 'نضرب الأعداد معاً ونُبقي المتغيّر: ٣ × ٢س = ٦س', EXP(B2), cols=2))
S.append(ex(3, 'هل إجابة سلطان صحيحة؟ ولماذا؟', 'نضرب الحدّ خارج الأقواس في كل حدٍّ بداخلها، ولا نجمع حدوداً غير متشابهة',
  [(f'({h}) {q} = {w}', f'خطأ: {why}') for h, (q, w, why) in zip(('أ', 'ب', 'ج', 'د'), SUL)], cols=2, per=2))
S.append(ex(4, 'أيّ العبارات تختلف عن الأخرى؟ اشرح إجابتك.', 'نفكّ الأقواس الأربعة أولاً ثم نقارن', [(q, w + ('<small>هي المختلفة</small>' if k == 3 else '')) for k, (q, w) in enumerate(DIF)], cols=2))

# ═══════════ ملحق: حلول كتاب النشاط ص٣٢–٣٣ (الإجابات من دليل المعلم ص٥٩) ═══════════
S.append(launch('ab', '٣٢ و ٣٣', note='الإجابات النهائية من دليل المعلم ص ٥٩'))
NA, NB = 'نشاط ص ٣٢ · تمرين', 'نشاط ص ٣٣ · تمرين'
A1 = [('٣', 'ل', '+', '٢'), ('٥', 'ك', '+', '٣'), ('٣', 'ح', '+', '٢'), ('٥', 'د', '-', '١'), ('٤', 'هـ', '-', '٩'), ('٣', 'و', '-', '٨'),
      ('٤', '٢', '+', 'و'), ('٨', '٧', '+', 'ص'), ('٩', '٣', '+', 'ص'), ('٤', '٤', '-', 'س'), ('٧', '١', '-', 'م'), ('٧', '٢', '-', 'و')]
S.append(ex(1, 'فكّ الأقواس', RL, EXP(A1), cols=2, src=NA))
A2 = [('٥', ('٢', 'م'), '+', '١'), ('٧', ('٣', 'س'), '+', '٢'), ('٩', ('٢', 'ص'), '+', '٣'), ('١١', ('٣', 'هـ'), '-', '٤'), ('٢', ('٢', 'ر'), '-', '٥'), ('٤', ('٥', 'س'), '-', '١'),
      ('٦', '١', '+', ('٢', 'و')), ('٨', '٦', '+', ('٤', 'م')), ('١٠', '٦', '+', ('٧', 'ح')), ('٥', '٣', '-', ('٥', 'ط')), ('٥', '٤', '-', ('٣', 'س')), ('٥', '٥', '-', ('٨', 'س'))]
S.append(ex(2, 'اضرب خارج الأقواس', 'نضرب الأعداد معاً ونُبقي المتغيّر', EXP(A2), cols=2, src=NA))
BDR = [(BR('٥', V('م'), PL, '٣'), M(T('٥', 'م'), PL, '٣'), 'نسي أن يضرب ٥ في ٣، والصحيح ٥م + ١٥'),
       (BR('٣', T('٤', 'س'), MI, '٥'), M(T('١٢', 'س'), MI, '٨'), 'جمع ٣ + ٥ بدل ٣ × ٥، والصحيح ١٢س − ١٥'),
       (BR('٤', '٣', MI, V('و')), M('١٢', MI, T('٤', 'و'), EQ, T('٨', 'و')), 'جمع حدّين غير متشابهين، والصحيح ١٢ − ٤و')]
S.append(ex(3, 'اشرح ما الذي أخطأ فيه بدر', 'نضرب الحدّ خارج الأقواس في كل حدٍّ بداخلها، ولا نجمع حدوداً غير متشابهة',
  [(f'({h}) {q} = {w}', f'خطأ: {why}') for h, (q, w, why) in zip(('أ', 'ب', 'ج'), BDR)], cols=1, per=2, src=NB,
  note='إجابات الدليل تطابق ما هنا. وفي كتاب النشاط كُتب حلّ (ب) بالمتغيّر ص بدل س (١٢ص − ٨)، وهو خطأٌ مطبعي.'))
ADF = [(BR('٢', T('٩', 'س'), PL, '١٢'), M(T('١٨', 'س'), PL, '٢٤')), (BR('٢', T('١٠', 'س'), PL, '٨'), M(T('٢٠', 'س'), PL, '١٦')), (BR('٦', '٤', PL, T('٣', 'س')), M('٢٤', PL, T('١٨', 'س'))),
       (BR('٣', '٨', PL, T('٦', 'س')), M('٢٤', PL, T('١٨', 'س'))), (BR('١', T('١٨', 'س'), PL, '٢٤'), M(T('١٨', 'س'), PL, '٢٤'))]
S.append(ex(4, 'أيّ العبارات تختلف عن الباقي؟', 'نفكّ الأقواس كلها ثم نقارن', [(q, w + ('<small>هي المختلفة</small>' if k == 1 else '')) for k, (q, w) in enumerate(ADF)], cols=2, per=3, src=NB))

EXTRA_CSS_OWN = '''
.var{color:var(--exp);font-weight:900}
.km{color:#D9480F;font-weight:900}
.term,.grp{display:inline-flex;direction:rtl;unicode-bidi:isolate;align-items:center}.grp{gap:.2em}
.mt{position:relative;display:inline-flex}
.mt>i{position:absolute;top:-.95em;left:50%;transform:translateX(-50%);font-size:.42em;font-style:normal;font-weight:900;color:#D9480F;background:#FFF1E6;border:2px solid #F5B585;border-radius:10px;padding:0 .35em;white-space:nowrap;line-height:1.3}
.arrw{padding-top:.6em}
.stps{display:flex;flex-direction:column;gap:1.6vh;align-items:stretch}
.stp{display:flex;align-items:center;gap:1.6vw;justify-content:space-between}
.stp .lab{flex:none;font-family:var(--fh);font-weight:800;color:#2563EB;background:#EAF1FF;border-radius:12px;padding:.2em .8em;text-align:center}
.stp.fin .lab{background:var(--good);color:#fff}
.rulebox{font-weight:800;font-size:clamp(28px,5.4vh,64px);background:#EAF7F8;border:4px solid var(--base);border-radius:20px;padding:1.2vh 2vw;text-align:center;line-height:1.5}
.box .col>.m:not(.mid):not(.sm):not(.big),.hid.col>.m:not(.mid):not(.sm):not(.big){font-size:clamp(34px,6.4vh,76px)}
.area{display:grid;grid-template-columns:auto 1.6fr 1fr;grid-template-rows:auto clamp(90px,17vh,200px);gap:0;width:min(1000px,70vw);direction:rtl;font-family:var(--fh);font-weight:900;font-size:clamp(30px,6vh,70px)}
.area .ah{text-align:center;padding-bottom:.2em}.area .ak{display:flex;align-items:center;padding-left:.4em;color:#D9480F}
.area .ac{display:flex;align-items:center;justify-content:center;border:4px solid var(--ink);font:inherit;color:var(--ink);cursor:pointer}
.area .a1{background:#E7F0FF}.area .a2{background:#FFF1E6;border-right:none}
.area button.ac .tap,.area button.ac .hid{font-size:clamp(30px,6vh,70px)}
.errs{display:flex;flex-direction:column;gap:1.4vh;width:min(1400px,92vw)}
.errs .err{display:flex;flex-direction:column;align-items:center;gap:.6vh;background:#fff;border:3px solid var(--line);border-radius:16px;padding:.8vh 1.6vw;font-size:clamp(28px,5.4vh,62px)}
.errs .err .xq{font-size:inherit}.errs .err .xa{font-size:clamp(24px,4.4vh,50px)}.errs.g2{display:grid;grid-template-columns:repeat(2,minmax(0,1fr))}.errs.g2 .err{font-size:clamp(26px,5vh,58px)}.errs .err .tap{font-size:clamp(18px,3vh,32px)}
.difg{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:2vh 2vw;width:min(1300px,90vw)}
.difg .dif{font-size:clamp(30px,5.6vh,64px);font-weight:900;gap:.6vh}.dif .hid{color:var(--good)}.dif.odd.open{border-color:var(--bad);background:#FFF0F0}.dif.odd.open .hid{color:var(--bad)}
.sumg{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:2vw;width:min(1600px,94vw)}
.sumg .col span{font-weight:700;font-size:clamp(26px,4.6vh,56px);line-height:1.4}
.sumg .kk{font-size:clamp(34px,6.4vh,76px)}
'''
