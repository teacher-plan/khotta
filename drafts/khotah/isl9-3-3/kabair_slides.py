# درس «أكبر الكبائر» (حديث شريف): التربية الإسلامية، الصف التاسع، الفصل الأول، الوحدة الثالثة، الدرس الثالث.
# الطريقة من دليل المعلم نفسه (ص١٤٨–١٥٦)، لا من طريقة معلّمٍ بعينه: تسير الشرائح بعناصر كتاب الطالب وترتيب المخرجات السبعة في الدليل:
#   التهيئة «أتأمّل وأتعرّف» (عصف ذهني) ← «أقرأ وأحفظ» (قراءة نموذجية ثم بالتناوب) ← «أتعرّف راوي الحديث» ← «أتعرّف المعنى»
#   ← «أقرأ وأفهم» (الحوار والمناقشة بأسئلة الدليل، والاستكشاف) ← «أتأمّل وأقوّم» (التعلّم بالأقران في مجموعات) ← «أقيّم تعلّمي» ← الحفظ.
#   ولطلبة في الخامسة عشرة: مواقف من واقعهم (الأبراج، الشجار في المدرسة، الأخبار المضلِّلة)، وتصنيفٌ تفاعلي، وتحدٍّ بين فريقين في التقويم.
# المراجع (أرقام مطبوعة): كتاب الطالب ص٩٤–٩٨، دليل المعلم ص١٤٨–١٥٦. الآيات من quran.com بالرسم العثماني.
exec(open(os.path.join(HERE, 'isl_common.py'), encoding='utf-8').read())
use('figs')
def SCEN(who, text): return f'<div class="scen st"><span class="who">{who}</span><p>{text}</p></div>'
def OPT(items, opts): return SORT(items, opts, cols=1)
SCORE = '<div class="score" onclick="event.stopPropagation()">' + ''.join(f'<div><b>{t}</b><button onclick="var n=this.nextElementSibling;n.textContent=Math.max(0,(+n.dataset.v||0)-1);n.dataset.v=n.textContent">−</button><i data-v="0">0</i><button onclick="var n=this.previousElementSibling;n.dataset.v=(+n.dataset.v||0)+1;n.textContent=n.dataset.v">+</button></div>' for t in ('الفريق الأوّل', 'الفريق الثاني')) + '</div>'
# مراحل الدرس بأسماء عناصر الكتاب (لا «محطات»): الطريقة من دليل المعلم ص١٤٨ — العصف الذهني، الاستكشاف، الحوار والمناقشة، التعلّم بالأقران.
B = {'t': '<span class="stage bq">🔎 أتأمّل وأتعرّف</span>', 'r': '<span class="stage bd">📖 أقرأ وأحفظ</span>', 'w': '<span class="stage bd">👤 أتعرّف راوي الحديث</span>',
     'm': '<span class="stage bd">📚 أتعرّف المعنى</span>', 'f': '<span class="stage bl">💡 أقرأ وأفهم</span>', 'q': '<span class="stage bq">🤔 أتأمّل وأقوّم</span>',
     'd': '<span class="stage bq">💬 نتحاور</span>', 'c': '<span class="stage bc">🏆 أقيّم تعلّمي</span>'}
def CHIPS(items): return '<div class="chips st">' + ''.join(f'<span>{x}</span>' for x in items) + '</div>'
def CASE(img, cap, ans):   # بطاقة موقف من نشاط «أتأمّل وأقوّم»: الصورة والموقف، والحكم يُكشف بضغطة
    return st(f'<button class="flip box col case">{FIG(img, "cimg", cap)}<span class="cap">{cap}</span><span class="tap">👆 ما حكمه؟</span><span class="hid col"><span class="kk c-we">{ans}</span></span></button>')

S.append(cover('٣', 'أكبر الكبائر', 'الصف التاسع · حديث شريف · الوحدة الثالثة', 'كتاب الطالب ص ٩٤ – ٩٨'))
S.append(goals(['أقرأ الحديث الشريف <b>قراءةً صحيحة</b> وأحفظه', 'أتعرّف <b>راوي</b> الحديث', 'أبيّن <b>معاني</b> بعض المفردات والتراكيب',
                'أعلّل تخصيص النبيّ ﷺ لهذه <b>الكبائر</b> بالذكر', 'أوضّح دلالة تغيير هيئته ﷺ عند ذكر <b>قول الزور</b>']).replace('</section>', tn('مخرجات التعلّم من دليل المعلم ص١٤٨، والسادس: يتجنّب ارتكاب الكبائر الواردة في الحديث. عدد الحصص: ٢. طرائق الدليل: العصف الذهني، والاستكشاف، والحوار والمناقشة، والتعلّم بالأقران؛ ويُعرض الحديث بجهاز ونشاط «أتأمّل وأقوّم».') + '</section>'))

