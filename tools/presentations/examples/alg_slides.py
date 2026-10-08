# شرائح درس ٢-١ «كتابة العبارات الجبرية» — الصف السابع (٣ حصص، كتاب الطالب ص٤٠–٤٢)
# المراجع: دليل المعلم ص٤٦ (الخطأ الشائع: ترتيب الحدود في الطرح، النشاط: وصفٌ لفظي لعبارة جبرية)، كتاب الطالب ص٤٠–٤٢ (مثال ٢-١)،
# وإجابات الدليل ص٥٤ (كتاب الطالب) وص٥٨ (كتاب النشاط ص٢٦–٢٨).
# python3.12 gen_powers.py alg_slides.py كتابة_العبارات_الجبرية_عرض_تفاعلي.html "كتابة العبارات الجبرية — الصف السابع"

def STP(lab, expr, cls=''): return st(f'<div class="stp {cls}"><span class="lab">{lab}</span>{expr}</div>')
def STEPS(*rows): return '<div class="stps">' + ''.join(rows) + '</div>'
MI = '<span class="x">−</span>'; DV = '<span class="x">÷</span>'
def FR(n, d): return f'<span class="fr"><span>{n}</span><span>{d}</span></span>'
def G(*p): return '<span class="grp">(' + ' '.join(p) + ')</span>'      # قوسان حول عبارة
def V(t): return f'<span class="var">{t}</span>'                                   # المتغيّر بلونٍ مميّز
S = []
ME = 'إعداد: أ. عيسى الحارثي'
S.append(slide(f'''<span class="tag">الصف السابع · الدرس ٢-١</span>
<h1 class="h1s">كتابة العبارات الجبرية</h1>
<p class="lead">كتاب الطالب ص ٤٠ إلى ٤٢ · ثلاث حصص</p>
<p class="lead" style="font-size:clamp(26px,4.8vh,56px)">{ME}</p>''', 'cover'))
CAN = ['أستخدم <b>حرفاً</b> لتمثيل عددٍ مجهول', 'أكتب <b>عبارةً جبرية</b> من وصفٍ لفظي', 'أكتب <b>وصفاً لفظياً</b> لعبارةٍ جبرية']
S.append(slide(f'''<h2>في نهاية هذا الدرس…</h2>
<div class="can">{''.join(f'<div><span class="can-i">✔</span><span><b>أنا أستطيع</b> أن {t}</span></div>' for t in CAN)}</div>'''))
S.append(slide(f'''<h2>مفردات الدرس</h2>
{st('<div class="vocab wide"><div><span>المجهول</span><i>unknown</i></div><div><span>العبارة الجبرية</span><i>expression</i></div><div><span>المتغيّر</span><i>variable</i></div></div>')}
<p class="lead">ثلاث حصص: <b class="c-i">أنا</b> ← <b class="c-we">نحن</b> ← <b class="c-u">أنتم</b></p>'''))

