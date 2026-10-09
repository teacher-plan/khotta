# شرائح درس ٥-٢ «قياسات الزوايا» — الصف السابع (حصتان، كتاب الطالب ص٩٤–٩٥)
# المراجع: دليل المعلم ص٩٧–٩٨ (المفردات: رباعي الأضلاع؛ نقاط التعلّم: الحقائق الثلاث (حول نقطة ٣٦٠°، على خط مستقيم ١٨٠°، المثلث ١٨٠°)،
# ورباعي الأضلاع ٣٦٠° بتقسيمه إلى مثلثين، وحلّ التمارين بخطواتٍ تبدأ بالزوايا المعروفة؛ الخطأ الشائع: الخلط بين الحقائق؛
# النشاط: الخماسي المنتظم في دائرة (مضاعفات ٧٢°)؛ تعليقات التمرينين ٧ و٨؛ الواجب: النشاط ص٦٥–٦٧)،
# كتاب الطالب ص٩٤–٩٥ (مثال ٥-٢)، وإجابات الدليل ص١٠٢ (كتاب الطالب) وص١٠٥ (كتاب النشاط).
# python3.12 gen_powers.py angmeas_slides.py قياسات_الزوايا_عرض_تفاعلي.html "قياسات الزوايا — الصف السابع"
exec(open(os.path.join(HERE, 'figs.py'), encoding='utf-8').read())

def STP(lab, expr='', cls=''): return st(f'<div class="stp {cls}"><span class="lab">{lab}</span>{expr}</div>')
def STEPS(*rows): return '<div class="stps">' + ''.join(rows) + '</div>'
def VC(items, cls=''): return f'<div class="voc3 {cls}">' + ''.join(st(f'<div><b>{w}</b><i>{e}</i><span>{d}</span></div>') for w, e, d in items) + '</div>'
def FACT(n, t, s): return st(f'<div class="fact"><b>{n}</b><span>{t}</span><i>{s}</i></div>')
MI = '<span class="x">−</span>'; PL = '<span class="x">+</span>'; DV = '<span class="x">÷</span>'
S = []
ME = 'إعداد: أ. عيسى الحارثي'
S.append(slide(f'''<span class="tag">الصف السابع · الدرس ٥-٢</span>
<h1 class="h1s">قياسات الزوايا</h1>
<p class="lead">كتاب الطالب ص ٩٤ و ٩٥ · حصتان</p>
<p class="lead" style="font-size:clamp(26px,4.8vh,56px)">{ME}</p>''', 'cover'))
CAN = ['أستخدم <b>حقائق الزوايا</b> لأحسب زاويةً مجهولة دون منقلة', 'أعرف أن مجموع زوايا <b>المثلث ١٨٠°</b>', 'أعرف أن مجموع زوايا <b>رباعي الأضلاع ٣٦٠°</b>']
S.append(slide(f'''<h2>في نهاية هذا الدرس…</h2>
<div class="can">{''.join(f'<div><span class="can-i">✔</span><span><b>أنا أستطيع</b> أن {t}</span></div>' for t in CAN)}</div>'''))
S.append(slide(f'''<h2>مفردة الدرس</h2>
{VC([('رباعي الأضلاع', 'quadrilateral', 'شكلٌ مكوّن من أربعة أضلاع')], 'c1')}''' + tn('المفردة من الدليل ص٩٧، والتعريف من الكتاب ص٩٤.')))

