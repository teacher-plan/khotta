# شرائح درس ١-٦ «القوى (الأسس) والجذور» — الصف السابع (حصتان، كتاب الطالب ص٣٢–٣٤)
# المراجع: دليل المعلم ص٣١ وما بعدها، كتاب الطالب ص٣٢–٣٤، وورقتا «درسي في صفحة» (القوى، الجذور).
# يُستورد من gen_powers.py بعد تعريف الدوال المساعدة (P, R, N, PN, M, mode, timer, quiz, st, box …).

def PM(v): return f'<span class="ng"><i>±</i>{a(v)}</span>'   # ±٥ كما يكتبها الكتاب، والإشارة يمين العدد
def ref(t): return f'<span class="ref">📘 {t}</span>'
def mk(): return '<span class="bk"><span class="blank">؟</span><sup class="e2">٢</sup></span>'  # الأسّ ملتصقٌ بالمربّع الفارغ

S = []
# ═══ الشريحة الأولى: العنوان + أهداف الدرس بصيغة «أنا أستطيع» (من نقاط التعلّم في دليل المعلم) ═══
CAN = ['أكتب الضرب المتكرر بالصورة الأسية، وأميّز <b class="c-b">الأساس</b> من <b class="c-exp">الأس</b>',
       'أجد قيمة القوى ذهنياً بسرعة ودقة، وأقارن بين قوّتين',
       'أتذكّر الأعداد المربّعة حتى <b>٢٠ × ٢٠ = ٤٠٠</b> ومكعبات الأعداد ١ – ١٠',
       f'أجد الجذر التربيعي للعدد المربّع {M(R(25),EQ,PM(5))} والجذر التكعيبي {M(R(125,3),EQ,"٥")}']
S.append(slide('''<span class="tag">الصف السابع · الدرس ١-٦</span>
<h1 class="h1s">القوى والجذور</h1>
<p class="lead">كتاب الطالب ص ٣٢–٣٤</p>
<p class="lead" style="font-size:clamp(26px,4.8vh,56px)">إعداد: أ. عيسى الحارثي</p>''', 'cover'))
S.append(slide(f'''<h2>في نهاية هذا الدرس…</h2>
<div class="can">{''.join(f'<div><span class="can-i">✔</span><span><b>أنا أستطيع</b> أن {t}</span></div>' for t in CAN)}</div>'''))

# ═══ المفردات (من دليل المعلم) ═══
S.append(slide(f'''<h2>مفردات الدرس</h2>
{st('<div class="vocab wide"><div><span>قوى العدد</span><i>power</i></div><div><span>مربّع العدد</span><i>square</i></div><div><span>الجذر التربيعي</span><i>square root</i></div><div><span>الأُسس</span><i>indices</i></div><div><span>مكعّب العدد</span><i>cube</i></div><div><span>الجذر التكعيبي</span><i>cube root</i></div></div>')}
<div class="row">{M(P(5,2),cls="mid")}{M(P(5,3),cls="mid")}{M(R(25),cls="mid")}{M(R(125,3),cls="mid")}</div>
<p class="lead">نتعلّم معاً ثم نتدرّب: <b class="c-i">أنا</b> ← <b class="c-we">نحن</b> ← <b class="c-u">أنتم</b></p>'''))

# ═══ الحصة الأولى ═══
S.append(slide(f'''<span class="tag">الحصة الأولى · ٤٠ دقيقة</span><h2>قوّة العدد، والمربعات والمكعبات</h2>
<div class="plan">
<div><b>٥ د</b>نشاط: كم تكبر قوى العدد ٢؟</div><div><b>١٠ د</b>مفهوم القوّة: التربيع والتكعيب</div>
<div><b>١٢ د</b>إيجاد قيمة القوّة والأخطاء الشائعة</div><div><b>٩ د</b>المربعات والمكعبات في مدى</div><div><b>٤ د</b>بطاقة الخروج</div></div>''', 'divider'))

# نشاط دليل المعلم: ٢² ، ٢³ … حتى نتجاوز ١٠٠٠
chain = ''.join(st(box(M(P(2,k),EQ,a(2**k),cls="sm"),cls=('hot' if k==10 else ''))) for k in range(2,11))
S.append(slide(f'''<span class="qbadge">نشاط 🚀</span><h2>ما أوّل أسٍّ للعدد ٢ يعطي عدداً أكبر من ١٠٠٠؟</h2>
<div class="chain">{chain}</div>
{st('<div class="note">الأس <b>١٠</b> — للمجيدين: أصغر أسٍّ للعدد ١٠ يصل إلى مليون؟ (<b>٦</b>)</div>')}'''))

# المفهوم
S.append(slide(f'''<h2>قوى العدد</h2><p class="lead st">نكرّر ضرب العدد في نفسه، و<b class="c-exp">الأس</b> يبيّن عدد المرّات</p>
<div class="pw">
{st(f'<div class="pwr">{M(P(5,2),EQ,rep(5,2),EQ,"٢٥",cls="sm")}<span class="rd">خمسة <b>تربيع</b></span></div>')}
{st(f'<div class="pwr">{M(P(5,3),EQ,rep(5,3),EQ,"١٢٥",cls="sm")}<span class="rd">خمسة <b>تكعيب</b></span></div>')}
{st(f'<div class="pwr">{M(P(5,4),EQ,rep(5,4),EQ,"٦٢٥",cls="sm")}<span class="rd">خمسة أس <b>أربعة</b></span></div>')}
</div>'''))
S.append(slide(f'''<h2>لماذا نقول «تربيع»؟</h2>
<div class="row" style="align-items:center"><div class="grid g5 st" id="g5">{"<i></i>"*25}</div>
<div class="col">{st(M(P(5),X,P(5),EQ,'٢٥',cls="mid"))}{st(M(P(5,2),EQ,'٢٥',cls="mid"))}{st('<p class="lead">مربّعٌ ضلعه ٥ فيه ٢٥ بلاطة — لذلك ٢٥ <b class="c-b">مربّع العدد ٥</b></p>')}</div></div>'''))
S.append(slide(f'''<h2>ولماذا نقول «تكعيب»؟</h2><p class="lead">المكعّب طبقاتٌ متطابقة: كل طبقة مربّع</p>
<div class="row layers">{''.join(st(f'<div class="col"><div class="grid g3">{"<i></i>"*9}</div><small>طبقة {a(k)}</small></div>') for k in (1,2,3))}</div>
{st(M(P(3,3),EQ,'٣ طبقات',X,'٩',EQ,'٢٧',cls="mid"))}'''))

