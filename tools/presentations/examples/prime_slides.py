# شرائح درس ١-٤ «الأعداد الأولية» — الصف السابع (٣ حصص، كتاب الطالب ص٢٨–٢٩)
# المراجع: دليل المعلم ص٢٧–٢٨ (غربال إراتوستينس مع ورقة المصادر ١-٤، الأخطاء الشائعة: ١ و ٩١)، كتاب الطالب ص٢٨–٢٩،
# ورقة «درسي في صفحة» ١-٤، وإجابات الدليل ص٣٦–٣٧ (كتاب الطالب) وص٤٢ (كتاب النشاط ص١٨–١٩).
# python3.12 gen_powers.py prime_slides.py الأعداد_الأولية_عرض_تفاعلي.html "الأعداد الأولية — الصف السابع"

def STP(lab, expr, cls=''): return st(f'<div class="stp {cls}"><span class="lab">{lab}</span>{expr}</div>')
def STEPS(*rows): return '<div class="stps">' + ''.join(rows) + '</div>'
def L(*xs, hot=()):
    return '<span class="lst">' + '<i>،</i>'.join(f'<b class="{"cm" if x in hot else ""}">{a(x)}</b>' for x in xs) + '</span>'
PRIMES = [p for p in range(2, 101) if all(p % d for d in range(2, int(p ** .5) + 1))]
def PF(n): return [p for p in PRIMES if n % p == 0]
S = []
ME = 'إعداد: أ. عيسى الحارثي'
S.append(slide(f'''<span class="tag">الصف السابع · الدرس ١-٤</span>
<h1 class="h1s">الأعداد الأوليّة</h1>
<p class="lead">كتاب الطالب ص ٢٨–٢٩ · ثلاث حصص</p>
<p class="lead" style="font-size:clamp(26px,4.8vh,56px)">{ME}</p>''', 'cover'))
CAN = ['أتعرّف <b>العدد الأولي</b>: له عاملان فقط هما ١ والعدد نفسه', 'أستخدم <b>غربال إراتوستينس</b> لإيجاد الأعداد الأولية حتى ١٠٠',
       'أجد <b>العوامل الأولية</b> لعدد', 'أكتب العدد في صورة <b>ناتج ضرب</b> أو <b>مجموع</b> أعدادٍ أولية']
S.append(slide(f'''<h2>في نهاية هذا الدرس…</h2>
<div class="can">{''.join(f'<div><span class="can-i">✔</span><span><b>أنا أستطيع</b> أن {t}</span></div>' for t in CAN)}</div>'''))
S.append(slide(f'''<h2>مفردات الدرس</h2>
{st('<div class="vocab wide"><div><span>العدد الأولي</span><i>prime number</i></div><div><span>غربال إراتوستينس</span><i>sieve of Eratosthenes</i></div><div><span>ناتج الضرب</span><i>product</i></div><div><span>العامل الأولي</span><i>prime factor</i></div></div>')}
<p class="lead">ثلاث حصص: <b class="c-i">أنا</b> ← <b class="c-we">نحن</b> ← <b class="c-u">أنتم</b></p>'''))

