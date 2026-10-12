# عرض مراجعة «الوحدة السابعة: المساحة والمحيط» — الصف السابع.
# المرجع: صفحة ملخّص الوحدة في كتاب الطالب ص١٤٣ («يجب أن تعرف أنّ» + «يجب أن تكون قادراً على»)، و«تمارين ومسائل عامة» ص١٤٤–١٤٥
# (إجابات دليل المعلم ص١٤٦).
# python3.12 gen_powers.py unit7_slides.py مراجعة_الوحدة_السابعة_عرض_تفاعلي.html "مراجعة الوحدة السابعة — الصف السابع"
# لكل جزء: بطاقة القاعدة ← رسمٌ ومثالٌ محلول بخطوات ← سؤالٌ سريع (أنتم).
exec(open(os.path.join(HERE, 'area_common.py'), encoding='utf-8').read())
MI = '<span class="x">−</span>'
def RULE(n, t): return f'<div class="rulecard"><span class="rn">قاعدة {a(n)}</span><span>{t}</span></div>'
NP = 5
def SEC(n, title, lesson, items):
    return slide(f'''<span class="tag">الجزء {a(n)} من {a(NP)} · {lesson}</span><h2>{title}</h2>
<div class="exit">{''.join(st(f'<div><b>{a(i + 1)}</b><span>{t}</span></div>') for i, t in enumerate(items))}</div>''', 'divider')

S = []
S.append(slide('''<span class="tag">الصف السابع · مراجعة الوحدة السابعة</span>
<h1 class="h1s">المساحة والمحيط</h1>
<p class="lead" style="font-size:clamp(26px,4.8vh,56px)">إعداد: أ. عيسى الحارثي</p>''', 'cover'))
S.append(slide(f'''<div class="row hdr"><span class="qbadge" style="background:#B45309;box-shadow:0 4px 0 #7C2D12">تحدّي البداية 🏡</span>{timer(3)}</div><h2>غرفة سالم الجديدة</h2>
<div class="row vrow">{st(DRAW([('P', [(0, 0), (6, 0), (6, 4), (0, 4)], '#FDE68A'), ('T', 3, 4.7, '٦ م'), ('T', -0.9, 2, '٤ م'), ('T', 3, 2, 'أرضية الغرفة', '#92400E')], k=48, cls='svgfig shp lg'))}<div class="exit" style="width:auto;flex:1">{st('<div><b>🧱</b>كم متراً من الوزرة الخشبية حول أرضية الغرفة؟</div>')}{st('<div><b>🧶</b>وكم متراً مربّعاً من السجاد يغطّي أرضيتها؟</div>')}{st('<div><b>🪟</b>وفوق الباب نافذةٌ نصف دائرية قطرها ٣ م: ما مساحة زجاجها؟</div>')}</div></div>''' + tn('تمهيدٌ من إعدادي (من خارج المرجع) يجمع موضوعات الوحدة في موقفٍ واحد، ونحلّه في آخر العرض: المحيط ٢٠ م ، المساحة ٢٤ م² ، الزجاج ½ × ٣٫١٤ × ١٫٥² ≈ ٣٫٥٣ م².')))
S.append(slide('''<h2>نراجع الوحدة كلّها في خمسة أجزاء</h2>
<div class="can">
<div><span class="can-i">١</span><span>وحدات قياس المساحة والتحويل بينها</span></div>
<div><span class="can-i">٢</span><span>مساحة المستطيل ومحيطه</span></div>
<div><span class="can-i">٣</span><span>مساحة المثلث ومتوازي الأضلاع وشبه المنحرف</span></div>
<div><span class="can-i">٤</span><span>محيط الدائرة ومساحتها</span></div>
<div><span class="can-i">٥</span><span>مساحة الأشكال المركّبة</span></div></div>'''))

# ═══ ١ ═══
S.append(SEC(1, 'وحدات المساحة', 'الدرس ٧-١', ['المساحة تُقاس بوحداتٍ مربّعة: ملم² ، سم² ، م² ، كم²', 'نضرب عند التحويل إلى وحدةٍ أصغر، ونقسم عند التحويل إلى وحدةٍ أكبر']))
S.append(slide(f'''{RULE(1, '١ سم² = ١٠٠ ملم² ، ١ م² = ١٠ ٠٠٠ سم² ، ١ كم² = ١ ٠٠٠ ٠٠٠ م²')}
{st(STAIR2(*AREA_STAIR))}''' + tn('من صفحة ملخّص الوحدة في الكتاب ص١٤٣: معاملات التحويل الخاصة بالمساحة.')))
S.append(slide(f'''{mode('u')}{timer(1)}''' + quiz('٥ م² = ؟ سم²', [M('٥٠ ٠٠٠', CM2), M('٥٠٠', CM2), M('٥٠', CM2)], 0, '٥ × ١٠ ٠٠٠ = ٥٠ ٠٠٠ (تمارين ومسائل عامة ٢ (ب))')))

