# عرض مراجعة «الوحدة الثالثة: الأعداد العشرية والكسور العشرية» — الصف السابع.
# المرجع: صفحة ملخّص الوحدة في كتاب الطالب ص٧٦ («يجب أن تعرف أنّ» + «يجب أن تكون قادراً على»)، و«تمارين ومسائل عامة» ص٧٧–٧٨
# (إجابات دليل المعلم ص٨٠، مع تصحيح ٢ (ج) و ٨ (أ) و ١٠ (ب)).
# python3.12 gen_powers.py unit3_slides.py مراجعة_الوحدة_الثالثة_عرض_تفاعلي.html "مراجعة الوحدة الثالثة — الصف السابع"
# لكل جزء: بطاقة القاعدة ← مثالٌ محلول بالرسم ← سؤالٌ سريع (أنتم).
exec(open(os.path.join(HERE, 'vcol.py'), encoding='utf-8').read())
exec(open(os.path.join(HERE, 'figs.py'), encoding='utf-8').read())
DV = '<span class="x">÷</span>'
def STP(lab, expr='', cls=''): return st(f'<div class="stp {cls}"><span class="lab">{lab}</span>{expr}</div>')
def STEPS(*rows): return '<div class="stps">' + ''.join(rows) + '</div>'
def RULE(n, t): return f'<div class="rulecard"><span class="rn">قاعدة {a(n)}</span><span>{t}</span></div>'
def VB(h): return f'<div class="vbox">{h}</div>'
NP = 7
def SEC(n, title, lesson, items):
    return slide(f'''<span class="tag">الجزء {a(n)} من {a(NP)} · الدرس {lesson}</span><h2>{title}</h2>
<div class="exit">{''.join(st(f'<div><b>{a(i + 1)}</b><span>{t}</span></div>') for i, t in enumerate(items))}</div>''', 'divider')

S = []
S.append(slide('''<span class="tag">الصف السابع · مراجعة الوحدة الثالثة</span>
<h1 class="h1s">الأعداد العشرية والكسور العشرية</h1>
<p class="lead" style="font-size:clamp(26px,4.8vh,56px)">إعداد: أ. عيسى الحارثي</p>''', 'cover'))
S.append(slide('''<h2>نراجع الوحدة كلّها في سبعة أجزاء</h2>
<div class="can c2">
<div><span class="can-i">١</span><span>ترتيب الأعداد العشرية</span></div>
<div><span class="can-i">٢</span><span>التقريب</span></div>
<div><span class="can-i">٣</span><span>الجمع والطرح</span></div>
<div><span class="can-i">٤</span><span>الضرب</span></div>
<div><span class="can-i">٥</span><span>القسمة</span></div>
<div><span class="can-i">٦</span><span>قوى ١٠ و ٠٫١ و ٠٫٠١</span></div>
<div><span class="can-i">٧</span><span>التقدير والتحقّق</span></div></div>'''))

# ═══ ١ الترتيب ═══
S.append(SEC(1, 'ترتيب الأعداد العشرية', '٣-١', ['نقارن المنازل من اليسار', 'نوحّد وحدات القياس قبل الترتيب']))
S.append(slide(f'''{RULE(1, 'نقارن الأعداد العشرية منزلةً منزلة من اليسار، وعند ترتيب <b>قياسات</b> نتأكّد أن لها <b>الوحدة نفسها</b>')}
<div class="row vrow">{STEPS(STP('نحوّل إلى سم', M('٧ م = ٧٠٠ سم ، ٠٫٧ م = ٧٠ سم', cls='sm')), STP('القياسات بالسم', M('٧٠٠ ، ٧٥٠ ، ٧٠ ، ٧٧', cls='sm')), STP('الترتيب تصاعدياً', M('٠٫٧ م ، ٧٧ سم ، ٧ م ، ٧٥٠ سم', cls='sm'), 'fin'))}
{VB(valign([('0.7', 'م'), ('0.77', 'م'), ('7', 'م'), ('7.5', 'م')]))}</div>''' + tn('من «تمارين ومسائل عامة» ٨ (ب). على اليسار: القياسات نفسها بالأمتار مصفوفةً عند الفاصلة.')))
S.append(slide(f'''{mode('u')}{timer(1)}''' + quiz('أيّ القياسين أكبر: ٤٢ ملم أم ٠٫٥ سم؟', [M('٤٢ ملم'), M('٠٫٥ سم'), M('متساويان'), M('لا يمكن المقارنة')], 0, '٠٫٥ سم = ٥ ملم، و ٤٢ ملم > ٥ ملم')))

