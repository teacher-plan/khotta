"""يبني «صانع-صفحة-الحصة.html» من builder.src.html وruntime.html."""
import json, os
here = os.path.dirname(os.path.abspath(__file__))
rt = open(os.path.join(here, 'runtime.html'), encoding='utf-8').read()
src = open(os.path.join(here, 'builder.src.html'), encoding='utf-8').read()
lit = json.dumps(rt, ensure_ascii=False).replace('</', '<\\/')
out = os.path.join(here, '..', 'صانع-صفحة-الحصة.html')
open(out, 'w', encoding='utf-8').write(src.replace('__RUNTIME__', lit))
print(os.path.getsize(out), 'bytes')
