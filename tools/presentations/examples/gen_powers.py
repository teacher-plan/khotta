# مولّد العروض التفاعلية — يعيد استخدام محرّك عرض «الأسس» (base.css / base.js)
# python3 gen_powers.py [ملف_المحتوى.py] [اسم_الخرج.html] [عنوان الصفحة]   — الافتراضي: درس «القوى والجذور»
import re, os, sys
HERE=os.path.dirname(os.path.abspath(__file__)); KIT=os.path.dirname(HERE)
AR = '٠١٢٣٤٥٦٧٨٩'
def a(n):  # أرقام عربية-هندية — خارج وسوم HTML فقط (لا نمسّ class="e2" ونحوها)
    return ''.join(seg if seg.startswith('<') else ''.join(AR[int(c)] if c.isdigit() else c for c in seg) for seg in re.split(r'(<[^>]*>)', str(n)))
def N(v): return f'<span class="ng"><i>−</i>{a(v)}</span>'  # السالب: الإشارة يمين العدد
def PN(v, e): return f'<span class="b"><span>({N(v)})</span><sup>{a(e)}</sup></span>'
def P(b, e=None):  # أساس بأسٍّ
    return f'<span class="b">{a(b)}' + (f'<sup>{a(e)}</sup>' if e is not None else '') + '</span>'
X = '<span class="x">×</span>'
EQ = '<span class="eq">=</span>'
PL = '<span class="x">+</span>'
def M(*parts, cls=''): return f'<span class="m {cls}">' + ' '.join(parts) + '</span>'
def R(v, k=2):  # جذرٌ مرسوم من اليمين لليسار: ذيلٌ صغير يميناً ثم نزولٌ فصعودٌ متّصل بالخط العلوي فوق العدد
    v=str(v)
    inner = N(v[1:]) if v.startswith('−') else a(v)
    idx = f'<i class="ri">{a(k)}</i>' if k==3 else ''
    return (f'<span class="rt">{idx}<svg class="rsv" viewBox="0 0 32 64" preserveAspectRatio="none" aria-hidden="true">'
            f'<path d="M31 38 L25 34 L15 62 L1 1.5"/></svg><span class="ov">{inner}</span></span>')
def rep(b, n): return X.join(P(b) for _ in range(n))

MODES = {'i': ('أنا', 'المعلّم يحلّ ويشرح', '👨‍🏫', 'i'), 'we': ('نحن', 'نحلّ معاً', '🤝', 'we'), 'u': ('أنتم', 'دوركم الآن', '✍️', 'u')}
def mode(k): t, s, ic, c = MODES[k]; return f'<div class="mode {c}"><span class="ic">{ic}</span><b>{t}</b><small>{s}</small></div>'
def timer(mins): return f'<button class="timer" data-s="{mins*60}"><span class="tt">{a(mins)}:٠٠</span><span class="tl">▶ ابدأ المؤقّت</span></button>'
def quiz(q, choices, ok, why, badge=None):
    ch = ''.join(f'<button class="ch">{c}</button>' for c in choices)
    return (f'<span class="qbadge">{badge}</span>' if badge else '') + f'<h2>{q}</h2><div class="q" data-ok="{ok}">{ch}</div><div class="fb" data-why="{why.replace(chr(34), "&quot;").replace("<","&lt;").replace(">","&gt;")}"></div>' + f'<aside class="tnote">الإجابة: {choices[ok]}<br>{why}</aside>'
def slide(inner, cls=''): return f'<section class="slide {cls}">{inner}</section>'
def st(inner, tag='div', cls=''): return f'<{tag} class="st {cls}">{inner}</{tag}>'
def box(inner, cls='', style=''): return f'<div class="box {cls}" style="{style}">{inner}</div>'

SLIDES = sys.argv[1] if len(sys.argv) > 1 else 'powers_slides.py'
OUT = sys.argv[2] if len(sys.argv) > 2 else 'القوى_والجذور_عرض_تفاعلي.html'
TITLE = sys.argv[3] if len(sys.argv) > 3 else 'القوى والجذور — الصف السابع'
exec(open(os.path.join(HERE,'common_slides.py'),encoding='utf-8').read())
exec(open(os.path.join(HERE,SLIDES),encoding='utf-8').read())
resolve_pages(S)
resolve_launch(S)   # شرائح الانطلاق إلى تمارين الكتابين (jump.js)