# ═══════════ التهيئة ═══════════
S.append(section('التهيئة', 'أتأمّل وأتعرّف · كتاب الطالب ص ٩٤'))
S.append(slide(f'''<div class="row hdr">{B['t']}{ref('كتاب الطالب ص ٩٤')}</div>
<div class="ayahbox st">{AY('ٱلَّذِينَ يَجْتَنِبُونَ كَبَـٰٓئِرَ ٱلْإِثْمِ وَٱلْفَوَٰحِشَ إِلَّا ٱللَّمَمَ', 'النجم: ٣٢')}</div>
<div class="bookimg sm st">{FIG('dhunub', 'bimg', 'مخطّط أقسام الذنوب: الصغائر والكبائر، وأكبر الكبائر الثلاث')}</div>''' + tn('التهيئة من الدليل ص١٤٩: يتأمّل الطلبة الآية والمخطّط. اللمم: الصغائر من الذنوب (حاشية الكتاب). الصغائر: الذنوب التي نهى الله عنها ولم يرد فيها وعيد.')))
S.append(slide(f'''<div class="row hdr">{B['t']}{ref('دليل المعلم ص ١٤٩')}</div><h2>صغيرة أم كبيرة؟</h2>
{OPT([('اللغو', 0), ('الإشراك بالله', 1), ('عقوق الوالدين', 1), ('قول الزور', 1)], ('صغيرة', 'كبيرة'))}''' + tn('أسئلة التهيئة في الدليل ص١٤٩: عدّد أنواع الذنوب (الصغائر والكبائر)، وأعطِ أمثلة (الصغائر مثل اللغو، والكبائر مثل الإشراك بالله وعقوق الوالدين وقول الزور). ثم انقلهم إلى الحديث بعبارة الدليل: «يا ترى، لماذا خصّها النبيّ ﷺ بالذكر؟».')))

# ═══════════ أقرأ وأحفظ ═══════════
S.append(section('الحديث الشريف', 'أقرأ وأحفظ · كتاب الطالب ص ٩٤'))
S.append(slide(f'''<div class="row hdr">{B['r']}{ref('كتاب الطالب ص ٩٤')}</div>
<div class="bookimg st">{FIG('hadith', 'bimg', 'نصّ الحديث الشريف: ألا أنبّئكم بأكبر الكبائر')}</div>''' + tn('المخرج الأول (الدليل ص١٤٩): يعرض المعلّم الحديث، ويقرؤه قراءةً صحيحة، ثم يقرؤه بعض الطلبة؛ ويمكن تفعيل رمز QR في الكتاب ص٩٤. يركّز على مهارة الجسد عند الاستفهام «ألا أنبّئكم بأكبر الكبائر» وتكرارها ثلاثاً، وعند تغيير هيئته ﷺ قبل ذكر قول الزور وتكراره.')))
S.append(slide(f'''<div class="row hdr">{B['r']}{ref('دليل المعلم ص ١٥٠')}</div><h2>نقرأ بالتناوب</h2>
<div class="read3">{st('<div><b>١</b><span>«ألا أنبّئكم بأكبر الكبائر؟» <i>(ثلاثاً)</i></span></div>')}{st('<div><b>٢</b><span>قالوا: بلى يا رسول الله. قال: «الإشراك بالله، وعقوق الوالدين»</span></div>')}{st('<div><b>٣</b><span>وجلس، وكان متّكئاً، فقال: «ألا وقولُ الزور»</span></div>')}{st('<div><b>٤</b><span>فما زال يكرّرها حتى قلنا: ليته سكت</span></div>')}</div>''' + tn('تقسيم الحديث أربعة مقاطع ليقرأها الطلبة بالتناوب (تعلّم بالأقران: يصوّب الزميل لزميله)، ثم يقرؤه طالبٌ كاملاً. البخاري، الصحيح، كتاب الشهادات، رقم ٢٦٥٤.')))

# ═══════════ أتعرّف راوي الحديث ═══════════
S.append(slide(f'''<div class="row hdr">{B['w']}{ref('كتاب الطالب ص ٩٤')}</div><h2>عبد الرحمن بن أبي بكرة</h2>
<div class="idcard st"><div><b>من هو؟</b><span>تابعيٌّ وُلد بالبصرة في خلافة عمر رضي الله عنه</span></div><div><b>أبوه</b><span>الصحابي أبو بكرة نُفيع بن الحارث رضي الله عنه</span></div><div><b>صفات أبيه</b><span>من علماء الصحابة وفضلائهم، عُرف بكثرة عبادته</span></div></div>
{FLIPS([('لماذا كنّاه النبيّ ﷺ «أبا بكرة»؟', 'لأنه تدلّى من أسوار الطائف ببَكَرة', 'عند الحصار · البَكَرة: خشبةٌ مستديرة في وسطها حبل، ولها محورٌ تدور عليه')], 'flex:1;min-width:60vw')}''' + tn('المخرج الثاني (الدليل ص١٥٠) وبطاقة التعارف «هوية» المقترحة فيه. صفات الصحابي التي يُقتدى بها (سؤال الدليل): العناية بالسنة النبوية، وكثرة العبادة. المرجع في الكتاب: ابن الأثير، أسد الغابة ٥/٣٨.')))

