# عرض مراجعة «ملخّص الوحدة الأولى: الأعداد الصحيحة والقوى والجذور» — الصف السابع.
# المرجع: صفحة ملخّص الوحدة في كتاب الطالب («يجب أن تعرف أنّ» + «يجب أن تكون قادراً على»).
# python3.12 gen_powers.py unit1_slides.py مراجعة_الوحدة_الأولى_عرض_تفاعلي.html "مراجعة الوحدة الأولى — الصف السابع"
# لكل قاعدة: بطاقة القاعدة ← مثالٌ محلول خطوةً خطوة ← سؤالٌ سريع (أنتم).

DV = '<span class="x">÷</span>'; MI = '<span class="x">−</span>'
def BR(*p): return '<span class="brk">(' + ' '.join(p) + ')</span>'
def STP(lab, expr, cls=''): return st(f'<div class="stp {cls}"><span class="lab">{lab}</span>{expr}</div>')
def STEPS(*rows): return '<div class="stps">' + ''.join(rows) + '</div>'
def RULE(n, t): return f'<div class="rulecard"><span class="rn">قاعدة {a(n)}</span><span>{t}</span></div>'
def SEC(n, title, items):
    return slide(f'''<span class="tag">الجزء {a(n)} من ٥</span><h2>{title}</h2>
<div class="exit">{''.join(st(f'<div><b>{a(i + 1)}</b><span>{t}</span></div>') for i, t in enumerate(items))}</div>''', 'divider')
def chips(nums, hot=()): return '<div class="chips">' + ''.join(f'<span class="chip{" hot" if n in hot else ""}">{a(n)}</span>' for n in nums) + '</div>'

S = []
# ═══ الغلاف ═══
S.append(slide('''<span class="tag">الصف السابع · مراجعة الوحدة الأولى</span>
<h1 class="h1s">الأعداد الصحيحة والقوى والجذور</h1>
<p class="lead" style="font-size:clamp(26px,4.8vh,56px)">إعداد: أ. عيسى الحارثي</p>''', 'cover'))
S.append(slide('''<h2>نراجع قواعد الوحدة كلّها في خمسة أجزاء</h2>
<div class="can">
<div><span class="can-i">١</span><span>الأعداد الصحيحة: الطرح، والضرب والقسمة</span></div>
<div><span class="can-i">٢</span><span>المضاعفات والعوامل والعوامل المشتركة</span></div>
<div><span class="can-i">٣</span><span>اختبارات قابلية القسمة</span></div>
<div><span class="can-i">٤</span><span>الأعداد الأولية، والعوامل الأولية، والعامل المشترك الأكبر والمضاعف المشترك الأصغر</span></div>
<div><span class="can-i">٥</span><span>القوى والجذور</span></div></div>'''))

