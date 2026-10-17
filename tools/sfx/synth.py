"""مولّد أصوات خُطّة — كلّها مُركّبة رياضياً هنا (لا عيّنات مسجّلة ولا حقوق طرفٍ ثالث).

التشغيل:  python3 tools/sfx/synth.py   ← يكتب sfx/*.mp3 في جذر المستودع
يحتاج numpy و ffmpeg (أو imageio_ffmpeg).

الفلسفة: أصوات دافئة لطيفة تناسب صفّاً من أطفال ٦–١٠ سنوات يسمعها عبر مكبّر:
آلات إيقاعية نغمية (ماريمبا/أجراس/خشب) بدل صفّارات الألعاب الإلكترونية،
والخطأ «بونك» خشبيّ هابط لا طنين مُحبِط، وكل صوتٍ بصدى غرفة خفيف.
"""
import numpy as np, subprocess, os, shutil, wave

SR = 44100
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, 'sfx')


def t_(d): return np.arange(int(SR * d)) / SR
def midi(n): return 440.0 * 2 ** ((n - 69) / 12)


def env(n, a=.004, d=.3, curve=4.0):
    """هجومٌ سريع ثم اضمحلالٌ أُسّي — شكل ضربة آلة إيقاعية"""
    t = np.arange(n) / SR
    e = np.exp(-t * curve / max(d, 1e-3))
    at = int(SR * a)
    if at > 0: e[:at] *= np.linspace(0, 1, at)
    return e


def marimba(f, d=.6, bright=1.0):
    t = t_(d)
    # نسب الماريمبا: الأساس + ٤× + ~٩٫٩× (قضيبٌ منحوت)
    s = (np.sin(2*np.pi*f*t) * env(len(t), .002, d*.9, 5)
         + .35*bright*np.sin(2*np.pi*f*3.99*t) * env(len(t), .001, d*.25, 6)
         + .12*bright*np.sin(2*np.pi*f*9.9*t) * env(len(t), .001, d*.08, 6))
    return s


def bell(f, d=1.4, bright=1.0):
    t = t_(d)
    parts = [(1, 1, 1), (2.0, .5, .7), (2.76, .35*bright, .5), (5.4, .18*bright, .3), (8.93, .08*bright, .2)]
    s = np.zeros_like(t)
    for r, a, dd in parts:
        s += a*np.sin(2*np.pi*f*r*t + .3*np.sin(2*np.pi*f*t)) * env(len(t), .001, d*dd, 5)
    return s


def pluck(f, d=.5):
    """وترٌ منقور (كاربلس–سترونغ) — دافئ للنغمات الإيجابية"""
    n = int(SR*d); p = max(2, int(SR/f))
    buf = np.random.uniform(-1, 1, p)
    out = np.zeros(n)
    for i in range(n):
        out[i] = buf[i % p]
        buf[i % p] = .996*.5*(buf[i % p] + buf[(i+1) % p])
    return out * env(n, .001, d, 3)


def noise(d): return np.random.uniform(-1, 1, int(SR*d))


def lowpass(x, fc):
    a = np.exp(-2*np.pi*fc/SR); y = np.zeros_like(x); s = 0.0
    for i, v in enumerate(x): s = (1-a)*v + a*s; y[i] = s
    return y


def highpass(x, fc): return x - lowpass(x, fc)


def reverb(x, mix=.18, size=1.0):
    """صدى غرفة صغيرة (شرودر): أربع أمشاط متوازية ثم مرشّحا تمريرٍ شامل"""
    tail = int(SR*.6*size); x2 = np.concatenate([x, np.zeros(tail)])
    out = np.zeros_like(x2)
    for dl, g in [(1557, .80), (1617, .79), (1491, .78), (1422, .77)]:
        dl = int(dl*size); y = x2.copy()
        for i in range(dl, len(y)): y[i] += g*y[i-dl]*.5
        out += y
    out /= 4
    for dl, g in [(225, .7), (556, .7)]:
        y = np.zeros_like(out); buf = np.zeros(dl)
        for i in range(len(out)):
            b = buf[i % dl]; v = out[i] + (-g)*b
            y[i] = b + g*v; buf[i % dl] = v
        out = y
    return (1-mix)*x2 + mix*out


def mix(*parts):
    n = max(len(p) + int(o*SR) for o, p in parts)
    y = np.zeros(n)
    for o, p in parts:
        s = int(o*SR); y[s:s+len(p)] += p
    return y


