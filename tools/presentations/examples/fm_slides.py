# شرائح درس ٢-٤ «استنتاج واستخدام الصيغ» — الصف السابع (٣ حصص، كتاب الطالب ص٤٨–٥٠)
# المراجع: دليل المعلم ص٥٠–٥١ (نقاط التعلّم، الأخطاء الشائعة: الخلط بين العبارة والصيغة، وترتيب العمليات؛ النشاط: صيغ من الحياة اليومية)،
# كتاب الطالب ص٤٨–٥٠ (مثال ٢-٤)، وإجابات الدليل ص٥٥–٥٦ (كتاب الطالب) وص٥٩ (كتاب النشاط ص٣٤–٣٦).
# python3.12 gen_powers.py fm_slides.py استنتاج_واستخدام_الصيغ_عرض_تفاعلي.html "استنتاج واستخدام الصيغ — الصف السابع"

def STP(lab, expr, cls=''): return st(f'<div class="stp {cls}"><span class="lab">{lab}</span>{expr}</div>')
def STEPS(*rows): return '<div class="stps">' + ''.join(rows) + '</div>'
MI = '<span class="x">−</span>'; DV = '<span class="x">÷</span>'
def V(t): return f'<span class="var">{t}</span>'                                   # المتغيّر بلونٍ مميّز
def T(k, v): return f'<span class="term">{k}{V(v)}</span>'                        # حدّ: المعامل ثم المتغيّر
def G(*p): return '<span class="grp">(' + ' '.join(p) + ')</span>'
def FR(n, d): return f'<span class="fr"><span>{n}</span><span>{d}</span></span>'
def SV(n): return f'<span class="sbv">{n}</span>'                                   # العدد المعوَّض في مكان المتغيّر
def VALS(*pairs): return '<div class="vals">' + ''.join(f'<span>{V(k)} = {v}</span>' for k, v in pairs) + '</div>'
S = []
ME = 'إعداد: أ. عيسى الحارثي'
S.append(slide(f'''<span class="tag">الصف السابع · الدرس ٢-٤</span>
<h1 class="h1s">استنتاج واستخدام الصيغ</h1>
<p class="lead">كتاب الطالب ص ٤٨ إلى ٥٠ · ثلاث حصص</p>
<p class="lead" style="font-size:clamp(26px,4.8vh,56px)">{ME}</p>''', 'cover'))
CAN = ['أعرف <b>الصيغة</b> وأميّزها من العبارة الجبرية', '<b>أعوّض</b> الأعداد في العبارات والصيغ وأتّبع ترتيب العمليات', '<b>أستنتج</b> صيغةً بالكلمات وبالحروف وأستخدمها في حلّ المسائل']
S.append(slide(f'''<h2>في نهاية هذا الدرس…</h2>
<div class="can">{''.join(f'<div><span class="can-i">✔</span><span><b>أنا أستطيع</b> أن {t}</span></div>' for t in CAN)}</div>'''))
S.append(slide(f'''<h2>مفردات الدرس</h2>
{st('<div class="vocab wide"><div><span>الصيغة</span><i>formula</i></div><div><span>التعويض</span><i>substitute</i></div><div><span>استنتاج</span><i>derive</i></div></div>')}
<p class="lead">ثلاث حصص: <b class="c-i">أنا</b> ← <b class="c-we">نحن</b> ← <b class="c-u">أنتم</b></p>'''))

