# غلاف الحلقة (1080×1920) لـ YouTube Shorts وInstagram Reels بهوية السلسلة نفسها.
# python3 cover.py <رقم الحلقة> "<المهارة>" "<السؤالان>" <صورة_السؤال.png> <خرج.png>
import base64, json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from blocks import AVATAR, STACK, T

HERE = os.path.dirname(os.path.abspath(__file__))


def main(ep, skill, qs, img, out):
    data = 'data:image/png;base64,' + base64.b64encode(open(img, 'rb').read()).decode()
    scene = STACK(
        T(0, '<span class="pill" style="font-size:26px">٤٠ من ٤٠</span>', cls='center'),
        T(0, f'الحلقة {ep}', cls='center', style='font-weight:900;font-size:30px'),
        T(0, skill, cls='title', style='font-size:84px;line-height:1.1'),
        '<div data-deco="1" style="height:10px;width:240px;margin:-14px auto 0;background:var(--coral);border-radius:6px"></div>',
        T(0, f'<div class="card" style="padding:6px;transform:rotate(-1.5deg)"><img src="{data}" style="width:100%;display:block"></div>'),
        T(0, f'<span class="pill w" style="font-size:22px">{qs} • امتحان الوزارة</span>', cls='center'),
        T(0, AVATAR),
        T(0, 'أ. عيسى الحارثي • رياضيات الصف السابع', cls='center', style='font-weight:900;font-size:21px'),
        gap=18, justify='center')
    html = open(os.path.join(HERE, 'template.html'), encoding='utf-8').read()
    html = html.replace('__TAG__', 'سلسلة حلّ امتحانات الوزارة').replace('__SCENES__', f'<section class="scene">{scene}</section>').replace('__DURS__', json.dumps([1000]))
    tmp = out + '.html'
    open(tmp, 'w', encoding='utf-8').write(html)
    js = f'''import {{ chromium }} from '/opt/node22/lib/node_modules/playwright/index.mjs'; import fs from 'fs';
const b = await chromium.launch(); const p = await b.newPage({{ viewport: {{ width: 540, height: 960 }}, deviceScaleFactor: 2 }});
await p.setContent(fs.readFileSync({json.dumps(tmp)}, 'utf8'), {{ waitUntil: 'networkidle' }}); await p.evaluate(() => document.fonts.ready);
await p.evaluate(() => window.seek(0, 900)); await p.screenshot({{ path: {json.dumps(out)} }}); await b.close();'''
    subprocess.run(['node', '--input-type=module', '-e', js], check=True)
    os.remove(tmp)
    print(out)


if __name__ == '__main__':
    main(*sys.argv[1:6])