# ═══════════ أتعرّف المعنى ═══════════
S.append(slide(f'''<div class="row hdr">{B['m']}{ref('كتاب الطالب ص ٩٥')}</div><h2>معاني المفردات</h2>
{FLIPS([('أُنبِّئكم', 'أُخبركم'), ('الكبائر', 'الذنوب العظيمة'), ('الزُّور', 'الكذب')], 'flex:1;min-width:26vw')}
<p class="hint st">وماذا تعني: الإشراك بالله · العقوق · الاتّكاء؟</p>''' + tn('المخرج الثالث (الدليل ص١٥٠): يقرأ الطلبة عنصر «أتعرّف المعنى»، ثم يفتح المعلّم مجال التساؤل عن الكلمات غير المدرجة: الإشراك بالله (عبادة غير الله معه)، العقوق (الإساءة إلى الوالدين ومخالفتهما)، الاتّكاء (الاستناد والميل).')))

# ═══════════ أقرأ وأفهم: لماذا هذه الكبائر؟ ═══════════
S.append(section('لماذا خصّ النبيّ ﷺ هذه الكبائر؟', 'أقرأ وأفهم · كتاب الطالب ص ٩٥ – ٩٧'))
S.append(slide(f'''<div class="row hdr">{B['f']}{ref('دليل المعلم ص ١٥١')}</div><h2>كيف بدأ النبيّ ﷺ حديثه؟</h2>
{FLIPS([('ما الأسلوب الذي استخدمه ﷺ في تعليم الصحابة؟', 'الاستفهام والتنبيه، والتكرار ثلاثاً'), ('وما الغاية منه؟', 'شدّ انتباههم وتهيئتهم لتلقّي حقائق عظيمة')], 'flex:1;min-width:38vw')}''' + tn('المخرج الرابع (الدليل ص١٥١) س١ و٢. اسأل الطلبة قبل الكشف: متى يكرّر المعلّم أو الأب كلاماً ثلاث مرّات؟')))
S.append(slide(f'''<div class="row hdr">{B['f']}{ref('كتاب الطالب ص ٩٥')}</div><h2>الكبيرة الأولى: الإشراك بالله</h2>
<div class="ayahbox st">{AY('وَإِذْ قَالَ لُقْمَـٰنُ لِٱبْنِهِۦ وَهُوَ يَعِظُهُۥ يَـٰبُنَىَّ لَا تُشْرِكْ بِٱللَّهِ ۖ إِنَّ ٱلشِّرْكَ لَظُلْمٌ عَظِيمٌ', 'لقمان: ١٣')}</div>
{FLIPS([('لماذا جاء الشرك في مقدّمة الكبائر؟', 'لأن توحيد الله هو أصل العبادات', 'أقبح الذنوب وأعظم ما عُصي به الله، ومخالفةٌ للفطرة السليمة، ولا يُغتفر لمن مات عليه')], 'flex:1;min-width:64vw')}''' + tn('الكتاب ص٩٥ والدليل ص١٥١–١٥٢ (س٥). وصفه لقمان بالظلم العظيم، وجعله أولى وصاياه لابنه.')))
S.append(slide(f'''<div class="row hdr">{B['d']}{ref('دليل المعلم ص ١٥١ – ١٥٢')}</div><h2>مظاهر للشرك في عصرنا</h2>
{CHIPS(['اللجوء إلى السحرة والمشعوذين', 'تعليق التمائم', 'تقديس الأضرحة وتقديم النذور', 'الهوس بالأبراج وقراءة الطالع', 'الانخداع بنظريات «الطاقة» و«قانون الجذب»'])}
{SCEN('موقف', 'زميلك يقرأ «حظّه» في الأبراج كل صباح، ويقول: «اليوم يومي السعيد، هكذا قال البرج».')}
<p class="hint st">بمَ تنصحه؟ وما المبدأ الذي يرسّخه الدرس؟</p>''' + tn('مظاهر الشرك من الدليل ص١٥١–١٥٢، والمبدأ: الإخلاص لله تعالى في أداء أي عمل. الموقف من إعداد العرض لتطبيق ما ذكره الدليل عن «الهوس بالأبراج».')))
S.append(slide(f'''<div class="row hdr">{B['f']}{ref('كتاب الطالب ص ٩٥ – ٩٦')}</div><h2>الكبيرة الثانية: عقوق الوالدين</h2>
<div class="ayahbox st">{AY('أَنِ ٱشْكُرْ لِى وَلِوَٰلِدَيْكَ إِلَىَّ ٱلْمَصِيرُ', 'لقمان: ١٤')}</div>
<div class="ayahbox st">{AY('فَلَا تَقُل لَّهُمَآ أُفٍّ', 'الإسراء: ٢٣')}</div>
<p class="lead st">قرن الله شكر الوالدين بشكره، وحقّهما في البرّ بحقّه في العبادة</p>''' + tn('الكتاب ص٩٥–٩٦. الدليل ص١٥٢: ناقش دلالة إقران الله تعالى بين الإشراك به والإحسان إلى الوالدين في عدّة آيات، وضرورة القول الحسن وعدم التأفّف ولو بأدنى كلمة.')))
S.append(slide(f'''<div class="row hdr">{B['d']}{ref('كتاب الطالب ص ٩٥ – ٩٦')}</div><h2>برٌّ أم عقوق؟</h2>
{OPT([('رفع الصوت في وجههما', 1), ('القول الحسن وطاعتهما في المعروف', 0), ('العبوس لهما والإغلاظ عليهما بالقول', 1), ('الدعاء لهما والصدقة عنهما بعد وفاتهما', 0), ('ذمّهما أمام الناس، والتخلّي عنهما حال الكِبَر', 1)], ('برّ', 'عقوق'))}''' + tn('صور البرّ والعقوق من الكتاب ص٩٥–٩٦، وجدول الدليل ص١٥٣ (س٧): حكم العقوق حرام؛ وجزاؤه حرمان البركة في الدنيا ودخول النار في الآخرة.')))
S.append(slide(f'''<div class="row hdr">{B['f']}{ref('كتاب الطالب ص ٩٦')}</div><h2>الجزاء من جنس العمل</h2>
<div class="ans3">{st('<div><b>في الدنيا</b><span>عقوبة العقوق تُعجَّل: يُحرم البركة في العمر والرزق، ويبعد عن التوفيق</span></div>')}{st('<div><b>في الآخرة</b><span>لا يدخل الجنّة عاقٌّ لوالديه</span></div>')}{st('<div><b>من برّ</b><span>من برّ والديه اليوم برّه أبناؤه غداً</span></div>')}</div>
<p class="hint st">وعلى الآباء: إعانة الأبناء على البرّ، والحذر من الدعاء عليهم: «لا تدعوا على أنفسكم، ولا تدعوا على أولادكم»</p>''' + tn('الكتاب ص٩٦، والحديث: أبو داود، السنن، رقم ١٥٣٢.')))
S.append(slide(f'''<div class="row hdr">{B['f']}{ref('كتاب الطالب ص ٩٦')}</div><h2>الكبيرة الثالثة: قول الزور</h2>
<div class="ayahbox st">{AY('فَٱجْتَنِبُوا۟ ٱلرِّجْسَ مِنَ ٱلْأَوْثَـٰنِ وَٱجْتَنِبُوا۟ قَوْلَ ٱلزُّورِ', 'الحج: ٣٠')}</div>
{FLIPS([('جلس ﷺ وكان متّكئاً، وكرّرها حتى قالوا: ليته سكت. ما دلالة ذلك؟', 'عِظَم قول الزور وخطورته', 'أراد أن يلفت انتباههم إلى عظم هذه الكبيرة، فجمع الله بينه وبين الشرك في الآية')], 'flex:1;min-width:64vw')}''' + tn('المخرج الخامس (الدليل ص١٥٣) س١. الكتاب ص٩٦: الشرك افتراءٌ على الله وزور، ومن صور قول الزور رمي المحصنات الغافلات واتّهام الناس في أعراضهم كذباً؛ وفي رواية «وشهادة الزور».')))
S.append(slide(f'''<div class="row hdr">{B['f']}{ref('كتاب الطالب ص ٩٦ – ٩٧')}</div><h2>شهادة الزور</h2>
<div class="ayahbox st">{AY('كُونُوا۟ قَوَّٰمِينَ بِٱلْقِسْطِ شُهَدَآءَ لِلَّهِ وَلَوْ عَلَىٰٓ أَنفُسِكُمْ أَوِ ٱلْوَٰلِدَيْنِ وَٱلْأَقْرَبِينَ', 'النساء: ١٣٥')}</div>
{FLIPS([('ما آثار شهادة الزور على الفرد والمجتمع؟', 'تُضيع الحقوق وتُهدر الدماء', 'تقطع الأرحام، وتفتح باب الرشاوى، وتنشر الأحقاد، ويُتّهم بها البريء'), ('وهل يجوز كتمان الشهادة إن احتيج إليها؟', 'لا', '﴿وَمَن يَكْتُمْهَا فَإِنَّهُۥٓ ءَاثِمٌ قَلْبُهُۥ﴾ البقرة: ٢٨٣')], 'flex:1;min-width:38vw')}''' + tn('الكتاب ص٩٦–٩٧، والدليل ص١٥٣ (س٢). الدليل: يوجّه المعلّم الطلبة إلى ما ورد في قانون الجزاء العُماني حول جزاء من يشهد زوراً.')))

