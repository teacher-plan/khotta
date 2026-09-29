# صفحة «تحضير الدرس»: العرض التفاعلي + الفيديو + ورقة الملخّص في رابطٍ واحد، مع زرّ حفظٍ لكل جزء
# (في تطبيق Claude على الهاتف يفتح الحفظ قائمة المشاركة: «حفظ في الصور» أو «حفظ في الملفات»).
#
# python3 tools/presentations/kit.py <مجلد_الخرج> --code "١-٧" --title "ترتيب العمليات الحسابية" \
#   --meta "الصف السابع · الوحدة الأولى · كتاب الطالب ص ٣٥" --slides 28 --minutes "٤ دقائق و٢٠ ثانية" \
#   --deck examples/ترتيب_العمليات_عرض_تفاعلي.html --video examples/فيديو_ترتيب_العمليات.mp4 \
#   --sheets examples/ملخصات/ملخص_ترتيب_العمليات_1.png examples/ملخصات/ملخص_ترتيب_العمليات_2.png \
#   --pdf examples/ملخصات/ملخص_ترتيب_العمليات.pdf
# ثم يُنشر المجلد بأداة Artifact: file_path=<الخرج>/index.html، root=<الخرج>، files=كل ما سواه،
# و capabilities={"downloads": true}. التحديث لاحقاً: إعادة النشر بالـ url نفسه.
import argparse, html, os, shutil

AR = '٠١٢٣٤٥٦٧٨٩'
def ar(n): return ''.join(AR[int(c)] if c.isdigit() else c for c in str(n))

ap = argparse.ArgumentParser()
ap.add_argument('out'); ap.add_argument('--code', required=True); ap.add_argument('--title', required=True)
ap.add_argument('--meta', required=True); ap.add_argument('--slides', type=int, required=True); ap.add_argument('--minutes', default='')
ap.add_argument('--deck-note', default='')
ap.add_argument('--deck', required=True); ap.add_argument('--video')  # اختياري (صفحات المراجعة بلا فيديو)
ap.add_argument('--sheets', nargs='+', required=True); ap.add_argument('--pdf', required=True)
A = ap.parse_args()
os.makedirs(A.out, exist_ok=True)
shutil.copy(A.deck, os.path.join(A.out, 'deck.html'))
if A.video: shutil.copy(A.video, os.path.join(A.out, 'video.mp4'))
shutil.copy(A.pdf, os.path.join(A.out, 'summary.pdf'))
for i, s in enumerate(A.sheets, 1): shutil.copy(s, os.path.join(A.out, f'sheet{i}.png'))

T = html.escape(A.title); base = A.title.replace(' ', '_')
NAMES = {'deck': f'{base}_عرض_تفاعلي.html', 'video': f'{base}_فيديو.mp4', 'pdf': f'ملخص_{base}.pdf'}
SAVE_ICON = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 4v11m0 0l-4.5-4.5M12 15l4.5-4.5M5 19h14"/></svg>'
def btn(src, name, label, cls='save'):
    return f'<button type="button" class="{cls}" data-src="{src}" data-name="{html.escape(name)}">{SAVE_ICON}<span>{label}</span></button>'
sheets = ''.join(f'<figure><img src="sheet{i}.png" alt="ورقة الملخّص، الصفحة {ar(i)}"><figcaption>الصفحة {ar(i)}</figcaption>'
                 f'{btn(f"sheet{i}.png", f"ملخص_{base}_{i}.png", f"حفظ الصفحة {ar(i)}")}</figure>' for i in range(1, len(A.sheets) + 1))

