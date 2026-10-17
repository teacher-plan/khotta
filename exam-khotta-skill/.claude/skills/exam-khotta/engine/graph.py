# شبكة الإحداثيات كما في كتاب الرياضيات (الصف السابع، الوحدة ١٦ «الرسوم البيانية»):
# خطوط الشبكة زرقاء فاتحة بوحدة واحدة، والمحوران أسودان بسهمين، و«س» عند طرف المحور الأفقي و«ص» أعلى الرأسي،
# والأعداد بالأرقام العربية والسالب بإشارة مرفوعة يمين العدد (٢⁻)، والنقطة علامة × وبجانبها حرفها.
# الحقل في ملف الاختبار: "graph" للسؤال، و"graph_answer" للإجابة في دليل التصحيح (guides/FORMAT.md).
import html

AR = str.maketrans('0123456789', '٠١٢٣٤٥٦٧٨٩')
FONT = "Arial, 'Noto Sans Arabic', 'Liberation Sans', sans-serif"
GRID, AXIS, INK, ANS = '#8ccfe9', '#111', '#111', '#c00000'


def _num(v, dg='ar'):
    """العدد على المحور: (نصّ العدد، سالب؟)"""
    s = ('%g' % abs(v)).replace('.', '٫' if dg == 'ar' else '.')
    return (s.translate(AR) if dg == 'ar' else s), v < 0


def _label(x, y, v, dg, anchor, size):
    s, neg = _num(v, dg)
    t = f'<text x="{x:.2f}" y="{y:.2f}" font-size="{size}" text-anchor="{anchor}" direction="ltr">{s}'
    if neg:   # الإشارة السالبة مرفوعة يمين العدد كما في الكتاب
        t += f'<tspan font-size="{size * 0.8:.2f}" dy="{-size * 0.35:.2f}">−</tspan>'
    return t + '</text>'


def check(g):
    """أخطاء تعريف الشبكة: النقاط والأشكال خارج المدى، ومدى غير صالح."""
    E = []
    try:
        x0, x1 = g.get('x', [-5, 5]); y0, y1 = g.get('y', [-5, 5])
    except (TypeError, ValueError):
        return ['المدى x و y زوجان مثل [-5, 5]']
    if x0 >= x1 or y0 >= y1:
        E.append('المدى غير صالح: الحدّ الأدنى أكبر من الأعلى')
    inside = lambda p: x0 <= p[0] <= x1 and y0 <= p[1] <= y1
    for p in g.get('points', []):
        if not inside(p['at']):
            E.append(f'النقطة {p.get("label", "")} {tuple(p["at"])} خارج الشبكة')
    for s in g.get('shapes', []):
        for p in s['pts']:
            if not inside(p):
                E.append(f'رأس الشكل {tuple(p)} خارج الشبكة')
    return E


