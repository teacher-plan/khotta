# يبني مصدر تصميم فيديو الدرس ١-٥ «الأسس» (.dc.html) — التوقيت من صوت_الأسس.
# python3 gen_index_video_dc.py ← python3 gen_powers_video.py فيديو_الأسس.dc.html صوت_الأسس فيديو_الأسس.html
import os
AUD, NARR = 'صوت_الأسس', 'narration_index.py'
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'video_common.py'), encoding='utf-8').read())

AR = str.maketrans('0123456789', '٠١٢٣٤٥٦٧٨٩')
def ar(n): return str(n).translate(AR)
def P(b, x=None): return f'<span class="b">{ar(b)}' + (f'<sup>{ar(x)}</sup>' if x else '') + '</span>'
def pill(t, d, c='#1E6FD9', bg='#EAF1FF'): return fu(t, d, f'font-size: 34px; font-weight: 700; padding: 10px 26px; border-radius: 18px; background: {bg}; color: {c}')
def tcard(t, s, d, c='#1E6FD9'): return fu(f'<b style="font-size: 40px; color: {c}">{t}</b><span style="font-size: 30px; font-weight: 700">{s}</span>', d, f'display: flex; flex-direction: column; gap: 10px; align-items: center; padding: 20px 30px; border-radius: 22px; background: #FFFFFF; border: 3px solid {c}; min-width: 300px')

def tree(t, times, h=420):
    """شجرة عوامل SVG؛ times[d] زمن ظهور المستوى d."""
    U, V, items, leaves = 110, 120, [], [0]
    def lay(n, d):
        if isinstance(n, tuple):
            xl, xr = lay(n[1], d + 1), lay(n[2], d + 1); x = (xl + xr) / 2
            items.append(('n', n[0], x, d)); items.append(('l', x, d, xl)); items.append(('l', x, d, xr)); return x
        x = leaves[0] * U + U / 2; leaves[0] += 1; items.append(('p', n, x, d)); return x
    lay(t, 0)
    D = max(i[3] for i in items if i[0] != 'l') + 1
    def g(d, inner): return f'<g style="opacity: 0; animation: fu .7s forwards; animation-delay: {times[min(d, len(times) - 1)]}s">{inner}</g>'
    out = [g(d + 1, f'<line x1="{x}" y1="{d * V + 78}" x2="{xc}" y2="{(d + 1) * V + 20}" stroke="#4A5E80" stroke-width="5" stroke-linecap="round"/>') for k, x, d, xc in items if k == 'l']
    for k, n, x, d in (i for i in items if i[0] != 'l'):
        y = d * V + 60
        c = f'<circle cx="{x}" cy="{y - 4}" r="40" fill="#FFF1D6" stroke="#C7361B" stroke-width="5"/>' if k == 'p' else ''
        out.append(g(d, c + f'<text x="{x}" y="{y + 14}" text-anchor="middle" font-size="52" font-weight="900" fill="#14305C">{ar(n)}</text>'))
    W = leaves[0] * U
    return f'<svg viewBox="0 0 {W} {D * V}" style="height: {h}px; width: auto">{"".join(out)}</svg>'