# ═══ ٢ ═══
S.append(SEC(2, 'المستطيل', 'الدرس ٧-٢', ['المساحة = الطول × العرض (وحدةٌ مربّعة)', 'المحيط = ٢ × الطول + ٢ × العرض (وحدة طول)', 'نوحّد الوحدات قبل الحساب']))
S.append(slide(f'''{RULE(2, 'م = ل × ض ، ط = ٢ل + ٢ض')}
<div class="row vrow">{st(RECT('٥ سم', '٨ ملم', 400, 70, '#BAE6FD'))}{STEPS(STP('١) نوحّد: ٥ سم = ٥٠ ملم', ''), STP('٢) المساحة', M('٥٠', X, '٨', EQ, '٤٠٠', MM2)), STP('٣) المحيط', M('٢', X, '٥٠', PL, '٢', X, '٨', EQ, '١١٦ ملم'), 'fin'))}</div>''' + tn('تمارين ومسائل عامة ٣ (ج)؛ إجابة الدليل ص١٤٦: المساحة ٤٠٠ ملم² (أو ٤ سم²)، والمحيط ١١٦ ملم (أو ١١٫٦ سم).')))
S.append(slide(f'''{mode('u')}{timer(2)}''' + quiz('غرفةٌ مستطيلة مساحتها ٢٤ م² وطولها ٦ م. عرضها ومحيطها:', [M('٤ م ، ٢٠ م'), M('٤ م ، ١٠ م'), M('١٨ م ، ٤٨ م')], 0, '٢٤ ÷ ٦ = ٤ م ، ٢ × ٦ + ٢ × ٤ = ٢٠ م (تمارين ومسائل عامة ٤)')))

# ═══ ٣ ═══
S.append(SEC(3, 'المثلث ومتوازي الأضلاع وشبه المنحرف', 'الدرسان ٧-٣ و ٧-٤', ['الارتفاع دائماً عمودي على القاعدة', 'المثلث نصف المستطيل، ومتوازي الأضلاع مثل المستطيل، وشبه المنحرف نصف متوازي أضلاع']))
S.append(slide(f'''{RULE(3, 'المثلث: ½ ق ع · متوازي الأضلاع: ق ع · شبه المنحرف: ½ (ق١ + ق٢) ع')}
<div class="row vrow">{st(box('<b class="kk c-b">١٥ و ٨٫٨</b>' + TRI('', '', apex=.3, B=300, H=180, cls='svgfig shp sm') + M(HALF, X, '١٥', X, '٨٫٨', EQ, '٦٦'), 'col'))}{st(box('<b class="kk c-we">٧ و ٤</b>' + PARA('', '', slant=70, B=260, H=150, cls='svgfig shp sm') + M('٧', X, '٤', EQ, '٢٨'), 'col'))}{st(box('<b class="kk c-exp">١٦ و ٢٤ ، ع = ٨</b>' + TRAP('', '', '', B=300, T=200, off=50, H=160, cls='svgfig shp sm') + M(HALF, X, '٤٠', X, '٨', EQ, '١٦٠'), 'col'))}</div>''' + tn('تمارين ومسائل عامة ٥؛ إجابات الدليل ص١٤٦: ٦٦ سم² ، ٢٨ سم² ، ١٦٠ م².')))
S.append(slide(f'''{mode('u')}{timer(1)}''' + quiz('مثلثٌ قاعدته ١٠ سم وارتفاعه ٦ سم. مساحته:', [M('٣٠', CM2), M('٦٠', CM2), M('١٥', CM2)], 0, '½ × ١٠ × ٦ = ٣٠ سم² (لا ننسى التنصيف)')))

