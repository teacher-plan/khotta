# يبني مصدر تصميم فيديو الدرس ١-٧ «ترتيب العمليات الحسابية» (.dc.html) من قالب فيديو «القوى والجذور»:
# نفس الرأس والأنماط وشريط التحكّم، بمشاهد جديدة مضبوطة التوقيت على التعليق (صوت_ترتيب_العمليات/durations.json).
# python3 gen_order_video_dc.py ← python3 gen_powers_video.py فيديو_ترتيب_العمليات.dc.html صوت_ترتيب_العمليات فيديو_ترتيب_العمليات.html
import os, json, re
HERE = os.path.dirname(os.path.abspath(__file__))
T = open(os.path.join(HERE, 'فيديو_القوى_والجذور.dc.html'), encoding='utf-8').read()
DURS = json.load(open(os.path.join(HERE, 'صوت_ترتيب_العمليات', 'durations.json')))['durations']

def b(base, e): return f'<span class="b">{base}<sup>{e}</sup></span>'
def nw(t): return f'<span class="nw">{t}</span>'                       # العملية التي ننفّذها الآن
def m(t, size=64, extra=''): return f'<span class="m" style="font-size: {size}px{extra}">{t}</span>'
def fu(inner, d, style='', cls='fu'): return f'<div class="{cls}" style="animation-delay: {d}s; {style}">{inner}</div>'
def stp(lab, expr, d, fin=False):
    return fu(f'<span class="lab{" fin" if fin else ""}">{lab}</span>{m(expr, 50)}', d, 'display: flex; align-items: center; gap: 24px')
def h2(t, d=0, color='#14305C'): return f'<h2 class="fu" style="margin: 0; font-size: 50px; color: {color}; animation-delay: {d}s">{t}</h2>'
def scene(i, inner, gap=28):
    return (f'<sc-if value="{{{{s{i}}}}}" hint-placeholder-val="{{{{ {"true" if i == 0 else "false"} }}}}">\n'
            f'<div style="display: flex; flex-direction: column; align-items: center; gap: {gap}px; text-align: center">\n{inner}\n</div>\n</sc-if>\n')
def card(inner, d, ok):
    c, bg = ('#1B7A3E', '#E3F6EA') if ok else ('#B3261E', '#FDE7E3')
    return fu(inner, d, f'display: flex; flex-direction: column; align-items: center; gap: 12px; padding: 22px 36px; border-radius: 24px; background: {bg}; border: 3px solid {c}; color: {c}')
X = '<span class="x">×</span>'; DV = '<span class="x">÷</span>'; PL = '<span class="x">+</span>'; MI = '<span class="x">−</span>'; EQ = '<span class="x">=</span>'
def e(*p): return ' '.join(p)
ORD = [('١', 'الأقواس ( )', '#2563EB'), ('٢', 'الأسس والجذور', '#C7361B'), ('٣', 'الضرب والقسمة', '#7A3FD1'), ('٤', 'الجمع والطرح', '#1B7A3E')]
def ordrows(delays, size=34):
    return ''.join(fu(f'<b style="width: 52px; height: 52px; border-radius: 26px; background: {c}; color: #FFFFFF; display: flex; align-items: center; justify-content: center">{n}</b><span>{t}</span>', d,
        f'display: flex; align-items: center; gap: 18px; padding: 8px 22px; border: 3px solid {c}; border-radius: 18px; background: #FFFFFF; font-size: {size}px; font-weight: 700; min-width: 420px') for (n, t, c), d in zip(ORD, delays))
MAN = '''<svg width="200" height="272" viewBox="0 0 220 300" fill="none" stroke-width="8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
<circle cx="110" cy="52" r="40" stroke="#2563EB"></circle><text x="110" y="64" fill="#2563EB" stroke="none" font-size="34" font-weight="700" text-anchor="middle">( )</text>
<path d="M92 104 L110 92 L128 104" stroke="#C7361B"></path>
<line x1="110" y1="92" x2="110" y2="205" stroke="#14305C"></line>
<line x1="40" y1="150" x2="180" y2="150" stroke="#7A3FD1"></line><text x="24" y="162" fill="#7A3FD1" stroke="none" font-size="34" text-anchor="middle">÷</text><text x="196" y="162" fill="#7A3FD1" stroke="none" font-size="34" text-anchor="middle">×</text>
<line x1="110" y1="205" x2="60" y2="270" stroke="#1B7A3E"></line><line x1="110" y1="205" x2="160" y2="270" stroke="#1B7A3E"></line>
<text x="46" y="298" fill="#1B7A3E" stroke="none" font-size="34" text-anchor="middle">−</text><text x="174" y="298" fill="#1B7A3E" stroke="none" font-size="34" text-anchor="middle">+</text></svg>'''