EXTRA_CSS = '''
.c-i{color:#2563EB}.c-we{color:#16A34A}.c-u{color:#EA580C}.c-b{color:var(--base)}.c-exp{color:var(--exp)}
.mode{display:flex;align-items:center;gap:.6em;padding:.45em 1.2em;border-radius:99px;font-size:clamp(16px,2.4vh,26px);border:3px solid;background:#fff}
.mode .ic{font-size:1.3em}.mode b{font-family:var(--fh);font-weight:900;font-size:1.25em}.mode small{font-weight:700;color:var(--ink2)}
.mode.i{border-color:#2563EB;color:#2563EB}.mode.we{border-color:#16A34A;color:#16A34A}.mode.u{border-color:#EA580C;color:#EA580C}
.slide:has(.mode.i){background:linear-gradient(90deg,transparent 0 calc(100% - 14px),#2563EB 0) }
.slide:has(.mode.we){background:linear-gradient(90deg,transparent 0 calc(100% - 14px),#16A34A 0)}
.slide:has(.mode.u){background:linear-gradient(90deg,transparent 0 calc(100% - 14px),#EA580C 0)}
.ask{font-size:clamp(18px,2.8vh,30px);font-weight:800;color:#16A34A}
.hint{font-size:clamp(14px,2vh,20px);font-weight:700;color:var(--ink2)}
.divider h2{font-size:clamp(30px,6vh,64px)}
.plan{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:1.4vh 1.2vw;width:min(1100px,90vw)}
.plan div{background:#fff;border:2.5px solid var(--line);border-radius:16px;padding:1.4vh 1vw;font-weight:800;font-size:clamp(15px,2.3vh,24px);display:flex;flex-direction:column;gap:.3em;align-items:center;text-align:center}
.plan b{font-family:var(--fh);color:var(--exp);font-size:1.3em}
.grid{display:grid;gap:5px}.grid i{display:block;width:clamp(26px,5.5vh,58px);aspect-ratio:1;border-radius:7px;background:#CFE9EC;border:2px solid var(--base)}
.g5{grid-template-columns:repeat(5,auto)}.g3{grid-template-columns:repeat(3,auto)}
.grid.st i{opacity:0;transform:scale(.3);transition:all .3s}
.grid.st.in i{opacity:1;transform:none}
''' + ''.join(f'.grid.st.in i:nth-child({k+1}){{transition-delay:{k*0.05:.2f}s}}' for k in range(25)) + '''
.g3 i{background:#FCE3DD;border-color:var(--exp)}
.layers small{font-weight:800;color:var(--ink2);font-size:clamp(14px,2vh,20px)}
.pw{display:flex;flex-direction:column;gap:1.6vh;width:min(1150px,92vw)}
.pwr{display:flex;align-items:center;justify-content:space-between;gap:2vw;background:#fff;border:2.5px solid var(--line);border-radius:18px;padding:1.4vh 2vw}
.rd{font-size:clamp(16px,2.5vh,26px);font-weight:700;color:var(--ink2)}.rd b{color:var(--exp)}
.timer{display:flex;align-items:center;gap:.8em;border:3px solid #EA580C;background:#FFF4EC;color:#9A3412;border-radius:16px;padding:.4em 1.1em;font-family:var(--fh);font-weight:900;cursor:pointer;font-size:clamp(16px,2.4vh,26px)}
.timer .tt{font-size:1.5em;font-variant-numeric:tabular-nums;min-width:3.2ch}
.timer.run{background:#EA580C;color:#fff}.timer.end{animation:shake .4s 3;background:#D63B3B;border-color:#D63B3B;color:#fff}
.sqs{display:grid;grid-template-columns:repeat(10,1fr);gap:1vh .7vw;width:min(1200px,94vw)}
.sqs.c10{grid-template-columns:repeat(5,1fr);width:min(900px,90vw)}.sqs.c4{grid-template-columns:repeat(4,1fr);width:min(1000px,90vw)}
.sq{display:flex;flex-direction:column;align-items:center;gap:.3vh;background:#fff;border:2.5px solid var(--line);border-radius:14px;padding:1vh .3vw;cursor:pointer;font-family:var(--fh);font-weight:900;box-shadow:0 5px 0 #DCE5F0}
.sq .n{font-size:clamp(20px,3.6vh,38px);color:var(--base)}
.sq .v{font-size:clamp(18px,3.2vh,34px);color:var(--exp);min-height:1.3em;visibility:hidden}
.sq.open{background:#FFF7F4;border-color:var(--exp)}.sq.open .v{visibility:visible;animation:pop .4s}
.sqs.c4 .n{font-size:clamp(34px,6vh,64px)}.sqs.c4 .v{font-size:clamp(30px,5.4vh,58px)}
.reveal-all{font-family:var(--fh);font-weight:800;background:none;border:2px dashed var(--ink2);color:var(--ink2);border-radius:12px;padding:.4em 1.2em;cursor:pointer;font-size:clamp(14px,2vh,20px)}
.chips{display:flex;gap:.8vw;flex-wrap:wrap;justify-content:center}
.blank{display:inline-flex;min-width:1.6em;justify-content:center;border:3px dashed var(--exp);border-radius:12px;color:var(--exp);padding:0 .2em}
.e2{color:var(--exp);font-size:.55em;position:relative;top:-.8em}
.arrow{font-size:clamp(26px,4.6vh,48px);color:var(--ink2);transform:rotate(-90deg)}
.exit{display:flex;flex-direction:column;gap:1.4vh;width:min(900px,90vw)}
.exit .st>div{display:flex;align-items:center;gap:1em;background:#fff;border:2.5px solid var(--line);border-radius:16px;padding:1.2vh 1.4vw;font-weight:800;font-size:clamp(20px,3.3vh,36px)}
.exit b{font-family:var(--fh);background:var(--ink);color:#fff;border-radius:50%;width:1.6em;height:1.6em;display:flex;align-items:center;justify-content:center;flex:none}
.pairs{display:flex;flex-direction:column;gap:.6vh;font-family:var(--fh);font-weight:900;font-size:clamp(20px,3.4vh,36px)}
.pairs span{background:#EAF1FA;border-radius:10px;padding:.1em .8em}.pairs .self{background:#FDE7E2;color:var(--exp);border:2px solid var(--exp)}
.fac{font-weight:800;font-size:clamp(17px,2.7vh,28px);color:var(--ink2)}
.kk{font-family:var(--fh);font-size:clamp(20px,3.2vh,34px)}
.even{color:var(--ink2);font-size:clamp(18px,2.8vh,30px)}.odd{color:var(--exp);font-size:clamp(18px,2.8vh,30px)}
button.flip{font:inherit;color:inherit;cursor:pointer}
.rt{display:inline-flex;align-items:stretch;direction:rtl;unicode-bidi:isolate;position:relative;margin-inline-end:.08em;color:var(--ink)}
.rt .rsv{width:.5em;flex:none;overflow:visible;margin-inline-start:.02em}
.rt .rsv path{fill:none;stroke:currentColor;stroke-width:.075em;stroke-linejoin:round;stroke-linecap:round;vector-effect:non-scaling-stroke}
.rt .ov{border-top:.075em solid currentColor;padding:.06em .12em 0;display:inline-flex;align-items:baseline;direction:rtl;line-height:1.08}
.rt .ri{font-style:normal;font-size:.4em;font-weight:700;color:var(--exp);position:absolute;right:-.02em;top:.1em;line-height:1}
'''
EXTRA_JS = '''
  // بطاقات المربعات: ضغطة تكشف، و«اكشف الكل»
  document.querySelectorAll('.sq').forEach(function(b){b.addEventListener('click',function(e){e.stopPropagation();if(!b.classList.contains('open')){b.classList.add('open');tone('step');}});});
  document.querySelectorAll('.reveal-all').forEach(function(b){b.addEventListener('click',function(e){e.stopPropagation();
    b.parentNode.querySelectorAll('.sq').forEach(function(x,i){setTimeout(function(){x.classList.add('open');},i*60);});tone('ok');});});
  // مؤقّت «أنتم»
  document.querySelectorAll('.timer').forEach(function(t){
    var total=+t.dataset.s,left=total,iv=null,tt=t.querySelector('.tt'),tl=t.querySelector('.tl');
    function fmt(s){return ar(Math.floor(s/60))+':'+ar(String(s%60).padStart(2,'0'));}
    t.addEventListener('click',function(e){e.stopPropagation();
      if(iv){clearInterval(iv);iv=null;t.classList.remove('run');tl.textContent='▶ استئناف';return;}
      if(left<=0){left=total;t.classList.remove('end');}
      t.classList.add('run');tl.textContent='⏸ إيقاف';
      iv=setInterval(function(){left--;tt.textContent=fmt(left);if(left<=5&&left>0)tone('step');
        if(left<=0){clearInterval(iv);iv=null;t.classList.remove('run');t.classList.add('end');tl.textContent='انتهى الوقت! ⟲';tone('no');}},1000);
    });
  });
'''
base_css = open(os.path.join(KIT,'base.css'),encoding='utf-8').read()
base_js = open(os.path.join(KIT,'base.js'),encoding='utf-8').read()
base_js = base_js.replace("document.querySelectorAll('.flip')", EXTRA_JS + "\n  document.querySelectorAll('.flip')")
html = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{TITLE}</title>
<style>{open(os.path.join(KIT,'fonts.css'),encoding='utf-8').read()}{base_css}{EXTRA_CSS}{EXTRA_CSS_LESSON}{EXTRA_CSS_LESSON_X}{globals().get('EXTRA_CSS_OWN','')}{open(os.path.join(KIT,'big.css'),encoding='utf-8').read()}{open(os.path.join(KIT,'deco.css'),encoding='utf-8').read()}</style></head><body>
<div class="deck" id="deck">
{chr(10).join(S)}
</div>
<canvas id="fx"></canvas>
<div class="clsbar" id="clsbar" aria-label="الحصة الحية">
  <button id="liveBtn" class="livebtn" title="بدء الحصة الحية بملء الشاشة"><span class="lv-ic">▶</span><span class="lv-lbl">ابدأ الحصة</span></button>
