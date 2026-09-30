# شرائح درس ١-٥ «الأسس» — الصف السابع (حصتان، كتاب الطالب ص٣٠–٣١)
# المراجع: دليل المعلم ص٢٩–٣٠ (نشاط شجرة عوامل العدد ٤٥٠ بطريقتين، الأخطاء الشائعة: ١ في الشجرة والخلط بين ع م ك و م م ص)،
# كتاب الطالب ص٣٠–٣١ (مثال ١-٥)، ورقة «درسي في صفحة» ١-٥، وإجابات الدليل ص٣٧ (كتاب الطالب) وص٤٣ (كتاب النشاط ص٢٠–٢٢).
# python3.12 gen_powers.py index_slides.py الأسس_عرض_تفاعلي.html "الأسس — الصف السابع"

def STP(lab, expr, cls=''): return st(f'<div class="stp {cls}"><span class="lab">{lab}</span>{expr}</div>')
def STEPS(*rows): return '<div class="stps">' + ''.join(rows) + '</div>'
PR = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
def FAC(n):
    f, d = {}, 2
    while n > 1:
        while n % d == 0: f[d] = f.get(d, 0) + 1; n //= d
        d += 1
    return f
def PF(f):  # أجزاء ناتج الضرب بالصورة الأسية مرتّبةً تصاعدياً (تُقرأ من اليمين)
    out = []
    for p in sorted(f):
        if out: out.append(X)
        out.append(P(p, f[p] if f[p] > 1 else None))
    return out
def PFM(n, cls=''): return M(a(n), EQ, *PF(FAC(n)), cls=cls)
def val(f):
    v = 1
    for p, e in f.items(): v *= p ** e
    return v

def TREE(t, cls=''):
    """شجرة عوامل من صفوف متداخلة: (العدد، الفرع الأيسر، الفرع الأيمن) أو عددٌ أولي في نهاية فرع."""
    U, V, pos, items = 100, 120, {}, []
    leaves = [0]
    def lay(n, d):
        if isinstance(n, tuple):
            xl = lay(n[1], d + 1); xr = lay(n[2], d + 1); x = (xl + xr) / 2
            items.append(('n', n[0], x, d)); items.append(('l', x, d, xl)); items.append(('l', x, d, xr))
            return x
        x = leaves[0] * U + U / 2; leaves[0] += 1
        items.append(('p', n, x, d)); return x
    lay(t, 0)
    D = max(i[3] for i in items if i[0] in 'np') + 1
    W, H = leaves[0] * U, D * V
    svg = []
    for it in items:
        if it[0] == 'l':
            _, x, d, xc = it; svg.append(f'<line x1="{x}" y1="{d * V + 78}" x2="{xc}" y2="{(d + 1) * V + 22}"/>')
    for it in items:
        if it[0] in 'np':
            k, n, x, d = it; y = d * V + 60
            if k == 'p': svg.append(f'<circle cx="{x}" cy="{y - 4}" r="38"/>')
            svg.append(f'<text x="{x}" y="{y + 14}">{a(n)}</text>')
    return f'<svg class="ftree {cls}" viewBox="0 0 {W} {H}" style="aspect-ratio:{W}/{H}">{"".join(svg)}</svg>'

def PT(rows, primes):
    """جدول الأسس: عمود لكل عامل أولي (٢ يميناً) وصفّ لكل عدد."""
    head = '<tr><th></th>' + ''.join(f'<th>{a(p)}</th>' for p in primes) + '</tr>'
    body = ''
    for lab, f, cls in rows:
        body += f'<tr class="{cls}"><th>{lab}</th>' + ''.join(f'<td>{M(P(p, f[p] if f[p] > 1 else None), cls="sm") if f.get(p) else "—"}</td>' for p in primes) + '</tr>'
    return f'<table class="ptab">{head}{body}</table>'

