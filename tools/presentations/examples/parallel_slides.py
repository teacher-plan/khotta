# شرائح درس ٥-٤ «الخطوط المتوازية» — الصف السابع (٣ حصص، كتاب الطالب ص٩٨–١٠١)
# المراجع: دليل المعلم ص١٠٠–١٠١ (المفردات: المتقابلة بالرأس، متوازٍ، القاطع، المتناظرة، المتبادلة؛ نقاط التعلّم: تحديد أربعة أزواج متناظرة
# وزوجين متبادلين وأربعة متقابلة بالرأس؛ الخطأ الشائع: الظنّ أن كل زاويتين متساويتين متناظرتان أو متبادلتان؛ النشاط ١: تحريك القاطع/الخط حتى
# يتوازى الخطّان فتتساوى المتناظرتان ثم المتبادلتان؛ الحرفان F و Z للتذكير فقط لا قاعدة؛ تعليقات التمرينين ٥ و٦؛ الواجب: النشاط ص٧٠–٧٢)،
# كتاب الطالب ص٩٨–١٠١ (مثال ٥-٤)، وإجابات الدليل ص١٠٣ (كتاب الطالب) وص١٠٦ (كتاب النشاط).
# python3.12 gen_powers.py parallel_slides.py الخطوط_المتوازية_عرض_تفاعلي.html "الخطوط المتوازية — الصف السابع"
exec(open(os.path.join(HERE, 'figs.py'), encoding='utf-8').read())

def STP(lab, expr='', cls=''): return st(f'<div class="stp {cls}"><span class="lab">{lab}</span>{expr}</div>')
def STEPS(*rows): return '<div class="stps">' + ''.join(rows) + '</div>'
def VC(items, cls=''): return f'<div class="voc3 {cls}">' + ''.join(st(f'<div><b>{w}</b><i>{e}</i><span>{d}</span></div>') for w, e, d in items) + '</div>'
MI = '<span class="x">−</span>'; PL = '<span class="x">+</span>'
S = []
ME = 'إعداد: أ. عيسى الحارثي'
S.append(slide(f'''<span class="tag">الصف السابع · الدرس ٥-٤</span>
<h1 class="h1s">الخطوط المتوازية</h1>
<p class="lead">كتاب الطالب ص ٩٨ إلى ١٠١ · ثلاث حصص</p>
<p class="lead" style="font-size:clamp(26px,4.8vh,56px)">{ME}</p>''', 'cover'))
CAN = ['أحدّد <b>الزوايا المتناظرة</b> و<b>المتبادلة</b> و<b>المتقابلة بالرأس</b>', 'أستخدم أنها <b>متساوية</b> لأحسب زوايا مجهولة', 'أحكم: هل الخطّان <b>متوازيان</b>؟ وأعطي سبباً']
S.append(slide(f'''<h2>في نهاية هذا الدرس…</h2>
<div class="can">{''.join(f'<div><span class="can-i">✔</span><span><b>أنا أستطيع</b> أن {t}</span></div>' for t in CAN)}</div>'''))
S.append(slide(f'''<h2>مفردات الدرس (١)</h2>
{VC([('متوازيان', 'parallel', 'خطّان البعد العمودي بينهما ثابت فلا يلتقيان'), ('القاطع', 'transversal', 'خطٌّ مستقيم يقطع خطّين متوازيين')], 'c2')}''' + tn('المفردات من الدليل ص١٠٠، والتعريفات من الكتاب ص٩٨.')))
S.append(slide(f'''<h2>مفردات الدرس (٢)</h2>
{VC([('المتناظرتان', 'corresponding angles', 'في الموضع نفسه عند تقاطعين (شكل F)'), ('المتبادلتان', 'alternate angles', 'على جانبين مختلفين من القاطع وبين المتوازيين (شكل Z)'), ('المتقابلتان بالرأس', 'vertically opposite', 'متقابلتان عند التقاطع نفسه')])}'''))