# ═══════════ الحصة الأولى: الصيغة والتعويض ═══════════
S.append(slide('''<span class="tag">الحصة الأولى · ٤٠ دقيقة</span><h2>الصيغة والتعويض</h2>
<div class="plan"><div><b>٥ د</b>تهيئة: صيغ من حياتنا</div><div><b>٧ د</b>ما الصيغة؟</div><div><b>٥ د</b>التعويض في صيغة</div>
<div><b>٨ د</b>مثال ٢-٤ (أ)</div><div><b>８ د</b>نحن ← أنتم</div><div><b>٤ د</b>انتبه</div><div><b>٣ د</b>بطاقة الخروج</div></div>'''.replace('８', '٨'), 'divider'))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">تهيئة 🤔</span>{ref('نشاط دليل المعلم')}</div><h2>كيف تُحسب هذه المبالغ؟</h2>
<div class="life">{''.join(st(f'<div><span class="ic2">{i}</span><b>{t}</b><small>{s}</small></div>') for i, t, s in (('🧾', 'فاتورة الكهرباء', 'سعر الوحدة × عدد الوحدات'), ('👷', 'أجر العامل', 'أجر الساعة × عدد الساعات'), ('🌡️', 'درجة الحرارة', 'تحويل من وحدة إلى أخرى')))}</div>''' + tn('نشاط الدليل: اطلب من الطلاب أمثلةً لصيغ يعرفونها من الحياة اليومية ومن دروس العلوم (السرعة والمسافة والزمن). كل واحدة منها قاعدةٌ تربط بين كميات.')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('كتاب الطالب ص ٤٨')}</div><h2>ما الصيغة؟</h2>
{st('<div class="rulebox"><b class="c-exp">الصيغة</b> قاعدةٌ رياضية توضّح العلاقة بين كميتين أو أكثر (متغيّرات)</div>')}
<div class="frm">{st(f'<div><span class="lab">بالكلمات</span><b>مساحة المستطيل = الطول × العرض</b></div>')}{st(f'<div><span class="lab">بالحروف</span>{M(V("م"), EQ, V("ل"), X, V("ض"))}</div>')}</div>'''))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('كتاب الطالب ص ٤٨')}</div><h2>نعوّض الأعداد في الصيغة {M(V("م"), EQ, V("ل"), X, V("ض"), cls="sm")}</h2>
{st(VALS(('ل', '٥ سم'), ('ض', '٤ سم')))}
{box(STEPS(STP('نضع ٥ مكان ل و ٤ مكان ض', M(V('م'), EQ, SV('٥'), X, SV('٤'), cls="sm")), STP('نحسب', M(V('م'), EQ, '٢٠ سم²', cls="sm"), 'fin')))}''' + tn('التعويض: نضع العدد مكان الحرف. لوّن العدد المعوَّض كما في الشريحة ليرى الطلاب مكانه.')))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">انتبه ⚠️</span>{ref('دليل المعلم ص ٥٠')}</div><h2>العبارة الجبرية أم الصيغة؟</h2>
<div class="row">{st(box(f'<div class="col"><span class="hint">عبارة جبرية (بلا =)</span>{M(V("ل"), X, V("ض"))}</div>', style="flex:1"))}{st(box(f'<div class="col"><span class="hint">صيغة (فيها =)</span>{M(V("م"), EQ, V("ل"), X, V("ض"))}</div>', style="flex:1;border-color:var(--base)"))}</div>
{st('<div class="note">كل صيغة تحتوي دائماً على إشارة التساوي <b>=</b></div>')}''' + tn('من الأخطاء الشائعة في الدليل: قد لا يفهم الطلاب الفرق بين العبارة الجبرية والصيغة. أكّد أن الصيغة فيها دائماً إشارة =.')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('مثال ٢-٤ (أ)')}</div><h2>أوجد قيمة {M(V("س"), PL, T("٣", "ص"), cls="sm")}</h2>
{st(VALS(('س', '٢'), ('ص', '٤')))}
{box(STEPS(STP('نعوّض: س = ٢ و ص = ٤', M(SV('٢'), PL, '٣', X, SV('٤'), cls="sm")), STP('الضرب أولاً', M('٢', PL, '١٢', cls="sm")), STP('ثم الجمع', M('١٤', cls="sm"), 'fin')))}
{st('<div class="note">٣ص تعني ٣ × ص، فنضرب قبل أن نجمع</div>')}''' + tn('الدليل يقترح تكرار المثال بقيمٍ أخرى، مثل س = ٥ و ص = ١ (الناتج ٨).')))
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('تمرين ١ (ج)')}</div><h2>معاً: أوجد قيمة {M(V("و"), PL, V("ر"), cls="sm")}</h2>
{st(VALS(('و', '٧'), ('ر', '٤')))}
<button class="flip box col"><span class="tap">👆 الحل</span><span class="hid col">{M(SV('٧'), PL, SV('٤'), EQ, '١١', cls="sm")}</span></button>'''))
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('تمرين ١ (و)')}</div><h2>معاً: أوجد قيمة {M(V("ع"), PL, T("٢", "ل"), cls="sm")}</h2>
{st(VALS(('ع', '٥'), ('ل', '٣')))}
<button class="flip box col"><span class="tap">👆 الحل</span><span class="hid col">{M(SV('٥'), PL, '٢', X, SV('٣'), cls="sm")}{M(EQ, '٥', PL, '٦', EQ, '١١', cls="sm")}</span></button>'''))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ١ (د)')}{timer(2)}</div>''' + quiz(f'أوجد قيمة {M(V("م"), MI, V("ع"))} عندما م = ١٠٠ ، ع = ٢٥', [M('١٢٥'), M('٧٥'), M('٨٥'), M('٤')], 1, '١٠٠ − ٢٥ = ٧٥')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ١ (هـ)')}</div>''' + quiz(f'أوجد قيمة {M(T("٣", "ك"))} عندما ك = ٥', [M('٣٥'), M('٨'), M('١٥'), M('٥٣')], 2, '٣ك تعني ٣ × ك = ٣ × ٥ = ١٥ ، وليست ٣٥')))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ١ 🎫</span><h2>أوجد القيمة</h2>
<div class="exit">{st(f'<div><b>١</b>{M(V("ص"), PL, "٥", cls="sm")} عندما ص = ٣</div>')}{st(f'<div><b>٢</b>{M(V("س"), MI, "٩", cls="sm")} عندما س = ٢٠</div>')}{st(f'<div><b>٣</b>{M(T("٤", "ن"), PL, V("م"), cls="sm")} عندما ن = ٢ ، م = ٣</div>')}</div>'''))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ١ 🎫</span><h2>الإجابات</h2>
<button class="flip box col" style="min-width:40vw"><span class="tap">👆 اضغط لإظهار الإجابات</span><span class="hid col">{M('٨', cls="sm")}{M('١١', cls="sm")}{M('٨', PL, '٣', EQ, '١١', cls="sm")}</span></button>'''))