S = []
ME = 'إعداد: أ. عيسى الحارثي'
S.append(slide(f'''<span class="tag">الصف السابع · الدرس ١-٥</span>
<h1 class="h1s">الأسس</h1>
<p class="lead">كتاب الطالب ص ٣٠–٣١ · حصتان</p>
<p class="lead" style="font-size:clamp(26px,4.8vh,56px)">{ME}</p>''', 'cover'))
CAN = ['أرسم <b>شجرة العوامل</b> لأكتب العدد في صورة ناتج ضرب عوامله الأولية', 'أستخدم <b>الأسس</b> لاختصار العوامل المتكررة',
       'أجد <b>م م ص</b> و<b>ع م ك</b> لعددين باستخدام عواملهما الأولية']
S.append(slide(f'''<h2>في نهاية هذا الدرس…</h2>
<div class="can">{''.join(f'<div><span class="can-i">✔</span><span><b>أنا أستطيع</b> أن {t}</span></div>' for t in CAN)}</div>'''))
S.append(slide(f'''<h2>مفردات الدرس</h2>
{st('<div class="vocab wide"><div><span>شجرة العوامل</span><i>factor tree</i></div><div><span>الأُسّ</span><i>index</i></div><div><span>الأسس</span><i>indices</i></div><div><span>المضاعف المشترك الأصغر (م م ص)</span><i>LCM</i></div></div>')}
<p class="lead">حصتان: <b class="c-i">أنا</b> ← <b class="c-we">نحن</b> ← <b class="c-u">أنتم</b></p>'''))

