# رسوماتٌ للعروض: صور أسئلة الكتاب (مقصوصة في sources/g7-math/figs) ورسومٌ توضيحية SVG من إعدادنا.
# FIG('3-3_mosque') ← صورة الكتاب مضمّنة؛ TBARS(4, 2) ← نموذج الأشرطة العشرية لـ ٤ × ٠٫٢؛ GRID100(cols, cells) ← شبكة المئة؛ SHARE(…) ← نموذج التقسيم.
import base64 as _b64
_FIGS = os.path.join(os.path.dirname(HERE) if os.path.basename(HERE) == 'examples' else HERE, 'sources', 'g7-math', 'figs')
def FIG(name, cls='fig', alt=''):
    data = _b64.b64encode(open(os.path.join(_FIGS, name + '.jpg'), 'rb').read()).decode()
    return f'<img class="{cls}" alt="{alt or name}" src="data:image/jpeg;base64,{data}">'

_AR10 = '٠١٢٣٤٥٦٧٨٩'
def _a(s): return ''.join(_AR10[int(c)] if c.isdigit() else ('٫' if c == '.' else c) for c in str(s))
PAL = ['#F59E0B', '#2563EB', '#16A34A', '#DB2777', '#7C3AED', '#0891B2', '#DC2626', '#65A30D', '#EA580C']

