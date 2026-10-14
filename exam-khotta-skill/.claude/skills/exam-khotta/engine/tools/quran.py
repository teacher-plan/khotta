#!/usr/bin/env python3
# نصّ الآيات القرآنية من مصدر موثّق (quran.com) — لا تُكتب آيةٌ من الذاكرة أبداً.
#
#   python3 quran.py 112:1-4                 ← الآيات ١–٤ من سورة الإخلاص بالرسم العثماني، مع أرقامها
#   python3 quran.py 2:255 --script imlaei   ← بالرسم الإملائي المشكول (كما في كثير من الكتب المدرسية)
#   python3 quran.py 103 --json              ← السورة كاملة، بصيغة JSON (للصق في ملف الاختبار داخل quran{…})
#   python3 quran.py --check "قُلْ هُوَ ٱللَّهُ أَحَدٌ" --ref 112:1   ← يقارن نصّاً مكتوباً بالمصدر حرفاً حرفاً (الآية أو جزءاً متّصلاً منها)
#
# الرسم: uthmani (المصحف، الافتراضي) أو imlaei (إملائي مشكول). اختر ما يطابق كتاب الطالب، وانظر في صفحته للتأكّد.
# الخط في PDF: Amiri Quran (مضمّن). في Word: «Traditional Arabic» أو خط مصحف مثبّت عند المعلّم (quran_font).
import argparse, json, os, re, sys, unicodedata
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import http_get

API = 'https://api.quran.com/api/v4'
AR = '٠١٢٣٤٥٦٧٨٩'
SURAH_AYAHS = None


def surah_len(s):
    global SURAH_AYAHS
    if SURAH_AYAHS is None:
        data = json.loads(http_get(f'{API}/chapters?language=ar'))
        SURAH_AYAHS = {c['id']: (c['verses_count'], c['name_arabic']) for c in data['chapters']}
    return SURAH_AYAHS[s]


def parse_ref(ref):
    m = re.fullmatch(r'(\d{1,3})(?::(\d{1,3})(?:-(\d{1,3}))?)?', ref.strip())
    if not m:
        raise SystemExit(f'مرجع غير صحيح «{ref}» (أمثلة: 112، 112:1، 2:255، 112:1-4)')
    s = int(m.group(1))
    n, name = surah_len(s)
    a = int(m.group(2) or 1); b = int(m.group(3) or (m.group(2) or n))
    if not (1 <= a <= b <= n):
        raise SystemExit(f'سورة {name} فيها {n} آية؛ النطاق {a}-{b} غير صحيح')
    return s, a, b, name


def fetch(s, a, b, script='uthmani'):
    field = 'text_uthmani' if script == 'uthmani' else 'text_imlaei'
    out = []
    page = 1
    while True:
        d = json.loads(http_get(f'{API}/verses/by_chapter/{s}?fields={field}&per_page=50&page={page}'))
        for v in d['verses']:
            if a <= v['verse_number'] <= b:
                out.append((v['verse_number'], v[field].strip()))
        if not d['pagination'].get('next_page') or (out and out[-1][0] >= b):
            break
        page = d['pagination']['next_page']
    return out


def num(n):
    return ''.join(AR[int(c)] for c in str(n))


def strip_marks(t):
    """للمقارنة: يحذف علامات الوقف والزخرفة ويوحّد المسافات (يُبقي الحروف والحركات)."""
    t = unicodedata.normalize('NFC', t)
    t = re.sub('[ۖ-ٰۭۥۦ۞۩]', lambda m: '' if m.group() not in 'ٰ' else m.group(), t)
    return re.sub(r'\s+', ' ', t).strip()


def main():
    ap = argparse.ArgumentParser(description='نص الآيات من مصدر موثّق')
    ap.add_argument('ref', nargs='?'); ap.add_argument('--script', choices=['uthmani', 'imlaei'], default='uthmani')
    ap.add_argument('--json', action='store_true'); ap.add_argument('--check'); ap.add_argument('--ref', dest='ref2')
    a = ap.parse_args()
    ref = a.ref or a.ref2
    if not ref:
        ap.error('أعطِ مرجع الآية، مثل 112:1-4')
    s, x, y, name = parse_ref(ref)
    verses = fetch(s, x, y, a.script)
    if a.check:
        src = ' '.join(t for _, t in verses)
        got, want = strip_marks(a.check), strip_marks(src)
        if got == want or (len(got) > 8 and got in want):   # الآية كاملة، أو جزء متّصل منها (للاقتباس)
            print(f'✔ مطابق للمصدر ({name} {num(x)}{"-" + num(y) if y != x else ""})')
            return
        # أول موضع اختلاف
        i = next((k for k, (p, q) in enumerate(zip(got, want)) if p != q), min(len(got), len(want)))
        print(f'✘ يختلف عن المصدر عند الحرف {i}:\n  المكتوب: …{got[max(0, i - 15):i + 15]}…\n  المصدر:  …{want[max(0, i - 15):i + 15]}…')
        print(f'النص الصحيح:\n{src}')
        sys.exit(1)
    text = ' '.join(f'{t} ({num(n)})' for n, t in verses)
    if a.json:
        print(json.dumps({'ref': f'{s}:{x}-{y}', 'surah': name, 'script': a.script,
                          'verses': [{'n': n, 'text': t} for n, t in verses],
                          'markup': f'quran{{{text}}} [{name}: {num(x)}{"–" + num(y) if y != x else ""}]'},
                         ensure_ascii=False, indent=1))
    else:
        print(f'﴿{text}﴾  [{name}: {num(x)}{"–" + num(y) if y != x else ""}]')


if __name__ == '__main__':
    main()
