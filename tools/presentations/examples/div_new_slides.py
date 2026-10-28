# شرائح درس ٣-٥ «قسمة الأعداد العشرية والكسور العشرية (١)» — الصف السابع (حصتان، كتاب الطالب ص٦٦–٦٧)
# المراجع: دليل المعلم ص٧١ (مهارة قسمة الأعداد الكاملة أولاً، الفواصل محاذاةٌ رأسياً، الخطأ الشائع: نسيان الفاصلة في الناتج؛
# النشاط: أسئلةٌ لفظية لقسمة ٦٫٣ ÷ ٣؛ التمرينان ٣ و ٤ بخطوات مثال ٣-٥، والتمرين ٥ بالمنطق لا بالتخمين)،
# كتاب الطالب ص٦٦–٦٧ (مثال ٣-٥)، وإجابات الدليل ص٧٨ (كتاب الطالب) وص٨٢ (كتاب النشاط ص٤٨–٤٩).
# نسخة تجريبية بطريقة تدريس جديدة (طلب الأستاذ عيسى، ٢٨ أكتوبر): ابدأ فوراً، مثال وتوأمه، سؤال المفصل، تدريب بالمستويات.
# python3.12 gen_powers.py div_new_slides.py قسمة_الأعداد_العشرية_تجريبي_عرض_تفاعلي.html "قسمة الأعداد العشرية والكسور العشرية (١) — الصف السابع"
# الوحدة الثالثة (طلب الأستاذ عيسى): الخط أصغر بنسبة ١٠٪، والأعداد في القوائم كلٌّ في مربّعه بلا «،» (gen_powers.py)
NUM_CHIPS = True
NO_AUTO_INTERACT = True   # تجربة مرفوضة؛ تبقى كما جُرّبت
EXTRA_CSS_LAST = 'html:root{--ui:calc(.70 * .8)} .q .ch{font-size:clamp(34px,7vh,84px)}'
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
<p class="lead">حصتان: ابدأ فوراً ← مثالٌ وتوأمه ← سؤال المفصل ← تدريبٌ بالمستويات</p>'''))

# ═══════════ طريقة الحصة التجريبية (طلب الأستاذ عيسى، ٢٨ أكتوبر) ═══════════
# ابدأ فوراً ← مثالٌ وتوأمه (أنا ثم أنتم مباشرةً على الألواح) ← سؤال المفصل ← تدريبٌ بثلاثة مستويات مع تصحيحٍ ذاتي ← بطاقة الخروج.
# كل الطلاب يجيبون معاً على ألواحٍ صغيرة («أروني»)، ولا رفع أيدٍ: المعلّم يختار بالقرعة. لا وقت ضائع: أول دقيقة عمل، ومن ينهي مستواه ينتقل إلى التالي.
def PH(t): return f'<span class="qbadge ph">{t}</span>'
def DONOW(items, ans, src):
    lis = ''.join(st(f'<div><b>{_ar(i + 1)}</b>{q}</div>') for i, q in enumerate(items))
    al = ''.join(M(f'({_ar(i + 1)}) {x}', cls='sm') for i, x in enumerate(ans))
    return slide(f'''<div class="row hdr">{PH('ابدأ فوراً ⏱️')}{timer(3)}</div><h2>حلّ في دفترك قبل أن نبدأ</h2>
