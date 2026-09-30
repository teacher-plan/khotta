# يبني مصدر تصميم فيديو الدرس ١-١ «الأعداد الصحيحة» (.dc.html) من قالب فيديو «القوى والجذور»:
# نفس الرأس والأنماط، بمشاهد مضبوطة التوقيت على التعليق (صوت_الأعداد_الصحيحة/durations.json).
# توقيت كل عنصر = موضع عبارته في نصّ السطر × مدّة السطر (at()).
# python3 gen_int_video_dc.py ← python3 gen_powers_video.py فيديو_الأعداد_الصحيحة.dc.html صوت_الأعداد_الصحيحة فيديو_الأعداد_الصحيحة.html
import os, json, re
HERE = os.path.dirname(os.path.abspath(__file__))
T = open(os.path.join(HERE, 'فيديو_القوى_والجذور.dc.html'), encoding='utf-8').read()
DURS = json.load(open(os.path.join(HERE, 'صوت_الأعداد_الصحيحة', 'durations.json')))['durations']
exec(open(os.path.join(HERE, 'narration_int.py'), encoding='utf-8').read())   # LINES

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

SC = []
L = LINES
SC.append(scene(0, f'''<div class="pop" style="animation-delay: .5s; display: flex; gap: 26px; font-size: 90px">{m(e(ng('٣'), PL, bn('٥')), 90)}</div>
<h1 class="fu" style="margin: 0; font-size: 84px; font-weight: 700; animation-delay: {at(0, 'دَرْسُنَا')}s"><span class="hl">الأعداد الصحيحة</span></h1>
<div style="display: flex; gap: 22px; font-size: 34px; font-weight: 700">{''.join(fu(t, at(0, k), 'padding: 8px 22px; border-radius: 16px; background: #EAF1FF; color: #1E6FD9') for t, k in [('الجمع', 'نَجْمَعُهَا'), ('الطرح', 'وَنَطْرَحُهَا'), ('الضرب', 'وَنَضْرِبُهَا'), ('القسمة', 'وَنَقْسِمُهَا')])}</div>''', 34))
NLV = '<div style="display: flex; direction: ltr; width: 1060px; border-top: 5px solid #14305C">' + ''.join(
    f'<span style="flex: 1; display: flex; flex-direction: column; align-items: center"><i style="width: 4px; height: 22px; background: #14305C; margin-top: -13px"></i><b style="font-size: 44px; direction: rtl; color: {"#C7361B" if k < 0 else "#14305C"}">{ng("٠١٢٣٤٥"[-k]) if k < 0 else "٠١٢٣٤٥"[k]}</b></span>' for k in range(-5, 6)) + '</div>'
