# شرائح درس ٣-٥ «قسمة الأعداد العشرية والكسور العشرية (١)» — الصف السابع (حصتان، كتاب الطالب ص٦٦–٦٧)
# المراجع: دليل المعلم ص٧١ (مهارة قسمة الأعداد الكاملة أولاً، الفواصل محاذاةٌ رأسياً، الخطأ الشائع: نسيان الفاصلة في الناتج؛
# النشاط: أسئلةٌ لفظية لقسمة ٦٫٣ ÷ ٣؛ التمرينان ٣ و ٤ بخطوات مثال ٣-٥، والتمرين ٥ بالمنطق لا بالتخمين)،
# كتاب الطالب ص٦٦–٦٧ (مثال ٣-٥)، وإجابات الدليل ص٧٨ (كتاب الطالب) وص٨٢ (كتاب النشاط ص٤٨–٤٩).
# python3.12 gen_powers.py div_slides.py قسمة_الأعداد_العشرية_عرض_تفاعلي.html "قسمة الأعداد العشرية والكسور العشرية (١) — الصف السابع"
exec(open(os.path.join(HERE, 'vcol.py'), encoding='utf-8').read())
exec(open(os.path.join(HERE, 'figs.py'), encoding='utf-8').read())

def STP(lab, expr='', cls=''): return st(f'<div class="stp {cls}"><span class="lab">{lab}</span>{expr}</div>')
def STEPS(*rows): return '<div class="stps">' + ''.join(rows) + '</div>'
DV = '<span class="x">÷</span>'
def VB(h): return f'<div class="vbox">{h}</div>'
def Q(a_, k): return f'{_ar(a_)} ÷ {_ar(k)}'
def PZ(q, dv, k):   # لغز القسمة: الأرقام الناقصة مربّعات (؟)
    TD = 'padding: 0 .07em; text-align: center; min-width: .6em'
    def cells(s, top):
        return ''.join(f'<td style="{TD}{"" if top else "; border-top: .07em solid currentColor"}{"; color: #C0262D" if c == "٫" else ""}">' + (f'<span class="bx">{c[1:]}</span>' if c.startswith('?') else c.replace('^', '<sup style="font-size: .6em; color: #C2410C">').replace('|', '</sup>')) + '</td>' for c in s)
    return (f'<table class="vcol" style="border-collapse: collapse; direction: ltr; display: inline-table; font-weight: 800; line-height: 1.2; margin: 0 auto">'
            f'<tr><td></td>{cells(q, True)}</tr><tr><td style="{TD}; border-right: .07em solid currentColor; padding-right: .18em">{k}</td>{cells(dv, False)}</tr></table>')
S = []
ME = 'إعداد: أ. عيسى الحارثي'
S.append(slide(f'''<span class="tag">الصف السابع · الدرس ٣-٥</span>
<h1 class="h1s">قسمة الأعداد العشرية والكسور العشرية (١)</h1>
<p class="lead">كتاب الطالب ص ٦٦ و ٦٧ · حصتان</p>
<p class="lead" style="font-size:clamp(26px,4.8vh,56px)">{ME}</p>''', 'cover'))
CAN = ['أقسم عدداً عشرياً على عددٍ من رقمٍ واحد <b>بالقسمة المختصرة</b>', 'أضع <b>الفاصلة في الناتج فوق الفاصلة</b> في المقسوم', 'أحلّ <b>مسائل</b> النقود والقياس بالقسمة']
S.append(slide(f'''<h2>في نهاية هذا الدرس…</h2>
<div class="can">{''.join(f'<div><span class="can-i">✔</span><span><b>أنا أستطيع</b> أن {t}</span></div>' for t in CAN)}</div>'''))
S.append(slide(f'''<h2>مفردات الدرس</h2>
{st('<div class="vocab wide"><div><span>القسمة المختصرة</span><i>short division</i></div><div><span>المقسوم</span><i>dividend</i></div><div><span>المقسوم عليه</span><i>divisor</i></div><div><span>الباقي</span><i>remainder</i></div></div>')}
<p class="lead">حصتان: <b class="c-i">أنا</b> ← <b class="c-we">نحن</b> ← <b class="c-u">أنتم</b></p>'''))