# ═══════════ الحصة الأولى: شجرة العوامل والأسس ═══════════
S.append(slide('''<span class="tag">الحصة الأولى · ٤٠ دقيقة</span><h2>شجرة العوامل والأسس</h2>
<div class="plan"><div><b>٥ د</b>تهيئة</div><div><b>١٠ د</b>شجرة العوامل</div><div><b>٥ د</b>الأُسّ</div>
<div><b>٨ د</b>نشاط: ٤٥٠ بطريقتين</div><div><b>٩ د</b>نحن ← أنتم</div><div><b>٣ د</b>بطاقة الخروج</div></div>''', 'divider'))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">تهيئة 🤔</span>{timer(1)}</div>''' + quiz('ما ناتج ٢ × ٢ × ٢ × ٣ ؟', [M('٢٤'), M('١٨'), M('١٢'), M('٣٦')], 0, '٢ × ٢ × ٢ = ٨ ، و ٨ × ٣ = ٢٤')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('كتاب الطالب ص ٣٠')}</div><h2>كل عددٍ غير أولي = ناتج ضرب أعدادٍ أولية</h2>
{st(box('<div class="col">' + M('٨٤', EQ, '٢', X, '٢', X, '٣', X, '٧') + M('٤٥', EQ, '٣', X, '٣', X, '٥') + M('١٩٦', EQ, '٢', X, '٢', X, '٧', X, '٧') + '</div>'))}
{st('<div class="note">كيف نجدها بسهولة؟ ← نرسم <b>شجرة العوامل</b></div>')}'''))
SV = ['ارسم فرعين لعددين حاصل ضربهما ١٢٠ ، مثل <em class="kb">١٠</em> و <em class="kb">١٢</em>',
      'كرّر مع كل عدد: ١٢ = ٣ × ٤ و ١٠ = ٢ × ٥ ، ثم ٤ = ٢ × ٢',
      'توقّف عند العدد الأولي وضع حوله <em class="kb">دائرة</em>',
      'اضرب الأعداد الموجودة في نهايات الفروع']
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('كتاب الطالب ص ٣٠')}</div><h2>شجرة العوامل للعدد ١٢٠</h2>
<div class="row" style="align-items:center;gap:3vw;flex-wrap:nowrap">{st(TREE((120, (10, 5, 2), (12, (4, 2, 2), 3))))}
<div class="exit sm" style="width:52vw">{''.join(st(f'<div><b>{a(k + 1)}</b><span>{t}</span></div>') for k, t in enumerate(SV))}</div></div>'''))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('كتاب الطالب ص ٣٠')}</div><h2>شجرةٌ أخرى للعدد ١٢٠ … والنتيجة نفسها!</h2>
<div class="row" style="align-items:center;gap:4vw">{st(TREE((120, (60, (30, (6, 3, 2), 5), 2), 2)))}
{st(box('<div class="col">' + M('١٢٠', EQ, '٢', X, '٢', X, '٢', X, '٣', X, '٥') + '<span class="hint">أعداد نهايات الفروع هي نفسها مهما رسمنا الشجرة</span></div>'))}</div>'''))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('كتاب الطالب ص ٣٠')}</div><h2>الأُسّ: اختصارٌ للعامل المتكرّر</h2>
<div class="row">{st(box('<div class="col">' + M(P(2, 3), EQ, '٢', X, '٢', X, '٢', cls="mid") + '<span class="kk">تُقرأ: ٢ أُسّ ٣</span></div>', style="flex:1"))}
{st(box('<div class="col"><span class="kk"><b class="c-we">٢</b> الأساس</span><span class="kk"><b class="c-exp">٣</b> الأُسّ</span><span class="hint">العدد الصغير المكتوب أعلى يسار الأساس</span></div>', style="flex:1"))}</div>
{st('<div class="rulebox">' + M('١٢٠', EQ, P(2, 3), X, '٣', X, '٥') + '</div>')}'''))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">نشاط 🌳</span>{ref('دليل المعلم ص ٢٩–٣٠')}</div><h2>العدد ٤٥٠ بشجرتين مختلفتين</h2>
<div class="row" style="gap:5vw;align-items:flex-end">{st(TREE((450, (10, 2, 5), (45, 5, (9, 3, 3)))))}{st(TREE((450, (45, (15, 5, 3), 3), (10, 5, 2))))}</div>
{st('<div class="rulebox">' + M('٤٥٠', EQ, '٢', X, P(3, 2), X, P(5, 2)) + '</div>')}'''))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">انتبه ⚠️ خطأ شائع</span>{ref('دليل المعلم ص ٢٩')}</div><h2>العدد ١ لا يظهر في شجرة العوامل</h2>
<div class="row">
{st(box(f'<div class="col"><span class="wrong">✘</span>{TREE((2, 1, 2), "sm")}<small class="hint">١ ليس عدداً أولياً</small></div>', style="flex:1;border-color:var(--bad);background:#FFF5F5"))}
{st(box('<div class="col"><span class="right">✔</span><span class="kk">نتوقّف عند العدد الأولي ٢</span><small class="hint">كل فرعٍ ينتهي بعددٍ أولي</small></div>', style="flex:1;border-color:var(--good);background:#F2FBF5"))}</div>'''))
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('تمرين ٤ (أ)')}</div><h2>معاً: اكتب ٢٤ في صورة ناتج ضرب عوامله الأولية</h2>
<div class="row" style="align-items:center;gap:4vw">{st(TREE((24, (6, 3, 2), (4, 2, 2))))}
{box(STEPS(STP('نهايات الفروع', M('٢', X, '٢', X, '٢', X, '٣', cls="sm")), STP('بالأسس', M('٢٤', EQ, P(2, 3), X, '٣', cls="sm"), 'fin')))}</div>'''))
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('تمرين ٤ (ج)')}</div><h2>معاً: العدد ٧٢</h2>
<div class="row" style="align-items:center;gap:4vw">{st(TREE((72, (8, (4, 2, 2), 2), (9, 3, 3))))}
{box(STEPS(STP('نهايات الفروع', M('٢', X, '٢', X, '٢', X, '٣', X, '٣', cls="sm")), STP('بالأسس', M('٧٢', EQ, P(2, 3), X, P(3, 2), cls="sm"), 'fin')))}</div>'''))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ٤ (ب)')}{timer(2)}</div>''' + quiz('العدد ٥٠ في صورة ناتج ضرب عوامله الأولية:', [M('٢', X, P(5, 2)), M(P(2, 2), X, '٥'), M('٥', X, '١٠'), M('٢', X, '٢٥')], 0, '٥٠ = ٢ × ٥ × ٥')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ٣ (ب)')}</div>''' + quiz(f'ما العدد الذي يمثّله {M("٢", X, P(3, 3))} ؟', [M('١٨'), M('٥٤'), M('٣٦'), M('٢٧')], 1, '٣ × ٣ × ٣ = ٢٧ ، و ٢٧ × ٢ = ٥٤')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ٢')}</div>''' + quiz('أيّها يساوي ١٨٠ ؟', [M(P(2, 2), X, P(3, 2), X, '٥'), M(P(2, 3), X, '٣', X, '٥'), M('٢', X, P(3, 2), X, '٥'), M(P(2, 2), X, P(3, 3))], 0, '٤ × ٩ × ٥ = ١٨٠')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ٣ (ج)')}</div>''' + quiz(f'{M("٣", X, P(11, 2))} = ؟', [M('٦٦'), M('٣٦٣'), M('١٢١'), M('٣٣٣')], 1, '١١ × ١١ = ١٢١ ، و ١٢١ × ٣ = ٣٦٣')))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ١ 🎫</span><h2>أجب في دفترك</h2>
<div class="exit">{st('<div><b>١</b>ارسم شجرة العوامل للعدد ٣٦</div>')}{st('<div><b>٢</b>اكتب ٢٠٠ في صورة ناتج ضرب عوامله الأولية بالأسس</div>')}{st(f'<div><b>٣</b>ما قيمة {M(P(2, 4), X, "٣", cls="sm")} ؟</div>')}</div>'''))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ١ 🎫</span><h2>الإجابات</h2>
<button class="flip box col" style="min-width:40vw"><span class="tap">👆 اضغط لإظهار الإجابات</span><span class="hid col">{PFM(36, "sm")}{PFM(200, "sm")}{M('٤٨', cls="sm")}</span></button>'''))

