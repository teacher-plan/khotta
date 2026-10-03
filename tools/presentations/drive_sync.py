# صفحة «رفع التحضيرات إلى Drive»: تجمع ملفات عدّة دروس وترفع كلّاً منها إلى مجلد درسه في Google Drive
# بضغطة زرّ واحدة «رفع الكل» (بحساب المعلّم، عبر موصل Google Drive) — ويُتخطّى ما رُفع سابقاً.
# python3 tools/presentations/drive_sync.py <مجلد_الخرج> <ملف_الدروس.json>
# ملف الدروس: [{"name": "١-٦ القوى والجذور", "folder": "<id>", "files": [["<مسار محلي>", "<العنوان في Drive>", "<mime>"], …]}, …]
#   بدل "folder" يمكن: "root": "<id>", "path": ["الوحدة الثانية", "٢-١ …"] — تُنشأ المجلدات الناقصة تلقائياً (ويُعاد استعمال الموجود بالاسم نفسه).
# ثم تُنشر بأداة Artifact: file_path=<الخرج>/index.html، root=<الخرج>، files=كل ما سواه،
# capabilities={"downloads": true, "mcp": {"servers": [{"server": "Google Drive", "tools": ["create_file", "search_files"]}]}}
import html, json, os, shutil, sys

out, spec = sys.argv[1], json.load(open(sys.argv[2], encoding='utf-8'))
os.makedirs(out, exist_ok=True)
EXT = {'text/html': 'html', 'video/mp4': 'mp4', 'image/png': 'png', 'application/pdf': 'pdf'}
items = []
for li, lesson in enumerate(spec, 1):
    for fi, (src, title, mime) in enumerate(lesson['files'], 1):
        pub = f'l{li}_{fi}.{EXT[mime]}'
        shutil.copy(src, os.path.join(out, pub))
        items.append({'src': pub, 'title': title, 'type': mime, 'folder': lesson.get('folder', ''), 'root': lesson.get('root', ''), 'path': lesson.get('path', []), 'lesson': lesson['name']})

