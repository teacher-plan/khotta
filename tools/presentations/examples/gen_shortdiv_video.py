# فيديو صفّي «القسمة المختصرة للأعداد العشرية» للدرسين ٣-٥ و٣-٦ (طلب الأستاذ عيسى، ٢٨ أكتوبر) — VIDEO.md القسم ١٠.
# مقدّمة ← ما القسمة المختصرة ← مثالان بلا باقٍ ← ٣ أسئلة بلا حلّ (وقفة) ← الحلول ← القسمة مع الباقي بحالاتها الستّ.
# الصوت ElevenLabs (صوت «Senen») مقطعاً لكل مشهد في صوت_shortdiv/NN.mp3؛ والخطوات تتبدّل في مكانها مع جملتها المنطوقة.
#   python3 gen_shortdiv_video.py narr   ← narration_shortdiv.json (النصوص مع وسوم المشاعر)
#   python3 gen_shortdiv_video.py        ← فيديو_shortdiv.html ، ثم: node ../video.mjs فيديو_shortdiv.html صوت_shortdiv خرج.mp4
import os, sys, json, re, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
_AR = '٠١٢٣٤٥٦٧٨٩'
def ar(s): return ''.join(_AR[int(c)] if c.isdigit() else ('٫' if c == '.' else c) for c in str(s))
DV = '<span class="x">÷</span>'; X = '<span class="x">×</span>'; EQ = '<span class="x">=</span>'; AP = '<span class="x">≈</span>'
def M(*p): return '<span class="m">' + ' '.join(p) + '</span>'

def vstep(a, k, s, added=(), hl=True, fs='100px', pt=None):
    # حالة القسمة المختصرة بعد معالجة s رقماً: الناتج فوق رقمه، والفاصلة فوق الفاصلة، والباقي صغيرٌ يسار الرقم التالي.
    # added: مواضع (في سلسلة a) الأصفار والفاصلة المضافة، وتظهر بالأزرق.
    k = int(k); i, hp, d = a.partition('.'); digs = list(i) + list(d); npos = len(i)
    r, qs, car, lead = 0, [], [''] * len(digs), True
    for j, ch in enumerate(digs):
        v = r * 10 + int(ch); q, r = divmod(v, k)
        hide = lead and q == 0 and j < npos - 1
        qs.append('' if hide else str(q)); lead = lead and hide
        if r and j + 1 < len(digs) and not hide: car[j + 1] = str(r)
    pos = lambda j: j if j < npos else j + 1      # موضع الرقم j في السلسلة a
    TD = 'padding: 0 .08em; text-align: center; min-width: .62em'
    def qcell(j):
        v = qs[j] if j < s else ''
        return f'<td style="{TD}; color: #0A7A3D">{ar(v)}</td>'
    def dcell(j):
        cur = hl and j == s - 1
        c = '#2563EB' if pos(j) in added else 'inherit'
        bg = '; background: #FFF1B8; border-radius: .12em' if cur else ''
        cr = car[j] if (car[j] and j <= s) else ''
        sup = f'<sup style="font-size: .55em; color: #C2410C; vertical-align: .6em">{ar(cr)}</sup>' if cr else ''
        return f'<td style="{TD}; border-top: .07em solid #14305C; color: {c}{bg}">{sup}{ar(digs[j])}</td>'
    qp = hp and (s > npos if pt is None else pt)   # فاصلة الناتج تظهر بعد تجاوز الآحاد، أو حين تُذكر (pt)
    q = [qcell(j) for j in range(npos)] + ([f'<td style="{TD}; color: #C0262D">{"٫" if qp else ""}</td>'] if hp else []) + [qcell(j) for j in range(npos, len(digs))]
    pc = '#2563EB' if npos in added else '#C0262D'
    dv = [dcell(j) for j in range(npos)] + ([f'<td style="{TD}; border-top: .07em solid #14305C; color: {pc}">٫</td>'] if hp else []) + [dcell(j) for j in range(npos, len(digs))]
    return (f'<table class="vd" style="font-size: {fs}"><tr><td></td>{"".join(q)}</tr>'
            f'<tr><td style="{TD}; border-right: .07em solid #14305C; padding-right: .2em">{ar(k)}</td>{"".join(dv)}</tr></table>')

def ST(anchor, a, k, s, note, added=(), slot='d', pt=None):
    # خطوةٌ تظهر مع عبارتها وتحلّ محلّ سابقتها في المكان نفسه
    return (anchor, f'<div class="pair">{vstep(a, k, s, added, pt=pt)}<div class="note">{note}</div></div>', 'step', slot)

def EX(title, prob, narr, steps, extra=()):
    return dict(title=title, sub=prob, narr=narr, items=[('', M(prob.replace('÷', DV)), 'prob', None)] + steps + list(extra))

