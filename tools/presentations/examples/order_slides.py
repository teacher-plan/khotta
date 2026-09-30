# شرائح درس ١-٧ «ترتيب العمليات الحسابية» — الصف السابع (حصة واحدة، كتاب الطالب ص٣٥)
# المراجع: دليل المعلم ص٣٣، كتاب الطالب ص٣٥، وورقة «درسي في صفحة» ١-٧. يُذكر في العرض اسم المعلّم المُعِدّ فقط.
# python3.12 gen_powers.py order_slides.py ترتيب_العمليات_عرض_تفاعلي.html "ترتيب العمليات الحسابية — الصف السابع"
# الرياضيات تُكتب من اليمين لليسار: أول ما يُقرأ هو أول ما يُمرَّر إلى M().

DV = '<span class="x">÷</span>'
MI = '<span class="x">−</span>'
def U(*p): return '<span class="now">' + ' '.join(p) + '</span>'          # العملية التي ننفّذها الآن
def BR(*p): return '<span class="brk">(' + ' '.join(p) + ')</span>'       # أقواس (تنعكس تلقائياً في اتجاه RTL)
def STP(lab, expr, cls=''): return st(f'<div class="stp {cls}"><span class="lab">{lab}</span>{expr}</div>')
def STEPS(*rows): return '<div class="stps">' + ''.join(rows) + '</div>'

S = []
# ═══ الشريحة الأولى: العنوان + أهداف «أنا أستطيع» (من نقاط التعلّم في دليل المعلم ص٣٣) ═══
CAN = ['أرتّب العمليات: <b class="o1">الأقواس</b> ثم <b class="o2">الأسس والجذور</b> ثم <b class="o3">الضرب والقسمة</b> ثم <b class="o4">الجمع والطرح</b>',
       'أُجري العمليات المتساوية في الأولوية <b>من اليمين إلى اليسار</b>',
       'أحلّ مسألةً فيها أكثر من عملية حسابية بعد قراءتها كاملة',
       'أضع الأقواس في المكان المناسب ليصبح الناتج صحيحاً']
S.append(slide('''<span class="tag">الصف السابع · الدرس ١-٧</span>
<h1 class="h1s">ترتيب العمليات الحسابية</h1>
<p class="lead">كتاب الطالب ص ٣٥</p>
<p class="lead" style="font-size:clamp(26px,4.8vh,56px)">إعداد: أ. عيسى الحارثي</p>''', 'cover'))
S.append(slide(f'''<h2>في نهاية هذا الدرس…</h2>
<div class="can">{''.join(f'<div><span class="can-i">✔</span><span><b>أنا أستطيع</b> أن {t}</span></div>' for t in CAN)}</div>'''))

# ═══ المفردات ═══
S.append(slide(f'''<h2>مفردات الدرس</h2>
{st('<div class="vocab wide"><div><span>ترتيب العمليات</span><i>order of operations</i></div><div><span>الأقواس</span><i>brackets</i></div><div><span>الأسس</span><i>indices</i></div><div><span>الجذور</span><i>roots</i></div><div><span>الضرب ×</span><i>multiplication</i></div><div><span>القسمة ÷</span><i>division</i></div><div><span>الجمع +</span><i>addition</i></div><div><span>الطرح −</span><i>subtraction</i></div></div>')}
<p class="lead">نتعلّم معاً ثم نتدرّب: <b class="c-i">أنا</b> ← <b class="c-we">نحن</b> ← <b class="c-u">أنتم</b></p>'''))

# ═══ خطة الحصة (٤٠ دقيقة) ═══
S.append(slide(f'''<span class="tag">حصة واحدة · ٤٠ دقيقة</span><h2>خطة الحصة</h2>
<div class="plan">
<div><b>٥ د</b>تهيئة: سناء أم خديجة؟</div><div><b>٨ د</b>قاعدة ترتيب العمليات</div>
<div><b>١٢ د</b>أنا ← نحن ← أنتم</div><div><b>٧ د</b>نشاط «العدد الهدف»</div><div><b>٥ د</b>ضع الأقواس</div><div><b>٣ د</b>بطاقة الخروج</div></div>''', 'divider'))