# ═══════════ الحصة الأولى ═══════════
S.append(slide('''<span class="tag">الحصة الأولى · ٤٠ دقيقة</span><h2>القسمة المختصرة</h2>
<div class="plan"><div><b>٥ د</b>تهيئة: قسمة أعداد كاملة</div><div><b>٥ د</b>القاعدة</div><div><b>٨ د</b>مثال ٣-٥ (أ)</div>
<div><b>٧ د</b>نحن</div><div><b>٨ د</b>أنتم</div><div><b>٤ د</b>انتبه</div><div><b>٣ د</b>بطاقة الخروج</div></div>''', 'divider'))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">تهيئة 🤔</span>{ref('دليل المعلم ص ٧١')}</div><h2>قسمة الأعداد الكاملة أولاً</h2>
<div class="row">{st(f'<button class="flip box col" style="flex:1"><span class="hint">٦٣ ÷ ٣</span><span class="tap">👆</span><span class="hid vfl">{vdiv("63", "3")}</span></button>')}{st(f'<button class="flip box col" style="flex:1"><span class="hint">٤٨٦ ÷ ٢</span><span class="tap">👆</span><span class="hid vfl">{vdiv("486", "2")}</span></button>')}</div>''' + tn('من الدليل: يجب أن يتقن الطلاب قسمة الأعداد الكاملة قبل البدء. العددان من خارج المرجع، واختيرا ليطابقا ٦٫٣ ÷ ٣ و ٤٫٨٦ ÷ ٢ بعد قليل.')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('كتاب الطالب ص ٦٦')}</div><h2>لقسمة عددٍ عشري على عددٍ من رقمٍ واحد</h2>
<div class="defs">{st('<div><b class="kk c-exp">١</b><span>نستخدم <b class="c-exp">القسمة المختصرة</b> كما في الأعداد الكاملة</span></div>')}{st('<div><b class="kk c-we">٢</b><span>نترك الفاصلة في المقسوم مكانها، ونكتب <b class="c-we">الفاصلة في الناتج فوقها تماماً</b></span></div>')}</div>'''))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('مثال ٣-٥ (أ)')}</div><h2>أوجد ناتج {Q('4.86', '2')}</h2>
<div class="row vrow">{STEPS(STP('الآحاد', M('٤', DV, '٢', EQ, '٢', cls='sm')), STP('نضع الفاصلة في الناتج فوق الفاصلة'), STP('الأجزاء من عشرة', M('٨', DV, '٢', EQ, '٤', cls='sm')), STP('الأجزاء من مئة', M('٦', DV, '٢', EQ, '٣', cls='sm')), STP('الناتج', M('٢٫٤٣', cls='sm'), 'fin'))}
{VB(vdiv('4.86', '2', reveal=True))}</div>''' + tn('قارن بالتهيئة: ٤٨٦ ÷ ٢ = ٢٤٣، والفرق الوحيد هو الفاصلة. التحقّق: ٢٫٤٣ × ٢ = ٤٫٨٦.')))
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('تمرين ١ (أ، ب)')}</div><h2>معاً: أوجد الناتج</h2>
<div class="row">{st(f'<button class="flip box col" style="flex:1"><span class="hint">{Q("6.3", "3")}</span><span class="tap">👆</span><span class="hid vfl">{vdiv("6.3", "3")}</span></button>')}{st(f'<button class="flip box col" style="flex:1"><span class="hint">{Q("4.6", "2")}</span><span class="tap">👆</span><span class="hid vfl">{vdiv("4.6", "2")}</span></button>')}</div>'''))
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('نشاط دليل المعلم')}</div><h2>٦٫٣ ÷ ٣ في الحياة</h2>
<div class="exit">{st('<div><b>١</b>قسم الأب ٦٫٣٠٠ ريالات على أبنائه الثلاثة بالتساوي</div>')}{st('<div><b>٢</b>حبلٌ طوله ٦٫٣ أمتار قُطع ثلاثة أجزاء متساوية</div>')}{st('<div><b>٣</b>كم مرةً يوجد العدد ٣ في ٦٫٣ ؟</div>')}</div>
{st('<div class="note">الجواب في كل مرة ٢٫١: ٢٫١٠٠ ريال، ٢٫١ م، ٢٫١ مرة</div>')}''' + tn('نشاط الدليل: ناقش مع الطلاب طرق صياغة أسئلةٍ لفظية لقسمة ٦٫٣ ÷ ٣، واطلب منهم صياغة سؤالٍ رابع.')))
S.append(slide(f'''<div class="row hdr">{mode('i')}<span class="qbadge">نموذج 🧩</span></div><h2>نرى القسمة: ٦٫٣ ÷ ٣</h2>
<div class="figrow">{st(SHARE(6, 3, 3, names=['👦 ١', '👦 ٢', '👦 ٣']))}{st('<div class="note">٦ وحدات و ٣ أجزاء من عشرة تُقسم على ٣:<br>لكلٍّ منهم وحدتان وجزءٌ من عشرة = <b>٢٫١</b></div>')}</div>''' + tn('رسمٌ من خارج المرجع: المربّع واحدٌ صحيح، والشريط الرفيع جزءٌ من عشرة. يوضّح لماذا ٦٫٣ ÷ ٣ = ٢٫١ قبل الخوارزمية.')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ١ (د)')}{timer(2)}</div>''' + quiz(f'{Q("8.4", "3")} = ؟', [M('٢٨'), M('٢٫٨'), M('٠٫٢٨'), M('٢٫٤')], 1, '٨ ÷ ٣ = ٢ والباقي ٢، فنقسم ٢٤ ÷ ٣ = ٨: ٢٫٨')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ٢ (أ)')}</div>''' + quiz(f'{Q("8.26", "2")} = ؟', [M('٤١٫٣'), M('٤٫١٣'), M('٤٫٣١'), M('٠٫٤١٣')], 1, '٨ ÷ ٢ = ٤، ٢ ÷ ٢ = ١، ٦ ÷ ٢ = ٣: ٤٫١٣')))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">انتبه ⚠️ خطأ شائع</span>{ref('دليل المعلم ص ٧١')}</div><h2>لا ننسى الفاصلة في الناتج</h2>
<div class="row">{st(box('<div class="col"><span class="hint no">✘ نسينا الفاصلة</span>' + M('٤٫٨٦ ÷ ٢ = ٢٤٣') + '</div>', style="flex:1"))}{st(box('<div class="col"><span class="hint ok">✔ الفاصلة فوق الفاصلة</span>' + M('٤٫٨٦ ÷ ٢ = ٢٫٤٣') + '</div>', style="flex:1"))}</div>
{st('<div class="note">تحقّق بالضرب: ٢٫٤٣ × ٢ = ٤٫٨٦ ✔ أما ٢٤٣ × ٢ = ٤٨٦</div>')}'''))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ١ 🎫</span><h2>أوجد الناتج</h2>
<div class="exit">{st(f'<div><b>١</b>{Q("6.93", "3")}</div>')}{st(f'<div><b>٢</b>{Q("4.84", "4")}</div>')}{st(f'<div><b>٣</b>{Q("45.05", "5")}</div>')}</div>'''))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ١ 🎫</span><h2>الإجابات</h2>
<button class="flip box col" style="min-width:40vw"><span class="tap">👆 اضغط لإظهار الإجابات</span><span class="hid col">{M('٢٫٣١', cls="sm")}{M('١٫٢١', cls="sm")}{M('٩٫٠١', cls="sm")}</span></button>'''))

# ═══════════ الحصة الثانية ═══════════
S.append(slide('''<span class="tag">الحصة الثانية · ٤٠ دقيقة</span><h2>القسمة مع الباقي</h2>
<div class="plan"><div><b>٣ د</b>إحماء</div><div><b>٨ د</b>مثال ٣-٥ (ب)</div><div><b>٥ د</b>رقمٌ أصغر من المقسوم عليه</div>
<div><b>٥ د</b>نحن</div><div><b>٥ د</b>أنتم</div><div><b>٦ د</b>مسألتا النقود</div><div><b>٥ د</b>أكمل القسمة</div><div><b>٣ د</b>بطاقة الخروج</div></div>''', 'divider'))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">إحماء 🔥</span>{timer(1)}</div>''' + quiz(f'{Q("6.3", "3")} = ؟', [M('٢٫١'), M('٢١'), M('٠٫٢١'), M('٣٫١')], 0, '٦ ÷ ٣ = ٢، و ٣ ÷ ٣ = ١، والفاصلة فوق الفاصلة')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('مثال ٣-٥ (ب)')}</div><h2>أوجد ناتج {Q('29.35', '5')}</h2>
<div class="row vrow">{STEPS(STP('٢ أصغر من ٥، فنقسم ٢٩', M('٢٩', DV, '٥', EQ, '٥ والباقي ٤', cls='sm')), STP('نكتب الباقي ٤ يسار ٣، ونضع الفاصلة'), STP('٤٣ ÷ ٥', M('٨ والباقي ٣', cls='sm')), STP('٣٥ ÷ ٥', M('٧ والباقي ٠', cls='sm')), STP('الناتج', M('٥٫٨٧', cls='sm'), 'fin'))}
{VB(vdiv('29.35', '5', reveal=True))}</div>''' + tn('الأرقام البرتقالية الصغيرة هي الباقي ينتقل إلى الرقم التالي (كما في الكتاب). التحقّق بالتقدير: ٣٠ ÷ ٥ = ٦.')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('تمرين ١ (ج)')}</div><h2>أوجد ناتج {Q('4.9', '7')}</h2>
<div class="row vrow">{STEPS(STP('٤ أصغر من ٧', M('٤', DV, '٧', EQ, '٠ والباقي ٤', cls='sm')), STP('نكتب ٠ في الناتج ثم الفاصلة'), STP('٤٩ ÷ ٧', M('٧', cls='sm')), STP('الناتج', M('٠٫٧', cls='sm'), 'fin'))}
{VB(vdiv('4.9', '7', reveal=True))}</div>''' + tn('الصفر في منزلة الآحاد ضروري: ٠٫٧ لا ٫٧. التحقّق: ٠٫٧ × ٧ = ٤٫٩.')))
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('تمرين ١ (هـ)، تمرين ٢ (د)')}</div><h2>معاً: أوجد الناتج</h2>
<div class="row">{st(f'<button class="flip box col" style="flex:1"><span class="hint">{Q("9.1", "7")}</span><span class="tap">👆</span><span class="hid vfl">{vdiv("9.1", "7")}</span></button>')}{st(f'<button class="flip box col" style="flex:1"><span class="hint">{Q("18.66", "6")}</span><span class="tap">👆</span><span class="hid vfl">{vdiv("18.66", "6")}</span></button>')}</div>''' + tn('في ١٨٫٦٦ ÷ ٦: ١ أصغر من ٦ فنقسم ١٨، ثم ٦ ÷ ٦ = ١ و ٦ ÷ ٦ = ١: ٣٫١١.')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('نشاط ص ٤٨ · تمرين ٣ (أ)')}{timer(2)}</div>''' + quiz(f'{Q("5.78", "2")} = ؟', [M('٢٫٨٩'), M('٢٫٣٩'), M('٢٨٫٩'), M('٣٫٨٩')], 0, '٥ ÷ ٢ = ٢ والباقي ١، ١٧ ÷ ٢ = ٨ والباقي ١، ١٨ ÷ ٢ = ٩')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('نشاط ص ٤٨ · تمرين ٣ (ج)')}</div>''' + quiz(f'{Q("3.04", "4")} = ؟', [M('٧٦'), M('٠٫٧٦'), M('٧٫٦'), M('٠٫٠٧٦')], 1, '٣ أصغر من ٤ فنكتب ٠، ثم ٣٠ ÷ ٤ = ٧ والباقي ٢، و ٢٤ ÷ ٤ = ٦')))
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('تمرين ٣')}</div><h2>٥ كيلوغرام من اللحم بسعر ١٨٫٢٥٠ ريالاً</h2>
<div class="row vrow">{STEPS(STP('ثمن الكيلوغرام', M('١٨٫٢٥٠', DV, '٥', cls='sm')), STP('نقسم بخطوات مثال ٣-٥'), STP('الإجابة', M('٣٫٦٥٠ ريالاً', cls='sm'), 'fin'))}
{VB(vdiv('18.250', '5', reveal=True))}{FIG('3-5_meat', 'fig sm')}</div>''' + tn('من الدليل: في التمرينين ٣ و ٤ وجّه الطلاب إلى اتباع خطوات مثال ٣-٥. ٣٫٦٥٠ ريالاً = ٣ ريالات و ٦٥٠ بيسة.')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ٤')}{timer(3)}</div><div class="figrow">{FIG('3-5_ribbon', 'fig sm')}</div>''' + quiz('دفعت ليلى ٩٫٢٨٠ ريالات ثمن ٨ م من الشريط. كم ثمن المتر؟', [M('١٫١٦٠ ريال'), M('١١٫٦٠ ريالاً'), M('١٫٢٦٠ ريال'), M('٠٫١١٦ ريال')], 0, '٩٫٢٨٠ ÷ ٨ = ١٫١٦٠ ريال')))
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('تمرين ٥')}</div><h2>أكمل عمليات القسمة</h2>
<div class="row pzr">{''.join(st(f'<button class="flip box col" style="flex:1"><span class="hint">({h})</span>{p_}<span class="tap">👆</span><span class="hid vfl">{s_}</span></button>') for h, p_, s_ in (
  ('أ', PZ(['?', '٫', '١', '?'], ['٦', '٫', '?', '^١|٨'], '٢'), vdiv('6.38', '2')),
  ('ب', PZ(['٢', '٫', '?', '٥'], ['?', '٫', '^١|٩', '?'], '٣'), vdiv('7.95', '3')),
  ('ج', PZ(['', '٥', '٫', '?', '٩'], ['٣', '٥', '٫', '^٥|٣', '?'], '<span class="bx"></span>'), vdiv('35.34', '6'))))}</div>''' + tn('من الدليل: يساعد هذا النوع على التفكير المنطقي بدلاً من المحاولة والخطأ. في (ج): ٣٥ ÷ ؟ = ٥ والباقي ٥، إذن المقسوم عليه ٦.')))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ٢ 🎫</span><h2>أوجد الناتج</h2>
<div class="exit">{st(f'<div><b>١</b>{Q("7.2", "3")}</div>')}{st(f'<div><b>٢</b>{Q("2.8", "7")}</div>')}{st(f'<div><b>٣</b>{Q("19.15", "5")}</div>')}</div>''' + tn('من كتاب النشاط ص ٤٨ (١ هـ، ١ ج، ٣ د).')))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ٢ 🎫</span><h2>الإجابات</h2>
<button class="flip box col" style="min-width:40vw"><span class="tap">👆 اضغط لإظهار الإجابات</span><span class="hid col">{M('٢٫٤', cls="sm")}{M('٠٫٤', cls="sm")}{M('٣٫٨٣', cls="sm")}</span></button>'''))
S.append(slide('''<span class="qbadge" style="background:#0A6770;box-shadow:0 4px 0 #05393E">الواجب المنزلي 🏠</span><h2>بعد الحصتين</h2>
<div class="exit"><div class="st"><div><b>١</b>صفحة ٤٨ في كتاب النشاط (القسمة المختصرة)</div></div><div class="st"><div><b>٢</b>صفحة ٤٩ في كتاب النشاط (مسألتان، وأكمل القسمة)</div></div></div>'''))
S.append(slide(f'''<h2>الخلاصة</h2>
<div class="sumg">
{st(box('<div class="col"><b class="kk c-exp">مختصرة</b><span>نقسم كالأعداد الكاملة</span></div>'))}
{st(box('<div class="col"><b class="kk c-we">الفاصلة</b><span>في الناتج فوق الفاصلة</span></div>'))}
{st(box('<div class="col"><b class="kk c-lcm">التحقّق</b><span>الناتج × المقسوم عليه = المقسوم</span></div>'))}</div>'''))

# ═══════════ ملحق: تمارين كتاب الطالب ص٦٧ (الإجابات من دليل المعلم ص٧٨) ═══════════
S.append(launch('sb', '٦٧', note=f'المراجع: كتاب الطالب ص٦٦ و ٦٧، ودليل المعلم ص٧١ وإجاباته ص٧٨ · {ME}'))
H = ['أ', 'ب', 'ج', 'د', 'هـ', 'و']
RD = 'قسمةٌ مختصرة، والفاصلة في الناتج فوق الفاصلة في المقسوم'
def DX(lst): return [(f'({h}) {Q(x, k)}', vdiv(x, k)) for h, (x, k) in zip(H, lst)]
S.append(ex(1, 'أوجد ناتج القسمة', RD, DX([('6.3', '3'), ('4.6', '2'), ('4.9', '7'), ('8.4', '3'), ('9.1', '7')]), cols=2))
S.append(ex(2, 'أوجد ناتج القسمة', RD, DX([('8.26', '2'), ('6.93', '3'), ('4.84', '4'), ('18.66', '6'), ('45.05', '5')]), cols=2))
S.append(ex(3, 'ثمن الكيلوغرام', 'نقسم الثمن على عدد الكيلوغرامات', [(FIG('3-5_meat') + '٥ كيلوغرام من اللحم بسعر ١٨٫٢٥٠ ريالاً: ما ثمن الكيلوغرام؟', vdiv('18.250', '5') + '<small>٣٫٦٥٠ ريالاً</small>')], cols=1))
S.append(ex(4, 'ثمن المتر', 'نقسم الثمن على عدد الأمتار', [(FIG('3-5_ribbon') + 'دفعت ليلى ٩٫٢٨٠ ريالات ثمن ٨ م من الشريط: ما ثمن المتر؟', vdiv('9.280', '8') + '<small>١٫١٦٠ ريال</small>')], cols=1))
S.append(ex(5, 'أكمل عمليات القسمة', 'نستنتج كل رقمٍ من الباقي المكتوب', [('(أ) ' + PZ(['?', '٫', '١', '?'], ['٦', '٫', '?', '^١|٨'], '٢'), vdiv('6.38', '2')), ('(ب) ' + PZ(['٢', '٫', '?', '٥'], ['?', '٫', '^١|٩', '?'], '٣'), vdiv('7.95', '3')), ('(ج) ' + PZ(['', '٥', '٫', '?', '٩'], ['٣', '٥', '٫', '^٥|٣', '?'], '<span class="bx"></span>'), vdiv('35.34', '6'))], cols=2))

# ═══════════ ملحق: حلول كتاب النشاط ص٤٨–٤٩ (الإجابات من دليل المعلم ص٨٢) ═══════════
S.append(launch('ab', '٤٨ و ٤٩', note='الإجابات النهائية من دليل المعلم ص ٨٢'))
NA, NB = 'نشاط ص ٤٨ · تمرين', 'نشاط ص ٤٩ · تمرين'
S.append(ex(1, 'أوجد الناتج', RD, DX([('9.6', '3'), ('8.2', '2'), ('2.8', '7'), ('6.4', '8'), ('7.2', '3'), ('8.4', '6')]), cols=2, src=NA))
S.append(ex(2, 'أوجد الناتج', RD, DX([('9.36', '3'), ('4.68', '2'), ('3.03', '3'), ('5.15', '5'), ('8.13', '3'), ('7.86', '6')]), cols=2, src=NA))
S.append(ex(3, 'أوجد الناتج', RD, DX([('5.78', '2'), ('9.51', '3'), ('3.04', '4'), ('19.15', '5'), ('23.64', '6'), ('21.42', '7')]), cols=2, src=NA))
S.append(ex(4, 'ثمن كيس الأسمنت', 'نقسم الثمن على عدد الأكياس', [(FIG('3-5_cement', 'fig side') + 'دفع كمال ٧٫٤٥٠ ريالات ثمن ٥ أكياس أسمنت: ما ثمن الكيس؟', vdiv('7.450', '5') + '<small>١٫٤٩٠ ريال</small>')], cols=1, src=NA))
S.append(ex(5, 'ثمن كيس الخرز', 'نقسم الثمن على عدد الأكياس', [(FIG('3-5_beads', 'fig side') + 'دفعت روان ٥٫٥٦٠ ريالات ثمن ٦ أكياس خرز: ما ثمن الكيس؟', '٥٫٥٦٠ ÷ ٦ ≈ ٠٫٩٢٧ ريال<small>القسمة لا تنتهي (٠٫٩٢٦٦…)؛ الدليل كتب ٠٫٩٢٦</small>')], cols=1, src=NB, note='القسمة هنا غير منتهية؛ قرّبها إلى ٣ منازل (أقرب بيسة): ٠٫٩٢٧ ريال، والدليل اقتطعها ٠٫٩٢٦.'))
S.append(ex(6, 'أكمل عمليات القسمة', 'نستنتج كل رقمٍ من الباقي المكتوب', [('(أ) ' + PZ(['?', '٫', '٢', '?'], ['٨', '٫', '?', '^١|٦'], '٢'), vdiv('8.56', '2')), ('(ب) ' + PZ(['١', '٫', '?', '٧'], ['?', '٫', '^١|٧', '?'], '٣'), vdiv('4.71', '3')), ('(ج) ' + PZ(['', '٥', '٫', '?', '٩'], ['٣', '٣', '٫', '^٣|٥', '?'], '<span class="bx"></span>'), vdiv('33.54', '6'))], cols=2, src=NB))

EXTRA_CSS_OWN = '''
.stps{display:flex;flex-direction:column;gap:1.1vh;align-items:stretch}
.stp{display:flex;align-items:center;gap:1.4vw;justify-content:space-between}
.stp .lab{flex:0 1 auto;max-width:70%;font-family:var(--fh);font-weight:800;color:#2563EB;background:#EAF1FF;border-radius:12px;padding:.2em .8em;text-align:center;line-height:1.4;font-size:clamp(20px,3.6vh,40px)}
.stp.fin .lab{background:var(--good);color:#fff}
.slide .vrow{align-items:center;justify-content:center;gap:2vh 3vw;flex-wrap:wrap}
.slide .vrow>.stps{flex:0 1 auto;max-width:min(1000px,62vw)}
@media (max-aspect-ratio:1/1){.slide .vrow{flex-direction:column}.slide .vrow>.stps{max-width:92vw}}
.vbox{flex:none;background:#fff;border:3px solid var(--line);border-radius:18px;padding:1vh 2vw;font-family:var(--fh);font-size:clamp(48px,9.6vh,110px)}
.hid.vfl{font-family:var(--fh);font-size:clamp(36px,6.8vh,80px)}
.pzr .vcol{font-family:var(--fh);font-size:clamp(30px,5.6vh,64px)}
.bx{display:inline-block;width:.62em;height:.9em;border:.07em solid #C0262D;border-radius:.1em;vertical-align:middle}
.box .col>.m:not(.mid):not(.sm):not(.big),.hid.col>.m:not(.mid):not(.sm):not(.big){font-size:clamp(32px,6vh,70px)}
.hint.no{color:var(--bad)}.hint.ok{color:var(--good)}
.defs{display:flex;flex-direction:column;gap:1.6vh;width:min(1400px,92vw)}
.defs .st>div{display:flex;align-items:center;gap:1.6vw;background:#fff;border:3px solid var(--line);border-radius:18px;padding:1.2vh 1.6vw}
.defs .kk{flex:none;font-size:clamp(36px,6.8vh,80px)}.defs span{font-weight:700;font-size:clamp(26px,4.8vh,56px);line-height:1.45}
.sumg{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:2vw;width:min(1600px,94vw)}
.sumg .col span{font-weight:700;font-size:clamp(26px,4.6vh,56px);line-height:1.4}
.sumg .kk{font-size:clamp(34px,6.4vh,76px)}
.xa .vcol{font-family:var(--fh);font-size:1.05em;margin:0 .3em;color:var(--ink)}
.xa small{display:block}
.xq .vcol{font-family:var(--fh);font-size:1.1em}
'''+FIG_CSS
