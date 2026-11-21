# لبنات مشاهد «٤٠ من ٤٠» — مشتركة بين كل الحلقات حتى تبقى الجودة البصرية ثابتة.
# كل مشهد عمودٌ واحد (STACK) تتتابع عناصره بمسافة ثابتة، فلا تراكب. لا مواضع مطلقة داخل المشهد.
# بعد البناء: node check.mjs <الحلقة.html> يجب أن يطبع ✓ قبل التصيير.

AVATAR = ('<div style="width:150px;height:150px;border-radius:50%;background:#14305C;border:5px solid #1E1B18;box-shadow:6px 6px 0 #1E1B18;'
          'margin:0 auto;display:flex;flex-direction:column;align-items:center;justify-content:center;color:#fff">'
          '<div style="font-weight:900;font-size:44px;line-height:1.1">عيسى</div>'
          '<div style="width:84px;height:6px;border-radius:4px;background:#FFE08A;margin:4px 0 6px"></div>'
          '<div style="font-weight:800;font-size:17px;color:#FFE08A">رياضيات</div></div>')


def STACK(*items, gap=16, justify='flex-start'):
    return f'<div class="stack" style="gap:{gap}px;justify-content:{justify}">{"".join(items)}</div>'


def T(t, html, fx='pop', cls='', style=''):
    """عنصر يظهر في الثانية t من المشهد."""
    return f'<div data-t="{t}" data-fx="{fx}" class="{cls}" style="{style}">{html}</div>'


def QCARD(n, marks, img, t=0):
    """بطاقة السؤال: رأسه ودرجته وصورته من الامتحان."""
    return (f'<div class="card" data-t="{t}" data-fx="up"><div class="qhd"><b>السؤال {n}</b><span class="mark">{marks}</span></div>'
            f'<img class="qimg" src="{{{{img:{img}}}}}" style="border-bottom:0"></div>')


def HEAD(title, marks):
    return (f'<div class="qhd" style="border:3.5px solid var(--ink);border-radius:14px;box-shadow:4px 4px 0 var(--ink)">'
            f'<b>{title}</b><span class="mark">{marks}</span></div>')


def RULE(title, lines, t):
    """بطاقة القاعدة. lines: [(الزمن، النص)…] سطرٌ لكل خطوة، كلٌّ في سطره."""
    body = ''.join(f'<div data-t="{lt}" data-fx="fade" style="padding:2px 0">{x}</div>' for lt, x in lines)
    return (f'<div class="card" data-t="{t}" data-fx="up"><div class="qhd" style="background:var(--ink)"><b style="font-size:26px">📌 {title}</b></div>'
            f'<div style="padding:10px 16px 12px;font-weight:800;font-size:22px;line-height:1.55">{body}</div></div>')


def CHIPS(*xs):
    return '<div class="chips">' + ''.join(f'<span class="mark">{x}</span>' for x in xs) + '</div>'


def STEPL(t, label, html, size=28):
    return (f'<div class="steprow" data-t="{t}" data-fx="up" style="font-size:{size}px"><span class="mark">{label}</span>'
            f'<span style="flex:1;text-align:center">{html}</span></div>')


def STEP(t, n, html, size=28):
    return STEPL(t, f'الخطوة {n}', html, size)


def ANS(t, html, size=38):
    return f'<div class="center" data-t="{t}"><span class="ans" style="font-weight:900;font-size:{size}px">{html}</span></div>'


def EXPR(parts, t_arcs=None, size=46):
    """تعبير مثل ٣(٢س + ٥): parts [(النص، المفتاح أو None، اللون أو None)…] بترتيب القراءة.
    المفاتيح a (العامل)، t1، t2 (الحدّان) تحدّد طرفَي قوسَي التوزيع؛ يُحسبان من مواضع الحدود الفعلية في القالب."""
    cells = ''.join(f'<span {"data-k=" + chr(34) + k + chr(34) if k else ""} style="display:inline-block;padding:0 4px;{"color:" + c if c else ""}">{x}</span>'
                    for x, k, c in parts)
    arcs = ''
    if t_arcs is not None:
        arcs = (f'<svg data-arcs="1" data-t="{t_arcs}" data-fx="draw" height="40" style="display:block">'
                '<path fill="none" stroke="#EC5B4F" stroke-width="3.5" stroke-linecap="round"/>'
                '<path fill="none" stroke="#EC5B4F" stroke-width="3.5" stroke-linecap="round"/></svg>')
    return (f'<div style="display:flex;flex-direction:column;align-items:center"><div style="position:relative">{arcs}'
            f'<div class="math" style="font-size:{size}px;white-space:nowrap">{cells}</div></div></div>')


PLACES = {'م': 'مئات', 'ع': 'عشرات', 'ا': 'آحاد', '١': 'أعشار', '٢': 'أجزاء من مئة', '٣': 'أجزاء من ألف'}