# ═══ ١ الأعداد الصحيحة ═══
S.append(SEC(1, 'الأعداد الصحيحة', ['طرح عددٍ سالب', 'إشارة ناتج الضرب والقسمة']))
S.append(slide(f'''{RULE(1, 'يمكنك طرح عددٍ سالب بإضافة العدد الموجب المقابل له')}
<div class="row">{box(STEPS(STP('المسألة', M('٥', MI, BR(N(3)), cls="sm")), STP('نحوّل الطرح', M(EQ, '٥', PL, '٣', cls="sm")), STP('الناتج', M(EQ, '٨', cls="sm"), 'fin')))}
{box(STEPS(STP('المسألة', M(N(2), MI, BR(N(7)), cls="sm")), STP('نحوّل الطرح', M(EQ, N(2), PL, '٧', cls="sm")), STP('الناتج', M(EQ, '٥', cls="sm"), 'fin')))}</div>
{st('<div class="note">«ناقص سالب» تصبح «زائد»: − (−) = +</div>')}'''))
S.append(slide(f'''{mode('u')}{timer(1)}''' + quiz(f'أوجد ناتج {M("٤", MI, BR(N(6)))}', [M('١٠'), M(N(2)), M('٢'), M(N(10))], 0, '٤ − (−٦) = ٤ + ٦ = ١٠')))
SIGN = lambda s1, s2, r, ok: f'<div class="sg {"pos" if ok else "neg"}"><span>{s1}</span><span class="x">×</span><span>{s2}</span><span class="x">=</span><b>{r}</b></div>'
S.append(slide(f'''{RULE(2, 'عند ضرب عددين صحيحين أو قسمتهما: <b class="c-good">إشارتان متشابهتان ← الناتج موجب</b>، و<b class="c-bad">إشارتان مختلفتان ← الناتج سالب</b>')}
<div class="row" style="align-items:center">
<div class="sgrid">{SIGN('+', '+', '+', 1)}{SIGN('−', '−', '+', 1)}{SIGN('+', '−', '−', 0)}{SIGN('−', '+', '−', 0)}</div>
<div class="col">{st(box(M(N(5), X, N(2), EQ, '١٠', cls="sm"), style="border-color:var(--good)"))}{st(box(M(N(5), X, '٢', EQ, N(10), cls="sm"), style="border-color:var(--bad)"))}
{st(box(M(N(20), DV, N(4), EQ, '٥', cls="sm"), style="border-color:var(--good)"))}{st(box(M('٢٠', DV, N(4), EQ, N(5), cls="sm"), style="border-color:var(--bad)"))}</div></div>'''))
S.append(slide(f'''{mode('u')}{timer(1)}''' + quiz(f'أوجد ناتج {M(N(6), X, N(3))}', [M(N(18)), M('١٨'), M(N(9)), M('٩')], 1, 'إشارتان متشابهتان ← موجب: ٦ × ٣ = ١٨')))
S.append(slide(f'''{mode('u')}''' + quiz(f'أوجد ناتج {M(N(24), DV, "٦")}', [M('٤'), M(N(4)), M(N(18)), M('١٨')], 1, 'إشارتان مختلفتان ← سالب: ٢٤ ÷ ٦ = ٤ ، إذن الناتج −٤')))

# ═══ ٢ المضاعفات والعوامل ═══
S.append(SEC(2, 'المضاعفات والعوامل', ['المضاعفات', 'العوامل', 'العوامل المشتركة']))
S.append(slide(f'''{RULE(3, 'تجد مضاعفات عددٍ بالضرب في ١، ٢، ٣، وهكذا')}
<p class="lead">مضاعفات العدد ٦:</p>
<div class="row">{''.join(st(box(M('٦', X, a(k), EQ, a(6 * k), cls="sm"))) for k in range(1, 6))}</div>
{st('<div class="ans l"><span class="k">مضاعفات ٦</span><span class="m sm">٦ ، ١٢ ، ١٨ ، ٢٤ ، ٣٠ ، …</span></div>')}
{st('<div class="note">المضاعفات لا تنتهي أبداً!</div>')}'''))
S.append(slide(f'''{RULE(4, 'كلّ عددٍ صحيحٍ موجب له مضاعفات و<b>عوامل</b> — والعوامل تأتي أزواجاً')}
<p class="lead">عوامل العدد ١٢: أيّ عددين ناتج ضربهما ١٢؟</p>
<div class="row">{st(box(M('١', X, '١٢', cls="sm")))}{st(box(M('٢', X, '٦', cls="sm")))}{st(box(M('٣', X, '٤', cls="sm")))}</div>
{st('<div class="ans g"><span class="k">عوامل ١٢</span><span class="m sm">١ ، ٢ ، ٣ ، ٤ ، ٦ ، ١٢</span></div>')}'''))
S.append(slide(f'''{RULE(5, 'من الممكن أن تكون هناك <b>عوامل مشتركة</b> بين عددين صحيحين')}
<div class="col" style="gap:1.4vh">
{st('<div class="frow"><b>عوامل ١٢</b>' + chips([1, 2, 3, 4, 6, 12], (1, 2, 3, 6)) + '</div>')}
{st('<div class="frow"><b>عوامل ١٨</b>' + chips([1, 2, 3, 6, 9, 18], (1, 2, 3, 6)) + '</div>')}</div>
{st('<div class="ans g"><span class="k">المشتركة</span><span class="m sm">١ ، ٢ ، ٣ ، ٦</span></div>')}
{st('<div class="note">أكبرها <b>٦</b> — وهو <b>العامل المشترك الأكبر</b> للعددين ١٢ و ١٨</div>')}'''))
S.append(slide(f'''{mode('u')}{timer(1)}''' + quiz('أيّ عددٍ <b>ليس</b> من مضاعفات ٧؟', [M('١٤'), M('٢١'), M('٢٧'), M('٣٥')], 2, '٧ × ٣ = ٢١ و ٧ × ٤ = ٢٨ ، إذن ٢٧ ليس من مضاعفات ٧')))
S.append(slide(f'''{mode('u')}''' + quiz('ما العوامل المشتركة للعددين ٨ و ١٢؟', [M('١ ، ٢ ، ٤'), M('٢ ، ٤ ، ٨'), M('١ ، ٢ ، ٣ ، ٤'), M('٤ فقط')], 0, 'عوامل ٨: ١، ٢، ٤، ٨ — عوامل ١٢: ١، ٢، ٣، ٤، ٦، ١٢ — المشتركة: ١، ٢، ٤')))