# ═══ ٢ التقريب ═══
S.append(SEC(2, 'التقريب', '٣-٢', ['نحدّد رقم المنزلة المطلوبة', 'الرقم على يمينها ٥ أو أكبر: نضيف ١']))
S.append(slide(f'''{RULE(2, 'نحدّد رقم المنزلة المطلوبة وننظر إلى الرقم على يمينها: <b>٥ أو أكبر</b> نضيف ١، و<b>أصغر من ٥</b> يبقى كما هو')}
<div class="row">{st(box(f'<div class="col"><span class="hint">٦٧٢٥ إلى أقرب ١٠٠</span>{M("٦٧٠٠")}</div>', style="flex:1"))}{st(box(f'<div class="col"><span class="hint">٦٣٫٨١ إلى أقرب عدد كامل</span>{M("٦٤")}</div>', style="flex:1"))}{st(box(f'<div class="col"><span class="hint">٧٫٥٦٦ لمنزلتين عشريتين</span>{M("٧٫٥٧")}</div>', style="flex:1"))}</div>'''))
S.append(slide(f'''{mode('u')}{timer(1)}''' + quiz('قرّب ٢٣٥٨٩٠ إلى أقرب ١٠٠٠٠', [M('٢٣٠٠٠٠'), M('٢٤٠٠٠٠'), M('٢٣٦٠٠٠'), M('٢٠٠٠٠٠')], 1, 'رقم عشرات الآلاف ٣ وعلى يمينه ٥، فنضيف ١: ٢٤٠٠٠٠')))

# ═══ ٣ الجمع والطرح ═══
S.append(SEC(3, 'جمع الأعداد العشرية وطرحها', '٣-٣', ['الصورة الرأسية والفواصل على خطٍّ واحد', 'نكمل المنازل بالأصفار']))
S.append(slide(f'''{RULE(3, 'نكتب العملية <b>رأسياً</b> والفواصل العشرية <b>على خطٍّ واحد</b>، ونكمل المنازل الفارغة بالأصفار')}
<div class="row vrow">{st(box(f'<div class="col"><span class="hint">مجموع رميتَي طلال</span>{vcol("27.29", "29.73", "+")}</div>', style="flex:1"))}{st(box(f'<div class="col"><span class="hint">الفرق بينهما</span>{vcol("29.73", "27.29", "-")}</div>', style="flex:1"))}</div>''' + tn('من «تمارين ومسائل عامة» ١٢: ٢٧٫٢٩ م و ٢٩٫٧٣ م.')))
S.append(slide(f'''{mode('u')}{timer(1)}''' + quiz('أوجد ٣٥ − ٤٫٤٧', [M('٣١٫٤٧'), M('٣٠٫٥٣'), M('٣١٫٥٣'), M('٣٠٫٤٣')], 1, 'نكتب ٣٥٫٠٠ − ٤٫٤٧ = ٣٠٫٥٣')))

# ═══ ٤ الضرب ═══
S.append(SEC(4, 'ضرب الأعداد العشرية', '٣-٤', ['نتجاهل الفاصلة ونضرب', 'نعيدها بعدد الأرقام يمينها في السؤال']))
S.append(slide(f'''{RULE(4, 'نتجاهل الفاصلة ونضرب، ثم <b>نعدّ</b> الأرقام يمين الفاصلة في السؤال و<b>نعيد</b> الفاصلة بالعدد نفسه')}
<div class="row vrow">{STEPS(STP('٦ × ٦ = ٣٦', M('٦', X, '٠٫٦', EQ, '٣٫٦', cls='sm'), 'fin'), STP('٥ × ٩ = ٤٥', M('٥', X, '٠٫٩', EQ, '٤٫٥', cls='sm'), 'fin'))}{st(TBARS(6, 6))}</div>''' + tn('من «تمارين ومسائل عامة» ١ (ج، د). الأشرطة: ٦ مجموعات × ٦ أجزاء من عشرة = ٣٦ جزءاً = ٣٫٦.')))
S.append(slide(f'''{mode('u')}{timer(1)}''' + quiz('٢ × ٠٫٤ = ؟', [M('٨'), M('٠٫٨'), M('٠٫٠٨'), M('٢٫٤')], 1, '٢ × ٤ = ٨، ورقمٌ واحد يمين الفاصلة: ٠٫٨')))

