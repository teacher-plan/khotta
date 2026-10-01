# عملية رأسية (جمع أو طرح) بفواصل عشرية على خطٍّ واحد — أنماطٌ مضمّنة، فتعمل في العرض والملخّص والفيديو.
# vcol('14.7', '8.56', '+')  ← الأعداد بأرقام لاتينية و«.» فاصلة، وتُعرض بأرقام عربية و«٫».
#   res: '=' يُحسب الناتج (الافتراضي)، None بلا ناتج (سطرٌ فارغ تحت الخط).
#   marks: 'auto' (الافتراضي) يحسب المحمول في الجمع وأرقام الاستلاف في الطرح ويشطب الأرقام المستلَف منها، None بلا علامات.
#   pad: الأصفار المضافة لإكمال المنازل تظهر بلونٍ مختلف. reveal=True: سطر العلامات وسطر الناتج يظهران خطوةً خطوة في العرض (class="st").
from decimal import Decimal as _Dec
_AR = '٠١٢٣٤٥٦٧٨٩'
def _ar(s): return ''.join(_AR[int(c)] if c.isdigit() else ('٫' if c == '.' else c) for c in str(s))
def vres(a, b, op):
    Dm = max(len(x.partition('.')[2]) for x in (a, b))
    r = _Dec(a) + _Dec(b) if op == '+' else _Dec(a) - _Dec(b)
    return f'{r:.{Dm}f}'
def vcol(a, b, op, res='=', marks='auto', pad=True, reveal=False, fs=''):
    if res == '=': res = vres(a, b, op)
    nums = [a, b] + ([res] if res else [])
    I = max(len(x.partition('.')[0]) for x in nums)
    Dm = max(len(x.partition('.')[2]) for x in nums)
    L = I + (1 + Dm if Dm else 0)
    def cells(x):
        i, hp, d = x.partition('.')
        out = [('', '')] * (I - len(i)) + [(c, '') for c in i]
        if Dm:
            out.append(('.', '' if hp else 'z'))
            out += [(c, '') for c in d] + [('0', 'z')] * (Dm - len(d))
        return out
    top, bot = cells(a), cells(b)
    mk, strike = [''] * L, set()
    if marks == 'auto':
        cols = [j for j in range(L) if top[j][0] != '.']
        if op == '+':
            c = 0
            for n, j in enumerate(reversed(cols)):
                s = sum(int(x[j][0]) if x[j][0] not in ('', '.') else 0 for x in (top, bot)) + c
                c = s // 10
                if c and n + 1 < len(cols): mk[list(reversed(cols))[n + 1]] = '1'
        else:
            cur = {j: int(top[j][0]) if top[j][0] else 0 for j in cols}
            for n, j in enumerate(reversed(cols)):
                bv = int(bot[j][0]) if bot[j][0] else 0
                if cur[j] < bv:
                    left = [k for k in cols if k < j][::-1]
                    for k in left:
                        if cur[k] > 0:
                            cur[k] -= 1; strike.add(k); mk[k] = str(cur[k]); break
                        cur[k] = 9; strike.add(k); mk[k] = '9'
                    cur[j] += 10; strike.add(j); mk[j] = str(cur[j])
    elif marks:
        mk = (list(marks) + [''] * L)[:L]
    TD = 'padding: 0 .07em; text-align: center; min-width: .6em'
    def td(c, k='', extra=''):
        s = TD
        if c == '.': s += '; color: #C0262D'
        if k == 'z' and pad: s += '; color: #2563EB; background-color: #E4EEFF; border-radius: .12em'
        if k == 'z' and not pad: c = ''
        return f'<td style="{s}{extra}">{_ar(c)}</td>'
    rows = []
    if any(m.strip() for m in mk):
        rows.append(('mk', ''.join(f'<td style="{TD}; font-size: .5em; color: #C2410C; vertical-align: bottom">{_ar(m.strip())}</td>' for m in mk) + '<td></td>'))
    SK = '; background-image: linear-gradient(to top right, transparent 44%, #C0262D 44%, #C0262D 56%, transparent 56%)'   # شَرطةٌ مائلة تظهر فوق الصفر أيضاً
    rows.append(('', ''.join(td(c, k, SK if j in strike else '') for j, (c, k) in enumerate(top)) + '<td></td>'))
    rows.append(('', ''.join(td(c, k) for c, k in bot) + f'<td style="{TD}; color: #C2410C; padding-inline-start: .25em">{"+" if op == "+" else "−"}</td>'))
    LN = '; border-top: .07em solid currentColor'
    if res:
        rows.append(('res', ''.join(td(c, '', LN + '; color: #0A7A3D') for c, _ in cells(res)) + f'<td style="{TD}{LN}"></td>'))
    else:
        rows.append(('', ''.join(f'<td style="{TD}{LN}">&nbsp;</td>' for _ in range(L)) + f'<td style="{TD}{LN}"></td>'))
    SC = ' class="st"'
    trs = ''.join(f'<tr{SC if reveal and k in ("mk", "res") else ""}>{r}</tr>' for k, r in rows)
    return (f'<table class="vcol" style="border-collapse: collapse; direction: ltr; unicode-bidi: isolate; display: inline-table; '
            f'font-weight: 800; line-height: 1.12; vertical-align: middle; margin: 0 auto{"; font-size: " + fs if fs else ""}">{trs}</table>')