# ═══════════ الحصة الأولى: المتغيّر والعبارة الجبرية ═══════════
S.append(slide('''<span class="tag">الحصة الأولى · ٤٠ دقيقة</span><h2>المتغيّر والعبارة الجبرية</h2>
<div class="plan"><div><b>٥ د</b>تهيئة: إناء الحلوى</div><div><b>٨ د</b>المتغيّر والعبارة</div><div><b>١٠ د</b>مثال ٢-١ (الأعمار)</div>
<div><b>١٠ د</b>نحن ← أنتم</div><div><b>٤ د</b>انتبه</div><div><b>٣ د</b>بطاقة الخروج</div></div>''', 'divider'))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">تهيئة 🤔</span>{ref('كتاب الطالب ص ٤٠')}</div><h2>كم قطعة حلوى في الإناء؟</h2>
<div class="row" style="gap:5vw;align-items:center">{st('<div class="jar"><span>📦</span><b>؟</b></div>')}{st('<p class="lead" style="max-width:22ch">لا نعرف العدد… فنرمز له بحرف: <b class="var">ع</b></p>')}</div>''' + tn('اسأل: كيف نكتب عدداً لا نعرفه؟ دع الطلاب يقترحون قبل أن تكشف الحرف.')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('كتاب الطالب ص ٤٠')}</div><h2>أخذنا ٣ قطع من الإناء</h2>
<div class="row" style="gap:4vw;align-items:center">{st('<div class="jar"><span>📦</span><b>ع</b></div>')}{st('<div class="take">🍬🍬🍬 <small>نأخذ ٣</small></div>')}{st(box(M(V('ع'), MI, '٣', cls="mid"), style="border-color:var(--base)"))}</div>
{st('<div class="note">يتبقّى <b>ع − ٣</b> من الحلوى</div>')}'''))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('كتاب الطالب ص ٤٠')}</div><h2>المتغيّر والعبارة الجبرية</h2>
<div class="defs">{st('<div><b class="kk c-we">المتغيّر</b><span>حرفٌ يمثّل عدداً مجهولاً، مثل ع</span></div>')}{st('<div><b class="kk c-exp">العبارة الجبرية</b><span>أرقامٌ ومتغيّرات وعمليات، مثل ع − ٣</span></div>')}</div>'''))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">انتبه ⚠️</span>{ref('كتاب الطالب ص ٤٠')}</div><h2>العبارة الجبرية لا تحتوي علامة =</h2>
<div class="row">{st(box(f'<div class="col"><span class="right">✔ عبارة جبرية</span>{M(V("س"), PL, "٥")}</div>', style="flex:1;border-color:var(--good)"))}{st(box(f'<div class="col"><span class="wrong">✘ ليست عبارة</span>{M(V("س"), PL, "٥", EQ, "٩")}<small class="hint">هذه معادلة (درس ٢-٥)</small></div>', style="flex:1;border-color:var(--bad)"))}</div>'''))
AGES = [('حسام', 'يبلغ س من العمر', M(V('س'))), ('خالد', 'أكبر من حسام بأربع سنوات', M(V('س'), PL, '٤')), ('آدم', 'أصغر من حسام بسنتين', M(V('س'), MI, '٢')),
        ('قاسم', 'عمره ٣ مرّات عمر حسام', M('٣' + V('س'))), ('معتز', 'عمره نصف عمر حسام', M(FR(V('س'), '٢')))]
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('مثال ٢-١')}</div><h2>اكتب عبارةً جبرية لعمر كلٍّ منهم</h2>
<div class="ages">{''.join(st(f'<div><b>{n}</b><span>{d}</span>{e}</div>') for n, d, e in AGES)}</div>''' + tn('أكبر ← نضيف، أصغر ← نطرح، مرّات ← نضرب، نصف ← نقسم على ٢. ونكتب ٣س لا س٣ ولا ٣ × س.')))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">قاعدة الكتابة ✍️</span>{ref('مثال ٢-١')}</div><h2>كيف نكتب الضرب والقسمة؟</h2>
<div class="row">{st(box(f'<div class="col"><span class="kk">٣ × س</span><span class="hint">نكتبها</span>{M("٣" + V("س"), cls="mid")}<small class="hint">العدد قبل المتغيّر، بلا علامة ×</small></div>', style="flex:1"))}{st(box(f'<div class="col"><span class="kk">س ÷ ٢</span><span class="hint">نكتبها</span>{M(FR(V("س"), "٢"), cls="mid")}<small class="hint">على صورة كسر</small></div>', style="flex:1"))}</div>'''))
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('تمرين ١')}</div><h2>معاً: حقيبة هبة فيها ع من أقراص العدّ</h2>
{box(STEPS(STP('أضافت ٤', M(V('ع'), PL, '٤', cls="sm"), 'fin'), STP('أخذت ٣', M(V('ع'), MI, '٣', cls="sm"), 'fin')))}''' + tn('تبدأ هبة بـ ع في كل جزء (ملاحظة الكتاب).')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ٢ (أ)')}{timer(2)}</div>''' + quiz('درجة الحرارة س، ثم ارتفعت درجتين. العبارة هي…', [M(V('س'), PL, '٢'), M(V('س'), MI, '٢'), M('٢' + V('س')), M(FR(V('س'), '٢'))], 0, 'ارتفعت ← نضيف ٢')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ٢ (ب)')}</div>''' + quiz('صارت الحرارة ضعف ما كانت (س). العبارة هي…', [M(V('س'), PL, '٢'), M('٢' + V('س')), M(FR(V('س'), '٢')), M(V('س'), MI, '٢')], 1, 'ضعف ← نضرب في ٢، ونكتب العدد قبل المتغيّر')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ٣ (ب)')}</div>''' + quiz('عمر علي س، وعمر شريف ص. مجموع عمريهما…', [M(V('س'), PL, V('ص')), M(V('س') + V('ص')), M('٢' + V('س')), M(V('س'), MI, V('ص'))], 0, 'مجموع ← نجمع المتغيّرين')))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ١ 🎫</span><h2>اكتب عبارةً جبرية</h2>
<div class="exit">{st('<div><b>١</b>لدى سعاد ع تفاحة، وأعطاها زياد ٥</div>')}{st('<div><b>٢</b>عمر أخي أصغر من عمري (ن) بثلاث سنوات</div>')}{st('<div><b>٣</b>نصف عدد الطلاب (ط)</div>')}</div>'''))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ١ 🎫</span><h2>الإجابات</h2>
<button class="flip box col" style="min-width:40vw"><span class="tap">👆 اضغط لإظهار الإجابات</span><span class="hid col">{M(V('ع'), PL, '٥', cls="sm")}{M(V('ن'), MI, '٣', cls="sm")}{M(FR(V('ط'), '٢'), cls="sm")}</span></button>'''))

