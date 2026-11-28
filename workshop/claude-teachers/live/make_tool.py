# يصنع «أداة تحضير الدروس» للمعلّم في ملف واحد: قالب وضع الحصة الحية (الهدية المرفقة)
# وفي أعلاه تعليماته ودروسه وملاحظاته، وسكربت جمع صفحة الحصة. يُشغَّل في بيئة كلود.
# اكتب الاسم في NAME، ونصّ الأداة كاملاً في TOOL_MD، ثم شغّل.
NAME = "اسم المعلّم"
TOOL_MD = """# أداة تحضير الدروس
"""

import glob, os, re
END = "<" + "/script>"
FENCE = "`" * 3
UP = [d for d in ["/mnt/user-data/uploads", "/mnt/data", "."] if os.path.isdir(d)]
OUT = next((d for d in ["/mnt/user-data/outputs", "/mnt/data", "."] if os.path.isdir(d)), ".")
def read(p):
    return open(p, encoding="utf-8", errors="ignore").read()
tpl = next(p for d in UP for p in glob.glob(os.path.join(d, "**", "*.html"), recursive=True)
           if 'id="skill"' in read(p) and 'id="data"' in read(p))
src = read(tpl)
block = re.search(r'<script type="text/markdown" ' + 'id="skill">(.*?)' + re.escape(END), src, re.S).group(1)
asm = re.search(FENCE + r"python\n(.*?)" + FENCE, block, re.S).group(1).strip()
body = (TOOL_MD.strip() + "\n\n## سكربت جمع صفحة الحصة\nشغّله كما هو بعد أن تملأ META فقط.\n\n" + FENCE + "python\n" + asm + "\n" + FENCE + "\n").replace(END, "<\\/script>")
src = re.sub(r'(<script type="text/markdown" ' + 'id="skill">).*?(' + re.escape(END) + ')', lambda m: m.group(1) + "\n" + body + "\n" + m.group(2), src, count=1, flags=re.S)
tag = '<script type="application/json" ' + 'id="data">'
i = src.rindex(tag) + len(tag); j = src.index(END, i)
src = src[:i] + '{"items":[]}' + src[j:]
out = os.path.join(OUT, "أداة-تحضير-دروس-" + re.sub(r'[\\/:*?"<>|]', "-", NAME) + ".html")
open(out, "w", encoding="utf-8").write(src)
print(out, round(os.path.getsize(out) / 1e3), "KB")
