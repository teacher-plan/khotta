# شرائح درس ٢-٢ «تجميع الحدود المتشابهة» — الصف السابع (حصتان، كتاب الطالب ص٤٣–٤٥)
# المراجع: دليل المعلم ص٤٧–٤٨ (المستطيلات الملوّنة، الأخطاء الشائعة: ٦س + ٤ = ١٠س …، النشاط)، كتاب الطالب ص٤٣–٤٥ (مثال ٢-٢)،
# وإجابات الدليل ص٥٤–٥٥ (كتاب الطالب) وص٥٨–٥٩ (كتاب النشاط ص٢٩–٣١).
# python3.12 gen_powers.py like_slides.py تجميع_الحدود_المتشابهة_عرض_تفاعلي.html "تجميع الحدود المتشابهة — الصف السابع"

def STP(lab, expr, cls=''): return st(f'<div class="stp {cls}"><span class="lab">{lab}</span>{expr}</div>')
def STEPS(*rows): return '<div class="stps">' + ''.join(rows) + '</div>'
MI = '<span class="x">−</span>'
import re as _re
def J(s): return '<span>' + _re.sub(r'(?<=[\u0621-\u064A\u0640])(?=[\u0621-\u063F\u0641-\u064A])', '\u200c<i class="vgap"></i>', s) + '</span>'   # متغيّران متجاوران (سص) يُفصلان فلا يتشابكان كأنهما كلمة
def V(t, c='v'): return f'<span class="{c}">{J(t)}</span>'
def T(k, v, c=None):   # حدّ جبري: المعامل ثم المتغيّر (المعامل ١ لا يُكتب)
    return f'<span class="term">{"" if k in ("", "١", 1) else a(k)}{V(v, c or CL.get(v, "v"))}</span>'
CL = {'س': 'vs', 'ص': 'vp', 'ع': 'vg'}
def BAR(seq, lab=True):   # مستطيلات: س صغير، ص متوسط، ع طويل
    W = {'س': 1, 'ص': 1.6, 'ع': 2.4}
    return '<div class="bars">' + ''.join(f'<span class="b-{CL[c]}" style="flex:{W[c]}">{c if lab else ""}</span>' for c in seq) + '</div>'
def PYR(rows, show=None, cls=''):   # هرم: الصفوف من الأعلى، والخانة = مجموع الخانتين تحتها؛ show: مجموعة (صف، عمود) الظاهرة، والباقي فارغ
    out = ''
    for r, row in enumerate(rows):
        out += '<div class="prow">' + ''.join(
            (f'<span class="pc">{c}</span>' if show is None or (r, k) in show else f'<button class="pc flip hole"><span class="tap">؟</span><span class="hid">{c}</span></button>')
            for k, c in enumerate(row)) + '</div>'
    return f'<div class="pyr2 {cls}">{out}</div>'
S = []
ME = 'إعداد: أ. عيسى الحارثي'
S.append(slide(f'''<span class="tag">الصف السابع · الدرس ٢-٢</span>
<h1 class="h1s">تجميع الحدود المتشابهة</h1>
<p class="lead">كتاب الطالب ص ٤٣ إلى ٤٥ · حصتان</p>
<p class="lead" style="font-size:clamp(26px,4.8vh,56px)">{ME}</p>''', 'cover'))
CAN = ['أتعرّف <b>الحدود المتشابهة</b>', 'أبسّط العبارة الجبرية بـ<b>تجميع الحدود المتشابهة</b> (جمعاً وطرحاً)', 'أكتشف الأخطاء في تبسيط العبارات وأصحّحها']
S.append(slide(f'''<h2>في نهاية هذا الدرس…</h2>
<div class="can">{''.join(f'<div><span class="can-i">✔</span><span><b>أنا أستطيع</b> أن {t}</span></div>' for t in CAN)}</div>'''))
S.append(slide(f'''<h2>مفردات الدرس</h2>
{st('<div class="vocab wide"><div><span>الحدود المتشابهة</span><i>like terms</i></div><div><span>تجميع الحدود المتشابهة</span><i>collecting like terms</i></div><div><span>التبسيط</span><i>simplify</i></div></div>')}
<p class="lead">حصتان: <b class="c-i">أنا</b> ← <b class="c-we">نحن</b> ← <b class="c-u">أنتم</b></p>'''))

