# أدوات مشتركة لعروض الوحدة السادسة «الكسور (١)»: الكسر المكدَّس، الخطوات، المفردات، بطاقات القلب، وتنسيقٌ موحّد.
# تُستدعى في أول كل ملف شرائح: exec(open(os.path.join(HERE, 'frac_common.py'), encoding='utf-8').read())
exec(open(os.path.join(HERE, 'figs.py'), encoding='utf-8').read())
def FR(n, d): return f'<span class="fr"><span>{n}</span><span>{d}</span></span>'
def MF(*p, cls=''): return M(*[FR(*x) if isinstance(x, tuple) else x for x in p], cls=cls)
def STP(lab, expr='', cls=''): return st(f'<div class="stp {cls}"><span class="lab">{lab}</span>{expr}</div>')
def STEPS(*rows): return '<div class="stps">' + ''.join(rows) + '</div>'
def VC(items, cls=''): return f'<div class="voc3 {cls}">' + ''.join(st(f'<div><b>{w}</b><i>{e}</i><span>{d}</span></div>') for w, e, d in items) + '</div>'
def FLIPS(items, style='flex:1'):
    items = [tuple(x) + ('',) * (3 - len(x)) for x in items]   # السبب (العنصر الثالث) اختياري
    return '<div class="row">' + ''.join(st(f'<button class="flip box col" style="{style}">{q}<span class="tap">👆</span><span class="hid col"><span class="kk c-we">{a_}</span>' + (f'<span class="why">{w}</span>' if w else '') + '</span></button>') for q, a_, w in items) + '</div>'
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

def LDIV(dvd, dvs, q='', size=420):
    # القسمة المطوّلة كما في الكتاب: المقسوم عليه يميناً خلف الخط العمودي، والمقسوم تحت الخط، والناتج فوقه (أرقامٌ عربية، والفاصلة ٫)
    n = max(len(dvd), len(q)); cw = 44; W = n * cw + 150; xr = W - 110
    out = [f'<line x1="{xr}" y1="78" x2="10" y2="78" stroke="#0E1B33" stroke-width="5"/>',
           f'<path d="M{xr},78 Q{xr + 16},112 {xr},146" fill="none" stroke="#0E1B33" stroke-width="5"/>',
           f'<text x="{xr + 60}" y="132" text-anchor="middle" font-size="60" {_FF} fill="#DB2777">{_a(dvs)}</text>',
           f'<text x="{xr - 18}" y="132" text-anchor="end" font-size="60" {_FF} fill="#0E1B33" style="letter-spacing:6px">{_a(dvd)}</text>']
    if q: out.append(f'<text x="{xr - 18}" y="62" text-anchor="end" font-size="60" {_FF} fill="#16A34A" style="letter-spacing:6px">{_a(q)}</text>')
    return f'<svg class="svgfig ldiv" viewBox="0 0 {W} 160" width="{size}" xmlns="http://www.w3.org/2000/svg" style="direction:ltr">{"".join(out)}</svg>'
FRAC_CSS += '''
.slide .svgfig.ldiv{width:auto;height:min(30vh,280px);max-width:46vw;max-height:none}
.slide .svgfig.nline{width:min(1500px,86vw);height:auto;max-height:none}
'''
FRAC_CSS += '''
.slide .box.col>.m,.slide .box.col>b>.m{font-size:clamp(40px,8vh,96px)}
.slide .box.col>b{font-size:clamp(28px,5.4vh,64px)}
'''

