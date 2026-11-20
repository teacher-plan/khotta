# الحلقة ١ — امتحان نهاية الفصل الأول ٢٠٢٣/٢٠٢٤ (المديرية العامة للتربية والتعليم بمحافظة ظفار)، الصفحة ١ (الأسئلة ١–٤، ٥ درجات)
# المصدر: home.moe.gov.om/images/zawity/file/Book746251.pdf
# الصوت: ElevenLabs، ‏eleven_v4، صوت الأستاذ عيسى المنسوخ QPCAh12JacbBf26hHQvQ («عيسى»، عُماني)، ثم تقصير الوقفات و atempo=1.2
# (النسخة الأولى كانت بصوت Maged Magdy المصري MLELiE1ybdYoTtlmFf5r و atempo=1.18)
# الأزمنة (data-t) بالثواني من بداية مقطع كل مشهد، من silencedetect على الصوت النهائي.
from build import CHK, F

TAG = 'الحلقة ١ • الصفحة ١ من ٧'

NARRATION = [
    '[cheerful] هلا والله يا شباب الصف السابع! هذي أول حلقة من سلسلة: أربعين من أربعين.',
    'كل يوم بناخذ صفحة من امتحان حقيقي. نفهم المطلوب من السؤال، ونحلّه خطوة خطوة، ونعرف الدرجة وين تروح.',
    'امتحان اليوم: نهاية الفصل الدراسي الأول، الدور الأول، سنة ألفين وثلاثة وعشرين، ألفين وأربعة وعشرين. يالله نبدأ الصفحة الأولى!',
    'السؤال الأول: صح ولّا خطأ؟ سعة الزجاجة لترين... صح! قارورة ماي كبيرة. طول القلم اثنين ملّي... خطأ! اثنين ملّي أصغر من حبّة العيش، والقلم طوله تقريباً خمسطعش سنتي.',
    'السؤال الثاني: الكسر واحد على ثلاثة يكافئ كم؟ نضرب البسط والمقام في نفس الرقم. واحد في خمسة بخمسة، وثلاثة في خمسة بخمسطعش. يعني الجواب: خمسة على خمسطعش.',
    'السؤال الثالث: فك الأقواس. ثلاثة، في اثنين س زائد خمسة. نضرب الثلاثة في كل حدّ داخل القوس: ثلاثة في اثنين س بستّة س، وثلاثة في خمسة بخمسطعش. الناتج: ستّة س زائد خمسطعش.',
    'السؤال الرابع: التقريب. نشوف الرقم اللي بعد المنزلة المطلوبة: إذا خمسة أو أكثر نزيد واحد، وإذا أقل يبقى. سبعة وعشرين فاصلة ثلاثة ثمانية، لأقرب عدد كامل: الثلاثة أقل من خمسة، يعني سبعة وعشرين. ميتين وخمسة وثلاثين فاصلة صفر تسعة واحد، لمنزلة وحدة: التسعة أكبر من خمسة، يعني ميتين وخمسة وثلاثين فاصلة واحد. وثمانية وستين فاصلة اثنين خمسة ثلاثة، لمنزلتين: الثلاثة أقل من خمسة، يعني ثمانية وستين فاصلة اثنين خمسة.',
    '[cheerful] كذا خلصنا الصفحة الأولى، وخذنا خمس درجات كاملة! باكر الصفحة الثانية. تابعونا عشان توصلون للأربعين من أربعين.',
]

W = 'position:absolute;left:30px;right:30px;'
AVATAR = ('<div style="width:200px;height:200px;border-radius:50%;background:#14305C;border:5px solid #1E1B18;box-shadow:7px 7px 0 #1E1B18;'
          'margin:0 auto;display:flex;flex-direction:column;align-items:center;justify-content:center;color:#fff">'
          '<div style="font-weight:900;font-size:58px;line-height:1.1">عيسى</div>'
          '<div style="width:110px;height:7px;border-radius:4px;background:#FFE08A;margin:4px 0 6px"></div>'
          '<div style="font-weight:800;font-size:22px;color:#FFE08A">رياضيات</div></div>')


def Q(n, marks, img, t=0):
    return (f'<div class="card" data-t="{t}" data-fx="up" style="{W}top:84px">'
            f'<div class="qhd"><b>السؤال {n}</b><span class="mark">{marks}</span></div>'
            f'<img class="qimg" src="{{{{img:{img}}}}}"></div>')


