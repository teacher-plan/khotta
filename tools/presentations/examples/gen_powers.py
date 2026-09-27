# مولّد عرض «القوى والجذور» — يعيد استخدام محرّك عرض «الأسس» (base.css / base.js)
import re, os
HERE=os.path.dirname(os.path.abspath(__file__)); KIT=os.path.dirname(HERE)
AR = '٠١٢٣٤٥٦٧٨٩'
def a(n): return ''.join(AR[int(c)] if c.isdigit() else c for c in str(n))
def N(v): return f'<span class="ng"><i>−</i>{a(v)}</span>'  # السالب: الإشارة يمين العدد
def PN(v, e): return f'<span class="b"><span>({N(v)})</span><sup>{a(e)}</sup></span>'
def P(b, e=None):  # أساس بأسٍّ
    return f'<span class="b">{a(b)}' + (f'<sup>{a(e)}</sup>' if e is not None else '') + '</span>'
X = '<span class="x">×</span>'
EQ = '<span class="eq">=</span>'
PL = '<span class="x">+</span>'
def M(*parts, cls=''): return f'<span class="m {cls}">' + ' '.join(parts) + '</span>'
def R(v, k=2):  # جذرٌ من اليمين لليسار: الرمز يميناً، والخط العلوي يمتدّ يساراً فوق العدد
    v=str(v)
    inner = N(v[1:]) if v.startswith('−') else a(v)
    return f'<span class="rt">' + (f'<i class="ri">{a(k)}</i>' if k==3 else '') + f'<span class="rs">√</span><span class="ov">{inner}</span></span>'
def rep(b, n): return X.join(P(b) for _ in range(n))

MODES = {'i': ('أنا', 'المعلّم يحلّ ويشرح', '👨‍🏫', 'i'), 'we': ('نحن', 'نحلّ معاً', '🤝', 'we'), 'u': ('أنتم', 'دوركم الآن', '✍️', 'u')}
def mode(k): t, s, ic, c = MODES[k]; return f'<div class="mode {c}"><span class="ic">{ic}</span><b>{t}</b><small>{s}</small></div>'
def timer(mins): return f'<button class="timer" data-s="{mins*60}"><span class="tt">{a(mins)}:٠٠</span><span class="tl">▶ ابدأ المؤقّت</span></button>'
def quiz(q, choices, ok, why, badge=None):
    ch = ''.join(f'<button class="ch">{c}</button>' for c in choices)
    return (f'<span class="qbadge">{badge}</span>' if badge else '') + f'<h2>{q}</h2><div class="q" data-ok="{ok}">{ch}</div><div class="fb" data-why="{why.replace(chr(34), "&quot;").replace("<","&lt;").replace(">","&gt;")}"></div>'
def slide(inner, cls=''): return f'<section class="slide {cls}">{inner}</section>'
def st(inner, tag='div', cls=''): return f'<{tag} class="st {cls}">{inner}</{tag}>'
def box(inner, cls='', style=''): return f'<div class="box {cls}" style="{style}">{inner}</div>'

S = []
# ═══ الغلاف ═══
S.append(slide(f'''<span class="tag">الصف السابع · الدرس ١-٦</span>
<div class="ttl"><h1>القوى والجذور</h1></div>
<div class="row" style="gap:3vw">{M(P(5,2),cls="big")}{M(P(5,3),cls="big")}{M(P(5,4),cls="big")}</div>
<p class="lead">نتعلّم معاً ثم نتدرّب: <b class="c-i">أنا</b> ← <b class="c-we">نحن</b> ← <b class="c-u">أنتم</b></p>''', 'cover'))

# ═══ الحصة الأولى ═══
S.append(slide(f'''<span class="tag">الحصة الأولى · ٤٠ دقيقة</span><h2>قوّة العدد، والمربعات والمكعبات</h2>
<div class="plan">
<div><b>٥ د</b>تهيئة: مربّع من البلاط</div><div><b>١٠ د</b>مفهوم القوّة: التربيع والتكعيب</div>
<div><b>١٠ د</b>إيجاد قيمة القوّة: أنا ← نحن ← أنتم</div><div><b>١٠ د</b>المربعات والمكعبات في مدى</div><div><b>٥ د</b>بطاقة الخروج</div></div>''', 'divider'))

# تهيئة
S.append(slide(f'''<span class="qbadge">تهيئة 🤔</span><h2>كم بلاطةً نحتاج لنبني مربّعاً ضلعه ٥ بلاطات؟</h2>
<div class="row" style="align-items:center"><div class="grid g5 st" id="g5">{"<i></i>"*25}</div>
<div class="col">{st(M(P(5),X,P(5),EQ,'٢٥',cls="mid"))}{st(M(P(5,2),EQ,'٢٥',cls="mid"))}{st('<p class="lead">لذلك نسمّي ٢٥ <b class="c-b">مربّع العدد ٥</b></p>')}</div></div>'''))

