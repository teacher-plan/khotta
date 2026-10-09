# هوية قناة YouTube «أ. عيسى الحارثي» بألوان فيديوهات الدروس وخطّها (Cairo وReadex Pro): صورة الملف، والبانر، وصور الفيديوهات المصغّرة، وأغلفة قوائم التشغيل.
#   python3 youtube_art.py <مجلد الخرج>      ← ملفات PNG/JPG جاهزة للرفع (تُرسم بـ playwright)
import json, os, subprocess, sys

NAVY, NAVY2, YEL, ORG, WHITE = '#14305C', '#0E2347', '#FFE08A', '#E8590C', '#FFFFFF'
UNITS = {
    1: ('الأولى', 'الأعداد الصحيحة والقوى والجذور', '#F59F00', '√٩'),
    2: ('الثانية', 'العبارات الجبرية والمعادلات والصيغ', '#37B24D', 'س + ص'),
    3: ('الثالثة', 'الأعداد العشرية والكسور العشرية', '#4DABF7', '٠٫٥'),
    4: ('الرابعة', 'الطول والكتلة والسعة', '#F06595', 'كغم'),
}
FONT = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cairo:wght@700;800;900&family=Readex+Pro:wght@500;700&display=swap">')
BASE = f'''*{{margin:0;box-sizing:border-box}}html,body{{width:100%;height:100%}}
body{{background:{NAVY};color:{WHITE};font-family:'Cairo',sans-serif;direction:rtl;overflow:hidden;position:relative;
background-image:linear-gradient(rgba(255,255,255,.05) 2px,transparent 2px),linear-gradient(90deg,rgba(255,255,255,.05) 2px,transparent 2px);background-size:64px 64px}}
.hl{{background:linear-gradient(transparent 62%,{YEL}55 62%)}}
.sym{{position:absolute;font-weight:900;opacity:.10;color:{WHITE};direction:ltr}}'''

def page(w, h, body, css=''):
    return f'<!doctype html><html lang="ar"><head><meta charset="utf-8">{FONT}<style>{BASE}{css}</style></head><body style="width:{w}px;height:{h}px">{body}</body></html>'

def scatter(items):  # رموزٌ رياضية خافتة للزينة: (الرمز، يسار٪، أعلى٪، الحجم)
    return ''.join(f'<span class="sym" style="left:{x}%;top:{y}%;font-size:{s}px">{t}</span>' for t, x, y, s in items)

SYMS = [('+', 4, 8, 150), ('÷', 14, 62, 130), ('√', 88, 10, 170), ('×', 92, 66, 140), ('π', 76, 78, 110), ('=', 24, 18, 120),
        ('%', 60, 6, 100), ('²', 46, 80, 120), ('∠', 68, 30, 90), ('٣', 8, 40, 110), ('٧', 96, 38, 90), ('½', 34, 52, 100)]

def profile():
    css = f'''.c{{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:6px}}
.m{{font-size:230px;font-weight:900;line-height:1.2;color:{WHITE}}}.u{{width:420px;height:22px;border-radius:11px;background:{YEL};margin-top:14px}}
.s{{font-family:'Readex Pro';font-weight:700;font-size:62px;color:{YEL};margin-top:30px}}'''
    return page(800, 800, scatter([('+', 10, 8, 120), ('÷', 76, 70, 120), ('√', 74, 6, 120), ('×', 8, 72, 110)]) +
                '<div class="c"><div class="m">عيسى</div><div class="u"></div><div class="s">رياضيات</div></div>', css)

def banner():  # ‏2560×1440، والمنطقة الآمنة لكل الأجهزة 1546×423 في الوسط
    css = f'''.safe{{position:absolute;left:507px;top:508px;width:1546px;height:423px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:14px;text-align:center}}
.n{{font-size:150px;font-weight:900;line-height:1.15;border-bottom:16px solid {YEL};padding:0 20px 6px}}.t{{font-family:'Readex Pro';font-weight:700;font-size:54px;color:{YEL}}}
.p{{display:flex;gap:18px;margin-top:14px}}.p span{{font-family:'Readex Pro';font-weight:700;font-size:34px;padding:8px 26px;border-radius:40px;background:rgba(255,255,255,.1);border:2px solid rgba(255,255,255,.25)}}'''
    pills = ''.join(f'<span style="border-color:{c}">الوحدة {o}</span>' for o, _, c, _ in UNITS.values())
    return page(2560, 1440, scatter([(t, x, y, s * 2) for t, x, y, s in SYMS]) + f'''<div class="safe">
<div class="n">أ. عيسى الحارثي</div>
<div class="t">شرح دروس الرياضيات للصف السابع · منهج سلطنة عُمان</div>
<div class="p">{pills}</div></div>''', css)