# ═══════════ الحصة الثانية: من الكلمات إلى الرموز ═══════════
S.append(slide('''<span class="tag">الحصة الثانية · ٤٠ دقيقة</span><h2>من الكلمات إلى الرموز</h2>
<div class="plan"><div><b>٥ د</b>إحماء</div><div><b>٨ د</b>قاموس الكلمات</div><div><b>٧ د</b>انتبه: ترتيب الطرح</div>
<div><b>١٢ د</b>أنا ← نحن ← أنتم</div><div><b>٥ د</b>تكلفة التذاكر</div><div><b>٣ د</b>بطاقة الخروج</div></div>''', 'divider'))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">إحماء 🔥</span>{timer(1)}</div>''' + quiz('أيّ مما يلي عبارة جبرية؟', [M(V('ص'), PL, '٧', EQ, '١٠'), M('٤' + V('ص'), MI, '١'), M('٣', PL, '٤', EQ, '٧'), M('١٢')], 1, 'فيها متغيّر ولا تحتوي علامة =')))
DICT = [('+', 'أضِف · يزيد · أكثر من · أكبر من · مجموع · اشترى', 'c-good'), ('−', 'اطرح · أقلّ من · أصغر من · أخذ · استخدم · أنفق', 'c-bad'),
        ('×', 'اضرب · ضعف · مرّات · لكلّ واحد', 'c-we'), ('÷', 'اقسم · نصف · ربع · على', 'c-exp')]