def finish(x, peak=.89, fade=.03):
    x = x - np.mean(x)
    nz = np.nonzero(np.abs(x) > 1e-4)[0]
    if len(nz): x = x[:nz[-1]+1]
    f = int(SR*fade)
    if len(x) > f: x[-f:] *= np.linspace(1, 0, f)
    m = np.max(np.abs(x)) or 1
    return np.tanh(x/m*1.1)/np.tanh(1.1)*peak


# ─────────────────────────── الأصوات ───────────────────────────
def s_ok():
    # «تِن-تِنغ» صاعد: ماريمبا دو٦→صول٦ + لمعة جرس خفيفة
    return reverb(mix((0, marimba(midi(84), .45)), (.075, marimba(midi(91), .6)),
                      (.075, .25*bell(midi(103), .6, .6))), .16)


def s_bad():
    # «بونك-بونك» خشبي هابط لطيف — يُفهم خطأً دون أن يُحبِط
    def bonk(f, d):
        t = t_(d); fr = f*(1+.25*np.exp(-t*40))
        ph = 2*np.pi*np.cumsum(fr)/SR
        return (np.sin(ph) + .3*np.sin(2*ph)) * env(len(t), .002, d*.5, 6)
    return reverb(mix((0, bonk(midi(55), .28)), (.14, bonk(midi(50), .38))), .12)


def s_pop():
    t = t_(.12); fr = 1400*np.exp(-t*28) + 300
    s = np.sin(2*np.pi*np.cumsum(fr)/SR) * env(len(t), .001, .06, 5)
    return reverb(mix((0, s), (0, .25*highpass(noise(.012), 2000)*env(int(SR*.012), .0005, .01, 5))), .08)


def s_click():
    t = t_(.05)
    s = np.sin(2*np.pi*2200*t)*env(len(t), .0005, .012, 6) + .4*highpass(noise(.05), 3000)*env(len(t), .0003, .006, 6)
    return s


def s_win():
    # فانفار ماريمبا + أوتار منقورة: دو-مي-صول-دو ثم كوردٌ متّسع ولمعات
    notes = [72, 76, 79, 84]
    parts = [(i*.11, marimba(midi(n), .55)) for i, n in enumerate(notes)]
    parts += [(i*.11, .5*pluck(midi(n-12), .5)) for i, n in enumerate(notes)]
    ch = .46
    for n in [72, 76, 79, 84, 88]:
        parts.append((ch, .55*bell(midi(n), 1.5, .5)))
        parts.append((ch, .35*pluck(midi(n-12), 1.2)))
    for k in range(10):
        parts.append((ch + .05 + k*.07, .12*bell(midi(96 + (k*5) % 12), .5, 1)))
    return reverb(mix(*parts), .22, 1.2)


def s_big():
    # إنجاز كبير (نجمة عاشرة…): صعودٌ سريع ثم جرسٌ عالٍ وشلّال لمعات
    parts = [(i*.06, .8*marimba(midi(n), .4)) for i, n in enumerate([67, 71, 74, 79, 83, 86])]
    parts += [(.38, bell(midi(91), 2.0, .8)), (.38, .6*bell(midi(79), 2.0, .5))]
    for k in range(14):
        parts.append((.42 + k*.055, .10*bell(midi(98 + (k*7) % 12), .45, 1)))
    return reverb(mix(*parts), .25, 1.3)


def s_ding():
    # نجمة: جرسٌ صافٍ مع لمعةٍ أعلى
    return reverb(mix((0, bell(midi(88), 1.1, .7)), (.04, .3*bell(midi(100), .6, .5))), .2)


def s_quiet():
    # إشارة انتباه بصوت إنذار (~٣ ث): «طوووط» — نغمةٌ واحدة ثابتة متصلة (٩٠٠ هرتز)
    # بموجةٍ مربّعة مُنعَّمة (واضحة دون حدّةٍ مؤذية). تبدأ فوراً بلا صمت وتنتهي بخفوتٍ قصير.
    d = 3.0; t = t_(d); f = 900.0
    ph = 2*np.pi*f*t
    sq = lowpass(.8*np.tanh(3.0*np.sin(ph)) + .25*np.sin(2*ph), 3500)
    e = np.ones_like(t); a_ = int(SR*.006); r_ = int(SR*.15)
    e[:a_] = np.linspace(0, 1, a_); e[-r_:] = np.linspace(1, 0, r_)
    return reverb(sq*e*.75, .06, .5)


