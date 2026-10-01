# شرائح درس ٢-٥ «كتابة المعادلات وحلّها» — الصف السابع (٣ حصص، كتاب الطالب ص٥١–٥٣)
# المراجع: دليل المعلم ص٥٢–٥٣ (الميزان ذو الكفتين، العمليات العكسية، الأخطاء الشائعة، النشاط: كتابة ستة أسئلة «أفكّر في عدد»)،
# كتاب الطالب ص٥١–٥٣ (مثال ٢-٥)، وإجابات الدليل ص٥٦ (كتاب الطالب) وص٦٠ (كتاب النشاط ص٣٧–٣٩).
# python3.12 gen_powers.py eq_slides.py كتابة_المعادلات_وحلها_عرض_تفاعلي.html "كتابة المعادلات وحلّها — الصف السابع"

def STP(lab, expr, cls=''): return st(f'<div class="stp {cls}"><span class="lab">{lab}</span>{expr}</div>')
def STEPS(*rows): return '<div class="stps">' + ''.join(rows) + '</div>'
MI = '<span class="x">−</span>'; DV = '<span class="x">÷</span>'
def V(t): return f'<span class="var">{t}</span>'
def T(k, v): return f'<span class="term">{k}{V(v)}</span>'
def FR(n, d): return f'<span class="fr"><span>{n}</span><span>{d}</span></span>'
def OP(t): return f'<span class="opb">{t}</span>'                                 # العملية المضافة إلى الطرفين
def BAL(l, r, cls=''):   # ميزان: الكفّة اليمنى = الطرف الأيمن من المعادلة (يُكتب أولاً)
    return f'<div class="bal {cls}"><div class="pans"><div class="pan">{l}</div><div class="pan">{r}</div></div><div class="beam"></div><div class="post"></div></div>'
def BARS(segs, total):   # مستطيلات متجاورة بأطوالها، وتحتها الطول الكلي
    return '<div class="sbar"><div class="segs">' + ''.join(f'<span class="{c}" style="flex:{f}">{t}</span>' for t, f, c in segs) + f'</div><div class="tot">{total}</div></div>'
S = []
ME = 'إعداد: أ. عيسى الحارثي'
S.append(slide(f'''<span class="tag">الصف السابع · الدرس ٢-٥</span>
<h1 class="h1s">كتابة المعادلات وحلّها</h1>
<p class="lead">كتاب الطالب ص ٥١ إلى ٥٣ · ثلاث حصص</p>
<p class="lead" style="font-size:clamp(26px,4.8vh,56px)">{ME}</p>''', 'cover'))
CAN = ['أعرف أنّ <b>حلّ المعادلة</b> هو إيجاد قيمة المتغيّر فيها', 'أحلّ المعادلة بـ<b>العمليات العكسية</b> على طرفيها، وأتحقّق من الحل', '<b>أكتب معادلةً</b> من وصفٍ لفظي أو شكلٍ ثم أحلّها']
S.append(slide(f'''<h2>في نهاية هذا الدرس…</h2>
<div class="can">{''.join(f'<div><span class="can-i">✔</span><span><b>أنا أستطيع</b> أن {t}</span></div>' for t in CAN)}</div>'''))
S.append(slide(f'''<h2>مفردات الدرس</h2>
{st('<div class="vocab wide"><div><span>حلّ المعادلة</span><i>solve equation</i></div><div><span>الحل</span><i>solution</i></div><div><span>العمليات العكسية</span><i>inverse operations</i></div><div><span>المعكوس الجمعي</span><i>additive inverse</i></div></div>')}
<p class="lead">ثلاث حصص: <b class="c-i">أنا</b> ← <b class="c-we">نحن</b> ← <b class="c-u">أنتم</b></p>'''))

