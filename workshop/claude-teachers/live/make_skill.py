# يصنع ملف مهارة المعلّم: قالب الحصة الحية وفي أعلاه تعليماته (يُشغَّل في بيئة كلود).
# اكتب نصّ المهارة في SKILL_MD، والاسم في NAME، ثم شغّل.
NAME = "اسم المعلّم"
SKILL_MD = """# مهارة تحضير الدروس
"""

import glob, json, os, re
END = "<" + "/script>"
UP = [d for d in ["/mnt/user-data/uploads", "/mnt/data", "."] if os.path.isdir(d)]
OUT = next((d for d in ["/mnt/user-data/outputs", "/mnt/data", "."] if os.path.isdir(d)), ".")
def read(p):
    return open(p, encoding="utf-8", errors="ignore").read()
tpl = next(p for d in UP for p in glob.glob(os.path.join(d, "**", "*.html"), recursive=True)
           if 'id="skill"' in read(p) and 'id="data"' in read(p))
src = read(tpl)
body = SKILL_MD.replace(END, "<\\/script>")
src = re.sub(r'(<script type="text/markdown" id="skill">).*?(' + re.escape(END) + ')', lambda m: m.group(1) + "\n" + body + "\n" + m.group(2), src, count=1, flags=re.S)
tag = '<script type="application/json" id="data">'
i = src.index(tag) + len(tag); j = src.index(END, i)
src = src[:i] + '{"items":[]}' + src[j:]
out = os.path.join(OUT, "مهارة-تحضير-دروس-" + re.sub(r'[\\/:*?"<>|]', "-", NAME) + ".html")
open(out, "w", encoding="utf-8").write(src)
print(out, round(os.path.getsize(out) / 1e3), "KB")
