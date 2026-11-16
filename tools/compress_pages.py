#!/usr/bin/env python3
"""ضغط صور صفحات الكتب وأدلّة المعلّم في مخزن Supabase في مكانها.

- الاسم والامتداد والنوع (image/jpeg) لا تتغيّر، فلا يتغيّر أي رابط أو كود.
- الدقّة (أبعاد الصورة) لا تتغيّر، فقط جودة الترميز.
- لا تُستبدل صورة إلا إذا صغرت ١٠٪ على الأقل.
- وضع sample: يقيس التوفير على عيّنة ويحفظ أمثلة قبل/بعد، بلا أي كتابة في المخزن.
- وضع apply: يحفظ نسخة احتياطية من الأصول (tar) ثم يستبدل الصور.

يعمل داخل GitHub Actions فقط (المتغيّرات: SERVICE_KEY، REF، MODE، QUALITY، OUT).
"""
import io, json, os, random, sys, tarfile, time, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor
from PIL import Image

REF = os.environ["REF"]
KEY = os.environ["SERVICE_KEY"]
MODE = os.environ.get("MODE", "sample")
QUALITY = int(os.environ.get("QUALITY", "65"))
OUT = os.environ.get("OUT", "/tmp/out")
BUCKET = "library-files"
BASE = f"https://{REF}.supabase.co/storage/v1"
os.makedirs(OUT, exist_ok=True)


def req(method, url, data=None, headers=None, tries=4):
    h = {"Authorization": f"Bearer {KEY}", "apikey": KEY}
    h.update(headers or {})
    for i in range(tries):
        try:
            r = urllib.request.Request(url, data=data, method=method, headers=h)
            with urllib.request.urlopen(r, timeout=60) as resp:
                return resp.read()
        except urllib.error.HTTPError as e:
            if e.code < 500 and e.code != 429:
                raise
        except Exception:
            pass
        time.sleep(2 ** i)
    raise RuntimeError(f"failed: {method} {url}")


def list_prefix(prefix):
    """يسرد كل الملفات تحت مجلد (تكراري)."""
    out = []
    stack = [prefix]
    while stack:
        p = stack.pop()
        off = 0
        while True:
            body = json.dumps({"prefix": p, "limit": 1000, "offset": off}).encode()
            items = json.loads(req("POST", f"{BASE}/object/list/{BUCKET}", body,
                                   {"Content-Type": "application/json"}))
            for it in items:
                full = f"{p}/{it['name']}" if p else it["name"]
                if it.get("id") is None:
                    stack.append(full)
                elif full.lower().endswith(".jpg"):
                    out.append((full, (it.get("metadata") or {}).get("size", 0)))
            if len(items) < 1000:
                break
            off += 1000
    return out


def encode(raw, q):
    im = Image.open(io.BytesIO(raw))
    im.load()
    if im.mode not in ("RGB", "L"):
        im = im.convert("RGB")
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=q, optimize=True, progressive=True, subsampling="4:2:0")
    return buf.getvalue(), im.size


def download(path):
    return req("GET", f"{BASE}/object/{BUCKET}/{urllib.parse.quote(path)}")


import urllib.parse  # noqa: E402

files = list_prefix("books") + list_prefix("teacher-guides")
total_before = sum(s for _, s in files)
print(f"عدد الصور: {len(files)}  الحجم الحالي: {total_before/1048576:.1f} MiB", flush=True)

if MODE == "sample":
    random.seed(7)
    sample = random.sample(files, min(200, len(files)))
    qs = [75, 70, 65, 60, 55]
    sums = {q: 0 for q in qs}
    base_sum = 0
    dims = {}
    for i, (path, _) in enumerate(sample):
        raw = download(path)
        base_sum += len(raw)
        for q in qs:
            new, size = encode(raw, q)
            sums[q] += min(len(new), len(raw))
        dims[size] = dims.get(size, 0) + 1
        if i < 4:
            stem = path.replace("/", "__")[:-4]
            open(f"{OUT}/{stem}__orig.jpg", "wb").write(raw)
            for q in (65, 60):
                open(f"{OUT}/{stem}__q{q}.jpg", "wb").write(encode(raw, q)[0])
    report = {"files": len(files), "total_mib": round(total_before / 1048576, 1),
              "sample": len(sample), "sample_mib": round(base_sum / 1048576, 2),
              "dims_top": sorted(dims.items(), key=lambda x: -x[1])[:5],
              "estimate": {}}
    for q in qs:
        ratio = sums[q] / base_sum
        report["estimate"][q] = {"ratio": round(ratio, 3),
                                 "after_mib": round(total_before * ratio / 1048576, 1),
                                 "saved_mib": round(total_before * (1 - ratio) / 1048576, 1)}
    print(json.dumps(report, ensure_ascii=False, indent=1, default=str))
    json.dump(report, open(f"{OUT}/report.json", "w"), ensure_ascii=False, indent=1, default=str)
    sys.exit(0)

# ── apply ──
backup = tarfile.open(f"{OUT}/originals.tar", "w")
stats = {"replaced": 0, "skipped": 0, "failed": 0, "before": 0, "after": 0}
fails = []


def work(item):
    path, _ = item
    try:
        raw = download(path)
        new, _ = encode(raw, QUALITY)
        return path, raw, new, None
    except Exception as e:  # noqa: BLE001
        return path, None, None, str(e)


def upload(path, data):
    req("PUT", f"{BASE}/object/{BUCKET}/{urllib.parse.quote(path)}", data,
        {"Content-Type": "image/jpeg", "x-upsert": "true", "cache-control": "3600"})


with ThreadPoolExecutor(16) as ex, ThreadPoolExecutor(16) as up:
    pending = []
    for n, (path, raw, new, err) in enumerate(ex.map(work, files), 1):
        if err:
            stats["failed"] += 1; fails.append((path, err)); continue
        ti = tarfile.TarInfo(path); ti.size = len(raw); ti.mtime = int(time.time())
        backup.addfile(ti, io.BytesIO(raw))
        stats["before"] += len(raw)
        if len(new) <= 0.9 * len(raw):
            pending.append((path, len(raw), len(new), up.submit(upload, path, new)))
        else:
            stats["skipped"] += 1; stats["after"] += len(raw)
        if n % 500 == 0:
            print(f"… {n}/{len(files)}", flush=True)
    for path, b, a, fut in pending:
        try:
            fut.result(); stats["replaced"] += 1; stats["after"] += a
        except Exception as e:  # noqa: BLE001
            stats["failed"] += 1; stats["after"] += b; fails.append((path, str(e)))
backup.close()
stats["before_mib"] = round(stats["before"] / 1048576, 1)
stats["after_mib"] = round(stats["after"] / 1048576, 1)
stats["saved_mib"] = round((stats["before"] - stats["after"]) / 1048576, 1)
stats["fails"] = fails[:50]
print(json.dumps(stats, ensure_ascii=False, indent=1))
json.dump(stats, open(f"{OUT}/report.json", "w"), ensure_ascii=False, indent=1)
sys.exit(1 if stats["failed"] else 0)
