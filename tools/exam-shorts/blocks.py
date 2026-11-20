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


def STEP(t, n, html):
    return f'<div class="steprow" data-t="{t}" data-fx="up"><span class="mark">الخطوة {n}</span><span style="flex:1;text-align:center">{html}</span></div>'


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
