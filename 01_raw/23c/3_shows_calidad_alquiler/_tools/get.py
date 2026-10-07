#!/usr/bin/env python3
# uso: python3 -I get.py URL subcarpeta/nombre "qué es" [args extra de curl]
import sys, subprocess, os, datetime, re, html
D='/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/c23c_raw/w3a_shows_calidad_alquiler'
url, name, what = sys.argv[1], sys.argv[2], sys.argv[3]
out=os.path.join(D,name)
os.makedirs(os.path.dirname(out),exist_ok=True)
extra=sys.argv[4:]
cmd=['curl','-sSL','--max-time','120','--retry','3','--retry-all-errors','-A','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36','-o',out,'-w','%{http_code}']+extra+[url]
r=subprocess.run(cmd,capture_output=True,text=True)
if r.returncode!=0 or not os.path.exists(out) or not r.stdout.startswith('2'):
    print('ERROR',r.returncode,r.stdout,r.stderr[:300])
    with open(os.path.join(D,'_tmp','errores.txt'),'a') as f: f.write(f'{datetime.date.today()} | {url} | {r.returncode} {r.stdout} {r.stderr[:200].strip()}\n')
    if os.path.exists(out): os.remove(out)
    sys.exit(1)
b=os.path.getsize(out)
txt=out+'.txt'
data=open(out,'rb').read()
if data[:4]==b'%PDF':
    import pymupdf
    d=pymupdf.open(out)
    t='\n'.join(f'=== página {i+1} ===\n'+p.get_text() for i,p in enumerate(d))
else:
    s=data.decode('utf-8','replace')
    s=re.sub(r'(?is)<(script|style|noscript)[^>]*>.*?</\1>',' ',s)
    s=re.sub(r'(?i)<br\s*/?>|</p>|</div>|</li>|</tr>|</h\d>','\n',s)
    s=re.sub(r'<[^>]+>',' ',s)
    s=html.unescape(s)
    s=re.sub(r'[ \t\r\f\v]+',' ',s)
    s=re.sub(r'\n\s*\n+','\n',s)
    t=s
open(txt,'w').write(t)
with open(os.path.join(D,'FUENTES.txt'),'a') as f:
    f.write(f'{name} | {b} | {url} | {datetime.date.today().isoformat()} | {what}\n')
print(name,b,len(t))
