# شرائح درس ٤-٢ «اختيار وحدات القياس المناسبة» — الصف السابع (حصة واحدة، كتاب الطالب ص٨٤–٨٦)
# المراجع: دليل المعلم ص٨٨–٨٩ (المفردات: وحدات القياس؛ نقاط التعلّم؛ الأخطاء الشائعة: الخلط بين الوحدة الأكبر والأصغر،
# وعدم إدراك مفهوم الوحدة: شخص كتلته ٧٢ غم، طفل طوله ١٫٣ ملم، حوض استحمام فيه ١٠٠ مل؛ النشاط: جدول الوحدات والأشياء والتقديرات؛
# تعليقات التمارين ١١–١٤)، كتاب الطالب ص٨٤–٨٦ (مثال ٤-٢)، وإجابات الدليل ص٩٠–٩١ (كتاب الطالب) وص٩٢ (كتاب النشاط ص٦١–٦٢).
# python3.12 gen_powers.py choose_slides.py اختيار_وحدات_القياس_المناسبة_عرض_تفاعلي.html "اختيار وحدات القياس المناسبة — الصف السابع"
exec(open(os.path.join(HERE, 'figs.py'), encoding='utf-8').read())

TR = str.maketrans('0123456789.', '٠١٢٣٤٥٦٧٨٩٫')
def D(x): return str(x).translate(TR)
def STP(lab, expr='', cls=''): return st(f'<div class="stp {cls}"><span class="lab">{lab}</span>{expr}</div>')
def STEPS(*rows): return '<div class="stps">' + ''.join(rows) + '</div>'
def BM(*items): return '<div class="bms">' + ''.join(st(f'<div><span>{ic}</span><small>{n}</small><b>{v}</b></div>') for ic, n, v in items) + '</div>'
LEN = (['كم', 'م', 'سم', 'ملم'], [1000, 100, 10], ['كيلومتر', 'متر', 'سنتيمتر', 'مليمتر'])
S = []
ME = 'إعداد: أ. عيسى الحارثي'
S.append(slide(f'''<span class="tag">الصف السابع · الدرس ٤-٢</span>
<h1 class="h1s">اختيار وحدات القياس المناسبة</h1>
<p class="lead">كتاب الطالب ص ٨٤ إلى ٨٦ · حصة واحدة</p>
<p class="lead" style="font-size:clamp(26px,4.8vh,56px)">{ME}</p>''', 'cover'))
CAN = ['أختار <b>وحدة القياس المناسبة</b> لما أقيسه', 'أقدّر القياسات بمقارنتها <b>بأشياء أعرفها</b>', 'أحكم على <b>معقولية التقدير</b> وأعطي سبباً']
S.append(slide(f'''<h2>في نهاية هذا الدرس…</h2>
<div class="can">{''.join(f'<div><span class="can-i">✔</span><span><b>أنا أستطيع</b> أن {t}</span></div>' for t in CAN)}</div>'''))
S.append(slide(f'''<h2>مفردات الدرس</h2>
<div class="voc3 c2">{st('<div><b>وحدات القياس</b><i>units of measurement</i><span>ما نقيس به الطول أو الكتلة أو السعة، مثل المتر والغرام واللتر</span></div>')}{st('<div><b>التقدير</b><i>estimate</i><span>قيمةٌ قريبة من القياس الحقيقي نتوقّعها دون قياسٍ دقيق</span></div>')}</div>''' + tn('«وحدات القياس» من مفردات الدليل ص٨٨. «التقدير» من الكتاب (مثال ٤-٢)، والتعريفان بجملةٍ واحدة من إعدادي.')))

