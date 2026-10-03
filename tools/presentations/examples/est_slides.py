# شرائح درس ٣-٨ «التقدير والتقريب» — الصف السابع (حصتان، كتاب الطالب ص٧٤–٧٥)
# المراجع: دليل المعلم ص٧٥–٧٦ (التحقّق بالتقدير أو بالعمليات العكسية واختيار الأنسب، كتابة كلماتٍ توضّح الحل؛
# الخطأ الشائع: إعادة المحاولة الأولى بدل التقدير أو العكس؛ النشاط: بطاقات ورقة المصادر ٣-٨)،
# كتاب الطالب ص٧٤–٧٥ (مثال ٣-٨)، وإجابات الدليل ص٧٩ (كتاب الطالب) وص٨٤ (كتاب النشاط ص٥٥–٥٧).
# python3.12 gen_powers.py est_slides.py التقدير_والتقريب_عرض_تفاعلي.html "التقدير والتقريب — الصف السابع"
exec(open(os.path.join(HERE, 'vcol.py'), encoding='utf-8').read())
exec(open(os.path.join(HERE, 'figs.py'), encoding='utf-8').read())

DV = '<span class="x">÷</span>'
AP = '<span class="x">≈</span>'
def STP(lab, expr='', cls=''): return st(f'<div class="stp {cls}"><span class="lab">{lab}</span>{expr}</div>')
def STEPS(*rows): return '<div class="stps">' + ''.join(rows) + '</div>'
def TAGS(*items): return '<div class="figrow tags">' + ''.join(f'<div class="ptag"><span>{ic}</span><small>{n}</small><b>{v}</b></div>' for ic, n, v in items) + '</div>'
S = []
ME = 'إعداد: أ. عيسى الحارثي'
S.append(slide(f'''<span class="tag">الصف السابع · الدرس ٣-٨</span>
<h1 class="h1s">التقدير والتقريب</h1>
<p class="lead">كتاب الطالب ص ٧٤ و ٧٥ · حصتان</p>
<p class="lead" style="font-size:clamp(26px,4.8vh,56px)">{ME}</p>''', 'cover'))
CAN = ['أقرّب الأعداد في السؤال لأجد <b>ناتجاً تقريبياً</b>', 'أتحقّق من صحة إجابتي <b>بالتقدير</b> أو <b>بالعمليات العكسية</b>', 'أحلّ <b>مسائل حياتية</b> من عدّة خطوات وأكتب كلماتٍ توضّح الحل']
S.append(slide(f'''<h2>في نهاية هذا الدرس…</h2>
<div class="can">{''.join(f'<div><span class="can-i">✔</span><span><b>أنا أستطيع</b> أن {t}</span></div>' for t in CAN)}</div>'''))
S.append(slide(f'''<h2>مفردات الدرس</h2>
{st('<div class="vocab wide"><div><span>التقدير</span><i>estimate</i></div><div><span>الناتج التقريبي</span><i>approximate answer</i></div><div><span>العملية العكسية</span><i>inverse operation</i></div></div>')}
<p class="lead">حصتان: <b class="c-i">أنا</b> ← <b class="c-we">نحن</b> ← <b class="c-u">أنتم</b></p>'''))

