# دوالّ مشتركة لدروس الوحدة الثامنة «النسب المئوية» — تُنفَّذ من ملفات الشرائح (exec).
# ملاحظة: «٢٥٪» تُكتب كما هي فتظهر العلامة يسار العدد كما في الكتاب.
exec(open(os.path.join(HERE, 'area_common.py'), encoding='utf-8').read())
MI = '<span class="x">−</span>'
def P(n): return f'{n}٪'

exec(open(os.path.join(HERE, 'pct_figs.py'), encoding='utf-8').read())
PCT_CSS = AREA_CSS + '''
.pctbig{font-family:var(--fh);font-weight:900;font-size:clamp(60px,14vh,160px);color:var(--base);line-height:1}
'''