# ═══════════ أتأمّل وأقوّم ═══════════
S.append(section('أتأمّل وأقوّم', 'قول الزور في حياتنا المعاصرة · كتاب الطالب ص ٩٧'))
S.append(slide(f'''<div class="row hdr">{B['q']}{ref('كتاب الطالب ص ٩٧')}{timer(4)}</div><h2>ما حكم كلّ موقف؟ وبمَ تنصح صاحبه؟</h2>
<div class="cases">{CASE('z1', 'يُعطي شهادةً بأن السيارة ليس بها عيب، والحقيقة أن بها أعطالاً جسيمة', 'لا يجوز، ويجب إخبار المشتري بكل العيوب: فهذه شهادة زور')}{CASE('z2', 'قدّم شهادة حضورٍ ومشاركةٍ في دورةٍ تدريبية، وهو لم يحضرها', 'لا يجوز: هذا تزوير، وعليه التوبة منه')}{CASE('z3', 'قناةٌ إعلامية تذيع أخباراً مضلِّلة', 'على من يتولّى هذا المنبر أن يتّقي الله، ولا يقدّم أخباراً كاذبة: فهذا من قول الزور')}{CASE('z4', 'يشهد أن المبنى نُفّذ حسب الاشتراطات المعتمدة، لكن الواقع خلاف ذلك', 'لا يجوز، ويجب البناء بالمواصفات المتّفق عليها، وعدم الغش والشهادة الكاذبة')}</div>''' + tn('نشاط «أتأمّل وأقوّم» (الكتاب ص٩٧) وإجاباته من الدليل ص١٥٤. اقترح: كل مجموعة تناقش موقفاً، ثم تعرض حكمه ونصيحتها، ويُكشف جواب الدليل. وفي الكتاب «مُظلِّلة» وصوابها «مُضلِّلة».')))
S.append(slide(f'''<div class="row hdr">{B['d']}{ref('دليل المعلم ص ١٥٥')}{timer(2)}</div>
{SCEN('موقف', 'وقع أمامك شجارٌ بين زميليك، فطلب منك مدير المدرسة أن تصف ما حصل.')}
<div class="disc">{st('<div>كيف تتصرّف؟ وما الذي ستحرص عليه في وصفك؟</div>')}{st('<div>كيف تتجنّب الكبائر الثلاث الواردة في الحديث في حياتك؟</div>')}</div>''' + tn('المخرج السادس (الدليل ص١٥٥): أسئلة الدليل نصّاً. الحوار والمناقشة: يصف الطالب ما رأى بصدق دون زيادة ولا كتمان، ولو كان أحدهما صديقه.')))
S.append(slide(f'''<div class="row hdr">{B['f']}{ref('دليل المعلم ص ١٥٥')}</div><h2>هل الكبائر ثلاثٌ فقط؟</h2>
<p class="lead st">لا… ذكرها النبيّ ﷺ على سبيل المثال لا الحصر، لخطورتها وانتشارها</p>
{CHIPS(['قتل النفس بغير حق', 'الزنا', 'أكل مال اليتيم', 'الربا', 'الانتحار', 'قذف المحصنات', 'شرب الخمر', 'إثارة النزاعات'])}
<div class="ayahbox st">{AY('قُلْ يَـٰعِبَادِىَ ٱلَّذِينَ أَسْرَفُوا۟ عَلَىٰٓ أَنفُسِهِمْ لَا تَقْنَطُوا۟ مِن رَّحْمَةِ ٱللَّهِ ۚ إِنَّ ٱللَّهَ يَغْفِرُ ٱلذُّنُوبَ جَمِيعًا', 'الزمر: ٥٣')}</div>''' + tn('الدليل ص١٥١ وص١٥٥: كبائر أخرى لم ترد في الحديث، والترغيب في التوبة لمن وقع في شيءٍ من الذنوب.')))