# ═══════════ الحصة الأولى: التقدير ═══════════
S.append(slide('''<span class="tag">الحصة الأولى · ٤٠ دقيقة</span><h2>التحقّق بالتقدير</h2>
<div class="plan"><div><b>٤ د</b>تهيئة</div><div><b>٦ د</b>قاعدة التقريب</div><div><b>٨ د</b>مثال ٣-٨ (ب)</div>
<div><b>٧ د</b>نحن</div><div><b>٧ د</b>أنتم</div><div><b>٥ د</b>واجب عائشة</div><div><b>٣ د</b>بطاقة الخروج</div></div>''', 'divider'))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">تهيئة 🤔</span></div><h2>كتب خالد: ٤٩ × ٢١ = ١٠٢٩</h2>
{st('<div class="note">من دون آلة حاسبة: هل الإجابة معقولة؟</div>')}
{st(f'<div class="note">٥٠ × ٢٠ = ١٠٠٠ ، و ١٠٢٩ قريبٌ من ١٠٠٠ ← <b>الإجابة معقولة</b></div>')}''' + tn('من خارج المرجع (الأعداد من إعدادي): ٤٩ × ٢١ = ١٠٢٩ صحيحة. الفكرة: التقدير يكشف الأخطاء الكبيرة بسرعة.')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('كتاب الطالب ص ٧٤')}</div><h2>نقرّب كل عددٍ في السؤال</h2>
<table class="rt">{''.join(f'<tr class="st"><td>{a_}</td><td>{b_}</td><td>{M(c_, cls="sm")}</td></tr>' for a_, b_, c_ in (
  ('رقمٌ واحد (٠ إلى ٩)', 'إلى أقرب عدد كامل', '٤٫٦ ≈ ٥'), ('رقمان (١٠ إلى ٩٩)', 'إلى أقرب ١٠', '٥٩ ≈ ٦٠'),
  ('ثلاثة أرقام', 'إلى أقرب ١٠٠', '٤٩٣ ≈ ٥٠٠'), ('أربعة أرقام', 'إلى أقرب ١٠٠٠', '٤٧٢٠ ≈ ٥٠٠٠')))}</table>
{st('<div class="note">ثم نحسب الناتج التقريبي: إذا كانت الإجابة قريبةً منه فهي صحيحة</div>')}''' + tn('الأمثلة في العمود الأخير من إعدادي لتوضيح القاعدة (العدد ٤٫٦ من مثال ٣-٨).')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('مثال ٣-٨ (ب)')}</div><h2>كم سعرةً حرارية في وجبة إفطار سالم؟</h2>
{TAGS(('🍞🍞', 'شريحتا خبز', '٥٩ × ٢'), ('🧈', 'زبدة', '٧٤'), ('🍯', 'مربّى', '٣٢'), ('🍐', 'كمثرى', '٦٨'))}
<div class="row vrow">{STEPS(STP('الحساب', M('١١٨ + ٧٤ + ٣٢ + ٦٨ = ٢٩٢', cls='sm')), STP('التقدير', M('١٢٠ + ٧٠ + ٣٠ + ٧٠ = ٢٩٠', cls='sm')), STP('٢٩٠ قريبٌ من ٢٩٢', M('صحيحة ✔', cls='sm'), 'fin'))}</div>''' + tn('كل الأعداد من رقمين فنقرّبها إلى أقرب ١٠. الرسوم التوضيحية (الرموز) من إعدادي.')))
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('نشاط ص ٥٥ · تمرين ١ (أ، ب)')}</div><h2>معاً: قدّر الناتج</h2>
<div class="row">{st(f'<button class="flip box col" style="flex:1"><span class="hint">٧٢ + ٢٩</span><span class="tap">👆</span><span class="hid col">{M("٧٠ + ٣٠ = ١٠٠", cls="sm")}</span></button>')}{st(f'<button class="flip box col" style="flex:1"><span class="hint">٦٢٣ − ٤٩٣</span><span class="tap">👆</span><span class="hid col">{M("٦٠٠ − ٥٠٠ = ١٠٠", cls="sm")}</span></button>')}</div>'''))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('نشاط ص ٥٥ · تمرين ١ (ج)')}{timer(1)}</div>''' + quiz('قدّر ناتج ٨٢ ÷ ٢٢', [M('٤'), M('٤٠'), M('٣٫٧٢'), M('٢')], 0, '٨٠ ÷ ٢٠ = ٤')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('نشاط ص ٥٥ · تمرين ١ (د)')}</div>''' + quiz('قدّر ناتج ٤٧٧ × ٣١', [M('١٥٠٠'), M('١٥٠٠٠'), M('١٢٠٠٠'), M('١٤٧٨٧')], 1, 'ثلاثة أرقام ← ٥٠٠، ورقمان ← ٣٠: ٥٠٠ × ٣٠ = ١٥٠٠٠')))
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('نشاط ص ٥٥ · تمرين ٢')}</div><h2>واجب عائشة: هل إجاباتها صحيحة؟</h2>
<div class="row vrow">{st(FIG('3-8_aisha'))}{STEPS(STP('(أ)', M('٦٠٠ + ٤٠٠ = ١٠٠٠', cls='sm')), STP('(ب)', M('٧٠ − ٥٠ = ٢٠', cls='sm')), STP('(ج)', M('٩٠٠ ÷ ٣٠ = ٣٠', cls='sm')), STP('(د)', M('٥٠ × ٢٠ = ١٠٠٠', cls='sm')), STP('كل التقديرات قريبة', M('إجاباتها معقولة ✔', cls='sm'), 'fin'))}</div>''' + tn('في (ب) التقدير ٢٠ والإجابة ٢٨: الفرق كبيرٌ نسبياً لأن الأعداد صغيرة، فالعملية العكسية أدقّ: ٢٨ + ٤٦ = ٧٤ ✔ (الجزء ٢ من التمرين).')))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ١ 🎫</span><h2>قدّر الناتج</h2>
<div class="exit">{st('<div><b>١</b>٣٨ + ٥٧ + ٢٢</div>')}{st('<div><b>٢</b>٩٢٨ ÷ ٣٢</div>')}{st('<div><b>٣</b>٢٤ × ٤٧</div>')}</div>''' + tn('الأعداد من مسائل الكتاب وكتاب النشاط.')))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ١ 🎫</span><h2>الإجابات</h2>
<button class="flip box col" style="min-width:40vw"><span class="tap">👆 اضغط لإظهار الإجابات</span><span class="hid col">{M('٤٠ + ٦٠ + ٢٠ = ١٢٠', cls="sm")}{M('٩٠٠ ÷ ٣٠ = ٣٠', cls="sm")}{M('٢٠ × ٥٠ = ١٠٠٠', cls="sm")}</span></button>'''))

# ═══════════ الحصة الثانية: العمليات العكسية والمسائل ═══════════
S.append(slide('''<span class="tag">الحصة الثانية · ٤٠ دقيقة</span><h2>العمليات العكسية والمسائل</h2>
<div class="plan"><div><b>٣ د</b>إحماء</div><div><b>٨ د</b>مثال ٣-٨ (أ)</div><div><b>٦ د</b>مدّخرات أسماء</div>
<div><b>٧ د</b>عرضا التلفاز</div><div><b>٦ د</b>أنتم: ناصر</div><div><b>٦ د</b>نشاط البطاقات</div><div><b>٤ د</b>بطاقة الخروج</div></div>''', 'divider'))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">إحماء 🔥</span>{timer(1)}</div>''' + quiz('ما العملية العكسية للطرح؟', [M('الجمع'), M('الضرب'), M('القسمة'), M('الطرح')], 0, 'الجمع يعكس الطرح، والقسمة تعكس الضرب')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('مثال ٣-٨ (أ)')}</div><h2>كتلة سالم ٨٩٫٢ كغم، ويريد ٧٢٫٥ كغم</h2>
<div class="row vrow">{STEPS(STP('ما يجب أن يفقده', M('٨٩٫٢ − ٧٢٫٥ = ١٦٫٧', cls='sm')), STP('فقد ٤٫٦ في شهر', M('١٦٫٧ − ٤٫٦ = ١٢٫١', cls='sm')), STP('نتحقّق بالعكس', M('١٢٫١ + ٤٫٦ = ١٦٫٧ ✔', cls='sm')), STP('ونتحقّق', M('١٦٫٧ + ٧٢٫٥ = ٨٩٫٢ ✔', cls='sm')), STP('لا يزال يحتاج أن يفقد', M('١٢٫١ كغم', cls='sm'), 'fin'))}</div>''' + tn('من الدليل: شجّع الطلاب على اختيار الطريقة الأنسب للتحقّق (التقدير أو العكس) بدل استخدام طريقتهم المفضّلة تلقائياً، وعلى كتابة كلمات توضّح الحل.')))
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('تمرين ١')}</div><h2>مدّخرات أسماء للعمرة: تحتاج ٣٥٠ ريالاً</h2>
<div class="row vrow">{st(FIG('3-8_savings'))}{STEPS(STP('نجمع المبالغ السبعة', M('٣٠٥ ريالاً', cls='sm')), STP('التقدير: ٤٠+٦٠+٢٠+٥٠+٧٠+٥٠+٢٠', M('٣١٠ ✔', cls='sm')), STP('الباقي', M('٣٥٠ − ٣٠٥ = ٤٥', cls='sm'), 'fin'))}</div>''' + tn('التقدير ٣١٠ قريبٌ من ٣٠٥، فالجمع صحيح. الإجابة: ٤٥ ريالاً (الدليل).')))
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('تمرين ٣')}</div><h2>عرضان لشراء تلفاز</h2>
<div class="row vrow">{st(FIG('3-8_tv', 'fig sm'))}{STEPS(STP('الأقساط', M('٨ × ٨٢ = ٦٥٦', cls='sm')), STP('العرض الثاني', M('١١٥ + ٦٥٦ = ٧٧١', cls='sm')), STP('الفرق بين العرضين', M('٧٧١ − ٦٩٩ = ٧٢', cls='sm'), 'fin'), STP('التقدير', M('١٠٠ + ٦٤٠ = ٧٤٠', cls='sm')))}</div>''' + tn('العرض الأول نقداً ٦٩٩ ريالاً أوفر بـ ٧٢ ريالاً.')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ٢ (أ)')}{timer(2)}</div>''' + quiz('ناصر يأخذ ١٠ ريالات للساعة و ٥ ريالات رسوماً. كم يأخذ مقابل ساعتين ونصف؟', [M('٢٥'), M('٣٠'), M('٣٥'), M('٢٠')], 1, '٢٫٥ × ١٠ + ٥ = ٣٠ ريالاً')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ٢ (ب)')}</div>''' + quiz('حصل ناصر على ١٧١ ريالاً. كم ساعةً عمل؟', [M('١٧ ساعة و ١٠ دقائق'), M('١٦ ساعة و ٣٦ دقيقة'), M('١٦ ساعة و ٦ دقائق'), M('١٧ ساعة')], 1, '(١٧١ − ٥) ÷ ١٠ = ١٦٫٦ ساعة = ١٦ ساعة و ٣٦ دقيقة (٠٫٦ × ٦٠ = ٣٦)')))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">انتبه ⚠️ خطأ شائع</span>{ref('دليل المعلم ص ٧٥')}</div><h2>لا نعيد المحاولة نفسها للتحقّق</h2>
<div class="row">{st(box('<div class="col"><span class="hint no">✘ أعدنا الحساب نفسه</span><span class="big2">قد نكرّر الخطأ نفسه</span></div>', style="flex:1"))}{st(box('<div class="col"><span class="hint ok">✔ تقدير أو عملية عكسية</span><span class="big2">طريقةٌ مختلفة تكشف الخطأ</span></div>', style="flex:1"))}</div>'''))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">نشاط 🃏</span>{ref('نشاط دليل المعلم')}</div><h2>سلسلة بطاقات التقدير</h2>
<div class="exit">{st('<div><b>١</b>في مجموعات من ٣ أو ٤: ١٨ بطاقة من ورقة المصادر ٣-٨</div>')}{st('<div><b>٢</b>نكتب سؤالاً تقديرياً ناتجه في أعلى البطاقة التالية (من ٣٥٠ إلى ٥٠ …)</div>')}{st('<div><b>٣</b>نتبادل البطاقات ونلعب: من يُنهي بطاقاته أولاً يفوز</div>')}</div>''' + tn('نشاط الدليل بعد تمارين ٣-٨: الغرض تقدير النواتج لا نتائج دقيقة. إن لم يتّسع الوقت فاجعله واجباً (أسئلة ونتائج على الورقة).')))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ٢ 🎫</span><h2>حلّ وتحقّق</h2>
<div class="exit">{st('<div><b>١</b>لدى فريدة ٦ دجاجات، تنتج كلٌّ منها ٥ بيضات أسبوعياً: كم بيضة في السنة (٥٢ أسبوعاً)؟</div>')}{st('<div><b>٢</b>تحقّق من إجابتك بطريقة مختلفة</div>')}</div>'''))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ٢ 🎫</span><h2>الإجابة</h2>
<button class="flip box col" style="min-width:40vw"><span class="tap">👆 اضغط لإظهار الإجابة</span><span class="hid col">{M('٦ × ٥ × ٥٢ = ١٥٦٠ بيضة', cls="sm")}{M('١٥٦٠ ÷ ٥٢ ÷ ٥ = ٦ ✔', cls="sm")}</span></button>'''))
S.append(slide('''<span class="qbadge" style="background:#0A6770;box-shadow:0 4px 0 #05393E">الواجب المنزلي 🏠</span><h2>بعد الحصتين</h2>
<div class="exit"><div class="st"><div><b>١</b>صفحة ٥٥ في كتاب النشاط (التقدير والتحقّق)</div></div><div class="st"><div><b>٢</b>صفحتا ٥٦ و ٥٧ في كتاب النشاط (مسائل حياتية)</div></div></div>'''))
S.append(slide(f'''<h2>الخلاصة</h2>
<div class="sumg">
{st(box('<div class="col"><b class="kk c-exp">نقرّب</b><span>كل عددٍ حسب عدد أرقامه</span></div>'))}
{st(box('<div class="col"><b class="kk c-we">نقدّر</b><span>الناتج التقريبي قريبٌ من الإجابة</span></div>'))}
{st(box('<div class="col"><b class="kk c-lcm">نعكس</b><span>العملية للتحقّق الدقيق</span></div>'))}</div>'''))