# ═══════════ الحصة الثانية: التعويض وترتيب العمليات ═══════════
S.append(slide('''<span class="tag">الحصة الثانية · ٤٠ دقيقة</span><h2>التعويض وترتيب العمليات</h2>
<div class="plan"><div><b>٤ د</b>إحماء</div><div><b>٤ د</b>تذكّر ترتيب العمليات</div><div><b>٧ د</b>مثال ٢-٤ (ب)</div>
<div><b>٧ د</b>الكسور</div><div><b>٦ د</b>نحن</div><div><b>٦ د</b>أنتم</div><div><b>٣ د</b>انتبه</div><div><b>٣ د</b>بطاقة الخروج</div></div>''', 'divider'))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">إحماء 🔥</span>{timer(1)}</div>''' + quiz(f'أوجد قيمة {M(T("٢", "ح"), PL, T("٣", "ر"))} عندما ح = ٨ ، ر = ٥', [M('٣١'), M('٢٣'), M('٤١'), M('١٨')], 0, '٢ × ٨ = ١٦ و ٣ × ٥ = ١٥ ، ثم ١٦ + ١٥ = ٣١')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('كتاب الطالب ص ٤٨')}</div><h2>تذكّر ترتيب العمليات</h2>
<div class="ord">{''.join(st(f'<div><b>{n}</b><span>{t}</span></div>') for n, t in (('١', 'الأقواس'), ('٢', 'الأسس والجذور'), ('٣', 'الضرب والقسمة من اليمين إلى اليسار'), ('٤', 'الجمع والطرح من اليمين إلى اليسار')))}</div>'''))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('مثال ٢-٤ (ب)')}</div><h2>أوجد قيمة {M(V("س"), G("١٠", MI, V("ص")), cls="sm")}</h2>
{st(VALS(('س', '٤'), ('ص', '٧')))}
{box(STEPS(STP('نعوّض', M(SV('٤'), G('١٠', MI, SV('٧')), cls="sm")), STP('الأقواس أولاً', M('٤', X, '٣', cls="sm")), STP('ثم الضرب', M('١٢', cls="sm"), 'fin')))}'''))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('تمرين ٢ (أ، هـ)')}</div><h2>صيغ فيها كسور</h2>
<div class="row">{st(box(f'<div class="col"><span class="hint">{M(FR(V("د"), "٤"), cls="sm")} عندما د = ٣٢</span>{M(FR(SV("٣٢"), "٤"), EQ, "٣٢", DV, "٤", EQ, "٨", cls="sm")}</div>', style="flex:1"))}{st(box(f'<div class="col"><span class="hint">{M(FR("٣٠", V("ح")), MI, "٢", cls="sm")} عندما ح = ٦</span>{M(FR("٣٠", SV("٦")), MI, "٢", EQ, "٥", MI, "٢", EQ, "٣", cls="sm")}</div>', style="flex:1"))}</div>
{st('<div class="note">خطّ الكسر يعني <b>القسمة</b>، والقسمة قبل الطرح</div>')}'''))
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('تمرين ٢ (و)')}</div><h2>معاً: أوجد قيمة {M(FR(M(V("س"), PL, V("د")), "٢"), cls="sm")}</h2>
{st(VALS(('س', '١٩'), ('د', '١١')))}
<button class="flip box col"><span class="tap">👆 الحل</span><span class="hid col">{M(FR(M(SV('١٩'), PL, SV('١١')), '٢'), EQ, FR('٣٠', '٢'), EQ, '١٥', cls="sm")}<small class="hint">البسط كلّه يُحسب أولاً، كأنه بين قوسين</small></span></button>'''))
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('تمرين ٣ (أ، د)')}</div><h2>معاً: الأقواس أولاً</h2>
<div class="row">{st(f'<button class="flip box col" style="flex:1"><span class="hint">{M("٤", G(V("س"), PL, "٩"), cls="sm")} عندما س = ٣</span><span class="tap">👆</span><span class="hid">{M("٤", X, "١٢", EQ, "٤٨", cls="sm")}</span></button>')}{st(f'<button class="flip box col" style="flex:1"><span class="hint">{M("٢٠", DV, G(V("ع"), MI, "٧"), cls="sm")} عندما ع = ١٢</span><span class="tap">👆</span><span class="hid">{M("٢٠", DV, "٥", EQ, "٤", cls="sm")}</span></button>')}</div>'''))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ٣ (هـ)')}{timer(2)}</div>''' + quiz(f'أوجد قيمة {M(G("٥", PL, V("س")), DV, V("ص"))} عندما س = ٢٢ ، ص = ٣', [M('١٢٫٣'), M('٩'), M('٢٧'), M('٣')], 1, '(٥ + ٢٢) ÷ ٣ = ٢٧ ÷ ٣ = ٩')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ٣ (و)')}</div>''' + quiz(f'أوجد قيمة {M("١٨", MI, G(V("ع"), PL, V("ل")))} عندما ع = ٧ ، ل = ٣', [M('١٤'), M('٨'), M('٢٨'), M('٢')], 1, '١٨ − (٧ + ٣) = ١٨ − ١٠ = ٨ ، أمّا ١٤ فتنتج من الطرح قبل الأقواس')))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">انتبه ⚠️</span>{ref('دليل المعلم ص ٥٠')}</div><h2>أيّ الحلّين صحيح؟</h2>
<div class="errs">{''.join(st(f'<button class="flip err"><span class="xq">{q}</span><span class="tap">👆</span><span class="hid xa {c}">{w}</span></button>') for q, w, c in (
  (M(SV('٥'), PL, '٢', X, SV('٣'), EQ, '٧', X, '٣', EQ, '٢١'), '✘ جمع قبل الضرب', 'no'), (M(SV('٥'), PL, '٢', X, SV('٣'), EQ, '٥', PL, '٦', EQ, '١١'), '✔ الضرب أولاً', '')))}</div>''' + tn('الخطأ الشائع الثاني في الدليل: إجراء العمليات بترتيبٍ غير صحيح بعد التعويض. العبارة ع + ٢ل عندما ع = ٥ و ل = ٣.')))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ٢ 🎫</span><h2>أوجد القيمة</h2>
<div class="exit">{st(f'<div><b>١</b>{M(V("ح"), MI, T("٤", "د"), cls="sm")} عندما ح = ١٠ ، د = ٢</div>')}{st(f'<div><b>٢</b>{M(FR(V("ع"), "٢"), PL, V("ل"), cls="sm")} عندما ع = ١٦ ، ل = ٩</div>')}{st(f'<div><b>٣</b>{M("٢", G(V("ر"), MI, V("م")), cls="sm")} عندما ر = ١٥ ، م = ٧</div>')}</div>'''))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ٢ 🎫</span><h2>الإجابات</h2>
<button class="flip box col" style="min-width:40vw"><span class="tap">👆 اضغط لإظهار الإجابات</span><span class="hid col">{M('١٠', MI, '٨', EQ, '٢', cls="sm")}{M('٨', PL, '٩', EQ, '١٧', cls="sm")}{M('٢', X, '٨', EQ, '١٦', cls="sm")}</span></button>'''))

# ═══════════ الحصة الثالثة: استنتاج الصيغ واستخدامها ═══════════
S.append(slide('''<span class="tag">الحصة الثالثة · ٤٠ دقيقة</span><h2>استنتاج الصيغ واستخدامها</h2>
<div class="plan"><div><b>٣ د</b>إحماء</div><div><b>٨ د</b>مثال ٢-٤ (ج، د)</div><div><b>٦ د</b>نحن: الدقائق</div>
<div><b>٨ د</b>أنتم: نستخدم الصيغ</div><div><b>٦ د</b>فكّر: قيمة ك</div><div><b>٦ د</b>مسألة الطبخ</div><div><b>٣ د</b>بطاقة الخروج</div></div>''', 'divider'))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">إحماء 🔥</span>{timer(1)}</div>''' + quiz('كم يوماً في ٣ أسابيع؟', [M('١٠'), M('٢١'), M('٢٤'), M('٣٧')], 1, 'في الأسبوع ٧ أيام: ٧ × ٣ = ٢١')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('مثال ٢-٤ (ج)')}</div><h2>صيغة لعدد الأيام في أي عدد من الأسابيع</h2>
<div class="frm">{st(f'<div><span class="lab">بالكلمات</span><b>عدد الأيام = ٧ × عدد الأسابيع</b></div>')}{st(f'<div><span class="lab">بالحروف</span>{M(V("د"), EQ, T("٧", "ع"))}<small class="hint">د للأيام، ع للأسابيع</small></div>')}</div>
{st('<div class="note">نكتب العدد قبل الحرف دائماً: <b>٧ع</b> وليس ع٧</div>')}'''))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('مثال ٢-٤ (د)')}</div><h2>نستخدم الصيغة {M(V("د"), EQ, T("٧", "ع"), cls="sm")} لثمانية أسابيع</h2>
{st(VALS(('ع', '٨')))}
{box(STEPS(STP('نعوّض ع = ٨', M(V('د'), EQ, '٧', X, SV('٨'), cls="sm")), STP('نحسب', M(V('د'), EQ, '٥٦ يوماً', cls="sm"), 'fin')))}'''))
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('تمرين ٤')}</div><h2>معاً: صيغة لعدد الدقائق في أي عدد من الساعات</h2>
<div class="frm">{st(f'<button class="flip"><span class="lab">بالكلمات</span><span class="tap">👆</span><b class="hid">عدد الدقائق = ٦٠ × عدد الساعات</b></button>')}{st(f'<button class="flip"><span class="lab">بالحروف</span><span class="tap">👆</span><span class="hid">{M(V("د"), EQ, T("٦٠", "س"))}</span></button>')}{st(f'<button class="flip"><span class="lab">في ٥ ساعات</span><span class="tap">👆</span><span class="hid">{M(V("د"), EQ, "٦٠", X, SV("٥"), EQ, "٣٠٠ دقيقة")}</span></button>')}</div>'''))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ٥ (ب)')}{timer(2)}</div>''' + quiz(f'{M(V("ك"), EQ, V("ط") + V("ص"))} : أوجد ك إذا ط = ٤ ، ص = ٩', [M('١٣'), M('٤٩'), M('٣٦'), M('٩٤')], 2, 'طص تعني ط × ص = ٤ × ٩ = ٣٦')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ٦ (أ)')}</div><h2>صيغة سيف: {M(V("ع"), EQ, V("ح") + V("ص"), PL, V("و"), cls="sm")}</h2>
<div class="legend">{''.join(f'<span>{V(k)} {t}</span>' for k, t in (('ع', 'المبلغ المدفوع'), ('ح', 'عدد ساعات العمل'), ('ص', 'أجر الساعة'), ('و', 'العلاوة')))}</div>
<p class="ask">عدنان: يعمل ٢٠ ساعة بأجر ٢٢ ريالاً للساعة، وعلاوته ٣٠ ريالاً</p>
<button class="flip box col"><span class="tap">👆 الحل</span><span class="hid col">{M(V('ع'), EQ, SV('٢٠'), X, SV('٢٢'), PL, SV('٣٠'), cls="sm")}{M(EQ, '٤٤٠', PL, '٣٠', EQ, '٤٧٠ ريالاً', cls="sm")}</span></button>''' + tn('(ب) حمود: ٣٢ × ٢٠ + ٥٠ = ٦٤٠ + ٥٠ = ٦٩٠ ريالاً.')))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">فكّر 💡</span>{ref('تمرين ٧')}</div><h2>ما قيمة ك التي تعطي الناتج نفسه؟</h2>
<div class="kcards"><div><b>{M(V("ك"), PL, "١٠")}</b><span class="kv" data-f="k+10">؟</span></div><div><b>{M(T("٣", "ك"))}</b><span class="kv" data-f="3*k">؟</span></div><div><b>{M(T("٤", "ك"), MI, "٥")}</b><span class="kv" data-f="4*k-5">؟</span></div></div>
<div class="kbtn"><span>جرّب ك =</span>{''.join(f'<button type="button" data-k="{k}">{a(k)}</button>' for k in range(1, 8))}</div>
<script>(function(){{var s=document.currentScript.parentNode,A='٠١٢٣٤٥٦٧٨٩';function ar(n){{return String(n).replace(/[0-9]/g,function(d){{return A[d];}});}}
s.querySelectorAll('.kbtn button').forEach(function(b){{b.addEventListener('click',function(e){{e.stopPropagation();var k=+b.dataset.k,v=[];s.querySelectorAll('.kv').forEach(function(x){{var r=Function('k','return '+x.dataset.f)(k);v.push(r);x.textContent=ar(r);}});
var same=v.every(function(r){{return r===v[0];}});s.querySelector('.kcards').classList.toggle('same',same);s.querySelectorAll('.kbtn button').forEach(function(o){{o.classList.toggle('on',o===b);}});}});}});}})();</script>''' + tn('تعليق الدليل: ابدأ بالبطاقة ٣ك، فالناتج من مضاعفات ٣. ما العدد الذي نضيفه إلى ١٠ لنحصل على مضاعفٍ للعدد ٣؟ الإجابة ك = ٥ (الناتج ١٥ في البطاقات الثلاث). اضغط الأزرار لتجربة القيم أمام الطلاب.')))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">فكّر 💡</span>{ref('تمرين ٨ (ب)')}</div><h2>وقت طهي قطعة لحم كتلتها ٢ كغم</h2>
<div class="cook">{st(f'<button class="flip box"><span class="ck"><b>الفرن الكهربائي</b><span class="hint">الوقت = (٦٦ × الكتلة) + ٣٥</span></span><span class="tap">👆</span><span class="hid">{M("٦٦", X, SV("٢"), PL, "٣٥", EQ, "١٦٧ دقيقة", cls="sm")}</span></button>')}{st(f'<button class="flip box"><span class="ck"><b>الميكروويف</b><span class="hint">الوقت = (٢٦ × الكتلة) + ١٥</span></span><span class="tap">👆</span><span class="hid">{M("٢٦", X, SV("٢"), PL, "١٥", EQ, "٦٧ دقيقة", cls="sm")}</span></button>')}</div>
<button class="flip note"><span class="tap">👆 الفرق؟</span><span class="hid">١٦٧ − ٦٧ = ١٠٠ دقيقة، أي ساعة و ٤٠ دقيقة</span></button>''' + tn('تعليق الدليل: (أ) القيمتان ٢٦ و ١٥ أصغر قليلاً من نصف ٦٦ و ٣٥، فإن استغرق الفرن ساعتين فالميكروويف أقل من ساعة تقريباً. (ب) ٢: نعم معقولة، فوقت الفرن نحو مرتين ونصف وقت الميكروويف.')))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ٣ 🎫</span><h2>استخدم الصيغة</h2>
<div class="exit">{st(f'<div><b>١</b>اكتب صيغة بالحروف لعدد الساعات س في ي يوماً</div>')}{st(f'<div><b>٢</b>استخدمها لإيجاد عدد الساعات في ٤ أيام</div>')}{st(f'<div><b>٣</b>{M(V("ك"), EQ, V("ط") + V("ص"), cls="sm")} : أوجد ك إذا ط = ٣ ، ص = ٧</div>')}</div>'''))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ٣ 🎫</span><h2>الإجابات</h2>
<button class="flip box col" style="min-width:40vw"><span class="tap">👆 اضغط لإظهار الإجابات</span><span class="hid col">{M(V('س'), EQ, T('٢٤', 'ي'), cls="sm")}{M('٢٤', X, '٤', EQ, '٩٦ ساعة', cls="sm")}{M('٣', X, '٧', EQ, '٢١', cls="sm")}</span></button>'''))
S.append(slide('''<span class="qbadge" style="background:#0A6770;box-shadow:0 4px 0 #05393E">الواجب المنزلي 🏠</span><h2>بعد الحصص الثلاث</h2>
<div class="exit"><div class="st"><div><b>١</b>صفحة ٣٤ في كتاب النشاط (التعويض والصيغ)</div></div><div class="st"><div><b>٢</b>صفحتا ٣٥ و ٣٦ في كتاب النشاط (استخدام الصيغ)</div></div></div>'''))
S.append(slide(f'''<h2>الخلاصة</h2>
<div class="sumg">
{st(box('<div class="col"><b class="kk c-we">الصيغة</b><span>قاعدةٌ فيها إشارة =</span>' + M(V('م'), EQ, V('ل'), X, V('ض')) + '</div>'))}
{st(box('<div class="col"><b class="kk c-exp">التعويض</b><span>نضع العدد مكان الحرف</span>' + M(SV('٥'), X, SV('٤'), EQ, '٢٠') + '</div>'))}
{st(box('<div class="col"><b class="kk c-lcm">الترتيب</b><span>أقواس، أسس، ضرب وقسمة، جمع وطرح</span></div>'))}</div>'''))

# ═══════════ ملحق: تمارين كتاب الطالب ص٤٩–٥٠ (الإجابات من دليل المعلم ص٥٥–٥٦) ═══════════
S.append(launch('sb', '٤٩ و ٥٠', note=f'المراجع: كتاب الطالب ص٤٨ إلى ٥٠، ودليل المعلم ص٥٠ و ٥١ وإجاباته ص٥٥ و ٥٦ · {ME}'))
H = ['أ', 'ب', 'ج', 'د', 'هـ', 'و', 'ز', 'ح', 'ط', 'ي', 'ك', 'ل']
RL = 'نعوّض كل حرفٍ بقيمته، ثم نحسب بترتيب العمليات'
def P(h, q, when, sub, ans): return (f'({h}) {q}<small>عندما {when}</small>', f'{M(sub, EQ, ans)}')
S.append(ex(1, 'أوجد قيمة كلٍّ من العبارات الجبرية', RL, [
  P('أ', M(V('ص'), PL, '٥'), 'ص = ٣', M(SV('٣'), PL, '٥'), '٨'), P('ب', M(V('س'), MI, '٩'), 'س = ٢٠', M(SV('٢٠'), MI, '٩'), '١١'),
  P('ج', M(V('و'), PL, V('ر')), 'و = ٧ ، ر = ٤', M(SV('٧'), PL, SV('٤')), '١١'), P('د', M(V('م'), MI, V('ع')), 'م = ١٠٠ ، ع = ٢٥', M(SV('١٠٠'), MI, SV('٢٥')), '٧٥'),
  P('هـ', M(T('٣', 'ك')), 'ك = ٥', M('٣', X, SV('٥')), '١٥'), P('و', M(V('ع'), PL, T('٢', 'ل')), 'ع = ٥ ، ل = ٣', M(SV('٥'), PL, '٢', X, SV('٣')), '١١')], cols=2, per=2))
S.append(ex(2, 'أوجد قيمة كلٍّ من العبارات الجبرية', 'خطّ الكسر قسمة، والضرب والقسمة قبل الجمع والطرح', [
  P('أ', M(FR(V('د'), '٤')), 'د = ٣٢', M(FR(SV('٣٢'), '٤')), '٨'), P('ب', M(V('ح'), MI, T('٤', 'د')), 'ح = ١٠ ، د = ٢', M(SV('١٠'), MI, '٤', X, SV('٢')), '٢'),
  P('ج', M(T('٢', 'ح'), PL, T('٣', 'ر')), 'ح = ٨ ، ر = ٥', M('١٦', PL, '١٥'), '٣١'), P('د', M(FR(V('ع'), '٢'), PL, V('ل')), 'ع = ١٦ ، ل = ٩', M('٨', PL, SV('٩')), '١٧'),
  P('هـ', M(FR('٣٠', V('ح')), MI, '٢'), 'ح = ٦', M('٥', MI, '٢'), '٣'), P('و', M(FR(M(V('س'), PL, V('د')), '٢')), 'س = ١٩ ، د = ١١', M(FR('٣٠', '٢')), '١٥')], cols=2, per=2))
S.append(ex(3, 'أوجد قيمة كل عبارة جبرية', 'نحسب ما بين الأقواس أولاً', [
  P('أ', M('٤', G(V('س'), PL, '٩')), 'س = ٣', M('٤', X, '١٢'), '٤٨'), P('ب', M('٢', G(V('ر'), MI, V('م'))), 'ر = ١٥ ، م = ٧', M('٢', X, '٨'), '١٦'),
  P('ج', M(V('ع'), G(V('ل'), PL, '١٢')), 'ع = ٣ ، ل = ٨', M('٣', X, '٢٠'), '٦٠'), P('د', M('٢٠', DV, G(V('ع'), MI, '٧')), 'ع = ١٢', M('٢٠', DV, '٥'), '٤'),
  P('هـ', M(G('٥', PL, V('س')), DV, V('ص')), 'س = ٢٢ ، ص = ٣', M('٢٧', DV, '٣'), '٩'), P('و', M('١٨', MI, G(V('ع'), PL, V('ل'))), 'ع = ٧ ، ل = ٣', M('١٨', MI, '١٠'), '٨')], cols=2, per=2))
S.append(ex(4, 'صيغة لعدد الدقائق في أي عدد من الساعات', 'في الساعة ٦٠ دقيقة', [
  ('(أ) ١ بالكلمات', 'عدد الدقائق = ٦٠ × عدد الساعات'), ('(أ) ٢ بالمتغيّرات', M(V('د'), EQ, T('٦٠', 'س'))), ('(ب) في ٥ ساعات', M('٦٠', X, SV('٥'), EQ, '٣٠٠ دقيقة'))], cols=2))
S.append(ex(5, 'استخدم الصيغة ك = طص لإيجاد ك', 'طص تعني ط × ص', [('(أ) ط = ٣ ، ص = ٧', M('٣', X, '٧', EQ, '٢١')), ('(ب) ط = ٤ ، ص = ٩', M('٤', X, '٩', EQ, '٣٦'))], cols=2))
S.append(ex(6, 'صيغة سيف: ع = حص + و', 'ح الساعات، ص أجر الساعة، و العلاوة', [('(أ) عدنان: ٢٠ ساعة × ٢٢ ريالاً، والعلاوة ٣٠', M('٤٤٠', PL, '٣٠', EQ, '٤٧٠ ريالاً')), ('(ب) حمود: ٣٢ ساعة × ٢٠ ريالاً، والعلاوة ٥٠', M('٦٤٠', PL, '٥٠', EQ, '٦٩٠ ريالاً'))], cols=1, per=2))
S.append(ex(7, 'قيمة ك التي تعطي الناتج نفسه', 'البطاقات: ك + ١٠ و ٣ك و ٤ك − ٥، ونبدأ بالبطاقة ٣ك', [('الإجابة', 'ك = ٥<small>٥ + ١٠ = ١٥ ، ٣ × ٥ = ١٥ ، ٢٠ − ٥ = ١٥</small>')], cols=1))
S.append(ex(8, 'مسألة وقت الطهي', 'الفرن: (٦٦ × الكتلة) + ٣٥ ، الميكروويف: (٢٦ × الكتلة) + ١٥', [
  ('(أ) ساعتان في الفرن، فكم في الميكروويف؟', 'أقل من ساعة تقريباً<small>٢٦ و ١٥ أقل قليلاً من نصف ٦٦ و ٣٥</small>'),
  ('(ب) ١ قطعة ٢ كغم: كم الفرق؟', '١٦٧ − ٦٧ = ١٠٠ دقيقة<small>أي ساعة و ٤٠ دقيقة</small>'),
  ('(ب) ٢ هل إجابة (أ) معقولة؟', 'نعم<small>وقت الفرن نحو مرتين ونصف وقت الميكروويف</small>')], cols=1, per=2))

# ═══════════ ملحق: حلول كتاب النشاط ص٣٤–٣٦ (الإجابات من دليل المعلم ص٥٩) ═══════════
S.append(launch('ab', '٣٤ إلى ٣٦', note='الإجابات النهائية من دليل المعلم ص ٥٩'))
NA, NB, NC = 'نشاط ص ٣٤ · تمرين', 'نشاط ص ٣٥ · تمرين', 'نشاط ص ٣٦ · تمرين'
S.append(ex(1, 'أوجد قيمة كلٍّ من العبارات الجبرية', RL, [
  P('أ', M(V('ح'), PL, '١٠'), 'ح = ٦', M(SV('٦'), PL, '١٠'), '١٦'), P('ب', M(V('د'), MI, '٣'), 'د = ١٢٠', M(SV('١٢٠'), MI, '٣'), '١١٧'),
  P('ج', M(V('ر'), PL, V('س')), 'ر = ٣ ، س = ١٧', M(SV('٣'), PL, SV('١٧')), '٢٠'), P('د', M(V('د'), MI, V('ص')), 'د = ٤٠ ، ص = ١٥', M(SV('٤٠'), MI, SV('١٥')), '٢٥'),
  P('هـ', M(T('٣', 'هـ')), 'هـ = ٢٠', M('٣', X, SV('٢٠')), '٦٠'), P('و', M(FR(V('و'), '٥')), 'و = ٣٥', M(FR(SV('٣٥'), '٥')), '٧'),
  P('ز', M(V('ط'), PL, T('٢', 'س')), 'ط = ١ ، س = ٦', M(SV('١'), PL, '١٢'), '١٣'), P('ح', M(V('ح'), MI, T('٤', 'م')), 'ح = ١٧ ، م = ٢', M(SV('١٧'), MI, '٨'), '٩'),
  P('ط', M(T('٢', 'ط'), PL, T('٣', 'ل')), 'ط = ٣ ، ل = ٢', M('٦', PL, '٦'), '١٢'), P('ي', M(FR(V('س'), '٢'), PL, V('ص')), 'س = ٣٠ ، ص = ٣', M('١٥', PL, SV('٣')), '١٨'),
  P('ك', M(FR('٢٤', V('ك')), MI, '٣'), 'ك = ٨', M('٣', MI, '٣'), '٠'), P('ل', M(FR(M(V('ع'), PL, V('هـ')), '٣')), 'ع = ١١ ، هـ = ٢٢', M(FR('٣٣', '٣')), '١١')], cols=2, src=NA, per=2))
S.append(ex(2, 'صيغة هلال لمقدار النقود', 'مقدار النقود = المسافة بالكيلومتر × سعر التبرّع لكل كيلومتر', [('(أ) محمود: ٥ كم × ١٦ ريالاً', M('٥', X, '١٦', EQ, '٨٠ ريالاً')), ('(ب) أسامة: ٨ كم × ١٨ ريالاً', M('٨', X, '١٨', EQ, '١٤٤ ريالاً'))], cols=1, per=2, src=NA))
S.append(ex(3, 'صيغة لعدد الساعات في عددٍ من الأيام', 'في اليوم ٢٤ ساعة', [('(أ) ١ بالكلمات', 'عدد الساعات = ٢٤ × عدد الأيام'), ('(أ) ٢ بالحروف', M(V('س'), EQ, T('٢٤', 'ي'))), ('(ب) في ٤ أيام', M('٢٤', X, SV('٤'), EQ, '٩٦ ساعة'))], cols=2, src=NA))
S.append(ex(4, 'استخدم الصيغة د = م ح', 'م ح تعني م × ح', [('(أ) م = ٤ ، ح = ٥', M('٤', X, '٥', EQ, '٢٠')), ('(ب) م = ٣ ، ح = ١٢', M('٣', X, '١٢', EQ, '٣٦'))], cols=2, src=NB))
S.append(ex(5, 'صيغة هاجر للوقت', 'و = م ÷ س ، أي الوقت = المسافة ÷ السرعة', [('(أ) ٦٠ كم بسرعة ٢٠ كم/ساعة', M('٦٠', DV, '٢٠', EQ, '٣ ساعات')), ('(ب) ١٤٠ كم بسرعة ٤٠ كم/ساعة', M('١٤٠', DV, '٤٠', EQ, '٣٫٥ ساعات'))], cols=1, per=2, src=NB))
S.append(ex(6, 'صيغة أمجد: و = ك ر + ل', 'ك الكتلة، ر الوقت لكل كغم، ل الوقت الإضافي', [('(أ) ٢ كغم ، ٤٠ دقيقة لكل كغم ، ٢٠ إضافية', M('٨٠', PL, '٢٠', EQ, '١٠٠ دقيقة') + '<small>ساعة و ٤٠ دقيقة</small>'), ('(ب) ٥ كغم ، ٣٥ دقيقة لكل كغم ، ١٠ إضافية', M('١٧٥', PL, '١٠', EQ, '١٨٥ دقيقة') + '<small>٣ ساعات و ٥ دقائق</small>')], cols=1, per=2, src=NB))
S.append(ex(7, 'قيمة س التي تعطي الناتج نفسه', 'البطاقات: ٦س − ٨ و ٤س و س + ١٢، ونبدأ بالبطاقة ٤س', [('الإجابة', 'س = ٤<small>٢٤ − ٨ = ١٦ ، ٤ × ٤ = ١٦ ، ٤ + ١٢ = ١٦</small>')], cols=1, src=NC))
S.append(ex(8, 'أيّ الشركتين تختار شيماء؟', 'نعوّض المسافة ٨٠ كم في صيغتي التكلفة ونقارن', [('الأولى: (٠٫٣٠ × ٨٠) + ٢٥', M('٢٤', PL, '٢٥', EQ, '٤٩ ريالاً')), ('الثانية: (٠٫٢٥ × ٨٠) + ٣٥', M('٢٠', PL, '٣٥', EQ, '٥٥ ريالاً')), ('القرار', 'الشركة الأولى<small>لأنها أرخص</small>')], cols=1, per=2, src=NC))

EXTRA_CSS_OWN = '''
.var{color:var(--exp);font-weight:900}
.term,.grp{display:inline-flex;direction:rtl;unicode-bidi:isolate;align-items:center}.grp{gap:.2em}
.fr{display:inline-flex;flex-direction:column;align-items:center;line-height:1.05;vertical-align:middle;margin:0 .1em}
.fr>span:first-child{border-bottom:.07em solid currentColor;padding:0 .15em .04em;align-self:stretch;text-align:center}
.sbv{display:inline-block;font-size:1em;background:#FFF1E6;color:#C2410C;border:3px solid #F5B585;border-radius:.3em;padding:0 .18em;line-height:1.2}
.vals{display:flex;gap:1.6vw;justify-content:center;flex-wrap:wrap}
.vals>span{font-family:var(--fh);font-weight:800;font-size:clamp(26px,5vh,58px);background:#EAF7F8;border:3px solid var(--base);border-radius:999px;padding:.1em .9em}
.stps{display:flex;flex-direction:column;gap:1.6vh;align-items:stretch}
.stp{display:flex;align-items:center;gap:1.6vw;justify-content:space-between}
.stp .lab,.frm .lab{flex:none;font-family:var(--fh);font-weight:800;color:#2563EB;background:#EAF1FF;border-radius:12px;padding:.2em .8em;text-align:center}
.stp.fin .lab{background:var(--good);color:#fff}
.rulebox{font-weight:800;font-size:clamp(28px,5.2vh,62px);background:#EAF7F8;border:4px solid var(--base);border-radius:20px;padding:1.2vh 2vw;text-align:center;line-height:1.5}
.box .col>.m:not(.mid):not(.sm):not(.big),.hid.col>.m:not(.mid):not(.sm):not(.big){font-size:clamp(34px,6.4vh,76px)}
.frm{display:flex;flex-direction:column;gap:1.6vh;width:min(1300px,90vw)}
.frm .st>div,.frm .st>button{display:flex;align-items:center;gap:2vw;background:#fff;border:3px solid var(--line);border-radius:18px;padding:1.2vh 1.6vw;font-size:clamp(28px,5.2vh,60px);font-weight:800;width:100%;font-family:var(--fb);color:var(--ink)}
.frm .hint{font-size:.8em}
.life{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:2vw;width:min(1500px,92vw)}
.life .st>div{display:flex;flex-direction:column;align-items:center;gap:.8vh;background:#fff;border:3px solid var(--line);border-radius:20px;padding:2vh 1vw;text-align:center}
.life .ic2{font-size:clamp(56px,11vh,120px)}.life b{font-size:clamp(32px,6vh,68px)}.life small{font-weight:700;font-size:clamp(24px,4.6vh,52px);color:var(--ink2)}
.ord{display:flex;flex-direction:column;gap:1.4vh;width:min(1200px,88vw)}
.ord .st>div{display:flex;align-items:center;gap:1.6vw;background:#fff;border:3px solid var(--line);border-radius:16px;padding:1vh 1.6vw;font-weight:800;font-size:clamp(28px,5.2vh,60px)}
.ord b{flex:none;width:1.6em;height:1.6em;border-radius:50%;background:var(--ink);color:#fff;display:flex;align-items:center;justify-content:center}
.errs{display:flex;flex-direction:column;gap:1.4vh;width:min(1400px,92vw)}
.errs .err{display:flex;flex-direction:column;align-items:center;gap:.6vh;background:#fff;border:3px solid var(--line);border-radius:16px;padding:.8vh 1.6vw;font-size:clamp(28px,5.4vh,62px)}
.errs .err .xq{font-size:inherit}.errs .err .xa{font-size:clamp(24px,4.4vh,50px)}
.legend{display:flex;flex-wrap:wrap;gap:1vw;justify-content:center}
.legend span{font-weight:700;font-size:clamp(24px,4.4vh,50px);background:#F4F7FB;border:2px solid var(--line);border-radius:12px;padding:.1em .6em}
.kcards{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:2vw;width:min(1300px,90vw)}
.kcards>div{display:flex;flex-direction:column;align-items:center;gap:1vh;background:#fff;border:4px solid var(--line);border-radius:20px;padding:2vh 1vw;font-size:clamp(34px,6.4vh,74px)}
.kcards .kv{font-family:var(--fh);font-weight:900;color:var(--base)}
.kcards.same>div{border-color:var(--good);background:#F2FBF5}.kcards.same .kv{color:var(--good)}
.kbtn{display:flex;align-items:center;gap:.8vw;flex-wrap:wrap;justify-content:center;font-weight:800;font-size:clamp(30px,5.6vh,64px)}
.kbtn button{font:inherit;min-width:2.2em;border-radius:12px;border:3px solid var(--line);background:#fff;cursor:pointer;color:var(--ink)}
.kbtn button.on{background:var(--base);color:#fff;border-color:var(--base)}
.cook{display:flex;flex-direction:column;gap:1.4vh;width:min(1400px,92vw)}.cook .box{display:flex;flex-direction:row;align-items:center;justify-content:space-between;gap:1.6vw;width:100%}.cook .ck{display:flex;flex-direction:column;align-items:flex-start;gap:.4vh}
.cook b{font-size:clamp(28px,5.2vh,60px)}.cook .hint{font-size:clamp(24px,4.4vh,50px)}
button.note{font-family:inherit;font-weight:800;font-size:clamp(28px,5.2vh,60px);cursor:pointer;color:var(--ink)}button.note .hid,button.note .tap{font-size:inherit}
.sumg{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:2vw;width:min(1600px,94vw)}
.sumg .col span{font-weight:700;font-size:clamp(26px,4.6vh,56px);line-height:1.4}
.sumg .kk{font-size:clamp(34px,6.4vh,76px)}
.xq small{display:block;font-size:.75em;color:var(--ink2)}
'''

# صفحات تمارين كتاب الطالب لشارة «كتاب الطالب ص … · تمرين …» (common_slides.py)
PG = {'تمرين': [(1, '٤٩'), (6, '٥٠')]}
