# شرائح درس ١-٢ «المضاعفات» — الصف السابع (حصة واحدة، كتاب الطالب ص٢٢–٢٣)
# المراجع: دليل المعلم ص٢٣–٢٤ (النشاط ١: شبكة الضرب)، كتاب الطالب ص٢٢–٢٣، ورقة «درسي في صفحة» ١-٢،
# وإجابات الدليل ص٣٥ (كتاب الطالب) وص٤١–٤٢ (كتاب النشاط ص١٥).
# python3.12 gen_powers.py mult_slides.py المضاعفات_عرض_تفاعلي.html "المضاعفات — الصف السابع"

def L(*xs, hot=()):  # قائمة أعداد مفصولة بفواصل؛ hot = المشتركة (تُحاط بدائرة)
    return '<span class="lst">' + '<i>،</i>'.join(f'<b class="{"cm" if x in hot else ""}">{a(x)}</b>' for x in xs) + '<i>، …</i></span>'
def GRID(rows, cols, shade_r=None, shade_c=None, show=True, given=None):
    head = '<tr><th class="op">×</th>' + ''.join(f'<th>{a(c)}</th>' for c in cols) + '</tr>'
    body = ''
    for r in rows:
        body += f'<tr><th>{a(r)}</th>' + ''.join(
            f'<td class="{"sh" if (r == shade_r or c == shade_c) else ""}{" both" if (r == shade_r and c == shade_c) else ""}">{a(r * c) if (show or (given and (r, c) in given)) else ""}</td>' for c in cols) + '</tr>'
    return f'<table class="otb">{head}{body}</table>'
BOX = '<span class="blank">؟</span>'
MI = '<span class="x">−</span>'
def STP(lab, expr, cls=''): return st(f'<div class="stp {cls}"><span class="lab">{lab}</span>{expr}</div>')
def STEPS(*rows): return '<div class="stps">' + ''.join(rows) + '</div>'
S = []
ME = 'إعداد: أ. عيسى الحارثي'
S.append(slide(f'''<span class="tag">الصف السابع · الدرس ١-٢</span>
<h1 class="h1s">المضاعفات</h1>
<p class="lead">كتاب الطالب ص ٢٢–٢٣</p>
<p class="lead" style="font-size:clamp(26px,4.8vh,56px)">{ME}</p>''', 'cover'))
CAN = ['أكتب <b>مضاعفات</b> عددٍ بالعدّ بالقفز أو بجدول الضرب',
       'أجد المضاعف الذي <b>ترتيبه</b> معلوم (الرابع، السابع عشر…)',
       'أجد <b>المضاعفات المشتركة</b> لعددين',
       'أجد <b>المضاعف المشترك الأصغر (م م ص)</b> وأستخدمه في حلّ المسائل']
S.append(slide(f'''<h2>في نهاية هذا الدرس…</h2>
<div class="can">{''.join(f'<div><span class="can-i">✔</span><span><b>أنا أستطيع</b> أن {t}</span></div>' for t in CAN)}</div>'''))
S.append(slide(f'''<h2>مفردات الدرس</h2>
{st('<div class="vocab wide"><div><span>المضاعف</span><i>multiple</i></div><div><span>المضاعف المشترك</span><i>common multiple</i></div><div><span>المضاعف المشترك الأصغر (م م ص)</span><i>LCM</i></div><div><span>حقائق الضرب</span><i>multiplication facts</i></div></div>')}
<p class="lead">نتعلّم معاً ثم نتدرّب: <b class="c-i">أنا</b> ← <b class="c-we">نحن</b> ← <b class="c-u">أنتم</b></p>'''))
S.append(slide('''<span class="tag">حصة واحدة · ٤٠ دقيقة</span><h2>خطة الحصة</h2>
<div class="plan"><div><b>٥ د</b>تهيئة: شبكة الضرب</div><div><b>٨ د</b>المضاعفات ونمطها</div><div><b>١٠ د</b>أنا ← نحن ← أنتم</div>
<div><b>٧ د</b>م م ص</div><div><b>٧ د</b>ألغاز الكتاب</div><div><b>٣ د</b>بطاقة الخروج</div></div>''', 'divider'))

