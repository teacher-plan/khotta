# بانٍ عامّ لفيديو الدرس من بيانات المشاهد (من الوحدة الثانية): كل مشهد = (العنوان، القاعدة أو السطر الفرعي، جملة البداية، [(التسمية، التعبير، الجملة المنطوقة، نهائي؟)…]).
# المشهد بلا خطوات = بطاقة عنوان (يُعرض فيها السطر الفرعي).
# في مولّد الدرس: D = [...] ثم exec(open('lesson_video.py').read()) ثم run(D, 'الأسس', 'الدرس ٢-١: …', 'كتابة العبارات الجبرية')
#   python3 gen_X_video_dc.py narr   ← narration_<key>.py ، ثم الصوت (VOICE_RATE افتراضياً +١٠٪)، ثم python3 gen_X_video_dc.py ، ثم gen_powers_video.py
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else os.getcwd()
X = '<span class="x">×</span>'; DV = '<span class="x">÷</span>'; PL = '<span class="x">+</span>'; MI = '<span class="x">−</span>'; EQ = '<span class="x">=</span>'
ARR = '<span class="x">←</span>'
import re as _re
def SEP(t):  # متغيّران متجاوران (سص) يُفصلان بفاصلٍ يمنع الاتصال وفجوةٍ صغيرة — VIDEO.md ٣ (للحدود داخل نصّ القاعدة أو التسمية)
    return _re.sub(r'(?<=[\u0621-\u064A\u0640])(?=[\u0621-\u063F\u0641-\u064A])', '\u200c<i style="display: inline-block; width: .1em"></i>', t)
def V(t): return f'<b style="color: #C2410C">{SEP(t)}</b>'
def FR(n, d): return (f'<span style="display: inline-flex; flex-direction: column; align-items: center; line-height: 1.05; vertical-align: middle">'
                      f'<span style="border-bottom: .07em solid currentColor; padding: 0 .15em .04em; align-self: stretch; text-align: center">{n}</span><span>{d}</span></span>')
def G(*p): return '<span style="display: inline-flex; gap: .2em; direction: rtl; unicode-bidi: isolate">(' + ' '.join(p) + ')</span>'
def e(*p): return ' '.join(p)

def run(D, key, header, short):
    lines = [' '.join([intro] + [s[2] for s in steps]) for _, _, intro, steps in D]
    narr = f'narration_{key}.py'
    if len(sys.argv) > 1 and sys.argv[1] == 'narr':
        open(os.path.join(HERE, narr), 'w', encoding='utf-8').write(f'# نصّ التعليق الصوتي لفيديو «{short}» — مولَّد من بيانات المشاهد (لا تعدّله يدوياً).\nLINES = [\n' + ''.join(f' {l!r},\n' for l in lines) + ']\n')
        print(narr, len(lines), 'سطراً', sum(len(l) for l in lines), 'حرفاً'); sys.exit()
    g = globals(); g['AUD'], g['NARR'] = f'صوت_{key}', narr
    exec(open(os.path.join(HERE, 'video_common.py'), encoding='utf-8').read(), g)
    fu, m, at, scene, h2, BOX, finalize = (g[k] for k in ('fu', 'm', 'at', 'scene', 'h2', 'BOX', 'finalize'))
    RULE = 'font-size: 30px; font-weight: 700; color: #123A6B; background: #EEF4FD; border: 2px solid #9BBBE8; border-inline-start: 10px solid #1E5FB8; border-radius: 16px; padding: 12px 26px; max-width: 1500px; line-height: 1.6'
    def row(lab, expr, d, fin):
        return fu(f'<span class="lab{" fin" if fin else ""}">{lab}</span>{m(expr, 50)}', d, 'display: flex; align-items: center; justify-content: space-between; gap: 28px')
    SC = []
    for i, (title, rule, intro, steps) in enumerate(D):
        if not steps:
            SC.append(scene(i, f'''<h1 class="pop" style="margin: 0; font-size: {84 if i == 0 else 70}px; font-weight: 700"><span class="hl">{title}</span></h1>
{fu(rule, 1.2, 'font-size: 38px; font-weight: 700; color: #3B5480; max-width: 1400px; line-height: 1.6') if rule else ''}''', 34))
            continue
        rows = ''.join(row(lab, ex, at(i, seg), fin) for lab, ex, seg, fin in steps)
        SC.append(scene(i, f'''{h2(title)}
{fu('📌 ' + rule, .6, RULE) if rule else ''}
<div style="{BOX}; min-width: 1100px">{rows}</div>''', 22))
    finalize(SC, header, short, f'فيديو_{key}.dc.html')