# ═══ التهيئة: تمرين ٢ (يقترحه الدليل لمناقشة النقطة الأولى) ═══
S.append(slide(f'''<div class="row hdr"><span class="qbadge">تهيئة 🤔</span>{ref('تمرين ٢')}</div><h2>أوجدت سناء وخديجة ناتج العملية نفسها</h2>
{st(box(M(P(6,2),PL,'٨',DV,'٢',cls="mid")))}
<div class="row">{st(box('<div class="col"><span class="who2">🧕 سناء</span><span class="m mid">٢٢</span></div>'))}{st(box('<div class="col"><span class="who2">🧕 خديجة</span><span class="m mid">٤٠</span></div>'))}</div>
{st('<div class="note">مَن منهما على صواب؟ صوّتوا الآن… وسنعرف الإجابة بعد قليل!</div>')}'''))

# ═══ لماذا نتّفق على ترتيب؟ (نقطة التعلّم الأولى) ═══
S.append(slide(f'''<h2>لماذا نحتاج إلى ترتيبٍ متّفقٍ عليه؟</h2>
<p class="lead st">العمليات الأربع: الجمع (+) والطرح (−) والضرب (×) والقسمة (÷)</p>
{st('<div class="note">ترتيب العمليات طريقةٌ يتّفق عليها علماء الرياضيات في <b>كل العالم</b> — فتُحلّ أيّ مسألة بالطريقة نفسها في أيّ مكان، ونحصل على <b>الناتج نفسه</b></div>')}'''))

# ═══ القاعدة + الرجل (من ورقة الملخّص) ═══
exec(open(os.path.join(HERE, 'order_building.py'), encoding='utf-8').read())   # «عمارة العمليات»
S.append(slide(f'''<div style="font-size:clamp(30px,6.5vh,76px)">{building(lambda i, h: st(h))}</div>'''))
S.append(slide(f'''<h2>🎵 نردّدها معاً</h2>
<div class="chant">{''.join(st(f'<span>{l}</span>') for l in CHANT)}</div>'''))

# ═══ الخطأ الشائع (دليل المعلم) ═══
S.append(slide(f'''<div class="row hdr"><span class="qbadge">انتبه ⚠️ خطأ شائع</span>{ref('تمرين ١ (ج)')}</div><h2>اقرأ المسألة <b class="c-exp">كاملةً</b> قبل أن تبدأ!</h2>
<div class="row">
{st(box(f'<div class="col"><span class="wrong">✘</span>{M(U('١٢',MI,'٤'),X,'٣',cls="sm")}{M(EQ,'٨',X,'٣',EQ,'٢٤',cls="sm")}<small class="hint">بدأ بالطرح لأنه جاء أولاً</small></div>',style="border-color:var(--bad);background:#FFF5F5"))}
{st(box(f'<div class="col"><span class="right">✔</span>{M('١٢',MI,U('٤',X,'٣'),cls="sm")}{M(EQ,'١٢',MI,'١٢',EQ,'٠',cls="sm")}<small class="hint">الضرب أولاً، ثم الطرح</small></div>',style="border-color:var(--good);background:#F2FBF5"))}</div>
{st('<div class="note">ضع خطاً تحت العملية ذات <b>الأولوية</b> أولاً</div>')}'''))

# ═══ أنا: مثال ١-٧ ═══
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('مثال ١-٧ (أ)')}</div><h2>أوجد ناتج: {M('٣',PL,'٤',X,'٥')}</h2>
{box(STEPS(STP('نُجري الضرب', M('٣',PL,U('٤',X,'٥'),EQ,'٣',PL,'٢٠',cls="sm")), STP('ثم الجمع', M(U('٣',PL,'٢٠'),EQ,'٢٣',cls="sm"),'fin')))}'''))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('مثال ١-٧ (ب)')}</div><h2>أوجد ناتج: {M('٣٠',DV,BR('٨',MI,'٣'))}</h2>
{box(STEPS(STP('نفكّ الأقواس أولاً', M('٣٠',DV,U(BR('٨',MI,'٣')),EQ,'٣٠',DV,'٥',cls="sm")), STP('ثم القسمة', M(U('٣٠',DV,'٥'),EQ,'٦',cls="sm"),'fin')))}'''))