# أنا / أخطاء شائعة / نحن / أنتم
S.append(slide(f'''{mode('i')}<h2>أوجد قيمة: {M(P(9,2))} و {M(P(7,3))}</h2>
<div class="row">{box(f'<div class="col">{M(P(9,2),cls="mid")}{st(M(rep(9,2),cls="sm"))}{st(M(EQ,"٨١",cls="mid res"))}</div>')}
{box(f'<div class="col">{M(P(7,3),cls="mid")}{st(M(rep(7,3),cls="sm"))}{st(M(EQ,"٤٩",X,"٧",cls="sm"))}{st(M(EQ,"٣٤٣",cls="mid res"))}</div>')}</div>'''))
S.append(slide(f'''<span class="qbadge">انتبه ⚠️ خطأ شائع</span><h2>الأس ليس عدداً نضرب فيه!</h2>
<div class="row">
{st(box(f'<div class="col"><span class="wrong">✘</span>{M(P(4,2),EQ,"٤",X,"٢",EQ,"٨",cls="sm")}<span class="wrong">✘</span>{M(P(2,4),EQ,"٢",X,"٤",EQ,"٨",cls="sm")}</div>',style="border-color:var(--bad);background:#FFF5F5"))}
{st(box(f'<div class="col"><span class="right">✔</span>{M(P(4,2),EQ,rep(4,2),EQ,"١٦",cls="sm")}<span class="right">✔</span>{M(P(2,4),EQ,rep(2,4),EQ,"١٦",cls="sm")}</div>',style="border-color:var(--good);background:#F2FBF5"))}</div>
{st('<div class="note">الأس يخبرنا <b>كم مرّة</b> نكتب الأساس ثم نضرب — قُل دائماً: «٤ مضروبة في نفسها مرتين»</div>')}'''))
S.append(slide(f'''{mode('we')}<h2>معاً: {M(P(10,5))} و {M(P(3,4))}</h2>
<div class="row">{box(f'<div class="col"><p class="ask">كم مرّة نكتب العدد ١٠؟</p>{st(M(rep(10,5),cls="sm"))}{st(M(EQ,"١٠٠٠٠٠",cls="mid res"))}{st('<small class="hint">لاحظ: خمسة أصفار = الأس ٥</small>')}</div>')}
{box(f'<div class="col"><p class="ask">وهنا؟</p>{st(M(rep(3,4),cls="sm"))}{st(M(EQ,"٩",X,"٩",cls="sm"))}{st(M(EQ,"٨١",cls="mid res"))}</div>')}</div>'''))
S.append(slide(f'''<div class="row hdr"><div class="row hdr">{mode('u')}{ref('تمرين ٨ (ب)')}</div>{timer(2)}</div>''' + quiz(f'أوجد قيمة {M(P(3,3))}', [M('٩'), M('٢٧'), M('٦'), M('٣٣')], 1, '٣ × ٣ × ٣ = ٢٧ — وليس ٣ × ٣')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ٨ (ج)')}</div>''' + quiz(f'أوجد قيمة {M(P(3,4))}', [M('١٢'), M('٢٧'), M('٨١'), M('٦٤')], 2, '٣ × ٣ × ٣ × ٣ = ٩ × ٩ = ٨١ — لاحظ: كل قوّة = السابقة × ٣')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ١٩ (ب)')}</div>''' + quiz(f'أوجد قيمة {M(P(10,3))}', [M('٣٠'), M('١٠٠'), M('١٠٠٠'), M('١٠٣')], 2, 'قاعدة: قوى العدد ١٠ ← عدد الأصفار = الأس')))

# جداول الحفظ
for lo, hi in ((1, 10), (11, 20)):   # عشرة في كل شريحة ليبقى الخط كبيراً
    cards = ''.join(f'<button class="sq pw2"><span class="n">{M(P(n,2),EQ)}</span><span class="v">{a(n*n)}</span></button>' for n in range(lo, hi + 1))
    S.append(slide(f'''<div class="row hdr"><h2>احفظ الأعداد المربّعة: {a(lo)} – {a(hi)}</h2>{ref('تمرين ١')}</div>
<div class="sqs c5">{cards}</div><button class="reveal-all">اكشف الكل</button>'''))
cards = ''.join(f'<button class="sq cu pw2"><span class="n">{M(P(n,3),EQ)}</span><span class="v">{a(n**3)}</span></button>' for n in range(1, 11))
S.append(slide(f'''<div class="row hdr"><h2>احفظ مكعبات الأعداد ١ – ١٠</h2>{ref('كتاب الطالب ص ٣٢')}</div>
<div class="sqs c5">{cards}</div><button class="reveal-all">اكشف الكل</button>'''))

# المربعات في مدى (تمرين ٢)
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('تمرين ٢ (أ)')}</div><h2>اكتب كلّ الأعداد المربّعة من ١٠٠ إلى ٢٠٠</h2>
<div class="row">{''.join(st(box(M(P(n,2),EQ,a(n*n),cls="sm"),style=('opacity:.5' if n*n>200 else ''))) for n in range(10,16))}</div>
{st(f'<div class="ans l" style="border-color:var(--base);background:#EAF7F8"><span class="m sm">١٠٠ ، ١٢١ ، ١٤٤ ، ١٦٩ ، ١٩٦</span></div>')}'''))
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('تمرين ٢ (ج)')}</div><h2>الأعداد المربّعة من ٣٠٠ إلى ٤٠٠</h2><p class="ask">من أين نبدأ؟ ما أوّل عددٍ مربّعه أكبر من ٣٠٠؟</p>
<div class="row">{''.join(st(box(M(P(n,2),EQ,a(n*n),cls="sm"),style=('opacity:.45' if not 300<=n*n<=400 else ''))) for n in (17,18,19,20,21))}</div>
{st(f'<div class="ans l" style="border-color:var(--base);background:#EAF7F8"><span class="m sm">٣٢٤ ، ٣٦١ ، ٤٠٠</span></div>')}'''))
S.append(slide(f'''<div class="row hdr"><div class="row hdr">{mode('u')}{ref('تمرين ٢ (ب)')}</div>{timer(2)}</div>''' + quiz('ما الأعداد المربّعة من ٢٠٠ إلى ٣٠٠؟', [M('٢٢٥ ، ٢٥٦ ، ٢٨٩'), M('٢٠٠ ، ٢٥٠ ، ٣٠٠'), M('٢١٦ ، ٢٤٣ ، ٢٨٩'), M('١٩٦ ، ٢٢٥ ، ٢٥٦')], 0, '١٥² = ٢٢٥ ، ١٦² = ٢٥٦ ، ١٧² = ٢٨٩ (و ١٨² = ٣٢٤ أكبر من ٣٠٠)')))

# بطاقة الخروج ١ + الواجب
S.append(slide(f'''<span class="qbadge">بطاقة الخروج 🎫</span><h2>أجب في دفترك قبل الخروج</h2>
<div class="exit">{st(f'<div><b>١</b>أوجد قيمة {M(P(8,2))}</div>')}{st(f'<div><b>٢</b>أوجد قيمة {M(P(3,4))}</div>')}{st(f'<div><b>٣</b>اكتب الأعداد المربّعة من ٥٠ إلى ١٠٠</div>')}</div>
<button class="flip box col" style="min-width:40vw"><span class="tap">👆 اضغط لإظهار الإجابات</span><span class="hid col">{M("٦٤",cls="sm")}{M("٨١",cls="sm")}{M("٦٤ ، ٨١ ، ١٠٠",cls="sm")}</span></button>'''))