S.append(slide(f'''<div class="row hdr">{mode('i')}<span class="qbadge">قاموس الجبر 📖</span></div><h2>كلماتٌ تدلّ على العمليات</h2>
<div class="dict">{''.join(st(f'<div><b class="{c}">{o}</b><span>{w}</span></div>') for o, w, c in DICT)}</div>''' + tn('اطلب من الطلاب إضافة كلمات من عندهم لكل عملية.')))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">انتبه ⚠️ خطأ شائع</span>{ref('دليل المعلم ص ٤٦')}</div><h2>«٢ أقلّ من س» = ؟</h2>
<div class="row">{st(box(f'<div class="col"><span class="wrong">✘</span>{M("٢", MI, V("س"))}</div>', style="flex:1;border-color:var(--bad);background:#FFF5F5"))}{st(box(f'<div class="col"><span class="right">✔</span>{M(V("س"), MI, "٢")}<small class="hint">نبدأ بـ س ثم نطرح منها ٢</small></div>', style="flex:1;border-color:var(--good);background:#F2FBF5"))}</div>''' + tn('في الطرح يهمّ الترتيب: «اطرح ٢ من س» = س − ٢ ، و«اطرح س من ٢» = ٢ − س.')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('تمرين ٤')}</div><h2>تفكّر فاطمة في عدد ل</h2>
{box(STEPS(STP('تضربه في ٣', M('٣' + V('ل'), cls="sm")), STP('تضربه في ٤ ثم تضيف ١', M('٤' + V('ل'), PL, '١', cls="sm")), STP('تقسمه على ٣', M(FR(V('ل'), '٣'), cls="sm"), 'fin')))}'''))
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('تمرين ٤ (د)')}</div><h2>معاً: تقسم العدد ل على ٢ ثم تطرح منه ٩</h2>
{box(STEPS(STP('أولاً: نقسم على ٢', M(FR(V('ل'), '٢'), cls="sm")), STP('ثانياً: نطرح ٩', M(FR(V('ل'), '٢'), MI, '٩', cls="sm"), 'fin')))}'''))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ٣ (أ)')}{timer(2)}</div>''' + quiz('لدى خالد س من الأقراص، واشترى ٦ أخرى. كم لديه الآن؟', [M(V('س'), PL, '٦'), M('٦' + V('س')), M(V('س'), MI, '٦'), M('٦', MI, V('س'))], 0, 'اشترى ← يزيد العدد، فنضيف ٦')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ٣ (ج)')}</div>''' + quiz('تتّسع البطاقة لـ ل صورة. كم صورة في ٣ بطاقات؟', [M(V('ل'), PL, '٣'), M('٣' + V('ل')), M(FR(V('ل'), '٣')), M(V('ل'))], 1, '٣ بطاقات × ل صورة = ٣ل')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('تمرين ٥')}</div><h2>تذكرة البالغ ع ريال، وتذكرة الطفل ل ريال</h2>
{box(STEPS(STP('بالغ وطفل', M(V('ع'), PL, V('ل'), cls="sm")), STP('بالغان وطفل', M('٢' + V('ع'), PL, V('ل'), cls="sm")), STP('٤ بالغين و ٥ أطفال', M('٤' + V('ع'), PL, '٥' + V('ل'), cls="sm"), 'fin')))}''' + tn('نضرب عدد التذاكر في سعر التذكرة، ثم نجمع.')))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ٢ 🎫</span><h2>اكتب عبارةً جبرية</h2>
<div class="exit">{st('<div><b>١</b>٥ أقلّ من العدد م</div>')}{st('<div><b>٢</b>اضرب العدد ك في ٦ ثم أضِف ٢</div>')}{st('<div><b>٣</b>ثمن ٣ دفاتر، ثمن الدفتر د ريال</div>')}</div>'''))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ٢ 🎫</span><h2>الإجابات</h2>
<button class="flip box col" style="min-width:40vw"><span class="tap">👆 اضغط لإظهار الإجابات</span><span class="hid col">{M(V('م'), MI, '٥', cls="sm")}{M('٦' + V('ك'), PL, '٢', cls="sm")}{M('٣' + V('د'), cls="sm")}</span></button>'''))

# ═══════════ الحصة الثالثة: عمليتان والأقواس، والوصف اللفظي ═══════════
S.append(slide('''<span class="tag">الحصة الثالثة · ٤٠ دقيقة</span><h2>عمليتان متتاليتان والأقواس</h2>
<div class="plan"><div><b>٥ د</b>إحماء</div><div><b>١٠ د</b>طريقة سالم</div><div><b>١٠ د</b>نحن ← أنتم</div>
<div><b>١٠ د</b>نشاط: صِف العبارة</div><div><b>٥ د</b>بطاقة الخروج</div></div>''', 'divider'))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">إحماء 🔥</span>{timer(1)}</div>''' + quiz('«اضرب ع في ٣ ثم أضِف ٢» تُكتب…', [M('٣' + V('ع'), PL, '٢'), M('٣', G(V('ع'), PL, '٢')), M('٢' + V('ع'), PL, '٣'), M(V('ع'), PL, '٥')], 0, 'الضرب أولاً ثم الإضافة، فلا نحتاج إلى أقواس')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('تمرين ٦ · طريقة سالم')}</div><h2>يضيف ٢ إلى العدد ع، ثم يضرب الناتج في ٥</h2>
{box(STEPS(STP('أولاً: يضيف ٢', M(V('ع'), PL, '٢', cls="sm")), STP('ثانياً: الناتج كلّه × ٥', M(G(V('ع'), PL, '٢'), X, '٥', cls="sm")), STP('نكتبها أيضاً', M('٥', G(V('ع'), PL, '٢'), cls="sm"), 'fin')))}''' + tn('القوسان يجعلان العملية الأولى تُنفَّذ أولاً (ترتيب العمليات، درس ١-٧).')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('تمرين ٦ · طريقة سالم')}</div><h2>يطرح ٣ من العدد ع، ثم يقسم الناتج على ٢</h2>
{box(STEPS(STP('أولاً: يطرح ٣', M(V('ع'), MI, '٣', cls="sm")), STP('ثانياً: الناتج كلّه ÷ ٢', M(G(V('ع'), MI, '٣'), DV, '٢', cls="sm")), STP('نكتبها أيضاً', M(FR(M(V('ع'), MI, '٣'), '٢'), cls="sm"), 'fin')))}'''))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">قارن 🔍</span>{ref('تمرين ٧')}</div><h2>الترتيب يغيّر العبارة</h2>
<div class="row">{st(box(f'<div class="col"><span class="hint">اضرب ع في ٣ ثم أضِف ٢</span>{M("٣" + V("ع"), PL, "٢")}</div>', style="flex:1"))}{st(box(f'<div class="col"><span class="hint">أضِف ٢ إلى ع ثم اضرب في ٣</span>{M("٣", G(V("ع"), PL, "٢"))}</div>', style="flex:1"))}</div>'''))
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('تمرين ٦ (أ)')}</div><h2>معاً: يضيف ٥ للعدد ع، ثم يضرب الناتج في ٣</h2>
<button class="flip box col"><span class="tap">👆 الحل</span><span class="hid col">{M(G(V('ع'), PL, '٥'), X, '٣', cls="sm")}{M(EQ, '٣', G(V('ع'), PL, '٥'), cls="sm")}</span></button>'''))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ٦ (ج)')}{timer(2)}</div>''' + quiz('يطرح ٢ من العدد ع، ثم يقسم الناتج على ٥', [M(FR(M(V('ع'), MI, '٢'), '٥')), M(V('ع'), MI, FR('٢', '٥')), M('٥' + V('ع'), MI, '٢'), M('٢', MI, FR(V('ع'), '٥'))], 0, 'الطرح أولاً، ثم نقسم الناتج كلّه')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ٦ (د)')}</div>''' + quiz('يطرح ٩ من العدد ع، ثم يضرب الناتج في ٨', [M('٨' + V('ع'), MI, '٩'), M('٨', G(V('ع'), MI, '٩')), M('٩', G(V('ع'), MI, '٨')), M(V('ع'), MI, '٧٢')], 1, 'الطرح أولاً داخل القوسين، ثم الضرب')))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">نشاط 🗣️</span>{ref('دليل المعلم ص ٤٦')}</div><h2>صِف كل عبارة بجملةٍ من حياتك</h2>
<div class="cards3">{''.join(st(box(M(*e, cls="sm")), 'div') for e in ([V('س'), PL, '٥'], [V('س'), MI, '١٠'], ['٢' + V('س')], [FR(V('س'), '٢')]))}</div>''' + tn('مثال: س + ٥ ← لدى سمير س قلماً وأعطاه والده ٥ أقلام. ذكّرهم أن س + ٥ يمكن أن تعطي عدداً لا نهائياً من الأعداد.')))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">فكّر 💡</span>{ref('تمرين ٧')}</div><h2>صِف العبارة {M('٢', MI, FR(V('ع'), '٣'), cls="sm")}</h2>
<button class="flip box col"><span class="tap">👆 الوصف</span><span class="hid col"><span class="kk">اقسم ع على ٣ ، ثم اطرح الناتج من ٢</span></span></button>'''))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ٣ 🎫</span><h2>اكتب عبارةً جبرية</h2>
<div class="exit">{st('<div><b>١</b>أضِف ٤ إلى ن ، ثم اضرب الناتج في ٢</div>')}{st('<div><b>٢</b>اطرح ١ من ن ، ثم اقسم الناتج على ٦</div>')}{st('<div><b>٣</b>اضرب ن في ٥ ، ثم اطرح الناتج من ٣</div>')}</div>'''))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ٣ 🎫</span><h2>الإجابات</h2>
<button class="flip box col" style="min-width:40vw"><span class="tap">👆 اضغط لإظهار الإجابات</span><span class="hid col">{M('٢', G(V('ن'), PL, '٤'), cls="sm")}{M(FR(M(V('ن'), MI, '١'), '٦'), cls="sm")}{M('٣', MI, '٥' + V('ن'), cls="sm")}</span></button>'''))
S.append(slide('''<span class="qbadge" style="background:#0A6770;box-shadow:0 4px 0 #05393E">الواجب المنزلي 🏠</span><h2>بعد الحصص</h2>
<div class="exit"><div class="st"><div><b>١</b>صفحتا ٢٦ و ٢٧ في كتاب النشاط</div></div><div class="st"><div><b>٢</b>صفحة ٢٨ في كتاب النشاط (صِل الوصف بالعبارة)</div></div></div>'''))
S.append(slide(f'''<h2>الخلاصة</h2>
<div class="sumg">
{st(box('<div class="col"><b class="kk c-we">المتغيّر</b><span>حرفٌ لعددٍ مجهول</span>' + M(V('س')) + '</div>'))}
{st(box('<div class="col"><b class="kk c-exp">العبارة الجبرية</b><span>أرقام ومتغيّرات، بلا =</span>' + M('٣' + V('س'), PL, '٢') + '</div>'))}
{st(box('<div class="col"><b class="kk c-lcm">عمليتان</b><span>القوسان للعملية الأولى</span>' + M('٥', G(V('ع'), PL, '٢')) + '</div>'))}</div>'''))