# ═══ نحن: مثال ١-٧ (ج) ═══
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('مثال ١-٧ (ج)')}</div><h2>معاً: {M(P(3,2),X,'٥',MI,BR('١٩',MI,'٨'))}</h2>
<p class="ask">ما أوّل عمليةٍ ننفّذها؟ ولماذا؟</p>
{box(STEPS(STP('الأقواس', M(P(3,2),X,'٥',MI,U(BR('١٩',MI,'٨')),EQ,P(3,2),X,'٥',MI,'١١',cls="sm")),
 STP('الأسس', M(U(P(3,2)),X,'٥',MI,'١١',EQ,'٩',X,'٥',MI,'١١',cls="sm")),
 STP('الضرب', M(U('٩',X,'٥'),MI,'١١',EQ,'٤٥',MI,'١١',cls="sm")),
 STP('الطرح', M(U('٤٥',MI,'١١'),EQ,'٣٤',cls="sm"),'fin')))}'''))

# ═══ أنتم: من تمرين ١ ═══
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ١ (أ)')}{timer(3)}</div>''' + quiz(f'أوجد ناتج {M("٢",PL,"٧",X,"٥")}', [M('٤٥'), M('٣٧'), M('٢٤'), M('١٤')], 1, '٧ × ٥ = ٣٥ أولاً، ثم ٢ + ٣٥ = ٣٧ — أمّا ٤٥ فخطأ: جمعنا قبل الضرب')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ١ (ز)')}</div>''' + quiz(f'أوجد ناتج {M("٢٠",DV,"٢",PL,"٨")}', [M('٢'), M('١٨'), M('١٤'), M('٢٠')], 1, '٢٠ ÷ ٢ = ١٠ أولاً، ثم ١٠ + ٨ = ١٨ — الناتج ٢ يكون لو وُجدت أقواس: ٢٠ ÷ (٢ + ٨)')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ١ (ل)')}</div>''' + quiz(f'أوجد ناتج {M(f'<span class="b"><span>(٣ + ٢)</span><sup>٢</sup></span>')}', [M('١٣'), M('١٠'), M('٢٥'), M('٧')], 2, 'الأقواس أولاً: ٣ + ٢ = ٥ ، ثم ٥ تربيع = ٢٥ — ولا نربّع كل عددٍ وحده (٩ + ٤ = ١٣ خطأ)')))

# ═══ العودة إلى التهيئة: من الصواب؟ ═══
S.append(slide(f'''<div class="row hdr"><span class="qbadge">الآن نعرف! 🎯</span>{ref('تمرين ٢')}</div><h2>سناء أم خديجة؟</h2>
<div class="row">
{st(box(f'<div class="col"><span class="wrong">✘ سناء ٢٢</span>{M(U(BR(P(6,2),PL,'٨')),DV,'٢',cls="sm")}{M(EQ,'٤٤',DV,'٢',EQ,'٢٢',cls="sm")}<small class="hint">جمعت قبل القسمة</small></div>',style="border-color:var(--bad);background:#FFF5F5"))}
{st(box(f'<div class="col"><span class="right">✔ خديجة ٤٠</span>{M(U(P(6,2)),PL,U('٨',DV,'٢'),cls="sm")}{M(EQ,'٣٦',PL,'٤',EQ,'٤٠',cls="sm")}<small class="hint">الأسس، ثم القسمة، ثم الجمع</small></div>',style="border-color:var(--good);background:#F2FBF5"))}</div>
{st('<div class="note">ترتيبٌ واحد للعالم كلّه ← جوابٌ واحد!</div>')}'''))

