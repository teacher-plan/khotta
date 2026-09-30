# دوالّ وأنماط مشتركة بين ملفات محتوى الدروس — تُنفَّذ قبل ملف الدرس (انظر gen_powers.py).
def PM(v): return f'<span class="ng"><i>±</i>{a(v)}</span>'   # ±٥ كما يكتبها الكتاب، والإشارة يمين العدد
def ref(t): return f'<span class="ref">📘 {t}</span>'
def mk(): return '<span class="bk"><span class="blank">؟</span><sup class="e2">٢</sup></span>'  # الأسّ ملتصقٌ بالمربّع الفارغ

def puzzle(who, ic, q, ans):
    return f'<button class="flip box col puz"><span class="who2">{ic} {who}</span><span class="pq">{q}</span><span class="tap">👆 اضغط للحل</span><span class="hid col">{ans}</span></button>'

EXG = {}   # src ← رقم مجموعة التمارين
def tn(t): return f'<aside class="tnote">{t}</aside>'   # ملاحظة للمعلّم: لا تظهر للطلاب إلا في «وضع المعلّم»

def launch(bk, pages, start=None, mins=10, note=''):
    # شريحة الانطلاق إلى تمارين الكتاب (bk: 'sb' كتاب الطالب، 'ab' كتاب النشاط) — يصل إليها زرّ الشريط السفلي مباشرةً.
    # تُترك علامة، ويبنيها gen_powers.py بعد اكتمال الشرائح بأرقام الأسئلة التي تليها (resolve_launch).
    import json as _j
    return '<!--LAUNCH ' + _j.dumps({'bk': bk, 'pages': pages, 'start': start, 'mins': mins, 'note': note}, ensure_ascii=False) + '-->'

def launch_slide(c, groups):
    bk = c['bk']; book = 'كتاب الطالب' if bk == 'sb' else 'كتاب النشاط'
    lab = {v: k for k, v in EXG.items()}
    def glab(g):
        t = lab[g].replace(' · تمرين', '').replace('نشاط ', '')
        return '' if t == 'تمرين' else t
    many = len(groups) > 1
    qs = ''.join((f'<div class="lgrp">' + (f'<span class="lgl">{glab(g)}</span>' if many else '') +
                  ''.join(f'<button class="lq" data-q="{g}-{n}" data-l="{a(n)}{("  (" + glab(g) + ")") if many and glab(g) else ""}">{a(n)}</button>' for n in ns) + '</div>') for g, ns in groups)
    return slide(f'''<span class="tag">{'📘' if bk == 'sb' else '📗'} تمارين {book}</span>
<h2 class="lh">افتحوا {book}، صفحة <span class="lpg">{c['pages']}</span></h2>
<div class="lstart"><span>ونبدأ الحل من السؤال</span><b class="lnum">{a(c['start']) if c['start'] else '؟'}</b></div>
<div class="lqs">{qs}</div>
<div class="row" style="align-items:center"><button class="lgo" hidden>انتقل إلى الحل ←</button>{timer(c['mins'])}</div>''' + tn('اختر رقم السؤال الذي يبدأ منه الطلاب فيظهر لهم كبيراً، ثم «انتقل إلى الحل» عند التصحيح.' + (f'<br>{c["note"]}' if c['note'] else '')), f'launch launch-{bk}" data-bk="{bk}')

def resolve_launch(S):
    import json as _j
    for i, x in enumerate(S):
        if not x.startswith('<!--LAUNCH '): continue
        c = _j.loads(x[11:-3]); groups = {}
        for y in S[i + 1:]:
            if y.startswith('<!--LAUNCH '): break
            for g, n in re.findall(r'exq-%s-(\d+)-(\d+)' % c['bk'], y):
                groups.setdefault(int(g), [])
                if int(n) not in groups[int(g)]: groups[int(g)].append(int(n))
        S[i] = launch_slide(c, [(g, sorted(ns)) for g, ns in groups.items()])