def svg(g, dg='ar', answer=None):
    """SVG للشبكة. answer: شبكة ثانية تُرسم فوقها بالأحمر (نموذج الإجابة)."""
    x0, x1 = g.get('x', [-5, 5]); y0, y1 = g.get('y', [-5, 5])
    u = float(g.get('unit', 6))          # مم لكل وحدة
    step = g.get('step', 1)              # تدريج الأعداد على المحورين
    pad = u * 1.4
    W, H = (x1 - x0) * u + 2 * pad, (y1 - y0) * u + 2 * pad
    X = lambda v: pad + (v - x0) * u
    Y = lambda v: pad + (y1 - v) * u
    fs = max(2.6, min(3.6, u * 0.55))    # حجم الأعداد بالمم
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W:.1f}mm" height="{H:.1f}mm" viewBox="0 0 {W:.2f} {H:.2f}" '
         f'font-family="{FONT}" fill="{INK}">']
    if g.get('grid', True):
        for i in range(int(x0), int(x1) + 1):
            o.append(f'<line x1="{X(i):.2f}" y1="{Y(y0):.2f}" x2="{X(i):.2f}" y2="{Y(y1):.2f}" stroke="{GRID}" stroke-width="0.25"/>')
        for j in range(int(y0), int(y1) + 1):
            o.append(f'<line x1="{X(x0):.2f}" y1="{Y(j):.2f}" x2="{X(x1):.2f}" y2="{Y(j):.2f}" stroke="{GRID}" stroke-width="0.25"/>')
    ax = g.get('axes', True)
    if ax:
        ext = u * 0.8
        o.append('<defs><marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">'
                 f'<path d="M0,0 L10,5 L0,10 z" fill="{AXIS}"/></marker></defs>')
        if y0 <= 0 <= y1:
            o.append(f'<line x1="{X(x0) - ext:.2f}" y1="{Y(0):.2f}" x2="{X(x1) + ext:.2f}" y2="{Y(0):.2f}" stroke="{AXIS}" '
                     f'stroke-width="0.45" marker-start="url(#ar)" marker-end="url(#ar)"/>')
        if x0 <= 0 <= x1:
            o.append(f'<line x1="{X(0):.2f}" y1="{Y(y0) + ext:.2f}" x2="{X(0):.2f}" y2="{Y(y1) - ext:.2f}" stroke="{AXIS}" '
                     f'stroke-width="0.45" marker-start="url(#ar)" marker-end="url(#ar)"/>')
        nx, ny = g.get('names', ['س', 'ص'])
        o.append(f'<text x="{X(x1) + ext + 0.6:.2f}" y="{Y(0) + fs * 0.35:.2f}" font-size="{fs * 1.25:.2f}" text-anchor="start">{html.escape(nx)}</text>')
        o.append(f'<text x="{X(0):.2f}" y="{Y(y1) - ext - 1:.2f}" font-size="{fs * 1.25:.2f}" text-anchor="middle">{html.escape(ny)}</text>')
        if g.get('numbers', True):
            k = x0
            while k <= x1 + 1e-9:   # الأعداد تحت المحور الأفقي، والصفر مرة واحدة عند نقطة الأصل
                if abs(k) > 1e-9:
                    o.append(_label(X(k), Y(0) + fs * 1.15, k, dg, 'middle', fs))
                k += step
            k = y0
            while k <= y1 + 1e-9:
                if abs(k) > 1e-9:
                    o.append(_label(X(0) - fs * 0.45, Y(k) + fs * 0.35, k, dg, 'end', fs))
                k += step
            o.append(_label(X(0) - fs * 0.45, Y(0) + fs * 1.15, 0, dg, 'end', fs))
    o += _items(g, X, Y, x0, x1, y0, y1, u, fs, INK)
    if answer:
        o += _items(answer, X, Y, x0, x1, y0, y1, u, fs, ANS)
    o.append('</svg>')
    return ''.join(o)


def _clip_line(ln, x0, x1, y0, y1):
    """طرفا المستقيم داخل الشبكة: {"x": 2} أو {"y": -3} أو {"m": 2, "c": 1} (ص = م س + ج) أو {"through": [[..],[..]]}."""
    if 'x' in ln:
        return (ln['x'], y0), (ln['x'], y1)
    if 'y' in ln:
        return (x0, ln['y']), (x1, ln['y'])
    if 'through' in ln:
        (a, b), (c, d) = ln['through']
        if a == c:
            return (a, y0), (a, y1)
        m = (d - b) / (c - a); cc = b - m * a
    else:
        m, cc = ln['m'], ln.get('c', 0)
    pts = []
    for xx in (x0, x1):
        yy = m * xx + cc
        if y0 - 1e-9 <= yy <= y1 + 1e-9:
            pts.append((xx, yy))
    if m:
        for yy in (y0, y1):
            xx = (yy - cc) / m
            if x0 - 1e-9 <= xx <= x1 + 1e-9:
                pts.append((xx, yy))
    pts = sorted(set((round(p[0], 6), round(p[1], 6)) for p in pts))
    return (pts[0], pts[-1]) if len(pts) >= 2 else None


