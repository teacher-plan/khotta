# شرائح درس ١-٣ «العوامل وقابلية القسمة» — الصف السابع (٣ حصص، كتاب الطالب ص٢٤–٢٧)
# المراجع: دليل المعلم ص٢٥–٢٦ (لعبة بطاقات العوامل مع ورقة المصادر ١-٣، الخطأ الشائع)، كتاب الطالب ص٢٤–٢٧،
# ورقة «درسي في صفحة» ١-٣، وإجابات الدليل ص٣٦ (كتاب الطالب) وص٤٢ (كتاب النشاط ص١٦–١٧).
# python3.12 gen_powers.py fac_slides.py العوامل_وقابلية_القسمة_عرض_تفاعلي.html "العوامل وقابلية القسمة — الصف السابع"

DV = '<span class="x">÷</span>'
MI = '<span class="x">−</span>'
def STP(lab, expr, cls=''): return st(f'<div class="stp {cls}"><span class="lab">{lab}</span>{expr}</div>')
def STEPS(*rows): return '<div class="stps">' + ''.join(rows) + '</div>'
def L(*xs, hot=()):
    return '<span class="lst">' + '<i>،</i>'.join(f'<b class="{"cm" if x in hot else ""}">{a(x)}</b>' for x in xs) + '</span>'
