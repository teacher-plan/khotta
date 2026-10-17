# عرض مراجعة «الوحدة الرابعة: الطول والكتلة والسعة» — الصف السابع.
# المرجع: صفحة ملخّص الوحدة في كتاب الطالب ص٨٧ («يجب أن تعرف أنّ» + «يجب أن تكون قادراً على»)، و«تمارين ومسائل عامة» ص٨٨
# (إجابات دليل المعلم ص٩١، مع تصحيح ترتيب ٤ (أ)).
# python3.12 gen_powers.py unit4_slides.py مراجعة_الوحدة_الرابعة_عرض_تفاعلي.html "مراجعة الوحدة الرابعة — الصف السابع"
# لكل جزء: بطاقة القاعدة ← مثالٌ محلول بخطوات ← سؤالٌ سريع (أنتم).
exec(open(os.path.join(HERE, 'figs.py'), encoding='utf-8').read())
DV = '<span class="x">÷</span>'
def STP(lab, expr='', cls=''): return st(f'<div class="stp {cls}"><span class="lab">{lab}</span>{expr}</div>')
def STEPS(*rows): return '<div class="stps">' + ''.join(rows) + '</div>'
def RULE(n, t): return f'<div class="rulecard"><span class="rn">قاعدة {a(n)}</span><span>{t}</span></div>'
NP = 3
def SEC(n, title, lesson, items):
    return slide(f'''<span class="tag">الجزء {a(n)} من {a(NP)} · الدرس {lesson}</span><h2>{title}</h2>
<div class="exit">{''.join(st(f'<div><b>{a(i + 1)}</b><span>{t}</span></div>') for i, t in enumerate(items))}</div>''', 'divider')
LEN = (['كم', 'م', 'سم', 'ملم'], [1000, 100, 10], ['كيلومتر', 'متر', 'سنتيمتر', 'مليمتر'])
MAS = (['طن', 'كغم', 'غم'], [1000, 1000], ['طن', 'كيلوغرام', 'غرام'])
CAP = (['لتر', 'مل'], [1000], ['لتر', 'مليلتر'])

S = []
S.append(slide('''<span class="tag">الصف السابع · مراجعة الوحدة الرابعة</span>
<h1 class="h1s">الطول والكتلة والسعة</h1>
<p class="lead" style="font-size:clamp(26px,4.8vh,56px)">إعداد: أ. عيسى الحارثي</p>''', 'cover'))
S.append(slide('''<h2>نراجع الوحدة كلّها في ثلاثة أجزاء</h2>
<div class="can">
<div><span class="can-i">١</span><span>التحويل بين الوحدات: نضرب أم نقسم؟</span></div>
<div><span class="can-i">٢</span><span>ترتيب القياسات بعد توحيد الوحدات</span></div>
<div><span class="can-i">٣</span><span>اختيار الوحدة المناسبة والتقدير</span></div></div>'''))

