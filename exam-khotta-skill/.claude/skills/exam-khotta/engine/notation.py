# الصيغة المختصرة للرياضيات والعلوم والنصوص العربية في ملف الاختبار، وتحويلها إلى HTML (لـ PDF) وإلى Word.
#
#   {٣/٤}  كسر        {١ ٢/٣}  عدد كسري      {س^{٢} + ١/٤}  كسر فيه أي صيغة (التداخل مسموح)
#   ٥^{٢}  أُسّ (يُعرض أعلى يسار الأساس كما في كتب الوزارة)        س_{١}  دليل سفلي
#   √{١٦}  جذر تربيعي        √[٣]{١٢٥}  جذر نوني (العلامة معكوسة كما في الكتاب، والدليل أعلى يمينها)
#   ‾{٣}  خطّ فوق (عشري دوري)      ce{2H2 + O2 -> 2H2O}  معادلة كيميائية      ltr{v = d/t}  نصّ لاتيني
#   quran[2:255] آية تُجلب آلياً، quran[17:23]{جزء} اقتباس يُتحقّق منه      **غامق**   u{تحته خط}   ___ فراغ   \n سطر   \{ قوس حرفي
#
# الأرقام اللاتينية في النص العربي تُحوَّل إلى (٠–٩)، إلا داخل رمز لاتيني (7Ni2، AO1) وداخل ce{} وltr{}.
# الفاصلة العشرية بين رقمين («.» أو «،» بلا مسافة) ← «٫»، و«%» ← «٪»، و« - » ← «−»، و« * » ← «×».
import html as _html
import re

AR = '٠١٢٣٤٥٦٧٨٩'
RLM = '‏'
LRE, PDF_ = '‪', '‬'


def ar(s, digits='ar'):
    s = str(s)
    if digits != 'ar':
        return s
    parts = re.split(r'([A-Za-z][A-Za-z0-9]*|\d+[A-Za-z][A-Za-z0-9]*)', s)
    for i in range(0, len(parts), 2):
        t = re.sub(r'(?<=\d)[.،,](?=\d|‾\{)', '٫', parts[i]).replace('%', '٪')
        parts[i] = t.translate(str.maketrans('0123456789', AR))
    return ''.join(parts)


# ═════════════ التحليل ═════════════
class _P:
    def __init__(self, s, dg):
        self.s, self.i, self.dg = s, 0, dg

    def group(self, open_='{', close='}'):
        """يقرأ المحتوى بين القوسين المتطابقين (المؤشر عند القوس الفاتح) ويعيده نصّاً خاماً."""
        assert self.s[self.i] == open_
        depth, j = 0, self.i
        while j < len(self.s):
            c = self.s[j]
            if c == '\\':
                j += 2; continue
            if c == open_:
                depth += 1
            elif c == close:
                depth -= 1
                if depth == 0:
                    raw = self.s[self.i + 1:j]; self.i = j + 1
                    return raw
            j += 1
        raise ValueError(f'قوس «{open_}» غير مغلق في: {self.s[self.i:self.i + 40]}…')

    def seq(self):
        out, buf = [], []
        def flush():
            if buf:
                out.append(('t', ar(''.join(buf), self.dg))); buf.clear()
        s = self.s
        while self.i < len(s):
            c = s[self.i]
            rest = s[self.i:]
            if c == '\\' and self.i + 1 < len(s):
                buf.append(s[self.i + 1]); self.i += 2; continue
            if rest.startswith('**'):
                j = s.find('**', self.i + 2)
                if j > 0:
                    flush(); out.append(('b', parse(s[self.i + 2:j], self.dg))); self.i = j + 2; continue
            m = re.match(r'_{3,}', rest)
            if m:
                flush(); out.append(('blank',)); self.i += m.end(); continue
            if c == '\n':
                flush(); out.append(('br',)); self.i += 1; continue
            if rest.startswith('^{') or rest.startswith('_{'):
                flush(); self.i += 1
                g = self.group()
                g = re.sub(r'^-(?=\d)', '−', g)   # أسّ سالب: 10^{-3}
                out.append(('sup' if c == '^' else 'sub', parse(g, self.dg))); continue
            if c == '√' and self.i + 1 < len(s) and s[self.i + 1] in '[{':
                flush(); self.i += 1; idx = None
                if s[self.i] == '[':
                    idx = parse(self.group('[', ']'), self.dg)
                out.append(('root', parse(self.group(), self.dg), idx)); continue
            if rest.startswith('‾{'):
                if len(buf) > 1 and buf[-1] in '.،,' and buf[-2].isdigit():
                    buf[-1] = '٫'   # فاصلة عشرية قبل الجزء الدوري
                flush(); self.i += 1; out.append(('ol', parse(self.group(), self.dg))); continue
            if rest.startswith('u{'):   # خطّ تحت الكلمة («أعرب ما تحته خط»)
                flush(); self.i += 1; out.append(('u', parse(self.group(), self.dg))); continue
            m = re.match(r'(ce|ltr|quran)\{', rest)
            if m:
                flush(); self.i += len(m.group(1)); raw = self.group()
                out.append(('ltr', _P(prep(raw), 'latin').seq()) if m.group(1) == 'ltr' else (m.group(1), raw)); continue
            if c == '{':
                flush(); raw = self.group()
                k = _top_slash(raw)
                if k is None:
                    out.append(('grp', parse(raw, self.dg)))
                else:
                    left, right = raw[:k], raw[k + 1:]
                    # عدد كسري فقط إن كان: عدد صحيح، مسافة، بسط عددي ({٢ ١/٣})؛ وإلا فالبسط كله عملية ({٣ + ٥/٢})
                    mm = re.match(r'^\s*([0-9٠-٩]+)\s+([0-9٠-٩]+)\s*$', left)
                    whole = parse(mm.group(1), self.dg) if mm else None
                    num = mm.group(2) if mm else left
                    out.append(('frac', whole, parse(num.strip(), self.dg), parse(right.strip(), self.dg)))
                continue
            buf.append(c); self.i += 1
        flush()
        return out


