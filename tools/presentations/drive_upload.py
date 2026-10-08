# رفع ملفات التحضير إلى Google Drive مباشرةً من الجلسة (طلب الأستاذ عيسى، ٨ أكتوبر).
# لا تمرّ الملفات عبر المحادثة: السكربت يتّصل بواجهة Drive بنفسه بمفتاحٍ محفوظ سرّاً في إعدادات البيئة.
#
# المتغيّرات (تُضاف في إعدادات البيئة، ولا تُلصق في المحادثة أبداً):
#   GDRIVE_CLIENT_ID، GDRIVE_CLIENT_SECRET، GDRIVE_REFRESH_TOKEN — لحساب Drive المالك لمجلدات الدروس.
#
# الاستخدام:
#   python3 tools/presentations/drive_upload.py <المجلد> <ملف> [<ملف> …]          ← بأسمائها كما هي
#   python3 tools/presentations/drive_upload.py <المجلد> <ملف>=<الاسم في Drive> …
#   python3 tools/presentations/drive_upload.py --spec دروس.json                 ← صيغة drive_sync.py نفسها
#   python3 tools/presentations/drive_upload.py --check                           ← يتأكّد من المفتاح فقط
# الملف الموجود بالاسم نفسه في المجلد **يُستبدل محتواه** (يبقى رابطه كما هو)، وإلا يُنشأ ملفٌ جديد.
# أي حجم (الفيديو أيضاً): رفعٌ على دفعات (resumable).
import json, mimetypes, os, sys, urllib.parse, urllib.request, urllib.error

API = 'https://www.googleapis.com/drive/v3/files'
UP = 'https://www.googleapis.com/upload/drive/v3/files'
MIME = {'.html': 'text/html', '.pdf': 'application/pdf', '.mp4': 'video/mp4', '.mp3': 'audio/mpeg', '.png': 'image/png', '.jpg': 'image/jpeg'}
CHUNK = 8 * 1024 * 1024

def req(method, url, data=None, headers=None, raw=False):
    r = urllib.request.Request(url, data=data, method=method, headers=headers or {})
    try:
        with urllib.request.urlopen(r, timeout=300) as resp:
            body = resp.read()
            return (resp, body) if raw else (json.loads(body) if body else {})
    except urllib.error.HTTPError as e:
        if raw and e.code == 308: return e, b''
        raise SystemExit(f'خطأ من Drive ({e.code}): {e.read().decode(errors="replace")[:400]}')

def token():
    need = ['GDRIVE_CLIENT_ID', 'GDRIVE_CLIENT_SECRET', 'GDRIVE_REFRESH_TOKEN']
    miss = [k for k in need if not os.environ.get(k)]
    if miss: raise SystemExit('المفتاح غير مضاف في إعدادات البيئة: ' + '، '.join(miss) + ' (انظر DRIVE.md «الرفع التلقائي»)')
    body = urllib.parse.urlencode({'client_id': os.environ['GDRIVE_CLIENT_ID'], 'client_secret': os.environ['GDRIVE_CLIENT_SECRET'],
                                   'refresh_token': os.environ['GDRIVE_REFRESH_TOKEN'], 'grant_type': 'refresh_token'}).encode()
    return req('POST', 'https://oauth2.googleapis.com/token', body, {'Content-Type': 'application/x-www-form-urlencoded'})['access_token']

def find(tok, folder, name):
    q = f"'{folder}' in parents and name = '{name.replace(chr(39), chr(92) + chr(39))}' and trashed = false"
    r = req('GET', API + '?' + urllib.parse.urlencode({'q': q, 'fields': 'files(id,name,size)', 'supportsAllDrives': 'true', 'includeItemsFromAllDrives': 'true'}),
            headers={'Authorization': 'Bearer ' + tok})
    return r.get('files', [])

def upload(tok, folder, path, name=None):
    name = name or os.path.basename(path)
    mime = MIME.get(os.path.splitext(path)[1].lower()) or mimetypes.guess_type(path)[0] or 'application/octet-stream'
    size = os.path.getsize(path)
    old = find(tok, folder, name)
    h = {'Authorization': 'Bearer ' + tok, 'Content-Type': 'application/json; charset=UTF-8', 'X-Upload-Content-Type': mime, 'X-Upload-Content-Length': str(size)}
    if old:   # استبدال المحتوى: الرابط نفسه يبقى صالحاً
        meta, url, method = {}, f'{UP}/{old[0]["id"]}?uploadType=resumable&supportsAllDrives=true&fields=id,name,size', 'PATCH'
    else:
        meta, url, method = {'name': name, 'parents': [folder]}, f'{UP}?uploadType=resumable&supportsAllDrives=true&fields=id,name,size', 'POST'
    resp, _ = req(method, url, json.dumps(meta).encode(), h, raw=True)
    loc = resp.headers['Location']
    with open(path, 'rb') as f:
        off = 0
        while True:
            chunk = f.read(CHUNK)
            end = off + len(chunk) - 1
            hh = {'Content-Length': str(len(chunk)), 'Content-Range': f'bytes {off}-{end}/{size}' if size else 'bytes */0'}
            resp, body = req('PUT', loc, chunk, hh, raw=True)
            off += len(chunk)
            if getattr(resp, 'status', None) in (200, 201) or (body and off >= size):
                out = json.loads(body); break
    act = 'استُبدل' if old else 'رُفع'
    if len(old) > 1: act += f' (يوجد {len(old)} ملفات بالاسم نفسه؛ حُدّث الأول)'
    print(f'✔ {act}: {name} ({int(out.get("size", size)) // 1024} ك.ب) ← https://drive.google.com/file/d/{out["id"]}/view')
    return out

def main(a):
    if not a or a[0] in ('-h', '--help'): print(__doc__ or open(__file__, encoding='utf-8').read().split('import')[0]); return
    tok = token()
    if a[0] == '--check':
        me = req('GET', 'https://www.googleapis.com/drive/v3/about?fields=user(emailAddress)', headers={'Authorization': 'Bearer ' + tok})
        print('✔ المفتاح يعمل، الحساب:', me['user']['emailAddress']); return
    if a[0] == '--spec':
        for lesson in json.load(open(a[1], encoding='utf-8')):
            print('—', lesson['name'])
            for src, title, _mime in lesson['files']: upload(tok, lesson['folder'], src, title)
        return
    folder = a[0]
    for item in a[1:]:
        path, _, name = item.partition('=')
        upload(tok, folder, path, name or None)

if __name__ == '__main__':
    main(sys.argv[1:])
