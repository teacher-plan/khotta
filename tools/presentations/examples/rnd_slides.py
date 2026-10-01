# شرائح درس ٣-٢ «التقريب» — الصف السابع (حصتان، كتاب الطالب ص٦٠–٦١)
# المراجع: دليل المعلم ص٦٥–٦٦ (القيمة المكانية، الرقم على يمين المنزلة، الخطأ الشائع: فقد الأصفار أو إضافتها؛ النشاط: تقدير أطوالٍ بالمساطر)،
# كتاب الطالب ص٦٠–٦١ (مثال ٣-٢)، وإجابات الدليل ص٧٧ (كتاب الطالب) وص٨١–٨٢ (كتاب النشاط ص٤٣–٤٤).
# python3.12 gen_powers.py rnd_slides.py التقريب_عرض_تفاعلي.html "التقريب — الصف السابع"

def STP(lab, expr, cls=''): return st(f'<div class="stp {cls}"><span class="lab">{lab}</span>{expr}</div>')
def STEPS(*rows): return '<div class="stps">' + ''.join(rows) + '</div>'
AR = '٠١٢٣٤٥٦٧٨٩'
def NUM(s, t=None, d=None):
    # عددٌ يُكتب من اليسار إلى اليمين (كما تُكتب الأعداد دائماً)؛ t = موضع رقم المنزلة المطلوبة، d = موضع الرقم الذي على يمينها
    out = ''
    for i, c in enumerate(s):
        ch = AR[int(c)] if c.isdigit() else ('٫' if c == '.' else (' ' if c == ' ' else c))
        cls = ' t' if i == t else (' d' if i == d else '')
        out += f'<span class="dg{cls}">{ch}</span>' if c not in ' .' else (f'<span class="dp">{ch}</span>' if c == '.' else '<span class="sp"></span>')
    return f'<span class="num">{out}</span>'
def NL(lo, hi, x, xpos, lab_lo, lab_hi, lab_x, mid=True):   # خط أعداد: من lo (يساراً) إلى hi (يميناً)، والعدد x عند xpos٪
    return f'''<div class="nl"><div class="line"></div><span class="tk" style="left:0%"><b>{lab_lo}</b></span><span class="tk" style="left:100%"><b>{lab_hi}</b></span>
{'<span class="tk mid" style="left:50%"><b>المنتصف</b></span>' if mid else ''}<span class="pt" style="left:{xpos}%"><b>{lab_x}</b></span></div>'''
S = []
ME = 'إعداد: أ. عيسى الحارثي'
S.append(slide(f'''<span class="tag">الصف السابع · الدرس ٣-٢</span>
<h1 class="h1s">التقريب</h1>
<p class="lead">كتاب الطالب ص ٦٠ و ٦١ · حصتان</p>
<p class="lead" style="font-size:clamp(26px,4.8vh,56px)">{ME}</p>''', 'cover'))
CAN = ['أحدّد <b>المنزلة</b> المطلوب التقريب إليها و<b>الرقم على يمينها</b>', 'أقرّب الأعداد الكاملة إلى أقرب ١٠ أو ١٠٠ أو ١٠٠٠ … أو مليون', 'أقرّب الأعداد العشرية إلى أقرب عدد كامل أو منزلة عشرية أو منزلتين']
S.append(slide(f'''<h2>في نهاية هذا الدرس…</h2>
<div class="can">{''.join(f'<div><span class="can-i">✔</span><span><b>أنا أستطيع</b> أن {t}</span></div>' for t in CAN)}</div>'''))
S.append(slide(f'''<h2>مفردات الدرس</h2>
{st('<div class="vocab wide"><div><span>التقريب</span><i>round</i></div><div><span>درجة الدقّة</span><i>degree of accuracy</i></div></div>')}
<p class="lead">حصتان: <b class="c-i">أنا</b> ← <b class="c-we">نحن</b> ← <b class="c-u">أنتم</b></p>'''))