# ═══════════ الحصة الأولى ═══════════
S.append(slide('''<span class="tag">الحصة الأولى · ٤٠ دقيقة</span><h2>المتوازيان والقاطع والزوايا المتناظرة</h2>
<div class="plan"><div><b>٤ د</b>تذكّر</div><div><b>٦ د</b>الخطوط المتوازية</div><div><b>٨ د</b>القاطع والزوايا الثماني</div>
<div><b>٨ د</b>المتناظرة (F)</div><div><b>٨ د</b>نحن ← أنتم</div><div><b>٣ د</b>انتبه</div><div><b>٣ د</b>بطاقة الخروج</div></div>''', 'divider'))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">تذكّر 🔁</span>{ref('الدرس ٥-٣')}{timer(1)}</div>''' + quiz('خطّان متقاطعان، إحدى الزوايا ٧٠°. الزاوية المقابلة لها بالرأس…', [M('٧٠°'), M('١١٠°'), M('٢٩٠°')], 0, 'المتقابلتان بالرأس متساويتان')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('كتاب الطالب ص ٩٨')}</div><h2>الخطوط المتوازية</h2>
<div class="row vrow">{st(FIG('5-4_par', 'fig lg'))}{STEPS(STP('البعد العمودي بينهما', '<span class="kk">ثابت</span>'), STP('لا يلتقيان مهما امتدّا', ''), STP('نرسم عليهما أسهماً متشابهة', '<span class="kk">⟶</span>', 'fin'))}</div>'''))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('كتاب الطالب ص ٩٨')}</div><h2>قاطعٌ يقطع خطّين متوازيين</h2>
<div class="row vrow">{st(PAR())}{STEPS(STP('تقاطعان', '<span class="kk">٨ زوايا</span>'), STP('عند العلوي', '<span class="kk">أ ب ج ء</span>'), STP('عند السفلي', '<span class="kk">هـ و ز ح</span>', 'fin'))}</div>''' + tn('رسمٌ من إعدادي بالترتيب نفسه عند كل تقاطع (أعلى اليمين، أعلى اليسار، أسفل اليسار، أسفل اليمين)؛ وشكل الكتاب ص٩٨ بحروفٍ أخرى.')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('كتاب الطالب ص ٩٨')}</div><h2>الزاويتان المتناظرتان: شكل F</h2>
<div class="row vrow">{st(PAR([(0, 4)], shape='F'))}{STEPS(STP('أ و هـ', '<span class="kk">في الموضع نفسه</span>'), STP('على جهة القاطع نفسها', ''), STP('المتناظرتان', '<span class="kk">متساويتان</span>', 'fin'))}</div>''' + tn('الدليل: يُشار أحياناً إلى المتناظرة بالحرف F والمتبادلة بالحرف Z، لكنهما لا يُستخدمان كقاعدة؛ بل لتذكير الطلاب بأشكال تلك الزوايا.')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('كتاب الطالب ص ٩٨')}</div><h2>أربعة أزواجٍ متناظرة</h2>
<div class="row vrow">{st(PAR([(0, 4), (1, 5), (2, 6), (3, 7)]))}{STEPS(STP('أ و هـ', ''), STP('ب و و', ''), STP('ج و ز', ''), STP('ء و ح', '', 'fin'))}</div>''' + tn('الدليل: يجب أن يتمكن الطلاب من تحديد أربعة أزواجٍ من الزوايا المتناظرة. كل زوجٍ بلونٍ واحد.')))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">النشاط 🎲</span>{ref('دليل المعلم ص ١٠٠')}</div><h2>متى تتساوى المتناظرتان؟</h2>
<div class="exit">{st('<div><b>١</b>خطّان ثابتان ومسطرةٌ طويلة تمثّل خطاً ثالثاً متحرّكاً</div>')}{st('<div><b>٢</b>إن لم يتوازَ الخطّان فالمتناظرتان غير متساويتين، ويلتقيان إن امتدّا</div>')}{st('<div><b>٣</b>نحرّك الخطّ حتى يتوازيا: تتساوى المتناظرتان</div>')}</div>''' + tn('النشاط ١ في الدليل ص١٠٠–١٠١: ارسم خطّين ثابتين على اللوح واستخدم مسطرةً طويلة، ويمكن التحقّق بورقةٍ شفافة تُنقل عليها الزاوية.')))
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('تمرين ١ (أ)')}</div><h2>معاً: الزاوية المتناظرة مع…</h2>
<div class="row vrow">{st(FIG('5-4_e1', 'fig'))}<div class="row">{''.join(st(f'<button class="flip box col"><span class="kk">{q}</span><span class="tap">👆</span><span class="hid col"><span class="kk c-we">{a_}</span></span></button>') for q, a_ in (('ش', 'ف'), ('ر', 'ع'), ('ت', 'ص'), ('ث', 'م')))}</div></div>''' + tn('في هذا الشكل الخطّان الرأسيان هما المتوازيان، والخطّ المائل هو القاطع. إجابة الدليل ص١٠٣.')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ٢ (أ)')}{timer(2)}</div>''' + quiz('أيّ زاويةٍ تناظر الزاوية ٦٢°؟ ' + FIG('5-4_e2', 'fig sm'), ['ب', 'أ', 'ج', 'ء'], 0, 'في الموضع نفسه: أعلى يمين التقاطع ⟸ ب = ٦٢°')))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">انتبه ⚠️ خطأ شائع</span>{ref('دليل المعلم ص ١٠٠')}</div><h2>متساويتان… لكن ليستا متناظرتين!</h2>
<div class="row vrow">{st(PAR([(0, 2)]))}<div class="errs">{st('<button class="flip err"><span class="xq">أ = ج ، إذن هما متناظرتان</span><span class="tap">👆</span><span class="hid xa no">✘ أ و ج متقابلتان بالرأس عند التقاطع نفسه</span></button>')}</div></div>''' + tn('الدليل: قد يعتقد بعض الطلاب أنه إذا تساوت زاويتان في القياس فإما أن تكونا متناظرتين أو متبادلتين، لذا أعطِ أمثلةً لتوضيح ذلك.')))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج 🎫</span><h2>الحصة الأولى</h2>
<div class="row vrow">{st(PAR())}<div class="exit">{st('<div><b>١</b>ما الزاوية المناظرة لـ ب؟</div>')}{st('<div><b>٢</b>ما الزاوية المناظرة لـ ح؟</div>')}</div></div>
<button class="flip box col" style="min-width:30vw"><span class="tap">👆 الإجابات</span><span class="hid col"><span class="kk">١) و</span><span class="kk">٢) ء</span></span></button>''' + tn('من إعدادي (غير موجودة في الكتابين).')))