def FACS(n): return [d for d in range(1, n + 1) if n % d == 0]
def PAIRS(n, upto=None):  # أزواج العوامل: ١ × ن ، ٢ × … حتى تتكرر
    rows, d = [], 1
    while (d <= upto) if upto else (d * d <= n):
        rows.append((d, n // d) if n % d == 0 else (d, None)); d += 1
    return rows
S = []
ME = 'إعداد: أ. عيسى الحارثي'
S.append(slide(f'''<span class="tag">الصف السابع · الدرس ١-٣</span>
<h1 class="h1s">العوامل وقابلية القسمة</h1>
<p class="lead">كتاب الطالب ص ٢٤–٢٧ · ثلاث حصص</p>
<p class="lead" style="font-size:clamp(26px,4.8vh,56px)">{ME}</p>''', 'cover'))
CAN = ['أجد <b>كل عوامل</b> العدد في صورة أزواج', 'أجد <b>العوامل المشتركة</b> و<b>العامل المشترك الأكبر (ع م ك)</b> لعددين',
       'أستخدم <b>اختبارات قابلية القسمة</b> على ٢ ، ٣ ، ٤ ، ٥ ، ٦ ، ٨ ، ٩ ، ١٠ ، ١٠٠', 'أربط بين العوامل والمضاعفات']
S.append(slide(f'''<h2>في نهاية هذا الدرس…</h2>
<div class="can">{''.join(f'<div><span class="can-i">✔</span><span><b>أنا أستطيع</b> أن {t}</span></div>' for t in CAN)}</div>'''))
S.append(slide(f'''<h2>مفردات الدرس</h2>
{st('<div class="vocab wide"><div><span>العامل</span><i>factor</i></div><div><span>العامل المشترك</span><i>common factor</i></div><div><span>الباقي</span><i>remainder</i></div><div><span>العامل المشترك الأكبر (ع م ك)</span><i>HCF</i></div><div><span>قابلية القسمة</span><i>divisible</i></div></div>')}
<p class="lead">ثلاث حصص: <b class="c-i">أنا</b> ← <b class="c-we">نحن</b> ← <b class="c-u">أنتم</b></p>'''))

# ═══════════ الحصة الأولى: العوامل ═══════════
S.append(slide('''<span class="tag">الحصة الأولى · ٤٠ دقيقة</span><h2>عوامل العدد</h2>
<div class="plan"><div><b>٥ د</b>تهيئة: عامل أم مضاعف؟</div><div><b>٥ د</b>تعريف العامل</div><div><b>١٢ د</b>أنا ← نحن ← أنتم</div>
<div><b>٥ د</b>انتبه: خطأ شائع</div><div><b>١٠ د</b>لعبة بطاقات العوامل</div><div><b>٣ د</b>بطاقة الخروج</div></div>''', 'divider'))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">تهيئة 🤔</span>{ref('كتاب الطالب ص ٢٤')}</div><h2>{M('٣', X, '٨', EQ, '٢٤')} — ماذا نستنتج؟</h2>
<div class="row">{st(box('<div class="col"><b class="kk c-we">٣ عاملٌ للعدد ٢٤</b><span class="hint">٢٤ ÷ ٣ = ٨ بدون باقٍ</span></div>', style="flex:1"))}{st(box('<div class="col"><b class="kk c-exp">٢٤ مضاعفٌ للعدد ٣</b><span class="hint">٣ × ٨ = ٢٤</span></div>', style="flex:1"))}</div>
{st('<div class="note">العبارتان تتّفقان: العوامل والمضاعفات وجهان لعملية واحدة</div>')}'''))
S.append(slide(f'''<h2>ما العامل؟</h2>
{st('<div class="rulebox">العامل: العدد الصحيح الذي يقسم عدداً صحيحاً آخر <b class="c-exp">بدون باقٍ</b></div>')}
<div class="row">{st(box('<div class="col"><b class="kk c-we">٢ و ٣ عاملان للعدد ٢٤</b>' + M('٢٤', DV, '٣', EQ, '٨') + '</div>', style="flex:1"))}{st(box('<div class="col"><b class="kk c-exp">٥ و ٧ ليسا عاملين</b><span class="hint">٢٤ ÷ ٥ لها باقٍ</span></div>', style="flex:1"))}</div>
{st('<div class="note">العدد <b>١</b> عاملٌ لكل عدد، وكل عددٍ عاملٌ لنفسه</div>')}'''))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('مثال ١-٣')}</div><h2>استنتج كل عوامل العدد ٤٠</h2>
<div class="pairs2">{''.join(st(f'<div class="{"ok" if q else "no"}"><span>{M(a(d), X, a(q), EQ, "٤٠") if q else M(a(d))}</span><small>{"عاملان" if q else "ليس عاملاً (له باقٍ)"}</small></div>') for d, q in PAIRS(40, 7))}</div>
{st('<div class="note">توقّفنا عند ٧ لأن ٨ موجودٌ في القائمة ← عوامل ٤٠: ١ ، ٢ ، ٤ ، ٥ ، ٨ ، ١٠ ، ٢٠ ، ٤٠</div>')}'''))
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('تمرين ٢ (ب)')}</div><h2>معاً: عوامل العدد ٢٨</h2><p class="ask">نبدأ بـ ١ × ٢٨ … ونتوقّف متى؟</p>
{box(STEPS(STP('الأزواج', M('١ × ٢٨ ، ٢ × ١٤ ، ٤ × ٧', cls="sm")), STP('العوامل', L(1, 2, 4, 7, 14, 28), 'fin')))}'''))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ٣')}{timer(2)}</div>''' + quiz('للعدد ٩٥ أربعة عوامل، هي…', ['١ ، ٥ ، ١٩ ، ٩٥', '١ ، ٥ ، ٩ ، ٩٥', '٥ ، ١٩', '١ ، ٣ ، ٥ ، ٩٥'], 0, '٩٥ = ١ × ٩٥ = ٥ × ١٩')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ٢ (هـ)')}</div>''' + quiz('ما عوامل العدد ١١؟', ['١١ فقط', '١ ، ١١', '١ ، ٢ ، ١١', 'ليس له عوامل'], 1, 'العدد ١ عاملٌ لكل عدد، والعدد عاملٌ لنفسه')))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">انتبه ⚠️ خطأ شائع</span>{ref('دليل المعلم ص ٢٥')}</div><h2>عوامل العدد ١٨ = ؟</h2>
<div class="row">
{st(box(f'<div class="col"><span class="wrong">✘</span>{L(2, 3, 6, 9)}<small class="hint">نسي ١ والعدد نفسه</small></div>', style="border-color:var(--bad);background:#FFF5F5"))}
{st(box(f'<div class="col"><span class="right">✔</span>{L(1, 2, 3, 6, 9, 18)}<small class="hint">١ والعدد نفسه عاملان دائماً</small></div>', style="border-color:var(--good);background:#F2FBF5"))}</div>'''))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">نشاط 🎲</span>{ref('دليل المعلم ص ٢٥ · ورقة المصادر ١-٣')}</div><h2>لعبة بطاقات العوامل</h2>
<div class="exit">{st('<div><b>١</b><span>بطاقات الأعداد <em class="kb">١ – ٢٠</em> على الطاولة، ولاعبان: <em class="kb">أ</em> و <em class="kb">ب</em></span></div>')}{st('<div><b>٢</b><span>(أ) يأخذ عدداً، و(ب) يأخذ <em class="kb">كل عوامله</em> المتبقية — ولا يُختار عددٌ ليس له عاملٌ على الطاولة</span></div>')}{st('<div><b>٣</b><span>في النهاية يجمع كلٌّ منهما أعداده، والأكبر مجموعاً يفوز — ثم يتبادلان الأدوار</span></div>')}</div>
<div class="row" style="align-items:center">{timer(8)}</div>'''))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ١ 🎫</span><h2>أجب في دفترك</h2>
<div class="exit">{st('<div><b>١</b>أوجد عوامل العدد ١٠</div>')}{st('<div><b>٢</b>أوجد عوامل العدد ٢٧</div>')}{st('<div><b>٣</b>هل ٧ عاملٌ للعدد ٢٤؟ لماذا؟</div>')}</div>'''))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ١ 🎫</span><h2>الإجابات</h2>
<button class="flip box col" style="min-width:40vw"><span class="tap">👆 اضغط لإظهار الإجابات</span><span class="hid col">{L(1, 2, 5, 10)}{L(1, 3, 9, 27)}<span class="kk">لا — ٢٤ ÷ ٧ لها باقٍ</span></span></button>'''))