# ═══ ٤ ═══
S.append(SEC(4, 'الدائرة', 'الدرس ٧-٥', ['المحيط: ط = π ق = ٢ π نق', 'المساحة: م = π نق²، بنصف القطر دائماً', 'نتحقّق بالتقريب: π ≈ ٣']))
S.append(slide(f'''{RULE(4, 'ط = ٢ π نق ، م = π نق² ، ونتحقّق بـ π ≈ ٣')}
<div class="row vrow">{st(CIRC(130, ('r',), lab={'r': '٤ سم'}))}{STEPS(STP('المساحة', M('٣٫١٤', X, '١٦', EQ, '٥٠٫٢٤', '≈', '٥٠٫٢', CM2)), STP('المحيط', M('٢', X, '٣٫١٤', X, '٤', '≈', '٢٥٫١ سم')), STP('نتحقّق بـ ٣', M('٣', X, '٤²', EQ, '٤٨', '،', '٢', X, '٣', X, '٤', EQ, '٢٤'), 'fin'))}</div>''' + tn('تمارين ومسائل عامة ٦ (أ) و ٧ (أ)؛ إجابات الدليل ص١٤٦.')))
S.append(slide(f'''{mode('u')}{timer(2)}''' + quiz('قطعة رخامٍ دائرية محيطها ٤٨ سم. قطرها لأقرب منزلةٍ عشرية:', [M('١٥٫٣ سم'), M('٧٫٦ سم'), M('١٥٠٫٧ سم')], 0, 'ق = ط ÷ π = ٤٨ ÷ ٣٫١٤ ≈ ١٥٫٣ سم (تمارين ومسائل عامة ٨)')))

# ═══ ٥ ═══
S.append(SEC(5, 'الأشكال المركّبة', 'الدرس ٧-٦', ['نقسّم الشكل إلى أشكالٍ بسيطة', 'نجمع المساحات، أو نطرح مساحة التجويف']))
S.append(slide(f'''{RULE(5, 'نقسّم ← نوجد كل مساحة ← نجمع أو نطرح')}
<div class="row vrow">{st(DRAW([('P', [(0, 0), (8, 0), (8, 4), (0, 4)], '#BBF7D0'), ('H', 4, 0, 4, '#BBF7D0'), ('D', (0, 0), (8, 0)), ('T', 4, 4.7, '٨ سم'), ('T', 8.9, 2, '٤ سم')], k=36))}{STEPS(STP('١) المستطيل', M('٨', X, '٤', EQ, '٣٢')), STP('٢) نصف الدائرة (نق = ٤)', M(HALF, X, '٣٫١٤', X, '١٦', EQ, '٢٥٫١٢')), STP('٣) نجمع', M('٥٧٫١٢', CM2), 'fin'))}</div>''' + tn('تمارين ومسائل عامة ٩ (ب)؛ إجابة الدليل ص١٤٦: ٥٧٫١٢ سم².')))
S.append(slide(f'''{mode('u')}{timer(2)}''' + quiz('مستطيلٌ ١٥ سم × ١٠ سم فيه فتحةٌ مستطيلة ٦ سم × ٣ سم. مساحة الجزء الملوّن:', [M('١٣٢', CM2), M('١٦٨', CM2), M('١٥٠', CM2)], 0, '١٥٠ − ١٨ = ١٣٢ سم² (نطرح التجويف؛ تمارين ومسائل عامة ١٠)')))
S.append(slide(f'''<div class="row hdr"><span class="qbadge" style="background:#B45309;box-shadow:0 4px 0 #7C2D12">نحلّ تحدّي البداية 🏡</span></div><h2>غرفة سالم</h2>
{FLIPS([('<span class="hint">🧱 الوزرة = المحيط</span>', '٢٠ م', '٢ × ٦ + ٢ × ٤'), ('<span class="hint">🧶 السجاد = المساحة</span>', '٢٤ م²', '٦ × ٤'), ('<span class="hint">🪟 زجاج النافذة</span>', '≈ ٣٫٥٣ م²', '½ × ٣٫١٤ × ١٫٥²')])}''' + tn('إغلاق تحدّي البداية.')))

# ═══ تقييمٌ ذاتي ═══
SK = ['التحويل بين وحدات قياس المساحة، مثل م² و سم² و ملم²', 'استخدام المعادلات الخاصة بمساحة المستطيل ومحيطه', 'استنتاج المعادلات الخاصة بمساحة المثلث ومتوازي الأضلاع وشبه المنحرف واستخدامها',
      'حساب مساحة الأشكال المركّبة', 'التعرّف على الدائرة ومكوّناتها', 'معرفة المعادلات الخاصة بمحيط الدائرة ومساحتها واستخدامها', 'العمل بطريقةٍ منطقية والتوصّل إلى استنتاجاتٍ بسيطة']
def CHECK(items, start):
    return ''.join(f'<button class="ck"><span class="cb">{a(start + i)}</span><span>{t}</span></button>' for i, t in enumerate(items))