# ═══════════ أقيّم تعلّمي ═══════════
S.append(section('أقيّم تعلّمي', 'كتاب الطالب ص ٩٨'))
S.append(slide(f'''<div class="row hdr">{B['c']}{ref('أولاً · كتاب الطالب ص ٩٨')}</div>{SCORE}<h2>بمَ شدّد النبيّ ﷺ على خطورة قول الزور؟</h2>
{TF([('أعاد التنبيه بـ «ألا»', 0), ('جلس وكان متّكئاً', 0), ('كرّرها مراراً', 0), ('رفع صوته بالدعاء على صاحبه', 1)])}''' + tn('«أولاً» من الكتاب ص٩٨ وإجابته في الدليل ص١٥٦: جلس وكان متّكئاً، كرّرها مراراً (والثالثة في الكتاب: أعاد التنبيه بـ«ألا»). العبارة الأخيرة خاطئة للتمييز. قسّم الصف فريقين، ولوحة النقاط لهذه الشريحة.')))
S.append(slide(f'''<div class="row hdr">{B['c']}{ref('دليل المعلم ص ١٥٢')}</div>{SCORE}<h2>صواب أم خطأ؟</h2>
{TF([('الكبائر محصورةٌ في الثلاث الواردة في الحديث', 1), ('عقوبة عقوق الوالدين تُعجَّل في الدنيا قبل الآخرة', 0), ('يجوز كتمان الشهادة إن احتيج إليها', 1), ('الشرك لا يُغتفر لمن مات عليه', 0)])}''' + tn('من الدليل ص١٥٢ (هل الكبائر مقصورة على الثلاث؟ لا) والكتاب ص٩٥–٩٧.')))
S.append(slide(f'''<div class="row hdr">{B['c']}{ref('ثانياً · كتاب الطالب ص ٩٨')}{timer(3)}</div><h2>اقترح طرقاً عملية تعزّز برّ الوالدين في مجتمعك</h2>
{FLIPS([('فكّروا في مجموعات، ثم اكشف مقترحات الدليل', 'غرس احترام الوالدين منذ الصغر', 'تعزيز قيم تقبيل رأس الوالدين ويدهما · محاضرات وبرامج في الإذاعة المدرسية والمساجد · التوعية في خطب الجمعة · رسائل قصيرة في وسائل التواصل · مقاطع توعوية وفيديوهات قصيرة')], 'flex:1;min-width:64vw')}''' + tn('«ثانياً» ص٩٨، والإجابة في الدليل ص١٥٦.')))
S.append(slide(f'''<div class="row hdr">{B['c']}{ref('ثالثاً · كتاب الطالب ص ٩٨')}</div><h2>قيّم ذاتك بصدق</h2>
<div class="disc">{st('<div>أنزعج عندما توقظني أمّي لصلاة الفجر</div>')}{st('<div>لا أذكر والديّ بسوءٍ أمام الناس</div>')}{st('<div>أستأذن من والديّ عند ذهابي مع أصدقائي</div>')}{st('<div>أتجنّب إثارة المشكلات، ولا أوقع والديّ في مواقف محرجة بسببي</div>')}</div>
<p class="hint st">دائماً · غالباً · أحياناً · نادراً · أبداً</p>''' + tn('«ثالثاً» ص٩٨: يحلّه الطالب في كتابه بمصداقية، وتُترك الإجابة له (الدليل ص١٥٦).')))
S.append(slide(f'''<span class="qbadge">بطاقة الخروج 🎫</span><h2>قبل أن تخرج</h2>
<div class="disc">{st('<div><b>١</b> اكتب الكبائر الثلاث الواردة في الحديث</div>')}{st('<div><b>٢</b> لماذا جاء الشرك في مقدّمتها؟</div>')}{st('<div><b>٣</b> موقفٌ في حياتك تتجنّب فيه قول الزور</div>')}</div>''' + tn('بطاقة خروج من إعداد العرض لقياس المخرجات ٤ و٥ و٦.')))
S.append(slide('''<span class="qbadge" style="background:#0A6770;box-shadow:0 4px 0 #05393E">الواجب 🏠</span><h2>أحفظ الحديث الشريف</h2>
<p class="lead">احفظ حديث «ألا أنبّئكم بأكبر الكبائر» حفظاً متقناً، وأكمل «أقيّم تعلّمي» في كتابك ص ٩٨</p>''' + tn('المخرج السابع (الدليل ص١٥٦): يوجّه المعلّم الطلبة لحفظ الحديث، ويتابع حفظهم ويعزّزهم مادياً أو معنوياً.')))