# ═══════════ ملحق: تمارين كتاب الطالب ص٤١–٤٢ (الإجابات من دليل المعلم ص٥٤) ═══════════
S.append(launch('sb', '٤١ و ٤٢', note=f'المراجع: كتاب الطالب ص٤٠ إلى ٤٢، ودليل المعلم ص٤٦ وإجاباته ص٥٤ · {ME}'))
H = ['أ', 'ب', 'ج', 'د', 'هـ', 'و', 'ز', 'ح']
RW = 'نحدّد العملية من الكلمات، ونكتب العدد قبل المتغيّر'
S.append(ex(1, 'حقيبة هبة فيها ع من أقراص العدّ', RW, [('(أ) أضافت ٤', M(V('ع'), PL, '٤')), ('(ب) أخذت ٣', M(V('ع'), MI, '٣'))], cols=2))
S.append(ex(2, 'درجة الحرارة يوم الثلاثاء س', RW, [('(أ) ترتفع درجتين', M(V('س'), PL, '٢')), ('(ب) تصير ضعفها', M('٢' + V('س')))], cols=2))
S.append(ex(3, 'اكتب العبارة الجبرية', RW, [('(أ) خالد: س واشترى ٦', M(V('س'), PL, '٦')), ('(ب) مجموع العمرين س و ص', M(V('س'), PL, V('ص'))), ('(ج) صور ٣ بطاقات', M('٣' + V('ل')))], cols=2))
S.append(ex(4, 'تفكّر فاطمة في عدد ل', RW, [('(أ) تضربه في ٣', M('٣' + V('ل'))), ('(ب) × ٤ ثم تضيف ١', M('٤' + V('ل'), PL, '١')),
  ('(ج) تقسمه على ٣', M(FR(V('ل'), '٣'))), ('(د) ÷ ٢ ثم تطرح ٩', M(FR(V('ل'), '٢'), MI, '٩'))], cols=2))