# ═══════════ الحصة الثانية ═══════════
S.append(slide('''<span class="tag">الحصة الثانية · ٤٠ دقيقة</span><h2>المتبادلة والمتقابلة بالرأس</h2>
<div class="plan"><div><b>٤ د</b>تذكّر</div><div><b>٨ د</b>المتبادلة (Z)</div><div><b>٦ د</b>المتقابلة بالرأس</div>
<div><b>٨ د</b>مثال ٥-٤</div><div><b>٨ د</b>نحن ← أنتم</div><div><b>٣ د</b>الحروف</div><div><b>٣ د</b>بطاقة الخروج</div></div>''', 'divider'))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">تذكّر 🔁</span>{timer(1)}</div>''' + quiz('المتناظرتان عند خطّين متوازيين…', ['متساويتان', 'مجموعهما ١٨٠°', 'لا علاقة بينهما'], 0, 'شكل F: في الموضع نفسه ومتساويتان')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('كتاب الطالب ص ٩٨')}</div><h2>الزاويتان المتبادلتان: شكل Z</h2>
<div class="row vrow">{st(PAR([(2, 4)], shape='Z'))}{STEPS(STP('ج و هـ', '<span class="kk">بين المتوازيين</span>'), STP('على جهتين مختلفتين من القاطع', ''), STP('المتبادلتان', '<span class="kk">متساويتان</span>', 'fin'))}</div>'''))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('كتاب الطالب ص ٩٨')}</div><h2>زوجان متبادلان، وأربعة أزواجٍ متقابلة بالرأس</h2>
<div class="row vrow">{st(PAR([(2, 4), (3, 5)]))}{STEPS(STP('المتبادلة', '<span class="kk">ج و هـ · ء و و</span>'), STP('المتقابلة بالرأس', '<span class="kk">أ و ج · ب و ء</span>'), STP('وأيضاً', '<span class="kk">هـ و ز · و و ح</span>', 'fin'))}</div>''' + tn('الدليل: زوجان من المتبادلة وأربعة أزواج من المتقابلة بالرأس عند خطّين متوازيين وقاطع.')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('مثال ٥-٤')}</div><h2>أكمل الفراغ برمز الزاوية الصحيح</h2>
<div class="row vrow">{st(FIG('5-4_ex', 'fig'))}{STEPS(STP('(أ) (ج) و ☐ متناظرتان', M('(ط)', cls='sm')), STP('(ب) (ج) و ☐ متبادلتان', M('(ن)', cls='sm')), STP('(ج) (ء) و ☐ متناظرتان', M('(ل)', cls='sm')), STP('(د) (ء) و ☐ متبادلتان', M('(ر)', cls='sm'), 'fin'))}</div>''' + tn('الكتاب ص٩٨: نبحث عن الزاوية التي تشكّل حرف F مع (ج) للمتناظرة، وحرف Z للمتبادلة.')))
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('تمرين ٤')}</div><h2>معاً: أكمل بما يناسب</h2>
<div class="row vrow">{st(FIG('5-4_e4', 'fig'))}<div class="col" style="gap:1vh">{''.join(st(f'<button class="flip box col"><span class="hint">{q}</span><span class="tap">👆</span><span class="hid col"><span class="kk c-we">{a_}</span></span></button>') for q, a_ in (('(أ ع ص) و (ج ف ص)', 'متناظرتان'), ('(أ ع ص) و (س ف ء)', 'متبادلتان'), ('(أ ع س) و ☐ متناظرتان', '(ج ف س)'), ('(ج ف س) و ☐ متبادلتان', '(ب ع ص)')))}</div></div>'''))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ٩')}{timer(2)}</div>''' + quiz('في شكل التمرين ٩: (ء) و (هـ) زاويتان… ' + FIG('5-4_e9', 'fig sm'), ['متبادلتان', 'متناظرتان', 'متقابلتان بالرأس'], 0, 'بين المتوازيين وعلى جهتين مختلفتين من القاطع')))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">تحدٍّ 💡</span>{ref('تمرين ٥')}</div><h2>حروفٌ إنجليزية فيها زوايا متناظرة أو متبادلة</h2>
<div class="row">{''.join(st(f'<button class="flip box col" style="flex:1"><span class="hint">{q}</span><span class="tap">👆</span><span class="hid col"><span class="kk c-we" style="direction:ltr">{a_}</span></span></button>') for q, a_ in (('متناظرة مثل F', 'E'), ('متبادلة مثل Z', 'N · W · H')))}</div>''' + tn('إجابة الدليل ص١٠٣: (أ) E (ب) H، N، W. وتعليق الدليل: تعتمد الإجابة على طريقة رسم الطلاب للحروف الكبيرة.')))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج 🎫</span><h2>الحصة الثانية</h2>
<div class="row vrow">{st(PAR())}<div class="exit">{st('<div><b>١</b>ما الزاوية المبادلة لـ ء؟</div>')}{st('<div><b>٢</b>ما الزاوية المقابلة لـ هـ بالرأس؟</div>')}</div></div>
<button class="flip box col" style="min-width:30vw"><span class="tap">👆 الإجابات</span><span class="hid col"><span class="kk">١) و</span><span class="kk">٢) ز</span></span></button>''' + tn('من إعدادي (غير موجودة في الكتابين).')))

