# شرائح درس ٣-٤ «ضرب الأعداد العشرية والكسور العشرية» — الصف السابع (حصتان، كتاب الطالب ص٦٤–٦٥)
# المراجع: دليل المعلم ص٦٩–٧٠ (تجاهل الفاصلة ثم إعادتها، عدّ الأرقام يمين الفاصلة، عدد المنازل في ناتج ضرب عددين عشريين = مجموع منازلهما؛
# الخطأ الشائع: ٠٫٢ × ٠٫٣ = ٠٫٦؛ النشاط: شبكة ٤ × ٤ وحجرا نرد؛ التمرين ٥: ٤٫٠ = ٤)،
# كتاب الطالب ص٦٤–٦٥ (مثال ٣-٤)، وإجابات الدليل ص٧٨ (كتاب الطالب) وص٨٢ (كتاب النشاط ص٤٧).
# python3.12 gen_powers.py mul_slides.py ضرب_الأعداد_العشرية_عرض_تفاعلي.html "ضرب الأعداد العشرية والكسور العشرية — الصف السابع"
exec(open(os.path.join(HERE, 'vcol.py'), encoding='utf-8').read())

def STP(lab, expr='', cls=''): return st(f'<div class="stp {cls}"><span class="lab">{lab}</span>{expr}</div>')
def STEPS(*rows): return '<div class="stps">' + ''.join(rows) + '</div>'
def DPC(x):   # العدد مع إبراز الأرقام يمين الفاصلة (التي نعدّها)
    i, _, d = x.partition('.')
    return f'<span class="dpc">{_ar(i)}{"٫<u>" + _ar(d) + "</u>" if d else ""}</span>'
def VB(h): return f'<div class="vbox">{h}</div>'
S = []
ME = 'إعداد: أ. عيسى الحارثي'
S.append(slide(f'''<span class="tag">الصف السابع · الدرس ٣-٤</span>
<h1 class="h1s">ضرب الأعداد العشرية والكسور العشرية</h1>
<p class="lead">كتاب الطالب ص ٦٤ و ٦٥ · حصتان</p>
<p class="lead" style="font-size:clamp(26px,4.8vh,56px)">{ME}</p>''', 'cover'))
CAN = ['أضرب عدداً عشرياً في عددٍ من رقمٍ واحد <b>ذهنياً</b>', 'أضرب بالطريقة <b>الكتابية</b> متجاهلاً الفاصلة ثم أعيدها', 'أحدّد مكان الفاصلة في الناتج <b>بعدّ الأرقام</b> يمين الفاصلة في السؤال']
S.append(slide(f'''<h2>في نهاية هذا الدرس…</h2>
<div class="can">{''.join(f'<div><span class="can-i">✔</span><span><b>أنا أستطيع</b> أن {t}</span></div>' for t in CAN)}</div>'''))
S.append(slide(f'''<h2>مفردات الدرس</h2>
{st('<div class="vocab wide"><div><span>الطريقة الذهنية</span><i>mental method</i></div><div><span>الطريقة الكتابية</span><i>written method</i></div><div><span>المنزلة العشرية</span><i>decimal place</i></div></div>')}
<p class="lead">حصتان: <b class="c-i">أنا</b> ← <b class="c-we">نحن</b> ← <b class="c-u">أنتم</b></p>'''))

