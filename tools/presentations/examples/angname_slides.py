# شرائح درس ٥-١ «تسمية الزوايا وتقديرها» — الصف السابع (حصتان، كتاب الطالب ص٩٠–٩٣)
# المراجع: دليل المعلم ص٩٤–٩٦ (المفردات؛ نقاط التعلّم: أنواع الزوايا، الدورة الكاملة ٣٦٠°، التسمية بثلاثة أحرف، التقدير لأقرب ١٠° ونصف القائمة ٤٥°؛
# الأخطاء الشائعة: ترتيب الحروف، وقراءة المنقلة خطأً ← التقدير أولاً؛ النشاط ٢: تكوين الزوايا بالأقلام؛ تعليقات التمارين ٥ و٦ و٨؛ الواجب: النشاط ص٦٣–٦٤)،
# كتاب الطالب ص٩٠–٩٣ (مثال ٥-١)، وإجابات الدليل ص١٠٢ (كتاب الطالب) وص١٠٥ (كتاب النشاط).
# python3.12 gen_powers.py angname_slides.py تسمية_الزوايا_وتقديرها_عرض_تفاعلي.html "تسمية الزوايا وتقديرها — الصف السابع"
exec(open(os.path.join(HERE, 'figs.py'), encoding='utf-8').read())

def STP(lab, expr='', cls=''): return st(f'<div class="stp {cls}"><span class="lab">{lab}</span>{expr}</div>')
def STEPS(*rows): return '<div class="stps">' + ''.join(rows) + '</div>'
def VC(items, cls=''): return f'<div class="voc3 {cls}">' + ''.join(st(f'<div><b>{w}</b><i>{e}</i><span>{d}</span></div>') for w, e, d in items) + '</div>'
def AT(svg, cap): return st(f'<div class="atile">{svg}<b>{cap}</b></div>')
MI = '<span class="x">−</span>'
S = []
ME = 'إعداد: أ. عيسى الحارثي'
S.append(slide(f'''<span class="tag">الصف السابع · الدرس ٥-١</span>
<h1 class="h1s">تسمية الزوايا وتقديرها</h1>
<p class="lead">كتاب الطالب ص ٩٠ إلى ٩٣ · حصتان</p>
<p class="lead" style="font-size:clamp(26px,4.8vh,56px)">{ME}</p>''', 'cover'))
CAN = ['أميّز <b>أنواع الزوايا</b> من قياسها', 'أسمّي الزاوية <b>بثلاثة أحرف</b> والحرف الأوسط رأسها', '<b>أقدّر</b> قياس الزاوية لأقرب ١٠°']
S.append(slide(f'''<h2>في نهاية هذا الدرس…</h2>
<div class="can">{''.join(f'<div><span class="can-i">✔</span><span><b>أنا أستطيع</b> أن {t}</span></div>' for t in CAN)}</div>'''))
S.append(slide(f'''<h2>مفردات الدرس (١)</h2>
{VC([('الزاوية', 'angle', 'تتكوّن من ضلعين يلتقيان في نقطةٍ اسمها الرأس'), ('الدرجة', 'degree', 'وحدة قياس الزوايا، والدورة الكاملة ٣٦٠°'), ('القطعة المستقيمة', 'line segment', 'جزءٌ من خطٍّ مستقيم يصل بين نقطتين')])}''' + tn('المفردات من الدليل ص٩٤، والتعريفات بجملةٍ واحدة من الكتاب ص٨٩–٩٠.')))
S.append(slide(f'''<h2>مفردات الدرس (٢)</h2>
{VC([('الحادّة', 'acute angle', 'أصغر من ٩٠°'), ('القائمة', 'right angle', 'تساوي ٩٠°'), ('المنفرجة', 'obtuse angle', 'بين ٩٠° و ١٨٠°'), ('المنعكسة', 'reflex angle', 'بين ١٨٠° و ٣٦٠°')], 'c4')}'''))