# ═══════════ الحصة الأولى: المعادلة والجمع والطرح ═══════════
S.append(slide('''<span class="tag">الحصة الأولى · ٤٠ دقيقة</span><h2>المعادلة: الجمع والطرح</h2>
<div class="plan"><div><b>٥ د</b>تهيئة: الميزان</div><div><b>٥ د</b>ما المعادلة؟</div><div><b>٧ د</b>المعكوس الجمعي</div>
<div><b>٧ د</b>مثال ٢-٥ (١ أ)</div><div><b>٩ د</b>نحن ← أنتم</div><div><b>٤ د</b>انتبه</div><div><b>٣ د</b>بطاقة الخروج</div></div>''', 'divider'))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">تهيئة 🤔</span>{ref('دليل المعلم ص ٥٢')}</div><h2>المعادلة مثل ميزانٍ ذي كفّتين</h2>
{st(BAL(M(V('س'), PL, '٥'), M('١٢')))}
{st('<div class="note">ما نفعله بكفّةٍ نفعله بالأخرى، <b>ليبقى الميزان متوازناً</b></div>')}''' + tn('نقطة التعلّم الأولى في الدليل: إن غيّرنا إحدى الكفّتين يجب أن نغيّر الأخرى بالمقدار نفسه. اسأل: كم يجب أن تكون س ليتوازن الميزان؟')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('كتاب الطالب ص ٥١')}</div><h2>المعادلة وحلّها</h2>
<div class="defs">{st('<div><b class="kk c-we">المعادلة</b><span>طرفان بينهما إشارة التساوي =</span></div>')}{st('<div><b class="kk c-exp">حلّ المعادلة</b><span>إيجاد قيمة المتغيّر فيها</span></div>')}</div>'''))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('كتاب الطالب ص ٥١')}</div><h2>حلّ {M(V("س"), PL, "٥", EQ, "١٢", cls="sm")}</h2>
{box(STEPS(STP('نضيف −٥ للطرفين', M(V('س'), PL, '٥', OP('− ٥'), EQ, '١٢', OP('− ٥'), cls="sm")), STP('الحل', M(V('س'), EQ, '٧', cls="sm"), 'fin')))}
{st('<div class="note">المعكوس الجمعي للعدد ٥ هو −٥، و ٥ + (−٥) = ٠</div>')}'''))
S.append(slide(f'''<div class="row hdr">{mode('i')}<span class="qbadge" style="background:#7048E8;box-shadow:0 4px 0 #4C2FB0">الميزان</span></div><h2>نطرح ٥ من الكفّتين</h2>
<div class="row" style="gap:3vw;align-items:center">{st(BAL(M(V('س'), PL, '٥'), M('١٢'), 'sm'))}{st('<span class="arrow">←</span>')}{st(BAL(M(V('س')), M('٧'), 'sm'))}</div>''' + tn('من خارج المرجع: الميزان رسمٌ يوضّح فكرة الدليل، ويبقى متوازناً بعد طرح ٥ من الكفّتين.')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('مثال ٢-٥ (١ أ)')}</div><h2>حلّ {M(V("س"), MI, "٣", EQ, "١٢", cls="sm")} وتحقّق</h2>
{box(STEPS(STP('نضيف ٣ للطرفين', M(V('س'), MI, '٣', OP('+ ٣'), EQ, '١٢', OP('+ ٣'), cls="sm")), STP('الحل', M(V('س'), EQ, '١٥', cls="sm"), 'fin'), STP('نتحقّق: نعوّض س = ١٥', M('١٥', MI, '٣', EQ, '١٢ ✔', cls="sm"))))}''' + tn('أكّد التحقّق دائماً: نعوّض الحل في المعادلة الأصلية، فإن تساوى الطرفان فالحل صحيح.')))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">تذكّر 📌</span>{ref('دليل المعلم ص ٥٢')}</div><h2>العمليات العكسية</h2>
<div class="inv">{''.join(st(f'<div><span>للتخلّص من</span><b>{a}</b><span>نستخدم</span><b class="c-good">{b}</b></div>') for a, b in (('+ ٢', '− ٢ في الطرفين'), ('− ٣', '+ ٣ في الطرفين'), ('× ٤', '÷ ٤ للطرفين'), ('÷ ٥', '× ٥ للطرفين')))}</div>''' + tn('اقتراح الدليل: اكتب هذه الملاحظات على السبورة قبل البدء في التمارين، ليرجع إليها الطلاب.')))
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('تمرين ١ (ج)')}</div><h2>معاً: حلّ {M("٢", PL, V("س"), EQ, "١٥", cls="sm")}</h2>
<button class="flip box col"><span class="tap">👆 الحل</span><span class="hid col">{M('٢', OP('− ٢'), PL, V('س'), EQ, '١٥', OP('− ٢'), cls="sm")}{M(V('س'), EQ, '١٣', cls="sm")}<small class="hint">تحقّق: ٢ + ١٣ = ١٥ ✔</small></span></button>'''))
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('تمرين ٢ (ج)')}</div><h2>معاً: حلّ {M("١٣", EQ, V("ص"), MI, "٥", cls="sm")}</h2>
<button class="flip box col"><span class="tap">👆 الحل</span><span class="hid col">{M('١٣', OP('+ ٥'), EQ, V('ص'), MI, '٥', OP('+ ٥'), cls="sm")}{M('١٨', EQ, V('ص'), cls="sm")}<small class="hint">المتغيّر في الطرف الأيسر، والطريقة نفسها</small></span></button>'''))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ١ (ز)')}{timer(2)}</div>''' + quiz(f'حلّ: {M(V("س"), MI, "١٢", EQ, "١٤")}', [M(V('س'), EQ, '٢'), M(V('س'), EQ, '٢٦'), M(V('س'), EQ, '١٦٨'), M(V('س'), EQ, '١٢')], 1, 'نضيف ١٢ إلى الطرفين: س = ١٤ + ١٢ = ٢٦')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ٢ (أ)')}</div>''' + quiz(f'حلّ: {M("١٥", EQ, V("ص"), PL, "٣")}', [M(V('ص'), EQ, '١٨'), M(V('ص'), EQ, '٥'), M(V('ص'), EQ, '١٢'), M(V('ص'), EQ, '٤٥')], 2, 'نطرح ٣ من الطرفين: ١٥ − ٣ = ١٢')))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">انتبه ⚠️ أخطاء شائعة</span>{ref('دليل المعلم ص ٥٢')}</div><h2>أين الخطأ؟</h2>
<div class="errs">{''.join(st(f'<button class="flip err"><span class="xq">{q}</span><span class="tap">👆</span><span class="hid xa no">{w}</span></button>') for q, w in (
  (M(V('س'), PL, '٥', OP('− ٥'), EQ, '١٢'), '✘ غيّر طرفاً واحداً فقط، فيجب طرح ٥ من الطرفين'),
  (M(V('س'), MI, '٣', EQ, '١٢', '←', V('س'), EQ, '٩'), '✘ لم يغيّر الإشارة: نضيف ٣ فيكون س = ١٥')))}</div>''' + tn('من الأخطاء الشائعة في الدليل: تغيير أحد الطرفين دون الآخر، ونسيان تغيير الإشارة، والخطأ في التعامل مع الأعداد في الطرفين.')))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ١ 🎫</span><h2>حلّ وتحقّق</h2>
<div class="exit">{st(f'<div><b>١</b>{M(V("س"), PL, "٤", EQ, "١١", cls="sm")}</div>')}{st(f'<div><b>٢</b>{M(V("س"), MI, "٤", EQ, "٩", cls="sm")}</div>')}{st(f'<div><b>٣</b>{M("٢٥", EQ, V("ص"), MI, "٣", cls="sm")}</div>')}</div>'''))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ١ 🎫</span><h2>الإجابات</h2>
<button class="flip box col" style="min-width:40vw"><span class="tap">👆 اضغط لإظهار الإجابات</span><span class="hid col">{M(V('س'), EQ, '٧', cls="sm")}{M(V('س'), EQ, '١٣', cls="sm")}{M(V('ص'), EQ, '٢٨', cls="sm")}</span></button>'''))

# ═══════════ الحصة الثانية: الضرب والقسمة، ومعادلات بخطوتين ═══════════
S.append(slide('''<span class="tag">الحصة الثانية · ٤٠ دقيقة</span><h2>الضرب والقسمة، ومعادلات بخطوتين</h2>
<div class="plan"><div><b>٤ د</b>إحماء</div><div><b>٦ د</b>القسمة على الطرفين</div><div><b>٧ د</b>الضرب في الطرفين</div>
<div><b>٨ د</b>مثال ٢-٥ (١ ب)</div><div><b>٦ د</b>نحن</div><div><b>٦ د</b>أنتم</div><div><b>٣ د</b>بطاقة الخروج</div></div>''', 'divider'))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">إحماء 🔥</span>{timer(1)}</div>''' + quiz(f'حلّ: {M(V("س"), PL, "٦", EQ, "٩")}', [M(V('س'), EQ, '١٥'), M(V('س'), EQ, '٣'), M(V('س'), EQ, '٥٤'), M(V('س'), EQ, '٦')], 1, 'نطرح ٦ من الطرفين: ٩ − ٦ = ٣')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('تمرين ١ (ط)')}</div><h2>حلّ {M(T("٣", "س"), EQ, "١٢", cls="sm")}</h2>
{box(STEPS(STP('٣س تعني ٣ × س، فنقسم الطرفين على ٣', M(FR(T('٣', 'س'), OP('٣')), EQ, FR('١٢', OP('٣')), cls="sm")), STP('الحل', M(V('س'), EQ, '٤', cls="sm"), 'fin'), STP('نتحقّق', M('٣', X, '٤', EQ, '١٢ ✔', cls="sm"))))}'''))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('تمرين ١ (م)')}</div><h2>حلّ {M(FR(V("س"), "٢"), EQ, "٤", cls="sm")}</h2>
{box(STEPS(STP('س مقسومة على ٢، فنضرب الطرفين في ٢', M(FR(V('س'), '٢'), OP('× ٢'), EQ, '٤', OP('× ٢'), cls="sm")), STP('الحل', M(V('س'), EQ, '٨', cls="sm"), 'fin'), STP('نتحقّق', M('٨', DV, '٢', EQ, '٤ ✔', cls="sm"))))}'''))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('مثال ٢-٥ (١ ب)')}</div><h2>حلّ {M(T("٢", "س"), PL, "٤", EQ, "١٦", cls="sm")}</h2>
{box(STEPS(STP('أولاً: نتخلّص من + ٤', M(T('٢', 'س'), PL, '٤', OP('− ٤'), EQ, '١٦', OP('− ٤'), cls="sm")), STP('نبسّط', M(T('٢', 'س'), EQ, '١٢', cls="sm")), STP('ثانياً: نقسم الطرفين على ٢', M(V('س'), EQ, '٦', cls="sm"), 'fin'), STP('نتحقّق', M('٢', X, '٦', PL, '٤', EQ, '١٦ ✔', cls="sm"))))}''' + tn('نقطة الدليل: نتخلّص أولاً من الحدود المضافة أو المطروحة، ثم من الضرب أو القسمة.')))
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('تمرين ٣ (و)')}</div><h2>معاً: حلّ {M(FR(V("ل"), "٤"), PL, "٣", EQ, "٧", cls="sm")}</h2>
<button class="flip box col"><span class="tap">👆 الحل</span><span class="hid col">{M(FR(V('ل'), '٤'), EQ, '٧', MI, '٣', EQ, '٤', cls="sm")}{M(V('ل'), EQ, '٤', X, '٤', EQ, '١٦', cls="sm")}<small class="hint">نطرح ٣ أولاً، ثم نضرب في ٤</small></span></button>'''))
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('تمرين ٣ (ي)')}</div><h2>معاً: حلّ {M("٢٩", EQ, T("٤", "ح"), MI, "٣", cls="sm")}</h2>
<button class="flip box col"><span class="tap">👆 الحل</span><span class="hid col">{M('٢٩', PL, '٣', EQ, T('٤', 'ح'), cls="sm")}{M('٣٢', EQ, T('٤', 'ح'), '←', V('ح'), EQ, '٨', cls="sm")}</span></button>'''))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ٣ (أ)')}{timer(2)}</div>''' + quiz(f'حلّ: {M(T("٢", "م"), PL, "٣", EQ, "١٣")}', [M(V('م'), EQ, '٨'), M(V('م'), EQ, '٥'), M(V('م'), EQ, '٦٫٥'), M(V('م'), EQ, '١٠')], 1, '٢م = ١٣ − ٣ = ١٠ ، ثم م = ١٠ ÷ ٢ = ٥')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ٣ (ح)')}</div>''' + quiz(f'حلّ: {M(FR(V("ل"), "٥"), MI, "١", EQ, "٥")}', [M(V('ل'), EQ, '٣٠'), M(V('ل'), EQ, '٢٠'), M(V('ل'), EQ, '٦'), M(V('ل'), EQ, '٢٤')], 0, 'نضيف ١: ل ÷ ٥ = ٦ ، ثم نضرب في ٥: ل = ٣٠')))
S.append(slide(f'''<span class="tag" style="background:#7048E8">للاطّلاع فقط</span><h2>إذا كان أمام المتغيّر إشارة سالبة: {M("٢", MI, V("س"), EQ, "٤", cls="sm")}</h2>
{box(STEPS(STP('نطرح ٢ من الطرفين', M(MI + V('س'), EQ, '٢', cls="sm")), STP('نضرب الطرفين في −١', M(V('س'), EQ, MI + '٢', cls="sm"), 'fin')))}''' + tn('من ورقة «درسي في صفحة» وليس في كتاب الطالب: معلومة إثرائية لا تدخل في زمن الحصة.')))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ٢ 🎫</span><h2>حلّ</h2>
<div class="exit">{st(f'<div><b>١</b>{M(T("٥", "س"), EQ, "٣٠", cls="sm")}</div>')}{st(f'<div><b>٢</b>{M(FR(V("س"), "٧"), EQ, "٣", cls="sm")}</div>')}{st(f'<div><b>٣</b>{M(T("٣", "م"), MI, "٢", EQ, "١٣", cls="sm")}</div>')}</div>'''))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ٢ 🎫</span><h2>الإجابات</h2>
<button class="flip box col" style="min-width:40vw"><span class="tap">👆 اضغط لإظهار الإجابات</span><span class="hid col">{M(V('س'), EQ, '٦', cls="sm")}{M(V('س'), EQ, '٢١', cls="sm")}{M(V('م'), EQ, '٥', cls="sm")}</span></button>'''))

