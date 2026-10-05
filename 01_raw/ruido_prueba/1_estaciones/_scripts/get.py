#!/usr/bin/env python3
# uso: get.py URL nombre_base "descripcion" [ext]
import sys, os, subprocess, datetime, re
W='/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/ruido_raw/x1_estaciones'
url, base, desc = sys.argv[1], sys.argv[2], sys.argv[3]
ext = sys.argv[4] if len(sys.argv)>4 else None
tmp = os.path.join(W, '_tmp_dl')
ua='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'
r = subprocess.run(['curl','-sSL','--max-time','120','-A',ua,'-H','Accept-Language: es-AR,es;q=0.9,en;q=0.8','-o',tmp,'-w','%{http_code} %{content_type}',url],capture_output=True,text=True)
code_ct = r.stdout.strip()
if r.returncode!=0 or not os.path.exists(tmp):
    print('ERR', r.stderr, code_ct); sys.exit(1)
data=open(tmp,'rb').read()
if ext is None:
    if data[:4]==b'%PDF': ext='pdf'
    else: ext='html'
orig=os.path.join(W, base+'.'+ext)
os.replace(tmp, orig)
txt=os.path.join(W, base+'.txt')
if ext=='pdf':
    import pymupdf
    d=pymupdf.open(orig)
    out=[]
    for i,p in enumerate(d):
        out.append(f'\n--- p{i+1}\n'+p.get_text())
    open(txt,'w').write(''.join(out))
else:
    from bs4 import BeautifulSoup
    enc='utf-8'
    try:
        s=data.decode('utf-8')
    except UnicodeDecodeError:
        s=data.decode('latin-1')
    soup=BeautifulSoup(s,'html.parser')
    for t in soup(['script','style','noscript']): t.decompose()
    t=soup.get_text('\n')
    t=re.sub(r'\n\s*\n+','\n\n',t)
    open(txt,'w').write(t)
size=os.path.getsize(orig)
today=datetime.date.today().isoformat()
with open(os.path.join(W,'FUENTES.txt'),'a') as f:
    f.write(f'{os.path.basename(orig)} | {size} | {url} | {today} | {desc}\n')
print(code_ct, os.path.basename(orig), size, 'txt', os.path.getsize(txt))
