# الحلقة ١ — امتحان نهاية الفصل الأول ٢٠٢٣/٢٠٢٤ (المديرية العامة للتربية والتعليم بمحافظة ظفار)، الصفحة ١: السؤالان ٣ و٤
# المصدر: home.moe.gov.om/images/zawity/file/Book746251.pdf
# الصيغة المعتمدة (٢٠ نوفمبر): سؤالان، لكلٍّ قاعدة ثم حلّ بخطوات، ثم سؤال تحدٍّ للتعليقات ودعوة للإعجاب والمتابعة والمشاركة.
# الصوت: ElevenLabs، ‏eleven_v4، صوت الأستاذ عيسى المنسوخ QPCAh12JacbBf26hHQvQ، بلغة رسمية ودودة، بلا تسريع ولا وسوم حماس.
# الأزمنة (data-t) بالثواني من بداية مقطع كل مشهد، من silencedetect على الصوت النهائي.
from build import CHK, F

TAG = 'الحلقة ١ • الصفحة ١ • السؤالان ٣ و٤'

NARRATION = [
    'السلام عليكم يا طلاب. في هذه الحلقة نحلّ سؤالين من امتحان الوزارة للصف السابع، ونتعلّم القاعدة التي تساعدك على حلّ أي سؤالٍ مشابه.',
    'السؤال الأول: فكّ الأقواس. ثلاثة، في اثنين سين زائد خمسة. القاعدة: العدد الذي خارج القوس، نضربه في كل حدٍّ داخل القوس.',
    'الخطوة الأولى: ثلاثة في اثنين سين، تساوي ستة سين. الخطوة الثانية: ثلاثة في خمسة، تساوي خمسة عشر. إذن الناتج: ستة سين زائد خمسة عشر.',
    'السؤال الثاني: التقريب. القاعدة ثلاث خطوات. أولاً: نحدّد المنزلة المطلوبة. ثانياً: ننظر إلى الرقم الذي بعدها مباشرة. ثالثاً: إذا كان خمسة أو أكثر نزيد واحداً، وإذا كان أقل من خمسة يبقى الرقم كما هو.',
    'سبعة وعشرون فاصلة ثلاثة ثمانية، لأقرب عدد كامل. الرقم بعد الآحاد ثلاثة، وهو أقل من خمسة. الجواب: سبعة وعشرون.',
    'مئتان وخمسة وثلاثون فاصلة صفر تسعة واحد، لمنزلة عشرية واحدة. الرقم بعد الأعشار تسعة، وهو أكبر من خمسة، فنزيد واحداً. الجواب: مئتان وخمسة وثلاثون فاصلة واحد.',
    'وثمانية وستون فاصلة اثنان خمسة ثلاثة، لمنزلتين عشريتين. الرقم بعد المنزلة الثانية ثلاثة، فالجواب: ثمانية وستون فاصلة اثنان خمسة.',
    'والآن دورك: قرّب أربعة فاصلة سبعة ستة، لأقرب منزلة عشرية واحدة، واكتب جوابك في التعليقات. وإذا استفدت من الحلقة، اضغط زر الإعجاب، وتابع القناة، وشارك المقطع مع زملائك. ونلتقي غداً في سؤالٍ جديد.',
]

W = 'position:absolute;left:30px;right:30px;'
AVATAR = ('<div style="width:170px;height:170px;border-radius:50%;background:#14305C;border:5px solid #1E1B18;box-shadow:6px 6px 0 #1E1B18;'
          'margin:0 auto;display:flex;flex-direction:column;align-items:center;justify-content:center;color:#fff">'
          '<div style="font-weight:900;font-size:50px;line-height:1.1">عيسى</div>'
          '<div style="width:96px;height:6px;border-radius:4px;background:#FFE08A;margin:4px 0 6px"></div>'
          '<div style="font-weight:800;font-size:19px;color:#FFE08A">رياضيات</div></div>')