# ═══════════ الحصة الأولى ═══════════
S.append(slide('''<span class="tag">الحصة الأولى · ٤٠ دقيقة</span><h2>حقائق الزوايا والمثلث</h2>
<div class="plan"><div><b>٤ د</b>تذكّر</div><div><b>٨ د</b>الحقائق الثلاث</div><div><b>٨ د</b>زوايا على خط وحول نقطة</div>
<div><b>٨ د</b>زوايا المثلث</div><div><b>٦ د</b>نحن ← أنتم</div><div><b>٣ د</b>انتبه</div><div><b>٣ د</b>بطاقة الخروج</div></div>''', 'divider'))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">تذكّر 🔁</span>{ref('الدرس ٥-١')}{timer(1)}</div>''' + quiz('الزاوية المستقيمة قياسها…', [M('٩٠°'), M('١٨٠°'), M('٣٦٠°')], 1, 'نصف دورة = ١٨٠°')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('كتاب الطالب ص ٩٤')}</div><h2>حقائق مهمّة حول الزوايا</h2>
<div class="facts">{FACT('٣٦٠°', 'حول نقطة', 'دورة كاملة')}{FACT('١٨٠°', 'على خطٍّ مستقيم', 'نصف دورة')}{FACT('١٨٠°', 'زوايا المثلث', 'س + ص + ع')}</div>''' + tn('الكتاب ص٩٤: مجموع قياسات الزوايا حول نقطة ٣٦٠°، وعلى خطٍّ مستقيم ١٨٠°، وزوايا المثلث ١٨٠°.')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('كتاب الطالب ص ٩٤')}</div><h2>لماذا زوايا المثلث ١٨٠°؟</h2>
<div class="row vrow">{st(FIG('5-2_tri', 'fig'))}{STEPS(STP('١) نقصّ رؤوس المثلث الثلاثة', ''), STP('٢) نضعها متجاورة', ''), STP('٣) تكوّن خطاً مستقيماً', M('١٨٠°', cls='sm'), 'fin'))}</div>''' + tn('الكتاب ص٨٩: الشكل الذي يوضّح أن زوايا المثلث تكوّن معاً زاويةً مستقيمة. يمكن تنفيذه بورقةٍ وتمزيق الرؤوس أمام الطلاب.')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('تمرين ١ (أ)')}</div><h2>زاويتان على خطٍّ مستقيم</h2>
<div class="row vrow">{st(FIG('5-2_e1a', 'fig'))}{STEPS(STP('١) على خطٍّ مستقيم', M('١٨٠°', cls='sm')), STP('٢) نطرح المعلومة', M('١٨٠', MI, '١١٦', cls='sm')), STP('٣) أ', M('٦٤°', cls='sm'), 'fin'))}</div>'''))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('تمرين ١ (هـ)')}</div><h2>ثلاث زوايا حول نقطة</h2>
<div class="row vrow">{st(FIG('5-2_e1e', 'fig'))}{STEPS(STP('١) حول نقطة', M('٣٦٠°', cls='sm')), STP('٢) نجمع المعلومتين', M('١٣٠', PL, '١٢٠', EQ, '٢٥٠', cls='sm')), STP('٣) أ', M('٣٦٠', MI, '٢٥٠', EQ, '١١٠°', cls='sm'), 'fin'))}</div>'''))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('تمرين ٣ (أ)')}</div><h2>الزاوية الثالثة في المثلث</h2>
<div class="row vrow">{st(FIG('5-2_e3a', 'fig'))}{STEPS(STP('١) زوايا المثلث', M('١٨٠°', cls='sm')), STP('٢) نجمع المعلومتين', M('٥٧', PL, '٤٩', EQ, '١٠٦', cls='sm')), STP('٣) (أ ب ج)', M('١٨٠', MI, '١٠٦', EQ, '٧٤°', cls='sm'), 'fin'))}</div>'''))
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('تمرين ١')}</div><h2>معاً: أوجد الزاوية المجهولة</h2>
<div class="row">{''.join(st(f'<button class="flip box col" style="flex:1">{FIG(f, "fig sm")}<span class="tap">👆</span><span class="hid col"><span class="kk c-we">{a_}</span><span class="why">{w}</span></span></button>') for f, a_, w in (('5-2_e1b', '١٢٥°', '١٨٠ − ٥٥'), ('5-2_e1c', '٩٦°', '١٨٠ − ٢٤ − ٦٠'), ('5-2_e1f', '١٦٨°', '٣٦٠ − ٣٧ − ١٥٥')))}</div>''' + tn('اسأل أولاً: على خطٍّ مستقيم أم حول نقطة؟')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ١ (د)')}{timer(2)}</div>''' + quiz('أوجد ء ' + FIG('5-2_e1d', 'fig sm'), [M('٥٦°'), M('١٤٦°'), M('٣٤°')], 0, 'على خطٍّ مستقيم: ١٨٠ − ٩٠ − ٣٤ = ٥٦°')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ٣ (ب)')}</div>''' + quiz('أوجد (أ ب ج) ' + FIG('5-2_e3b', 'fig sm'), [M('٦٢°'), M('١٥٢°'), M('٧٢°')], 0, '١٨٠ − ٩٠ − ٢٨ = ٦٢°')))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">انتبه ⚠️ خطأ شائع</span>{ref('دليل المعلم ص ٩٧')}</div><h2>أيّ حقيقةٍ نستخدم؟</h2>
<div class="errs">{''.join(st(f'<button class="flip err"><span class="xq">{q}</span><span class="tap">👆</span><span class="hid xa no">{w}</span></button>') for q, w in (
  ('زاويتان على خطٍّ مستقيم: ٣٦٠ − ١١٦ = ٢٤٤°', '✘ على خطٍّ مستقيم المجموع ١٨٠°: ١٨٠ − ١١٦ = ٦٤°'),
  ('زوايا حول نقطة: ١٨٠ − ١٣٠ − ١٢٠', '✘ حول نقطة المجموع ٣٦٠°: ٣٦٠ − ٢٥٠ = ١١٠°')))}</div>''' + tn('الدليل: قد يخلط الطلاب في تطبيق الحقائق الخاصة بالزوايا عند حلّهم للتمارين.')))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج 🎫</span><h2>الحصة الأولى</h2>
<div class="exit">{st('<div><b>١</b>زاويتان على خطٍّ مستقيم: ٧٠° و س. ما س؟</div>')}{st('<div><b>٢</b>زاويتان في مثلث: ٥٠° و ٦٠°. ما الثالثة؟</div>')}</div>
<button class="flip box col" style="min-width:36vw"><span class="tap">👆 الإجابات</span><span class="hid col"><span class="kk">١) ١٨٠ − ٧٠ = ١١٠°</span><span class="kk">٢) ١٨٠ − ١١٠ = ٧٠°</span></span></button>''' + tn('من إعدادي (غير موجودة في الكتابين).')))