# ═══════════ الحصة الثانية: م م ص و ع م ك بالعوامل الأولية ═══════════
S.append(slide('''<span class="tag">الحصة الثانية · ٤٠ دقيقة</span><h2>م م ص و ع م ك بالعوامل الأولية</h2>
<div class="plan"><div><b>٥ د</b>إحماء</div><div><b>١٢ د</b>مثال ١-٥</div><div><b>٨ د</b>نحن معاً</div>
<div><b>٧ د</b>أنتم</div><div><b>٥ د</b>فكّر</div><div><b>٣ د</b>بطاقة الخروج</div></div>''', 'divider'))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">إحماء 🔥</span>{timer(1)}</div>''' + quiz('العدد ٦٠ في صورة ناتج ضرب عوامله الأولية:', [M(P(2, 2), X, '٣', X, '٥'), M('٢', X, '٣', X, '١٠'), M(P(2, 3), X, '٥'), M('٤', X, '١٥')], 0, '٦٠ = ٢ × ٢ × ٣ × ٥')))
F60, F75 = FAC(60), FAC(75)
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('مثال ١-٥')}</div><h2>أوجد م م ص و ع م ك للعددين ٦٠ ، ٧٥</h2><p class="ask">الخطوة ١: نكتب كلا العددين في صورة ناتج ضرب عوامله الأولية</p>
{st(box('<div class="col">' + PFM(60) + PFM(75) + '</div>'))}'''))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('مثال ١-٥')}</div><h2>نرتّب العوامل في جدول</h2>
{st(PT([('٦٠', F60, ''), ('٧٥', F75, '')], [2, 3, 5]))}
<div class="row">{st('<div class="rulebox lcm">م م ص: نأخذ <b>الأُسّ الأكبر</b> لكل عامل</div>')}{st('<div class="rulebox hcf">ع م ك: نأخذ <b>الأُسّ الأصغر</b> للعوامل المشتركة فقط</div>')}</div>'''))
LCM = {p: max(F60.get(p, 0), F75.get(p, 0)) for p in (2, 3, 5)}
HCF = {p: min(F60[p], F75[p]) for p in (3, 5)}
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('مثال ١-٥')}</div><h2>م م ص و ع م ك للعددين ٦٠ ، ٧٥</h2>
{PT([('٦٠', F60, ''), ('٧٥', F75, ''), ('م م ص', LCM, 'st lcm'), ('ع م ك', HCF, 'st hcf')], [2, 3, 5])}
<div class="row">{st(M('م م ص', EQ, P(2, 2), X, '٣', X, P(5, 2), EQ, '٣٠٠', cls="sm c-lcm"))}{st(M('ع م ك', EQ, '٣', X, '٥', EQ, '١٥', cls="sm c-hcf"))}</div>'''))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">انتبه ⚠️ خطأ شائع</span>{ref('دليل المعلم ص ٢٩')}</div><h2>لا تخلط بين م م ص و ع م ك</h2>
<div class="row">
{st(box('<div class="col"><b class="kk c-lcm">م م ص</b><span class="kk">كل العوامل · الأُسّ الأكبر</span><span class="hint">الناتج مضاعفٌ لكلا العددين ← أكبر منهما أو يساوي أكبرهما</span></div>', style="flex:1"))}
{st(box('<div class="col"><b class="kk c-hcf">ع م ك</b><span class="kk">المشتركة فقط · الأُسّ الأصغر</span><span class="hint">الناتج عاملٌ لكلا العددين ← أصغر منهما أو يساوي أصغرهما</span></div>', style="flex:1"))}</div>
{st('<div class="note">تحقّق: ٣٠٠ ÷ ٦٠ = ٥ و ٣٠٠ ÷ ٧٥ = ٤ ✔ — و ٦٠ ÷ ١٥ = ٤ و ٧٥ ÷ ١٥ = ٥ ✔</div>')}'''))
F45 = FAC(45)
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('تمرين ٥')}</div><h2>معاً: م م ص و ع م ك للعددين ٤٥ ، ٧٥</h2>
{st(PT([('٤٥', F45, ''), ('٧٥', F75, '')], [3, 5]))}
{box(STEPS(STP('م م ص', M(P(3, 2), X, P(5, 2), EQ, '٢٢٥', cls="sm"), 'fin'), STP('ع م ك', M('٣', X, '٥', EQ, '١٥', cls="sm"), 'fin')))}'''))
F90, F140 = FAC(90), FAC(140)
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('تمرين ٦')}</div><h2>معاً: العددان ٩٠ ، ١٤٠</h2>
{st(PT([('٩٠', F90, ''), ('١٤٠', F140, '')], [2, 3, 5, 7]))}
<div class="note">٣ و ٧ ليسا مشتركين ← لا يدخلان في ع م ك</div>'''))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ٦ (ب)')}{timer(2)}</div>''' + quiz('م م ص للعددين ٩٠ ، ١٤٠ هو…', [M('١٢٦٠'), M('٦٣٠'), M('١٢٦٠٠'), M('٢٥٢٠')], 0, '٢² × ٣² × ٥ × ٧ = ٤ × ٩ × ٣٥ = ١٢٦٠')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ٦ (ج)')}</div>''' + quiz('ع م ك للعددين ٩٠ ، ١٤٠ هو…', [M('٥'), M('١٠'), M('٢٠'), M('٣٠')], 1, 'العاملان المشتركان ٢ و ٥ بالأُسّ الأصغر: ٢ × ٥ = ١٠')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('نشاط ص ٢٠ · تمرين ٤')}</div><h2>{M('٨٤', EQ, P(2, 2), X, '٣', X, '٧')} و {M('٩٠', EQ, '٢', X, P(3, 2), X, '٥')}</h2>
<div class="row">
<button class="flip box col" style="flex:1"><span class="tap">👆 ع م ك</span><span class="hid col">{M('٢', X, '٣', EQ, '٦', cls="sm")}</span></button>
<button class="flip box col" style="flex:1"><span class="tap">👆 م م ص</span><span class="hid col">{M(P(2, 2), X, P(3, 2), X, '٥', X, '٧', cls="sm")}{M(EQ, '١٢٦٠', cls="sm")}</span></button></div>'''))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">فكّر 💡</span>{ref('تمرين ٧')}</div><h2>٣٧ و ٤٧ عددان أوّليّان. ما ع م ك؟ وما م م ص؟</h2>
<div class="row">
<button class="flip box col" style="flex:1"><span class="tap">👆 ع م ك</span><span class="hid col">{M('١', cls="mid")}<span class="hint">لا عوامل أولية مشتركة</span></span></button>
<button class="flip box col" style="flex:1"><span class="tap">👆 م م ص</span><span class="hid col">{M('٣٧', X, '٤٧', EQ, '١٧٣٩', cls="sm")}<span class="hint">نضرب العددين</span></span></button></div>'''))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ٢ 🎫</span><h2>أجب في دفترك</h2>
<div class="exit">{st(f'<div><b>١</b>{M("٢٤", EQ, P(2, 3), X, "٣", cls="sm")} و {M("٣٦", EQ, P(2, 2), X, P(3, 2), cls="sm")}</div>')}{st('<div><b>٢</b>أوجد ع م ك للعددين ٢٤ ، ٣٦</div>')}{st('<div><b>٣</b>أوجد م م ص للعددين ٢٤ ، ٣٦</div>')}</div>'''))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ٢ 🎫</span><h2>الإجابات</h2>
<button class="flip box col" style="min-width:40vw"><span class="tap">👆 اضغط لإظهار الإجابات</span><span class="hid col">{M('ع م ك', EQ, P(2, 2), X, '٣', EQ, '١٢', cls="sm")}{M('م م ص', EQ, P(2, 3), X, P(3, 2), EQ, '٧٢', cls="sm")}</span></button>'''))
S.append(slide('''<span class="qbadge" style="background:#0A6770;box-shadow:0 4px 0 #05393E">الواجب المنزلي 🏠</span><h2>بعد الحصتين</h2>
<div class="exit"><div class="st"><div><b>١</b>صفحة ٢٠ في كتاب النشاط (شجرة العوامل والأسس)</div></div><div class="st"><div><b>٢</b>صفحتا ٢١ و ٢٢ في كتاب النشاط (م م ص و ع م ك)</div></div></div>'''))
S.append(slide(f'''<h2>الخلاصة</h2>
<div class="sumg">
{st(box('<div class="col"><b class="kk c-we">شجرة العوامل</b><span>نتوقّف عند الأعداد الأولية</span><span>١ لا يظهر فيها</span></div>'))}
{st(box('<div class="col"><b class="kk c-exp">الأُسّ</b>' + M(P(2, 3), EQ, '٢ × ٢ × ٢', cls="sm") + '<span>١٢٠ = ٢³ × ٣ × ٥</span></div>'))}
{st(box('<div class="col"><b class="kk c-lcm">م م ص · ع م ك</b><span>م م ص: الأُسّ الأكبر لكل عامل</span><span>ع م ك: الأُسّ الأصغر للمشترك</span></div>'))}</div>'''))