SCENES = [
    # ١ — الافتتاح
    f'''<div style="{W}top:130px;text-align:center">
      <div data-t="0">{AVATAR}</div>
      <div data-t="0.3" style="margin-top:26px"><span class="pill w" style="font-size:28px">أ. عيسى الحارثي</span></div>
      <div data-t="2.1" style="margin-top:44px"><span class="pill">أوّل حلقة من سلسلة</span></div>
      <div data-t="3.6" class="title" style="font-size:96px;margin-top:18px">٤٠ من ٤٠</div>
      <div data-t="3.9" data-fx="wipe" style="height:10px;width:300px;margin:-6px auto 0;background:var(--coral);border-radius:6px"></div>
      <div data-t="4.2" data-fx="fade" class="note" style="margin-top:22px;font-size:24px">رياضيات الصف السابع • امتحانات حقيقية</div>
    </div>''',
    # ٢ — فكرة السلسلة
    f'''<div class="title" data-t="0" style="{W}top:120px">كل حلقة</div>
    <div class="card" data-t="0.4" data-fx="up" style="{W}top:220px">
      <div class="hd">صفحة من امتحان حقيقي</div>
      <div class="note" style="margin-top:10px">امتحانات الوزارة • رياضيات الصف السابع</div>
      <div class="row"><span data-t="2.2" data-fx="fade">المطلوب من السؤال</span>{CHK(2.6)}</div>
      <div class="row"><span data-t="3.6" data-fx="fade">الحل خطوة بخطوة</span>{CHK(4.0)}</div>
      <div class="row" style="margin-bottom:18px"><span data-t="5.0" data-fx="fade">توزيع الدرجات</span>{CHK(5.4)}</div>
    </div>''',
    # ٣ — بطاقة الاقتباس من الامتحان
    f'''<div class="title" data-t="0" style="{W}top:110px;font-size:52px">من امتحان الوزارة</div>
    <div data-t="0.5" style="{W}top:200px;transform-origin:center">
      <div class="card" style="transform:rotate(-2deg);padding:6px"><img src="{{{{img:head}}}}" style="width:100%;display:block"></div></div>
    <div style="{W}top:440px;text-align:center">
      <div data-t="1.0"><span class="pill">نهاية الفصل الدراسي الأول</span></div>
      <div data-t="3.5" style="margin-top:22px"><span class="pill w">الدور الأول • ٢٠٢٣ / ٢٠٢٤</span></div>
      <div data-t="6.3" class="title" style="margin-top:40px;font-size:64px">الصفحة <span style="color:var(--coral)">١</span></div>
    </div>''',
    # ٤ — السؤال ١: صح أم خطأ
    Q('١', 'درجة واحدة', 'q1') + f'''
    <div style="{W}top:320px">
      <div class="row" data-t="2.0" data-fx="up">سعة الزجاجة = ٢ لتر <span class="ok" data-t="3.5" style="font-size:22px">صحيحة</span>{CHK(3.5)}</div>
      <div class="note" data-t="4.1" data-fx="fade">زجاجة ماء كبيرة ← ٢ لتر معقول</div>
      <div class="row" data-t="5.2" data-fx="up" style="margin-top:22px">طول القلم = ٢ ملم <span class="no" data-t="6.7" style="font-size:22px">خاطئة</span>{CHK(6.7, ok=False)}</div>
      <div class="note" data-t="7.3" data-fx="fade">٢ ملم أصغر من حبّة الأرز!</div>
      <div data-t="9.3" style="text-align:center;margin-top:18px"><span class="ans" style="font-weight:900;font-size:30px">طول القلم ≈ ١٥ سم</span></div>
      <svg data-t="9.7" data-fx="wipe" viewBox="0 0 480 50" style="display:block;width:100%;margin-top:14px"><rect x="10" y="8" width="460" height="34" rx="5" fill="#FFE08A" stroke="#1E1B18" stroke-width="3"/>
        <g stroke="#1E1B18" stroke-width="2.5">''' + ''.join(f'<line x1="{20 + i * 29.3:.1f}" y1="8" x2="{20 + i * 29.3:.1f}" y2="{24 if i % 5 == 0 else 18}"/>' for i in range(16)) + '''</g></svg>
    </div>''',
    # ٥ — السؤال ٢: كسر مكافئ
    Q('٢', 'درجة واحدة', 'q2') + f'''
    <div style="{W}top:360px;text-align:center">
      <div class="note" data-t="3.4" data-fx="fade" style="font-size:24px;color:var(--ink)">نضرب البسط والمقام في <b style="color:var(--coral)">العدد نفسه</b></div>
      <div class="math" style="margin-top:18px;font-size:46px">
        <span data-t="3.6" style="display:inline-block">{F('١', '٣')}</span>
        <span data-t="5.5" style="display:inline-block">= {F('١ × <b style="color:var(--coral)">٥</b>', '٣ × <b style="color:var(--coral)">٥</b>')}</span>
        <span data-t="7.2" style="display:inline-block">= {F('٥', '١٥')}</span>
      </div>
      <div data-t="9.0" style="margin-top:26px"><span class="ans math" style="font-size:34px">الإجابة: {F('٥', '١٥')} ✓</span></div>
    </div>''',
    # ٦ — السؤال ٣: فك الأقواس
    Q('٣', 'درجة واحدة', 'q3') + f'''
    <div style="{W}top:330px;text-align:center">
      <div class="math" data-t="2.4" style="font-size:52px"><span style="color:var(--coral)">٣</span>(٢س + ٥)</div>
      <div class="note" data-t="4.3" data-fx="fade" style="font-size:23px;color:var(--ink);margin-top:6px">نضرب <b style="color:var(--coral)">٣</b> في كل حدّ داخل القوس</div>
      <div class="row" data-t="6.8" data-fx="up" style="justify-content:center;font-size:32px"><span style="color:var(--coral)">٣</span>&nbsp;×&nbsp;٢س&nbsp;=&nbsp;<b>٦س</b></div>
      <div class="row" data-t="8.8" data-fx="up" style="justify-content:center;font-size:32px"><span style="color:var(--coral)">٣</span>&nbsp;×&nbsp;٥&nbsp;=&nbsp;<b>١٥</b></div>
      <div data-t="11.4" style="margin-top:18px"><span class="ans math" style="font-size:40px">٦س + ١٥ ✓</span></div>
    </div>''',
    # ٧ — السؤال ٤: التقريب
    Q('٤', 'درجتان', 'q4') + f'''
    <div class="card" data-t="1.8" data-fx="up" style="{W}top:370px;padding:6px 14px;text-align:center;font-weight:900;font-size:21px;box-shadow:4px 4px 0 var(--ink)">
      ننظر إلى الرقم <u>بعد</u> المنزلة المطلوبة<br>
      <span class="ok">٥ أو أكثر ← نزيد ١</span> &nbsp;•&nbsp; <span class="no">أقل من ٥ ← يبقى</span></div>
    <div style="{W}top:474px">''' + ''.join(
        f'''<div class="row" data-t="{t0}" data-fx="up" style="font-size:28px;margin:8px 0;min-height:54px">
          <bdi class="L">{a}<span class="hl no" data-t="{t1}" data-fx="hl">{d}</span>{b}</bdi>
          <span style="font-size:17px;color:var(--mut)">{lab}</span>
          <span data-t="{t2}" style="margin-inline-start:auto" class="ans">≈ <bdi class="L">{r}</bdi></span></div>'''
        for t0, t1, t2, a, d, b, lab, r in [
            (6.0, 9.6, 10.8, '٢٧٫', '٣', '٨', 'لأقرب عدد كامل', '٢٧'),
            (12.4, 18.0, 19.6, '٢٣٥٫٠', '٩', '١', 'منزلة عشرية واحدة', '٢٣٥٫١'),
            (21.3, 24.9, 26.6, '٦٨٫٢٥', '٣', '', 'منزلتان عشريتان', '٦٨٫٢٥'),
        ]) + '</div>',
    # ٨ — الختام
    f'''<div style="{W}top:120px;text-align:center">
      <div class="title" data-t="0">خلّصنا الصفحة ١</div>
      <div data-t="1.4" style="margin:26px auto 0;width:230px;height:230px;border-radius:50%;background:var(--paper);border:5px solid var(--ink);box-shadow:7px 7px 0 var(--ink);display:flex;flex-direction:column;align-items:center;justify-content:center">
        <div style="font-family:Lalezar;font-size:84px;line-height:1;color:var(--green)">٥ / ٥</div><div style="font-weight:900;font-size:22px">درجات كاملة</div></div>
      <div data-t="2.0" data-fx="fade" style="margin-top:34px;font-weight:900;font-size:20px">الطريق إلى ٤٠</div>
      <div data-t="2.0" data-fx="fade" style="height:26px;border:3px solid var(--ink);border-radius:14px;background:#fff;overflow:hidden;margin-top:6px">
        <div data-t="2.3" data-fx="wipe" style="height:100%;width:12.5%;margin-inline-start:0;background:var(--coral);float:right"></div></div>
      <div data-t="3.3" style="margin-top:30px"><span class="pill" style="font-size:28px">غداً: الصفحة ٢</span></div>
      <div data-t="4.5" data-fx="fade" class="note" style="margin-top:22px;font-size:22px;color:var(--ink)">إعداد: أ. عيسى الحارثي</div>
    </div>''',
]