def PV(cols, target, decider, t_target, t_dec):
    """لوحة المنازل. cols: [(المنزلة، الرقم)…] من اليسار إلى اليمين كما يُكتب العدد، و('.', '') للفاصلة.
    المنزلة المطلوبة: إطارٌ أحمر داخل مربّعها (لا يتعدّاه)، والرقم الحاسم: مربّعه أصفر."""
    out = []
    for i, (p, d) in enumerate(cols):
        if p == '.':
            out.append('<div class="pvc" style="width:12px"><div class="pvlab"></div><div class="pvsep">٫</div></div>')
            continue
        fx = (f' data-t="{t_target}" data-fx="tgt"' if i == target else f' data-t="{t_dec}" data-fx="dec"' if i == decider else '')
        out.append(f'<div class="pvc"><div class="pvlab">{PLACES[p]}</div><div class="pvbox"{fx}>{d}</div></div>')
    return f'<div class="card" style="padding:12px 8px 14px"><div class="pv">{"".join(out)}</div></div>'


def FR(a, b, size=None):
    """كسر عمودي (بسط فوق مقام)."""
    st = f' style="font-size:{size}px"' if size else ''
    return f'<span class="frac"{st}><span>{a}</span><span>{b}</span></span>'


def OPEN(ep, skill, qcard, t_card=0):
    """افتتاح قصير: شارة السلسلة والحلقة، ثم المهارة، وبطاقة السؤال الأول من الثانية الأولى."""
    return STACK(T(0, f'<span class="pill">٤٠ من ٤٠ • الحلقة {ep}</span>', cls='center'),
                 T(0.2, skill, cls='title', style='font-size:56px;line-height:1.15'),
                 qcard,
                 T(0.6, 'أ. عيسى الحارثي • من امتحان الوزارة', 'fade', 'center', 'font-weight:800;font-size:19px;color:var(--mut)'),
                 gap=18)


def MISTAKE(head, t, wrong, why, right, t_right):
    """⚠️ خطأ شائع: الجواب الخاطئ مشطوباً وسببه، ثم الصحيح."""
    return STACK(head,
                 f'<div class="card" data-t="{t}" data-fx="up"><div class="qhd" style="background:#B3261E"><b style="font-size:28px">⚠️ خطأ شائع</b></div>'
                 f'<div class="center" style="padding:14px 14px 6px"><span style="display:inline-block;border:3px dashed #B3261E;border-radius:12px;background:#FDECEA;padding:4px 14px;font-weight:900;font-size:28px;color:#B3261E">'
                 f'<span class="mark" style="background:#B3261E;color:#fff;border-color:#B3261E;font-size:15px;vertical-align:middle">✗ خطأ</span> {wrong}</span></div>'
                 f'<div class="center" style="padding:0 16px 14px;font-weight:800;font-size:21px;line-height:1.5">{why}</div></div>',
                 ANS(t_right, f'✓ الصحيح: {right}', 34), gap=22)


def CHALLENGE(q, sub, t_comment, t_like, t_follow, t_share, t_bye):
    return STACK(T(0, 'دورك! ✍️', cls='title', style='font-size:58px;line-height:1.1'),
                 '<div class="card" data-t="0.4" data-fx="up"><div class="hd" style="font-size:30px">سؤال التحدّي</div>'
                 f'<div class="center" style="padding:14px 16px 6px;font-weight:900;font-size:30px">{q}</div>'
                 f'<div class="center" style="padding:0 16px 14px;font-weight:800;font-size:23px">{sub}</div></div>',
                 T(t_comment, '💬 اكتب جوابك في التعليقات', 'fade', 'center', 'font-weight:900;font-size:24px'),
                 '<div style="display:flex;gap:10px;justify-content:center">'
                 f'<span class="pill w" data-t="{t_like}" style="font-size:21px">👍 إعجاب</span>'
                 f'<span class="pill w" data-t="{t_follow}" style="font-size:21px">🔔 متابعة</span>'
                 f'<span class="pill" data-t="{t_share}" style="font-size:21px">↗ مشاركة</span></div>',
                 T(t_bye, '<span class="pill" style="background:var(--ink)">نلتقي غداً في سؤالٍ جديد</span>', 'fade', 'center'),
                 T(t_bye, 'إعداد: أ. عيسى الحارثي', 'fade', 'center', 'font-weight:800;font-size:20px'), gap=20)


CTA_NARR = 'واكتب جوابك في التعليقات. وإذا استفدت من الحلقة، اضغط زر الإعجاب، وتابع القناة، وشارك المقطع مع زملائك. ونلتقي غداً إن شاء الله في سؤال جديد.'


def CHALLENGE_AT(q, sub):
    """سؤال التحدّي بأزمنة مربوطة بكلمات التعليق القياسي (CTA_NARR)."""
    return CHALLENGE(q, sub, '@واكتب جوابك', '@اضغط زر', '@وتابع القناة', '@وشارك المقطع', '@ونلتقي')