page = '''<title>رفع التحضيرات إلى Drive</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Readex+Pro:wght@400;600;700&display=swap">
<style>
/* صفحة عملٍ واحدة: عنوان، حالة عامة، ثم قائمة الملفات مجمّعة حسب الدرس */
:root{--bg:#F6F8FB;--card:#FFFFFF;--ink:#14305C;--muted:#4A5E80;--line:#D5DFEC;--blue:#2563EB;--ok:#1B7A3E;--err:#B3261E;--soft:#EAF1FF;--f:'Readex Pro',Tahoma,sans-serif}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#0F1726;--card:#172238;--ink:#E6EDF7;--muted:#A9B8CF;--line:#2B3A55;--blue:#7AA7FF;--ok:#6BD39A;--err:#FF8A7A;--soft:#1F2F4D;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#0F1726;--card:#172238;--ink:#E6EDF7;--muted:#A9B8CF;--line:#2B3A55;--blue:#7AA7FF;--ok:#6BD39A;--err:#FF8A7A;--soft:#1F2F4D;color-scheme:dark}
body{background:var(--bg);color:var(--ink);font-family:var(--f);direction:rtl}
.wrap{max-width:820px;margin:0 auto;padding-inline:16px;padding-block:28px 48px;display:flex;flex-direction:column;gap:18px}
h1{margin:0;font-size:clamp(26px,5vw,36px)}
p{margin:0;color:var(--muted);line-height:1.7}
#status{font-weight:700;color:var(--ink);background:var(--soft);border-radius:12px;padding:12px 16px}
button{align-self:flex-start;font:inherit;font-weight:700;font-size:17px;background:var(--blue);color:#fff;border:0;border-radius:12px;padding:10px 22px;min-height:44px;cursor:pointer}
button:focus-visible{outline:3px solid var(--ink);outline-offset:3px}
section{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px 16px;display:flex;flex-direction:column;gap:8px}
h2{margin:0;font-size:19px}
ul{margin:0;padding:0;list-style:none;display:flex;flex-direction:column;gap:6px}
li{display:flex;justify-content:space-between;gap:10px;font-size:15px;padding:6px 10px;border-radius:8px;background:var(--soft);min-width:0}
li b{font-weight:600;overflow-wrap:anywhere}li span{flex:none}
li{flex-wrap:wrap}.sv{font-size:14px;min-height:40px;padding:6px 14px;background:var(--ok)}
.ok{color:var(--ok)}.err{color:var(--err)}
</style>
<div class="wrap">
<h1>رفع التحضيرات إلى Google Drive</h1>
<p>اضغط «رفع الكل» مرةً واحدة: يذهب كل ملف إلى مجلد درسه في «خطة — تحضير الدروس». الملف الموجود مسبقاً بالاسم نفسه لا يُكرَّر. أبقِ الصفحة مفتوحة حتى ينتهي.</p>
<button type="button" id="go">رفع الكل إلى Drive ↑</button>
<div id="status" role="status" aria-live="polite"></div>
<div id="list"></div>
</div>
<script>
const ITEMS = ''' + json.dumps(items, ensure_ascii=False) + ''';
(async function () {
  const S = 'Google Drive', status = document.getElementById('status'), go = document.getElementById('go'), list = document.getElementById('list');
  const rows = {};
  const groups = {};
  ITEMS.forEach(function (f) {
    if (!groups[f.lesson]) { const s = document.createElement('section'); s.innerHTML = '<h2></h2><ul></ul>'; s.firstChild.textContent = f.lesson; list.appendChild(s); groups[f.lesson] = s.lastChild; }
    const li = document.createElement('li'); li.innerHTML = '<b></b><span>في الانتظار</span>'; li.firstChild.textContent = f.title; groups[f.lesson].appendChild(li); rows[f.src] = li.lastChild;
  });
  let mcp = null;
  try { mcp = window.claude && window.claude.use ? await window.claude.use('mcp') : null; } catch (e) { mcp = null; }
  if (!mcp) { status.textContent = 'الرفع إلى Drive غير متاح هنا. افتح الصفحة من تطبيق Claude أو موقعه.'; go.hidden = true; return; }
  const FATAL = ['server_not_connected', 'server_not_found', 'needs_reauth', 'not_granted', 'consent_required', 'approval_required'];
  function why(e) {
    const c = e && e.code;
    if (c === 'server_not_connected' || c === 'server_not_found') return 'Google Drive غير مربوط: اربطه من إعدادات الموصلات في Claude ثم أعد المحاولة.';
    if (c === 'needs_reauth') return 'انتهت صلاحية ربط Drive: أعد ربطه من إعدادات الموصلات في Claude.';
    if (c === 'not_granted' || c === 'consent_required' || c === 'approval_required') return 'لم تُمنح الصفحة إذن الوصول إلى Drive: اضغط «أعد المحاولة» ووافق.';
    if (c === 'tool_error') return 'رفض Drive الملف: ' + (e.message || '');
    return 'تعذّر الرفع (' + (c || 'خطأ') + ')';
  }
  function b64(buf) { let s = '', a = new Uint8Array(buf); for (let i = 0; i < a.length; i += 0x8000) s += String.fromCharCode.apply(null, a.subarray(i, i + 0x8000)); return btoa(s); }
  let dl = null;
  try { dl = await window.claude.use('downloads'); } catch (e) { dl = null; }
  function offerSave(f, st) {
    if (!dl || st.parentNode.querySelector('.sv')) return;
    const b = document.createElement('button'); b.type = 'button'; b.className = 'sv'; b.textContent = 'احفظه ثم اختر Drive';
    b.addEventListener('click', async function () {
      b.disabled = true;
      try { await dl.save({ filename: f.title, data: await (await fetch(f.src)).blob() }); b.textContent = 'اختر «Drive» ثم مجلد «' + f.lesson + '» ✓'; }
      catch (e) { b.disabled = false; b.textContent = e && e.code === 'declined' ? 'أُلغي — اضغط مجدداً' : 'تعذّر الحفظ هنا'; }
    });
    st.parentNode.appendChild(b);
  }
  const FOLDER = 'application/vnd.google-apps.folder', fcache = {};
  function listOf(pl) { return pl && (pl.files || (Array.isArray(pl) ? pl : null)); }
  async function folderFor(f) {  // يحلّ مسار المجلد، وينشئ الناقص منه
    if (f.folder) return f.folder;
    let parent = f.root, key = f.root;
    for (const name of f.path) {
      key += '/' + name;
      if (!fcache[key]) {
        const ex = await mcp.callTool(S, 'search_files', { query: "title = '" + name.split("'").join('') + "' and parentId = '" + parent + "' and mimeType = '" + FOLDER + "'", excludeContentSnippets: true }, { cache: false });
        const got = listOf(ex && ex.payload);
        if (got && got.length) fcache[key] = got[0].id;
        else { const cr = await mcp.callTool(S, 'create_file', { title: name, parentId: parent, contentMimeType: FOLDER }); fcache[key] = cr && cr.payload && cr.payload.id; }
        if (!fcache[key]) throw { code: 'tool_error', message: 'تعذّر إنشاء المجلد ' + name };
      }
      parent = fcache[key];
    }
    return parent;
  }
  let running = false;
  async function run() {
    if (running) return; running = true; go.hidden = true;
    let fileArgs = false, done = 0, skipped = 0, failed = 0, fatal = '';
    try { const lt = await mcp.listTools(); fileArgs = !!(lt && lt.fileArgs); } catch (e) { fileArgs = false; }
    for (const f of ITEMS) {
      const st = rows[f.src];
      if (st.className === 'ok') { skipped++; continue; }
      if (fatal) { st.textContent = '—'; continue; }
      status.textContent = 'جارٍ رفع: ' + f.title;
      try {
        st.textContent = 'فحص…'; st.className = '';
        f.folder = await folderFor(f);
        const ex = await mcp.callTool(S, 'search_files', { query: "title = '" + f.title.split("'").join('') + "' and parentId = '" + f.folder + "'", excludeContentSnippets: true }, { cache: false });
        const pl = ex && ex.payload, found = pl && (pl.files || (Array.isArray(pl) ? pl : null));
        if (found && found.length) { st.textContent = 'موجود ✓'; st.className = 'ok'; skipped++; continue; }
        st.textContent = 'رفع…';
        const blob = await (await fetch(f.src)).blob();
        const input = { title: f.title, parentId: f.folder, contentMimeType: f.type, disableConversionToGoogleType: true };
        if (/^text\//.test(f.type) && blob.size < 1500000) input.textContent = await blob.text();   // النص أخفّ من base64 بالثلث
        else if (blob.size < 700000) input.base64Content = b64(await blob.arrayBuffer());
        else if (fileArgs) input.base64Content = { $file: { data: blob, name: f.src, type: f.type } };
        else throw { code: 'too_big' };
        await mcp.callTool(S, 'create_file', input);
        st.textContent = 'تمّ ✓'; st.className = 'ok'; done++;
      } catch (e) {
        failed++; st.className = 'err';
        st.textContent = (e && e.code === 'too_big' ? 'هذا العرض لا يرسل ملفاً بهذا الحجم إلى Drive' : why(e)) + (e && e.code && e.code !== 'too_big' ? ' [' + e.code + ']' : '');
        offerSave(f, st);
        if (e && FATAL.includes(e.code)) fatal = why(e);
      }
    }
    running = false;
    if (fatal) { status.textContent = fatal; go.textContent = 'أعد المحاولة'; go.hidden = false; }
    else if (failed) { status.textContent = 'انتهى: رُفع ' + done + '، وكان موجوداً ' + skipped + '، وتعذّر ' + failed + '. اضغط «أعد المحاولة» للباقي.'; go.textContent = 'أعد المحاولة'; go.hidden = false; }
    else status.textContent = 'اكتمل ✓ — رُفع ' + done + ' ملفاً، وكان موجوداً ' + skipped + '. يمكنك إغلاق الصفحة.';
  }
  go.addEventListener('click', function () { go.hidden = true; run(); });
})();
</script>
'''
open(os.path.join(out, 'index.html'), 'w', encoding='utf-8').write(page)
print(os.path.join(out, 'index.html'), len(items), 'ملفاً')
