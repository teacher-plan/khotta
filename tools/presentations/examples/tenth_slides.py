# شرائح درس ٣-٧ «الضرب في ٠٫١ أو ٠٫٠١ والقسمة عليهما» — الصف السابع (٣ حصص، كتاب الطالب ص٧٠–٧٣)
# المراجع: دليل المعلم ص٧٣–٧٤ (قوى العدد ١٠ وعدد الأصفار يمين ١؛ الأخطاء الشائعة: ٠٫١ = ١/١٠ و ٠٫٠١ = ١/١٠٠، والقسمة على ٠٫١ = الضرب في ١٠؛
# النشاط: ورقة المصادر ٣-٧ بمسابقة «من ينفذ أولاً»؛ التمرين ٥ العمليات العكسية، ٩ و ١٠ التفكير)،
# كتاب الطالب ص٧٠–٧٣ (مثالا ٣-٧أ و ٣-٧ب)، وإجابات الدليل ص٧٩ (كتاب الطالب) وص٨٣ (كتاب النشاط ص٥٢–٥٤).
# python3.12 gen_powers.py tenth_slides.py الضرب_في_٠٫١_و٠٫٠١_عرض_تفاعلي.html "الضرب في ٠٫١ أو ٠٫٠١ والقسمة عليهما — الصف السابع"
exec(open(os.path.join(HERE, 'vcol.py'), encoding='utf-8').read())

DV = '<span class="x">÷</span>'
def FR(n, d): return f'<span class="frc"><span>{n}</span><span>{d}</span></span>'
def STP(lab, expr='', cls=''): return st(f'<div class="stp {cls}"><span class="lab">{lab}</span>{expr}</div>')
def STEPS(*rows): return '<div class="stps">' + ''.join(rows) + '</div>'
def VB(h): return f'<div class="vbox">{h}</div>'
T = '١٠'
S = []
ME = 'إعداد: أ. عيسى الحارثي'
S.append(slide(f'''<span class="tag">الصف السابع · الدرس ٣-٧</span>
<h1 class="h1s">الضرب في ٠٫١ أو ٠٫٠١ والقسمة عليهما</h1>
<p class="lead">كتاب الطالب ص ٧٠ إلى ٧٣ · ثلاث حصص</p>
<p class="lead" style="font-size:clamp(26px,4.8vh,56px)">{ME}</p>''', 'cover'))
CAN = ['أكتب الأعداد ١٠ و ١٠٠ و ١٠٠٠ … <b>بقوى العدد ١٠</b>', 'أضرب في <b>٠٫١ أو ٠٫٠١</b> بالقسمة على ١٠ أو ١٠٠', 'أقسم على <b>٠٫١ أو ٠٫٠١</b> بالضرب في ١٠ أو ١٠٠، وأتحقّق بالعملية العكسية']
S.append(slide(f'''<h2>في نهاية هذا الدرس…</h2>
<div class="can">{''.join(f'<div><span class="can-i">✔</span><span><b>أنا أستطيع</b> أن {t}</span></div>' for t in CAN)}</div>'''))
S.append(slide(f'''<h2>مفردات الدرس</h2>
{st('<div class="vocab wide"><div><span>قوى العدد عشرة</span><i>powers of 10</i></div><div><span>الأُس</span><i>index</i></div><div><span>العملية العكسية</span><i>inverse operation</i></div></div>')}
<p class="lead">ثلاث حصص: <b class="c-i">أنا</b> ← <b class="c-we">نحن</b> ← <b class="c-u">أنتم</b></p>'''))