# ═══════════ ملحق: تمارين كتاب الطالب ص٧٥ (الإجابات من دليل المعلم ص٧٩) ═══════════
S.append(launch('sb', '٧٥', note=f'المراجع: كتاب الطالب ص٧٤ و ٧٥، ودليل المعلم ص٧٥ و ٧٦ وإجاباته ص٧٩ · {ME}'))
RP = 'نحلّ بخطوات واضحة، ثم نتحقّق بالتقدير أو بالعملية العكسية'
S.append(ex(1, 'مدّخرات أسماء', RP, [(FIG('3-8_savings') + 'تحتاج أسماء ٣٥٠ ريالاً: كم تحتاج أن تدّخر بعد؟', '٣٥٠ − ٣٠٥ = ٤٥ ريالاً<small>المجموع ٣٠٥، والتقدير ٣١٠</small>')], cols=1))
S.append(ex(2, 'ناصر الكهربائي', RP, [('(أ) ١٠ ريالات للساعة و ٥ ريالات رسوم: كم يأخذ عن ساعتين ونصف؟', '٢٫٥ × ١٠ + ٥ = ٣٠ ريالاً'), ('(ب) حصل على ١٧١ ريالاً: كم استغرق العمل؟', '(١٧١ − ٥) ÷ ١٠ = ١٦٫٦<small>١٦ ساعة و ٣٦ دقيقة</small>')], cols=1))
S.append(ex(3, 'عرضا التلفاز', RP, [(FIG('3-8_tv', 'fig side') + '(أ) تكلفة العرض الثاني (ب) الفرق بين العرضين', '(أ) ١١٥ + ٨ × ٨٢ = ٧٧١ ريالاً<small>(ب) ٧٧١ − ٦٩٩ = ٧٢ ريالاً</small>')], cols=1))
S.append(ex(4, 'دجاجات فريدة', RP, [('(أ) ٦ دجاجات، ٥ بيضات لكلٍّ أسبوعياً: كم بيضة في السنة؟', '٦ × ٥ × ٥٢ = ١٥٦٠ بيضة'), ('(ب) تبيع كل ١٠ بيضات بـ ١٫٢٥٠ ريال: كم تجمع في السنة؟', '١٥٦ × ١٫٢٥٠ = ١٩٥ ريالاً<small>الدليل كتب ٣٢٥ (كأنها ١٢ بيضة بـ ٢٫٥)</small>')], cols=1,
  note='في إجابات الدليل ص ٧٩: ٤ (ب) = ٣٢٥ ريالاً، والصحيح بحسب الكتاب: ١٥٦٠ ÷ ١٠ = ١٥٦ مجموعة × ١٫٢٥٠ = ١٩٥ ريالاً.'))

