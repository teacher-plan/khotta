# عرض مراجعة «الوحدة الثانية: العبارات الجبرية والمعادلات والصيغ» — الصف السابع.
# المرجع: صفحة ملخّص الوحدة في كتاب الطالب ص٥٣ («يجب أن تعرف أنّ» + «يجب أن تكون قادراً على»)، و«تمارين ومسائل عامة» ص٥٤–٥٥
# (إجابات دليل المعلم ص٥٦–٥٧).
# python3.12 gen_powers.py unit2_slides.py مراجعة_الوحدة_الثانية_عرض_تفاعلي.html "مراجعة الوحدة الثانية — الصف السابع"
# لكل قاعدة: بطاقة القاعدة ← مثالٌ محلول خطوةً خطوة ← سؤالٌ سريع (أنتم).

MI = '<span class="x">−</span>'; DV = '<span class="x">÷</span>'
def V(t): return f'<span class="var">{t}</span>'
def T(k, v): return f'<span class="term">{k}{V(v)}</span>'
def G(*p): return '<span class="grp">(' + ' '.join(p) + ')</span>'
def FR(n, d): return f'<span class="fr"><span>{n}</span><span>{d}</span></span>'
def STP(lab, expr, cls=''): return st(f'<div class="stp {cls}"><span class="lab">{lab}</span>{expr}</div>')
def STEPS(*rows): return '<div class="stps">' + ''.join(rows) + '</div>'
def RULE(n, t): return f'<div class="rulecard"><span class="rn">قاعدة {a(n)}</span><span>{t}</span></div>'
def SEC(n, title, lesson, items):
    return slide(f'''<span class="tag">الجزء {a(n)} من ٥ · الدرس {lesson}</span><h2>{title}</h2>
<div class="exit">{''.join(st(f'<div><b>{a(i + 1)}</b><span>{t}</span></div>') for i, t in enumerate(items))}</div>''', 'divider')
def PYR(rows):
    return '<div class="pyr2">' + ''.join('<div class="prow">' + ''.join(f'<span class="pc">{c}</span>' for c in row) + '</div>' for row in rows) + '</div>'
def BARS(segs, total):
    return '<div class="sbar"><div class="segs">' + ''.join(f'<span class="{c}" style="flex:{f}">{t}</span>' for t, f, c in segs) + f'</div><div class="tot">{total}</div></div>'

S = []
S.append(slide('''<span class="tag">الصف السابع · مراجعة الوحدة الثانية</span>
<h1 class="h1s">العبارات الجبرية والمعادلات والصيغ</h1>
<p class="lead" style="font-size:clamp(26px,4.8vh,56px)">إعداد: أ. عيسى الحارثي</p>''', 'cover'))
S.append(slide('''<h2>نراجع قواعد الوحدة كلّها في خمسة أجزاء</h2>
<div class="can">
<div><span class="can-i">١</span><span>كتابة العبارات الجبرية</span></div>
<div><span class="can-i">٢</span><span>تجميع الحدود المتشابهة</span></div>
<div><span class="can-i">٣</span><span>فكّ الأقواس</span></div>
<div><span class="can-i">٤</span><span>الصيغ والتعويض</span></div>
<div><span class="can-i">٥</span><span>كتابة المعادلات وحلّها</span></div></div>'''))