# ═══════════ الحصة الأولى ═══════════
S.append(slide('''<span class="tag">الحصة الأولى · ٤٠ دقيقة</span><h2>أنواع الزوايا وتسميتها</h2>
<div class="plan"><div><b>٤ د</b>الدورة الكاملة</div><div><b>٨ د</b>أنواع الزوايا</div><div><b>٨ د</b>التسمية بثلاثة أحرف</div>
<div><b>٦ د</b>مثال ٥-١</div><div><b>٨ د</b>نحن ← أنتم</div><div><b>٣ د</b>انتبه</div><div><b>٣ د</b>بطاقة الخروج</div></div>''', 'divider'))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('كتاب الطالب ص ٨٩')}</div><h2>الدورة الكاملة = ٣٦٠°</h2>
<div class="row atiles">{AT(ANG(90, 0, size=260), 'ربع دورة')}{AT(ANG(180, 0, size=260), 'نصف دورة')}{AT(ANG(359.9, 0, label='٣٦٠°', size=260), 'دورة كاملة')}</div>''' + tn('الكتاب ص٨٩: قسّم البابليون الدورة الكاملة إلى ٣٦٠ جزءاً منذ ١٥٠٠ قبل الميلاد، وكل جزء درجة.')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('كتاب الطالب ص ٩٠')}</div><h2>أنواع الزوايا (١)</h2>
<div class="row atiles">{AT(ANG(40, 10, size=260), 'حادّة: أصغر من ٩٠°')}{AT(ANG(90, 15, size=260), 'قائمة: تساوي ٩٠°')}{AT(ANG(130, 15, size=260), 'منفرجة: بين ٩٠° و ١٨٠°')}</div>'''))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('كتاب الطالب ص ٩٠')}</div><h2>أنواع الزوايا (٢)</h2>
<div class="row atiles">{AT(ANG(180, 0, size=260), 'مستقيمة: تساوي ١٨٠°')}{AT(ANG(60, 20, reflex=True, size=260), 'منعكسة: بين ١٨٠° و ٣٦٠°')}</div>
{st('<div class="note">قوس الزاوية المنعكسة يدور من الخارج</div>')}''' + tn('الكتاب ص٩٠: الزاوية المنعكسة يزيد قياسها عن زاويتين قائمتين.')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('كتاب الطالب ص ٩٠')}</div><h2>نسمّي الزاوية بثلاثة أحرف</h2>
<div class="row vrow">{st(ANG(50, 15, names=('ب', 'أ', 'ج'), size=320))}{STEPS(STP('١) الرأس في الوسط', M('(ب أ ج)', cls='sm')), STP('٢) أو بالعكس', M('(ج أ ب)', cls='sm')), STP('٣) الأخرى منعكسة', '<span class="kk">(ب أ ج) المنعكسة</span>', 'fin'))}</div>''' + tn('الكتاب ص٩٠: القطعتان (أب) و(أج) تلتقيان في أ؛ والزاوية (ب أ ج) أو (ج أ ب). عند النقطة أ زاويتان: الحادّة، والمنعكسة التي تُسمّى (ب أ ج) المنعكسة.')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('مثال ٥-١')}</div><h2>(ج ء هـ) قائمة، فما قياسها المنعكسة؟</h2>
<div class="row vrow">{st(ANG(90, 180, names=('ج', 'ء', 'هـ'), reflex=False, size=300))}{STEPS(STP('١) الزاويتان حول ء', M('٣٦٠°', cls='sm')), STP('٢) نطرح القائمة', M('٣٦٠°', MI, '٩٠°', cls='sm')), STP('٣) المنعكسة', M('٢٧٠°', cls='sm'), 'fin'))}</div>''' + tn('الكتاب: مجموع قياسي (ج ء هـ) و(ج ء هـ) المنعكسة عند النقطة ء يساوي ٣٦٠°.')))
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('تمرين ٣')}</div><h2>معاً: ما نوع الزاوية؟</h2>
<div class="row">{''.join(st(f'<button class="flip box col" style="flex:1"><span class="kk">{q}</span><span class="tap">👆</span><span class="hid col"><span class="kk c-we">{a_}</span></span></button>') for q, a_ in (('١٢٠°', 'منفرجة'), ('٢٠٠°', 'منعكسة'), ('١٠°', 'حادّة')))}</div>''' + tn('اسأل: أصغر من ٩٠؟ بين ٩٠ و ١٨٠؟ أكبر من ١٨٠؟')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ٣ (د)')}{timer(1)}</div>''' + quiz('زاويةٌ قياسها ٣٠٠° هي…', ['حادّة', 'منفرجة', 'منعكسة', 'مستقيمة'], 2, '٣٠٠° بين ١٨٠° و ٣٦٠°')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ٢ (هـ)')}</div>''' + quiz('ما نوع هذه الزاوية؟ ' + FIG('5-1_e2e', 'fig sm'), ['منفرجة', 'منعكسة', 'حادّة'], 1, 'القوس من الخارج: أكبر من ١٨٠°')))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">انتبه ⚠️ خطأ شائع</span>{ref('دليل المعلم ص ٩٥')}</div><h2>الحرف الأوسط هو الرأس</h2>
<div class="row vrow">{st(ANG(50, 15, names=('ب', 'أ', 'ج'), size=300))}<div class="errs">{''.join(st(f'<button class="flip err"><span class="xq">{q}</span><span class="tap">👆</span><span class="hid xa {c}">{w}</span></button>') for q, w, c in (
  ('(أ ب ج)', '✘ رأسها ب، وهي زاويةٌ أخرى', 'no'), ('(ب أ ج)', '✔ رأسها أ', 'ok')))}</div></div>''' + tn('الدليل: قد يخطئ الطلاب في ترتيب الحروف، فنبّههم أن الحرف الأوسط يشير إلى رأس الزاوية.')))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج 🎫</span><h2>الحصة الأولى</h2>
<div class="exit">{st('<div><b>١</b>ما نوع زاويةٍ قياسها ٩٥°؟</div>')}{st('<div><b>٢</b>زاويةٌ قياسها ١٠٠°: ما قياس المنعكسة؟</div>')}</div>
<button class="flip box col" style="min-width:36vw"><span class="tap">👆 الإجابات</span><span class="hid col"><span class="kk">١) منفرجة</span><span class="kk">٢) ٣٦٠ − ١٠٠ = ٢٦٠°</span></span></button>''' + tn('من إعدادي (غير موجودة في الكتابين).')))

