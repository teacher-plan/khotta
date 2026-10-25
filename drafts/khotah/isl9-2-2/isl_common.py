# أدوات مشتركة لعروض التربية الإسلامية بطريقة «اقرأ ← نظّم ← ثبّت» (من نسخة المكيّ والمدنيّ ٢)
use('frac_common')
QF = open(os.path.join(HERE, 'amiri_quran.css'), encoding='utf-8').read()
FF = open(os.path.join(HERE, 'fonts_sub.css'), encoding='utf-8').read() if os.path.exists(os.path.join(HERE, 'fonts_sub.css')) else ''
def AY(t, ref_=''):
    return f'<span class="ayah">﴿{t}﴾</span>' + (f'<span class="aref">[{ref_}]</span>' if ref_ else '')
def MK(t): return f'<b class="mk">{t}</b>'
def MD(t): return f'<b class="md">{t}</b>'
def KW(t): return f'<button class="kw" onclick="event.stopPropagation();this.classList.add(\'on\')"><span>{t}</span></button>'   # كلمةٌ مفتاحية تُكشف بضغطة
def READ(pg, sentence, note=''):   # «اقرأ»: الجملة المفتاحية للفقرة
    return f'<div class="row hdr"><span class="stage s1">١ اقرأ</span>{ref("كتاب الطالب ص " + pg)}</div>' + f'<div class="keyline st">{sentence}</div>'
def STAGE(n): return {2: '<span class="stage s2">٢ نظّم</span>', 3: '<span class="stage s3">٣ ثبّت</span>'}[n]
def SORT(items, opts=('مكّيّة', 'مدنيّة'), cols=2):   # لعبة تصنيف: لكلّ بطاقةٍ أزرار، والصحيح يتلوّن والخطأ يهتزّ
    cls = ['o-mk', 'o-md', 'o-x']
    out = []
    for q, ok, *w in items:
        bt = ''.join(f'<button class="sb {cls[i] if len(opts) == 2 else "o-" + str(i)}" onclick="srt(event,this,{i})">{o}</button>' for i, o in enumerate(opts))
        out.append(st(f'<div class="sc" data-ok="{ok}"><div class="sqx">{q}</div><div class="sbs">{bt}</div>' + (f'<div class="sw">{w[0]}</div>' if w else '') + '</div>'))
    return f'<div class="sort c{cols}">' + ''.join(out) + '</div>'
TF = lambda items: SORT(items, ('✔ صواب', '✘ خطأ'))