# ═══════════ الحصة الأولى: ما العدد الأولي؟ ═══════════
S.append(slide('''<span class="tag">الحصة الأولى · ٤٠ دقيقة</span><h2>ما العدد الأولي؟</h2>
<div class="plan"><div><b>٥ د</b>تهيئة: عوامل ١١ و ٢٣</div><div><b>٨ د</b>تعريف العدد الأولي</div><div><b>١٢ د</b>أنا ← نحن ← أنتم</div>
<div><b>٧ د</b>انتبه: خطآن شائعان</div><div><b>٥ د</b>فكّر</div><div><b>٣ د</b>بطاقة الخروج</div></div>''', 'divider'))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">تهيئة 🤔</span>{timer(1)}</div>''' + quiz('ما عوامل العدد ١١ ؟', ['١ ، ١١', '١ ، ٢ ، ١١', '١١ فقط', '١ ، ٣ ، ١١'], 0, 'له عاملان فقط: ١ والعدد نفسه')))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">تهيئة 🤔</span>{ref('كتاب الطالب ص ٢٨')}</div><h2>بعض الأعداد لها عاملان فقط!</h2>
<div class="col" style="gap:2vh">
{st(f'<div class="mrow"><b>عوامل ١١</b>{L(1, 11)}</div>')}
{st(f'<div class="mrow"><b>عوامل ٢٣</b>{L(1, 23)}</div>')}
{st(f'<div class="mrow"><b>عوامل ١٢</b>{L(1, 2, 3, 4, 6, 12)}</div>')}</div>
{st('<div class="note">١١ و ٢٣ لكلٍّ منهما عاملان فقط — أمّا ١٢ فله ستة عوامل</div>')}'''))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('كتاب الطالب ص ٢٨')}</div><h2>العدد الأولي</h2>
{st('<div class="rulebox">العدد الأولي: عددٌ له <b class="c-exp">عاملان فقط</b> هما ١ والعدد نفسه</div>')}
{st('<div class="note">إذا كان للعدد عواملُ أخرى فإنه <b>ليس</b> عدداً أولياً</div>')}'''))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('كتاب الطالب ص ٢٨')}</div><h2>أوليّ أم لا؟</h2>
<div class="row">
{st(box(f'<div class="col"><b class="kk">٧</b>{L(1, 7)}<span class="right">✔ أولي</span></div>', style="flex:1;border-color:var(--good)"))}
{st(box(f'<div class="col"><b class="kk">٩</b>{L(1, 3, 9)}<span class="wrong">✘ ليس أولياً</span></div>', style="flex:1;border-color:var(--bad)"))}
{st(box(f'<div class="col"><b class="kk">١٥</b>{M("٣", X, "٥", EQ, "١٥", cls="sm")}<span class="wrong">✘ ليس أولياً</span></div>', style="flex:1;border-color:var(--bad)"))}</div>'''))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('كتاب الطالب ص ٢٨')}</div><h2>الأعداد الأولية الأصغر من ٢٠</h2>
{st(f'<div class="pchips">{"".join(f"<b>{a(p)}</b>" for p in PRIMES if p < 20)}</div>')}
{st('<div class="note">ثمانية أعداد — وكلّها <b>فردية</b> ما عدا العدد <b class="c-exp">٢</b>: العدد الأولي الزوجي الوحيد</div>')}'''))
S.append(slide(f'''<div class="row hdr">{mode('we')}</div><h2>معاً: هل ٢١ عددٌ أولي؟</h2><p class="ask">نبحث عن عاملٍ غير ١ و ٢١</p>
{box(STEPS(STP('على ٢؟', M('٢١ فردي', '←', 'لا', cls="sm"), 'bad'), STP('على ٣؟', M('٢', PL, '١', EQ, '٣', '←', 'نعم', cls="sm")), STP('النتيجة', M('٢١', EQ, '٣', X, '٧', '←', 'ليس أولياً', cls="sm"), 'fin')))}'''))
S.append(slide(f'''<div class="row hdr">{mode('we')}</div><h2>معاً: هل ٢٩ عددٌ أولي؟</h2>
{box(STEPS(STP('على ٢ ، ٣ ، ٥؟', M('لا', cls="sm"), 'bad'), STP('على ٧؟', M('٧', X, '٤', EQ, '٢٨', '←', 'لا', cls="sm"), 'bad'), STP('النتيجة', M('١ ، ٢٩', '←', 'أولي', cls="sm"), 'fin')))}'''))
S.append(slide(f'''<div class="row hdr">{mode('u')}{timer(2)}</div>''' + quiz('أيّ هذه الأعداد أولي؟', [M('٢٧'), M('٣١'), M('٣٣'), M('٣٩')], 1, '٢٧ = ٣ × ٩ ، ٣٣ = ٣ × ١١ ، ٣٩ = ٣ × ١٣')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ١')}</div>''' + quiz('العددان الأوليّان بين ٢٠ و ٣٠ هما…', ['٢١ ، ٢٣', '٢٣ ، ٢٩', '٢٣ ، ٢٧', '٢٥ ، ٢٩'], 1, '٢١ = ٣ × ٧ ، ٢٥ = ٥ × ٥ ، ٢٧ = ٣ × ٩')))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">انتبه ⚠️ خطأ شائع</span>{ref('دليل المعلم ص ٢٧')}</div><h2>هل العدد ١ عددٌ أولي؟</h2>
<div class="row">
{st(box('<div class="col"><span class="wrong">✘</span><span class="kk">١ عددٌ أولي</span></div>', style="flex:1;border-color:var(--bad);background:#FFF5F5"))}
{st(box('<div class="col"><span class="right">✔</span><span class="kk">١ ليس أولياً</span><span class="hint">له عاملٌ واحد فقط</span></div>', style="flex:1;border-color:var(--good);background:#F2FBF5"))}</div>
{st('<div class="note">العدد الأولي له <b>عاملان مختلفان</b> دائماً</div>')}'''))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">انتبه ⚠️ خطأ شائع</span>{ref('دليل المعلم ص ٢٧')}</div><h2>هل ٩١ عددٌ أولي؟</h2>
<button class="flip box col"><span class="tap">👆 تحقّق</span><span class="hid col">{M('٩١', EQ, '٧', X, '١٣', cls="mid")}<span class="wrong">✘ ليس أولياً</span><span class="hint">جرّب القسمة على ٧ قبل أن تحكم!</span></span></button>'''))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">فكّر 💡</span>{ref('نشاط ص ١٨ · تمرين ٤')}</div><h2>لماذا لا يمكن أن يكون العدد الأولي مربّعاً؟</h2>
<button class="flip box col"><span class="tap">👆 الحل</span><span class="hid col">{M('٤٩', EQ, '٧', X, '٧', cls="mid")}<span class="kk">للمربّع عاملٌ آخر هو جذره، والعدد الأولي له عاملان فقط</span></span></button>'''))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ١ 🎫</span><h2>أجب في دفترك</h2>
<div class="exit">{st('<div><b>١</b>ما تعريف العدد الأولي؟</div>')}{st('<div><b>٢</b>هل ٥١ عددٌ أولي؟ لماذا؟</div>')}{st('<div><b>٣</b>ما العدد الأولي الزوجي الوحيد؟</div>')}</div>'''))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ١ 🎫</span><h2>الإجابات</h2>
<button class="flip box col" style="min-width:40vw"><span class="tap">👆 اضغط لإظهار الإجابات</span><span class="hid col"><span class="kk">له عاملان فقط: ١ ونفسه</span><span class="kk">لا — ٥١ = ٣ × ١٧</span>{M('٢', cls="sm")}</span></button>'''))

# ═══════════ الحصة الثانية: غربال إراتوستينس ═══════════
S.append(slide('''<span class="tag">الحصة الثانية · ٤٠ دقيقة</span><h2>غربال إراتوستينس</h2>
<div class="plan"><div><b>٥ د</b>إحماء</div><div><b>٥ د</b>خطوات الغربال</div><div><b>١٥ د</b>نشاط: الغربال حتى ١٠٠</div>
<div><b>١٠ د</b>أنتم: أسئلة</div><div><b>٥ د</b>بطاقة الخروج</div></div>''', 'divider'))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">إحماء 🔥</span>{timer(1)}</div>''' + quiz('كم عدداً أولياً أصغر من ٢٠ ؟', [M('٧'), M('٨'), M('٩'), M('١٠')], 1, '٢ ، ٣ ، ٥ ، ٧ ، ١١ ، ١٣ ، ١٧ ، ١٩')))
SV = ['اكتب الأعداد حتى <em class="kb">١٠٠</em>، واشطب العدد <em class="kb">١</em>',
      'ضع مربّعاً حول <em class="kb">٢</em>، ثم اشطب كل مضاعفاته: ٤ ، ٦ ، ٨ …',
      'ضع مربّعاً حول <em class="kb">٣</em>، ثم اشطب مضاعفاته التي لم تُشطب: ٩ ، ١٥ …',
      'استمرّ مع <em class="kb">٥</em> ثم <em class="kb">٧</em> — ما يبقى هو الأعداد الأولية']
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('كتاب الطالب ص ٢٨')}</div><h2>خطوات غربال إراتوستينس</h2>
<div class="exit">{''.join(st(f'<div><b>{a(k + 1)}</b><span>{t}</span></div>') for k, t in enumerate(SV))}</div>'''))
cells = ''.join(f'<button class="sv{" one" if n == 1 else ""}" data-n="{n}">{a(n)}</button>' for n in range(1, 101))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">نشاط 🧮</span>{ref('ورقة المصادر ١-٤')}</div>
<div class="sieve s100" id="sieve">{cells}</div>
<div class="row svb">{''.join(f'<button class="svbtn" data-p="{p}">مضاعفات {a(p)}</button>' for p in (2, 3, 5, 7))}<button class="svbtn show">الأعداد الأولية</button><button class="svbtn reset">↺</button></div>
<script>(function(){{var g=document.getElementById('sieve');
g.parentNode.querySelectorAll('.svbtn').forEach(function(b){{b.addEventListener('click',function(e){{e.stopPropagation();
 var cs=g.querySelectorAll('.sv');
 if(b.classList.contains('reset')){{cs.forEach(function(c){{c.classList.remove('out','pr','cur');}});return;}}
 if(b.classList.contains('show')){{cs.forEach(function(c){{if(!c.classList.contains('out')&&c.dataset.n!=='1')c.classList.add('pr');}});return;}}
 var p=+b.dataset.p;cs.forEach(function(c){{var n=+c.dataset.n;c.classList.remove('cur');if(n===p)c.classList.add('cur');else if(n%p===0)c.classList.add('out');}});
}});}});}})();</script>''', 'sievesl'))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('دليل المعلم ص ٢٧')}</div><h2>الأعداد الأولية الأصغر من ١٠٠: ٢٥ عدداً</h2>
{st(f'<div class="pchips p25">{"".join(f"<b>{a(p)}</b>" for p in PRIMES)}</div>')}
{st('<div class="note">لماذا نتوقّف عند ٧؟ لأن ١١ × ١١ = ١٢١ أكبر من ١٠٠</div>')}'''))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">هل تعلم؟ 🌍</span>{ref('كتاب الطالب ص ٢٨')}</div><h2>الأعداد الأولية لا تنتهي</h2>
<div class="row">{st(box('<div class="col"><b class="kk c-we">إراتوستينس</b><span class="hint">وُلد عام ٢٧٦ قبل الميلاد في ليبيا الحديثة، وأوّل من حسب محيط الأرض</span></div>', style="flex:1"))}{st(box('<div class="col"><b class="kk c-exp">🔒 التشفير</b><span class="hint">الأعداد الأولية الكبيرة تحمي بطاقات الائتمان على الإنترنت</span></div>', style="flex:1"))}</div>'''))
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('تمرين ٢')}</div><h2>معاً: الأعداد الأولية بين ٣٠ و ٤٠</h2>
{box(STEPS(STP('نشطب', L(32, 33, 34, 35, 36, 38, 39), 'bad'), STP('يبقى', L(31, 37), 'fin'), STP('عددها', M('٢', cls="sm"), 'fin')))}'''))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ٣')}{timer(2)}</div>''' + quiz('كم عدداً أولياً بين ٩٠ و ١٠٠ ؟', [M('٠'), M('١'), M('٢'), M('٣')], 1, 'العدد الوحيد هو ٩٧')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('نشاط ص ١٨ · تمرين ٢')}</div>''' + quiz('ما العدد الأولي الخامس عشر؟', [M('٤٣'), M('٤٧'), M('٥٣'), M('٤١')], 1, 'عُدّ في القائمة: ٢ ، ٣ ، ٥ ، … ، ٤٣ ، ٤٧')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('نشاط ص ١٨ · تمرين ٣')}</div>''' + quiz('الأعداد الأولية بين ٨٠ و ٩٠:', ['٨١ ، ٨٣', '٨٣ ، ٨٩', '٨٣ ، ٨٧', '٨٣ فقط'], 1, '٨١ = ٩ × ٩ ، ٨٧ = ٣ × ٢٩')))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">فكّر 💡</span>{ref('تمرين ٥')}</div><h2>خمسة أعداد متتالية ليس بينها عددٌ أولي</h2>
<button class="flip box col"><span class="tap">👆 مثال من الدليل</span><span class="hid col">{L(24, 25, 26, 27, 28)}<span class="hint">وسبعة أعداد؟ نعم: ٩٠ ، ٩١ ، … ، ٩٦</span></span></button>'''))
ROWS6 = [list(range(r * 6 + 1, r * 6 + 7)) for r in range(6)]
tb = ''.join(f'<tr class="{"extra" if i == 5 else ""}">' + ''.join(f'<td data-c="{c % 6}">{a(c)}</td>' for c in row) + '</tr>' for i, row in enumerate(ROWS6))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">فكّر 💡</span>{ref('تمرين ٦')}</div>
<div class="row" style="align-items:center;gap:3vw"><table class="t6" id="t6">{tb}</table>
<div class="col t6b">{''.join(f'<button class="svbtn" data-k="{k}">{t}</button>' for k, t in (('m3', 'مضاعفات ٣'), ('m6', 'مضاعفات ٦'), ('c5', 'عمود الأوليّات'), ('ex', 'أضف صفّاً')))}<button class="svbtn reset" data-k="">↺</button></div></div>
<script>(function(){{var t=document.getElementById('t6');t.parentNode.querySelectorAll('.t6b .svbtn').forEach(function(b){{b.addEventListener('click',function(e){{e.stopPropagation();
 var k=b.dataset.k;if(!k){{t.className='t6';return;}}t.classList.add(k);}});}});}})();</script>
{st('<div class="note">عمود ٥ ، ١١ ، ١٧ ، ٢٣ ، ٢٩ … لكن ٣٥ = ٥ × ٧ ليس أولياً!</div>')}'''))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ٢ 🎫</span><h2>أجب في دفترك</h2>
<div class="exit">{st('<div><b>١</b>اكتب الأعداد الأولية بين ٤٠ و ٥٠</div>')}{st('<div><b>٢</b>هل توجد ثلاثة أعدادٍ فردية متتالية كلّها أولية؟</div>')}</div>'''))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ٢ 🎫</span><h2>الإجابات</h2>
<button class="flip box col" style="min-width:40vw"><span class="tap">👆 اضغط لإظهار الإجابات</span><span class="hid col">{L(41, 43, 47)}<span class="kk">نعم: ٣ ، ٥ ، ٧</span></span></button>'''))