# المفهوم
S.append(slide(f'''<h2>قوّة العدد</h2><p class="lead st">عملية ضرب العدد في نفسه عدّة مرات</p>
<div class="pw">
{st(f'<div class="pwr">{M(P(5,2),EQ,rep(5,2),EQ,"٢٥",cls="sm")}<span class="rd">يُقرأ: ٥ <b>تربيع</b> — ٢٥ مربّع العدد ٥</span></div>')}
{st(f'<div class="pwr">{M(P(5,3),EQ,rep(5,3),EQ,"١٢٥",cls="sm")}<span class="rd">يُقرأ: ٥ <b>تكعيب</b> — ١٢٥ مكعّب العدد ٥</span></div>')}
{st(f'<div class="pwr">{M(P(5,4),EQ,rep(5,4),EQ,"٦٢٥",cls="sm")}<span class="rd">يُقرأ: <b>القوّة الرابعة</b> للعدد ٥، أو ٥ أُس ٤</span></div>')}
</div>'''))

# المكعب بصرياً
S.append(slide(f'''<h2>لماذا نقول «تكعيب»؟</h2><p class="lead">المكعّب طبقاتٌ متطابقة: كل طبقة مربّع</p>
<div class="row layers">{''.join(st(f'<div class="col"><div class="grid g3">{"<i></i>"*9}</div><small>طبقة {a(k)}</small></div>') for k in (1,2,3))}</div>
{st(M(P(3,3),EQ,'٣ طبقات',X,'٩',EQ,'٢٧',cls="mid"))}'''))

# أنا
S.append(slide(f'''{mode('i')}<h2>أوجد قيمة: {M(P(9,2))} و {M(P(7,3))}</h2>
<div class="row">{box(f'<div class="col">{M(P(9,2),cls="mid")}{st(M(rep(9,2),cls="sm"))}{st(M(EQ,"٨١",cls="mid res"))}</div>')}
{box(f'<div class="col">{M(P(7,3),cls="mid")}{st(M(rep(7,3),cls="sm"))}{st(M(EQ,"٤٩",X,"٧",cls="sm"))}{st(M(EQ,"٣٤٣",cls="mid res"))}</div>')}</div>
{st('<div class="note">الأس يخبرنا <b>كم مرّة</b> نكتب الأساس ثم نضرب — لا نضرب الأساس في الأس!</div>')}'''))

# نحن
S.append(slide(f'''{mode('we')}<h2>معاً: {M(P(10,5))} و {M(P(3,4))}</h2>
<div class="row">{box(f'<div class="col"><p class="ask">كم مرّة نكتب العدد ١٠؟</p>{st(M(rep(10,5),cls="sm"))}{st(M(EQ,"١٠٠٠٠٠",cls="mid res"))}{st('<small class="hint">لاحظ: خمسة أصفار = الأس ٥</small>')}</div>')}
{box(f'<div class="col"><p class="ask">وهنا؟</p>{st(M(rep(3,4),cls="sm"))}{st(M(EQ,"٩",X,"٩",cls="sm"))}{st(M(EQ,"٨١",cls="mid res"))}</div>')}</div>'''))

# أنتم
S.append(slide(f'''{mode('u')}{timer(2)}''' + quiz(f'أوجد قيمة {M(P(6,2))}', [M('١٢'), M('٣٦'), M('٨'), M('٦٦')], 1, '٦ × ٦ = ٣٦')))
S.append(slide(f'''{mode('u')}''' + quiz(f'أوجد قيمة {M(P(2,5))}', [M('١٠'), M('٢٥'), M('٣٢'), M('١٦')], 2, '٢ × ٢ × ٢ × ٢ × ٢ = ٣٢')))
S.append(slide(f'''{mode('u')}''' + quiz(f'أوجد قيمة {M(P(4,3))}', [M('١٢'), M('٦٤'), M('١٦'), M('٤٣')], 1, '٤ × ٤ × ٤ = ١٦ × ٤ = ٦٤')))

# جدول المربعات
cards = ''.join(f'<button class="sq"><span class="n">{a(n)}</span><span class="v">{a(n*n)}</span></button>' for n in range(1, 21))
S.append(slide(f'''<h2>احفظ الأعداد المربّعة حتى مربّع ٢٠</h2><p class="lead">اضغط على العدد ليظهر مربّعه — أو اكشفها كلّها</p>
<div class="sqs">{cards}</div><button class="reveal-all">اكشف الكل</button>'''))
cards = ''.join(f'<button class="sq cu"><span class="n">{a(n)}</span><span class="v">{a(n**3)}</span></button>' for n in range(1, 11))
S.append(slide(f'''<h2>احفظ الأعداد المكعّبة حتى مكعّب ١٠</h2><p class="lead">اضغط على العدد ليظهر مكعّبه</p>
<div class="sqs c10">{cards}</div><button class="reveal-all">اكشف الكل</button>'''))