# ═══ ٥ القسمة ═══
S.append(SEC(5, 'قسمة الأعداد العشرية', '٣-٥ و ٣-٦', ['قسمةٌ مختصرة والفاصلة فوق الفاصلة', 'عند الباقي نكمل بالأصفار ثم نقرّب']))
S.append(slide(f'''{RULE(5, 'نقسم قسمةً مختصرة والفاصلة في الناتج <b>فوق الفاصلة</b>، وعند وجود باقٍ نكمل بالأصفار ونحسب <b>منزلةً زائدة</b> ثم نقرّب')}
<div class="row vrow">{st(box(f'<div class="col"><span class="hint">٣٥٫١٥ ÷ ٥</span>{vdiv("35.15", "5")}</div>', style="flex:1"))}{st(box(f'<div class="col"><span class="hint">٩٦ ÷ ٧ لمنزلة واحدة</span>{vdiv("96.00", "7")}<span class="hint ok">١٣٫٧١ ≈ ١٣٫٧</span></div>', style="flex:1"))}</div>''' + tn('من «تمارين ومسائل عامة» ٢ (د) و ٣ (أ).')))
S.append(slide(f'''{mode('u')}{timer(2)}''' + quiz('٨٫٤٧ ÷ ٦ لأقرب منزلتين عشريتين', [M('١٫٤١'), M('١٫٤٢'), M('١٫٤'), M('١٤٫١')], 0, '٨٫٤٧٠ ÷ ٦ = ١٫٤١١ ≈ ١٫٤١')))

# ═══ ٦ قوى ١٠ و ٠٫١ و ٠٫٠١ ═══
S.append(SEC(6, 'قوى ١٠ والضرب في ٠٫١ و ٠٫٠١', '٣-٧', ['الأُس = عدد الأصفار يمين ١', '× ٠٫١ = ÷ ١٠ ، و ÷ ٠٫١ = × ١٠']))
S.append(slide(f'''{RULE(6, 'الأُس في قوى ١٠ = <b>عدد الأصفار</b>. والضرب في ٠٫١ أو ٠٫٠١ <b>قسمةٌ</b> على ١٠ أو ١٠٠، والقسمة عليهما <b>ضربٌ</b> في ١٠ أو ١٠٠')}
<div class="row vrow">{st(box(f'<div class="col"><span class="hint">٠٫١ عمودٌ من عشرة</span>{GRID100(1)}</div>'))}{STEPS(STP('١٠ أُس ٤', M('١٠٠٠٠', cls='sm')), STP('٤١ × ٠٫١', M('٤١ ÷ ١٠ = ٤٫١', cls='sm')), STP('٠٫٢٤ ÷ ٠٫٠١', M('٠٫٢٤ × ١٠٠ = ٢٤', cls='sm'), 'fin'))}</div>''' + tn('من «تمارين ومسائل عامة» ٥ و ٧.')))
S.append(slide(f'''{mode('u')}{timer(1)}''' + quiz('٧٫٢ ÷ ٠٫١ = ؟', [M('٠٫٧٢'), M('٧٢'), M('٧٢٠'), M('٧٫٢١')], 1, 'القسمة على ٠٫١ = الضرب في ١٠: ٧٢')))

# ═══ ٧ التقدير ═══
S.append(SEC(7, 'التقدير والتحقّق', '٣-٨', ['نقرّب كل عددٍ ونقدّر الناتج', 'أو نتحقّق بالعملية العكسية']))
S.append(slide(f'''{RULE(7, 'نتحقّق من الإجابة <b>بالتقدير</b> (نقرّب كل عدد) أو <b>بالعملية العكسية</b>')}
<div class="row vrow">{st(FIG('u3_gym', 'fig sm'))}{STEPS(STP('١٨ لشهر، ١٢ لشهرين، ١٥ لثلاثة', M('١٨ × ٢٥ + ١٢ × ٣٦ + ١٥ × ٤٢', cls='sm')), STP('المجموع', M('٤٥٠ + ٤٣٢ + ٦٣٠ = ١٥١٢', cls='sm'), 'fin'), STP('التقدير', M('٥٠٠ + ٤٠٠ + ٦٠٠ = ١٥٠٠', cls='sm')))}</div>''' + tn('من «تمارين ومسائل عامة» ١٣. التقدير كما في الدليل: ٢٠ × ٢٥ + ١٠ × ٤٠ + ١٥ × ٤٠ = ١٥٠٠.')))
S.append(slide(f'''{mode('u')}{timer(1)}''' + quiz('أفضل تحقّق من ٩٢٨ ÷ ٣٢ = ٢٩ هو…', [M('٢٩ × ٣٢'), M('٩٢٨ − ٣٢'), M('٢٩ + ٣٢'), M('٩٢٨ × ٣٢')], 0, 'الضرب يعكس القسمة: ٢٩ × ٣٢ = ٩٢٨ ✔')))