# ═══ ١ العبارات الجبرية ═══
S.append(SEC(1, 'كتابة العبارات الجبرية', '٢-١', ['الحرف يمثّل عدداً مجهولاً', 'نكتب عبارةً جبرية من وصفٍ لفظي']))
S.append(slide(f'''{RULE(1, 'في الجبر يمكن استخدام <b>حرفٍ</b> لتمثيل عددٍ مجهول، و<b>العبارة الجبرية</b> فيها أرقامٌ وحروف وعمليات، بلا إشارة =')}
{box(STEPS(STP('تضرب العدد في ٤', M(T('٤', 'س'), cls="sm")), STP('تطرح ٦ من العدد', M(V('س'), MI, '٦', cls="sm")), STP('تضرب في ٣ ثم تضيف ٥', M(T('٣', 'س'), PL, '٥', cls="sm")), STP('تقسم على ٦ ثم تطرح ١', M(FR(V('س'), '٦'), MI, '١', cls="sm"), 'fin')))}''' + tn('من «تمارين ومسائل عامة» تمرين ١: تفكّر مريم في عدد س.')))
S.append(slide(f'''{mode('u')}{timer(1)}''' + quiz('«أضِف ٢ إلى ع ثم اضرب الناتج في ٥» تُكتب…', [M('٥' + V('ع'), PL, '٢'), M('٥', G(V('ع'), PL, '٢')), M(V('ع'), PL, '١٠'), M('٢' + V('ع'), PL, '٥')], 1, 'الجمع أولاً، فنضع ع + ٢ بين قوسين ثم نضرب في ٥')))

# ═══ ٢ تجميع الحدود المتشابهة ═══
S.append(SEC(2, 'تجميع الحدود المتشابهة', '٢-٢', ['الحدود المتشابهة: المتغيّر نفسه', 'نجمع المعاملات ونُبقي المتغيّر']))
S.append(slide(f'''{RULE(2, 'تُسمّى الحدود التي تحتوي على <b>المتغيّر نفسه</b> حدوداً متشابهة، ونجمع معاملاتها أو نطرحها ونُبقي المتغيّر')}
{box(STEPS(STP('المسألة', M(T('٦', 'ح'), PL, T('٥', 'ك'), PL, T('٥', 'ح'), PL, V('ك'), cls="sm")), STP('نرتّب المتشابهة', M(T('٦', 'ح'), PL, T('٥', 'ح'), PL, T('٥', 'ك'), PL, V('ك'), cls="sm")), STP('الناتج', M(T('١١', 'ح'), PL, T('٦', 'ك'), cls="sm"), 'fin')))}''' + tn('تمرين ٤ (ب) من «تمارين ومسائل عامة».')))
S.append(slide(f'''{mode('u')}{timer(1)}''' + quiz(f'بسّط {M(T("٩", "س"), MI, V("س"))}', [M('٩'), M(T('٨', 'س')), M(T('١٠', 'س')), M('٨')], 1, 'س تعني ١س: ٩ − ١ = ٨ ، فالناتج ٨س')))
S.append(slide(f'''{mode('u')}''' + quiz(f'بسّط {M(T("١١", "ك"), MI, T("١٠", "ك"))}', [M('١'), M(T('٢١', 'ك')), M(V('ك')), M('٠')], 2, '١١ك − ١٠ك = ١ك ونكتبها ك')))

# ═══ ٣ فكّ الأقواس ═══
S.append(SEC(3, 'فكّ الأقواس', '٢-٣', ['العدد الملاصق للقوس يعني الضرب', 'نضرب ما خارج القوس في كل حدٍّ بداخله']))
S.append(slide(f'''{RULE(3, 'لفكّ الأقواس (الضرب خارج الأقواس) نضرب <b>الحدّ الموجود خارج الأقواس</b> في <b>كل حدٍّ</b> بداخلها')}
<div class="row">{box(STEPS(STP('المسألة', M('٤', G(T('٣', 'س'), PL, '٢'), cls="sm")), STP('نضرب', M('٤', X, T('٣', 'س'), PL, '٤', X, '٢', cls="sm")), STP('الناتج', M(T('١٢', 'س'), PL, '٨', cls="sm"), 'fin')))}
{box(STEPS(STP('المسألة', M('٦', G('٣', MI, V('ر')), cls="sm")), STP('نضرب', M('٦', X, '٣', MI, '٦', X, V('ر'), cls="sm")), STP('الناتج', M('١٨', MI, T('٦', 'ر'), cls="sm"), 'fin')))}</div>''' + tn('تمرين ٧ (أ) وتمرين ٦ (د) من «تمارين ومسائل عامة».')))
S.append(slide(f'''{mode('u')}{timer(1)}''' + quiz(f'فكّ الأقواس {M("٤", G(V("د"), MI, "٥"))}', [M(T('٤', 'د'), MI, '٥'), M(T('٤', 'د'), MI, '٢٠'), M(T('٤', 'د'), MI, '٩'), M(T('٤', 'د'), PL, '٢٠')], 1, '٤ × د = ٤د ، و ٤ × ٥ = ٢٠ ، والإشارة − تبقى')))

