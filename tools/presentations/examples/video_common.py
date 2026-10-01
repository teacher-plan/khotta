# أدوات مشتركة لمشاهد فيديو الدروس (.dc.html) — تُنفَّذ بعد تعريف: AUD (مجلد الصوت) و NARR (ملف LINES).
# الاستخدام في مولّد الدرس: exec(open('video_common.py').read()) ثم SC.append(scene(…)) ثم finalize(SC, 'الدرس ١-٢: المضاعفات', 'المضاعفات', 'فيديو_المضاعفات.dc.html')
import os, json, re
HERE = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else os.getcwd()
T = open(os.path.join(HERE, 'فيديو_القوى_والجذور.dc.html'), encoding='utf-8').read()
DURS = json.load(open(os.path.join(HERE, AUD, 'durations.json')))['durations']
exec(open(os.path.join(HERE, NARR), encoding='utf-8').read())   # LINES
def at(i, phrase, lead=.3):  # متى تُقال العبارة في السطر i (تقريباً بنسبة موضعها في النص)
    k = LINES[i].index(phrase)
    return round(max(0, DURS[i] * k / len(LINES[i]) - lead), 1)
def m(t, size=64, extra=''): return f'<span class="m" style="font-size: {size}px{extra}">{t}</span>'
def fu(inner, d, style='', cls='fu'): return f'<div class="{cls}" style="animation-delay: {d}s; {style}">{inner}</div>'
def stp(lab, expr, d, fin=False):
    return fu(f'<span class="lab{" fin" if fin else ""}">{lab}</span>{m(expr, 54)}', d, 'display: flex; align-items: center; justify-content: space-between; gap: 24px')
def h2(t, d=0, color='#14305C'): return f'<h2 class="fu" style="margin: 0; font-size: 54px; color: {color}; animation-delay: {d}s">{t}</h2>'
def scene(i, inner, gap=28):
    return (f'<sc-if value="{{{{s{i}}}}}" hint-placeholder-val="{{{{ {"true" if i == 0 else "false"} }}}}">\n'
            f'<div style="display: flex; flex-direction: column; align-items: center; gap: {gap}px; text-align: center">\n{inner}\n</div>\n</sc-if>\n')
def card(inner, d, ok, extra=''):
    c, bg = ('#1B7A3E', '#E3F6EA') if ok else ('#B3261E', '#FDE7E3')
    return fu(inner, d, f'display: flex; flex-direction: column; align-items: center; gap: 12px; padding: 22px 36px; border-radius: 24px; background: {bg}; border: 3px solid {c}; color: {c}{extra}')
X = '<span class="x">×</span>'; DV = '<span class="x">÷</span>'; PL = '<span class="x">+</span>'; MI = '<span class="x">−</span>'; EQ = '<span class="x">=</span>'
def e(*p): return ' '.join(p)
def ng(v): return f'<span class="ngv"><i>−</i>{v}</span>'                 # السالب: الإشارة يمين العدد
def bn(v): return f'<span class="brv">({ng(v)})</span>'                  # (−٣)
BOX = 'display: flex; flex-direction: column; gap: 18px; align-items: stretch; padding: 24px 40px; border-radius: 24px; background: #FFFFFF; border: 2px solid #C9D6E8'


def finalize(SC, header, short, outname):
    a = T.index('<sc-if value="{{s0}}"'); z = T.index('\n</div>\n\n<div style="height: 88px')
    out = T[:a] + ''.join(SC) + T[z:]
    N = len(DURS)
    u = re.search(r'الدرس ([١-٩])-', header)   # الوحدة من رقم الدرس (القالب مكتوبٌ للوحدة الأولى)
    if u: out = out.replace('الصف السابع · الوحدة الأولى', 'الصف السابع · الوحدة ' + 'الأولى الثانية الثالثة الرابعة الخامسة السادسة السابعة الثامنة التاسعة'.split()['١٢٣٤٥٦٧٨٩'.index(u[1])])
    out = out.replace('الدرس ١-٦: القوى والجذور', header).replace('<title>فيديو القوى والجذور</title>', f'<title>فيديو {short}</title>')
    out = re.sub(r'const DURS = \[[^\]]*\]', 'const DURS = ' + json.dumps(DURS), out)
    out = out.replace('hint-placeholder-count="9"', f'hint-placeholder-count="{N}"').replace('const N = 9,', 'const N = DURS.length,')
    out = out.replace('this.state.scene < 8', 'this.state.scene < DURS.length - 1').replace('Math.min(8, i)', 'Math.min(DURS.length - 1, i)').replace('s === 8 &&', 's === DURS.length - 1 &&')
    out = out.replace('@media (prefers-reduced-motion', '''.lab{flex:none;font-size:26px;font-weight:700;color:#1E6FD9;background:#EAF1FF;border-radius:12px;padding:4px 16px;min-width:170px}
    .lab.fin{background:#1B7A3E;color:#FFFFFF}
    .ngv{display:inline-flex;direction:rtl;unicode-bidi:isolate}.ngv i{font-style:normal}
    .brv{display:inline-flex;gap:.12em;direction:rtl;unicode-bidi:isolate}
    @media (prefers-reduced-motion''', 1)
    p = os.path.join(HERE, outname); open(p, 'w', encoding='utf-8').write(out); print(p, N, 'مشاهد')