# المربعات في مدى
def chips(nums, hot): return '<div class="chips">' + ''.join(f'<span class="chip{" hot" if n in hot else ""}">{a(n)}</span>' for n in nums) + '</div>'
S.append(slide(f'''{mode('i')}<h2>اكتب كلّ الأعداد المربّعة من ١٠٠ إلى ٢٠٠</h2>
{st(f'<p class="lead">أبدأ من أوّل عددٍ مربّعه ١٠٠ وأصعد حتى أتجاوز ٢٠٠:</p>')}
<div class="row">{''.join(st(box(M(P(n,2),EQ,a(n*n),cls="sm"),style=('opacity:.5' if n*n>200 else ''))) for n in range(10,16))}</div>
{st(f'<div class="ans l" style="border-color:var(--base);background:#EAF7F8"><span class="m sm">١٠٠ ، ١٢١ ، ١٤٤ ، ١٦٩ ، ١٩٦</span></div>')}'''))
S.append(slide(f'''{mode('we')}<h2>الأعداد المربّعة من ٣٠٠ إلى ٤٠٠</h2><p class="ask">من أين نبدأ؟ ما أوّل عددٍ مربّعه أكبر من ٣٠٠؟</p>
<div class="row">{''.join(st(box(M(P(n,2),EQ,a(n*n),cls="sm"),style=('opacity:.45' if not 300<=n*n<=400 else ''))) for n in (17,18,19,20,21))}</div>
{st(f'<div class="ans l" style="border-color:var(--base);background:#EAF7F8"><span class="m sm">٣٢٤ ، ٣٦١ ، ٤٠٠</span></div>')}'''))
S.append(slide(f'''{mode('u')}{timer(2)}''' + quiz('ما الأعداد المكعّبة بين ١٠٠ و ٦٠٠؟', [M('١٢٥ ، ٢١٦ ، ٣٤٣ ، ٥١٢'), M('١٠٠ ، ٢٠٠ ، ٤٠٠'), M('١٢١ ، ١٤٤ ، ١٦٩'), M('١٢٥ ، ٢٥٠ ، ٥٠٠')], 0, '٥³ = ١٢٥ ، ٦³ = ٢١٦ ، ٧³ = ٣٤٣ ، ٨³ = ٥١٢')))

# بطاقة الخروج ١
S.append(slide(f'''<span class="qbadge">بطاقة الخروج 🎫</span><h2>أجب في دفترك قبل الخروج</h2>
<div class="exit">{st(f'<div><b>١</b>أوجد قيمة {M(P(8,2))}</div>')}{st(f'<div><b>٢</b>أوجد قيمة {M(P(3,3))}</div>')}{st(f'<div><b>٣</b>اكتب الأعداد المربّعة من ٥٠ إلى ١٠٠</div>')}</div>
<button class="flip box col" style="min-width:40vw"><span class="tap">👆 اضغط لإظهار الإجابات</span><span class="hid col">{M("٦٤",cls="sm")}{M("٢٧",cls="sm")}{M("٦٤ ، ٨١ ، ١٠٠",cls="sm")}</span></button>'''))

# ═══ الحصة الثانية ═══
S.append(slide(f'''<span class="tag">الحصة الثانية · ٤٠ دقيقة</span><h2>نقارن القوى، ونستفيد منها، ونكتشف الجذور</h2>
<div class="plan">
<div><b>٥ د</b>إحماء: تحدّي المربعات السريع</div><div><b>٧ د</b>أيّ القوّتين أكبر؟</div>
<div><b>٦ د</b>نستخدم حقيقةً لنجد غيرها</div><div><b>٦ د</b>العدد المفقود</div><div><b>١٢ د</b>الجذور التربيعية والتكعيبية</div><div><b>٤ د</b>بطاقة الخروج</div></div>''', 'divider'))
# إحماء
flash = ''.join(f'<button class="sq"><span class="n">{M(P(n,2))}</span><span class="v">{a(n*n)}</span></button>' for n in (7, 12, 15, 9, 13, 20, 11, 16))
S.append(slide(f'''<span class="qbadge">إحماء ⚡</span><h2>مَن يجيب أوّلاً؟</h2><div class="sqs c4">{flash}</div>'''))

