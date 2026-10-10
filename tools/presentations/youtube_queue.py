# رفع فيديوهات الوحدتين الثانية والثالثة إلى YouTube بدفعاتٍ يومية (حدّ الرفع ~١٠ في ٢٤ ساعة) — VIDEO.md ٥-ب.
#   python3 youtube_queue.py      ← يرفع من Drive بالترتيب ما ليس في قائمة وحدته بعد، مع الصورة المصغّرة، ويتوقّف عند الحدّ.
# بلا ملف حالة: ما في القائمة يُعدّ مرفوعاً. الصور المصغّرة وغلافا القائمتين تُرسم بـ youtube_art.py عند الحاجة.
import os, sys, json, glob, subprocess, requests
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); import youtube_upload as Y
ART = '/tmp/yt_art'
U = {2: ('الثانية', 'العبارات الجبرية والمعادلات والصيغ'), 3: ('الثالثة', 'الأعداد العشرية والكسور العشرية')}
J = [('2-1','٢-١','كتابة العبارات الجبرية','1hXBvU5SbaY0b1Fa91WuQmEziCd2U4AT0'),('2-2','٢-٢','تجميع الحدود المتشابهة','1rV86usu3lrzbv6gtYyQrssIAzRIOs-sM'),
 ('2-3','٢-٣','فك الأقواس','1FPAEhq0pjv-zM6ze4FVGBKP_4SaqSuom'),('2-4','٢-٤','استنتاج واستخدام الصيغ','1ciHWgcQV9oJE6DTPctuehSZjj5TI2ZP2'),
 ('2-5','٢-٥','كتابة المعادلات وحلها','12kmUnAwRzqlrrWO_0WachZwF0SMFDWVq'),('2-r','','','1LDbr4ondbvLytWZMFfDKuI-yhM7wIgIE'),
 ('3-1','٣-١','ترتيب الأعداد العشرية والكسور العشرية','1KsmraPn9sZW-p8oSI-BlDXl73BGPSI4c'),('3-2','٣-٢','التقريب','1SgoIQ1Csl3LMMhK1JIUR8cyrPdxpIlRF'),
 ('3-3','٣-٣','جمع الأعداد العشرية والكسور العشرية وطرحها','1C-WScQ0F4KxqtVtu-KD-Y9c2UuJ8Rub2'),('3-4','٣-٤','ضرب الأعداد العشرية والكسور العشرية','1Bkazi7Sb6yztp9GEc7XIq1b3KHInAt3C'),
 ('3-5','٣-٥','قسمة الأعداد العشرية والكسور العشرية (١)','1CmVhw3oIQv589Tx1mmIbidaZccGJ7KEn'),('3-6','٣-٦','قسمة الأعداد العشرية والكسور العشرية (٢)','1vZymzNkdTZQK0evRmZG75Ysm4rhqrBXs'),
 ('3-7','٣-٧','الضرب في ٠٫١ أو ٠٫٠١ والقسمة عليهما','1yE_DXtU_Xi6zbk8S-lCwAwDcQIGKpxEG'),('3-8','٣-٨','التقدير والتقريب','1pzcsw3PHDJTME8uPcdzDMNn2TCBPNMV-'),
 ('3-r','','','1EJJllpr1gblu_zdL8ae2_PD3HabwMAhq')]

def art(name):
    p = f'{ART}/{name}.jpg'
    if not os.path.exists(p):
        subprocess.run([sys.executable, os.path.join(HERE, 'youtube_art.py'), ART], check=True, capture_output=True)
        for png in glob.glob(f'{ART}/*.png'): subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', png, '-q:v', '3', png[:-4] + '.jpg'], check=True)
    return open(p, 'rb').read()

def titles(H, pid):
    out, pg = {}, None
    while True:
        r = requests.get(f'{Y.API}/playlistItems', params={'part': 'snippet', 'playlistId': pid, 'maxResults': 50, **({'pageToken': pg} if pg else {})}, headers=H, timeout=30).json()
        for i in r.get('items', []): out[i['snippet']['title']] = i['snippet']['resourceId']['videoId']
        pg = r.get('nextPageToken')
        if not pg: return out

def cover(H, pid, u):
    B = 'xxBOUNDxx'
    body = (f'--{B}\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n' + json.dumps({'snippet': {'playlistId': pid, 'type': 'hero'}}) + f'\r\n--{B}\r\nContent-Type: image/jpeg\r\n\r\n').encode() + art(f'cover_u{u}') + f'\r\n--{B}--'.encode()
    r = requests.post('https://www.googleapis.com/upload/youtube/v3/playlistImages', params={'part': 'snippet', 'uploadType': 'multipart'}, data=body, headers={**H, 'Content-Type': f'multipart/related; boundary={B}'}, timeout=60)
    print('غلاف قائمة الوحدة', u, '✔' if r.ok else f'✘ {r.status_code} {r.text[:150]}')

H = Y.token(); new, done = [], 0
for key, num, name, fid in J:
    u = int(key[0]); o, un = U[u]; pl = f'رياضيات الصف السابع — الوحدة {o}: {un}'
    if num: title, desc = f'الدرس {num}: {name} — رياضيات الصف السابع', f'شرح الدرس {num} من منهج الرياضيات للصف السابع، الوحدة {o}: {un}.\nإعداد: أ. عيسى الحارثي'
    else: title, desc = f'مراجعة الوحدة {o}: {un} — رياضيات الصف السابع', f'مراجعة الوحدة {o} كاملةً من منهج الرياضيات للصف السابع: {un}.\nإعداد: أ. عيسى الحارثي'
    pid = Y.playlist(H, pl); have = titles(H, pid)
    if title in have: done += 1; continue
    first = not have
    path = Y.from_drive(fid); size = os.path.getsize(path)
    meta = {'snippet': {'title': title, 'description': desc, 'categoryId': '27', 'defaultLanguage': 'ar', 'defaultAudioLanguage': 'ar'}, 'status': {'privacyStatus': 'private', 'selfDeclaredMadeForKids': False}}
    r = requests.post(Y.UP, params={'uploadType': 'resumable', 'part': 'snippet,status'}, json=meta, timeout=60, headers={**H, 'X-Upload-Content-Type': 'video/mp4', 'X-Upload-Content-Length': str(size)})
    if r.status_code != 200:
        os.remove(path); print('توقّف عند', key, 'uploadLimitExceeded (حدّ الرفع)' if 'uploadLimitExceeded' in r.text else f'{r.status_code} {r.text[:200]}'); break
    r = requests.put(r.headers['Location'], data=open(path, 'rb').read(), timeout=900, headers={**H, 'Content-Type': 'video/mp4'}); os.remove(path)
    if r.status_code not in (200, 201): print('فشل رفع', key, r.status_code, r.text[:200]); break
    vid = r.json()['id']
    t = requests.post('https://www.googleapis.com/upload/youtube/v3/thumbnails/set', params={'videoId': vid}, headers={**H, 'Content-Type': 'image/jpeg'}, data=art(f'thumb_{key}'), timeout=60)
    p = requests.post(f'{Y.API}/playlistItems', params={'part': 'snippet'}, headers=H, timeout=30, json={'snippet': {'playlistId': pid, 'resourceId': {'kind': 'youtube#video', 'videoId': vid}}})
    print(key, f'https://youtu.be/{vid}', 'صورة', '✔' if t.ok else '✘', 'قائمة', '✔' if p.ok else '✘')
    if first: cover(H, pid, u)
    new.append((key, vid)); done += 1
print(json.dumps({'new': new, 'done': done, 'total': len(J)}, ensure_ascii=False))