# ═══════════ الحصة الثالثة ═══════════
S.append(slide('''<span class="tag">الحصة الثالثة · ٤٠ دقيقة</span><h2>نحسب الزوايا ونحكم على التوازي</h2>
<div class="plan"><div><b>٤ د</b>تذكّر</div><div><b>٨ د</b>زاويةٌ واحدة تكفي</div><div><b>٨ د</b>هل هما متوازيان؟</div>
<div><b>٨ د</b>نحن</div><div><b>٦ د</b>أنتم</div><div><b>٣ د</b>الخلاصة</div><div><b>٣ د</b>بطاقة الخروج</div></div>''', 'divider'))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">تذكّر 🔁</span>{timer(1)}</div>''' + quiz('المتبادلتان عند خطّين متوازيين…', ['متساويتان', 'مجموعهما ٣٦٠°', 'لا علاقة بينهما'], 0, 'شكل Z: متساويتان')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('تمرين ٣')}</div><h2>زاويةٌ واحدة تكفي لمعرفة الثماني</h2>
<div class="row vrow">{st(PAR([(0, 2, 4, 6), (1, 3, 5, 7)], vals=['٦٠°', '١٢٠°', '٦٠°', '١٢٠°', '٦٠°', '١٢٠°', '٦٠°', '١٢٠°']))}{STEPS(STP('١) المتقابلة بالرأس', '<span class="why">متساوية</span>'), STP('٢) على خطٍّ مستقيم', M('١٨٠', MI, '٦٠', EQ, '١٢٠°', cls='sm')), STP('٣) المتناظرة', '<span class="why">تنقل القياسات إلى التقاطع الآخر</span>', 'fin'))}</div>''' + tn('الأرقام من إعدادي على نمط التمرين ٣ (١٠٥° و ٧٥°): الزوايا الثماني نوعان فقط.')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('تمرين ٣')}</div><h2>الزوايا التي تساوي ١٠٥° والتي تساوي ٧٥°</h2>
<div class="row vrow">{st(FIG('5-4_e3', 'fig'))}{STEPS(STP('١) ف تقابل ١٠٥° بالرأس', M('١٠٥°', cls='sm')), STP('٢) ص تناظر ١٠٥°', M('١٠٥°', cls='sm')), STP('٣) ش تقابل ص بالرأس', M('١٠٥°', cls='sm')), STP('٤) و ع ، م ، ر', M('٧٥°', cls='sm'), 'fin'))}</div>'''))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('تمرين ٦')}</div><h2>لماذا لا يمكن أن يكون أب و ج ء متوازيين؟</h2>
<div class="row vrow">{st(FIG('5-4_e6', 'fig'))}{STEPS(STP('١) لو كانا متوازيين', '<span class="why">تتساوى المتناظرتان</span>'), STP('٢) المتناظرتان هنا', M('٥٠° و ٤٠°', cls='sm')), STP('٣) غير متساويتين', '<span class="kk">ليسا متوازيين</span>', 'fin'))}</div>''' + tn('تعليق الدليل: يجب أن يتأكد الطلاب أنه إذا لم تكن الزوايا المتناظرة متساوية فإن المستقيمات غير متوازية، رغم أن الزوايا تبدو متساوية في الشكل.')))
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('النشاط تمرين ٢')}</div><h2>معاً: أ و ب و ج و ء</h2>
<div class="row vrow">{st(FIG('5-4_a2', 'fig'))}<div class="row">{''.join(st(f'<button class="flip box col"><span class="kk">{q}</span><span class="tap">👆</span><span class="hid col"><span class="kk c-we">{a_}</span><span class="why">{w}</span></span></button>') for q, a_, w in (('أ', '٧٥°', 'متقابلة بالرأس'), ('ب', '٧٥°', 'تناظر ٧٥°'), ('ج', '١٠٥°', 'على خطٍّ مستقيم'), ('ء', '١٠٥°', 'تبادل ج')))}</div></div>''' + tn('إجابة الدليل ص١٠٦.')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('النشاط تمرين ٥')}{timer(2)}</div>''' + quiz('أيّ خطّين متوازيان؟ ' + FIG('5-4_a5', 'fig sm'), ['ل و ن', 'ل و م', 'م و ن'], 0, 'المتناظرتان عندهما متساويتان (٨٠° و ١٠٠°)')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('النشاط تمرين ٦')}</div>''' + quiz('أوجد ن ' + FIG('5-4_a6', 'fig sm'), [M('١٢٠°'), M('٦٠°'), M('٢٤٠°')], 0, 'تقابل ١٢٠° بالرأس ثم تناظرها: ن = ١٢٠°')))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج 🎫</span><h2>الحصة الثالثة</h2>
<div class="row vrow">{st(PAR(vals=['٧٠°', None, None, None, None, None, None, None]))}<div class="exit">{st('<div><b>١</b>أوجد هـ</div>')}{st('<div><b>٢</b>أوجد و</div>')}</div></div>
<button class="flip box col" style="min-width:30vw"><span class="tap">👆 الإجابات</span><span class="hid col"><span class="kk">١) ٧٠° (تناظر أ)</span><span class="kk">٢) ١١٠° (على خطٍّ مستقيم مع هـ)</span></span></button>''' + tn('من إعدادي (غير موجودة في الكتابين).')))
S.append(slide('''<span class="qbadge" style="background:#0A6770;box-shadow:0 4px 0 #05393E">الواجب المنزلي 🏠</span><h2>كتاب النشاط</h2>
<div class="exit"><div class="st"><div><b>١</b>الصفحات ٧٠ إلى ٧٢ في كتاب النشاط</div></div></div>'''))
S.append(slide(f'''<h2>الخلاصة</h2>
<div class="sumg">
{st(box('<div class="col"><b class="kk c-b">المتناظرة</b><span>الموضع نفسه (F)<br>متساوية</span></div>'))}
{st(box('<div class="col"><b class="kk c-we">المتبادلة</b><span>بين المتوازيين (Z)<br>متساوية</span></div>'))}
{st(box('<div class="col"><b class="kk c-exp">المتقابلة بالرأس</b><span>عند التقاطع نفسه<br>متساوية</span></div>'))}</div>'''))

# ═══════════ ملحق: تمارين كتاب الطالب ص٩٩–١٠١ (الإجابات من دليل المعلم ص١٠٣) ═══════════
S.append(launch('sb', '٩٩ إلى ١٠١', note=f'المراجع: كتاب الطالب ص٩٨ إلى ١٠١، ودليل المعلم ص١٠٠ و ١٠١ وإجاباته ص١٠٣ · {ME}'))
H = ['أ', 'ب', 'ج', 'د']
RF = 'المتناظرة: الموضع نفسه (F) · المتبادلة: بين المتوازيين وعلى جهتين (Z)'
S.append(ex(1, 'انظر إلى الشكل', RF, [(FIG('5-4_e1', 'fig side') + '(أ) أربعة أزواجٍ متناظرة', '(ش ، ف) · (ت ، ص)<small>(ر ، ع) · (ث ، م)</small>'), ('(ب) زوجان متبادلان', '(ث ، ف) · (ر ، ص)')], cols=1))
S.append(ex(2, 'إحدى الزوايا ٦٢°', RF, [(FIG('5-4_e2', 'fig side') + '(أ) ☐ = ٦٢° لأن المتناظرة متساوية', 'ب'), ('(ب) ☐ = ٦٢° لأن المتبادلة متساوية', 'ء')], cols=1))
S.append(ex(3, 'في الشكل المقابل', 'المتقابلة بالرأس والمتناظرة متساوية', [(FIG('5-4_e3', 'fig side') + '(أ) الزوايا التي تساوي ١٠٥°', 'ف ، ص ، ش'), ('(ب) الزوايا التي تساوي ٧٥°', 'ع ، م ، ر')], cols=1))
S.append(ex(4, 'أكمل بما يناسب', RF, [(FIG('5-4_e4', 'fig side') + '(أ) (أ ع ص) و (ج ف ص)', 'متناظرتان'), ('(ب) (أ ع ص) و (س ف ء)', 'متبادلتان'), ('(ج) (أ ع س) و ☐ متناظرتان', '(ج ف س)'), ('(د) (ج ف س) و ☐ متبادلتان', '(ب ع ص)')], cols=2))
S.append(ex(5, 'الحروف الإنجليزية الكبيرة', 'في F زوايا متناظرة، وفي Z زوايا متبادلة', [('(أ) حروفٌ فيها زوايا متناظرة', '<span style="direction:ltr;display:inline-block">E</span>'), ('(ب) حروفٌ فيها زوايا متبادلة', '<span style="direction:ltr;display:inline-block">H · N · W</span>')], cols=2, note='تعليق الدليل: تعتمد الإجابة على كيفية رسم الطلاب للحروف الكبيرة.'))
S.append(ex(6, 'لماذا لا يكون أب و ج ء متوازيين؟', 'لو توازيا لتساوت المتناظرتان', [(FIG('5-4_e6', 'fig side') + 'التفسير', 'المتناظرتان (س م أ) و (س ر ج) يجب أن تتساويا<small>وهما ٥٠° و ٤٠°، فالخطّان غير متوازيين</small>')], cols=1))
S.append(ex(7, 'ثلاثة خطوطٍ متوازية', RF, [(FIG('5-4_e7', 'fig side') + '(أ) ثلاث زوايا متناظرة مع (و)', 'ب ، و ، ي'), ('(ب) زوجٌ متبادل يشمل (ع)', '(ع ، هـ)'), ('(ج) زوجٌ آخر متبادل يشمل (ع)', '(ع ، ط)')], cols=1, note='الحرفان ج و ع متشابهان في الشكل: الزاوية أسفل يسار التقاطع العلوي هي (ع).'))
S.append(ex(8, 'خطّان متوازيان وآخران متوازيان', RF, [(FIG('5-4_e8', 'fig side') + '(أ) زوجان متناظران يشملان (ط)', '(ط ، ف) · (ط ، ك)'), ('(ب) زوجان متبادلان يشملان (س)', '(س ، ي) · (س ، ر)')], cols=1))
S.append(ex(9, 'سمِّ كل زاويتين', 'متبادلة أو متناظرة أو متقابلة بالرأس', [(FIG('5-4_e9', 'fig side') + '(أ) (أ) و (ء)', 'متقابلتان بالرأس'), ('(ب) (ب) و (و)', 'متناظرتان'), ('(ج) (ج) و (ر)', 'متناظرتان'), ('(د) (ء) و (هـ)', 'متبادلتان')], cols=2))

# ═══════════ ملحق: حلول كتاب النشاط ص٧٠–٧٢ (الإجابات من دليل المعلم ص١٠٦) ═══════════
S.append(launch('ab', '٧٠ إلى ٧٢', note='الإجابات النهائية من دليل المعلم ص ١٠٦'))
NA, NB, NC = 'نشاط ص ٧٠ · تمرين', 'نشاط ص ٧١ · تمرين', 'نشاط ص ٧٢ · تمرين'
S.append(ex(1, 'س و ص', RF, [(FIG('5-4_a1', 'fig side') + '(أ) لماذا س = ص؟', 'متقابلتان بالرأس'), ('(ب) المتناظرة مع س', FIG('5-4_g1b') + '<small>الزوايا المظلّلة (من الدليل)</small>'), ('(ج) المتبادلة مع ص', FIG('5-4_g1c') + '<small>الزوايا المظلّلة (من الدليل)</small>')], cols=1, src=NA))
S.append(ex(2, 'احسب أ و ب و ج و ء', 'المتقابلة بالرأس والمتناظرة والمتبادلة متساوية', [(FIG('5-4_a2', 'fig side') + 'الزوايا الأربع', 'أ = ٧٥° (بالرأس) ، ب = ٧٥° (متناظرة)<small>ج = ١٠٥° (على خطٍّ مستقيم) ، ء = ١٠٥° (تبادل ج)</small>')], cols=1, src=NA))
S.append(ex(3, 'الزاوية ٦٨°', RF, [(FIG('5-4_a3', 'fig side') + '(أ) المتناظرة معها', 'ن ، ط'), ('(ب) المتبادلة معها', 'ج ، هـ')], cols=1, src=NA))
S.append(ex(4, 'أكمل العبارات', RF, [(FIG('5-4_a4', 'fig side') + '(أ) (١) متبادلتان: (أ ب ن) و ☐', '(ب هـ و)'), ('(٢) متبادلتان: (ج ب هـ) و ☐', '(ء هـ ب)'), ('(٣) متناظرتان: (ن هـ و) و ☐', '(هـ ب ج)'), ('(ب) هل زينب على صواب؟', 'لا')], cols=2, src=NA))
S.append(ex(5, 'خطّان متوازيان من ثلاثة', 'المتوازيان: المتناظرتان عندهما متساويتان', [(FIG('5-4_a5', 'fig side') + 'حدّدهما واشرح', 'ل و ن<small>المتناظرتان ٨٠° و ١٠٠° متساويتان، والزوايا عند م مختلفة</small>')], cols=1, src=NB))
S.append(ex(6, 'أوجد ن', 'المتقابلة بالرأس ثم المتناظرة', [(FIG('5-4_a6', 'fig side') + 'قياس ن', '١٢٠°<small>تقابل ١٢٠° بالرأس، ثم تناظر ن</small>')], cols=1, src=NB))
S.append(ex(7, 'هل ل١ و ل٢ متوازيان؟', 'نبحث عن متبادلتين متساويتين', [(FIG('5-4_a7', 'fig side') + 'أعطِ سبباً', 'نعم<small>المقابلة بالرأس لـ ٥٠° هي ٥٠°، و ٥٠ + ٧٥ = ١٢٥° تبادل ١٢٥°</small>')], cols=1, src=NB))
S.append(ex(8, 'لماذا أ + ب = ١٨٠°؟', 'متناظرتان ثم خطٌّ مستقيم', [(FIG('5-4_a8', 'fig side') + 'التفسير', 'أ تناظر الزاوية المجاورة لـ ب<small>وهما معاً على خطٍّ مستقيم: ١٨٠°</small>')], cols=1, src=NC))

PG = {'تمرين': [(1, '٩٩'), (5, '١٠٠'), (9, '١٠١')]}

EXTRA_CSS_OWN = FIG_CSS + '''
.stps{display:flex;flex-direction:column;gap:1.2vh;align-items:stretch}
.stp{display:flex;align-items:center;gap:1.4vw;justify-content:space-between}
.stp .lab{flex:0 1 auto;max-width:62%;font-family:var(--fh);font-weight:800;color:#2563EB;background:#EAF1FF;border-radius:12px;padding:.2em .8em;text-align:center;line-height:1.4;font-size:clamp(20px,3.6vh,42px)}
.stp.fin .lab{background:var(--good);color:#fff}
.slide .vrow{align-items:center;justify-content:center;gap:2vh 3vw;flex-wrap:wrap}
.voc3{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1.6vw;width:min(1500px,94vw)}.voc3.c2{grid-template-columns:repeat(2,minmax(0,1fr))}
.voc3 .st>div{display:flex;flex-direction:column;align-items:center;gap:.6vh;background:#fff;border:3px solid var(--line);border-radius:18px;padding:1.6vh 1vw;text-align:center}
.voc3 b{font-family:var(--fh);font-size:clamp(28px,5.4vh,64px);color:var(--base)}.voc3 i{font-style:normal;font-weight:700;color:var(--ink2);font-size:clamp(16px,2.8vh,32px)}
.voc3 span{font-weight:700;font-size:clamp(20px,3.6vh,42px);line-height:1.5}
.slide .svgfig.ang{width:auto;height:min(80vh,780px);max-width:54vw;max-height:none}
.slide .vrow .fig{height:min(56vh,520px);width:auto;max-width:52vw;max-height:none}
.slide .vrow .fig.lg{max-width:60vw;height:auto}
.why{font-weight:700;color:var(--ink2);font-size:clamp(20px,3.4vh,40px)}
.errs{display:flex;flex-direction:column;gap:1.4vh;width:min(900px,60vw)}
.errs .err{display:flex;flex-direction:column;align-items:center;gap:.6vh;background:#fff;border:3px solid var(--line);border-radius:16px;padding:.8vh 1.6vw;font-size:clamp(24px,4.6vh,54px);font-weight:700}
.errs .err .xa{font-size:clamp(20px,3.8vh,44px)}
.sumg{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:2vw;width:min(1600px,94vw)}
.sumg .col span{font-weight:700;font-size:clamp(20px,3.6vh,42px);line-height:1.5}
.sumg .kk{font-size:clamp(26px,4.8vh,58px)}
.hid.col .kk{font-size:clamp(26px,4.8vh,56px)}
.q .fig{height:26vh;width:auto;vertical-align:middle}
.xq .fig.side{height:40vh}
.xa .fig{height:18vh;width:auto;display:block;margin:.4vh auto}
.xa small{display:block}
@media (max-aspect-ratio:1/1){.voc3,.voc3.c2,.sumg{grid-template-columns:1fr}.errs{width:92vw}}
'''
