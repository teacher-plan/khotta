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
        rows.append(('mk', ''.join(f'<td style="{TD}; font-size: .6em; color: #C2410C; vertical-align: bottom">{_ar(m.strip())}</td>' for m in mk) + '<td></td>'))
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

def vmul(a, k, reveal=False, fs=''):
    # ضربٌ رأسي لعددٍ كامل (الأرقام بعد تجاهل الفاصلة) في رقمٍ واحد، والمحمول فوق المنزلة التالية — كما في مثال ٣-٤
    res = str(int(a) * int(k)); L = max(len(a), len(res))
    top = [''] * (L - len(a)) + list(a)
    mk, c = [''] * L, 0
    for j in range(L - 1, -1, -1):
        if not top[j]: break
        c = (int(top[j]) * int(k) + c) // 10
        if c and j > 0 and top[j - 1]: mk[j - 1] = str(c)
    TD = 'padding: 0 .07em; text-align: center; min-width: .6em'
    LN = '; border-top: .07em solid currentColor'
    SC = ' class="st"' if reveal else ''
    rows = []
    if any(mk): rows.append(f'<tr{SC}>' + ''.join(f'<td style="{TD}; font-size: .6em; color: #C2410C; vertical-align: bottom">{_ar(m)}</td>' for m in mk) + '<td></td></tr>')
    rows.append('<tr>' + ''.join(f'<td style="{TD}">{_ar(d)}</td>' for d in top) + '<td></td></tr>')
    rows.append('<tr>' + f'<td style="{TD}"></td>' * (L - 1) + f'<td style="{TD}">{_ar(k)}</td><td style="{TD}; color: #C2410C; padding-inline-start: .25em">×</td></tr>')
    rows.append(f'<tr{SC}>' + ''.join(f'<td style="{TD}{LN}; color: #0A7A3D">{_ar(d)}</td>' for d in [''] * (L - len(res)) + list(res)) + f'<td style="{TD}{LN}"></td></tr>')
    return (f'<table class="vcol" style="border-collapse: collapse; direction: ltr; unicode-bidi: isolate; display: inline-table; '
            f'font-weight: 800; line-height: 1.12; vertical-align: middle; margin: 0 auto{"; font-size: " + fs if fs else ""}">{"".join(rows)}</table>')

def vdiv(a, k, fs='', reveal=False):
    # القسمة المختصرة كما في مثال ٣-٥: المقسوم عليه يساراً، والناتج فوق المقسوم والفاصلة فوق الفاصلة، والباقي صغيرٌ قبل الرقم التالي.
    k = int(k); i, _, d = a.partition('.'); digs = list(i) + list(d); npos = len(i)
    r, qs, car, lead = 0, [], [''] * len(digs), True
    for j, ch in enumerate(digs):
        v = r * 10 + int(ch); q, r = divmod(v, k)
        hide = lead and q == 0 and j < npos - 1
        if hide: qs.append('')
        else: lead = False; qs.append(str(q))
        if r and j + 1 < len(digs) and not hide: car[j + 1] = str(r)
    TD = 'padding: 0 .07em; text-align: center; min-width: .6em'
    def cols(vals, f):
        out = [f(v, j) for j, v in enumerate(vals[:npos])]
        if d: out.append(f'<td style="{TD}; color: #C0262D">٫</td>')
        return out + [f(v, j + npos) for j, v in enumerate(vals[npos:])]
    q = cols(qs, lambda v, j: f'<td style="{TD}; color: #0A7A3D">{_ar(v)}</td>')
    dv = cols(digs, lambda v, j: f'<td style="{TD}; border-top: .07em solid currentColor">'
              + (f'<sup style="font-size: .6em; color: #C2410C; vertical-align: .55em">{_ar(car[j])}</sup>' if car[j] else '') + f'{_ar(v)}</td>')
    if d: dv[npos] = f'<td style="{TD}; border-top: .07em solid currentColor; color: #C0262D">٫</td>'
    SC = ' class="st"' if reveal else ''
    return (f'<table class="vcol" style="border-collapse: collapse; direction: ltr; unicode-bidi: isolate; display: inline-table; '
            f'font-weight: 800; line-height: 1.15; vertical-align: middle; margin: 0 auto{"; font-size: " + fs if fs else ""}">'
            f'<tr{SC}><td></td>{"".join(q)}</tr><tr><td style="{TD}; border-right: .07em solid currentColor; padding-right: .18em">{_ar(k)}</td>{"".join(dv)}</tr></table>')
def dres(a, k):   # ناتج القسمة نصّاً بالأرقام العربية (للتحقّق والإجابات)
    from decimal import Decimal as D_
    return _ar(str(D_(a) / D_(k)))

def valign(rows, fs=''):
    # أعدادٌ مصفوفةٌ عند الفاصلة لنرى انتقال الأرقام بين المنازل: rows = [(العدد بأرقام لاتينية، التسمية يميناً)]؛ لا أصفار مضافة
    I = max(len(x.partition('.')[0]) for x, _ in rows); Dm = max(len(x.partition('.')[2]) for x, _ in rows)
    TD = 'padding: 0 .07em; text-align: center; min-width: .6em'
    out = ''
    for x, lab in rows:
        i, hp, d = x.partition('.')
        cells = [''] * (I - len(i)) + list(i) + ([('.' if hp else '')] if Dm else []) + list(d) + [''] * (Dm - len(d))
        out += '<tr>' + ''.join(f'<td style="{TD}{"; color: #C0262D" if c == "." else ""}">{_ar(c)}</td>' for c in cells) + \
               f'<td style="{TD}; padding-inline-start: .5em; font-size: .55em; color: #C2410C; text-align: left; white-space: nowrap">{lab}</td></tr>'
    return (f'<table class="vcol" style="border-collapse: collapse; direction: ltr; unicode-bidi: isolate; display: inline-table; '
            f'font-weight: 800; line-height: 1.2; vertical-align: middle; margin: 0 auto{"; font-size: " + fs if fs else ""}">{out}</table>')