# ═══ ١ التحويل ═══
S.append(SEC(1, 'التحويل بين وحدات القياس', '٤-١', ['معاملات التحويل: ١٠ ، ١٠٠ ، ١٠٠٠', 'إلى وحدةٍ أصغر نضرب، وإلى وحدةٍ أكبر نقسم']))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">سلّم الطول</span>{ref('كتاب الطالب ص ٨٧')}</div>
{st(STAIR(*LEN))}''' + tn('الرسم نفسه في الدرس ٤-١: النزول إلى وحدةٍ أصغر ضرب، والصعود إلى وحدةٍ أكبر قسمة.')))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">سلّما الكتلة والسعة</span>{ref('كتاب الطالب ص ٨٧')}</div>
<div class="row stairs">{st(STAIR(*MAS))}{st(STAIR(*CAP))}</div>'''))
S.append(slide(f'''{RULE(1, 'من وحدةٍ <b>كبيرة إلى أصغر نضرب</b> في معامل التحويل، ومن وحدةٍ <b>صغيرة إلى أكبر نقسم</b> عليه')}
<div class="row vrow">{STEPS(STP('١) ٣٫٢ كغم إلى غم', M('٣٫٢', X, '١٠٠٠', EQ, '٣٢٠٠', cls='sm')), STP('٢) ٨٠٠٠ مل إلى لتر', M('٨٠٠٠', DV, '١٠٠٠', EQ, '٨', cls='sm')), STP('٣) ١٢٠ سم إلى م', M('١٢٠', DV, '١٠٠', EQ, '١٫٢', cls='sm'), 'fin'))}</div>''' + tn('من «تمارين ومسائل عامة» ٢ (ب) و ٣ (أ) و ١ (ج).')))
S.append(slide(f'''{mode('u')}{timer(1)}''' + quiz('٠٫٢٥ طن = ؟ كغم', [M('٢٥'), M('٢٥٠'), M('٢٥٠٠'), M('٠٫٠٠٠٢٥')], 1, 'من طن إلى كغم (وحدةٌ أصغر) نضرب في ١٠٠٠: ٢٥٠ كغم')))
S.append(slide(f'''{mode('u')}{timer(1)}''' + quiz('٧٥ ملم = ؟ سم', [M('٧٥٠'), M('٠٫٧٥'), M('٧٫٥'), M('٧٥٠٠')], 2, 'من ملم إلى سم (وحدةٌ أكبر) نقسم على ١٠: ٧٫٥ سم')))

# ═══ ٢ الترتيب ═══
S.append(SEC(2, 'ترتيب القياسات', '٤-١', ['نحوّل كل القياسات إلى الوحدة نفسها', 'نرتّب، ثم نكتب الوحدات الأصلية']))
S.append(slide(f'''{RULE(2, 'عند ترتيب قياسات نتأكّد أن لها <b>الوحدة نفسها</b>، ثم نكتب الإجابة <b>بالوحدات الأصلية</b>')}
<div class="row vrow">{STEPS(STP('١) نحوّل إلى مل', M('٦٣٠٠ ، ٨٨٠ ، ٧٠٠', cls='sm')), STP('٢) نرتّب الأعداد', M('٧٠٠ ، ٨٨٠ ، ٦٣٠٠', cls='sm')), STP('٣) بالوحدات الأصلية', M('٠٫٧ لتر ، ٨٨٠ مل ، ٦٫٣ لتر', cls='sm'), 'fin'))}</div>''' + tn('من «تمارين ومسائل عامة» ٤ (ب): ٦٫٣ لتر ، ٨٨٠ مل ، ٠٫٧ لتر.')))
S.append(slide(f'''{mode('u')}{timer(2)}''' + quiz('أصغر القياسات: ٣٢٥ م ، ٨٥٠ سم ، ٢ كم', [M('٣٢٥ م'), M('٨٥٠ سم'), M('٢ كم')], 1, '٨٥٠ سم = ٨٫٥ م، وهي أصغر من ٣٢٥ م ومن ٢ كم (٢٠٠٠ م)')))