VIDEO = (f'''<section id="video">
  <h2><b>٢</b>فيديو الدرس</h2>
  <p>{html.escape(A.minutes)} بالتعليق الصوتي، ودقّة 1080p — صالح لليوتيوب والواتساب.</p>
  <video controls preload="metadata" src="video.mp4"></video>
  <div class="acts">{btn("video.mp4", NAMES["video"], "حفظ الفيديو")}</div>
</section>
''' if A.video else '')
page = f'''<title>تحضير درس {T}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Readex+Pro:wght@400;600;700&family=Cairo:wght@700&display=swap">
<style>
/* صفحة واحدة: رأس الدرس، ثم ثلاثة أجزاء بترتيب الاستعمال (العرض، الفيديو، الملخّص)، ولكلٍّ زرّ حفظ */
:root{{
  --bg:#F6F8FB; --card:#FFFFFF; --ink:#14305C; --muted:#4A5E80; --line:#D5DFEC; --accent:#C7361B; --blue:#2563EB; --soft:#EAF1FF; --ok:#1B7A3E;
  --fd:'Readex Pro','Cairo',Tahoma,sans-serif; --fn:'Cairo','Readex Pro',sans-serif;
}}
@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]){{--bg:#0F1726;--card:#172238;--ink:#E6EDF7;--muted:#A9B8CF;--line:#2B3A55;--accent:#FF7A5C;--blue:#7AA7FF;--soft:#1F2F4D;--ok:#6BD39A;color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#0F1726;--card:#172238;--ink:#E6EDF7;--muted:#A9B8CF;--line:#2B3A55;--accent:#FF7A5C;--blue:#7AA7FF;--soft:#1F2F4D;--ok:#6BD39A;color-scheme:dark}}
body{{background:var(--bg);color:var(--ink);font-family:var(--fd);direction:rtl}}
.wrap{{max-width:980px;margin:0 auto;padding-inline:16px;padding-block:28px 48px;display:flex;flex-direction:column;gap:22px}}
header{{display:flex;flex-direction:column;gap:6px}}
.eyebrow{{font-size:14px;color:var(--muted)}}
h1{{margin:0;font-size:clamp(28px,5vw,40px);line-height:1.25;text-wrap:balance}}
h1 .n{{font-family:var(--fn);color:var(--accent)}}
.lead{{margin:0;color:var(--muted);font-size:16px;line-height:1.7;max-width:62ch}}
section{{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:20px;display:flex;flex-direction:column;gap:14px;min-width:0}}
h2{{margin:0;font-size:22px;display:flex;align-items:center;gap:10px}}
h2 b{{font-family:var(--fn);width:30px;height:30px;border-radius:50%;background:var(--ink);color:var(--bg);display:inline-flex;align-items:center;justify-content:center;font-size:16px;flex:none}}
p{{margin:0;line-height:1.7;color:var(--muted)}}
.acts{{display:flex;flex-wrap:wrap;gap:10px}}
.btn,.save{{display:inline-flex;align-items:center;gap:8px;font:inherit;font-weight:700;border-radius:12px;cursor:pointer;min-height:44px}}
.btn{{background:var(--blue);color:#FFFFFF;text-decoration:none;font-size:18px;padding:10px 22px}}
.save{{background:var(--soft);color:var(--blue);border:1.5px solid var(--blue);font-size:16px;padding:8px 16px}}
.save svg{{width:20px;height:20px;fill:none;stroke:currentColor;stroke-width:2.2;stroke-linecap:round;stroke-linejoin:round}}
.save[disabled]{{opacity:.6;cursor:progress}}
.save.done{{color:var(--ok);border-color:var(--ok)}}
.btn:focus-visible,.save:focus-visible{{outline:3px solid var(--accent);outline-offset:3px}}
video{{width:100%;max-width:100%;border-radius:12px;background:#000;aspect-ratio:16/9}}
.sheets{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}}
.sheets figure{{margin:0;display:flex;flex-direction:column;gap:8px;align-items:center;min-width:0}}
.sheets img{{border:1px solid var(--line);border-radius:10px;width:100%;height:auto;background:#fff}}
figcaption{{font-size:14px;color:var(--muted)}}
.msg{{font-size:14px;color:var(--muted);min-height:1.4em}}
.hide-saves .save{{display:none}}
@media (max-width:640px){{.sheets{{grid-template-columns:minmax(0,1fr)}}}}
</style>
<div class="wrap" id="app">
<header>
  <span class="eyebrow">{html.escape(A.meta)}</span>
  <h1>الدرس <span class="n">{html.escape(A.code)}</span>: {T}</h1>
  <p class="lead">تحضير الدرس كاملاً في صفحة واحدة. زرّ «حفظ» تحت كل جزء يحفظه في جهازك: على الهاتف تظهر قائمة المشاركة، فاختر «حفظ في الصور» للفيديو والصور أو «حفظ في الملفات».</p>
</header>

<section id="deck">
  <h2><b>١</b>العرض التفاعلي</h2>
  <p>{ar(A.slides)} شريحة{A.deck_note or ' لحصة مدّتها ٤٠ دقيقة'}. التنقّل بالزرّين في الزاوية السفلية اليمنى، أو بالأسهم، أو بالسحب بالإصبع.</p>
  <div class="acts"><a class="btn" href="deck.html">افتح العرض التفاعلي ←</a>{btn("deck.html", NAMES["deck"], "حفظ العرض في الملفات")}</div>
</section>

{VIDEO}
<section id="sheet">
  <h2><b>{'٣' if A.video else '٢'}</b>ورقة الملخّص للطلاب</h2>
  <p>صورٌ لمجموعة الصف، وملف PDF للطباعة.</p>
  <div class="sheets">{sheets}</div>
  <div class="acts">{btn("summary.pdf", NAMES["pdf"], "حفظ الملخّص PDF")}</div>
</section>
<p class="msg" id="msg" role="status" aria-live="polite"></p>
</div>
<script>
(async function () {{
  const app = document.getElementById('app'), msg = document.getElementById('msg');
  let dl = null;
  try {{ dl = window.claude && window.claude.use ? await window.claude.use('downloads') : null; }} catch (e) {{ dl = null; }}
  if (!dl) {{ app.classList.add('hide-saves'); return; }}
  document.querySelectorAll('.save').forEach(function (b) {{
    const label = b.querySelector('span'), orig = label.textContent;
    b.addEventListener('click', async function () {{
      b.disabled = true; label.textContent = 'جارٍ التجهيز…'; msg.textContent = '';
      try {{
        const r = await fetch(b.dataset.src);
        if (!r.ok) throw {{ code: 'fetch' }};
        await dl.save({{ filename: b.dataset.name, data: await r.blob() }});
        b.classList.add('done'); label.textContent = 'تمّ ✓';
      }} catch (e) {{
        const c = e && e.code;
        label.textContent = orig;
        if (c === 'declined') msg.textContent = 'أُلغي الحفظ.';
        else if (c === 'rate_limited') msg.textContent = 'نافذة حفظٍ أخرى مفتوحة؛ أكملها ثم أعد المحاولة.';
        else if (c === 'fetch') msg.textContent = 'تعذّر تحميل الملف؛ تحقّق من الاتصال ثم أعد المحاولة.';
        else {{ msg.textContent = 'الحفظ غير متاح في هذا العرض.'; app.classList.add('hide-saves'); }}
      }} finally {{ b.disabled = false; }}
    }});
  }});
}})();
</script>
'''
open(os.path.join(A.out, 'index.html'), 'w', encoding='utf-8').write(page)
print(os.path.join(A.out, 'index.html'), sorted(os.listdir(A.out)))
