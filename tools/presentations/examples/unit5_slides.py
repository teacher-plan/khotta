# عرض مراجعة «الوحدة الخامسة: الزوايا» — الصف السابع.
# المرجع: صفحة ملخّص الوحدة في كتاب الطالب ص١٠١ («يجب أن تعرف أنّ» + «يجب أن تكون قادراً على»)، و«تمارين ومسائل عامة» ص١٠٢
# (إجابات دليل المعلم ص١٠٤).
# python3.12 gen_powers.py unit5_slides.py مراجعة_الوحدة_الخامسة_عرض_تفاعلي.html "مراجعة الوحدة الخامسة — الصف السابع"
# لكل جزء: بطاقة القاعدة ← رسمٌ ومثالٌ محلول بخطوات ← سؤالٌ سريع (أنتم).
exec(open(os.path.join(HERE, 'figs.py'), encoding='utf-8').read())
DV = '<span class="x">÷</span>'; MI = '<span class="x">−</span>'; PL = '<span class="x">+</span>'
def STP(lab, expr='', cls=''): return st(f'<div class="stp {cls}"><span class="lab">{lab}</span>{expr}</div>')
def STEPS(*rows): return '<div class="stps">' + ''.join(rows) + '</div>'
def RULE(n, t): return f'<div class="rulecard"><span class="rn">قاعدة {a(n)}</span><span>{t}</span></div>'
def AT(svg, cap): return st(f'<div class="atile">{svg}<b>{cap}</b></div>')
NP = 4
def SEC(n, title, lesson, items):
    return slide(f'''<span class="tag">الجزء {a(n)} من {a(NP)} · الدرس {lesson}</span><h2>{title}</h2>
<div class="exit">{''.join(st(f'<div><b>{a(i + 1)}</b><span>{t}</span></div>') for i, t in enumerate(items))}</div>''', 'divider')

S = []
S.append(slide('''<span class="tag">الصف السابع · مراجعة الوحدة الخامسة</span>
<h1 class="h1s">الزوايا</h1>
<p class="lead" style="font-size:clamp(26px,4.8vh,56px)">إعداد: أ. عيسى الحارثي</p>''', 'cover'))
S.append(slide('''<h2>نراجع الوحدة كلّها في أربعة أجزاء</h2>
<div class="can">
<div><span class="can-i">١</span><span>أنواع الزوايا وتسميتها وتقديرها</span></div>
<div><span class="can-i">٢</span><span>حقائق الزوايا: النقطة والخط والمثلث والرباعي</span></div>
<div><span class="can-i">٣</span><span>المتقابلة بالرأس والمثلث متطابق الضلعين</span></div>
<div><span class="can-i">٤</span><span>الخطوط المتوازية: المتناظرة والمتبادلة</span></div></div>'''))

# ═══ ١ الأنواع ═══
S.append(SEC(1, 'أنواع الزوايا وتسميتها', '٥-١', ['حادّة، قائمة، منفرجة، مستقيمة، منعكسة', 'الحرف الأوسط في الاسم هو الرأس']))
S.append(slide(f'''{RULE(1, 'حادّة &lt; ٩٠° · قائمة = ٩٠° · منفرجة بين ٩٠° و ١٨٠° · منعكسة بين ١٨٠° و ٣٦٠°')}
<div class="row atiles">{AT(ANG(40, 10, size=240), 'حادّة')}{AT(ANG(90, 15, size=240), 'قائمة')}{AT(ANG(130, 15, size=240), 'منفرجة')}{AT(ANG(60, 20, reflex=True, size=240), 'منعكسة')}</div>'''))
S.append(slide(f'''{mode('u')}{timer(1)}''' + quiz('زاويةٌ قياسها ٢٤٠° هي…', ['منفرجة', 'منعكسة', 'مستقيمة'], 1, 'بين ١٨٠° و ٣٦٠°')))
S.append(slide(f'''{mode('u')}{timer(1)}''' + quiz('زاويةٌ ٧٠°: ما قياس المنعكسة؟', [M('٢٩٠°'), M('١١٠°'), M('٢٧٠°')], 0, '٣٦٠ − ٧٠ = ٢٩٠°')))