def s_flip():
    # قلب بطاقة: نفخة هواء قصيرة + نقرة ورق
    n = noise(.14); b = highpass(lowpass(n, 5000), 900)
    e = np.sin(np.linspace(0, np.pi, len(b)))**2
    return mix((0, b*e*.7), (.11, .4*s_click()))


def s_whoosh():
    d = .45; n = noise(d); t = np.linspace(0, 1, len(n))
    out = np.zeros_like(n); s = 0.0
    for i, v in enumerate(n):
        fc = 400 + 3500*np.sin(np.pi*t[i])**2; a = np.exp(-2*np.pi*fc/SR)
        s = (1-a)*v + a*s; out[i] = s
    return out*np.sin(np.pi*t)**1.5


def s_tick():
    t = t_(.06)
    return (np.sin(2*np.pi*1800*t) + .5*np.sin(2*np.pi*3300*t))*env(len(t), .0005, .02, 6)


def s_tock():
    t = t_(.3)
    return reverb(marimba(midi(69), .3) + .3*np.sin(2*np.pi*880*t)*env(len(t), .001, .05, 5), .1)


def s_spin():
    # طقطقة عجلةٍ تتباطأ: التوقيت يطابق منحنى الدوران في اللعبة (1-(1-p)^3 خلال ٣٫٤ث)
    dur, turns, slots = 3.4, 4.8, 10
    tick = s_tick()*.9
    total = turns*slots; y = np.zeros(int(SR*(dur+.3)))
    k = 1
    while k < total:
        p = 1 - (1 - k/total)**(1/3)          # معكوس منحنى التباطؤ
        s = int(p*dur*SR)
        pitch = 1 + .15*np.random.rand()
        tk = np.interp(np.arange(0, len(tick), pitch), np.arange(len(tick)), tick)
        y[s:s+len(tk)] += tk*(.6 + .4*(1-p))
        k += 1
    return reverb(y, .08)


def s_correct_streak():
    # سلسلة إجابات صحيحة: arpeggio أعلى من ok
    return reverb(mix(*[(i*.06, marimba(midi(n), .4)) for i, n in enumerate([84, 88, 91, 96])]), .18)


def s_countdown():
    # «٣-٢-١-انطلق»
    parts = [(i*.8, .9*marimba(midi(72), .5)) for i in range(3)]
    parts.append((2.4, marimba(midi(84), .9)))
    parts.append((2.4, .6*bell(midi(96), 1.0, .6)))
    return reverb(mix(*parts), .18)


def s_reveal():
    # كشف/فتح صندوق: صعودٌ غامض قصير ثم لمعة
    t = t_(.5); fr = 300 + 900*t**2
    sw = np.sin(2*np.pi*np.cumsum(fr)/SR)*np.sin(np.pi*t/1.0)**2*.4
    return reverb(mix((0, sw), (.45, bell(midi(91), .9, .8))), .22)


def s_drop():
    # إسقاط عنصر في مكانه الصحيح: «تَك» خشبيّة مكتومة + نغمة صغيرة
    t = t_(.15)
    k = np.sin(2*np.pi*np.cumsum(220*(1+np.exp(-t*60)))/SR)*env(len(t), .001, .07, 6)
    return reverb(mix((0, k), (.02, .5*marimba(midi(86), .3))), .1)


def s_timeup():
    # انتهاء الوقت: جرسا منبّهٍ مزدوجان ودودان (لا صفّارة إنذار)
    parts = []
    for r in range(2):
        o = r*.55
        parts += [(o, bell(midi(84), .9, .7)), (o+.14, bell(midi(79), .9, .7))]
    return reverb(mix(*parts), .22)


# ───────────── أصوات الجيل الثالث من الألعاب (ملعب، نهر، ميزان، حبل) ─────────────
def biquad_bp(x, fc, q=4.0):
    """مرشّح تمرير نطاقٍ رنّان (RBJ) — لصياغة أحرف العلّة والرنين"""
    w = 2*np.pi*fc/SR; al = np.sin(w)/(2*q); c = np.cos(w)
    b0, b2 = al, -al; a0, a1, a2 = 1+al, -2*c, 1-al
    b0, b2, a1, a2 = b0/a0, b2/a0, a1/a0, a2/a0
    y = np.zeros_like(x); x1 = x2 = y1 = y2 = 0.0
    for i, v in enumerate(x):
        o = b0*v + b2*x2 - a1*y1 - a2*y2
        x2, x1, y2, y1 = x1, v, y1, o; y[i] = o
    return y


