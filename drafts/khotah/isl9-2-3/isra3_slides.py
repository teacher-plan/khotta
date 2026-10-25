# درس «سورة الإسراء (١٠٥–١١١)» (تفسير) — التربية الإسلامية، الصف التاسع، الفصل الأول، الوحدة الثانية، الدرس الثاني.
# النسخة ٣: «محطّات التدبّر بالأسئلة الكبرى» لطلبة في الخامسة عشرة — بدل «اقرأ ← نظّم ← ثبّت» التي لم تناسب المعلّم.
#   كل محطة: ❓ سؤالٌ كبير أو موقفٌ من الواقع ← 💬 فكّر · زاوج · شارك (مؤقّت) ← 📖 الآية تجيب ← 🧭 في حياتي.
#   تبدأ الحصة باستطلاعٍ يثير الرأي، وتنتهي بتحدّي الفرق (لوحة نقاط) وبطاقة خروج ٣-٢-١.
#   صور الكتاب (الآيات، المفردات، مخطّط الحِكم، سبب النزول، رسما المربّي) مقصوصة من كتاب الطالب في figs/.
# المراجع (أرقام مطبوعة): كتاب الطالب ص٥٦–٦١، دليل المعلم ص٨٧–٩٦. الآيات من quran.com بالرسم العثماني.
exec(open(os.path.join(HERE, 'isl_common.py'), encoding='utf-8').read())
use('figs')
TILAWA = 'https://ict.moe.gov.om/tlawti/video/9/P1/cls9_Islamic_altafsir2.mp4'   # رمز QR في كتاب الطالب ص٥٦ (qrs.ly/ofgtqr4)
def AUDIO():
    return f'<div class="tilawa" onclick="event.stopPropagation()"><span>🔊 التلاوة النموذجية</span><audio controls preload="none" src="{TILAWA}"></audio></div>'
B = {'q': '<span class="stage bq">❓ سؤال المحطة</span>', 'd': '<span class="stage bd">📖 نتدبّر</span>', 'l': '<span class="stage bl">🧭 في حياتي</span>',
     'c': '<span class="stage bc">🏆 تحدّي الفرق</span>'}
def HDR(k, r=''): return f'<div class="row hdr">{B[k]}{ref(r) if r else ""}</div>'
def BIGQ(q, sub='', mins=2):   # السؤال الكبير: يفكّر الطالب وحده ثم مع زميله ثم يشارك الصف
    return (f'<div class="bigq st"><b>{q}</b>' + (f'<span>{sub}</span>' if sub else '') + '</div>'
            f'<div class="tps st"><span>🤔 فكّر وحدك</span><i>←</i><span>👥 ناقش زميلك</span><i>←</i><span>🙋 شارك الصف</span>{timer(mins)}</div>')
def POLL(q, opts):   # استطلاع رأي: يضغط المعلّم الخيار بعدد الأيدي المرفوعة
    bt = ''.join(f'<button class="pl" onclick="event.stopPropagation();var n=this.querySelector(\'i\');n.textContent=(+n.textContent||0)+1"><b>{o}</b><i>٠</i></button>' for o in opts)
    return f'<div class="bigq st"><b>{q}</b></div><div class="poll st">{bt}</div>'
def SCEN(who, text): return f'<div class="scen st"><span class="who">{who}</span><p>{text}</p></div>'
def OPT(items, opts): return SORT(items, opts, cols=1)
def VR(t, r=''):
    return re.sub(r'﴿([٠-٩]+)﴾', r'<i class="an">\1</i>', AY(t, r).replace('<span class="ayah">﴿', '<span class="ayah">⁅', 1)).replace('⁅', '﴿', 1)