SC.append(scene(1, f'''{h2('خط الأعداد')}
{fu('أعدادٌ كاملة: <b style="color: #1E6FD9">موجبة</b> و<b style="color: #C7361B">سالبة</b> — والصفر أيضاً', at(1, 'الْأَعْدَادُ'), 'font-size: 34px; font-weight: 700')}
{fu(NLV, at(1, 'عَلَى خَطِّ'))}
<div style="display: flex; gap: 60px; font-size: 32px; font-weight: 700">{fu('تزداد القيمة →', at(1, 'يَمِينًا'), 'color: #1B7A3E')}{fu('← تتناقص القيمة', at(1, 'يَسَارًا'), 'color: #C7361B')}</div>
{fu(m(e(ng('٥'), '<', '٣'), 80), at(1, 'لِذَلِكَ'), cls='pop')}''', 30))
SC.append(scene(2, f'''{h2('الجمع: إشارتان متشابهتان')}
{fu('نجمع، ونضع الإشارة نفسها', at(2, 'نَجْمَعُ'), 'font-size: 36px; font-weight: 700; color: #1B7A3E')}
{fu(m(e(ng('٣'), PL, bn('٨')), 96), at(2, 'سَالِبُ ثَلَاثَةٍ'))}
<div style="{BOX}">{stp('نجمع', e('٣', PL, '٨', EQ, '١١'), at(2, 'زَائِدُ سَالِبِ'))}{stp('الإشارة نفسها', e(ng('٣'), PL, bn('٨'), EQ, ng('١١')), at(2, 'يُسَاوِي'), True)}</div>''', 30))
SC.append(scene(3, f'''{h2('الجمع: إشارتان مختلفتان')}
{fu('نطرح، ونضع إشارة العدد الأكبر', at(3, 'نَطْرَحُ'), 'font-size: 36px; font-weight: 700; color: #C7361B')}
{fu(m(e('٣', PL, bn('٧')), 96), at(3, 'ثَلَاثَةٌ،'))}
<div style="{BOX}">{stp('نطرح', e('٧', MI, '٣', EQ, '٤'), at(3, 'سَبْعَةٌ نَاقِصُ'))}{stp('إشارة الأكبر', e('٣', PL, bn('٧'), EQ, ng('٤')), at(3, 'إِذَنْ'), True)}</div>''', 30))
SC.append(scene(4, f'''{h2('المعكوس الجمعي… والطرح')}
{fu(m(e('٣', PL, bn('٣'), EQ, '٠'), 72), at(4, 'مِثْلَ'))}
{fu('<span class="hl">الطرح = جمع المعكوس الجمعي</span>', at(4, 'وَالطَّرْحُ'), 'font-size: 40px; font-weight: 700')}
<div style="{BOX}">{stp('نطرح −٣', e('٥', MI, bn('٣')), at(4, 'خَمْسَةٌ نَاقِصُ'))}{stp('نجمع ٣', e(EQ, '٥', PL, '٣', EQ, '٨'), at(4, 'تُصْبِحُ'), True)}</div>''', 30))
SC.append(scene(5, f'''{h2('مثالٌ آخر على الطرح')}
{fu(m(e(ng('٥'), MI, '٨'), 96), at(5, 'سَالِبُ خَمْسَةٍ نَاقِصُ'))}
<div style="{BOX}">{stp('معكوس ٨ هو −٨', e(EQ, ng('٥'), PL, bn('٨')), at(5, 'نُحَوِّلُهَا'))}{stp('متشابهتان: نجمع', e(EQ, ng('١٣')), at(5, 'فَالنَّاتِجُ'), True)}</div>''', 30))
PAT = [('٣', '١٥'), ('٢', '١٠'), ('١', '٥'), ('٠', '٠')]
SC.append(scene(6, f'''{h2('الضرب: تابعوا النمط')}
<div style="display: flex; flex-direction: column; gap: 8px; font-size: 52px">{''.join(fu(m(e(x, X, '٥', EQ, r), 52), at(6, k)) for (x, r), k in zip(PAT, ['ثَلَاثَةٌ فِي', 'اثْنَانِ فِي', 'وَيَقِلُّ', 'وَيَقِلُّ']))}
{fu(m(e(ng('١'), X, '٥', EQ, ng('٥')), 52, '; color: #C7361B'), at(6, 'سَالِبِ وَاحِدٍ'), cls='pop')}</div>
{fu('<span class="hl">سالب × موجب = سالب</span>', at(6, 'إِذَنْ'), 'font-size: 40px; font-weight: 700')}''', 24))
SC.append(scene(7, f'''{h2('قاعدة الإشارات في الضرب والقسمة')}
<div style="display: flex; gap: 40px">{card('<div style="font-size: 32px; font-weight: 700">متشابهتان ← موجب</div>' + m(e(ng('٨'), X, bn('٥'), EQ, '٤٠'), 50), at(7, 'مُتَشَابِهَتَانِ'), True)}
{card('<div style="font-size: 32px; font-weight: 700">مختلفتان ← سالب</div>' + m(e('١٢', X, bn('٣'), EQ, ng('٣٦')), 50), at(7, 'مُخْتَلِفَتَانِ'), False)}</div>
{fu('والقاعدة نفسها للقسمة: ' + m(e(ng('٢٤'), DV, bn('٦'), EQ, '٤'), 40), at(7, 'وَالْقَاعِدَةُ نَفْسُهَا'), 'font-size: 34px; font-weight: 700; display: flex; align-items: center; gap: 16px')}''', 32))
SC.append(scene(8, f'''{h2('انتبهوا: لا تخلطوا القواعد!', 0, '#8E2A18')}
<div style="display: flex; gap: 40px">{card('<div style="font-size: 32px; font-weight: 700">جمع</div>' + m(e(ng('٣'), PL, bn('٥'), EQ, ng('٨')), 54), at(8, 'زَائِدُ'), True, '; color: #1B7A3E')}
{card('<div style="font-size: 32px; font-weight: 700">ضرب</div>' + m(e(ng('٣'), X, bn('٥'), EQ, '١٥'), 54), at(8, 'أَمَّا'), True)}</div>
{fu('<span class="hl">«سالب × سالب = موجب» للضرب والقسمة فقط</span>', at(8, 'هَذِهِ الْقَاعِدَةُ'), 'font-size: 34px; font-weight: 700')}''', 34))
SC.append(scene(9, f'''<h2 class="pop" style="margin: 0; font-size: 58px"><span class="hl">تذكّروا</span></h2>
<div style="display: flex; gap: 26px">{''.join(fu(f'<b style="font-size: 38px; color: {c}">{t}</b><span style="font-size: 28px">{s}</span>', at(9, k), f'display: flex; flex-direction: column; gap: 10px; align-items: center; padding: 20px 28px; border-radius: 22px; background: #FFFFFF; border: 3px solid {c}; min-width: 280px')
  for t, s, c, k in [('الجمع', 'انظر إلى الإشارتين', '#1B7A3E', 'فِي الْجَمْعِ'), ('الطرح', 'جمع المعكوس', '#C7361B', 'وَالطَّرْحُ'), ('الضرب والقسمة', 'متشابهتان: موجب<br>مختلفتان: سالب', '#7A3FD1', 'وَفِي الضَّرْبِ')])}</div>
{fu('كتاب النشاط ص ١٣ و ١٤ · راجعوا ورقة الملخّص', at(9, 'حُلُّوا'), 'font-size: 30px; color: #3B5480')}''', 34))