# ═══ «يجب أن تكون قادراً على» — تقييمٌ ذاتي ═══
SK = ['قراءة قوى العدد ١٠ للأعداد الصحيحة الموجبة وكتابتها', 'ضرب الأعداد الصحيحة والعشرية في ٠٫١ أو ٠٫٠١', 'ترتيب الأعداد العشرية والكسور العشرية',
      'تقريب الأعداد الكاملة إلى أقرب ١٠ أو ١٠٠ أو ١٠٠٠ …', 'تقريب الأعداد العشرية إلى أقرب عدد كامل أو منزلة أو منزلتين', 'جمع الأعداد العشرية وطرحها',
      'قسمة الأعداد العشرية على عددٍ من رقمٍ واحد حتى منزلةٍ محدّدة', 'استخدام التقدير والعمليات العكسية للتحقّق من صحة الحل', 'عرض الحل بشكلٍ واضح ودقيق']
def CHECK(items, start):
    return ''.join(f'<button class="ck"><span class="cb">{a(start + i)}</span><span>{t}</span></button>' for i, t in enumerate(items))
CKJS = "<script>document.querySelectorAll('.ck').forEach(function(b){b.onclick=function(e){e.stopPropagation();b.classList.toggle('ok');};});</script>"
for k in range(0, len(SK), 3):
    last = k + 3 >= len(SK)
    S.append(slide(f'''<div class="row hdr"><span class="qbadge">تقييمٌ ذاتي ✅</span><span class="tag">اضغط على ما تتقنه ليصبح أخضر</span></div><h2>يجب أن أكون قادراً على… ({a(k // 3 + 1)})</h2>
<div class="cks">{CHECK(SK[k:k+3], k + 1)}</div>{CKJS if last else ''}'''))
S.append(slide(f'''<h2>أحسنتم! 🎉</h2>
<div class="note">راجعوا ورقة ملخّص الوحدة، وحلّوا «تمارين ومسائل عامة» ص ٧٧ و ٧٨</div>
<p class="hint st">المرجع: كتاب الطالب، صفحة ملخّص الوحدة الثالثة · إعداد: أ. عيسى الحارثي</p>'''))

# ═══ ملحق: «تمارين ومسائل عامة» ص٧٧–٧٨ (الإجابات من دليل المعلم ص٨٠) ═══
S.append(launch('sb', '٧٧ و ٧٨', note='تمارين ومسائل عامة: الإجابات من دليل المعلم ص ٨٠ (مع تصحيح ٢ (ج) و ٨ (أ) و ١٠ (ب))'))
H = ['أ', 'ب', 'ج', 'د', 'هـ', 'و']
def L(items): return [(f'({h}) {q}', r) for h, (q, r) in zip(H, items)]
S.append(ex(1, 'احسب ذهنياً', 'نتجاهل الفاصلة ونضرب، ثم نعيدها', L([('٦ × ٠٫١', '٠٫٦'), ('٢ × ٠٫٤', '٠٫٨'), ('٦ × ٠٫٦', '٣٫٦'), ('٥ × ٠٫٩', '٤٫٥')]), cols=2))
S.append(ex(2, 'أوجد الناتج', 'قسمةٌ مختصرة والفاصلة فوق الفاصلة', [('(أ) ٢٤ ÷ ٢', vdiv('24', '2')), ('(ب) ٤٫٢ ÷ ٦', vdiv('4.2', '6')), ('(ج) ٨٫٧٤ ÷ ٣٨', '٠٫٢٣<small>الدليل كتب ٠٫٢٥؛ والقسمة على عددٍ من رقمين خارج الوحدة</small>'), ('(د) ٣٥٫١٥ ÷ ٥', vdiv('35.15', '5'))], cols=2,
  note='في ٢ (ج) طُبع في الكتاب ٨٫٧٤ ÷ ٣٨ (= ٠٫٢٣ تقريباً)، بينما إجابة الدليل ٠٫٢٥؛ والأرجح خطأٌ مطبعي، والقسمة على عددٍ من رقمين ليست من الوحدة.'))