# ═══════════ ملحق: حلول كتاب النشاط ص٥٥–٥٧ (الإجابات من دليل المعلم ص٨٤) ═══════════
S.append(launch('ab', '٥٥ إلى ٥٧', note='الإجابات من دليل المعلم ص ٨٤'))
NA, NB, NC = 'نشاط ص ٥٥ · تمرين', 'نشاط ص ٥٦ · تمرين', 'نشاط ص ٥٧ · تمرين'
S.append(ex(1, 'قدّر الناتج', 'نقرّب كل عددٍ حسب عدد أرقامه', [('(أ) ٧٢ + ٢٩', '٧٠ + ٣٠ = ١٠٠'), ('(ب) ٦٢٣ − ٤٩٣', '٦٠٠ − ٥٠٠ = ١٠٠'), ('(ج) ٨٢ ÷ ٢٢', '٨٠ ÷ ٢٠ = ٤'), ('(د) ٤٧٧ × ٣١', '٥٠٠ × ٣٠ = ١٥٠٠٠')], cols=2, src=NA))
S.append(ex(2, 'واجب عائشة', 'بالتقدير، ثم بالعمليات العكسية', [(FIG('3-8_aisha', 'fig side') + '(١) بالتقدير', '١٠٠٠ ، ٢٠ ، ٣٠ ، ١٠٠٠'), (FIG('3-8_aisha', 'fig side') + '(٢) بالعمليات العكسية', '١٠١٣ − ٤٢٤ = ٥٨٩ ، ٢٨ + ٤٦ = ٧٤<small>٢٩ × ٣٢ = ٩٢٨ ، ١١٢٨ ÷ ٢٤ = ٤٧</small>')], cols=1, src=NA))
S.append(ex(3, 'عربات التسوّق', '٢٠ بيسة لكل عربة، ثم نقرّب لأقرب ريال', [(FIG('3-8_carts', 'fig side') + 'كم يحصل جمال في الأسبوع؟', '٤٠١ × ٠٫٠٢٠ = ٨٫٠٢٠ ≈ ٨ ريالات')], cols=1, src=NA))
S.append(ex(4, 'بدر فنّي الكهرباء', '٢٨ ريالاً للساعة و ٣٠ ريالاً رسوماً', [('(أ) ٣٫٥ ساعة: كم يحصل؟', '٣٫٥ × ٢٨ + ٣٠ = ١٢٨ ريالاً'), ('(ب) حصل على ٦٥ ريالاً: كم ساعة عمل؟', '(٦٥ − ٣٠) ÷ ٢٨ = ١٫٢٥<small>ساعة و ١٥ دقيقة</small>')], cols=1, src=NB))
S.append(ex(5, 'سيارة كوثر', 'نحسب التقسيط ثم نطرح السعر النقدي', [('نقداً ١٧٩٩٥ ريالاً، أو ٤٩٩٥ ثم ٣٦ قسطاً × ٤٢٠: كم التكلفة الزائدة؟', '٤٩٩٥ + ١٥١٢٠ = ٢٠١١٥<small>٢٠١١٥ − ١٧٩٩٥ = ٢١٢٠ ريالاً</small>')], cols=1, src=NB))
S.append(ex(6, 'كعك سلمى', 'عدد الكعكات ثم عدد مجموعات الأربع', [('٧٠ كعكة يومياً، ٥ أيام × ٤٦ أسبوعاً، و ١٤٫٧٥٠ ريالاً لكل ٤: كم تجني؟', '٧٠ × ٥ × ٤٦ = ١٦١٠٠ كعكة<small>١٦١٠٠ ÷ ٤ × ١٤٫٧٥٠ = ٥٩٣٦٨٫٧٥٠ ريالاً</small>')], cols=1, src=NC))