# ═══ من اليمين إلى اليسار ═══
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('تمرين ٣ (ج)')}</div><h2>عمليتان من المستوى نفسه: {M('٢٠',MI,'٧',MI,'٢')}</h2>
<p class="ask">الطرح والطرح متساويان… فمن أين نبدأ؟</p>
{box(STEPS(STP('من اليمين أولاً', M(U('٢٠',MI,'٧'),MI,'٢',EQ,'١٣',MI,'٢',cls="sm")), STP('ثم التالي', M(U('١٣',MI,'٢'),EQ,'١١',cls="sm"),'fin')))}
{st('<div class="note">الجمع والطرح، وكذلك الضرب والقسمة: نُجريها <b>من اليمين إلى اليسار</b> بترتيب ظهورها</div>')}'''))

# ═══ نشاط الدليل: «العدد الهدف» ═══
S.append(slide(f'''<div class="row hdr"><span class="qbadge">نشاط 🎯</span>{timer(3)}</div><h2>لعبة «العدد الهدف»</h2>
<div class="exit">{st('<div><b>١</b><span>طالبٌ يختار <em class="kb">خمسة أرقام مختلفة</em> من ١ إلى ٩</span></div>')}{st('<div><b>٢</b><span>طالبٌ آخر يختار <em class="kb">العدد الهدف</em>: أكبر من ٤٠ وأصغر من ١٠٠</span></div>')}{st('<div><b>٣</b><span>اكتب مسألةً فيها أكثر من عملية ناتجها العدد الهدف: <em class="kb">نقطتان</em> — وبعد ٣ دقائق: الأقرب إلى الهدف <em class="kb">نقطة</em></span></div>')}</div>
'''))
S.append(slide(f'''<span class="qbadge">نشاط 🎯</span><h2>مثال: الأرقام ٢، ٣، ٥، ٧، ٩ والهدف ٦٤</h2>
<div class="row" style="align-items:center"><button class="flip box col"><span class="tap">👆 اضغط لإظهار حلٍّ ممكن</span><span class="hid col">{M('٧',X,'٩',PL,'٣',MI,'٢',EQ,'٦٣',PL,'٣',MI,'٢',EQ,'٦٤',cls="sm")}</span></button></div>'''))

# ═══ ضع الأقواس (تمرين ٣) ═══
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('تمرين ٣ (أ)')}</div><h2>ضع الأقواس: {M('٣',X,'٢',PL,'١',EQ,'٩')}</h2>
{box(STEPS(STP('بدون أقواس', M('٣',X,'٢',PL,'١',EQ,'٦',PL,'١',EQ,'٧',cls="sm"),'bad'),
 STP('نجرّب الأقواس', M('٣',X,U(BR('٢',PL,'١')),cls="sm")),
 STP('للتأكّد', M('٣',X,'٣',EQ,'٩',cls="sm"),'fin')))}'''))
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('تمرين ٣ (ب)')}</div><h2>معاً: {M('٨',MI,'٣',X,'٢',EQ,'١٠')}</h2><p class="ask">أيّ عمليةٍ نريدها أن تحدث أولاً؟</p>
{box(STEPS(STP('بدون أقواس', M('٨',MI,'٦',EQ,'٢',cls="sm"),'bad'), STP('بالأقواس', M(U(BR('٨',MI,'٣')),X,'٢',cls="sm")), STP('للتأكّد', M('٥',X,'٢',EQ,'١٠',cls="sm"),'fin')))}'''))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ٣ (د)')}{timer(2)}</div>''' + quiz(f'أين نضع الأقواس ليكون: {M("٥",PL,P(2,2),EQ,"٤٩")} ؟',
  [M(f'<span class="b"><span>(٥ + ٢)</span><sup>٢</sup></span>'), M('(٥)',PL,P(2,2)), M('٥',PL,f'<span class="b"><span>(٢)</span><sup>٢</sup></span>')], 0, '(٥ + ٢) تربيع = ٧ تربيع = ٤٩ — بدون أقواس: ٥ + ٤ = ٩')))

# ═══ فكّر (من ورقة الملخّص) ═══
S.append(slide(f'''<span class="qbadge">فكّر 💡</span><h2>عمليتان داخل الأقواس: {M(f'<span class="b">٣<sup>(١٠ − ٤ × ٢)</sup></span>')}</h2>
<p class="ask st">داخل الأقواس نطبّق الترتيب نفسه!</p>
{box(STEPS(STP('الضرب داخل القوس', M(f'<span class="b">٣<sup>(١٠ − {U("٤ × ٢")})</sup></span>',EQ,f'<span class="b">٣<sup>(١٠ − ٨)</sup></span>',cls="sm")),
 STP('ثم الطرح', M(EQ,P(3,2),cls="sm")), STP('ثم الأس', M(EQ,'٩',cls="sm"),'fin')))}'''))