# ═══════════ الحصة الثانية: العوامل المشتركة و ع م ك ═══════════
S.append(slide('''<span class="tag">الحصة الثانية · ٤٠ دقيقة</span><h2>العوامل المشتركة و ع م ك</h2>
<div class="plan"><div><b>٥ د</b>إحماء</div><div><b>١٠ د</b>العوامل المشتركة</div><div><b>٥ د</b>ع م ك</div>
<div><b>١٢ د</b>أنا ← نحن ← أنتم</div><div><b>٥ د</b>فكّر</div><div><b>٣ د</b>بطاقة الخروج</div></div>''', 'divider'))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">إحماء 🔥</span>{timer(1)}</div>''' + quiz('العدد ١٨ له ستة عوامل، منها ١ و ١٨. فما الأخرى؟', ['٢ ، ٣ ، ٦ ، ٩', '٢ ، ٤ ، ٦ ، ٩', '٣ ، ٦ ، ٩ ، ١٢', '٢ ، ٣ ، ٤ ، ٦'], 0, '١٨ = ١ × ١٨ = ٢ × ٩ = ٣ × ٦')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('كتاب الطالب ص ٢٤')}</div><h2>العوامل المشتركة للعددين ٢٤ و ٤٠</h2>
<div class="col" style="gap:2vh">
{st(f'<div class="mrow"><b>عوامل ٢٤</b>{L(1, 2, 3, 4, 6, 8, 12, 24, hot=(1, 2, 4, 8))}</div>')}
{st(f'<div class="mrow"><b>عوامل ٤٠</b>{L(1, 2, 4, 5, 8, 10, 20, 40, hot=(1, 2, 4, 8))}</div>')}</div>
{st('<div class="rulebox">العوامل المشتركة: ١ ، ٢ ، ٤ ، ٨ — وأكبرها <b class="c-exp">٨</b> = العامل المشترك الأكبر (ع م ك)</div>')}'''))
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('تمرين ٧ (هـ)')}</div><h2>معاً: العوامل المشتركة للعددين ١٢ و ١٨</h2>
{box(STEPS(STP('عوامل ١٢', L(1, 2, 3, 4, 6, 12, hot=(1, 2, 3, 6))), STP('عوامل ١٨', L(1, 2, 3, 6, 9, 18, hot=(1, 2, 3, 6))), STP('المشتركة · ع م ك', M('١ ، ٢ ، ٣ ، ٦', '←', 'ع م ك', EQ, '٦', cls="sm"), 'fin')))}'''))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ٧ (ب)')}{timer(2)}</div>''' + quiz('العوامل المشتركة للعددين ٢٠ و ٢٥:', ['١ ، ٥', '٥ فقط', '١ ، ٢ ، ٥', '١ ، ٥ ، ١٠'], 0, 'عوامل ٢٠: ١،٢،٤،٥،١٠،٢٠ — عوامل ٢٥: ١،٥،٢٥')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ٨ (ج)')}</div>''' + quiz('ع م ك للعددين ١٦ و ٤٠ هو…', [M('٤'), M('٨'), M('١٦'), M('٢')], 1, 'العوامل المشتركة ١ ، ٢ ، ٤ ، ٨ وأكبرها ٨')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ٧ (ج)')}</div>''' + quiz('العوامل المشتركة للعددين ٨ و ١٥:', ['١ فقط', 'لا يوجد', '١ ، ٣', '١ ، ٥'], 0, 'قد يكون العامل المشترك الوحيد هو ١')))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">فكّر 💡</span>{ref('تمرين ٦')}</div><h2>للعددين ٤ و ٩ ثلاثة عوامل فقط. أوجد عددين آخرين مثلهما</h2>
<button class="flip box col"><span class="tap">👆 الحل</span><span class="hid col">{L(1, 2, 4)}{L(1, 3, 9)}<span class="hint">كلاهما مربّع عددٍ له عاملان فقط (٢×٢ و ٣×٣)</span>{M('٢٥', 'و', '٤٩', cls="mid")}</span></button>'''))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">فكّر 💡</span>{ref('تمرين ٩')}</div><h2>عددٌ أصغر من ٣٠ له ٨ عوامل، وعددٌ أصغر من ٥٠ له ١٠ عوامل</h2>
<button class="flip box col"><span class="tap">👆 الحل</span><span class="hid col">{M('٢٤', ':', cls="sm")}{L(1, 2, 3, 4, 6, 8, 12, 24)}{M('٤٨', ':', cls="sm")}{L(1, 2, 3, 4, 6, 8, 12, 16, 24, 48)}</span></button>'''))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ٢ 🎫</span><h2>أجب في دفترك</h2>
<div class="exit">{st('<div><b>١</b>العوامل المشتركة للعددين ٦ و ١٠</div>')}{st('<div><b>٢</b>ع م ك للعددين ٦ و ١٥</div>')}{st('<div><b>٣</b>ع م ك للعددين ٢٠ و ٥٠</div>')}</div>'''))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ٢ 🎫</span><h2>الإجابات</h2>
<button class="flip box col" style="min-width:40vw"><span class="tap">👆 اضغط لإظهار الإجابات</span><span class="hid col">{L(1, 2)}{M('٣', cls="sm")}{M('١٠', cls="sm")}</span></button>'''))