# ═══════════ الحصة الثالثة: كتابة المعادلات ═══════════
S.append(slide('''<span class="tag">الحصة الثالثة · ٤٠ دقيقة</span><h2>كتابة المعادلات وحلّها</h2>
<div class="plan"><div><b>٣ د</b>إحماء</div><div><b>٨ د</b>مثال ٢-٥ (٢): ميا</div><div><b>٦ د</b>نحن: أفكّر في عدد</div>
<div><b>٥ د</b>أنتم</div><div><b>٦ د</b>المستطيلات</div><div><b>٦ د</b>فكّر: البطاقات</div><div><b>٣ د</b>نشاط</div><div><b>٣ د</b>بطاقة الخروج</div></div>''', 'divider'))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">إحماء 🔥</span>{timer(1)}</div>''' + quiz(f'حلّ: {M(T("٤", "م"), PL, "١", EQ, "١٧")}', [M(V('م'), EQ, '٤'), M(V('م'), EQ, '٤٫٥'), M(V('م'), EQ, '١٦'), M(V('م'), EQ, '٧٢')], 0, '٤م = ١٦ ، م = ٤')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('مثال ٢-٥ (٢ أ)')}</div><h2>مسألة ميا: نكتب المعادلة جزءاً جزءاً</h2>
<div class="read">{''.join(st(f'<div><span>{t}</span><b>{e}</b></div>') for t, e in (('«تفكّر ميا في عدد»', M(V('ع'))), ('«تقسمه على ٢»', M(FR(V('ع'), '٢'))), ('«ثم تضيف ٣»', M(FR(V('ع'), '٢'), PL, '٣')), ('«والإجابة ٧»', M(FR(V('ع'), '٢'), PL, '٣', EQ, '٧'))))}</div>''' + tn('نقطة الدليل: وضّح للطلاب أثناء قراءة المثال كيف يُكتب كل جزءٍ يقرؤونه، جزءاً جزءاً.')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('مثال ٢-٥ (٢ ب)')}</div><h2>نحلّ معادلة ميا {M(FR(V("ع"), "٢"), PL, "٣", EQ, "٧", cls="sm")}</h2>
{box(STEPS(STP('نطرح ٣ من الطرفين', M(FR(V('ع'), '٢'), EQ, '٤', cls="sm")), STP('نضرب الطرفين في ٢', M(V('ع'), EQ, '٤', X, '٢', EQ, '٨', cls="sm"), 'fin'), STP('نتحقّق', M('٨', DV, '٢', PL, '٣', EQ, '٧ ✔', cls="sm"))))}'''))
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('تمرين ٤ (أ، ج)')}</div><h2>معاً: اكتب معادلة ثم حلّها</h2>
<div class="errs">{''.join(st(f'<button class="flip err"><span class="xq">{q}</span><span class="tap">👆</span><span class="hid xa">{w}</span></button>') for q, w in (
  ('أفكّر في عدد إذا أضفت إليه ٣ يكون الناتج ١٨', M(V('س'), PL, '٣', EQ, '١٨', '←', V('س'), EQ, '١٥')),
  ('أفكّر في عدد إذا ضربته في ٤ يكون الناتج ٢٤', M(T('٤', 'س'), EQ, '٢٤', '←', V('س'), EQ, '٦'))))}</div>''' + tn('تعليق الدليل على التمرين ٤: ذكّر الطلاب أنه يمكنهم اختيار أي حرف ليمثّل المجهول، مثل س.')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ٤ (هـ)')}{timer(2)}</div>''' + quiz('عددٌ ضربناه في ٤ ثم أضفنا ٢ فكان ٢٦. ما العدد؟', [M('٧'), M('٦'), M('٢٨'), M('٥')], 1, '٤س + ٢ = ٢٦ ، ٤س = ٢٤ ، س = ٦')))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">فكّر 💡</span>{ref('تمرين ٥ (أ)')}</div><h2>اكتب معادلة لأطوال المستطيلات ثم حلّها</h2>
{st(BARS([('م سم', 1, 'y'), ('م سم', 1, 'y'), ('٨ سم', 2, 'w')], '٢٠ سم'))}
<button class="flip box col"><span class="tap">👆 الحل</span><span class="hid col">{M(V('م'), PL, V('م'), PL, '٨', EQ, '٢٠', cls="sm")}{M(T('٢', 'م'), EQ, '١٢', '←', V('م'), EQ, '٦', cls="sm")}</span></button>''' + tn('تعليق الدليل: قد يجد بعض الطلاب الإجابة ذهنياً، لكن فكرة التمرين كتابة المعادلة من الشكل. (ب): ٣ل + ٣ = ٢٤ ، ل = ٧.')))
CARDS = [('٤م + ٤', 'p'), ('٢م − ٦', 'p'), ('٦م + ٢', 'p'), ('=', 'e'), ('٣٢', 'b'), ('٤٤', 'b'), ('٢٠', 'b')]
S.append(slide(f'''<div class="row hdr"><span class="qbadge">فكّر 💡</span>{ref('تمرين ٦')}</div><h2>بطاقات راشد: وردية = زرقاء</h2>
<div class="cards">{''.join(f'<span class="c{c}">{t}</span>' for t, c in CARDS)}</div>
<div class="row">{st(f'<button class="flip box col" style="flex:1"><span class="rq">(أ) أكبر قيمة للرمز م</span><span class="tap">👆</span><span class="hid">{M(T("٢", "م"), MI, "٦", EQ, "٤٤", "←", V("م"), EQ, "٢٥", cls="sm")}</span></button>')}{st(f'<button class="flip box col" style="flex:1"><span class="rq">(ب) أصغر قيمة للرمز م</span><span class="tap">👆</span><span class="hid">{M(T("٦", "م"), PL, "٢", EQ, "٢٠", "←", V("م"), EQ, "٣", cls="sm")}</span></button>')}</div>''' + tn('تعليق الدليل: المتفوّقون يحلّونها بسهولة، والباقون يحتاجون محاولاتٍ أكثر في (أ) فيسهل عليهم (ب). جرّب التوافيق التسعة مع الطلاب إن احتاجوا.')))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">نشاط 🧩</span>{ref('نشاط دليل المعلم')}</div><h2>اكتب سؤالك: «أفكّر في عدد…»</h2>
{st('<div class="note">اكتب ٤ أسئلة بعملية واحدة (+، −، ×، ÷) وسؤالين بعمليتين، ويكون العدد المجهول عدداً كاملاً</div>')}
{st(box(f'<div class="col"><span class="hint">مثال: أفكّر في عدد إذا ضربته في ٤ ثم طرحت منه ٢ يكون الناتج ١٠</span>{M(T("٤", "س"), MI, "٢", EQ, "١٠", "←", V("س"), EQ, "٣")}</div>'))}''' + tn('نشاط الدليل بعد التمرين ٤: يتبادل الطلاب الأسئلة ويحلّونها ويتحقّقون أن المجهول عددٌ كامل.')))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ٣ 🎫</span><h2>اكتب معادلة ثم حلّها</h2>
<div class="exit">{st('<div><b>١</b>أفكّر في عدد إذا طرحت منه ٤ يكون الناتج ١٠</div>')}{st('<div><b>٢</b>أفكّر في عدد إذا قسمته على ٦ يكون الناتج ١٢</div>')}{st('<div><b>٣</b>أفكّر في عدد إذا قسمته على ٣ ثم طرحت منه ٨ يكون الناتج ٤</div>')}</div>'''))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ٣ 🎫</span><h2>الإجابات</h2>
<button class="flip box col" style="min-width:40vw"><span class="tap">👆 اضغط لإظهار الإجابات</span><span class="hid col">{M(V('س'), MI, '٤', EQ, '١٠', '←', '١٤', cls="sm")}{M(FR(V('س'), '٦'), EQ, '١٢', '←', '٧٢', cls="sm")}{M(FR(V('س'), '٣'), MI, '٨', EQ, '٤', '←', '٣٦', cls="sm")}</span></button>'''))
S.append(slide('''<span class="qbadge" style="background:#0A6770;box-shadow:0 4px 0 #05393E">الواجب المنزلي 🏠</span><h2>بعد الحصص الثلاث</h2>
<div class="exit"><div class="st"><div><b>١</b>صفحتا ٣٧ و ٣٨ في كتاب النشاط (حلّ المعادلات)</div></div><div class="st"><div><b>٢</b>صفحة ٣٩ في كتاب النشاط (كتابة المعادلات)</div></div></div>'''))
S.append(slide(f'''<h2>الخلاصة</h2>
<div class="sumg">
{st(box('<div class="col"><b class="kk c-we">الحل</b><span>إيجاد قيمة المتغيّر</span>' + M(V('س'), EQ, '٧') + '</div>'))}
{st(box('<div class="col"><b class="kk c-exp">الطرفان</b><span>العملية العكسية على الطرفين معاً</span>' + M('+ ↔ −', '،', '× ↔ ÷') + '</div>'))}
{st(box('<div class="col"><b class="kk c-lcm">التحقّق</b><span>نعوّض الحل في المعادلة</span>' + M('١٥', MI, '٣', EQ, '١٢ ✔') + '</div>'))}</div>'''))