SC = []
SC.append(scene(0, f'''<div class="pop" style="animation-delay: .5s">{m(e(P(2, 3), '=', '٢ × ٢ × ٢'), 84)}</div>
<h1 class="fu" style="margin: 0; font-size: 84px; font-weight: 700; animation-delay: {at(0, 'دَرْسُنَا')}s"><span class="hl">الأسس</span></h1>
<div style="display: flex; gap: 22px">{pill('شجرة العوامل', at(0, 'سَنَرْسُمُ'))}{pill('الأسس', at(0, 'وَنَكْتُبُ'))}{pill('م م ص و ع م ك', at(0, 'وَنَجِدُ'))}</div>''', 34))
SC.append(scene(1, f'''{h2('كل عددٍ غير أولي = ناتج ضرب أعدادٍ أولية')}
{fu(m(e('٨٤', '=', '٢', '×', '٢', '×', '٣', '×', '٧'), 90), at(1, 'مِثْلُ'), cls='pop')}''', 40))
t2 = [at(2, 'لِنَرْسُمْ'), at(2, 'نَرْسُمُ فَرْعَيْنِ'), at(2, 'ثُمَّ عَشَرَةٌ'), at(2, 'وَأَرْبَعَةٌ تُسَاوِي')]
SC.append(scene(2, f'''{h2('شجرة العوامل للعدد ١٢٠')}
{tree((120, (10, 5, 2), (12, (4, 2, 2), 3)), t2, 460)}''', 20))
SC.append(scene(3, f'''{h2('نضرب نهايات الفروع')}
<div style="display: flex; gap: 60px; align-items: center">{tree((120, (60, (30, (6, 3, 2), 5), 2), 2), [at(3, 'وَمَهْمَا')] * 5, 400)}
{fu(m(e('١٢٠', '=', '٢', '×', '٢', '×', '٢', '×', '٣', '×', '٥'), 60), at(3, 'نَضْرِبُ'))}</div>
{fu('<span class="hl">النتيجة نفسها مهما رسمنا الشجرة</span>', at(3, 'سَنَحْصُلُ'), 'font-size: 40px; font-weight: 700')}''', 24))
SC.append(scene(4, f'''{h2('الأُسّ')}
{fu(m(e(P(2, 3), '=', '٢ × ٢ × ٢'), 90), at(4, 'نَكْتُبُهَا'), cls='pop')}
<div style="display: flex; gap: 30px">{tcard('٢', 'الأساس', at(4, 'اثْنَانِ هُوَ'))}{tcard('٣', 'الأُسّ', at(4, 'وَثَلَاثَةٌ هُوَ'), '#C7361B')}</div>
{fu(m(e('١٢٠', '=', P(2, 3), '×', '٣', '×', '٥'), 64), at(4, 'إِذَنْ'))}''', 26))
SC.append(scene(5, f'''{h2('انتبهوا!', 0, '#8E2A18')}
{fu('<span style="color: #C7361B">✘ العدد ١ لا يظهر في شجرة العوامل</span>', at(5, 'الْعَدَدُ وَاحِدٌ'), 'font-size: 50px; font-weight: 700')}
{fu('لأنه ليس عدداً أولياً', at(5, 'لِأَنَّهُ'), 'font-size: 40px; font-weight: 700; color: #3B5480')}''', 34))
SC.append(scene(6, f'''{h2('م م ص للعددين ٦٠ ، ٧٥')}
{fu(m(e('٦٠', '=', P(2, 2), '×', '٣', '×', '٥'), 60), at(6, 'سِتُّونَ تُسَاوِي'))}
{fu(m(e('٧٥', '=', '٣', '×', P(5, 2)), 60), at(6, 'وَخَمْسَةٌ وَسَبْعُونَ تُسَاوِي'))}
{fu('نأخذ <b style="color: #7A3FD1">الأُسّ الأكبر</b> لكل عامل', at(6, 'نَأْخُذُ'), 'font-size: 38px; font-weight: 700')}
{fu(m(e('م م ص', '=', P(2, 2), '×', '٣', '×', P(5, 2), '=', '٣٠٠'), 62, '; color: #7A3FD1'), at(6, 'فَيَكُونُ'), cls='pop')}''', 22))
SC.append(scene(7, f'''{h2('ع م ك للعددين ٦٠ ، ٧٥')}
{fu('نأخذ <b style="color: #C7361B">الأُسّ الأصغر</b> للعوامل المشتركة فقط', at(7, 'نَأْخُذُ'), 'font-size: 38px; font-weight: 700')}
{fu(m(e('ع م ك', '=', '٣', '×', '٥', '=', '١٥'), 70, '; color: #C7361B'), at(7, 'ثَلَاثَةٌ فِي'), cls='pop')}''', 34))
SC.append(scene(8, f'''<h2 class="pop" style="margin: 0; font-size: 58px"><span class="hl">تذكّروا</span></h2>
<div style="display: flex; gap: 26px">{tcard('شجرة العوامل', 'تنتهي بأعدادٍ أولية', at(8, 'الشَّجَرَةُ'))}{tcard('الأُسّ', 'يختصر الضرب المتكرّر', at(8, 'وَالْأُسُّ'), '#C7361B')}</div>
{fu('كتاب النشاط ص ٢٠ – ٢٢ · راجعوا ورقة الملخّص', at(8, 'حُلُّوا'), 'font-size: 30px; color: #3B5480')}''', 34))
finalize(SC, 'الدرس ١-٥: الأسس', 'الأسس', 'فيديو_الأسس.dc.html')