# ═══════════ الحصة ═══════════
S.append(slide('''<span class="tag">الحصة · ٤٠ دقيقة</span><h2>اختيار الوحدة المناسبة والتقدير</h2>
<div class="plan"><div><b>٤ د</b>تذكّر: سلّم التحويل</div><div><b>٦ د</b>كيف نختار الوحدة؟</div><div><b>٦ د</b>أشياء نعرف قياسها</div>
<div><b>٩ د</b>مثال ٤-٢</div><div><b>٨ د</b>نحن ← أنتم</div><div><b>٤ د</b>انتبه</div><div><b>٣ د</b>بطاقة الخروج</div></div>''', 'divider'))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">تذكّر 🔁</span>{ref('الدرس ٤-١')}{timer(1)}</div><h2>سلّم التحويل</h2>
{st(STAIR(*LEN))}
{st('<div class="note">كم سنتيمتراً في المتر؟ وكم متراً في الكيلومتر؟</div>')}''' + tn('مراجعةٌ سريعة للدرس السابق بالرسم نفسه: ١٠٠ سم، و١٠٠٠ م.')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('كتاب الطالب ص ٨٤')}</div><h2>كيف نختار الوحدة المناسبة؟</h2>
<div class="col" style="gap:1.4vh">{st(box('<div class="col"><b class="kk c-we">شيءٌ صغير ← وحدةٌ صغيرة</b><span class="why">ملم ، سم ، غم ، مل</span></div>', style="min-width:66vw"))}{st(box('<div class="col"><b class="kk c-exp">شيءٌ كبير ← وحدةٌ كبيرة</b><span class="why">م ، كم ، كغم ، طن ، لتر</span></div>', style="min-width:66vw"))}</div>
{st('<div class="note">نختار الوحدة التي تجعل العدد معقولاً: لا كبيراً جداً ولا صغيراً جداً</div>')}''' + tn('الكتاب ص٨٤: نختار الوحدة المناسبة لنقدّر القياسات ونحسبها ونحلّ مشكلات الحياة اليومية.')))
S.append(slide(f'''<div class="row hdr">{mode('i')}<span class="qbadge" style="background:#7048E8;box-shadow:0 4px 0 #4C2FB0">أطوالٌ نعرفها</span></div><h2>نقدّر الأطوال بأشياء نعرفها</h2>
{BM(('🧍', 'طول الرجل', '١٫٧ م'), ('🚪', 'ارتفاع الباب', '٢ م'), ('🚗', 'طول السيارة', '٣ إلى ٥ م'), ('⚽', 'ملعب كرة القدم', 'حوالي ١٠٠ م'))}''' + tn('من الكتاب ودليله: الرجل ١٫٧ م (مثال ٤-٢)، الباب ٢ م (إجابة التمرين العام ٧)، السيارة ٣ إلى ٥ م (التمرين ١٣)، الملعب ١٠٠ م (مثال ٤-٢).')))
S.append(slide(f'''<div class="row hdr">{mode('i')}<span class="qbadge" style="background:#7048E8;box-shadow:0 4px 0 #4C2FB0">كتلٌ وسعاتٌ نعرفها</span></div><h2>نقدّر الكتل والسعات بأشياء نعرفها</h2>
{BM(('🥚', 'بيضة', '٦٠ غم'), ('🧑', 'شخص بالغ', '٧٥ كغم'), ('🥄', 'ملعقة شاي', '٥ مل'), ('🥫', 'علبة عصير', '٣٣٠ مل'))}''' + tn('من الدليل: البيضة ٦٠ غم (التمرين ٧)، البالغ ٧٥ كغم (مثال ٤-٢)، ملعقة الشاي ٥ مل (التمرين ١)، علبة العصير ٣٣٠ مل (التمرين ٥). وكتلة التفاحة ١٠٠ إلى ١٥٠ غم (تعليق التمرين ١١).')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('مثال ٤-٢ (١، ٢)')}</div><h2>الوحدة المناسبة، ومعقولية التقدير</h2>
{box(STEPS(STP('(١) طول ملعب كرة القدم', '<span class="kk">المتر (م)</span>'), STP('لماذا؟', '<span class="why">طوله يماثل مسار سباق ١٠٠ م</span>'), STP('(٢) كتلة الفيل ١٥٠ كغم؟', '<span class="kk c-exp">غير واقعي ✘</span>'), STP('لماذا؟', '<span class="why">الفيل حوالي ١٠ أمثال البالغ (٧٥ كغم)</span>', 'fin')))}''' + tn('الكتاب: كتلة الفيل تزيد عن مقدار كتلة رجلين، فـ ١٥٠ كغم تقديرٌ غير واقعي.')))
S.append(slide(f'''<div class="row hdr">{mode('i')}{ref('مثال ٤-٢ (٣)')}</div><h2>ارتفاع الشجرة ٦ أمثال طول الرجل</h2>
{box(STEPS(STP('١) نقدّر طول الرجل', M('١٫٧ م', cls="sm")), STP('٢) نستخدم التقدير', M('٦', X, '١٫٧', cls="sm")), STP('٣) الناتج بوحدته', M('١٠٫٢ م', cls="sm"), 'fin')))}''' + tn('الكتاب: نبدأ بتقديرٍ مناسب لطول الرجل، ثم نتأكّد من كتابة الوحدة (بالمتر) في الإجابة.')))
S.append(slide(f'''<div class="row hdr">{mode('we')}{ref('تمرين ١')}</div><h2>معاً: أيّ قياسٍ أنسب؟</h2>
<div class="row">{''.join(st(f'<button class="flip box col" style="flex:1"><span class="hint">{q}</span><span class="tap">👆</span><span class="hid col"><span class="kk c-we">{a_}</span></span></button>') for q, a_ in (
  ('عرض شاشة الحاسوب<br>٣٢ ملم · ٣٢ سم · ٣٢ م', '٣٢ سم'), ('ارتفاع الحافلة<br>٣٠٠ ملم · ٣٠ م · ٣ م', '٣ م'), ('سعة الدلو<br>٥ لتر · ٥٠ لتر · ٥٠ مل', '٥ لتر')))}</div>''' + tn('اسأل في كل بطاقة: ما الشيء الذي نعرف قياسه ويشبهه؟')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ١ (و)')}{timer(2)}</div>''' + quiz('كتلة الحصان:', [M('٦٠٠ كغم'), M('٦ طن'), M('٦٠ كغم')], 0, 'الحصان أثقل بكثير من الشخص البالغ (٧٥ كغم)، لكنه لا يبلغ ٦ أطنان')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ١ (هـ)')}</div>''' + quiz('سعة ملعقة الشاي:', [M('٥٠٠ مل'), M('٥ لتر'), M('٥ مل')], 2, 'ملعقة الشاي صغيرة جداً: ٥ مل')))