# ═══════════ ملحق: تمارين كتاب الطالب ص٥٢–٥٣ (الإجابات من دليل المعلم ص٥٦) ═══════════
S.append(launch('sb', '٥٢ و ٥٣', note=f'المراجع: كتاب الطالب ص٥١ إلى ٥٣، ودليل المعلم ص٥٢ و ٥٣ وإجاباته ص٥٦ · {ME}'))
H = ['أ', 'ب', 'ج', 'د', 'هـ', 'و', 'ز', 'ح', 'ط', 'ي', 'ك', 'ل', 'م', 'ن', 'س', 'ع']
RL = 'نستخدم العملية العكسية على الطرفين، ثم نتحقّق بالتعويض'
def Q(h, eq, steps, ans): return (f'({h}) {eq}', f'{ans}<small>{steps}</small>')
B1 = [('س + ٤ = ١١', 'نطرح ٤', 'س = ٧'), ('س + ٣ = ٦', 'نطرح ٣', 'س = ٣'), ('٢ + س = ١٥', 'نطرح ٢', 'س = ١٣'), ('٧ + س = ١٩', 'نطرح ٧', 'س = ١٢'),
      ('س − ٤ = ٩', 'نضيف ٤', 'س = ١٣'), ('س − ٢ = ٨', 'نضيف ٢', 'س = ١٠'), ('س − ١٢ = ١٤', 'نضيف ١٢', 'س = ٢٦'), ('س − ١٨ = ٣٠', 'نضيف ١٨', 'س = ٤٨'),
      ('٣س = ١٢', 'نقسم على ٣', 'س = ٤'), ('٥س = ٣٠', 'نقسم على ٥', 'س = ٦'), ('٧س = ٧٠', 'نقسم على ٧', 'س = ١٠'), ('١٢س = ٧٢', 'نقسم على ١٢', 'س = ٦'),
      ('س ÷ ٢ = ٤', 'نضرب في ٢', 'س = ٨'), ('س ÷ ٣ = ٥', 'نضرب في ٣', 'س = ١٥'), ('س ÷ ٧ = ٣', 'نضرب في ٧', 'س = ٢١'), ('س ÷ ٩ = ٧', 'نضرب في ٩', 'س = ٦٣')]
