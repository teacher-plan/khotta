# دوالّ مشتركة لدروس الوحدة السابعة «المساحة والمحيط» — تُنفَّذ من ملفات الشرائح (exec) بعد frac_common.py.
# رسومٌ من إعدادي (SVG): مستطيل، مثلث، متوازي أضلاع، شبه منحرف، دائرة وأجزاؤها، أشكالٌ مركّبة، شبكة وحدات.
import math as _mm
exec(open(os.path.join(HERE, 'frac_common.py'), encoding='utf-8').read())

def U2(u): return f'{u}<sup class="u2">٢</sup>'          # وحدة مربّعة: سم² …
CM2, MM2, M2, KM2 = U2('سم'), U2('ملم'), U2('م'), U2('كم')
PL = '<span class="x">+</span>'
HALF = FR('١', '٢')
PI = '<span class="pi">π</span>'

exec(open(os.path.join(HERE, 'area_figs.py'), encoding='utf-8').read())

AREA_CSS = FRAC_CSS + '''
.u2{font-size:.55em;vertical-align:super;line-height:0;margin-inline-start:.04em}
.xa small{margin-top:.45em}
.pi{font-family:'Times New Roman',serif;font-style:italic;font-weight:700}
.slide .svgfig.shp{width:auto;height:min(46vh,440px);max-width:46vw;max-height:none}
.slide .svgfig.shp.lg{height:min(56vh,540px);max-width:60vw}
.slide .svgfig.shp.sm{height:min(32vh,300px);max-width:34vw}
.box.col .svgfig.shp{height:min(36vh,340px);max-width:40vw}
.xq .svgfig.shp{display:block;margin:.4vh auto;height:26vh;width:auto;max-width:90%}
.slide .svgfig.stair{width:auto;height:min(54vh,540px);max-width:92vw;max-height:none}
.fml{display:block;line-height:1.7;text-align:center;font-family:var(--fh);font-weight:900;font-size:clamp(34px,7vh,80px);background:#FFF6E3;border:4px solid #E9A23B;border-radius:22px;padding:1vh 2vw;color:var(--ink)}
.fml small{display:block;font-size:.5em;color:var(--ink2);font-weight:700}
.act{border-collapse:separate;border-spacing:0;font-weight:800;font-size:clamp(22px,4vh,46px);background:#fff;border:3px solid var(--ink);border-radius:14px;overflow:hidden;width:min(1300px,92vw)}
.act th{background:var(--ink);color:#fff;padding:.3em .6em}.act td{text-align:center;padding:.25em .6em;border-top:2px solid var(--line)}.act td+td,.act th+th{border-inline-start:2px solid var(--line)}
.act .hid{display:none}.act .open .hid,.act td.flip.open .hid{display:inline}
'''
