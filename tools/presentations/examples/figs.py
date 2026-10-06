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