S.append(ex(5, 'تذكرة البالغ ع ريال، والطفل ل ريال', 'عدد التذاكر × السعر، ثم نجمع', [('(أ) بالغ وطفل', M(V('ع'), PL, V('ل'))), ('(ب) بالغان وطفل', M('٢' + V('ع'), PL, V('ل'))), ('(ج) ٤ بالغين و ٥ أطفال', M('٤' + V('ع'), PL, '٥' + V('ل')))], cols=2))
S.append(ex(6, 'طريقة سالم: يفكّر راشد في عدد ع', 'العملية الأولى داخل القوسين', [('(أ) +٥ ثم × ٣', M('٣', G(V('ع'), PL, '٥'))), ('(ب) +٧ ثم ÷ ٤', M(FR(M(V('ع'), PL, '٧'), '٤'))),
  ('(ج) −٢ ثم ÷ ٥', M(FR(M(V('ع'), MI, '٢'), '٥'))), ('(د) −٩ ثم × ٨', M('٨', G(V('ع'), MI, '٩')))], cols=2))
S.append(ex(7, 'صِل كل وصف بالعبارة الصحيحة', 'اقرأ الوصف خطوةً خطوة ثم ابحث عن العبارة', [('(أ) × ٣ واطرحه من ٢', M('٢', MI, '٣' + V('ع')) + '<small>العبارة ٣</small>'), ('(ب) +٢ ثم × ٣', M('٣', G(V('ع'), PL, '٢')) + '<small>العبارة ٥</small>'),
  ('(ج) × ٣ واطرح منه ٢', M('٣' + V('ع'), MI, '٢') + '<small>العبارة ٤</small>'), ('(د) × ٣ وأضِف ٢', M('٢', PL, '٣' + V('ع')) + '<small>العبارة ١</small>'),
  ('(هـ) +٢ ثم ÷ ٣', M(FR(M(V('ع'), PL, '٢'), '٣')) + '<small>العبارة ٧</small>'), ('(و) ÷ ٣ وأضِف ٢', M('٢', PL, FR(V('ع'), '٣')) + '<small>العبارة ٢</small>'),
  ('العبارة المتبقية ٦', M('٢', MI, FR(V('ع'), '٣')) + '<small>اقسم ع على ٣ ثم اطرح الناتج من ٢</small>')], cols=2, per=3))