SC = []
SC.append(scene(0, f'''<div class="pop" style="animation-delay: 3.5s; font-size: 110px">{m(e('٢',PL,'٧',X,'٥',EQ,'<span style="color: #C7361B">؟</span>'), 110)}</div>
<h1 class="fu" style="margin: 0; font-size: 80px; font-weight: 700; animation-delay: 11s"><span class="hl">ترتيب العمليات الحسابية</span></h1>
<p class="fu" style="margin: 0; font-size: 30px; color: #3B5480; animation-delay: 12.5s">الدرس ١-٧ · كتاب الطالب ص ٣٥</p>''', 36))
SC.append(scene(1, f'''{h2('مسألةٌ واحدة… وجوابان؟')}
{fu(m(e(b('٦','٢'),PL,'٨',DV,'٢'), 96), 1.5)}
<div style="display: flex; gap: 40px">{card('<div style="font-size: 30px; font-weight: 700">سناء</div>' + m('٢٢', 72), 8.5, False)}{card('<div style="font-size: 30px; font-weight: 700">خديجة</div>' + m('٤٠', 72), 12, True)}</div>
{fu('<span class="hl">مَن منهما على صواب؟</span>', 16.5, 'font-size: 34px; font-weight: 700')}''', 32))
SC.append(scene(2, f'''{h2('ترتيب العمليات الحسابية')}
<div style="display: flex; align-items: center; gap: 60px"><div style="display: flex; flex-direction: column; gap: 14px">{ordrows([8.5, 10.5, 12.5, 14.5])}</div>
{fu(MAN + '<div style="font-size: 24px; color: #3B5480">من الرأس إلى القدمين</div>', 21, 'display: flex; flex-direction: column; align-items: center; gap: 8px', 'pop')}</div>
{fu('المتساوية في الأولوية: <b>من اليمين إلى اليسار</b>', 16.5, 'font-size: 30px; padding: 10px 28px; border-radius: 40px; background: #FFF4D6; border: 2px solid #F2C94C')}''', 24))
SC.append(scene(3, f'''{h2('مثال (أ)')}
{fu(m(e('٣',PL,'٤',X,'٥'), 96), .5)}
<div style="display: flex; flex-direction: column; gap: 22px; align-items: stretch; padding: 26px 40px; border-radius: 24px; background: #FFFFFF; border: 2px solid #C9D6E8">
{stp('الضرب أولاً', e('٣',PL,nw(e('٤',X,'٥')),EQ,'٣',PL,'٢٠'), 5.5)}{stp('ثم الجمع', e(nw(e('٣',PL,'٢٠')),EQ,'٢٣'), 10.5, True)}</div>''', 30))
SC.append(scene(4, f'''{h2('مثال (ج): مسألةٌ أطول')}
{fu(m(e(b('٣','٢'),X,'٥',MI,'(١٩ − ٨)'), 80), .5)}
<div style="display: flex; flex-direction: column; gap: 16px; align-items: stretch; padding: 22px 40px; border-radius: 24px; background: #FFFFFF; border: 2px solid #C9D6E8">
{stp('الأقواس', e(b('٣','٢'),X,'٥',MI,nw('(١٩ − ٨)'),EQ,b('٣','٢'),X,'٥',MI,'١١'), 11)}
{stp('الأسس', e(EQ,nw(b('٣','٢')),X,'٥',MI,'١١',EQ,'٩',X,'٥',MI,'١١'), 15.5)}
{stp('الضرب', e(EQ,nw(e('٩',X,'٥')),MI,'١١',EQ,'٤٥',MI,'١١'), 20.5)}
{stp('الطرح', e(EQ,nw(e('٤٥',MI,'١١')),EQ,'٣٤'), 26.5, True)}</div>''', 22))
SC.append(scene(5, f'''{h2('توقّفوا: خطأٌ شائع!', 0, '#8E2A18')}
{fu(m(e('١٢',MI,'٤',X,'٣'), 88), 3.5)}
<div style="display: flex; gap: 40px">{card('<div style="font-size: 26px; font-weight: 700">✘ طرحنا أولاً</div>' + m(e(nw(e('١٢',MI,'٤')),X,'٣',EQ,'٨',X,'٣',EQ,'٢٤'), 44), 8.5, False)}
{card('<div style="font-size: 26px; font-weight: 700">✔ الضرب أولاً</div>' + m(e('١٢',MI,nw(e('٤',X,'٣')),EQ,'١٢',MI,'١٢',EQ,'٠'), 44), 15.5, True)}</div>
{fu('<span class="hl">اقرؤوا المسألة كاملةً قبل أن تبدؤوا</span>', 24, 'font-size: 34px; font-weight: 700')}''', 32))
SC.append(scene(6, f'''{h2('سناء أم خديجة؟')}
{fu(m(e(b('٦','٢'),PL,'٨',DV,'٢'), 80), .5)}
<div style="display: flex; flex-direction: column; gap: 16px; align-items: stretch; padding: 22px 40px; border-radius: 24px; background: #FFFFFF; border: 2px solid #C9D6E8">
{stp('الأسس', e(EQ,nw(b('٦','٢')),PL,'٨',DV,'٢',EQ,'٣٦',PL,'٨',DV,'٢'), 3.5)}{stp('القسمة', e(EQ,'٣٦',PL,nw(e('٨',DV,'٢')),EQ,'٣٦',PL,'٤'), 7.5)}{stp('الجمع', e(EQ,'٤٠'), 11, True)}</div>
{fu('✔ خديجة على صواب — وسناء جمعت قبل القسمة', 13, 'font-size: 32px; font-weight: 700; color: #1B7A3E', 'pop')}''', 26))
SC.append(scene(7, f'''{h2('عملياتٌ متساوية: من اليمين إلى اليسار')}
{fu(m(e('٢٠',MI,'٧',MI,'٢'), 88), 2.5)}
<div style="display: flex; gap: 40px">{card('<div style="font-size: 26px; font-weight: 700; color: #14305C">بدون أقواس</div>' + m(e(nw(e('٢٠',MI,'٧')),MI,'٢',EQ,'١٣',MI,'٢',EQ,'١١'), 48, '; color: #14305C'), 6.5, True)}
{card('<div style="font-size: 26px; font-weight: 700">بالأقواس</div>' + m(e('٢٠',MI,nw('(٧ − ٢)'),EQ,'٢٠',MI,'٥',EQ,'١٥'), 48), 15.5, True)}</div>
{fu('<span class="hl">الأقواس تغيّر الناتج!</span>', 21, 'font-size: 34px; font-weight: 700')}''', 32))
SC.append(scene(8, f'''{h2('ضع الأقواس ليكون الناتج صحيحاً')}
<div style="display: flex; gap: 40px">
<div style="display: flex; flex-direction: column; gap: 18px; align-items: center">{fu(m(e('٣',X,'٢',PL,'١',EQ,'٩'), 60), 5)}{fu(m(e('٣',X,nw('(٢ + ١)'),EQ,'٣',X,'٣',EQ,'٩'), 54, '; color: #1B7A3E'), 10, cls='pop')}</div>
<div style="display: flex; flex-direction: column; gap: 18px; align-items: center">{fu(m(e('٥',PL,b('٢','٢'),EQ,'٤٩'), 60), 16.5)}{fu(m(e(nw(b('(٥ + ٢)','٢')),EQ,b('٧','٢'),EQ,'٤٩'), 54, '; color: #1B7A3E'), 22, cls='pop')}</div></div>
{fu('حدِّد ما يجب أن يحدث أولاً… ثم تأكّد بالحساب', 26, 'font-size: 30px; color: #3B5480')}''', 44))
SC.append(scene(9, f'''<h2 class="pop" style="margin: 0; font-size: 64px"><span class="hl">تذكّروا الترتيب دائماً</span></h2>
<div style="display: flex; flex-direction: column; gap: 12px">{ordrows([1, 2.5, 4, 5.5], 30)}</div>
{fu('راجعوا ورقة الملخّص · كتاب النشاط ص ٢٥', 9.5, 'font-size: 28px; color: #3B5480')}''', 24))