# ═══ الحصة الثانية ═══
S.append(slide(f'''<span class="tag">الحصة الثانية · ٤٠ دقيقة</span><h2>نقارن القوى، ونستفيد منها، ونتعرّف الجذور</h2>
<div class="plan">
<div><b>٤ د</b>إحماء: تحدّي المربعات السريع</div><div><b>٦ د</b>أيّ العددين أكبر؟</div>
<div><b>٥ د</b>نستخدم حقيقةً لنجد غيرها</div><div><b>٥ د</b>العدد المفقود</div><div><b>١٢ د</b>الجذور التربيعية والتكعيبية</div><div><b>٥ د</b>ألغاز وتفكير</div><div><b>٣ د</b>بطاقة الخروج</div></div>''', 'divider'))
flash = ''.join(f'<button class="sq"><span class="n">{M(P(n,2))}</span><span class="v">{a(n*n)}</span></button>' for n in (7, 12, 15, 9, 13, 20, 11, 16))
S.append(slide(f'''<span class="qbadge">إحماء ⚡</span><h2>مَن يجيب أوّلاً؟</h2><div class="sqs c4">{flash}</div>'''))

# المقارنة (تمرين ٩)
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('تمرين ٩ (أ)')}</div><h2>أيّهما أكبر: {M(P(3,5))} أم {M(P(5,3))} ؟</h2>
<div class="row">{box(f'<div class="col">{M(P(3,5),cls="mid")}{st(M(rep(3,5),cls="sm"))}{st(M(EQ,"٢٤٣",cls="mid res"))}</div>')}
{box(f'<div class="col">{M(P(5,3),cls="mid")}{st(M(rep(5,3),cls="sm"))}{st(M(EQ,"١٢٥",cls="mid res"))}</div>')}</div>
{st(f'<div class="note">{M(P(3,5))} أكبر — نحسب ثم نقارن</div>')}'''))
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('تمرين ٩ (ج)')}</div><h2>أيّهما أكبر: {M(P(5,4))} أم {M(P(4,5))} ؟</h2>
<div class="row">{box(f'<div class="col">{M(P(5,4),cls="mid")}{st(M(rep(5,4),cls="sm"))}{st(M(EQ,"٦٢٥",cls="mid res"))}</div>')}
{box(f'<div class="col">{M(P(4,5),cls="mid")}{st(M(rep(4,5),cls="sm"))}{st(M(EQ,"١٠٢٤",cls="mid res"))}</div>')}</div>
{st(f'<div class="note">{M(P(4,5))} أكبر</div>')}'''))
S.append(slide(f'''<div class="row hdr"><div class="row hdr">{mode('u')}{ref('تمرين ٩ (ب)')}</div>{timer(2)}</div>''' + quiz(f'أيّهما أكبر: {M(P(12,2))} أم {M(P(2,6))} ؟', [M(P(12,2)), M(P(2,6)), 'متساويان'], 0, '١٢ تربيع = ١٤٤ و ٢ أس ٦ = ٦٤ ، إذن ١٢ تربيع أكبر')))

# ٢^١٠ (تمرين ١٥)
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('تمرين ١٥')}</div><h2>إذا علمت أن {M(P(2,10),EQ,'١٠٢٤')} فأوجد {M(P(2,11))}</h2>
{st(f'<p class="lead">{M(P(2,11))} تعني أننا ضربنا العدد ٢ مرّةً <b>إضافية</b></p>')}
{st(box(M(P(2,11),EQ,P(2,10),X,'٢',cls="mid")))}{st(box(M(EQ,'١٠٢٤',X,'٢',EQ,'٢٠٤٨',cls="mid")))}'''))
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('تمرين ١٥')}</div><h2>ومنها: {M(P(2,12))} و {M(P(2,9))}</h2>
<div class="row">{box(f'<div class="col"><p class="ask">مرّتان إضافيتان…</p>{st(M(P(2,12),EQ,"١٠٢٤",X,"٢",X,"٢",cls="sm"))}{st(M(EQ,"٤٠٩٦",cls="mid res"))}</div>')}
{box(f'<div class="col"><p class="ask">مرّة أقل… فنقسم!</p>{st(M(P(2,9),EQ,"١٠٢٤","÷","٢",cls="sm"))}{st(M(EQ,"٥١٢",cls="mid res"))}</div>')}</div>'''))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ٢٠')}</div>''' + quiz(f'{M(P(10,6))} يساوي واحد مليون. كم يساوي؟', [M('١٠٠٠٠٠'), M('١٠٠٠٠٠٠'), M('٦٠'), M('١٠٠٠٠٠٠٠')], 1, 'ستة أصفار: ١٠٠٠٠٠٠ — وبالقاعدة نفسها ١٠ أس ٩ = مليار (تسعة أصفار)')))

# العدد المفقود (تمرين ٣)
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('تمرين ٣ (أ)')}</div><h2>أوجد العدد المفقود: {M(P(3,2),PL,P(4,2),EQ,mk())}</h2>
<div class="row">{st(box(M(P(3,2),EQ,'٩',cls="sm")))}{st(box(M(P(4,2),EQ,'١٦',cls="sm")))}</div>
{st(box(M('٩',PL,'١٦',EQ,'٢٥',cls="mid")))}
{st(box(M('٢٥',EQ,P(5,2),cls="mid"),style="border-color:var(--base)"))}'''))
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('تمرين ٣ (ب)')}</div><h2>معاً: {M(P(8,2),PL,P(6,2),EQ,mk())}</h2>
{st(box(M('٦٤',PL,'٣٦',EQ,'١٠٠',cls="mid")))}{st(box(M('١٠٠',EQ,P(10,2),cls="mid"),style="border-color:var(--base)"))}'''))
S.append(slide(f'''<div class="row hdr"><div class="row hdr">{mode('u')}{ref('تمرين ٣ (ج)')}</div>{timer(3)}</div>''' + quiz(f'{M(P(12,2),PL,P(5,2),EQ,mk())}', [M('١٧'), M('١٣'), M('١٦٩'), M('١٤')], 1, '١٤٤ + ٢٥ = ١٦٩ = ١٣ × ١٣')))