S.append(ex(3, 'لأقرب منزلة عشرية واحدة', 'نحسب منزلتين ثم نقرّب', [('(أ) ٩٦ ÷ ٧', vdiv('96.00', '7') + '<small>١٣٫٧١ ≈ ١٣٫٧</small>'), ('(ب) ٢٧٨ ÷ ٣', vdiv('278.00', '3') + '<small>٩٢٫٦٦ ≈ ٩٢٫٧</small>')], cols=2))
S.append(ex(4, 'لأقرب منزلتين عشريتين', 'نحسب ثلاث منازل ثم نقرّب', [('(أ) ٨٫٤٧ ÷ ٦', vdiv('8.470', '6') + '<small>١٫٤١١ ≈ ١٫٤١</small>'), ('(ب) ٨٫٧ ÷ ٩', vdiv('8.700', '9') + '<small>٠٫٩٦٦ ≈ ٠٫٩٧</small>')], cols=2))
S.append(ex(5, 'اكتب ١٠ أُس ٤', 'الأُس = عدد الأصفار يمين ١', [('(أ) بالأعداد', '١٠٠٠٠'), ('(ب) بالكلمات', 'عشرة آلاف')], cols=2))
S.append(ex(6, 'اكتب ١٠٠٠٠٠٠٠٠ بقوى العدد ١٠', 'نعدّ الأصفار', [('١٠٠٠٠٠٠٠٠', P('10', 8))], cols=1))
S.append(ex(7, 'أوجد الناتج', '× ٠٫١ = ÷ ١٠ ، و ÷ ٠٫٠١ = × ١٠٠', L([('٤١ × ٠٫١', '٤٫١'), ('٢٣ × ٠٫٠١', '٠٫٢٣'), ('٧٫٢ ÷ ٠٫١', '٧٢'), ('٠٫٢٤ ÷ ٠٫٠١', '٢٤')]), cols=2))
S.append(ex(8, 'رتّب تصاعدياً', 'نوحّد الوحدات أولاً', [('(أ) ١٠٫٩ سم ، ١٠٫٩٨ م ، ١٠٫٨ م ، ١٠٫٠٩ سم', '١٠٫٠٩ سم ، ١٠٫٩ سم ، ١٠٫٨ م ، ١٠٫٩٨ م<small>الدليل رتّبها دون الوحدات</small>'), ('(ب) ٧ م ، ٧٥٠ سم ، ٠٫٧ م ، ٧٧ سم', '٠٫٧ م ، ٧٧ سم ، ٧ م ، ٧٥٠ سم')], cols=1,
  note='في إجابة الدليل ٨ (أ) «١٠٫٠٩ ، ١٠٫٨ ، ١٠٫٩ ، ١٠٫٩٨» رُتّبت الأعداد دون الوحدات؛ والصحيح أن السنتيمترات أصغر: ١٠٫٠٩ سم ، ١٠٫٩ سم ، ١٠٫٨ م ، ١٠٫٩٨ م.'))
S.append(ex(9, 'ضع &lt; أو &gt;', 'نقارن منزلةً منزلة، ونوحّد الوحدات', L([('٣٫٦٥ ☐ ٣٫٥٦', '&gt;'), ('٩٫٠١ ☐ ٩٫١', '&lt;'), ('٤٢ ملم ☐ ٠٫٥ سم', '&gt;<small>٠٫٥ سم = ٥ ملم</small>')]), cols=1, per=3))
S.append(ex(10, 'ضع = أو ≠', 'نحوّل إلى الوحدة نفسها', L([('٣٫٠٥ كغم ☐ ٣٠٠٥ غم', '≠<small>٣٫٠٥ كغم = ٣٠٥٠ غم</small>'), ('٠٫٦٧١ لتر ☐ ٦٧٠ مل', '≠<small>٠٫٦٧١ لتر = ٦٧١ مل؛ الدليل كتب =</small>'), ('٠٫٣ كم ☐ ٣٠ م', '≠<small>٠٫٣ كم = ٣٠٠ م</small>')]), cols=1, per=3,
  note='في إجابة الدليل ١٠ (ب) «=»، والصحيح ≠ لأن ٠٫٦٧١ لتر = ٦٧١ مل لا ٦٧٠ مل.'))