<div class="exit">{lis}</div>
<button class="flip box col"><span class="tap">👆 الإجابات</span><span class="hid row dnans">{al}</span></button>''' + tn(f'تبدأ الحصة بعملٍ من أول دقيقة: الأسئلة على الشاشة عند دخول الطلاب، والمعلّم يتفقّد الحضور والدفاتر أثناء الحل. {src}'))
def TWIN(q, a_, k, rf, extra=''):
    return slide(f'''<div class="row hdr">{mode('u')}{PH('أروني 🙋')}{ref(rf)}{timer(1)}</div><h2>دورك: المسألة التوأم</h2>
{extra}<div class="row">{st(f'<button class="flip box col" style="flex:1"><span class="hint">{q}</span><span class="tap">👆</span><span class="hid vfl">{vdiv(a_, k)}</span></button>')}</div>''' + tn('الكل يحلّ على اللوح الصغير (أو ورقة في كيسٍ شفاف) دقيقةً واحدة، ثم «٣، ٢، ١، أروني!» فيرفع الجميع ألواحهم معاً. انظر إلى الألواح لا إلى الأيدي، واختر طالباً بالقرعة ليشرح خطوته.'))
def HINGE(q, ch, ok, why, rf, mis):
    return slide(f'''<div class="row hdr">{PH('سؤال المفصل 🎯')}{ref(rf)}</div>''' + quiz(q, ch, ok, why) + tn('يرفع كل طالب أصابعه (١ إلى ٤) برقم الخيار معاً. إن أجاب ٨ من كل ١٠ صحيحاً فانتقل إلى التدريب، وإلا فأعد المثال بالنموذج. ما يكشفه كل خيار خاطئ: ' + mis))
def TIERS(rows, rf, note='أجبت سؤال المفصل صحيحاً؟ ابدأ من 🟡'):
    cols = ''.join(f'<div class="tier {c}"><b class="th">{h}</b>' + ''.join(f'<span class="ti">{x}</span>' for x in xs) + '</div>' for c, h, xs, _ in rows)
    return slide(f'''<div class="row hdr">{PH('تدريبٌ بالمستويات')}{timer(rows[0][3])}</div><h2>اختر مستواك وابدأ</h2>
{st(f'<div class="tiers">{cols}</div>')}
{st(f'<div class="note">{note} · أنهيت مستواك؟ انتقل إلى التالي</div>')}''' + tn('كل طالب يعمل في مستواه، والمعلّم يجلس مع مجموعة 🟢 (من أخطؤوا سؤال المفصل) يحلّ معهم خطوةً خطوة، والباقون يصحّحون بأنفسهم من الشريحة التالية. المصادر: ' + rf))
def TANS(rows):
    cols = ''.join(st(f'<button class="flip box col tier {c}" style="flex:1"><b class="th">{h}</b><span class="tap">👆</span><span class="hid col">' + ''.join(M(x, cls='sm') for x in xs) + '</span></button>') for c, h, xs in rows)
    return slide(f'''<div class="row hdr">{PH('صحّح بنفسك ✅')}</div><h2>الإجابات</h2><div class="row tansr">{cols}</div>''' + tn('يكشف المعلّم إجابات المستوى الذي انتهى منه أغلب طلابه، ومن أخطأ يعيد المسألة ويقارن خطواته بخطوات المثال.'))

# ═══════════ الحصة الأولى ═══════════
S.append(slide('''<span class="tag">الحصة الأولى · ٤٠ دقيقة</span><h2>القسمة المختصرة</h2>
<div class="plan"><div><b>٣ د</b>ابدأ فوراً</div><div><b>٤ د</b>نرى القسمة</div><div><b>٥ د</b>مثال ١ وتوأمه</div>
<div><b>٥ د</b>مثال ٢ وتوأمه</div><div><b>٣ د</b>سؤال المفصل</div><div><b>١٥ د</b>تدريبٌ بالمستويات</div><div><b>٥ د</b>بطاقة الخروج</div></div>''', 'divider'))
S.append(slide(f'''<span class="qbadge">كيف نعمل في حصتنا؟</span><h2>الكل يحلّ، والكل يجيب</h2>
<div class="exit">{st('<div><b>١</b>✍️ نحلّ كلّنا على اللوح الصغير</div>')}{st('<div><b>٢</b>🙋 عند «أروني» نرفع الألواح معاً</div>')}{st('<div><b>٣</b>🎯 بعد سؤال المفصل يختار كلٌّ مستواه</div>')}{st('<div><b>٤</b>✅ نصحّح بأنفسنا ثم ننتقل إلى المستوى التالي</div>')}</div>''' + tn('تُعرض في أول حصةٍ بالطريقة الجديدة فقط. جهّز لكل طالب لوحاً صغيراً وقلماً (أو ورقة A4 في كيسٍ شفاف). لا رفع أيدٍ للإجابة: من يُسأل يُختار بالقرعة من شريط الحصة.')))
S.append(DONOW(['٦٣ ÷ ٣', '٤٨٦ ÷ ٢', '٨٤ ÷ ٣'], ['٢١', '٢٤٣', '٢٨'], 'من الدليل ص ٧١: يجب إتقان قسمة الأعداد الكاملة قبل البدء. الأعداد من خارج المرجع، واختيرت لتطابق أمثلة الدرس (٤٫٨٦ ÷ ٢ و ٨٫٤ ÷ ٣).'))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('نشاط دليل المعلم')}</div><h2>قسم الأب ٦٫٣٠٠ ريالات على أبنائه الثلاثة</h2>
<div class="figrow">{st(SHARE(6, 3, 3, names=['👦 ١', '👦 ٢', '👦 ٣']))}{st('<div class="note">لكلٍّ منهم وحدتان وجزءٌ من عشرة<br>٦٫٣ ÷ ٣ = <b>٢٫١</b></div>')}</div>''' + tn('سؤال نشاط الدليل اللفظي مع نموذج التقسيم (رسمٌ من خارج المرجع: المربّع واحدٌ صحيح، والشريط جزءٌ من عشرة). اسأل: «كم ريالاً لكل ابن؟» ثم اكشف النموذج.')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('كتاب الطالب ص ٦٦')}</div><h2>لقسمة عددٍ عشري على عددٍ من رقمٍ واحد</h2>
<div class="defs">{st('<div><b class="kk c-exp">١</b><span>نستخدم <b class="c-exp">القسمة المختصرة</b> كما في الأعداد الكاملة</span></div>')}{st('<div><b class="kk c-we">٢</b><span>نكتب <b class="c-we">الفاصلة في الناتج فوق الفاصلة</b> في المقسوم تماماً</span></div>')}</div>'''))
S.append(slide(f'''<div class="row hdr">{mode('i')}{PH('مثال ١')}{ref('مثال ٣-٥ (أ)')}</div><h2>أوجد ناتج {Q('4.86', '2')}</h2>
<div class="row vrow">{STEPS(STP('الآحاد', M('٤', DV, '٢', EQ, '٢', cls='sm')), STP('الفاصلة في الناتج فوق الفاصلة'), STP('الأجزاء من عشرة', M('٨', DV, '٢', EQ, '٤', cls='sm')), STP('الأجزاء من مئة', M('٦', DV, '٢', EQ, '٣', cls='sm')), STP('الناتج', M('٢٫٤٣', cls='sm'), 'fin'))}
{VB(vdiv('4.86', '2', reveal=True))}</div>''' + tn('مثالٌ قصير بصوتٍ عالٍ (دقيقتان)، ثم التوأم فوراً. قارن بـ ٤٨٦ ÷ ٢ = ٢٤٣ من «ابدأ فوراً»: الفرق الوحيد الفاصلة.')))
S.append(TWIN(Q('8.26', '2'), '8.26', '2', 'تمرين ٢ (أ)'))
S.append(slide(f'''<div class="row hdr">{mode('i')}{PH('مثال ٢')}{ref('تمرين ١ (د)')}</div><h2>أوجد ناتج {Q('8.4', '3')}</h2>
<div class="row vrow">{STEPS(STP('الآحاد', M('٨', DV, '٣', EQ, '٢ والباقي ٢', cls='sm')), STP('الفاصلة في الناتج فوق الفاصلة'), STP('نكتب الباقي ٢ قبل ٤', M('٢٤', DV, '٣', EQ, '٨', cls='sm')), STP('الناتج', M('٢٫٨', cls='sm'), 'fin'))}
{VB(vdiv('8.4', '3', reveal=True))}</div>''' + tn('الجديد هنا: الباقي ينتقل إلى الرقم التالي (الرقم البرتقالي الصغير). التحقّق: ٢٫٨ × ٣ = ٨٫٤.')))
S.append(TWIN(Q('8.4', '6'), '8.4', '6', 'نشاط ص ٤٨ · تمرين ١ (و)'))
S.append(HINGE(f'{Q("9.36", "3")} = ؟', [M('٣١٢'), M('٣٫١٢'), M('٣١٫٢'), M('٠٫٣١٢')], 1, '٩ ÷ ٣ = ٣، والفاصلة فوق الفاصلة، ثم ٣ ÷ ٣ = ١ و ٦ ÷ ٣ = ٢: ٣٫١٢', 'نشاط ص ٤٨ · تمرين ٢ (أ)',
    '٣١٢ نسي الفاصلة (الخطأ الشائع في الدليل)، ٣١٫٢ وضعها في غير مكانها، ٠٫٣١٢ لم يقسم الآحاد.'))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">انتبه ⚠️ خطأ شائع</span>{ref('دليل المعلم ص ٧١')}</div><h2>لا ننسى الفاصلة في الناتج</h2>
<div class="row">{st(box('<div class="col"><span class="hint no">✘ نسينا الفاصلة</span>' + M('٤٫٨٦ ÷ ٢ = ٢٤٣') + '</div>', style="flex:1"))}{st(box('<div class="col"><span class="hint ok">✔ الفاصلة فوق الفاصلة</span>' + M('٤٫٨٦ ÷ ٢ = ٢٫٤٣') + '</div>', style="flex:1"))}</div>
{st('<div class="note">نتحقّق بالضرب: ٢٫٤٣ × ٢ = ٤٫٨٦ ✔</div>')}''' + tn('تُعرض فقط إن ظهر الخيار «٣١٢» على أكثر من لوحين في سؤال المفصل.')))
T1 = [('t1', '🟢 أساسي', ['٤٫٦ ÷ ٢', '٩٫٦ ÷ ٣', '٨٫٢ ÷ ٢', '٤٫٦٨ ÷ ٢'], 15),
      ('t2', '🟡 متوسط', ['١٨٫٦٦ ÷ ٦', '٨٫١٣ ÷ ٣', '٧٫٨٦ ÷ ٦', '٩٫٥١ ÷ ٣'], 15),
      ('t3', '🔴 تحدٍّ', ['٣٫٠٣ ÷ ٣', '٥٫١٥ ÷ ٥', 'اكتب سؤالاً من حياتك يُحلّ بـ ٦٫٣ ÷ ٣'], 15)]