# ═══════════ الحصة الثالثة: العوامل الأولية ═══════════
S.append(slide('''<span class="tag">الحصة الثالثة · ٤٠ دقيقة</span><h2>العوامل الأولية</h2>
<div class="plan"><div><b>٥ د</b>إحماء</div><div><b>١٠ د</b>مثال ١-٤</div><div><b>١٠ د</b>أنا ← نحن ← أنتم</div>
<div><b>١٠ د</b>ناتج ضرب ومجموع أوّليّين</div><div><b>٥ د</b>بطاقة الخروج</div></div>''', 'divider'))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">إحماء 🔥</span>{timer(1)}</div>''' + quiz('أيّ هذه الأعداد ليس أولياً؟', [M('٥٣'), M('٥٩'), M('٥٧'), M('٦١')], 2, '٥٧ = ٣ × ١٩')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('مثال ١-٤')}</div><h2>أوجد العوامل الأولية للعدد ٣٠</h2><p class="ask">نتحقّق من الأعداد الأولية فقط: ٢ ، ٣ ، ٥ ، ٧ …</p>
{box(STEPS(STP('٢ عامل (زوجي)', M('٢', X, '١٥', EQ, '٣٠', cls="sm")), STP('٣ عامل', M('٣', X, '١٠', EQ, '٣٠', cls="sm")), STP('٥ عامل (الآحاد ٠)', M('٥', X, '٦', EQ, '٣٠', cls="sm")), STP('العوامل الأولية', L(2, 3, 5), 'fin')))}'''))
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('تمرين ٤ (و)')}</div><h2>معاً: العوامل الأولية للعدد ٧٠</h2>
{box(STEPS(STP('٢ ؟', M('٢', X, '٣٥', EQ, '٧٠', cls="sm")), STP('٣ ؟', M('٧ + ٠ = ٧', '←', 'لا', cls="sm"), 'bad'), STP('٥ ؟', M('٥', X, '١٤', EQ, '٧٠', cls="sm")), STP('٧ ؟', M('٧', X, '١٠', EQ, '٧٠', cls="sm")), STP('العوامل الأولية', L(2, 5, 7), 'fin')))}'''))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ٤ (هـ)')}{timer(2)}</div>''' + quiz('العوامل الأولية للعدد ٤٥:', ['٣ ، ٥', '٣ ، ٩ ، ٥', '٥ ، ٩', '١ ، ٣ ، ٥'], 0, '٩ ليس أولياً، و ١ ليس أولياً')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ٤ (د)')}</div>''' + quiz('العوامل الأولية للعدد ٢٨:', ['٢ ، ٧', '٤ ، ٧', '٢ ، ١٤', '٢ ، ٤ ، ٧'], 0, '٢٨ = ٢ × ٢ × ٧')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('تمرين ٧')}</div><h2>العدد ٢٢٦ ناتج ضرب عددين أوّليّين. ما هما؟</h2>
{box(STEPS(STP('نبدأ بـ ٢ (زوجي)', M('٢٢٦', '<span class="x">÷</span>', '٢', EQ, '١١٣', cls="sm")), STP('نختبر ٢ ، ٣ ، ٥ ، ٧', M('١١٣', '←', 'أولي', cls="sm")), STP('النتيجة', M('٢٢٦', EQ, '٢', X, '١١٣', cls="sm"), 'fin')))}'''))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ٧')}</div>''' + quiz('العدد ١٣٣ = ؟', ['٣ × ٤٤', '٧ × ١٩', '١١ × ١٣', '٥ × ٢٧'], 1, 'اختبر ٢ ، ٣ ، ٥ ثم ٧: ١٣٣ ÷ ٧ = ١٩')))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">فكّر 💡</span>{ref('تمرين ٨')}</div><h2>طريقة حسن: ابدأ بـ ١١ ثم أضف ٢ ، ٤ ، ٦ …</h2>
<div class="hs">{''.join(st(f'<span>{M(a(x), PL, a(d), EQ, a(x + d), cls="sm")}</span>') for x, d in ((11, 2), (13, 4), (17, 6), (23, 8), (31, 10), (41, 12), (53, 14), (67, 16), (83, 18), (101, 20)))}</div>
<button class="flip box col"><span class="tap">👆 هل حسن على صواب؟</span><span class="hid col"><span class="kk c-exp">لا — ١٢١ = ١١ × ١١</span><span class="hint">لا نعمّم من أمثلةٍ قليلة</span></span></button>'''))
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('تمرين ٩')}</div><h2>معاً: عددان أوّليّان مختلفان مجموعهما ١٨</h2>
{box(STEPS(STP('نجرّب', M('٥', PL, '١٣', EQ, '١٨', cls="sm"), 'fin'), STP('وأيضاً', M('٧', PL, '١١', EQ, '١٨', cls="sm"), 'fin'), STP('عدد الطرق', M('٢', cls="sm"), 'fin')))}
{st('<div class="note">حدسية غولدباخ: كل عددٍ زوجي أكبر من ٢ هو مجموع عددين أوّليّين — لم تُبرهَن حتى الآن!</div>')}'''))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ٩')}{timer(2)}</div>''' + quiz('بكم طريقة نكتب ٣٠ مجموعَ عددين أوّليّين مختلفين؟', [M('١'), M('٢'), M('٣'), M('٤')], 2, '٧ + ٢٣ ، ١١ + ١٩ ، ١٣ + ١٧')))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ٣ 🎫</span><h2>أجب في دفترك</h2>
<div class="exit">{st('<div><b>١</b>أوجد العوامل الأولية للعدد ١٢</div>')}{st('<div><b>٢</b>اكتب ٣٥ ناتجَ ضرب عددين أوّليّين</div>')}{st('<div><b>٣</b>اكتب ٢٦ مجموعَ عددين أوّليّين</div>')}</div>'''))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج ٣ 🎫</span><h2>الإجابات</h2>
<button class="flip box col" style="min-width:40vw"><span class="tap">👆 اضغط لإظهار الإجابات</span><span class="hid col">{L(2, 3)}{M('٥', X, '٧', cls="sm")}{M('٣', PL, '٢٣', 'أو', '٧', PL, '١٩', cls="sm")}</span></button>'''))
S.append(slide('''<span class="qbadge" style="background:#0A6770;box-shadow:0 4px 0 #05393E">الواجب المنزلي 🏠</span><h2>بعد الحصص</h2>
<div class="exit"><div class="st"><div><b>١</b>صفحة ١٨ في كتاب النشاط (الأعداد الأولية)</div></div><div class="st"><div><b>٢</b>صفحة ١٩ في كتاب النشاط (ناتج ضرب أعدادٍ أولية)</div></div></div>'''))
S.append(slide(f'''<h2>الخلاصة</h2>
<div class="sumg">
{st(box('<div class="col"><b class="kk c-we">العدد الأولي</b><span>عاملان فقط: ١ ونفسه</span><span>١ ليس أولياً · ٢ الزوجي الوحيد</span></div>'))}
{st(box('<div class="col"><b class="kk c-exp">الغربال</b><span>نشطب مضاعفات</span><span>٢ ، ٣ ، ٥ ، ٧</span><span>٢٥ عدداً أولياً &lt; ١٠٠</span></div>'))}
{st(box('<div class="col"><b class="kk c-lcm">العوامل الأولية</b>' + M('٣٠', '←', '٢ ، ٣ ، ٥') + '<span>نختبر الأوّليّات فقط</span></div>'))}</div>'''))

