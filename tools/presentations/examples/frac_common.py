# أدوات مشتركة لعروض الوحدة السادسة «الكسور (١)»: الكسر المكدَّس، الخطوات، المفردات، بطاقات القلب، وتنسيقٌ موحّد.
# تُستدعى في أول كل ملف شرائح: exec(open(os.path.join(HERE, 'frac_common.py'), encoding='utf-8').read())
exec(open(os.path.join(HERE, 'figs.py'), encoding='utf-8').read())
def FR(n, d): return f'<span class="fr"><span>{n}</span><span>{d}</span></span>'
def MF(*p, cls=''): return M(*[FR(*x) if isinstance(x, tuple) else x for x in p], cls=cls)
def STP(lab, expr='', cls=''): return st(f'<div class="stp {cls}"><span class="lab">{lab}</span>{expr}</div>')
def STEPS(*rows): return '<div class="stps">' + ''.join(rows) + '</div>'
def VC(items, cls=''): return f'<div class="voc3 {cls}">' + ''.join(st(f'<div><b>{w}</b><i>{e}</i><span>{d}</span></div>') for w, e, d in items) + '</div>'
def FLIPS(items, style='flex:1'):
    return '<div class="row">' + ''.join(st(f'<button class="flip box col" style="{style}">{q}<span class="tap">👆</span><span class="hid col"><span class="kk c-we">{a_}</span><span class="why">{w}</span></span></button>') for q, a_, w in items) + '</div>'
MI = '<span class="x">−</span>'; DV = '<span class="x">÷</span>'; X = '<span class="x">×</span>'

FRAC_CSS = FIG_CSS + '''
.fr{display:inline-flex;flex-direction:column;align-items:center;line-height:1.05;vertical-align:middle;margin:0 .12em}
.fr>span:first-child{border-bottom:.07em solid currentColor;padding:0 .15em .04em;align-self:stretch;text-align:center}
.stps{display:flex;flex-direction:column;gap:1.2vh;align-items:stretch}
.stp{display:flex;align-items:center;gap:1.4vw;justify-content:space-between}
.stp .lab{flex:0 1 auto;max-width:60%;font-family:var(--fh);font-weight:800;color:#2563EB;background:#EAF1FF;border-radius:12px;padding:.2em .8em;text-align:center;line-height:1.4;font-size:clamp(20px,3.6vh,42px)}
.stp.fin .lab{background:var(--good);color:#fff}
.slide .vrow{align-items:center;justify-content:center;gap:2vh 3vw;flex-wrap:wrap}
.voc3{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1.6vw;width:min(1500px,94vw)}
.voc3 .st>div{display:flex;flex-direction:column;align-items:center;gap:.6vh;background:#fff;border:3px solid var(--line);border-radius:18px;padding:1.6vh 1vw;text-align:center}
.voc3 b{font-family:var(--fh);font-size:clamp(28px,5.4vh,64px);color:var(--base)}.voc3 i{font-style:normal;font-weight:700;color:var(--ink2);font-size:clamp(16px,2.8vh,32px)}
.voc3 span{font-weight:700;font-size:clamp(20px,3.6vh,42px);line-height:1.5}
.facs{display:flex;gap:2vw;justify-content:center;flex-wrap:wrap}
.facs .st>div{display:flex;flex-direction:column;align-items:center;gap:.6vh;background:#fff;border:3px solid var(--line);border-radius:18px;padding:1.4vh 2vw}
.facs b{font-family:var(--fh);font-size:clamp(34px,6.4vh,76px);color:#2563EB}.facs span{font-weight:800;font-size:clamp(40px,7.6vh,90px)}
.bars{display:flex;flex-direction:row;gap:2vw;align-items:center;justify-content:center}
.slide .svgfig.fbar{width:auto;height:min(50vh,480px);max-width:30vw;max-height:none}
.slide .svgfig.fcirc{width:auto;height:min(70vh,680px);max-width:30vw;max-height:none}
.slide .svgfig.eqv{width:auto;height:min(84vh,800px);max-width:44vw;max-height:none}
.box .row .svgfig.eqv{height:min(66vh,640px);max-width:22vw}
.box.col .svgfig.eqv{height:min(72vh,700px)}
.circs{gap:3vw;justify-content:center}
.slide .vrow .fig{height:min(56vh,520px);width:auto;max-width:52vw;max-height:none}
.slide .vrow .fig.lg{max-width:56vw;height:auto;max-height:40vh}
.why{font-weight:700;color:var(--ink2);font-size:clamp(20px,3.4vh,40px)}
.errs{display:flex;flex-direction:column;gap:1.4vh;width:min(1300px,90vw)}
.errs>.st{width:100%}.errs .err{width:100%;display:flex;flex-direction:column;align-items:center;gap:.6vh;background:#fff;border:3px solid var(--line);border-radius:16px;padding:.8vh 1.6vw;font-size:clamp(24px,4.6vh,54px);font-weight:700}
.errs .err .xa{font-size:clamp(28px,5.4vh,64px);display:block;text-align:center;line-height:1.6}
.xa.ok{color:var(--good)}
.sumg{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:2vw;width:min(1600px,94vw)}
.sumg .col span{font-weight:700;font-size:clamp(20px,3.6vh,42px);line-height:1.5}
.sumg .kk{font-size:clamp(26px,4.8vh,58px)}
.hid.col .kk{font-size:clamp(34px,7vh,84px)}
.flip.box{font-size:clamp(34px,7vh,84px);font-weight:800}.flip.box .hint{font-size:clamp(24px,4.6vh,54px)}
.facs+.row{margin-top:2vh}
.stps{min-width:34vw}.slide .stp .m{font-size:clamp(44px,9vh,100px)!important}.slide .stp .lab{font-size:clamp(28px,5.4vh,62px)}
.xq .fig.side{height:66vh;max-height:none;width:auto;max-width:50vw}
.vcol{display:flex;flex-direction:column;align-items:center;gap:2vh}.slide .fig.wide{width:min(1100px,62vw);height:auto;max-height:none}
.xq .fig.lg{height:auto;width:min(1100px,80vw);max-height:48vh}
.xa small{display:block}
@media (max-aspect-ratio:1/1){.voc3,.sumg{grid-template-columns:1fr}.slide .svgfig.eqv{max-width:80vw}}
'''