# ═══════════ ملحق: تمارين كتاب الطالب ص٣١ ═══════════
S.append(slide(f'''<span class="tag">ملحق · للمراجعة وتصحيح الواجب</span><h2>تمارين كتاب الطالب ص ٣١</h2>
<p class="lead">اضغط على الجزء ليظهر حلّه</p>
<p class="hint">المراجع: كتاب الطالب ص٣٠–٣١ ودليل المعلم ص٢٩–٣٠ وإجاباته ص٣٧ — {ME}</p>''', 'divider'))
RT = 'نرسم شجرة العوامل ونكتب نهايات الفروع بالأسس'
RL = 'م م ص: الأُسّ الأكبر لكل عامل · ع م ك: الأُسّ الأصغر للمشترك'
H = ['أ', 'ب', 'ج', 'د', 'هـ', 'و', 'ز', 'ح']
S.append(ex(1, 'أكمل أشجار العوامل واكتب كل عدد بالعوامل الأولية', RT, [(f'({h}) {a(n)}', PFM(n)) for h, n in zip(H, [48, 100, 108])], cols=2,
          note='(أ) و (ب): توجد طرقٌ مختلفة لإكمال الشجرة، والعوامل الأولية في النهاية هي نفسها'))
S.append(ex(2, 'صِل كل عدد بعوامله الأولية', RT, [(a(n), PFM(n)) for n in (20, 24, 42, 50, 180)], cols=2))
S.append(ex(3, 'ما العدد الذي تمثّله العمليات؟', 'نفكّ الأسس ثم نضرب', [(f'({h}) ' + M(*PF(f), cls="sm"), M(a(val(f)))) for h, f in zip(H, [{2: 2, 3: 1, 5: 1}, {2: 1, 3: 3}, {3: 1, 11: 2}, {2: 3, 7: 2}, {2: 4, 3: 2}, {5: 2, 13: 1}])], cols=2))
S.append(ex(4, 'اكتب في صورة ناتج ضرب العوامل الأولية', RT, [(f'({h}) {a(n)}', PFM(n)) for h, n in zip(H, [24, 50, 72, 200, 165, 136])], cols=2))
S.append(ex(5, 'العددان ٤٥ ، ٧٥', RL, [('(أ)(١) ٤٥', PFM(45)), ('(أ)(٢) ٧٥', PFM(75)), ('(ب) م م ص', M('٢٢٥')), ('(ج) ع م ك', M('١٥'))], cols=2))
S.append(ex(6, 'العددان ٩٠ ، ١٤٠', RL, [('(أ)(١) ٩٠', PFM(90)), ('(أ)(٢) ١٤٠', PFM(140)), ('(ب) م م ص', M('١٢٦٠')), ('(ج) ع م ك', M('١٠'))], cols=2))
S.append(ex(7, '٣٧ و ٤٧ عددان أوّليّان', 'لا عوامل مشتركة غير ١', [('(أ) ع م ك', M('١')), ('(ب) م م ص', M('٣٧', X, '٤٧', EQ, '١٧٣٩'))], cols=2))

