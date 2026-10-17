# شرائح درس ٥-٣ «حل مسائل الزوايا» — الصف السابع (حصتان، كتاب الطالب ص٩٦–٩٧)
# المراجع: دليل المعلم ص٩٩ (المفردات: الزوايا المتقابلة بالرأس، متعامد، متطابق الضلعين؛ نقاط التعلّم: إثبات تساوي المتقابلتين بالرأس؛
# الخطأ الشائع: لا يعرف الطلاب ماذا يكتبون عند التبرير، وتكفي عبارةٌ مثل «متقابلتان بالرأس»؛ تعليقات التمارين ٣ و٤ و٦؛ الواجب: النشاط ص٧٠–٧١)،
# كتاب الطالب ص٩٦–٩٧، وإجابات الدليل ص١٠٣ (كتاب الطالب) وص١٠٥ (كتاب النشاط ص٦٨–٦٩).
# python3.12 gen_powers.py angsolve_slides.py حل_مسائل_الزوايا_عرض_تفاعلي.html "حل مسائل الزوايا — الصف السابع"
exec(open(os.path.join(HERE, 'figs.py'), encoding='utf-8').read())

def STP(lab, expr='', cls=''): return st(f'<div class="stp {cls}"><span class="lab">{lab}</span>{expr}</div>')
def STEPS(*rows): return '<div class="stps">' + ''.join(rows) + '</div>'
def VC(items, cls=''): return f'<div class="voc3 {cls}">' + ''.join(st(f'<div><b>{w}</b><i>{e}</i><span>{d}</span></div>') for w, e, d in items) + '</div>'
MI = '<span class="x">−</span>'; PL = '<span class="x">+</span>'; DV = '<span class="x">÷</span>'
S = []
ME = 'إعداد: أ. عيسى الحارثي'
S.append(slide(f'''<span class="tag">الصف السابع · الدرس ٥-٣</span>
<h1 class="h1s">حل مسائل الزوايا</h1>
<p class="lead">كتاب الطالب ص ٩٦ و ٩٧ · حصتان</p>
<p class="lead" style="font-size:clamp(26px,4.8vh,56px)">{ME}</p>''', 'cover'))
CAN = ['أعرف أن <b>الزاويتين المتقابلتين بالرأس</b> متساويتان وأبرّر ذلك', 'أستخدم خواص <b>المثلث متطابق الضلعين</b>', 'أحلّ مسائل الزوايا <b>بخطواتٍ</b> وأذكر السبب بعبارةٍ قصيرة']
S.append(slide(f'''<h2>في نهاية هذا الدرس…</h2>
<div class="can">{''.join(f'<div><span class="can-i">✔</span><span><b>أنا أستطيع</b> أن {t}</span></div>' for t in CAN)}</div>'''))
S.append(slide(f'''<h2>مفردات الدرس</h2>
{VC([('متقابلتان بالرأس', 'vertically opposite angles', 'زاويتان متقابلتان عند تقاطع خطّين'), ('متعامدان', 'perpendicular', 'خطّان يتقاطعان بزاويةٍ قائمة ٩٠°'), ('متطابق الضلعين', 'isosceles', 'مثلثٌ فيه ضلعان متطابقان وزاويتان متساويتان')])}''' + tn('المفردات من الدليل ص٩٩، والتعريفات من الكتاب ص٩٦–٩٧.')))