EXTRA_CSS_OWN = '''
.stps{display:flex;flex-direction:column;gap:1.1vh;align-items:stretch}
.stp{display:flex;align-items:center;gap:1.4vw;justify-content:space-between}
.stp .lab{flex:0 1 auto;max-width:60%;font-family:var(--fh);font-weight:800;color:#2563EB;background:#EAF1FF;border-radius:12px;padding:.2em .8em;text-align:center;line-height:1.4;font-size:clamp(20px,3.5vh,40px)}
.stp.fin .lab{background:var(--good);color:#fff}
.slide .vrow{align-items:center;justify-content:center;gap:2vh 3vw;flex-wrap:wrap}
.slide .vrow>.stps{flex:0 1 auto;max-width:min(1300px,90vw)}
@media (max-aspect-ratio:1/1){.slide .vrow{flex-direction:column}.slide .vrow>.stps{max-width:92vw}.stp{flex-wrap:wrap;justify-content:center}}
.tags{gap:1.6vw}
.ptag{display:flex;flex-direction:column;align-items:center;background:#FFF6E3;border:3px solid #E9A23B;border-radius:18px 18px 18px 4px;padding:.8vh 1.4vw;font-family:var(--fh)}
.ptag span{font-size:clamp(34px,7vh,80px)}.ptag small{font-size:clamp(16px,2.6vh,28px);color:var(--ink2)}.ptag b{font-size:clamp(22px,4vh,46px)}
.rt{border-collapse:separate;border-spacing:0 1vh;font-weight:700;font-size:clamp(22px,4vh,46px)}
.rt td{background:#fff;border-top:3px solid var(--line);border-bottom:3px solid var(--line);padding:.6vh 1.4vw;text-align:center}
.rt td:first-child{border-right:3px solid var(--line);border-radius:0 14px 14px 0;color:#2563EB}.rt td:last-child{border-left:3px solid var(--line);border-radius:14px 0 0 14px}
.big2{font-weight:700;font-size:clamp(24px,4.4vh,50px);line-height:1.4}
.box .col>.m:not(.mid):not(.sm):not(.big),.hid.col>.m:not(.mid):not(.sm):not(.big){font-size:clamp(32px,6vh,70px)}
.hint.no{color:var(--bad)}.hint.ok{color:var(--good)}
.sumg{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:2vw;width:min(1600px,94vw)}
.sumg .col span{font-weight:700;font-size:clamp(24px,4.4vh,52px);line-height:1.4}
.sumg .kk{font-size:clamp(30px,5.6vh,66px)}
.xa small{display:block}
''' + FIG_CSS