# ═══════════ ملحق: حلول كتاب النشاط ص٢٠–٢٢ (الإجابات من دليل المعلم ص٤٣) ═══════════
S.append(slide('''<span class="tag">ملحق · تصحيح الواجب</span><h2>حلول كتاب النشاط ص ٢٠–٢٢</h2>
<p class="lead">اضغط على الجزء ليظهر حلّه</p>
<p class="hint">الإجابات النهائية من دليل المعلم ص ٤٣</p>''', 'divider'))
NA, NB, NC = 'نشاط ص ٢٠ · تمرين', 'نشاط ص ٢١ · تمرين', 'نشاط ص ٢٢ · تمرين'
S.append(ex(1, 'أكمل شجرة العوامل', RT, [('(أ) ٨٨ = ١١ × ٨', PFM(88)), ('(ب) ١٣٥ = ١٥ × ٩', PFM(135)), ('(ج) ٢٦٠ = ١٠ × ٢٦', PFM(260))], cols=2, src=NA))
S.append(ex(2, 'شجرتا عوامل مختلفتان للعدد ٨٠', RT, [('(أ) نهايات الفروع دائماً', M('٢ ، ٢ ، ٢ ، ٢ ، ٥')), ('(ب) بالعوامل الأولية', PFM(80))], cols=2, src=NA))
S.append(ex(3, 'أوجد الناتج', 'نفكّ الأسس ثم نضرب', [(f'({h}) ' + M(*PF(f), cls="sm"), M(a(val(f)))) for h, f in zip(H, [{2: 1, 3: 2, 5: 2}, {2: 4, 3: 3}, {2: 2, 11: 2}])], cols=2, src=NA))
S.append(ex(4, '٨٤ = ٢² × ٣ × ٧ ، ٩٠ = ٢ × ٣² × ٥', RL, [('(أ) ع م ك', M('٢', X, '٣')), ('(ب) م م ص', M(P(2, 2), X, P(3, 2), X, '٥', X, '٧'))], cols=2, src=NA))
S.append(ex(5, 'العددان ١٢٠ ، ١٦٠', RL, [('(أ)(١) ١٢٠', PFM(120)), ('(أ)(٢) ١٦٠', PFM(160)), ('(ب) م م ص', M('٤٨٠')), ('(ج) ع م ك', M('٤٠'))], cols=2, src=NB))
S.append(ex(6, 'العددان ٨٤ ، ٩٦', RL, [('(أ) ع م ك', M('١٢')), ('(ب) م م ص', M('٦٧٢'))], cols=2, src=NB))
S.append(ex(7, 'العددان ١٠٤ ، ١٥٦', RL, [('(أ) ع م ك', M('٥٢')), ('(ب) م م ص', M('٣١٢'))], cols=2, src=NB))
S.append(ex(8, '١٠ = ٢ × ٥ ، ١٠٠ = ٢² × ٥² ، ١٠٠٠ = ٢³ × ٥³', 'لاحظ النمط', [('١٠٠٠٠', M('١٠٠٠٠', EQ, P(2, 4), X, P(5, 4)))], cols=1, src=NB))
S.append(ex(9, 'حسن: «أفكّر في عددين أوّليّين»', 'عوامل كلٍّ منهما: ١ ونفسه', [('(أ) ع م ك', 'العامل المشترك الوحيد هو ١'), ('(ب) م م ص', 'نضرب العددين الأوّليّين')], cols=2, src=NC))
S.append(ex(10, 'العددان ٨١ ، ١٥٤', RT, [('(أ) ٨١', PFM(81)), ('(ب) ١٥٤', PFM(154)), ('(ج) لماذا ع م ك = ١ ؟', 'لا توجد عوامل أولية مشتركة')], cols=2, src=NC))