# المقارنة
S.append(slide(f'''{mode('i')}<h2>أيّهما أكبر: {M(P(3,5))} أم {M(P(5,3))} ؟</h2>
<div class="row">{box(f'<div class="col">{M(P(3,5),cls="mid")}{st(M(rep(3,5),cls="sm"))}{st(M(EQ,"٢٤٣",cls="mid res"))}</div>')}
{box(f'<div class="col">{M(P(5,3),cls="mid")}{st(M(rep(5,3),cls="sm"))}{st(M(EQ,"١٢٥",cls="mid res"))}</div>')}</div>
{st(f'<div class="note">إذن {M(P(3,5))} أكبر — لا نحكم بالنظر إلى الأس أو الأساس وحده، بل <b>نحسب القيمة</b> ثم نقارن</div>')}'''))
S.append(slide(f'''{mode('we')}<h2>أيّهما أكبر: {M(P(5,4))} أم {M(P(4,5))} ؟</h2><p class="ask">توقّعوا أولاً… ثم نحسب معاً</p>
<div class="row">{box(f'<div class="col">{M(P(5,4),cls="mid")}{st(M(rep(5,4),cls="sm"))}{st(M(EQ,"٦٢٥",cls="mid res"))}</div>')}
{box(f'<div class="col">{M(P(4,5),cls="mid")}{st(M(rep(4,5),cls="sm"))}{st(M(EQ,"١٠٢٤",cls="mid res"))}</div>')}</div>
{st(f'<div class="note">{M(P(4,5))} أكبر</div>')}'''))
S.append(slide(f'''{mode('u')}{timer(2)}''' + quiz(f'أيّهما أكبر: {M(P(2,6))} أم {M(P(6,2))} ؟', [M(P(2,6)), M(P(6,2)), 'متساويان'], 0, '٢⁶ = ٦٤ و ٦² = ٣٦ ، إذن ٢⁶ أكبر'.replace('٢⁶','٢ أُس ٦').replace('٦²','٦ تربيع'))))

# ٢^١٠
S.append(slide(f'''{mode('i')}<h2>إذا علمت أن {M(P(2,10),EQ,'١٠٢٤')} فأوجد {M(P(2,11))}</h2>
{st(f'<p class="lead">{M(P(2,11))} تعني أننا ضربنا العدد ٢ مرّةً <b>إضافية</b></p>')}
{st(box(M(P(2,11),EQ,P(2,10),X,'٢',EQ,'١٠٢٤',X,'٢',EQ,'٢٠٤٨',cls="mid")))}'''))
S.append(slide(f'''{mode('we')}<h2>ومنها: {M(P(2,12))} و {M(P(2,9))}</h2>
<div class="row">{box(f'<div class="col"><p class="ask">مرّتان إضافيتان…</p>{st(M(P(2,12),EQ,"١٠٢٤",X,"٢",X,"٢",cls="sm"))}{st(M(EQ,"٤٠٩٦",cls="mid res"))}</div>')}
{box(f'<div class="col"><p class="ask">مرّة أقل… فنقسم!</p>{st(M(P(2,9),EQ,"١٠٢٤","÷","٢",cls="sm"))}{st(M(EQ,"٥١٢",cls="mid res"))}</div>')}</div>'''))
S.append(slide(f'''{mode('u')}''' + quiz(f'استخدم {M(P(2,10),EQ,"١٠٢٤")} لإيجاد {M(P(2,8))}', [M('٢٥٦'), M('٥١٢'), M('٢٠٤٨'), M('١٠٢٢')], 0, 'مرّتان أقل: ١٠٢٤ ÷ ٢ ÷ ٢ = ٢٥٦')))

# العدد المفقود
def box_q(v, show=False): return f'<span class="blank{" shown" if show else ""}">{a(v) if show else "؟"}</span>'
S.append(slide(f'''{mode('i')}<h2>أوجد العدد المفقود: {M(P(3,2),PL,P(4,2),EQ,'<span class="blank">؟</span><sup class="e2">٢</sup>')}</h2>
<div class="row">{st(box(M(P(3,2),EQ,'٩',cls="sm")))}{st(box(M(P(4,2),EQ,'١٦',cls="sm")))}</div>
{st(box(M('٩',PL,'١٦',EQ,'٢٥',cls="mid")))}
{st(box(M('٢٥',EQ,P(5,2),cls="mid"),style="border-color:var(--base)"))}
{st('<div class="note">أيّ عددٍ مربّعه ٢٥؟ إنه <b>٥</b> — لذلك نحتاج أن نحفظ المربعات!</div>')}'''))
S.append(slide(f'''{mode('we')}<h2>معاً: {M(P(8,2),PL,P(6,2),EQ,'<span class="blank">؟</span><sup class="e2">٢</sup>')}</h2>
{st(box(M('٦٤',PL,'٣٦',EQ,'١٠٠',cls="mid")))}{st(box(M('١٠٠',EQ,P(10,2),cls="mid"),style="border-color:var(--base)"))}'''))
S.append(slide(f'''{mode('u')}{timer(3)}''' + quiz(f'{M(P(12,2),PL,P(5,2),EQ,"<span class=\"blank\">؟</span><sup class=\"e2\">٢</sup>")}', [M('١٧'), M('١٣'), M('١٦٩'), M('١٤')], 1, '١٤٤ + ٢٥ = ١٦٩ = ١٣ × ١٣')))