S.append(slide(f'''<div class="row hdr">{mode('u')}{ref('تمرين ٤ (ج)')}</div>''' + quiz('«طول القلم ٢٠ ملم» عبارةٌ:', ['✔ صحيحة', '✘ خاطئة'], 1, '٢٠ ملم = ٢ سم فقط، والقلم أطول من ذلك بكثير')))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">انتبه ⚠️ أخطاء شائعة</span>{ref('دليل المعلم ص ٨٨')}</div><h2>هل هذا التقدير معقول؟</h2>
<div class="errs">{''.join(st(f'<button class="flip err"><span class="xq">{q}</span><span class="tap">👆</span><span class="hid xa no">{w}</span></button>') for q, w in (
  ('كتلة الشخص ٧٢ غم', '✘ الوحدة المناسبة الكيلوغرام: ٧٢ كغم'),
  ('طول الطفل ١٫٣ ملم', '✘ الوحدة المناسبة المتر: ١٫٣ م'),
  ('في حوض الاستحمام ١٠٠ مل من الماء', '✘ الوحدة المناسبة اللتر: ١٠٠ لتر')))}</div>''' + tn('الخطآن الشائعان في الدليل: الخلط بين الوحدة الأكبر والأصغر، وعدم إدراك مفهوم الوحدة (الأمثلة الثلاثة من الدليل نفسه).')))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">النشاط 🎲</span>{ref('دليل المعلم ص ٨٨')}</div><h2>شيءٌ يُقاس بهذه الوحدة، وتقديره</h2>
<table class="act"><tr><th>الوحدة</th><th>شيءٌ يُقاس بها</th><th>تقدير القياس</th></tr><tr><td>المليلتر</td><td>ملعقة كبيرة من الماء</td><td>٢٠ مل</td></tr><tr><td>الكيلومتر</td><td>؟</td><td>؟</td></tr><tr><td>الغرام</td><td>؟</td><td>؟</td></tr></table>''' + tn('النشاط بعد حلّ تمارين ٤-٢: مجموعاتٌ ثنائية، والجدول في الدليل ثماني وحدات (المليمتر، اللتر، الكيلومتر، الغرام، السنتيمتر، الطن، المليلتر، الكيلوغرام). ناقش تقديراتهم.')))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج 🎫</span><h2>اختر وقدّر</h2>
<div class="exit">{st('<div><b>١</b>وحدة قياس طول قلم الرصاص</div>')}{st('<div><b>٢</b>وحدة قياس كتلة السيارة</div>')}{st('<div><b>٣</b>«سعة كوب الماء ٢ لتر»: هل التقدير معقول؟</div>')}</div>''' + tn('من إعدادي (غير موجودة في الكتابين).')))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج 🎫</span><h2>الإجابات</h2>
<button class="flip box col" style="min-width:40vw"><span class="tap">👆 اضغط لإظهار الإجابات</span><span class="hid col"><span class="kk">١) السنتيمتر</span><span class="kk">٢) الطن (أو الكيلوغرام)</span><span class="kk">٣) لا، الكوب يتّسع لحوالي ٢٥٠ مل</span></span></button>'''))
S.append(slide('''<span class="qbadge" style="background:#0A6770;box-shadow:0 4px 0 #05393E">الواجب المنزلي 🏠</span><h2>كتاب النشاط</h2>
<div class="exit"><div class="st"><div><b>١</b>الصفحتان ٦١ و ٦٢ في كتاب النشاط</div></div></div>'''))
S.append(slide(f'''<h2>الخلاصة</h2>
<div class="sumg">
{st(box('<div class="col"><b class="kk c-b">الوحدة</b><span>شيءٌ صغير ← وحدةٌ صغيرة<br>شيءٌ كبير ← وحدةٌ كبيرة</span></div>'))}
{st(box('<div class="col"><b class="kk c-we">التقدير</b><span>نقارن بأشياء نعرف قياسها:<br>رجل ١٫٧ م · بالغ ٧٥ كغم</span></div>'))}
{st(box('<div class="col"><b class="kk c-exp">المعقولية</b><span>نحكم على التقدير<br>ونعطي سبباً</span></div>'))}</div>'''))