# ═══════════ الحصة الأولى: قوى العدد ١٠ ═══════════
S.append(slide('''<span class="tag">الحصة الأولى · ٤٠ دقيقة</span><h2>قوى العدد ١٠</h2>
<div class="plan"><div><b>٤ د</b>تهيئة</div><div><b>٨ د</b>نمط قوى ١٠</div><div><b>٨ د</b>مثال ٣-٧أ</div>
<div><b>٧ د</b>نحن</div><div><b>٨ د</b>أنتم</div><div><b>٥ د</b>بطاقة الخروج</div></div>''', 'divider'))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">تهيئة 🤔</span></div><h2>كم صفراً في المليون؟</h2>
{st(f'<div class="note">١٠ × ١٠ × ١٠ × ١٠ × ١٠ × ١٠ = {M("١٠٠٠٠٠٠", cls="sm")}</div>')}
{st('<div class="note">ستة أصفار، ورقم ١٠ مضروبٌ في نفسه ست مرات</div>')}''' + tn('من خارج المرجع: سؤال تمهيدي يربط عدد الأصفار بعدد مرات الضرب في ١٠ (نقطة الدليل الأولى).')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('كتاب الطالب ص ٧٠')}</div><h2>نمط قوى العدد ١٠</h2>
<table class="pwt">{''.join(f'<tr class="st"><td>{M(_ar(n), cls="sm")}</td><td>{M(f, cls="sm")}</td><td>{M(P("10", e), cls="sm")}</td><td class="w">{w}</td></tr>' for n, f, e, w in (
  ('10', '١٠', 1, 'عشرة'), ('100', '١٠ × ١٠', 2, 'مئة: مربّع العدد ١٠'), ('1000', '١٠ × ١٠ × ١٠', 3, 'ألف: مكعّب العدد ١٠'), ('10000', '١٠ × ١٠ × ١٠ × ١٠', 4, 'عشرة آلاف')))}</table>
{st('<div class="note">قيمة الأُس = عدد الأصفار يمين الرقم ١</div>')}''' + tn('الأُس يعبّر عن عدد العشرات المضروبة في بعضها، وعن عدد الأصفار يمين ١ (من الكتاب والدليل).')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('مثال ٣-٧أ (١)')}</div><h2>اكتب {P('10', 6)} بالأعداد والكلمات</h2>
<div class="row vrow">{STEPS(STP('الأُس ٦ ← ستة أصفار يمين ١', M('١٠٠٠٠٠٠', cls='sm')), STP('بالكلمات', M('مليون', cls='sm'), 'fin'))}</div>'''))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('مثال ٣-٧أ (٢)')}</div><h2>اكتب ١٠٠٠٠٠ بقوى العدد ١٠</h2>
<div class="row vrow">{STEPS(STP('نعدّ الأصفار يمين ١', M('خمسة أصفار', cls='sm')), STP('الأُس ٥', M('١٠٠٠٠٠', EQ, P('10', 5), cls='sm'), 'fin'))}</div>'''))
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('تمرين ١ (أ، ب)')}</div><h2>معاً: اكتب بالأعداد والكلمات</h2>
<div class="row">{st(f'<button class="flip box col" style="flex:1"><span class="hint">{P("10", 3)}</span><span class="tap">👆</span><span class="hid col">{M("١٠٠٠", cls="sm")}<b class="w2">ألف</b></span></button>')}{st(f'<button class="flip box col" style="flex:1"><span class="hint">{P("10", 5)}</span><span class="tap">👆</span><span class="hid col">{M("١٠٠٠٠٠", cls="sm")}<b class="w2">مئة ألف</b></span></button>')}</div>'''))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ١ (ج)')}{timer(1)}</div>''' + quiz(f'{P("10", 7)} = ؟', [M('١٠٠٠٠٠٠'), M('١٠٠٠٠٠٠٠'), M('٧٠'), M('١٠٠٠٠٠٠٠٠')], 1, 'سبعة أصفار يمين ١: عشرة ملايين')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ٢ (ب)')}</div>''' + quiz('اكتب ١٠٠٠٠٠٠٠ بقوى العدد ١٠', [M(P('10', 8)), M(P('10', 7)), M(P('10', 6)), M(P('10', 1))], 1, 'سبعة أصفار يمين ١: ١٠ أُس ٧')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ١ (د)')}</div>''' + quiz(f'{P("10", 1)} = ؟', [M('١'), M('١٠'), M('٠'), M('١١')], 1, 'صفرٌ واحد يمين ١: عشرة')))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ١ 🎫</span><h2>اكتب</h2>
<div class="exit">{st(f'<div><b>١</b>{P("10", 4)} بالأعداد والكلمات</div>')}{st('<div><b>٢</b>١٠٠ بقوى العدد ١٠</div>')}{st('<div><b>٣</b>١٠٠٠٠٠٠٠٠٠٠ بقوى العدد ١٠</div>')}</div>''' + tn('من تمرين ٢ (أ، د) في الكتاب، و ١٠ أُس ٤ من كتاب النشاط.')))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ١ 🎫</span><h2>الإجابات</h2>
<button class="flip box col" style="min-width:40vw"><span class="tap">👆 اضغط لإظهار الإجابات</span><span class="hid col">{M('١٠٠٠٠ عشرة آلاف', cls="sm")}{M(P('10', 2), cls="sm")}{M(P('10', 10), cls="sm")}</span></button>'''))

