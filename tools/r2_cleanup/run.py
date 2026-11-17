#!/usr/bin/env python3
"""حذف صفحات الكتب وأدلّة المعلّم من مخزن Supabase بعد نقلها إلى Cloudflare R2.

لا يُحذف ملفٌ إلا إذا تحقّقت فيه الشروط الثلاثة معاً:
  ١) مسارُه في delete_list.tsv (قائمة ما نُسخ إلى R2 وتحقّق حجمه، ١٧ نوفمبر)،
  ٢) حجمُه في Supabase الآن = حجمه في القائمة (لم يتغيّر منذ النسخ)،
  ٣) يُحمَّل الآن من https://files.khotati.com بالحجم نفسه.
MODE=verify: فحصٌ فقط بلا حذف. MODE=delete: الحذف على دفعات من ١٠٠٠.
"""
import json, os, sys, urllib.request, urllib.parse
from concurrent.futures import ThreadPoolExecutor

REF = os.environ["REF"]; KEY = os.environ["SERVICE_KEY"]; MODE = os.environ.get("MODE", "verify")
SB = f"https://{REF}.supabase.co/storage/v1"; R2 = "https://files.khotati.com/library-files/"
H = {"Authorization": f"Bearer {KEY}", "apikey": KEY, "Content-Type": "application/json"}

def req(method, url, body=None, headers=None, timeout=60):
    r = urllib.request.Request(url, data=json.dumps(body).encode() if body is not None else None, method=method, headers=headers or {})
    with urllib.request.urlopen(r, timeout=timeout) as resp:
        return resp.status, dict(resp.headers), resp.read()

want = {}
for ln in open(os.path.join(os.path.dirname(__file__), "delete_list.tsv"), encoding="utf-8"):
    p, s = ln.rstrip("\n").split("\t"); want[p] = int(s)

# ٢) أحجام Supabase الحالية
cur, stack = {}, ["books", "teacher-guides"]
while stack:
    pfx = stack.pop(); off = 0
    while True:
        _, _, raw = req("POST", f"{SB}/object/list/library-files", {"prefix": pfx, "limit": 1000, "offset": off}, H)
        items = json.loads(raw)
        for it in items:
            full = f"{pfx}/{it['name']}"
            if it.get("id") is None: stack.append(full)
            else: cur[full] = int((it.get("metadata") or {}).get("size", -1))
        if len(items) < 1000: break
        off += 1000
print(f"Supabase now: {len(cur)} objects; list: {len(want)}")

cand = [p for p in want if cur.get(p) == want[p]]
changed = [p for p in want if p in cur and cur[p] != want[p]]
not_listed = [p for p in cur if p not in want]
print(f"size match: {len(cand)}  changed since copy: {len(changed)}  in Supabase but not copied: {len(not_listed)}")

# ٣) موجودٌ على R2 بالحجم نفسه
def r2ok(p):
    for _ in range(3):
        try:
            # وكيلٌ صريح: Cloudflare يرفض وكيل Python الافتراضي (Python-urllib) بـ 403
            st, hd, _ = req("HEAD", R2 + urllib.parse.quote(p, safe="/"), headers={"User-Agent": "khotta-cleanup/1.0"}, timeout=30)
            return st == 200 and int(hd.get("Content-Length", -1)) == want[p]
        except Exception:
            pass
    return False
with ThreadPoolExecutor(32) as ex:
    res = list(ex.map(r2ok, cand))
safe = [p for p, ok in zip(cand, res) if ok]
bad = [p for p, ok in zip(cand, res) if not ok]
print(f"verified on R2: {len(safe)}  NOT verified on R2: {len(bad)}")
for p in bad[:20]: print("  missing/size-mismatch on R2:", p)
print(f"bytes to free: {sum(want[p] for p in safe)/1048576:.1f} MiB")

if MODE != "delete":
    print("MODE=verify — nothing deleted"); sys.exit(0)
if bad:
    print("Refusing to delete: some files are not verified on R2"); sys.exit(1)
deleted = 0
for i in range(0, len(safe), 1000):
    batch = safe[i:i+1000]
    _, _, raw = req("DELETE", f"{SB}/object/library-files", {"prefixes": batch}, H, timeout=120)
    deleted += len(json.loads(raw) or [])
    print(f"deleted {deleted}/{len(safe)}", flush=True)
print(f"DONE deleted={deleted}")