def TBARS(groups, per, label=True):
    # groups مجموعات، في كلٍّ منها per جزءاً من عشرة؛ كل شريطٍ واحدٌ صحيح مقسومٌ إلى ١٠ أجزاء
    total = groups * per; bars = max(1, -(-total // 10)); cw, ch, gap = 40, 46, 16
    W = 10 * cw + 4; H = bars * (ch + gap) + (30 if label else 0)
    out = []
    for b in range(bars):
        y = b * (ch + gap)
        for c in range(10):
            k = b * 10 + c; fill = PAL[k // per % len(PAL)] if k < total else '#fff'
            out.append(f'<rect x="{2 + c * cw}" y="{y + 2}" width="{cw}" height="{ch}" fill="{fill}" stroke="#334155" stroke-width="2"/>')
        out.append(f'<rect x="2" y="{y + 2}" width="{10 * cw}" height="{ch}" fill="none" stroke="#0E1B33" stroke-width="4"/>')
    if label:
        val = f'{total // 10}' + (f'.{total % 10}' if total % 10 else '')
        out.append(f'<text x="{W / 2}" y="{H - 4}" text-anchor="middle" direction="rtl" font-size="26" font-weight="800" fill="#0E1B33">{_a(total)} {"أجزاء" if 3 <= total <= 10 else "جزءاً"} من عشرة = {_a(val)}</text>')
    return f'<svg class="svgfig" viewBox="0 0 {W} {H}" style="direction:ltr">{"".join(out)}</svg>'

def GRID100(cols=0, cells=0, color='#2563EB', color2='#F59E0B'):
    # شبكة ١٠ × ١٠ تمثّل الواحد: نظلّل cols أعمدة (كل عمودٍ ٠٫١) ثم cells مربّعات (كل مربّعٍ ٠٫٠١)
    s = 30; out = []
    for c in range(10):
        for r in range(10):
            fill = color if c < cols else (color2 if c == cols and r < cells else '#fff')
            out.append(f'<rect x="{2 + c * s}" y="{2 + r * s}" width="{s}" height="{s}" fill="{fill}" stroke="#94A3B8" stroke-width="1.5"/>')
    out.append(f'<rect x="2" y="2" width="{10 * s}" height="{10 * s}" fill="none" stroke="#0E1B33" stroke-width="4"/>')
    return f'<svg class="svgfig sq" viewBox="0 0 {10 * s + 4} {10 * s + 4}" style="direction:ltr">{"".join(out)}</svg>'

def SHARE(wholes, tenths, k, names=None):
    # تقسيم (wholes + tenths/10) بالتساوي على k: لكل صفٍّ wholes/k مربّعاتٍ كاملة و tenths/k أشرطة (جزء من عشرة)
    w1, t1 = wholes // k, tenths // k; s, tw, gap = 52, 9, 16; out = []
    W = 150 + w1 * (s + 10) + t1 * (tw + 6) + 10; H = k * (s + gap)
    for i in range(k):
        y = i * (s + gap); col = PAL[i % len(PAL)]
        lab = names[i] if names else f'{i + 1}'
        out.append(f'<text x="{W - 4}" y="{y + s / 2 + 9}" text-anchor="end" font-size="26" font-weight="800" fill="{col}">{lab}</text>')
        x = 4
        for _ in range(w1):
            out.append(f'<rect x="{x}" y="{y}" width="{s}" height="{s}" rx="6" fill="{col}" stroke="#0E1B33" stroke-width="2.5"/>'); x += s + 10
        for _ in range(t1):
            out.append(f'<rect x="{x}" y="{y}" width="{tw}" height="{s}" rx="2" fill="{col}" opacity=".75" stroke="#0E1B33" stroke-width="2"/>'); x += tw + 6
    return f'<svg class="svgfig" viewBox="0 0 {W} {H}" style="direction:ltr">{"".join(out)}</svg>'

FIG_CSS = '''
.fig{width:min(560px,38vw);height:auto;max-height:40vh;border-radius:14px;border:3px solid var(--line);background:#fff;object-fit:contain}
.fig.sm{width:min(400px,28vw)}.fig.lg{max-width:min(760px,56vw);max-height:40vh}
.svgfig{width:min(560px,40vw);height:auto;max-height:36vh;font-family:var(--fh)}
.svgfig.sq{width:auto;height:min(38vh,380px)}
.figrow{display:flex;align-items:center;justify-content:center;gap:2.4vw;flex-wrap:wrap}
.xq .fig.lg{height:32vh}
.xq .fig.side{float:right;height:36vh;margin:0 0 0 1.6vw}
.xq .fig{display:block;margin:.4vh auto;height:22vh;width:auto;max-width:90%}
'''

def STAIR(units, facs, names=None, colors=('#DBEAFE', '#DCFCE7', '#FEF3C7', '#FCE7F3')):
    # سلّم التحويل (الوحدة الرابعة): الوحدة الكبرى أعلى اليمين، وننزل درجةً درجةً إلى الصغرى.
    # نزولاً (إلى وحدةٍ أصغر) نضرب، وصعوداً (إلى وحدةٍ أكبر) نقسم؛ معامل كل درجةٍ في دائرةٍ على حافّتها.
    n, sw, sh, pad, top = len(units), 170, 78, 16, 118
    W = max(n * sw, 560) + 2 * pad; H = top + n * sh + 40
    o = ['<defs><marker id="ag" viewBox="0 0 10 10" markerWidth="3.6" markerHeight="3.6" refX="6" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#15803D"/></marker>'
         '<marker id="ar" viewBox="0 0 10 10" markerWidth="3.6" markerHeight="3.6" refX="6" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#DC2626"/></marker></defs>']
    X = lambda i: W - pad - (i + 1) * sw
    Y = lambda i: top + i * sh
    for i, u in enumerate(units):
        o.append(f'<rect x="{X(i)}" y="{Y(i)}" width="{sw}" height="{H - pad - Y(i)}" rx="10" fill="{colors[i % len(colors)]}" stroke="#1E3A5F" stroke-width="3"/>')
        o.append(f'<text x="{X(i) + sw / 2}" y="{Y(i) + 44}" text-anchor="middle" font-size="38" font-weight="900" fill="#0E1B33">{u}</text>')
        if names: o.append(f'<text x="{X(i) + sw / 2}" y="{Y(i) + 70}" text-anchor="middle" font-size="19" font-weight="700" fill="#334155">{names[i]}</text>')
    for i, f in enumerate(facs):
        cx, cy = X(i), Y(i) + sh / 2 + 4
        o.append(f'<circle cx="{cx}" cy="{cy}" r="27" fill="#fff" stroke="#1E3A5F" stroke-width="3"/>')
        o.append(f'<text x="{cx}" y="{cy + 8}" text-anchor="middle" font-size="{22 if f >= 1000 else 25}" font-weight="900" fill="#0E1B33">{_a(f)}</text>')
    x0, y0, x1, y1 = X(0) + sw * 0.6, Y(0) - 40, X(n - 1) + sw * 0.4, Y(n - 1) - 40
    o.append(f'<line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y1}" stroke="#15803D" stroke-width="6" marker-end="url(#ag)"/>')
    o.append(f'<line x1="{x1}" y1="{y1 - 40}" x2="{x0}" y2="{y0 - 40}" stroke="#DC2626" stroke-width="6" marker-end="url(#ar)"/>')
    o.append(f'<text x="{pad + 300}" y="34" font-size="27" font-weight="900" fill="#DC2626" direction="rtl" text-anchor="start">÷ صعوداً إلى وحدةٍ أكبر</text>')
    o.append(f'<text x="{pad + 300}" y="72" font-size="27" font-weight="900" fill="#15803D" direction="rtl" text-anchor="start">× نزولاً إلى وحدةٍ أصغر</text>')
    return f'<svg class="svgfig stair" viewBox="0 0 {W} {H}" style="direction:ltr;font-family:Tajawal,\'Noto Kufi Arabic\',sans-serif">{"".join(o)}</svg>'

# ── الزوايا (الوحدة الخامسة) ──
import math as _m
def ANG(deg, start=0, label=None, names=None, reflex=False, color='#2563EB', size=300, arm=1.0, mark=True, sub=None):
    # زاويةٌ قياسها deg بين ضلعٍ باتجاه start وآخر باتجاه start+deg (عكس عقارب الساعة).
    # reflex=True: يُرسم قوس الزاوية المنعكسة (الخارجية). names=('ب','أ','ج'): طرف الضلع الأول، الرأس، طرف الضلع الثاني.
    # label: نصّ القياس (افتراضياً deg°)؛ sub: سطرٌ تحت الرسم.
    W = H = size; cx = cy = size / 2; L = size * .42 * arm; _pts = [(cx, cy)]
    def pt(a, r): return cx + r * _m.cos(_m.radians(a)), cy - r * _m.sin(_m.radians(a))
    a1, a2 = start, start + deg
    p1, p2 = pt(a1, L), pt(a2, L); _pts += [p1, p2]
    out = [f'<line x1="{cx}" y1="{cy}" x2="{p1[0]:.1f}" y2="{p1[1]:.1f}" stroke="#14305C" stroke-width="5" stroke-linecap="round"/>',
           f'<line x1="{cx}" y1="{cy}" x2="{p2[0]:.1f}" y2="{p2[1]:.1f}" stroke="#14305C" stroke-width="5" stroke-linecap="round"/>']
    r = size * (.13 if not reflex else .11); _pts += [(cx - r, cy - r), (cx + r, cy + r)] if reflex or deg >= 180 else []
    if mark:
        if deg == 90 and not reflex:
            s = size * .08; q1, q2 = pt(a1, s), pt(a2, s); q3 = (q1[0] + q2[0] - cx, q1[1] + q2[1] - cy)
            out.append(f'<path d="M{q1[0]:.1f},{q1[1]:.1f} L{q3[0]:.1f},{q3[1]:.1f} L{q2[0]:.1f},{q2[1]:.1f}" fill="none" stroke="{color}" stroke-width="4"/>')
        else:
            s1, s2 = pt(a1, r), pt(a2, r)
            if reflex:
                out.append(f'<path d="M{cx},{cy} L{s1[0]:.1f},{s1[1]:.1f} A{r},{r} 0 {1 if 360 - deg > 180 else 0} 1 {s2[0]:.1f},{s2[1]:.1f} Z" fill="{color}22" stroke="none"/>'
                           f'<path d="M{s1[0]:.1f},{s1[1]:.1f} A{r},{r} 0 {1 if 360 - deg > 180 else 0} 1 {s2[0]:.1f},{s2[1]:.1f}" fill="none" stroke="{color}" stroke-width="4"/>')
            else:
                out.append(f'<path d="M{cx},{cy} L{s1[0]:.1f},{s1[1]:.1f} A{r},{r} 0 {1 if deg > 180 else 0} 0 {s2[0]:.1f},{s2[1]:.1f} Z" fill="{color}22" stroke="none"/>'
                           f'<path d="M{s1[0]:.1f},{s1[1]:.1f} A{r},{r} 0 {1 if deg > 180 else 0} 0 {s2[0]:.1f},{s2[1]:.1f}" fill="none" stroke="{color}" stroke-width="4"/>')
    if label != '':
        txt = label if label is not None else _a(deg if not reflex else 360 - deg) + '°'
        mid = (a1 + a2) / 2 + (180 if reflex else 0)
        lr = r + size * (.13 if deg >= 60 or reflex else .24)
        t = pt(mid, lr); _pts += [(t[0] - size * .12, t[1] - size * .06), (t[0] + size * .12, t[1] + size * .06)]
        out.append(f'<text x="{t[0]:.1f}" y="{t[1] + 10:.1f}" text-anchor="middle" direction="rtl" font-size="{size * .095:.0f}" font-weight="800" fill="{color}" font-family="Readex Pro,Tahoma,sans-serif">{txt}</text>')
    if names:
        for (a, rr), n in zip(((a1, L + size * .07), (None, 0), (a2, L + size * .07)), names):
            if not n: continue
            if a is None:
                mid = (a1 + a2) / 2 + (0 if reflex else 180); t = pt(mid, size * .1); t = (t[0], t[1] + (size * .04 if not reflex else 0))
            else: t = pt(a, rr)
            _pts += [(t[0] - size * .05, t[1] - size * .05), (t[0] + size * .05, t[1] + size * .06)]
            out.append(f'<text x="{t[0]:.1f}" y="{t[1] + 10:.1f}" text-anchor="middle" font-size="{size * .09:.0f}" font-weight="800" fill="#14305C" font-family="Readex Pro,Tahoma,sans-serif">{n}</text>')
    pad = size * .05
    x0 = min(p[0] for p in _pts) - pad; x1 = max(p[0] for p in _pts) + pad; y0 = min(p[1] for p in _pts) - pad; y1 = max(p[1] for p in _pts) + pad
    if sub:
        out.append(f'<text x="{(x0 + x1) / 2:.1f}" y="{y1 + size * .09:.0f}" text-anchor="middle" font-size="{size * .085:.0f}" font-weight="800" fill="#14305C" font-family="Readex Pro,Tahoma,sans-serif">{sub}</text>'); y1 += size * .13
    vw, vh = x1 - x0, y1 - y0
    return f'<svg class="svgfig ang" viewBox="{x0:.1f} {y0:.1f} {vw:.1f} {vh:.1f}" width="{vw:.0f}" height="{vh:.0f}" xmlns="http://www.w3.org/2000/svg">' + ''.join(out) + '</svg>'

def XL(theta=35, labels=('أ', 'ب', 'ج', 'ء'), colors=('#2563EB', '#DB2777', '#2563EB', '#DB2777'), size=420, perp=False):
    # خطّان مستقيمان متقاطعان بزاوية theta؛ الزوايا الأربع حول التقاطع: labels بالترتيب (أ أعلى، ب يسار، ج أسفل، ء يمين).
    # الزاويتان المتقابلتان بالرأس بلون واحد. perp=True: خطّان متعامدان بمربّعات قائمة.
    if perp: theta = 90
    W, H = size, size * .75; cx, cy = W / 2, H / 2; L = size * .46
    def pt(a, r): return cx + r * _m.cos(_m.radians(a)), cy - r * _m.sin(_m.radians(a))
    a1, a2 = 90 - theta / 2, 90 + theta / 2
    lines = [(a1, a1 + 180), (a2, a2 + 180)]
    out = []
    order = [(a1, a2), (a2, a1 + 180), (a1 + 180, a2 + 180), (a2 + 180, a1 + 360)]   # أعلى، يسار، أسفل، يمين
    r = size * .12
    for (s0, s1), lab, col in zip(order, labels, colors):
        if perp:
            k = size * .06; q1, q2 = pt(s0, k), pt(s1, k); q3 = (q1[0] + q2[0] - cx, q1[1] + q2[1] - cy)
            out.append(f'<path d="M{q1[0]:.1f},{q1[1]:.1f} L{q3[0]:.1f},{q3[1]:.1f} L{q2[0]:.1f},{q2[1]:.1f}" fill="none" stroke="{col}" stroke-width="4"/>')
        else:
            p1, p2 = pt(s0, r), pt(s1, r)
            out.append(f'<path d="M{cx},{cy} L{p1[0]:.1f},{p1[1]:.1f} A{r},{r} 0 0 0 {p2[0]:.1f},{p2[1]:.1f} Z" fill="{col}2A" stroke="{col}" stroke-width="3"/>')
        if lab:
            t = pt((s0 + s1) / 2, r + size * .07)
            out.append(f'<text x="{t[0]:.1f}" y="{t[1] + 11:.1f}" text-anchor="middle" direction="rtl" font-size="{size * .075:.0f}" font-weight="800" fill="{col}" font-family="Readex Pro,Tahoma,sans-serif">{lab}</text>')
    for b, e in lines:
        p, q = pt(b, L), pt(e, L)
        out.append(f'<line x1="{p[0]:.1f}" y1="{p[1]:.1f}" x2="{q[0]:.1f}" y2="{q[1]:.1f}" stroke="#14305C" stroke-width="5" stroke-linecap="round"/>')
    return f'<svg class="svgfig ang" viewBox="0 {-size * .08:.0f} {W} {H + size * .16:.0f}" width="{W}" height="{H + size * .16:.0f}" xmlns="http://www.w3.org/2000/svg">' + ''.join(out) + '</svg>'

def PAR(hl=(), labels=('أ', 'ب', 'ج', 'ء', 'هـ', 'و', 'ز', 'ح'), vals=None, tilt=62, size=460, colors=('#2563EB', '#DB2777', '#16A34A', '#F59E0B'), shape=''):
    # خطّان متوازيان أفقيان (بأسهم) يقطعهما قاطعٌ مائل بزاوية tilt. الزوايا الثماني بالترتيب:
    # عند التقاطع العلوي: ٠ أعلى اليمين، ١ أعلى اليسار، ٢ أسفل اليسار، ٣ أسفل اليمين؛ وعند السفلي: ٤، ٥، ٦، ٧ بالترتيب نفسه.
    # hl: مجموعات زوايا تُلوَّن معاً، مثل [(0, 4)] للمتناظرتين. vals: قياسات تُكتب بدل الحروف. shape='F' أو 'Z': يرسم الحرف فوق الشكل.
    W, H = size, size * .78; y1, y2 = H * .3, H * .72; dx = (y2 - y1) / _m.tan(_m.radians(tilt)); x1 = W / 2 + dx / 2; x2 = W / 2 - dx / 2
    out = []
    for y in (y1, y2):
        out.append(f'<line x1="{W * .04:.1f}" y1="{y:.1f}" x2="{W * .96:.1f}" y2="{y:.1f}" stroke="#14305C" stroke-width="5"/>')
        ax = W * .5 + (W * .3 if y == y1 else -W * .28)
        out.append(f'<path d="M{ax - 14:.1f},{y - 9:.1f} L{ax + 4:.1f},{y:.1f} L{ax - 14:.1f},{y + 9:.1f}" fill="none" stroke="#14305C" stroke-width="4"/>')
    ext = H * .22
    tx1, ty1 = x1 + ext / _m.tan(_m.radians(tilt)), y1 - ext; tx2, ty2 = x2 - ext / _m.tan(_m.radians(tilt)), y2 + ext
    rays = [0, tilt, 180, 180 + tilt]   # يمين، القاطع لأعلى، يسار، القاطع لأسفل
    secs = [(0, tilt), (tilt, 180), (180, 180 + tilt), (180 + tilt, 360)]
    r = size * .075; col = {}
    for gi, g in enumerate(hl):
        for i in g: col[i] = colors[gi % len(colors)]
    for k in range(8):
        cx, cy = (x1, y1) if k < 4 else (x2, y2); s0, s1 = secs[k % 4]
        def pt(a, rr): return cx + rr * _m.cos(_m.radians(a)), cy - rr * _m.sin(_m.radians(a))
        c = col.get(k)
        if c:
            p1, p2 = pt(s0, r), pt(s1, r)
            out.append(f'<path d="M{cx:.1f},{cy:.1f} L{p1[0]:.1f},{p1[1]:.1f} A{r},{r} 0 0 0 {p2[0]:.1f},{p2[1]:.1f} Z" fill="{c}55" stroke="{c}" stroke-width="3"/>')
        lab = (vals[k] if vals and vals[k] is not None else labels[k]) if (labels or vals) else ''
        if lab:
            t = pt((s0 + s1) / 2, r + size * .055)
            out.append(f'<text x="{t[0]:.1f}" y="{t[1] + 9:.1f}" text-anchor="middle" direction="rtl" font-size="{size * .06:.0f}" font-weight="800" fill="{c or "#14305C"}" font-family="Readex Pro,Tahoma,sans-serif">{lab}</text>')
    out.append(f'<line x1="{tx1:.1f}" y1="{ty1:.1f}" x2="{tx2:.1f}" y2="{ty2:.1f}" stroke="#14305C" stroke-width="5" stroke-linecap="round"/>')
    if shape == 'F':
        out.append(f'<path d="M{x2 + W * .25:.1f},{y2:.1f} L{x2:.1f},{y2:.1f} L{x1:.1f},{y1:.1f} L{x1 + W * .25:.1f},{y1:.1f}" fill="none" stroke="#DC2626" stroke-width="7" stroke-opacity=".6" stroke-linejoin="round"/>')
    if shape == 'Z':
        out.append(f'<path d="M{x1 - W * .25:.1f},{y1:.1f} L{x1:.1f},{y1:.1f} L{x2:.1f},{y2:.1f} L{x2 + W * .25:.1f},{y2:.1f}" fill="none" stroke="#DC2626" stroke-width="7" stroke-opacity=".6" stroke-linejoin="round"/>')
    return f'<svg class="svgfig ang par" viewBox="0 {-H * .04:.0f} {W} {H * 1.08:.0f}" width="{W}" height="{H * 1.08:.0f}" xmlns="http://www.w3.org/2000/svg">' + ''.join(out) + '</svg>'
