# رفع فيديو الدرس إلى قناة الأستاذ عيسى على YouTube (YouTube Data API v3) — VIDEO.md القسم ٥-ب.
# المفاتيح من إعدادات البيئة فقط (لا تُكتب في المستودع ولا في المحادثة): YOUTUBE_CLIENT_ID و YOUTUBE_CLIENT_SECRET و YOUTUBE_REFRESH_TOKEN
#   python3 youtube_upload.py whoami                                   ← اسم القناة (للتحقّق من الربط)
#   python3 youtube_upload.py upload <ملف.mp4> "<العنوان>" "<الوصف>" [--playlist "<اسم القائمة>"] [--privacy private|unlisted|public]
# الرفع مستأنَف (resumable) بقطعٍ من ٨ ميغابايت. مشروع Google غير المُراجَع يجعل الفيديو خاصّاً مهما طُلب.
import json, os, sys, requests

API = 'https://www.googleapis.com/youtube/v3'
UP = 'https://www.googleapis.com/upload/youtube/v3/videos'

def token():
    need = ['YOUTUBE_CLIENT_ID', 'YOUTUBE_CLIENT_SECRET', 'YOUTUBE_REFRESH_TOKEN']
    miss = [k for k in need if not os.environ.get(k)]
    if miss: sys.exit('مفاتيح ناقصة في إعدادات البيئة: ' + '، '.join(miss))
    r = requests.post('https://oauth2.googleapis.com/token', data={
        'client_id': os.environ['YOUTUBE_CLIENT_ID'], 'client_secret': os.environ['YOUTUBE_CLIENT_SECRET'],
        'refresh_token': os.environ['YOUTUBE_REFRESH_TOKEN'], 'grant_type': 'refresh_token'}, timeout=30)
    if r.status_code != 200: sys.exit(f'تعذّر تجديد الرمز ({r.status_code}): {r.json().get("error_description", r.text[:200])}')
    return {'Authorization': 'Bearer ' + r.json()['access_token']}

def whoami(H):
    r = requests.get(f'{API}/channels', params={'part': 'snippet', 'mine': 'true'}, headers=H, timeout=30); r.raise_for_status()
    it = r.json().get('items', [])
    print(it[0]['snippet']['title'] if it else 'لا توجد قناة على هذا الحساب'); return it

def playlist(H, title):
    pg = None
    while True:
        r = requests.get(f'{API}/playlists', params={'part': 'snippet', 'mine': 'true', 'maxResults': 50, **({'pageToken': pg} if pg else {})}, headers=H, timeout=30); r.raise_for_status()
        for p in r.json().get('items', []):
            if p['snippet']['title'] == title: return p['id']
        pg = r.json().get('nextPageToken')
        if not pg: break
    r = requests.post(f'{API}/playlists', params={'part': 'snippet,status'}, headers=H, timeout=30,
                      json={'snippet': {'title': title, 'defaultLanguage': 'ar'}, 'status': {'privacyStatus': 'public'}}); r.raise_for_status()
    return r.json()['id']

def upload(H, path, title, desc, privacy='private', pl=None):
    meta = {'snippet': {'title': title[:100], 'description': desc[:5000], 'categoryId': '27', 'defaultLanguage': 'ar', 'defaultAudioLanguage': 'ar'},
            'status': {'privacyStatus': privacy, 'selfDeclaredMadeForKids': False}}
    size = os.path.getsize(path)
    r = requests.post(UP, params={'uploadType': 'resumable', 'part': 'snippet,status'}, json=meta, timeout=60,
                      headers={**H, 'X-Upload-Content-Type': 'video/mp4', 'X-Upload-Content-Length': str(size)})
    if r.status_code != 200: sys.exit(f'تعذّر بدء الرفع ({r.status_code}): {r.text[:300]}')
    loc, sent, CH = r.headers['Location'], 0, 8 * 1024 * 1024
    with open(path, 'rb') as f:
        while sent < size:
            chunk = f.read(CH)
            r = requests.put(loc, data=chunk, timeout=300, headers={**H, 'Content-Range': f'bytes {sent}-{sent + len(chunk) - 1}/{size}'})
            if r.status_code in (200, 201): break
            if r.status_code != 308: sys.exit(f'انقطع الرفع ({r.status_code}): {r.text[:300]}')
            rng = r.headers.get('Range'); sent = int(rng.split('-')[1]) + 1 if rng else 0; f.seek(sent)
    v = r.json(); vid = v['id']
    print(json.dumps({'id': vid, 'url': f'https://youtu.be/{vid}', 'privacy': v['status']['privacyStatus']}, ensure_ascii=False))
    if pl:
        r = requests.post(f'{API}/playlistItems', params={'part': 'snippet'}, headers=H, timeout=30,
                          json={'snippet': {'playlistId': playlist(H, pl), 'resourceId': {'kind': 'youtube#video', 'videoId': vid}}})
        print('القائمة:', pl, '✔' if r.ok else f'✘ {r.status_code} {r.text[:200]}')
    return vid

if __name__ == '__main__':
    a = sys.argv[1:]
    if not a: sys.exit(__doc__ or 'whoami | upload <mp4> <title> <desc> [--playlist X] [--privacy P]')
    H = token()
    if a[0] == 'whoami': whoami(H)
    elif a[0] == 'upload':
        opt = lambda k, d=None: a[a.index(k) + 1] if k in a else d
        upload(H, a[1], a[2], a[3], opt('--privacy', 'private'), opt('--playlist'))