# ═══ بطاقة الخروج + الواجب + الخلاصة ═══
S.append(slide(f'''<span class="qbadge">بطاقة الخروج 🎫</span><h2>أجب في دفترك قبل الخروج</h2>
<div class="exit">{st(f'<div><b>١</b>أوجد ناتج {M("٣٥",MI,"١٥",DV,"٣")}</div>')}{st(f'<div><b>٢</b>أوجد ناتج {M("٢٠",DV,BR("٢",PL,"٨"))}</div>')}{st(f'<div><b>٣</b>ضع الأقواس: {M("٢٠",MI,"٧",MI,"٢",EQ,"١٥")}</div>')}</div>
'''))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج 🎫</span><h2>الإجابات</h2>
<button class="flip box col" style="min-width:40vw"><span class="tap">👆 اضغط لإظهار الإجابات</span><span class="hid col">{M("٣٥",MI,"٥",EQ,"٣٠",cls="sm")}{M("٢٠",DV,"١٠",EQ,"٢",cls="sm")}{M("٢٠",MI,BR("٧",MI,"٢"),EQ,"١٥",cls="sm")}</span></button>'''))
S.append(slide(f'''<span class="qbadge" style="background:#0A6770;box-shadow:0 4px 0 #05393E">الواجب المنزلي 🏠</span><h2>قبل الحصة القادمة</h2>
<div class="exit">{st('<div><b>١</b>حلّ صفحة ٢٥ في كتاب النشاط</div>')}{st('<div><b>٢</b>أكمل أجزاء تمرين ١ في كتاب الطالب ص ٣٥</div>')}</div>'''))
S.append(slide(f'''<div style="font-size:clamp(26px,5.5vh,64px)">{building(sub=False)}</div>
{st('<div class="note">اقرأ كاملةً ← ضع خطاً ← احسب خطوةً خطوة</div>')}'''))

# ═══════════ ملحق: تمارين كتاب الطالب ص٣٥ ═══════════
S.append(launch('sb', '٣٥', note='المراجع: كتاب الطالب ص٣٥ ودليل المعلم ص٣٣ — إعداد: أ. عيسى الحارثي'))
PW = lambda inner, e: f'<span class="b"><span>{inner}</span><sup>{a(e)}</sup></span>'
def exs(num, title, rule, parts, per=4, src='تمرين'):  # أربعة أجزاء في الشريحة (٢×٢) ليبقى الخط كبيراً
    for k in range(0, len(parts), per): S.append(ex(num, title, rule, parts[k:k+per], cols=2, src=src))
R1 = 'الأقواس ← الأسس ← الضرب والقسمة ← الجمع والطرح (المتساوية من اليمين إلى اليسار)'
exs(1, 'أوجد ناتج العمليات الحسابية', R1, [
  ('(أ) ' + M('٢',PL,'٧',X,'٥'), M('٢',PL,'٣٥',EQ,'٣٧')),
  ('(ب) ' + M(BR('٢',MI,'٧'),X,'٥'), M(N(5),X,'٥',EQ,N(25))),
  ('(ج) ' + M('١٢',MI,'٤',X,'٣'), M('١٢',MI,'١٢',EQ,'٠')),
  ('(د) ' + M(BR('١٢',MI,'٤'),X,'٣'), M('٨',X,'٣',EQ,'٢٤')),
  ('(هـ) ' + M('٤',X,'٢',PL,'٥',X,'٣'), M('٨',PL,'١٥',EQ,'٢٣')),
  ('(و) ' + M('٤',X,BR('٢',PL,'٥'),X,'٣'), M('٤',X,'٧',X,'٣',EQ,'٨٤')),
  ('(ز) ' + M('٢٠',DV,'٢',PL,'٨'), M('١٠',PL,'٨',EQ,'١٨'))])
exs(1, 'أوجد ناتج العمليات الحسابية', R1, [
  ('(ح) ' + M('٢٠',DV,BR('٢',PL,'٨')), M('٢٠',DV,'١٠',EQ,'٢')),
  ('(ط) ' + M('٣٥',MI,'١٥',DV,'٣'), M('٣٥',MI,'٥',EQ,'٣٠')),
  ('(ي) ذهنياً ' + M('٤',X,P(2,3)), M('٤',X,'٨',EQ,'٣٢')),
  ('(ك) ' + M('١٥',X,'٣',DV,PW('(٧ − ٤)',2)), M('٤٥',DV,'٩',EQ,'٥')),
  ('(ل) ' + M(PW('(٣ + ٢)',2)), M(P(5,2),EQ,'٢٥')),
  ('(م) ' + M('٥٦',MI,PW('(١٢ + ٤)',2)), M('٥٦',MI,'٢٥٦',EQ,N(200))),
  ('(ن) ' + M(BR('٥٦',MI,'١٢'),PL,'٤'), M('٤٤',PL,'٤',EQ,'٤٨')),
  ('(س) ' + M('١٠٠',MI,PW('(٢٥ − ١٧)',2)), M('١٠٠',MI,'٦٤',EQ,'٣٦'))])
S.append(ex(2, 'سناء: ٢٢ ، خديجة: ٤٠ — من منهما على صواب؟', 'الأسس أولاً، ثم القسمة، ثم الجمع', [
  (M(P(6,2),PL,'٨',DV,'٢'), M('٣٦',PL,'٤',EQ,'٤٠') + '<small>خديجة على صواب — سناء جمعت قبل القسمة</small>')], cols=2))
exs(3, 'ضع الأقواس في المكان المناسب', 'حدِّد العملية التي يجب أن تحدث أولاً وضعها بين قوسين، ثم تأكّد بالحساب', [
  ('(أ) ' + M('٣',X,'٢',PL,'١',EQ,'٩'), M('٣',X,BR('٢',PL,'١'),EQ,'٣',X,'٣',EQ,'٩')),
  ('(ب) ' + M('٨',MI,'٣',X,'٢',EQ,'١٠'), M(BR('٨',MI,'٣'),X,'٢',EQ,'٥',X,'٢',EQ,'١٠')),
  ('(ج) ' + M('٢٠',MI,'٧',MI,'٢',EQ,'١٥'), M('٢٠',MI,BR('٧',MI,'٢'),EQ,'٢٠',MI,'٥',EQ,'١٥')),
  ('(د) ' + M('٥',PL,P(2,2),EQ,'٤٩'), M(PW('(٥ + ٢)',2),EQ,P(7,2),EQ,'٤٩'))])


# ═══════════ ملحق: حلول كتاب النشاط ص٢٥ (الإجابات من دليل المعلم ص٤٤ — الخطوات من إعداد العرض) ═══════════
S.append(launch('ab', '٢٥', note='الإجابات النهائية من دليل المعلم ص ٤٤'))
NS = 'نشاط ص ٢٥ · تمرين'
exs(1, 'أوجد ناتج العمليات الحسابية', R1, [
  ('(أ) ' + M('٨',PL,'٤',X,'٢'), M('٨',PL,'٨',EQ,'١٦')),
  ('(ب) ' + M('١٠',X,BR('٦',PL,'٣')), M('١٠',X,'٩',EQ,'٩٠')),
  ('(ج) ' + M('١٦',MI,'٨',DV,'٢'), M('١٦',MI,'٤',EQ,'١٢')),
  ('(د) ' + M(BR('٢',PL,'٥'),X,'٤'), M('٧',X,'٤',EQ,'٢٨')),
  ('(هـ) ' + M(PW('٥', '(٤ − ٤ × ٣)')), M('الأس:','٤',MI,'١٢',EQ,N(8)) + M(EQ,f'<span class="b">٥<sup>{N(8)}</sup></span>')),
  ('(و) ' + M('١٦',MI,'٨',DV,'٢'), M('١٦',MI,'٤',EQ,'١٢')),
  ('(ز) ' + M('١٨',DV,'٣',PL,'٤'), M('٦',PL,'٤',EQ,'١٠')),
  ('(ح) ' + M(PW('(٢ + ٨)',2)), M(P(10,2),EQ,'١٠٠')),
  ('(ط) ' + M('٥٠',MI,P(6,2)), M('٥٠',MI,'٣٦',EQ,'١٤')),
  ('(ي) ' + M('٦',PL,'١٢',DV,'٤'), M('٦',PL,'٣',EQ,'٩')),
  ('(ك) ' + M(BR('٢٠',MI,'١٢'),X,'٤'), M('٨',X,'٤',EQ,'٣٢')),
  ('(ل) ' + M(PW('(٣ + ٥)','(٢ ÷ ٢)')), M('الأس:','٢',DV,'٢',EQ,'١') + M(P(8,1),EQ,'٨'))], src=NS)
S.append(ex(2, 'مريم: ٤٥ ، حسن: ٧ — ناتج ' + M('٥٧',MI,P(6,2),DV,'٣'), 'الأسس أولاً، ثم القسمة، ثم الطرح', [
  ('(أ) أيّ الإجابتين صحيحة؟', M('٥٧',MI,U('٣٦',DV,'٣')) + M(EQ,'٥٧',MI,'١٢',EQ,'٤٥') + '<small>مريم على حق</small>'),
  ('(ب) ما خطأ حسن؟', M(U(BR('٥٧',MI,'٣٦')),DV,'٣') + M(EQ,'٢١',DV,'٣',EQ,'٧') + '<small>طرح قبل القسمة</small>')], cols=2, src=NS))
exs(3, 'ضع الأقواس في المكان المناسب', 'حدِّد العملية التي يجب أن تحدث أولاً وضعها بين قوسين، ثم تأكّد بالحساب', [
  ('(أ) ' + M('٦',X,'٥',MI,'٢',EQ,'١٨'), M('٦',X,BR('٥',MI,'٢'),EQ,'٦',X,'٣',EQ,'١٨')),
  ('(ب) ' + M('٧',PL,'٣',X,'٥',EQ,'٥٠'), M(BR('٧',PL,'٣'),X,'٥',EQ,'١٠',X,'٥',EQ,'٥٠')),
  ('(ج) ' + M('٢٠',PL,'٦',DV,'٢',EQ,'١٣'), M(BR('٢٠',PL,'٦'),DV,'٢',EQ,'٢٦',DV,'٢',EQ,'١٣'))], src=NS)

EXTRA_CSS_OWN = '''
.now{display:inline-flex;gap:.28em;align-items:baseline;border-bottom:.09em solid var(--exp);padding-bottom:.02em}
.brk{display:inline-flex;gap:.2em;align-items:baseline;direction:rtl;unicode-bidi:isolate}
.stps{display:flex;flex-direction:column;gap:1.6vh;align-items:stretch}
.stp{display:flex;align-items:center;gap:1.4vw;justify-content:space-between}
.stp .lab{flex:none;font-family:var(--fh);font-weight:800;font-size:clamp(17px,2.8vh,30px);color:#2563EB;background:#EAF1FF;border-radius:12px;padding:.2em .8em;min-width:7em;text-align:center}
.stp.fin .lab{background:var(--good);color:#fff}.stp.fin .m{color:var(--good)}
.stp.bad .lab{background:#FDE7E3;color:var(--bad)}.stp.bad .m{color:var(--bad);text-decoration:line-through;text-decoration-thickness:.06em}
.ord{display:flex;flex-direction:column;gap:1.4vh;min-width:min(620px,60vw)}
.ord .st>div,.ord>div{display:flex;align-items:center;gap:1em;background:#fff;border:3px solid;border-radius:18px;padding:1.1vh 1.4vw;font-weight:700;font-size:clamp(22px,3.8vh,42px)}
.ord b{font-family:var(--fh)}
.ord div>b:first-child{color:#fff;border-radius:50%;width:1.6em;height:1.6em;display:flex;align-items:center;justify-content:center;flex:none}
.o1{border-color:#2563EB!important}.o1>b:first-child{background:#2563EB}.o2{border-color:var(--exp)!important}.o2>b:first-child{background:var(--exp)}
.o3{border-color:#7A3FD1!important}.o3>b:first-child{background:#7A3FD1}.o4{border-color:var(--good)!important}.o4>b:first-child{background:var(--good)}
.can .o1{color:#2563EB}.can .o2{color:var(--exp)}.can .o3{color:#7A3FD1}.can .o4{color:var(--good)}
.man{width:min(22vw,250px);height:auto}
.man circle,.man line,.man path{fill:none;stroke-width:7;stroke-linecap:round;stroke-linejoin:round}
.man .bd{stroke:var(--ink)}.man .o1s{stroke:#2563EB}.man .o2s{stroke:var(--exp)}.man .o3s{stroke:#7A3FD1}.man .o4s{stroke:var(--good)}
.man .mt{font-family:var(--fh);font-weight:900;font-size:34px;text-anchor:middle}.man .mt2{font-family:var(--fh);font-weight:800;font-size:20px;text-anchor:middle}
.man .o1t{fill:#2563EB}.man .o2t{fill:var(--exp)}.man .o3t{fill:#7A3FD1}.man .o4t{fill:var(--good)}
.exit .kb{font-style:normal;color:var(--exp);font-weight:900}
.chant{display:flex;flex-direction:column;gap:2vh;background:#FFF6E3;border:3px dashed var(--gold);border-radius:22px;padding:2vh 2vw;max-width:34vw;text-align:center}
.chant b{font-family:var(--fh);font-size:clamp(20px,3vh,32px);color:var(--ink2)}
.chant span{font-weight:800;font-size:clamp(20px,3.3vh,36px);line-height:1.6}
.hl2{color:var(--exp)}

.who2{font-family:var(--fh);font-weight:900;font-size:clamp(22px,3.6vh,38px)}
'''