S.append(cover('٢', 'سورة الإسراء (١٠٥ – ١١١)', 'الصف التاسع · تفسير · الوحدة الثانية', 'كتاب الطالب ص ٥٦ – ٦١'))
S.append(goals(['أتلو الآيات <b>(١٠٥–١١١)</b> من سورة الإسراء مراعياً أحكام التجويد', 'أتعرّف <b>معاني</b> بعض المفردات والتراكيب', 'أُبيّن <b>المعنى الإجمالي</b> للآيات',
                'أستنتج <b>القيم</b> المستفادة من الآيات', 'أوضّح <b>الحكمة</b> من نزول القرآن منجّماً']).replace('</section>', tn('مخرجات التعلّم من دليل المعلم ص٨٧ (والسادس: يعظّم القرآن الكريم). الحصص المقترحة: ٣. طريقة العرض: خمس محطات، في كلٍّ منها سؤالٌ كبير يناقشه الطلبة (فكّر · زاوج · شارك) قبل أن تُعرض الآية التي تجيب عنه، ثم ربطٌ بالحياة. وفي الختام تحدّي الفرق.') + '</section>'))

# ═══════════ الانطلاقة ═══════════
S.append(section('الانطلاقة', 'ما رأيك أنت؟'))
S.append(slide(f'''{HDR('q', 'دليل المعلم ص ٨٨')}
{POLL('لو نزل القرآن كتاباً كاملاً في يومٍ واحد… هل كان ذلك أفضل؟', ['نعم، أسهل', 'لا', 'لستُ متأكّداً'])}
<p class="hint st">احتفظ برأيك… سنعود إليه في المحطة الأولى</p>''' + tn('بديلٌ مثيرٌ للرأي عن أسئلة التهيئة في الدليل ص٨٨ (كم جزءاً في القرآن؟ كم نستغرق لقراءة جزء؟ هل يمكن أن نحفظ القرآن مرّةً واحدة؟). اطلب رفع الأيدي واضغط الخيار بعدد الأيدي.')))
S.append(slide(f'''<div class="row hdr"><span class="stage bd">📖 أتلو وأتدبّر</span>{ref('كتاب الطالب ص ٥٦')}{AUDIO()}</div>
<div class="bookimg st">{FIG('ayat', 'bimg', 'الآيات ١٠٥–١١١ من سورة الإسراء كما في كتاب الطالب')}</div>''' + tn('المخرج الأول (الدليل ص٨٨): تلاوة نموذجية (زرّ التلاوة يشغّل تسجيل رمز QR في الكتاب، ويحتاج إنترنت)، ثم يتلو بعض الطلبة ويصوّب لهم زملاؤهم (تعليم الأقران). الآية ١٠٩ موضع سجدة.')))
S.append(slide(f'''<div class="row hdr"><span class="stage bd">📖 أتعرّف المعنى</span>{ref('كتاب الطالب ص ٥٦')}</div>
<div class="bookimg st">{FIG('vocab', 'bimg', 'جدول أتعرّف المعنى: مكث، يخرّون للأذقان، تخافت، كبّره')}</div>
{OPT([('من أمارات التضرّع والإخبات', 1, '﴿يَبْكُونَ﴾'), ('تعظيم الله تعالى وتوقيره', 0, '﴿وَكَبِّرْهُ﴾')], ('كَبِّرْهُ', 'يَبْكُونَ', 'سُجَّدًا', 'سُبْحَانَ رَبِّنَا'))}''' + tn('المخرج الثاني (الدليل ص٨٩). العبارتان من «أقيّم تعلّمي» أولاً ص٦٠، والبقية في تحدّي الفرق.')))

