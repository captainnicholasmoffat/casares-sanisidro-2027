#!/usr/bin/env python3
# uso: get.py URL nombre "descripcion" [--noappend] [--es]
import sys, subprocess, os, datetime, re, html
D="/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/c23d_raw/v1_inspectores_banco/"
url, name, desc = sys.argv[1], sys.argv[2], sys.argv[3]
path=os.path.join(D,name)
ua="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
extra=[]
if "sanisidro.gob.ar" in url: extra=["--cacert",D+"_tools/ca_msi.pem"]
r=subprocess.run(["curl","-sSL","-m","120"]+extra+["-A",ua,"-H","Accept-Language: es-AR,es;q=0.9,en;q=0.8","-c","/dev/null","-o",path,"-w","%{http_code} %{content_type}",url],capture_output=True,text=True)
print("curl:",r.stdout,r.stderr[:300])
code=(r.stdout.split() or ['000'])[0]
if code.startswith(('4','5','0')):
    print("FALLO http",code)
    with open(D+"_tools/errores.log","a") as f: f.write(f"{datetime.date.today()} | {url} | http {code} | {r.stderr[:200].strip()}\n")
    if os.path.exists(path): os.remove(path)
    sys.exit(1)
b=open(path,'rb').read()
txt=None
if b[:4]==b'%PDF':
    import pymupdf
    doc=pymupdf.open(path)
    txt="\n".join(f"=== p{i+1} ===\n"+p.get_text() for i,p in enumerate(doc))
elif b'<html' in b[:5000].lower() or b'<!doctype' in b[:500].lower() or name.endswith(('.html','.htm')):
    s=b.decode('utf-8','replace')
    if 'charset=iso-8859-1' in s[:3000].lower() or 'charset=windows-1252' in s[:3000].lower():
        s=b.decode('latin-1')
    s=re.sub(r'(?is)<(script|style|noscript)[^>]*>.*?</\1>',' ',s)
    s=re.sub(r'(?i)<br\s*/?>|</p>|</div>|</tr>|</h\d>|</li>','\n',s)
    s=re.sub(r'(?i)</td>|</th>',' | ',s)
    s=re.sub(r'<[^>]+>',' ',s)
    s=html.unescape(s)
    s=re.sub(r'[ \t\r\f\v]+',' ',s)
    s=re.sub(r'\n\s*\n+','\n',s)
    txt=s
else:
    txt=b.decode('utf-8','replace')
open(path+".txt","w").write(txt)
print("txt chars",len(txt))
if "--noappend" not in sys.argv:
    with open(os.path.join(D,"FUENTES.txt"),"a") as f:
        f.write(f"{name} | {os.path.getsize(path)} | {url} | {datetime.date.today().isoformat()} | {desc}\n")
print("bytes",os.path.getsize(path))
