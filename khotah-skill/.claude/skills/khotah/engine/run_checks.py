# كل فحوص ما قبل التسليم في أمرٍ واحد:
#   python3 engine/run_checks.py --deck العرض.html --summary ملخص.html [--pdf-dir مجلد]
# العرض: ovf (الخروج من الشاشة) + boxovf (الخروج من المربّع) + overlap (التراكب وتناسق الخط) + dense (الازدحام) + fontaudit (حجم الخط ≥ ٤٫٢vh)
# الملخّص: sheetcheck (تراكب ورصّ وطول) + sheet (تحويل PDF) + qrcheck (قراءة رموز QR ومطابقتها)
import argparse, subprocess, os, sys
E = os.path.dirname(os.path.abspath(__file__)); C = os.path.join(E, 'checks')
ap = argparse.ArgumentParser(); ap.add_argument('--deck'); ap.add_argument('--summary'); ap.add_argument('--pdf-dir')
A = ap.parse_args()
def run(*cmd):
    print('▶', ' '.join(os.path.basename(c) if c.endswith(('.mjs', '.py')) else c for c in cmd), flush=True)
    return subprocess.run(cmd).returncode
rc = 0
if A.deck:
    for m in ('ovf.mjs', 'boxovf.mjs', 'overlap.mjs', 'dense.mjs'): rc |= run('node', os.path.join(C, m), A.deck)
    import re
    ui = re.findall(r'--ui:([\d.]+)\}', open(A.deck, encoding='utf-8').read())
    ui = float(ui[-1]) if ui else 1.0
    # الحدّ ٤٫٢vh قبل التصغير العامّ، فالحدّ المقيس = ٤٫٢ × ui (الأسس الصغيرة مستثناة بالنظر)
    rc |= run('node', os.path.join(C, 'fontaudit.mjs'), A.deck, f'{4.2 * ui:.2f}')
if A.summary:
    rc |= run('node', os.path.join(C, 'sheetcheck.mjs'), A.summary)
    out = A.pdf_dir or os.path.dirname(os.path.abspath(A.summary))
    rc |= run('node', os.path.join(C, 'sheet.mjs'), A.summary, out)
    rc |= run(sys.executable, os.path.join(C, 'qrcheck.py'), A.summary)
print('اقرأ النتائج أعلاه: كل سطر يجب أن يكون OK / لا تراكب / ٠ شريحة مزدحمة / نظيف.')