# ═══════════ ملحق: تمارين كتاب الطالب ص٢٩ ═══════════
S.append(launch('sb', '٢٩', note=f'المراجع: كتاب الطالب ص٢٨–٢٩ ودليل المعلم ص٢٧–٢٨ وإجاباته ص٣٦–٣٧ — {ME}'))
RP = 'العدد الأولي له عاملان فقط: ١ والعدد نفسه'
H = ['أ', 'ب', 'ج', 'د', 'هـ', 'و', 'ز', 'ح']
S.append(ex(1, 'العددان الأوليّان بين ٢٠ و ٣٠', RP, [('العددان', L(23, 29))], cols=1))
S.append(ex(2, 'الأعداد الأولية بين ٣٠ و ٤٠ وعددها', RP, [('الأعداد', L(31, 37)), ('عددها', M('٢'))], cols=2))
S.append(ex(3, 'كم عدداً أولياً بين ٩٠ و ١٠٠؟', RP, [('العدد', M('١') + '<small>هو ٩٧</small>')], cols=1))
S.append(ex(4, 'أوجد العوامل الأولية', 'نختبر ٢ ، ٣ ، ٥ ، ٧ …', [(f'({h}) {a(n)}', L(*PF(n))) for h, n in zip(H, [10, 15, 25, 28, 45, 70])], cols=2))
S.append(ex(5, 'أعدادٌ متتالية ليس بينها عددٌ أولي', 'استخدم شبكة الغربال', [('(أ) خمسة أعداد', M('٢٤ ، ٢٥ ، ٢٦ ، ٢٧ ، ٢٨') + '<small>مثال</small>'), ('(ب) سبعة أعداد', M('٩٠ ، ٩١ ، … ، ٩٦') + '<small>نعم، مثال</small>')], cols=2))
S.append(ex(6, 'الجدول ذو الأعمدة الستة', 'انظر إلى كل عمود', [('(أ)(١) مضاعفات ٣', 'العمودان ٣ و ٦'), ('(أ)(٢) مضاعفات ٦', 'العمود ٦'),
  ('(ب) عمود الأوّليّات', 'العمود ٥'), ('(ج) بعد إضافة صفوف؟', 'لا — ٣٥ ليس أولياً')], cols=2))
