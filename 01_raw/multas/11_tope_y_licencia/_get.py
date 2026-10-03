#!/usr/bin/env python3
# uso: _get.py URL nombre_archivo "descripcion"
import sys, subprocess, os, datetime, re, html
O=os.path.dirname(os.path.abspath(__file__))
url, name, desc = sys.argv[1], sys.argv[2], sys.argv[3]
path=os.path.join(O,name)
os.makedirs(os.path.dirname(path),exist_ok=True)
r=subprocess.run(['curl','-sSL','--max-time','90','-A','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36','-H','Accept-Language: es-AR,es;q=0.9,en;q=0.8','-o',path,'-w','%{http_code} %{content_type} %{url_effective}',url],capture_output=True,text=True)
print('curl:',r.stdout,r.stderr[:300])
if not os.path.exists(path) or os.path.getsize(path)==0:
    print('FALLO'); sys.exit(1)
size=os.path.getsize(path)
txt=os.path.splitext(path)[0]+'.txt'
data=open(path,'rb').read()
if data[:4]==b'%PDF':
    import pymupdf
    d=pymupdf.open(path); t='\n'.join(f'--- p{i+1}\n'+p.get_text() for i,p in enumerate(d))
else:
    for enc in ('utf-8','latin-1'):
        try: s=data.decode(enc); break
        except: pass
    s=re.sub(r'(?is)<(script|style|noscript)[^>]*>.*?</\1>',' ',s)
    s=re.sub(r'(?i)<br\s*/?>|</p>|</div>|</li>|</tr>|</h[1-6]>','\n',s)
    s=re.sub(r'<[^>]+>',' ',s); s=html.unescape(s)
    s=re.sub(r'[ \t\r\f\v]+',' ',s); t=re.sub(r'\n\s*\n+','\n',s)
open(txt,'w').write(t)
code=r.stdout.split()[0] if r.stdout else '?'
with open(os.path.join(O,'_log.tsv'),'a') as f:
    f.write('\t'.join([name,str(size),url,datetime.date.today().isoformat(),desc,code])+'\n')
print(name,size,'bytes; txt',len(t),'chars; http',code)