def MX(w, n, d): return f'<span class="mx">{w}{FR(n, d)}</span>'   # عددٌ كسري: العدد الكامل يمين الكسر (كما في الكتاب)
def WHOLES(den, num, rows=1, color='#F59E0B'):
    # num جزءاً من أجزاءٍ حجمها 1/den موزّعة على مستطيلاتٍ متطابقة (كل مستطيلٍ واحدٌ صحيح)؛ يبدأ التظليل من المستطيل الأيمن
    k = max(1, -(-num // den)); return '<div class="wholes">' + ''.join(FBAR(den, min(den, num - i * den), rows=rows, color=color, label=False, w=260 if rows > 1 else 300) for i in range(k)) + '</div>'
FRAC_CSS += '''
.mx{display:inline-flex;align-items:center;gap:.12em;direction:rtl;unicode-bidi:isolate}
.wholes{display:flex;gap:1.6vw;justify-content:center;align-items:center;direction:rtl}
.slide .wholes .svgfig.fbar{height:min(30vh,280px);width:auto;max-width:26vw}
'''

def QBAR(total, den, num, unit='', color='#16A34A', w=900):
    # نموذج الشريط لكسرٍ من كمية: شريطٌ طوله الكمية (مكتوبةٌ فوقه) مقسومٌ إلى den جزءاً، في كلٍّ منها total/den، ويُظلَّل num جزءاً من اليمين ويُكتب ناتجها تحته
    part = total // den; cw = w / den; h = 110; y0 = 70; out = []
    out.append(f'<path d="M4,{y0 - 14} L4,{y0 - 30} L{w + 4},{y0 - 30} L{w + 4},{y0 - 14}" fill="none" stroke="#0E1B33" stroke-width="4"/>')
    out.append(f'<text x="{w / 2 + 4}" y="{y0 - 40}" text-anchor="middle" direction="rtl" font-size="44" {_FF} fill="#0E1B33">{_a(total)} {unit}</text>')
    for i in range(den):
        x = 4 + w - (i + 1) * cw; sh = i < num
        out.append(f'<rect x="{x:.1f}" y="{y0}" width="{cw:.1f}" height="{h}" fill="{color if sh else "#fff"}" stroke="#334155" stroke-width="3"/>')
        if den <= 12: out.append(f'<text x="{x + cw / 2:.1f}" y="{y0 + h / 2 + 15}" text-anchor="middle" font-size="{40 if den <= 8 else 30}" {_FF} fill="{"#fff" if sh else "#334155"}">{_a(part)}</text>')
    out.append(f'<rect x="4" y="{y0}" width="{w}" height="{h}" fill="none" stroke="#0E1B33" stroke-width="5"/>')
    xs = 4 + w - num * cw
    out.append(f'<path d="M{xs:.1f},{y0 + h + 14} L{xs:.1f},{y0 + h + 30} L{w + 4},{y0 + h + 30} L{w + 4},{y0 + h + 14}" fill="none" stroke="{color}" stroke-width="4"/>')
    out.append(f'<text x="{(xs + w + 4) / 2:.1f}" y="{y0 + h + 76}" text-anchor="middle" direction="rtl" font-size="44" {_FF} fill="{color}">{_a(part * num)} {unit}</text>')
    return f'<svg class="svgfig qbar" viewBox="0 0 {w + 8} {y0 + h + 92}" width="{w + 8}" xmlns="http://www.w3.org/2000/svg" style="direction:ltr">{"".join(out)}</svg>'
FRAC_CSS += '''
.slide .svgfig.qbar{width:min(1400px,80vw);height:auto;max-height:46vh}
'''

def DEC(s):
    # كسرٌ عشري بأرقامٍ عربية وفاصلة ٫؛ الرقم المسبوق بـ ^ تعلوه نقطة التكرار: DEC('0.^6^3') ← ٠٫٦̇٣̇
    out, dot = [], False
    for ch in s:
        if ch == '^': dot = True; continue
        c = _a(ch)
        out.append(f'<span class="dot">{c}</span>' if dot else c); dot = False
    return '<span class="dec">' + ''.join(out) + '</span>'
FRAC_CSS += '''
.dec{direction:ltr;unicode-bidi:isolate;display:inline-block}
.dot{position:relative;display:inline-block}.dot::after{content:'•';position:absolute;top:-.62em;left:50%;transform:translateX(-50%);font-size:.6em;color:#DB2777}
'''