S = [
 dict(title='قسمة الأعداد العشرية', sub='بالقسمة المختصرة', card=True,
  narr='[warm] أَهْلًا بِكُمْ يَا أَبْطَالَ الرِّيَاضِيَّاتِ! [curious] تَخَيَّلُوا أَبًا مَعَهُ سِتَّةُ رِيَالَاتٍ وَثَلَاثُمِئَةِ بَيْسَةٍ، يُرِيدُ أَنْ يُقَسِّمَهَا بِالتَّسَاوِي عَلَى أَبْنَائِهِ الثَّلَاثَةِ. كَمْ يَأْخُذُ كُلُّ ابْنٍ؟ [pause] لِنَعْرِفَ الْجَوَابَ، نَتَعَلَّمُ الْيَوْمَ: قِسْمَةَ الْأَعْدَادِ الْعَشْرِيَّةِ، بِطَرِيقَةِ الْقِسْمَةِ الْمُخْتَصَرَةِ.',
  items=[('تَخَيَّلُوا', '💰 ٦٫٣٠٠ ريالات', 'big', None), ('أَبْنَائِهِ', '👦 👦 👦', 'emo', None), ('كَمْ يَأْخُذُ', M('٦٫٣٠٠', DV, '٣', EQ, '؟'), 'prob', None),
         ('بِطَرِيقَةِ', 'الدرسان ٣-٥ و٣-٦', 'chip', None)]),
 dict(title='ما القسمة المختصرة؟', sub='للقسمة على عددٍ من رقمٍ واحد',
  narr='[serious] مَا الْقِسْمَةُ الْمُخْتَصَرَةُ؟ هِيَ طَرِيقَةٌ نَقْسِمُ بِهَا عَلَى عَدَدٍ مِنْ رَقْمٍ وَاحِدٍ، دُونَ أَنْ نَكْتُبَ خُطُوَاتِ الطَّرْحِ الطَّوِيلَةَ. نَكْتُبُ الْمَقْسُومَ تَحْتَ الْخَطِّ، وَالْمَقْسُومَ عَلَيْهِ عَلَى يَسَارِهِ، ثُمَّ نَكْتُبُ النَّاتِجَ فَوْقَ الْخَطِّ: كُلُّ رَقْمٍ فَوْقَ الرَّقْمِ الَّذِي قَسَمْنَاهُ. وَإِذَا بَقِيَ بَاقٍ، نَكْتُبُهُ صَغِيرًا يَسَارَ الرَّقْمِ التَّالِي.',
  items=[('نَكْتُبُ الْمَقْسُومَ', 'FIG', 'fig', None),
         ('نَكْتُبُ الْمَقْسُومَ', '⬇ المقسوم: تحت الخط', 'lab', None), ('وَالْمَقْسُومَ عَلَيْهِ', '⬅ المقسوم عليه: على يساره', 'lab', None),
         ('ثُمَّ نَكْتُبُ النَّاتِجَ', '⬆ الناتج: فوق الخط، كل رقمٍ فوق رقمه', 'lab', None), ('وَإِذَا بَقِيَ', '✏️ الباقي: صغيراً يسار الرقم التالي', 'lab', None)]),
 EX('نجرّب على عددٍ كامل', '٧٤ ÷ ٢',
  '[excited] لِنُجَرِّبْ مَعًا عَلَى عَدَدٍ كَامِلٍ: أَرْبَعَةٌ وَسَبْعُونَ، عَلَى اثْنَيْنِ. نَبْدَأُ دَائِمًا مِنَ الْيَسَارِ، أَيْ مِنْ أَكْبَرِ مَنْزِلَةٍ. سَبْعَةٌ عَلَى اثْنَيْنِ: ثَلَاثَةٌ، وَالْبَاقِي وَاحِدٌ. نَكْتُبُ الثَّلَاثَةَ فَوْقَ السَّبْعَةِ، وَنَكْتُبُ الْوَاحِدَ صَغِيرًا يَسَارَ الْأَرْبَعَةِ، فَتَصِيرُ أَرْبَعَةَ عَشَرَ. أَرْبَعَةَ عَشَرَ عَلَى اثْنَيْنِ: سَبْعَةٌ. إِذَنِ النَّاتِجُ: سَبْعَةٌ وَثَلَاثُونَ.',
  [ST('', '74', 2, 0, 'نبدأ من اليسار'), ST('سَبْعَةٌ عَلَى اثْنَيْنِ', '74', 2, 1, M('٧', DV, '٢', EQ, '٣') + '<br>والباقي ١'),
   ST('أَرْبَعَةَ عَشَرَ عَلَى', '74', 2, 2, M('١٤', DV, '٢', EQ, '٧')), ('إِذَنِ النَّاتِجُ', f'<div class="pair">{vstep("74", 2, 2, hl=False)}<div class="note ok">الناتج {M("٣٧")}</div></div>', 'step', 'd')]),
 dict(title='القاعدة', sub='لقسمة عددٍ عشري على عددٍ من رقمٍ واحد',
  narr='[warm] وَالْآنَ إِلَى الْأَعْدَادِ الْعَشْرِيَّةِ. وَالْخَبَرُ الْجَمِيلُ: الطَّرِيقَةُ نَفْسُهَا تَمَامًا! نَقْسِمُ قِسْمَةً مُخْتَصَرَةً كَمَا نَقْسِمُ الْأَعْدَادَ الْكَامِلَةَ. وَالْقَاعِدَةُ الذَّهَبِيَّةُ: الْفَاصِلَةُ فِي النَّاتِجِ، نَكْتُبُهَا فَوْقَ الْفَاصِلَةِ فِي الْمَقْسُومِ تَمَامًا.',
  items=[('نَقْسِمُ قِسْمَةً', '١ نقسم كما نقسم الأعداد الكاملة', 'rule', None), ('وَالْقَاعِدَةُ الذَّهَبِيَّةُ', '٢ الفاصلة في الناتج فوق الفاصلة في المقسوم', 'rule gold', None)]),
]
def DONE(a, k, txt, anchor, added=()):
    return (anchor, f'<div class="pair">{vstep(a, k, 99, added, hl=False)}<div class="note ok">{txt}</div></div>', 'step', 'd')
