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
    # إشارة هدوء: ثلاث نغمات «تشايم» هابطة ناعمة تشبه جرس المدرسة الهادئ
    return reverb(mix((0, bell(midi(81), 1.6, .4)), (.32, bell(midi(77), 1.6, .4)),
                      (.64, bell(midi(72), 2.2, .4))), .3, 1.4)


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


SOUNDS = {
    'timeup': s_timeup,
    'ok': s_ok, 'bad': s_bad, 'pop': s_pop, 'click': s_click, 'win': s_win, 'big': s_big,
    'ding': s_ding, 'quiet': s_quiet, 'flip': s_flip, 'whoosh': s_whoosh, 'tick': s_tick,
    'tock': s_tock, 'spin': s_spin, 'streak': s_correct_streak, 'countdown': s_countdown,
    'reveal': s_reveal, 'drop': s_drop,
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