# الجذور — كتاب الطالب ص٣٢: √٢٥ = ±٥ ، ∛١٢٥ = ٥ (جذر تكعيبي صحيح واحد)
S.append(slide(f'''<h2>الجذر التربيعي: العملية العكسية للتربيع</h2>
<div class="row">{st(box(f'<div class="col"><small class="hint">مربّع العدد ٥</small>{M(P(5,2),EQ,"٢٥",cls="sm")}<small class="hint">ومربّع العدد (−٥)</small>{M(PN(5,2),EQ,"٢٥",cls="sm")}</div>'))}
{st(box(f'<div class="col">{M(R(25),EQ,PM(5),cls="mid")}<small class="hint">إذن للعدد ٢٥ جذران تربيعيان: ٥ و −٥</small></div>',style="border-color:var(--base)"))}</div>
{st(f'<div class="note">أمثلة: {M(R(169),EQ,PM(13))} &nbsp;و&nbsp; {M(R(361),EQ,PM(19))} — للأعداد المربّعة جذورٌ تربيعية عبارة عن أعداد صحيحة</div>')}'''))
S.append(slide(f'''<h2>الجذر التكعيبي: العملية العكسية للتكعيب</h2>
<div class="row">{st(box(f'<div class="col">{M(P(5,3),EQ,"١٢٥",cls="sm")}<span class="arrow">↩</span>{M(R(125,3),EQ,"٥",cls="mid")}</div>',style="border-color:var(--base)"))}
{st(box(f'<div class="col"><b class="kk">لماذا جذرٌ واحد فقط؟</b>{M(PN(5,3),EQ,N(125),cls="sm")}<small class="hint">(−٥) ليس جذراً تكعيبياً للعدد ١٢٥</small></div>'))}</div>
{st('<div class="note">العدد ١٢٥ له <b>جذرٌ تكعيبيٌّ صحيحٌ واحد فقط</b> هو ٥</div>')}'''))
S.append(slide(f'''<div class="row hdr"><span class="qbadge" style="background:#6A2FC4;box-shadow:0 4px 0 #3F1A7A">معلومة إثرائية 💡</span><span class="tag">للاطّلاع فقط</span></div><h2>هل يمكن أن يكون تحت الجذر عددٌ سالب؟</h2>
<div class="row">{st(box(f'<div class="col"><div class="rule l">الجذر التربيعي</div><b class="kk">لا</b><small class="hint">ضرب عددين متشابهين في الإشارة يعطي موجباً دائماً</small></div>'))}
{st(box(f'<div class="col"><div class="rule g">الجذر التكعيبي</div>{M(R("−125",3),EQ,N(5),cls="mid")}<small class="hint">لأن {M(PN(5,3),EQ,N(125))}</small></div>'))}</div>
'''))
S.append(slide(f'''{mode('i')}<h2>أوجد: {M(R(9))} و {M(R(27,3))}</h2>
<div class="row">{box(f'<div class="col">{M(R(9),cls="mid")}{st('<p class="ask" style="color:#2563EB">ما العدد الذي مربّعه ٩؟</p>')}{st(M(P(3,2),EQ,"٩","و",PN(3,2),EQ,"٩",cls="sm"))}{st(M(EQ,PM(3),cls="mid res"))}</div>')}
{box(f'<div class="col">{M(R(27,3),cls="mid")}{st('<p class="ask" style="color:#2563EB">ما العدد الذي مكعّبه ٢٧؟</p>')}{st(M(rep(3,3),EQ,"٢٧",cls="sm"))}{st(M(EQ,"٣",cls="mid res"))}</div>')}</div>'''))
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('تمرينا ١٠ و ١٣')}</div><h2>معاً: {M(R(196))} و {M(R(1000,3))}</h2>
<div class="row">{box(f'<div class="col"><p class="ask">ابحثوا في جدول المربعات…</p>{st(M(P(14,2),EQ,"١٩٦",cls="sm"))}{st(M(EQ,PM(14),cls="mid res"))}</div>')}
{box(f'<div class="col"><p class="ask">ما العدد الذي مكعّبه ١٠٠٠؟</p>{st(M(rep(10,3),EQ,"١٠٠٠",cls="sm"))}{st(M(EQ,"١٠",cls="mid res"))}</div>')}</div>'''))
S.append(slide(f'''<div class="row hdr"><div class="row hdr">{mode('u')}{ref('تمرين ١٠')}</div>{timer(2)}</div>''' + quiz(f'ما قيمة {M(R(81))} ؟', [M(PM(9)), M('٩'), M('٤٠٫٥'), M('٨١')], 0, 'لأن ٩ × ٩ = ٨١ و (−٩) × (−٩) = ٨١ — لا تنسَ الجذر السالب!')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ١٣ (د)')}</div>''' + quiz(f'ما قيمة {M(R("100 − 36"))} ؟', [M(R(100),'−',R(36)), M(PM(8)), M('٦٤'), M(PM(4))], 1, 'نُكمل العملية داخل الجذر أولاً: ١٠٠ − ٣٦ = ٦٤ ، ثم الجذر = ±٨')))
S.append(slide(f'''{ref('تمرين ٦')}<h2>ماذا يحدث إذا ربّعنا الجذر التربيعي؟</h2>
<div class="row">{st(box(M(f'({R(36)})<sup class="e2">٢</sup>',EQ,'٣٦',cls="mid")))}{st(box(M(f'({R(196)})<sup class="e2">٢</sup>',EQ,'١٩٦',cls="mid")))}</div>
{st('<div class="note">تربيع الجذر التربيعي لأيّ عددٍ مربّع يساوي العدد المربّع نفسه — <b>التربيع يلغي الجذر التربيعي</b></div>')}'''))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">فكّر 💡</span>{ref('تمرين ٥')}</div><h2>هل {M(R("9 + 16"))} = {M(R(9),PL,R(16))} ؟</h2>
<div class="row">{st(box(f'<div class="col">{M(R("9 + 16"),EQ,R(25),EQ,"٥",cls="mid")}</div>'))}{st(box(f'<div class="col">{M(R(9),PL,R(16),EQ,"٣",PL,"٤",EQ,"٧",cls="mid")}</div>'))}</div>
{st('<div class="note"><b>لا!</b> ٥ ≠ ٧ — نُكمل العملية داخل الجذر أولاً، ولا نوزّع الجذر على الجمع</div>')}'''))

# ألغاز وتفكير
S.append(slide(f'''<div class="row hdr"><span class="qbadge">فكّر 💡</span>{ref('تمرين ٧')}</div><h2>بأيّ رقمٍ ينتهي العدد المربّع؟</h2>
<div class="sqs">{''.join(f'<button class="sq open"><span class="n">{M(P(n,2))}</span><span class="v">{a(n*n)[:-1]}<u>{a(n*n)[-1]}</u></span></button>' for n in range(1,11))}</div>
{st('<div class="note">آحاد العدد المربّع: ٠ أو ١ أو ٤ أو ٥ أو ٦ أو ٩ — <b>لا يوجد</b> عددٌ مربّع آحاده ٢ أو ٣ أو ٧ أو ٨</div>')}'''))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">فكّر 💡</span>{ref('تمرين ٤')}</div><h2>هل صحيحٌ أن للعدد المربّع عدداً <b class="c-exp">فردياً</b> من العوامل دائماً؟</h2>
<div class="row">{st(box(f'<div class="col"><b class="kk">١٢ (ليس مربّعاً)</b><div class="pairs"><span>١ × ١٢</span><span>٢ × ٦</span><span>٣ × ٤</span></div><b class="even">٦ عوامل ← زوجي</b></div>'))}
{st(box(f'<div class="col"><b class="kk">١٦ (مربّع)</b><div class="pairs"><span>١ × ١٦</span><span>٢ × ٨</span><span class="self">٤ × ٤</span></div><b class="odd">٥ عوامل ← فردي</b></div>',style="border-color:var(--exp)"))}</div>
{st('<div class="note">في المربّع عاملٌ مضروبٌ في نفسه (٤ × ٤) يُعدّ مرّة واحدة</div>')}'''))
def puzzle(who, ic, q, ans):
    return f'<button class="flip box col puz"><span class="who2">{ic} {who}</span><span class="pq">{q}</span><span class="tap">👆 اضغط للحل</span><span class="hid col">{ans}</span></button>'