def Q(n, marks, img, t=0):
    return (f'<div class="card" data-t="{t}" data-fx="up" style="{W}top:84px">'
            f'<div class="qhd"><b>السؤال {n}</b><span class="mark">{marks}</span></div>'
            f'<img class="qimg" src="{{{{img:{img}}}}}"></div>')


def HEAD(title, marks):
    return (f'<div style="{W}top:84px"><div class="qhd" style="border:3.5px solid var(--ink);border-radius:14px;box-shadow:4px 4px 0 var(--ink)">'
            f'<b>{title}</b><span class="mark">{marks}</span></div></div>')


def RULE(title, body, top, t):
    return (f'<div class="card" data-t="{t}" data-fx="up" style="{W}top:{top}px">'
            f'<div class="qhd" style="background:var(--ink)"><b style="font-size:26px">📌 {title}</b></div>'
            f'<div style="padding:10px 16px 12px;font-weight:800;font-size:22px;line-height:1.6">{body}</div></div>')


def EXPR(t_arcs=None, size=46):
    """٣(٢س + ٥) بعرضٍ ثابت لكل جزء، ومعه قوسا التوزيع من ٣ إلى كل حدّ (يُرسمان في t_arcs)."""
    parts = [('٣', 50, 'var(--coral)'), ('(', 24, ''), ('٢س', 80, ''), ('+', 50, ''), ('٥', 50, ''), (')', 24, '')]
    cells = ''.join(f'<span style="display:inline-block;width:{w}px;text-align:center;{"color:" + c if c else ""}">{x}</span>' for x, w, c in parts)
    arcs = ''
    if t_arcs is not None:
        arcs = (f'<svg data-t="{t_arcs}" data-fx="draw" width="278" height="46" viewBox="0 0 278 46" style="display:block;margin:0 auto -6px">'
                '<path d="M253 44 Q208 2 164 44" fill="none" stroke="#EC5B4F" stroke-width="3.5" stroke-linecap="round"/>'
                '<path d="M253 44 Q151 -22 49 44" fill="none" stroke="#EC5B4F" stroke-width="3.5" stroke-linecap="round"/></svg>')
    return f'{arcs}<div class="math" style="font-size:{size}px;display:flex;flex-direction:row;justify-content:center;width:278px;margin:0 auto">{cells}</div>'


PLACES = {'م': 'مئات', 'ع': 'عشرات', 'ا': 'آحاد', '١': 'أعشار', '٢': 'أجزاء من مئة', '٣': 'أجزاء من ألف'}


def PV(cols, target, decider, t_target, t_dec):
    """لوحة المنازل: cols قائمة (المنزلة، الرقم) من اليسار إلى اليمين كما يُكتب العدد، و'.' للفاصلة.
    target: فهرس المنزلة المطلوبة (إطار أحمر)، decider: فهرس الرقم الحاسم (أصفر)."""
    out = []
    for i, (p, d) in enumerate(cols):
        if p == '.':
            out.append('<div style="align-self:flex-end;font-weight:900;font-size:44px;padding:0 2px">٫</div>')
            continue
        box = ('border:3px solid var(--ink);border-radius:10px;background:#fff;width:56px;height:64px;display:flex;'
               'align-items:center;justify-content:center;font-weight:900;font-size:40px')
        inner = d
        if i == decider:
            inner = f'<span class="hl no" data-t="{t_dec}" data-fx="hl" style="padding:0 6px">{d}</span>'
        ring = ''
        if i == target:
            ring = f'<div data-t="{t_target}" data-fx="pop" style="position:absolute;inset:-7px;border:4px solid var(--coral);border-radius:14px"></div>'
        out.append(f'<div style="display:flex;flex-direction:column;align-items:center;gap:4px">'
                   f'<div style="font-size:13px;font-weight:800;color:var(--mut);height:34px;display:flex;align-items:flex-end;'
                   f'text-align:center;line-height:1.1;width:60px;justify-content:center">{PLACES[p]}</div>'
                   f'<div style="position:relative;{box}">{inner}{ring}</div></div>')
    return f'<div style="display:flex;direction:ltr;justify-content:center;gap:6px">{"".join(out)}</div>'


