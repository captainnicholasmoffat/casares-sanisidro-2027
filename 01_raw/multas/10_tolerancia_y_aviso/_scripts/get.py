#!/usr/bin/env python3
# uso: get.py URL nombre_archivo "descripcion"
import sys, subprocess, os, re, html, datetime
O='/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/multas_raw/p2_tolerancia_y_aviso'
url, name, desc = sys.argv[1], sys.argv[2], sys.argv[3]
path=os.path.join(O,name)
ua='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'
r=subprocess.run(['curl','-sSL','--max-time','90','-A',ua,'-H','Accept-Language: es-AR,es;q=0.9,en;q=0.8','-o',path,'-w','%{http_code} %{content_type}',url],capture_output=True,text=True)
print('curl:',r.stdout,r.stderr.strip()[:300])
code=r.stdout.split(' ')[0]
if not os.path.exists(path) or os.path.getsize(path)==0 or not code.startswith('2'):
    if os.path.exists(path): os.remove(path)
    with open(os.path.join(O,'_noguardado.tsv'),'a') as f:
        f.write(f'(no guardado: HTTP {code} {r.stderr.strip()[:80]})\t-\t{url}\t{datetime.date.today().isoformat()}\t{desc}\n')
    print('FALLO',code); sys.exit(1)
size=os.path.getsize(path)
txt=None
with open(path,'rb') as f: head=f.read(5)
if head.startswith(b'%PDF'):
    import fitz
    d=fitz.open(path); t='\n'.join(f'=====PAGE {i+1}=====\n'+p.get_text() for i,p in enumerate(d))
    txt=path.rsplit('.',1)[0]+'.txt'; open(txt,'w').write(t)
else:
    from bs4 import BeautifulSoup
    s=BeautifulSoup(open(path,'rb').read(),'html.parser')
    for x in s(['script','style','noscript','svg']): x.decompose()
    t=s.get_text('\n'); t=re.sub(r'\n\s*\n+','\n',t)
    txt=path.rsplit('.',1)[0]+'.txt'
    if txt!=path: open(txt,'w').write(t)
today=datetime.date.today().isoformat()
with open(os.path.join(O,'_fuentes.tsv'),'a') as f:
    f.write(f'{name}\t{size}\t{url}\t{today}\t{desc}\n')
    if txt and txt!=path: f.write(f'{os.path.basename(txt)}\t{os.path.getsize(txt)}\t{url}\t{today}\tTexto extraído de {name}\n')
print('OK',name,size, 'txt:',os.path.basename(txt) if txt else None, os.path.getsize(txt) if txt else 0)
