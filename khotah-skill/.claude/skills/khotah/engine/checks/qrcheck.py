# فحص رموز QR في ورقة الملخّص قبل التسليم (rules/GENERAL.md «تمارين تدرّب وإجاباتها»):
#   python3 engine/checks/qrcheck.py ملخص.html
# ١) يصوّر صفحات الورقة كما ستُطبع (sheet.mjs --png) ثم يقرأ كل رمز بـ OpenCV.
# ٢) يقارن النصّ المقروء بالنصّ المحفوظ في ملخص.html.qr.json حرفاً بحرف.
# ٣) يتحقّق أن مقاس كل رمز ٢٫٥ سم على الأقل، ويعيد القراءة بدقّة منخفضة (تحاكي صورة واتساب).
# المتطلبات: pip install opencv-python-headless (أو opencv-python). إن تعذّر التثبيت يطبع ذلك ويخرج بالرمز ٣.
import sys, os, json, subprocess, tempfile, glob, re
HERE = os.path.dirname(os.path.abspath(__file__))
f = os.path.abspath(sys.argv[1])
want = json.load(open(f + '.qr.json', encoding='utf-8')) if os.path.exists(f + '.qr.json') else []
if not want: print('لا رموز QR في الورقة'); sys.exit(0)
try:
    import cv2
except ImportError:
    print('⚠ لا قارئ QR: ثبّت opencv-python-headless ثم أعد الفحص (لم يُتحقَّق من الرموز).'); sys.exit(3)
# المقاس المطبوع
html = open(f, encoding='utf-8').read()
sizes = [float(x) for x in re.findall(r'class="qr" style="width:([\d.]+)mm', html)]
small = [s for s in sizes if s < 25]
tmp = tempfile.mkdtemp()
subprocess.run(['node', os.path.join(HERE, 'sheet.mjs'), f, tmp, '--png'], check=True, stdout=subprocess.DEVNULL)
det = cv2.QRCodeDetector()
got = []
lowres = []
for png in sorted(glob.glob(os.path.join(tmp, '*.png'))):
    img = cv2.imread(png)
    for scale, bag in ((1.0, got), (0.6, lowres)):
        im = img if scale == 1 else cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
        ok, texts, _, _ = det.detectAndDecodeMulti(im)
        if ok: bag += [t for t in texts if t]
        # احتياط: قراءة كل رمز وحده إن فشلت القراءة المتعدّدة
        if not ok or len([t for t in texts if t]) == 0:
            t, _, _ = det.detectAndDecode(im)
            if t: bag.append(t)
        # احتياط ثانٍ: على الصفحة كاملةً قد يكتشف OpenCV الرمز ولا يفكّه (مربّعات أرقام الخطوات تشبه علامات الزوايا).
        # الهاتف يؤطّر الرمز وحده، فنحاكيه بنوافذ متداخلة (ثلث الصفحة) ونفكّ كلاً منها.
        if not all(w in bag for w in want):
            H, W = im.shape[:2]; th, tw = H // 3, W // 2
            for y in range(0, H - th // 2, th // 2):
                for x in range(0, W - tw // 2, tw // 2):
                    t, _, _ = det.detectAndDecode(im[y:y + th, x:x + tw])
                    if t: bag.append(t)
miss = [w for w in want if w not in got]
miss_low = [w for w in want if w not in lowres]
print(os.path.basename(f), f'رموز: {len(want)} · قُرئ: {len(set(got) & set(want))}' + (f' · مقاس أصغر من ٢٥ مم: {small}' if small else ''))
for w in miss: print('  ✘ لم يُقرأ أو اختلف:', w.replace('\n', ' | ')[:120])
for w in miss_low:
    if w not in miss: print('  ⚠ لا يُقرأ بدقّة منخفضة (صورة مضغوطة):', w.replace('\n', ' | ')[:80])
print('  نظيف' if not miss and not small else '  يحتاج إصلاحاً')
sys.exit(1 if miss or small else 0)