# ═══════════ الحصة الأولى: الطريقة الذهنية ═══════════
S.append(slide('''<span class="tag">الحصة الأولى · ٤٠ دقيقة</span><h2>الضرب الذهني</h2>
<div class="plan"><div><b>٤ د</b>تهيئة</div><div><b>٧ د</b>الخطوات الأربع</div><div><b>٨ د</b>مثال ٣-٤ (١)</div>
<div><b>٦ د</b>نحن</div><div><b>٧ د</b>أنتم</div><div><b>٥ د</b>انتبه</div><div><b>٣ د</b>بطاقة الخروج</div></div>''', 'divider'))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">تهيئة 🤔</span>{ref('كتاب الطالب ص ٦٤')}</div><h2>كم يساوي ٤ × ٠٫٢ ؟</h2>
{st('<table class="pvt"><tr><th>آحاد</th><th class="pt">٫</th><th>الجزء من عشرة</th><th>الجزء من مئة</th></tr><tr><td>١</td><td class="pt">٫</td><td>١ / ١٠</td><td>١ / ١٠٠</td></tr></table>')}
{st('<div class="note">٠٫٢ تعني <b>جزأين من عشرة</b>، و ٤ مرات جزأين من عشرة = <b>٨ أجزاء من عشرة</b> = ٠٫٨</div>')}''' + tn('جدول القيمة المكانية من الكتاب ص ٦٤، والدليل يقترحه وسيلةً مرئية (تعليقه على التمرين ٥).')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('كتاب الطالب ص ٦٤')}</div><h2>لضرب عددٍ عشري في عددٍ من رقمٍ واحد</h2>
<div class="defs">{st('<div><b class="kk c-exp">١</b><span><b class="c-exp">نتجاهل</b> الفاصلة العشرية</span></div>')}{st('<div><b class="kk c-we">٢</b><span>نضرب كالأعداد الكاملة</span></div>')}{st('<div><b class="kk c-lcm">٣</b><span><b>نعدّ</b> الأرقام يمين الفاصلة في السؤال</span></div>')}{st('<div><b class="kk c-i">٤</b><span><b>نعيد</b> الفاصلة إلى الناتج بالعدد نفسه من الأرقام على يمينها</span></div>')}</div>'''))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('مثال ٣-٤ (١ أ)')}</div><h2>الطريقة الذهنية: ٤ × ٠٫٢</h2>
<div class="row vrow">{STEPS(STP('نتجاهل الفاصلة', M('٢', X, '٤', EQ, '٨', cls='sm')), STP('في السؤال رقمٌ واحد يمين الفاصلة', DPC('0.2')), STP('رقمٌ واحد يمين الفاصلة في الناتج', M('٠٫٢', X, '٤', EQ, '٠٫٨', cls='sm'), 'fin'))}</div>'''))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('مثال ٣-٤ (١ ب)')}</div><h2>الطريقة الذهنية: ٢ × ٠٫٦</h2>
<div class="row vrow">{STEPS(STP('نتجاهل الفاصلة', M('٦', X, '٢', EQ, '١٢', cls='sm')), STP('في السؤال رقمٌ واحد يمين الفاصلة', DPC('0.6')), STP('رقمٌ واحد يمين الفاصلة في الناتج', M('٠٫٦', X, '٢', EQ, '١٫٢', cls='sm'), 'fin'))}</div>
{st('<div class="note">٢ × ٦ أجزاء من عشرة = ١٢ جزءاً من عشرة = ١٫٢</div>')}'''))
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('تمرين ١ (أ، ب)')}</div><h2>معاً: احسب ذهنياً</h2>
<div class="row">{st(f'<button class="flip box col" style="flex:1"><span class="hint">٨ × ٠٫١</span><span class="tap">👆</span><span class="hid">{M("٠٫٨")}</span></button>')}{st(f'<button class="flip box col" style="flex:1"><span class="hint">٣ × ٠٫٣</span><span class="tap">👆</span><span class="hid">{M("٠٫٩")}</span></button>')}</div>''' + tn('اطلب من الطلاب قول الخطوات بصوتٍ عالٍ: «٨ × ١ = ٨، ورقمٌ واحد يمين الفاصلة، إذن ٠٫٨».')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ١ (ج)')}{timer(1)}</div>''' + quiz('٥ × ٠٫٥ = ؟', [M('٢٥'), M('٠٫٢٥'), M('٢٫٥'), M('٥٫٥')], 2, '٥ × ٥ = ٢٥، ورقمٌ واحد يمين الفاصلة: ٢٫٥')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ١ (د)')}</div>''' + quiz('٦ × ٠٫٧ = ؟', [M('٤٫٢'), M('٤٢'), M('٠٫٤٢'), M('٣٫٢')], 0, '٦ × ٧ = ٤٢، ورقمٌ واحد يمين الفاصلة: ٤٫٢')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ١ (هـ)')}</div>''' + quiz('٢ × ٠٫٩ = ؟', [M('١٨'), M('١٫٨'), M('٠٫١٨'), M('٢٫٩')], 1, '٢ × ٩ = ١٨، ورقمٌ واحد يمين الفاصلة: ١٫٨')))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">انتبه ⚠️ خطأ شائع</span>{ref('دليل المعلم ص ٦٩')}</div><h2>عددان عشريان: نجمع المنازل</h2>
<div class="errs">{st('<button class="flip err" style="font-size:clamp(34px,6.6vh,76px)"><span class="xq">٠٫٢ × ٠٫٣ = ٠٫٦</span><span class="tap">👆</span><span class="hid xa no">✘ الصحيح ٠٫٠٦</span></button>')}</div>
{st('<div class="note">عدد المنازل العشرية في الناتج = مجموع المنازل العشرية في العددين</div>')}''' + tn('الخطأ الشائع ونقطة التعلّم الثالثة من الدليل؛ كتاب الطالب في هذا الدرس يضرب في عددٍ كامل فقط، فاعرضه توسعةً. تحقّق: ٠٫٢ × ٠٫٣ أصغر من ٠٫٣، فلا يمكن أن يكون ٠٫٦ (ضعفه).')))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ١ 🎫</span><h2>احسب ذهنياً</h2>
<div class="exit">{st('<div><b>١</b>٧ × ٠٫٧</div>')}{st('<div><b>٢</b>٦ × ٠٫٨</div>')}{st('<div><b>٣</b>٥ × ٠٫٦</div>')}</div>''' + tn('من كتاب النشاط ص ٤٧ تمرين ١ (هـ، و، د).')))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ١ 🎫</span><h2>الإجابات</h2>
<button class="flip box col" style="min-width:40vw"><span class="tap">👆 اضغط لإظهار الإجابات</span><span class="hid col">{M('٤٫٩', cls="sm")}{M('٤٫٨', cls="sm")}{M('٣٫٠ = ٣', cls="sm")}</span></button>'''))

# ═══════════ الحصة الثانية: الطريقة الكتابية ═══════════
S.append(slide('''<span class="tag">الحصة الثانية · ٤٠ دقيقة</span><h2>الضرب بالطريقة الكتابية</h2>
<div class="plan"><div><b>٣ د</b>إحماء</div><div><b>٦ د</b>مثال ٣-٤ (٢)</div><div><b>٧ د</b>مثال ٣-٤ (٣)</div>
<div><b>٥ د</b>نحن</div><div><b>٥ د</b>أنتم</div><div><b>٤ د</b>سامي وهيثم</div><div><b>٦ د</b>أكمل العمليات</div><div><b>٤ د</b>بطاقة الخروج</div></div>''', 'divider'))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">إحماء 🔥</span>{timer(1)}</div>''' + quiz('٤ × ٠٫٢ = ؟', [M('٨'), M('٠٫٨'), M('٠٫٠٨'), M('٤٫٢')], 1, '٤ × ٢ = ٨، ورقمٌ واحد يمين الفاصلة')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('مثال ٣-٤ (٢)')}</div><h2>أوجد ناتج ٦ × ٥٫١</h2>
<div class="row vrow">{STEPS(STP('نتجاهل الفاصلة', M('٥١', X, '٦', cls='sm')), STP('في السؤال رقمٌ واحد يمين الفاصلة', DPC('5.1')), STP('الناتج', M('٣٠٫٦', cls='sm'), 'fin'))}
{VB(vmul('51', '6', reveal=True))}</div>''' + tn('تحقّق بالتقدير: ٦ × ٥ = ٣٠، والناتج ٣٠٫٦ قريبٌ منه (لا ٣٠٦ ولا ٣٫٠٦).')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('مثال ٣-٤ (٣)')}</div><h2>أوجد ناتج ٤ × ٢٫١٦</h2>
<div class="row vrow">{STEPS(STP('نتجاهل الفاصلة', M('٢١٦', X, '٤', cls='sm')), STP('في السؤال رقمان يمين الفاصلة', DPC('2.16')), STP('رقمان يمين الفاصلة في الناتج', M('٨٫٦٤', cls='sm'), 'fin'))}
{VB(vmul('216', '4', reveal=True))}</div>''' + tn('المحمول ٢ (من ٦ × ٤ = ٢٤) فوق منزلة الرقم ١ كما في الكتاب. التقدير: ٤ × ٢ = ٨.')))
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('تمرين ٢ (أ)، تمرين ٣ (أ)')}</div><h2>معاً: أوجد الناتج</h2>
<div class="row">{st(f'<button class="flip box col" style="flex:1"><span class="hint">٥ × ٢٫٧</span><span class="tap">👆</span><span class="hid col vfl">{vmul("27", "5")}{M("١٣٫٥", cls="sm")}</span></button>')}{st(f'<button class="flip box col" style="flex:1"><span class="hint">٢ × ٣٫١٥</span><span class="tap">👆</span><span class="hid col vfl">{vmul("315", "2")}{M("٦٫٣٠ = ٦٫٣", cls="sm")}</span></button>')}</div>''' + tn('في (٢ × ٣٫١٥): الناتج ٦٫٣٠ وهو يساوي ٦٫٣، فالصفر الأخير بعد الفاصلة لا يغيّر القيمة.')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ٢ (ب)')}{timer(2)}</div>''' + quiz('٨ × ٣٫٦ = ؟', [M('٢٨٨'), M('٢٫٨٨'), M('٢٨٫٨'), M('٢٤٫٨')], 2, '٣٦ × ٨ = ٢٨٨، ورقمٌ واحد يمين الفاصلة: ٢٨٫٨')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ٣ (ج)')}</div>''' + quiz('٩ × ٣٫٢١ = ؟', [M('٢٨٫٨٩'), M('٢٨٨٫٩'), M('٢٧٫٨٩'), M('٢٫٨٨٩')], 0, '٣٢١ × ٩ = ٢٨٨٩، ورقمان يمين الفاصلة: ٢٨٫٨٩')))
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('تمرين ٥')}</div><h2>سامي وهيثم: ٥ × ٠٫٨</h2>
<div class="row sh">{st(box('<div class="col"><span class="hint">سامي 🧑</span>' + M('٤٫٠') + '</div>', style="flex:1"))}{st(box('<div class="col"><span class="hint">هيثم 👦</span>' + M('٤') + '</div>', style="flex:1"))}</div>
{st('<div class="note">كلاهما صحيح: ٥ × ٨ = ٤٠، ورقمٌ واحد يمين الفاصلة، فالناتج ٤٫٠ وهو يساوي ٤</div>')}''' + tn('من الدليل: يجب أن يفهم الطلاب أن ٤٫٠ يساوي العدد الصحيح ٤، وجدول القيمة المكانية وسيلةٌ مرئية جيدة.')))
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('تمرين ٤')}</div><h2>أكمل مستخدماً كل عددٍ مرةً واحدة</h2>
<div class="pool">{''.join(f'<span>{n}</span>' for n in ('١٨٫٣', '٢', '٣٦٫٨', '٠٫٦', '٦٫١', '٧', '٠٫٧'))}</div>
<div class="xgrid c3 pz">{''.join(st(f'<button class="flip xcard"><span class="xq">{q}</span><span class="tap">👆</span><span class="hid xa">{a_}</span></button>') for q, a_ in (
  ('(أ) ٦ × ٠٫١ = ☐', '٠٫٦'), ('(ب) ٠٫٤ × ☐ = ٢٫٨', '٧'), ('(ج) ☐ × ٥ = ٣٫٥', '٠٫٧'), ('(د) ٤٫٣ × ☐ = ٨٫٦', '٢'), ('(هـ) ٩٫٢ × ٤ = ☐', '٣٦٫٨'), ('(و) ☐ × ٣ = ☐', '٦٫١ و ١٨٫٣')))}</div>''' + tn('ابدأ بالسهل (أ، هـ)، ثم (و) بآخر عددين باقيين: ٦٫١ × ٣ = ١٨٫٣.')))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">نشاط 🎲</span>{ref('نشاط دليل المعلم')}</div><h2>شبكة الضرب ونرد العشري</h2>