S.append(TIERS(T1, '🟢 كتاب الطالب تمرين ١ (ب) ونشاط ص ٤٨ تمرين ١ (أ، ب) و ٢ (ب)؛ 🟡 كتاب الطالب تمرين ٢ (د) ونشاط ص ٤٨ تمرين ٢ (هـ، و) و ٣ (ب)؛ 🔴 نشاط ص ٤٨ تمرين ٢ (ج، د) وسؤال نشاط الدليل اللفظي. في 🔴 صفرٌ داخل الناتج (١٫٠١ و ١٫٠٣).'))
S.append(TANS([(c, h.split()[0], [f'{q} = {a_}' for q, a_ in zip(xs, A)]) for (c, h, xs, _), A in zip(T1, (['٢٫٣', '٣٫٢', '٤٫١', '٢٫٣٤'], ['٣٫١١', '٢٫٧١', '١٫٣١', '٣٫١٧'], ['١٫٠١', '١٫٠٣'])) ]))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ١ 🎫</span><h2>أوجد الناتج</h2>
<div class="exit">{st(f'<div><b>١</b>{Q("6.93", "3")}</div>')}{st(f'<div><b>٢</b>{Q("4.84", "4")}</div>')}{st(f'<div><b>٣</b>{Q("45.05", "5")}</div>')}</div>''' + tn('من كتاب الطالب تمرين ٢ (ب، ج، هـ). من يخطئ في سؤالين يبدأ الحصة القادمة مع المعلّم في 🟢.')))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ١ 🎫</span><h2>الإجابات</h2>
<button class="flip box col" style="min-width:40vw"><span class="tap">👆 اضغط لإظهار الإجابات</span><span class="hid col">{M('٢٫٣١', cls="sm")}{M('١٫٢١', cls="sm")}{M('٩٫٠١', cls="sm")}</span></button>'''))