# ═══════════ المحطة ١: لماذا ٢٣ سنة؟ ═══════════
S.append(section('المحطة ١: لماذا ٢٣ سنة؟', 'الآيتان ١٠٥ – ١٠٦'))
S.append(slide(f'''{HDR('q')}
{BIGQ('لماذا لم ينزل القرآن مرّةً واحدة، بل في ثلاثٍ وعشرين سنة؟', 'تذكّر رأيك في الاستطلاع: هل تغيّر؟')}''' + tn('دقيقتان للتفكير والنقاش. اقبل كل الإجابات المعقولة واكتب أبرزها على السبورة، ثم انتقل إلى الآية.')))
S.append(slide(f'''{HDR('d', 'كتاب الطالب ص ٥٦ – ٥٧')}
<div class="ayahbox st">{AY('وَقُرْءَانًا فَرَقْنَـٰهُ لِتَقْرَأَهُۥ عَلَى ٱلنَّاسِ عَلَىٰ مُكْثٍ وَنَزَّلْنَـٰهُ تَنزِيلًا', 'الإسراء: ١٠٦')}</div>
<div class="bookimg st">{FIG('hikam', 'bimg', 'مخطّط نزول القرآن من اللوح المحفوظ إلى السماء الدنيا جملةً ثم إلى النبي منجّماً، وحِكَمه الخمس')}</div>''' + tn('الكتاب ص٥٧ ومخطّط ص٥٩: نزل جملةً واحدة إلى السماء الدنيا في ليلة القدر، ثم منجّماً على النبي ﷺ. الدليل ص٩٠ (س٢ و٣): الآية الدالة على نزوله مفرّقاً هي ١٠٦، والحكمة أن يقرأه على الناس في تؤدة وتمهّل.')))
S.append(slide(f'''<div class="row hdr"><span class="stage bc">👥 أتعاون مع زملائي</span>{ref('كتاب الطالب ص ٥٩')}</div><h2>أيّ حكمةٍ في كلّ موقف؟</h2>
{OPT([('يتنزّل الوحي بما يثبّت قلبه ﷺ، فله في قصص الأنبياء أسوة', 0), ('نزوله مفرّقاً خير عونٍ على حفظه وتدبّره في تؤدة', 1), ('مع تباعد أزمانه جاء كالعقد المنتظم، محكم النسج', 2), ('تربية الأمّة بالسير بها خطوةً خطوة', 3), ('يسأل المشركون أسئلة تعجيز، فتنزل الآيات تُفحمهم', 4)], ('التثبيت', 'التيسير', 'الدلالة', 'التدرّج', 'التحدّي'))}''' + tn('نشاط الكتاب ص٥٩ في مجموعات (الدليل ص٩٢–٩٣). الإجابات من الدليل ص٩٣.')))
S.append(slide(f'''{HDR('l')}<h2>وأنت… كيف تحفظ سورةً طويلة؟</h2>
{FLIPS([('دفعةً واحدة في ليلة الاختبار؟', 'لا… شيئاً فشيئاً مع المراجعة', 'وهذا ما يُسمّى التدرّج: سنّةٌ في نزول القرآن نفسه')], 'flex:1;min-width:60vw')}''' + tn('ربطٌ بالحياة من إعداد العرض، مبنيٌّ على حكمة «تيسير حفظه وفهمه».')))

# ═══════════ المحطة ٢: هل يحتاج الحقّ إلى تصفيق؟ ═══════════
S.append(section('المحطة ٢: هل يحتاج الحقّ إلى تصفيق؟', 'الآيتان ١٠٥ و ١٠٧'))
S.append(slide(f'''{HDR('q')}
{SCEN('موقف', 'نشر شخصٌ على وسائل التواصل أنه «لا يؤمن بالقرآن»، وحصد آلاف الإعجابات.')}
{BIGQ('هل يُنقص ذلك من القرآن شيئاً؟', '', 2)}''' + tn('موقفٌ من إعداد العرض يقرّب معنى ﴿قُلْ ءَامِنُوا۟ بِهِۦٓ أَوْ لَا تُؤْمِنُوٓا۟﴾.')))
S.append(slide(f'''{HDR('d', 'كتاب الطالب ص ٥٦ – ٥٧')}
<div class="ayahbox st">{AY('وَبِٱلْحَقِّ أَنزَلْنَـٰهُ وَبِٱلْحَقِّ نَزَلَ ۗ وَمَآ أَرْسَلْنَـٰكَ إِلَّا مُبَشِّرًا وَنَذِيرًا', 'الإسراء: ١٠٥')}</div>
<div class="ayahbox st">{AY('قُلْ ءَامِنُوا۟ بِهِۦٓ أَوْ لَا تُؤْمِنُوٓا۟', 'الإسراء: ١٠٧')}</div>
<div class="ans3">{st('<div><b>نزل بالحقّ</b><span>وتكفّل الله بحفظه من التحريف</span></div>')}{st('<div><b>الرسول ﷺ</b><span>مبشّرٌ ونذير، وما عليه إلا البلاغ</span></div>')}{st('<div><b>أسلوب تحقير</b><span>إيمانهم لا يزيده كمالاً، وتكذيبهم لا يُنقصه</span></div>')}</div>''' + tn('الكتاب ص٥٦–٥٧، وإجابات الدليل ص٨٩–٩٠ (س١ و٤ و٦).')))
S.append(slide(f'''{HDR('l', 'دليل المعلم ص ٩٤')}<h2>نقاش: علاقتي بالقرآن</h2>
<div class="disc">{st('<div>هل يمكن أن نستغني عن القرآن الكريم؟</div>')}{st('<div>ما تأثير القرآن الكريم في حياتك؟</div>')}{st('<div>بمَ تنصح زميلاً لا يقرأ القرآن إلا في رمضان؟</div>')}</div>''' + tn('أسئلة المخرج السادس من الدليل ص٩٤ (يستشعر عظمة القرآن الكريم).')))

