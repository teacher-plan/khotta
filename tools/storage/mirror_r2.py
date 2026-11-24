"""ينسخ كل ملفات Supabase Storage (library-files وuser-files) إلى Cloudflare R2 بالمسار نفسه.
يطلب من دالة r2-files روابط رفعٍ موقّعة لما ينقص فقط، فيُعاد تشغيله بأمان. يطبع أعداداً فقط."""
import os, sys, json, tempfile, requests

URL = "https://mkdsnnfkkdwdkywnwnjh.supabase.co"
K = os.environ["SVC"]
H = {"Authorization": "Bearer " + K, "apikey": K}

def walk(bucket, prefix=""):
    off = 0
    while True:
        r = requests.post(f"{URL}/storage/v1/object/list/{bucket}", headers=H, json={"prefix": prefix, "limit": 1000, "offset": off}, timeout=60)
        r.raise_for_status(); rows = r.json()
        for x in rows:
            p = (prefix + "/" if prefix else "") + x["name"]
            if x.get("id") is None: yield from walk(bucket, p)
            else:
                md = x.get("metadata") or {}
                yield {"key": f"{bucket}/{p}", "size": int(md.get("size") or 0), "type": md.get("mimetype") or "application/octet-stream"}
        if len(rows) < 1000: break
        off += 1000

stats = {"total": 0, "exists": 0, "copied": 0, "failed": 0, "bytes": 0}
def run(batch):
    r = requests.post(f"{URL}/functions/v1/r2-files?mirror=1", headers=H, json={"items": batch}, timeout=120)
    r.raise_for_status()
    for it in r.json()["items"]:
        if it.get("skip") == "exists": stats["exists"] += 1; continue
        if "putUrl" not in it: stats["failed"] += 1; continue
        try:
            with tempfile.TemporaryFile() as f:
                with requests.get(f"{URL}/storage/v1/object/authenticated/{it['key']}", headers=H, stream=True, timeout=600) as g:
                    g.raise_for_status()
                    for c in g.iter_content(1 << 20): f.write(c)
                n = f.tell(); f.seek(0)
                p = requests.put(it["putUrl"], data=f, headers={"Content-Type": it["type"], "Content-Length": str(n)}, timeout=900)
                p.raise_for_status()
            stats["copied"] += 1; stats["bytes"] += n
        except Exception as e:
            stats["failed"] += 1; print("fail", type(e).__name__, file=sys.stderr)

for b in ("library-files", "user-files"):
    batch = []
    for it in walk(b):
        stats["total"] += 1; batch.append(it)
        if len(batch) == 40: run(batch); batch = []
    if batch: run(batch)
    print(b, json.dumps(stats), flush=True)
print("MIRROR", json.dumps(stats))
sys.exit(1 if stats["failed"] else 0)