# ═══ ٣ قابلية القسمة ═══
TESTS = [('٢', 'الآحاد زوجي: ٠، ٢، ٤، ٦، ٨'), ('٣', 'مجموع الأرقام يقبل القسمة على ٣'), ('٤', 'العدد المكوَّن من آخر رقمين يقبل القسمة على ٤'),
         ('٥', 'الآحاد ٠ أو ٥'), ('٦', 'يقبل القسمة على ٢ وعلى ٣ معاً'), ('٨', 'العدد المكوَّن من آخر ثلاثة أرقام يقبل القسمة على ٨'),
         ('٩', 'مجموع الأرقام يقبل القسمة على ٩'), ('١٠', 'الآحاد ٠'), ('١٠٠', 'آخر رقمين ٠٠')]
S.append(SEC(3, 'اختبارات قابلية القسمة', ['اختبارات بسيطة للقسمة على ٢، ٣، ٤، ٥، ٦، ٨، ٩، ١٠، ١٠٠', 'نطبّقها على عددٍ واحد']))
for part in (TESTS[:4], TESTS[4:8], TESTS[8:]):   # أربع بطاقات في الشريحة ليبقى الخط كبيراً
    S.append(slide(f'''{RULE(6, 'اختباراتٌ بسيطة لقابلية القسمة — اضغط على البطاقة')}
<div class="xgrid c{2 if len(part) > 1 else 1}">{''.join(f'<button class="flip xcard dv"><span class="xq">القسمة على <b>{n}</b></span><span class="tap">👆</span><span class="hid xa">{t}</span></button>' for n, t in part)}</div>'''))
RES = [('٢', 1, 'الآحاد ٢ زوجي'), ('٣', 1, '٣ + ٧ + ٢ = ١٢'), ('٤', 1, '٧٢ ÷ ٤ = ١٨'), ('٥', 0, 'الآحاد ليس ٠ أو ٥'), ('٦', 1, 'يقبل ٢ و ٣'),
       ('٨', 0, '٣٧٢ ÷ ٨ = ٤٦ والباقي ٤'), ('٩', 0, 'مجموع الأرقام ١٢'), ('١٠', 0, 'الآحاد ليس ٠'), ('١٠٠', 0, 'آخر رقمين ليسا ٠٠')]
for part in (RES[:6], RES[6:]):
    S.append(slide(f'''<div class="row hdr">{mode('we')}<h2>هل يقبل <b class="c-exp">٣٧٢</b> القسمة على…؟</h2></div>
<div class="xgrid c3">{''.join(f'<button class="flip xcard dv"><span class="xq">على <b>{n}</b>؟</span><span class="tap">👆</span><span class="hid xa {"yes" if ok else "no"}">{"✔ نعم" if ok else "✘ لا"}<small>{w}</small></span></button>' for n, ok, w in part)}</div>'''))
S.append(slide(f'''{mode('u')}{timer(1)}''' + quiz('هل يقبل العدد ٥٤٠ القسمة على ٩؟', ['نعم', 'لا'], 0, 'مجموع أرقامه ٥ + ٤ + ٠ = ٩ ، و ٩ يقبل القسمة على ٩')))