# ═══════════ ملحق: تمارين كتاب الطالب ص٨٥–٨٦ (الإجابات من دليل المعلم ص٩٠–٩١) ═══════════
S.append(launch('sb', '٨٥ و ٨٦', note=f'المراجع: كتاب الطالب ص٨٤ إلى ٨٦، ودليل المعلم ص٨٨ و ٨٩ وإجاباته ص٩٠ و ٩١ · {ME}'))
H = ['أ', 'ب', 'ج', 'د', 'هـ', 'و']
RU = 'نقارن بأشياء نعرف قياسها، ونختار الوحدة التي تجعل العدد معقولاً'
S.append(ex(1, 'أيّ القياسات أكثر ملاءمة؟', RU, [(f'({h}) {q}', a_) for h, (q, a_) in zip(H, [
  ('عرض شاشة الحاسوب: ٣٢ ملم ، ٣٢ سم ، ٣٢ م', 'ب) ٣٢ سم'), ('كتلة ثمرة الأناناس: ٢٠ غم ، ٢ كغم ، ٢٠٠ غم', 'ب) ٢ كغم<small>الدليل: ج) ٢٠٠ غم</small>'),
  ('سعة الدلو: ٥ لتر ، ٥٠ لتر ، ٥٠ مل', 'أ) ٥ لتر'), ('ارتفاع الحافلة: ٣٠٠ ملم ، ٣٠ م ، ٣ م', 'ج) ٣ م'),
  ('سعة ملعقة الشاي: ٥٠٠ مل ، ٥ لتر ، ٥ مل', 'ج) ٥ مل'), ('كتلة الحصان: ٦٠٠ كغم ، ٦ طن ، ٦٠ كغم', 'أ) ٦٠٠ كغم')])], cols=2,
  note='في إجابات الدليل ص٩٠ كتلة الأناناس ٢٠٠ غم (ج). في الواقع كتلة ثمرة الأناناس غالباً بين ١ و ٢ كغم، فالأقرب ٢ كغم (ب). قرّر ما تعتمده مع طلابك.'))
