# صفحة «تحضير الدرس»: العرض التفاعلي + الفيديو + ورقة الملخّص في رابطٍ واحد، مع زرّ حفظٍ لكل جزء
# (في تطبيق Claude على الهاتف يفتح الحفظ قائمة المشاركة: «حفظ في الصور» أو «حفظ في الملفات»).
#
# python3 tools/presentations/kit.py <مجلد_الخرج> --code "١-٧" --title "ترتيب العمليات الحسابية" \
#   --meta "الصف السابع · الوحدة الأولى · كتاب الطالب ص ٣٥" --slides 28 --minutes "٤ دقائق و٢٠ ثانية" \
#   --deck examples/ترتيب_العمليات_عرض_تفاعلي.html --video examples/فيديو_ترتيب_العمليات.mp4 \
#   --pdf examples/ملخصات/ملخص_ترتيب_العمليات.pdf
# ثم يُنشر المجلد بأداة Artifact: file_path=<الخرج>/index.html، root=<الخرج>، files=كل ما سواه،
# و capabilities={"downloads": true, "mcp": {"servers": [{"server": "Google Drive", "tools": ["create_file", "search_files"]}]}}.
# زرّ «ارفع التحضير إلى Google Drive» يرفع كل الملفات إلى مجلد الدرس (--drive-folder) بحساب المعلّم. التحديث لاحقاً: إعادة النشر بالـ url نفسه.
import argparse, html, os, shutil

AR = '٠١٢٣٤٥٦٧٨٩'
def ar(n): return ''.join(AR[int(c)] if c.isdigit() else c for c in str(n))

ap = argparse.ArgumentParser()
ap.add_argument('out'); ap.add_argument('--code', required=True); ap.add_argument('--title', required=True)
ap.add_argument('--meta', required=True); ap.add_argument('--slides', type=int, required=True); ap.add_argument('--minutes', default='')
ap.add_argument('--deck-note', default='')
ap.add_argument('--drive-folder', default='')  # معرّف مجلد الدرس في Google Drive (يُنشأ مسبقاً)
ap.add_argument('--deck', required=True); ap.add_argument('--video')  # اختياري (صفحات المراجعة بلا فيديو)
ap.add_argument('--sheets', nargs='*', default=[])  # اختياري: صور الملخّص (المعتمد الآن: PDF فقط)
ap.add_argument('--pdf', required=True)
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

DFILES = [('deck.html', NAMES['deck'], 'text/html')] + ([('video.mp4', NAMES['video'], 'video/mp4')] if A.video else []) + \
         [(f'sheet{i}.png', f'ملخص_{base}_{i}.png', 'image/png') for i in range(1, len(A.sheets) + 1)] + [('summary.pdf', NAMES['pdf'], 'application/pdf')]
import json as _json
DRIVE = (f'''<section id="drive" class="drive">
  <h2>☁️ الحفظ في Google Drive</h2>
  <p>ارفع ملفات هذا التحضير كلّها إلى مجلد الدرس في Drive بضغطةٍ واحدة. الملف الموجود مسبقاً لا يُكرَّر.</p>
  <div class="acts"><button type="button" class="btn" id="up">رفع التحضير إلى Drive ↑</button><a class="save" href="https://drive.google.com/drive/folders/{A.drive_folder}" target="_blank" rel="noopener">فتح مجلد الدرس</a></div>
  <ul class="ul" id="ul"></ul>
</section>
<script>window.KIT_DRIVE = {_json.dumps({'folder': A.drive_folder, 'files': [{'src': a_, 'title': b_, 'type': c_} for a_, b_, c_ in DFILES]}, ensure_ascii=False)};</script>
''' if A.drive_folder else '')
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
.drive{{border-color:var(--blue)}}
.ul{{margin:0;padding:0;list-style:none;display:flex;flex-direction:column;gap:6px}}
.ul li{{display:flex;justify-content:space-between;gap:10px;font-size:15px;padding:6px 10px;border-radius:8px;background:var(--soft)}}
.ul li b{{font-weight:600}}.ul .ok{{color:var(--ok)}}.ul .err{{color:var(--accent)}}
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

{DRIVE}<section id="deck">
  <h2><b>١</b>العرض التفاعلي</h2>
  <p>{ar(A.slides)} شريحة{A.deck_note or ' لحصة مدّتها ٤٠ دقيقة'}. التنقّل بالزرّين في الزاوية السفلية اليمنى، أو بالأسهم، أو بالسحب بالإصبع.</p>
  <div class="acts"><a class="btn" href="deck.html">افتح العرض التفاعلي ←</a>{btn("deck.html", NAMES["deck"], "حفظ العرض في الملفات")}</div>