for who, ic, t, q, ans in [('مريم','🧕','تمرين ١١','عددٌ بين ٢٥٠ و ٣٥٠، وجذره التربيعي عددٌ صحيح', M('٢٥٦ ، ٢٨٩ ، ٣٢٤',cls="mid")),
                           ('حسن','👦','تمرين ١٢','عددٌ فرديّ موجب أصغر من ٥٠٠، وجذره التكعيبي عددٌ صحيح. ما أكبر عدد؟', M('٣٤٣',EQ,P(7,3),cls="mid")),
                           ('سناء','🧕','تمرين ١٤','عددٌ أصغر من ٣٠٠ له جذرٌ تربيعي وجذرٌ تكعيبي صحيحان', M('١ ، ٦٤',cls="mid"))]:
    S.append(slide(f'''<div class="row hdr"><span class="qbadge">ألغاز الكتاب 🧩</span>{ref(t)}</div><h2>{ic} {who} {'يفكّر' if who=='حسن' else 'تفكّر'} في عدد…</h2>
<button class="flip box col puz"><span class="pq">{q}</span><span class="tap">👆 اضغط للحل</span><span class="hid col">{ans}</span></button>'''))

# بطاقة الخروج ٢ + الواجب + الخلاصة
S.append(slide(f'''<span class="qbadge">بطاقة الخروج 🎫</span><h2>أجب في دفترك</h2>
<div class="exit">{st(f'<div><b>١</b>أيّهما أكبر: {M(P(2,5))} أم {M(P(5,2))}؟</div>')}{st(f'<div><b>٢</b>أوجد العدد المفقود: {M(P(6,2),PL,P(8,2),EQ,mk())}</div>')}{st(f'<div><b>٣</b>أوجد {M(R(49))} و {M(R(8,3))}</div>')}</div>
<button class="flip box col" style="min-width:40vw"><span class="tap">👆 اضغط لإظهار الإجابات</span><span class="hid col">{M("٣٢ أكبر من ٢٥ ← ",P(2,5),cls="sm")}{M("٣٦",PL,"٦٤",EQ,"١٠٠",EQ,P(10,2),cls="sm")}{M(PM(7)," ؛ ","٢",cls="sm")}</span></button>'''))
S.append(slide(f'''<span class="qbadge" style="background:#0A6770;box-shadow:0 4px 0 #05393E">الواجب المنزلي 🏠</span><h2>قبل الحصة القادمة</h2>
<div class="exit">{st('<div><b>١</b>احفظ الأعداد المربّعة حتى ٢٠ × ٢٠ = ٤٠٠ وجذورها التربيعية</div>')}{st('<div><b>٢</b>احفظ مكعبات الأعداد ١ إلى ٥ وجذورها التكعيبية</div>')}{st('<div><b>٣</b>حلّ صفحتي ٢٣–٢٤ في كتاب النشاط</div>')}</div>'''))
S.append(slide(f'''<h2>الخلاصة</h2><div style="display:grid;grid-template-columns:1fr 1fr;gap:2vh 2vw;width:min(1500px,92vw)">
{st(box(f'<div class="col">{M(P(5,2),cls="mid")}<b class="kk">تربيع — مربّع العدد</b></div>',style="flex:1;min-width:210px"))}
{st(box(f'<div class="col">{M(P(5,3),cls="mid")}<b class="kk">تكعيب — مكعّب العدد</b></div>',style="flex:1;min-width:210px"))}
{st(box(f'<div class="col">{M(R(25),EQ,PM(5),cls="mid")}<b class="kk">للعدد المربّع جذران تربيعيان</b></div>',style="flex:1;min-width:210px"))}
{st(box(f'<div class="col">{M(R(125,3),EQ,"٥",cls="mid")}<b class="kk">جذرٌ تكعيبيٌّ واحد</b></div>',style="flex:1;min-width:210px"))}</div>'''))


# ═══════════ ملحق: تمارين كتاب الطالب ص٣٢–٣٤ (القاعدة + أجزاء تُكشف بضغطة) ═══════════
S.append(slide('''<span class="tag">ملحق · للمراجعة وتصحيح الواجب</span><h2>تمارين كتاب الطالب ص ٣٢–٣٤</h2>
<p class="lead">اضغط على الجزء ليظهر حلّه</p>
<p class="hint">المراجع: كتاب الطالب ص٣٢–٣٤ ودليل المعلم — إعداد: أ. عيسى الحارثي</p>''', 'divider'))
S.append(ex(1,'اكتب أوّل ٢٠ عدداً مربّعاً','مربّع العدد = العدد × نفسه',[(M(P(n,2)),M(a(n*n))) for n in (1,2,3,10,15,20)],note='باقي الأعداد في جدول الحفظ'))
S.append(ex(2,'اكتب كلّ الأعداد المربّعة في كلّ مدى','ابدأ بأوّل عددٍ مربّعه لا يقلّ عن بداية المدى، واصعد حتى تتجاوز نهايته',
  [('(أ) من ١٠٠ إلى ٢٠٠',M('١٠٠ ، ١٢١ ، ١٤٤ ، ١٦٩ ، ١٩٦')),('(ب) من ٢٠٠ إلى ٣٠٠',M('٢٢٥ ، ٢٥٦ ، ٢٨٩')),('(ج) من ٣٠٠ إلى ٤٠٠',M('٣٢٤ ، ٣٦١ ، ٤٠٠'))]))
S.append(ex(3,'أوجد العدد المفقود','احسب المجموع أولاً، ثم ابحث عن العدد الذي مربّعه يساوي المجموع',
  [(M(P(3,2),PL,P(4,2),EQ,mk()),M('٢٥',EQ,P(5,2))),(M(P(8,2),PL,P(6,2),EQ,mk()),M('١٠٠',EQ,P(10,2))),
   (M(P(12,2),PL,P(5,2),EQ,mk()),M('١٦٩',EQ,P(13,2))),(M(P(8,2),PL,P(15,2),EQ,mk()),M('٦٤',PL,'٢٢٥',EQ,'٢٨٩',EQ,P(17,2)))],cols=2))
S.append(ex(4,'اذكر عوامل كلّ عددٍ مربّع، وعدّها','العوامل تأتي أزواجاً، إلا عاملاً مضروباً في نفسه — فعدد عوامل المربّع <b>فردي</b> دائماً',
  [('١٦','١، ٢، ٤، ٨، ١٦ ← <b>٥</b>'),('٢٥','١، ٥، ٢٥ ← <b>٣</b>'),('٣٦','١، ٢، ٣، ٤، ٦، ٩، ١٢، ١٨، ٣٦ ← <b>٩</b>'),
   ('٤٩','١، ٧، ٤٩ ← <b>٣</b>'),('٨١','١، ٣، ٩، ٢٧، ٨١ ← <b>٥</b>'),('١٠٠','١، ٢، ٤، ٥، ١٠، ٢٠، ٢٥، ٥٠، ١٠٠ ← <b>٩</b>')]))
