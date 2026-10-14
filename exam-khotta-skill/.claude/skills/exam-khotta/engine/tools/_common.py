# أدوات مشتركة لسكربتات tools/: التنزيل، وتطبيع النص العربي المستخرج من PDF، والأرقام، وفتح PDF.
# لا تحتاج إلا المكتبة القياسية و PyMuPDF (pip install pymupdf) و Pillow للصور.
import os, re, sys, time, json, ssl, unicodedata, urllib.request, urllib.parse

UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36'
AR_DIGITS = '٠١٢٣٤٥٦٧٨٩'


def log(*a):
    print(*a, file=sys.stderr, flush=True)


def _ctx():
    caf = os.environ.get('SSL_CERT_FILE')
    return ssl.create_default_context(cafile=caf) if caf and os.path.exists(caf) else ssl.create_default_context()


def http_get(url, binary=False, tries=4, timeout=90):
    """GET مع ترويسة متصفّح وإعادة محاولة (٢، ٤، ٨ ث). يعيد النص أو البايتات."""
    last = None
    for k in range(tries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept-Language': 'ar,en;q=0.8'})
            with urllib.request.urlopen(req, timeout=timeout, context=_ctx()) as r:
                data = r.read()
                return data if binary else data.decode('utf-8', 'ignore')
        except Exception as e:  # شبكة، 5xx، مهلة
            last = e
            if k < tries - 1:
                time.sleep(2 ** (k + 1))
    raise RuntimeError(f'تعذّر الوصول إلى {url}: {last}')


def download(url, path, tries=4):
    """ينزّل ملفاً كبيراً على دفعات إلى path، ويعيد حجمه بالبايت."""
    last = None
    for k in range(tries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': UA})
            with urllib.request.urlopen(req, timeout=300, context=_ctx()) as r, open(path + '.part', 'wb') as f:
                while True:
                    b = r.read(1 << 20)
                    if not b:
                        break
                    f.write(b)
            os.replace(path + '.part', path)
            return os.path.getsize(path)
        except Exception as e:
            last = e
            if k < tries - 1:
                time.sleep(2 ** (k + 1))
    raise RuntimeError(f'فشل تنزيل {url}: {last}')


def is_pdf(path):
    with open(path, 'rb') as f:
        return f.read(5) == b'%PDF-'


# ── النص العربي ──
_LAM_FIX = [('اإل', 'الإ'), ('األ', 'الأ'), ('اآل', 'الآ'), ('اال', 'الا')]   # لام-ألف مفكوكة معكوسة من بعض ملفات InDesign


def norm_ar(s):
    """يطبّع نصاً عربياً مستخرجاً من PDF للبحث والمطابقة (لا للعرض)."""
    s = unicodedata.normalize('NFKC', s or '')
    for a, b in _LAM_FIX:
        s = s.replace(a, b)
    s = re.sub('[ً-ْـ]', '', s)          # الحركات والتطويل
    s = s.replace('أ', 'ا').replace('إ', 'ا').replace('آ', 'ا').replace('ة', 'ه').replace('ى', 'ي')
    s = s.translate(str.maketrans(AR_DIGITS + '۰۱۲۳۴۵۶۷۸۹', '0123456789' * 2))
    return re.sub(r'\s+', ' ', s).strip()


def to_ar(n):
    return str(n).translate(str.maketrans('0123456789', AR_DIGITS))


def to_int(s):
    s = str(s).translate(str.maketrans(AR_DIGITS, '0123456789'))
    return int(s) if s.isdigit() else None


# ── PDF ──
def open_pdf(path):
    try:
        import pymupdf
    except ImportError:
        import fitz as pymupdf
    return pymupdf.open(path)


def render(page, out, dpi=110, clip=None):
    pix = page.get_pixmap(dpi=dpi, clip=clip)
    pix.save(out)
    return out


def save_json(obj, path):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
