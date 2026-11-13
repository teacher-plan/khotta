#!/usr/bin/env python3
"""بحث في بنك برومبتات الموشن جرافيكس (videos.json — مجموعة awesome-opus5-5-videos، رخصة MIT).

أمثلة:
  python3 tools/motion-bank/search.py fraction pie --cat explainer
  python3 tools/motion-bank/search.py --cat motion --tag svg --tag gsap -n 15
  python3 tools/motion-bank/search.py --slug heyiamnick-119558 --full
  python3 tools/motion-bank/search.py --stats
"""
import argparse, json, os, re, sys, collections

HERE = os.path.dirname(os.path.abspath(__file__))


def load():
    with open(os.path.join(HERE, "videos.json"), encoding="utf-8") as f:
        data = json.load(f)
    for x in data:
        t = x.get("tech_tags")
        if isinstance(t, str):
            x["tech_tags"] = re.findall(r"[\w-]+", t)
        x["partial"] = str(x.get("prompt_partial")) == "True"
    return data


def score(x, words):
    text = (x.get("prompt") or "").lower()
    s = 0
    for w in words:
        n = text.count(w.lower())
        if n == 0:
            return 0
        s += 1 + min(n, 3)
    return s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("words", nargs="*", help="كلمات إنجليزية يجب أن ترد كلّها في البرومبت")
    ap.add_argument("--cat", choices=["motion", "explainer", "3d", "interactive"])
    ap.add_argument("--tag", action="append", default=[], help="canvas, svg, threejs, shader, gsap, css, audio, ...")
    ap.add_argument("--slug")
    ap.add_argument("--complete", action="store_true", help="البرومبتات الكاملة فقط (لا المقتطعة)")
    ap.add_argument("--full", action="store_true", help="اطبع البرومبت كاملاً")
    ap.add_argument("-n", type=int, default=10)
    ap.add_argument("--stats", action="store_true")
    a = ap.parse_args()
    data = load()
    if a.stats:
        print("العدد:", len(data))
        print("الفئات:", dict(collections.Counter(x["category"] for x in data)))
        print("التقنيات:", collections.Counter(t for x in data for t in x["tech_tags"]).most_common(20))
        return
    res = []
    for x in data:
        if a.slug and x["slug"] != a.slug:
            continue
        if a.cat and x["category"] != a.cat:
            continue
        if any(t not in x["tech_tags"] for t in a.tag):
            continue
        if a.complete and x["partial"]:
            continue
        s = score(x, a.words) if a.words else 1
        if s:
            res.append((s, len(x.get("prompt") or ""), x))
    res.sort(key=lambda r: (-r[0], -r[1]))
    print(f"# {len(res)} نتيجة")
    for s, _, x in res[: a.n]:
        p = re.sub(r"[ \t]+", " ", (x.get("prompt") or "")).strip()
        if not a.full and len(p) > 420:
            p = p[:420] + " …"
        print(f"\n## {x['slug']}  [{x['category']}] {', '.join(x['tech_tags'])}{'  (مقتطع)' if x['partial'] else ''}")
        print(f"by @{x['author']} — {x['post_url']}")
        print(p)


if __name__ == "__main__":
    sys.exit(main())
