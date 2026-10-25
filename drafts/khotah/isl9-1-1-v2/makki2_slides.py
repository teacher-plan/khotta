# درس «المكيّ والمدنيّ» (علوم القرآن) — التربية الإسلامية، الصف التاسع، الفصل الأول، الوحدة الأولى، الدرس الأول.
# النسخة ٢ (تجربة): استراتيجية «اقرأ ← نظّم ← ثبّت» للمحتوى النصّي الكثيف بدل التدرّج «أنا ← نحن ← أنتم»:
#   اقرأ: فقرة الكتاب مكثّفةً في جملةٍ مفتاحية، كلماتها المفتاحية فراغاتٌ يستنتجها الطلبة ثم تُكشف بضغطة.
#   نظّم: الفقرة نفسها في منظّمٍ بصري (خطّ زمني، جدول موازنة، شجرة، بطاقات).
#   ثبّت: لعبةٌ قصيرة فورية (تصنيف، صواب وخطأ) تُصحَّح على الشاشة.
#   وفي الختام خريطةٌ ذهنية للدرس كله، ثم أسئلة «أقيّم تعلّمي».
# المراجع (أرقام مطبوعة): كتاب الطالب ص٢٠–٢٤، دليل المعلم ص٢٩–٣٧. الآيات من quran.com بالرسم العثماني.
use('frac_common')
QF = open(os.path.join(HERE, 'amiri_quran.css'), encoding='utf-8').read()
FF = open(os.path.join(HERE, 'fonts_sub.css'), encoding='utf-8').read() if os.path.exists(os.path.join(HERE, 'fonts_sub.css')) else ''

def AY(t, ref_=''):
    return f'<span class="ayah">﴿{t}﴾</span>' + (f'<span class="aref">[{ref_}]</span>' if ref_ else '')
def MK(t): return f'<b class="mk">{t}</b>'
def MD(t): return f'<b class="md">{t}</b>'
def KW(t): return f'<button class="kw" onclick="event.stopPropagation();this.classList.add(\'on\')"><span>{t}</span></button>'   # كلمةٌ مفتاحية تُكشف بضغطة
def READ(pg, sentence, note=''):   # «اقرأ»: الجملة المفتاحية للفقرة
    return f'<div class="row hdr"><span class="stage s1">١ اقرأ</span>{ref("كتاب الطالب ص " + pg)}</div>' + f'<div class="keyline st">{sentence}</div>'
def STAGE(n): return {2: '<span class="stage s2">٢ نظّم</span>', 3: '<span class="stage s3">٣ ثبّت</span>'}[n]
def SORT(items, opts=('مكّيّة', 'مدنيّة'), cols=2):   # لعبة تصنيف: لكلّ بطاقةٍ أزرار، والصحيح يتلوّن والخطأ يهتزّ
    cls = ['o-mk', 'o-md', 'o-x']
    out = []
    for q, ok, *w in items:
        bt = ''.join(f'<button class="sb {cls[i] if len(opts) == 2 else "o-" + str(i)}" onclick="srt(event,this,{i})">{o}</button>' for i, o in enumerate(opts))
        out.append(st(f'<div class="sc" data-ok="{ok}"><div class="sqx">{q}</div><div class="sbs">{bt}</div>' + (f'<div class="sw">{w[0]}</div>' if w else '') + '</div>'))
    return f'<div class="sort c{cols}">' + ''.join(out) + '</div>'
TF = lambda items: SORT(items, ('✔ صواب', '✘ خطأ'))

S.append(cover('١', 'المكيّ والمدنيّ', 'الصف التاسع · علوم القرآن', 'كتاب الطالب ص ٢٠ – ٢٤'))
S.append(goals(['أُعرّف <b>المكيّ والمدنيّ</b>', 'أُبيّن <b>طرق معرفة</b> المكيّ والمدنيّ', 'أُوازن بين المكيّ والمدنيّ <b>من حيث الضوابط</b>',
                'أستخلص <b>فوائد</b> معرفة المكيّ والمدنيّ', 'أُدرك <b>أهمية</b> علم المكيّ والمدنيّ']).replace('</section>', tn('مخرجات التعلّم من دليل المعلم ص٢٩. عدد الحصص المقترح: حصتان. طريقة العرض: كل فقرة من الكتاب تمرّ بثلاث محطات: ١ اقرأ (الجملة المفتاحية، والطلبة يستنتجون الكلمات المخفية قبل كشفها)، ٢ نظّم (منظّم بصري)، ٣ ثبّت (لعبة تصنيف أو صواب وخطأ).') + '</section>'))
S.append(slide(f'''<h2>طريقتنا في هذا الدرس</h2>
<div class="way">{st('<div class="w1"><b>١ اقرأ</b><span>نقرأ الفقرة ونستخرج كلماتها المفتاحية</span></div>')}{st('<div class="w2"><b>٢ نظّم</b><span>نرتّبها في شكلٍ واحد يسهل حفظه</span></div>')}{st('<div class="w3"><b>٣ ثبّت</b><span>نلعب لعبةً قصيرة نتأكّد بها أننا فهمنا</span></div>')}</div>'''))

