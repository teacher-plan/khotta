# مقاطع «شورتس» عمودية (1080×1920، أقل من دقيقة): كل مقطع خطأٌ شائع من منهج الصف السابع — VIDEO.md القسم ٩.
# الصوت: ElevenLabs (eleven_v4، صوت «Senen» فصحى) — مقطع صوتي لكل مشهد في صوت_شورت_<n>/NN.mp3.
#   python3 shorts.py narr          ← shorts_narration.json (نصوص المشاهد مع وسوم المشاعر لتوليد الصوت)
#   python3 shorts.py html <n>      ← شورت_<n>.html (يقرأ مدد الصوت)، ثم: VW=720 VH=1280 node ../video.mjs شورت_<n>.html صوت_شورت_<n> خرج.mp4
import os, sys, json, re, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
AR = str.maketrans('0123456789', '٠١٢٣٤٥٦٧٨٩')
def ar(n): return str(n).translate(AR)
X = '<span class="x">×</span>'; PL = '<span class="x">+</span>'; MI = '<span class="x">−</span>'; EQ = '<span class="x">=</span>'
def e(*p): return ' '.join(p)
def P(b, x): return f'<span class="b">{ar(b)}<sup>{ar(x)}</sup></span>'
def ng(v): return f'<span class="ngv"><i>−</i>{ar(v)}</span>'
def bn(v): return f'<span class="brv">({ng(v)})</span>'
def FR(n, d): return (f'<span class="fr"><span class="fn">{ar(n)}</span><span>{ar(d)}</span></span>')
def K(t): return f'<b class="k">{t}</b>'
# عنصر يظهر عند نسبةٍ من مدّة المشهد: (النسبة، HTML، الصنف: m رياضيات | bad | ok | rule | txt | big)
CTA_TAIL = 'اكْتُبْ إِجَابَتَكَ فِي التَّعْلِيقَاتِ، وَاضْغَطْ زِرَّ الْإِعْجَابِ، وَاشْتَرِكْ فِي الْقَنَاةِ لِتَصِلَكَ الْمَقَاطِعُ الْقَادِمَةُ!'
def CTA(q_spoken, q_html):
    return (f'[excited] وَالْآنَ تَحَدٍّ لَكَ: {q_spoken} [pause] {CTA_TAIL}',
            [(0, '🎯 تحدٍّ لك', 'tag'), (.04, q_html, 'm'), (.42, '💬 اكتب إجابتك في التعليقات', 'txt'),
             (.6, '👍 إعجاب', 'pill'), (.7, '🔔 اشترك في القناة', 'pill')])
