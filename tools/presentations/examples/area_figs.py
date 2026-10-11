# رسوم الوحدة السابعة (SVG) — مشتركة بين الشرائح (area_common.py) والملخّصات (gen_*_summary.py).
import re, math as _mm
_FONT = "font-family:Tajawal,'Noto Kufi Arabic',sans-serif"
def _t(x, y, s, fs=30, col='#0E1B33', anc='middle', w=800):
    s = _a(str(s).replace('²', '\x01')).replace('\x01', '<tspan baseline-shift="super" font-size="70%">٢</tspan>')
    return f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anc}" dominant-baseline="middle" direction="rtl" font-size="{fs}" font-weight="{w}" fill="{col}">{s}</text>'

class _C:   # لوحة رسم: تجمع العناصر وتحسب حدود الرسم تلقائياً
    def __init__(s): s.o = []; s.bx = [1e9, 1e9, -1e9, -1e9]
    def grow(s, x, y, r=0):
        b = s.bx; b[0] = min(b[0], x - r); b[1] = min(b[1], y - r); b[2] = max(b[2], x + r); b[3] = max(b[3], y + r)
    def poly(s, pts, fill='#DBEAFE', stroke='#1E3A5F', sw=5, dash=''):
        for x, y in pts: s.grow(x, y)
        d = f' stroke-dasharray="{dash}"' if dash else ''
        s.o.append(f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"{d}/>')
    def line(s, p, q, col='#1E3A5F', sw=4, dash='', cap='round', marker=''):
        s.grow(*p); s.grow(*q)
        d = f' stroke-dasharray="{dash}"' if dash else ''
        s.o.append(f'<line x1="{p[0]:.1f}" y1="{p[1]:.1f}" x2="{q[0]:.1f}" y2="{q[1]:.1f}" stroke="{col}" stroke-width="{sw}" stroke-linecap="{cap}"{d}{marker}/>')
    def text(s, x, y, t, fs=30, col='#0E1B33', anc='middle', w=800):
        n = len(re.sub(r'<[^>]+>', '', str(t))); hw = n * fs * 0.3 + 6
        s.grow(x - (hw if anc == 'middle' else (2 * hw if anc == 'end' else 0)), y - fs * .6)
        s.grow(x + (hw if anc == 'middle' else (2 * hw if anc == 'start' else 0)), y + fs * .6)
        s.o.append(_t(x, y, t, fs, col, anc, w))
    def circle(s, cx, cy, r, fill='#FEF3C7', stroke='#1E3A5F', sw=5):
        s.grow(cx, cy, r); s.o.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
    def dot(s, x, y, r=8, col='#0E1B33'): s.grow(x, y, r); s.o.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{col}"/>')
    def path(s, d, fill='none', stroke='#1E3A5F', sw=5, pts=()):
        for p in pts: s.grow(*p)
        s.o.append(f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"/>')
    def right(s, p, u, v, k=22, col='#1E3A5F'):   # علامة الزاوية القائمة عند p باتجاهَي u و v
        a_ = (p[0] + u[0] * k, p[1] + u[1] * k); c = (p[0] + v[0] * k, p[1] + v[1] * k); b = (a_[0] + v[0] * k, a_[1] + v[1] * k)
        s.o.append(f'<polyline points="{a_[0]:.1f},{a_[1]:.1f} {b[0]:.1f},{b[1]:.1f} {c[0]:.1f},{c[1]:.1f}" fill="none" stroke="{col}" stroke-width="3"/>')
    def elab(s, p, q, t, off=34, fs=30, col='#0E1B33', side=1):   # تسمية ضلعٍ في منتصفه، مزاحةً عمودياً عنه
        mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2; dx, dy = q[0] - p[0], q[1] - p[1]; L = _mm.hypot(dx, dy) or 1
        nx, ny = dy / L * side, -dx / L * side
        s.text(mx + nx * off, my + ny * off, t, fs, col)
    def svg(s, cls='svgfig shp', pad=14):
        b = s.bx; x0, y0 = b[0] - pad, b[1] - pad; W, H = b[2] - b[0] + 2 * pad, b[3] - b[1] + 2 * pad
        return f'<svg class="{cls}" viewBox="{x0:.0f} {y0:.0f} {W:.0f} {H:.0f}" style="direction:ltr;{_FONT}">{"".join(s.o)}</svg>'

def _u(p, q):
    dx, dy = q[0] - p[0], q[1] - p[1]; L = _mm.hypot(dx, dy) or 1; return dx / L, dy / L

def RECT(l, w, L=420, Wd=240, fill='#DBEAFE', grid=None, side=True, top=False, cls='svgfig shp', fs=32):
    # مستطيل: الطول l أسفله، والعرض w على يمينه؛ grid=(أعمدة، صفوف) يرسم مربّعات الوحدة
    c = _C(); P = [(0, 0), (L, 0), (L, Wd), (0, Wd)]
    c.poly(P, fill)
    if grid:
        gc, gr = grid
        for i in range(1, gc): c.line((L * i / gc, 0), (L * i / gc, Wd), '#64748B', 2)
        for j in range(1, gr): c.line((0, Wd * j / gr), (L, Wd * j / gr), '#64748B', 2)
        c.poly(P, 'none')
    if l: c.elab(P[3], P[2], l, -30, fs)
    if w and side: c.elab(P[1], P[2], w, 30 + len(_a(w)) * fs * .28, fs)
    if top and l: c.elab(P[1], P[0], top if isinstance(top, str) else l, -30, fs)
    return c.svg(cls)

def SQGRID(n, side_lab, area_lab, L=300, fill='#FDBA74'):
    # مربّعٌ مقسومٌ n × n (لتوضيح ١ سم² = ١٠٠ ملم²)
    c = _C(); P = [(0, 0), (L, 0), (L, L), (0, L)]; c.poly(P, fill, '#9A3412', 5)
    for i in range(1, n):
        c.line((L * i / n, 0), (L * i / n, L), '#9A3412', 1.5); c.line((0, L * i / n), (L, L * i / n), '#9A3412', 1.5)
    c.elab(P[3], P[2], side_lab, -30, 28); c.elab(P[1], P[2], side_lab, 30 + len(_a(side_lab)) * 8, 28)
    c.text(L / 2, -34, area_lab, 30, '#9A3412')
    return c.svg()

def TRI(base, h, apex=0.35, B=420, H=260, fill='#DCFCE7', hl=True, sides=(), cls='svgfig shp', fs=32, hcol='#DB2777'):
    # مثلث قاعدته أفقية؛ apex موضع الرأس نسبةً للقاعدة (٠ قائم يساراً، ١ قائم يميناً، >١ أو <٠ منفرج والارتفاع خارج المثلث)
    c = _C(); A, Bp, T = (0, H), (B, H), (B * apex, 0)
    c.poly([A, Bp, T], fill)
    if base: c.elab(A, Bp, base, -34, fs)
    if hl:
        foot = (T[0], H)
        if apex < 0 or apex > 1: c.line(foot, A if apex < 0 else Bp, '#1E3A5F', 3, '10 8')
        if 0 < apex < 1 or apex < 0 or apex > 1: c.line(T, foot, hcol, 4, '12 9')
        else: c.line(T, foot, hcol, 6)
        c.right(foot, (0, -1), (1, 0) if apex <= 0.5 else (-1, 0))
        if h: c.text(T[0] + (1 if apex < .5 else -1) * (14 + len(_a(h)) * fs * .3), H / 2 + 10, h, fs, hcol)
    for i, t in sides:   # تسمية الأضلاع المائلة: ٠ الأيسر، ١ الأيمن
        p, q = (A, T) if i == 0 else (T, Bp); c.elab(p, q, t, 30 + len(_a(t)) * 8, fs - 4, '#334155', 1)
    return c.svg(cls)

def PARA(base, h, slant=110, B=380, H=230, fill='#FEF3C7', side='', cls='svgfig shp', fs=32, hcol='#DB2777'):
    c = _C(); P = [(0, H), (B, H), (B + slant, 0), (slant, 0)]; c.poly(P, fill)
    if base: c.elab(P[0], P[1], base, -34, fs)
    c.line((slant, 0), (slant, H), hcol, 4, '12 9'); c.right((slant, H), (0, -1), (1, 0))
    if h: c.text(slant + 16 + len(_a(h)) * fs * .3, H / 2, h, fs, hcol)
    if side: c.elab(P[1], P[2], side, 30 + len(_a(side)) * 8, fs - 4, '#334155', -1)
    return c.svg(cls)

def TRAP(a, b, h, B=440, T=230, off=70, H=220, fill='#EDE9FE', cls='svgfig shp', fs=32, hcol='#DB2777'):
    # شبه منحرف: القاعدة السفلى b، والعليا a (ضلعان متوازيان)، والارتفاع h
    c = _C(); P = [(0, H), (B, H), (off + T, 0), (off, 0)]; c.poly(P, fill)
    if b: c.elab(P[0], P[1], b, -34, fs)
    if a: c.elab(P[3], P[2], a, 34, fs)
    x = off + T * .5; c.line((x, 0), (x, H), hcol, 4, '12 9'); c.right((x, H), (0, -1), (1, 0))
    if h: c.text(x + 16 + len(_a(h)) * fs * .3, H / 2 + 6, h, fs, hcol)
    return c.svg(cls)

def CIRC(r=150, show=('r',), lab=None, fill='#FEF3C7', cls='svgfig shp', fs=32):
    # دائرة وأجزاؤها: 'c' المركز، 'r' نصف القطر، 'd' القطر، 'ch' وتر، 'arc' قوس، 'sec' قطاع، 'seg' قطعة، 'circ' المحيط
    lab = lab or {}; c = _C(); cx = cy = 0
    P = lambda deg, rr=r: (cx + rr * _mm.cos(_mm.radians(deg)), cy - rr * _mm.sin(_mm.radians(deg)))
    c.circle(cx, cy, r, fill)
    if 'sec' in show:
        a1, a2 = P(20), P(80); c.path(f'M{cx},{cy} L{a1[0]:.1f},{a1[1]:.1f} A{r},{r} 0 0 0 {a2[0]:.1f},{a2[1]:.1f} Z', '#F9A8D4', '#BE185D', 4)
        m = P(50, r * .62); c.text(m[0], m[1], lab.get('sec', 'قطاع'), fs - 6, '#831843')
    if 'seg' in show:
        a1, a2 = P(200), P(280); c.path(f'M{a1[0]:.1f},{a1[1]:.1f} A{r},{r} 0 0 0 {a2[0]:.1f},{a2[1]:.1f} Z', '#93C5FD', '#1D4ED8', 4)
        m = P(240, r * .8); c.text(m[0], m[1], lab.get('seg', 'قطعة'), fs - 8, '#1E3A8A')
    if 'circ' in show:
        c.path(f'M{cx - r},{cy} A{r},{r} 0 1 1 {cx - r},{cy + .1}', 'none', '#16A34A', 9)
        p = P(135, r + 34); c.text(p[0] - 30, p[1], lab.get('circ', 'المحيط'), fs, '#15803D')
    if 'arc' in show:
        a1, a2 = P(100), P(160); c.path(f'M{a1[0]:.1f},{a1[1]:.1f} A{r},{r} 0 0 0 {a2[0]:.1f},{a2[1]:.1f}', 'none', '#16A34A', 10)
        p = P(130, r + 36); c.text(p[0], p[1], lab.get('arc', 'قوس'), fs, '#15803D')
    if 'd' in show:
        c.line(P(180), P(0), '#2563EB', 6); c.text(cx + r * .45, cy + 30, lab.get('d', 'القطر'), fs, '#1D4ED8')
    if 'r' in show:
        q = P(-40) if 'd' in show else P(0)
        c.line((cx, cy), q, '#DB2777', 6); m = ((cx + q[0]) / 2, (cy + q[1]) / 2)
        c.text(m[0] + (22 if 'd' in show else 0), m[1] + (30 if 'd' in show else -28), lab.get('r', 'نصف القطر'), fs, '#BE185D')
    if 'ch' in show:
        a1, a2 = P(215), P(325); c.line(a1, a2, '#7C3AED', 6); c.text(cx, a1[1] + 30, lab.get('ch', 'وتر'), fs, '#6D28D9')
    if 'c' in show or 'r' in show or 'd' in show:
        c.dot(cx, cy)
        if 'c' in show: c.text(cx - 6, cy - 30, lab.get('c', 'المركز'), fs - 4, '#0E1B33')
    return c.svg(cls)

def COMP(pts, labels=(), cuts=(), fills=None, fill='#DBEAFE', cls='svgfig shp', fs=30, rights=True, regions=()):
    # شكلٌ مركّب من نقاط (إحداثيات بوحدةٍ ما × k)؛ labels: (رقم الضلع، النص، الإزاحة)؛ cuts: خطوط تقسيمٍ متقطّعة
    # regions: مضلّعات ملوّنة داخل الشكل (نقاط، لون، نص)
    c = _C(); c.poly(pts, fill)
    for rp, col, t in regions:
        c.poly(rp, col, 'none', 0)
        if t: cx = sum(x for x, _ in rp) / len(rp); cy = sum(y for _, y in rp) / len(rp); c.text(cx, cy, t, fs, '#0E1B33')
    c.poly(pts, 'none')
    for p, q in cuts: c.line(p, q, '#DB2777', 4, '12 9')
    n = len(pts)
    for i, t, *o in labels:
        p, q = pts[i], pts[(i + 1) % n]; off = o[0] if o else 30 + len(_a(t)) * fs * .22
        c.elab(p, q, t, off, fs, '#0E1B33', -1)
    return c.svg(cls)


def STAIR2(units, facs, names=None, colors=('#DBEAFE', '#DCFCE7', '#FEF3C7', '#FCE7F3')):
    # سلّم تحويل وحدات المساحة: مثل STAIR في figs.py لكن بمعاملاتٍ كبيرة (١٠٠٠٠٠٠) في شاراتٍ عريضة
    n, sw, sh, pad, top = len(units), 210, 84, 16, 118
    W = n * sw + 2 * pad + 60; H = top + n * sh + 40
    o = ['<defs><marker id="ag2" viewBox="0 0 10 10" markerWidth="3.6" markerHeight="3.6" refX="6" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#15803D"/></marker>'
         '<marker id="ar2" viewBox="0 0 10 10" markerWidth="3.6" markerHeight="3.6" refX="6" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#DC2626"/></marker></defs>']
    X = lambda i: W - pad - (i + 1) * sw
    Y = lambda i: top + i * sh
    for i, u in enumerate(units):
        o.append(f'<rect x="{X(i)}" y="{Y(i)}" width="{sw}" height="{H - pad - Y(i)}" rx="10" fill="{colors[i % len(colors)]}" stroke="#1E3A5F" stroke-width="3"/>')
        o.append(_t(X(i) + sw / 2, Y(i) + 40, u, 40, '#0E1B33', 'middle', 900))
        if names: o.append(_t(X(i) + sw / 2, Y(i) + 74, names[i], 19, '#334155', 'middle', 700))
    for i, f in enumerate(facs):
        s = _a(f'{f:,}'.replace(',', ' ')); w = 26 + len(s) * 15
        cx, cy = X(i), Y(i) + sh / 2 + 4
        o.append(f'<rect x="{cx - w / 2}" y="{cy - 24}" width="{w}" height="48" rx="24" fill="#fff" stroke="#1E3A5F" stroke-width="3"/>')
        o.append(_t(cx, cy + 2, s, 26, '#0E1B33', 'middle', 900))
    x0, y0, x1, y1 = X(0) + sw * 0.6, Y(0) - 40, X(n - 1) + sw * 0.4, Y(n - 1) - 40
    o.append(f'<line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y1}" stroke="#15803D" stroke-width="6" marker-end="url(#ag2)"/>')
    o.append(f'<line x1="{x1}" y1="{y1 - 40}" x2="{x0}" y2="{y0 - 40}" stroke="#DC2626" stroke-width="6" marker-end="url(#ar2)"/>')
    o.append(_t(pad + 330, 30, '÷ صعوداً إلى وحدةٍ أكبر', 27, '#DC2626', 'start', 900))
    o.append(_t(pad + 330, 70, '× نزولاً إلى وحدةٍ أصغر', 27, '#15803D', 'start', 900))
    return f'<svg class="svgfig stair" viewBox="-40 0 {W + 40} {H}" style="direction:ltr;{_FONT}">{"".join(o)}</svg>'
AREA_STAIR = (['كم²', 'م²', 'سم²', 'ملم²'], [1000000, 10000, 100], ['كيلومتر مربّع', 'متر مربّع', 'سنتيمتر مربّع', 'مليمتر مربّع'])
def NB(s): return s.replace(' ', ' ')   # أعدادٌ بفواصل مسافات لا تنكسر: ١٠ ٠٠٠
_GRP = re.compile(r'(?<![٠-٩٫])[٠-٩]{1,3}(?:[ \u00a0][٠-٩]{3})+(?:٫[٠-٩]+)?(?![٠-٩])')
def FIXNUM(S):
    # الأعداد المكتوبة بمجموعات (١٠ ٠٠٠): نعزلها LTR ونمنع كسر السطر، وإلا انعكس ترتيب المجموعات في السياق العربي
    return [_GRP.sub(lambda m: '⁦' + m.group(0).replace(' ', ' ') + '⁩', x) for x in S]
_TAGS = re.compile(r'(<[^>]+>)')
def SUP2(x):   # ² في النص فقط (لا داخل سمات الوسوم مثل data-why) ← أسٌّ مرفوع
    return ''.join(q if q.startswith('<') else q.replace('²', '<sup class="u2">٢</sup>') for q in _TAGS.split(x))

def HALVES(W=240, H=150, gap=50, cls='svgfig shp lg'):
    # المثلث نصف المستطيل المحيط به: ثلاث حالات (قائم، رأسه في المنتصف، رأسه قرب الطرف) والجزءان الخارجيان باللون الفاتح
    c = _C()
    for k, ap in enumerate((0, .5, .85)):
        x0 = k * (W + gap); T = (x0 + W * ap, 0)
        c.poly([(x0, 0), (x0 + W, 0), (x0 + W, H), (x0, H)], '#D1FAE5', '#475569', 3, '9 7')
        c.poly([(x0, H), (x0 + W, H), T], '#16A34A', '#14532D', 4)
        if 0 < ap < 1: c.line(T, (T[0], H), '#14532D', 3, '8 6')
    c.text((W * 3 + gap * 2) / 2, H + 40, 'المثلث الأخضر = نصف المستطيل', 30, '#14532D')
    return c.svg(cls)