# ═══ ٤ الأعداد الأولية ═══
S.append(SEC(4, 'الأعداد الأولية', ['العدد الأولي له عاملان فقط', 'غربال إراتوستينس', 'كتابة العدد بدلالة عوامله الأولية', 'العامل المشترك الأكبر والمضاعف المشترك الأصغر']))
S.append(slide(f'''{RULE(7, 'الأعداد الأوليّة لها <b>عاملان فقط</b>: الواحد والعدد نفسه')}
<div class="row">
{st(box(f'<div class="col"><b class="kk">٧</b><span class="m sm">١ ، ٧</span><span class="right">✔ أولي</span></div>', style="border-color:var(--good)"))}
{st(box(f'<div class="col"><b class="kk">٩</b><span class="m sm">١ ، ٣ ، ٩</span><span class="wrong">✘ ليس أولياً</span></div>', style="border-color:var(--bad)"))}
{st(box(f'<div class="col"><b class="kk">١</b><span class="m sm">١</span><span class="wrong">✘ ليس أولياً</span></div>', style="border-color:var(--bad)"))}</div>
{st('<div class="note">العدد ١ له عاملٌ واحد فقط، لذلك <b>ليس أولياً</b> — و ٢ هو العدد الأولي الزوجي الوحيد</div>')}'''))
PR = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47}
cells = ''.join(f'<button class="sv{" one" if n == 1 else ""}" data-n="{n}">{a(n)}</button>' for n in range(1, 51))
S.append(slide(f'''{RULE(8, 'يمكن استخدام طريقة <b>غربال إراتوستينس</b> لإيجاد الأعداد الأولية')}
<div class="sieve" id="sieve">{cells}</div>
<div class="row svb">{''.join(f'<button class="svbtn" data-p="{p}">احذف مضاعفات {a(p)}</button>' for p in (2, 3, 5, 7))}<button class="svbtn show">أظهر الأعداد الأولية</button><button class="svbtn reset">من جديد</button></div>
<script>(function(){{var g=document.getElementById('sieve');
document.querySelectorAll('.svbtn').forEach(function(b){{b.addEventListener('click',function(e){{e.stopPropagation();
 var cs=g.querySelectorAll('.sv');
 if(b.classList.contains('reset')){{cs.forEach(function(c){{c.classList.remove('out','pr','cur');}});return;}}
 if(b.classList.contains('show')){{cs.forEach(function(c){{if(!c.classList.contains('out')&&c.dataset.n!=='1')c.classList.add('pr');}});return;}}
 var p=+b.dataset.p;cs.forEach(function(c){{var n=+c.dataset.n;c.classList.remove('cur');if(n===p)c.classList.add('cur');else if(n%p===0)c.classList.add('out');}});
}});}});}})();</script>'''))
S.append(slide(f'''{RULE(9, 'يمكنك كتابة كلّ عددٍ صحيحٍ موجب في صورة ناتج ضرب أعدادٍ أوليّة')}
{box(STEPS(STP('نقسم على ٢', M('٥٠٠', DV, '٢', EQ, '٢٥٠', cls="sm")), STP('على ٢ مرة أخرى', M('٢٥٠', DV, '٢', EQ, '١٢٥', cls="sm")),
 STP('على ٥', M('١٢٥', DV, '٥', EQ, '٢٥', cls="sm")), STP('على ٥', M('٢٥', DV, '٥', EQ, '٥', cls="sm")), STP('على ٥', M('٥', DV, '٥', EQ, '١', cls="sm"))))}'''))