# ═══════════ الحصة الأولى ═══════════
S.append(slide('''<span class="tag">الحصة الأولى · ٤٠ دقيقة</span><h2>الزوايا المتقابلة بالرأس</h2>
<div class="plan"><div><b>٤ د</b>تذكّر</div><div><b>٨ د</b>خطّان متقاطعان</div><div><b>٨ د</b>لماذا تتساويان؟</div>
<div><b>٦ د</b>الخطّان المتعامدان</div><div><b>٨ د</b>نحن ← أنتم</div><div><b>٣ د</b>انتبه</div><div><b>٣ د</b>بطاقة الخروج</div></div>''', 'divider'))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">تذكّر 🔁</span>{ref('الدرس ٥-٢')}{timer(1)}</div>''' + quiz('زاويتان على خطٍّ مستقيم: ١١٠° و س. ما س؟', [M('٧٠°'), M('٢٥٠°'), M('١١٠°')], 0, '١٨٠ − ١١٠ = ٧٠°')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('كتاب الطالب ص ٩٦')}</div><h2>خطّان مستقيمان متقاطعان</h2>
<div class="row vrow">{st(XL(70))}{STEPS(STP('أ و ج', '<span class="kk">متقابلتان بالرأس</span>'), STP('ب و ء', '<span class="kk">متقابلتان بالرأس</span>'), STP('كل متقابلتين', '<span class="kk">متساويتان</span>', 'fin'))}</div>''' + tn('الكتاب ص٩٦: (أ) و(ج) زاويتان متقابلتان بالرأس، و(ب) و(ء) أيضاً. واللون نفسه للزاويتين المتقابلتين.')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('كتاب الطالب ص ٩٦')}</div><h2>لماذا أ = ج؟</h2>
<div class="row vrow">{st(XL(70))}{STEPS(STP('١) أ + ء = ١٨٠°', '<span class="why">على خطٍّ مستقيم</span>'), STP('٢) ج + ء = ١٨٠°', '<span class="why">على خطٍّ مستقيم</span>'), STP('٣) أ = ١٨٠° − ء = ج', '<span class="kk">أ = ج</span>', 'fin'))}</div>''' + tn('الكتاب ص٩٦ وإجابة التمرين ١ في الدليل: البرهان نفسه يثبت أن ب = ء. ناقش الطلاب في كل خطوة (نقاط التعلّم في الدليل).')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('كتاب الطالب ص ٩٦')}</div><h2>حالةٌ خاصّة: خطّان متعامدان</h2>
<div class="row vrow">{st(XL(perp=True, labels=('', '', '', '')))}{STEPS(STP('يتقاطعان بزاويةٍ قائمة', M('٩٠°', cls='sm')), STP('الزوايا الأربع', M('٩٠°', cls='sm'), 'fin'))}</div>'''))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('تمرين ٢')}</div><h2>ثلاثة خطوطٍ متقاطعة</h2>
<div class="row vrow">{st(FIG('5-3_e2', 'fig'))}{STEPS(STP('١) أ على خطٍّ مستقيم', M('١٨٠', MI, '٦١', MI, '٤٦', EQ, '٧٣°', cls='sm')), STP('٢) ب تقابل ٦١° بالرأس', M('٦١°', cls='sm')), STP('٣) ج تقابل ٤٦° بالرأس', M('٤٦°', cls='sm')), STP('٤) ء تقابل أ بالرأس', M('٧٣°', cls='sm'), 'fin'))}</div>''' + tn('إجابة الدليل ص١٠٣: أ = ٧٣°، ب = ٦١°، ج = ٤٦°، ء = ٧٣°.')))
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('نحن')}</div><h2>معاً: أوجد الزوايا الثلاث</h2>
<div class="row vrow">{st(XL(110, labels=('١١٠°', 'ب', 'ج', 'ء')))}<div class="row">{''.join(st(f'<button class="flip box col">{q}<span class="tap">👆</span><span class="hid col"><span class="kk c-we">{a_}</span><span class="why">{w}</span></span></button>') for q, a_, w in (('<span class="kk">ج</span>', '١١٠°', 'متقابلة بالرأس'), ('<span class="kk">ب</span>', '٧٠°', 'على خطٍّ مستقيم'), ('<span class="kk">ء</span>', '٧٠°', 'تقابل ب بالرأس')))}</div></div>''' + tn('من إعدادي (غير موجودة في الكتابين).')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('النشاط تمرين ١')}{timer(2)}</div>''' + quiz('أوجد أ ' + FIG('5-3_a1', 'fig sm'), [M('٧٤°'), M('٦٤°'), M('٤٢°')], 0, 'على خطٍّ مستقيم: ١٨٠ − ٦٤ − ٤٢ = ٧٤°')))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">انتبه ⚠️</span>{ref('دليل المعلم ص ٩٩')}</div><h2>ماذا نكتب عند التبرير؟</h2>
<div class="errs">{''.join(st(f'<button class="flip err"><span class="xq">{q}</span><span class="tap">👆</span><span class="hid xa {c}">{w}</span></button>') for q, w, c in (
  ('ج = ٤٦° (بدون سبب)', '✘ نكتب السبب بعبارةٍ قصيرة', 'no'), ('ج = ٤٦° لأنهما متقابلتان بالرأس', '✔ تكفي هذه العبارة', 'ok')))}</div>''' + tn('الدليل: يحتاج الطلاب إلى أن يفهموا ماذا يجب أن يفعلوه عندما يُطلب إليهم تبرير إجابة؛ لا يتطلب هذا الكثير من الكتابة، فعبارةٌ مثل «زوايا متقابلة» كافية.')))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج 🎫</span><h2>الحصة الأولى</h2>
<div class="exit">{st('<div><b>١</b>خطّان متقاطعان، إحدى الزوايا ٤٠°. أوجد الثلاث الأخرى.</div>')}</div>
<button class="flip box col" style="min-width:36vw"><span class="tap">👆 الإجابة</span><span class="hid col"><span class="kk">٤٠° (متقابلة بالرأس)</span><span class="kk">١٤٠° و ١٤٠° (على خطٍّ مستقيم)</span></span></button>''' + tn('من إعدادي (غير موجودة في الكتابين).')))