# ═══════════ ملحق: حلول كتاب النشاط ص٢٦–٢٨ (الإجابات من دليل المعلم ص٥٨) ═══════════
S.append(launch('ab', '٢٦ إلى ٢٨', note='الإجابات النهائية من دليل المعلم ص ٥٨'))
NA, NB, NC = 'نشاط ص ٢٦ · تمرين', 'نشاط ص ٢٧ · تمرين', 'نشاط ص ٢٨ · تمرين'
S.append(ex(1, 'صندوق مهند فيه ر من الدمى', RW, [('(أ) يضيف ٤', M(V('ر'), PL, '٤')), ('(ب) يأخذ ٢', M(V('ر'), MI, '٢')), ('(ج) يضيف ٥', M(V('ر'), PL, '٥')), ('(د) يأخذ نصفها', M(FR(V('ر'), '٢')))], cols=2, src=NA))
S.append(ex(2, 'لدى ماهر د من الحلوى، ولدى حاتم ل', 'نعبّر عن عدد حاتم بدلالة د', [('(أ) تزيد بقطعتين', M(V('د'), PL, '٢')), ('(ب) تزيد بثلاث', M(V('د'), PL, '٣')), ('(ج) تقلّ بستّ', M(V('د'), MI, '٦')), ('(د) نصف ما لدى ماهر', M(FR(V('د'), '٢')))], cols=2, src=NA))
S.append(ex(3, 'اكتب عبارةً جبرية', RW, [('(أ) س واشترى ٢', M(V('س'), PL, '٢')), ('(ب) ر واستخدم ١٥', M(V('ر'), MI, '١٥')), ('(ج) مجموع العمرين', M(V('ح'), PL, V('ط'))),
  ('(د) بطاقتان سعة كلٍّ ط', M('٢' + V('ط'))), ('(هـ) ربع المال د', M(FR(V('د'), '٤')))], cols=2, src=NA))
S.append(ex(4, 'تفكّر نسرين في عدد ع', RW, [('(أ) × ٦', M('٦' + V('ع'))), ('(ب) × ٥ ثم +١', M('٥' + V('ع'), PL, '١')), ('(ج) × ٧ ثم +٢', M('٧' + V('ع'), PL, '٢')),
  ('(د) ÷ ٤', M(FR(V('ع'), '٤'))), ('(هـ) ÷ ٢ ثم +١٠', M(FR(V('ع'), '٢'), PL, '١٠')), ('(و) ÷ ٥ ثم −٣', M(FR(V('ع'), '٥'), MI, '٣'))], cols=2, src=NB))
S.append(ex(5, 'وجبة الكبار هـ ريال، ووجبة الطفل و ريال', 'عدد الوجبات × السعر، ثم نجمع', [('(أ) كبير وطفل', M(V('هـ'), PL, V('و'))), ('(ب) كبير و ٣ أطفال', M(V('هـ'), PL, '٣' + V('و'))),
  ('(ج) ٤ كبار وطفل', M('٤' + V('هـ'), PL, V('و'))), ('(د) ٤ كبار و ٥ أطفال', M('٤' + V('هـ'), PL, '٥' + V('و')))], cols=2, src=NB))
S.append(ex(6, 'تفكّر فاطمة في عدد س', 'العملية الأولى داخل القوسين', [('(أ) +٢ ثم × ٣', M('٣', G(V('س'), PL, '٢'))), ('(ب) +٢ ثم ÷ ٣', M(FR(M(V('س'), PL, '٢'), '٣'))),
  ('(ج) −٥ ثم × ٤', M('٤', G(V('س'), MI, '٥'))), ('(د) −٥ ثم ÷ ٤', M(FR(M(V('س'), MI, '٥'), '٤')))], cols=2, src=NB))