# النشاط ١ (دليل المعلم ص٢٣–٢٤): شبكة ضرب بصفٍّ وعمودٍ مظلّلين
S.append(slide(f'''<div class="row hdr"><span class="qbadge">نشاط ١ 🔍</span>{ref('دليل المعلم ص ٢٣')}</div><h2>شبكة الضرب: ماذا تلاحظ في المظلّل؟</h2>
<button class="flip box col tbc"><span class="tap">👆 أكمل الشبكة</span>{GRID([3, 6, 4], [2, 4, 7], 6, 4, show=False, given={(3, 2): 6})}<span class="hid col">{GRID([3, 6, 4], [2, 4, 7], 6, 4)}</span></button>
{st('<div class="note">الصف المظلّل: مضاعفات <b>٦</b> — العمود المظلّل: مضاعفات <b>٤</b> — و <b>٢٤</b> مضاعفٌ مشترك لهما</div>')}'''))

S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('كتاب الطالب ص ٢٢')}</div><h2>انظر إلى النمط</h2>
<div class="col" style="gap:2vh">
{st(f'<div class="mrow"><b>مضاعفات العدد ٣</b>{L(3, 6, 9, 12, 15)}</div>')}
{st(f'<div class="mrow"><b>مضاعفات العدد ٧</b>{L(7, 14, 21, 28, 35)}</div>')}
{st(f'<div class="mrow"><b>مضاعفات العدد ٢٥</b>{L(25, 50, 75, 100, 125)}</div>')}</div>
{st('<div class="note">نبدأ <b>بالعدد نفسه</b>، ثم نضيفه في كل مرّة — والنقاط تعني أن النمط يستمر</div>')}'''))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('تمرين ١')}</div><h2>اكتب أوّل ستة مضاعفات للعدد ٧</h2>
{box(STEPS(STP('نبدأ بالعدد نفسه', M('٧', X, '١', EQ, '٧', cls="sm")), STP('نضيف ٧ كل مرّة', L(7, 14, 21, 28, 35, 42), 'fin')))}'''))
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('تمرين ٣ (ب)')}</div><h2>معاً: المضاعف الرابع للعدد ١٢</h2><p class="ask">هل نكتب القائمة كلها… أم نضرب مباشرة؟</p>
{box(STEPS(STP('بالقائمة', L(12, 24, 36, 48)), STP('أسرع: بالضرب', M('١٢', X, '٤', EQ, '٤٨', cls="sm"), 'fin')))}'''))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ٣ (ج)')}{timer(2)}</div>''' + quiz('المضاعف الرابع للعدد ٢١ هو…', [M('٢٥'), M('٨٤'), M('٦٣'), M('١٠٥')], 1, '٢١ × ٤ = ٨٤ — أمّا ٦٣ فهو المضاعف الثالث')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ٥')}</div>''' + quiz('المضاعف السابع عشر للعدد ٨ هو ١٣٦ — فما المضاعف الثامن عشر؟', [M('١٣٧'), M('١٤٤'), M('١٢٨'), M('١٥٢')], 1, 'المضاعف التالي = ١٣٦ + ٨ = ١٤٤ (والسادس عشر = ١٣٦ − ٨ = ١٢٨)')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('مثال ١-٢')}</div><h2>مضاعفات ٦ و ٨ الأصغر من ١٠٠</h2>
<div class="col" style="gap:2vh">
{st(f'<div class="mrow"><b>مضاعفات ٦</b>{L(6, 12, 18, 24, 30, 36, 42, 48, 54, hot=(24, 48))}</div>')}
{st(f'<div class="mrow"><b>مضاعفات ٨</b>{L(8, 16, 24, 32, 40, 48, 56, hot=(24, 48))}</div>')}</div>
{st('<div class="rulebox">المضاعفات المشتركة: ٢٤ ، ٤٨ ، ٧٢ ، ٩٦ — وأصغرها <b class="c-exp">٢٤</b> = المضاعف المشترك الأصغر (م م ص)</div>')}'''))
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('تمرين ٧ (أ)')}</div><h2>معاً: م م ص للعددين ٤ و ٦</h2>
{box(STEPS(STP('مضاعفات ٤', L(4, 8, 12, 16, hot=(12,))), STP('مضاعفات ٦', L(6, 12, 18, hot=(12,))), STP('أوّل مشترك', M('م م ص', EQ, '١٢', cls="sm"), 'fin')))}'''))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ٧ (هـ)')}{timer(2)}</div>''' + quiz('م م ص للعددين ٩ و ١١ هو…', [M('٢٠'), M('٩٩'), M('١٨'), M('١')], 1, 'لا يوجد مضاعف مشترك قبل ٩ × ١١ = ٩٩')))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">انتبه ⚠️</span>{ref('دليل المعلم ص ٢٣')}</div><h2>المضاعفات غير العوامل!</h2>
<div class="row">
{st(box(f'<div class="col"><b class="kk c-we">مضاعفات ٦</b>{L(6, 12, 18, 24)}<small class="hint">أكبر من العدد أو تساويه — ولا تنتهي</small></div>', style="flex:1"))}
{st(box(f'<div class="col"><b class="kk c-exp">عوامل ٦</b><span class="lst"><b>١</b><i>،</i><b>٢</b><i>،</i><b>٣</b><i>،</i><b>٦</b></span><small class="hint">أصغر من العدد أو تساويه — ومحدودة</small></div>', style="flex:1"))}</div>'''))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">فكّر 💡</span>{ref('تمرين ٨')}</div><h2>ضيوف سارة: بين ٥٠ و ١٠٠، يجلسون ٨ أو ١٢ على كل مائدة دون مقعدٍ فارغ</h2>
<button class="flip box col"><span class="tap">👆 الحل</span><span class="hid col">{L(24, 48, 72, 96, hot=(72, 96))}<span class="hint">المضاعفات المشتركة للعددين ٨ و ١٢ بين ٥٠ و ١٠٠</span>{M('٧٢', 'أو', '٩٦', cls="mid")}</span></button>'''))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">فكّر 💡</span>{ref('تمرين ٩')}</div><h2>تتبقى قطعة حلوى واحدة دائماً عند التوزيع على ٢ أو ٣ أو ٤ أو ٥ أو ٦</h2>
<button class="flip box col"><span class="tap">👆 الحل</span><span class="hid col">{M('م م ص', EQ, '٦٠', cls="sm")}<span class="hint">يكفي النظر إلى ٤ و ٥ و ٦ (لأن ٦ مضاعف للعددين ٢ و ٣)</span>{M('٦٠', PL, '١', EQ, '٦١', cls="mid")}</span></button>'''))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج 🎫</span><h2>أجب في دفترك</h2>
<div class="exit">{st('<div><b>١</b>اكتب أوّل أربعة مضاعفات للعدد ٩</div>')}{st('<div><b>٢</b>ما المضاعف الخامس للعدد ٩؟</div>')}{st('<div><b>٣</b>أوجد م م ص للعددين ٣ و ٥</div>')}</div>'''))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج 🎫</span><h2>الإجابات</h2>
<button class="flip box col" style="min-width:40vw"><span class="tap">👆 اضغط لإظهار الإجابات</span><span class="hid col">{L(9, 18, 27, 36)}{M('٤٥', cls="sm")}{M('١٥', cls="sm")}</span></button>'''))
S.append(slide('''<span class="qbadge" style="background:#0A6770;box-shadow:0 4px 0 #05393E">الواجب المنزلي 🏠</span><h2>قبل الحصة القادمة</h2>
<div class="exit"><div class="st"><div><b>١</b>حلّ صفحة ١٥ في كتاب النشاط</div></div><div class="st"><div><b>٢</b>تدرّب على حقائق الضرب حتى ١٠ × ١٠</div></div></div>'''))
S.append(slide(f'''<h2>الخلاصة</h2>
<div class="sumg">
{st(box('<div class="col"><b class="kk c-we">المضاعفات</b><span>نبدأ بالعدد ثم نضيفه</span>' + L(5, 10, 15) + '</div>'))}
{st(box('<div class="col"><b class="kk c-exp">المضاعف رقم ن</b><span>العدد × ن</span>' + M('١٢', X, '٤', EQ, '٤٨') + '</div>'))}
{st(box('<div class="col"><b class="kk c-lcm">م م ص</b><span>أصغر مضاعفٍ مشترك</span>' + M('٤ ، ٦', '←', '١٢') + '</div>'))}</div>'''))

# ═══════════ ملحق: تمارين كتاب الطالب ص٢٢–٢٣ ═══════════
S.append(launch('sb', '٢٢ و ٢٣', note=f'المراجع: كتاب الطالب ص٢٢–٢٣ ودليل المعلم ص٢٣–٢٤ وإجاباته ص٣٥ — {ME}'))
RM = 'نبدأ بالعدد نفسه ثم نضيفه في كل مرّة'
S.append(ex(1, 'اكتب أوّل ستة مضاعفات للعدد ٧', RM, [('مضاعفات ٧', L(7, 14, 21, 28, 35, 42))], cols=1))
S.append(ex(2, 'اكتب أوّل أربعة مضاعفات', RM, [(f'({h}) {a(n)}', L(n, 2 * n, 3 * n, 4 * n)) for h, n in zip(['أ', 'ب', 'ج', 'د', 'هـ'], [5, 9, 10, 30, 11])], cols=2))
S.append(ex(3, 'أوجد المضاعف الرابع', 'المضاعف الرابع = العدد × ٤', [(f'({h}) {a(n)}', M(a(n), X, '٤', EQ, a(4 * n))) for h, n in zip(['أ', 'ب', 'ج', 'د', 'هـ'], [6, 12, 21, 15, 32])], cols=2))
S.append(ex(4, 'العدد ٣٥ مضاعفٌ للعددين ١ و ٣٥ ولعددين آخرين', 'نبحث عن عددين حاصل ضربهما ٣٥', [('العددان', M('٥', X, '٧', EQ, '٣٥') + '<small>العددان: ٥ و ٧</small>')], cols=1))
S.append(ex(5, 'المضاعف السابع عشر للعدد ٨ هو ١٣٦', 'المضاعف التالي: نضيف ٨ — والسابق: نطرح ٨', [('(أ) الثامن عشر', M('١٣٦', PL, '٨', EQ, '١٤٤')), ('(ب) السادس عشر', M('١٣٦', MI, '٨', EQ, '١٢٨'))], cols=2))
S.append(ex(6, 'اكتب أربعة مضاعفات مشتركة', 'المضاعفات المشتركة = مضاعفات م م ص', [('(أ) ٢ و ٣', L(6, 12, 18, 24)), ('(ب) ٤ و ٥', L(20, 40, 60, 80))], cols=2))
S.append(ex(7, 'أوجد م م ص لكل زوج', 'اكتب مضاعفات العددين حتى تجد أوّل مضاعفٍ مشترك', [(f'({h}) {a(x)} و {a(y)}', M(a(r))) for h, (x, y, r) in zip(['أ', 'ب', 'ج', 'د', 'هـ'], [(4, 6, 12), (5, 6, 30), (6, 9, 18), (4, 10, 20), (9, 11, 99)])], cols=2))
S.append(ex(8, 'ضيوف سارة (بين ٥٠ و ١٠٠)', 'مضاعفات مشتركة للعددين ٨ و ١٢', [('عدد الضيوف', M('٧٢', 'أو', '٩٦'))], cols=1))
S.append(ex(9, 'أصغر عدد من قطع الحلوى', 'م م ص للأعداد ٢ ، ٣ ، ٤ ، ٥ ، ٦ ثم نضيف ١', [('العدد', M('٦٠', PL, '١', EQ, '٦١'))], cols=1))

# ═══════════ ملحق: حلول كتاب النشاط ص١٥ (الإجابات من دليل المعلم ص٤١–٤٢) ═══════════
S.append(launch('ab', '١٥', note='الإجابات النهائية من دليل المعلم ص ٤١–٤٢'))
NA = 'نشاط ص ١٥ · تمرين'
S.append(ex(1, 'اكتب أوّل خمسة مضاعفات', RM, [(f'({h}) {a(n)}', L(n, 2 * n, 3 * n, 4 * n, 5 * n)) for h, n in zip(['أ', 'ب', 'ج'], [9, 12, 20])], cols=2, src=NA))
S.append(ex(2, 'أوجد المضاعف المطلوب', 'المضاعف رقم ن = العدد × ن', [('(أ) الرابع للعدد ٦', M('٦', X, '٤', EQ, '٢٤')), ('(ب) السادس للعدد ٤', M('٤', X, '٦', EQ, '٢٤'))], cols=2, src=NA))
S.append(ex(3, 'أكمل من الإطار: ٢٠ ، ٢٦ ، ٣٢ ، ٤٥ ، ٤٤', 'نحسب ثم نختار', [('(أ) الرابع للعدد ٨', M('٣٢')), ('(ب) الثاني للعدد ١٠', M('٢٠')), ('(ج) الرابع للعدد ١١', M('٤٤')), ('(د) مشترك للعددين ٩ و ١٥', M('٤٥'))], cols=2, src=NA))
S.append(ex(4, 'أوجد عدداً بين ٤٠ و ٥٠ يكون', 'نكتب المضاعفات حتى نصل إلى ما بين ٤٠ و ٥٠', [('(أ) مضاعفاً للعدد ٧', M('٤٢', 'أو', '٤٩')), ('(ب) مضاعفاً للعدد ١٢', M('٤٨')), ('(ج) مضاعفاً للعدد ١٤', M('٤٢'))], cols=2, src=NA))
S.append(ex(5, 'المضاعف السادس عشر للعدد ٧ هو ١١٢', 'التالي: نضيف ٧ — والسابق: نطرح ٧', [('(أ) السابع عشر', M('١١٢', PL, '٧', EQ, '١١٩')), ('(ب) الخامس عشر', M('١١٢', '<span class="x">−</span>', '٧', EQ, '١٠٥'))], cols=2, src=NA))
S.append(ex(6, 'أوجد م م ص', 'أوّل مضاعفٍ مشترك', [(f'({h}) {a(x)} و {a(y)}', M(a(r))) for h, (x, y, r) in zip(['أ', 'ب', 'ج', 'د'], [(3, 5, 15), (6, 8, 24), (10, 15, 30), (4, 7, 28)])], cols=2, src=NA))
S.append(ex(7, 'تفاحات مريم تتوزّع بالتساوي على ٣ أو ٤ أو ٥', 'م م ص للأعداد ٣ و ٤ و ٥', [('أصغر عدد', M('٣', X, '٤', X, '٥', EQ, '٦٠'))], cols=1, src=NA))
S.append(ex(8, 'مضاعفات العدد ١٦٧', 'المضاعف رقم ن = ١٦٧ × ن', [('(أ) الثالث', M('١٦٧', X, '٣', EQ, '٥٠١')), ('(ب) السادس والتاسع', M('١٠٠٢', 'و', '١٥٠٣'))], cols=2, src=NA))

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
.rulebox{font-weight:800;font-size:clamp(28px,5.4vh,64px);background:#EAF7F8;border:4px solid var(--base);border-radius:20px;padding:1.4vh 2vw;text-align:center;line-height:1.5}
.otb{border-collapse:collapse;font-family:var(--fh);font-weight:800;font-size:clamp(34px,7.4vh,88px);direction:rtl}
.otb th,.otb td{border:.05em solid var(--ink);min-width:2.3em;height:1.35em;text-align:center;padding:0 .2em}
.otb th{background:#FFF3C4}.otb th.op{background:var(--ink);color:#fff}
.otb td.sh{background:#E4F4F5}.otb td.both{background:#FDE7E3;color:var(--exp)}
.tbc{padding:1.2vh 1.4vw}.tbc.open>.otb{display:none}
.sumg{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:2vw;width:min(1600px,94vw)}
.sumg .col span{font-weight:700;font-size:clamp(28px,5.4vh,64px);line-height:1.4}
.sumg .kk{font-size:clamp(36px,7vh,84px)}.sumg .lst{font-size:clamp(28px,5.4vh,64px)}
'''

# صفحات تمارين كتاب الطالب لشارة «كتاب الطالب ص … · تمرين …» (common_slides.py)
PG = {'تمرين': [(1, '٢٢'), (6, '٢٣')]}