# ═══ ٣ الاختيار والتقدير ═══
S.append(SEC(3, 'اختيار الوحدة المناسبة والتقدير', '٤-٢', ['شيءٌ صغير ← وحدةٌ صغيرة، وشيءٌ كبير ← وحدةٌ كبيرة', 'نقدّر بأشياء نعرف قياسها، ونحكم على المعقولية']))
S.append(slide(f'''{RULE(3, 'نختار الوحدة التي تجعل العدد معقولاً، ونقدّر بمقارنة الشيء <b>بأشياء نعرف قياسها</b>')}
<div class="bms">{''.join(st(f'<div><span>{ic}</span><small>{n}</small><b>{v}</b></div>') for ic, n, v in (('🧍', 'طول الرجل', '١٫٧ م'), ('🚪', 'ارتفاع الباب', '٢ م'), ('🧑', 'شخص بالغ', '٧٥ كغم'), ('🥄', 'ملعقة شاي', '٥ مل')))}</div>'''))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('تمرين ٨')}</div><h2>عمود الإنارة ٢٫٥ مرة قدر طول منى</h2>
<div class="row vrow">{STEPS(STP('١) طول منى', M('١٫٦ م', cls='sm')), STP('٢) نضرب في ٢٫٥', M('١٫٦', X, '٢٫٥', cls='sm')), STP('٣) الناتج بوحدته', M('٤ م', cls='sm'), 'fin'))}</div>'''))
S.append(slide(f'''{mode('u')}{timer(1)}''' + quiz('«ارتفاع المطبخ ٢ م»: هل التقدير منطقي؟', ['✔ نعم', '✘ لا'], 1, 'ارتفاع الباب وحده حوالي ٢ م، والمطبخ عادةً بين ٣ و ٣٫٥ م')))

# ═══ «يجب أن تكون قادراً على» — تقييمٌ ذاتي ═══
SK = ['استخدام اختصارات وحدات الطول والكتلة والسعة', 'التحويل بين الكيلومتر والمتر والسنتيمتر والمليمتر', 'التحويل بين الطن والكيلوغرام والغرام',
      'التحويل بين اللتر والمليلتر', 'اختيار وحدات القياس المناسبة واستخدامها في التقدير', 'حلّ مشكلاتٍ من الحياة اليومية بالقياسات', 'العمل بطريقةٍ منطقية والتوصّل إلى استنتاجاتٍ بسيطة']
def CHECK(items, start):
    return ''.join(f'<button class="ck"><span class="cb">{a(start + i)}</span><span>{t}</span></button>' for i, t in enumerate(items))
CKJS = "<script>document.querySelectorAll('.ck').forEach(function(b){b.onclick=function(e){e.stopPropagation();b.classList.toggle('ok');};});</script>"
for k in range(0, len(SK), 4):
    last = k + 4 >= len(SK)
    S.append(slide(f'''<div class="row hdr"><span class="qbadge">تقييمٌ ذاتي ✅</span><span class="tag">اضغط على ما تتقنه ليصبح أخضر</span></div><h2>يجب أن أكون قادراً على… ({a(k // 4 + 1)})</h2>
<div class="cks">{CHECK(SK[k:k+4], k + 1)}</div>{CKJS if last else ''}'''))
S.append(slide(f'''<h2>أحسنتم! 🎉</h2>
<div class="note">راجعوا ورقة ملخّص الوحدة، وحلّوا «تمارين ومسائل عامة» ص ٨٨</div>
<p class="hint st">المرجع: كتاب الطالب، صفحة ملخّص الوحدة الرابعة · إعداد: أ. عيسى الحارثي</p>'''))

# ═══ ملحق: «تمارين ومسائل عامة» ص٨٨ (الإجابات من دليل المعلم ص٩١) ═══
S.append(launch('sb', '٨٨', note='تمارين ومسائل عامة: الإجابات من دليل المعلم ص ٩١ (مع تصحيح ترتيب ٤ (أ))'))
H = ['أ', 'ب', 'ج', 'د', 'هـ', 'و']
def L(items): return [(f'({h}) {q}', r) for h, (q, r) in zip(H, items)]
S.append(ex(1, 'حوّل الأطوال', 'إلى وحدةٍ أصغر نضرب، وإلى وحدةٍ أكبر نقسم', L([('٧٥ ملم = ☐ سم', '٧٫٥<small>٧٥ ÷ ١٠</small>'), ('١٫٢ كم = ☐ م', '١٢٠٠<small>١٫٢ × ١٠٠٠</small>'), ('١٢٠ سم = ☐ م', '١٫٢<small>١٢٠ ÷ ١٠٠</small>')]), cols=1, per=3))
S.append(ex(2, 'حوّل الكتل', 'معامل التحويل ١٠٠٠', L([('٢٠٠٠ كغم = ☐ طن', '٢<small>٢٠٠٠ ÷ ١٠٠٠</small>'), ('٣٫٢ كغم = ☐ غم', '٣٢٠٠<small>٣٫٢ × ١٠٠٠</small>'), ('٠٫٢٥ طن = ☐ كغم', '٢٥٠<small>٠٫٢٥ × ١٠٠٠</small>')]), cols=1, per=3))
S.append(ex(3, 'حوّل السعات', '١٠٠٠ مل = ١ لتر', L([('٨٠٠٠ مل = ☐ لتر', '٨<small>٨٠٠٠ ÷ ١٠٠٠</small>'), ('٤٫٢ لتر = ☐ مل', '٤٢٠٠<small>٤٫٢ × ١٠٠٠</small>'), ('٦٥٠ مل = ☐ لتر', '٠٫٦٥<small>٦٥٠ ÷ ١٠٠٠</small>')]), cols=1, per=3))
S.append(ex(4, 'رتّب تصاعدياً', 'نوحّد الوحدات، ثم نكتب الوحدات الأصلية', L([('٣٢٥ م ، ٨٥٠ سم ، ٢٫٠ كم', '٨٥٠ سم ، ٣٢٥ م ، ٢٫٠ كم<small>٨٫٥ م ، ٣٢٥ م ، ٢٠٠٠ م</small>'), ('٦٫٣ لتر ، ٨٨٠ مل ، ٠٫٧ لتر', '٠٫٧ لتر ، ٨٨٠ مل ، ٦٫٣ لتر<small>٧٠٠ مل ، ٨٨٠ مل ، ٦٣٠٠ مل</small>')]), cols=1,
  note='في الكتاب «تصاعدياً (من الأكبر إلى الأصغر)»، والتصاعدي من الأصغر إلى الأكبر كما في إجابة الدليل لـ (ب). وفي إجابة الدليل لـ (أ) «٨٥٠ سم ، ٢٫٠ كم ، ٣٢٥ م»، والصحيح ٣٢٥ م قبل ٢ كم.'))
S.append(ex(5, 'أيّ القياسات أكثر ملاءمة؟', 'نقارن بأشياء نعرف قياسها', L([('طول قدم الرجل: ٣٠ ملم ، ٣ م ، ٣٠ سم', 'ج) ٣٠ سم'), ('كتلة الكرسي: ٩ كغم ، ٩٠ غم ، ٠٫٩ طن', 'أ) ٩ كغم'), ('سعة وعاء الطهي: ١٫٨ مل ، ١٫٥ لتر ، ١٥ مل', 'ب) ١٫٥ لتر'), ('ارتفاع الطاولة: ٧٥ سم ، ٧٫٥ ملم ، ٧٥٠ م', 'أ) ٧٥ سم')]), cols=2))
S.append(ex(6, 'حدّد وحدة القياس المناسبة', 'شيءٌ صغير ← وحدةٌ صغيرة', L([('طول موقف السيارة', 'م'), ('طول رمش العين', 'ملم'), ('كتلة الدراجة النارية', 'كغم'), ('كتلة علبة الأقلام', 'غم'), ('سعة كأس العصير', 'مل'), ('سعة خزّان الماء', 'لتر')]), cols=2))
S.append(ex(7, 'مطبخ عايدة', 'ارتفاع الباب حوالي ٢ م', [('ارتفاع المطبخ ٢ م: هل التقدير مناسب؟', 'لا<small>الباب وحده حوالي ٢ م، والمطبخ عادةً بين ٣ و ٣٫٥ م</small>')], cols=1))
S.append(ex(8, 'عمود الإنارة', '٢٫٥ مرة قدر طولها: نضرب', [('طول منى ١٫٦ م، والعمود ٢٫٥ مرة قدر طولها', '١٫٦ × ٢٫٥ = ٤ م')], cols=1))
S.append(ex(9, 'المصعد', 'البالغ ٧٠ إلى ٨٠ كغم، والطفل ١٠ إلى ٣٠ كغم', [('٨ بالغين و ٦ أطفال: قدّر كتلتهم الإجمالية', '٦٢٠ إلى ٨٢٠ كغم<small>٨ × (٧٠ إلى ٨٠) + ٦ × (١٠ إلى ٣٠)</small>')], cols=1))
S.append(ex(10, 'الرجل والشجرة', 'نعدّ كم مرةً يتكرّر طول الرجل', [(FIG('u4_tree', 'fig side') + 'قدّر ارتفاع الشجرة', '١٠ أو ١١ م تقريباً<small>٦ × (١٫٧ إلى ١٫٨ م) = ١٠٫٢ إلى ١٠٫٨ م</small>')], cols=1))

EXTRA_CSS_OWN = FIG_CSS + '''
.stps{display:flex;flex-direction:column;gap:1.2vh;align-items:stretch}
.stp{display:flex;align-items:center;gap:1.4vw;justify-content:space-between}
.stp .lab{flex:0 1 auto;max-width:55%;font-family:var(--fh);font-weight:800;color:#2563EB;background:#EAF1FF;border-radius:12px;padding:.2em .8em;text-align:center;line-height:1.4;font-size:clamp(20px,3.5vh,40px)}
.stp.fin .lab{background:var(--good);color:#fff}
.slide .vrow{align-items:center;justify-content:center;gap:2vh 3vw;flex-wrap:wrap}
.slide .vrow>.stps{flex:0 1 auto;max-width:min(1200px,80vw)}
@media (max-aspect-ratio:1/1){.slide .vrow{flex-direction:column}.slide .vrow>.stps{max-width:92vw}.stp{flex-wrap:wrap;justify-content:center}}
.rulecard{display:flex;align-items:center;gap:1em;background:#fff;border:3px solid var(--ink);border-radius:20px;padding:1.4vh 1.6vw;width:min(1300px,92vw);font-weight:700;font-size:clamp(22px,4vh,46px);line-height:1.5;box-shadow:0 7px 0 #DCE5F0}
.rulecard .rn{flex:none;font-family:var(--fh);font-weight:900;background:var(--ink);color:#fff;border-radius:14px;padding:.2em .7em;font-size:.8em}
.cks{display:flex;flex-direction:column;gap:1.2vh;width:min(1300px,92vw)}
.ck{display:flex;align-items:center;gap:1em;text-align:start;font-family:var(--fb);font-weight:700;font-size:clamp(24px,4.4vh,50px);background:#fff;border:2.5px solid var(--line);border-radius:14px;padding:1vh 1.4vw;cursor:pointer;color:var(--ink);line-height:1.4}
.ck .cb{flex:none;width:1.6em;height:1.6em;border-radius:50%;background:#EEF2F7;display:flex;align-items:center;justify-content:center;font-family:var(--fh)}
.ck.ok{border-color:var(--good);background:#F2FBF5}.ck.ok .cb{background:var(--good);color:#fff}
.bms{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:1.4vw;width:min(1500px,94vw)}
.bms .st>div{display:flex;flex-direction:column;align-items:center;gap:.4vh;background:#fff;border:3px solid var(--base);border-radius:18px;padding:1.4vh .6vw;text-align:center}
.bms span{font-size:clamp(46px,9vh,104px);line-height:1.1}.bms small{font-weight:800;font-size:clamp(20px,3.6vh,40px);color:var(--ink2)}.bms b{font-family:var(--fh);font-size:clamp(28px,5.4vh,62px);color:var(--base)}
.slide .svgfig.stair{width:auto;height:min(60vh,600px);max-width:92vw;max-height:none}
.slide .stairs{gap:2vw;flex-wrap:wrap;justify-content:center}.slide .stairs .svgfig.stair{height:min(48vh,480px);max-width:46vw}
.xa small{display:block}
@media (max-aspect-ratio:1/1){.bms{grid-template-columns:repeat(2,minmax(0,1fr))}.slide .stairs .svgfig.stair{max-width:92vw;height:min(34vh,340px)}}
'''