S.append(ex(2, 'حدّد وحدة القياس المناسبة', RU, [(f'({h}) {q}', a_) for h, (q, a_) in zip(H, [
  ('طول ملعب كرة المضرب', 'م'), ('طول طابع البريد', 'ملم'), ('كتلة البرتقالة', 'غم'), ('كتلة القطة', 'كغم'), ('سعة حوض الاستحمام', 'لتر'), ('سعة الملعقة', 'مل')])], cols=2))
S.append(ex(3, 'سعة خزّان الماء في المنزل', RU, [('حدّد وحدة القياس المناسبة', 'اللتر')], cols=1))
S.append(ex(4, 'ضع ✔ أو ✘', RU, [(f'({h}) {q}', a_) for h, (q, a_) in zip(H, [
  ('ارتفاع الحصان ٢٫٥ م', '✔'), ('كتلة الطفل حديث الولادة ٣ كغم', '✔'), ('طول القلم ٢٠ ملم', '✘<small>٢٠ ملم = ٢ سم فقط</small>'), ('سعة الزجاجة ٢ لتر', '✔')])], cols=2))
S.append(ex(5, 'بطاقات محمد', 'لكل شيء: عددٌ (وردي) ووحدةٌ (زرقاء) مناسبان', [(FIG('4-2_cards', 'fig lg') + 'صنّف البطاقات في مجموعات', 'علبة العصير ٣٣٠ مل · حقيبة السفر ٢٥ كغم · فرشاة الأسنان ١٨ سم<small>المنزل ١٠ م · الهاتف ١٢٥ غم · حوض الاستحمام ٨٠ لتر</small>')], cols=1))
S.append(ex(6, 'غرفة نوم مها', RU, [('طول الغرفة ٢٠ م: هل التقدير مناسب؟', 'غير منطقي على الأرجح<small>قد يصحّ لو كان المنزل ضخماً جداً</small>')], cols=1))
S.append(ex(7, 'بيضة فريدة', RU, [(FIG('4-2_eggs', 'fig side') + 'كتلة البيضة ٧٥ غم: هل التقدير مناسب؟', 'نعم<small>البيضة العادية حوالي ٦٠ غم، والكبيرة قد تبلغ ٧٥ غم</small>')], cols=1))
S.append(ex(8, 'مسافة سعيد', RU, [('٤٠٠ كم في ساعتين بالسيارة: هل التقدير مناسب؟', 'لا<small>معناه أن يقود بسرعة ٢٠٠ كم في الساعة</small>')], cols=1))
S.append(ex(9, 'قطّتا سعاد', 'ثلاثة أمثال: نضرب في ٣', [('السوداء ٣ كغم، والبيضاء ثلاثة أمثالها', '٣ × ٣ = ٩ كغم')], cols=1))
S.append(ex(10, 'كوب حسن', 'أقلّ بعشر مرات: نقسم على ١٠، ثم نحوّل إلى مل', [('الإبريق ١٫٥ لتر، والكوب أقلّ منه بعشر مرات', '١٫٥ ÷ ١٠ = ٠٫١٥ لتر = ١٥٠ مل')], cols=1))
S.append(ex(11, 'كيس نور', 'التفاحة الواحدة بين ١٠٠ و ١٥٠ غم', [('قدّر كتلة كيسٍ فيه ١٢ تفاحة (بالكيلوغرام)', '١ إلى ٢ كغم<small>١٢ × ١٠٠ إلى ١٢ × ١٥٠ = ١٢٠٠ إلى ١٨٠٠ غم</small>')], cols=1, note='تعليق الدليل: ناقش الطلاب في أن متوسط كتلة التفاحة الواحدة بين ١٠٠ و ١٥٠ غراماً.'))
S.append(ex(12, 'المصعد', 'نقسم الحمولة على عدد الأشخاص ونقارن بكتلة البالغ', [(FIG('4-2_lift', 'fig side') + 'ثمانية بالغين: هل المصعد ممتلئٌ بشكلٍ زائد؟', 'نعم<small>٥٠٠ ÷ ٨ = ٦٢٫٥ كغم، وأغلب البالغين أثقل من ذلك</small>')], cols=1))
S.append(ex(13, 'سور القلعة', 'السيارة طولها ٣ إلى ٥ م، ونعدّ كم سيارةً تملأ السور', [(FIG('4-2_fort', 'fig lg') + 'قدّر طول سور القلعة', '٢٧ إلى ٤٥ م<small>٩ × (٣ إلى ٥ م)</small>')], cols=1, note='تعليق الدليل: أطوال السيارات بين ٢٫٥ و ٦ أمتار تقريباً، وعليها يبنون تقديرهم.'))
S.append(ex(14, 'ارتفاع المبنى', 'طول الرجل ١٫٥ إلى ١٫٩ م، ونعدّ كم رجلاً فوق بعضهم', [(FIG('4-2_building', 'fig lg') + 'قدّر ارتفاع المبنى', '١٣٫٦ إلى ١٤٫٤ م<small>١٫٧ × ٨ = ١٣٫٦ م ، أو ١٫٨ × ٨ = ١٤٫٤ م</small>')], cols=1, note='تعليق الدليل: طريقةٌ بسيطة: نعلّم طول الرجل على ورقة ونحرّكها لأعلى المبنى مرةً بعد مرة.'))