# ═══════════ الحصة الأولى: تقريب الأعداد الكاملة ═══════════
S.append(slide('''<span class="tag">الحصة الأولى · ٤٠ دقيقة</span><h2>تقريب الأعداد الكاملة</h2>
<div class="plan"><div><b>٤ د</b>تهيئة</div><div><b>٧ د</b>قاعدة التقريب</div><div><b>٥ د</b>خط الأعداد</div>
<div><b>٩ د</b>مثال ٣-٢ (أ، ب، ج)</div><div><b>٨ د</b>نحن ← أنتم</div><div><b>٤ د</b>انتبه</div><div><b>٣ د</b>بطاقة الخروج</div></div>''', 'divider'))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">تهيئة 🤔</span></div><h2>حضر المباراةَ ٢٣٢٥٢ مشجّعاً</h2>
{st('<div class="note">لماذا يقول المذيع: «حضر المباراة <b>نحو ٢٣٠٠٠</b> مشجّع»؟</div>')}
{st('<div class="note">نقرّب العدد ليصبح أسهل في القراءة والتذكّر، ويبقى <b>قريباً</b> من العدد الأصلي</div>')}''' + tn('من خارج المرجع: تهيئة بالعدد نفسه في مثال ٣-٢ (ب). ذكّر الطلاب أن العدد بعد التقريب يكون قريباً من العدد الأصلي (نقطة الدليل).')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('كتاب الطالب ص ٦٠')}</div><h2>لتقريب عددٍ لمنزلةٍ معيّنة</h2>
<div class="defs">{st('<div><b class="kk c-exp">١</b><span>نحدّد الرقم الموجود في <b class="c-exp">المنزلة المطلوبة</b></span></div>')}{st('<div><b class="kk c-we">٢</b><span>ننظر إلى <b class="c-we">الرقم على يمينها</b>: إذا كان ٥ أو أكبر نضيف ١، وإذا كان أصغر من ٥ يبقى الرقم كما هو</span></div>')}{st('<div><b class="kk c-lcm">٣</b><span>الأرقام بعد المنزلة تصبح <b>أصفاراً</b></span></div>')}</div>''' + tn('يُسمّى المقدار المطلوب «درجة الدقّة»: إلى أقرب ١٠، أو ١٠٠، أو منزلة عشرية واحدة …')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('مثال ٣-٢ (أ)')}</div><h2>قرّب ٣٧٦ إلى أقرب ١٠٠</h2>
{st(NUM('376', t=0, d=1))}
{st(NL('300', '400', '376', 76, '٣٠٠', '٤٠٠', '٣٧٦'))}
{box(STEPS(STP('رقم المئات ٣، والرقم على يمينه ٧', M('٧', '&gt;', '٥', cls="sm")), STP('نضيف ١ إلى ٣', M('٣٧٦', '≈', '٤٠٠', cls="sm"), 'fin')))}''' + tn('خط الأعداد من خارج المرجع: ٣٧٦ أقرب إلى ٤٠٠ منه إلى ٣٠٠.')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('مثال ٣-٢ (ب)')}</div><h2>قرّب ٢٣٢٥٢ إلى أقرب ١٠٠٠</h2>
{st(NUM('23 252', t=1, d=3))}
{box(STEPS(STP('رقم الآلاف ٣، والرقم على يمينه ٢', M('٢', '&lt;', '٥', cls="sm")), STP('يبقى ٣ كما هو', M('٢٣٢٥٢', '≈', '٢٣٠٠٠', cls="sm"), 'fin')))}'''))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('مثال ٣-٢ (ج)')}</div><h2>قرّب ٢٦٥٨٠٠٠٠ إلى أقرب مليون</h2>
{st(NUM('26 580 000', t=1, d=3))}
{box(STEPS(STP('رقم الملايين ٦، والرقم على يمينه ٥', M('٥', EQ, '٥', cls="sm")), STP('نضيف ١ إلى ٦', M('٢٦٥٨٠٠٠٠', '≈', '٢٧٠٠٠٠٠٠', cls="sm"), 'fin')))}
{st('<div class="note">الرقم ٥ يرفع المنزلة: «٥ أو أكبر» نضيف ١</div>')}'''))
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('تمرين ١ (ب، د)')}</div><h2>معاً: قرّب</h2>
<div class="row">{st(f'<button class="flip box col" style="flex:1"><span class="hint">١٥٧ إلى أقرب ١٠</span>{NUM("157", t=1, d=2)}<span class="tap">👆</span><span class="hid">{M("١٦٠")}</span></button>')}{st(f'<button class="flip box col" style="flex:1"><span class="hint">٤٧٦ إلى أقرب ١٠٠</span>{NUM("476", t=0, d=1)}<span class="tap">👆</span><span class="hid">{M("٥٠٠")}</span></button>')}</div>'''))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ١ (و)')}{timer(2)}</div>''' + quiz('قرّب ١٢٥٧٥ إلى أقرب ١٠٠٠', [M('١٢٠٠٠'), M('١٣٠٠٠'), M('١٢٥٠٠'), M('١٢٦٠٠')], 1, 'رقم الآلاف ٢ وعلى يمينه ٥، فنضيف ١: ١٣٠٠٠')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ١ (ل)')}</div>''' + quiz('قرّب ٢٥٤٩٩٥٠٠ إلى أقرب مليون', [M('٢٦٠٠٠٠٠٠'), M('٢٥٠٠٠٠٠٠'), M('٢٥٥٠٠٠٠٠'), M('٣٠٠٠٠٠٠٠')], 1, 'رقم الملايين ٥ وعلى يمينه ٤ وهو أصغر من ٥، فيبقى: ٢٥٠٠٠٠٠٠')))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">انتبه ⚠️ خطأ شائع</span>{ref('دليل المعلم ص ٦٥')}</div><h2>لا نفقد الأصفار ولا نضيفها</h2>
<div class="errs">{''.join(st(f'<button class="flip err"><span class="xq">{q}</span><span class="tap">👆</span><span class="hid xa no">{w}</span></button>') for q, w in (
  ('٣٢٢٥ إلى أقرب ١٠٠ = ٣٢', '✘ فقدنا الأصفار: الصحيح ٣٢٠٠'), ('٣٤٫٦٧٧٧ إلى منزلة عشرية واحدة = ٣٤٫٧٧٧٧', '✘ أبقينا المنازل: الصحيح ٣٤٫٧')))}</div>''' + tn('الخطأ الأكثر شيوعاً في الدليل. اسأل باستمرار: «هل إجابتك تقريباً هي العدد نفسه الذي في السؤال؟» ٣٢ بعيدٌ جداً عن ٣٢٢٥.')))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ١ 🎫</span><h2>قرّب</h2>
<div class="exit">{st('<div><b>١</b>٤٢ إلى أقرب ١٠</div>')}{st('<div><b>٢</b>٢٣٢ إلى أقرب ١٠٠</div>')}{st('<div><b>٣</b>٤٥٢٩٨٥ إلى أقرب ١٠٠٠٠٠</div>')}</div>'''))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ١ 🎫</span><h2>الإجابات</h2>
<button class="flip box col" style="min-width:40vw"><span class="tap">👆 اضغط لإظهار الإجابات</span><span class="hid col">{M('٤٠', cls="sm")}{M('٢٠٠', cls="sm")}{M('٥٠٠٠٠٠', cls="sm")}</span></button>'''))

# ═══════════ الحصة الثانية: تقريب الأعداد العشرية ═══════════
S.append(slide('''<span class="tag">الحصة الثانية · ٤٠ دقيقة</span><h2>تقريب الأعداد العشرية</h2>
<div class="plan"><div><b>٣ د</b>إحماء</div><div><b>٧ د</b>إلى أقرب عدد كامل</div><div><b>٦ د</b>منزلة عشرية واحدة</div>
<div><b>٦ د</b>منزلتان عشريتان</div><div><b>٦ د</b>نحن</div><div><b>٦ د</b>أنتم</div><div><b>٣ د</b>نشاط</div><div><b>٣ د</b>بطاقة الخروج</div></div>''', 'divider'))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">إحماء 🔥</span>{timer(1)}</div>''' + quiz('قرّب ٤٣٨٠ إلى أقرب ١٠٠٠', [M('٤٠٠٠'), M('٥٠٠٠'), M('٤٤٠٠'), M('٤٣٠٠')], 0, 'رقم الآلاف ٤ وعلى يمينه ٣ وهو أصغر من ٥')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('مثال ٣-٢ (د)')}</div><h2>قرّب ١٢٫٦٧ إلى أقرب عدد كامل</h2>
{st(NUM('12.67', t=1, d=3))}
{st(NL('12', '13', '12.67', 67, '١٢', '١٣', '١٢٫٦٧'))}
{box(STEPS(STP('رقم الآحاد ٢، وعلى يمينه ٦', M('٦', '&gt;', '٥', cls="sm")), STP('نضيف ١، ونحذف الجزء العشري', M('١٢٫٦٧', '≈', '١٣', cls="sm"), 'fin')))}'''))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('مثال ٣-٢ (هـ)')}</div><h2>قرّب ٢٫٧٠٦ إلى أقرب منزلة عشرية واحدة</h2>
{st(NUM('2.706', t=2, d=3))}
{box(STEPS(STP('رقم الأجزاء من عشرة ٧، وعلى يمينه ٠', M('٠', '&lt;', '٥', cls="sm")), STP('يبقى ٧، ونحذف ما بعده', M('٢٫٧٠٦', '≈', '٢٫٧', cls="sm"), 'fin')))}
{st('<div class="note">في الجزء العشري نحذف الأرقام بعد المنزلة، ولا نكتب مكانها أصفاراً</div>')}'''))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('مثال ٣-٢ (و)')}</div><h2>قرّب ٠٫٤٦٩٢ إلى أقرب منزلتين عشريتين</h2>
{st(NUM('0.4692', t=3, d=4))}
{box(STEPS(STP('رقم الأجزاء من مئة ٦، وعلى يمينه ٩', M('٩', '&gt;', '٥', cls="sm")), STP('نضيف ١ إلى ٦', M('٠٫٤٦٩٢', '≈', '٠٫٤٧', cls="sm"), 'fin')))}'''))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">انتبه ⚠️</span>{ref('درسي في صفحة')}</div><h2>الصفر الأخير يبقى إذا طُلبت منزلته</h2>
<div class="row">{st(box(f'<div class="col"><span class="hint">٣٫٩٨ إلى منزلة عشرية واحدة</span>{M("٤٫٠")}</div>', style="flex:1"))}{st(box(f'<div class="col"><span class="hint">١٤٦٫٧٩٨ إلى منزلتين عشريتين</span>{M("١٤٦٫٨٠")}</div>', style="flex:1"))}</div>
{st('<div class="note">نكتب ٤٫٠ لا ٤، و ١٤٦٫٨٠ لا ١٤٦٫٨: عدد المنازل يبيّن درجة الدقّة</div>')}''' + tn('من ورقة «درسي في صفحة»، وهو في إجابات الدليل أيضاً (٢ (ي): ١٤٦٫٨٠).')))
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('تمرين ٢ (ب، د)')}</div><h2>معاً: قرّب</h2>
<div class="row">{st(f'<button class="flip box col" style="flex:1"><span class="hint">٩٫٥٥ إلى أقرب عدد كامل</span>{NUM("9.55", t=0, d=2)}<span class="tap">👆</span><span class="hid">{M("١٠")}</span></button>')}{st(f'<button class="flip box col" style="flex:1"><span class="hint">١١٫٤٥ إلى منزلة عشرية واحدة</span>{NUM("11.45", t=3, d=4)}<span class="tap">👆</span><span class="hid">{M("١١٫٥")}</span></button>')}</div>'''))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ٢ (ح)')}{timer(2)}</div>''' + quiz('قرّب ١٢٫٩١٥ إلى أقرب منزلتين عشريتين', [M('١٢٫٩١'), M('١٢٫٩٢'), M('١٢٫٩'), M('١٣٫٠٠')], 1, 'رقم الأجزاء من مئة ١ وعلى يمينه ٥، فنضيف ١: ١٢٫٩٢')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ٢ (ط)')}</div>''' + quiz('قرّب ٠٫٠٧٥٩ إلى أقرب منزلتين عشريتين', [M('٠٫٠٧'), M('٠٫٠٨'), M('٠٫٧٦'), M('٠٫١')], 1, 'رقم الأجزاء من مئة ٧ وعلى يمينه ٥، فنضيف ١: ٠٫٠٨')))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">نشاط 📏</span>{ref('نشاط دليل المعلم')}</div><h2>نقدّر الأطوال ثم نقيسها</h2>
<div class="exit">{st('<div><b>١</b>نقدّر طول كل خطٍّ في ورقة المصادر ٣-٢ ونقرّبه</div>')}{st('<div><b>٢</b>نجمع تقديرين ونقارن بالقياس الدقيق بالمسطرة</div>')}</div>''' + tn('نشاط الدليل بعد تمارين ٣-٢ ويحتاج ورقة المصادر ٣-٢ ومساطر الطلاب. الإجابات في دليل المعلم ص ٦٥ و ٦٦.')))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ٢ 🎫</span><h2>قرّب</h2>
<div class="exit">{st('<div><b>١</b>١٩٫٩٢٤ إلى أقرب عدد كامل</div>')}{st('<div><b>٢</b>٠٫٩٢٩ إلى منزلة عشرية واحدة</div>')}{st('<div><b>٣</b>٩٫٤٥٣ إلى منزلتين عشريتين</div>')}</div>'''))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ٢ 🎫</span><h2>الإجابات</h2>
<button class="flip box col" style="min-width:40vw"><span class="tap">👆 اضغط لإظهار الإجابات</span><span class="hid col">{M('٢٠', cls="sm")}{M('٠٫٩', cls="sm")}{M('٩٫٤٥', cls="sm")}</span></button>'''))
S.append(slide('''<span class="qbadge" style="background:#0A6770;box-shadow:0 4px 0 #05393E">الواجب المنزلي 🏠</span><h2>بعد الحصتين</h2>
<div class="exit"><div class="st"><div><b>١</b>صفحة ٤٣ في كتاب النشاط (التقريب)</div></div><div class="st"><div><b>٢</b>صفحة ٤٤ في كتاب النشاط (اختر الإجابة، وصحّح الخطأ)</div></div></div>'''))
S.append(slide(f'''<h2>الخلاصة</h2>
<div class="sumg">
{st(box('<div class="col"><b class="kk c-exp">المنزلة</b><span>نحدّد الرقم في المنزلة المطلوبة</span></div>'))}
{st(box('<div class="col"><b class="kk c-we">٥ أو أكبر</b><span>على يمينها: نضيف ١</span></div>'))}
{st(box('<div class="col"><b class="kk c-lcm">أصغر من ٥</b><span>يبقى الرقم كما هو</span></div>'))}</div>'''))

# ═══════════ ملحق: تمارين كتاب الطالب ص٦١ (الإجابات من دليل المعلم ص٧٧) ═══════════
S.append(launch('sb', '٦١', note=f'المراجع: كتاب الطالب ص٦٠ و ٦١، ودليل المعلم ص٦٥ و ٦٦ وإجاباته ص٧٧ · {ME}'))
H = ['أ', 'ب', 'ج', 'د', 'هـ', 'و', 'ز', 'ح', 'ط', 'ي', 'ك', 'ل']
RL = 'نحدّد رقم المنزلة، فإن كان الرقم على يمينها ٥ أو أكبر نضيف ١'
B1 = [('٤٢', '١٠', '٤٠'), ('١٥٧', '١٠', '١٦٠'), ('٢٣٢', '١٠٠', '٢٠٠'), ('٤٧٦', '١٠٠', '٥٠٠'), ('٤٣٨٠', '١٠٠٠', '٤٠٠٠'), ('١٢٥٧٥', '١٠٠٠', '١٣٠٠٠'),
      ('٣٢٤٧٩', '١٠٠٠٠', '٣٠٠٠٠'), ('١٢٥٤٥٠', '١٠٠٠٠', '١٣٠٠٠٠'), ('٤٥٢٩٨٥', '١٠٠٠٠٠', '٥٠٠٠٠٠'), ('١٤٢٧٥٤٦', '١٠٠٠٠٠', '١٤٠٠٠٠٠'), ('٧٨٥٦٩٢٠', 'مليون', '٨٠٠٠٠٠٠'), ('٢٥٤٩٩٥٠٠', 'مليون', '٢٥٠٠٠٠٠٠')]
S.append(ex(1, 'قرّب إلى درجة الدقّة المحدّدة', RL, [(f'({h}) {n}<small>إلى أقرب {p}</small>', r) for h, (n, p, r) in zip(H, B1)], cols=2))
B2 = [('٧٥٫٢', 'أقرب عدد كامل', '٧٥'), ('٩٫٥٥', 'أقرب عدد كامل', '١٠'), ('١٩٫٩٢٤', 'أقرب عدد كامل', '٢٠'), ('١١٫٤٥', 'منزلة عشرية واحدة', '١١٫٥'), ('٠٫٩٢٩', 'منزلة عشرية واحدة', '٠٫٩'),
      ('١٢٥٫٨٨١', 'منزلة عشرية واحدة', '١٢٥٫٩'), ('٩٫٤٥٣', 'منزلتين عشريتين', '٩٫٤٥'), ('١٢٫٩١٥', 'منزلتين عشريتين', '١٢٫٩٢'), ('٠٫٠٧٥٩', 'منزلتين عشريتين', '٠٫٠٨'), ('١٤٦٫٧٩٨', 'منزلتين عشريتين', '١٤٦٫٨٠')]
S.append(ex(2, 'قرّب العدد العشري إلى درجة الدقّة المحدّدة', 'نحذف الأرقام بعد المنزلة المطلوبة، ونُبقي صفرها الأخير إن طُلبت', [(f'({h}) {n}<small>إلى {p}</small>', r) for h, (n, p, r) in zip(H, B2)], cols=2))

# ═══════════ ملحق: حلول كتاب النشاط ص٤٣–٤٤ (الإجابات من دليل المعلم ص٨١–٨٢) ═══════════
S.append(launch('ab', '٤٣ و ٤٤', note='الإجابات النهائية من دليل المعلم ص ٨١ و ٨٢'))
NA, NB = 'نشاط ص ٤٣ · تمرين', 'نشاط ص ٤٤ · تمرين'
A1 = [('١٣', '١٠', '١٠'), ('٤٢٨', '١٠', '٤٣٠'), ('٥٠٥', '١٠٠', '٥٠٠'), ('٢٦١', '١٠٠', '٣٠٠'), ('٧٥٣١', '١٠٠٠', '٨٠٠٠'), ('٣٥٤٣٢', '١٠٠٠', '٣٥٠٠٠'),
      ('٧١١٧٧', '١٠٠٠٠', '٧٠٠٠٠'), ('٣٤٥٤٣٢', '١٠٠٠٠', '٣٥٠٠٠٠'), ('٧٥٠٠٠٠', '١٠٠٠٠٠', '٨٠٠٠٠٠'), ('٣٧٤٨٩٥٠٤', '١٠٠٠٠٠', '٣٧٥٠٠٠٠٠'), ('٣٧٤٨٩٥٠٤', '١٠٠٠٠٠٠', '٣٧٠٠٠٠٠٠'), ('٨٩٤٩٩٥٥٥', 'مليون', '٨٩٠٠٠٠٠٠')]
S.append(ex(1, 'قرّب إلى درجة الدقّة المطلوبة', RL, [(f'({h}) {n}<small>إلى أقرب {p}</small>', r) for h, (n, p, r) in zip(H, A1)], cols=2, src=NA))
A2 = [('٨٣٫٤', 'أقرب عدد كامل', '٨٣'), ('٥٩٫٥٠١', 'أقرب عدد كامل', '٦٠'), ('٠٫٣٧٧', 'أقرب عدد كامل', '٠'), ('٥٢٣٫٨١٥', 'منزلة عشرية واحدة', '٥٢٣٫٨'), ('٣٧٫٢٧٥', 'منزلة عشرية واحدة', '٣٧٫٣'),
      ('٠٫٩٨٣', 'منزلة عشرية واحدة', '١٫٠'), ('٠٫٠٥٤٣', 'منزلتين عشريتين', '٠٫٠٥'), ('٢٫٧٢٥', 'منزلتين عشريتين', '٢٫٧٣'), ('٥٩٫٩٩٥', 'منزلتين عشريتين', '٦٠٫٠٠')]
S.append(ex(2, 'قرّب إلى درجة الدقّة المطلوبة', 'نحذف الأرقام بعد المنزلة المطلوبة، ونُبقي صفرها الأخير إن طُلبت', [(f'({h}) {n}<small>إلى {p}</small>', r) for h, (n, p, r) in zip(H, A2)], cols=2, src=NA))
A3 = [('٥٢٩٩ إلى أقرب ١٠', '(ب) ٥٣٠٠'), ('٧٢٢٢٠ إلى أقرب ١٠٠', '(ج) ٧٢٢٠٠'), ('٥٤٩٧٥٠ إلى أقرب ١٠٠٠٠', '(أ) ٥٥٠٠٠٠'), ('٧٫٩٧ إلى منزلة عشرية واحدة', '(ب) ٨٫٠'),
      ('٤٨٫٥٩٥ إلى منزلتين عشريتين', '(ب) ٤٨٫٦٠'), ('١٠٫٩٩٩ إلى منزلتين عشريتين', '(ج) ١١٫٠٠')]
S.append(ex(3, 'اختر الإجابة الصحيحة', 'عدد المنازل في الإجابة يساوي درجة الدقّة المطلوبة', [(f'({h}) {q}', a_) for h, (q, a_) in zip(H, A3)], cols=2, src=NB))
A4 = [('١٧٫٠٥ إلى أقرب عدد كامل = ١٧٫٠', '✘<small>الصحيح ١٧</small>'), ('١٢٣٩٩ إلى أقرب ١٠ = ١٢٤٠٠', '✔'), ('٣٧٥٤٨ إلى أقرب ١٠٠٠ = ٣٨٠٠٠', '✔'),
      ('٤٥٫٩٩٦ إلى منزلتين عشريتين = ٤٥٫٠٠', '✘<small>الصحيح ٤٦٫٠٠</small>'), ('٣٩٫٩٥٠١ إلى منزلة عشرية واحدة = ٣٩٫٩', '✘<small>الصحيح ٤٠٫٠</small>')]
S.append(ex(4, 'ضع ✔ أو ✘ ثم صحّح العبارة الخاطئة', 'نقرّب بأنفسنا ثم نقارن بالعبارة', [(f'({h}) {q}', a_) for h, (q, a_) in zip(H, A4)], cols=1, per=3, src=NB))

EXTRA_CSS_OWN = '''
.stps{display:flex;flex-direction:column;gap:1.4vh;align-items:stretch}
.stp{display:flex;align-items:center;gap:1.6vw;justify-content:space-between}
.stp .lab{flex:none;max-width:52%;font-family:var(--fh);font-weight:800;color:#2563EB;background:#EAF1FF;border-radius:12px;padding:.2em .8em;text-align:center;line-height:1.4}
.stp.fin .lab{background:var(--good);color:#fff}
.box .col>.m:not(.mid):not(.sm):not(.big),.hid.col>.m:not(.mid):not(.sm):not(.big){font-size:clamp(34px,6.4vh,76px)}
.num{display:inline-flex;direction:ltr;unicode-bidi:isolate;font-family:var(--fh);font-weight:900;font-size:clamp(48px,9vh,104px);gap:.04em;align-items:flex-end}
.num .dg{padding:0 .06em;border-radius:.15em;line-height:1.15}
.num .dg.t{background:#FFE7A8;box-shadow:0 0 0 .07em #C77700 inset;color:#7A4A00}
.num .dg.d{color:#fff;background:var(--base);border-radius:50%;min-width:1.1em;text-align:center}
.num .dp{color:var(--bad)}.num .sp{width:.25em}
.flip .num{font-size:clamp(36px,6.6vh,78px)}
.flip.box .hid .m{font-size:clamp(34px,6.4vh,76px)}
.nl .tk b{white-space:nowrap}
.nl{position:relative;width:min(1000px,70vw);height:clamp(80px,14vh,150px);direction:ltr;margin:1vh auto}
.nl .line{position:absolute;left:0;right:0;top:40%;height:5px;background:var(--ink);border-radius:4px}
.nl .tk{position:absolute;top:40%;transform:translate(-50%,-50%);display:flex;flex-direction:column;align-items:center}
.nl .tk::before{content:'';width:4px;height:clamp(22px,4vh,44px);background:var(--ink)}
.nl .tk b{font-family:var(--fh);font-size:clamp(24px,4.6vh,52px);margin-top:.4vh}
.nl .tk.mid::before{background:#9FB0C6}.nl .tk.mid b{color:#7A8BA6;font-size:clamp(20px,3.8vh,42px)}
.nl .pt{position:absolute;top:40%;transform:translate(-50%,-100%);display:flex;flex-direction:column;align-items:center}
.nl .pt b{font-family:var(--fh);font-size:clamp(26px,5vh,56px);color:#C2410C;background:#FFF1E6;border-radius:10px;padding:0 .3em;margin-bottom:.6vh}
.nl .pt::after{content:'';width:clamp(16px,2.6vh,28px);height:clamp(16px,2.6vh,28px);border-radius:50%;background:#C2410C;transform:translateY(50%)}
.defs{display:flex;flex-direction:column;gap:1.6vh;width:min(1400px,92vw)}
.defs .st>div{display:flex;align-items:center;gap:1.6vw;background:#fff;border:3px solid var(--line);border-radius:18px;padding:1.2vh 1.6vw}
.defs .kk{flex:none;font-size:clamp(36px,6.8vh,80px)}.defs span{font-weight:700;font-size:clamp(26px,4.8vh,56px);line-height:1.45}
.errs{display:flex;flex-direction:column;gap:1.4vh;width:min(1400px,92vw)}
.errs .err{display:flex;flex-direction:column;align-items:center;gap:.6vh;background:#fff;border:3px solid var(--line);border-radius:16px;padding:.8vh 1.6vw;font-size:clamp(26px,5vh,58px);font-weight:700}
.errs .err .xq{font-size:inherit}.errs .err .xa{font-size:clamp(24px,4.4vh,50px)}
.sumg{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:2vw;width:min(1600px,94vw)}
.sumg .col span{font-weight:700;font-size:clamp(26px,4.6vh,56px);line-height:1.4}
.sumg .kk{font-size:clamp(34px,6.4vh,76px)}
.xq small{display:block;font-size:.72em;color:var(--ink2)}
'''