def _top_slash(raw):
    depth, j = 0, 0
    while j < len(raw):
        c = raw[j]
        if c == '\\':
            j += 2; continue
        if c in '{[':
            depth += 1
        elif c in '}]':
            depth -= 1
        elif c == '/' and depth == 0:
            return j
        j += 1
    return None


def prep(text, dg='ar'):
    text = str(text if text is not None else '')
    text = re.sub(r'(?<=\S) - (?=\S)', ' − ', text).replace(' * ', ' × ')
    return text


def parse(text, dg='ar'):
    ns = _P(prep(text, dg), dg).seq()
    return group_quantities(ns) if dg != 'ar' else ns


# كمية لاتينية: عدد (وسالب) [× 10] [وحدات]، مثل 20 mL، (0.5 cm)، 9.81 m/s، 5 × 10، 100 °C
UNIT = r'(?:°[CF]|[A-Za-zΩμ%][A-Za-z0-9Ωμ/·]*(?:-\d)?)'
QTY = re.compile(r'\(?[−-]?\d+(?:[.,]\d+)?(?:\s*×\s*10(?=$))?(?:\s*×\s*10\b)?(?:\s+' + UNIT + r'|' + UNIT + r'(?=\s|$|\)))*\)?')


ARABIC_RUN = re.compile(r'[ء-غف-يٱ-ۓ][ء-ٰٟ-ۓـ]*'
                        r'(?:[\s،؛]+[ء-غف-يٱ-ۓ][ء-ٰٟ-ۓـ]*)*')
EDGE = re.compile(r'^[\s،؛؟.:!«»"\'–—]*|[\s،؛؟.:!«»"\'–—]*$')


def _trim(tx):
    """يفصل الحواف (مسافات وترقيم) عن لبّ المقطع، ويُخرج قوساً غير مطابق."""
    m1 = re.match(r'^[\s،؛؟.:!«»"\'–—]*', tx); lead = m1.group()
    rest = tx[len(lead):]
    m2 = re.search(r'[\s،؛؟.:!«»"\'–—]*$', rest); trail = m2.group()
    core = rest[:len(rest) - len(trail)]
    changed = True
    while changed and core:   # أقواس غير مطابقة على الحافتين تبقى خارج العزل
        changed = False
        if core[0] in ')]' or (core[0] in '([' and core.count(core[0]) > core.count(')' if core[0] == '(' else ']')):
            lead += core[0]; core = core[1:]; changed = True
        elif core and (core[-1] in '([' or (core[-1] in ')]' and core.count(core[-1]) > core.count('(' if core[-1] == ')' else '['))):
            trail = core[-1] + trail; core = core[:-1]; changed = True
        if changed:
            m1 = re.match(r'^[\s\u060c\u061b\u061f.:!«»"\'–—]*', core); lead += m1.group(); core = core[len(m1.group()):]
            m2 = re.search(r'[\s\u060c\u061b\u061f.:!«»"\'–—]*$', core); trail = m2.group() + trail; core = core[:len(core) - len(m2.group())]
    return lead, core, trail