S.append(ex(1, 'حلّ المعادلات وتحقّق من صحة إجاباتك', RL, [Q(h, *b) for h, b in zip(H, B1)], cols=2))
B2 = [('١٥ = ص + ٣', 'نطرح ٣', 'ص = ١٢'), ('٩ = ص + ٢', 'نطرح ٢', 'ص = ٧'), ('١٣ = ص − ٥', 'نضيف ٥', 'ص = ١٨'), ('٢٥ = ص − ٣', 'نضيف ٣', 'ص = ٢٨'),
      ('٢٤ = ٨ص', 'نقسم على ٨', 'ص = ٣'), ('٤٢ = ٦ص', 'نقسم على ٦', 'ص = ٧'), ('٥ = ص ÷ ٢', 'نضرب في ٢', 'ص = ١٠'), ('٧ = ص ÷ ٥', 'نضرب في ٥', 'ص = ٣٥')]
S.append(ex(2, 'حلّ المعادلات', 'المتغيّر في الطرف الأيسر، والطريقة نفسها', [Q(h, *b) for h, b in zip(H, B2)], cols=2))
B3 = [('٢م + ٣ = ١٣', '٢م = ١٠', 'م = ٥'), ('٤م + ١ = ١٧', '٤م = ١٦', 'م = ٤'), ('٣م − ٢ = ١٣', '٣م = ١٥', 'م = ٥'), ('٢م − ٨ = ٤', '٢م = ١٢', 'م = ٦'),
      ('ل ÷ ٢ + ١ = ٥', 'ل ÷ ٢ = ٤', 'ل = ٨'), ('ل ÷ ٤ + ٣ = ٧', 'ل ÷ ٤ = ٤', 'ل = ١٦'), ('ل ÷ ٣ − ٢ = ٢', 'ل ÷ ٣ = ٤', 'ل = ١٢'), ('ل ÷ ٥ − ١ = ٥', 'ل ÷ ٥ = ٦', 'ل = ٣٠'),
      ('١٤ = ٣ح + ٢', '١٢ = ٣ح', 'ح = ٤'), ('٢٩ = ٤ح − ٣', '٣٢ = ٤ح', 'ح = ٨'), ('٩ = ح ÷ ٣ + ٢', '٧ = ح ÷ ٣', 'ح = ٢١'), ('١ = ح ÷ ٦ − ٦', '٧ = ح ÷ ٦', 'ح = ٤٢')]