def s_kick():
    # ركلة كرة: «دُمّ» جلديّ منخفض قصير + صفعة عالية خاطفة
    # مكبّرات الصف لا تُسمِع ما تحت ~١٢٠ هرتز، فالضربة تبدأ أعلى وتُدعَم بصفعة جلدٍ واضحة
    t = t_(.24); fr = 110 + 260*np.exp(-t*30)
    thump = (np.sin(2*np.pi*np.cumsum(fr)/SR) + .35*np.sin(4*np.pi*np.cumsum(fr)/SR))*env(len(t), .001, .11, 5)
    slap = biquad_bp(noise(.04), 2200, 1.2)*env(int(SR*.04), .0004, .014, 6)
    return reverb(mix((0, thump), (0, .9*slap)), .07)


def s_whistle():
    # صافرة الحكم: نغمةٌ حادّة ~٢٫٩ك مع رعشة الكرة الداخلية (تضمين ~٣٤ هرتز)
    d = .62; t = t_(d)
    wob = np.sin(2*np.pi*34*t + 1.5*np.sin(2*np.pi*2.5*t))
    f = 2900 + 90*wob
    tone = np.sin(2*np.pi*np.cumsum(f)/SR)*(.72 + .28*wob)
    breath = biquad_bp(noise(d), 2900, 3)*.35
    e = np.ones_like(t); a_ = int(SR*.025); r_ = int(SR*.09)
    e[:a_] = np.linspace(0, 1, a_); e[-r_:] = np.linspace(1, 0, r_)
    return reverb((tone + breath)*e*.8, .14, .9)


def _crowd(d, vowel, swell, voices=26, seed=3):
    rng = np.random.RandomState(seed); n = int(SR*d); t = np.arange(n)/SR
    out = np.zeros(n)
    F = {'ah': (720, 1240, 2550), 'aw': (560, 900, 2450), 'oo': (380, 820, 2300)}[vowel]
    base = noise(d)
    for v in range(voices):
        # كل «صوت» في الجمهور: ضجيجٌ مصفّى بأحرف علّة بارتفاعٍ مختلف قليلاً وتذبذبٍ بطيء
        sh = 1 + rng.uniform(-.12, .12)
        src = np.roll(base, rng.randint(0, n))
        y = sum(g*biquad_bp(src, f*sh, 6) for f, g in zip(F, (1, .6, .25)))
        lfo = 1 + .35*np.sin(2*np.pi*rng.uniform(1.5, 4)*t + rng.uniform(0, 6))
        out += y*lfo
    return out*swell(t)


def s_cheer():
    # هتاف الجمهور بعد الهدف: موجة «آآآه» تتصاعد ثم تخفت ببطء، مع صفيرٍ متناثر
    d = 2.4
    sw = lambda t: np.clip(t/.18, 0, 1)*np.exp(-np.clip(t-.5, 0, None)*1.25)
    c = _crowd(d, 'ah', sw)
    c = c/np.max(np.abs(c))
    parts = [(0, c)]
    rng = np.random.RandomState(11)
    for k in range(5):
        tt = t_(.35); f0 = rng.uniform(1300, 1700)
        fr = f0 + 700*np.sin(np.pi*tt/.35)
        parts.append((.15 + k*.28 + rng.uniform(0, .1), .16*np.sin(2*np.pi*np.cumsum(fr)/SR)*np.sin(np.pi*tt/.35)**2))
    for k in range(14):  # تصفيق
        parts.append((.25 + rng.uniform(0, 1.6), .22*highpass(noise(.02), 1200)*env(int(SR*.02), .0005, .01, 6)))
    return reverb(mix(*parts), .2, 1.4)


def s_groan():
    # «أوووه» الجمهور عند التصدّي: حرف علّةٍ هابطٌ قصير
    d = 1.3; t = t_(d)
    sw = lambda t: np.clip(t/.12, 0, 1)*np.exp(-np.clip(t-.25, 0, None)*2.2)
    c = _crowd(d, 'aw', sw, 20, 5)
    # هبوطٌ في النبرة: إعادة أخذ عيّناتٍ متباطئة
    idx = np.cumsum(np.linspace(1.0, .78, len(c))); idx = idx[idx < len(c)-1]
    c = np.interp(idx, np.arange(len(c)), c)
    return reverb(c/np.max(np.abs(c)), .18, 1.2)