S.append(ex(7, 'صِل كل وصف بالعبارة الصحيحة', 'اقرأ الوصف خطوةً خطوة ثم ابحث عن العبارة', [('(أ) × ٥ ثم اطرح ٤', M('٥' + V('س'), MI, '٤') + '<small>العبارة ٥</small>'), ('(ب) +٤ ثم × ٥', M('٥', G(V('س'), PL, '٤')) + '<small>العبارة ١</small>'),
  ('(ج) × ٥ ثم اطرحه من ٤', M('٤', MI, '٥' + V('س')) + '<small>العبارة ٣</small>'), ('(د) × ٥ وأضِف ٤', M('٤', PL, '٥' + V('س')) + '<small>العبارة ٤</small>'),
  ('(هـ) +٤ ثم ÷ ٥', M(FR(M(V('س'), PL, '٤'), '٥')) + '<small>العبارة ٧</small>'), ('(و) ÷ ٥ وأضِف ٤', M('٤', PL, FR(V('س'), '٥')) + '<small>العبارة ٢</small>'),
  ('العبارة المتبقية ٦', M('٤', MI, FR(V('س'), '٥')) + '<small>اقسم س على ٥ ثم اطرح الناتج من ٤</small>')], cols=2, src=NC, per=3))

EXTRA_CSS_OWN = '''
.var{color:var(--exp);font-weight:900}
.fr{display:inline-flex;flex-direction:column;align-items:center;line-height:1.05;vertical-align:middle;margin:0 .1em}
.fr>span:first-child{border-bottom:.07em solid currentColor;padding:0 .15em .04em;align-self:stretch;text-align:center}
.grp{display:inline-flex;gap:.2em;align-items:center;direction:rtl;unicode-bidi:isolate}
.stps{display:flex;flex-direction:column;gap:1.6vh;align-items:stretch}
.stp{display:flex;align-items:center;gap:1.6vw;justify-content:space-between}
.stp .lab{flex:none;font-family:var(--fh);font-weight:800;color:#2563EB;background:#EAF1FF;border-radius:12px;padding:.2em .8em;text-align:center}
.stp.fin .lab{background:var(--good);color:#fff}.stp.fin .m{color:var(--good)}
.box .col>.m:not(.mid):not(.sm):not(.big),.hid.col>.m:not(.mid):not(.sm):not(.big){font-size:clamp(34px,6.4vh,76px)}
.jar{display:flex;flex-direction:column;align-items:center;font-size:clamp(90px,20vh,230px);line-height:1}
.jar b{font-family:var(--fh);font-size:.45em;color:var(--exp);margin-top:.08em}
.take{font-size:clamp(40px,8vh,96px);display:flex;flex-direction:column;align-items:center}.take small{font-size:clamp(22px,4.2vh,48px);font-weight:800;color:var(--ink2)}
.defs{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:2vw;width:min(1500px,92vw)}
.defs .st>div{display:flex;flex-direction:column;gap:1vh;align-items:center;background:#fff;border:3px solid var(--line);border-radius:20px;padding:2.4vh 2vw;text-align:center}
.defs .st>div>span{font-weight:700;font-size:clamp(26px,5vh,58px);line-height:1.4}
.ages{display:flex;flex-direction:column;gap:1.1vh;width:min(1300px,90vw)}
.ages .st>div{display:grid;grid-template-columns:7em 1fr auto;align-items:center;gap:1.4vw;background:#fff;border:3px solid var(--line);border-radius:16px;padding:.5vh 1.6vw}
.ages .st>div>b{font-family:var(--fh);font-size:clamp(26px,4.8vh,56px);color:#2563EB}.ages .st>div>span{font-weight:700;font-size:clamp(22px,4.2vh,48px);color:var(--ink2)}
.ages .st>div>.m{font-size:clamp(30px,5.8vh,68px)}
.dict{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1.6vh 1.6vw;width:min(1500px,92vw)}
.dict .st>div{display:flex;align-items:center;gap:1.4vw;background:#fff;border:3px solid var(--line);border-radius:18px;padding:1.2vh 1.4vw}
.dict b{flex:none;font-family:var(--fh);font-size:clamp(50px,10vh,120px);width:1.2em;text-align:center}
.dict .st>div>span{font-weight:700;font-size:clamp(22px,4.2vh,48px);line-height:1.45}
.cards3{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:1.6vw;width:min(1500px,92vw)}
.cards3 .box{display:flex;justify-content:center}
.exit .kb{font-style:normal;color:var(--exp);font-weight:900}
.sumg{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:2vw;width:min(1600px,94vw)}
.sumg .col span{font-weight:700;font-size:clamp(26px,4.6vh,56px);line-height:1.4}
.sumg .kk{font-size:clamp(34px,6.4vh,76px)}
'''

# صفحات تمارين كتاب الطالب لشارة «كتاب الطالب ص … · تمرين …» (common_slides.py)
PG = {'تمرين': [(1, '٤١'), (6, '٤٢')]}