S.append(ex(3, 'حلّ المعادلات وتحقّق من صحة إجاباتك', 'نتخلّص من الجمع أو الطرح أولاً، ثم من الضرب أو القسمة', [Q(h, *b) for h, b in zip(H, B3)], cols=2))
B4 = [('أفكّر في عدد إذا أضفت إليه ٣ يكون الناتج ١٨', 'س + ٣ = ١٨', 'س = ١٥'), ('أفكّر في عدد إذا طرحت منه ٤ يكون الناتج ١٠', 'س − ٤ = ١٠', 'س = ١٤'),
      ('أفكّر في عدد إذا ضربته في ٤ يكون الناتج ٢٤', '٤س = ٢٤', 'س = ٦'), ('أفكّر في عدد إذا قسمته على ٦ يكون الناتج ١٢', 'س ÷ ٦ = ١٢', 'س = ٧٢'),
      ('أفكّر في عدد إذا ضربته في ٤ ثم أضفت إليه ٢ يكون الناتج ٢٦', '٤س + ٢ = ٢٦', 'س = ٦'), ('أفكّر في عدد إذا قسمته على ٣ ثم طرحت منه ٨ يكون الناتج ٤', 'س ÷ ٣ − ٨ = ٤', 'س = ٣٦')]
S.append(ex(4, 'اكتب معادلة ثم حلّها', 'نكتب كل جزءٍ نقرؤه، ونرمز للعدد بحرف', [(f'({h}) {q}', f'{e}<small>{x}</small>') for h, (q, e, x) in zip(H, B4)], cols=1, per=2))
S.append(ex(5, 'اكتب معادلة لأطوال المستطيلات ثم حلّها', 'مجموع الأطوال الصغيرة = الطول الكلي', [
  ('(أ)' + BARS([('م', 1, 'y'), ('م', 1, 'y'), ('٨', 2, 'w')], '٢٠ سم'), 'م + م + ٨ = ٢٠<small>٢م = ١٢ ، م = ٦</small>'),
  ('(ب)' + BARS([('ل', 1, 'g'), ('ل', 1, 'g'), ('ل', 1, 'g'), ('٣', .8, 'w')], '٢٤ سم'), '٣ل + ٣ = ٢٤<small>٣ل = ٢١ ، ل = ٧</small>')], cols=1, per=1))
S.append(ex(6, 'بطاقات راشد: وردية = زرقاء', 'الوردية: ٤م + ٤ ، ٢م − ٦ ، ٦م + ٢ · الزرقاء: ٣٢ ، ٤٤ ، ٢٠', [('(أ) أكبر قيمة للرمز م', '٢م − ٦ = ٤٤<small>م = ٢٥</small>'), ('(ب) أصغر قيمة للرمز م', '٦م + ٢ = ٢٠<small>م = ٣</small>')], cols=2))