# ═══════════ المحطة ٣: دموع العلماء ═══════════
S.append(section('المحطة ٣: لماذا بكى العلماء؟', 'الآيات ١٠٧ – ١٠٩'))
S.append(slide(f'''{HDR('q')}
{BIGQ('ما الذي يجعل عالِماً كبيراً يسجد ويبكي حين يسمع آياتٍ من القرآن؟')}''' + tn('دقيقتان. وجّه الطلبة إلى أن العلم الحقيقي يقود إلى الخشوع.')))
S.append(slide(f'''{HDR('d', 'كتاب الطالب ص ٥٧')}
<div class="ayahbox st">{AY('إِنَّ ٱلَّذِينَ أُوتُوا۟ ٱلْعِلْمَ مِن قَبْلِهِۦٓ إِذَا يُتْلَىٰ عَلَيْهِمْ يَخِرُّونَ لِلْأَذْقَانِ سُجَّدًا', 'الإسراء: ١٠٧')}</div>
<div class="chain">{st('<div><i>١</i><b>سمعوا</b><span>عرفوا نعت النبيّ ﷺ في كتبهم</span></div>')}{st('<div><i>٢</i><b>خرّوا سُجّداً</b><span>انقادوا لما سمعوا</span></div>')}{st('<div><i>٣</i><b>سبحان ربّنا</b><span>تنزيهٌ وتصديقٌ بالوعد</span></div>')}{st('<div><i>٤</i><b>بكوا خشوعاً</b><span>تأثّراً بمواعظه</span></div>')}</div>''' + tn('الكتاب ص٥٧. ومنه النجاشي حين سمع القرآن: «إنّ هذا والذي جاء به موسى ليخرج من مشكاةٍ واحدة» (أحمد، المسند، ١٧٤٠). إجابة «ثالثاً» في الدليل ص٩٥: تكرار ﴿يَخِرُّونَ﴾ دلالةٌ على المبالغة في الخضوع والخشوع.')))
S.append(slide(f'''{HDR('l', 'أتأمّل وأستخرج ص ٥٨')}<h2>ثلاث قيم… أين تجدها في الآيات؟</h2>
{FLIPS([('تشريف الله تعالى لأهل العلم', AY('إِنَّ ٱلَّذِينَ أُوتُوا۟ ٱلْعِلْمَ مِن قَبْلِهِۦٓ')), ('مشروعيّة التسبيح في سجود التلاوة', AY('وَيَقُولُونَ سُبْحَـٰنَ رَبِّنَآ')), ('الوسطيّة والاعتدال في الإسلام', AY('وَٱبْتَغِ بَيْنَ ذَٰلِكَ سَبِيلًا'))], 'flex:1;min-width:26vw')}''' + tn('إجابة النشاط من الدليل ص٩٢. المخرج الرابع: يطبّق الطلبة القيم في واقعهم.')))