# ═══════════ الحصة الأولى: الحدود المتشابهة ═══════════
S.append(slide('''<span class="tag">الحصة الأولى · ٤٠ دقيقة</span><h2>الحدود المتشابهة</h2>
<div class="plan"><div><b>٥ د</b>تهيئة: المستطيلات</div><div><b>١٠ د</b>ما الحدود المتشابهة؟</div><div><b>١٠ د</b>مثال ٢-٢ (أ، ب)</div>
<div><b>٨ د</b>نحن ← أنتم</div><div><b>٤ د</b>انتبه</div><div><b>٣ د</b>بطاقة الخروج</div></div>''', 'divider'))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">تهيئة 🤔</span>{ref('كتاب الطالب ص ٤٣')}</div><h2>مستطيلان: طول البرتقالي س ، وطول الأزرق ص</h2>
<div class="col" style="gap:2.4vh">{st(BAR('س') )}{st(BAR('ص'))}</div>''' + tn('استخدم أشرطة ورقية حقيقية إن أمكن (اقتراح الدليل).')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('كتاب الطالب ص ٤٣')}</div><h2>نجمع أطوال المستطيلات</h2>
<div class="bargrid">{st(f'<div>{BAR("سسس")}{M(T("٣", "س"))}</div>')}{st(f'<div>{BAR("صص")}{M(T("٢", "ص"))}</div>')}{st(f'<div>{BAR("صصسسس")}{M(T("٣", "س"), PL, T("٢", "ص"))}</div>')}</div>'''))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('كتاب الطالب ص ٤٣')}</div><h2>الحدود المتشابهة</h2>
{st('<div class="rulebox">الحدود المتشابهة: حدودٌ تحتوي على <b class="c-exp">المتغيّر نفسه</b></div>')}
<div class="row">{st(box(f'<div class="col"><span class="right">✔ متشابهة</span>{M(T("٢", "س"), "،", T("٣", "س"))}</div>', style="flex:1;border-color:var(--good)"))}{st(box(f'<div class="col"><span class="wrong">✘ غير متشابهة</span>{M(T("٣", "س"), "،", T("٢", "ص"))}</div>', style="flex:1;border-color:var(--bad)"))}</div>'''))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('كتاب الطالب ص ٤٣')}</div><h2>نجمع أو نطرح الحدود المتشابهة فقط</h2>
{st('<div class="rulebox">نجمع المعاملات (الأعداد) ونُبقي المتغيّر كما هو</div>')}
<div class="row">{st(box(M(T("٣", "س"), PL, T("٢", "س"), EQ, T("٥", "س"), cls="mid"), style="flex:1"))}{st(box(M(T("٣", "س"), PL, T("٢", "ص"), cls="mid") + '<small class="hint">لا تُبسَّط أكثر</small>', 'col', style="flex:1"))}</div>'''))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('مثال ٢-٢ (أ، ب)')}</div><h2>بسّط</h2>
{box(STEPS(STP('(أ) ٢س و ٣س متشابهان', M(T('٢', 'س'), PL, T('٣', 'س'), EQ, T('٥', 'س'), cls="sm"), 'fin'), STP('(ب) ٧ص و ٢ص متشابهان', M(T('٧', 'ص'), MI, T('٢', 'ص'), EQ, T('٥', 'ص'), cls="sm"), 'fin')))}'''))
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('تمرين ١')}</div><h2>معاً: اكتب طول الشريط في أبسط صورة</h2>
<div class="bargrid">{st(f'<div>{BAR("سسسس")}<button class="flip fl1"><span class="tap">👆</span><span class="hid">{M(T("٤", "س"))}</span></button></div>')}{st(f'<div>{BAR("صسس")}<button class="flip fl1"><span class="tap">👆</span><span class="hid">{M(T("٢", "س"), PL, T("", "ص"))}</span></button></div>')}{st(f'<div>{BAR("سصسصس")}<button class="flip fl1"><span class="tap">👆</span><span class="hid">{M(T("٣", "س"), PL, T("٢", "ص"))}</span></button></div>')}</div>''' + tn('المستطيل الأصفر س، والأخضر ص، والأزرق ع في كتاب الطالب. الإجابات: ٤س ، ٢س + ص ، ٣س + ٢ص.')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ٢ (أ)')}{timer(2)}</div>''' + quiz(f'بسّط: {M(T("", "س"), PL, T("", "س"), PL, T("", "س"), PL, T("", "س"), PL, T("", "س"))}', [M(T('٥', 'س')), M(T('', 'س'), '<sup>٥</sup>'), M(T('٤', 'س')), M('٥')], 0, 'خمسة حدود متشابهة: ١ + ١ + ١ + ١ + ١ = ٥')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ٢ (هـ)')}</div>''' + quiz(f'بسّط: {M(T("٨", "هـ"), PL, T("٥", "هـ"), PL, T("", "هـ"))}', [M(T('١٣', 'هـ')), M(T('١٤', 'هـ')), M(T('٤٠', 'هـ')), M(T('١٤', 'هـ'), '<sup>٣</sup>')], 1, 'هـ وحدها تعني ١هـ: ٨ + ٥ + ١ = ١٤')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ٢ (ل)')}</div>''' + quiz(f'بسّط: {M(T("٨", "ك"), MI, T("٥", "ك"), MI, T("٢", "ك"))}', [M(T('', 'ك')), M(T('٣', 'ك')), M('٠'), M(T('١٥', 'ك'))], 0, '٨ − ٥ − ٢ = ١ ، ونكتب ١ك على صورة ك')))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">انتبه ⚠️ أخطاء شائعة</span>{ref('دليل المعلم ص ٤٧')}</div><h2>أيّها صحيح؟</h2>
<div class="errs">{''.join(st(f'<button class="flip err"><span class="xq">{M(*q)}</span><span class="tap">👆</span><span class="hid xa no">{w}</span></button>') for q, w in (
  ([T('٦', 'س'), PL, '٤', EQ, T('١٠', 'س')], '✘ خطأ: ٤ ليس حدّاً متشابهاً مع ٦س'), ([T('٦', 'س'), PL, T('٤', 'ص'), EQ, J('١٠سص')], '✘ خطأ: س و ص غير متشابهين'),
  ([T('٦', 'س'), MI, T('', 'س'), EQ, '٦'], '✘ خطأ: ٦س − س = ٥س')))}</div>''' + tn('من الأخطاء الشائعة في الدليل. ارجع إلى المستطيلات: مستطيلان أحمران ومستطيل أزرق لا تعطي ثلاثة مستطيلات من لونٍ واحد.')))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ١ 🎫</span><h2>بسّط</h2>
<div class="exit">{st(f'<div><b>١</b>{M(T("٤", "م"), PL, T("٣", "م"), cls="sm")}</div>')}{st(f'<div><b>٢</b>{M(T("٩", "ر"), MI, T("", "ر"), cls="sm")}</div>')}{st(f'<div><b>٣</b>{M(T("٢", "س"), PL, T("٥", "ص"), PL, T("", "س"), cls="sm")}</div>')}</div>'''))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ١ 🎫</span><h2>الإجابات</h2>
<button class="flip box col" style="min-width:40vw"><span class="tap">👆 اضغط لإظهار الإجابات</span><span class="hid col">{M(T('٧', 'م'), cls="sm")}{M(T('٨', 'ر'), cls="sm")}{M(T('٣', 'س'), PL, T('٥', 'ص'), cls="sm")}</span></button>'''))

# ═══════════ الحصة الثانية: تبسيط عبارات أطول ═══════════
S.append(slide('''<span class="tag">الحصة الثانية · ٤٠ دقيقة</span><h2>تبسيط عبارات أطول</h2>
<div class="plan"><div><b>٥ د</b>إحماء</div><div><b>١٠ د</b>مثال ٢-٢ (ج، د)</div><div><b>٥ د</b>حدود بمتغيّرين</div>
<div><b>٨ د</b>نحن ← أنتم</div><div><b>٧ د</b>هرم الحدود</div><div><b>٥ د</b>اكتشف الخطأ</div></div>''', 'divider'))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">إحماء 🔥</span>{timer(1)}</div>''' + quiz(f'أيّ الحدّين متشابهان؟', [M(T('٣', 'س'), '،', T('٣', 'ص')), M(T('٥', 'ع'), '،', T('', 'ع')), M(T('٢', 'م'), '،', '٢'), M(T('٤', 'ل'), '،', T('٤', 'ك'))], 1, 'المتغيّر نفسه ع في الحدّين')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('مثال ٢-٢ (ج)')}</div><h2>بسّط {M(T('٤', 'ل'), PL, T('٣', 'م'), PL, T('٢', 'ل'), MI, T('', 'م'), cls="sm")}</h2>
{box(STEPS(STP('نرتّب المتشابهة معاً', M(T('٤', 'ل'), PL, T('٢', 'ل'), PL, T('٣', 'م'), MI, T('', 'م'), cls="sm")), STP('نجمع كل نوع', M(T('٦', 'ل'), PL, T('٢', 'م'), cls="sm"), 'fin')))}
{st('<div class="note">الإشارة تنتقل مع الحدّ الذي بعدها: <b>− م</b> تبقى سالبة</div>')}''' + tn('لا يمكن تبسيط ٦ل + ٢م أكثر لأنهما حدّان غير متشابهين.')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('مثال ٢-٢ (د)')}</div><h2>بسّط {M(T('٥', 'ع'), PL, '٧', MI, T('٣', 'ع'), PL, '٣', cls="sm")}</h2>
{box(STEPS(STP('نرتّب', M(T('٥', 'ع'), MI, T('٣', 'ع'), PL, '٧', PL, '٣', cls="sm")), STP('نجمع', M(T('٢', 'ع'), PL, '١٠', cls="sm"), 'fin')))}
{st('<div class="note">الأعداد وحدها حدودٌ متشابهة فيما بينها</div>')}'''))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('تمرين ٥')}</div><h2>حدودٌ فيها متغيّران</h2>
{st(f'<div class="rulebox">{J("سص")} و {J("صس")} حدّان متشابهان، لأنّ س × ص = ص × س</div>')}
{box(STEPS(STP('بسّط', M(T('٢', 'سص'), PL, T('٣', 'صس'), cls="sm")), STP('الناتج', M(T('٥', 'سص'), cls="sm"), 'fin')))}'''))
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('تمرين ٤ (ي)')}</div><h2>معاً: بسّط {M(T('٧', 'ص'), PL, T('٢', 'ح'), PL, T('٣', 'ر'), MI, T('٢', 'ص'), PL, T('', 'ح'), PL, T('٢', 'ر'), cls="sm")}</h2>
<button class="flip box col"><span class="tap">👆 الحل</span><span class="hid col">{M(T('٧', 'ص'), MI, T('٢', 'ص'), PL, T('٢', 'ح'), PL, T('', 'ح'), PL, T('٣', 'ر'), PL, T('٢', 'ر'), cls="sm")}{M(EQ, T('٥', 'ص'), PL, T('٣', 'ح'), PL, T('٥', 'ر'), cls="sm")}</span></button>'''))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ٤ (ز)')}{timer(2)}</div>''' + quiz(f'بسّط: {M(T("١٠", "م"), MI, T("٥", "م"), PL, "١٧", MI, "٩")}', [M(T('٥', 'م'), PL, '٨'), M(T('١٣', 'م')), M(T('٥', 'م'), PL, '٢٦'), M(T('١٥', 'م'), PL, '٨')], 0, '١٠م − ٥م = ٥م ، و ١٧ − ٩ = ٨')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ٥ (ز)')}</div>''' + quiz(f'بسّط: {M(T("٤", "مل"), MI, T("٣", "لم"), PL, T("٧", "طح"), MI, T("٧", "حط"))}', [M(T('', 'مل')), M(T('٧', 'مل')), M(T('', 'مل'), PL, T('١٤', 'طح')), M('٠')], 0, '٤مل − ٣مل = مل ، و ٧طح − ٧طح = ٠')))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">هرم الحدود 🔺</span>{ref('تمرين ٣ (أ)')}</div><h2>كل خانة = مجموع الخانتين تحتها</h2>
{PYR([[T('١٤', 'س')], [T('٨', 'س'), T('٦', 'س')], [T('٣', 'س'), T('٥', 'س'), T('', 'س')]], show={(1, 1), (2, 0), (2, 1), (2, 2)})}''' + tn('٥س + س = ٦س (معطاة في الكتاب)، ثم ٣س + ٥س = ٨س، ثم ٨س + ٦س = ١٤س.')))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">هرم الحدود 🔺</span>{ref('تمرين ٣ (ب)')}</div><h2>نستخدم الطرح لنجد الخانات السفلى</h2>
{PYR([[T('١٢', 'ع')], [T('٨', 'ع'), T('٤', 'ع')], [T('٧', 'ع'), T('', 'ع'), T('٣', 'ع')]], show={(0, 0), (1, 0), (2, 0)})}''' + tn('ابدأ بـ ١٢ع − ٨ع = ٤ع (تلميح الكتاب)، ثم ٨ع − ٧ع = ع، ثم ٤ع − ع = ٣ع.')))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">اكتشف الخطأ 🔍</span>{ref('تمرين ٦')}</div><h2>حلّ أحمد: {M(T('٢', 'س'), PL, '٨', PL, T('٦', 'س'), MI, '٤', EQ, T('٨', 'س'), PL, '٤', EQ, T('١٢', 'س'), cls="sm")}</h2>
<button class="flip box col"><span class="tap">👆 أين الخطأ؟</span><span class="hid col"><span class="kk c-bad">٨س + ٤ لا تُبسَّط إلى ١٢س</span><span class="hint">٨س و ٤ حدّان غير متشابهين، والإجابة الصحيحة ٨س + ٤</span></span></button>'''))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ٢ 🎫</span><h2>بسّط</h2>
<div class="exit">{st(f'<div><b>١</b>{M(T("٣", "س"), PL, "٥", PL, T("٤", "س"), MI, "٢", cls="sm")}</div>')}{st(f'<div><b>٢</b>{M(T("٦", "ك"), PL, T("٢", "و"), MI, T("٤", "ك"), PL, T("", "و"), cls="sm")}</div>')}{st(f'<div><b>٣</b>{M(T("٣", "سص"), PL, T("٢", "صس"), cls="sm")}</div>')}</div>'''))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ٢ 🎫</span><h2>الإجابات</h2>
<button class="flip box col" style="min-width:40vw"><span class="tap">👆 اضغط لإظهار الإجابات</span><span class="hid col">{M(T('٧', 'س'), PL, '٣', cls="sm")}{M(T('٢', 'ك'), PL, T('٣', 'و'), cls="sm")}{M(T('٥', 'سص'), cls="sm")}</span></button>'''))
S.append(slide('''<span class="qbadge" style="background:#0A6770;box-shadow:0 4px 0 #05393E">الواجب المنزلي 🏠</span><h2>بعد الحصتين</h2>
<div class="exit"><div class="st"><div><b>١</b>صفحتا ٢٩ و ٣٠ في كتاب النشاط</div></div><div class="st"><div><b>٢</b>صفحة ٣١ في كتاب النشاط (اكتشف الخطأ والهرم)</div></div></div>'''))
S.append(slide(f'''<h2>الخلاصة</h2>
<div class="sumg">
{st(box('<div class="col"><b class="kk c-we">متشابهة</b><span>المتغيّر نفسه</span>' + M(T('٢', 'س'), '،', T('٥', 'س')) + '</div>'))}
{st(box('<div class="col"><b class="kk c-exp">نجمع المعاملات</b><span>والمتغيّر كما هو</span>' + M(T('٣', 'س'), PL, T('٢', 'س'), EQ, T('٥', 'س')) + '</div>'))}
{st(box('<div class="col"><b class="kk c-lcm">غير المتشابهة</b><span>تبقى كما هي</span>' + M(T('٣', 'س'), PL, T('٢', 'ص')) + '</div>'))}</div>'''))

# ═══════════ ملحق: تمارين كتاب الطالب ص٤٤–٤٥ (الإجابات من دليل المعلم ص٥٤–٥٥) ═══════════
S.append(launch('sb', '٤٤ و ٤٥', note=f'المراجع: كتاب الطالب ص٤٣ إلى ٤٥، ودليل المعلم ص٤٧ و ٤٨ وإجاباته ص٥٤ و ٥٥ · {ME}'))
H = ['أ', 'ب', 'ج', 'د', 'هـ', 'و', 'ز', 'ح', 'ط', 'ي', 'ك', 'ل']
RL = 'نجمع أو نطرح الحدود المتشابهة فقط، ونُبقي المتغيّر كما هو'
def P(*t): return M(*t)
S.append(ex(1, 'مجموع أطوال المستطيلات (س أصفر، ص أخضر، ع أزرق)', RL, [('(أ)', P(T('٤', 'س'))), ('(ب)', P(T('٣', 'ص'))), ('(ج)', P(T('٢', 'س'), PL, T('', 'ص'))),
  ('(د)', P(T('٢', 'س'), PL, T('٢', 'ع'))), ('(هـ)', P(T('٣', 'س'), PL, T('٢', 'ص'))), ('(و)', P(T('', 'ص'), PL, T('٢', 'ع')))], cols=2))
A2 = [T('٥', 'س'), T('٦', 'ص'), T('٨', 'د'), T('١٣', 'ر'), T('١٤', 'هـ'), T('١٦', 'ع'), T('٣', 'ل'), T('٧', 'ع'), T('٤', 'ح'), T('٥', 'و'), T('٣', 'م'), T('', 'ك')]
Q2 = ['س + س + س + س + س', '٢ص + ٤ص', '٥د + ٣د', '٦ر + ٣ر + ٤ر', '٨هـ + ٥هـ + هـ', '٩ع + ع + ٦ع', '٧ل − ٤ل', '٨ع − ع', '٩ح − ٥ح', '٦و + ٢و − ٣و', '٩م + م − ٧م', '٨ك − ٥ك − ٢ك']
S.append(ex(2, 'بسّط', RL, [(f'({h}) {q}', P(x)) for h, q, x in zip(H, Q2, A2)], cols=2))
S.append(ex(3, 'اكتب الحدود المفقودة في الهرم', 'الخانة = مجموع الخانتين تحتها، ونطرح لنجد المفقود', [
  ('(أ)', PYR([[T('١٤', 'س')], [T('٨', 'س'), T('٦', 'س')], [T('٣', 'س'), T('٥', 'س'), T('', 'س')]], cls='sm')),
  ('(ب)', PYR([[T('١٢', 'ع')], [T('٨', 'ع'), T('٤', 'ع')], [T('٧', 'ع'), T('', 'ع'), T('٣', 'ع')]], cls='sm'))], cols=2))
Q4 = ['٢ل + ٣ل + ٥ك', '٣ر + ٥ر + ٢د + د', '٤س + ٥ص + ٣س + ٢ص', '٧ح + ٨ل + ٢ح + ل', '٤ر + ١ + ٣ر + ٩', '٦م − ٢م + ٧ع − ٣ع',
      '١٠م − ٥م + ١٧ − ٩', '٦ر + ٣ط − ٤ر + ط', '٩ك + ٥و − ٣ك − ٢و', '٧ص + ٢ح + ٣ر − ٢ص + ح + ٢ر', '١١م + ٦ط + ٩ − ٣ط − ٧', '١٢ + ٦ح + ٨ك − ٦ − ٣ح + ٣ك']
A4 = [(T('٥', 'ل'), PL, T('٥', 'ك')), (T('٨', 'ر'), PL, T('٣', 'د')), (T('٧', 'س'), PL, T('٧', 'ص')), (T('٩', 'ح'), PL, T('٩', 'ل')), (T('٧', 'ر'), PL, '١٠'), (T('٤', 'م'), PL, T('٤', 'ع')),
      (T('٥', 'م'), PL, '٨'), (T('٢', 'ر'), PL, T('٤', 'ط')), (T('٦', 'ك'), PL, T('٣', 'و')), (T('٥', 'ص'), PL, T('٣', 'ح'), PL, T('٥', 'ر')), (T('١١', 'م'), PL, T('٣', 'ط'), PL, '٢'), ('٦', PL, T('٣', 'ح'), PL, T('١١', 'ك'))]
S.append(ex(4, 'بسّط بتجميع الحدود المتشابهة', 'نرتّب المتشابهة معاً، والإشارة تنتقل مع حدّها', [(f'({h}) {q}', P(*x)) for h, q, x in zip(H, Q4, A4)], cols=2, per=2))
Q5 = ['٢سص + ٣سص + ٥عم + ٧مع', '٣كر + ٥كر + ٩عل + ٧لع', '٤طل + ٢لط + ٦ود − ٤دو', '١١صر + ٩طح − ٢صر − ٧حط', '٨حد + ١٢حهـ + ٣دح − ٩هـح', '٦س + ٧سص − ٢س + سص', '٤مل − ٣لم + ٧طح − ٧حط']
Q5 = [J(q) for q in Q5]
A5 = [(T('٥', 'سص'), PL, T('١٢', 'عم')), (T('٨', 'كر'), PL, T('١٦', 'عل')), (T('٦', 'لط'), PL, T('٢', 'ود')), (T('٩', 'صر'), PL, T('٢', 'طح')), (T('١١', 'حد'), PL, T('٣', 'حهـ')), (T('٤', 'س'), PL, T('٨', 'سص')), (T('', 'مل'),)]
S.append(ex(5, 'اكتب في أبسط صورة', J('سص') + ' و ' + J('صس') + ' متشابهان', [(f'({h}) {q}', P(*x)) for h, q, x in zip(H, Q5, A5)], cols=2, per=2))
S.append(ex(6, 'هل إجابة أحمد صحيحة؟', 'لا نجمع إلا الحدود المتشابهة', [('(أ) ٨س + ٤ = ١٢س', 'خطأ: ٨س و ٤ غير متشابهين، والصحيح ' + P(T('٨', 'س'), PL, '٤')),
  ('(ب) ٥هـو + ٥هـد + ٣دهـ', 'جمع ٢هـو بدل طرحه، ولم يجمع ٥هـد مع ٣دهـ؛ والصحيح ' + P(T('', 'هـو'), PL, T('٨', 'هـد')))], cols=1, per=1))
S.append(ex(7, 'أكمل الفراغات في الهرم', 'نطرح من الخانة العليا لنجد الخانة المفقودة', [('الحل', PYR([['١٢ح + ١١د'], ['٥ح + ٨د', '٧ح + ٣د'], ['٢ح + ٦د', '٣ح + ٢د', '٤ح + د'], ['٢ح + ٤د', '٢د', '٣ح', 'ح + د']], cls='sm'))], cols=1))

# ═══════════ ملحق: حلول كتاب النشاط ص٢٩–٣١ (الإجابات من دليل المعلم ص٥٨–٥٩) ═══════════
S.append(launch('ab', '٢٩ إلى ٣١', note='الإجابات النهائية من دليل المعلم ص ٥٨ و ٥٩'))
NA, NB, NC = 'نشاط ص ٢٩ · تمرين', 'نشاط ص ٣٠ · تمرين', 'نشاط ص ٣١ · تمرين'
S.append(ex(1, 'اكتب عبارةً تعبّر عن المستطيلات', RL, [('(أ)', P(T('٣', 'س'))), ('(ب)', P(T('٢', 'ع'))), ('(ج)', P(T('٢', 'س'), PL, T('', 'ص'))),
  ('(د)', P(T('٢', 'ع'), PL, T('', 'س'))), ('(هـ)', P(T('٣', 'س'), PL, T('٢', 'ص'))), ('(و)', P(T('٢', 'س'), PL, T('٢', 'ص'), PL, T('', 'ع')))], cols=2, src=NA))
QA2 = ['م + م + م + م', '٤ح + ٣ح', '٤ر + ٧ر', '٢د + ٣د + ٤د', '٦هـ + ٦هـ + هـ', '١٠و + و + ٤و', '٩ل − ٣ل', '٤ح − ٣ح', '٩ط − ط', '٨م + ٢م − ٤م', 'ك + ٦ك − ٣ك', '١٢ص − ٤ص − ٧ص']
AA2 = [T('٤', 'م'), T('٧', 'ح'), T('١١', 'ر'), T('٩', 'د'), T('١٣', 'هـ'), T('١٥', 'و'), T('٦', 'ل'), T('', 'ح'), T('٨', 'ط'), T('٦', 'م'), T('٤', 'ك'), T('', 'ص')]
S.append(ex(2, 'اكتب في أبسط صورة', RL, [(f'({h}) {q}', P(x)) for h, q, x in zip(H, QA2, AA2)], cols=2, src=NA))
S.append(ex(3, 'أكمل الهرمين', 'الخانة = مجموع الخانتين تحتها', [
  ('(أ)', PYR([[T('١٨', 'س')], [T('١٠', 'س'), T('٨', 'س')], [T('٣', 'س'), T('٧', 'س'), T('', 'س')]], cls='sm')),
  ('(ب)', PYR([[T('١٥', 'س')], [T('٨', 'س'), T('٧', 'س')], [T('٥', 'س'), T('٣', 'س'), T('٤', 'س')]], cls='sm'))], cols=2, src=NB))
QA4 = ['٣س + ٤س + ٥ص', '٥ع + ٥ع + ٥ر + ر', '٣ر + ٤م + ٤ر + ٥م', '٤س + ٥ + ٣س + ٢', 'د + ١ + د + ١', '٥و − ٣و + ١٢ط − ٣ط', '٤٥ − ١٥ + ١٢و − و',
       '٧س + ٥ص − ٣س + ص', '٨ر + ٦م − ٤ر − ٥م', '٤و + ٣س + ٧ص − ٢و − ٣س + ١٣ص', '٢٠٠ر + ٢٠ط + ١٠٠ − ١٥ط − ٧٠']
AA4 = [(T('٧', 'س'), PL, T('٥', 'ص')), (T('١٠', 'ع'), PL, T('٦', 'ر')), (T('٧', 'ر'), PL, T('٩', 'م')), (T('٧', 'س'), PL, '٧'), (T('٢', 'د'), PL, '٢'), (T('٢', 'و'), PL, T('٩', 'ط')),
       ('٣٠', PL, T('١١', 'و')), (T('٤', 'س'), PL, T('٦', 'ص')), (T('٤', 'ر'), PL, T('', 'م')), (T('٢', 'و'), PL, T('٢٠', 'ص')), (T('٢٠٠', 'ر'), PL, T('٥', 'ط'), PL, '٣٠')]
S.append(ex(4, 'بسّط بتجميع الحدود المتشابهة', 'نرتّب المتشابهة معاً، والإشارة تنتقل مع حدّها', [(f'({h}) {q}', P(*x)) for h, q, x in zip(H, QA4, AA4)], cols=2, src=NB, per=2))
QA5 = ['٤رم + ٢رم + ٣سص + ٥سص', '٣صد + ٣صد + ٥رح + ٦رح', '٥رط + ٦رط + ٩وك − ٥كو', '٨هـو + ٧دح − ٣وهـ − ٤حد', '٥ح + ١٥صح − ٢ح + حص', '٧سم − ٤مس + ١١هـو − ١١وهـ']
QA5 = [J(q) for q in QA5]
AA5 = [(T('٦', 'رم'), PL, T('٨', 'سص')), (T('٦', 'صد'), PL, T('١١', 'رح')), (T('١١', 'رط'), PL, T('٤', 'كو')), (T('٥', 'هـو'), PL, T('٣', 'دح')), (T('٣', 'ح'), PL, T('١٦', 'صح')), (T('٣', 'سم'),)]
S.append(ex(5, 'اكتب في أبسط صورة', 'رم و مر متشابهان', [(f'({h}) {q}', P(*x)) for h, q, x in zip(H, QA5, AA5)], cols=2, src=NB, per=2))
S.append(ex(6, 'ما الذي أخطأ فيه منير؟', 'لا نجمع إلا الحدود المتشابهة', [('(أ)', 'جمع حدوداً غير متشابهة: ٢س + ٨ ليست ١٠س'), ('(ب)', 'ظنّ ٤ر − ر = ٤ والصحيح ٣ر، وظنّ ٥صد و ٢دص غير متشابهين')], cols=1, src=NC))
S.append(ex(7, 'أكمل الفراغات في الهرم', 'نطرح من الخانة العليا لنجد الخانة المفقودة', [('الحل', PYR([['١٧س + ١١ص'], ['٩س + ٥ص', '٨س + ٦ص'], ['٤س + ٣ص', '٥س + ٢ص', '٣س + ٤ص'], ['٢س + ٢ص', '٢س + ص', '٣س + ص', '٣ص']], cls='sm'))], cols=1, src=NC))

EXTRA_CSS_OWN = '''
.v{color:var(--exp);font-weight:900}.vs{color:#D9480F;font-weight:900}.vp{color:#1C6DD0;font-weight:900}.vg{color:#12824C;font-weight:900}
.term{display:inline-flex;direction:rtl;unicode-bidi:isolate}
.stps{display:flex;flex-direction:column;gap:1.6vh;align-items:stretch}
.stp{display:flex;align-items:center;gap:1.6vw;justify-content:space-between}
.stp .lab{flex:none;font-family:var(--fh);font-weight:800;color:#2563EB;background:#EAF1FF;border-radius:12px;padding:.2em .8em;text-align:center}
.stp.fin .lab{background:var(--good);color:#fff}
.rulebox{font-weight:800;font-size:clamp(28px,5.4vh,64px);background:#EAF7F8;border:4px solid var(--base);border-radius:20px;padding:1.2vh 2vw;text-align:center;line-height:1.5}
.box .col>.m:not(.mid):not(.sm):not(.big),.hid.col>.m:not(.mid):not(.sm):not(.big){font-size:clamp(34px,6.4vh,76px)}
.bars{display:flex;gap:3px;width:min(900px,62vw);direction:rtl}
.bars span{height:clamp(34px,6.4vh,72px);border-radius:8px;display:flex;align-items:center;justify-content:center;font-family:var(--fh);font-weight:900;color:#fff;font-size:clamp(22px,4.2vh,48px)}
.b-vs{background:#F08C3C}.b-vp{background:#3D86E0}.b-vg{background:#2FA56B}
.bargrid{display:flex;flex-direction:column;gap:2vh;align-items:center}
.bargrid .st>div{display:flex;align-items:center;gap:2vw}
.bargrid .m{font-size:clamp(34px,6.4vh,76px)}
.fl1{min-width:12vw;background:#fff;border:3px dashed var(--line);border-radius:14px;padding:.2em .6em;font-size:clamp(34px,6.4vh,76px)}
.errs{display:flex;flex-direction:column;gap:1.4vh;width:min(1300px,90vw)}
.err{display:flex;align-items:center;justify-content:space-between;gap:2vw;background:#fff;border:3px solid var(--line);border-radius:16px;padding:.8vh 1.6vw;font-size:clamp(30px,5.8vh,68px)}
.err .xa{font-size:clamp(22px,4.2vh,48px)}
.pyr2{display:flex;flex-direction:column;align-items:center;gap:6px;direction:rtl}
.prow{display:flex;gap:6px}
.pc{font-family:var(--fh);font-weight:900;font-size:clamp(28px,5.6vh,66px);min-width:3.4em;padding:.15em .4em;text-align:center;background:#EAF7EE;border:3px solid #9CD3B0;border-radius:10px;color:var(--ink)}
.pyr2 button.pc.hole,.pyr2 button.pc.hole .hid,.pyr2 button.pc.hole .tap{font-size:clamp(28px,5.6vh,66px)}.pc.hole{background:#fff;border-style:dashed;cursor:pointer}.pc.hole .tap{color:var(--exp)}
.pyr2.sm .pc{font-size:clamp(20px,4.2vh,46px);min-width:2.8em}
.xa .pyr2 .pc{background:#fff}
.sumg{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:2vw;width:min(1600px,94vw)}
.sumg .col span{font-weight:700;font-size:clamp(26px,4.6vh,56px);line-height:1.4}
.sumg .kk{font-size:clamp(34px,6.4vh,76px)}
'''

# صفحات تمارين كتاب الطالب لشارة «كتاب الطالب ص … · تمرين …» (common_slides.py)
PG = {'تمرين': [(1, '٤٤'), (4, 'ز', '٤٥')]}
