# أدوات مشتركة لفيديوهات الوحدتين ٧ و٨ (تُنفَّذ بعد lesson_video.py): رسوم area_figs.py وpct_figs.py في فضاءٍ مستقل
# حتى لا تُستبدل FR وX… الخاصة بالفيديو.
_ns = {'__builtins__': __builtins__, 'os': os, 'HERE': HERE}
for _f in ('figs.py', 'area_figs.py', 'pct_figs.py'):
    exec(open(os.path.join(HERE, _f), encoding='utf-8').read(), _ns)
for _k in ('RECT', 'SQGRID', 'TRI', 'PARA', 'TRAP', 'CIRC', 'COMP', 'STAIR2', 'AREA_STAIR', 'NB', 'HALVES', 'PARACUT', 'TRAP2', 'SEMI', 'QUAR', 'SECTORS', 'DRAW',
           'BATT', 'PBAR', 'GRIDN', 'NL3', 'SPIDER'):
    globals()[_k] = _ns[_k]
def SV(svg, h=300): return svg.replace('<svg class="svgfig', f'<svg style="height: {h}px; width: auto; vertical-align: middle; direction: ltr" class="svgfig', 1)
def K(t): return f'<b style="color: #C2410C">{t}</b>'
def P(n): return f'{n}٪'
LT, GT = '<span class="x">&lt;</span>', '<span class="x">&gt;</span>'