SHORTS = [
 ('خطأ شائع في القوى', 'الوحدة ١ · القوى والجذور', [
  ('[curious] سُؤَالٌ سَرِيعٌ: كَمْ تُسَاوِي أَرْبَعَةٌ تَرْبِيع؟ إِذَا قُلْتَ ثَمَانِيَةً... [pause] فَقَدْ وَقَعْتَ فِي أَشْهَرِ خَطَأٍ فِي الْقُوَى!',
   [(0, '❓ كم تساوي؟', 'tag'), (.05, P(4, 2), 'big'), (.5, e(P(4, 2), EQ, '٨', '✘'), 'bad')]),
  ('[serious] الْأُسُّ لَيْسَ عَدَدًا نَضْرِبُ فِيهِ. الْأُسُّ يُخْبِرُنَا: كَمْ مَرَّةً نَكْتُبُ الْأَسَاسَ، وَنَضْرِبُهُ فِي نَفْسِهِ.',
   [(0, 'لماذا خطأ؟', 'tag'), (.05, e(P(4, 2), '≠', '٤', X, '٢'), 'bad'), (.45, 'الأُسّ = عدد مرّات تكرار الأساس', 'txt')]),
  ('[excited] إِذَنْ: أَرْبَعَةٌ تَرْبِيع، تَعْنِي أَرْبَعَةً فِي أَرْبَعَةٍ، وَالنَّاتِجُ: سِتَّةَ عَشَرَ! وَاثْنَانِ أُسُّ ثَلَاثَةٍ؟ اثْنَانِ فِي اثْنَيْنِ فِي اثْنَيْنِ: ثَمَانِيَةٌ، لَا سِتَّةٌ.',
   [(0, '✔ الصحيح', 'tag'), (.05, e(P(4, 2), EQ, '٤', X, '٤', EQ, K('١٦')), 'ok'), (.5, e(P(2, 3), EQ, '٢', X, '٢', X, '٢', EQ, K('٨')), 'ok')]),
  ('[warm] تَذَكَّرْ دَائِمًا: الْأُسُّ هُوَ عَدَدُ مَرَّاتِ الضَّرْبِ، وَلَيْسَ عَدَدًا نَضْرِبُ فِيهِ.',
   [(0, '📌 القاعدة', 'tag'), (.05, 'الأُسّ يخبرنا كم مرّة نضرب الأساس في نفسه', 'rule')]),
  CTA('كَمْ تُسَاوِي ثَلَاثَةٌ أُسُّ أَرْبَعَةٍ؟', e(P(3, 4), EQ, '؟'))]),
 ('خطأ شائع في ترتيب العمليات', 'الوحدة ١ · ترتيب العمليات', [
  ('[curious] احْسُبْ مَعِي: اثْنَانِ، زَائِدُ ثَلَاثَةٍ فِي أَرْبَعَةٍ. هَلْ قُلْتَ عِشْرِينَ؟ [pause] لِلْأَسَفِ... هَذَا خَطَأٌ شَائِعٌ جِدًّا!',
   [(0, '❓ احسب', 'tag'), (.05, e('٢', PL, '٣', X, '٤'), 'big'), (.55, e('٢', PL, '٣', X, '٤', EQ, '٢٠', '✘'), 'bad')]),
  ('[serious] الْخَطَأُ: أَنَّنَا جَمَعْنَا أَوَّلًا لِأَنَّ الْجَمْعَ جَاءَ أَوَّلًا. لَكِنَّ لِلْعَمَلِيَّاتِ تَرْتِيبًا، وَلَا نَحْسُبُهَا كَمَا نَقْرَأُ فَقَطْ.',
   [(0, 'لماذا خطأ؟', 'tag'), (.05, e('٥', X, '٤', EQ, '٢٠'), 'bad'), (.4, 'جمعنا أولاً لأنه جاء أولاً ✘', 'txt')]),
  ('[excited] الضَّرْبُ قَبْلَ الْجَمْعِ! ثَلَاثَةٌ فِي أَرْبَعَةٍ: اثْنَا عَشَرَ. ثُمَّ اثْنَانِ زَائِدُ اثْنَيْ عَشَرَ: أَرْبَعَةَ عَشَرَ!',
   [(0, '✔ الصحيح', 'tag'), (.1, e('٣', X, '٤', EQ, '١٢'), 'ok'), (.5, e('٢', PL, '١٢', EQ, K('١٤')), 'ok')]),
  ('[warm] الْقَاعِدَةُ: الْأَقْوَاسُ أَوَّلًا، ثُمَّ الْأُسُسُ، ثُمَّ الضَّرْبُ وَالْقِسْمَةُ، وَأَخِيرًا الْجَمْعُ وَالطَّرْحُ.',
   [(0, '📌 القاعدة', 'tag'), (.05, '١ الأقواس', 'step'), (.25, '٢ الأسس', 'step'), (.45, '٣ الضرب والقسمة', 'step'), (.7, '٤ الجمع والطرح', 'step')]),
  CTA('كَمْ تُسَاوِي عَشَرَةٌ، نَاقِصُ اثْنَيْنِ فِي ثَلَاثَةٍ؟', e('١٠', MI, '٢', X, '٣', EQ, '؟'))]),
 ('خطأ شائع في ضرب الأعداد السالبة', 'الوحدة ١ · الأعداد الصحيحة', [
  ('[curious] سَالِبُ ثَلَاثَةٍ، فِي سَالِبِ أَرْبَعَةٍ... كَمْ تُسَاوِي؟ كَثِيرٌ مِنَ الطُّلَّابِ يَقُولُونَ: سَالِبُ اثْنَيْ عَشَرَ! [pause] وَهَذَا خَطَأٌ.',
   [(0, '❓ كم تساوي؟', 'tag'), (.05, e(bn(3), X, bn(4)), 'big'), (.5, e(bn(3), X, bn(4), EQ, ng(12), '✘'), 'bad')]),
  ('[serious] السَّبَبُ: الْخَلْطُ بَيْنَ قَاعِدَةِ الْجَمْعِ وَقَاعِدَةِ الضَّرْبِ. فِي الْجَمْعِ: سَالِبٌ مَعَ سَالِبٍ يُعْطِي سَالِبًا، أَمَّا فِي الضَّرْبِ فَالْأَمْرُ مُخْتَلِفٌ.',
   [(0, 'لماذا خطأ؟', 'tag'), (.3, e(ng(3), PL, bn(4), EQ, ng(7)), 'm'), (.3, 'في الجمع ✔', 'txt'), (.7, 'لكن الضرب مختلف!', 'txt')]),
  ('[excited] فِي الضَّرْبِ: سَالِبٌ فِي سَالِبٍ يُعْطِي مُوجَبًا! إِذَنْ: سَالِبُ ثَلَاثَةٍ فِي سَالِبِ أَرْبَعَةٍ يُسَاوِي: مُوجَبَ اثْنَيْ عَشَرَ.',
   [(0, '✔ الصحيح', 'tag'), (.05, '(−) × (−) = (+)', 'ok'), (.45, e(bn(3), X, bn(4), EQ, K('+١٢')), 'ok')]),
  ('[warm] احْفَظْهَا: الْإِشَارَتَانِ الْمُتَشَابِهَتَانِ تُعْطِيَانِ مُوجَبًا، وَالْمُخْتَلِفَتَانِ تُعْطِيَانِ سَالِبًا. وَالْقِسْمَةُ مِثْلُ الضَّرْبِ تَمَامًا.',
   [(0, '📌 القاعدة', 'tag'), (.05, 'إشارتان متشابهتان ← موجب', 'step'), (.35, 'إشارتان مختلفتان ← سالب', 'step'), (.7, 'والقسمة مثل الضرب', 'txt')]),
  CTA('كَمْ تُسَاوِي سَالِبُ خَمْسَةٍ، فِي سَالِبِ اثْنَيْنِ؟', e(bn(5), X, bn(2), EQ, '؟'))]),
 ('خطأ شائع في جمع الكسور', 'الوحدة ٦ · جمع الكسور', [
  ('[curious] نِصْفٌ زَائِدُ ثُلُثٍ... هَلْ يُسَاوِي اثْنَيْنِ مِنْ خَمْسَةٍ؟ [pause] إِذَا جَمَعْتَ الْبَسْطَيْنِ وَالْمَقَامَيْنِ، فَقَدْ وَقَعْتَ فِي الْفَخِّ!',
   [(0, '❓ هل هذا صحيح؟', 'tag'), (.05, e(FR(1, 2), PL, FR(1, 3)), 'big'), (.3, e(FR(1, 2), PL, FR(1, 3), EQ, FR(2, 5), '✘'), 'bad')]),
  ('[serious] فَكِّرْ قَلِيلًا: النِّصْفُ وَحْدَهُ أَكْبَرُ مِنِ اثْنَيْنِ مِنْ خَمْسَةٍ! فَكَيْفَ يَصْغُرُ الْمَجْمُوعُ بَعْدَ أَنْ أَضَفْنَا إِلَيْهِ؟',
   [(0, 'لماذا خطأ؟', 'tag'), (.1, e(FR(1, 2), '>', FR(2, 5)), 'm'), (.5, 'المجموع لا يصغر بالإضافة! 🤔', 'txt')]),
  ('[excited] الصَّحِيحُ: نُوَحِّدُ الْمَقَامَاتِ أَوَّلًا. النِّصْفُ يُسَاوِي ثَلَاثَةَ أَسْدَاسٍ، وَالثُّلُثُ يُسَاوِي سُدُسَيْنِ. وَالْمَجْمُوعُ: خَمْسَةُ أَسْدَاسٍ!',
   [(0, '✔ الصحيح', 'tag'), (.2, e(FR(1, 2), EQ, FR(3, 6), '،', FR(1, 3), EQ, FR(2, 6)), 'ok'), (.7, e(FR(3, 6), PL, FR(2, 6), EQ, K(FR(5, 6))), 'ok')]),
  ('[warm] الْقَاعِدَةُ: نُوَحِّدُ الْمَقَامَاتِ أَوَّلًا، ثُمَّ نَجْمَعُ الْبُسُوطَ فَقَطْ، وَيَبْقَى الْمَقَامُ كَمَا هُوَ.',
   [(0, '📌 القاعدة', 'tag'), (.05, '١ نوحّد المقامات', 'step'), (.35, '٢ نجمع البسوط فقط', 'step'), (.65, '٣ المقام يبقى كما هو', 'step')]),
  CTA('كَمْ يُسَاوِي رُبْعٌ، زَائِدُ نِصْفٍ؟', e(FR(1, 4), PL, FR(1, 2), EQ, '؟'))]),
 ('خطأ شائع في النسبة المئوية', 'الوحدة ٨ · النسبة المئوية', [
  ('[curious] سِعْرُ لُعْبَةٍ مِئَةُ رِيَالٍ. زَادَ عِشْرِينَ فِي الْمِئَةِ، ثُمَّ نَقَصَ عِشْرِينَ فِي الْمِئَةِ. هَلْ رَجَعَ إِلَى مِئَةٍ؟ [pause] أَغْلَبُنَا يَقُولُ: نَعَمْ... وَهَذَا خَطَأٌ!',
   [(0, '❓ فكّر', 'tag'), (.05, '🧸 ١٠٠ ريال', 'big'), (.2, '⬆ زيادة ٢٠٪', 'step'), (.35, '⬇ ثم نقص ٢٠٪', 'step'), (.75, 'يرجع ١٠٠ ريال؟ ✘', 'bad')]),
  ('[serious] السِّرُّ: النِّسْبَةُ الْمِئَوِيَّةُ تُحْسَبُ دَائِمًا مِنَ الْقِيمَةِ الْحَالِيَّةِ، لَا مِنَ الْقِيمَةِ الْأُولَى.',
   [(0, 'لماذا خطأ؟', 'tag'), (.1, 'النسبة تُحسب من القيمة الحالية', 'rule')]),
  ('[excited] بَعْدَ الزِّيَادَةِ: مِئَةٌ وَعِشْرُونَ رِيَالًا. وَعِشْرُونَ فِي الْمِئَةِ مِنْهَا: أَرْبَعَةٌ وَعِشْرُونَ. إِذَنِ السِّعْرُ الْجَدِيدُ: سِتَّةٌ وَتِسْعُونَ رِيَالًا فَقَطْ!',
   [(0, '✔ الصحيح', 'tag'), (.05, e('١٠٠', PL, '٢٠', EQ, '١٢٠'), 'ok'), (.3, e('٢٠٪', 'من', '١٢٠', EQ, '٢٤'), 'ok'), (.6, e('١٢٠', MI, '٢٤', EQ, K('٩٦')), 'ok')]),
  ('[warm] تَذَكَّرْ: قَبْلَ أَنْ تَحْسُبَ أَيَّ نِسْبَةٍ، اسْأَلْ نَفْسَكَ: نِسْبَةٌ مِنْ مَاذَا؟',
   [(0, '📌 القاعدة', 'tag'), (.1, 'اسأل نفسك: نسبة من ماذا؟', 'rule')]),
  CTA('سِعْرٌ مِئَتَا رِيَالٍ، نَقَصَ عَشَرَةً فِي الْمِئَةِ، كَمْ يُصْبِحُ؟', e('٢٠٠', MI, '١٠٪', EQ, '؟'))]),
]
# الدفعة الثانية (٢٦ أكتوبر): بلا شريطٍ علويّ أو سفليّ، والعنوان مشهدٌ أول داخل الإطار.
def VR(t): return f'<span class="v">{t}</span>'
SHORTS += [
 ('خطأ شائع في الحدود المتشابهة', 'الوحدة ٢ · العبارات الجبرية', [
  ('[curious] ثَلَاثَةُ سٍ، زَائِدُ اثْنَيْنِ. هَلْ تُسَاوِي خَمْسَةَ سٍ؟ [pause] هَذَا أَشْهَرُ خَطَأٍ فِي الْجَبْرِ!',
   [(0, '❓ هل تساوي؟', 'tag'), (.06, e(VR('٣س'), PL, '٢'), 'big'), (.55, e(VR('٣س'), PL, '٢', EQ, VR('٥س'), '✘'), 'bad')]),
  ('[serious] لَا نَجْمَعُ إِلَّا الْحُدُودَ الْمُتَشَابِهَةَ. ثَلَاثَةُ سٍ فِيهَا مُتَغَيِّرٌ، وَالِاثْنَانِ عَدَدٌ ثَابِتٌ.',
   [(0, 'لماذا خطأ؟', 'tag'), (.1, e(VR('٣س'), '←', 'فيه متغيّر'), 'm'), (.5, e('٢', '←', 'عدد ثابت'), 'm')]),
  ('[excited] الصَّحِيحُ: تَبْقَى كَمَا هِيَ! أَمَّا ثَلَاثَةُ سٍ زَائِدُ أَرْبَعَةِ سٍ، فَتُسَاوِي سَبْعَةَ سٍ، لِأَنَّهُمَا مُتَشَابِهَانِ.',
   [(0, '✔ الصحيح', 'tag'), (.05, e(VR('٣س'), PL, '٢', EQ, K('٣س + ٢')), 'ok'), (.5, e(VR('٣س'), PL, VR('٤س'), EQ, K('٧س')), 'ok')]),
  ('[warm] الْقَاعِدَةُ: لَا نَجْمَعُ الْحُدُودَ إِلَّا إِذَا تَشَابَهَ الْمُتَغَيِّرُ.',
   [(0, '📌 القاعدة', 'tag'), (.08, 'نجمع الحدود المتشابهة فقط', 'rule')]),
  CTA('كَمْ يُسَاوِي خَمْسَةُ صٍ، نَاقِصُ صٍ؟', e(VR('٥ص'), MI, VR('ص'), EQ, '؟'))]),
 ('خطأ شائع في حلّ المعادلات', 'الوحدة ٢ · المعادلات', [
  ('[curious] س، زَائِدُ خَمْسَةٍ، يُسَاوِي اثْنَيْ عَشَرَ. هَلْ س تُسَاوِي سَبْعَةَ عَشَرَ؟ [pause] كَثِيرُونَ يَجْمَعُونَ هُنَا!',
   [(0, '❓ أوجد س', 'tag'), (.06, e(VR('س'), PL, '٥', EQ, '١٢'), 'big'), (.6, e(VR('س'), EQ, '١٧', '✘'), 'bad')]),
  ('[serious] الْخَمْسَةُ مَجْمُوعَةٌ إِلَى سٍ. وَلِنَعْزِلَ سًا، نَفْعَلُ عَكْسَ الْعَمَلِيَّةِ، لَا الْعَمَلِيَّةَ نَفْسَهَا.',
   [(0, 'لماذا خطأ؟', 'tag'), (.12, 'نفعل عكس العملية', 'rule')]),
  ('[excited] الْجَمْعُ عَكْسُهُ الطَّرْحُ! نَطْرَحُ خَمْسَةً مِنَ الطَّرَفَيْنِ: س تُسَاوِي سَبْعَةً. وَنَتَأَكَّدُ: سَبْعَةٌ زَائِدُ خَمْسَةٍ يُسَاوِي اثْنَيْ عَشَرَ.',
   [(0, '✔ الصحيح', 'tag'), (.05, e(VR('س'), PL, '٥', MI, '٥', EQ, '١٢', MI, '٥'), 'ok'), (.45, e(VR('س'), EQ, K('٧')), 'ok'), (.75, e('٧', PL, '٥', EQ, '١٢', '✔'), 'm')]),
  ('[warm] الْقَاعِدَةُ: مَا نَفْعَلُهُ بِطَرَفٍ نَفْعَلُهُ بِالطَّرَفِ الْآخَرِ، بِعَكْسِ الْعَمَلِيَّةِ.',
   [(0, '📌 القاعدة', 'tag'), (.05, 'الجمع ← نطرح', 'step'), (.4, 'الضرب ← نقسم', 'step')]),
  CTA('إِذَا كَانَ سٌ نَاقِصُ ثَلَاثَةٍ يُسَاوِي عَشَرَةً، فَكَمْ س؟', e(VR('س'), MI, '٣', EQ, '١٠'))]),
 ('خطأ شائع في ضرب الكسور', 'الوحدة ٦ · ضرب الكسور', [
  ('[curious] نِصْفٌ، فِي ثُلُثٍ. هَلْ نُوَحِّدُ الْمَقَامَاتِ أَوَّلًا؟ [pause] لَا! هُنَا يَخْلِطُ كَثِيرُونَ بَيْنَ الْجَمْعِ وَالضَّرْبِ.',
   [(0, '❓ ماذا نفعل؟', 'tag'), (.06, e(FR(1, 2), X, FR(1, 3)), 'big'), (.55, 'نوحّد المقامات؟ ✘', 'bad')]),
  ('[serious] تَوْحِيدُ الْمَقَامَاتِ لِلْجَمْعِ وَالطَّرْحِ فَقَطْ. أَمَّا الضَّرْبُ فَأَسْهَلُ بِكَثِيرٍ.',
   [(0, 'لماذا خطأ؟', 'tag'), (.1, 'التوحيد للجمع والطرح فقط', 'rule')]),
  ('[excited] فِي الضَّرْبِ: بَسْطٌ فِي بَسْطٍ، وَمَقَامٌ فِي مَقَامٍ. وَاحِدٌ فِي وَاحِدٍ: وَاحِدٌ. وَاثْنَانِ فِي ثَلَاثَةٍ: سِتَّةٌ. فَالنَّاتِجُ: سُدُسٌ.',
   [(0, '✔ الصحيح', 'tag'), (.05, 'بسط × بسط ، مقام × مقام', 'txt'), (.5, e(FR(1, 2), X, FR(1, 3), EQ, K(FR(1, 6))), 'ok')]),
  ('[warm] تَذَكَّرْ: الْجَمْعُ يَحْتَاجُ تَوْحِيدَ الْمَقَامَاتِ، وَالضَّرْبُ لَا يَحْتَاجُهُ أَبَدًا.',
   [(0, '📌 القاعدة', 'tag'), (.05, 'الجمع ← نوحّد المقامات', 'step'), (.45, 'الضرب ← نضرب مباشرة', 'step')]),
  CTA('كَمْ يُسَاوِي ثُلُثَانِ، فِي ثَلَاثَةِ أَرْبَاعٍ؟', e(FR(2, 3), X, FR(3, 4), EQ, '؟'))]),
 ('خطأ شائع في زوايا المثلث', 'الوحدة ٥ · الزوايا', [
  ('[curious] مُثَلَّثٌ فِيهِ زَاوِيَتَانِ: سَبْعُونَ، وَثَمَانُونَ دَرَجَةً. هَلِ الثَّالِثَةُ تُسَاوِي مِئَةً وَخَمْسِينَ؟ [pause] انْتَبِهْ!',
   [(0, '❓ الزاوية الثالثة', 'tag'), (.06, '٧٠° + ٨٠°', 'big'), (.55, 'الثالثة = ١٥٠° ✘', 'bad')]),
  ('[serious] جَمَعْنَا الزَّاوِيَتَيْنِ وَتَوَقَّفْنَا! لَكِنَّ مَجْمُوعَ زَوَايَا الْمُثَلَّثِ دَائِمًا مِئَةٌ وَثَمَانُونَ دَرَجَةً.',
   [(0, 'لماذا خطأ؟', 'tag'), (.12, 'مجموع زوايا المثلث = ١٨٠°', 'rule')]),
  ('[excited] إِذَنْ نَطْرَحُ! سَبْعُونَ زَائِدُ ثَمَانِينَ: مِئَةٌ وَخَمْسُونَ. وَمِئَةٌ وَثَمَانُونَ نَاقِصُ مِئَةٍ وَخَمْسِينَ: ثَلَاثُونَ دَرَجَةً.',
   [(0, '✔ الصحيح', 'tag'), (.05, '٧٠° + ٨٠° = ١٥٠°', 'ok'), (.5, e('١٨٠°', MI, '١٥٠°', EQ, K('٣٠°')), 'ok')]),
  ('[warm] الْقَاعِدَةُ: اجْمَعِ الْمَعْلُومَتَيْنِ، ثُمَّ اطْرَحْ مِنْ مِئَةٍ وَثَمَانِينَ.',
   [(0, '📌 القاعدة', 'tag'), (.05, '١ اجمع المعلومتين', 'step'), (.45, '٢ اطرح من ١٨٠°', 'step')]),
  CTA('مُثَلَّثٌ فِيهِ تِسْعُونَ وَأَرْبَعُونَ دَرَجَةً، فَكَمِ الثَّالِثَةُ؟', '٩٠° + ٤٠° + ؟')]),
 ('خطأ شائع بين المحيط والمساحة', 'الوحدة ٧ · المساحة', [
  ('[curious] مُسْتَطِيلٌ طُولُهُ ثَمَانِيَةٌ، وَعَرْضُهُ ثَلَاثَةٌ. كَمْ مِسَاحَتُهُ؟ إِذَا قُلْتَ اثْنَيْنِ وَعِشْرِينَ... [pause] فَقَدْ حَسَبْتَ الْمُحِيطَ!',
   [(0, '❓ المساحة', 'tag'), (.06, '٨ سم × ٣ سم', 'big'), (.6, 'المساحة = ٢٢ ✘', 'bad')]),
  ('[serious] الْمُحِيطُ سِيَاجٌ حَوْلَ الشَّكْلِ، وَالْمِسَاحَةُ بِلَاطٌ يَمْلَؤُهُ مِنَ الدَّاخِلِ.',
   [(0, 'الفرق', 'tag'), (.08, '🚧 المحيط ← سياج حول الشكل', 'txt'), (.5, '🟦 المساحة ← بلاط يملؤه', 'txt')]),
  ('[excited] الْمُحِيطُ: نَجْمَعُ الْأَضْلَاعَ، فَيُسَاوِي اثْنَيْنِ وَعِشْرِينَ سَنْتِيمِتْرًا. وَالْمِسَاحَةُ: نَضْرِبُ الطُّولَ فِي الْعَرْضِ: أَرْبَعَةٌ وَعِشْرُونَ سَنْتِيمِتْرًا مُرَبَّعًا!',
   [(0, '✔ الصحيح', 'tag'), (.05, 'المحيط = ٨+٣+٨+٣ = ٢٢ سم', 'ok'), (.5, e('المساحة', EQ, '٨', X, '٣', EQ, K('٢٤ سم²')), 'ok')]),
  ('[warm] عَلَامَةٌ لَا تُخْطِئُ: وَحْدَةُ الْمُحِيطِ سَنْتِيمِتْرٌ، وَالْمِسَاحَةِ سَنْتِيمِتْرٌ مُرَبَّعٌ.',
   [(0, '📌 علامة', 'tag'), (.05, 'المحيط ← سم', 'step'), (.45, 'المساحة ← سم²', 'step')]),
  CTA('مُرَبَّعٌ ضِلْعُهُ خَمْسَةُ سَنْتِيمِتْرَاتٍ، كَمْ مِسَاحَتُهُ؟', 'مربّع ضلعه ٥ سم')]),
]