S.append(ex(5,'أوجد قيمة الجذر التربيعي','للعدد المربّع جذران (±) — وإن كان داخل الجذر عملية <b>نُكملها أولاً</b>',
  [(M(R(81)),M(PM(9))),(M(R(36)),M(PM(6))),(M(R(1)),M(PM(1))),(M(R("29 + 35")),M(R(64),EQ,PM(8))),
   (M(R("144 + 256")),M(R(400),EQ,PM(20)))],note='(هـ): '+M(P(12,2),PL,P(16,2),EQ,'١٤٤',PL,'٢٥٦',EQ,'٤٠٠')))
S.append(ex(6,'تربيع الجذر، وجذر المربّع','تربيع الجذر التربيعي لعددٍ مربّع = العدد نفسه، أما الجذر التربيعي لمربّع عدد فهو عددان: موجب وسالب',
  [(M(f'({R(36)})<sup class="e2">٢</sup>'),M('٣٦')),(M(f'({R(196)})<sup class="e2">٢</sup>'),M('١٩٦')),
   (M(R('5<sup class="e2">2</sup>')),M(R(25),EQ,PM(5))),(M(R('16<sup class="e2">2</sup>')),M(R(256),EQ,PM(16)))],cols=2))
S.append(ex(7,'آحاد أوّل عشرة أعداد مربّعة: دائماً، أحياناً، أبداً؟','آحاد المربّع أحد الأرقام: ٠، ١، ٤، ٥، ٦، ٩ فقط',
  [('(أ) آحاد العدد هو ٥','<b>أحياناً</b> (٢٥)'),('(ب) آحاد العدد هو ٧','<b>أبداً</b>'),('(ج) آحاد العدد عددٌ مربّع','<b>أحياناً</b>'),('(د) آحاد العدد ليس ٣ أو ٨','<b>دائماً</b>')],cols=2))
S.append(ex(8,'أوجد قيمة كلٍّ مما يلي','كل قوّة = القوّة السابقة × الأساس',
  [(M(P(3,2)),M('٩')),(M(P(3,3)),M('٢٧')),(M(P(3,4)),M('٨١')),(M(P(3,5)),M('٢٤٣'))],cols=4))
S.append(ex(9,'أيّ العددين أكبر؟','لا نحكم بالنظر — نحسب قيمة كل قوّة ثم نقارن',
  [(M(P(3,5),'أم',P(5,3)),M('٢٤٣ > ١٢٥ ←',P(3,5))),(M(P(12,2),'أم',P(2,6)),M('١٤٤ > ٦٤ ←',P(12,2))),(M(P(5,4),'أم',P(4,5)),M('٦٢٥ < ١٠٢٤ ←',P(4,5)))],
  note='(ب) كما قرأتُها في الصفحة: '+M(P(12,2))+' أم '+M(P(2,6))+' — تأكّد منها في الكتاب'))
S.append(ex(10,'أوجد قيمة الجذر التربيعي','استخدم جدول المربعات عكسياً، ولا تنسَ الجذر السالب',
  [(M(R(n)),M(PM(int(n**.5)))) for n in (9,36,81,196,225,400)]))
S.append(ex(13,'أوجد قيمة كلٍّ مما يلي','الجذر التكعيبي: العدد الذي مكعّبه يساوي ما تحت الجذر (قيمة واحدة)',
  [(M(R(27,3)),M('٣')),(M(R(125,3)),M('٥')),(M(R(1000,3)),M('١٠')),(M(R("100 − 36")),M(R(64),EQ,PM(8)))],cols=2))
S.append(ex(15,'استخدم الحقيقة '+M(P(2,10),EQ,'١٠٢٤'),'مرّة إضافية ← نضرب في ٢ ، مرّة أقل ← نقسم على ٢',
  [(M(P(2,11)),M('١٠٢٤',X,'٢',EQ,'٢٠٤٨')),(M(P(2,12)),M('١٠٢٤',X,'٤',EQ,'٤٠٩٦')),(M(P(2,9)),M('١٠٢٤','÷','٢',EQ,'٥١٢'))]))
S.append(ex(16,'جذور مجموع المكعبات','جذر مجموع مكعبات الأعداد من ١ إلى ن = ١ + ٢ + … + ن',
  [(M(P(1,3),PL,P(2,3)),M('٩')),(M(R("1 + 8")),M(PM(3))),(M(R("1 + 8 + 27")),M(R(36),EQ,PM(6))),(M(R("1 + 8 + 27 + 64")),M(R(100),EQ,PM(10))),
   ('(د) مكعبات ١ إلى ٥',M(R(225),EQ,PM(15)))],note='الطريقة السهلة: ١ + ٢ + ٣ + ٤ + ٥ = ١٥'))
S.append(ex(17,'أوجد العدد المربّع العشرين والثلاثين والخمسين','مربّع العشرات: نربّع الرقم ثم نضيف صفرين',
  [(M(P(20,2)),M('٤٠٠')),(M(P(30,2)),M('٩٠٠')),(M(P(50,2)),M('٢٥٠٠'))]))
S.append(ex(18,'أوجد ثلاثة أعدادٍ مربّعة مجموعها ١٢٥','جرّب من الأكبر: خذ مربّعاً كبيراً ثم أكمل الباقي بمربّعين',
  [('الحل الأوّل',M('١٠٠',PL,'١٦',PL,'٩')),('الحل الثاني',M('٦٤',PL,'٣٦',PL,'٢٥'))],cols=2,note=M(P(10,2),PL,P(4,2),PL,P(3,2),EQ,'١٢٥')+' &nbsp;و&nbsp; '+M(P(8,2),PL,P(6,2),PL,P(5,2),EQ,'١٢٥')))
S.append(ex(19,'أوجد قيمة كلٍّ مما يلي','قوى العدد ١٠: عدد الأصفار = الأس',
  [(M(P(10,2)),M('١٠٠')),(M(P(10,3)),M('١٠٠٠')),(M(P(10,4)),M('١٠٠٠٠'))]))
S.append(ex(20,'المليون والمليار','القاعدة نفسها: عدد الأصفار = الأس',
  [(M(P(10,6)),M('١٠٠٠٠٠٠')+'<small>مليون</small>'),(M(P(10,9)),M('١٠٠٠٠٠٠٠٠٠')+'<small>مليار</small>')],cols=2))
S.append(ex('١١ و ١٢ و ١٤','ألغاز الكتاب','اكتب قائمة المربعات أو المكعبات في المدى المطلوب، ثم طبّق الشرط',
  [('١١ مريم: بين ٢٥٠ و ٣٥٠، وجذره التربيعي صحيح',M('٢٥٦ ، ٢٨٩ ، ٣٢٤')),('١٢ حسن: فرديّ أصغر من ٥٠٠، جذره التكعيبي صحيح — أكبر عدد؟',M('٣٤٣')),
   ('١٤ سناء: أصغر من ٣٠٠، مربّع ومكعّب معاً',M('١ ، ٦٤'))],cols=2,src='تمارين',per=2))