def ISL_FINISH():
    global EXTRA_CSS_OWN
    SCRIPT = '''<script>
    function srt(e,b,i){e.stopPropagation();var c=b.closest('.sc');if(c.classList.contains('done'))return;
     if(+c.dataset.ok===i){c.classList.add('done');b.classList.add('ok');}
     else{b.classList.add('bad');c.classList.remove('shk');void c.offsetWidth;c.classList.add('shk');setTimeout(function(){b.classList.remove('bad')},700);}}
    </script>'''
    S[-1] = S[-1].replace('</section>', SCRIPT + '</section>')
    
    EXTRA_CSS_OWN = FF + QF + '''
    :root:root{--fh:'Noto Kufi Arabic',Tahoma,sans-serif;--fb:'Noto Naskh Arabic','Noto Kufi Arabic',Tahoma,serif;--mkc:#9A4A0C;--mdc:#0B6B4F;--gold:#B8892B;--navy:#123A5A}
    body,.slide{font-family:var(--fb)}
    .slide h1,.slide h2{color:var(--navy);font-weight:800}
    .lead,.hint,.keyline,.sqx,.cmp td,.t-k span,.pan li,.lamp span,.fan span,.mm-b span,.ex3 span,.way span{font-family:var(--fb);font-weight:700}
    .ayah{font-family:'Amiri Quran','Amiri',serif;font-size:clamp(28px,5.4vh,64px);line-height:1.9;color:#0B3D2E;font-weight:400}
    .sqx .ayah,.pan .ayah,.sort .ayah{font-size:1.15em;line-height:1.6}
    .aref{font-family:var(--fb);font-size:clamp(20px,3.8vh,42px);color:#6B6250;margin-inline-start:.5em;white-space:nowrap}
    .ayahbox{background:#F6FAF4;border:2px solid #C9DCC4;border-radius:14px;padding:1vh 3vw;text-align:center;max-width:86vw}
    .mk{color:var(--mkc)}.md{color:var(--mdc)}
    .lead{font-size:clamp(22px,4.4vh,50px);color:#2B2B2B;text-align:center;text-wrap:balance}
    .hint{font-size:clamp(18px,3.6vh,40px);color:#5B5B5B}
    .stage{font-family:var(--fh);font-weight:800;font-size:clamp(20px,3.6vh,40px);padding:.2em .9em;border-radius:10px;color:#fff}
    .s1{background:var(--navy)}.s2{background:var(--gold)}.s3{background:#0B6B4F}
    .slide:has(.stage.s1){background:linear-gradient(90deg,transparent 0 calc(100% - 12px),var(--navy) 0)}
    .slide:has(.stage.s2){background:linear-gradient(90deg,transparent 0 calc(100% - 12px),var(--gold) 0)}
    .slide:has(.stage.s3){background:linear-gradient(90deg,transparent 0 calc(100% - 12px),#0B6B4F 0)}
    .keyline{font-size:clamp(28px,6vh,70px);line-height:1.9;text-align:center;max-width:84vw;color:#1F1F1F;font-weight:700;text-wrap:balance}
    .kw{font:inherit;color:transparent;background:none;border:0;border-bottom:.08em dashed var(--gold);cursor:pointer;padding:0 .15em;position:relative;transition:color .3s}
    .kw::after{content:"؟";position:absolute;inset:0;display:flex;align-items:center;justify-content:center;color:var(--gold);font-family:var(--fh)}
    .kw.on{color:var(--mdc);border-bottom:.08em solid var(--mdc);background:#EAF4EE;border-radius:6px}.kw.on::after{content:none}
    .way{display:grid;grid-template-columns:repeat(3,1fr);gap:2vw;width:86vw}
    .way>div>div{border-radius:16px;padding:3vh 1.5vw;display:flex;flex-direction:column;gap:1.4vh;text-align:center;border:2px solid #E3DED2;background:#fff}
    .way b{font-family:var(--fh);font-size:clamp(30px,6vh,70px)}.way span{font-size:clamp(20px,4vh,46px);line-height:1.5}
    .w1 b{color:var(--navy)}.w2 b{color:var(--gold)}.w3 b{color:#0B6B4F}
    .tl{display:flex;align-items:stretch;width:84vw;border-radius:16px;overflow:hidden;border:2px solid #D8D2C4}
    .tl>div{display:flex;flex-direction:column;align-items:center;justify-content:center;padding:2.4vh 1vw;gap:.6vh}
    .tl-mk{flex:13;background:#FBF1E6}.tl-md{flex:10;background:#E9F4EF}.tl-h{flex:0 0 auto;background:var(--navy);color:#fff}
    .tl b{font-family:var(--fh);font-size:clamp(26px,5.4vh,62px)}.tl span{font-size:clamp(20px,4vh,46px);font-weight:700}
    .tl-mk b{color:var(--mkc)}.tl-md b{color:var(--mdc)}.tl-h b{color:#fff;font-size:clamp(22px,4.2vh,48px)}
    .cmp{border-collapse:separate;border-spacing:0;width:88vw;background:#fff;border:2px solid #D8D2C4;border-radius:14px;overflow:hidden}
    .cmp th,.cmp td{padding:1vh 1.2vw;border-bottom:1px solid #ECE7DC;font-size:clamp(20px,3.6vh,40px);line-height:1.4;text-align:center}
    .cmp thead th{font-family:var(--fh);font-size:clamp(22px,4.2vh,48px);background:#FAF7F0}
    .cmp tbody th{font-family:var(--fh);color:var(--navy);background:#FAF7F0;white-space:nowrap;width:14%}
    .cmp tbody td:nth-child(2){background:#FFFBF6}.cmp tbody td:nth-child(3){background:#F7FBF9}
    .cmp tr.st{display:table-row}
    .sort{display:grid;gap:1.4vh 1.4vw;width:88vw}.sort.c2{grid-template-columns:1fr 1fr}.sort.c1{grid-template-columns:1fr}
    .sc{display:flex;align-items:center;gap:1.2vw;background:#fff;border:2px solid #E3DED2;border-radius:14px;padding:1vh 1.2vw;transition:border-color .3s,background .3s}
    .sqx{flex:1;font-size:clamp(22px,4.2vh,48px);line-height:1.45}
    .sbs{display:flex;gap:.6vw;flex:0 0 auto}
    .sb{font-family:var(--fh);font-weight:800;font-size:clamp(20px,3.6vh,40px);padding:.25em .8em;border-radius:10px;border:2px solid;background:#fff;cursor:pointer}
    .o-mk{color:var(--mkc);border-color:#E6C9AE}.o-md{color:var(--mdc);border-color:#B6DACB}
    .sb.ok{color:#fff}.o-mk.ok{background:var(--mkc);border-color:var(--mkc)}.o-md.ok{background:var(--mdc);border-color:var(--mdc)}
    .sb.bad{background:#FDECEC;border-color:#D64545;color:#B42318}
    .sc.done{border-color:#0B6B4F;background:#F5FBF7}.sc.done .sb:not(.ok){opacity:.3}
    .sw{display:none;font-size:clamp(16px,3vh,32px);color:#0B6B4F;font-weight:700}.sc.done .sw{display:block}
    .sc.shk{animation:shk .45s}@keyframes shk{20%,60%{transform:translateX(8px)}40%,80%{transform:translateX(-8px)}}
    .rule{display:flex;align-items:baseline;gap:1.2vw;padding:1.6vh 3vw;border:2px solid var(--gold);border-radius:14px;background:#FFFBF0}
    .rule span{font-size:clamp(22px,4.4vh,50px);font-weight:700}.rule b{font-family:var(--fh);font-size:clamp(30px,6.4vh,72px);color:var(--gold)}
    .axis{display:flex;width:86vw;align-items:stretch;gap:0}
    .axis>div{display:flex;flex-direction:column;align-items:center;justify-content:center}
    .axis .st{flex:1;display:flex}.axis .st>div{flex:1;width:100%;box-sizing:border-box}.axis .st>div{padding:1.6vh 1vw;display:flex;flex-direction:column;align-items:center;gap:.4vh;border-radius:14px}
    .ax-mk{background:#FBF1E6}.ax-md{background:#E9F4EF}
    .ax-mid{padding:0 1.4vw}.ax-mid b{font-family:var(--fh);background:var(--navy);color:#fff;padding:.4em .8em;border-radius:10px;font-size:clamp(20px,4vh,44px)}
    .axis b{font-family:var(--fh);font-size:clamp(26px,5vh,58px)}.ax-mk b{color:var(--mkc)}.ax-md b{color:var(--mdc)}.axis span{font-size:clamp(18px,3.6vh,40px);font-weight:700}
    .ex3{display:flex;flex-wrap:wrap;gap:1vh 1.4vw;justify-content:center;max-width:88vw}
    .ex3 span{background:#fff;border:2px solid #E3DED2;border-radius:12px;padding:.6vh 1.2vw;font-size:clamp(18px,3.6vh,40px)}
    .tree2{display:flex;flex-direction:column;align-items:center;gap:2vh;width:88vw}
    .t-root{font-family:var(--fh);font-weight:800;font-size:clamp(22px,4.4vh,50px);background:var(--navy);color:#fff;padding:.4em 1.4em;border-radius:12px}
    .t-kids{display:grid;grid-template-columns:1fr 1fr;gap:2vw;width:100%}
    .t-k{display:flex;flex-direction:column;gap:1vh;align-items:center;text-align:center;background:#fff;border:2px solid #E3DED2;border-top:8px solid;border-radius:14px;padding:2vh 1.4vw}
    .k1{border-top-color:var(--gold)}.k2{border-top-color:#0B6B4F}
    .t-k b{font-family:var(--fh);font-size:clamp(26px,5vh,58px)}.k1 b{color:var(--gold)}.k2 b{color:#0B6B4F}
    .t-k span{font-size:clamp(19px,3.7vh,42px);line-height:1.5}.t-k em{font-style:normal;font-family:var(--fh);font-size:clamp(18px,3.4vh,38px);color:var(--navy)}
    .two{display:grid;grid-template-columns:1fr 1fr;gap:2vw;width:88vw}
    .pan{background:#fff;border:2px solid;border-radius:14px;padding:1.6vh 1.6vw}.mkp{border-color:#E6C9AE}.mdp{border-color:#B6DACB}
    .pan>b{display:block;font-family:var(--fh);font-size:clamp(24px,4.6vh,52px);margin-bottom:1vh}.mkp>b{color:var(--mkc)}.mdp>b{color:var(--mdc)}
    .pan ul{margin:0;padding-inline-start:1.2em;display:flex;flex-direction:column;gap:.6vh}.pan li{font-size:clamp(18px,3.5vh,40px);line-height:1.45}
    .lamp{display:flex;flex-direction:column;gap:2vh;width:84vw}
    .lamp>div>div{display:flex;flex-direction:column;gap:.8vh;background:#FFFBF0;border:2px solid #EAD9A8;border-radius:14px;padding:1.8vh 2vw}
    .lamp b{font-family:var(--fh);font-size:clamp(24px,4.8vh,54px);color:var(--gold)}.lamp span{font-size:clamp(20px,4vh,46px);line-height:1.5}
    .fan{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1.2vw;width:84vw}
    .fan>div>div{display:flex;flex-direction:column;align-items:center;text-align:center;gap:1vh;background:#fff;border:2px solid #E3DED2;border-radius:14px;padding:2.4vh 1.2vw;height:100%;box-sizing:border-box}
    .fan i{font-style:normal;font-family:var(--fh);width:1.8em;height:1.8em;border-radius:50%;background:var(--gold);color:#fff;display:grid;place-items:center;font-size:clamp(20px,3.8vh,42px)}
    .fan b{font-family:var(--fh);font-size:clamp(24px,4.6vh,52px);color:var(--navy)}.fan span{font-size:clamp(19px,3.7vh,42px);line-height:1.5}
    .mm{display:grid;grid-template-columns:1fr auto 1fr;grid-template-rows:auto auto;gap:2vh 2vw;align-items:center;width:88vw}
    .mm-c{grid-column:2;grid-row:1/3;font-family:var(--fh);font-weight:800;font-size:clamp(26px,5vh,58px);background:var(--navy);color:#fff;border-radius:50%;width:11em;max-width:26vw;aspect-ratio:1;display:grid;place-items:center;text-align:center;line-height:1.4;font-size:clamp(22px,4.2vh,48px)}
    .mm>.st:nth-of-type(1){grid-column:1;grid-row:1}.mm>.st:nth-of-type(2){grid-column:3;grid-row:1}.mm>.st:nth-of-type(3){grid-column:1;grid-row:2}.mm>.st:nth-of-type(4){grid-column:3;grid-row:2}
    .mm-b{display:flex;flex-direction:column;gap:.8vh;background:#fff;border:2px solid #E3DED2;border-radius:14px;padding:1.8vh 1.4vw;text-align:center}
    .mm-b b{font-family:var(--fh);font-size:clamp(24px,4.6vh,52px)}.mm-b span{font-size:clamp(19px,3.7vh,42px);line-height:1.5}
    .b1 b{color:var(--navy)}.b2 b{color:var(--gold)}.b3 b{color:var(--mkc)}.b4 b{color:#0B6B4F}
    .slide .flip{max-width:84vw}.slide .flip span{white-space:normal}
    .box>span:not(.kk):not(.tap),.why,.flip .hid .why{font-size:clamp(20px,4vh,46px)!important;line-height:1.45}
    '''
    EXTRA_CSS_OWN += '.sqx u{text-decoration:none;border-bottom:.1em solid #B42318;color:#B42318}.sqx{text-align:start}'