S.append(ex(7, 'كلٌّ منها ناتج ضرب عددين أوّليّين', 'نقسم على ٢ ، ٣ ، ٥ ، ٧', [(f'{a(n)}', M(a(p), X, a(n // p))) for n, p in ((226, 2), (321, 3), (305, 5), (133, 7))], cols=2))
S.append(ex(8, 'هل طريقة حسن صحيحة؟', 'استمرّ في النمط', [('الإجابة', 'لا ' + M('١٢١', EQ, '١١', X, '١١'))], cols=1))
S.append(ex(9, 'عددان أوّليّان مختلفان مجموعهما', 'جرّب الأعداد الأولية الأصغر', [('(أ)(١) ١٨', M('٥ + ١٣ ، ٧ + ١١')), ('(أ)(٢) ٢٦', M('٣ + ٢٣ ، ٧ + ١٩')),
  ('(أ)(٣) ٣٠', M('٧ + ٢٣ ، ١١ + ١٩ ، ١٣ + ١٧')), ('(ب) عدد الطرق', M('٢ ، ٢ ، ٣'))], cols=1, per=2))

# ═══════════ ملحق: حلول كتاب النشاط ص١٨–١٩ (الإجابات من دليل المعلم ص٤٢) ═══════════
S.append(launch('ab', '١٨ و ١٩', note='الإجابات النهائية من دليل المعلم ص ٤٢'))
NA, NB = 'نشاط ص ١٨ · تمرين', 'نشاط ص ١٩ · تمرين'
S.append(ex(1, 'كم عدداً أولياً أصغر من ٢٠؟', RP, [('العدد', M('٨'))], cols=1, src=NA))
S.append(ex(2, 'العدد الأولي الخامس عشر', 'عُدّ في قائمة الأوّليّات', [('الإجابة', M('٤٧'))], cols=1, src=NA))
S.append(ex(3, 'الأعداد الأولية بين ٨٠ و ٩٠', RP, [('الأعداد', L(83, 89))], cols=1, src=NA))
S.append(ex(4, 'لماذا لا يكون العدد الأولي مربّعاً؟', 'فكّر في عوامل المربّع', [('السبب', 'للمربّع عاملٌ آخر هو جذره')], cols=1, src=NA))
S.append(ex(5, 'صحيحة أم خاطئة؟', 'ابحث عن مثالٍ مضاد', [('(أ) كل الأوّليّات فردية', 'خاطئة — ٢ زوجي'), ('(ب) لا توجد ٣ فردية متتالية أولية', 'خاطئة — ٣ ، ٥ ، ٧'),
  ('(ج) عددٌ أولي واحد بين ٩٠ و ١٠٠', 'صحيحة — ٩٧')], cols=2, src=NA))
S.append(ex(6, '٢٥ مجموع ثلاثة أعدادٍ أولية مختلفة', 'جرّب الأعداد الفردية الأولية', [('(أ) مثال', M('٣ + ٥ + ١٧') + '<small>أو ٥ + ٧ + ١٣</small>'), ('(ب) عدد الطرق', M('٢'))], cols=2, src=NA))
S.append(ex(7, 'أوجد العوامل الأولية', 'نختبر ٢ ، ٣ ، ٥ ، ٧', [(f'({h}) {a(n)}', L(*PF(n))) for h, n in zip(H, [12, 27, 28, 30])], cols=2, src=NA))
S.append(ex(8, 'اكتب في صورة ضرب أعدادٍ أولية', 'نقسم على ٢ ، ٣ ، ٥ ، ٧', [(f'({h}) {a(n)}', M(a(p), X, a(n // p))) for h, (n, p) in zip(H, ((21, 3), (22, 2), (35, 5), (51, 3), (65, 5)))], cols=2, src=NB))
S.append(ex(9, 'لماذا للعددين الأوليين عاملٌ مشترك واحد؟', 'عوامل كلٍّ منهما: ١ ونفسه', [('السبب', 'العامل المشترك الوحيد هو ١')], cols=1, src=NB))

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
.box .col>.m:not(.mid):not(.sm):not(.big),.hid.col>.m:not(.mid):not(.sm):not(.big){font-size:clamp(34px,6.4vh,76px)}
.exit .kb{font-style:normal;color:var(--exp);font-weight:900}
.pchips{display:flex;flex-wrap:wrap;gap:1.2vh 1.2vw;justify-content:center;direction:rtl;width:min(1500px,92vw)}
.pchips b{font-family:var(--fh);font-weight:900;font-size:clamp(36px,7vh,84px);background:var(--good);color:#fff;border-radius:16px;padding:.1em .45em;min-width:2.2em;text-align:center}
.pchips.p25 b{font-size:clamp(28px,5.2vh,62px)}
.sieve{display:grid;grid-template-columns:repeat(10,minmax(0,1fr));gap:.5vh .5vw;direction:rtl}
.sieve.s100{width:min(1300px,80vw)}.sieve.s100 .sv{font-size:clamp(20px,4.2vh,48px);padding:0;line-height:1.25}
.sv{font-family:var(--fh);font-weight:900;background:#fff;border:2.5px solid var(--line);border-radius:10px;color:var(--ink);position:relative}
.sv.one{color:#9FB0C6}.sv.out{color:#B8C4D4;background:#F2F5F9}
.sv.out::after{content:'';position:absolute;inset:50% 12%;border-top:3px solid var(--bad);transform:rotate(-20deg)}
.sv.cur{background:#FFF1D6;border-color:var(--gcd)}.sv.pr{background:var(--good);border-color:var(--good);color:#fff}
.svb{gap:.8vw;flex-wrap:wrap;justify-content:center}.svbtn{font-family:var(--fh);font-weight:800;font-size:clamp(20px,4.2vh,48px);background:#fff;border:2.5px solid var(--ink2);color:var(--ink);border-radius:12px;padding:.1em .7em;cursor:pointer}
.svbtn.show{background:var(--good);border-color:var(--good);color:#fff}.svbtn.reset{border-style:dashed}
.slide.sievesl{gap:1.2vh}
.t6{border-collapse:separate;border-spacing:.5vh;direction:rtl}
.t6 td{font-family:var(--fh);font-weight:900;font-size:clamp(28px,5.6vh,66px);background:#FFF7D6;border:3px solid #2563EB;border-radius:10px;padding:0 .5em;text-align:center;transition:.3s}
.t6 tr.extra{display:none}.t6.ex tr.extra{display:table-row}.t6.ex tr.extra td{background:#EAF1FF}
.t6.m3 td[data-c="3"],.t6.m3 td[data-c="0"]{background:#D8E6FF}
.t6.m6 td[data-c="0"]{background:#C7361B;color:#fff}
.t6.c5 td[data-c="5"]{background:var(--good);color:#fff}
.t6.c5.ex tr.extra td[data-c="5"]{background:var(--bad)}
.t6b{gap:1.2vh}
.hs{display:grid;grid-template-columns:repeat(5,auto);grid-auto-flow:row;gap:1vh 1.5vw;direction:rtl}
.hs .m.sm{font-size:clamp(24px,4.4vh,52px)}
.sumg{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:2vw;width:min(1600px,94vw)}
.sumg .col span{font-weight:700;font-size:clamp(26px,5vh,60px);line-height:1.4}
.sumg .kk{font-size:clamp(36px,7vh,84px)}
'''