a = T.index('<sc-if value="{{s0}}"'); z = T.index('\n</div>\n\n<div style="height: 88px')
out = T[:a] + ''.join(SC) + T[z:]
N = len(DURS)
out = out.replace('الدرس ١-٦: القوى والجذور', 'الدرس ١-٧: ترتيب العمليات الحسابية').replace('<title>فيديو القوى والجذور</title>', '<title>فيديو ترتيب العمليات</title>')
out = re.sub(r'const DURS = \[[^\]]*\]', 'const DURS = ' + json.dumps(DURS), out)
out = out.replace('hint-placeholder-count="9"', f'hint-placeholder-count="{N}"').replace('const N = 9,', 'const N = DURS.length,')
out = out.replace('this.state.scene < 8', 'this.state.scene < DURS.length - 1').replace('Math.min(8, i)', 'Math.min(DURS.length - 1, i)').replace('s === 8 &&', 's === DURS.length - 1 &&')
out = out.replace("audioSrc: 'audio/powers_'", "audioSrc: 'audio/powers_'")  # أسماء ملفات الصوت نفسها: powers_01.mp3 …
out = out.replace('@media (prefers-reduced-motion', '''.nw{display:inline-flex;gap:.25em;border-bottom:5px solid #C7361B;padding-bottom:2px}
.lab{flex:none;font-size:24px;font-weight:700;color:#1E6FD9;background:#EAF1FF;border-radius:12px;padding:4px 16px;min-width:150px}
.lab.fin{background:#1B7A3E;color:#FFFFFF}
@media (prefers-reduced-motion''', 1)
p = os.path.join(HERE, 'فيديو_ترتيب_العمليات.dc.html'); open(p, 'w', encoding='utf-8').write(out); print(p, N, 'مشاهد')
