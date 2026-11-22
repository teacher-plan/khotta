# بانٍ حلقات «أربعين من أربعين»: ملف الحلقة (episodes/epNN.py) ← صفحة مشاهد HTML (540×960 تُصوَّر ×٢ = 1080×1920).
# python3 build.py episodes/ep01.py <مجلد_الصور> <مجلد_الصوت> out.html
import base64, importlib.util, json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
PAD = 250          # ملّي ثانية بعد كل مقطع صوتي
TAIL = 1200        # ذيل المشهد الأخير


def CHK(t, ok=True, size=38):
    """علامة ✓ (خضراء) أو ✗ (حمراء) تُرسم في الثانية t من المشهد."""
    if ok:
        p = '<path d="M9 21 L17 29 L31 11" stroke="#2E9E5B" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
    else:
        p = '<path d="M11 11 L29 29 M29 11 L11 29" stroke="#EC5B4F" stroke-width="5" fill="none" stroke-linecap="round"/>'
    return (f'<svg class="chk" style="width:{size}px;height:{size}px" viewBox="0 0 40 40">'
            f'<circle cx="20" cy="20" r="17" fill="#fff" stroke="#1E1B18" stroke-width="3"/>'
            f'<g data-t="{t}" data-fx="draw">{p}</g></svg>')


def F(a, b):
    return f'<span class="frac"><span>{a}</span><span>{b}</span></span>'


def dur_ms(f):
    out = subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f])
    return int(float(out) * 1000)


def pauses(f):
    """نهايات الوقفات في المقطع (ثوانٍ)."""
    r = subprocess.run(['ffmpeg', '-i', f, '-af', 'silencedetect=n=-30dB:d=0.15', '-f', 'null', '-'], capture_output=True, text=True)
    return [float(x) for x in re.findall(r'silence_end: ([0-9.]+)', r.stderr)]


def anchor_times(html, text, dur_s, ends):
    """data-t="@كلمة" ← زمن نطق الكلمة: موضعها في نصّ التعليق نسبةً إلى طوله × مدّة المقطع،
    ثم يُلصق بأقرب نهاية وقفة قبله أو بعده بقليل (بداية الجملة التي فيها الكلمة)."""
    plain = re.sub(r'\[[^\]]*\]\s*', '', text)

    def at(m):
        key = m.group(1)
        i = plain.find(key)
        if i < 0:
            raise SystemExit(f'مرساة غير موجودة في التعليق: «{key}»')
        t = dur_s * i / max(1, len(plain))
        near = [e for e in ends if -0.9 <= e - t <= 0.6]
        if near:
            t = min(near, key=lambda e: abs(e - t))
        return f'data-t="{max(0.0, t - 0.05):.2f}"'
    return re.sub(r'data-t="@([^"]+)"', at, html)


def main(ep_file, img_dir, aud_dir, out):
    spec = importlib.util.spec_from_file_location('ep', ep_file)
    ep = importlib.util.module_from_spec(spec)
    sys.modules['build'] = sys.modules[__name__]
    spec.loader.exec_module(ep)
    mp3 = sorted(x for x in os.listdir(aud_dir) if x.endswith('.mp3'))
    assert len(mp3) == len(ep.SCENES), f'{len(mp3)} صوت ≠ {len(ep.SCENES)} مشهد'
    durs = [dur_ms(os.path.join(aud_dir, m)) + PAD for m in mp3]
    durs[-1] += TAIL

    def img(m):
        p = os.path.join(img_dir, m.group(1) + '.png')
        return 'data:image/png;base64,' + base64.b64encode(open(p, 'rb').read()).decode()

    narr = getattr(ep, 'NARRATION', None)
    # ألفاظ مرفوضة (SERIES.md «ألفاظ مُلزِمة»): تبي ← تريد، مو ← ما/ليس، باكر ← غداً
    for k, tx in enumerate(narr or []):
        bad = re.findall(r'(?<!\S)(تبي|مو|باكر)(?!\S)', tx)
        if bad:
            print(f'⚠️ مشهد {k + 1}: ألفاظ مرفوضة في التعليق: {"، ".join(bad)} — صحّحها قبل توليد الصوت', file=sys.stderr)
    src = []
    for k, sc in enumerate(ep.SCENES):
        if narr and 'data-t="@' in sc:
            f = os.path.join(aud_dir, mp3[k])
            sc = anchor_times(sc, narr[k], dur_ms(f) / 1000, pauses(f))
        src.append(sc)
    scenes = ''.join(f'<section class="scene">{re.sub(r"\{\{img:(\w+)\}\}", img, s)}</section>\n' for s in src)
    html = open(os.path.join(HERE, 'template.html'), encoding='utf-8').read()
    html = html.replace('__TAG__', ep.TAG).replace('__SCENES__', scenes).replace('__DURS__', json.dumps(durs))
    open(out, 'w', encoding='utf-8').write(html)
    print(out, f'{sum(durs) / 1000:.1f} ث', len(durs), 'مشهد')


if __name__ == '__main__':
    main(*sys.argv[1:5])