# الجذور — مطابقة لصفحة «الجذور»: للجذر التربيعي قيمتان (±)، والتكعيبي يقبل السالب
def PM(v): return f'{a(v)} ، {N(v)}'
S.append(slide(f'''<h2>الجذر التربيعي: العملية العكسية للتربيع</h2>
<div class="row">{st(box(f'<div class="col">{M(P(5,2),EQ,rep(5,2),EQ,"٢٥",cls="sm")}{M(PN(5,2),EQ,N(5),X,N(5),EQ,"٢٥",cls="sm")}</div>'))}
{st(box(f'<div class="col">{M(R(25),EQ,PM(5),cls="mid")}<small class="hint">للجذر التربيعي قيمتان: موجبة وسالبة</small></div>',style="border-color:var(--base)"))}</div>
{st('<div class="note">هل يوجد جذر تربيعي لعدد سالب؟ <b>لا</b> — لأن ناتج ضرب عددين متشابهين في الإشارة موجبٌ دائماً</div>')}'''))
S.append(slide(f'''<h2>الجذر التكعيبي: العملية العكسية للتكعيب</h2>
<div class="row">{st(box(f'<div class="col">{M(P(5,3),EQ,"١٢٥",cls="sm")}<span class="arrow">↩</span>{M(R(125,3),EQ,"٥",cls="mid")}</div>'))}
{st(box(f'<div class="col">{M(PN(5,3),EQ,N(125),cls="sm")}<span class="arrow">↩</span>{M(R("−125",3),EQ,N(5),cls="mid")}</div>',style="border-color:var(--exp)"))}</div>
{st('<div class="note">لاحظ: <b>يمكن</b> كتابة عددٍ سالب تحت الجذر التكعيبي، والإجابة تكون سالبة</div>')}'''))
S.append(slide(f'''{mode('i')}<h2>أوجد: {M(R(9))} و {M(R(27,3))}</h2>
<div class="row">{box(f'<div class="col">{M(R(9),cls="mid")}{st('<p class="ask" style="color:#2563EB">ما العدد الذي مربّعه ٩؟</p>')}{st(M(P(3,2),EQ,"٩","و",PN(3,2),EQ,"٩",cls="sm"))}{st(M(EQ,PM(3),cls="mid res"))}</div>')}
{box(f'<div class="col">{M(R(27,3),cls="mid")}{st('<p class="ask" style="color:#2563EB">ما العدد الذي مكعّبه ٢٧؟</p>')}{st(M(rep(3,3),EQ,"٢٧",cls="sm"))}{st(M(EQ,"٣",cls="mid res"))}</div>')}</div>'''))
S.append(slide(f'''{mode('we')}<h2>معاً: {M(R(196))} و {M(R("−27",3))}</h2>
<div class="row">{box(f'<div class="col"><p class="ask">ابحثوا في جدول المربعات…</p>{st(M(P(14,2),EQ,"١٩٦",cls="sm"))}{st(M(EQ,PM(14),cls="mid res"))}</div>')}
{box(f'<div class="col"><p class="ask">عددٌ سالب تحت الجذر التكعيبي؟</p>{st(M(N(3),X,N(3),X,N(3),EQ,N(27),cls="sm"))}{st(M(EQ,N(3),cls="mid res"))}</div>')}</div>'''))
S.append(slide(f'''{mode('u')}{timer(2)}''' + quiz(f'ما قيمة {M(R(81))} ؟', [M(PM(9)), M('٩'), M('٤٠٫٥'), M('٨١ ، '+N(81))], 0, 'لأن ٩ × ٩ = ٨١ و (−٩) × (−٩) = ٨١')))
S.append(slide(f'''{mode('u')}''' + quiz(f'ما قيمة {M(R(1000,3))} ؟', [M('١٠٠'), M('١٠'), M(PM(10)), M('٣٣٣')], 1, '١٠ × ١٠ × ١٠ = ١٠٠٠')))
S.append(slide(f'''<span class="qbadge">فكّر 💡</span><h2>هل {M(R("9 + 16"))} = {M(R(9),PL,R(16))} ؟</h2>
<div class="row">{st(box(f'<div class="col">{M(R("9 + 16"),EQ,R(25),EQ,"٥",cls="mid")}</div>'))}{st(box(f'<div class="col">{M(R(9),PL,R(16),EQ,"٣",PL,"٤",EQ,"٧",cls="mid")}</div>'))}</div>
{st('<div class="note"><b>لا!</b> ٥ ≠ ٧ — لا يمكن توزيع الجذر على الجمع الذي بداخله</div>')}'''))
# تفكير: عدد العوامل
S.append(slide(f'''<span class="qbadge">فكّر 💡</span><h2>هل صحيحٌ أن للعدد المربّع عدداً <b class="c-exp">فردياً</b> من العوامل دائماً؟</h2>
<div class="row">{st(box(f'<div class="col"><b class="kk">١٢ (ليس مربّعاً)</b><div class="pairs"><span>١ × ١٢</span><span>٢ × ٦</span><span>٣ × ٤</span></div><div class="fac">١ ، ٢ ، ٣ ، ٤ ، ٦ ، ١٢</div><b class="even">٦ عوامل ← زوجي</b></div>'))}
{st(box(f'<div class="col"><b class="kk">١٦ (مربّع)</b><div class="pairs"><span>١ × ١٦</span><span>٢ × ٨</span><span class="self">٤ × ٤</span></div><div class="fac">١ ، ٢ ، ٤ ، ٨ ، ١٦</div><b class="odd">٥ عوامل ← فردي</b></div>',style="border-color:var(--exp)"))}</div>
{st('<div class="note">نعم! العوامل تأتي أزواجاً، إلا في العدد المربّع: هناك عاملٌ مضروبٌ في نفسه (٤ × ٤) فيُعدّ مرّة واحدة</div>')}'''))