def s_net():
    # ارتطام الكرة بالشبكة: حفيفٌ ناعم ممتدّ
    d = .45; n = noise(d); t = np.linspace(0, 1, len(n))
    b = highpass(lowpass(n, 3500), 500)*(np.exp(-t*5)*(1 - np.exp(-t*60)))
    return reverb(b*.9, .1)


def s_catch():
    # الحارس يمسك الكرة: صفعة قفّازٍ مكتومة
    t = t_(.18); fr = 90 + 120*np.exp(-t*50)
    th = np.sin(2*np.pi*np.cumsum(fr)/SR)*env(len(t), .001, .06, 5)
    sl = lowpass(noise(.06), 2500)*env(int(SR*.06), .0005, .025, 6)
    return reverb(mix((0, th), (0, .8*sl)), .08)


def s_creak():
    # شدّ الحبل: احتكاك «تزحلق-التصاق» لحبلٍ مشدود + دفعة جهد
    d = .7; n = int(SR*d); t = np.arange(n)/SR
    f = 95 + 40*np.sin(2*np.pi*1.3*t)
    ph = np.cumsum(f)/SR; saw = 2*(ph % 1) - 1
    grain = (np.random.rand(n) < .004).astype(float)
    y = biquad_bp(saw + .6*lowpass(grain*np.random.uniform(-1, 1, n)*8, 1500), 650, 2.5)
    e = np.sin(np.pi*t/d)**1.2
    heave = np.sin(2*np.pi*np.cumsum(70 + 30*np.exp(-t*8))/SR)*env(n, .01, .25, 4)*.5
    return reverb(y*e + heave, .12)


def s_freeze():
    # تجميد الفريق المخطئ: تكسّر جليدٍ زجاجيّ هابط
    parts = []
    rng = np.random.RandomState(4)
    for k in range(9):
        f = 4200 - k*300 + rng.uniform(-150, 150)
        parts.append((k*.035, .35*bell(f, .35, 1.2)))
    parts.append((0, .5*highpass(noise(.12), 3000)*env(int(SR*.12), .001, .05, 5)))
    return reverb(mix(*parts), .25, .9)


def s_splash():
    # رذاذ ماء: انفجار ضجيجٍ يُكتَم تدريجياً + فقاعاتٌ صاعدة
    d = .9; n = noise(d); t = np.linspace(0, d, len(n))
    out = np.zeros_like(n); s = 0.0
    for i, v in enumerate(n):
        fc = 300 + 5000*np.exp(-t[i]*7); a = np.exp(-2*np.pi*fc/SR)
        s = (1-a)*v + a*s; out[i] = s
    out *= np.exp(-t*4.5)*(1 - np.exp(-t*80))
    parts = [(0, out*1.4)]
    rng = np.random.RandomState(9)
    for k in range(8):
        tt = t_(.06); f0 = rng.uniform(500, 1100)
        parts.append((.12 + rng.uniform(0, .55), .25*np.sin(2*np.pi*np.cumsum(f0*(1 + 2.5*tt/.06))/SR)*env(len(tt), .002, .04, 5)))
    return reverb(mix(*parts), .15)


def s_clank():
    # ثقلٌ نحاسيّ يُوضع في الكفّة: رنينٌ معدنيّ غير متناسق قصير
    t = t_(.7); f = 520
    s = np.zeros_like(t)
    for r, a, dd in [(1, 1, .5), (2.32, .7, .35), (4.25, .5, .22), (6.63, .3, .15), (9.38, .2, .1)]:
        s += a*np.sin(2*np.pi*f*r*t)*env(len(t), .0005, .7*dd, 5)
    hit = highpass(noise(.01), 2500)*env(int(SR*.01), .0003, .005, 6)
    return reverb(mix((0, s*.8), (0, .5*hit)), .14)


def s_chime():
    # توازن الميزان: أجراسٌ صافية متتابعة ثم كوردٌ رنّان
    parts = [(i*.07, .6*bell(midi(n), 1.2, .6)) for i, n in enumerate([79, 84, 88, 91])]
    parts += [(.3, .4*bell(midi(96), 1.6, .5))]
    return reverb(mix(*parts), .26, 1.2)


