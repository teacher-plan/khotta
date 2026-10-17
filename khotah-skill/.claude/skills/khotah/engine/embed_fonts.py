import re,sys,base64,subprocess,urllib.request,ssl,os
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
def get(u):
    return subprocess.run(['curl','-sS','-A',UA,u],capture_output=True,check=True).stdout
def embed(q):
    css=get("https://fonts.googleapis.com/css2?"+q+"&display=swap").decode()
    out=[]
    for blk in re.findall(r'/\* (\w[\w-]*) \*/\s*(@font-face\s*\{[^}]*\})',css):
        sub,face=blk
        if sub not in ('arabic','latin'):continue
        url=re.search(r'url\((https://[^)]+)\)',face).group(1)
        data=base64.b64encode(get(url)).decode()
        out.append(face.replace(url,'data:font/woff2;base64,'+data))
    return '\n'.join(out)
if __name__=='__main__':
    open(sys.argv[2],'w').write(embed(sys.argv[1]))