# ═══════════ ملحق: حلول كتاب النشاط ص٣٧–٣٩ (الإجابات من دليل المعلم ص٦٠) ═══════════
S.append(launch('ab', '٣٧ إلى ٣٩', note='الإجابات النهائية من دليل المعلم ص ٦٠'))
NA, NB, NC = 'نشاط ص ٣٧ · تمرين', 'نشاط ص ٣٨ · تمرين', 'نشاط ص ٣٩ · تمرين'
A1 = [('س + ٢ = ٦', 'نطرح ٢', 'س = ٤'), ('س + ٦ = ٩', 'نطرح ٦', 'س = ٣'), ('٤ + س = ١١', 'نطرح ٤', 'س = ٧'), ('١٥ + س = ٢١', 'نطرح ١٥', 'س = ٦'),
      ('س − ٥ = ١٠', 'نضيف ٥', 'س = ١٥'), ('س − ٤ = ٦', 'نضيف ٤', 'س = ١٠'), ('س − ١٥ = ١٢', 'نضيف ١٥', 'س = ٢٧'), ('٥س = ٢٠', 'نقسم على ٥', 'س = ٤'),
      ('٣س = ٣٠', 'نقسم على ٣', 'س = ١٠'), ('٤س = ٢٨', 'نقسم على ٤', 'س = ٧'), ('س ÷ ٥ = ١٠', 'نضرب في ٥', 'س = ٥٠'), ('س ÷ ٣ = ٩', 'نضرب في ٣', 'س = ٢٧')]
S.append(ex(1, 'حلّ المعادلات ثم تحقّق من صحة إجاباتك', RL, [Q(h, *b) for h, b in zip(H, A1)], cols=2, src=NA))
A2 = [('١٤ = س + ٣', 'نطرح ٣', 'س = ١١'), ('٩ = س + ٥', 'نطرح ٥', 'س = ٤'), ('١٢ = س − ٦', 'نضيف ٦', 'س = ١٨'), ('٢٠ = س − ٥', 'نضيف ٥', 'س = ٢٥'),
      ('١٤ = ٢س', 'نقسم على ٢', 'س = ٧'), ('٥٠ = ١٠س', 'نقسم على ١٠', 'س = ٥'), ('٦ = س ÷ ٣', 'نضرب في ٣', 'س = ١٨'), ('٨ = س ÷ ٨', 'نضرب في ٨', 'س = ٦٤')]
S.append(ex(2, 'حلّ المعادلات ثم تحقّق من صحة إجاباتك', 'المتغيّر في الطرف الأيسر، والطريقة نفسها', [Q(h, *b) for h, b in zip(H, A2)], cols=2, src=NA))
A3 = [('٣س + ٢ = ١١', '٣س = ٩', 'س = ٣'), ('٥س + ١ = ١١', '٥س = ١٠', 'س = ٢'), ('٤س − ٢ = ١٨', '٤س = ٢٠', 'س = ٥'), ('٢س − ٨ = ١٨', '٢س = ٢٦', 'س = ١٣'),
      ('ص ÷ ٢ + ٥ = ٧', 'ص ÷ ٢ = ٢', 'ص = ٤'), ('ص ÷ ٣ + ٣ = ٦', 'ص ÷ ٣ = ٣', 'ص = ٩'), ('ص ÷ ٤ − ٥ = ٦', 'ص ÷ ٤ = ١١', 'ص = ٤٤'), ('ص ÷ ٥ − ٢ = ٠', 'ص ÷ ٥ = ٢', 'ص = ١٠'),
      ('١٧ = ٥ص + ٢', '١٥ = ٥ص', 'ص = ٣'), ('١٨ = ٣ص − ٣', '٢١ = ٣ص', 'ص = ٧'), ('٥ = ص ÷ ٤ + ٢', '٣ = ص ÷ ٤', 'ص = ١٢'), ('٢ = ص ÷ ١٠ − ٦', '٨ = ص ÷ ١٠', 'ص = ٨٠')]
S.append(ex(3, 'حلّ المعادلات ثم تحقّق من صحة إجاباتك', 'نتخلّص من الجمع أو الطرح أولاً، ثم من الضرب أو القسمة', [Q(h, *b) for h, b in zip(H, A3)], cols=2, src=NB))
S.append(ex(4, 'ما العدد الذي أفكّر فيه؟', 'نكتب معادلة ثم نحلّها', [('(أ) إذا أضفت إليه ٥ أصبح ٢١', 'س + ٥ = ٢١<small>س = ١٦</small>'), ('(ب) إذا طرحت منه ٥ يصبح ٢١', 'س − ٥ = ٢١<small>س = ٢٦</small>')], cols=2, src=NB))
A5 = [('إذا ضربته في ٥ يكون الناتج ٢٠', '٥س = ٢٠', 'س = ٤'), ('إذا قسمته على ٥ يكون الناتج ٢٠', 'س ÷ ٥ = ٢٠', 'س = ١٠٠'),
      ('إذا ضربته في ٥ ثم أضفت إليه ٥ يكون الناتج ٢٠', '٥س + ٥ = ٢٠', 'س = ٣'), ('إذا قسمته على ٥ ثم طرحت منه ٥ يكون الناتج ٤', 'س ÷ ٥ − ٥ = ٤', 'س = ٤٥')]
S.append(ex(5, 'اكتب معادلة ثم أوجد العدد المجهول', 'نرمز للعدد بالحرف س', [(f'({h}) {q}', f'{e}<small>{x}</small>') for h, (q, e, x) in zip(H, A5)], cols=1, per=2, src=NC))
S.append(ex(6, 'اكتب معادلة لأطوال المستطيلات ثم حلّها', 'مجموع الأطوال الصغيرة = الطول الكلي', [
  ('(أ)' + BARS([('س', 1, 'h'), ('س', 1, 'h'), ('س', 1, 'h'), ('١٠', 1.7, 'w')], '٢٨ سم'), '٣س + ١٠ = ٢٨<small>٣س = ١٨ ، س = ٦</small>'),
  ('(ب)' + BARS([('ص', .7, 'k'), ('٢٠', 3, 'w'), ('ص', .7, 'k')], '٢٥ سم'), '٢ص + ٢٠ = ٢٥<small>٢ص = ٥ ، ص = ٢٫٥</small>')], cols=1, per=1, src=NC))

