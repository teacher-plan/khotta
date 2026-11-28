# يجلب ملف الدرس من مستودع الورشة ويحفظه في المحادثة، ثم يجهّز صفحاته للقراءة.
# اكتب المفتاح واسم مجلد الدرس كما في الفهرس، ثم شغّل.
KEY = "math-10-1"
FOLDER = "١-٤ الميل"

import os, shutil, subprocess, urllib.parse, urllib.request
OUT = next((d for d in ["/mnt/user-data/outputs", "/mnt/data", "."] if os.path.isdir(d)), ".")
path = "lessons/%s/%s/صفحات-الدرس.pdf" % (KEY, FOLDER)
url = "https://raw.githubusercontent.com/popm18183-alt/workshop-skills/main/" + urllib.parse.quote(path)
dst = os.path.join(OUT, "صفحات-الدرس-" + FOLDER.replace("/", "-") + ".pdf")
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=60) as r, open(dst, "wb") as f:
    f.write(r.read())
assert open(dst, "rb").read(5) == b"%PDF-", "الملف ليس PDF"
pages = "/tmp/lesson-pages"
os.makedirs(pages, exist_ok=True)
if shutil.which("pdftoppm"):
    subprocess.run(["pdftoppm", "-r", "70", "-png", dst, os.path.join(pages, "p")], check=True)
if shutil.which("pdftotext"):
    subprocess.run(["pdftotext", "-layout", dst, os.path.join(pages, "text.txt")], check=True)
print(dst, round(os.path.getsize(dst) / 1e6, 2), "MB")
print(sorted(os.listdir(pages)))