# ═══════════ ملحق: حلول كتاب النشاط ص٢٣–٢٤ (الإجابات من دليل المعلم ص٤٣–٤٤ — الخطوات من إعداد العرض) ═══════════
MI = '<span class="x">−</span>'
def FR(n, d): return f'<span style="display:inline-flex;flex-direction:column;align-items:center;line-height:1.05;vertical-align:middle"><span style="border-bottom:.07em solid currentColor;padding:0 .15em .05em;align-self:stretch;text-align:center">{n}</span><span>{d}</span></span>'
S.append(slide('''<span class="tag">ملحق · تصحيح الواجب</span><h2>حلول كتاب النشاط ص ٢٣–٢٤</h2>
<p class="lead">اضغط على الجزء ليظهر حلّه خطوةً خطوة</p>
<p class="hint">الإجابات النهائية من دليل المعلم ص ٤٣–٤٤</p>''', 'divider'))
NS = 'نشاط ص ٢٣ · تمرين'
S.append(ex(1, 'أوجد قيمة كلٍّ مما يلي', 'التربيع: العدد × نفسه', [('(أ) ' + M(P(5,2)), M('٥',X,'٥',EQ,'٢٥')), ('(ب) ' + M(P(9,2)), M('٩',X,'٩',EQ,'٨١')),
  ('(ج) ' + M(P(11,2)), M('١١',X,'١١',EQ,'١٢١')), ('(د) ' + M(P(18,2)), M('١٨',X,'١٨',EQ,'٣٢٤'))], cols=2, src=NS))
S.append(ex(2, 'أوجد قيمة كلٍّ مما يلي', 'التكعيب: العدد × نفسه × نفسه', [('(أ) ' + M(P(2,3)), M(rep(2,3),EQ,'٨')), ('(ب) ' + M(P(3,3)), M(rep(3,3),EQ,'٢٧')),
  ('(ج) ' + M(P(4,3)), M(rep(4,3),EQ,'٦٤')), ('(د) ' + M(P(5,3)), M(rep(5,3),EQ,'١٢٥')), ('(هـ) ' + M(P(10,3)), M(rep(10,3),EQ,'١٠٠٠'))], cols=2, src=NS))
S.append(ex(3, 'أوجد قيمة كلٍّ مما يلي', 'الأس ٤: نضرب العدد في نفسه أربع مرات', [('(أ) ' + M(P(2,4)), M(rep(2,4),EQ,'١٦')), ('(ب) ' + M(P(3,4)), M(rep(3,4),EQ,'٨١')),
  ('(ج) ' + M(P(4,4)), M('١٦',X,'١٦',EQ,'٢٥٦')), ('(د) ' + M(P(10,4)), M('١٠٠',X,'١٠٠',EQ,'١٠٠٠٠'))], cols=2, src=NS))
S.append(ex(4, 'انظر إلى النمط: ' + M(P(4,2),MI,P(2,2),EQ,'٦',X,'٢'), 'الفرق بين مربّعي عددين الفرق بينهما ٢ = مجموعهما × ٢', [
  ('(أ) تحقّق: ' + M(P(4,2),MI,P(2,2)), M('١٦',MI,'٤',EQ,'١٢') + M(EQ,'٦',X,'٢')),
  ('(أ) تحقّق: ' + M(P(5,2),MI,P(3,2)), M('٢٥',MI,'٩',EQ,'١٦') + M(EQ,'٨',X,'٢')),
  ('(ب) أكمل النمط', M(P(7,2),MI,P(5,2),EQ,'٢٤') + M(EQ,'١٢',X,'٢')),
  ('(ب) ثم', M(P(8,2),MI,P(6,2),EQ,'٢٨') + M(EQ,'١٤',X,'٢')),
  ('(ج) ' + M(P(51,2),MI,P(49,2)), M('١٠٠',X,'٢',EQ,'٢٠٠') + '<small>٥١ + ٤٩ = ١٠٠</small>')], cols=2, src=NS))
S.append(ex(5, 'للعدد ١٠٠ جذران تربيعيان', M(R(100),EQ,PM(10)) + ' — أي ١٠ و −١٠', [('(أ) ما ناتج جمعهما؟', M('١٠',PL,N(10),EQ,'٠')),
  ('(ب) ما ناتج ضربهما؟', M('١٠',X,N(10),EQ,N(100)))], cols=2, src=NS))
S.append(ex(6, 'أوجد الجذور التربيعية', 'للعدد المربّع جذران تربيعيان: موجب وسالب', [('(أ) ١', M(R(1),EQ,PM(1))), ('(ب) ٣٦', M(R(36),EQ,PM(6))),
  ('(ج) ١٦٩', M(R(169),EQ,PM(13))), ('(د) ٢٥٦', M(R(256),EQ,PM(16))), ('(هـ) ٣٦١', M(R(361),EQ,PM(19)))], cols=2, src=NS))
S.append(ex(7, 'هل ' + M(R('9 + 16')) + ' يساوي ' + M(R(9),PL,R(16)) + '؟', 'نُكمل العملية داخل الجذر أولاً — ولا نوزّع الجذر على الجمع', [
  (M(R('9 + 16')), M(R(25),EQ,'٥')), (M(R(9),PL,R(16)), M('٣',PL,'٤',EQ,'٧') + '<small>لا: القيمة الأولى ٥ والثانية ٧</small>')], cols=2, src='نشاط ص ٢٤ · تمرين'))
S.append(ex(8, 'وضّح كيف…', 'احسب الطرفين كلٌّ على حدة، ثم قارن', [
  ('(أ) ' + M(FR(M(P(3,3),MI,'١'),'٢'),EQ,P(3,2),PL,'٣',PL,'١'), M(FR('٢٦','٢'),EQ,'١٣') + M('٩',PL,'٣',PL,'١',EQ,'١٣')),
  ('(ب) ' + M(FR(M(P(4,3),MI,'١'),'٣'),EQ,P(4,2),PL,'٤',PL,'١'), M(FR('٦٣','٣'),EQ,'٢١') + M('١٦',PL,'٤',PL,'١',EQ,'٢١')),
  ('(ج) عبارة مماثلة تتضمّن ' + M(P(5,3)), M(FR(M(P(5,3),MI,'١'),'٤'),EQ,P(5,2),PL,'٥',PL,'١') + '<small>كلاهما = ٣١</small>')], cols=2, src='نشاط ص ٢٤ · تمرين', per=2))
S.append(ex(9, 'أعداد الإطار كلّها = ٤٠٩٦', M(P(2,12),EQ,P(4,6),EQ,P(16,3),EQ,P(64,2)) + ' — اختر القوّة المناسبة: التربيع للجذر التربيعي، والتكعيب للجذر التكعيبي', [
  ('(أ) ' + M(R(4096)), M(P(64,2),EQ,'٤٠٩٦') + M(R(4096),EQ,'٦٤') + '<small>كما في الدليل — وللعدد جذرٌ تربيعي آخر هو −٦٤</small>'),
  ('(ب) ' + M(R(4096,3)), M(P(16,3),EQ,'٤٠٩٦') + M(R(4096,3),EQ,'١٦'))], cols=2, src='نشاط ص ٢٤ · تمرين'))
