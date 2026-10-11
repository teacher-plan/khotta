# مساعدات ملخّصات الوحدة السابعة: تُنفَّذ بعد summary2.py (exec). وحدات مربّعة، أعدادٌ بمجموعات، ورسومٌ صغيرة من area_figs.py.
exec(open(os.path.join(HERE, 'figs.py'), encoding='utf-8').read())
exec(open(os.path.join(HERE, 'area_figs.py'), encoding='utf-8').read())
def U2(u): return f'{u}<sup class="u2">٢</sup>'
CM2, MM2, M2, KM2 = U2('سم'), U2('ملم'), U2('م'), U2('كم')
PI = '<span class="pi">π</span>'
def SF(svg, h=30): return f'<div class="sfig" style="--h:{h}mm">{svg}</div>'
CSS += '''.u2{font-size:.6em;vertical-align:super;line-height:0}
.pi{font-family:'Times New Roman',serif;font-style:italic;font-weight:700}
.sfig{display:flex;justify-content:center;gap:6mm;align-items:center}.sfig svg{height:var(--h);width:auto;max-width:100%}
.figrow{display:flex;gap:4mm;align-items:center}.figrow>.ex,.figrow>div:first-child{flex:1}
'''
def FIX(x): return FIXNUM([x])[0].replace('²', '<sup class="u2">٢</sup>')   # أعدادٌ بمجموعات معزولة LTR، و ² أسٌّ مرفوع