STEPS_MINI = ('<div style="display:flex;gap:6px;justify-content:center;flex-wrap:wrap">'
              '<span class="mark" style="font-size:15px">١) المنزلة المطلوبة</span>'
              '<span class="mark" style="font-size:15px">٢) الرقم بعدها</span>'
              '<span class="mark" style="font-size:15px">٣) ٥ فأكثر: نزيد ١ • أقل: يبقى</span></div>')


def ROUND(task, cols, target, decider, verdict, ans, t):
    """مشهد تقريب عددٍ واحد. t = (المهمة، المنزلة، الرقم الحاسم، الحكم، الجواب) بالثواني."""
    t0, t1, t2, t3, t4 = t
    return HEAD('السؤال ٤ • التقريب', 'درجتان') + f'''
    <div style="{W}top:160px">{STEPS_MINI}</div>
    <div data-t="{t0}" data-fx="up" style="{W}top:225px;text-align:center;font-weight:900;font-size:26px">{task}</div>
    <div class="card" data-t="{t0}" data-fx="up" style="{W}top:285px;padding:14px 8px 18px">{PV(cols, target, decider, t1, t2)}</div>
    <div data-t="{t3}" data-fx="up" style="{W}top:455px;text-align:center"><span class="row" style="display:inline-flex;margin:0;font-size:26px">{verdict}</span></div>
    <div data-t="{t4}" style="{W}top:545px;text-align:center"><span class="ans" style="font-weight:900;font-size:40px">الجواب: <bdi class="L">{ans}</bdi></span></div>'''


