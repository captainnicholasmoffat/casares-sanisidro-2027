#!/usr/bin/env python3
# uso: get.py <archivo> <url> <descripcion> [--ca extra.pem]
import sys, subprocess, os, datetime, re
D='/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/c23_raw/y5_plataforma_personas'
name,url,desc=sys.argv[1],sys.argv[2],sys.argv[3]
extra=sys.argv[4] if len(sys.argv)>4 else None
out=os.path.join(D,name)
cmd=['curl','-sSL','--max-time','90','-A','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36','-H','Accept-Language: es-AR,es;q=0.9,en;q=0.8','-o',out,'-w','%{http_code}',url]
if extra: cmd[1:1]=['--cacert',extra]
r=subprocess.run(cmd,capture_output=True,text=True)
code=r.stdout.strip()
if r.returncode!=0 or not os.path.exists(out):
    print('FALLO',r.returncode,code,r.stderr[:300]); sys.exit(1)
size=os.path.getsize(out)
txt=out+'.txt' if not out.endswith('.txt') else out+'.plain.txt'
with open(out,'rb') as f: head=f.read(5)
if head.startswith(b'%PDF'):
    import pymupdf
    doc=pymupdf.open(out)
    open(txt,'w').write('\n'.join(f'--- página {i+1} ---\n'+pg.get_text() for i,pg in enumerate(doc)))
else:
    try:
        from bs4 import BeautifulSoup
        raw=open(out,'rb').read()
        if head[:1] in (b'{',b'['):
            open(txt,'wb').write(raw)
        else:
            s=BeautifulSoup(raw,'html.parser')
            for t in s(['script','style','noscript','svg']): t.decompose()
            t=s.get_text('\n')
            t=re.sub(r'\n\s*\n+','\n\n',t)
            open(txt,'w').write(t)
    except Exception as e:
        print('txt error',e)
tsize=os.path.getsize(txt) if os.path.exists(txt) else 0
fecha=datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
with open(os.path.join(D,'FUENTES.txt'),'a') as f:
    f.write(f'{name} | {size} | {url} | {fecha} | {desc} (HTTP {code})\n')
print(code,size,tsize,txt)