# ═══════════ المحطة ٤: صوتك في الصلاة ═══════════
S.append(section('المحطة ٤: كيف يكون صوتك في الصلاة؟', 'الآية ١١٠'))
S.append(slide(f'''{HDR('q')}
<div class="two2">{SCEN('أحمد', 'يرفع صوته في صلاته بالمسجد حتى يشوّش على من حوله.')}{SCEN('سالم', 'يقرأ في صلاته الجهرية بصوتٍ لا يسمعه حتى من خلفه.')}</div>
{BIGQ('أيّهما على صواب؟', '', 2)}''' + tn('موقفٌ من إعداد العرض. الجواب: لا هذا ولا ذاك، بل التوسّط.')))
S.append(slide(f'''{HDR('d', 'كتاب الطالب ص ٥٨')}
<div class="ayahbox st">{AY('وَلَا تَجْهَرْ بِصَلَاتِكَ وَلَا تُخَافِتْ بِهَا وَٱبْتَغِ بَيْنَ ذَٰلِكَ سَبِيلًا', 'الإسراء: ١١٠')}</div>
<div class="bookimg st">{FIG('sabab', 'bimg', 'سبب نزول الآية من كتاب الطالب')}</div>''' + tn('سبب النزول من الكتاب ص٥٨ (البخاري، ٤٧٢٢): فالتوسّط هو المنهج الربّاني.')))
S.append(slide(f'''{HDR('d', 'كتاب الطالب ص ٥٧')}<h2>﴿قُلِ ٱدْعُوا۟ ٱللَّهَ أَوِ ٱدْعُوا۟ ٱلرَّحْمَـٰنَ﴾</h2>
{FLIPS([('قال المشركون: يدعو واحداً وهو يدعو اثنين! فهل بين الدعاء باسم «الله» و«الرحمن» فرق؟', 'لا فرق', 'فلله الأسماء الحسنى، وتعدّد الأسماء لا يعني تعدّد المسمّى')], 'flex:1;min-width:64vw')}''' + tn('الكتاب ص٥٧، وإجابة الدليل ص٩٠ (س٧).')))

# ═══════════ المحطة ٥: أوّل كلمات الطفل ═══════════
S.append(section('المحطة ٥: أوّل ما يتعلّمه الطفل', 'الآية ١١١'))
S.append(slide(f'''{HDR('q', 'كتاب الطالب ص ٦١')}
{BIGQ('كان النبيّ ﷺ إذا أفصح الغلام علّمه آيةً واحدة… لماذا اختار هذه الآية بالذات؟', 'أفصح: تكلّم')}''' + tn('من إضاءة الكتاب ص٦١. لا تكشف الآية قبل النقاش.')))
S.append(slide(f'''{HDR('d', 'كتاب الطالب ص ٥٧ – ٥٨')}
<div class="ayahbox st">{AY('وَقُلِ ٱلْحَمْدُ لِلَّهِ ٱلَّذِى لَمْ يَتَّخِذْ وَلَدًا وَلَمْ يَكُن لَّهُۥ شَرِيكٌ فِى ٱلْمُلْكِ وَلَمْ يَكُن لَّهُۥ وَلِىٌّ مِّنَ ٱلذُّلِّ ۖ وَكَبِّرْهُ تَكْبِيرًۢا', 'الإسراء: ١١١')}</div>
<div class="ans3">{st('<div><b>لا ولد</b><span>الخلق كلّهم عنده سواء</span></div>')}{st('<div><b>لا شريك</b><span>الشريك للعاجز المحتاج</span></div>')}{st('<div><b>لا وليّ من الذلّ</b><span>لا يحتاج حليفاً لنصرته</span></div>')}</div>
<p class="lead st">فالتكبير أبلغ لفظةٍ عند العرب في معنى التعظيم والإجلال</p>''' + tn('الكتاب ص٥٧–٥٨ وإضاءة ص٦١: تُغرس العقيدة الصحيحة في الطفل من أول كلماته.')))