# ═══════════ ملحق: حلول كتاب النشاط ص٦١–٦٢ (الإجابات من دليل المعلم ص٩٢) ═══════════
S.append(launch('ab', '٦١ و ٦٢', note='الإجابات النهائية من دليل المعلم ص ٩٢'))
NA, NB = 'نشاط ص ٦١ · تمرين', 'نشاط ص ٦٢ · تمرين'
S.append(ex(1, 'حدّد الوحدات', RU, [(f'({h}) {q}', a_) for h, (q, a_) in zip(H, [
  ('ارتفاع جبل', 'م'), ('عرض كتاب', 'سم'), ('كتلة سفينة', 'طن'), ('كتلة هاتف جوّال', 'غم'), ('سعة كوب', 'مل'), ('سعة حمّام سباحة متنقل للأطفال', 'لتر')])], cols=2, src=NA))
S.append(ex(2, 'ضع ✔ أو ✘', RU, [(f'({h}) {q}', a_) for h, (q, a_) in zip(H, [
  ('طول المكتب ١٢٠ ملم', '✘<small>١٢٠ ملم = ١٢ سم فقط</small>'), ('كتلة الفيل ١ طن', '✔'), ('سعة الملعقة الكبيرة لتران', '✘'), ('ارتفاع المنزل ٣ م', '✘')])], cols=2, src=NA))
S.append(ex(3, 'سيارة سليم', RU, [('ارتفاع السيارة ٢٫٥ م: هل التقدير مناسب؟', 'لا<small>السيارة أقلّ ارتفاعاً من أغلب البالغين، و ٢٫٥ م أكبر بكثير من طولهم</small>')], cols=1, src=NA))
S.append(ex(4, 'صديقة سارة', RU, [('كتلة الصديقة ٦٥ كغم: هل التقدير مناسب؟', 'نعم<small>بعض البالغين كتلتهم مماثلة</small>')], cols=1, src=NA))
S.append(ex(5, 'سيارة إبراهيم', RU, [('٣٠ كم مشياً في ٣ ساعات: هل التقدير مناسب؟', 'لا<small>معناه السير بسرعة ١٠ كم في الساعة، وهذا غير ممكن مشياً</small>')], cols=1, src=NA))
S.append(ex(6, 'مازن وعلي', 'ثلاثة أمثال: نضرب في ٣', [('مازن ٢٢٫٥ كغم، وعلي ثلاثة أمثاله', '٢٢٫٥ × ٣ = ٦٧٫٥ كغم')], cols=1, src=NB))
S.append(ex(7, 'مغرفة فهد', 'نضرب، ثم نحوّل إلى كغم', [(FIG('4-2_scoop', 'fig side') + 'المغرفة ٢٠٠ غم، والكيس ٥٠ مرة أكثر', '٢٠٠ × ٥٠ = ١٠٠٠٠ غم = ١٠ كغم')], cols=1, src=NB))
S.append(ex(8, 'صندوق سارة', 'نقدّر كتلة العلبة الواحدة، ثم نضرب في ١٢', [('قدّر كتلة صندوقٍ فيه ١٢ علبة مشروبات (كغم)', '٣ إلى ٦ كغم')], cols=1, src=NB))
S.append(ex(9, 'المبنى والرجل', 'نعدّ كم مرةً يتكرّر طول الرجل', [(FIG('4-2_building2', 'fig lg') + '(أ) قدّر ارتفاع المبنى (ب) قدّر طوله', '(أ) ٦٫٥ إلى ٧٫٥ م<small>(ب) ١١ إلى ١٣ م</small>')], cols=1, src=NB))