def thumb(num, title, unit, review=False):
    o, uname, col, glyph = UNITS[unit]
    css = f'''.bar{{position:absolute;top:0;right:0;width:22px;height:100%;background:{col}}}
.r{{position:absolute;right:70px;top:70px;width:760px;display:flex;flex-direction:column;gap:26px}}
.num{{align-self:flex-start;font-size:{86 if review else 104}px;font-weight:900;line-height:1.15;color:{NAVY};background:{YEL};border-radius:22px;padding:0 34px}}
.ti{{font-size:{92 if len(title) < 16 else 78 if len(title) < 24 else 66}px;font-weight:900;line-height:1.25}}
.un{{font-family:'Readex Pro';font-weight:700;font-size:34px;color:{col}}}
.g{{position:absolute;left:70px;top:150px;width:330px;height:330px;border-radius:50%;background:{col};display:flex;align-items:center;justify-content:center;
font-size:{150 if len(glyph) < 3 else 110}px;font-weight:900;color:{NAVY};box-shadow:0 0 0 18px rgba(255,255,255,.08);direction:rtl}}
.ft{{position:absolute;left:70px;bottom:46px;font-family:'Readex Pro';font-weight:700;font-size:34px;color:rgba(255,255,255,.85)}}
.ft b{{color:{YEL}}}'''
    return page(1280, 720, scatter(SYMS[:6]) + f'''<div class="bar"></div><div class="g">{glyph}</div>
<div class="r"><div class="num">{'مراجعة الوحدة' if review else 'الدرس ' + num}</div><div class="ti">{title}</div>
<div class="un">الوحدة {o} · {uname}</div></div>
<div class="ft"><b>أ. عيسى الحارثي</b> · رياضيات الصف السابع</div>''', css)

def cover(unit, n, w=1280, h=720):  # قوائم التشغيل في YouTube تقبل غلافاً مربّعاً فقط (w=h)
    o, uname, col, glyph = UNITS[unit]
    css = f'''.c{{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:24px;text-align:center}}
.k{{font-family:'Readex Pro';font-weight:700;font-size:44px;color:{col}}}.u{{font-size:130px;font-weight:900;line-height:1.1}}
.t{{font-size:66px;font-weight:800;color:{YEL};max-width:90%;line-height:1.35}}.f{{font-family:'Readex Pro';font-weight:700;font-size:34px;color:rgba(255,255,255,.8);margin-top:10px}}
.band{{position:absolute;bottom:0;left:0;right:0;height:22px;background:{col}}}'''
    return page(w, h, scatter(SYMS) + f'''<div class="c"><div class="k">رياضيات الصف السابع</div><div class="u">الوحدة {o}</div>
<div class="t">{uname}</div><div class="f">{str(n).translate(str.maketrans('0123456789','٠١٢٣٤٥٦٧٨٩'))} فيديوهات · أ. عيسى الحارثي</div></div><div class="band"></div>''', css)

LESSONS = {  # (رقم الدرس، العنوان، الوحدة، مراجعة؟) — عناوين القناة كما رُفعت
    '1-1': ('١-١', 'الأعداد الصحيحة', 1), '1-2': ('١-٢', 'المضاعفات', 1), '1-3': ('١-٣', 'العوامل وقابلية القسمة', 1),
    '1-4': ('١-٤', 'الأعداد الأولية', 1), '1-5': ('١-٥', 'الأسس', 1), '1-6': ('١-٦', 'القوى والجذور', 1),
    '1-7': ('١-٧', 'ترتيب العمليات الحسابية', 1), '1-r': ('', 'الأعداد الصحيحة والقوى والجذور', 1),
    '4-1': ('٤-١', 'التعرّف على وحدات القياس', 4), '4-2': ('٤-٢', 'اختيار وحدات القياس المناسبة', 4), '4-r': ('', 'الطول والكتلة والسعة', 4),
}

if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else 'youtube_art'
    os.makedirs(out, exist_ok=True); jobs = []
    def add(name, html, w, h):
        p = os.path.join(out, name + '.html'); open(p, 'w', encoding='utf-8').write(html); jobs.append([p, os.path.join(out, name + '.png'), w, h])
    add('profile', profile(), 800, 800); add('banner', banner(), 2560, 1440)
    for k, (num, title, u) in LESSONS.items(): add('thumb_' + k, thumb(num, title, u, k.endswith('-r')), 1280, 720)
    for u, n in ((1, 8), (4, 3)): add(f'cover_u{u}', cover(u, n, 1080, 1080), 1080, 1080)
    js = os.path.join(out, 'jobs.json'); json.dump(jobs, open(js, 'w'))
    subprocess.run(['node', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'snap_art.mjs'), js], check=True)