# ═══ ٤ الصيغ والتعويض ═══
S.append(SEC(4, 'الصيغ والتعويض', '٢-٤', ['الصيغة فيها إشارة =', 'نعوّض العدد مكان الحرف', 'نتّبع ترتيب العمليات']))
S.append(slide(f'''{RULE(4, 'الصيغة قاعدةٌ توضّح العلاقة بين كميات، وفيها دائماً إشارة =. و<b>التعويض</b> أن نضع العدد مكان الحرف ثم نحسب بترتيب العمليات')}
{box(STEPS(STP('أوجد ع + ٣ص عندما ع = ٣ ، ص = ٤', M('٣', PL, '٣', X, '٤', cls="sm")), STP('الضرب أولاً', M('٣', PL, '١٢', cls="sm")), STP('الناتج', M('١٥', cls="sm"), 'fin')))}''' + tn('تمرين ٢ (ب) من «تمارين ومسائل عامة».')))
S.append(slide(f'''{mode('u')}{timer(1)}''' + quiz(f'أوجد قيمة {M(V("س"), PL, "٣")} عندما س = ٨', [M('٢٤'), M('١١'), M('٥'), M('٨٣')], 1, '٨ + ٣ = ١١')))

# ═══ ٥ المعادلات ═══
S.append(SEC(5, 'كتابة المعادلات وحلّها', '٢-٥', ['المعادلة فيها إشارة =', 'حلّها: إيجاد قيمة المتغيّر', 'نتحقّق بالتعويض']))
S.append(slide(f'''{RULE(5, 'لحلّ معادلة نجد قيمة المتغيّر بالعمليات العكسية على <b>الطرفين</b>، ونتحقّق من الحل بالتعويض في المعادلة')}
{box(STEPS(STP('المسألة', M(T('٣', 'ل'), PL, '٢', EQ, '١٧', cls="sm")), STP('نطرح ٢ من الطرفين', M(T('٣', 'ل'), EQ, '١٥', cls="sm")), STP('نقسم على ٣', M(V('ل'), EQ, '٥', cls="sm"), 'fin'), STP('نتحقّق', M('٣', X, '٥', PL, '٢', EQ, '١٧ ✔', cls="sm"))))}''' + tn('تمرين ١٠ (أ) من «تمارين ومسائل عامة».')))
S.append(slide(f'''{RULE(6, 'نكتب المعادلة من الوصف اللفظي جزءاً جزءاً، ثم نحلّها')}
{box(STEPS(STP('«أفكّر في عدد إذا ضربته في ٢ وأضفت إليه ٤ يصبح ٢٨»', M(T('٢', 'س'), PL, '٤', EQ, '٢٨', cls="sm")), STP('نطرح ٤', M(T('٢', 'س'), EQ, '٢٤', cls="sm")), STP('نقسم على ٢', M(V('س'), EQ, '١٢', cls="sm"), 'fin')))}''' + tn('لغز عائشة في تمرين ١١ (ب) من «تمارين ومسائل عامة».')))
S.append(slide(f'''{mode('u')}{timer(1)}''' + quiz(f'حلّ {M(FR(V("س"), "٥"), EQ, "٣")}', [M(V('س'), EQ, '٨'), M(V('س'), EQ, '١٥'), M(V('س'), EQ, '٢'), M(V('س'), EQ, '٠٫٦')], 1, 'نضرب الطرفين في ٥: س = ١٥')))

