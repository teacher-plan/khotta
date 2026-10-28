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

# شارة «كتاب الطالب ص … · تمرين … · الجزئية …» أعلى يسار شرائح حلّ التمارين (طلب الأستاذ عيسى، ٨ أكتوبر).
# صفحة تمرين كتاب الطالب: من PG في ملف الدرس عند تعدّد الصفحات، وإلا من صفحة شريحة الانطلاق.
#   PG = {'تمرين': [(١، '٨٥'), (٨، '٨٦')]} — والمدخل (رقم، 'جزئية'، 'صفحة') يبدأ صفحةً من جزئيةٍ بعينها.
#   مجموعات كتاب الطالب الأخرى بمفتاح src نفسه (مثل 'تمرين ١-١أ'). وتمارين النشاط صفحتها في src («نشاط ص ٦١ · تمرين»).
PG = {}
PARTS = ['أ', 'ب', 'ج', 'د', 'هـ', 'و', 'ز', 'ح', 'ط', 'ي', 'ك', 'ل', 'م', 'ن', 'س', 'ع', 'ف', 'ص']
def plabel(q):
    m = re.match(r'\s*\(([^()]{1,3})\)', re.sub(r'<[^>]+>', '', q))
    return m.group(1) if m else ''

def resolve_pages(S):
    import json as _j
    sbpg = ''
    for i, x in enumerate(S):
        if x.startswith('<!--LAUNCH '):
            c = _j.loads(x[11:-3])
            if c['bk'] == 'sb': sbpg = c['pages']
            continue
        for blk in re.findall(r'<!--PGB (.*?)-->', x):
            c = _j.loads(blk); src = c['src']; parts = c['parts']
            if src.startswith('نشاط'):
                book, pages = 'كتاب النشاط', [re.search(r'ص\s*([٠-٩]+)', src).group(1)]
            else:
                book = 'كتاب الطالب'
                ent = PG.get('تمرين' if src == 'تمارين' else src) or PG.get('تمرين')
                if c['pg']: pages = [c['pg']]
                elif ent:
                    def page_of(part):
                        key = (int(c['num']), PARTS.index(part) if part in PARTS else 0); pgv = ''
                        for e in ent:
                            k = (e[0], PARTS.index(e[1]) if len(e) == 3 else 0)
                            if k <= key: pgv = e[-1]
                        return pgv
                    pages = list(dict.fromkeys(page_of(p) for p in (parts or [''])))
                elif sbpg and ' و ' not in sbpg and 'إلى' not in sbpg: pages = [sbpg]
                else: raise SystemExit(f'صفحة التمرين {c["num"]} غير معروفة: أضف PG في ملف الدرس')
            num = c['num'] if isinstance(c['num'], str) else a(c['num'])
            lab = 'تمارين' if isinstance(c['num'], str) else 'تمرين'
            pp = ''
            if len(parts) == 1: pp = f'<span class="pgb-pt">الجزئية <b>({parts[0]})</b></span>'
            elif len(parts) == 2: pp = f'<span class="pgb-pt" data-all="1">الجزئيتان <b>({parts[0]}) و ({parts[1]})</b></span>'
            elif parts: pp = f'<span class="pgb-pt" data-all="({parts[0]}) – ({parts[-1]})">الجزئيات <b>({parts[0]}) – ({parts[-1]})</b></span>'
            badge = (f'<div class="pgb"><span class="pgb-bk">{"📘" if book == "كتاب الطالب" else "📗"} {book}</span>'
                     f'<span>ص <b>{" و ".join(pages)}</b></span><span>{lab} <b>{num}</b></span>{pp}</div>')
            x = x.replace('<!--PGB ' + blk + '-->', badge)
        S[i] = x