def _is_formula(core):
    """معادلة برموز لاتينية: قبل أول «=» حرف لاتيني (n(Mg) = …، M: Mg = …، F = ma)."""
    if '=' not in core:
        return False
    return bool(re.search(r'[A-Za-zΑ-Ωα-ω]', core.split('=', 1)[0]))


def _absorb(grp, ns, i, formula):
    """يضمّ إلى المقطع ما يليه مباشرة: أسّاً أو دليلاً (10^{8}) أو كسراً، ثم بقية الوحدات أو المعادلة في النص التالي."""
    while i + 1 < len(ns):
        nx = ns[i + 1]
        if nx[0] in ('sup', 'sub') or (formula and nx[0] in ('frac', 'ce', 'ol')):
            grp.append(nx); i += 1; continue
        if nx[0] == 't':
            t = nx[1]
            if formula:
                m = ARABIC_RUN.search(t)
                pre = t[:m.start()] if m else t
            else:
                mm = re.match(r'(?:\s*' + UNIT + r')+', t)
                pre = mm.group() if mm else ''
            _, core, trail = _trim(pre) if pre else ('', '', '')
            lead_ws = re.match(r'^\s*', pre).group() if pre else ''
            if core and (formula or re.search(r'[A-Za-z°Ωμ]', core)):
                grp.append(('t', lead_ws + core))
                ns[i + 1] = ('t', t[len(lead_ws) + len(core):])
            break
        break
    return i


def group_quantities(ns):
    """وضع الأرقام اللاتينية (العلوم): يحيط بعزلٍ من اليسار لليمين
    ١) كل معادلة طرفها الأيسر رمز لاتيني (n(Mg) = 4.8 g ÷ 24 g/mol) كاملةً،
    ٢) وكل كمية لاتينية (20 mL، (0.5 cm)، 5 × 10^{3}، 9.81 m/s^{2}) داخل الجملة العربية؛
    ويبقى ترتيب المعادلة التي تبدأ بكلمة عربية (المسافة = {300/15} = 20 cm) من اليمين كما في الكتاب."""
    ns = list(ns)
    out = []
    i = 0
    while i < len(ns):
        n = ns[i]
        if n[0] != 't':
            out.append((n[0], group_quantities(n[1])) if n[0] in ('b', 'grp') else n)
            i += 1; continue
        t = n[1]
        pieces, pos = [], 0
        for m in ARABIC_RUN.finditer(t):
            if m.start() > pos:
                pieces.append((False, t[pos:m.start()]))
            pieces.append((True, m.group())); pos = m.end()
        if pos < len(t):
            pieces.append((False, t[pos:]))
        for idx, (is_ar, tx) in enumerate(pieces):
            if is_ar:
                out.append(('t', tx)); continue
            last = idx == len(pieces) - 1
            lead, core, trail = _trim(tx)
            if _is_formula(core):
                grp = [('t', core)]
                if last and not trail:
                    i = _absorb(grp, ns, i, True)
                if lead:
                    out.append(('t', lead))
                out.append(('ltr', grp))
                if trail:
                    out.append(('t', trail))
                continue
            # كميات منفردة
            p2 = 0
            for m in QTY.finditer(tx):
                if not re.search(r'\d', m.group()) or m.start() < p2:
                    continue
                g, st = m.group(), m.start()
                if g.startswith('(') and not g.endswith(')'):
                    g = g[1:]; st += 1
                if g.endswith(')') and not g.startswith('('):
                    g = g[:-1]
                en = st + len(g)
                if st > p2:
                    out.append(('t', tx[p2:st]))
                grp = [('t', g)]
                p2 = en
                if last and en == len(tx):
                    i = _absorb(grp, ns, i, False)
                out.append(('ltr', grp))
            if p2 < len(tx):
                out.append(('t', tx[p2:]))
        i += 1
    return out


def plain_nodes(ns):
    return plain_walk(ns)


def plain(text, dg='ar'):
    return plain_walk(parse(text, dg))


def plain_walk(ns):
    def walk(ns):
        r = []
        for n in ns:
            k = n[0]
            if k == 't':
                r.append(n[1])
            elif k in ('b', 'grp', 'sup', 'sub', 'ol', 'u'):
                r.append(walk(n[1]))
            elif k == 'frac':
                r.append((walk(n[1]) + ' ' if n[1] else '') + walk(n[2]) + '/' + walk(n[3]))
            elif k == 'root':
                r.append('√' + walk(n[1]))
            elif k == 'ltr':
                r.append(walk(n[1]))
            elif k in ('ce', 'quran'):
                r.append(n[1])
        return ''.join(r)
    return walk(ns)