# ═══ «يجب أن تكون قادراً على» — تقييمٌ ذاتي ═══
SK = ['إنشاء عباراتٍ جبرية بسيطة', 'استنتاج واستخدام صيغٍ بسيطة', 'التعويض بقيمة المتغيّر (العدد) في المعادلات والصيغ البسيطة',
      'تبسيط العبارات الجبرية عن طريق تجميع الحدود المتشابهة', 'فكّ الحدّ الذي يتضمّن أقواساً', 'إنشاء وحلّ المعادلات',
      'استخدام الأعداد والعبارات الجبرية', 'التحقّق من صحة حلّ المعادلة', 'التعبير عن الصيغ بالكلمات والحروف']
def CHECK(items, start):
    return ''.join(f'<button class="ck"><span class="cb">{a(start + i)}</span><span>{t}</span></button>' for i, t in enumerate(items))
CKJS = "<script>document.querySelectorAll('.ck').forEach(function(b){b.onclick=function(e){e.stopPropagation();b.classList.toggle('ok');};});</script>"
for k in range(0, len(SK), 3):
    last = k + 3 >= len(SK)
    S.append(slide(f'''<div class="row hdr"><span class="qbadge">تقييمٌ ذاتي ✅</span><span class="tag">اضغط على ما تتقنه ليصبح أخضر</span></div><h2>يجب أن أكون قادراً على… ({a(k // 3 + 1)})</h2>
<div class="cks">{CHECK(SK[k:k+3], k + 1)}</div>{CKJS if last else ''}'''))
S.append(slide(f'''<h2>أحسنتم! 🎉</h2>
<div class="note">راجعوا ورقة ملخّص الوحدة، وحلّوا «تمارين ومسائل عامة» ص ٥٤ و ٥٥</div>
<p class="hint st">المرجع: كتاب الطالب، صفحة ملخّص الوحدة الثانية · إعداد: أ. عيسى الحارثي</p>'''))

# ═══ ملحق: «تمارين ومسائل عامة» ص٥٤–٥٥ (الإجابات من دليل المعلم ص٥٦–٥٧) ═══
S.append(launch('sb', '٥٤ و ٥٥', note='تمارين ومسائل عامة: الإجابات من دليل المعلم ص ٥٦ و ٥٧'))
S.append(ex(1, 'تفكّر مريم في عدد س. اكتب عبارةً جبرية عندما…', 'نترجم كل عملية إلى رموز بالترتيب', [('(أ) تضرب العدد في ٤', M(T('٤', 'س'))), ('(ب) تطرح ٦ من العدد', M(V('س'), MI, '٦')),
  ('(ج) تضرب في ٣ ثم تضيف ٥', M(T('٣', 'س'), PL, '٥')), ('(د) تقسم على ٦ ثم تطرح ١', M(FR(V('س'), '٦'), MI, '١'))], cols=2))
S.append(ex(2, 'أوجد قيمة كلٍّ من العبارات الجبرية', 'نعوّض ثم نحسب بترتيب العمليات', [('(أ) س + ٣ عندما س = ٨', '٨ + ٣ = ١١'), ('(ب) ع + ٣ص عندما ع = ٣ ، ص = ٤', '٣ + ١٢ = ١٥')], cols=2))
S.append(ex(3, 'بسّط العبارات الجبرية', 'نجمع معاملات الحدود المتشابهة', [('(أ) ص + ص + ص', M(T('٣', 'ص'))), ('(ب) ٣ح + ٥ح', M(T('٨', 'ح'))), ('(ج) ٩س − س', M(T('٨', 'س'))), ('(د) ١١ك − ١٠ك', M(V('ك')))], cols=2))
S.append(ex(4, 'بسّط بتجميع الحدود المتشابهة', 'نرتّب المتشابهة معاً، والإشارة تنتقل مع حدّها', [('(أ) ٥ح + ٦ح + ٢د', M(T('١١', 'ح'), PL, T('٢', 'د'))), ('(ب) ٦ح + ٥ك + ٥ح + ك', M(T('١١', 'ح'), PL, T('٦', 'ك'))),
  ('(ج) ٣و + د + ٥دص − ٢و + ٣دص', M(V('و'), PL, V('د'), PL, T('٨', 'دص')))], cols=1, per=3))