CKJS = "<script>document.querySelectorAll('.ck').forEach(function(b){b.onclick=function(e){e.stopPropagation();b.classList.toggle('ok');};});</script>"
for k in range(0, len(SK), 4):
    last = k + 4 >= len(SK)
    S.append(slide(f'''<div class="row hdr"><span class="qbadge">تقييمٌ ذاتي ✅</span><span class="tag">اضغط على ما تتقنه ليصبح أخضر</span></div><h2>يجب أن أكون قادراً على… ({a(k // 4 + 1)})</h2>
<div class="cks">{CHECK(SK[k:k+4], k + 1)}</div>{CKJS if last else ''}'''))
S.append(slide(f'''<h2>أحسنتم! 🎉</h2>
<div class="note">راجعوا ورقة ملخّص الوحدة، وحلّوا «تمارين ومسائل عامة» ص ١٤٤ و ١٤٥</div>
<p class="hint st">المرجع: كتاب الطالب، صفحة ملخّص الوحدة السابعة ص ١٤٣ · إعداد: أ. عيسى الحارثي</p>'''))

# ═══ ملحق: «تمارين ومسائل عامة» ص١٤٤–١٤٥ (الإجابات من دليل المعلم ص١٤٦) ═══
S.append(launch('sb', '١٤٤ و ١٤٥', note='تمارين ومسائل عامة: الإجابات من دليل المعلم ص ١٤٦'))
H = PARTS
def L(items): return [(f'({h}) {q}', r) for h, (q, r) in zip(H, items)]
S.append(ex(1, 'الوحدات المناسبة لقياس المساحة', 'شيءٌ كبير ← وحدةٌ كبيرة', L([('ملعب هوكي', 'م²'), ('غلاف كتاب', 'سم²')]), cols=2))
S.append(ex(2, 'أكمل', 'نضرب نزولاً ونقسم صعوداً: ١٠٠ ، ١٠ ٠٠٠', L([('٨ سم² = ؟ ملم²', '٨٠٠'), ('٥ م² = ؟ سم²', '٥٠ ٠٠٠'), ('٤٢٠ ملم² = ؟ سم²', '٤٫٢')]), cols=3))
S.append(ex(3, 'مساحة المستطيل ومحيطه', 'م = ل × ض ، ط = ٢ل + ٢ض', L([(RECT('٦ سم', '٥ سم', 260, 210, '#FDBA74', cls='svgfig shp', fs=36), '٣٠ سم² ، ٢٢ سم'), (RECT('٧ م', '٣ م', 300, 130, '#FEF08A', cls='svgfig shp', fs=36), '٢١ م² ، ٢٠ م'), (RECT('٥ سم', '٨ ملم', 340, 60, '#BAE6FD', cls='svgfig shp', fs=36), '٤٠٠ ملم² ، ١١٦ ملم<small>أو ٤ سم² ، ١١٫٦ سم</small>')]), cols=3))
S.append(ex(4, 'الغرفة', 'العرض = المساحة ÷ الطول', L([('مساحتها ٢٤ م² وطولها ٦ م: عرضها', '٤ م'), ('محيطها', '٢٠ م')]), cols=2))
S.append(ex(5, 'مساحة كل شكل', 'المثلث ½ ق ع ، متوازي الأضلاع ق ع ، شبه المنحرف ½ (ق١ + ق٢) ع', L([(TRI('١٥ سم', '٨٫٨ سم', apex=.3, B=330, H=190, cls='svgfig shp', fs=36), '٦٦ سم²'), (PARA('٧ سم', '٤ سم', slant=90, B=280, H=150, fill='#FED7AA', cls='svgfig shp', fs=36), '٢٨ سم²'), (TRAP('١٦ م', '٢٤ م', '٨ م', B=330, T=220, off=55, H=170, fill='#FBCFE8', cls='svgfig shp', fs=36), '١٦٠ م²')]), cols=3))
S.append(ex(6, 'مساحة الدائرة ومحيطها', 'م = π نق² ، ط = ٢ π نق ، π = ٣٫١٤', L([('نق = ٤ سم', '٥٠٫٢ سم² ، ٢٥٫١ سم'), ('ق = ١٢ سم', '١١٣٫٠ سم² ، ٣٧٫٧ سم')]), cols=2))
S.append(ex(7, 'نتحقّق بعددٍ من رقمٍ واحد', 'نستخدم ٣ بدلاً من π', L([('للدائرة (أ): نق = ٤', '٤٨ سم² ، ٢٤ سم<small>٣ × ١٦ ، ٢ × ٣ × ٤</small>'), ('للدائرة (ب): ق = ١٢', '١٠٨ سم² ، ٣٦ سم<small>٣ × ٣٦ ، ٣ × ١٢</small>')]), cols=2))
S.append(ex(8, 'قطعة الرخام', 'ق = ط ÷ π', [('محيطها ٤٨ سم: قطرها لأقرب منزلةٍ عشرية', '١٥٫٣ سم<small>٤٨ ÷ ٣٫١٤</small>')], cols=1))
S.append(ex(9, 'الأشكال المركّبة', 'نقسّم ثم نجمع', L([(DRAW([('P', [(0, 2), (4, 2), (4, 0), (8, 0), (8, 5), (0, 5)], '#FDBA74'), ('D', (4, 2), (4, 5)), ('T', 4, 5.7, '٨ سم'), ('T', -0.9, 3.5, '٣ سم'), ('T', 8.9, 2.5, '٥ سم'), ('T', 6, -0.6, '٤ سم')], k=30, cls='svgfig shp', fs=34), '٣٢ سم²<small>٤ × ٥ + ٤ × ٣</small>'), (DRAW([('P', [(0, 0), (8, 0), (8, 4), (0, 4)], '#BBF7D0'), ('H', 4, 0, 4, '#BBF7D0'), ('D', (0, 0), (8, 0)), ('T', 4, 4.7, '٨ سم'), ('T', 8.9, 2, '٤ سم')], k=26, cls='svgfig shp', fs=34), '٥٧٫١٢ سم²<small>٣٢ + ½ × ٣٫١٤ × ٤²</small>')]), cols=2,
  note='في إجابات الدليل ص١٤٦ للجزئية (أ) «٢٩ سم²»، والصحيح من أبعاد الشكل في الكتاب (٨ و ٣ و ٥ و ٤ سم) هو ٤ × ٥ + ٤ × ٣ = ٣٢ سم² (أو ٨ × ٣ + ٤ × ٢ = ٣٢).'))