EXLOG = []
def ex(num, title, rule, parts, cols=3, note='', src='تمرين', per=4, pg=None):
    # src: «تمرين» لكتاب الطالب، «نشاط ص ٢٥ · تمرين» لكتاب النشاط.
    # الخط الكبير: أربعة أجزاء على الأكثر في الشريحة (٢×٢) — التمرين الأطول يُقسَّم تلقائياً على شرائح متتالية.
    EXLOG.append((src, num, parts))   # لـ«طابق» التلقائية (auto_interact)
    out = []
    n = -(-len(parts) // per); per = -(-len(parts) // n)   # توزيعٌ متوازن: ٥ أجزاء ← ٣ + ٢ لا ٤ + ١
    for k in range(0, len(parts), per):
        chunk = parts[k:k+per]
        labs = [plabel(q) for q, _ in chunk]
        if not all(labs) or len(set(labs)) < len(labs): labs = [''] * len(chunk)
        dp = [(' data-p="' + l + '"') if l else '' for l in labs]
        cards=''.join(f'<button class="flip xcard"{d}><span class="xq">{q}</span><span class="tap">👆</span><span class="hid xa">{ans}</span></button>' for (q,ans),d in zip(chunk,dp))
        last = k + per >= len(parts)
        bk = 'ab' if src.startswith('نشاط') else 'sb'   # لربط شريحة الانطلاق بسؤالها (jump.js)
        g = EXG.setdefault('تمرين' if src == 'تمارين' else src, len(EXG))                # مجموعة التمارين (يُعاد الترقيم من ١ في كل مجموعة)
        import json as _j
        pgb = '<!--PGB ' + _j.dumps({'src': src, 'num': num, 'parts': [l for l in labs if l], 'pg': pg}, ensure_ascii=False) + '-->'
        out.append(slide(f'''{pgb}<div class="xhead"><h2>{title}</h2></div>
<div class="xrule"><b>القاعدة</b><span>{rule}</span></div>
<div class="xgrid c{min(cols, 2) if len(chunk) > 1 else 1}">{cards}</div>{(tn(note) if ('دليل' in note or 'قرأت' in note) else f'<p class="hint">{note}</p>') if note and last else ''}''', f'exs ex-{bk}' + (f' exq-{bk}-{g}-{num}' if k == 0 else '')))
    return '\n'.join(out)

EXTRA_CSS_LESSON_X = '''
.xhead{display:flex;align-items:center;gap:1.4vw;justify-content:center;flex-wrap:wrap}
.slide>.pgb.pgb{position:absolute;zoom:calc(var(--ar,1) * var(--ui,1));top:1.4vh;left:1.2vw;z-index:4;display:flex;align-items:center;gap:.25em;flex-wrap:wrap;max-width:58vw;direction:rtl;background:#14305C;color:#fff;border-radius:14px;padding:.3em .8em;font-family:var(--fh);font-weight:700;font-size:clamp(20px,3.6vh,40px);line-height:1.35;box-shadow:0 4px 0 #0B1E3B}
.pgb>span+span::before{content:'·';margin-inline:.35em;opacity:.7}
.pgb b{font-weight:900;color:#FFD66B}
.pgb .pgb-pt.on b{background:#FFD66B;color:#14305C;border-radius:8px;padding:0 .25em}
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

# ═══════════ أدوات التفاعل (interact.js / interact.css — طلب الأستاذ عيسى، ٢٨ أكتوبر) ═══════════
def _q(s): return str(s).replace('"', '&quot;')
def KEYPAD(q, ans, hint='', why='', long=False):
    # لوحة أرقام: يكتب الطالب الناتج ثم «تحقّق»؛ ans بالأرقام اللاتينية مثل '0.7'
    K = [('7', '٧'), ('8', '٨'), ('9', '٩'), ('del', '⌫'), ('4', '٤'), ('5', '٥'), ('6', '٦'), ('.', '٫'), ('1', '١'), ('2', '٢'), ('3', '٣'), ('0', '٠')]
    keys = ''.join(f'<button data-k="{k}"{" class=kd" if k == "del" else ""}>{t}</button>' for k, t in K) + '<button data-k="go" class="kg">✔ تحقّق</button>'
    return (f'<div class="ixk" data-a="{ans}" data-h="{_q(hint)}" data-w="{_q(why)}"><div class="ixk-q{' long' if long else ''}"><span>{q}</span>'
            f'<span class="ixk-out empty">؟</span><span class="ixk-fb"></span></div><div class="ixk-keys">{keys}</div></div>')
def ORDER(items):
    # اسحب ورتّب: items بالترتيب الصحيح، وتظهر مخلوطة (خلطٌ ثابت لا يساوي الترتيب الصحيح)
    import random
    idx = list(range(len(items))); rnd = random.Random(len(items) * 7 + sum(len(x) for x in items))
    while idx == sorted(idx): rnd.shuffle(idx)
    li = ''.join(f'<div class="ixo-i" data-i="{i}">{items[i]}</div>' for i in idx)
    return f'<div class="ixo"><div class="ixo-l">{li}</div><button class="ixo-go">✔ تحقّق</button><div class="ixo-fb"></div></div>'
def MATCH(pairs):
    # طابق: المسائل يميناً ونواتجها مخلوطة يساراً؛ يلمس الطالب مسألةً ثم ناتجها
    import random
    idx = list(range(len(pairs))); rnd = random.Random(len(pairs) * 13)
    while idx == sorted(idx): rnd.shuffle(idx)
    A = ''.join(f'<button class="ixm-i" data-m="{i}">{q}</button>' for i, (q, _) in enumerate(pairs))
    B = ''.join(f'<button class="ixm-i" data-m="{i}">{pairs[i][1]}</button>' for i in idx)
    return f'<div class="ixm"><div class="ixm-cols"><div class="ixm-a">{A}</div><div class="ixm-b">{B}</div></div><div class="ixm-fb"></div></div>'
def TEAMS():
    # شريحة بدء منافسة الفريقين: بعدها تظهر لوحة النقاط أسفل كل الشرائح، وبعد كل إجابة صحيحة «النقطة لمن؟»
    return slide('''<span class="qbadge">منافسة 🏆</span><h2>منافسة الفريقين</h2>
<div class="ixt-teams"><div class="a">🔵 الفريق الأزرق</div><div class="b">🔴 الفريق الأحمر</div></div>
<button class="ixt-start">▶ ابدأ المنافسة</button>''' + tn('قسّم الصف فريقين (مثلاً نصف الصف الأيمن والأيسر). بعد كل إجابة صحيحة في سؤالٍ أو لوحة أرقام أو ترتيب أو مطابقة يسألك العرض «النقطة لمن؟». ويمكنك لمس اسم الفريق أسفل الشاشة لإضافة نقطة، و↺ للتراجع.'))
def TEAMS_END():
    return slide('''<span class="qbadge">منافسة 🏆</span><h2>نتيجة المنافسة</h2>
<button class="ixt-end">🏆 أعلن الفائز</button><div class="ixt-win"></div>''')
def WHERE(title, items, note=''):
    # أين أرى هذا؟ ثلاثة مواقف يومية، كلٌّ بطاقة تُكشف عمليتها بلمسة
    cards = ''.join(st(f'<button class="flip box"><span class="wi">{ic}</span><span class="wt">{t}</span><span class="tap">👆</span><span class="hid">{r}</span></button>') for ic, t, r in items)
    return slide(f'''<span class="qbadge">أين أرى هذا؟ 🌍</span><h2>{title}</h2><div class="ixw">{cards}</div>''' + (tn(note) if note else ''))

# ═══════════ أدوات التفاعل التلقائية في كل عرض (طلب الأستاذ عيسى، ٢٨ أكتوبر: «طبّقها في كل درس كتنويعٍ لطرق الحل») ═══════════
# - منافسة الفريقين: تبدأ بعد شريحة خطة كل حصة، وتُعلن النتيجة في آخرها.
# - لوحة الأرقام: كل سؤال «أنتم» ثانٍ ناتجه عددٌ واحد يصير لوحة أرقام بدل الاختيار من متعدد.
# - اسحب ورتّب: بعد أول مثالٍ محلول بخطوات (STEPS) شريحة «رتّب خطوات الحل».
# - طابق: قبل بطاقة الخروج الأخيرة، أربع مسائل من تمارين الكتاب مع نواتجها.
# - أين أرى هذا؟: من where_data.py قبل خطة الحصة الأولى.
# لإيقافها في عرضٍ بعينه: NO_AUTO_INTERACT = True في ملف الدرس.
import html as _html
QUIZ_LOG = []; _QN = [0]; _quiz0 = quiz
def _txt(h): return ' '.join(_html.unescape(re.sub(r'<[^>]+>', ' ', str(h))).split())
def _latin(t):
    t = t.translate(str.maketrans('٠١٢٣٤٥٦٧٨٩٫', '0123456789.')).replace(' ', '')
    return t if re.fullmatch(r'\d+(\.\d+)?', t) else None
def quiz(q, choices, ok, why, badge=None):
    ans = _txt(choices[ok]); num = _latin(ans); QUIZ_LOG.append((q, choices[ok], num))
    if num is not None and not globals().get('NO_AUTO_INTERACT'):
        _QN[0] += 1
        if _QN[0] % 2 == 0:
            qq = re.sub(r'=\s*؟\s*$', '=', q.strip())
            return ((f'<span class="qbadge">{badge}</span>' if badge else '') + '<h2>اكتب الناتج ثم «تحقّق»</h2>'
                    + KEYPAD(qq, num, hint='راجع خطواتك وحاول مرة أخرى', why=why, long=len(_txt(qq)) > 22)
                    + tn(f'لوحة أرقام (بدل الاختيار من متعدد للتنويع): يأتي طالبٌ إلى الشاشة ويكتب الناتج. الإجابة: {choices[ok]}<br>{why}'))
    return _quiz0(q, choices, ok, why, badge)
def _cls(sl): m = re.match(r'<section class="slide ([^"]*)"', sl); return m[1] if m else ''
def auto_interact(S):
    if globals().get('NO_AUTO_INTERACT'): return S
    W = globals().get('WHERE_DATA', {}).get(os.path.basename(SLIDES))
    # اسحب ورتّب بعد أول مثالٍ محلول بخطوات
    for i, sl in enumerate(S):
        if globals().get('AUTO_ORDER', True) and 'class="stps"' in sl and 'mode i' in sl:
            st_ = re.findall(r'<div class="stp[^"]*"><span class="lab">(.*?)</span>(.*?)</div></div>', sl, re.S)
            st_ = [(re.sub(r'^\s*[٠-٩0-9]+\)\s*', '', l), e) for l, e in st_]   # بلا أرقام الخطوات، وإلا رتّبها الطالب بالأرقام
            items = [((l + (': ' + e if _txt(e) else '')) if _txt(l) else e) for l, e in st_]
            h = re.search(r'<h2[^>]*>(.*?)</h2>', sl, re.S); ht = _txt(h[1]) if h else ''
            seq = ht[:1] in '٠١٢٣٤٥٦٧٨٩' or ht.split(' ')[0] in ('أوجد', 'حوّل', 'اكتب', 'رتّب', 'احسب', 'بسّط', 'الطريقة', 'قرّب', 'حلّ', 'اجمع', 'اطرح', 'اضرب', 'اقسم')
            if seq and not any(re.search(r'(^|\s)أو\s|لماذا', _txt(x)) for x in items) and 3 <= len(items) <= 5 and len({_txt(x) for x in items}) == len(items):
                S.insert(i + 1, slide(f'<div class="row hdr">{mode("we")}<span class="qbadge">اسحب ورتّب ↕️</span></div><h2>رتّب خطوات: {h[1] if h else "الحل"}</h2>' + ORDER(items)
                                      + tn('يسحب طالبٌ البطاقات بإصبعه إلى ترتيبها، ثم «تحقّق»: الخضراء في مكانها والحمراء لا. استرجاعٌ لخطوات المثال السابق بلا النظر إليه.')))
            break
    # طابق: من تمارين كتاب الطالب أولاً ثم كتاب النشاط، وإلا من أسئلة الحصة
    def ok_(h): return not re.search(r'<img|<table|vcol|<svg|<br|class="fig', str(h))
    pairs = []
    for src, num, parts in sorted(EXLOG, key=lambda e: e[0] != 'تمرين'):
        c = []
        for q, a_ in parts:
            q = re.sub(r'^\(\S+\)\s*', '', q); a_ = re.sub(r'<small>.*?</small>', '', str(a_), flags=re.S)
            if not (ok_(q) and ok_(a_) and 0 < len(_txt(q)) <= 24): continue
            if '=' in _txt(a_):   # «٤ + ٦ = ١٠» ← الناتج وحده، وإلا كشف الجوابُ السؤال
                if 'class="fr"' in str(a_): continue
                a_ = _txt(a_).split('=')[-1].strip()
                m_ = re.match(r'^([−\d٠-٩٫\s]+?)\s+(نطرح|نضيف|نقسم|نضرب)', a_)
                if m_: a_ = m_[1]
            at = _txt(a_)
            if not (0 < len(at) <= 14) or at[:1] in '<>≠≤≥=' or _txt(q) in at: continue
            c.append((q, a_))
        seen, c2 = set(), []
        for q, a_ in c:
            if _txt(a_) not in seen: seen.add(_txt(a_)); c2.append((q, a_))
        box = [x for x in c2 if '☐' in x[0]]; nob = [x for x in c2 if '☐' not in x[0]]
        c2 = box if len(box) > len(nob) else nob   # نوعٌ واحد من الأسئلة في الشريحة
        if len(c2) >= 3: pairs = c2[:4]; break
    if not pairs:
        seen = set()
        for q, ch, num in QUIZ_LOG:
            qq = re.sub(r'=\s*؟\s*$', '', q.strip()).strip()
            if num and ok_(qq) and len(_txt(qq)) <= 24 and num not in seen: seen.add(num); pairs.append((qq, ch))
        pairs = pairs[:4] if len(pairs) >= 3 else []
    if pairs:
        ex_i = [i for i, sl in enumerate(S) if 'بطاقة الخروج' in sl and '>الإجابات</h2>' not in sl]
        at = ex_i[-1] if ex_i else next((i for i, sl in enumerate(S) if sl.startswith('<!--LAUNCH')), len(S))
        S.insert(at, slide(f'<div class="row hdr">{mode("u")}<span class="qbadge">طابق 🔗</span></div><h2>المس المسألة ثم ناتجها</h2>' + MATCH(pairs)
                           + tn('مسائل من تمارين الكتاب: يلمس الطالب المسألة ثم ناتجها؛ الصحيحة تتلوّن بلونٍ واحد، والخاطئة تهتزّ.')))
    # منافسة الفريقين في كل حصة، و«أين أرى هذا؟» قبل الحصة الأولى
    dv = [i for i, sl in enumerate(S) if 'divider' in _cls(sl).split()]
    ln = next((i for i, sl in enumerate(S) if sl.startswith('<!--LAUNCH')), len(S))
    ins = [(ln, TEAMS_END())] if dv else []
    for k, i in enumerate(dv):
        ins.append((i + 1, TEAMS()))
        if k: ins.append((i, TEAMS_END()))
    if not dv: ins += [(min(3, len(S)), TEAMS()), (ln, TEAMS_END())]
    if W: ins.append((dv[0] if dv else min(3, len(S)), WHERE(W['title'], W['items'], W.get('note', 'مواقف من بيئة الطالب (من خارج المرجع). اسأل: «أي عمليةٍ نحتاج؟» ثم المس البطاقة لتكشف العملية والناتج.'))))
    for i, h in sorted(ins, key=lambda x: -x[0]): S.insert(i, h)
    return S
