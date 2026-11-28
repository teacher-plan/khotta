# يجمع مخرجات الدرس في صفحة الحصة الحية (يُشغَّل في بيئة كلود).
# عدّل META فقط، ثم شغّل.
META = {"title": "عنوان الدرس", "subject": "المادة", "cls": "الصف", "unit": "", "objectives": [], "students": []}

import base64, glob, json, os, re
END = "<" + "/script>"
UP = [d for d in ["/mnt/user-data/uploads", "/mnt/data", "."] if os.path.isdir(d)]
OUT = next((d for d in ["/mnt/user-data/outputs", "/mnt/data", "."] if os.path.isdir(d)), ".")
def find(dirs, pat):
    return [p for d in dirs for p in glob.glob(os.path.join(d, "**", pat), recursive=True)]
def read(p):
    return open(p, encoding="utf-8", errors="ignore").read()
tpl = next(p for p in find(UP, "*.html") if 'id="skill"' in read(p) and 'id="data"' in read(p))
src = re.sub(r'(<script type="text/markdown" ' + 'id="skill">).*?(' + re.escape(END) + ')', r"\1\2", read(tpl), count=1, flags=re.S)
items = []
pdfs = find(UP + [OUT], "صفحات-الدرس*.pdf") or find(UP, "*.pdf")
if pdfs:
    items.append(("pages", sorted(pdfs, key=os.path.getmtime)[-1]))
for prefix, kind in [("عرض", "deck"), ("ملخص", "summary"), ("لعبة", "game"), ("كتاب-تفاعلي", "book")]:
    c = glob.glob(os.path.join(OUT, prefix + "-*.html"))
    if c:
        items.append((kind, sorted(c, key=os.path.getmtime)[-1]))
mime = {".html": "text/html", ".htm": "text/html", ".pdf": "application/pdf"}
data = dict(META, items=[{"kind": k, "name": os.path.basename(p), "mime": mime.get(os.path.splitext(p)[1].lower(), "application/octet-stream"),
                          "b64": base64.b64encode(open(p, "rb").read()).decode()} for k, p in items])
tag = '<script type="application/json" ' + 'id="data">'
i = src.rindex(tag) + len(tag); j = src.index(END, i)
html = src[:i] + json.dumps(data, ensure_ascii=False).replace("<", "\\u003c") + src[j:]
name = re.sub(r'[\\/:*?"<>|]', "-", META["title"] or "الحصة")
out = os.path.join(OUT, "حصة-" + name + ".html")
open(out, "w", encoding="utf-8").write(html)
print(out, [k for k, _ in items], round(os.path.getsize(out) / 1e6, 2), "MB")