EXTRA_CSS_OWN = '''
.stps{display:flex;flex-direction:column;gap:1.2vh;align-items:stretch}
.stp{display:flex;align-items:center;gap:1.4vw;justify-content:space-between}
.stp .lab{flex:0 1 auto;max-width:60%;font-family:var(--fh);font-weight:800;color:#2563EB;background:#EAF1FF;border-radius:12px;padding:.2em .8em;text-align:center;line-height:1.4;font-size:clamp(20px,3.6vh,42px)}
.stp.fin .lab{background:var(--good);color:#fff}
.box .col>.m:not(.mid):not(.sm):not(.big),.hid.col>.m:not(.mid):not(.sm):not(.big){font-size:clamp(32px,6vh,70px)}
.voc3{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1.6vw;width:min(1500px,94vw)}.voc3.c2{grid-template-columns:repeat(2,minmax(0,1fr))}
.voc3 .st>div{display:flex;flex-direction:column;align-items:center;gap:.6vh;background:#fff;border:3px solid var(--line);border-radius:18px;padding:1.6vh 1vw;text-align:center}
.voc3 b{font-family:var(--fh);font-size:clamp(34px,6.4vh,76px);color:var(--base)}.voc3 i{font-style:normal;font-weight:700;color:var(--ink2);font-size:clamp(20px,3.4vh,38px)}
.voc3 span{font-weight:700;font-size:clamp(22px,3.8vh,44px);line-height:1.5}
.bms{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:1.4vw;width:min(1500px,94vw)}
.bms .st>div{display:flex;flex-direction:column;align-items:center;gap:.4vh;background:#fff;border:3px solid var(--base);border-radius:18px;padding:1.4vh .6vw;text-align:center}
.bms span{font-size:clamp(46px,9vh,104px);line-height:1.1}.bms small{font-weight:800;font-size:clamp(20px,3.6vh,40px);color:var(--ink2)}.bms b{font-family:var(--fh);font-size:clamp(28px,5.4vh,62px);color:var(--base)}
.slide .svgfig.stair{width:auto;height:min(54vh,540px);max-width:92vw;max-height:none}
.why{font-weight:700;color:var(--ink2);font-size:clamp(22px,3.8vh,44px)}
.errs{display:flex;flex-direction:column;gap:1.4vh;width:min(1400px,92vw)}
.errs .err{display:flex;flex-direction:column;align-items:center;gap:.6vh;background:#fff;border:3px solid var(--line);border-radius:16px;padding:.8vh 1.6vw;font-size:clamp(26px,5vh,58px);font-weight:700}
.errs .err .xa{font-size:clamp(24px,4.4vh,50px)}
.act{border-collapse:separate;border-spacing:0;font-weight:800;font-size:clamp(24px,4.4vh,50px);background:#fff;border:3px solid var(--ink);border-radius:14px;overflow:hidden;width:min(1200px,90vw)}
.act th{background:var(--ink);color:#fff;padding:.3em .6em}.act td{text-align:center;padding:.25em .6em;border-top:2px solid var(--line)}.act td+td,.act th+th{border-inline-start:2px solid var(--line)}
.sumg{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:2vw;width:min(1600px,94vw)}
.sumg .col span{font-weight:700;font-size:clamp(22px,4vh,46px);line-height:1.5}
.sumg .kk{font-size:clamp(30px,5.6vh,66px)}
.hid.col .kk{font-size:clamp(28px,5.2vh,60px)}
.xa small{display:block}
@media (max-aspect-ratio:1/1){.voc3,.sumg{grid-template-columns:1fr}.bms{grid-template-columns:repeat(2,minmax(0,1fr))}}
''' + FIG_CSS