# ═══════════ الحصة الثانية ═══════════
S.append(slide('''<span class="tag">الحصة الثانية · ٤٠ دقيقة</span><h2>القسمة مع الباقي ومسائل النقود</h2>
<div class="plan"><div><b>٣ د</b>ابدأ فوراً</div><div><b>٢ د</b>كم ثمن الكيلو؟</div><div><b>٥ د</b>مثال ١ وتوأمه</div><div><b>٥ د</b>مثال ٢ وتوأمه</div>
<div><b>٥ د</b>مثال ٣ وتوأمه</div><div><b>٣ د</b>سؤال المفصل</div><div><b>١٢ د</b>تدريبٌ بالمستويات</div><div><b>٥ د</b>بطاقة الخروج</div></div>''', 'divider'))
S.append(DONOW([Q('6.3', '3'), Q('8.26', '2'), Q('8.4', '6')], ['٢٫١', '٤٫١٣', '١٫٤'], 'استرجاعٌ لمسائل الحصة الأولى (مثال النموذج والتوأمين).'))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">موقف 🛒</span>{ref('تمرين ٣')}</div><h2>٥ كيلوغرام من اللحم بسعر ١٨٫٢٥٠ ريالاً</h2>
<div class="figrow">{FIG('3-5_meat', 'fig sm')}{st('<div class="note">قدّر: هل ثمن الكيلوغرام أقل من ٤ ريالات أم أكثر؟</div>')}</div>''' + tn('تقديرٌ سريع برفع الألواح: «أقل» أو «أكثر». التقدير: ٢٠ ÷ ٥ = ٤، والثمن أقل من ٢٠ فالكيلوغرام أقل من ٤ ريالات. نعود إلى الموقف ونحلّه في مثال ٣.')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{PH('مثال ١')}{ref('مثال ٣-٥ (ب)')}</div><h2>أوجد ناتج {Q('29.35', '5')}</h2>
<div class="row vrow">{STEPS(STP('٢ أصغر من ٥، فنقسم ٢٩', M('٢٩', DV, '٥', EQ, '٥ والباقي ٤', cls='sm')), STP('الفاصلة، ثم ٤٣ ÷ ٥', M('٨ والباقي ٣', cls='sm')), STP('٣٥ ÷ ٥', M('٧', cls='sm')), STP('الناتج', M('٥٫٨٧', cls='sm'), 'fin'))}
{VB(vdiv('29.35', '5', reveal=True))}</div>''' + tn('الباقي ينتقل إلى الرقم التالي كما في الكتاب. التحقّق بالتقدير: ٣٠ ÷ ٥ = ٦.')))
S.append(TWIN(Q('23.64', '6'), '23.64', '6', 'نشاط ص ٤٨ · تمرين ٣ (هـ)'))
S.append(slide(f'''<div class="row hdr">{mode('i')}{PH('مثال ٢')}{ref('تمرين ١ (ج)')}</div><h2>أوجد ناتج {Q('4.9', '7')}</h2>
<div class="row vrow">{STEPS(STP('٤ أصغر من ٧', M('٤', DV, '٧', EQ, '٠ والباقي ٤', cls='sm')), STP('نكتب ٠ في الناتج ثم الفاصلة'), STP('٤٩ ÷ ٧', M('٧', cls='sm')), STP('الناتج', M('٠٫٧', cls='sm'), 'fin'))}
{VB(vdiv('4.9', '7', reveal=True))}</div>''' + tn('الصفر في منزلة الآحاد ضروري: ٠٫٧ لا ٫٧. التحقّق: ٠٫٧ × ٧ = ٤٫٩.')))
S.append(TWIN(Q('6.4', '8'), '6.4', '8', 'نشاط ص ٤٨ · تمرين ١ (د)'))
S.append(slide(f'''<div class="row hdr">{mode('i')}{PH('مثال ٣')}{ref('تمرين ٣')}</div><h2>نعود إلى اللحم: ١٨٫٢٥٠ ÷ ٥</h2>
<div class="row vrow">{STEPS(STP('ثمن الكيلوغرام', M('١٨٫٢٥٠', DV, '٥', cls='sm')), STP('نقسم بخطوات المثال ١'), STP('الإجابة', M('٣٫٦٥٠ ريالاً', cls='sm'), 'fin'))}
{VB(vdiv('18.250', '5', reveal=True))}</div>''' + tn('من الدليل: في التمرينين ٣ و ٤ وجّه الطلاب إلى خطوات مثال ٣-٥. قارن بالتقدير: ٣٫٦٥٠ أقل من ٤ ✔')))
S.append(TWIN('دفعت ليلى ٩٫٢٨٠ ريالات ثمن ٨ م من الشريط. كم ثمن المتر؟', '9.280', '8', 'تمرين ٤', extra=f'<div class="figrow">{FIG("3-5_ribbon", "fig sm")}</div>'))
S.append(HINGE(f'{Q("3.04", "4")} = ؟', [M('٧٦'), M('٠٫٧٦'), M('٧٫٦'), M('٠٫٠٧٦')], 1, '٣ أصغر من ٤ فنكتب ٠، ثم ٣٠ ÷ ٤ = ٧ والباقي ٢، و ٢٤ ÷ ٤ = ٦', 'نشاط ص ٤٨ · تمرين ٣ (ج)',
    '٧٦ نسي الفاصلة والصفر، ٧٫٦ لم يكتب صفر الآحاد فانزاحت الفاصلة، ٠٫٠٧٦ أضاف صفراً زائداً.'))
