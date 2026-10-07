#!/usr/bin/env python3
# uso: python3 -I get.py URL ruta_relativa_en_u2 "qué es" [--sanisidro]
import sys, subprocess, os, datetime, re, html
T=os.path.dirname(os.path.abspath(__file__)); D=os.path.dirname(T)
url, name, what = sys.argv[1], sys.argv[2], sys.argv[3]
out=os.path.join(D,name); os.makedirs(os.path.dirname(out),exist_ok=True)
cmd=['curl','-sSL','--max-time','120','-A','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36','--cacert',os.path.join(T,'ca_all.pem'),'-o',out,url]
r=subprocess.run(cmd,capture_output=True,text=True)
if r.returncode!=0 or not os.path.exists(out):
    print('ERROR',r.stderr)
    with open(os.path.join(D,'_errores.txt'),'a') as f: f.write(f'{url} | {datetime.date.today()} | {r.stderr.strip()} | {what}\n')
    sys.exit(1)
b=os.path.getsize(out); data=open(out,'rb').read()
if data[:4]==b'%PDF':
    import pymupdf
    d=pymupdf.open(out); t='\n'.join(f'=== página {i+1} ===\n'+p.get_text() for i,p in enumerate(d))
else:
    s=data.decode('utf-8','replace')
    s=re.sub(r'(?is)<(script|style|noscript)[^>]*>.*?</\1>',' ',s)
    s=re.sub(r'(?i)<br\s*/?>|</p>|</div>|</li>|</tr>|</h\d>','\n',s)
    s=re.sub(r'<[^>]+>',' ',s); s=html.unescape(s)
    s=re.sub(r'[ \t\r\f\v]+',' ',s); s=re.sub(r'\n\s*\n+','\n',s); t=s
open(out+'.txt','w').write(t)
with open(os.path.join(D,'FUENTES.txt'),'a') as f:
    f.write(f'{name} (+ .txt) | {b} | {url} | {datetime.date.today().isoformat()} | {what}\n')
print(name,b,len(t))
