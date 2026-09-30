# يبني مصدر تصميم فيديو الدرس ١-٢ «المضاعفات» (.dc.html) — التوقيت من صوت_المضاعفات.
# python3 gen_mult_video_dc.py ← python3 gen_powers_video.py فيديو_المضاعفات.dc.html صوت_المضاعفات فيديو_المضاعفات.html
import os
AUD, NARR = 'صوت_المضاعفات', 'narration_mult.py'
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'video_common.py'), encoding='utf-8').read())

def lst(xs, d0, step, hot=(), size=46):  # قائمة تظهر عدداً عدداً
    return '<div style="display: flex; gap: 14px; direction: rtl; align-items: center; font-weight: 700">' + '<span style="color: #7A8BA8">،</span>'.join(
        fu(x, round(d0 + k * step, 1), f'font-size: {size}px; ' + ('border: 4px solid #C7361B; border-radius: 50%; padding: 0 10px; color: #C7361B' if x in hot else ''), 'pop') for k, x in enumerate(xs)) + f'<span style="font-size: {size}px; color: #7A8BA8">، …</span></div>'
ROW = 'display: flex; align-items: center; gap: 28px; padding: 14px 30px; border-radius: 20px; background: #FFFFFF; border: 2px solid #C9D6E8'
SC = []
SC.append(scene(0, f'''<div class="pop" style="animation-delay: .5s">{lst(['٥', '١٠', '١٥', '٢٠'], .5, .5, size=70)}</div>
<h1 class="fu" style="margin: 0; font-size: 90px; font-weight: 700; animation-delay: {at(0, 'دَرْسُنَا')}s"><span class="hl">المضاعفات</span></h1>
{fu('المضاعف المشترك الأصغر (م م ص)', at(0, 'الْمُشْتَرَكَ'), 'font-size: 36px; color: #3B5480; font-weight: 700')}''', 34))
SC.append(scene(1, f'''{h2('مضاعفات العدد')}
<div style="{ROW}">{fu('<b style="font-size: 36px; color: #1E6FD9">مضاعفات ٣</b>', at(1, 'مُضَاعَفَاتُ الْعَدَدِ'))}{lst(['٣', '٦', '٩', '١٢', '١٥'], at(1, 'ثَلَاثَةٌ،'), .9)}</div>
{fu('نبدأ <b>بالعدد نفسه</b>، ثم نضيفه في كل مرّة', at(1, 'نَبْدَأُ'), 'font-size: 36px; font-weight: 700; padding: 10px 28px; border-radius: 40px; background: #FFF4D6; border: 2px solid #F2C94C')}
<div style="{ROW}">{fu('<b style="font-size: 36px; color: #1E6FD9">مضاعفات ٧</b>', at(1, 'وَمُضَاعَفَاتُ سَبْعَةٍ'))}{lst(['٧', '١٤', '٢١', '٢٨'], at(1, 'سَبْعَةٌ،'), .9)}</div>''', 30))
SC.append(scene(2, f'''{h2('المضاعف الرابع للعدد ١٢')}
<div style="{BOX}">{stp('بالقائمة؟ طويلة…', e('١٢', '،', '٢٤', '،', '٣٦', '،', '٤٨'), at(2, 'فَلَا'))}{stp('بالضرب مباشرة', e('١٢', X, '٤', EQ, '٤٨'), at(2, 'نَضْرِبُ'), True)}</div>''', 34))
SC.append(scene(3, f'''{h2('السابع عشر للعدد ٨ هو ١٣٦')}
<div style="{BOX}">{stp('الثامن عشر: نضيف ٨', e('١٣٦', PL, '٨', EQ, '١٤٤'), at(3, 'نُضِيفُ'), True)}{stp('السادس عشر: نطرح ٨', e('١٣٦', MI, '٨', EQ, '١٢٨'), at(3, 'نَطْرَحُ'), True)}</div>''', 34))
SC.append(scene(4, f'''{h2('المضاعفات المشتركة')}
<div style="{ROW}">{fu('<b style="font-size: 34px; color: #1E6FD9">مضاعفات ٦</b>', at(4, 'مُضَاعَفَاتِ سِتَّةٍ'))}{lst(['٦', '١٢', '١٨', '٢٤', '٣٠', '٣٦', '٤٢', '٤٨'], at(4, 'مُضَاعَفَاتِ سِتَّةٍ') + .3, .25, hot=('٢٤', '٤٨'), size=40)}</div>
<div style="{ROW}">{fu('<b style="font-size: 34px; color: #1E6FD9">مضاعفات ٨</b>', at(4, 'وَمُضَاعَفَاتِ ثَمَانِيَةٍ'))}{lst(['٨', '١٦', '٢٤', '٣٢', '٤٠', '٤٨'], at(4, 'وَمُضَاعَفَاتِ ثَمَانِيَةٍ') + .3, .25, hot=('٢٤', '٤٨'), size=40)}</div>
{fu('<span class="hl">م م ص (٦ ، ٨) = ٢٤</span>', at(4, 'وَأَصْغَرُهَا'), 'font-size: 46px; font-weight: 700', 'pop')}''', 26))
SC.append(scene(5, f'''{h2('جرّبوا معي: م م ص للعددين ٤ و ٦')}
<div style="{ROW}">{fu('<b style="font-size: 34px; color: #1E6FD9">مضاعفات ٤</b>', at(5, 'مُضَاعَفَاتُ أَرْبَعَةٍ'))}{lst(['٤', '٨', '١٢'], at(5, 'أَرْبَعَةٌ،'), .7, hot=('١٢',))}</div>
<div style="{ROW}">{fu('<b style="font-size: 34px; color: #1E6FD9">مضاعفات ٦</b>', at(5, 'وَمُضَاعَفَاتُ سِتَّةٍ'))}{lst(['٦', '١٢'], at(5, 'سِتَّةٌ،'), .7, hot=('١٢',))}</div>
{fu(m(e('م م ص', EQ, '١٢'), 70, '; color: #1B7A3E'), at(5, 'إِذَنْ'), cls='pop')}''', 28))
SC.append(scene(6, f'''{h2('ضيوف سارة')}
{fu('بين ٥٠ و ١٠٠ · يجلسون <b>٨</b> أو <b>١٢</b> على كل مائدة', at(6, 'دَعَتْ'), 'font-size: 36px; font-weight: 700')}
{fu('مضاعفات مشتركة للعددين ٨ و ١٢:', at(6, 'الْمُضَاعَفَاتُ'), 'font-size: 32px; color: #3B5480')}
{lst(['٢٤', '٤٨', '٧٢', '٩٦'], at(6, 'أَرْبَعَةٌ وَعِشْرُونَ'), 1.3, hot=('٧٢', '٩٦'), size=60)}
{fu(m(e('٧٢', 'أو', '٩٦'), 76, '; color: #1B7A3E'), at(6, 'وَبَيْنَ'), cls='pop')}''', 26))
SC.append(scene(7, f'''<h2 class="pop" style="margin: 0; font-size: 58px"><span class="hl">تذكّروا</span></h2>
<div style="display: flex; gap: 26px">{''.join(fu(f'<b style="font-size: 38px; color: {c}">{t}</b><span style="font-size: 28px">{s}</span>', at(7, k), f'display: flex; flex-direction: column; gap: 10px; align-items: center; padding: 20px 28px; border-radius: 22px; background: #FFFFFF; border: 3px solid {c}; min-width: 320px')
  for t, s, c, k in [('المضاعفات', 'تبدأ بالعدد نفسه ولا تنتهي', '#1E6FD9', 'الْمُضَاعَفَاتُ'), ('م م ص', 'أوّل عددٍ مشترك', '#C7361B', 'وَالْمُضَاعَفُ')])}</div>
{fu('كتاب النشاط ص ١٥ · راجعوا ورقة الملخّص', at(7, 'حُلُّوا'), 'font-size: 30px; color: #3B5480')}''', 34))
finalize(SC, 'الدرس ١-٢: المضاعفات', 'المضاعفات', 'فيديو_المضاعفات.dc.html')