CSS = '''
html,body{margin:0;width:720px;height:1280px;overflow:hidden;font-family:'Cairo','Readex Pro',sans-serif;color:#14305C;font-feature-settings:"ss01"}
body{background:#FBFCFE;background-image:linear-gradient(#E8EEF6 1px,transparent 1px),linear-gradient(90deg,#E8EEF6 1px,transparent 1px);background-size:36px 36px}
.top{position:absolute;top:0;left:0;right:0;height:210px;background:#14305C;color:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px}
.top .ch{font-size:22px;color:#F5C451;font-weight:700}.top h1{margin:0;font-size:44px;font-weight:700;line-height:1.25;text-align:center;padding:0 24px}
.top .ls{font-size:22px;color:#BFD0EA}
.mid{position:absolute;top:250px;bottom:190px;left:30px;right:30px}
.sc{position:absolute;inset:0;display:none;flex-direction:column;align-items:center;justify-content:center;gap:44px;text-align:center}
.el{opacity:0}
.m,.big,.bad,.ok{display:inline-flex;align-items:center;gap:.25em;direction:rtl;unicode-bidi:isolate;white-space:nowrap;font-family:'Cairo',sans-serif;font-weight:800}
.m{font-size:78px}.big{font-size:170px}
.bad,.ok{font-size:70px;padding:16px 30px;border-radius:26px;border:4px solid}
.bad{color:#B3261E;background:#FDE7E3;border-color:#B3261E}.ok{color:#1B7A3E;background:#E3F6EA;border-color:#1B7A3E}
.tag{font-size:40px;font-weight:800;background:#F5C451;color:#14305C;border-radius:40px;padding:8px 34px}
.txt{font-size:46px;font-weight:800;line-height:1.5}
.rule{font-size:46px;font-weight:800;line-height:1.6;color:#123A6B;background:#EEF4FD;border:3px solid #9BBBE8;border-inline-start:14px solid #1E5FB8;border-radius:22px;padding:24px 30px}
.step{font-size:46px;font-weight:800;background:#fff;border:3px solid #C9D6E8;border-radius:20px;padding:14px 30px;min-width:460px}
.pill{font-size:46px;font-weight:800;background:#C7361B;color:#fff;border-radius:50px;padding:14px 44px}
.x{color:#5A6F92;font-weight:700}.k{color:#C2410C}.v{color:#1E6FD9}
.b{color:#0A6770;display:inline-flex;align-items:flex-start;direction:rtl;unicode-bidi:isolate;font-weight:800;line-height:1}.b sup{color:#C7361B;font-size:.5em;line-height:1;position:relative;top:-.05em;margin-inline-start:.03em}
.ngv{display:inline-flex;direction:rtl;unicode-bidi:isolate}.ngv i{font-style:normal}.brv{display:inline-flex;gap:.12em;direction:rtl;unicode-bidi:isolate}
.fr{display:inline-flex;flex-direction:column;align-items:center;line-height:1.05;vertical-align:middle}.fn{border-bottom:.07em solid currentColor;padding:0 .15em .04em;align-self:stretch;text-align:center}
.bot{position:absolute;bottom:0;left:0;right:0;height:150px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:14px;font-size:24px;color:#3B5480;font-weight:700}
.bar{width:600px;height:10px;border-radius:5px;background:#DDE5EF;overflow:hidden}.bar i{display:block;height:100%;width:0;background:#C7361B}
'''
# نمط الدفعة الثانية: بلا شريطين، إطارٌ كامل، وعنوانٌ صغير أعلى كل مشهد (بلا اسم المعلّم).
CSS_BARE = '''
.mid{position:absolute;inset:150px 44px 120px}
.hd{position:absolute;top:56px;left:0;right:0;text-align:center;font-size:40px;font-weight:800;color:#14305C}
.hd b{background:linear-gradient(transparent 62%,#FFE08A 62%);padding:0 .12em}
.bar{position:absolute;bottom:46px;left:120px;right:120px;width:auto;height:12px;border-radius:6px}
'''
JS = '''
const T0 = DURS.reduce((a, d, i) => (a.push((a[i - 1] || 0) + (i ? DURS[i - 1] : 0)), a), []), TOT = DURS.reduce((a, b) => a + b, 0);
const fit = () => document.querySelectorAll('.sc').forEach(sc => { sc.style.display = 'flex'; sc.querySelectorAll('.el').forEach(el => { const w = Math.max(el.scrollWidth, el.getBoundingClientRect().width); if (w > 620) el.style.fontSize = (parseFloat(getComputedStyle(el).fontSize) * 640 / w) + 'px'; }); sc.style.display = 'none'; });
document.fonts.ready.then(fit);
window.seek = (i, t) => {
  document.querySelectorAll('.sc').forEach((s, k) => s.style.display = k === i ? 'flex' : 'none');
  document.querySelectorAll('.sc')[i].querySelectorAll('.el').forEach(el => {
    const d = (t - Number(el.dataset.f) * DURS[i]) / 450, p = Math.max(0, Math.min(1, d)), q = 1 - Math.pow(1 - p, 3);
    el.style.opacity = q; el.style.transform = `translateY(${(1 - q) * 40}px) scale(${.85 + .15 * q})`;
  });
  document.querySelector('.bar i').style.width = (100 * (T0[i] + t) / TOT) + '%';
};
'''