S.append(ex(11, 'قرّب إلى درجة الدقّة المحدّدة', 'رقم المنزلة والرقم على يمينها', L([('٦٧٢٥ (أقرب ١٠٠)', '٦٧٠٠'), ('٢٣٥٨٩٠ (أقرب ١٠٠٠٠)', '٢٤٠٠٠٠'), ('٨٢١٦٨٩٩ (أقرب مليون)', '٨٠٠٠٠٠٠'), ('٦٣٫٨١ (أقرب عدد كامل)', '٦٤'), ('١٢٫٦٢ (منزلة عشرية)', '١٢٫٦'), ('٧٫٥٦٦ (منزلتان)', '٧٫٥٧')]), cols=2))
S.append(ex(12, 'رمي القرص: ٢٧٫٢٩ م و ٢٩٫٧٣ م', 'الفواصل على خطٍّ واحد', [('(أ) مجموع المسافتين', vcol('27.29', '29.73', '+') + '<small>٥٧٫٠٢ م</small>'), ('(ب) الفرق بينهما', vcol('29.73', '27.29', '-') + '<small>٢٫٤٤ م</small>')], cols=2))
S.append(ex(13, 'صالة سالم الرياضية', 'نحسب ثم نتحقّق بالتقدير', [(FIG('u3_gym', 'fig side') + '١٨ شخصاً لشهر، و ١٢ لشهرين، و ١٥ لثلاثة أشهر: كم يدفعون؟', '٤٥٠ + ٤٣٢ + ٦٣٠ = ١٥١٢ ريالاً<small>التقدير: ٥٠٠ + ٤٠٠ + ٦٠٠ = ١٥٠٠</small>')], cols=1))

EXTRA_CSS_OWN = '''
.stps{display:flex;flex-direction:column;gap:1.2vh;align-items:stretch}
.stp{display:flex;align-items:center;gap:1.4vw;justify-content:space-between}
.stp .lab{flex:0 1 auto;max-width:55%;font-family:var(--fh);font-weight:800;color:#2563EB;background:#EAF1FF;border-radius:12px;padding:.2em .8em;text-align:center;line-height:1.4;font-size:clamp(20px,3.5vh,40px)}
.stp.fin .lab{background:var(--good);color:#fff}
.slide .vrow{align-items:center;justify-content:center;gap:2vh 3vw;flex-wrap:wrap}
.slide .vrow>.stps{flex:0 1 auto;max-width:min(1200px,80vw)}
@media (max-aspect-ratio:1/1){.slide .vrow{flex-direction:column}.slide .vrow>.stps{max-width:92vw}.stp{flex-wrap:wrap;justify-content:center}}
.vbox{flex:none;background:#fff;border:3px solid var(--line);border-radius:18px;padding:1vh 2vw;font-family:var(--fh);font-size:clamp(40px,8vh,92px)}
.box .col .vcol{font-family:var(--fh);font-size:clamp(32px,6vh,70px)}
.box .col>.m:not(.mid):not(.sm):not(.big){font-size:clamp(34px,6.4vh,76px)}
.hint.ok{color:var(--good)}
.rulecard{display:flex;align-items:center;gap:1em;background:#fff;border:3px solid var(--ink);border-radius:20px;padding:1.4vh 1.6vw;width:min(1300px,92vw);font-weight:700;font-size:clamp(22px,4vh,46px);line-height:1.5;box-shadow:0 7px 0 #DCE5F0}
.rulecard .rn{flex:none;font-family:var(--fh);font-weight:900;background:var(--ink);color:#fff;border-radius:14px;padding:.2em .7em;font-size:.8em}
.can.c2{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1.4vh 2vw;width:min(1400px,92vw)}
.cks{display:flex;flex-direction:column;gap:1.2vh;width:min(1300px,92vw)}
.ck{display:flex;align-items:center;gap:1em;text-align:start;font-family:var(--fb);font-weight:700;font-size:clamp(24px,4.4vh,50px);background:#fff;border:2.5px solid var(--line);border-radius:14px;padding:1vh 1.4vw;cursor:pointer;color:var(--ink);line-height:1.4}
.ck .cb{flex:none;width:1.6em;height:1.6em;border-radius:50%;background:#EEF2F7;display:flex;align-items:center;justify-content:center;font-family:var(--fh)}
.ck.ok{border-color:var(--good);background:#F2FBF5}.ck.ok .cb{background:var(--good);color:#fff}
.xa .vcol{font-family:var(--fh);font-size:1.05em;margin:0 .3em;color:var(--ink)}
.xa small{display:block}
''' + FIG_CSS

# صفحات تمارين كتاب الطالب لشارة «كتاب الطالب ص … · تمرين …» (common_slides.py)
PG = {'تمرين': [(1, '٧٧'), (12, '٧٨')]}