# ═════════════ الكيمياء ═════════════
ARROWS = [('<=>', '⇌'), ('<->', '↔'), ('->', '→'), ('<-', '←')]


def ce_tokens(raw):
    """يحوّل معادلة كيميائية إلى أجزاء [(نص، 'n'|'sub'|'sup')]: الأرقام بعد رمز عنصر أو قوس سفلية، والمعامل في أول
    الصيغة عادي، والشحنة ^{2-} أو ^2- أو ^+ علوية، والأسهم -> و <=> تتحوّل."""
    s = raw
    for a, b in ARROWS:
        s = s.replace(a, b)
    out = []
    i = 0
    prev = ''   # آخر حرف عادي
    while i < len(s):
        c = s[i]
        if c == '^':
            if i + 1 < len(s) and s[i + 1] == '{':
                j = s.index('}', i)
                out.append((s[i + 2:j].replace('-', '−'), 'sup')); i = j + 1
            else:
                m = re.match(r'\^(\d*[+-])', s[i:])
                if m:
                    out.append((m.group(1).replace('-', '−'), 'sup')); i += m.end()
                else:
                    out.append((c, 'n')); i += 1
            prev = ''
            continue
        if c.isdigit() and prev and (prev.isalpha() or prev in ')]'):   # المعامل في أول الصيغة يبقى عادياً
            m = re.match(r'\d+', s[i:])
            out.append((m.group(), 'sub')); i += m.end(); continue
        out.append((c, 'n')); prev = c; i += 1
    # دمج المتجاور من النوع نفسه
    merged = []
    for t, k in out:
        if merged and merged[-1][1] == k:
            merged[-1] = (merged[-1][0] + t, k)
        else:
            merged.append((t, k))
    return merged


# ═════════════ HTML ═════════════
RADICAL_SVG = ('<svg class="rad" viewBox="0 0 10 24" preserveAspectRatio="none" aria-hidden="true">'
               '<path d="M0.6 0.8 L3.6 23 L7.2 13.5 L9.6 15" fill="none" stroke="currentColor" stroke-width="1.5" '
               'vector-effect="non-scaling-stroke" stroke-linejoin="round" stroke-linecap="round"/></svg>')

CSS = '''
.mix { display: inline-flex; align-items: center; gap: .12em; vertical-align: middle; }
.fr { display: inline-flex; flex-direction: column; text-align: center; line-height: 1.12; font-size: .92em; vertical-align: middle; margin: 0 .15em; }
.fr > span:first-child { border-bottom: 1.3px solid currentColor; padding: 0 .2em .05em; }
.fr > span:last-child { padding: .05em .2em 0; }
.rt { display: inline-flex; align-items: stretch; vertical-align: middle; margin: 0 .1em; position: relative; }
.rt .rad { width: .5em; flex: none; margin-top: .02em; overflow: visible; }
.rt .rc { border-top: 1.4px solid currentColor; padding: .06em .15em 0; display: inline-flex; align-items: center; line-height: 1.25; }
.rt .ri { position: absolute; right: -.15em; top: -.2em; font-size: .58em; line-height: 1; }
.rt.hasi { padding-right: .3em; }
.ol { border-top: 1.3px solid currentColor; padding-top: .02em; }
sup.x, sub.x { font-size: .62em; line-height: 0; unicode-bidi: isolate; }
.ce, .ltr { unicode-bidi: isolate; direction: ltr; display: inline-block; font-family: 'Readex Pro', 'DejaVu Sans', sans-serif; }
.ce sub, .ce sup { font-size: .68em; line-height: 0; }
.quran { font-family: 'Amiri Quran', 'Amiri', serif; font-size: 1.12em; line-height: 2.1; }
.blank { display: inline-block; min-width: 26mm; border-bottom: 1.4px dotted #222; height: 1.2em; vertical-align: baseline; }
'''