# ═══════════ ١: نزول القرآن في مكّة والمدينة (ص٢٠) ═══════════
S.append(section('نزول القرآن في مكّة والمدينة', 'كتاب الطالب ص ٢٠'))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">تهيئة 📖</span>{ref('دليل المعلم ص ٣٠')}</div><h2>افتح المصحف على فهرس السور</h2>
<p class="lead">ما المعلومات الموجودة في فهرس السور؟</p>
{FLIPS([('<span class="hint">في الفهرس</span>', 'اسم السورة · رقمها · رقم الصفحة · <u>مكّيّة أو مدنيّة</u>', 'وهذا موضوع درسنا، وهو أحد علوم القرآن الكريم')], 'flex:1;min-width:46vw')}''' + tn('التهيئة من الدليل ص٣٠.')))
S.append(slide(READ('٢٠', f'أنزل الله القرآن على نبيّه ﷺ {KW("مفرّقاً")} في {KW("ثلاثٍ وعشرين")} سنة، مكث منها قرابة {KW("ثلاث عشرة")} سنة في {KW("مكّة")}') + f'''
{st(f'<div class="tl"><div class="tl-mk"><b>في مكّة</b><span>قرابة ١٣ سنة</span></div><div class="tl-h"><i></i><b>الهجرة</b></div><div class="tl-md"><b>في المدينة</b><span>بقيّة المدّة</span></div></div>')}
<p class="hint st">مجموع المدّة: ٢٣ سنة</p>''' + tn('الكتاب ص٢٠. الدليل ص٣١: استخدم مخططاً زمنياً يوضّح متى نزل القرآن في مكة وبعد الهجرة. اطلب من الطلبة توقّع الكلمة المخفية قبل الضغط عليها.')))
S.append(slide(f'''<div class="row hdr">{STAGE(2)}{ref('كتاب الطالب ص ٢٠')}</div><h2>كيف اختلف الحال بين مكّة والمدينة؟</h2>
<table class="cmp"><thead><tr><th></th><th class="mk">في مكّة</th><th class="md">في المدينة</th></tr></thead><tbody>
<tr class="st"><th>الحُكم</th><td>للجاهليّة والشرك</td><td>للإسلام</td></tr>
<tr class="st"><th>الموضوعات</th><td>عبادة الله وحده، والردّ على المشركين، والبعث، وقصص الأمم</td><td>التشريع والأحكام، والعبادات والمعاملات، والجهاد</td></tr>
<tr class="st"><th>المخاطَبون</th><td>المشركون، أهل الفصاحة والبيان</td><td>المؤمنون، وأهل الكتاب، وكشف المنافقين</td></tr>
<tr class="st"><th>الأسلوب</th><td>قويّ: «كلّا»، القسم، ضرب المثل</td><td>هادئٌ مفصّل</td></tr>
<tr class="st"><th>الطول</th><td>آياتٌ وسورٌ <b>قصيرة</b></td><td>آياتٌ وسورٌ <b>طويلة</b></td></tr>
</tbody></table>''' + tn('من نص الكتاب ص٢٠ كله في جدول واحد. «هادئ مفصّل» وصفٌ مقابل من إعداد العرض، والكتاب يذكر صراحةً: تنظيم شؤون المسلمين، وطول الآيات والسور. كلمات القوة من الكتاب: كلّا، الصاخّة، القارعة، الغاشية، الواقعة. إثراء الدليل ص٣٤: تكرّرت «كلّا» في النصف الأخير من القرآن لأن أكثره نزل بمكة وأكثر أهلها جبابرة.')))
S.append(slide(f'''<div class="row hdr">{STAGE(3)}<span class="hint">اضغط على الإجابة</span></div><h2>مكّة أم المدينة؟</h2>
{SORT([('دعوةٌ إلى عبادة الله وحده', 0), ('بيان أحكام العبادات والمعاملات', 1), ('كلماتٌ قويّة مثل: القارعة، الغاشية', 0), ('آياتٌ طويلة تنظّم شؤون المسلمين', 1)], ('مكّة', 'المدينة'))}''' + tn('اقرأ البطاقة، واطلب من الطلبة رفع الأيدي (يمين: مكة، يسار: المدينة)، ثم اضغط الإجابة التي اختارها أكثرهم.')))

# ═══════════ ٢: تعريف المكيّ والمدنيّ (ص٢٠–٢١) ═══════════
S.append(section('تعريف المكيّ والمدنيّ', 'كتاب الطالب ص ٢٠ – ٢١'))
S.append(slide(READ('٢٠', f'المكيّ ما نزل {KW("قبل الهجرة")} وإن كان بغير مكّة، والمدنيّ ما نزل {KW("بعد الهجرة")} وإن كان بمكّة') + f'''
<div class="rule st"><span>العبرة</span><b>بزمن النزول</b><span>لا بمكانه</span></div>''' + tn('الكتاب ص٢٠: وبناءً على اعتبار الزمان… الدليل ص٣٢: اعرض بطاقات تعريفية توضّح المفهوم.')))
S.append(slide(f'''<div class="row hdr">{STAGE(2)}{ref('كتاب الطالب ص ٢٠ – ٢١')}</div><h2>الهجرة هي الفاصل</h2>
<div class="axis">{st('<div class="ax-mk"><b>المكيّ</b><span>كلّ ما نزل قبلها</span></div>')}<div class="ax-mid"><b>الهجرة</b></div>{st('<div class="ax-md"><b>المدنيّ</b><span>كلّ ما نزل بعدها</span></div>')}</div>
{st('<div class="ayahbox">' + AY('إِنَّ ٱللَّهَ يَأْمُرُكُمْ أَن تُؤَدُّوا۟ ٱلْأَمَـٰنَـٰتِ إِلَىٰٓ أَهْلِهَآ', 'النساء: ٥٨') + '</div>')}
{st('<div class="ex3"><span>📍 نزلت <b>في جوف الكعبة</b></span><span>🕓 <b>عام الفتح</b>، بعد الهجرة</span><span>⬅ فهي ' + MD('مدنيّة') + '</span></div>')}''' + tn('الكتاب ص٢٠–٢١. إثراء الدليل ص٣٦: نزلت حين أخذ النبي ﷺ مفتاح الكعبة من عثمان بن طلحة ثم ردّه إليه.')))
S.append(slide(f'''<div class="row hdr">{STAGE(3)}<span class="hint">العبرة بالزمان</span></div><h2>مكّيّة أم مدنيّة؟</h2>
{SORT([('آيةٌ نزلت <b>بعد</b> الهجرة في مكّة', 1, 'نزلت بعد الهجرة'), ('آيةٌ نزلت <b>قبل</b> الهجرة خارج مكّة', 0, 'نزلت قبل الهجرة'), ('آية النساء ٥٨: نزلت في جوف الكعبة عام الفتح', 1, 'عام الفتح بعد الهجرة'), ('﴿ٱلْيَوْمَ أَكْمَلْتُ لَكُمْ دِينَكُمْ﴾ نزلت بعرفة في حجّة الوداع', 1, 'حجّة الوداع بعد الهجرة')])}''' + tn('المثال الرابع (المائدة: ٣) من إثراء الدليل ص٣٦.')))

# ═══════════ ٣: طريقا معرفة المكيّ والمدنيّ (ص٢١) ═══════════
S.append(section('كيف نعرف المكيّ والمدنيّ؟', 'كتاب الطالب ص ٢١'))
S.append(slide(READ('٢١', f'لمعرفة المكيّ والمدنيّ طريقان: {KW("السماعيّ النقليّ")} و{KW("القياسيّ الاجتهاديّ")}') + tn('الكتاب ص٢١، والدليل ص٣٢ (المخرج الثاني).')))
S.append(slide(f'''<div class="row hdr">{STAGE(2)}{ref('كتاب الطالب ص ٢١')}</div><h2>طريقا المعرفة</h2>
<div class="tree2"><div class="t-root">طرق معرفة المكيّ والمدنيّ</div><div class="t-kids">
{st('<div class="t-k k1"><b>السماعيّ النقليّ</b><span>يستند إلى <u>الرواية الصحيحة</u> عن الصحابة الذين شهدوا النزول</span><em>أداته: النقل</em></div>')}
{st('<div class="t-k k2"><b>القياسيّ الاجتهاديّ</b><span>يستند إلى <u>خصائص</u> المكيّ والمدنيّ <u>وضوابطهما</u></span><em>أداته: العقل</em></div>')}</div></div>
<p class="lead st">والنقل والعقل هما طريقا المعرفة السليمة والتحقيق العلميّ</p>''' + tn('الكتاب ص٢١.')))
S.append(slide(f'''<div class="row hdr">{STAGE(2)}{ref('كتاب الطالب ص ٢١')}</div><h2>مثالٌ على الطريق النقليّ</h2>
<p class="lead">روت أمّ المؤمنين عائشة رضي الله عنها أن قوله تعالى:</p>
<div class="ayahbox st">{AY('بَلِ ٱلسَّاعَةُ مَوْعِدُهُمْ وَٱلسَّاعَةُ أَدْهَىٰ وَأَمَرُّ', 'القمر: ٤٦')}</div>
<div class="ex3 st"><span>نزلت وهي طفلةٌ <b>في مكّة</b></span><span>وسورتا البقرة والنساء نزلتا <b>في المدينة</b></span></div>''' + tn('الكتاب ص٢١، والحاشية: البخاري، الصحيح، رقم ٤٩٩٣.')))
S.append(slide(f'''<div class="row hdr">{STAGE(3)}</div><h2>أيّ الطريقين؟</h2>
{SORT([('صحابيٌّ يروي أين ومتى نزلت الآية', 0, 'رواية: نقل'), ('نعرف السورة من علامةٍ فيها كالسجدة', 1, 'ضابط: عقل'), ('حديث عائشة رضي الله عنها عن سورة القمر', 0, 'رواية: نقل'), ('سورةٌ بدأت بالحروف المقطّعة فنحكم أنها مكّيّة', 1, 'ضابط: عقل')], ('السماعيّ', 'القياسيّ'))}''' + tn('الدليل ص٣٣: نشاط تفاعلي، تصنيف وفق الطريقة (السماعية أو القياسية).')))

# ═══════════ ٤: الضوابط (ص٢٢) ═══════════
S.append(section('ضوابط المكيّ والمدنيّ', 'أتعاون مع زملائي · كتاب الطالب ص ٢٢'))
S.append(slide(READ('٢٢', f'{KW("الضوابط")} علاماتٌ في السورة نعرف بها أنها مكّيّة أو مدنيّة، وهي أداة الطريق {KW("القياسيّ")}') + tn('التعريف من جدول المفاهيم في الدليل ص٢٩.')))
CTRL = [('انفردت بـ' + AY('يَـٰٓأَيُّهَا ٱلنَّاسُ') + ' دون نداء المؤمنين', 0), ('فيها قصص الأنبياء والأمم السابقة', 0), ('ذُكر فيها المنافقون إلا سورة العنكبوت', 1),
        ('فيها إذنٌ بالقتال وبيانٌ لأحكامه', 1), ('فيها سجدةٌ إلا سورة الحجّ', 0), ('فيها ' + AY('يَـٰٓأَيُّهَا ٱلَّذِينَ ءَامَنُوٓا۟'), 1),
        ('فيها قصّة آدم سوى سورة البقرة', 0), ('فيها ' + AY('يَـٰٓأَيُّهَا ٱلنَّبِىُّ') + ' أو ' + AY('يَـٰٓأَيُّهَا ٱلرَّسُولُ'), 1),
        ('ابتدأت بالحروف المقطّعة إلا البقرة وآل عمران', 0), ('فيها ذكر الحدود والفرائض (المواريث)', 1)]
S.append(slide(f'''<div class="row hdr">{STAGE(3)}{ref('أتعاون مع زملائي ص ٢٢')}</div><h2>صنّفوا الضوابط (١)</h2>
{SORT([(f'كلّ سورةٍ {q}', k) for q, k in CTRL[:5]], cols=1)}''' + tn('نشاط الكتاب ص٢٢ نفسه، بالعمل التعاوني (الدليل ص٣٣). الإجابات من الدليل ص٣٣: المكية ١ و٢ و٥ و٧ و٩، والمدنية ٣ و٤ و٦ و٨ و١٠. وفي الكتاب خطأ مطبعي: رقما الضابطين الأوّلين كلاهما «١».')))
S.append(slide(f'''<div class="row hdr">{STAGE(3)}{ref('أتعاون مع زملائي ص ٢٢')}</div><h2>صنّفوا الضوابط (٢)</h2>
{SORT([(f'كلّ سورةٍ {q}', k) for q, k in CTRL[5:]], cols=1)}''' + tn('الضوابط ٦ إلى ١٠.')))
S.append(slide(f'''<div class="row hdr">{STAGE(2)}{ref('دليل المعلم ص ٣٣')}</div><h2>الضوابط في لوحةٍ واحدة</h2>
<div class="two">{st('<div class="pan mkp"><b>علامات المكيّ</b><ul><li>' + AY('يَـٰٓأَيُّهَا ٱلنَّاسُ') + ' وحدها</li><li>قصص الأنبياء والأمم</li><li>قصّة آدم (سوى البقرة)</li><li>السجدة (إلا الحجّ)</li><li>الحروف المقطّعة (إلا البقرة وآل عمران)</li></ul></div>')}
{st('<div class="pan mdp"><b>علامات المدنيّ</b><ul><li>' + AY('يَـٰٓأَيُّهَا ٱلَّذِينَ ءَامَنُوٓا۟') + '</li><li>' + AY('يَـٰٓأَيُّهَا ٱلنَّبِىُّ') + ' أو ' + AY('يَـٰٓأَيُّهَا ٱلرَّسُولُ') + '</li><li>المنافقون (إلا العنكبوت)</li><li>الإذن بالقتال وأحكامه</li><li>الحدود والفرائض</li></ul></div>')}</div>''' + tn('خلاصة إجابة النشاط من الدليل ص٣٣ في لوحة واحدة. نبّه على الاستثناءات بين القوسين.')))
S.append(slide(f'''<div class="row hdr"><span class="qbadge">💡 أضيء</span>{ref('كتاب الطالب ص ٢٢')}</div><h2>انتبه لهاتين المعلومتين</h2>
<div class="lamp">{st('<div><b>السورة توصف بأكثر آياتها</b><span>فقد يكون في المكّيّة آياتٌ مدنيّة، وفي المدنيّة آياتٌ مكّيّة</span></div>')}{st('<div><b>المكيّ والمدنيّ يتّفقان</b><span>في جزالة الألفاظ وروعة التراكيب، فهو كلّه في أعلى ذُرا البلاغة المعجِزة</span></div>')}</div>''' + tn('الإضاءة في الكتاب ص٢٢، والدليل ص٣٢.')))
S.append(slide(f'''<div class="row hdr">{STAGE(3)}{ref('أقيّم تعلّمي (ثالثاً) ص ٢٤')}</div><h2>صنّف الآية، واذكر الضابط</h2>
{SORT([(AY('يسٓ ١ وَٱلْقُرْءَانِ ٱلْحَكِيمِ', 'يس: ١–٢'), 0, 'ابتدأت بالحروف المقطّعة'), (AY('يَـٰٓأَيُّهَا ٱلرَّسُولُ بَلِّغْ مَآ أُنزِلَ إِلَيْكَ مِن رَّبِّكَ', 'المائدة: ٦٧'), 1, 'فيها ﴿يَـٰٓأَيُّهَا ٱلرَّسُولُ﴾'), (AY('كَلَّا لَا تُطِعْهُ وَٱسْجُدْ وَٱقْتَرِب ۩', 'العلق: ١٩'), 0, 'فيها «كلّا» وسجدة')], cols=1)}''' + tn('من «أقيّم تعلّمي» ثالثاً ص٢٤، والإجابات من الدليل ص٣٧.')))

# ═══════════ ٥: الفوائد والأهمية (ص٢١ و٢٣) ═══════════
S.append(section('لماذا نتعلّم المكيّ والمدنيّ؟', 'كتاب الطالب ص ٢١ و ٢٣'))
S.append(slide(READ('٢١', f'اهتمّ العلماء بهذا العلم لأهميّته لباقي علوم القرآن، كـ{KW("أسباب النزول")} و{KW("التفسير")}، وعنايتهم به أعظم دليلٍ على {KW("سلامة القرآن")} من النقص والزيادة والتحريف') + tn('الكتاب ص٢١.')))
S.append(slide(f'''<div class="row hdr">{STAGE(2)}{ref('أتأمّل وأوظّف ص ٢٣')}</div><h2>ثلاث فوائد لمعرفة المكيّ والمدنيّ</h2>
<div class="fan">{st('<div><i>١</i><b>تفسير القرآن</b><span>نعرف زمن نزول الآية والوقائع التي صاحبتها</span></div>')}{st('<div><i>٢</i><b>أساليب الدعوة</b><span>لكلّ مرحلةٍ موضوعاتها وأسلوب خطابها</span></div>')}{st('<div><i>٣</i><b>السيرة النبويّة</b><span>تتابع الوحي ساير أحداث العهدين</span></div>')}</div>''' + tn('إجابة «أتأمّل وأوظّف» من الدليل ص٣٥. وفي حياتنا (الدليل ص٣٤–٣٥): نختار الأسلوب المناسب لمن نخاطبه، والموضوعات المناسبة لحاله، ونتدرّج في الدعوة.')))
S.append(slide(f'''<div class="row hdr">{STAGE(3)}{ref('أقيّم تعلّمي (ثانياً) ص ٢٣')}</div><h2>علّل: العقائد في المكيّ، والأحكام في المدنيّ</h2>
<button class="flip box col" style="min-width:60vw"><span class="tap">👆 الإجابة</span><span class="hid col"><span class="kk c-we">لأن أهل مكّة كانوا مشركين يعبدون الأوثان، ولهم عاداتٌ سيّئة</span><span class="why">فصُحّحت العقيدة أولاً، ثم جاءت الأحكام التي تنظّم حياتهم</span></span></button>''' + tn('إجابة الدليل ص٣٧ (ثانياً).')))

# ═══════════ ٦: الخلاصة ═══════════
S.append(section('خلاصة الدرس', 'خريطةٌ واحدة وتحدٍّ أخير'))
S.append(slide(f'''<h2>خريطة الدرس</h2>
<div class="mm"><div class="mm-c">المكيّ<br>والمدنيّ</div>
{st('<div class="mm-b b1"><b>التعريف</b><span>' + MK('المكيّ') + ' قبل الهجرة · ' + MD('المدنيّ') + ' بعدها</span></div>')}
{st('<div class="mm-b b2"><b>طريقا المعرفة</b><span>النقل (الرواية) · العقل (الضوابط)</span></div>')}
{st('<div class="mm-b b3"><b>الضوابط</b><span>عشر علاماتٍ في السورة</span></div>')}
{st('<div class="mm-b b4"><b>الفوائد</b><span>التفسير · الدعوة · السيرة</span></div>')}</div>''' + tn('اطلب من الطلبة قبل كشف كل فرع أن يذكروا ما فيه.')))
S.append(slide(f'''<div class="row hdr">{STAGE(3)}{ref('أقيّم تعلّمي (أولاً) ص ٢٣')}</div><h2>تحدّي الخروج: صواب أم خطأ؟</h2>
{TF([('المكيّ ما نزل <u>بمكّة</u>', 1, 'بل ما نزل قبل الهجرة'), ('قصّة آدم في سورة البقرة، فهي <u>مكّيّة</u>', 1, 'البقرة مدنيّة، وهي مستثناة'), ('السماعيّ يعتمد على <u>العقل</u>', 1, 'بل على النقل'), ('نزلت سورة الفتح في السنة السادسة بين مكّة والمدينة، فهي <u>مدنيّة</u>', 0, 'نزلت بعد الهجرة')])}''' + tn('عبارات «أقيّم تعلّمي» أولاً ص٢٣، والإجابات من الدليل ص٣٧: ١) قبل الهجرة ٢) مدنية ٣) النقل ٤) صحيحة.')))
S.append(slide('''<span class="qbadge" style="background:#0A6770;box-shadow:0 4px 0 #05393E">الواجب 🏠</span><h2>أقيّم تعلّمي</h2>
<p class="lead">أكمل «أقيّم تعلّمي» في كتاب الطالب ص ٢٣ و ٢٤</p>''' + tn('اقتراح للمعلم؛ لا يذكر الدليل واجباً مستقلاً.')))

# ═══════════ ملحق: أقيّم تعلّمي ص٢٣–٢٤ ═══════════
S.append(section('ملحق: أقيّم تعلّمي', 'كتاب الطالب ص ٢٣ و ٢٤', '📘', major=False))

S.append(ex(3, 'صنّف الآيات مع التعليل', 'نعلّل بذكر الضابط', [
  (AY('يسٓ ١ وَٱلْقُرْءَانِ ٱلْحَكِيمِ','يس'), 'مكّيّة<small>ابتدأت بالحروف المقطّعة</small>'),
  (AY('وَأَحَلَّ ٱللَّهُ ٱلْبَيْعَ وَحَرَّمَ ٱلرِّبَوٰا۟','البقرة: ٢٧٥'), 'مدنيّة<small>بيّنت الأحكام التفصيليّة</small>'),
  (AY('يَـٰٓأَيُّهَا ٱلرَّسُولُ بَلِّغْ مَآ أُنزِلَ إِلَيْكَ مِن رَّبِّكَ','المائدة: ٦٧'), 'مدنيّة<small>ورد فيها ﴿يَـٰٓأَيُّهَا ٱلرَّسُولُ﴾</small>'),
  (AY('وَلَا تَقْتُلُوٓا۟ أَوْلَـٰدَكُمْ خَشْيَةَ إِمْلَـٰقٍ','الإسراء: ٣١'), 'مكّيّة<small>طرح الأخلاق الذميمة والعادات السيئة</small>'),
  (AY('كَلَّا لَا تُطِعْهُ وَٱسْجُدْ وَٱقْتَرِب ۩','العلق: ١٩'), 'مكّيّة<small>فيها «كلّا» وسجدة</small>')], cols=2, per=2, pg='٢٤'))

SCRIPT = '''<script>
function srt(e,b,i){e.stopPropagation();var c=b.closest('.sc');if(c.classList.contains('done'))return;
 if(+c.dataset.ok===i){c.classList.add('done');b.classList.add('ok');}
 else{b.classList.add('bad');c.classList.remove('shk');void c.offsetWidth;c.classList.add('shk');setTimeout(function(){b.classList.remove('bad')},700);}}
