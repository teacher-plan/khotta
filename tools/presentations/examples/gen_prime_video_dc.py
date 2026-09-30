# يبني مصدر تصميم فيديو الدرس ١-٤ «الأعداد الأولية» (.dc.html) — التوقيت من صوت_الأولية.
# python3 gen_prime_video_dc.py ← python3 gen_powers_video.py فيديو_الأولية.dc.html صوت_الأولية فيديو_الأولية.html
import os
AUD, NARR = 'صوت_الأولية', 'narration_prime.py'
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'video_common.py'), encoding='utf-8').read())

def pill(t, d, c='#1E6FD9', bg='#EAF1FF'): return fu(t, d, f'font-size: 34px; font-weight: 700; padding: 10px 26px; border-radius: 18px; background: {bg}; color: {c}')
def chip(t, d, bg='#1B7A3E', size=46): return fu(t, d, f'font-size: {size}px; font-weight: 700; padding: 4px 18px; border-radius: 14px; background: {bg}; color: #FFFFFF; min-width: 70px; text-align: center', 'pop')
def tcard(t, s, d, c='#1E6FD9'): return fu(f'<b style="font-size: 40px; color: {c}">{t}</b><span style="font-size: 30px; font-weight: 700">{s}</span>', d, f'display: flex; flex-direction: column; gap: 10px; align-items: center; padding: 20px 30px; border-radius: 22px; background: #FFFFFF; border: 3px solid {c}; min-width: 300px')
PRIMES = [p for p in range(2, 101) if all(p % d for d in range(2, int(p ** .5) + 1))]
AR = str.maketrans('0123456789', '٠١٢٣٤٥٦٧٨٩')
def ar(n): return str(n).translate(AR)
SC = []
SC.append(scene(0, f'''<div class="pop" style="animation-delay: .5s">{m(e('٢', '،', '٣', '،', '٥', '،', '٧', '،', '١١'), 80)}</div>
<h1 class="fu" style="margin: 0; font-size: 84px; font-weight: 700; animation-delay: {at(0, 'دَرْسُنَا')}s"><span class="hl">الأعداد الأوليّة</span></h1>
<div style="display: flex; gap: 22px">{pill('العدد الأولي', at(0, 'سَنَتَعَرَّفُ'))}{pill('غربال إراتوستينس', at(0, 'وَنَسْتَخْدِمُ'))}{pill('العوامل الأولية', at(0, 'وَنَجِدُ'))}</div>''', 34))
SC.append(scene(1, f'''{h2('ما العدد الأولي؟')}
{fu('له <b style="color: #C7361B">عاملان فقط</b>: ١ والعدد نفسه', at(1, 'الْعَدَدُ الْأَوَّلِيُّ'), 'font-size: 44px; font-weight: 700')}
<div style="display: flex; gap: 30px">{card('<b style="font-size: 40px">١١ ← ١ ، ١١ ✔</b>', at(1, 'مِثْلُ'), True)}{card('<b style="font-size: 40px">٩ ← ١ ، ٣ ، ٩ ✘</b>', at(1, 'أَمَّا'), False)}</div>''', 30))
SC.append(scene(2, f'''{h2('انتبهوا!', 0, '#8E2A18')}
<div style="display: flex; gap: 30px">{tcard('١ ليس أولياً', 'له عاملٌ واحد فقط', at(2, 'الْعَدَدُ وَاحِدٌ'), '#C7361B')}{tcard('٢ أولي', 'الأولي الزوجي الوحيد', at(2, 'وَالْعَدَدُ اثْنَانِ'), '#1B7A3E')}</div>''', 34))
SC.append(scene(3, f'''{h2('الأعداد الأولية الأصغر من ٢٠')}
<div style="display: flex; gap: 16px; direction: rtl">{''.join(chip(ar(p), round(at(3, 'اثْنَانِ') + k * .75, 1)) for k, p in enumerate(PRIMES[:8]))}</div>
{fu('<span class="hl">ثمانية أعداد</span>', at(3, 'ثَمَانِيَةٌ'), 'font-size: 44px; font-weight: 700')}''', 34))
SC.append(scene(4, f'''{h2('غربال إراتوستينس')}
<div style="display: flex; gap: 16px">{''.join(pill(f'مضاعفات {ar(p)}', at(4, w), '#C7361B', '#FDE7E3') for p, w in ((2, 'مُضَاعَفَاتِ اثْنَيْنِ'), (3, 'ثَلَاثَةٍ'), (5, 'خَمْسَةٍ'), (7, 'سَبْعَةٍ')))}</div>
<div style="display: grid; grid-template-columns: repeat(9, auto); gap: 10px; direction: rtl">{''.join(chip(ar(p), round(at(4, 'وَمَا يَبْقَى') + k * .08, 2), size=34) for k, p in enumerate(PRIMES))}</div>
{fu('<span class="hl">٢٥ عدداً أولياً حتى ١٠٠</span>', at(4, 'خَمْسَةٌ وَعِشْرُونَ'), 'font-size: 42px; font-weight: 700')}''', 26))
SC.append(scene(5, f'''{h2('احذروا!', 0, '#8E2A18')}
{fu(m(e('٩١', EQ, '٧', X, '١٣'), 96), at(5, 'يُسَاوِي'), cls='pop')}
{fu('<span style="color: #C7361B">✘ ليس أولياً</span>', at(5, 'إِذَنْ'), 'font-size: 48px; font-weight: 700')}''', 34))
SC.append(scene(6, f'''{h2('العوامل الأولية للعدد ٣٠')}
{''.join(fu(m(e(p, X, q, EQ, '٣٠'), 60), at(6, w)) for p, q, w in (('٢', '١٥', 'اثْنَانِ فِي'), ('٣', '١٠', 'ثَلَاثَةٌ فِي'), ('٥', '٦', 'خَمْسَةٌ فِي')))}
{fu('<span class="hl">العوامل الأولية: ٢ ، ٣ ، ٥</span>', at(6, 'إِذَنِ'), 'font-size: 46px; font-weight: 700', 'pop')}''', 26))
SC.append(scene(7, f'''{h2('ناتج ضرب ومجموع أوّليّين')}
<div style="display: flex; gap: 30px">{tcard('ناتج ضرب', m(e('٣٥', EQ, '٥', X, '٧'), 50), at(7, 'نَاتِجَ'))}{tcard('مجموع', m(e('١٨', EQ, '٥', PL, '١٣'), 50), at(7, 'أَوْ مَجْمُوعَ'), '#7A3FD1')}</div>''', 32))
SC.append(scene(8, f'''<h2 class="pop" style="margin: 0; font-size: 58px"><span class="hl">تذكّروا</span></h2>
<div style="display: flex; gap: 26px">{tcard('العدد الأولي', 'عاملان فقط: ١ ونفسه', at(8, 'الْعَدَدُ'))}{tcard('العدد ١', 'ليس أولياً', at(8, 'وَالْوَاحِدُ'), '#C7361B')}</div>
{fu('كتاب النشاط ص ١٨ و ١٩ · راجعوا ورقة الملخّص', at(8, 'حُلُّوا'), 'font-size: 30px; color: #3B5480')}''', 34))
finalize(SC, 'الدرس ١-٤: الأعداد الأولية', 'الأعداد الأولية', 'فيديو_الأولية.dc.html')