S += [
 EX('مثال ١', '٤٫٨٦ ÷ ٢',
  '[excited] الْمِثَالُ الْأَوَّلُ: أَوْجِدْ نَاتِجَ أَرْبَعَةٍ فَاصِلَة سِتَّةٍ وَثَمَانِينَ، عَلَى اثْنَيْنِ. نَبْدَأُ مِنَ الْيَسَارِ: أَرْبَعَةٌ عَلَى اثْنَيْنِ: اثْنَانِ، نَكْتُبُهَا فَوْقَ الْأَرْبَعَةِ. وَصَلْنَا إِلَى الْفَاصِلَةِ، فَنَضَعُ الْفَاصِلَةَ فِي النَّاتِجِ فَوْقَهَا. ثَمَانِيَةٌ عَلَى اثْنَيْنِ: أَرْبَعَةٌ. سِتَّةٌ عَلَى اثْنَيْنِ: ثَلَاثَةٌ. النَّاتِجُ: اثْنَانِ فَاصِلَة ثَلَاثَةٍ وَأَرْبَعِينَ. وَنَتَحَقَّقُ بِالضَّرْبِ: اثْنَانِ فَاصِلَة ثَلَاثَةٍ وَأَرْبَعِينَ، فِي اثْنَيْنِ، يُسَاوِي أَرْبَعَةً فَاصِلَة سِتَّةٍ وَثَمَانِينَ. [excited] صَحِيحٌ!',
  [ST('', '4.86', 2, 0, 'نبدأ من اليسار'), ST('أَرْبَعَةٌ عَلَى اثْنَيْنِ', '4.86', 2, 1, M('٤', DV, '٢', EQ, '٢')),
   ('وَصَلْنَا إِلَى الْفَاصِلَةِ', f'<div class="pair">{vstep("4.86", 2, 1, hl=False, pt=True)}<div class="note gold">الفاصلة فوق الفاصلة</div></div>', 'step', 'd'),
   ST('ثَمَانِيَةٌ عَلَى اثْنَيْنِ', '4.86', 2, 2, M('٨', DV, '٢', EQ, '٤')), ST('سِتَّةٌ عَلَى اثْنَيْنِ', '4.86', 2, 3, M('٦', DV, '٢', EQ, '٣')),
   DONE('4.86', 2, 'الناتج ' + M('٢٫٤٣'), 'النَّاتِجُ: اثْنَانِ'),
   ('وَنَتَحَقَّقُ', M('٢٫٤٣', X, '٢', EQ, '٤٫٨٦', '✔'), 'check', None)]),
 EX('مثال ٢', '٦٫٣٠٠ ÷ ٣',
  '[curious] الْمِثَالُ الثَّانِي يُجِيبُ عَنْ سُؤَالِ الْبِدَايَةِ: سِتَّةُ رِيَالَاتٍ وَثَلَاثُمِئَةِ بَيْسَةٍ، نَكْتُبُهَا: سِتَّةٌ فَاصِلَة ثَلَاثِمِئَةٍ، وَنَقْسِمُهَا عَلَى ثَلَاثَةٍ. سِتَّةٌ عَلَى ثَلَاثَةٍ: اثْنَانِ، ثُمَّ الْفَاصِلَةُ فَوْقَ الْفَاصِلَةِ. ثَلَاثَةٌ عَلَى ثَلَاثَةٍ: وَاحِدٌ. صِفْرٌ عَلَى ثَلَاثَةٍ: صِفْرٌ، وَصِفْرٌ عَلَى ثَلَاثَةٍ: صِفْرٌ. [excited] إِذَنْ يَأْخُذُ كُلُّ ابْنٍ: رِيَالَيْنِ وَمِئَةَ بَيْسَةٍ!',
  [ST('', '6.300', 3, 0, 'نبدأ من اليسار'), ST('سِتَّةٌ عَلَى ثَلَاثَةٍ', '6.300', 3, 1, M('٦', DV, '٣', EQ, '٢') + '<br>والفاصلة فوق الفاصلة', pt=True),
   ST('ثَلَاثَةٌ عَلَى ثَلَاثَةٍ', '6.300', 3, 2, M('٣', DV, '٣', EQ, '١')), ST('صِفْرٌ عَلَى ثَلَاثَةٍ: صِفْرٌ، وَصِفْرٌ', '6.300', 3, 4, M('٠', DV, '٣', EQ, '٠')),
   DONE('6.300', 3, '👦 كل ابن: ٢٫١٠٠ ريال', 'إِذَنْ يَأْخُذُ')]),
 dict(title='⏸ دورك الآن', sub='أوقف الفيديو وحلّ في دفترك', hold=6,
  narr='[excited] حَانَ دَوْرُكُمْ! حُلُّوا هَذِهِ الْأَسْئِلَةَ الثَّلَاثَةَ بِالْقِسْمَةِ الْمُخْتَصَرَةِ: ثَمَانِيَةٌ فَاصِلَة سِتَّةٍ وَأَرْبَعِينَ، عَلَى اثْنَيْنِ. تِسْعَةٌ فَاصِلَة ثَلَاثَةٍ وَسِتِّينَ، عَلَى ثَلَاثَةٍ. ثَمَانِيَةٌ فَاصِلَة ثَمَانِيَةٍ وَأَرْبَعِينَ، عَلَى أَرْبَعَةٍ. [pause] أَوْقِفُوا الْفِيدْيُو الْآنَ، وَلَا تَنْسَوُا الْفَاصِلَةَ!',
  items=[('ثَمَانِيَةٌ فَاصِلَة سِتَّةٍ', 'س١: ' + M('٨٫٤٦', DV, '٢'), 'q', None), ('تِسْعَةٌ فَاصِلَة', 'س٢: ' + M('٩٫٦٣', DV, '٣'), 'q', None),
         ('ثَمَانِيَةٌ فَاصِلَة ثَمَانِيَةٍ', 'س٣: ' + M('٨٫٤٨', DV, '٤'), 'q', None), ('أَوْقِفُوا', '⏸ أوقف الفيديو الآن', 'pause', None)]),
 dict(title='الحلول', sub='تأكّد من إجاباتك',
  narr='[warm] هَلْ حَلَلْتُمْ؟ لِنَتَأَكَّدْ. السُّؤَالُ الْأَوَّلُ: أَرْبَعَةٌ فَاصِلَة ثَلَاثَةٍ وَعِشْرِينَ. السُّؤَالُ الثَّانِي: ثَلَاثَةٌ فَاصِلَة وَاحِدٍ وَعِشْرِينَ. السُّؤَالُ الثَّالِثُ: اثْنَانِ فَاصِلَة اثْنَيْ عَشَرَ. [excited] مَنْ أَجَابَ عَنِ الثَّلَاثَةِ صَحِيحَةً، فَهُوَ بَطَلٌ!',
  items=[('الْأَوَّلُ', f'<div class="sol">{vstep("8.46", 2, 9, hl=False, fs="60px")}</div>', 'solc', None),
         ('الثَّانِي', f'<div class="sol">{vstep("9.63", 3, 9, hl=False, fs="60px")}</div>', 'solc', None),
         ('الثَّالِثُ', f'<div class="sol">{vstep("8.48", 4, 9, hl=False, fs="60px")}</div>', 'solc', None), ('مَنْ أَجَابَ', '🏆 أحسنت!', 'chip', None)]),
 dict(title='القسمة مع الباقي', sub='خمس حالات نتعرّفها واحدةً واحدة',
  narr='[curious] وَالْآنَ إِلَى الْجُزْءِ الثَّانِي: مَاذَا نَفْعَلُ إِذَا لَمْ تَنْقَسِمِ الْأَرْقَامُ بِالضَّبْطِ، وَبَقِيَ بَاقٍ؟ سَنَتَعَرَّفُ خَمْسَ حَالَاتٍ، وَاحِدَةً تِلْوَ الْأُخْرَى.',
  items=[(f'@{.35 + .1 * n}', t, 'case', None) for n, t in enumerate(
   ['١ الباقي ينتقل إلى الرقم التالي', '٢ الرقم الأول أصغر ← صفر قبل الفاصلة',
    '٣ باقٍ بعد آخر رقم ← نضيف صفراً', '٤ عددٌ كامل وفيه باقٍ ← نضع الفاصلة', '٥ قسمةٌ لا تنتهي ← نقرّب'])]),
 EX('الحالة ١: الباقي ينتقل', '٧٫٣٥ ÷ ٥',
  '[serious] الْحَالَةُ الْأُولَى: الْبَاقِي يَنْتَقِلُ إِلَى الرَّقْمِ التَّالِي. مِثَالٌ: سَبْعَةٌ فَاصِلَة خَمْسَةٍ وَثَلَاثِينَ، عَلَى خَمْسَةٍ. سَبْعَةٌ عَلَى خَمْسَةٍ: وَاحِدٌ، وَالْبَاقِي اثْنَانِ. نَكْتُبُ الِاثْنَيْنِ صَغِيرًا يَسَارَ الثَّلَاثَةِ، فَتَصِيرُ ثَلَاثَةً وَعِشْرِينَ، وَالْفَاصِلَةُ فَوْقَ الْفَاصِلَةِ. ثَلَاثَةٌ وَعِشْرُونَ عَلَى خَمْسَةٍ: أَرْبَعَةٌ، وَالْبَاقِي ثَلَاثَةٌ، فَتَصِيرُ الْخَمْسَةُ خَمْسَةً وَثَلَاثِينَ. خَمْسَةٌ وَثَلَاثُونَ عَلَى خَمْسَةٍ: سَبْعَةٌ. النَّاتِجُ: وَاحِدٌ فَاصِلَة سَبْعَةٍ وَأَرْبَعِينَ.',
  [ST('', '7.35', 5, 0, 'نبدأ من اليسار'), ST('سَبْعَةٌ عَلَى خَمْسَةٍ', '7.35', 5, 1, M('٧', DV, '٥', EQ, '١') + '<br>والباقي ٢'),
   ST('ثَلَاثَةٌ وَعِشْرُونَ عَلَى', '7.35', 5, 2, M('٢٣', DV, '٥', EQ, '٤') + '<br>والباقي ٣'), ST('خَمْسَةٌ وَثَلَاثُونَ عَلَى', '7.35', 5, 3, M('٣٥', DV, '٥', EQ, '٧')),
   DONE('7.35', 5, 'الناتج ' + M('١٫٤٧'), 'النَّاتِجُ: وَاحِدٌ')]),
 EX('الحالة ٢: الرقم الأول أصغر', '٤٫٩ ÷ ٧',
  '[serious] الْحَالَةُ الثَّانِيَةُ: الرَّقْمُ الْأَوَّلُ أَصْغَرُ مِنَ الْمَقْسُومِ عَلَيْهِ. مِثَالٌ: أَرْبَعَةٌ فَاصِلَة تِسْعَةٍ، عَلَى سَبْعَةٍ. أَرْبَعَةٌ عَلَى سَبْعَةٍ؟ لَا تَنْقَسِمُ! نَكْتُبُ صِفْرًا فَوْقَ الْأَرْبَعَةِ، ثُمَّ الْفَاصِلَةَ، وَتَنْتَقِلُ الْأَرْبَعَةُ بَاقِيًا، فَتَصِيرُ التِّسْعَةُ تِسْعَةً وَأَرْبَعِينَ. تِسْعَةٌ وَأَرْبَعُونَ عَلَى سَبْعَةٍ: سَبْعَةٌ. النَّاتِجُ: صِفْرٌ فَاصِلَة سَبْعَةٍ.',
  [ST('', '4.9', 7, 0, 'نبدأ من اليسار'), ST('أَرْبَعَةٌ عَلَى سَبْعَةٍ', '4.9', 7, 0, M('٤', '&lt;', '٧') + '<br>لا تنقسم!'),
   ST('نَكْتُبُ صِفْرًا', '4.9', 7, 1, 'نكتب <b class="k">٠</b> ثم الفاصلة<br>والباقي ٤', pt=True), ST('تِسْعَةٌ وَأَرْبَعُونَ عَلَى', '4.9', 7, 2, M('٤٩', DV, '٧', EQ, '٧')),
   DONE('4.9', 7, 'الناتج ' + M('٠٫٧'), 'النَّاتِجُ: صِفْرٌ')]),
 EX('الحالة ٣: باقٍ بعد آخر رقم', '٩٫٣ ÷ ٦',
  '[serious] الْحَالَةُ الثَّالِثَةُ: بَقِيَ بَاقٍ بَعْدَ آخِرِ رَقْمٍ. مِثَالٌ: تِسْعَةٌ فَاصِلَة ثَلَاثَةٍ، عَلَى سِتَّةٍ. تِسْعَةٌ عَلَى سِتَّةٍ: وَاحِدٌ، وَالْبَاقِي ثَلَاثَةٌ، ثُمَّ الْفَاصِلَةُ. ثَلَاثَةٌ وَثَلَاثُونَ عَلَى سِتَّةٍ: خَمْسَةٌ، وَالْبَاقِي ثَلَاثَةٌ. [curious] انْتَهَتِ الْأَرْقَامُ، وَمَا زَالَ مَعَنَا بَاقٍ! [excited] الْحَلُّ: نُضِيفُ صِفْرًا بَعْدَ آخِرِ رَقْمٍ عَشْرِيٍّ، فَالْأَصْفَارُ بَعْدَ آخِرِ رَقْمٍ عَشْرِيٍّ لَا تُغَيِّرُ قِيمَةَ الْعَدَدِ. ثَلَاثُونَ عَلَى سِتَّةٍ: خَمْسَةٌ. النَّاتِجُ: وَاحِدٌ فَاصِلَة خَمْسَةٍ وَخَمْسِينَ.',
  [ST('', '9.3', 6, 0, 'نبدأ من اليسار'), ST('تِسْعَةٌ عَلَى سِتَّةٍ', '9.3', 6, 1, M('٩', DV, '٦', EQ, '١') + '<br>والباقي ٣', pt=True),
   ST('ثَلَاثَةٌ وَثَلَاثُونَ عَلَى', '9.3', 6, 2, M('٣٣', DV, '٦', EQ, '٥') + '<br>والباقي ٣'),
   ('انْتَهَتِ الْأَرْقَامُ', f'<div class="pair">{vstep("9.3", 6, 2, hl=False)}<div class="note bad">الباقي ٣ ولا أرقام!</div></div>', 'step', 'd'),
   ST('نُضِيفُ صِفْرًا', '9.30', 6, 2, 'نضيف <b style="color: #2563EB">٠</b>', added=(3,)),
   ST('ثَلَاثُونَ عَلَى سِتَّةٍ', '9.30', 6, 3, M('٣٠', DV, '٦', EQ, '٥'), added=(3,)), DONE('9.30', 6, 'الناتج ' + M('١٫٥٥'), 'النَّاتِجُ: وَاحِدٌ', added=(3,))]),
 EX('الحالة ٤: عددٌ كامل وفيه باقٍ', '١٤ ÷ ٤',
  '[serious] الْحَالَةُ الرَّابِعَةُ: عَدَدٌ كَامِلٌ، وَفِي الْقِسْمَةِ بَاقٍ. مِثَالٌ: أَرْبَعَةَ عَشَرَ عَلَى أَرْبَعَةٍ. وَاحِدٌ عَلَى أَرْبَعَةٍ لَا يَنْقَسِمُ، فَنَأْخُذُ أَرْبَعَةَ عَشَرَ: ثَلَاثَةٌ، وَالْبَاقِي اثْنَانِ. [curious] لَا تُوجَدُ فَاصِلَةٌ! [excited] نَضَعُ فَاصِلَةً بَعْدَ الْعَدَدِ، وَنُضِيفُ صِفْرًا، وَنَضَعُ الْفَاصِلَةَ فِي النَّاتِجِ أَيْضًا. عِشْرُونَ عَلَى أَرْبَعَةٍ: خَمْسَةٌ. النَّاتِجُ: ثَلَاثَةٌ فَاصِلَة خَمْسَةٍ.',
  [ST('', '14', 4, 0, 'نبدأ من اليسار'), ST('وَاحِدٌ عَلَى أَرْبَعَةٍ', '14', 4, 1, M('١', '&lt;', '٤') + '<br>فنأخذ ١٤'),
   ST('فَنَأْخُذُ', '14', 4, 2, M('١٤', DV, '٤', EQ, '٣') + '<br>والباقي ٢'),
   ('لَا تُوجَدُ فَاصِلَةٌ', f'<div class="pair">{vstep("14", 4, 2, hl=False)}<div class="note bad">الباقي ٢ ولا فاصلة!</div></div>', 'step', 'd'),
   ST('نَضَعُ فَاصِلَةً', '14.0', 4, 2, 'نضع <b style="color: #2563EB">٫</b> ونضيف <b style="color: #2563EB">٠</b>', added=(2, 3), pt=True),
   ST('عِشْرُونَ عَلَى', '14.0', 4, 3, M('٢٠', DV, '٤', EQ, '٥'), added=(2, 3)), DONE('14.0', 4, 'الناتج ' + M('٣٫٥'), 'النَّاتِجُ: ثَلَاثَةٌ', added=(2, 3))]),
 EX('الحالة ٥: قسمةٌ لا تنتهي', '٦٨ ÷ ٧ لأقرب منزلة عشرية',
  '[serious] الْحَالَةُ الْخَامِسَةُ: قِسْمَةٌ لَا تَنْتَهِي. مِثَالٌ: ثَمَانِيَةٌ وَسِتُّونَ عَلَى سَبْعَةٍ، لِأَقْرَبِ مَنْزِلَةٍ عَشْرِيَّةٍ وَاحِدَةٍ. الْمَطْلُوبُ مَنْزِلَةٌ وَاحِدَةٌ، فَنَحْسُبُ مَنْزِلَتَيْنِ: نَكْتُبُ ثَمَانِيَةً وَسِتِّينَ فَاصِلَة صِفْر صِفْر. سِتَّةٌ عَلَى سَبْعَةٍ لَا تَنْقَسِمُ، فَنَأْخُذُ ثَمَانِيَةً وَسِتِّينَ عَلَى سَبْعَةٍ: تِسْعَةٌ، وَالْبَاقِي خَمْسَةٌ. خَمْسُونَ عَلَى سَبْعَةٍ: سَبْعَةٌ، وَالْبَاقِي وَاحِدٌ. عَشَرَةٌ عَلَى سَبْعَةٍ: وَاحِدٌ. [pause] النَّاتِجُ: تِسْعَةٌ فَاصِلَة وَاحِدٍ وَسَبْعِينَ، وَنُقَرِّبُهُ: تِسْعَةٌ فَاصِلَة سَبْعَةٍ تَقْرِيبًا، لِأَنَّ الرَّقْمَ الزَّائِدَ وَاحِدٌ، وَهُوَ أَصْغَرُ مِنْ خَمْسَةٍ.',
  [ST('', '68', 7, 0, 'المطلوب منزلة واحدة'), ST('نَكْتُبُ ثَمَانِيَةً', '68.00', 7, 0, 'نحسب <b>منزلتين</b>', added=(2, 3, 4)),
   ST('فَنَأْخُذُ', '68.00', 7, 2, M('٦٨', DV, '٧', EQ, '٩') + '<br>والباقي ٥', added=(2, 3, 4)),
   ST('خَمْسُونَ عَلَى', '68.00', 7, 3, M('٥٠', DV, '٧', EQ, '٧') + '<br>والباقي ١', added=(2, 3, 4)),
   ST('عَشَرَةٌ عَلَى', '68.00', 7, 4, M('١٠', DV, '٧', EQ, '١'), added=(2, 3, 4)),
   DONE('68.00', 7, M('٩٫٧١', AP, '٩٫٧'), 'وَنُقَرِّبُهُ', added=(2, 3, 4))]),
 dict(title='ملخّص الحالات', sub='وفي كل الحالات: الفاصلة فوق الفاصلة',
  narr='[warm] لِنُلَخِّصْ: الْبَاقِي يَنْتَقِلُ دَائِمًا إِلَى الرَّقْمِ التَّالِي. وَإِذَا كَانَ الرَّقْمُ الْأَوَّلُ أَصْغَرَ مِنَ الْمَقْسُومِ عَلَيْهِ، نَكْتُبُ صِفْرًا قَبْلَ الْفَاصِلَةِ. وَإِذَا بَقِيَ بَاقٍ فِي النِّهَايَةِ، نُضِيفُ أَصْفَارًا، وَنَضَعُ الْفَاصِلَةَ إِنْ لَمْ تَكُنْ مَوْجُودَةً. وَإِذَا لَمْ تَنْتَهِ الْقِسْمَةُ، نَحْسُبُ مَنْزِلَةً زَائِدَةً ثُمَّ نُقَرِّبُ. [excited] وَفِي كُلِّ الْحَالَاتِ: الْفَاصِلَةُ فَوْقَ الْفَاصِلَةِ!',
  items=[('الْبَاقِي يَنْتَقِلُ', '↪ الباقي ← يسار الرقم التالي', 'case', None), ('وَإِذَا كَانَ الرَّقْمُ', '٠ الرقم الأول أصغر ← صفر قبل الفاصلة', 'case', None),
         ('وَإِذَا بَقِيَ', '➕ باقٍ في النهاية ← نضيف أصفاراً (والفاصلة)', 'case', None), ('وَإِذَا لَمْ تَنْتَهِ', '≈ لا تنتهي ← منزلة زائدة ثم نقرّب', 'case', None),
         ('وَفِي كُلِّ', '⭐ الفاصلة فوق الفاصلة', 'rule gold', None)]),
 dict(title='أحسنتم!', sub='تدرّبوا في كتاب النشاط', card=True,
  narr='[excited] أَحْسَنْتُمْ! الْآنَ أَصْبَحْتُمْ تُتْقِنُونَ الْقِسْمَةَ الْمُخْتَصَرَةَ لِلْأَعْدَادِ الْعَشْرِيَّةِ بِكُلِّ حَالَاتِهَا. تَدَرَّبُوا عَلَيْهَا فِي كِتَابِ النَّشَاطِ، وَإِلَى اللِّقَاءِ فِي الدَّرْسِ الْقَادِمِ!',
  items=[('تَدَرَّبُوا', '📘 كتاب النشاط', 'chip', None)]),
]
FIG = f'<div class="fig">{vstep("84", 2, 9, hl=False, fs="88px")}</div>'

