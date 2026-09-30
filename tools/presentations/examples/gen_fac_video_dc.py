# يبني مصدر تصميم فيديو الدرس ١-٣ «العوامل وقابلية القسمة» (.dc.html) — التوقيت من صوت_العوامل.
# python3 gen_fac_video_dc.py ← python3 gen_powers_video.py فيديو_العوامل.dc.html صوت_العوامل فيديو_العوامل.html
import os
AUD, NARR = 'صوت_العوامل', 'narration_fac.py'
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'video_common.py'), encoding='utf-8').read())

def lst(xs, d0, step, hot=(), size=46):
    return '<div style="display: flex; gap: 14px; direction: rtl; align-items: center; font-weight: 700">' + '<span style="color: #7A8BA8">،</span>'.join(
        fu(x, round(d0 + k * step, 1), f'font-size: {size}px; ' + ('border: 4px solid #C7361B; border-radius: 50%; padding: 0 10px; color: #C7361B' if x in hot else ''), 'pop') for k, x in enumerate(xs)) + '</div>'
ROW = 'display: flex; align-items: center; gap: 28px; padding: 14px 30px; border-radius: 20px; background: #FFFFFF; border: 2px solid #C9D6E8'
DV = '<span class="x">÷</span>'
def pill(t, d, c='#1E6FD9', bg='#EAF1FF'): return fu(t, d, f'font-size: 34px; font-weight: 700; padding: 10px 26px; border-radius: 18px; background: {bg}; color: {c}')
SC = []
SC.append(scene(0, f'''<div class="pop" style="animation-delay: .5s">{m(e('٣', X, '٨', EQ, '٢٤'), 90)}</div>
<h1 class="fu" style="margin: 0; font-size: 84px; font-weight: 700; animation-delay: {at(0, 'دَرْسُنَا')}s"><span class="hl">العوامل وقابلية القسمة</span></h1>
<div style="display: flex; gap: 22px">{pill('العوامل', at(0, 'كُلَّ عَوَامِلِ'))}{pill('ع م ك', at(0, 'وَالْعَامِلَ'))}{pill('اختبارات القسمة', at(0, 'وَاخْتِبَارَاتٍ'))}</div>''', 34))
SC.append(scene(1, f'''{h2('ما العامل؟')}
{fu('يقسم العدد <b style="color: #C7361B">بدون باقٍ</b>', at(1, 'الْعَامِلُ'), 'font-size: 40px; font-weight: 700')}
{fu(m(e('٣', X, '٨', EQ, '٢٤'), 84), at(1, 'ثَلَاثَةٌ فِي'))}
<div style="display: flex; gap: 30px">{card('<b style="font-size: 36px">٣ عاملٌ للعدد ٢٤</b>', at(1, 'إِذَنْ'), True)}{card('<b style="font-size: 36px">٢٤ مضاعفٌ للعدد ٣</b>', at(1, 'وَأَرْبَعَةٌ وَعِشْرُونَ مُضَاعَفٌ'), False, '; color: #7A3FD1; border-color: #7A3FD1; background: #F3ECFD')}</div>''', 30))
PR = [('١', '٤٠', 'وَاحِدٌ فِي'), ('٢', '٢٠', 'اثْنَانِ فِي'), ('٤', '١٠', 'أَرْبَعَةٌ فِي'), ('٥', '٨', 'خَمْسَةٌ فِي')]
SC.append(scene(2, f'''{h2('عوامل العدد ٤٠ في أزواج')}
<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px 40px">{''.join(fu(m(e(x, X, y, EQ, '٤٠'), 54), at(2, k), ROW) for x, y, k in PR)}</div>
{fu(lst(['١', '٢', '٤', '٥', '٨', '١٠', '٢٠', '٤٠'], at(2, 'وَنَتَوَقَّفُ'), .25, size=48), at(2, 'وَنَتَوَقَّفُ'))}''', 30))
SC.append(scene(3, f'''{h2('انتبهوا!', 0, '#8E2A18')}
{fu('<span class="hl">١ عاملٌ لكل عدد · وكل عددٍ عاملٌ لنفسه</span>', at(3, 'الْعَدَدُ وَاحِدٌ'), 'font-size: 40px; font-weight: 700')}
<div style="{ROW}">{fu('<b style="font-size: 36px; color: #1E6FD9">عوامل ١٨</b>', at(3, 'فَعَوَامِلُ'))}{lst(['١', '٢', '٣', '٦', '٩', '١٨'], at(3, 'هِيَ'), .9, hot=('١', '١٨'), size=52)}</div>''', 34))
SC.append(scene(4, f'''{h2('العوامل المشتركة و ع م ك')}
<div style="{ROW}">{fu('<b style="font-size: 34px; color: #1E6FD9">عوامل ٢٤</b>', at(4, 'عَوَامِلُ أَرْبَعَةٍ'))}{lst(['١', '٢', '٣', '٤', '٦', '٨', '١٢', '٢٤'], at(4, 'عَوَامِلُ أَرْبَعَةٍ') + .3, .3, hot=('١', '٢', '٤', '٨'), size=42)}</div>
<div style="{ROW}">{fu('<b style="font-size: 34px; color: #1E6FD9">عوامل ٤٠</b>', at(4, 'وَعَوَامِلُ أَرْبَعِينَ'))}{lst(['١', '٢', '٤', '٥', '٨', '١٠', '٢٠', '٤٠'], at(4, 'وَعَوَامِلُ أَرْبَعِينَ') + .3, .3, hot=('١', '٢', '٤', '٨'), size=42)}</div>
{fu('<span class="hl">ع م ك (٢٤ ، ٤٠) = ٨</span>', at(4, 'وَأَكْبَرُهَا'), 'font-size: 48px; font-weight: 700', 'pop')}''', 26))
T1 = [('على ٢', 'الآحاد زوجي', 'عَلَى اثْنَيْنِ'), ('على ٥', 'الآحاد ٠ أو ٥', 'عَلَى خَمْسَةٍ'), ('على ١٠', 'الآحاد ٠', 'وَعَلَى عَشَرَةٍ')]
def tcard(t, s, d, c='#1E6FD9'): return fu(f'<b style="font-size: 40px; color: {c}">{t}</b><span style="font-size: 30px; font-weight: 700">{s}</span>', d, f'display: flex; flex-direction: column; gap: 10px; align-items: center; padding: 20px 30px; border-radius: 22px; background: #FFFFFF; border: 3px solid {c}; min-width: 300px')
SC.append(scene(5, f'''{h2('اختبارات قابلية القسمة: الآحاد')}
<div style="display: flex; gap: 26px">{''.join(tcard(t, s, at(5, k)) for t, s, k in T1)}</div>''', 34))
SC.append(scene(6, f'''{h2('على ٣ و ٩: نجمع الأرقام')}
{fu(m(e('٦', PL, '٧', PL, '٨', PL, '٦', EQ, '٢٧'), 72), at(6, 'مَجْمُوعُ'))}
<div style="display: flex; gap: 26px">{tcard('على ٣ ✔', '٢٧ ÷ ٣ = ٩', at(6, 'إِذَنْ'), '#1B7A3E')}{tcard('على ٩ ✔', '٢٧ ÷ ٩ = ٣', at(6, 'وَعَلَى تِسْعَةٍ'), '#1B7A3E')}{tcard('على ٦', 'على ٢ و ٣ معاً', at(6, 'وَعَلَى سِتَّةٍ'), '#7A3FD1')}</div>''', 30))
SC.append(scene(7, f'''{h2('على ٤ و ٨: آخر الأرقام')}
<div style="display: flex; gap: 26px">{tcard('على ٤', 'آخر رقمين', at(7, 'وَعَلَى أَرْبَعَةٍ'))}{tcard('على ٨', 'آخر ثلاثة أرقام', at(7, 'وَعَلَى ثَمَانِيَةٍ'))}</div>
{fu(m(e('٣٧٢٤', '←', '<span style="color: #C7361B">٢٤</span>', DV, '٤', EQ, '٦'), 66), at(7, 'الْعَدَدُ'), cls='pop')}''', 32))
SC.append(scene(8, f'''<h2 class="pop" style="margin: 0; font-size: 58px"><span class="hl">تذكّروا</span></h2>
<div style="display: flex; gap: 26px">{tcard('العوامل', 'بدون باقٍ · في أزواج', at(8, 'الْعَوَامِلُ'))}{tcard('ع م ك', 'أكبر عاملٍ مشترك', at(8, 'وَالْعَامِلُ'), '#C7361B')}</div>
{fu('كتاب النشاط ص ١٦ و ١٧ · راجعوا ورقة الملخّص', at(8, 'حُلُّوا'), 'font-size: 30px; color: #3B5480')}''', 34))
finalize(SC, 'الدرس ١-٣: العوامل وقابلية القسمة', 'العوامل وقابلية القسمة', 'فيديو_العوامل.dc.html')