# ═══════════ الحصة الثانية: الضرب في ٠٫١ و ٠٫٠١ ═══════════
S.append(slide('''<span class="tag">الحصة الثانية · ٤٠ دقيقة</span><h2>الضرب في ٠٫١ و ٠٫٠١</h2>
<div class="plan"><div><b>٣ د</b>إحماء</div><div><b>٦ د</b>٠٫١ و ٠٫٠١ كسورٌ</div><div><b>٨ د</b>مثال ٣-٧ب (أ، ب)</div>
<div><b>٧ د</b>نحن</div><div><b>٨ د</b>أنتم</div><div><b>٤ د</b>انتبه</div><div><b>٤ د</b>بطاقة الخروج</div></div>''', 'divider'))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">إحماء 🔥</span>{timer(1)}</div>''' + quiz('٣٢ ÷ ١٠ = ؟', [M('٣٢٠'), M('٣٫٢'), M('٠٫٣٢'), M('٢٢')], 1, 'القسمة على ١٠ تنقل الأرقام منزلةً واحدة إلى اليمين')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('كتاب الطالب ص ٧٠')}</div><h2>الكسران العشريان ٠٫١ و ٠٫٠١</h2>
<div class="row">{st(box(f'<div class="col"><span class="hint">جزءٌ من عشرة</span>{M("٠٫١", EQ, FR("١", "١٠"))}</div>', style="flex:1"))}{st(box(f'<div class="col"><span class="hint">جزءٌ من مئة</span>{M("٠٫٠١", EQ, FR("١", "١٠٠"))}</div>', style="flex:1"))}</div>
{st('<div class="note">الضرب في ٠٫١ = الضرب في <b>عُشر</b> = <b>القسمة على ١٠</b></div>')}''' + tn('الخطأ الشائع الأول في الدليل: صعوبة فهم أن ٠٫١ = ١/١٠ و ٠٫٠١ = ١/١٠٠. اربطه بجدول القيمة المكانية.')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('كتاب الطالب ص ٧٠')}</div><h2>الضرب في ٠٫١ أو ٠٫٠١</h2>
<div class="defs">{st(f'<div><b class="kk c-exp">× ٠٫١</b><span>= القسمة على <b class="c-exp">١٠</b>: {M("٨", X, "٠٫١", EQ, "٨", DV, "١٠", EQ, "٠٫٨", cls="sm")}</span></div>')}{st(f'<div><b class="kk c-we">× ٠٫٠١</b><span>= القسمة على <b class="c-we">١٠٠</b>: {M("٨", X, "٠٫٠١", EQ, "٨", DV, "١٠٠", EQ, "٠٫٠٨", cls="sm")}</span></div>')}</div>
{st('<div class="note">الناتج أصغر من العدد: الأرقام تنتقل إلى اليمين منزلةً أو منزلتين</div>')}'''))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('مثال ٣-٧ب (أ)')}</div><h2>أوجد ناتج ٣٢ × ٠٫١</h2>
<div class="row vrow">{STEPS(STP('الضرب في ٠٫١ = القسمة على ١٠'), STP('٣٢ ÷ ١٠', M('٣٫٢', cls='sm'), 'fin'))}
{VB(valign([('32', ''), ('3.2', '÷ ١٠')]))}</div>'''))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('مثال ٣-٧ب (ب)')}</div><h2>أوجد ناتج ٤٫٢ × ٠٫٠١</h2>
<div class="row vrow">{STEPS(STP('الضرب في ٠٫٠١ = القسمة على ١٠٠'), STP('٤٫٢ ÷ ١٠٠', M('٠٫٠٤٢', cls='sm'), 'fin'))}
{VB(valign([('4.2', ''), ('0.042', '÷ ١٠٠')]))}</div>''' + tn('الأرقام تنتقل منزلتين إلى اليمين، فنكتب ٠ في الآحاد و ٠ في الأجزاء من عشرة.')))
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('تمرين ٣ (أ، هـ)')}</div><h2>معاً: أوجد الناتج</h2>
<div class="row">{st(f'<button class="flip box col" style="flex:1"><span class="hint">٦٢ × ٠٫١</span><span class="tap">👆</span><span class="hid col">{M("٦٢ ÷ ١٠ = ٦٫٢", cls="sm")}</span></button>')}{st(f'<button class="flip box col" style="flex:1"><span class="hint">٣٧ × ٠٫٠١</span><span class="tap">👆</span><span class="hid col">{M("٣٧ ÷ ١٠٠ = ٠٫٣٧", cls="sm")}</span></button>')}</div>'''))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ٣ (ج)')}{timer(1)}</div>''' + quiz('١٢٥ × ٠٫١ = ؟', [M('١٢٥٠'), M('١٢٫٥'), M('١٫٢٥'), M('١٢٥٫١')], 1, '١٢٥ ÷ ١٠ = ١٢٫٥')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ٣ (ز)')}</div>''' + quiz('٧٥٠ × ٠٫٠١ = ؟', [M('٧٥'), M('٧٫٥'), M('٧٥٠٠٠'), M('٠٫٧٥')], 1, '٧٥٠ ÷ ١٠٠ = ٧٫٥')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ٣ (ح)')}</div>''' + quiz('٤ × ٠٫٠١ = ؟', [M('٠٫٤'), M('٤٠٠'), M('٠٫٠٤'), M('٠٫٠٠٤')], 2, '٤ ÷ ١٠٠ = ٠٫٠٤')))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">انتبه ⚠️ خطأ شائع</span>{ref('دليل المعلم ص ٧٣')}</div><h2>الضرب لا يُكبّر دائماً</h2>
<div class="row">{st(box('<div class="col"><span class="hint no">✘ ضربنا في ١٠</span>' + M('٥٠ × ٠٫١ = ٥٠٠') + '</div>', style="flex:1"))}{st(box('<div class="col"><span class="hint ok">✔ قسمنا على ١٠</span>' + M('٥٠ × ٠٫١ = ٥') + '</div>', style="flex:1"))}</div>
{st('<div class="note">الضرب في عددٍ أصغر من ١ يعطي ناتجاً أصغر من العدد</div>')}'''))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ٢ 🎫</span><h2>أوجد الناتج</h2>
<div class="exit">{st('<div><b>١</b>٣٫٢ × ٠٫١</div>')}{st('<div><b>٢</b>٦٠٠ × ٠٫٠١</div>')}{st('<div><b>٣</b>٨٫٧ × ٠٫١</div>')}</div>'''))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ٢ 🎫</span><h2>الإجابات</h2>
<button class="flip box col" style="min-width:40vw"><span class="tap">👆 اضغط لإظهار الإجابات</span><span class="hid col">{M('٠٫٣٢', cls="sm")}{M('٦', cls="sm")}{M('٠٫٨٧', cls="sm")}</span></button>'''))

# ═══════════ الحصة الثالثة: القسمة على ٠٫١ و ٠٫٠١ ═══════════
S.append(slide('''<span class="tag">الحصة الثالثة · ٤٠ دقيقة</span><h2>القسمة على ٠٫١ و ٠٫٠١</h2>
<div class="plan"><div><b>٣ د</b>إحماء</div><div><b>٧ د</b>مثال ٣-٧ب (ج، د)</div><div><b>٥ د</b>نحن</div>
<div><b>٥ د</b>أنتم</div><div><b>٥ د</b>طريقة هيثم</div><div><b>٥ د</b>× أم ÷ ؟</div><div><b>٦ د</b>تحدٍّ</div><div><b>٤ د</b>بطاقة الخروج</div></div>''', 'divider'))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">إحماء 🔥</span>{timer(1)}</div>''' + quiz('كم مرةً يوجد ٠٫١ في ٦ ؟', [M('٠٫٦'), M('٦٠'), M('٦'), M('٦٠٠')], 1, 'في الواحد ١٠ أجزاء من عشرة، ففي ٦ ستون جزءاً')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('كتاب الطالب ص ٧٠')}</div><h2>القسمة على ٠٫١ أو ٠٫٠١</h2>
<div class="defs">{st(f'<div><b class="kk c-exp">÷ ٠٫١</b><span>= الضرب في <b class="c-exp">١٠</b>: {M("٨", DV, "٠٫١", EQ, "٨", X, "١٠", EQ, "٨٠", cls="sm")}</span></div>')}{st(f'<div><b class="kk c-we">÷ ٠٫٠١</b><span>= الضرب في <b class="c-we">١٠٠</b>: {M("٨", DV, "٠٫٠١", EQ, "٨", X, "١٠٠", EQ, "٨٠٠", cls="sm")}</span></div>')}</div>
{st('<div class="note">الناتج أكبر من العدد: الأرقام تنتقل إلى اليسار منزلةً أو منزلتين</div>')}''' + tn('الخطأ الشائع الثاني في الدليل: صعوبة تذكّر أن القسمة على ٠٫١ = الضرب في ١٠. ذكّرهم بسؤال الإحماء: كم مرةً يوجد ٠٫١ في العدد؟')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('مثال ٣-٧ب (ج)')}</div><h2>أوجد ناتج ٦ ÷ ٠٫١</h2>
<div class="row vrow">{STEPS(STP('القسمة على ٠٫١ = الضرب في ١٠'), STP('٦ × ١٠', M('٦٠', cls='sm'), 'fin'))}
{VB(valign([('6', ''), ('60', '× ١٠')]))}</div>'''))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('مثال ٣-٧ب (د)')}</div><h2>أوجد ناتج ٤٫١٥٦ ÷ ٠٫٠١</h2>
<div class="row vrow">{STEPS(STP('القسمة على ٠٫٠١ = الضرب في ١٠٠'), STP('٤٫١٥٦ × ١٠٠', M('٤١٥٫٦', cls='sm'), 'fin'))}
{VB(valign([('4.156', ''), ('415.6', '× ١٠٠')]))}</div>'''))
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('تمرين ٤ (أ، هـ)')}</div><h2>معاً: أوجد الناتج</h2>
<div class="row">{st(f'<button class="flip box col" style="flex:1"><span class="hint">٧ ÷ ٠٫١</span><span class="tap">👆</span><span class="hid col">{M("٧ × ١٠ = ٧٠", cls="sm")}</span></button>')}{st(f'<button class="flip box col" style="flex:1"><span class="hint">٢ ÷ ٠٫٠١</span><span class="tap">👆</span><span class="hid col">{M("٢ × ١٠٠ = ٢٠٠", cls="sm")}</span></button>')}</div>'''))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ٤ (ج)')}{timer(1)}</div>''' + quiz('٥٢٫٢ ÷ ٠٫١ = ؟', [M('٥٫٢٢'), M('٥٢٢'), M('٥٢٢٠'), M('٥٢٫٣')], 1, '٥٢٫٢ × ١٠ = ٥٢٢')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ٤ (ح)')}</div>''' + quiz('٧٫٢٢٥ ÷ ٠٫٠١ = ؟', [M('٧٢٢٫٥'), M('٧٢٫٢٥'), M('٠٫٠٧٢٢٥'), M('٧٢٢٥')], 0, '٧٫٢٢٥ × ١٠٠ = ٧٢٢٫٥')))
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('تمرين ٥: طريقة هيثم')}</div><h2>نتحقّق بالعملية العكسية</h2>
<div class="row">{st(box(f'<div class="col"><span class="hint">٢٣ × ٠٫١ = ٢٣ ÷ ١٠ = ٢٫٣</span>{M("٢٫٣ × ١٠ = ٢٣ ✔", cls="sm")}</div>', style="flex:1"))}{st(box(f'<div class="col"><span class="hint">٨٫٣ ÷ ٠٫٠١ = ٨٣٠٠ ؟</span>{M("٨٣٠٠ ÷ ١٠٠ = ٨٣ ✘", cls="sm")}<span class="hint ok">الصحيح ٨٣٠</span></div>', style="flex:1"))}</div>''' + tn('من الكتاب (ورقة هيثم): العملية العكسية تكشف الخطأ. الدليل: شجّع الطلاب على استخدامها لتعزيز فهم العلاقة بين الضرب والقسمة.')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ٥ (ب، د)')}</div><h2>احسب ثم تحقّق</h2>
<div class="row">{st(f'<button class="flip box col" style="flex:1"><span class="hint">٢٣٫٦ × ٠٫٠١</span><span class="tap">👆</span><span class="hid col">{M("٠٫٢٣٦", cls="sm")}<small class="ck">تحقّق: ٠٫٢٣٦ × ١٠٠ = ٢٣٫٦</small></span></button>')}{st(f'<button class="flip box col" style="flex:1"><span class="hint">٤٫٥ ÷ ٠٫٠١</span><span class="tap">👆</span><span class="hid col">{M("٤٥٠", cls="sm")}<small class="ck">تحقّق: ٤٥٠ ÷ ١٠٠ = ٤٫٥</small></span></button>')}</div>'''))
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('تمرين ٦')}</div><h2>ضع × أو ÷</h2>
<div class="xgrid c3 pz">{''.join(st(f'<button class="flip xcard"><span class="xq">{q}</span><span class="tap">👆</span><span class="hid xa">{a_}</span></button>') for q, a_ in (
  ('٦٫٧ ☐ ٠٫١ = ٦٧', '÷'), ('٤٫٥ ☐ ٠٫٠١ = ٠٫٠٤٥', '×'), ('٠٫٩ ☐ ٠٫١ = ٠٫٠٩', '×'), ('٥٥٠ ☐ ٠٫٠١ = ٥٫٥', '×'), ('٠٫٢٣ ☐ ٠٫١ = ٢٫٣', '÷'), ('١٢ ☐ ٠٫٠١ = ١٢٠٠', '÷')))}</div>''' + tn('القاعدة السريعة: الناتج أكبر من العدد ← قسمة، أصغر ← ضرب.')))
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('تمرين ٩')}</div><h2>فكّر فهد في عدد…</h2>
<div class="row vrow">{STEPS(STP('ضربه في ٠٫١', M('÷ ١٠', cls='sm')), STP('قسم على ٠٫٠١', M('× ١٠٠', cls='sm')), STP('قسم على ٠٫١', M('× ١٠', cls='sm')), STP('النتيجة: العدد × ١٠٠ = ١٢٥٠٠', M('العدد ١٢٥', cls='sm'), 'fin'))}</div>''' + tn('الدليل: حثّ الطلاب على التفكير في العمليات العكسية. طريقةٌ أخرى: نبدأ من ١٢٥٠٠ ونعكس كل خطوة.')))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">نشاط 🏁</span>{ref('نشاط دليل المعلم')}</div><h2>من ينفذ أولاً؟</h2>
<div class="exit">{st('<div><b>١</b>كل طالب أو مجموعة تحلّ أسئلة ورقة المصادر ٣-٧ بأسرع ما يمكن (٥ إلى ١٥ دقيقة)</div>')}{st('<div><b>٢</b>نستخدم الأنماط: × ٠٫١ = ÷ ١٠ و ÷ ٠٫١ = × ١٠ …</div>')}{st('<div><b>٣</b>نتحقّق بالعمليات العكسية دون آلة حاسبة</div>')}</div>''' + tn('نشاط الدليل بعد إكمال تمارين ٣-٧. الجزء الثاني من ورقة المصادر يسرد الحلول، فيمكن استخدامه ورقة إجابة.')))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ٣ 🎫</span><h2>أوجد الناتج</h2>
<div class="exit">{st('<div><b>١</b>٤٫٥ ÷ ٠٫١</div>')}{st('<div><b>٢</b>٨٫٥ ÷ ٠٫٠١</div>')}{st('<div><b>٣</b>٠٫٦٧ ÷ ٠٫١</div>')}</div>'''))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ٣ 🎫</span><h2>الإجابات</h2>
<button class="flip box col" style="min-width:40vw"><span class="tap">👆 اضغط لإظهار الإجابات</span><span class="hid col">{M('٤٥', cls="sm")}{M('٨٥٠', cls="sm")}{M('٦٫٧', cls="sm")}</span></button>'''))
S.append(slide('''<span class="qbadge" style="background:#0A6770;box-shadow:0 4px 0 #05393E">الواجب المنزلي 🏠</span><h2>بعد الحصص الثلاث</h2>
<div class="exit"><div class="st"><div><b>١</b>صفحة ٥٢ في كتاب النشاط (قوى ١٠، الضرب والقسمة)</div></div><div class="st"><div><b>٢</b>صفحتا ٥٣ و ٥٤ في كتاب النشاط (الرمز المناسب، والتفكير)</div></div></div>'''))
S.append(slide(f'''<h2>الخلاصة</h2>
<div class="sum4">{''.join(st(box(M(t, cls='sm'))) for t in ('× ٠٫١ = ÷ ١٠', '× ٠٫٠١ = ÷ ١٠٠', '÷ ٠٫١ = × ١٠', '÷ ٠٫٠١ = × ١٠٠'))}</div>
{st(f'<div class="note">{P("10", "ن")} هو الرقم ١ وبعده ن من الأصفار</div>')}'''))

# ═══════════ ملحق: تمارين كتاب الطالب ص٧١–٧٣ (الإجابات من دليل المعلم ص٧٩) ═══════════
S.append(launch('sb', '٧١ إلى ٧٣', note=f'المراجع: كتاب الطالب ص٧٠ إلى ٧٣، ودليل المعلم ص٧٣ و ٧٤ وإجاباته ص٧٩ · {ME}'))
H = ['أ', 'ب', 'ج', 'د', 'هـ', 'و', 'ز', 'ح']
S.append(ex(1, 'اكتب بالأعداد والكلمات', 'الأُس = عدد الأصفار يمين ١', [(f'({h}) {P("10", e)}', f'{_ar(n)}<small>{w}</small>') for h, (e, n, w) in zip(H, [(3, '1000', 'ألف'), (5, '100000', 'مئة ألف'), (7, '10000000', 'عشرة ملايين'), (1, '10', 'عشرة')])], cols=2))
S.append(ex(2, 'اكتب بقوى العدد ١٠', 'نعدّ الأصفار يمين ١', [(f'({h}) {_ar(n)}', P('10', e)) for h, (n, e) in zip(H, [('100', 2), ('10000000', 7), ('10000', 4), ('10000000000', 10)])], cols=2))
RM, RD = '× ٠٫١ = ÷ ١٠ ، و × ٠٫٠١ = ÷ ١٠٠', '÷ ٠٫١ = × ١٠ ، و ÷ ٠٫٠١ = × ١٠٠'
S.append(ex(3, 'أوجد الناتج', RM, [(f'({h}) {q}', r) for h, (q, r) in zip(H, [('٦٢ × ٠٫١', '٦٫٢'), ('٥٠ × ٠٫١', '٥'), ('١٢٥ × ٠٫١', '١٢٫٥'), ('٣٫٢ × ٠٫١', '٠٫٣٢'), ('٣٧ × ٠٫٠١', '٠٫٣٧'), ('٦٠٠ × ٠٫٠١', '٦'), ('٧٥٠ × ٠٫٠١', '٧٫٥'), ('٤ × ٠٫٠١', '٠٫٠٤')])], cols=2))
S.append(ex(4, 'أوجد الناتج', RD, [(f'({h}) {q}', r) for h, (q, r) in zip(H, [('٧ ÷ ٠٫١', '٧٠'), ('٤٫٥ ÷ ٠٫١', '٤٥'), ('٥٢٫٢ ÷ ٠٫١', '٥٢٢'), ('٠٫٦٧ ÷ ٠٫١', '٦٫٧'), ('٢ ÷ ٠٫٠١', '٢٠٠'), ('٨٫٥ ÷ ٠٫٠١', '٨٥٠'), ('٠٫٣٢ ÷ ٠٫٠١', '٣٢'), ('٧٫٢٢٥ ÷ ٠٫٠١', '٧٢٢٫٥')])], cols=2))
S.append(ex(5, 'احسب ثم تحقّق بالعملية العكسية', 'نعكس العملية فنعود إلى العدد الأصلي', [(f'({h}) {q}', f'{r}<small>{c}</small>') for h, (q, r, c) in zip(H, [('١٨ × ٠٫١', '١٫٨', '١٫٨ × ١٠ = ١٨'), ('٢٣٫٦ × ٠٫٠١', '٠٫٢٣٦', '٠٫٢٣٦ × ١٠٠ = ٢٣٫٦'), ('٠٫٦ ÷ ٠٫١', '٦', '٦ ÷ ١٠ = ٠٫٦'), ('٤٫٥ ÷ ٠٫٠١', '٤٥٠', '٤٥٠ ÷ ١٠٠ = ٤٫٥')])], cols=2))
S.append(ex(6, 'ضع × أو ÷', 'الناتج أكبر من العدد ← ÷ ، والناتج أصغر ← ×', [(f'({h}) {q}', r) for h, (q, r) in zip(H, [('٦٫٧ ☐ ٠٫١ = ٦٧', '÷'), ('٤٫٥ ☐ ٠٫٠١ = ٠٫٠٤٥', '×'), ('٠٫٩ ☐ ٠٫١ = ٠٫٠٩', '×'), ('٥٥٠ ☐ ٠٫٠١ = ٥٫٥', '×'), ('٠٫٢٣ ☐ ٠٫١ = ٢٫٣', '÷'), ('١٢ ☐ ٠٫٠١ = ١٢٠٠', '÷')])], cols=2))
S.append(ex(7, 'اكتب ٠٫١ أو ٠٫٠١', 'منزلةٌ واحدة ← ٠٫١ ، ومنزلتان ← ٠٫٠١', [(f'({h}) {q}', r) for h, (q, r) in zip(H, [('٢٦ × ☐ = ٠٫٢٦', '٠٫٠١'), ('٣٫٤ ÷ ☐ = ٣٤', '٠٫١'), ('٠٫٠٦ × ☐ = ٠٫٠٠٠٦', '٠٫٠١'), ('٧ ÷ ☐ = ٧٠', '٠٫١'), ('٨٫٩٩ × ☐ = ٠٫٨٩٩', '٠٫١'), ('٥٢ ÷ ☐ = ٥٢٠', '٠٫١')])], cols=2))
S.append(ex(8, 'أيّ العمليات ناتجها مختلف؟', 'نحسب كل عملية', [('(أ) ٥٫٢ × ٠٫١ (ب) ٥٢ ÷ ٠٫٠١ (ج) ٠٫٠٥٢ ÷ ٠٫١ (د) ٥٢ × ٠٫٠١', '(ب) = ٥٢٠٠<small>والبقية = ٠٫٥٢</small>')], cols=1))
S.append(ex(9, 'فكّر فهد في عدد', 'نعكس العمليات أو نجمع أثرها', [('× ٠٫١ ثم ÷ ٠٫٠١ ثم ÷ ٠٫١ فحصل على ١٢٥٠٠: ما العدد؟', '١٢٥<small>÷ ١٠ ثم × ١٠٠ ثم × ١٠ = × ١٠٠</small>')], cols=1))
S.append(ex(10, 'مثالٌ يبيّن خطأ العبارة', 'يكفي مثالٌ واحد مخالف', [('(أ) الضرب في ٠٫١ لعددٍ غير الصفر يعطي ناتجاً أكبر من صفر', 'عددٌ سالب<small>−٥ × ٠٫١ = −٠٫٥</small>'), ('(ب) قسمة عددٍ بمنزلة عشرية على ٠٫٠١ تعطي أكبر من ١٠٠', 'عددٌ أصغر من ١<small>٠٫٥ ÷ ٠٫٠١ = ٥٠</small>')], cols=1))

# ═══════════ ملحق: حلول كتاب النشاط ص٥٢–٥٤ (الإجابات من دليل المعلم ص٨٣) ═══════════
S.append(launch('ab', '٥٢ إلى ٥٤', note='الإجابات النهائية من دليل المعلم ص ٨٣'))
NA, NB, NC = 'نشاط ص ٥٢ · تمرين', 'نشاط ص ٥٣ · تمرين', 'نشاط ص ٥٤ · تمرين'
S.append(ex(1, 'اكتب بالأرقام والكلمات', 'الأُس = عدد الأصفار يمين ١', [('(أ) ' + P('10', 2), '١٠٠<small>مئة</small>'), ('(ب) ' + P('10', 4), '١٠٠٠٠<small>عشرة آلاف</small>'), ('(ج) ' + P('10', 8), '١٠٠٠٠٠٠٠٠<small>مئة مليون</small>'), ('(د) ' + P('1', 9), '١<small>واحد: ١ × ١ × … = ١</small>')], cols=2, src=NA))
S.append(ex(2, 'اكتب بقوى العدد ١٠', 'نعدّ الأصفار يمين ١', [(f'({h}) {_ar(n)}', P('10', e)) for h, (n, e) in zip(H, [('10', 1), ('1000000', 6), ('1000', 3), ('10000000', 7)])], cols=2, src=NA))
S.append(ex(3, 'أوجد الناتج', RM, [(f'({h}) {q}', r) for h, (q, r) in zip(H, [('٣٣ × ٠٫١', '٣٫٣'), ('٩٩٩ × ٠٫١', '٩٩٫٩'), ('٣٠ × ٠٫١', '٣'), ('٨٫٧ × ٠٫١', '٠٫٨٧'), ('٧٧ × ٠٫٠١', '٠٫٧٧'), ('٧٠ × ٠٫٠١', '٠٫٧'), ('٧٠٠ × ٠٫٠١', '٧'), ('٧ × ٠٫٠١', '٠٫٠٧')])], cols=2, src=NA))
S.append(ex(4, 'أوجد الناتج', RD, [(f'({h}) {q}', r) for h, (q, r) in zip(H, [('٥ ÷ ٠٫١', '٥٠'), ('٥٫٦ ÷ ٠٫١', '٥٦'), ('٥٥٫٦ ÷ ٠٫١', '٥٥٦'), ('٠٫٥٥ ÷ ٠٫١', '٥٫٥'), ('٥ ÷ ٠٫٠١', '٥٠٠'), ('٥٫٦ ÷ ٠٫٠١', '٥٦٠'), ('٥٥٫٦ ÷ ٠٫٠١', '٥٥٦٠'), ('٠٫٥٥ ÷ ٠٫٠١', '٥٥')])], cols=2, src=NA))
S.append(ex(5, 'احسب ثم تحقّق بالعملية العكسية', 'نعكس العملية فنعود إلى العدد الأصلي', [(f'({h}) {q}', f'{r}<small>{c}</small>') for h, (q, r, c) in zip(H, [('٢٧ × ٠٫١', '٢٫٧', '٢٫٧ × ١٠ = ٢٧'), ('٢٧٫٩ × ٠٫٠١', '٠٫٢٧٩', '٠٫٢٧٩ × ١٠٠ = ٢٧٫٩'), ('٠٫٢ ÷ ٠٫١', '٢', '٢ ÷ ١٠ = ٠٫٢'), ('٢٫٧ ÷ ٠٫٠١', '٢٧٠', '٢٧٠ ÷ ١٠٠ = ٢٫٧')])], cols=2, src=NA))
S.append(ex(6, 'اكتب × أو ÷', 'الناتج أكبر من العدد ← ÷ ، والناتج أصغر ← ×', [(f'({h}) {q}', r) for h, (q, r) in zip(H, [('٥٥ ☐ ٠٫١ = ٥٥٠', '÷'), ('٤٦ ☐ ٠٫٠١ = ٠٫٤٦', '×'), ('٣٫٧ ☐ ٠٫١ = ٣٧', '÷'), ('٢٠٨ ☐ ٠٫٠١ = ٢٫٠٨', '×'), ('٠٫١٩ ☐ ٠٫١ = ١٫٩', '÷'), ('٥٠٥ ☐ ٠٫٠١ = ٥٫٠٥', '×')])], cols=2, src=NB))
S.append(ex(7, 'اكتب ٠٫١ أو ٠٫٠١', 'منزلةٌ واحدة ← ٠٫١ ، ومنزلتان ← ٠٫٠١', [(f'({h}) {q}', r) for h, (q, r) in zip(H, [('٤٤ × ☐ = ٤٫٤', '٠٫١'), ('٤٫٤ ÷ ☐ = ٤٤', '٠٫١'), ('٠٫٤٠ × ☐ = ٠٫٠٠٤', '٠٫٠١'), ('٤ ÷ ☐ = ٤٠', '٠٫١'), ('٤٤٫٤ × ☐ = ٠٫٤٤٤', '٠٫٠١'), ('٤٤ ÷ ☐ = ٤٤٠٠', '٠٫٠١')])], cols=2, src=NB))
S.append(ex(8, 'أيّ العمليات ناتجها مختلف؟', 'نحسب كل عملية', [('(أ) ٠٫٠٩٦ ÷ ٠٫١ (ب) ٩٦ × ٠٫٠١ (ج) ٩٫٦ × ٠٫١ (د) ٩٦ ÷ ٠٫٠١', '(د) = ٩٦٠٠<small>والبقية = ٠٫٩٦</small>')], cols=1, src=NB))
S.append(ex(9, 'فكّرت نور في عدد', 'نعكس العمليات أو نجمع أثرها', [('÷ ٠٫٠١ ثم × ٠٫١ ثم ÷ ٠٫٠١ فحصلت على ٢٣٤٠: ما العدد؟', '٢٫٣٤<small>× ١٠٠ ثم ÷ ١٠ ثم × ١٠٠ = × ١٠٠٠</small>')], cols=1, src=NB))
S.append(ex(10, 'مثالٌ يبيّن خطأ العبارة', 'يكفي مثالٌ واحد مخالف', [('(أ) قسمة عددٍ بمنزلة عشرية على ٠٫١ تعطي أكبر من ١', '٠٫١ ÷ ٠٫١ = ١<small>وليس أكبر من ١</small>'), ('(ب) ضرب عددٍ بمنزلتين عشريتين في ٠٫٠١ يعطي أكبر من ٠٫٠١', 'عددٌ أصغر من ١<small>٠٫٥٠ × ٠٫٠١ = ٠٫٠٠٥</small>')], cols=1, src=NC))

# الأعداد الكبيرة بمجموعاتٍ ثلاثية كما في الكتاب (١٠ ٠٠٠ ٠٠٠) ليسهل عدّ الأصفار
def _g3(m):
    t = m.group(0); parts = []
    while len(t) > 3: parts.insert(0, t[-3:]); t = t[:-3]
    return '<span class="g3">' + '\u202f'.join([t] + parts) + '</span>'
S = [re.sub(r'(?<![٠-٩٫])[٠-٩]{5,}(?![٠-٩٫])', _g3, x) for x in S]

EXTRA_CSS_OWN = '''
.stps{display:flex;flex-direction:column;gap:1.2vh;align-items:stretch}
.stp{display:flex;align-items:center;gap:1.4vw;justify-content:space-between}
.stp .lab{flex:0 1 auto;max-width:72%;font-family:var(--fh);font-weight:800;color:#2563EB;background:#EAF1FF;border-radius:12px;padding:.2em .8em;text-align:center;line-height:1.4;font-size:clamp(20px,3.6vh,40px)}
.stp.fin .lab{background:var(--good);color:#fff}
.slide .vrow{align-items:center;justify-content:center;gap:2vh 3vw;flex-wrap:wrap}
.slide .vrow>.stps{flex:0 1 auto;max-width:min(1000px,62vw)}
@media (max-aspect-ratio:1/1){.slide .vrow{flex-direction:column}.slide .vrow>.stps{max-width:92vw}}
.vbox{flex:none;background:#fff;border:3px solid var(--line);border-radius:18px;padding:1vh 2vw;font-family:var(--fh);font-size:clamp(48px,9.6vh,110px)}
.frc{display:inline-flex;flex-direction:column;align-items:center;line-height:1.05;vertical-align:middle;font-size:1em}
.g3{direction:ltr;unicode-bidi:isolate;white-space:nowrap}
.frc>span:first-child{border-bottom:.07em solid currentColor;padding:0 .15em;align-self:stretch;text-align:center}
.pwt{border-collapse:separate;border-spacing:0 1vh;font-weight:700}
.pwt td{background:#fff;border-top:3px solid var(--line);border-bottom:3px solid var(--line);padding:.6vh 1.4vw;text-align:center}
.pwt td:first-child{border-right:3px solid var(--line);border-radius:0 14px 14px 0}.pwt td:last-child{border-left:3px solid var(--line);border-radius:14px 0 0 14px}
.pwt .w{font-size:clamp(20px,3.6vh,40px);color:var(--ink2)}
.w2{font-size:clamp(26px,4.8vh,54px)}
.ck{font-size:clamp(18px,3vh,32px);color:var(--good)}
.box .col>.m:not(.mid):not(.sm):not(.big),.hid.col>.m:not(.mid):not(.sm):not(.big){font-size:clamp(32px,6vh,70px)}
.hint.no{color:var(--bad)}.hint.ok{color:var(--good)}
.defs{display:flex;flex-direction:column;gap:1.6vh;width:min(1400px,92vw)}
.defs .st>div{display:flex;align-items:center;gap:1.6vw;background:#fff;border:3px solid var(--line);border-radius:18px;padding:1.2vh 1.6vw}
.defs .kk{flex:none;font-size:clamp(30px,5.6vh,64px)}.defs span{font-weight:700;font-size:clamp(24px,4.4vh,50px);line-height:1.45}
.sumg{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:2vw;width:min(1600px,94vw)}
.sumg .col span{font-weight:700;font-size:clamp(24px,4.4vh,52px);line-height:1.4}
.sumg .kk{font-size:clamp(28px,5.2vh,60px)}
.sum4{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:2vh 2vw;width:min(1300px,92vw)}
.sum4 .m{font-size:clamp(32px,6.4vh,74px)!important}
.pz>.st{display:flex}.pz>.st>.xcard{flex:1}
.xa small{display:block}
'''