# ═══════════ الحصة الثانية ═══════════
S.append(slide('''<span class="tag">الحصة الثانية · ٤٠ دقيقة</span><h2>رباعي الأضلاع</h2>
<div class="plan"><div><b>٤ د</b>تذكّر</div><div><b>٨ د</b>زوايا الرباعي ٣٦٠°</div><div><b>٨ د</b>مثال ٥-٢</div>
<div><b>٦ د</b>زوايا متساوية</div><div><b>٨ د</b>نحن ← أنتم</div><div><b>٣ د</b>انتبه</div><div><b>٣ د</b>بطاقة الخروج</div></div>''', 'divider'))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">تذكّر 🔁</span>{timer(1)}</div>''' + quiz('مجموع زوايا المثلث…', [M('٩٠°'), M('١٨٠°'), M('٣٦٠°')], 1, 'زوايا المثلث تكوّن خطاً مستقيماً')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('كتاب الطالب ص ٩٤')}</div><h2>زوايا رباعي الأضلاع = ٣٦٠°</h2>
<div class="row vrow">{st(FIG('5-2_quad', 'fig lg'))}{STEPS(STP('١) نقسمه بقطرٍ إلى مثلثين', ''), STP('٢) زوايا كل مثلث', M('١٨٠°', cls='sm')), STP('٣) المجموع', M('٢', X, '١٨٠', EQ, '٣٦٠°', cls='sm'), 'fin'))}</div>''' + tn('الدليل: استنتج مع الطلاب أن المجموع ٣٦٠° برسم رباعي وتقسيمه إلى مثلثين، واطلب منهم رسم رباعياتٍ مختلفة بعضها بزاويةٍ منعكسة.')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('مثال ٥-٢')}</div><h2>ثلاث زوايا متساوية، كلٌّ منها ٨٥°</h2>
{box(STEPS(STP('١) مجموع الثلاث', M('٣', X, '٨٥', EQ, '٢٥٥°', cls='sm')), STP('٢) زوايا الرباعي', M('٣٦٠°', cls='sm')), STP('٣) الرابعة', M('٣٦٠', MI, '٢٥٥', EQ, '١٠٥°', cls='sm'), 'fin')))}''' + tn('الكتاب ص٩٤: مجموع الزوايا الثلاث ٢٥٥°، ومجموع قياسات زوايا الشكل الرباعي ٣٦٠°.')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('تمرين ٢ (ب)')}</div><h2>زوايا متساوية حول نقطة</h2>
<div class="row vrow">{st(FIG('5-2_e2b', 'fig'))}{STEPS(STP('١) حول نقطة', M('٣٦٠°', cls='sm')), STP('٢) عدد الزوايا', M('٥', cls='sm')), STP('٣) كل زاوية', M('٣٦٠', DV, '٥', EQ, '٧٢°', cls='sm'), 'fin'))}</div>'''))
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('تمرين ٦')}</div><h2>معاً: الزاوية المجهولة في الرباعي</h2>
<div class="row">{''.join(st(f'<button class="flip box col" style="flex:1">{FIG(f, "fig sm")}<span class="tap">👆</span><span class="hid col"><span class="kk c-we">{a_}</span><span class="why">{w}</span></span></button>') for f, a_, w in (('5-2_e6a', '٩٢°', '٣٦٠ − ٦٣ − ٩٥ − ١١٠'), ('5-2_e6c', '٥٣°', '٣٦٠ − ١٠٠ − ١٧٢ − ٣٥')))}</div>'''))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ٥')}{timer(2)}</div>''' + quiz('ثلاث زوايا في رباعي: ٦٠° و ٨٠° و ١١٠°. الرابعة؟', [M('١١٠°'), M('٧٠°'), M('١٣٠°')], 0, '٣٦٠ − ٢٥٠ = ١١٠°')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ٨')}</div>''' + quiz('قاست نور ثلاث زوايا في رباعي: ١٢٥° و ١٦٠° و ٩٠°. هل يمكن ذلك؟', ['✔ نعم', '✘ لا'], 1, 'مجموعها ٣٧٥° وهو أكبر من ٣٦٠°')))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">النشاط 🎲</span>{ref('دليل المعلم ص ٩٧')}</div><h2>الخماسي المنتظم في دائرة</h2>
<div class="exit">{st('<div><b>١</b>خمس نقاطٍ متساوية البعد على الدائرة: الزاوية عند المركز ٧٢°</div>')}{st('<div><b>٢</b>نصل كل نقطةٍ بباقي النقاط</div>')}{st('<div><b>٣</b>نحسب الزوايا بالحقائق: مجموع زوايا الخماسي ٥٤٠°</div>')}</div>''' + tn('النشاط في الدليل ص٩٧–٩٨: ٣٦٠ ÷ ٥ = ٧٢°؛ ومجموع زوايا الخماسي ٥ × ١٠٨ = ٥٤٠° أو ٣ × ١٨٠ (ثلاثة مثلثات).')))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">انتبه ⚠️</span>{ref('تمرين ٧')}</div><h2>زواياه الأربع متساوية</h2>
<div class="errs">{st('<button class="flip err"><span class="xq">«إذن هو مربّع»</span><span class="tap">👆</span><span class="hid xa no">✘ قد يكون مستطيلاً أو مربعاً<br>الزوايا وحدها لا تحدّد أطوال الأضلاع</span></button>')}</div>''' + tn('تعليق الدليل على التمرين ٧: يظن الطلاب أن الشكل مربع، ووجّههم إلى أنه لا يمكن تحديد نوعه من الزوايا فقط دون معرفة أطوال الأضلاع.')))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج 🎫</span><h2>الحصة الثانية</h2>
<div class="exit">{st('<div><b>١</b>رباعي فيه ثلاث زوايا قائمة. ما الرابعة؟</div>')}{st('<div><b>٢</b>أربع زوايا متساوية حول نقطة. كم كلٌّ منها؟</div>')}</div>
<button class="flip box col" style="min-width:36vw"><span class="tap">👆 الإجابات</span><span class="hid col"><span class="kk">١) ٣٦٠ − ٢٧٠ = ٩٠°</span><span class="kk">٢) ٣٦٠ ÷ ٤ = ٩٠°</span></span></button>''' + tn('من إعدادي (غير موجودة في الكتابين).')))
S.append(slide('''<span class="qbadge" style="background:#0A6770;box-shadow:0 4px 0 #05393E">الواجب المنزلي 🏠</span><h2>كتاب النشاط</h2>
<div class="exit"><div class="st"><div><b>١</b>الصفحات ٦٥ إلى ٦٧ في كتاب النشاط</div></div></div>'''))
S.append(slide(f'''<h2>الخلاصة</h2>
<div class="sumg">
{st(box('<div class="col"><b class="kk c-b">١٨٠°</b><span>على خطٍّ مستقيم<br>وزوايا المثلث</span></div>'))}
{st(box('<div class="col"><b class="kk c-we">٣٦٠°</b><span>حول نقطة<br>وزوايا رباعي الأضلاع</span></div>'))}
{st(box('<div class="col"><b class="kk c-exp">الخطوات</b><span>نجمع المعلوم<br>ثم نطرحه من المجموع</span></div>'))}</div>'''))

# ═══════════ ملحق: تمارين كتاب الطالب ص٩٤–٩٥ (الإجابات من دليل المعلم ص١٠٢) ═══════════
S.append(launch('sb', '٩٤ و ٩٥', note=f'المراجع: كتاب الطالب ص٩٤ و ٩٥، ودليل المعلم ص٩٧ و ٩٨ وإجاباته ص١٠٢ · {ME}'))
H = ['أ', 'ب', 'ج', 'د', 'هـ', 'و', 'ز', 'ح']
R1 = 'على خطٍّ مستقيم ١٨٠° · حول نقطة ٣٦٠°'
ANS1 = [('٦٤°', '١٨٠ − ١١٦'), ('١٢٥°', '١٨٠ − ٥٥'), ('٩٦°', '١٨٠ − ٢٤ − ٦٠'), ('٥٦°', '١٨٠ − ٩٠ − ٣٤'), ('١١٠°', '٣٦٠ − ١٣٠ − ١٢٠'), ('١٦٨°', '٣٦٠ − ٣٧ − ١٥٥'), ('٢٠٤°', '٣٦٠ − ٥٢ − ٦٨ − ٣٦'), ('٢٢٨°', '٣٦٠ − ٩٠ − ٤٢')]
S.append(ex(1, 'احسب الزوايا المشار إليها بالرموز', R1, [(f'({h}) ' + FIG(f'5-2_e1{c}'), f'{a_}<small>{w}</small>') for h, c, (a_, w) in zip(H, 'abcdefgh', ANS1)], cols=3, per=3))
S.append(ex(2, 'الزوايا متساوية في القياس', 'حول نقطة ٣٦٠°، نقسم على عدد الزوايا', [('(أ) ' + FIG('5-2_e2a'), '١٢٠°<small>٣٦٠ ÷ ٣</small>'), ('(ب) ' + FIG('5-2_e2b'), '٧٢°<small>٣٦٠ ÷ ٥</small>')], cols=2))
S.append(ex(3, 'احسب (أ ب ج) في كل مثلث', 'مجموع زوايا المثلث ١٨٠°', [('(أ) ' + FIG('5-2_e3a'), '٧٤°<small>١٨٠ − ٥٧ − ٤٩</small>'), ('(ب) ' + FIG('5-2_e3b'), '٦٢°<small>١٨٠ − ٩٠ − ٢٨</small>'), ('(ج) ' + FIG('5-2_e3c'), '١١٧°<small>١٨٠ − ٢٥ − ٣٨</small>')], cols=3, per=3))
S.append(ex(4, 'احسب (ب ج ء)', 'نوجد زاوية المثلث أولاً، ثم نستخدم الخط المستقيم', [('(أ) ' + FIG('5-2_e4a'), '١١٥°<small>زاوية المثلث ٦٥°، و ١٨٠ − ٦٥</small>'), ('(ب) ' + FIG('5-2_e4b'), '١٥٥°<small>زاوية المثلث ٢٥°، و ١٨٠ − ٢٥</small>'), ('(ج) ' + FIG('5-2_e4c'), '٦١°<small>زاوية ب في المثلث ٤٨°، و ١٨٠ − ٤٨ − ٧١</small>')], cols=3, per=3, note='تذكير الدليل: نبدأ بتحديد الزوايا التي يمكن معرفتها مباشرة، ثم نصل إلى المطلوبة.'))
S.append(ex(5, 'الزاوية الرابعة في الرباعي', 'مجموع زوايا رباعي الأضلاع ٣٦٠°', [('٦٠° و ٨٠° و ١١٠°', '١١٠°<small>٣٦٠ − ٢٥٠</small>')], cols=1))
S.append(ex(6, 'احسب الزوايا المحدّدة بالرموز', 'مجموع زوايا رباعي الأضلاع ٣٦٠°', [('(أ) ' + FIG('5-2_e6a'), '٩٢°<small>٣٦٠ − ٦٣ − ٩٥ − ١١٠</small>'), ('(ب) ' + FIG('5-2_e6b'), '٢٢٣°<small>٣٦٠ − ٤٠ − ٣٥ − ٦٢</small>'), ('(ج) ' + FIG('5-2_e6c'), '٥٣°<small>٣٦٠ − ١٠٠ − ١٧٢ − ٣٥</small>')], cols=3, per=3))
S.append(ex(7, 'زوايا الرباعي متساوية', 'كل زاوية ٣٦٠ ÷ ٤ = ٩٠°', [('ماذا تقول عنه؟', 'مستطيل أو مربع<small>لا نحدّد بالزوايا وحدها</small>')], cols=1))
S.append(ex(8, 'قياسات نور', 'مجموع زوايا الرباعي ٣٦٠°', [('١٢٥° و ١٦٠° و ٩٠°: هل هي صحيحة؟', 'لا<small>مجموعها ٣٧٥° أكبر من ٣٦٠°</small>')], cols=1))
S.append(ex(9, 'زاويةٌ ١٥٠° والثلاث الأخرى متساوية', 'نطرح ثم نقسم على ٣', [('قياس كل زاويةٍ منها', '٧٠°<small>(٣٦٠ − ١٥٠) ÷ ٣ = ٢١٠ ÷ ٣</small>')], cols=1))

# ═══════════ ملحق: حلول كتاب النشاط ص٦٥–٦٧ (الإجابات من دليل المعلم ص١٠٥) ═══════════
S.append(launch('ab', '٦٥ إلى ٦٧', note='الإجابات النهائية من دليل المعلم ص ١٠٥'))
NA, NB, NC = 'نشاط ص ٦٥ · تمرين', 'نشاط ص ٦٦ · تمرين', 'نشاط ص ٦٧ · تمرين'
S.append(ex(1, 'أوجد قيمة الزاوية المحدّدة برمز', 'على خطٍّ مستقيم ١٨٠°', [('(أ) ' + FIG('5-2_a1a'), '١٢٨°<small>١٨٠ − ٥٢</small>'), ('(ب) ' + FIG('5-2_a1b'), '١٠١°<small>١٨٠ − ١٧ − ٦٢</small>'), ('(ج) ' + FIG('5-2_a1c'), '٨٣°<small>١٨٠ − ٢٥ − ٧٢</small>')], cols=3, per=3, src=NA))
S.append(ex(2, 'احسب الزوايا المحدّدة بالرموز', 'حول نقطة ٣٦٠°', [('(أ) ' + FIG('5-2_a2a'), '١١٤°<small>٣٦٠ − ١٤٥ − ١٠١</small>'), ('(ب) ' + FIG('5-2_a2b'), '٢٤٠°<small>٣٦٠ − ٨٨ − ٣٢</small>'), ('(ج) ' + FIG('5-2_a2c'), '٦١°<small>٣٦٠ − ٩٠ − ١٥٣ − ٥٦</small>')], cols=3, per=3, src=NA))
S.append(ex(3, 'الزاوية الثالثة في المثلث', 'مجموع زوايا المثلث ١٨٠°', [(f'({h}) {q}', a_) for h, (q, a_) in zip(H, [('٤٢° و ٧٨°', '٦٠°'), ('٣٧° و ١٥°', '١٢٨°'), ('٧٥° و ٧٥°', '٣٠°'), ('١٥٣° و ١٤°', '١٣°')])], cols=2, src=NA))
S.append(ex(4, 'احسب الزاوية المحدّدة برمز', 'نبدأ بالزوايا التي نعرفها مباشرة', [('(أ) ' + FIG('5-2_a4a'), '٩٧°<small>زاوية المثلث ٨٣°، و ١٨٠ − ٨٣</small>'), ('(ب) ' + FIG('5-2_a4b'), '١٩°<small>١٨٠ − ٣٨ − (١٨٠ − ٥٧)</small>'), ('(ج) ' + FIG('5-2_a4c'), 'ع = ٥٤° ، ء = ٤١°<small>١٨٠ − ٤٦ − ٨٠ ، و ١٨٠ − ٣٩ − ١٠٠</small>')], cols=3, per=3, src=NB))
S.append(ex(5, 'زوايا المثلث أعدادٌ كاملة مختلفة', 'أصغر زاويتين ممكنتين ١° و ٢°', [('أكبر قياسٍ ممكن لأكبر زاوية', '١٧٧°<small>١٨٠ − ١ − ٢</small>')], cols=1, src=NB))
S.append(ex(6, 'الزاوية الرابعة في الرباعي', 'مجموع زوايا رباعي الأضلاع ٣٦٠°', [(f'({h}) {q}', a_) for h, (q, a_) in zip(H, [('٦٥° و ٧٥° و ٨٥°', '١٣٥°'), ('١٣٥° و ٩٨° و ٧١°', '٥٦°'), ('٨٤° و ٨٤° و ١١١°', '٨١°')])], cols=1, per=3, src=NB))
S.append(ex(7, 'مجموع ثلاث زوايا في رباعي ١٠٥°', 'مجموع زوايا رباعي الأضلاع ٣٦٠°', [('الزاوية الرابعة', '٢٥٥°<small>٣٦٠ − ١٠٥</small>')], cols=1, src=NB))
S.append(ex(8, 'احسب الزوايا المحدّدة بالرموز', 'زوايا الرباعي ٣٦٠°، وعلى خطٍّ مستقيم ١٨٠°', [(FIG('5-2_a8a'), 'أ = ١٠٥°<small>الرابعة ٣٦٠ − ٢٨٥ = ٧٥°، و ١٨٠ − ٧٥</small>'), (FIG('5-2_a8b'), 'ب = ١٠٨°<small>الداخلية ١٨٠ − ٦٥ = ١١٥°، و ٣٦٠ − ١١٥ − ٨٣ − ٥٤</small>')], cols=2, src=NC))
S.append(ex(9, 'قصّ ماجد زاويةً من مثلثٍ متطابق الأضلاع', 'زوايا المثلث متطابق الأضلاع ٦٠°، والباقي رباعي', [(FIG('5-2_a9', 'fig side') + 'ماذا تقول عن أ و ب؟', 'مجموعهما ٢٤٠°<small>٣٦٠ − ٦٠ − ٦٠</small>')], cols=1, src=NC))
S.append(ex(10, 'من الشكل المجاور', 'زوايا الرباعي ٣٦٠° والمثلث ١٨٠° والخط ١٨٠°', [(FIG('5-2_a10', 'fig side') + '(أ) (ب ء هـ)', '١٣٢°<small>٣٦٠ − ٧٢ − ٨٠ − ٧٦</small>'), ('(ب) (ج ب ء)', '١٠٠°<small>١٨٠ − ٨٠</small>'), ('(ج) (أ ج هـ)', '٣٢°<small>١٨٠ − ٧٢ − ٧٦</small>')], cols=1, src=NC))

PG = {'تمرين': [(1, '٩٤'), (2, '٩٥')]}

EXTRA_CSS_OWN = FIG_CSS + '''
.stps{display:flex;flex-direction:column;gap:1.2vh;align-items:stretch}
.stp{display:flex;align-items:center;gap:1.4vw;justify-content:space-between}
.stp .lab{flex:0 1 auto;max-width:60%;font-family:var(--fh);font-weight:800;color:#2563EB;background:#EAF1FF;border-radius:12px;padding:.2em .8em;text-align:center;line-height:1.4;font-size:clamp(20px,3.6vh,42px)}
.stp.fin .lab{background:var(--good);color:#fff}
.slide .vrow{align-items:center;justify-content:center;gap:2vh 3vw;flex-wrap:wrap}
.voc3{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1.6vw;width:min(1500px,94vw)}.voc3.c1{grid-template-columns:minmax(0,1fr);width:min(900px,80vw)}
.voc3 .st>div{display:flex;flex-direction:column;align-items:center;gap:.6vh;background:#fff;border:3px solid var(--line);border-radius:18px;padding:1.6vh 1vw;text-align:center}
.voc3 b{font-family:var(--fh);font-size:clamp(34px,6.4vh,76px);color:var(--base)}.voc3 i{font-style:normal;font-weight:700;color:var(--ink2);font-size:clamp(20px,3.4vh,38px)}
.voc3 span{font-weight:700;font-size:clamp(22px,3.8vh,44px);line-height:1.5}
.facts{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1.6vw;width:min(1400px,92vw)}
.fact{display:flex;flex-direction:column;align-items:center;gap:.6vh;background:#fff;border:3px solid var(--base);border-radius:18px;padding:2vh 1vw;text-align:center}
.fact b{font-family:var(--fh);font-size:clamp(44px,9vh,100px);color:var(--base)}.fact span{font-weight:800;font-size:clamp(24px,4.4vh,50px)}.fact i{font-style:normal;font-weight:700;color:var(--ink2);font-size:clamp(20px,3.4vh,38px)}
.slide .vrow .fig{height:min(56vh,520px);width:auto;max-width:56vw;max-height:none}
.slide .vrow .fig.lg{max-width:62vw}
.why{font-weight:700;color:var(--ink2);font-size:clamp(20px,3.4vh,40px)}
.errs{display:flex;flex-direction:column;gap:1.4vh;width:min(1300px,90vw)}
.errs .err{display:flex;flex-direction:column;align-items:center;gap:.6vh;background:#fff;border:3px solid var(--line);border-radius:16px;padding:.8vh 1.6vw;font-size:clamp(24px,4.6vh,54px);font-weight:700}
.errs .err .xa{font-size:clamp(20px,3.8vh,44px)}
.sumg{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:2vw;width:min(1600px,94vw)}
.sumg .col span{font-weight:700;font-size:clamp(20px,3.6vh,42px);line-height:1.5}
.sumg .kk{font-size:clamp(30px,5.6vh,66px)}
.hid.col .kk{font-size:clamp(28px,5.2vh,60px)}
.box .fig.sm{height:36vh;width:auto;max-width:40vw}
.q .fig{height:26vh;width:auto;vertical-align:middle}
.xq .fig{height:30vh;max-width:95%}
.xa small{display:block}
@media (max-aspect-ratio:1/1){.facts,.sumg{grid-template-columns:1fr}}
'''