# ═══════════ الحصة الثانية ═══════════
S.append(slide('''<span class="tag">الحصة الثانية · ٤٠ دقيقة</span><h2>المثلث متطابق الضلعين ومسائل أكثر</h2>
<div class="plan"><div><b>٤ د</b>تذكّر</div><div><b>٨ د</b>متطابق الضلعين</div><div><b>٨ د</b>نجمع أكثر من حقيقة</div>
<div><b>٦ د</b>زاويتان متساويتان</div><div><b>٨ د</b>نحن ← أنتم</div><div><b>٣ د</b>لماذا ١٨٠°؟</div><div><b>٣ د</b>بطاقة الخروج</div></div>''', 'divider'))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">تذكّر 🔁</span>{timer(1)}</div>''' + quiz('زاويتان متقابلتان بالرأس…', ['متساويتان', 'مجموعهما ١٨٠°', 'مجموعهما ٣٦٠°'], 0, 'الزاويتان المتقابلتان بالرأس متساويتان')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('تمرين ٤')}</div><h2>المثلث متطابق الضلعين: (ب أ ج) = ٤٠°</h2>
<div class="row vrow">{st(FIG('5-3_e4', 'fig'))}{STEPS(STP('١) زاويتا القاعدة متساويتان', '<span class="why">أب = أج</span>'), STP('٢) مجموعهما', M('١٨٠', MI, '٤٠', EQ, '١٤٠°', cls='sm')), STP('٣) كلٌّ منهما', M('١٤٠', DV, '٢', EQ, '٧٠°', cls='sm'), 'fin'))}</div>''' + tn('تعليق الدليل على التمرين ٤: ذكّر الطلاب أن زاويتي القاعدة للمثلث متطابق الضلعين متساويتان.')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('تمرين ٥')}</div><h2>نجمع حقيقتين</h2>
<div class="row vrow">{st(FIG('5-3_e5', 'fig'))}{STEPS(STP('١) الثالثة في المثلث', M('١٨٠', MI, '٤٥', MI, '٦٠', EQ, '٧٥°', cls='sm')), STP('٢) أ تقابلها بالرأس', M('أ', EQ, '٧٥°', cls='sm'), 'fin'))}</div>'''))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('تمرين ٦')}</div><h2>لماذا أب = أج؟</h2>
<div class="row vrow">{st(FIG('5-3_e6', 'fig'))}{STEPS(STP('١) الزاوية عند ب', M('١٨٠', MI, '٣٦', MI, '٧٢', EQ, '٧٢°', cls='sm')), STP('٢) زاويتان متساويتان', '<span class="why">عند ب وعند ج</span>'), STP('٣) المثلث متطابق الضلعين', '<span class="kk">أب = أج</span>', 'fin'))}</div>''' + tn('تعليق الدليل: يجب أن يذكر الطلاب أنه إذا تساوت زاويتان في مثلث فهو متطابق الضلعين.')))
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('النشاط تمرين ٤')}</div><h2>معاً: زاويةٌ في مثلثٍ متطابق الضلعين ٣٨°</h2>
<div class="row">{''.join(st(f'<button class="flip box col" style="flex:1"><span class="hint">{q}</span><span class="tap">👆</span><span class="hid col"><span class="kk c-we">{a_}</span><span class="why">{w}</span></span></button>') for q, a_, w in (('إن كانت ٣٨° زاوية الرأس', '٧١° و ٧١°', '(١٨٠ − ٣٨) ÷ ٢'), ('إن كانت ٣٨° زاوية قاعدة', '٣٨° و ١٠٤°', '١٨٠ − ٣٨ − ٣٨')))}</div>''' + tn('إجابة الدليل ص١٠٥: ٣٨°، ١٠٤° أو ٧١°، ٧١°.')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('النشاط تمرين ٣')}{timer(2)}</div>''' + quiz('زاويتان في مثلث: ١٢٨° و ٢٦°. لماذا هو متطابق الضلعين؟', ['لأن الثالثة ٢٦°', 'لأن فيه زاويةً منفرجة', 'لأن مجموعهما ١٥٤°'], 0, '١٨٠ − ١٢٨ − ٢٦ = ٢٦°، فهناك زاويتان متساويتان')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('تمرين ٣')}</div><h2>لماذا زوايا المثلث ١٨٠°؟</h2>
<div class="row vrow">{st(FIG('5-3_e3', 'fig lg'))}{STEPS(STP('١) عند أ ثلاث زوايا ملوّنة', ''), STP('٢) هي زوايا المثلث الثلاث', ''), STP('٣) تكوّن معاً خطاً مستقيماً', M('١٨٠°', cls='sm'), 'fin'))}</div>''' + tn('تعليق الدليل على التمرين ٣: وجّه الطلاب إلى قراءة الفقرة الأخيرة في مقدمة الوحدة (ص٨٩).')))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج 🎫</span><h2>الحصة الثانية</h2>
<div class="exit">{st('<div><b>١</b>متطابق الضلعين زاوية رأسه ١٠٠°. أوجد زاويتي القاعدة.</div>')}{st('<div><b>٢</b>مثلثٌ زاويتان فيه ٥٠° و ٨٠°. هل هو متطابق الضلعين؟</div>')}</div>
<button class="flip box col" style="min-width:36vw"><span class="tap">👆 الإجابات</span><span class="hid col"><span class="kk">١) ٤٠° و ٤٠°</span><span class="kk">٢) نعم: الثالثة ٥٠°</span></span></button>''' + tn('من إعدادي (غير موجودة في الكتابين).')))
S.append(slide('''<span class="qbadge" style="background:#0A6770;box-shadow:0 4px 0 #05393E">الواجب المنزلي 🏠</span><h2>كتاب النشاط</h2>
<div class="exit"><div class="st"><div><b>١</b>الصفحتان ٦٨ و ٦٩ في كتاب النشاط</div></div></div>''' + tn('الدليل ص٩٩ يذكر «ص٧٠–٧١»، وتمارين هذا الدرس في كتاب النشاط ص٦٨–٦٩ (وص٧٠ تبدأ بالدرس ٥-٤).')))
S.append(slide(f'''<h2>الخلاصة</h2>
<div class="sumg">
{st(box('<div class="col"><b class="kk c-b">متقابلتان بالرأس</b><span>متساويتان</span></div>'))}
{st(box('<div class="col"><b class="kk c-we">متطابق الضلعين</b><span>زاويتا القاعدة متساويتان</span></div>'))}
{st(box('<div class="col"><b class="kk c-exp">التبرير</b><span>عبارةٌ قصيرة تكفي</span></div>'))}</div>'''))

# ═══════════ ملحق: تمارين كتاب الطالب ص٩٦–٩٧ (الإجابات من دليل المعلم ص١٠٣) ═══════════
S.append(launch('sb', '٩٦ و ٩٧', note=f'المراجع: كتاب الطالب ص٩٦ و ٩٧، ودليل المعلم ص٩٩ وإجاباته ص١٠٣ · {ME}'))
H = ['أ', 'ب', 'ج', 'د', 'هـ']
S.append(ex(1, 'أثبت أن (أ ع ج) = (ء ع ب)', 'زاويتان على خطٍّ مستقيم مجموعهما ١٨٠°', [(FIG('5-3_e1', 'fig side') + 'البرهان', '(أ ع ج) = ١٨٠° − (أ ع ء)<small>(ء ع ب) = ١٨٠° − (أ ع ء) ، إذن الزاويتان متساويتان</small>')], cols=1))
S.append(ex(2, 'احسب أ و ب و ج و ء', 'على خطٍّ مستقيم ١٨٠° · المتقابلتان بالرأس متساويتان', [(FIG('5-3_e2', 'fig side') + 'الزوايا الأربع', 'أ = ٧٣° ، ب = ٦١°<small>ج = ٤٦° ، ء = ٧٣° (متقابلة بالرأس)</small>')], cols=1))
S.append(ex(3, 'لماذا مجموع زوايا المثلث ١٨٠°؟', 'انظر إلى الزوايا عند النقطة أ', [(FIG('5-3_e3', 'fig lg') + 'التفسير', 'الزوايا عند أ هي زوايا المثلث الثلاث<small>وتكوّن معاً خطاً مستقيماً</small>')], cols=1))
S.append(ex(4, 'متطابق الضلعين و (ب أ ج) = ٤٠°', 'زاويتا القاعدة متساويتان', [(FIG('5-3_e4', 'fig side') + 'باقي الزوايا', '٧٠° و ٧٠°<small>(١٨٠ − ٤٠) ÷ ٢</small>')], cols=1))
S.append(ex(5, 'احسب أ', 'الثالثة في المثلث، ثم المتقابلة بالرأس', [(FIG('5-3_e5', 'fig side') + 'قياس أ', '٧٥°<small>١٨٠ − ٤٥ − ٦٠ = ٧٥° ، وأ تقابلها بالرأس</small>')], cols=1))
S.append(ex(6, 'فسّر لماذا أب = أج', 'زاويتان متساويتان ← مثلثٌ متطابق الضلعين', [(FIG('5-3_e6', 'fig side') + 'التفسير', 'الزاوية الثالثة ٧٢°<small>فالمثلث متطابق الضلعين، والضلعان أب و أج متساويان</small>')], cols=1))

# ═══════════ ملحق: حلول كتاب النشاط ص٦٨–٦٩ (الإجابات من دليل المعلم ص١٠٥) ═══════════
S.append(launch('ab', '٦٨ و ٦٩', note='الإجابات النهائية من دليل المعلم ص ١٠٥'))
NA, NB = 'نشاط ص ٦٨ · تمرين', 'نشاط ص ٦٩ · تمرين'
S.append(ex(1, 'ثلاثة خطوطٍ تتقاطع في نقطة', 'على خطٍّ مستقيم ١٨٠° · المتقابلتان بالرأس متساويتان', [(FIG('5-3_a1', 'fig side') + 'أ و ب و ج', 'أ = ٧٤° ، ب = ٤٢°<small>ج = ٦٤° (متقابلات بالرأس)</small>')], cols=1, src=NA))
S.append(ex(2, 'أب و ج ء متعامدان', 'القائمة ٩٠° · المتقابلتان بالرأس متساويتان', [(FIG('5-3_a2', 'fig side') + '(أ) (ب ن و)', '٥٥°<small>٩٠ − ٣٥</small>'), ('(ب) (هـ ن ج)', '٣٥°<small>تقابل (ء ن و) بالرأس</small>'), ('(ج) (أ ن هـ)', '٥٥°<small>تقابل (ب ن و) بالرأس</small>')], cols=1, src=NA))
S.append(ex(3, 'زاويتان في مثلث: ١٢٨° و ٢٦°', 'زاويتان متساويتان ← متطابق الضلعين', [('لماذا هو متطابق الضلعين؟', 'الثالثة ١٨٠ − ١٥٤ = ٢٦°<small>فهناك زاويتان متساويتان</small>')], cols=1, src=NA))
S.append(ex(4, 'زاويةٌ في متطابق الضلعين ٣٨°', 'قد تكون زاوية الرأس أو زاوية قاعدة', [('الزاويتان الأخريان', '٧١° و ٧١°<small>أو ٣٨° و ١٠٤°</small>')], cols=1, src=NA))
S.append(ex(5, 'أب = أج = أء', 'كل مثلثٍ منهما متطابق الضلعين', [(FIG('5-3_a5', 'fig side') + '(أ) (أ ب ج)', '٦٥°<small>(١٨٠ − ٥٠) ÷ ٢</small>'), ('(ب) (أ ء ج)', '٦٨°<small>(١٨٠ − ٤٤) ÷ ٢</small>'), ('(ج) (ب ج ء)', '١٣٣°<small>٦٥ + ٦٨</small>')], cols=1, src=NB))

PG = {'تمرين': [(1, '٩٦'), (4, '٩٧')]}

EXTRA_CSS_OWN = FIG_CSS + '''
.stps{display:flex;flex-direction:column;gap:1.2vh;align-items:stretch}
.stp{display:flex;align-items:center;gap:1.4vw;justify-content:space-between}
.stp .lab{flex:0 1 auto;max-width:60%;font-family:var(--fh);font-weight:800;color:#2563EB;background:#EAF1FF;border-radius:12px;padding:.2em .8em;text-align:center;line-height:1.4;font-size:clamp(20px,3.6vh,42px)}
.stp.fin .lab{background:var(--good);color:#fff}
.slide .vrow{align-items:center;justify-content:center;gap:2vh 3vw;flex-wrap:wrap}
.voc3{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1.6vw;width:min(1500px,94vw)}
.voc3 .st>div{display:flex;flex-direction:column;align-items:center;gap:.6vh;background:#fff;border:3px solid var(--line);border-radius:18px;padding:1.6vh 1vw;text-align:center}
.voc3 b{font-family:var(--fh);font-size:clamp(28px,5.4vh,64px);color:var(--base)}.voc3 i{font-style:normal;font-weight:700;color:var(--ink2);font-size:clamp(16px,2.8vh,32px)}
.voc3 span{font-weight:700;font-size:clamp(20px,3.6vh,42px);line-height:1.5}
.slide .svgfig.ang{width:auto;height:min(84vh,820px);max-width:54vw;max-height:none}
.slide .vrow .fig{height:min(56vh,520px);width:auto;max-width:52vw;max-height:none}
.slide .vrow .fig.lg{max-width:62vw;height:auto}
.why{font-weight:700;color:var(--ink2);font-size:clamp(20px,3.4vh,40px)}
.errs{display:flex;flex-direction:column;gap:1.4vh;width:min(1300px,90vw)}
.errs .err{display:flex;flex-direction:column;align-items:center;gap:.6vh;background:#fff;border:3px solid var(--line);border-radius:16px;padding:.8vh 1.6vw;font-size:clamp(24px,4.6vh,54px);font-weight:700}
.errs .err .xa{font-size:clamp(20px,3.8vh,44px)}
.xa.ok{color:var(--good)}
.sumg{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:2vw;width:min(1600px,94vw)}
.sumg .col span{font-weight:700;font-size:clamp(20px,3.6vh,42px);line-height:1.5}
.sumg .kk{font-size:clamp(26px,4.8vh,58px)}
.hid.col .kk{font-size:clamp(26px,4.8vh,56px)}
.q .fig{height:26vh;width:auto;vertical-align:middle}
.xq .fig.side{height:40vh}
.xa small{display:block}
@media (max-aspect-ratio:1/1){.voc3,.sumg{grid-template-columns:1fr}}
'''