EXTRA_CSS_OWN = '''
.stps{display:flex;flex-direction:column;gap:1.6vh;align-items:stretch}
.stp{display:flex;align-items:center;gap:1.4vw;justify-content:space-between}
.stp .lab{flex:none;font-family:var(--fh);font-weight:800;color:#2563EB;background:#EAF1FF;border-radius:12px;padding:.2em .8em;text-align:center}
.stp.fin .lab{background:var(--good);color:#fff}.stp.fin .m{color:var(--good)}
.rulebox{font-weight:800;font-size:clamp(28px,5.4vh,64px);background:#EAF7F8;border:4px solid var(--base);border-radius:20px;padding:1.2vh 2vw;text-align:center;line-height:1.5}
.rulebox.lcm{border-color:#7A3FD1;background:#F3ECFD}.rulebox.hcf{border-color:#C7361B;background:#FDECE8}
.slide .b sup{font-size:max(.62em,4.3vh)}
.c-lcm{color:#7A3FD1}.c-hcf{color:#C7361B}
.box .col>.m:not(.mid):not(.sm):not(.big),.hid.col>.m:not(.mid):not(.sm):not(.big){font-size:clamp(34px,6.4vh,76px)}
.exit .kb{font-style:normal;color:var(--exp);font-weight:900}
.exit.sm>div>div{font-size:clamp(22px,4.2vh,48px);padding:.6vh 1vw}
.ftree{height:min(50vh,600px);width:auto;max-width:44vw}.ftree.sm{height:26vh}
.ftree text{font-family:var(--fh);font-weight:900;font-size:52px;text-anchor:middle;fill:var(--ink)}
.ftree line{stroke:#4A5E80;stroke-width:5;stroke-linecap:round}.ftree circle{fill:#FFF1D6;stroke:var(--exp);stroke-width:5}
.ptab{border-collapse:separate;border-spacing:.8vh;direction:rtl}
.ptab th,.ptab td{font-family:var(--fh);font-weight:900;font-size:clamp(28px,5.4vh,64px);text-align:center;padding:.2vh 1.6vw;border-radius:14px}
.ptab tr:first-child th{background:#EAF1FF;color:#2563EB}.ptab td{background:#fff;border:3px solid var(--line);color:var(--ink2)}
.ptab tr>th:first-child{color:var(--ink);text-align:right}
.ptab tr.lcm td{border-color:#7A3FD1;background:#F3ECFD;color:#7A3FD1}.ptab tr.lcm th{color:#7A3FD1}
.ptab tr.hcf td{border-color:#C7361B;background:#FDECE8;color:#C7361B}.ptab tr.hcf th{color:#C7361B}
.ptab .m.sm{font-size:1em;color:inherit}
.sumg{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:2vw;width:min(1600px,94vw)}
.sumg .col span{font-weight:700;font-size:clamp(26px,4.6vh,56px);line-height:1.4}
.sumg .kk{font-size:clamp(34px,6.4vh,76px)}
'''
