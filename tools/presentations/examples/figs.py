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