S.append(slide(f'''{RULE(9, 'نكتب العدد ناتجَ ضرب أعدادٍ أوليّة، ثم نختصره بالأسس')}
{st(box(M('٥٠٠', EQ, '٢', X, '٢', X, '٥', X, '٥', X, '٥', cls="mid")))}{st(box(M('٥٠٠', EQ, P(2, 2), X, P(5, 3), cls="big"), style="border-color:var(--base)"))}'''))
S.append(slide(f'''{RULE(10, 'يمكن استخدام نواتج ضرب العوامل الأوليّة لإيجاد <b class="c-gcd">العامل المشترك الأكبر</b> و<b class="c-lcm">المضاعف المشترك الأصغر</b>')}
<div class="row">{st(box(M('١٢', EQ, P(2, 2), X, '٣', cls="sm")))}{st(box(M('١٨', EQ, '٢', X, P(3, 2), cls="sm")))}</div>
<div class="row">
{st(f'<div class="ans g col"><span class="k">العامل المشترك الأكبر</span><small class="hint">الأساسات المشتركة بالأس الأصغر</small>{M("٢", X, "٣", EQ, "٦", cls="sm")}</div>')}
{st(f'<div class="ans l col"><span class="k">المضاعف المشترك الأصغر</span><small class="hint">كلّ الأساسات بالأس الأكبر</small>{M(P(2, 2), X, P(3, 2), EQ, "٣٦", cls="sm")}</div>')}</div>
{st('<div class="note">للتأكّد: ٣٦ أوّل عددٍ في مضاعفات ١٢ (١٢، ٢٤، ٣٦) وفي مضاعفات ١٨ (١٨، ٣٦)</div>')}'''))
S.append(slide(f'''{mode('u')}{timer(2)}''' + quiz('اكتب ٣٦ بدلالة عوامله الأولية', [M(P(2, 2), X, P(3, 2)), M('٤', X, '٩'), M('٢', X, P(3, 2)), M(P(2, 3), X, '٣')], 0, '٣٦ = ٢ × ٢ × ٣ × ٣ = ٢² × ٣² — أمّا ٤ × ٩ فعاملاه ليسا أوليين')))
S.append(slide(f'''{mode('u')}''' + quiz('ما العامل المشترك الأكبر للعددين ٨ و ١٢؟', [M('٢'), M('٤'), M('٢٤'), M('٩٦')], 1, '٨ = ٢³ و ١٢ = ٢² × ٣ ← المشترك ٢² = ٤')))
S.append(slide(f'''{mode('u')}''' + quiz('ما المضاعف المشترك الأصغر للعددين ٤ و ٦؟', [M('٢٤'), M('٢'), M('١٢'), M('١٠')], 2, 'مضاعفات ٤: ٤، ٨، ١٢ — مضاعفات ٦: ٦، ١٢ ← أصغر مضاعفٍ مشترك ١٢')))

# ═══ ٥ القوى والجذور ═══
S.append(SEC(5, 'القوى والجذور', ['المربّع والجذر التربيعي', 'المكعّب والجذر التكعيبي', 'التعبير الأسّي']))
S.append(slide(f'''{RULE(11, f'{M(P(7, 2))} تُقرأ «مربّع العدد ٧»، و {M(R(49))} تُقرأ «الجذر التربيعي للعدد ٤٩» — وللأعداد الصحيحة الموجبة <b>جذران تربيعيان</b>')}
<div class="row">{st(box(M(P(7, 2), EQ, '٧', X, '٧', EQ, '٤٩', cls="mid")))}{st(box(M(PN(7, 2), EQ, '٤٩', cls="mid")))}</div>
{st(box(M(R(49), EQ, PM(7), cls="mid"), style="border-color:var(--base)"))}
{st('<div class="note">لأن ٧ × ٧ = ٤٩ و (−٧) × (−٧) = ٤٩ — تذكّر: احفظ المربعات حتى ٢٠ × ٢٠ = ٤٠٠</div>')}'''))
S.append(slide(f'''{RULE(12, f'{M(P(4, 3))} تُقرأ «مكعّب العدد ٤»، و {M(R(64, 3))} تُقرأ «الجذر التكعيبي للعدد ٦٤»')}
<div class="row">{st(box(M(P(4, 3), EQ, '٤', X, '٤', X, '٤', EQ, '٦٤', cls="mid")))}</div>
{st(box(M(R(64, 3), EQ, '٤', cls="mid"), style="border-color:var(--base)"))}'''))
S.append(slide(f'''{RULE(13, f'{M(P(5, 4))} يعني {M("٥", X, "٥", X, "٥", X, "٥")} — نستخدم التعبير الأسّي لقوى الأعداد الصحيحة الموجبة')}
{box(STEPS(STP('نكتب الضرب', M(P(5, 4), EQ, '٥', X, '٥', X, '٥', X, '٥', cls="sm")), STP('نضرب مثنى', M(EQ, '٢٥', X, '٢٥', cls="sm")), STP('الناتج', M(EQ, '٦٢٥', cls="sm"), 'fin')))}
{st('<div class="note">الأس يخبرنا كم مرّةً نكتب الأساس — وليس عدداً نضرب فيه: ٥⁴ ≠ ٥ × ٤</div>'.replace('٥⁴', M(P(5, 4))))}'''))
S.append(slide(f'''{mode('u')}{timer(1)}''' + quiz(f'ما قيمة {M(R(144))} ؟', [M('١٢'), M(PM(12)), M('٧٢'), M(PM(72))], 1, '١٢ × ١٢ = ١٤٤ و (−١٢) × (−١٢) = ١٤٤')))
S.append(slide(f'''{mode('u')}''' + quiz(f'ما قيمة {M(R(125, 3))} ؟', [M('٥'), M(PM(5)), M('٢٥'), M('١٥')], 0, '٥ × ٥ × ٥ = ١٢٥ — للجذر التكعيبي (لعددٍ موجب) قيمةٌ واحدة')))
S.append(slide(f'''{mode('u')}''' + quiz(f'ما قيمة {M(P(2, 5))} ؟', [M('١٠'), M('٢٥'), M('٣٢'), M('٧')], 2, '٢ × ٢ × ٢ × ٢ × ٢ = ٣٢')))