CSS = '''
html,body{margin:0;width:1280px;height:720px;overflow:hidden;font-family:'Cairo','Readex Pro',sans-serif;color:#14305C}
body{background:#FBFCFE;background-image:linear-gradient(#E8EEF6 1px,transparent 1px),linear-gradient(90deg,#E8EEF6 1px,transparent 1px);background-size:32px 32px}
.hdr{position:absolute;top:0;left:0;right:0;height:54px;display:flex;align-items:center;justify-content:space-between;padding:0 30px;background:#14305C;color:#fff;font-size:20px;font-weight:700}
.hdr b{color:#F5C451}
.ftr{position:absolute;bottom:12px;left:30px;right:30px;display:flex;align-items:center;gap:18px;font-size:16px;color:#3B5480;font-weight:700}
.bar{flex:1;height:8px;border-radius:4px;background:#DDE5EF;overflow:hidden}.bar i{display:block;height:100%;width:0;background:#C7361B}
.sc{position:absolute;top:64px;bottom:40px;left:40px;right:40px;display:none;flex-direction:column;align-items:center;justify-content:flex-start;gap:8px;text-align:center}
.sc.card{justify-content:center;gap:26px}
h2{margin:4px 0 0;font-size:42px;font-weight:800}.card h2{font-size:64px}
h2 b{background:linear-gradient(transparent 60%,#FFE08A 60%);padding:0 .15em}
.sub{font-size:22px;font-weight:700;color:#3B5480;margin-top:-4px}
.body{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:12px;width:100%}
.el{opacity:0}
.m{display:inline-flex;align-items:center;gap:.25em;direction:rtl;unicode-bidi:isolate;white-space:nowrap;font-weight:800}
.x{color:#5A6F92;font-weight:700}.k{color:#C2410C}
.prob{font-size:40px;background:#14305C;color:#fff;border-radius:18px;padding:4px 30px}.prob .x{color:#BFD0EA}
.big{font-size:54px;font-weight:800}.emo{font-size:54px}
.chip{font-size:26px;font-weight:800;background:#F5C451;border-radius:40px;padding:6px 30px}
.rule{font-size:34px;font-weight:800;line-height:1.5;color:#123A6B;background:#EEF4FD;border:3px solid #9BBBE8;border-inline-start:14px solid #1E5FB8;border-radius:20px;padding:14px 30px;min-width:820px}
.rule.gold{background:#FFF6D6;border-color:#E8C35A;border-inline-start-color:#D49A00}
.lab{font-size:24px;font-weight:800;background:#fff;border:3px solid #C9D6E8;border-radius:14px;padding:3px 22px;min-width:600px}
.fig{margin:4px 0}
.slot{display:grid;width:100%;justify-items:center;align-items:center}.slot>.el{grid-area:1/1}
.pair{display:flex;align-items:center;justify-content:center;gap:70px}
.vd{border-collapse:collapse;direction:ltr;unicode-bidi:isolate;font-weight:800;line-height:1.12}
.note{font-size:36px;font-weight:800;line-height:1.6;background:#fff;border:3px solid #C9D6E8;border-radius:20px;padding:12px 30px;min-width:360px}
.note.ok{background:#E3F6EA;border-color:#1B7A3E;color:#1B7A3E}.note.gold{background:#FFF6D6;border-color:#D49A00}
.note.bad{background:#FDE7E3;border-color:#B3261E;color:#B3261E}
.check{font-size:40px;color:#1B7A3E;background:#E3F6EA;border:3px solid #1B7A3E;border-radius:18px;padding:4px 26px}
.bad{font-size:40px;color:#B3261E;background:#FDE7E3;border:3px solid #B3261E;border-radius:18px;padding:4px 26px}
.q{font-size:46px;font-weight:800;background:#fff;border:3px solid #C9D6E8;border-radius:18px;padding:2px 40px;min-width:480px}
.pause{font-size:32px;font-weight:800;color:#fff;background:#C7361B;border-radius:40px;padding:8px 40px}
.solc{display:inline-flex}.sols{display:flex;gap:34px;justify-content:center;align-items:center}
.sol{background:#E3F6EA;border:3px solid #1B7A3E;border-radius:20px;padding:10px 30px}
.case{font-size:25px;font-weight:800;background:#fff;border:3px solid #C9D6E8;border-radius:14px;padding:3px 24px;min-width:720px;text-align:start}
'''
JS = '''
const T0 = DURS.reduce((a, d, i) => (a.push(i ? a[i - 1] + DURS[i - 1] : 0), a), []), TOT = DURS.reduce((a, b) => a + b, 0);
window.seek = (i, t) => {
  document.querySelectorAll('.sc').forEach((s, k) => s.style.display = k === i ? 'flex' : 'none');
  document.querySelectorAll('.sc')[i].querySelectorAll('.el').forEach(el => {
    const a = Number(el.dataset.t), u = Number(el.dataset.u || 1e9);
    const p = Math.max(0, Math.min(1, (t - a) / 350)), q = 1 - Math.pow(1 - p, 3), on = t < u;
    el.style.opacity = on ? q : 0; el.style.transform = `translateY(${(1 - q) * 24}px)`;
  });
  document.querySelector('.bar i').style.width = (100 * (T0[i] + t) / TOT) + '%';
};
'''
CLEAN = lambda s: re.sub(r'\s*\[[^\]]*\]\s*', ' ', s).strip()