OFF = {'ne': (1, -1, 'start'), 'nw': (-1, -1, 'end'), 'se': (1, 1, 'start'), 'sw': (-1, 1, 'end'),
       'n': (0, -1.3, 'middle'), 's': (0, 1.6, 'middle'), 'e': (1.3, 0.3, 'start'), 'w': (-1.3, 0.3, 'end')}


def _items(g, X, Y, x0, x1, y0, y1, u, fs, color):
    o = []
    for s in g.get('shapes', []):
        pts = ' '.join(f'{X(p[0]):.2f},{Y(p[1]):.2f}' for p in s['pts'])
        tag = 'polygon' if s.get('closed', True) else 'polyline'
        fill = s.get('fill') or 'none'
        dash = ' stroke-dasharray="1.2,0.9"' if s.get('dashed') else ''
        o.append(f'<{tag} points="{pts}" fill="{fill}" fill-opacity="0.35" stroke="{color}" stroke-width="0.5"{dash}/>')
        for p, lab in zip(s['pts'], s.get('labels', [])):
            if lab:
                dx, dy, an = OFF[s.get('label_pos', 'ne')] if isinstance(s.get('label_pos'), str) else OFF['ne']
                o.append(f'<text x="{X(p[0]) + dx * fs * 0.5:.2f}" y="{Y(p[1]) + dy * fs * 0.5:.2f}" font-size="{fs * 1.2:.2f}" '
                         f'fill="{color}" text-anchor="{an}">{html.escape(lab)}</text>')
    for ln in g.get('lines', []):
        ends = _clip_line(ln, x0, x1, y0, y1)
        if not ends:
            continue
        (a, b), (c, d) = ends
        dash = ' stroke-dasharray="1.2,0.9"' if ln.get('dashed') else ''
        o.append(f'<line x1="{X(a):.2f}" y1="{Y(b):.2f}" x2="{X(c):.2f}" y2="{Y(d):.2f}" stroke="{color}" stroke-width="0.5"{dash}/>')
        if ln.get('label'):
            lx, ly = (c, d) if ln.get('label_at', 'end') == 'end' else (a, b)
            o.append(f'<text x="{X(lx):.2f}" y="{Y(ly) - fs * 0.5:.2f}" font-size="{fs * 1.1:.2f}" fill="{color}" '
                     f'text-anchor="middle">{html.escape(ln["label"])}</text>')
    for p in g.get('points', []):
        x, y = X(p['at'][0]), Y(p['at'][1]); r = u * 0.22
        if p.get('mark', 'x') == 'dot':
            o.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r * 0.6:.2f}" fill="{color}"/>')
        else:
            o.append(f'<path d="M{x - r:.2f},{y - r:.2f}L{x + r:.2f},{y + r:.2f}M{x - r:.2f},{y + r:.2f}L{x + r:.2f},{y - r:.2f}" '
                     f'stroke="{color}" stroke-width="0.5"/>')
        if p.get('label'):
            dx, dy, an = OFF.get(p.get('pos', 'ne'), OFF['ne'])
            o.append(f'<text x="{x + dx * fs * 0.7:.2f}" y="{y + dy * fs * 0.75:.2f}" font-size="{fs * 1.2:.2f}" fill="{color}" '
                     f'text-anchor="{an}">{html.escape(p["label"])}</text>')
    return o


if __name__ == '__main__':   # معاينة: python3 graph.py > g.svg
    print(svg({'x': [-5, 5], 'y': [-5, 5], 'points': [{'at': [2, 4], 'label': 'أ'}, {'at': [-4, -1], 'label': 'ج', 'pos': 's'}],
               'shapes': [{'pts': [[-3, 1], [1, 1], [1, -2], [-3, -2]], 'labels': ['ب', 'ج', 'د', 'هـ']}],
               'lines': [{'m': 2, 'c': 1, 'label': 'ص = ٢س + ١'}]}))