</script>'''
S[-1] = S[-1].replace('</section>', SCRIPT + '</section>')

EXTRA_CSS_OWN = FF + QF + '''
:root:root{--fh:'Noto Kufi Arabic',Tahoma,sans-serif;--fb:'Noto Naskh Arabic','Noto Kufi Arabic',Tahoma,serif;--mkc:#9A4A0C;--mdc:#0B6B4F;--gold:#B8892B;--navy:#123A5A}
body,.slide{font-family:var(--fb)}
.slide h1,.slide h2{color:var(--navy);font-weight:800}
.lead,.hint,.keyline,.sqx,.cmp td,.t-k span,.pan li,.lamp span,.fan span,.mm-b span,.ex3 span,.way span{font-family:var(--fb);font-weight:700}
.ayah{font-family:'Amiri Quran','Amiri',serif;font-size:clamp(28px,5.4vh,64px);line-height:1.9;color:#0B3D2E;font-weight:400}
.sqx .ayah,.pan .ayah,.sort .ayah{font-size:1.15em;line-height:1.6}
.aref{font-family:var(--fb);font-size:clamp(20px,3.8vh,42px);color:#6B6250;margin-inline-start:.5em;white-space:nowrap}
.ayahbox{background:#F6FAF4;border:2px solid #C9DCC4;border-radius:14px;padding:1vh 3vw;text-align:center;max-width:86vw}
.mk{color:var(--mkc)}.md{color:var(--mdc)}
.lead{font-size:clamp(22px,4.4vh,50px);color:#2B2B2B;text-align:center;text-wrap:balance}
.hint{font-size:clamp(18px,3.6vh,40px);color:#5B5B5B}
.stage{font-family:var(--fh);font-weight:800;font-size:clamp(20px,3.6vh,40px);padding:.2em .9em;border-radius:10px;color:#fff}
.s1{background:var(--navy)}.s2{background:var(--gold)}.s3{background:#0B6B4F}
.slide:has(.stage.s1){background:linear-gradient(90deg,transparent 0 calc(100% - 12px),var(--navy) 0)}
.slide:has(.stage.s2){background:linear-gradient(90deg,transparent 0 calc(100% - 12px),var(--gold) 0)}
.slide:has(.stage.s3){background:linear-gradient(90deg,transparent 0 calc(100% - 12px),#0B6B4F 0)}
.keyline{font-size:clamp(28px,6vh,70px);line-height:1.9;text-align:center;max-width:84vw;color:#1F1F1F;font-weight:700;text-wrap:balance}
.kw{font:inherit;color:transparent;background:none;border:0;border-bottom:.08em dashed var(--gold);cursor:pointer;padding:0 .15em;position:relative;transition:color .3s}
.kw::after{content:"؟";position:absolute;inset:0;display:flex;align-items:center;justify-content:center;color:var(--gold);font-family:var(--fh)}
.kw.on{color:var(--mdc);border-bottom:.08em solid var(--mdc);background:#EAF4EE;border-radius:6px}.kw.on::after{content:none}
.way{display:grid;grid-template-columns:repeat(3,1fr);gap:2vw;width:86vw}
.way>div>div{border-radius:16px;padding:3vh 1.5vw;display:flex;flex-direction:column;gap:1.4vh;text-align:center;border:2px solid #E3DED2;background:#fff}
.way b{font-family:var(--fh);font-size:clamp(30px,6vh,70px)}.way span{font-size:clamp(20px,4vh,46px);line-height:1.5}
.w1 b{color:var(--navy)}.w2 b{color:var(--gold)}.w3 b{color:#0B6B4F}
.tl{display:flex;align-items:stretch;width:84vw;border-radius:16px;overflow:hidden;border:2px solid #D8D2C4}
.tl>div{display:flex;flex-direction:column;align-items:center;justify-content:center;padding:2.4vh 1vw;gap:.6vh}
.tl-mk{flex:13;background:#FBF1E6}.tl-md{flex:10;background:#E9F4EF}.tl-h{flex:0 0 auto;background:var(--navy);color:#fff}
.tl b{font-family:var(--fh);font-size:clamp(26px,5.4vh,62px)}.tl span{font-size:clamp(20px,4vh,46px);font-weight:700}
.tl-mk b{color:var(--mkc)}.tl-md b{color:var(--mdc)}.tl-h b{color:#fff;font-size:clamp(22px,4.2vh,48px)}
.cmp{border-collapse:separate;border-spacing:0;width:88vw;background:#fff;border:2px solid #D8D2C4;border-radius:14px;overflow:hidden}
.cmp th,.cmp td{padding:1vh 1.2vw;border-bottom:1px solid #ECE7DC;font-size:clamp(20px,3.6vh,40px);line-height:1.4;text-align:center}
.cmp thead th{font-family:var(--fh);font-size:clamp(22px,4.2vh,48px);background:#FAF7F0}
.cmp tbody th{font-family:var(--fh);color:var(--navy);background:#FAF7F0;white-space:nowrap;width:14%}
.cmp tbody td:nth-child(2){background:#FFFBF6}.cmp tbody td:nth-child(3){background:#F7FBF9}
.cmp tr.st{display:table-row}
.sort{display:grid;gap:1.4vh 1.4vw;width:88vw}.sort.c2{grid-template-columns:1fr 1fr}.sort.c1{grid-template-columns:1fr}
.sc{display:flex;align-items:center;gap:1.2vw;background:#fff;border:2px solid #E3DED2;border-radius:14px;padding:1vh 1.2vw;transition:border-color .3s,background .3s}
.sqx{flex:1;font-size:clamp(22px,4.2vh,48px);line-height:1.45}
.sbs{display:flex;gap:.6vw;flex:0 0 auto}
.sb{font-family:var(--fh);font-weight:800;font-size:clamp(20px,3.6vh,40px);padding:.25em .8em;border-radius:10px;border:2px solid;background:#fff;cursor:pointer}
.o-mk{color:var(--mkc);border-color:#E6C9AE}.o-md{color:var(--mdc);border-color:#B6DACB}
.sb.ok{color:#fff}.o-mk.ok{background:var(--mkc);border-color:var(--mkc)}.o-md.ok{background:var(--mdc);border-color:var(--mdc)}
.sb.bad{background:#FDECEC;border-color:#D64545;color:#B42318}
.sc.done{border-color:#0B6B4F;background:#F5FBF7}.sc.done .sb:not(.ok){opacity:.3}
.sw{display:none;font-size:clamp(16px,3vh,32px);color:#0B6B4F;font-weight:700}.sc.done .sw{display:block}
.sc.shk{animation:shk .45s}@keyframes shk{20%,60%{transform:translateX(8px)}40%,80%{transform:translateX(-8px)}}
.rule{display:flex;align-items:baseline;gap:1.2vw;padding:1.6vh 3vw;border:2px solid var(--gold);border-radius:14px;background:#FFFBF0}
.rule span{font-size:clamp(22px,4.4vh,50px);font-weight:700}.rule b{font-family:var(--fh);font-size:clamp(30px,6.4vh,72px);color:var(--gold)}
.axis{display:flex;width:86vw;align-items:stretch;gap:0}
.axis>div{display:flex;flex-direction:column;align-items:center;justify-content:center}
.axis .st{flex:1;display:flex}.axis .st>div{flex:1;width:100%;box-sizing:border-box}.axis .st>div{padding:1.6vh 1vw;display:flex;flex-direction:column;align-items:center;gap:.4vh;border-radius:14px}
.ax-mk{background:#FBF1E6}.ax-md{background:#E9F4EF}
.ax-mid{padding:0 1.4vw}.ax-mid b{font-family:var(--fh);background:var(--navy);color:#fff;padding:.4em .8em;border-radius:10px;font-size:clamp(20px,4vh,44px)}
.axis b{font-family:var(--fh);font-size:clamp(26px,5vh,58px)}.ax-mk b{color:var(--mkc)}.ax-md b{color:var(--mdc)}.axis span{font-size:clamp(18px,3.6vh,40px);font-weight:700}
.ex3{display:flex;flex-wrap:wrap;gap:1vh 1.4vw;justify-content:center;max-width:88vw}
.ex3 span{background:#fff;border:2px solid #E3DED2;border-radius:12px;padding:.6vh 1.2vw;font-size:clamp(18px,3.6vh,40px)}
.tree2{display:flex;flex-direction:column;align-items:center;gap:2vh;width:88vw}
.t-root{font-family:var(--fh);font-weight:800;font-size:clamp(22px,4.4vh,50px);background:var(--navy);color:#fff;padding:.4em 1.4em;border-radius:12px}
.t-kids{display:grid;grid-template-columns:1fr 1fr;gap:2vw;width:100%}
.t-k{display:flex;flex-direction:column;gap:1vh;align-items:center;text-align:center;background:#fff;border:2px solid #E3DED2;border-top:8px solid;border-radius:14px;padding:2vh 1.4vw}
.k1{border-top-color:var(--gold)}.k2{border-top-color:#0B6B4F}
.t-k b{font-family:var(--fh);font-size:clamp(26px,5vh,58px)}.k1 b{color:var(--gold)}.k2 b{color:#0B6B4F}
.t-k span{font-size:clamp(19px,3.7vh,42px);line-height:1.5}.t-k em{font-style:normal;font-family:var(--fh);font-size:clamp(18px,3.4vh,38px);color:var(--navy)}
.two{display:grid;grid-template-columns:1fr 1fr;gap:2vw;width:88vw}
.pan{background:#fff;border:2px solid;border-radius:14px;padding:1.6vh 1.6vw}.mkp{border-color:#E6C9AE}.mdp{border-color:#B6DACB}
.pan>b{display:block;font-family:var(--fh);font-size:clamp(24px,4.6vh,52px);margin-bottom:1vh}.mkp>b{color:var(--mkc)}.mdp>b{color:var(--mdc)}
.pan ul{margin:0;padding-inline-start:1.2em;display:flex;flex-direction:column;gap:.6vh}.pan li{font-size:clamp(18px,3.5vh,40px);line-height:1.45}
.lamp{display:flex;flex-direction:column;gap:2vh;width:84vw}
.lamp>div>div{display:flex;flex-direction:column;gap:.8vh;background:#FFFBF0;border:2px solid #EAD9A8;border-radius:14px;padding:1.8vh 2vw}
.lamp b{font-family:var(--fh);font-size:clamp(24px,4.8vh,54px);color:var(--gold)}.lamp span{font-size:clamp(20px,4vh,46px);line-height:1.5}
.fan{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1.2vw;width:84vw}
.fan>div>div{display:flex;flex-direction:column;align-items:center;text-align:center;gap:1vh;background:#fff;border:2px solid #E3DED2;border-radius:14px;padding:2.4vh 1.2vw;height:100%;box-sizing:border-box}
.fan i{font-style:normal;font-family:var(--fh);width:1.8em;height:1.8em;border-radius:50%;background:var(--gold);color:#fff;display:grid;place-items:center;font-size:clamp(20px,3.8vh,42px)}
.fan b{font-family:var(--fh);font-size:clamp(24px,4.6vh,52px);color:var(--navy)}.fan span{font-size:clamp(19px,3.7vh,42px);line-height:1.5}
.mm{display:grid;grid-template-columns:1fr auto 1fr;grid-template-rows:auto auto;gap:2vh 2vw;align-items:center;width:88vw}
.mm-c{grid-column:2;grid-row:1/3;font-family:var(--fh);font-weight:800;font-size:clamp(26px,5vh,58px);background:var(--navy);color:#fff;border-radius:50%;width:11em;max-width:26vw;aspect-ratio:1;display:grid;place-items:center;text-align:center;line-height:1.4;font-size:clamp(22px,4.2vh,48px)}
.mm>.st:nth-of-type(1){grid-column:1;grid-row:1}.mm>.st:nth-of-type(2){grid-column:3;grid-row:1}.mm>.st:nth-of-type(3){grid-column:1;grid-row:2}.mm>.st:nth-of-type(4){grid-column:3;grid-row:2}
.mm-b{display:flex;flex-direction:column;gap:.8vh;background:#fff;border:2px solid #E3DED2;border-radius:14px;padding:1.8vh 1.4vw;text-align:center}
.mm-b b{font-family:var(--fh);font-size:clamp(24px,4.6vh,52px)}.mm-b span{font-size:clamp(19px,3.7vh,42px);line-height:1.5}
.b1 b{color:var(--navy)}.b2 b{color:var(--gold)}.b3 b{color:var(--mkc)}.b4 b{color:#0B6B4F}
.slide .flip{max-width:84vw}.slide .flip span{white-space:normal}
.box>span:not(.kk):not(.tap),.why,.flip .hid .why{font-size:clamp(20px,4vh,46px)!important;line-height:1.45}
'''
EXTRA_CSS_OWN += '.sqx u{text-decoration:none;border-bottom:.1em solid #B42318;color:#B42318}.sqx{text-align:start}'