ISL_FINISH()
EXTRA_CSS_OWN += '''
.stage.bq{background:#7A2E5A}.stage.bd{background:var(--navy)}.stage.bl{background:#0B6B4F}.stage.bc{background:var(--gold)}
.slide:has(.stage.bq){background:linear-gradient(90deg,transparent 0 calc(100% - 12px),#7A2E5A 0)}
.slide:has(.stage.bd){background:linear-gradient(90deg,transparent 0 calc(100% - 12px),var(--navy) 0)}
.slide:has(.stage.bl){background:linear-gradient(90deg,transparent 0 calc(100% - 12px),#0B6B4F 0)}
.slide:has(.stage.bc){background:linear-gradient(90deg,transparent 0 calc(100% - 12px),var(--gold) 0)}
.bigq{display:flex;flex-direction:column;align-items:center;gap:1.2vh;max-width:84vw;text-align:center}
.bigq b{font-family:var(--fh);font-weight:800;font-size:clamp(28px,6vh,68px);line-height:1.5;color:#3E1530;text-wrap:balance}
.bigq span{font-size:clamp(20px,4vh,46px);color:#6B5B65;font-weight:700}
.tps{display:flex;align-items:center;gap:1vw;flex-wrap:wrap;justify-content:center}
.tps>span{font-family:var(--fh);font-weight:800;font-size:clamp(18px,3.6vh,40px);background:#F7EEF3;border:2px solid #E5CCDA;color:#7A2E5A;border-radius:12px;padding:.3em .8em}
.tps>i{font-style:normal;color:#B98AA6;font-size:clamp(18px,3.6vh,40px)}
.poll{flex-wrap:wrap;display:flex;gap:1.6vw;justify-content:center}
.pl{display:flex;flex-direction:column;align-items:center;gap:.6vh;background:#fff;border:3px solid #E5CCDA;border-radius:16px;padding:1.6vh 2.4vw;cursor:pointer;min-width:16vw}
.pl b{font-family:var(--fh);font-size:clamp(22px,4.4vh,50px);color:#3E1530}.pl i{font-style:normal;font-family:var(--fh);font-size:clamp(30px,6vh,70px);color:#7A2E5A}
.pl:active{transform:scale(.97)}
.scen{display:flex;align-items:center;gap:1.4vw;background:#FFF8EC;border:2px solid #EAD9A8;border-radius:16px;padding:1.6vh 2vw;max-width:84vw}
.scen .who{font-family:var(--fh);font-weight:800;background:var(--gold);color:#fff;border-radius:10px;padding:.3em .8em;font-size:clamp(18px,3.6vh,40px);white-space:nowrap}
.scen p{margin:0;font-size:clamp(22px,4.4vh,50px);line-height:1.55;font-weight:700}
.two2{display:grid;grid-template-columns:1fr 1fr;gap:1.6vw;width:88vw}.two2 .scen{max-width:none;height:100%;box-sizing:border-box}
.bookimg{display:flex;justify-content:center}.bimg{max-width:84vw;max-height:52vh;border-radius:14px;border:2px solid #E3DED2;box-shadow:0 6px 20px rgba(0,0,0,.08);object-fit:contain}
.bookimg.sm .bimg{max-height:34vh}
.ans3{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1.2vw;width:88vw}
.ans3>div>div{display:flex;flex-direction:column;align-items:center;text-align:center;gap:.8vh;background:#fff;border:2px solid #E3DED2;border-top:6px solid var(--navy);border-radius:14px;padding:1.6vh 1vw;height:100%;box-sizing:border-box}
.ans3 b{font-family:var(--fh);font-size:clamp(22px,4.4vh,50px);color:var(--navy)}.ans3 span{font-size:clamp(19px,3.7vh,42px);line-height:1.45;font-weight:700}
.disc{display:flex;flex-direction:column;gap:1.6vh;width:80vw}
.disc>div>div{background:#fff;border:2px solid #E3DED2;border-inline-start:8px solid #0B6B4F;border-radius:14px;padding:1.6vh 2vw;font-size:clamp(22px,4.6vh,52px);font-weight:700}
.disc b{font-family:var(--fh);color:var(--gold);font-size:1.3em;margin-inline-end:.4em}
.chain{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:1.2vw;width:88vw}
.chain>div>div{display:flex;flex-direction:column;align-items:center;text-align:center;gap:1vh;background:#fff;border:2px solid #E3DED2;border-radius:14px;padding:1.6vh 1vw;height:100%;box-sizing:border-box}
.chain i{font-style:normal;font-family:var(--fh);width:1.8em;height:1.8em;border-radius:50%;background:#0B6B4F;color:#fff;display:grid;place-items:center;font-size:clamp(20px,3.6vh,40px)}
.chain b{font-family:var(--fh);font-size:clamp(22px,4.2vh,48px);color:var(--navy)}.chain span{font-size:clamp(18px,3.5vh,40px);line-height:1.45}
.score{display:flex;gap:2vw;justify-content:center}
.score>div{display:flex;align-items:center;gap:.8vw;background:#FFFBF0;border:2px solid #EAD9A8;border-radius:14px;padding:.4em 1em}
.score b{font-family:var(--fh);font-size:clamp(18px,3.6vh,40px);color:var(--navy)}.score i{font-style:normal;font-family:var(--fh);font-size:clamp(26px,5vh,58px);color:var(--gold);min-width:1.4em;text-align:center}
.score button{font-family:var(--fh);font-size:clamp(20px,4vh,44px);width:1.6em;height:1.6em;border-radius:50%;border:2px solid #EAD9A8;background:#fff;cursor:pointer}
.sb.o-0,.sb.o-1,.sb.o-2,.sb.o-3,.sb.o-4{color:var(--navy);border-color:#C9D3DD}.sb.o-0.ok,.sb.o-1.ok,.sb.o-2.ok,.sb.o-3.ok,.sb.o-4.ok{background:#0B6B4F;border-color:#0B6B4F;color:#fff}
.sbs{flex-wrap:wrap;justify-content:flex-end;max-width:52%}
.tilawa{display:flex;align-items:center;gap:.8vw;background:#F6FAF4;border:2px solid #C9DCC4;border-radius:12px;padding:.3em .8em}
.tilawa span{font-family:var(--fh);font-weight:800;color:#0B6B4F;font-size:clamp(18px,3.4vh,38px);white-space:nowrap}
.tilawa audio{height:clamp(32px,5vh,52px);width:min(30vw,420px)}
.slide .flip.box{font-size:clamp(20px,4vh,46px);font-weight:700;line-height:1.45}.slide .flip .ayah{font-size:1.1em;line-height:1.7}
'''
EXTRA_CSS_OWN += '.tps{max-width:88vw;gap:.6vw}.tps>span{font-size:clamp(18px,3.5vh,40px);padding:.25em .6em}.tps .timer{font-size:clamp(18px,3.5vh,40px);padding:.25em .7em}'
EXTRA_CSS_OWN += '.tps .timer{flex:0 0 auto;width:auto}.bimg{max-height:60vh;max-width:88vw}.bookimg.sm .bimg{max-height:36vh}'
EXTRA_CSS_OWN += '.tps .timer{max-width:34vw}.tps .timer .tl{flex:0 1 auto}'
EXTRA_CSS_OWN += '''
.read3{display:flex;flex-direction:column;gap:1.4vh;width:84vw}
.read3>div>div{display:flex;align-items:center;gap:1.4vw;background:#fff;border:2px solid #E3DED2;border-inline-start:8px solid var(--navy);border-radius:14px;padding:1.2vh 1.6vw}
.read3 b{font-family:var(--fh);color:#fff;background:var(--navy);border-radius:50%;width:1.7em;height:1.7em;display:grid;place-items:center;flex:0 0 auto;font-size:clamp(20px,3.6vh,40px)}
.read3 span{font-size:clamp(22px,4.4vh,50px);line-height:1.5;font-weight:700}.read3 i{font-style:normal;color:#6B6250;font-size:.8em}
.idcard{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1.2vw;width:88vw}
.idcard>div{display:flex;flex-direction:column;gap:.8vh;align-items:center;text-align:center;background:#fff;border:2px solid #E3DED2;border-top:6px solid #0B6B4F;border-radius:14px;padding:1.6vh 1vw}
.idcard b{font-family:var(--fh);font-size:clamp(22px,4.2vh,48px);color:#0B6B4F}.idcard span{font-size:clamp(19px,3.7vh,42px);line-height:1.45;font-weight:700}
.chips{display:flex;flex-wrap:wrap;gap:1.2vh 1vw;justify-content:center;max-width:88vw}
.chips span{background:#fff;border:2px solid #C9DCC4;border-radius:999px;padding:.5vh 1.4vw;font-size:clamp(19px,3.7vh,42px);font-weight:700;color:#0B3D2E}
.cases{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:1vw;width:92vw}
.cases>div{display:flex}.slide .cases .flip.case{flex:1;max-width:none;justify-content:flex-start;gap:.8vh;padding:1vh .8vw}
.cimg{width:100%;max-height:22vh;object-fit:contain;border-radius:10px}
.case .cap{font-size:clamp(16px,2.9vh,32px);line-height:1.45;font-weight:700;white-space:normal}
.case .hid .kk{font-size:clamp(16px,3vh,34px)!important;line-height:1.45}
'''
EXTRA_CSS_OWN += '.hdr .timer{flex:0 0 auto;width:auto;max-width:30vw}.hdr .timer .tl{flex:0 1 auto}'