def narr():
    out = [s['narr'] for s in S]
    json.dump(out, open(os.path.join(HERE, 'narration_shortdiv.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(len(out), 'مشهداً', sum(len(CLEAN(x)) for x in out), 'حرفاً')

def dur(p):
    import imageio_ffmpeg
    r = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-i', p], capture_output=True, text=True).stderr
    h, m_, s_ = re.search(r'Duration: (\d+):(\d+):([\d.]+)', r).groups(); return int(h) * 3600 + int(m_) * 60 + float(s_)

def build():
    aud = os.path.join(HERE, 'صوت_shortdiv')
    mp3 = sorted(x for x in os.listdir(aud) if x.endswith('.mp3')); assert len(mp3) == len(S), (len(mp3), len(S))
    A = [dur(os.path.join(aud, x)) for x in mp3]
    DURS = [round((a + .9 + s.get('hold', 0)) * 1000) for a, s in zip(A, S)]
    html = []
    for (sc, a) in zip(S, A):
        txt = CLEAN(sc['narr'])
        cur = [0]
        def T(anchor):
            if not anchor: return 0
            if anchor.startswith('@'): return round(float(anchor[1:]) * a * 1000)
            k = txt.index(anchor, cur[0]); cur[0] = k   # بحثٌ متتابع: العبارة بعد سابقتها (لا أول ظهورٍ لها في النص)
            return round(max(0, a * k / len(txt) - .2) * 1000)
        times = [T(it[0]) for it in sc['items']]
        for sl in {it[3] for it in sc['items'] if it[3]}:   # خطوات المكان الواحد مرتّبة زمنياً، وإلا تراكبت
            ts = [times[n] for n, it in enumerate(sc['items']) if it[3] == sl]
            assert all(x < y for x, y in zip(ts, ts[1:])), (sc['title'], ts)
        slots = {}
        for n, it in enumerate(sc['items']):
            if it[3]: slots.setdefault(it[3], []).append(n)
        body, done = [], set()
        sols = [n for n, it in enumerate(sc['items']) if it[2] == 'solc']
        for n, (anc, h, cls, slot) in enumerate(sc['items']):
            if n in done: continue
            if h == 'FIG': h = FIG
            if slot:
                ns = slots[slot]; done.update(ns)
                body.append('<div class="slot">' + ''.join(
                    f'<div class="el" data-t="{times[m]}" data-u="{times[ns[q + 1]] if q + 1 < len(ns) else ""}">{sc["items"][m][1]}</div>' for q, m in enumerate(ns)) + '</div>')
            elif n in sols:
                done.update(sols)
                body.append('<div class="sols">' + ''.join(f'<div class="el solc" data-t="{times[m]}"><div>{sc["items"][m][1]}</div></div>' for m in sols) + '</div>')
            else:
                body.append(f'<div class="el {cls}" data-t="{times[n]}">{h}</div>')
        title = f'<h2><b>{sc["title"]}</b></h2>' + (f'<div class="sub">{sc["sub"]}</div>' if sc.get('sub') and not sc['items'][0][2] == 'prob' else '')
        html.append(f'<div class="sc{" card" if sc.get("card") else ""}">{title}<div class="body">{"".join(body)}</div></div>')
    page = f'''<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><title>القسمة المختصرة للأعداد العشرية</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cairo:wght@600;700;800;900&amp;display=swap"><style>{CSS}</style></head><body>
<div class="hdr"><span>الصف السابع · الوحدة الثالثة · <b>الدرسان ٣-٥ و٣-٦</b></span><span>القسمة المختصرة للأعداد العشرية</span></div>
{"".join(html)}
<div class="ftr"><span>إعداد: أ. عيسى الحارثي</span><div class="bar"><i></i></div></div>
<script>const DURS = window.DURS = {json.dumps(DURS)};{JS}seek(0, 0);</script></body></html>'''
    p = os.path.join(HERE, 'فيديو_shortdiv.html'); open(p, 'w', encoding='utf-8').write(page); print(p, round(sum(DURS) / 1000), 'ث')

if __name__ == '__main__':
    narr() if sys.argv[1:] == ['narr'] else build()