def ex(num, title, rule, parts, cols=3, note='', src='تمرين', per=4):
    # src: «تمرين» لكتاب الطالب، «نشاط ص ٢٥ · تمرين» لكتاب النشاط.
    # الخط الكبير: أربعة أجزاء على الأكثر في الشريحة (٢×٢) — التمرين الأطول يُقسَّم تلقائياً على شرائح متتالية.
    out = []
    n = -(-len(parts) // per); per = -(-len(parts) // n)   # توزيعٌ متوازن: ٥ أجزاء ← ٣ + ٢ لا ٤ + ١
    for k in range(0, len(parts), per):
        chunk = parts[k:k+per]
        cards=''.join(f'<button class="flip xcard"><span class="xq">{q}</span><span class="tap">👆</span><span class="hid xa">{ans}</span></button>' for q,ans in chunk)
        last = k + per >= len(parts)
        bk = 'ab' if src.startswith('نشاط') else 'sb'   # لربط شريحة الانطلاق بسؤالها (jump.js)
        g = EXG.setdefault('تمرين' if src == 'تمارين' else src, len(EXG))                # مجموعة التمارين (يُعاد الترقيم من ١ في كل مجموعة)
        out.append(slide(f'''<div class="xhead"><span class="xnum">📘 {src} {a(num)}</span><h2>{title}</h2></div>
<div class="xrule"><b>القاعدة</b><span>{rule}</span></div>
<div class="xgrid c{min(cols, 2) if len(chunk) > 1 else 1}">{cards}</div>{f'<p class="hint">{note}</p>' if note and last else ''}''', f'exs ex-{bk}' + (f' exq-{bk}-{g}-{num}' if k == 0 else '')))
    return '\n'.join(out)

EXTRA_CSS_LESSON_X = '''
.xhead{display:flex;align-items:center;gap:1.4vw;justify-content:center;flex-wrap:wrap}
.xnum{font-family:var(--fh);font-weight:700;font-size:clamp(20px,3.2vh,34px);background:var(--ink);color:#fff;border-radius:99px;padding:.25em 1em}
.xhead h2{font-size:clamp(28px,5.2vh,58px)}
.xrule{display:flex;align-items:center;gap:1em;background:#FFF6E3;border:3px solid #E9A23B;border-radius:18px;padding:1.1vh 1.6vw;width:min(1150px,92vw);font-weight:700;font-size:clamp(19px,3.1vh,33px);line-height:1.55}
.xrule b{flex:none;background:#E9A23B;color:#fff;border-radius:12px;padding:.15em .7em;font-family:var(--fh)}
.xgrid{display:grid;gap:1.6vh 1.4vw;width:min(1150px,92vw)}
.xgrid.c2{grid-template-columns:repeat(2,minmax(0,1fr))}.xgrid.c3{grid-template-columns:repeat(3,minmax(0,1fr))}.xgrid.c4{grid-template-columns:repeat(4,minmax(0,1fr))}
.xgrid.c4 .xq{font-size:clamp(18px,3vh,32px)}
.xcard{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:.8vh;background:#fff;border:3px solid var(--line);border-radius:18px;padding:1.4vh 1vw;cursor:pointer;font-family:var(--fb);color:var(--ink);box-shadow:0 6px 0 #D4DFEC;min-height:13vh}
.xq{font-weight:700;font-size:clamp(20px,3.4vh,38px);line-height:1.5;text-align:center}
.xq .m{font-size:1.15em}
.xa{font-weight:700;font-size:clamp(19px,3.2vh,35px);color:var(--good);text-align:center;line-height:1.5;flex-direction:column;align-items:center}
.xa .m{color:var(--good)}.xa small{font-size:.6em;color:var(--ink2)}
.xcard.open{border-color:var(--good);background:#F2FBF5}
.xcard .tap{font-size:clamp(16px,2.3vh,24px)}
'''

EXTRA_CSS_LESSON = '''
.sq.pw2 .n{font-size:clamp(20px,3.6vh,38px)}
.sq.pw2 .n .m{gap:.18em}
.sqs.c5{grid-template-columns:repeat(5,minmax(0,1fr));width:min(1100px,90vw)}
.sqs.c5 .n{font-size:clamp(30px,5.2vh,56px)}.sqs.c5 .v{font-size:clamp(30px,5.2vh,56px)}
.h1s{font-size:clamp(48px,10vh,112px)!important}
.can{background:#fff;border:3px solid var(--line);border-radius:22px;padding:1.6vh 2vw;display:flex;flex-direction:column;gap:1.2vh;width:min(1150px,92vw);box-shadow:0 8px 0 #E3EAF4}
.can-t{font-family:var(--fh);font-size:clamp(20px,3.2vh,34px);color:var(--ink2)}
.can>div{display:flex;align-items:center;gap:.8em;font-weight:800;font-size:clamp(20px,3.4vh,37px);line-height:1.55}
.can-i{flex:none;width:1.5em;height:1.5em;border-radius:50%;background:var(--good);color:#fff;display:flex;align-items:center;justify-content:center;font-size:.8em}
.can b{color:var(--ink)}.can .c-b{color:var(--base)}.can .c-exp{color:var(--exp)}
.vocab.wide{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1.2vh 2.4vw;width:min(1100px,90vw);padding:2vh 2vw}
.vocab.wide div{font-size:clamp(22px,3.8vh,40px)}
.ref{font-family:var(--fh);font-weight:800;font-size:clamp(15px,2.2vh,22px);color:#0A6770;background:#E4F4F5;border:2px solid #9ED5D9;border-radius:99px;padding:.2em .9em}
.goals{display:flex;flex-direction:column;gap:1.4vh;flex:1.4;min-width:340px}
.goals .st>div{background:#fff;border:3px solid var(--line);border-radius:16px;padding:1.2vh 1.3vw;font-weight:800;font-size:clamp(19px,3.1vh,33px);line-height:1.6}
.vocab{background:#fff;border:3px solid var(--line);border-radius:18px;padding:1.4vh 1.4vw;display:flex;flex-direction:column;gap:.8vh;min-width:300px}
.vocab>b{font-family:var(--fh);font-size:clamp(20px,3.2vh,34px);text-align:center;color:var(--ink)}
.vocab div{display:flex;justify-content:space-between;gap:1.2vw;font-weight:800;font-size:clamp(17px,2.7vh,29px);border-bottom:2px dashed #DCE6F2;padding-bottom:.4vh}
.vocab i{font-style:normal;direction:ltr;color:#0A6770;font-family:Tahoma,sans-serif}
.chain{display:flex;flex-wrap:wrap;gap:1.4vh 1.2vw;justify-content:center;max-width:1180px}
.chain .box{padding:1.2vh 1.4vw}.chain .box.hot{border-color:var(--exp);background:#FFF1EC;box-shadow:0 0 0 5px rgba(198,58,34,.18)}
.wrong,.right{font-size:clamp(26px,4.4vh,46px);font-weight:900}.wrong{color:var(--bad)}.right{color:var(--good)}
.sq u{text-decoration:none;color:#fff;background:var(--exp);border-radius:8px;padding:0 .12em}
.puz{flex:1;min-width:280px;max-width:390px;gap:1.2vh}
.who2{font-family:var(--fh);font-weight:900;font-size:clamp(22px,3.6vh,38px)}
.pq{font-weight:800;font-size:clamp(18px,2.9vh,31px);line-height:1.6}
'''