S.append(ex(5, 'أكمل الهرم', 'كل خانة = مجموع الخانتين تحتها', [('الحل', PYR([['١٣س + ٢٠ص'], ['٧س + ١١ص', '٦س + ٩ص'], ['٤س + ٦ص', '٣س + ٥ص', '٣س + ٤ص'], ['٣س + ٢ص', 'س + ٤ص', '٢س + ص', 'س + ٣ص']]))], cols=1))
S.append(ex(6, 'فكّ الأقواس', 'نضرب ما خارج القوس في كل حدٍّ بداخله', [('(أ) ٣(س + ٢)', M(T('٣', 'س'), PL, '٦')), ('(ب) ٤(د − ٥)', M(T('٤', 'د'), MI, '٢٠')), ('(ج) ٢(٣ + ص)', M('٦', PL, T('٢', 'ص'))), ('(د) ٦(٣ − ر)', M('١٨', MI, T('٦', 'ر')))], cols=2))
S.append(ex(7, 'اضرب خارج الأقواس', 'نضرب الأعداد ونُبقي المتغيّر', [('(أ) ٤(٣س + ٢)', M(T('١٢', 'س'), PL, '٨')), ('(ب) ٢(٢د − ٣)', M(T('٤', 'د'), MI, '٦')), ('(ج) ٥(٥ + ٣ص)', M('٢٥', PL, T('١٥', 'ص'))), ('(د) ٣(٧ − ٤ط)', M('٢١', MI, T('١٢', 'ط')))], cols=2))
S.append(ex(8, 'أيّ العبارات تختلف عن الأخرى؟', 'نفكّ الأقواس كلها ثم نقارن', [('٦(٦ + ٨س)', '٣٦ + ٤٨س'), ('٤(١٢س + ٨)', '٤٨س + ٣٢<small>هي المختلفة</small>'), ('٢(١٨ + ٢٤س)', '٣٦ + ٤٨س'), ('٣(١٦س + ١٢)', '٤٨س + ٣٦')], cols=2))
S.append(ex(9, 'حلّ المعادلات وتحقّق من صحة إجاباتك', 'العملية العكسية على الطرفين', [('(أ) ص + ٦ = ١٥', 'ص = ٩'), ('(ب) م − ٤ = ١٢', 'م = ١٦'), ('(ج) ٣ع = ٢٤', 'ع = ٨'), ('(د) س ÷ ٥ = ٣', 'س = ١٥')], cols=2,
  note='في إجابات دليل المعلم ص ٥٧ كُتب حلّ (أ) «ع = ٥»، والصحيح ص = ٩ لأن ٩ + ٦ = ١٥.'))
S.append(ex(10, 'حلّ المعادلات وتحقّق من صحة إجاباتك', 'نتخلّص من الجمع أو الطرح أولاً، ثم من الضرب أو القسمة', [('(أ) ٣ل + ٢ = ١٧', 'ل = ٥'), ('(ب) ٤ح − ١ = ١٩', 'ح = ٥'), ('(ج) د ÷ ٣ + ٢ = ٩', 'د = ٢١'), ('(د) ل ÷ ٢ − ١ = ٤', 'ل = ١٠')], cols=2))
S.append(ex(11, 'اكتب معادلةً لكل لغز ثم حلّها', 'نرمز للعدد بالحرف س', [('(أ) محمد: أفكّر في عدد إذا أضفت إليه ٣ أصبح ٢٢', 'س + ٣ = ٢٢<small>س = ١٩</small>'), ('(ب) عائشة: أفكّر في عدد إذا ضربته في ٢ وأضفت إليه ٤ يصبح ٢٨', '٢س + ٤ = ٢٨<small>س = ١٢</small>')], cols=1, per=2))
S.append(ex(12, 'اكتب معادلةً لمجموع أطوال المستطيلات ثم حلّها', 'مجموع الأطوال الصغيرة = الطول الكلي', [
  ('(أ)' + BARS([('س', 1, 'y'), ('س', 1, 'y'), ('س', 1, 'y'), ('٦', 1.6, 'w')], '٢١ سم'), '٣س + ٦ = ٢١<small>س = ٥</small>'),
  ('(ب)' + BARS([('ص', 1, 'g'), ('ص', 1, 'g'), ('ص', 1, 'g'), ('ص', 1, 'g'), ('٢', .6, 'w')], '٣٤ سم'), '٤ص + ٢ = ٣٤<small>ص = ٨</small>')], cols=1, per=1))