EXTRA_CSS_OWN = '''
.var{color:var(--exp);font-weight:900}
.term{display:inline-flex;direction:rtl;unicode-bidi:isolate;align-items:center}
.fr{display:inline-flex;flex-direction:column;align-items:center;line-height:1.05;vertical-align:middle;margin:0 .1em}
.fr>span:first-child{border-bottom:.07em solid currentColor;padding:0 .15em .04em;align-self:stretch;text-align:center}
.opb{display:inline-block;color:#C2410C;background:#FFF1E6;border:3px solid #F5B585;border-radius:.3em;padding:0 .2em;line-height:1.2;font-size:1em}
.stps{display:flex;flex-direction:column;gap:1.6vh;align-items:stretch}
.stp{display:flex;align-items:center;gap:1.6vw;justify-content:space-between}
.stp .lab{flex:none;max-width:44%;font-family:var(--fh);font-weight:800;color:#2563EB;background:#EAF1FF;border-radius:12px;padding:.2em .8em;text-align:center;line-height:1.4}
.stp.fin .lab{background:var(--good);color:#fff}
.box .col>.m:not(.mid):not(.sm):not(.big),.hid.col>.m:not(.mid):not(.sm):not(.big){font-size:clamp(34px,6.4vh,76px)}
.bal{position:relative;display:flex;flex-direction:column;align-items:center;width:min(900px,64vw)}
.bal .pans{display:flex;justify-content:space-between;width:100%;gap:4vw;direction:rtl}
.bal .pan{flex:1;display:flex;align-items:center;justify-content:center;min-height:clamp(80px,16vh,180px);background:#EAF7F8;border:4px solid var(--base);border-radius:0 0 50% 50%/0 0 40% 40%;font-size:clamp(36px,7vh,84px);padding:1vh 1vw}
.bal .beam{width:100%;height:1vh;min-height:8px;background:var(--ink);border-radius:8px;margin-top:-.4vh}
.bal .post{width:1.2vw;min-width:10px;height:7vh;background:var(--ink);border-radius:0 0 8px 8px}
.bal.sm{width:min(560px,38vw)}.bal.sm .pan{font-size:clamp(28px,5.4vh,64px);min-height:clamp(60px,12vh,130px)}
.arrow{font-size:clamp(48px,9vh,100px);font-weight:900;color:var(--base)}
.defs{display:flex;flex-direction:column;gap:2vh;width:min(1300px,90vw)}
.defs .st>div{display:flex;align-items:center;gap:2vw;background:#fff;border:3px solid var(--line);border-radius:18px;padding:1.4vh 2vw}
.defs .kk{flex:none;font-size:clamp(32px,6vh,70px)}.defs span{font-weight:700;font-size:clamp(28px,5.2vh,60px)}
.inv{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1.6vh 2vw;width:min(1400px,92vw)}
.inv .st>div{display:flex;align-items:center;justify-content:center;gap:1vw;flex-wrap:wrap;background:#fff;border:3px solid var(--line);border-radius:16px;padding:1.2vh 1vw;font-weight:700;font-size:clamp(24px,4.4vh,50px)}
.inv b{font-family:var(--fh);font-size:1.25em}.c-good{color:var(--good)}
.errs{display:flex;flex-direction:column;gap:1.4vh;width:min(1400px,92vw)}
.errs .err{display:flex;flex-direction:column;align-items:center;gap:.6vh;background:#fff;border:3px solid var(--line);border-radius:16px;padding:.8vh 1.6vw;font-size:clamp(26px,5vh,58px);font-weight:700}
.errs .err .xq{font-size:inherit}.errs .err .xa{font-size:clamp(24px,4.4vh,50px)}
.read{display:flex;flex-direction:column;gap:1.2vh;width:min(1300px,90vw)}
.read .st>div{display:flex;align-items:center;justify-content:space-between;gap:2vw;background:#fff;border:3px solid var(--line);border-radius:16px;padding:.8vh 1.6vw}
.read span{font-weight:700;font-size:clamp(26px,4.8vh,56px);color:var(--ink2)}.read b{font-size:clamp(32px,6vh,70px)}
.sbar{display:flex;flex-direction:column;align-items:stretch;gap:.6vh;width:min(1000px,70vw);direction:rtl}
.sbar .segs{display:flex;border:3px solid var(--ink);border-radius:6px;overflow:hidden}
.sbar .segs span{display:flex;align-items:center;justify-content:center;height:clamp(40px,7vh,80px);border-inline-start:3px solid var(--ink);font-family:var(--fh);font-weight:800;font-size:clamp(24px,4.6vh,52px)}
.sbar .segs span:first-child{border-inline-start:0}
.sbar .y{background:#FBE36B}.sbar .g{background:#5CC27A}.sbar .w{background:#fff}.sbar .h{background:repeating-linear-gradient(45deg,#fff 0 6px,#C9D3E0 6px 9px)}.sbar .k{background:#E6E9EF}
.sbar .tot{text-align:center;font-weight:800;font-size:clamp(24px,4.4vh,50px);border-top:3px solid var(--ink2);padding-top:.3vh}
.xq .sbar{width:min(900px,62vw);margin-top:.6vh}.xcard .xq{display:flex;flex-direction:column;align-items:center}
.rq{font-weight:800;font-size:clamp(26px,4.8vh,56px)}
.cards{display:flex;gap:1vw;flex-wrap:wrap;justify-content:center;direction:rtl}
.cards span{font-family:var(--fh);font-weight:900;font-size:clamp(28px,5.4vh,62px);padding:.2em .7em;border-radius:12px}
.cards .cp{background:#FAD4E4}.cards .ce{background:#E2D6F3}.cards .cb{background:#5BC4E8}
.sumg{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:2vw;width:min(1600px,94vw)}
.sumg .col span{font-weight:700;font-size:clamp(26px,4.6vh,56px);line-height:1.4}
.sumg .kk{font-size:clamp(34px,6.4vh,76px)}
'''