# ═══════════ الحصة الثانية ═══════════
S.append(slide('''<span class="tag">الحصة الثانية · ٤٠ دقيقة</span><h2>تقدير الزوايا</h2>
<div class="plan"><div><b>٤ د</b>تذكّر</div><div><b>٨ د</b>زوايا مرجعية</div><div><b>٨ د</b>نقدّر لأقرب ١٠°</div>
<div><b>٨ د</b>الزوايا حول نقطة</div><div><b>٦ د</b>النشاط</div><div><b>٣ د</b>انتبه</div><div><b>٣ د</b>بطاقة الخروج</div></div>''', 'divider'))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">تذكّر 🔁</span>{timer(1)}</div>''' + quiz('زاويةٌ قياسها ١٧٠° هي…', ['حادّة', 'منفرجة', 'منعكسة'], 1, 'بين ٩٠° و ١٨٠°')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('دليل المعلم ص ٩٤')}</div><h2>زوايا نقارن بها</h2>
<div class="row atiles">{AT(ANG(45, 20, size=230), 'نصف القائمة')}{AT(ANG(90, 20, size=230), 'قائمة')}{AT(ANG(180, 0, size=230), 'مستقيمة')}{AT(ANG(90, 20, reflex=True, label='٢٧٠°', size=230), 'ثلاث قوائم')}</div>''' + tn('الدليل: يحتاج الطلاب إلى تقدير الزوايا لأقرب ١٠°، ومعرفة أن نصف القائمة ٤٥° تساعدهم.')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('تمرين ٧')}</div><h2>كيف نقدّر الزاوية؟</h2>
<div class="row vrow">{st(ANG(130, 10, label='؟', size=300))}{STEPS(STP('١) أكبر من ٩٠°؟', '<span class="kk">نعم</span>'), STP('٢) أصغر من ١٨٠°؟', '<span class="kk">نعم</span>'), STP('٣) أقرب لمنتصفهما ١٣٥°', M('حوالي ١٣٠°', cls='sm'), 'fin'))}</div>''' + tn('التقدير قبل القياس يحمي من قراءة التدريج الخطأ في المنقلة (الدليل ص٩٥). الإجابة بالقياس: ١٣٠° (تمرين ٧ (ب)).')))
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('تمرين ٦')}</div><h2>معاً: كل زاويةٍ من مضاعفات ٣٠°</h2>
<div class="row">{''.join(st(f'<button class="flip box col" style="flex:1">{FIG(f, "fig sm")}<span class="tap">👆</span><span class="hid col"><span class="kk c-we">{a_}</span></span></button>') for f, a_ in (('5-1_e6a', '٦٠°'), ('5-1_e6b', '١٢٠°'), ('5-1_e6d', '٣٠°')))}</div>''' + tn('تعليق الدليل: يجب أن يدرك الطلاب مفهوم مضاعفات العدد؛ مضاعفات ٣٠: ٣٠، ٦٠، ٩٠، ١٢٠، …')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('تمرين ٨ (ج)')}</div><h2>الزوايا حول نقطة مجموعها ٣٦٠°</h2>
<div class="row vrow">{st(FIG('5-1_e8', 'fig'))}{STEPS(STP('١) نقيس س و ع', M('٨٠° ، ٤٥°', cls='sm')), STP('٢) نجمعهما', M('١٢٥°', cls='sm')), STP('٣) ص = ٣٦٠ − ١٢٥', M('٢٣٥°', cls='sm'), 'fin'))}</div>''' + tn('تعليق الدليل: يحتاج الطلاب إلى معرفة أن مجموع قياس الزوايا حول نقطة ٣٦٠°. إجابة الدليل: س = ٨٠°، ع = ٤٥°، ص = ٢٣٥°.')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ٥ (ب)')}{timer(2)}</div>''' + quiz('كل زاويةٍ في المثلثات ٦٠°. ما قياس (أ م ج)؟ ' + FIG('5-1_hex', 'fig sm'), [M('٦٠°'), M('١٢٠°'), M('١٨٠°')], 1, 'زاويتان من ٦٠°: ٢ × ٦٠ = ١٢٠°')))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">النشاط 🎲</span>{ref('دليل المعلم ص ٩٦')}</div><h2>كوّن الزاوية بقلمين</h2>
<div class="exit">{st('<div><b>١</b>زاويةٌ حادّة</div>')}{st('<div><b>٢</b>زاويةٌ قائمة</div>')}{st('<div><b>٣</b>زاويةٌ منفرجة</div>')}</div>''' + tn('النشاط ٢ في الدليل: يربط كل طالب نهايتي قلمين ليكوّن الزاوية المطلوبة، ثم يذكر الطلاب أمثلةً لأنواع الزوايا من الصف حولهم.')))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">انتبه ⚠️ خطأ شائع</span>{ref('دليل المعلم ص ٩٥')}</div><h2>قدّر قبل أن تقيس</h2>
<div class="errs">{st('<button class="flip err"><span class="xq">زاويةٌ حادّة قيست ١٥٠°</span><span class="tap">👆</span><span class="hid xa no">✘ قُرئ التدريج الآخر؛ الحادّة أصغر من ٩٠°، فهي ٣٠°</span></button>')}</div>''' + tn('الدليل: عند استخدام المنقلة قد يقرأ الطالب القياس بطريقةٍ خاطئة، ولتجنّب ذلك وجّههم إلى تقدير الزاوية أولاً.')))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج 🎫</span><h2>الحصة الثانية</h2>
<div class="exit">{st('<div><b>١</b>قدّر: زاويةٌ أكبر قليلاً من القائمة</div>')}{st('<div><b>٢</b>زاويتان حول نقطة: ١٥٠° و س. ما س؟</div>')}</div>
<button class="flip box col" style="min-width:36vw"><span class="tap">👆 الإجابات</span><span class="hid col"><span class="kk">١) حوالي ١٠٠°</span><span class="kk">٢) ٣٦٠ − ١٥٠ = ٢١٠°</span></span></button>''' + tn('من إعدادي (غير موجودة في الكتابين).')))
S.append(slide('''<span class="qbadge" style="background:#0A6770;box-shadow:0 4px 0 #05393E">الواجب المنزلي 🏠</span><h2>كتاب النشاط</h2>
<div class="exit"><div class="st"><div><b>١</b>الصفحتان ٦٣ و ٦٤ في كتاب النشاط</div></div></div>'''))
S.append(slide(f'''<h2>الخلاصة</h2>
<div class="sumg">
{st(box('<div class="col"><b class="kk c-b">الأنواع</b><span>حادّة &lt; ٩٠° · قائمة ٩٠°<br>منفرجة حتى ١٨٠° · منعكسة بعدها</span></div>'))}
{st(box('<div class="col"><b class="kk c-we">التسمية</b><span>ثلاثة أحرف<br>والأوسط هو الرأس</span></div>'))}
{st(box('<div class="col"><b class="kk c-exp">التقدير</b><span>نقارن بـ ٩٠° و ١٨٠°<br>وحول نقطة ٣٦٠°</span></div>'))}</div>'''))

# ═══════════ ملحق: تمارين كتاب الطالب ص٩١–٩٣ (الإجابات من دليل المعلم ص١٠٢) ═══════════
S.append(launch('sb', '٩١ إلى ٩٣', note=f'المراجع: كتاب الطالب ص٩٠ إلى ٩٣، ودليل المعلم ص٩٤ إلى ٩٦ وإجاباته ص١٠٢ · {ME}'))
H = ['أ', 'ب', 'ج', 'د', 'هـ', 'و', 'ز', 'ح']
RT = 'حادّة &lt; ٩٠° · قائمة = ٩٠° · منفرجة بين ٩٠° و ١٨٠° · منعكسة بين ١٨٠° و ٣٦٠°'
S.append(ex(1, 'المثلث أ ب ج', 'الحرف الأوسط في اسم الزاوية هو رأسها', [(FIG('5-1_tri', 'fig side') + '(أ) حدّد (ج أ ب)', 'الزاوية عند الرأس أ'), ('(ب) سمِّ باقي زوايا المثلث', '(أ ب ج) و (أ ج ب)')], cols=1))
S.append(ex(2, 'حدّد نوع الزاوية', RT, [(f'({h}) ' + FIG(f'5-1_e2{c}'), a_) for h, c, a_ in zip(H, 'abcdef', ['حادّة', 'منعكسة', 'قائمة', 'منفرجة', 'منعكسة', 'منعكسة'])], cols=3, per=3))
S.append(ex(3, 'حدّد نوع الزاوية', RT, [(f'({h}) {q}', a_) for h, (q, a_) in zip(H, [('١٢٠°', 'منفرجة'), ('٦٠°', 'حادّة'), ('٢٠٠°', 'منعكسة'), ('٣٠٠°', 'منعكسة'), ('١٠°', 'حادّة'), ('١٧٠°', 'منفرجة')])], cols=2))
S.append(ex(4, '(أ ب ج) قائمة، و (أ ب ء) = (ء ب ج)', 'القائمة ٩٠°، والمنعكسة = ٣٦٠° − الزاوية', [(FIG('5-1_e4', 'fig side') + '(أ) (أ ب ء)', '٩٠ ÷ ٢ = ٤٥°'), ('(ب) (أ ب ج) المنعكسة', '٣٦٠ − ٩٠ = ٢٧٠°'), ('(ج) (أ ب ء) المنعكسة', '٣٦٠ − ٤٥ = ٣١٥°'), ('(د) (ج ب ء) المنعكسة', '٣٦٠ − ٤٥ = ٣١٥°')], cols=2))
S.append(ex(5, 'كل زاويةٍ في المثلثات ٦٠°', 'نعدّ الزوايا الصغيرة ونضرب في ٦٠، والمنعكسة = ٣٦٠ − الزاوية', [(FIG('5-1_hex', 'fig side') + '(أ) (أ ب ج)', '٢ × ٦٠ = ١٢٠°'), ('(ب) (أ م ج)', '٢ × ٦٠ = ١٢٠°'), ('(ج) (م هـ ء)', '٦٠°'), ('(د) (ب م ء) المنعكسة', '٣٦٠ − ١٢٠ = ٢٤٠°'), ('(هـ) (أ م و) المنعكسة', '٣٦٠ − ٦٠ = ٣٠٠°')], cols=2, note='تعليق الدليل: ذكّر الطلاب بأن السداسي المنتظم يتكوّن من ستّ مثلثاتٍ متطابقة الأضلاع.'))
S.append(ex(6, 'قياس كل زاويةٍ من مضاعفات ٣٠°', 'نقارن بالقائمة (٩٠°) والمستقيمة (١٨٠°)', [(f'({h}) ' + FIG(f'5-1_e6{c}'), a_) for h, c, a_ in zip(H, 'abcdef', ['٦٠°', '١٢٠°', '٢٧٠°', '٣٠°', '٢٤٠°', '٣٠٠°'])], cols=3, per=3))
S.append(ex(7, 'قدّر قياس كل زاوية ثم قِسها', 'نقدّر أولاً بالمقارنة بـ ٩٠° و ١٨٠°، ثم نقيس بالمنقلة', [(f'({h}) ' + FIG(f'5-1_e7{c}'), a_) for h, c, a_ in zip(H, 'abcdefgh', ['٥٥°', '١٣٠°', '٢٢٠°', '٣٢٥°', '١٦٥°', '٣٣°', '٢٩٢°', '٢٤٦°'])], cols=3, per=3, note='القياسات من إجابات الدليل؛ يقبل المعلّم التقديرات القريبة منها.'))
S.append(ex(8, 'الزوايا س و ص و ع', 'مجموع الزوايا حول نقطة ٣٦٠°', [(FIG('5-1_e8', 'fig side') + '(أ) و (ب) قدّر ثم قِس', 'س = ٨٠° ، ع = ٤٥° ، ص = ٢٣٥°'), ('(ج) لماذا مجموعها ٣٦٠°؟', 'لأنها زوايا تلتقي في نقطةٍ وتكوّن دورةً كاملة')], cols=1))

# ═══════════ ملحق: حلول كتاب النشاط ص٦٣–٦٤ (الإجابات من دليل المعلم ص١٠٥) ═══════════
S.append(launch('ab', '٦٣ و ٦٤', note='الإجابات النهائية من دليل المعلم ص ١٠٥'))
NA, NB = 'نشاط ص ٦٣ · تمرين', 'نشاط ص ٦٤ · تمرين'
S.append(ex(1, 'حادّة أم منفرجة أم منعكسة', RT, [(f'({h}) {q}', a_) for h, (q, a_) in zip(H, [('٢١٠°', 'منعكسة'), ('١٢٠°', 'منفرجة'), ('٣١°', 'حادّة'), ('٣٠١°', 'منعكسة'), ('١٠٣°', 'منفرجة')])], cols=2, src=NA))
S.append(ex(2, 'صحيحة أم خاطئة', RT, [(f'({h}) {q}', a_) for h, (q, a_) in zip(H, [
  ('أصغر من ٧٥° ← حادّة', 'صحيحة<small>الدليل: خاطئة</small>'), ('أكبر من ١٠٠° ← منفرجة', 'خاطئة<small>قد تكون منعكسة</small>'), ('أكبر من ٣٣٠° ← منفرجة', 'خاطئة<small>هي منعكسة</small>'),
  ('أصغر من ٣٣٠° ← منعكسة', 'خاطئة<small>قد تكون حادّة أو منفرجة</small>'), ('نصف المنعكسة ← منفرجة', 'صحيحة<small>نصف ما بين ١٨٠° و ٣٦٠° بين ٩٠° و ١٨٠°</small>')])], cols=2, src=NA,
  note='في إجابات الدليل ص١٠٥ (أ) «خاطئة»، لكن كل زاويةٍ أصغر من ٧٥° أصغر من ٩٠° فهي حادّة؛ والأرجح أن الصحيح «صحيحة». قرّر ما تعتمده مع طلابك.'))
S.append(ex(3, 'قدّر قياس كل زاوية', 'نقارن بـ ٩٠° و ١٨٠° و ٢٧٠°', [(f'({h}) ' + FIG(f'5-1_a3{c}'), a_) for h, c, a_ in zip(H, 'abcde', ['٨٠°', '١٥٠°', '٣٢٠°', '٢٦٠°', '٢٤٠°'])], cols=3, per=3, src=NA))
S.append(ex(4, 'من الشكل المجاور', 'المنعكسة = ٣٦٠° − الزاوية', [(FIG('5-1_a4', 'fig side') + '(أ) (أ ء ب)', '٤٥°'), ('(ب) (أ ء ب) المنعكسة', '٣٦٠ − ٤٥ = ٣١٥°'), ('(ج) (ب ء ج) المنعكسة', '٣٦٠ − ٩٠ = ٢٧٠°'), ('(د) (أ ء ج) المنعكسة', '٣٦٠ − ١٣٥ = ٢٢٥°')], cols=2, src=NB))
S.append(ex(5, 'من الشبه المنحرف أكمل', 'المنعكسة الأكبر من ثلاث قوائم أكبر من ٢٧٠°', [(FIG('5-1_a5', 'fig side') + '(أ) زاويةٌ منفرجة', '(ب أ ء) أو (أ ء ج)'), ('(ب) منعكسة أكبر من ٢٧٠°', '(أ ب ج) المنعكسة أو (ب ج ء) المنعكسة'), ('(ج) منعكسة أصغر من ٢٧٠°', '(ب أ ء) المنعكسة أو (أ ء ج) المنعكسة')], cols=1, src=NB))

PG = {'تمرين': [(1, '٩١'), (5, '٩٢'), (8, '٩٣')]}

EXTRA_CSS_OWN = FIG_CSS + '''
.stps{display:flex;flex-direction:column;gap:1.2vh;align-items:stretch}
.stp{display:flex;align-items:center;gap:1.4vw;justify-content:space-between}
.stp .lab{flex:0 1 auto;max-width:60%;font-family:var(--fh);font-weight:800;color:#2563EB;background:#EAF1FF;border-radius:12px;padding:.2em .8em;text-align:center;line-height:1.4;font-size:clamp(20px,3.6vh,42px)}
.stp.fin .lab{background:var(--good);color:#fff}
.slide .vrow{align-items:center;justify-content:center;gap:2vh 3vw;flex-wrap:wrap}
.voc3{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1.6vw;width:min(1500px,94vw)}.voc3.c4{grid-template-columns:repeat(4,minmax(0,1fr))}
.voc3 .st>div{display:flex;flex-direction:column;align-items:center;gap:.6vh;background:#fff;border:3px solid var(--line);border-radius:18px;padding:1.6vh 1vw;text-align:center}
.voc3 b{font-family:var(--fh);font-size:clamp(30px,5.8vh,70px);color:var(--base)}.voc3 i{font-style:normal;font-weight:700;color:var(--ink2);font-size:clamp(18px,3.2vh,36px)}
.voc3 span{font-weight:700;font-size:clamp(20px,3.6vh,42px);line-height:1.5}
.atiles{gap:2vw;justify-content:center;flex-wrap:nowrap}
.xq .fig{height:34vh;max-width:95%}
.atile{display:flex;flex-direction:column;align-items:center;gap:.6vh;background:#fff;border:3px solid var(--line);border-radius:18px;padding:1vh 1vw}
.atiles .svgfig.ang{max-width:25vw;height:min(50vh,480px)}
.atile b{font-family:var(--fh);font-size:clamp(20px,3.6vh,40px);color:var(--ink)}
.slide .svgfig.ang{width:auto;height:min(58vh,560px);max-width:46vw;max-height:none}
.slide .vrow .svgfig.ang{height:min(72vh,680px);max-width:62vw}
.why{font-weight:700;color:var(--ink2);font-size:clamp(22px,3.8vh,44px)}
.errs{display:flex;flex-direction:column;gap:1.4vh;width:min(1100px,80vw)}
.errs .err{display:flex;flex-direction:column;align-items:center;gap:.6vh;background:#fff;border:3px solid var(--line);border-radius:16px;padding:.8vh 1.6vw;font-size:clamp(26px,5vh,58px);font-weight:700}
.errs .err .xa{font-size:clamp(22px,4vh,46px)}
.xa.ok{color:var(--good)}
.sumg{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:2vw;width:min(1600px,94vw)}
.sumg .col span{font-weight:700;font-size:clamp(20px,3.6vh,42px);line-height:1.5}
.sumg .kk{font-size:clamp(30px,5.6vh,66px)}
.hid.col .kk{font-size:clamp(28px,5.2vh,60px)}
.box .fig.sm{height:40vh;width:auto;max-width:44vw}
.opt .fig,.q .fig{height:20vh;width:auto;vertical-align:middle}
.xa small{display:block}
@media (max-aspect-ratio:1/1){.atiles{flex-wrap:wrap}.voc3,.voc3.c4,.sumg{grid-template-columns:1fr 1fr}.slide .svgfig.ang{max-width:42vw}}
'''