SCENES = [
    # ١ — الافتتاح: المعلّم والسلسلة وبطاقة الاقتباس من الامتحان
    f'''<div style="{W}top:96px;text-align:center">
      <div data-t="0">{AVATAR}</div>
      <div data-t="0.3" style="margin-top:20px"><span class="pill w" style="font-size:26px">أ. عيسى الحارثي</span></div>
      <div data-t="1.0" class="title" style="font-size:72px;margin-top:22px">٤٠ من ٤٠</div>
      <div data-t="1.2" data-fx="wipe" style="height:8px;width:220px;margin:-4px auto 0;background:var(--coral);border-radius:6px"></div>
      <div data-t="3.0" style="margin-top:24px"><span class="pill">سؤالان من امتحان الوزارة</span></div>
    </div>
    <div data-t="4.0" style="{W}top:600px"><div class="card" style="transform:rotate(-1.5deg);padding:5px"><img src="{{{{img:head}}}}" style="width:100%;display:block"></div></div>''',
    # ٢ — السؤال ٣ وقاعدته
    Q('٣', 'درجة واحدة', 'q3') + f'''
    <div data-t="2.6" data-fx="up" style="{W}top:300px">{EXPR(t_arcs=8.5)}</div>
    ''' + RULE('القاعدة', 'العدد الذي <b style="color:var(--coral)">خارج القوس</b> نضربه في <b style="color:var(--coral)">كل حدّ</b> داخل القوس', 440, 5.5),
    # ٣ — حلّ السؤال ٣ بخطوتين
    HEAD('السؤال ٣ • فكّ الأقواس', 'درجة واحدة') + f'''
    <div style="{W}top:180px">{EXPR(t_arcs=0)}</div>
    <div style="{W}top:300px">
      <div class="row" data-t="0.2" data-fx="up" style="font-size:30px"><span class="mark">الخطوة ١</span>&nbsp;<span style="color:var(--coral)">٣</span>&nbsp;×&nbsp;٢س&nbsp;=&nbsp;<b>٦س</b></div>
      <div class="row" data-t="5.0" data-fx="up" style="font-size:30px"><span class="mark">الخطوة ٢</span>&nbsp;<span style="color:var(--coral)">٣</span>&nbsp;×&nbsp;٥&nbsp;=&nbsp;<b>١٥</b></div>
      <div data-t="9.4" style="text-align:center;margin-top:26px"><span class="ans math" style="font-size:44px">الناتج: ٦س + ١٥</span></div>
    </div>''',
    # ٤ — السؤال ٤ وقاعدته بثلاث خطوات
    Q('٤', 'درجتان', 'q4') + RULE('القاعدة: ثلاث خطوات',
        '<div data-t="4.4" data-fx="fade">١) نحدّد <b style="color:var(--coral)">المنزلة المطلوبة</b>.</div>'
        '<div data-t="7.4" data-fx="fade">٢) ننظر إلى <b style="color:var(--coral)">الرقم الذي بعدها</b> مباشرة.</div>'
        '<div data-t="11.4" data-fx="fade">٣) <span class="ok">٥ أو أكثر ← نزيد ١</span><br>&nbsp;&nbsp;&nbsp;&nbsp;<span class="no">أقل من ٥ ← يبقى كما هو</span></div>',
        372, 2.4),
    # ٥ — ٢٧٫٣٨ لأقرب عدد كامل
    ROUND('<bdi class="L">٢٧٫٣٨</bdi> ← لأقرب عدد كامل',
          [('ع', '٢'), ('ا', '٧'), ('.', ''), ('١', '٣'), ('٢', '٨')], 1, 3,
          '٣ أقل من ٥ ← يبقى ٧', '٢٧', (0, 1.6, 3.8, 4.7, 6.9)),
    # ٦ — ٢٣٥٫٠٩١ لمنزلة عشرية واحدة
    ROUND('<bdi class="L">٢٣٥٫٠٩١</bdi> ← لمنزلة عشرية واحدة',
          [('م', '٢'), ('ع', '٣'), ('ا', '٥'), ('.', ''), ('١', '٠'), ('٢', '٩'), ('٣', '١')], 4, 5,
          '٩ أكبر من ٥ ← نزيد ١ على الصفر', '٢٣٥٫١', (0, 4.2, 8.4, 8.8, 11.4)),
    # ٧ — ٦٨٫٢٥٣ لمنزلتين عشريتين
    ROUND('<bdi class="L">٦٨٫٢٥٣</bdi> ← لمنزلتين عشريتين',
          [('ع', '٦'), ('ا', '٨'), ('.', ''), ('١', '٢'), ('٢', '٥'), ('٣', '٣')], 4, 5,
          '٣ أقل من ٥ ← يبقى ٥', '٦٨٫٢٥', (0, 3.7, 7.0, 7.4, 8.6)),
    # ٨ — سؤال التحدّي والدعوة للتفاعل
    f'''<div class="title" data-t="0" style="{W}top:96px;font-size:62px">دورك! ✍️</div>
    <div class="card" data-t="0.4" data-fx="up" style="{W}top:200px">
      <div class="hd" style="font-size:30px">سؤال التحدّي</div>
      <div style="padding:16px;text-align:center;font-weight:900;font-size:30px">قرّب <bdi class="L">٤٫٧٦</bdi><br><span style="font-size:24px">لأقرب منزلة عشرية واحدة</span></div>
      <div data-t="5.7" data-fx="fade" class="note" style="padding:0 0 14px;font-size:22px;color:var(--ink)">💬 اكتب جوابك في التعليقات</div>
    </div>
    <div style="{W}top:470px;display:flex;gap:10px;justify-content:center">
      <span class="pill w" data-t="9.2" style="font-size:22px">👍 إعجاب</span>
      <span class="pill w" data-t="11.0" style="font-size:22px">🔔 متابعة</span>
      <span class="pill" data-t="11.8" style="font-size:22px">↗ مشاركة</span>
    </div>
    <div data-t="13.6" data-fx="fade" style="{W}top:560px;text-align:center"><span class="pill" style="background:var(--ink)">نلتقي غداً في سؤالٍ جديد</span></div>
    <div data-t="13.6" data-fx="fade" class="note" style="{W}top:640px;font-size:21px;color:var(--ink)">إعداد: أ. عيسى الحارثي</div>''',
]