# بطاقة الخروج ٢ + خلاصة
S.append(slide(f'''<span class="qbadge">بطاقة الخروج 🎫</span><h2>أجب في دفترك</h2>
<div class="exit">{st(f'<div><b>١</b>أيّهما أكبر: {M(P(2,5))} أم {M(P(5,2))}؟</div>')}{st(f'<div><b>٢</b>أوجد العدد المفقود: {M(P(6,2),PL,P(8,2),EQ,'<span class="blank">؟</span><sup class="e2">٢</sup>')}</div>')}{st(f'<div><b>٣</b>أوجد {M(R(49))} و {M(R("−8",3))}</div>')}</div>
<button class="flip box col" style="min-width:40vw"><span class="tap">👆 اضغط لإظهار الإجابات</span><span class="hid col">{M("٣٢ أكبر من ٢٥ ← ",P(2,5),cls="sm")}{M("٣٦",PL,"٦٤",EQ,"١٠٠",EQ,P(10,2),cls="sm")}{M(PM(7)," ؛ ",N(2),cls="sm")}</span></button>'''))
S.append(slide(f'''<h2>الخلاصة</h2><div class="row" style="max-width:1150px">
{st(box(f'<div class="col">{M(P(5,2),cls="mid")}<b>تربيع — مربّع العدد</b></div>',style="flex:1;min-width:210px"))}
{st(box(f'<div class="col">{M(P(5,3),cls="mid")}<b>تكعيب — مكعّب العدد</b></div>',style="flex:1;min-width:210px"))}
{st(box(f'<div class="col"><span class="m mid">⚖️</span><b>لنقارن القوى نحسب قيمتها</b></div>',style="flex:1;min-width:210px"))}
{st(box(f'<div class="col">{M(R(49),EQ,PM(7),cls="mid")}<b>الجذر يعكس القوّة</b></div>',style="flex:1;min-width:210px"))}</div>
<p class="who st">المرجع: ورقة «درسي في صفحة» — الدرس ١-٦ القوى (الأسس) والجذور</p>'''))