# ═══════════ تحدّي الفرق ═══════════
S.append(section('تحدّي الفرق', 'أقيّم تعلّمي · كتاب الطالب ص ٦٠ – ٦١'))
SCORE = '<div class="score" onclick="event.stopPropagation()">' + ''.join(f'<div><b>{t}</b><button onclick="var n=this.nextElementSibling;n.textContent=Math.max(0,(+n.dataset.v||0)-1);n.dataset.v=n.textContent">−</button><i data-v="0">0</i><button onclick="var n=this.previousElementSibling;n.dataset.v=(+n.dataset.v||0)+1;n.textContent=n.dataset.v">+</button></div>' for t in ('الفريق الأوّل', 'الفريق الثاني')) + '</div>'
S.append(slide(f'''{HDR('c', 'أقيّم تعلّمي (أولاً) ص ٦٠')}{SCORE}
{OPT([('أقرب ما يكون العبد من ربّه', 2, '﴿سُجَّدًا﴾'), ('تنزيه الله تعالى عمّا لا يليق به', 3, '﴿سُبْحَـٰنَ رَبِّنَآ﴾')], ('كَبِّرْهُ', 'يَبْكُونَ', 'سُجَّدًا', 'سُبْحَانَ رَبِّنَا'))}''' + tn('قسّم الصف فريقين؛ يجيب الفريق صاحب الدور ويضغط المعلم + للنقطة. لكل شريحة لوحتها، فانقل المجموع على السبورة. الإجابات من الدليل ص٩٥.')))
S.append(slide(f'''{HDR('c', 'أقيّم تعلّمي (ثانياً) ص ٦٠')}{SCORE}
{OPT([(AY('كِتَـٰبٌ أُحْكِمَتْ ءَايَـٰتُهُۥ ثُمَّ فُصِّلَتْ مِن لَّدُنْ حَكِيمٍ خَبِيرٍ', 'هود: ١'), 2), (AY('يَسْـَٔلُونَكَ عَنِ ٱلسَّاعَةِ أَيَّانَ مُرْسَىٰهَا', 'الأعراف: ١٨٧'), 4), (AY('هُوَ ٱلَّذِى بَعَثَ فِى ٱلْأُمِّيِّـۧنَ رَسُولًا مِّنْهُمْ', 'الجمعة: ٢'), 1), (AY('كَذَٰلِكَ لِنُثَبِّتَ بِهِۦ فُؤَادَكَ', 'الفرقان: ٣٢'), 0)], ('التثبيت', 'التيسير', 'الدلالة', 'التدرّج', 'التحدّي'))}''' + tn('إجابات الدليل ص٩٥: الدلالة، التحدّي، التيسير، التثبيت.')))
S.append(slide(f'''{HDR('c', 'أقيّم تعلّمي (رابعاً) ص ٦١')}<h2>كيف يستفيد المربّي من التدرّج؟</h2>
<div class="bookimg sm st">{FIG('murabbi', 'bimg', 'رسمان من الكتاب: أبٌ يعلّم ابنه القرآن، وفتاةٌ تتدرّب على الصلاة')}</div>
{FLIPS([('تعليم القرآن وحفظه', 'بطريقةٍ ميسّرة مستمرّة بلا تعنيف، ويبدأ بقصار السور'), ('تدريب الناشئة على الصلاة', 'بالقدوة والترغيب، ثم التعليم تدريجياً حتى العاشرة')], 'flex:1;min-width:36vw')}''' + tn('إجابة الدليل ص٩٥ (رابعاً)، مختصرة.')))

# ═══════════ الخروج ═══════════
S.append(slide(f'''<span class="qbadge">بطاقة الخروج 🎫</span><h2>٣ – ٢ – ١</h2>
<div class="disc">{st('<div><b>٣</b> أشياء تعلّمتها اليوم</div>')}{st('<div><b>٢</b> قيمتان سأطبّقهما في حياتي</div>')}{st('<div><b>١</b> سؤالٌ ما زال في ذهني</div>')}</div>''' + tn('يكتبها الطالب على ورقة صغيرة قبل الخروج، وتقرؤها لتعرف ما يحتاج إلى مراجعة.')))
S.append(slide('''<span class="qbadge" style="background:#0A6770;box-shadow:0 4px 0 #05393E">الواجب 🏠</span><h2>أقيّم تعلّمي (خامساً)</h2>
<p class="lead">ارجع إلى المصحف، واتلُ الآيات (٩٠–٩٣) من سورة الإسراء التي فيها خوارق ماديّة طلبها المشركون من الرسول ﷺ حتى يؤمنوا</p>''' + tn('«أقيّم تعلّمي» خامساً ص٦١، والآيات في الدليل ص٩٦.')))

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