</div>
<nav class="nav2" aria-label="التنقّل بين الشرائح">
  <button id="prev" title="السابق" aria-label="السابق"><svg viewBox="0 0 24 24"><path d="M9 6l6 6-6 6"/></svg></button>
  <button id="next" class="next" title="التالي" aria-label="التالي"><svg viewBox="0 0 24 24"><path d="M15 6l-6 6 6 6"/></svg></button>
</nav>
<script>{base_js}</script><script>{open(os.path.join(KIT,'deco.js'),encoding='utf-8').read()}</script><script>{open(os.path.join(KIT,'jump.js'),encoding='utf-8').read()}</script></body></html>'''
# حدود العرض بوحدة vw تتصغّر مع zoom الشرائح (--ui و--fit و--ar)، فيضيق المربّع عن سطره ويخرج النص منه (iPad):
# نقسمها على معامل التكبير --zz لتبقى بعرضها المرئي الأصلي، ويصغر الخط وحده.
def _unz(css):
    css = re.sub(r'((?:max-|min-)?width):\s*(min\([^;{}()]*vw\)|\d+(?:\.\d+)?vw)', lambda m: f'{m[1]}:calc({m[2]} / var(--zz,1))', css)
    return css + '.slide{--zz:calc(var(--ar,1) * var(--fit,1) * var(--ui,1))}'
html = re.sub(r'<style>(.*?)</style>', lambda m: '<style>' + _unz(m[1]) + '</style>', html, count=1, flags=re.S)
open(os.path.join(HERE,OUT), 'w', encoding='utf-8').write(html)
print(len(S), 'slides')