<div class="exit">{st('<div><b>١</b>يرسم كل طالب شبكة ٤ × ٤ ويكتب فيها ١٦ عدداً من القائمة</div>')}{st('<div><b>٢</b>نرمي نرداً للعدد الكامل (١ إلى ٦) ونرداً للعشري (٠٫١ إلى ٠٫٦)</div>')}{st('<div><b>٣</b>نضرب العددين ونظلّل الناتج إن وُجد، والفائز أول من يظلّل كل أعداده</div>')}</div>''' + tn('قائمة الدليل: ٠٫١، ٠٫٢، ٠٫٣، ٠٫٤، ٠٫٥، ٠٫٦، ٠٫٨، ٠٫٩، ١، ١٫٢، ١٫٥، ١٫٦، ١٫٨، ٢، ٢٫٤، ٢٫٥، ٣، ٣٫٦. ناقش لماذا تظهر ٠٫٦ و ١٫٢ كثيراً، والأقلّ ظهوراً ٠٫١ و ٠٫٩ و ١٫٦ و ٢٫٥ و ٣٫٦.')))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ٢ 🎫</span><h2>أوجد الناتج</h2>
<div class="exit">{st('<div><b>١</b>٦ × ٦٫٦</div>')}{st('<div><b>٢</b>٥ × ٣٫١٣</div>')}{st('<div><b>٣</b>٣ × ٤٫٥٦</div>')}</div>'''))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ٢ 🎫</span><h2>الإجابات</h2>
<button class="flip box col" style="min-width:40vw"><span class="tap">👆 اضغط لإظهار الإجابات</span><span class="hid col">{M('٣٩٫٦', cls="sm")}{M('١٥٫٦٥', cls="sm")}{M('١٣٫٦٨', cls="sm")}</span></button>'''))
S.append(slide('''<span class="qbadge" style="background:#0A6770;box-shadow:0 4px 0 #05393E">الواجب المنزلي 🏠</span><h2>بعد الحصتين</h2>
<div class="exit"><div class="st"><div><b>١</b>صفحة ٤٧ في كتاب النشاط (ضرب الأعداد العشرية)</div></div></div>'''))
S.append(slide(f'''<h2>الخلاصة</h2>
<div class="sumg">
{st(box('<div class="col"><b class="kk c-exp">نتجاهل</b><span>الفاصلة ونضرب</span></div>'))}
{st(box('<div class="col"><b class="kk c-we">نعدّ</b><span>الأرقام يمين الفاصلة في السؤال</span></div>'))}
{st(box('<div class="col"><b class="kk c-lcm">نعيد</b><span>الفاصلة بالعدد نفسه في الناتج</span></div>'))}</div>'''))

# ═══════════ ملحق: تمارين كتاب الطالب ص٦٥ (الإجابات من دليل المعلم ص٧٨) ═══════════
S.append(launch('sb', '٦٥', note=f'المراجع: كتاب الطالب ص٦٤ و ٦٥، ودليل المعلم ص٦٩ و ٧٠ وإجاباته ص٧٨ · {ME}'))
H = ['أ', 'ب', 'ج', 'د', 'هـ', 'و']
RM = 'نتجاهل الفاصلة ونضرب، ثم نعيدها بعدد الأرقام التي يمينها في السؤال'
def MX(lst): return [(f'({h}) {_ar(k)} × {_ar(x)}', (vmul(x.replace('.', ''), k) if w else '') + M(_ar(r), cls='sm')) for h, (k, x, r, w) in zip(H, lst)]
S.append(ex(1, 'احسب ذهنياً', RM, MX([('8', '0.1', '0.8', 0), ('3', '0.3', '0.9', 0), ('5', '0.5', '2.5', 0), ('6', '0.7', '4.2', 0), ('2', '0.9', '1.8', 0)]), cols=2))
S.append(ex(2, 'احسب بالطريقة الكتابية', RM, MX([('5', '2.7', '13.5', 1), ('8', '3.6', '28.8', 1), ('3', '9.8', '29.4', 1), ('6', '6.6', '39.6', 1)]), cols=2))
S.append(ex(3, 'أوجد الناتج', RM, MX([('2', '3.15', '6.3', 1), ('5', '3.13', '15.65', 1), ('9', '3.21', '28.89', 1), ('3', '4.56', '13.68', 1)]), cols=2))
S.append(ex(4, 'أكمل بالأعداد: ١٨٫٣، ٢، ٣٦٫٨، ٠٫٦، ٦٫١، ٧، ٠٫٧', 'كل عددٍ مرةً واحدةً فقط', [('(أ) ٦ × ٠٫١ = ☐', '٠٫٦'), ('(ب) ٠٫٤ × ☐ = ٢٫٨', '٧'), ('(ج) ☐ × ٥ = ٣٫٥', '٠٫٧'), ('(د) ٤٫٣ × ☐ = ٨٫٦', '٢'), ('(هـ) ٩٫٢ × ٤ = ☐', '٣٦٫٨'), ('(و) ☐ × ٣ = ☐', '٦٫١ × ٣ = ١٨٫٣')], cols=2))
S.append(ex(5, 'سامي وهيثم', 'نحسب ثم نقارن', [('٥ × ٠٫٨: سامي يقول ٤٫٠، وهيثم يقول ٤. من المصيب؟', 'كلاهما صحيح<small>٤٫٠ و ٤ يساويان القيمة نفسها</small>')], cols=1))

# ═══════════ ملحق: حلول كتاب النشاط ص٤٧ (الإجابات من دليل المعلم ص٨٢) ═══════════
S.append(launch('ab', '٤٧', note='الإجابات النهائية من دليل المعلم ص ٨٢'))
NA = 'نشاط ص ٤٧ · تمرين'
S.append(ex(1, 'احسب ذهنياً', RM, MX([('2', '0.3', '0.6', 0), ('4', '0.2', '0.8', 0), ('6', '0.4', '2.4', 0), ('5', '0.6', '3', 0), ('7', '0.7', '4.9', 0), ('6', '0.8', '4.8', 0)]), cols=2, src=NA))
S.append(ex(2, 'أوجد الناتج', RM, MX([('3', '3.6', '10.8', 1), ('7', '3.6', '25.2', 1), ('9', '3.6', '32.4', 1), ('4', '4.8', '19.2', 1), ('7', '4.8', '33.6', 1), ('9', '4.8', '43.2', 1)]), cols=2, src=NA))
S.append(ex(3, 'أوجد الناتج', RM, MX([('3', '3.69', '11.07', 1), ('7', '3.69', '25.83', 1), ('9', '3.69', '33.21', 1), ('4', '4.82', '19.28', 1), ('7', '4.82', '33.74', 1), ('9', '4.82', '43.38', 1)]), cols=2, src=NA))
S.append(ex(4, 'أكمل بالأعداد: ٠٫٤، ٠٫٥، ٠٫٦، ٢، ٤، ٦، ٣٫٨', 'كل عددٍ مرةً واحدةً فقط', [('(أ) ٣ × ٠٫٢ = ☐', '٠٫٦'), ('(ب) ٠٫٦ × ☐ = ٢٫٤', '٤'), ('(ج) ☐ × ٩ = ٤٫٥', '٠٫٥'), ('(د) ٦٫٣ × ☐ = ٣٧٫٨', '٦'), ('(هـ) ٧٫٦ × ٠٫٥ = ☐', '٣٫٨'), ('(و) ☐ × ٥ = ☐', '٠٫٤ × ٥ = ٢')], cols=2, src=NA))

EXTRA_CSS_OWN = '''
.stps{display:flex;flex-direction:column;gap:1.2vh;align-items:stretch}
.stp{display:flex;align-items:center;gap:1.4vw;justify-content:space-between}
.stp .lab{flex:0 1 auto;max-width:70%;font-family:var(--fh);font-weight:800;color:#2563EB;background:#EAF1FF;border-radius:12px;padding:.2em .8em;text-align:center;line-height:1.4;font-size:clamp(20px,3.6vh,40px)}
.stp.fin .lab{background:var(--good);color:#fff}
.slide .vrow{align-items:center;justify-content:center;gap:2vh 3vw;flex-wrap:wrap}
.slide .vrow>.stps{flex:0 1 auto;max-width:min(1000px,70vw)}
@media (max-aspect-ratio:1/1){.slide .vrow{flex-direction:column}.slide .vrow>.stps{max-width:92vw}}
.vbox{flex:none;background:#fff;border:3px solid var(--line);border-radius:18px;padding:1vh 2vw;font-family:var(--fh);font-size:clamp(48px,9.6vh,110px)}
.dpc{font-family:var(--fh);font-weight:900;font-size:clamp(34px,6.4vh,74px);direction:ltr;unicode-bidi:isolate}
.dpc u{text-decoration:none;color:#C2410C;background:#FFF1E6;border-bottom:.08em solid #C2410C;border-radius:.1em;padding:0 .05em}
.pvt{border-collapse:collapse;font-weight:700;font-size:clamp(28px,5.4vh,62px);direction:rtl}
.pvt th,.pvt td{border:3px solid #C9A400;padding:.3em .7em;text-align:center;background:#FFF7C9}
.pvt th{background:#FFE98A}.pvt .pt{background:#fff;color:var(--bad);padding:.3em .2em}
.hid.vfl{font-family:var(--fh);font-size:clamp(36px,6.8vh,80px)}
.box .col>.m:not(.mid):not(.sm):not(.big),.hid.col>.m:not(.mid):not(.sm):not(.big){font-size:clamp(34px,6.4vh,76px)}
.pool{display:flex;flex-wrap:wrap;gap:1vw;justify-content:center;background:#EAF6D8;border:3px solid #9CC86A;border-radius:16px;padding:1vh 1.6vw}
.pool span{font-family:var(--fh);font-weight:800;font-size:clamp(24px,4.4vh,50px);padding:0 .4em}
.defs{display:flex;flex-direction:column;gap:1.4vh;width:min(1400px,92vw)}
.defs .st>div{display:flex;align-items:center;gap:1.6vw;background:#fff;border:3px solid var(--line);border-radius:18px;padding:1vh 1.6vw}
.defs .kk{flex:none;font-size:clamp(34px,6.2vh,74px)}.defs span{font-weight:700;font-size:clamp(24px,4.4vh,52px);line-height:1.45}
.errs{display:flex;flex-direction:column;gap:1.4vh;width:min(1400px,92vw)}
.errs .err{display:flex;flex-direction:column;align-items:center;gap:.6vh;background:#fff;border:3px solid var(--line);border-radius:16px;padding:.8vh 1.6vw;font-size:clamp(26px,5vh,58px);font-weight:700}
.errs .err .xq{font-size:inherit}.errs .err .xa{font-size:clamp(24px,4.4vh,50px)}
.sumg{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:2vw;width:min(1600px,94vw)}
.sumg .col span{font-weight:700;font-size:clamp(26px,4.6vh,56px);line-height:1.4}
.sumg .kk{font-size:clamp(34px,6.4vh,76px)}
.xa .vcol{font-family:var(--fh);font-size:1.05em;margin:0 .3em;color:var(--ink)}
.xa small{display:block}
.pz>.st{display:flex}.pz>.st>.xcard{flex:1}
.sh .m{font-size:clamp(44px,8.6vh,100px)!important}
.errs .err .xq .m{font-size:inherit}
'''