T2 = [('t1', '🟢 أساسي', ['٩٫١ ÷ ٧', '٥٫٧٨ ÷ ٢'], 12),
      ('t2', '🟡 متوسط', ['٢١٫٤٢ ÷ ٧', '٥ أكياس أسمنت بـ ٧٫٤٥٠ ريالات: كم ثمن الكيس؟'], 12),
      ('t3', '🔴 تحدٍّ', ['أكمل القسمة: كتاب الطالب تمرين ٥', 'كتاب النشاط ص ٤٩ تمرين ٦'], 12)]
S.append(TIERS(T2, '🟢 كتاب الطالب تمرين ١ (هـ) ونشاط ص ٤٨ تمرين ٣ (أ)؛ 🟡 نشاط ص ٤٨ تمرين ٣ (و) وص ٤٩ تمرين ٤؛ 🔴 ألغاز «أكمل القسمة» (من الدليل: بالمنطق لا بالتخمين). حلول ألغاز النشاط في ملحق كتاب النشاط.', note='أخطأت سؤال المفصل؟ ابدأ من 🟢 مع المعلّم'))
S.append(TANS([('t1', '🟢', ['٩٫١ ÷ ٧ = ١٫٣', '٥٫٧٨ ÷ ٢ = ٢٫٨٩']), ('t2', '🟡', ['٢١٫٤٢ ÷ ٧ = ٣٫٠٦', 'الكيس ١٫٤٩٠ ريال']), ('t3', '🔴', ['٦٫٣٨ ÷ ٢ = ٣٫١٩', '٧٫٩٥ ÷ ٣ = ٢٫٦٥', '٣٥٫٣٤ ÷ ٦ = ٥٫٨٩'])]))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ٢ 🎫</span><h2>أوجد الناتج</h2>
<div class="exit">{st(f'<div><b>١</b>{Q("7.2", "3")}</div>')}{st(f'<div><b>٢</b>{Q("2.8", "7")}</div>')}{st(f'<div><b>٣</b>{Q("19.15", "5")}</div>')}</div>''' + tn('من كتاب النشاط ص ٤٨ (١ هـ، ١ ج، ٣ د).')))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ٢ 🎫</span><h2>الإجابات</h2>
<button class="flip box col" style="min-width:40vw"><span class="tap">👆 اضغط لإظهار الإجابات</span><span class="hid col">{M('٢٫٤', cls="sm")}{M('٠٫٤', cls="sm")}{M('٣٫٨٣', cls="sm")}</span></button>'''))
S.append(slide('''<span class="qbadge" style="background:#0A6770;box-shadow:0 4px 0 #05393E">الواجب المنزلي 🏠</span><h2>بعد الحصتين</h2>
<div class="exit"><div class="st"><div><b>١</b>أكمل ما لم تحلّه من مستواك</div></div><div class="st"><div><b>٢</b>باقي تمارين كتاب النشاط ص ٤٨ و ٤٩</div></div></div>'''))
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
.qbadge.ph{background:#7C3AED;box-shadow:0 4px 0 #4C1D95}
.tiers{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1.6vw;width:min(1600px,94vw)}
.tier{display:flex;flex-direction:column;align-items:center;gap:1vh;background:#fff;border:4px solid var(--line);border-radius:18px;padding:1.2vh 1.2vw}
.tier .th{font-family:var(--fh);font-weight:900;font-size:clamp(28px,5.4vh,62px)}
.tier .ti{font-family:var(--fh);font-weight:800;font-size:clamp(26px,4.8vh,56px);text-align:center;line-height:1.4}
.tier.t1{border-color:#16A34A;background:#F0FDF4}.tier.t2{border-color:#CA8A04;background:#FEFCE8}.tier.t3{border-color:#DC2626;background:#FEF2F2}
.tansr{width:min(1600px,94vw)}
.dnans{gap:3vw;justify-content:center}
'''+FIG_CSS