# ═══ ٢ الحقائق ═══
S.append(SEC(2, 'حقائق الزوايا', '٥-٢', ['حول نقطة ٣٦٠° · على خطٍّ مستقيم ١٨٠°', 'المثلث ١٨٠° · رباعي الأضلاع ٣٦٠°']))
S.append(slide(f'''{RULE(2, 'نحدّد الحقيقة ومجموعها، <b>نجمع المعلوم</b> ثم <b>نطرحه من المجموع</b>')}
<div class="row vrow">{STEPS(STP('١) زاويتان في مثلث: ٤٥° و ٧٥°', M('١٨٠', MI, '١٢٠', EQ, '٦٠°', cls='sm')), STP('٢) ثلاث في رباعي: ٧٢° و ٩٧° و ١١٣°', M('٣٦٠', MI, '٢٨٢', EQ, '٧٨°', cls='sm')), STP('٣) ثلاث متساوية في رباعي، كلٌّ ٧٧°', M('٣٦٠', MI, '٢٣١', EQ, '١٢٩°', cls='sm'), 'fin'))}</div>''' + tn('من «تمارين ومسائل عامة» ٢ (أ) و ٣ (أ) و ٣ (ج).')))
S.append(slide(f'''{mode('u')}{timer(2)}''' + quiz('هل يمكن أن يكون لرباعي أربع زوايا حادّة؟', ['✔ نعم', '✘ لا'], 1, 'مجموعها يكون أصغر من ٣٦٠°')))

# ═══ ٣ المتقابلة بالرأس ومتطابق الضلعين ═══
S.append(SEC(3, 'المتقابلة بالرأس ومتطابق الضلعين', '٥-٣', ['المتقابلتان بالرأس متساويتان', 'في متطابق الضلعين زاويتا القاعدة متساويتان']))
S.append(slide(f'''{RULE(3, 'المتقابلتان بالرأس <b>متساويتان</b>، وإذا تساوت زاويتان في مثلثٍ فهو <b>متطابق الضلعين</b>')}
<div class="row vrow">{st(XL(70, labels=('١١٠°', 'ب', 'ج', 'ء')))}{STEPS(STP('ج تقابل ١١٠°', M('١١٠°', cls='sm')), STP('ب على خطٍّ مستقيم', M('١٨٠', MI, '١١٠', EQ, '٧٠°', cls='sm')), STP('ء تقابل ب', M('٧٠°', cls='sm'), 'fin'))}</div>'''))
S.append(slide(f'''{mode('u')}{timer(1)}''' + quiz('أيّ المثلثات متطابق الضلعين؟ زاويتان فيه…', [M('٥٤° و ٥٤°'), M('٤٥° و ٧٥°'), M('٨° و ١١°')], 0, 'زاويتان متساويتان (والثالثة ٧٢°)')))

# ═══ ٤ المتوازية ═══
S.append(SEC(4, 'الخطوط المتوازية', '٥-٤', ['المتناظرة (F) متساوية', 'المتبادلة (Z) متساوية']))
S.append(slide(f'''{RULE(4, 'عند خطّين متوازيين وقاطع: <b>المتناظرة</b> متساوية، و<b>المتبادلة</b> متساوية')}
<div class="row vrow">{st(PAR([(0, 4)], shape='F'))}{st(PAR([(2, 4)], shape='Z'))}</div>'''))
S.append(slide(f'''{RULE(4, 'زاويةٌ واحدة تكفي لمعرفة الزوايا الثماني')}
<div class="row vrow">{st(FIG('u5_e5', 'fig'))}{STEPS(STP('١) ل تقابل ٧٥° بالرأس', M('٧٥°', cls='sm')), STP('٢) المجاورة على خطٍّ مستقيم', M('١٠٥°', cls='sm')), STP('٣) ن تناظرها', M('١٠٥°', cls='sm'), 'fin'))}</div>''' + tn('من «تمارين ومسائل عامة» ٥؛ إجابة الدليل: ل = ٧٥°، ن = ١٠٥°.')))
S.append(slide(f'''{mode('u')}{timer(1)}''' + quiz('المتبادلتان عند خطّين متوازيين…', ['متساويتان', 'مجموعهما ١٨٠°', 'مجموعهما ٣٦٠°'], 0, 'شكل Z: متساويتان')))

# ═══ تقييمٌ ذاتي ═══
SK = ['تسمية الخطوط والزوايا والأشكال بالرموز', 'تقدير قياس الزوايا وقياسها بالمنقلة', 'حساب الزوايا حول نقطة وعلى خطٍّ مستقيم وفي المثلث',
      'إثبات أن الزاويتين المتقابلتين بالرأس متساويتان', 'مجموع زوايا رباعي الأضلاع ٣٦٠°', 'إيجاد قياسات الزوايا وشرح طريقة الوصول',
      'العلاقات بين الزوايا عند قطع مستقيمٍ لخطوطٍ متوازية', 'تحديد الزوايا المتبادلة والمتناظرة']
def CHECK(items, start):
    return ''.join(f'<button class="ck"><span class="cb">{a(start + i)}</span><span>{t}</span></button>' for i, t in enumerate(items))