def to_html(nodes, ltr=False):
    o = []
    for n in nodes:
        k = n[0]
        if k == 't':
            o.append(_html.escape(n[1]))
        elif k == 'b':
            o.append(f'<b>{to_html(n[1], ltr)}</b>')
        elif k == 'u':
            o.append(f'<u>{to_html(n[1], ltr)}</u>')
        elif k == 'grp':
            o.append(to_html(n[1], ltr))
        elif k == 'frac':
            w = f'<span class="whole">{to_html(n[1])}</span>' if n[1] else ''
            o.append(f'<span class="mix">{w}<span class="fr"><span>{to_html(n[2])}</span><span>{to_html(n[3])}</span></span></span>')
        elif k in ('sup', 'sub'):
            o.append(f'{"" if ltr else RLM}<{k} class="x">{to_html(n[1], ltr)}</{k}>')
        elif k == 'root':
            idx = f'<span class="ri">{to_html(n[2])}</span>' if n[2] else ''
            o.append(f'<span class="rt{" hasi" if n[2] else ""}">{idx}{RADICAL_SVG}<span class="rc">{to_html(n[1])}</span></span>')
        elif k == 'ol':
            o.append(f'<span class="ol">{to_html(n[1])}</span>')
        elif k == 'ce':
            parts = ''.join(_html.escape(t) if kk == 'n' else f'<{kk}>{_html.escape(t)}</{kk}>' for t, kk in ce_tokens(n[1]))
            o.append(f'<span class="ce" dir="ltr">{parts}</span>')
        elif k == 'ltr':
            o.append(f'<span class="ltr" dir="ltr">{to_html(n[1], True)}</span>')
        elif k == 'quran':
            o.append(f'<span class="quran">﴿{_html.escape(n[1].strip())}﴾</span>')
        elif k == 'blank':
            o.append('<span class="blank"></span>')
        elif k == 'br':
            o.append('<br>')
    return ''.join(o)


def html(text, dg='ar'):
    return to_html(parse(text, dg))


def needs_image(nodes):
    """هل في الصيغة جذر (لا يمكن عكس علامته في Word)؟"""
    for n in nodes:
        k = n[0]
        if k == 'root':
            return True
        if k in ('b', 'grp', 'sup', 'sub', 'ol', 'ltr') and needs_image(n[1]):
            return True
        if k == 'frac' and any(needs_image(x) for x in n[1:] if x):
            return True
    return False


# ═════════════ Word: معادلات OMML بترتيب العرض ═════════════
# منطقة المعادلة في Word تُكتب من اليسار لليمين دائماً، فنرتّب الرموز بترتيب ظهورها (عكس الترتيب المنطقي للنص العربي)
# مع إبقاء الأعداد والكلمات اللاتينية كما هي، وعكس الأقواس وعلامات المقارنة، ووضع الأسّ قبل أساسه (m:sPre) ليظهر يساره.
MIRROR = str.maketrans('()[]{}<>≤≥«»', ')(][}{><≥≤»«')
TOKEN = re.compile(r'[0-9٠-٩][0-9٠-٩٫,.:]*|[A-Za-z][A-Za-z0-9]*|\s+|.')


def atoms(nodes):
    """قائمة ذرّات بالترتيب المنطقي: ('tok', نص) أو ('node', عقدة) أو ('pre', ذرّة_الأساس، sup، sub)."""
    out = []
    for n in nodes:
        k = n[0]
        if k == 't':
            out += [('tok', t) for t in TOKEN.findall(n[1])]
        elif k in ('grp', 'b', 'u'):
            out += atoms(n[1])
        elif k in ('sup', 'sub'):
            base = out.pop() if out else ('tok', '')
            if base[0] == 'tok' and not base[1].strip():   # مسافة قبل ^ : لا أساس
                out.append(base); base = ('tok', '')
            sup = n[1] if k == 'sup' else None
            sub = n[1] if k == 'sub' else None
            if base[0] == 'pre':   # أسّ ودليل معاً على الأساس نفسه
                _, b0, s0, d0 = base
                out.append(('pre', b0, sup or s0, sub or d0))
            else:
                out.append(('pre', base, sup, sub))
        else:
            out.append(('node', n))
    return out


