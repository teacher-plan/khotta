# بانٍ حلقات «أربعين من أربعين»: ملف الحلقة (episodes/epNN.py) ← صفحة مشاهد HTML (540×960 تُصوَّر ×٢ = 1080×1920).
# python3 build.py episodes/ep01.py <مجلد_الصور> <مجلد_الصوت> out.html
import base64, importlib.util, json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
PAD = 350          # ملّي ثانية بعد كل مقطع صوتي
TAIL = 1500        # ذيل المشهد الأخير


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

    scenes = ''.join(f'<section class="scene">{re.sub(r"\{\{img:(\w+)\}\}", img, s)}</section>\n' for s in ep.SCENES)
    html = open(os.path.join(HERE, 'template.html'), encoding='utf-8').read()
    html = html.replace('__TAG__', ep.TAG).replace('__SCENES__', scenes).replace('__DURS__', json.dumps(durs))
    open(out, 'w', encoding='utf-8').write(html)
    print(out, f'{sum(durs) / 1000:.1f} ث', len(durs), 'مشهد')


if __name__ == '__main__':
    main(*sys.argv[1:5])