# ═══════════ الحصة الثالثة: اختبارات قابلية القسمة ═══════════
S.append(slide('''<span class="tag">الحصة الثالثة · ٤٠ دقيقة</span><h2>اختبارات قابلية القسمة</h2>
<div class="plan"><div><b>٥ د</b>إحماء</div><div><b>١٠ د</b>اختبارات ٢ ، ٥ ، ١٠ ، ١٠٠ ، ٤ ، ٨</div><div><b>١٠ د</b>اختبارات ٣ ، ٩ ، ٦</div>
<div><b>١٠ د</b>أنا ← نحن ← أنتم</div><div><b>٥ د</b>بطاقة الخروج</div></div>''', 'divider'))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">إحماء 🔥</span>{timer(1)}</div>''' + quiz('ع م ك للعددين ٨ و ٢٤ هو…', [M('٨'), M('٤'), M('٢٤'), M('٢')], 0, '٨ عاملٌ للعدد ٢٤ نفسه، فهو العامل المشترك الأكبر')))
TESTS1 = [('٢', 'الآحاد ٠ أو ٢ أو ٤ أو ٦ أو ٨'), ('٥', 'الآحاد ٠ أو ٥'), ('١٠', 'الآحاد ٠'), ('١٠٠', 'آخر رقمين ٠٠'),
          ('٤', 'العدد المكوَّن من آخر رقمين يقبل القسمة على ٤'), ('٨', 'العدد المكوَّن من آخر ثلاثة أرقام يقبل القسمة على ٨')]