CKJS = "<script>document.querySelectorAll('.ck').forEach(function(b){b.onclick=function(e){e.stopPropagation();b.classList.toggle('ok');};});</script>"
for k in range(0, len(SK), 4):
    last = k + 4 >= len(SK)
    S.append(slide(f'''<div class="row hdr"><span class="qbadge">تقييمٌ ذاتي ✅</span><span class="tag">اضغط على ما تتقنه ليصبح أخضر</span></div><h2>يجب أن أكون قادراً على… ({a(k // 4 + 1)})</h2>
<div class="cks">{CHECK(SK[k:k+4], k + 1)}</div>{CKJS if last else ''}'''))
S.append(slide(f'''<h2>أحسنتم! 🎉</h2>
<div class="note">راجعوا ورقة ملخّص الوحدة، وحلّوا «تمارين ومسائل عامة» ص ١٠٢</div>
<p class="hint st">المرجع: كتاب الطالب، صفحة ملخّص الوحدة الخامسة · إعداد: أ. عيسى الحارثي</p>'''))

# ═══ ملحق: «تمارين ومسائل عامة» ص١٠٢ (الإجابات من دليل المعلم ص١٠٤) ═══
S.append(launch('sb', '١٠٢', note='تمارين ومسائل عامة: الإجابات من دليل المعلم ص ١٠٤'))
H = ['أ', 'ب', 'ج', 'د']
def L(items): return [(f'({h}) {q}', r) for h, (q, r) in zip(H, items)]
S.append(ex(1, 'احسب قياس كل زاوية', 'المثلث ١٨٠° · المنعكسة = ٣٦٠° − الزاوية', [(FIG('u5_e1', 'fig side') + '(أ) (أ ء ج)', '٧٠°<small>٤٠ + ٣٠: في المثلث هـ ء ج: ١٨٠ − ١٠٠ − ٥٠ = ٣٠°</small>'), ('(ب) (ء ب ج)', '٥٠°<small>١٨٠ − ٨٠ − ٥٠</small>'), ('(ج) (أ هـ ب) المنعكسة', '٢٦٠°<small>٣٦٠ − ١٠٠</small>'), ('(د) (ب ج ء)', '١٠٠°<small>٥٠ + ٥٠</small>')], cols=2))
S.append(ex(2, 'الزاوية الثالثة في المثلث', 'مجموع زوايا المثلث ١٨٠°', L([('٤٥° و ٧٥°', '٦٠°'), ('٨° و ١١°', '١٦١°'), ('٥٤° و ٥٤°', '٧٢°<small>متطابق الضلعين</small>'), ('١٣٨° و ٢١°', '٢١°<small>متطابق الضلعين</small>')]), cols=2, note='(ب) المثلثان (ج) و(د) لهما ضلعان متطابقان، لأن في كلٍّ منهما زاويتين متساويتين.'))
S.append(ex(3, 'الزاوية الرابعة في الرباعي', 'مجموع زوايا رباعي الأضلاع ٣٦٠°', L([('٧٢° و ٩٧° و ١١٣°', '٧٨°'), ('٥٥° و ٥٥° و ١٥٥°', '٩٥°'), ('ثلاث زوايا كلٌّ منها ٧٧°', '١٢٩°<small>٣٦٠ − ٢٣١</small>')]), cols=1, per=3))
S.append(ex(4, 'هل يمكن لرباعي أن يكون له…؟', 'مجموع زواياه ٣٦٠° بالضبط', L([('أربع زوايا حادّة', 'لا<small>مجموعها أصغر من ٣٦٠°</small>'), ('ثلاث زوايا منفرجة', 'نعم<small>مثل ١٠٠° و ١٠٠° و ١٠٠° و ٦٠°</small>'), ('زاوية واحدة منعكسة', 'نعم<small>مثل ٢٤٠° و ٥٠° و ٣٥° و ٣٥°</small>'), ('زاويتان منعكستان', 'لا<small>مجموعهما وحدهما أكبر من ٣٦٠°</small>')]), cols=2))
S.append(ex(5, 'أب و ء ج متوازيان', 'المتقابلة بالرأس والمتناظرة متساوية', [(FIG('u5_e5', 'fig side') + 'ل و ن', 'ل = ٧٥°<small>ن = ١٠٥°</small>')], cols=1))
S.append(ex(6, 'أكمل', 'المتقابلة بالرأس · المتناظرة · المتبادلة · مجموعهما ١٨٠°', [(FIG('u5_e6', 'fig side') + 'الأجزاء الأربعة', '(أ) هـ ، (ب) و ، (ج) ج<small>(د) ء أو و أو ب أو ع</small>')], cols=1, note='(أ) ج وَ هـ بالرأس · (ب) ع وَ و متناظرتان · (ج) س وَ ج متبادلتان · الحرف «ج» عند التقاطع السفلي يشبه «ع».'))
S.append(ex(7, 'أوجد أ و ب و ج و ء', 'نبدأ بـ ٤٥° ونطبّق الحقائق', [(FIG('u5_e7', 'fig side') + 'الزوايا الأربع', 'أ = ٤٥° (متناظرة) ، ب = ٤٥° (بالرأس)<small>ج = ٤٥° (بالرأس) ، ء = ١٣٥° (على خطٍّ مستقيم)</small>')], cols=1))