# ═══ «يجب أن تكون قادراً على» — تقييمٌ ذاتي ═══
SK = ['جمع الأعداد الصحيحة، وطرحها، وضربها، وقسمتها', 'تحديد المضاعفات والعوامل، واستخدامها', 'تحديد الأعداد الأوليّة، واستخدامها',
      'إيجاد العوامل المشتركة والعامل المشترك الأكبر', 'إيجاد المضاعف المشترك الأصغر', f'كتابة عددٍ بدلالة عوامله الأوليّة، مثل: {M("٥٠٠", EQ, P(2, 2), X, P(5, 3))}',
      'معرفة الاختبارات البسيطة لقابلية القسمة وتطبيقها', 'استخدام طريقة غربال إراتوستينس لاستنتاج الأعداد الأوليّة',
      'التعرّف على مربعات الأعداد حتى ٢٠ × ٢٠ على الأقل، والجذور التربيعية المقابلة لها', 'حساب مربعات الأعداد الموجبة والسالبة وجذورها التربيعية، ومكعبات الأعداد وجذورها التكعيبية',
      'استخدام التعبير الأسّي لقوى الأعداد الصحيحة الموجبة', 'التعرّف على الخصائص والأنماط والعلاقات الرياضية، وتعميمها في الحالات البسيطة',
      'استخدام الأعداد وتطبيق الخوارزميات، مثل: إيجاد العامل المشترك الأكبر والمضاعف المشترك الأصغر لعددين']
def CHECK(items, start):
    return ''.join(f'<button class="ck"><span class="cb">{a(start + i)}</span><span>{t}</span></button>' for i, t in enumerate(items))
CKJS = "<script>document.querySelectorAll('.ck').forEach(function(b){b.onclick=function(e){e.stopPropagation();b.classList.toggle('ok');};});</script>"
for k in range(0, len(SK), 4):   # أربعة بنود في الشريحة ليبقى الخط كبيراً
    last = k + 4 >= len(SK)
    S.append(slide(f'''<div class="row hdr"><span class="qbadge">تقييمٌ ذاتي ✅</span><span class="tag">اضغط على ما تتقنه ليصبح أخضر</span></div><h2>يجب أن أكون قادراً على… ({a(k // 4 + 1)})</h2>
<div class="cks">{CHECK(SK[k:k+4], k + 1)}</div>{CKJS if last else ''}'''))
S.append(slide(f'''<h2>أحسنتم! 🎉</h2>
<div class="note">راجعوا ورقة ملخّص الوحدة: كل قاعدة ومعها مثالٌ محلول</div>
<p class="hint st">المرجع: كتاب الطالب — صفحة ملخّص الوحدة الأولى — إعداد: أ. عيسى الحارثي</p>'''))