</section>

{VIDEO}
<section id="sheet">
  <h2><b>{'٣' if A.video else '٢'}</b>ورقة الملخّص للطلاب</h2>
  <p>{'صورٌ لمجموعة الصف، وملف PDF للطباعة.' if A.sheets else 'ملف PDF واحد جاهز للطباعة وللإرسال في مجموعة الصف.'}</p>
  {f'<div class="sheets">{sheets}</div>' if A.sheets else ''}
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
(async function () {{
  const K = window.KIT_DRIVE, up = document.getElementById('up');
  if (!K || !up) return;
  const sec = document.getElementById('drive'), ul = document.getElementById('ul'), S = 'Google Drive';
  let mcp = null;
  try {{ mcp = window.claude && window.claude.use ? await window.claude.use('mcp') : null; }} catch (e) {{ mcp = null; }}
  if (!mcp) {{ sec.querySelector('p').textContent = 'الرفع إلى Drive غير متاح في هذا العرض. افتح الصفحة من تطبيق Claude أو موقعه.'; up.hidden = true; return; }}
  const q = (t) => String(t).split("'").join('');  // عناوين الملفات بلا علامات اقتباس
  function row(f) {{ const li = document.createElement('li'); li.innerHTML = '<b></b><span></span>'; li.firstChild.textContent = f.title; ul.appendChild(li); return li.lastChild; }}
  function why(e) {{
    const c = e && e.code;
    if (c === 'server_not_connected' || c === 'server_not_found') return 'Google Drive غير مربوط بحسابك: اربطه من إعدادات الموصلات في Claude.';
    if (c === 'needs_reauth') return 'انتهت صلاحية ربط Drive: أعد ربطه من إعدادات الموصلات في Claude.';
    if (c === 'not_granted' || c === 'consent_required' || c === 'approval_required') return 'لم تُمنح الصفحة إذن الوصول إلى Drive.';
    if (c === 'tool_error') return 'رفض Drive الملف: ' + (e.message || '');
    return 'تعذّر الرفع (' + (c || 'خطأ') + ')، أعد المحاولة لاحقاً.';
  }}
  function b64(buf) {{ let s = '', a = new Uint8Array(buf); for (let i = 0; i < a.length; i += 0x8000) s += String.fromCharCode.apply(null, a.subarray(i, i + 0x8000)); return btoa(s); }}
  up.addEventListener('click', async function () {{
    up.disabled = true; ul.innerHTML = ''; let files = false, stop = '';
    try {{ const lt = await mcp.listTools(); files = !!(lt && lt.fileArgs); }} catch (e) {{ files = false; }}
    for (const f of K.files) {{
      const st = row(f);
      if (stop) {{ st.textContent = '—'; continue; }}
      try {{
        st.textContent = 'فحص…';
        const ex = await mcp.callTool(S, 'search_files', {{ query: "title = '" + q(f.title) + "' and parentId = '" + K.folder + "'", excludeContentSnippets: true }}, {{ cache: false }});
        const pl = ex && ex.payload, list = pl && (pl.files || pl.items || (Array.isArray(pl) ? pl : null));
        if (list && list.length) {{ st.textContent = 'موجود ✓'; st.className = 'ok'; continue; }}
        st.textContent = 'رفع…';
        const blob = await (await fetch(f.src)).blob();
        const input = {{ title: f.title, parentId: K.folder, contentMimeType: f.type, disableConversionToGoogleType: true }};
        if (blob.size < 700000) input.base64Content = b64(await blob.arrayBuffer());
        else if (files) input.base64Content = {{ $file: {{ data: blob, name: f.src, type: f.type }} }};
        else throw {{ code: 'too_big' }};
        await mcp.callTool(S, 'create_file', input);
        st.textContent = 'تمّ ✓'; st.className = 'ok';
      }} catch (e) {{
        st.className = 'err';
        if (e && e.code === 'too_big') st.textContent = 'كبير جداً على هذا العرض: احفظه بزرّ «حفظ» ثم ارفعه يدوياً';
        else {{ st.textContent = why(e); if (['server_not_connected','server_not_found','needs_reauth','not_granted','consent_required','approval_required'].includes(e && e.code)) stop = e.code; }}
      }}
    }}
    up.disabled = false; up.textContent = 'أعد الرفع (يتخطّى الموجود)';
  }});
}})();
</script>
'''
open(os.path.join(A.out, 'index.html'), 'w', encoding='utf-8').write(page)
print(os.path.join(A.out, 'index.html'), sorted(os.listdir(A.out)))
