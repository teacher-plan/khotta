# تدقيق آلي لأخطاء التشكيل البنيوية وعلامات الترقيم في النص العربي.
# لا يحكم على صحة الإعراب (ذلك على الوكيل والمعلّم)، بل يكشف ما لا يصحّ كتابةً في أي حال:
#   حركة بلا حرف، حركتان على حرف، تنوين وسط الكلمة، سكون مع حركة، حركة على ألف المدّ أو الألف الممدودة،
#   تنوين فتح بلا ألف بعده (إلا على التاء المربوطة والهمزة المتطرفة)، ة أو ى وسط الكلمة، وترقيم لاتيني.
#   python3 arabic_check.py "نص"     أو من Python: check(text) ← [(نوع، رسالة)]  النوع: 'E' خطأ، 'W' تنبيه
import re, sys, unicodedata

FATHATAN, DAMMATAN, KASRATAN = 'ً', 'ٌ', 'ٍ'
FATHA, DAMMA, KASRA, SHADDA, SUKUN = 'َ', 'ُ', 'ِ', 'ّ', 'ْ'
DAGGER = 'ٰ'
TANWEEN = FATHATAN + DAMMATAN + KASRATAN
VOWELS = FATHA + DAMMA + KASRA
MARKS = TANWEEN + VOWELS + SHADDA + SUKUN + DAGGER
LETTER = re.compile(r'[ء-يٱ-ۓۺ-ۿ]')
QURAN_MARKS = re.compile('[ۖ-ۭٓ-ٟ]')   # علامات المصحف: لا تُدقّق


def words(text):
    return re.findall(r'[ء-ٰٟ-ۿـ]+', text)


def check(text, punctuation=True):
    out = []
    t = unicodedata.normalize('NFC', str(text or ''))
    # ١) حركة لا تتبع حرفاً
    for m in re.finditer(f'(^|[^\\u0621-\\u064a\\u0671-\\u06ff\\u0640{MARKS}])([{MARKS}])', t):
        out.append(('E', f'حركة «{m.group(2)}» ليست على حرف (قرب «{t[max(0, m.start() - 6):m.end() + 6]}»)'))
    for w in words(t):
        if QURAN_MARKS.search(w):
            continue
        # تقسيم الكلمة إلى (حرف، علاماته)
        units = re.findall(f'([^{MARKS}])([{MARKS}]*)', w)
        for i, (ch, mk) in enumerate(units):
            last = i == len(units) - 1
            vowels = [c for c in mk if c in VOWELS + TANWEEN]
            if len(vowels) > 1:
                out.append(('E', f'«{w}»: أكثر من حركة على «{ch}»'))
            if SUKUN in mk and (vowels or SHADDA in mk):
                out.append(('E', f'«{w}»: سكون مع حركة أو شدّة على «{ch}»'))
            if mk.count(SHADDA) > 1:
                out.append(('E', f'«{w}»: شدّتان على «{ch}»'))
            tn = [c for c in mk if c in TANWEEN]
            if tn:
                rest = units[i + 1:]
                ok_fath = tn[0] == FATHATAN and rest and all(r[0] in 'اى' and not r[1] for r in rest) and len(rest) == 1
                if not last and not ok_fath:
                    out.append(('E', f'«{w}»: تنوين وسط الكلمة على «{ch}»'))
                if tn[0] == FATHATAN and last and ch not in 'ةءأئؤا' and not (i > 0 and units[i - 1][0] == 'ا' and ch == 'ء'):
                    out.append(('W', f'«{w}»: تنوين فتح بلا ألف بعده (اكتب «{ch}ًا» إلا مع التاء المربوطة والهمزة)'))
            if ch == 'ا' and any(c in mk for c in VOWELS + TANWEEN + SUKUN):
                if i == 0:
                    if FATHA in mk or DAMMA in mk:   # «اَ» و«اُ» غالباً خطأ عن «أَ» و«أُ»؛ وكسرة همزة الوصل «اِ» جائزة
                        out.append(('W', f'«{w}»: ألف عليها فتحة أو ضمة في أول الكلمة؛ هل المقصود «أ»؟'))
                elif not (last and mk == FATHATAN):   # «كتاباً» (التنوين على الألف) جائز
                    out.append(('E', f'«{w}»: حركة على الألف الممدودة'))
            if ch == 'آ' and mk.strip(SHADDA):
                out.append(('W', f'«{w}»: حركة على ألف المدّ «آ»'))
            if ch in 'ةى' and not last:
                out.append(('E', f'«{w}»: «{ch}» لا تقع وسط الكلمة'))
    if punctuation:
        for m in re.finditer(r'[؀-ۿ][\s]*([,;?])', t):
            rep = {',': '،', ';': '؛', '?': '؟'}[m.group(1)]
            out.append(('W', f'ترقيم لاتيني «{m.group(1)}» بعد نص عربي: استعمل «{rep}»'))
        if '  ' in t:
            out.append(('W', 'مسافتان متتاليتان'))
    seen, uniq = set(), []
    for x in out:
        if x not in seen:
            seen.add(x); uniq.append(x)
    return uniq


if __name__ == '__main__':
    txt = ' '.join(sys.argv[1:]) or sys.stdin.read()
    res = check(txt)
    for k, msg in res:
        print('✘' if k == 'E' else '⚠', msg)
    if not res:
        print('✔ لا أخطاء بنيوية في التشكيل والترقيم')
    sys.exit(1 if any(k == 'E' for k, _ in res) else 0)