EXTRA_CSS_OWN = '''
.var{color:var(--exp);font-weight:900}
.term,.grp{display:inline-flex;direction:rtl;unicode-bidi:isolate;align-items:center}.grp{gap:.2em}
.fr{display:inline-flex;flex-direction:column;align-items:center;line-height:1.05;vertical-align:middle;margin:0 .1em}
.fr>span:first-child{border-bottom:.07em solid currentColor;padding:0 .15em .04em;align-self:stretch;text-align:center}
.stps{display:flex;flex-direction:column;gap:1.4vh;align-items:stretch}
.stp{display:flex;align-items:center;gap:1.4vw;justify-content:space-between}
.stp .lab{flex:none;max-width:48%;font-family:var(--fh);font-weight:800;color:#2563EB;background:#EAF1FF;border-radius:12px;padding:.2em .8em;text-align:center;line-height:1.4}
.stp.fin .lab{background:var(--good);color:#fff}.stp.fin .m{color:var(--good)}
.rulecard{display:flex;align-items:center;gap:1em;background:#fff;border:3px solid var(--ink);border-radius:20px;padding:1.4vh 1.6vw;width:min(1300px,92vw);font-weight:700;font-size:clamp(24px,4.4vh,50px);line-height:1.5;box-shadow:0 7px 0 #DCE5F0}
.rulecard .rn{flex:none;font-family:var(--fh);font-weight:900;background:var(--ink);color:#fff;border-radius:14px;padding:.2em .7em;font-size:.8em}
.pyr2{display:flex;flex-direction:column;align-items:center;gap:6px;direction:rtl}
.prow{display:flex;gap:6px}
.pc{font-family:var(--fh);font-weight:900;font-size:clamp(22px,4.3vh,48px);min-width:4.6em;padding:.15em .4em;text-align:center;background:#EAF7EE;border:3px solid #9CD3B0;border-radius:10px;color:var(--ink)}
.sbar{display:flex;flex-direction:column;align-items:stretch;gap:.6vh;width:min(900px,62vw);direction:rtl;margin-top:.6vh}
.sbar .segs{display:flex;border:3px solid var(--ink);border-radius:6px;overflow:hidden}
.sbar .segs span{display:flex;align-items:center;justify-content:center;height:clamp(40px,7vh,80px);border-inline-start:3px solid var(--ink);font-family:var(--fh);font-weight:800;font-size:clamp(24px,4.6vh,52px)}
.sbar .segs span:first-child{border-inline-start:0}
.sbar .y{background:#FBE36B}.sbar .g{background:#5CC27A}.sbar .w{background:#fff}
.sbar .tot{text-align:center;font-weight:800;font-size:clamp(24px,4.4vh,50px);border-top:3px solid var(--ink2);padding-top:.3vh}
.xcard .xq{display:flex;flex-direction:column;align-items:center}
.cks{display:flex;flex-direction:column;gap:1.2vh;width:min(1300px,92vw)}
.ck{display:flex;align-items:center;gap:1em;text-align:start;font-family:var(--fb);font-weight:700;font-size:clamp(24px,4.4vh,50px);background:#fff;border:2.5px solid var(--line);border-radius:14px;padding:1vh 1.4vw;cursor:pointer;color:var(--ink);line-height:1.4}
.ck .cb{flex:none;width:1.6em;height:1.6em;border-radius:50%;background:#EEF2F7;display:flex;align-items:center;justify-content:center;font-family:var(--fh)}
.ck.ok{border-color:var(--good);background:#F2FBF5}.ck.ok .cb{background:var(--good);color:#fff}
'''