EXTRA_CSS_OWN = FIG_CSS + '''
.stps{display:flex;flex-direction:column;gap:1.2vh;align-items:stretch}
.stp{display:flex;align-items:center;gap:1.4vw;justify-content:space-between}
.stp .lab{flex:0 1 auto;max-width:55%;font-family:var(--fh);font-weight:800;color:#2563EB;background:#EAF1FF;border-radius:12px;padding:.2em .8em;text-align:center;line-height:1.4;font-size:clamp(20px,3.5vh,40px)}
.stp.fin .lab{background:var(--good);color:#fff}
.slide .vrow{align-items:center;justify-content:center;gap:2vh 3vw;flex-wrap:wrap}
.slide .vrow>.stps{flex:0 1 auto;max-width:min(1200px,80vw)}
@media (max-aspect-ratio:1/1){.atiles{flex-wrap:wrap}.slide .vrow{flex-direction:column}.slide .vrow>.stps{max-width:92vw}.stp{flex-wrap:wrap;justify-content:center}}
.rulecard{display:flex;align-items:center;gap:1em;background:#fff;border:3px solid var(--ink);border-radius:20px;padding:1.4vh 1.6vw;width:min(1300px,92vw);font-weight:700;font-size:clamp(22px,4vh,46px);line-height:1.5;box-shadow:0 7px 0 #DCE5F0}
.rulecard .rn{flex:none;font-family:var(--fh);font-weight:900;background:var(--ink);color:#fff;border-radius:14px;padding:.2em .7em;font-size:.8em}
.cks{display:flex;flex-direction:column;gap:1.2vh;width:min(1300px,92vw)}
.ck{display:flex;align-items:center;gap:1em;text-align:start;font-family:var(--fb);font-weight:700;font-size:clamp(24px,4.4vh,50px);background:#fff;border:2.5px solid var(--line);border-radius:14px;padding:1vh 1.4vw;cursor:pointer;color:var(--ink);line-height:1.4}
.ck .cb{flex:none;width:1.6em;height:1.6em;border-radius:50%;background:#EEF2F7;display:flex;align-items:center;justify-content:center;font-family:var(--fh)}
.ck.ok{border-color:var(--good);background:#F2FBF5}.ck.ok .cb{background:var(--good);color:#fff}
.bms{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:1.4vw;width:min(1500px,94vw)}
.bms .st>div{display:flex;flex-direction:column;align-items:center;gap:.4vh;background:#fff;border:3px solid var(--base);border-radius:18px;padding:1.4vh .6vw;text-align:center}
.bms span{font-size:clamp(46px,9vh,104px);line-height:1.1}.bms small{font-weight:800;font-size:clamp(20px,3.6vh,40px);color:var(--ink2)}.bms b{font-family:var(--fh);font-size:clamp(28px,5.4vh,62px);color:var(--base)}
.slide .svgfig.ang{width:auto;height:min(70vh,680px);max-width:44vw;max-height:none}
.atiles{gap:1.6vw;justify-content:center;flex-wrap:nowrap}.atiles .svgfig.ang{max-width:21vw;height:min(68vh,640px)}
.atile{display:flex;flex-direction:column;align-items:center;gap:.6vh;background:#fff;border:3px solid var(--line);border-radius:18px;padding:1vh 1vw}.atile b{font-family:var(--fh);font-size:clamp(20px,3.6vh,40px)}
.slide .vrow .fig{height:min(80vh,760px);width:auto;max-width:52vw;max-height:none}
.xq .fig.side{height:62vh;max-height:none;max-width:60vw;width:auto}.xa .fig.lg{height:auto;width:96%;max-width:none;max-height:none}
.slide .stairs{gap:2vw;flex-wrap:wrap;justify-content:center}.slide .stairs .svgfig.stair{height:min(48vh,480px);max-width:46vw}
.xa small{display:block}
@media (max-aspect-ratio:1/1){.atiles{flex-wrap:wrap}.bms{grid-template-columns:repeat(2,minmax(0,1fr))}.slide .stairs .svgfig.stair{max-width:92vw;height:min(34vh,340px)}}
'''