EXTRA_CSS_OWN = '''
.brk{display:inline-flex;gap:.2em;align-items:baseline;direction:rtl;unicode-bidi:isolate}
.stps{display:flex;flex-direction:column;gap:1.4vh;align-items:stretch}
.stp{display:flex;align-items:center;gap:1.4vw;justify-content:space-between}
.stp .lab{flex:none;font-family:var(--fh);font-weight:800;font-size:clamp(16px,2.6vh,28px);color:#2563EB;background:#EAF1FF;border-radius:12px;padding:.2em .8em;min-width:6.5em;text-align:center}
.stp.fin .lab{background:var(--good);color:#fff}.stp.fin .m{color:var(--good)}
.rulecard{display:flex;align-items:center;gap:1em;background:#fff;border:3px solid var(--ink);border-radius:20px;padding:1.4vh 1.6vw;width:min(1150px,92vw);font-weight:700;font-size:clamp(20px,3.3vh,36px);line-height:1.6;box-shadow:0 7px 0 #DCE5F0}
.rulecard .rn{flex:none;font-family:var(--fh);font-weight:900;background:var(--ink);color:#fff;border-radius:14px;padding:.2em .7em;font-size:.8em}
.c-good{color:var(--good)}.c-bad{color:var(--bad)}.c-gcd{color:var(--gcd)}.c-lcm{color:var(--lcm)}
.sgrid{display:grid;grid-template-columns:repeat(2,auto);gap:1.2vh 1.2vw}
.sg{display:flex;align-items:center;gap:.4em;font-family:var(--fh);font-weight:900;font-size:clamp(28px,5vh,56px);background:#fff;border:3px solid;border-radius:16px;padding:.2em .6em}
.sg.pos{border-color:var(--good)}.sg.pos b{color:var(--good)}.sg.neg{border-color:var(--bad)}.sg.neg b{color:var(--bad)}
.chips{display:flex;gap:.6vw;flex-wrap:wrap}
.chip{font-family:var(--fh);font-weight:900;font-size:clamp(22px,3.8vh,42px);background:#fff;border:3px solid var(--line);border-radius:14px;padding:.1em .6em}
.chip.hot{background:#FFF1D6;border-color:var(--gcd);color:#7A4A00}
.frow{display:flex;align-items:center;gap:1.2vw}.frow>b{font-family:var(--fh);font-size:clamp(20px,3.3vh,36px);min-width:5.5em}
.xcard.dv .xq b{color:var(--exp);font-size:1.2em}
.xa.yes{color:var(--good)}.xa.no{color:var(--bad)}.xa small{font-size:.6em;color:var(--ink2)}
.sieve{display:grid;grid-template-columns:repeat(10,minmax(0,1fr));gap:.6vh .5vw;width:min(1000px,88vw)}
.sv{font-family:var(--fh);font-weight:900;font-size:clamp(18px,3.2vh,34px);background:#fff;border:2.5px solid var(--line);border-radius:10px;padding:.35vh 0;color:var(--ink);position:relative}
.sv.one{color:#9FB0C6}.sv.out{color:#B8C4D4;background:#F2F5F9}
.sv.out::after{content:'';position:absolute;inset:50% 12%;border-top:3px solid var(--bad);transform:rotate(-20deg)}
.sv.cur{background:#FFF1D6;border-color:var(--gcd)}.sv.pr{background:var(--good);border-color:var(--good);color:#fff}
.svb{gap:.8vw}.svbtn{font-family:var(--fh);font-weight:800;font-size:clamp(15px,2.3vh,24px);background:#fff;border:2.5px solid var(--ink2);color:var(--ink);border-radius:12px;padding:.3em .9em;cursor:pointer}
.svbtn.show{background:var(--good);border-color:var(--good);color:#fff}.svbtn.reset{border-style:dashed}
.cks{display:flex;flex-direction:column;gap:1vh;width:min(1150px,92vw)}
.ck{display:flex;align-items:center;gap:1em;text-align:start;font-family:var(--fb);font-weight:700;font-size:clamp(17px,2.8vh,30px);background:#fff;border:2.5px solid var(--line);border-radius:14px;padding:.8vh 1.2vw;cursor:pointer;color:var(--ink);line-height:1.5}
.ck .cb{flex:none;width:1.7em;height:1.7em;border-radius:50%;border:2.5px solid var(--ink2);display:flex;align-items:center;justify-content:center;font-family:var(--fh);font-size:.8em}
.ck.ok{border-color:var(--good);background:#F2FBF5}.ck.ok .cb{background:var(--good);border-color:var(--good);color:#fff}
.kk{font-family:var(--fh);font-size:clamp(34px,6vh,64px)}
.exit .st>div>span{flex:1}
'''
