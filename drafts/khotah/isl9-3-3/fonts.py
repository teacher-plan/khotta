# تنزيل خطّي Noto Naskh/Kufi Arabic (المتغيّرين) وتقليصهما إلى حروف العرض فقط، ثم حذف خطوط المحرّك غير المستخدمة
import re,sys,base64,subprocess,io,os
from fontTools import subset
from fontTools.ttLib import TTFont
D=os.path.dirname(os.path.abspath(__file__)); html=sys.argv[1]
def get(u): return subprocess.run(['curl','-sS','-A','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36',u],capture_output=True,check=True).stdout
h=open(html,encoding='utf-8').read()
txt=re.sub(r'<script.*?</script>|<style.*?</style>','',h,flags=re.S); txt=re.sub(r'<[^>]+>',' ',txt)+'٠١٢٣٤٥٦٧٨٩0123456789()[]«»:،؛؟!.-–ـ'
out=[]
for fam,q in (('Noto Naskh Arabic','Noto+Naskh+Arabic:wght@400..700'),('Noto Kufi Arabic','Noto+Kufi+Arabic:wght@400..800')):
    css=get('https://fonts.googleapis.com/css2?family='+q).decode()
    url=re.search(r'/\* arabic \*/\s*@font-face\s*\{[^}]*url\((https://[^)]+)\)',css)[1]
    f=TTFont(io.BytesIO(get(url)))
    o=subset.Options(); o.flavor='woff2'; o.layout_features=['*']; o.name_IDs=['*']
    s=subset.Subsetter(o); s.populate(text=txt); s.subset(f)
    b=io.BytesIO(); f.flavor='woff2'; f.save(b)
    w='400 700' if 'Naskh' in fam else '400 800'
    out.append(f"@font-face{{font-family:'{fam}';font-weight:{w};font-display:block;src:url(data:font/woff2;base64,{base64.b64encode(b.getvalue()).decode()}) format('woff2')}}")
    print(fam,len(b.getvalue()))
open(os.path.join(D,'fonts_sub.css'),'w').write('\n'.join(out))