EXTRA_CSS = '''
.c-i{color:#2563EB}.c-we{color:#16A34A}.c-u{color:#EA580C}.c-b{color:var(--base)}.c-exp{color:var(--exp)}
.mode{display:flex;align-items:center;gap:.6em;padding:.45em 1.2em;border-radius:99px;font-size:clamp(16px,2.4vh,26px);border:3px solid;background:#fff}
.mode .ic{font-size:1.3em}.mode b{font-family:var(--fh);font-weight:900;font-size:1.25em}.mode small{font-weight:700;color:var(--ink2)}
.mode.i{border-color:#2563EB;color:#2563EB}.mode.we{border-color:#16A34A;color:#16A34A}.mode.u{border-color:#EA580C;color:#EA580C}
.slide:has(.mode.i){background:linear-gradient(90deg,transparent 0 calc(100% - 14px),#2563EB 0) }
.slide:has(.mode.we){background:linear-gradient(90deg,transparent 0 calc(100% - 14px),#16A34A 0)}
.slide:has(.mode.u){background:linear-gradient(90deg,transparent 0 calc(100% - 14px),#EA580C 0)}
.ask{font-size:clamp(18px,2.8vh,30px);font-weight:800;color:#16A34A}
.hint{font-size:clamp(14px,2vh,20px);font-weight:700;color:var(--ink2)}
.divider h2{font-size:clamp(30px,6vh,64px)}
.plan{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:1.4vh 1.2vw;width:min(1100px,90vw)}
.plan div{background:#fff;border:2.5px solid var(--line);border-radius:16px;padding:1.4vh 1vw;font-weight:800;font-size:clamp(15px,2.3vh,24px);display:flex;flex-direction:column;gap:.3em;align-items:center;text-align:center}
.plan b{font-family:var(--fh);color:var(--exp);font-size:1.3em}
.grid{display:grid;gap:5px}.grid i{display:block;width:clamp(26px,5.5vh,58px);aspect-ratio:1;border-radius:7px;background:#CFE9EC;border:2px solid var(--base)}
.g5{grid-template-columns:repeat(5,auto)}.g3{grid-template-columns:repeat(3,auto)}
.grid.st i{opacity:0;transform:scale(.3);transition:all .3s}
.grid.st.in i{opacity:1;transform:none}
''' + ''.join(f'.grid.st.in i:nth-child({k+1}){{transition-delay:{k*0.05:.2f}s}}' for k in range(25)) + '''
.g3 i{background:#FCE3DD;border-color:var(--exp)}
.layers small{font-weight:800;color:var(--ink2);font-size:clamp(14px,2vh,20px)}
.pw{display:flex;flex-direction:column;gap:1.6vh;width:min(1150px,92vw)}
.pwr{display:flex;align-items:center;justify-content:space-between;gap:2vw;background:#fff;border:2.5px solid var(--line);border-radius:18px;padding:1.4vh 2vw}
.rd{font-size:clamp(16px,2.5vh,26px);font-weight:700;color:var(--ink2)}.rd b{color:var(--exp)}
.timer{display:flex;align-items:center;gap:.8em;border:3px solid #EA580C;background:#FFF4EC;color:#9A3412;border-radius:16px;padding:.4em 1.1em;font-family:var(--fh);font-weight:900;cursor:pointer;font-size:clamp(16px,2.4vh,26px)}
.timer .tt{font-size:1.5em;font-variant-numeric:tabular-nums;min-width:3.2ch}
.timer.run{background:#EA580C;color:#fff}.timer.end{animation:shake .4s 3;background:#D63B3B;border-color:#D63B3B;color:#fff}
.sqs{display:grid;grid-template-columns:repeat(10,1fr);gap:1vh .7vw;width:min(1200px,94vw)}
.sqs.c10{grid-template-columns:repeat(5,1fr);width:min(900px,90vw)}.sqs.c4{grid-template-columns:repeat(4,1fr);width:min(1000px,90vw)}
.sq{display:flex;flex-direction:column;align-items:center;gap:.3vh;background:#fff;border:2.5px solid var(--line);border-radius:14px;padding:1vh .3vw;cursor:pointer;font-family:var(--fh);font-weight:900;box-shadow:0 5px 0 #DCE5F0}
.sq .n{font-size:clamp(20px,3.6vh,38px);color:var(--base)}
.sq .v{font-size:clamp(18px,3.2vh,34px);color:var(--exp);min-height:1.3em;visibility:hidden}
.sq.open{background:#FFF7F4;border-color:var(--exp)}.sq.open .v{visibility:visible;animation:pop .4s}
.sqs.c4 .n{font-size:clamp(34px,6vh,64px)}.sqs.c4 .v{font-size:clamp(30px,5.4vh,58px)}
.reveal-all{font-family:var(--fh);font-weight:800;background:none;border:2px dashed var(--ink2);color:var(--ink2);border-radius:12px;padding:.4em 1.2em;cursor:pointer;font-size:clamp(14px,2vh,20px)}
.chips{display:flex;gap:.8vw;flex-wrap:wrap;justify-content:center}
.blank{display:inline-flex;min-width:1.6em;justify-content:center;border:3px dashed var(--exp);border-radius:12px;color:var(--exp);padding:0 .2em}
.e2{color:var(--exp);font-size:.55em;position:relative;top:-.8em}
.arrow{font-size:clamp(26px,4.6vh,48px);color:var(--ink2);transform:rotate(-90deg)}
.exit{display:flex;flex-direction:column;gap:1.4vh;width:min(900px,90vw)}
.exit .st>div{display:flex;align-items:center;gap:1em;background:#fff;border:2.5px solid var(--line);border-radius:16px;padding:1.2vh 1.4vw;font-weight:800;font-size:clamp(20px,3.3vh,36px)}
.exit b{font-family:var(--fh);background:var(--ink);color:#fff;border-radius:50%;width:1.6em;height:1.6em;display:flex;align-items:center;justify-content:center;flex:none}
.pairs{display:flex;flex-direction:column;gap:.6vh;font-family:var(--fh);font-weight:900;font-size:clamp(20px,3.4vh,36px)}
.pairs span{background:#EAF1FA;border-radius:10px;padding:.1em .8em}.pairs .self{background:#FDE7E2;color:var(--exp);border:2px solid var(--exp)}
.fac{font-weight:800;font-size:clamp(17px,2.7vh,28px);color:var(--ink2)}
.kk{font-family:var(--fh);font-size:clamp(20px,3.2vh,34px)}
.even{color:var(--ink2);font-size:clamp(18px,2.8vh,30px)}.odd{color:var(--exp);font-size:clamp(18px,2.8vh,30px)}
button.flip{font:inherit;color:inherit;cursor:pointer}
.rt{display:inline-flex;align-items:flex-start;direction:rtl;unicode-bidi:isolate;position:relative}
.rt .rs{font-family:Tahoma,sans-serif;font-weight:400;transform:scale(-1,1.15);color:var(--ink)}
.rt .ov{border-top:.07em solid var(--ink);padding:0 .08em;margin-inline-start:-.04em;display:inline-flex;direction:rtl}
.ng{direction:rtl;unicode-bidi:isolate;display:inline-flex}.ng i{font-style:normal}
.rt .ri{font-style:normal;font-size:.42em;color:var(--exp);position:absolute;right:.05em;top:-.05em}
'''
EXTRA_JS = '''
  // بطاقات المربعات: ضغطة تكشف، و«اكشف الكل»
  document.querySelectorAll('.sq').forEach(function(b){b.addEventListener('click',function(e){e.stopPropagation();if(!b.classList.contains('open')){b.classList.add('open');tone('step');}});});
  document.querySelectorAll('.reveal-all').forEach(function(b){b.addEventListener('click',function(e){e.stopPropagation();
    b.parentNode.querySelectorAll('.sq').forEach(function(x,i){setTimeout(function(){x.classList.add('open');},i*60);});tone('ok');});});
  // مؤقّت «أنتم»
  document.querySelectorAll('.timer').forEach(function(t){
    var total=+t.dataset.s,left=total,iv=null,tt=t.querySelector('.tt'),tl=t.querySelector('.tl');
    function fmt(s){return ar(Math.floor(s/60))+':'+ar(String(s%60).padStart(2,'0'));}
    t.addEventListener('click',function(e){e.stopPropagation();
      if(iv){clearInterval(iv);iv=null;t.classList.remove('run');tl.textContent='▶ استئناف';return;}
      if(left<=0){left=total;t.classList.remove('end');}
      t.classList.add('run');tl.textContent='⏸ إيقاف';
      iv=setInterval(function(){left--;tt.textContent=fmt(left);if(left<=5&&left>0)tone('step');
        if(left<=0){clearInterval(iv);iv=null;t.classList.remove('run');t.classList.add('end');tl.textContent='انتهى الوقت! ⟲';tone('no');}},1000);
    });
  });
'''
base_css = open(os.path.join(KIT,'base.css'),encoding='utf-8').read()
base_js = open(os.path.join(KIT,'base.js'),encoding='utf-8').read()
base_js = base_js.replace("document.querySelectorAll('.flip')", EXTRA_JS + "\n  document.querySelectorAll('.flip')")
html = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>القوى والجذور — الصف السابع</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Noto+Kufi+Arabic:wght@600;800;900&family=Tajawal:wght@500;700;800&display=swap" rel="stylesheet">
<style>{base_css}{EXTRA_CSS}{open(os.path.join(KIT,'big.css'),encoding='utf-8').read()}</style></head><body>
<div class="deck" id="deck">
{chr(10).join(S)}
</div>
<canvas id="fx"></canvas>
<nav class="bar">
  <button id="fs" title="ملء الشاشة" aria-label="ملء الشاشة"><svg viewBox="0 0 24 24"><path d="M4 9V4h5M20 9V4h-5M4 15v5h5M20 15v5h-5"/></svg></button>
  <button id="prev" title="السابق" aria-label="السابق"><svg viewBox="0 0 24 24"><path d="M9 6l6 6-6 6"/></svg></button>
  <span class="cnt" id="cnt"></span><div class="prog"><i id="pg"></i></div>
  <button id="next" class="next" aria-label="التالي">التالي <svg viewBox="0 0 24 24"><path d="M15 6l-6 6 6 6"/></svg></button>
</nav>
<script>{base_js}</script></body></html>'''
open(os.path.join(HERE,'القوى_والجذور_عرض_تفاعلي.html'), 'w', encoding='utf-8').write(html)
print(len(S), 'slides')