def s_hoot():
    # البومة الحكيمة: «هوو-هوو» ناعمة مع نفَس
    def h(d, f0):
        t = t_(d); f = f0*(1 + .06*np.sin(np.pi*t/d))
        s = np.sin(2*np.pi*np.cumsum(f)/SR) + .15*np.sin(4*np.pi*np.cumsum(f)/SR)
        br = lowpass(noise(d), 900)*.25
        return (s + br)*np.sin(np.pi*t/d)**1.5
    return reverb(mix((0, h(.32, 380)), (.4, h(.42, 350))), .2)


def s_boing():
    # قفزة الضفدع: نابضٌ صاعد مع رعشة
    t = t_(.38); f = 180 + 520*(t/.38)**.7
    s = np.sin(2*np.pi*np.cumsum(f*(1 + .08*np.sin(2*np.pi*28*t)))/SR)
    return reverb(s*env(len(t), .004, .3, 3)*.8, .1)


def s_ribbit():
    # نقيق: «رِب-بِت» — نبضاتٌ حنجرية سريعة تمرّ بفورمانت
    def croak(d, f0, rate):
        n = int(SR*d); t = np.arange(n)/SR
        pulses = (np.sin(2*np.pi*rate*t) > .55).astype(float)
        src = pulses*np.sin(2*np.pi*f0*t) + .4*pulses*np.sin(2*np.pi*f0*2.02*t)
        y = biquad_bp(src, 900, 3) + .5*biquad_bp(src, 1800, 4)
        return y*np.sin(np.pi*t/d)**.8
    return reverb(mix((0, croak(.13, 260, 42)), (.17, croak(.17, 230, 38))), .12)


def s_gulp():
    # لسان الضفدع يلتقط الحشرة: «سلورب» صاعد ثم بلع
    t = t_(.14); f = 300 + 900*(t/.14)
    a = np.sin(2*np.pi*np.cumsum(f)/SR)*env(len(t), .002, .1, 3)
    t2 = t_(.16); b = np.sin(2*np.pi*np.cumsum(160 - 60*t2/.16)/SR)*env(len(t2), .004, .1, 4)
    return reverb(mix((0, .6*a), (.16, b)), .1)


def s_drumroll():
    # قرع طبول قصير قبل الحسم: ضرباتٌ متسارعة تنتهي بضربة صنج
    parts = []; tt = 0.0; k = 0
    while tt < .9:
        g = .35 + .5*(tt/.9)
        parts.append((tt, g*highpass(noise(.05), 900)*env(int(SR*.05), .0005, .03, 6)))
        tt += .07 - .035*(tt/.9); k += 1
    parts.append((.92, .8*highpass(noise(.6), 3000)*env(int(SR*.6), .001, .45, 4)))
    return reverb(mix(*parts), .14)


SOUNDS = {
    'timeup': s_timeup,
    'ok': s_ok, 'bad': s_bad, 'pop': s_pop, 'click': s_click, 'win': s_win, 'big': s_big,
    'ding': s_ding, 'quiet': s_quiet, 'flip': s_flip, 'whoosh': s_whoosh, 'tick': s_tick,
    'tock': s_tock, 'spin': s_spin, 'streak': s_correct_streak, 'countdown': s_countdown,
    'reveal': s_reveal, 'drop': s_drop,
    'kick': s_kick, 'whistle': s_whistle, 'cheer': s_cheer, 'groan': s_groan, 'net': s_net, 'catch': s_catch,
    'creak': s_creak, 'freeze': s_freeze, 'splash': s_splash, 'clank': s_clank, 'chime': s_chime, 'hoot': s_hoot,
    'boing': s_boing, 'ribbit': s_ribbit, 'gulp': s_gulp, 'drumroll': s_drumroll,
}


def ffmpeg():
    exe = shutil.which('ffmpeg')
    if exe: return exe
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


def write(name, x):
    os.makedirs(OUT, exist_ok=True)
    wav = os.path.join(OUT, name + '.wav')
    pcm = (finish(x)*32767).astype(np.int16)
    with wave.open(wav, 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
    mp3 = os.path.join(OUT, name + '.mp3')
    subprocess.run([ffmpeg(), '-y', '-loglevel', 'error', '-i', wav, '-codec:a', 'libmp3lame', '-b:a', '96k', mp3], check=True)
    os.remove(wav)
    return mp3


if __name__ == '__main__':
    np.random.seed(7)
    import sys
    only = sys.argv[1:]
    for k, fn in SOUNDS.items():
        if only and k not in only: continue
        print(k, os.path.getsize(write(k, fn())))