S.append(ex(10, 'المنطقة الملوّنة', 'الشكل الكامل − التجويف', [(DRAW([('P', [(0, 0), (15, 0), (15, 10), (0, 10)], '#E9D5FF'), ('P', [(2.5, 2.5), (8.5, 2.5), (8.5, 5.5), (2.5, 5.5)], '#fff'), ('T', 7.5, 10.9, '١٥ سم'), ('T', 16.3, 5, '١٠ سم'), ('T', 5.5, 1.6, '٦ سم'), ('T', 9.7, 4, '٣ سم')], k=18, cls='svgfig shp', fs=30) + 'مساحتها', '١٣٢ سم²<small>١٥٠ − ١٨</small>')], cols=1))

EXTRA_CSS_OWN = AREA_CSS + '''
.rulecard{display:flex;align-items:center;gap:1em;background:#fff;border:3px solid var(--ink);border-radius:20px;padding:1.4vh 1.6vw;width:min(1300px,92vw);font-weight:700;font-size:clamp(22px,4vh,46px);line-height:1.5;box-shadow:0 7px 0 #DCE5F0}
.rulecard .rn{flex:none;font-family:var(--fh);font-weight:900;background:var(--ink);color:#fff;border-radius:14px;padding:.2em .7em;font-size:.8em}
.cks{display:flex;flex-direction:column;gap:1.2vh;width:min(1300px,92vw)}
.ck{display:flex;align-items:center;gap:1em;text-align:start;font-family:var(--fb);font-weight:700;font-size:clamp(24px,4.4vh,50px);background:#fff;border:2.5px solid var(--line);border-radius:14px;padding:1vh 1.4vw;cursor:pointer;color:var(--ink);line-height:1.4}
.ck .cb{flex:none;width:1.6em;height:1.6em;border-radius:50%;background:#EEF2F7;display:flex;align-items:center;justify-content:center;font-family:var(--fh)}
.ck.ok{border-color:var(--good);background:#F2FBF5}.ck.ok .cb{background:var(--good);color:#fff}
.slide .box.col>.m{font-size:clamp(30px,5.6vh,66px)}
.box.col .svgfig.shp.sm{height:min(22vh,200px);max-width:26vw}
.q .m{font-size:1.1em}
'''
PG = {'تمرين': [(1, '١٤٤'), (7, '١٤٥')]}
S = FIXNUM(S)
S = [SUP2(x) for x in S]
