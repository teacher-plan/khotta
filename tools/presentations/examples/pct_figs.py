# رسوم الوحدة الثامنة (SVG): بطارية، شريط النسبة المئوية، شبكة — تحتاج area_figs.py.
def BATT(p, w=240, h=110, col=None, cls='svgfig shp sm'):
    # بطارية هاتف مشحونة p٪
    col = col or ('#16A34A' if p >= 50 else ('#F59E0B' if p >= 20 else '#DC2626'))
    c = _C(); c.poly([(0, 0), (w, 0), (w, h), (0, h)], '#fff', '#0E1B33', 6)
    c.poly([(w, h * .3), (w + 18, h * .3), (w + 18, h * .7), (w, h * .7)], '#0E1B33', '#0E1B33', 2)
    if p: c.poly([(8, 8), (8 + (w - 16) * p / 100, 8), (8 + (w - 16) * p / 100, h - 8), (8, h - 8)], col, col, 1)
    c.text(w / 2, h + 40, _a(p) + '٪', 40, '#0E1B33', w=900)
    return c.svg(cls)

def PBAR(parts, total=100, w=900, h=90, cls='svgfig shp lg', labels=True):
    # شريطٌ من ٠ إلى ١٠٠٪ مقسّم أجزاء: parts = [(القيمة، اللون، النص)]
    c = _C(); x = 0
    for v, col, t in parts:
        ww = w * v / total; c.poly([(x, 0), (x + ww, 0), (x + ww, h), (x, h)], col, '#0E1B33', 3)
        if labels and t: c.text(x + ww / 2, h / 2, t, 34, '#0E1B33', w=900)
        x += ww
    if x < w: c.poly([(x, 0), (w, 0), (w, h), (x, h)], '#fff', '#0E1B33', 3)
    c.poly([(0, 0), (w, 0), (w, h), (0, h)], 'none', '#0E1B33', 5)
    for k in range(0, 101, 25):
        X_ = w * k / 100; c.line((X_, h), (X_, h + 14), '#0E1B33', 3); c.text(X_, h + 38, _a(k) + '٪', 26, '#334155')
    return c.svg(cls)

def GRIDN(rows, cols, shaded, col='#B8A97E', cell=50, cls='svgfig shp'):
    # شبكة صفوف × أعمدة، والمربّعات المظلّلة قائمةٌ بأزواج (صف، عمود) أو عددٌ يظلّل من البداية
    c = _C()
    S_ = set(shaded) if not isinstance(shaded, int) else {(k // cols, k % cols) for k in range(shaded)}
    for r in range(rows):
        for q in range(cols):
            c.poly([(q * cell, r * cell), ((q + 1) * cell, r * cell), ((q + 1) * cell, (r + 1) * cell), (q * cell, (r + 1) * cell)], col if (r, q) in S_ else '#fff', '#334155', 2)
    c.poly([(0, 0), (cols * cell, 0), (cols * cell, rows * cell), (0, rows * cell)], 'none', '#0E1B33', 4)
    return c.svg(cls)