TESTS2 = [('٣', 'مجموع الأرقام يقبل القسمة على ٣'), ('٩', 'مجموع الأرقام يقبل القسمة على ٩'), ('٦', 'يقبل القسمة على ٢ وعلى ٣ معاً'), ('٧', 'لا يوجد اختبارٌ بسيط')]
for part in (TESTS1[:4], TESTS1[4:], TESTS2):
    S.append(slide(f'''<div class="row hdr"><span class="qbadge">اختبارات قابلية القسمة</span>{ref('كتاب الطالب ص ٢٥')}</div><h2>اضغط على البطاقة لتظهر القاعدة</h2>
<div class="xgrid c2">{''.join(f'<button class="flip xcard dv"><span class="xq">يقبل القسمة على <b>{n}</b></span><span class="tap">👆</span><span class="hid xa">{t}</span></button>' for n, t in part)}</div>'''))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('كتاب الطالب ص ٢٥')}</div><h2>هل ٦٧٨٦ يقبل القسمة على ٣ ؟ وعلى ٩ ؟</h2>
{box(STEPS(STP('مجموع الأرقام', M('٦', PL, '٧', PL, '٨', PL, '٦', EQ, '٢٧', cls="sm")), STP('٢٧ ÷ ٣ و ٢٧ ÷ ٩', M('نعم', 'و', 'نعم', cls="sm"), 'fin')))}'''))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('كتاب الطالب ص ٢٥')}</div><h2>القسمة على ٤ و ٨: ننظر إلى آخر الأرقام فقط</h2>
{box(STEPS(STP('٣٧٢٦ على ٤؟', M('٢٦ ليس مضاعفاً للعدد ٤', '←', 'لا', cls="sm"), 'bad'), STP('٣٧٢٤ على ٤؟', M('٢٤', DV, '٤', EQ, '٦', '←', 'نعم', cls="sm"), 'fin'), STP('١٧٨١٦ على ٨؟', M('٨١٦', DV, '٨', EQ, '١٠٢', '←', 'نعم', cls="sm"), 'fin')))}'''))
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('تمرين ٤')}</div><h2>معاً: ٤٩٠٤ يقبل القسمة على ٨ — فما العدد التالي الذي يقبل القسمة على ٨؟</h2>
{box(STEPS(STP('مضاعفات ٨ متتالية', M('٤٩٠٤', PL, '٨', cls="sm")), STP('العدد التالي', M(EQ, '٤٩١٢', cls="sm"), 'fin')))}'''))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ١١ (ب)')}{timer(2)}</div>''' + quiz('أيّ الأعداد التالية مضاعفٌ للعدد ٦ ؟', [M('٤٢١'), M('١٢٣٤٥'), M('٥٩٤'), M('٦٧٥٥٥')], 2, '٥٩٤ زوجي، ومجموع أرقامه ١٨ يقبل القسمة على ٣')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ١٢ (أ)')}</div>''' + quiz('أيّها مضاعفٌ للعدد ٨ ؟', [M('٥٥٨١٠'), M('٥٥٨١٦'), M('٥٥٨١٢'), M('٥٥٨١٤')], 1, '٨١٦ ÷ ٨ = ١٠٢ بدون باقٍ')))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">فكّر 💡</span>{ref('تمرين ٥')}</div><h2>أيّ الأعداد يختلف عن البقية؟ ١٣ ، ١٧ ، ٢١ ، ٢٣ ، ٢٩</h2>
<button class="flip box col"><span class="tap">👆 الحل</span><span class="hid col">{M('٢١', cls="mid")}<span class="kk">له أربعة عوامل: ١ ، ٣ ، ٧ ، ٢١ — والبقية لكلٍّ منها عاملان فقط</span></span></button>'''))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ٣ 🎫</span><h2>أجب في دفترك</h2>
<div class="exit">{st('<div><b>١</b>هل ٢٧٣ يقبل القسمة على ٣ ؟</div>')}{st('<div><b>٢</b>هل ٥١٦ يقبل القسمة على ٤ ؟</div>')}{st('<div><b>٣</b>هل ٢٨٨٥ يقبل القسمة على ١٠ ؟</div>')}</div>'''))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ٣ 🎫</span><h2>الإجابات</h2>
<button class="flip box col" style="min-width:40vw"><span class="tap">👆 اضغط لإظهار الإجابات</span><span class="hid col"><span class="kk">نعم — ٢ + ٧ + ٣ = ١٢</span><span class="kk">نعم — ١٦ ÷ ٤ = ٤</span><span class="kk">لا — آحاده ٥ لا ٠</span></span></button>'''))
S.append(slide('''<span class="qbadge" style="background:#0A6770;box-shadow:0 4px 0 #05393E">الواجب المنزلي 🏠</span><h2>بعد الحصص</h2>
<div class="exit"><div class="st"><div><b>١</b>صفحة ١٦ في كتاب النشاط (العوامل والعوامل المشتركة)</div></div><div class="st"><div><b>٢</b>صفحة ١٧ في كتاب النشاط (ع م ك وقابلية القسمة)</div></div></div>'''))
S.append(slide(f'''<h2>الخلاصة</h2>
<div class="sumg">
{st(box('<div class="col"><b class="kk c-we">العوامل</b><span>تقسم العدد بدون باقٍ</span><span>نجدها أزواجاً: ١ × ن …</span></div>'))}
{st(box('<div class="col"><b class="kk c-exp">ع م ك</b><span>أكبر عاملٍ مشترك</span>' + M('٢٤ ، ٤٠', '←', '٨') + '</div>'))}
{st(box('<div class="col"><b class="kk c-lcm">قابلية القسمة</b><span>٢ ، ٥ ، ١٠: الآحاد</span><span>٣ ، ٩: مجموع الأرقام</span><span>٤ ، ٨: آخر ٢ أو ٣ أرقام</span></div>'))}</div>'''))

# ═══════════ ملحق: تمارين كتاب الطالب ص٢٦–٢٧ ═══════════
S.append(launch('sb', '٢٦ و ٢٧', note=f'المراجع: كتاب الطالب ص٢٤–٢٧ ودليل المعلم ص٢٥–٢٦ وإجاباته ص٣٦ — {ME}'))
RF = 'نكتب الأزواج: ١ × ن ، ٢ × … ونتوقّف عندما تتكرر'
H = ['أ', 'ب', 'ج', 'د', 'هـ', 'و', 'ز', 'ح']
S.append(ex(1, 'للعدد ١٨ ستة عوامل، منها ١ و ١٨', RF, [('العوامل الأخرى', L(2, 3, 6, 9))], cols=1))
S.append(ex(2, 'أوجد عوامل الأعداد', RF, [(f'({h}) {a(n)}', L(*FACS(n))) for h, n in zip(H, [10, 28, 27, 44, 11, 30, 16, 32])], cols=2))
S.append(ex(3, 'للعدد ٩٥ أربعة عوامل', RF, [('العوامل', L(1, 5, 19, 95))], cols=1))
S.append(ex(4, '٤٩٠٤ يقبل القسمة على ٨ — العدد التالي؟', 'نضيف ٨', [('العدد التالي', M('٤٩٠٤', PL, '٨', EQ, '٤٩١٢'))], cols=1))
S.append(ex(5, 'أيّ الأعداد يختلف: ١٣ ، ١٧ ، ٢١ ، ٢٣ ، ٢٩', 'اكتب عوامل كل عدد', [('العدد المختلف', M('٢١') + '<small>له ٤ عوامل، والبقية لكلٍّ منها عاملان فقط</small>')], cols=1))
S.append(ex(6, 'عددان آخران لهما ثلاثة عوامل فقط', 'مثل ٤ و ٩: مربّع عددٍ له عاملان فقط', [('مثال', M('٢٥', 'و', '٤٩'))], cols=1))
CF = [(6, 10), (20, 25), (8, 15), (8, 24), (12, 18), (20, 50)]
S.append(ex(7, 'أوجد العوامل المشتركة', 'عوامل العدد الأول التي تظهر أيضاً في عوامل الثاني', [(f'({h}) {a(x)} و {a(y)}', L(*[d for d in FACS(x) if y % d == 0])) for h, (x, y) in zip(H, CF)], cols=2))
S.append(ex(8, 'أوجد العوامل المشتركة (والأكبر منها)', 'ع م ك = أكبر عاملٍ مشترك', [(f'({h}) {a(x)} و {a(y)}', L(*[d for d in FACS(x) if y % d == 0]) + f'<small>ع م ك = {a(max(d for d in FACS(x) if y % d == 0))}</small>') for h, (x, y) in zip(H, [(6, 15), (7, 21), (16, 40)])], cols=2,
          note='إجابة الدليل للجزأين (أ) و (ب) هي ع م ك فقط: ٣ و ٧'))
S.append(ex(9, 'عددٌ < ٣٠ له ٨ عوامل، وعددٌ < ٥٠ له ١٠ عوامل', 'جرّب مضاعفات ٦ أو ١٢', [('أصغر من ٣٠', M('٢٤')), ('أصغر من ٥٠', M('٤٨'))], cols=2))
S.append(ex(10, 'أعدادٌ كل عواملها فردية', 'العدد فردي = ناتج ضرب عددين فرديين', [('(أ) ٤ عوامل', M('١٥ ، ٢١ ، ٣٣ ، ٣٥') + '<small>أيٌّ منها</small>'), ('(ب) ٦ عوامل', M('٤٥', 'أو', '٧٥'))], cols=2))
S.append(ex(11, 'الأعداد: ٤٢١ ، ٢٢٢ ، ٥٩٤ ، ١٢٣٤٥ ، ٦٧٥٥٤', 'اختبارات قابلية القسمة', [('(أ) يقبل القسمة على ٣', M('٢٢٢ ، ٥٩٤ ، ١٢٣٤٥ ، ٦٧٥٥٤')), ('(ب) مضاعفٌ للعدد ٦', M('٢٢٢ ، ٥٩٤ ، ٦٧٥٥٤')),
  ('(ج) يقبل القسمة على ٩', M('٥٩٤ ، ٦٧٥٥٤')), ('(د) أحد عوامله ٥', M('١٢٣٤٥'))], cols=2))
S.append(ex(12, 'النمط: ٥٥٨٠٨ ، ٥٥٨١٠ ، … ، ٥٥٨١٨', 'اختبارات قابلية القسمة', [('(١) مضاعفٌ للعدد ١٠', M('٥٥٨١٠')), ('(٢) أحد عوامله ٢', 'كل الأعداد'),
  ('(٣) يقبل القسمة على ٤', M('٥٥٨٠٨ ، ٥٥٨١٢ ، ٥٥٨١٦')), ('(٤) مضاعفٌ للعدد ٨', M('٥٥٨٠٨ ، ٥٥٨١٦')), ('(ب) أوّل مضاعفٍ للعدد ١٠٠', M('٥٥٩٠٠'))], cols=2))

# ═══════════ ملحق: حلول كتاب النشاط ص١٦–١٧ (الإجابات من دليل المعلم ص٤٢) ═══════════
S.append(launch('ab', '١٦ و ١٧', note='الإجابات النهائية من دليل المعلم ص ٤٢'))
NA, NB = 'نشاط ص ١٦ · تمرين', 'نشاط ص ١٧ · تمرين'
S.append(ex(1, 'للعدد ٢٤ عاملان هما ١ و ٢٤', RF, [('باقي العوامل', L(2, 3, 4, 6, 8, 12))], cols=1, src=NA))
S.append(ex(2, 'أوجد عوامل', RF, [(f'({h}) {a(n)}', L(*FACS(n))) for h, n in zip(H, [8, 12, 21, 17, 40])], cols=2, src=NA))
S.append(ex(3, 'أيّ الأعداد ٣ ، ٦ ، ١٦ ، ٢٦ ، ٣٦ ، ٤٦ عامله ٣ ؟', 'مجموع الأرقام يقبل القسمة على ٣', [('الأعداد', M('٣ ، ٦ ، ٣٦'))], cols=1, src=NA))
S.append(ex(4, 'عددان بين ٣٠ و ٤٠ لكلٍّ منهما عاملان فقط', 'اكتب عوامل كل عدد', [('العددان', M('٣١', 'و', '٣٧'))], cols=1, src=NA))
S.append(ex(5, 'أوجد عوامل العدد ٩١', RF, [('العوامل', L(1, 7, 13, 91) + '<small>٩١ = ٧ × ١٣</small>')], cols=1, src=NA))
CF2 = [(12, 15), (20, 30), (8, 24), (15, 32)]
S.append(ex(6, 'أوجد العوامل المشتركة', 'عوامل العدد الأول التي تظهر في الثاني', [(f'({h}) {a(x)} و {a(y)}', L(*[d for d in FACS(x) if y % d == 0])) for h, (x, y) in zip(H, CF2)], cols=2, src=NA))
S.append(ex(7, 'أوجد ع م ك', 'أكبر عاملٍ مشترك', [(f'({h}) {a(x)} و {a(y)}', M(a(max(d for d in FACS(x) if y % d == 0)))) for h, (x, y) in zip(H, CF2)], cols=2, src=NB))
S.append(ex(8, 'أوجد عدداً لديه فقط', 'المربّعات لها عددٌ فردي من العوامل', [('(أ) ٣ عوامل', M('٩', 'أو', '٢٥') + '<small>مثال</small>'), ('(ب) ٥ عوامل', M('١٦', 'أو', '٨١') + '<small>مثال</small>')], cols=2, src=NB))
S.append(ex(9, 'الأعداد: ٢٥٧١ ، ٥٤٢٧ ، ٦٦٢٢ ، ٨٥٦٨', 'مجموع الأرقام', [('(أ) مضاعفات ٣', M('٢٥٧١ ، ٥٤٢٧ ، ٨٥٦٨')), ('(ب) مضاعفات ٩', M('٥٤٢٧ ، ٨٥٦٨'))], cols=2, src=NB))
S.append(ex(10, 'الأعداد: ٢٨٨٤ ، ٢٨٨٥ ، ٢٨٨٦ ، ٢٨٨٧ ، ٢٨٨٨', 'اختبارات قابلية القسمة', [('(أ) مضاعفات ٤', M('٢٨٨٤ ، ٢٨٨٨')), ('(ب) مضاعفات ٥', M('٢٨٨٥')),
  ('(ج) مضاعفات ٦', M('٢٨٨٦')), ('(د) مضاعفات ٨', M('٢٨٨٨')), ('(هـ) مضاعفات ١٠', 'لا يوجد')], cols=2, src=NB))
S.append(ex(11, 'أصغر عددٍ عوامله ٢ ، ٣ ، ٤ ، ٥ ، ٦', 'م م ص للأعداد', [('العدد', M('٦٠'))], cols=1, src=NB))

EXTRA_CSS_OWN = '''
.lst{display:inline-flex;flex-wrap:wrap;gap:.25em;align-items:center;font-family:var(--fh);font-weight:800;font-size:clamp(34px,6.4vh,76px);direction:rtl;justify-content:center}
.lst i{font-style:normal;color:var(--ink2)}
.lst b.cm{border:.08em solid var(--exp);border-radius:50%;padding:0 .18em;color:var(--exp)}
.mrow{display:flex;align-items:center;gap:2vw;background:#fff;border:3px solid var(--line);border-radius:18px;padding:1vh 2vw}
.mrow>b{flex:none;font-size:clamp(28px,5vh,58px);color:var(--ink2)}
.stps{display:flex;flex-direction:column;gap:1.6vh;align-items:stretch}
.stp{display:flex;align-items:center;gap:1.4vw;justify-content:space-between}
.stp .lab{flex:none;font-family:var(--fh);font-weight:800;color:#2563EB;background:#EAF1FF;border-radius:12px;padding:.2em .8em;text-align:center}
.stp.fin .lab{background:var(--good);color:#fff}.stp.fin .m,.stp.fin .lst{color:var(--good)}
.stp.bad .lab{background:#FDE7E3;color:var(--bad)}.stp.bad .m{color:var(--bad)}
.rulebox{font-weight:800;font-size:clamp(28px,5.4vh,64px);background:#EAF7F8;border:4px solid var(--base);border-radius:20px;padding:1.4vh 2vw;text-align:center;line-height:1.5}
.pairs2{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));grid-auto-flow:column;grid-template-rows:repeat(4,auto);gap:1.2vh 2vw;width:min(1500px,92vw)}
.pairs2 .st>div{display:flex;align-items:center;justify-content:space-between;gap:1vw;background:#fff;border:3px solid;border-radius:16px;padding:.6vh 1.4vw}
.pairs2 .ok{border-color:var(--good)}.pairs2 .no{border-color:#E6B3AB;opacity:.75}
.pairs2 small{font-weight:700;font-size:clamp(22px,4.2vh,48px);color:var(--ink2)}
.box .col>.m:not(.mid):not(.sm):not(.big),.pairs2 .m,.hid.col>.m:not(.mid):not(.sm):not(.big){font-size:clamp(34px,6.4vh,76px)}
.exit .kb{font-style:normal;color:var(--exp);font-weight:900}
.xcard.dv .xq b{color:var(--exp);font-size:1.2em}
.sumg{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:2vw;width:min(1600px,94vw)}
.sumg .col span{font-weight:700;font-size:clamp(26px,5vh,60px);line-height:1.4}
.sumg .kk{font-size:clamp(36px,7vh,84px)}
'''

# صفحات تمارين كتاب الطالب لشارة «كتاب الطالب ص … · تمرين …» (common_slides.py)
PG = {'تمرين': [(1, '٢٦'), (11, '٢٧')]}