a = T.index('<sc-if value="{{s0}}"'); z = T.index('\n</div>\n\n<div style="height: 88px')
out = T[:a] + ''.join(SC) + T[z:]
N = len(DURS)
out = out.replace('الدرس ١-٦: القوى والجذور', 'الدرس ١-١: الأعداد الصحيحة').replace('<title>فيديو القوى والجذور</title>', '<title>فيديو الأعداد الصحيحة</title>')
out = re.sub(r'const DURS = \[[^\]]*\]', 'const DURS = ' + json.dumps(DURS), out)
out = out.replace('hint-placeholder-count="9"', f'hint-placeholder-count="{N}"').replace('const N = 9,', 'const N = DURS.length,')
out = out.replace('this.state.scene < 8', 'this.state.scene < DURS.length - 1').replace('Math.min(8, i)', 'Math.min(DURS.length - 1, i)').replace('s === 8 &&', 's === DURS.length - 1 &&')
out = out.replace('@media (prefers-reduced-motion', '''.lab{flex:none;font-size:26px;font-weight:700;color:#1E6FD9;background:#EAF1FF;border-radius:12px;padding:4px 16px;min-width:170px}
.lab.fin{background:#1B7A3E;color:#FFFFFF}
.ngv{display:inline-flex;direction:rtl;unicode-bidi:isolate}.ngv i{font-style:normal}
.brv{display:inline-flex;gap:.12em;direction:rtl;unicode-bidi:isolate}
@media (prefers-reduced-motion''', 1)
p = os.path.join(HERE, 'فيديو_الأعداد_الصحيحة.dc.html'); open(p, 'w', encoding='utf-8').write(out); print(p, N, 'مشاهد')