def narr():
    out = [[s[0] for s in sc] for _, _, sc in SHORTS]
    json.dump(out, open(os.path.join(HERE, 'shorts_narration.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    for i, s in enumerate(out, 1): print(i, sum(len(re.sub(r'\[[^\]]*\]', '', x)) for x in s), 'حرفاً')

def dur(p):
    import imageio_ffmpeg
    r = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-i', p], capture_output=True, text=True).stderr
    h, m_, s = re.search(r'Duration: (\d+):(\d+):([\d.]+)', r).groups(); return (int(h) * 3600 + int(m_) * 60 + float(s))

def html(n):
    title, lesson, sc = SHORTS[n - 1]
    bare = n >= 6   # الدفعة الثانية فصاعداً: بلا شريطين
    aud = os.path.join(HERE, f'صوت_شورت_{n}')
    mp3 = sorted(x for x in os.listdir(aud) if x.endswith('.mp3'))
    assert len(mp3) == len(sc), (len(mp3), len(sc))
    DURS = [round(dur(os.path.join(aud, x)) * 1000) + 500 for x in mp3]   # + نصف ثانية بين المشاهد
    body = ''.join('<div class="sc">' + ''.join(f'<div class="el {c}" data-f="{f}">{h}</div>' for f, h, c in els) + '</div>' for _, els in sc)
    page = f'''<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><title>{title}</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cairo:wght@600;700;800;900&amp;family=Readex+Pro:wght@400;600;700&amp;display=swap">
<style>{CSS}{CSS_BARE if bare else ''}</style></head><body>
{'' if bare else f'<div class="top"><span class="ch">أ. عيسى الحارثي · رياضيات الصف السابع</span><h1>⚠️ {title}</h1><span class="ls">{lesson}</span></div>'}
{f'<div class="hd">⚠️ <b>{title}</b></div>' if bare else ''}
<div class="mid">{body}</div>
{'<div class="bar"><i></i></div>' if bare else '<div class="bot"><div class="bar"><i></i></div><span>إعداد: أ. عيسى الحارثي</span></div>'}
<script>const DURS = window.DURS = {json.dumps(DURS)};{JS}seek(0, 0);</script></body></html>'''
    p = os.path.join(HERE, f'شورت_{n}.html'); open(p, 'w', encoding='utf-8').write(page); print(p, sum(DURS) / 1000, 'ث')

if __name__ == '__main__':
    if sys.argv[1] == 'narr': narr()
    else: html(int(sys.argv[2]))