S.append(ex(10, 'أوجد قيمة', 'الجذر التكعيبي: العدد الذي مكعّبه يساوي ما تحت الجذر', [('(أ) ' + M(R(8,3)), M(rep(2,3),EQ,'٨') + M(EQ,'٢')),
  ('(ب) ' + M(R(125,3)), M(rep(5,3),EQ,'١٢٥') + M(EQ,'٥')), ('(ج) ' + M(R(27,3)), M(rep(3,3),EQ,'٢٧') + M(EQ,'٣')),
  ('(د) ' + M(R(1000,3)), M(rep(10,3),EQ,'١٠٠٠') + M(EQ,'١٠'))], cols=2, src='نشاط ص ٢٤ · تمرين'))
S.append(ex(11, 'نور: «قد يكون الجذر التربيعي للعدد ٢٥ أقلّ من الجذر التربيعي للعدد ١٦»', 'لكل عددٍ مربّع جذران: موجب وسالب', [
  ('هل ما تقوله نور صحيح؟', '<b>نعم</b>' + M(R(25),EQ,PM(5)) + M(R(16),EQ,PM(4)) + '<small>−٥ أصغر من ٤ و −٤</small>')], cols=1, src='نشاط ص ٢٤ · تمرين'))

EXTRA_CSS_LESSON_X = '''
.xhead{display:flex;align-items:center;gap:1.4vw;justify-content:center;flex-wrap:wrap}
.xnum{font-family:var(--fh);font-weight:700;font-size:clamp(20px,3.2vh,34px);background:var(--ink);color:#fff;border-radius:99px;padding:.25em 1em}
.xhead h2{font-size:clamp(28px,5.2vh,58px)}
.xrule{display:flex;align-items:center;gap:1em;background:#FFF6E3;border:3px solid #E9A23B;border-radius:18px;padding:1.1vh 1.6vw;width:min(1150px,92vw);font-weight:700;font-size:clamp(19px,3.1vh,33px);line-height:1.55}
.xrule b{flex:none;background:#E9A23B;color:#fff;border-radius:12px;padding:.15em .7em;font-family:var(--fh)}
.xgrid{display:grid;gap:1.6vh 1.4vw;width:min(1150px,92vw)}
.xgrid.c2{grid-template-columns:repeat(2,minmax(0,1fr))}.xgrid.c3{grid-template-columns:repeat(3,minmax(0,1fr))}.xgrid.c4{grid-template-columns:repeat(4,minmax(0,1fr))}
.xgrid.c4 .xq{font-size:clamp(18px,3vh,32px)}
.xcard{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:.8vh;background:#fff;border:3px solid var(--line);border-radius:18px;padding:1.4vh 1vw;cursor:pointer;font-family:var(--fb);color:var(--ink);box-shadow:0 6px 0 #D4DFEC;min-height:13vh}
.xq{font-weight:700;font-size:clamp(20px,3.4vh,38px);line-height:1.5;text-align:center}
.xq .m{font-size:1.15em}
.xa{font-weight:700;font-size:clamp(19px,3.2vh,35px);color:var(--good);text-align:center;line-height:1.5;flex-direction:column;align-items:center}
.xa .m{color:var(--good)}.xa small{font-size:.6em;color:var(--ink2)}
.xcard.open{border-color:var(--good);background:#F2FBF5}
.xcard .tap{font-size:clamp(16px,2.3vh,24px)}
'''

EXTRA_CSS_LESSON = '''
.sq.pw2 .n{font-size:clamp(20px,3.6vh,38px)}
.sq.pw2 .n .m{gap:.18em}
.sqs.c5{grid-template-columns:repeat(5,minmax(0,1fr));width:min(1100px,90vw)}
.sqs.c5 .n{font-size:clamp(30px,5.2vh,56px)}.sqs.c5 .v{font-size:clamp(30px,5.2vh,56px)}
.h1s{font-size:clamp(48px,10vh,112px)!important}
.can{background:#fff;border:3px solid var(--line);border-radius:22px;padding:1.6vh 2vw;display:flex;flex-direction:column;gap:1.2vh;width:min(1150px,92vw);box-shadow:0 8px 0 #E3EAF4}
.can-t{font-family:var(--fh);font-size:clamp(20px,3.2vh,34px);color:var(--ink2)}
.can>div{display:flex;align-items:center;gap:.8em;font-weight:800;font-size:clamp(20px,3.4vh,37px);line-height:1.55}
.can-i{flex:none;width:1.5em;height:1.5em;border-radius:50%;background:var(--good);color:#fff;display:flex;align-items:center;justify-content:center;font-size:.8em}
.can b{color:var(--ink)}.can .c-b{color:var(--base)}.can .c-exp{color:var(--exp)}
.vocab.wide{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1.2vh 2.4vw;width:min(1100px,90vw);padding:2vh 2vw}
.vocab.wide div{font-size:clamp(22px,3.8vh,40px)}
.ref{font-family:var(--fh);font-weight:800;font-size:clamp(15px,2.2vh,22px);color:#0A6770;background:#E4F4F5;border:2px solid #9ED5D9;border-radius:99px;padding:.2em .9em}
.goals{display:flex;flex-direction:column;gap:1.4vh;flex:1.4;min-width:340px}
.goals .st>div{background:#fff;border:3px solid var(--line);border-radius:16px;padding:1.2vh 1.3vw;font-weight:800;font-size:clamp(19px,3.1vh,33px);line-height:1.6}
.vocab{background:#fff;border:3px solid var(--line);border-radius:18px;padding:1.4vh 1.4vw;display:flex;flex-direction:column;gap:.8vh;min-width:300px}
.vocab>b{font-family:var(--fh);font-size:clamp(20px,3.2vh,34px);text-align:center;color:var(--ink)}
.vocab div{display:flex;justify-content:space-between;gap:1.2vw;font-weight:800;font-size:clamp(17px,2.7vh,29px);border-bottom:2px dashed #DCE6F2;padding-bottom:.4vh}
.vocab i{font-style:normal;direction:ltr;color:#0A6770;font-family:Tahoma,sans-serif}
.chain{display:flex;flex-wrap:wrap;gap:1.4vh 1.2vw;justify-content:center;max-width:1180px}
.chain .box{padding:1.2vh 1.4vw}.chain .box.hot{border-color:var(--exp);background:#FFF1EC;box-shadow:0 0 0 5px rgba(198,58,34,.18)}
.wrong,.right{font-size:clamp(26px,4.4vh,46px);font-weight:900}.wrong{color:var(--bad)}.right{color:var(--good)}
.sq u{text-decoration:none;color:#fff;background:var(--exp);border-radius:8px;padding:0 .12em}
.puz{flex:1;min-width:280px;max-width:390px;gap:1.2vh}
.who2{font-family:var(--fh);font-weight:900;font-size:clamp(22px,3.6vh,38px)}
.pq{font-weight:800;font-size:clamp(18px,2.9vh,31px);line-height:1.6}
'''