class OMML:
    def __init__(self, el, mrun):
        self.el, self.mrun = el, mrun   # دوال من docx_writer: إنشاء عنصر، وإنشاء m:r

    def seq(self, nodes):
        """عناصر OMML بترتيب العرض من اليسار لليمين."""
        res = []
        for a in reversed(atoms(nodes)):
            res += self.atom(a)
        return res

    def atom(self, a):
        el = self.el
        if a[0] == 'tok':
            t = a[1]
            if not t:
                return []
            return [self.mrun(t if re.match(r'[0-9٠-٩A-Za-z]', t) else t.translate(MIRROR))]
        if a[0] == 'pre':
            _, base, sup, sub = a
            pre = el('m:sPre')
            s1 = el('m:sub'); [s1.append(x) for x in (self.seq(sub) if sub else [])]
            s2 = el('m:sup'); [s2.append(x) for x in (self.seq(sup) if sup else [])]
            e = el('m:e'); [e.append(x) for x in self.atom(base)]
            pre.append(s1); pre.append(s2); pre.append(e)
            return [pre]
        n = a[1]
        k = n[0]
        if k == 'frac':
            f = el('m:f')
            num = el('m:num'); [num.append(x) for x in self.seq(n[2])]
            den = el('m:den'); [den.append(x) for x in self.seq(n[3])]
            f.append(num); f.append(den)
            # العدد الكسري: الصحيح يمين الكسر ← بعده في ترتيب العرض
            return [f] + (self.seq(n[1]) if n[1] else [])
        if k == 'ol':
            b = el('m:bar'); pr = el('m:barPr'); pr.append(el('m:pos', **{'m:val': 'top'})); b.append(pr)
            e = el('m:e'); [e.append(x) for x in self.seq(n[1])]; b.append(e)
            return [b]
        if k == 'root':   # احتياطي فقط (العلامة غير معكوسة)؛ الأصل صورة
            r = el('m:rad'); pr = el('m:radPr')
            if not n[2]:
                pr.append(el('m:degHide', **{'m:val': 1}))
            r.append(pr)
            d = el('m:deg'); [d.append(x) for x in (self.seq(n[2]) if n[2] else [])]
            e = el('m:e'); [e.append(x) for x in self.seq(n[1])]
            r.append(d); r.append(e)
            return [r]
        if k == 'ltr':
            return [x for a in atoms(n[1]) for x in self.atom(a)]
        if k in ('ce', 'quran'):
            return [self.mrun(n[1])]
        if k == 'blank':
            return [self.mrun(' …… ')]
        return []


# ═════════════ تدقيق الكتابة ═════════════
GREEK_LATIN = re.compile(r'[A-Za-zΑ-Ωα-ωΔΩλμπθ]')


def lint(text, dg='ar'):
    """أخطاء (تمنع البناء) وتنبيهات في كتابة الصيغ. يعيد (أخطاء، تنبيهات)."""
    E, W = [], []
    s = str(text or '')
    try:
        nodes = parse(s, dg)
    except ValueError as e:
        return [str(e)], W
    if re.search(r'\^(?!\{)', s):
        E.append('أسّ بلا قوسين: اكتب ^{٢} لا ^٢')
    if re.search(r'√(?![\[{])', s):
        E.append('جذر بلا قوسين: اكتب √{١٦}')
    def walk(ns, top=True):
        for n in ns:
            k = n[0]
            if k == 't':
                t = n[1]
                if re.search(r'[٠-٩]\s*/\s*[٠-٩]', t):
                    W.append(f'«{t.strip()[:30]}»: كسر مكتوب بشرطة مائلة؛ اكتبه {{٣/٤}} ليظهر كسراً')
                if re.search(r'(?<![A-Za-z])[0-9٠-٩]\s*[xX]\s*[0-9٠-٩]', t):
                    W.append(f'«{t.strip()[:30]}»: استعمل «×» للضرب لا الحرف x')
                if re.search(r'(^|[\s(=])-\s*[0-9٠-٩]', t):
                    W.append(f'«{t.strip()[:30]}»: السالب بعلامة «−» (U+2212) لا الشرطة «-»')
                if dg == 'ar' and GREEK_LATIN.search(t) and re.search(r'[٠-٩]', t) and not re.fullmatch(r'[\s\S]*\b\d*[A-Z][a-z]\d+\b[\s\S]*', t):
                    W.append(f'«{t.strip()[:40]}»: رموز لاتينية أو يونانية مع أرقام عربية في سطر واحد قد يضطرب ترتيبها؛ '
                             'اكتب العبارة كلها ltr{λ = 500 nm} بأرقام لاتينية، أو بالرموز العربية')
            elif k in ('b', 'grp', 'sup', 'sub', 'ol'):
                walk(n[1], False)
            elif k == 'frac':
                for x in n[1:]:
                    if x:
                        walk(x, False)
            elif k == 'root':
                walk(n[1], False)
                if n[2]:
                    walk(n[2], False)
            elif k == 'ce' and re.search(r'[٠-٩]', n[1]):
                E.append(f'ce{{{n[1]}}}: الصيغ الكيميائية بالأرقام اللاتينية (H2O لا H٢O)')
    walk(nodes)
    return E, W
