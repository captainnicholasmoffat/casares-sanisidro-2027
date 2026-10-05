#!/usr/bin/env python3
# uso: get.py URL nombre "descripcion" [--noappend] [--post DATA]
import sys, subprocess, os, datetime, re, html
D="/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/c23_raw/y2_canon_privados/"
url, name, desc = sys.argv[1], sys.argv[2], sys.argv[3]
path=os.path.join(D,name)
ua="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
extra=[]
if "--post" in sys.argv:
    extra=["--data",sys.argv[sys.argv.index("--post")+1]]
base=["curl","-sSL","-g","-m","180","-A",ua]+extra
if "sanisidro.gob.ar" in url:
    base+=["--cacert",D+"_tools/ca_plus_ov_dv.pem"]
if "abc.gob.ar" in url:
    base+=["--ciphers","DEFAULT@SECLEVEL=1"]
r=subprocess.run(base+["-o",path,"-w","%{http_code} %{content_type}",url],capture_output=True,text=True)
print("curl:",r.stdout,r.stderr[:300])
code=(r.stdout.split() or ['000'])[0]
if code.startswith(('4','5','0')) :
    print("FALLO http",code)
    if os.path.exists(path): os.remove(path)
    sys.exit(1)
if not os.path.exists(path) or os.path.getsize(path)==0:
    print("FALLO"); sys.exit(1)
b=open(path,'rb').read()
txt=None
if b[:4]==b'%PDF':
    import pymupdf
    doc=pymupdf.open(path)
    txt="\n".join(f"=== p{i+1} ===\n"+p.get_text() for i,p in enumerate(doc))
elif name.endswith(('.html','.htm')) or b'<html' in b[:3000].lower() or b'<!doctype' in b[:300].lower():
    s=b.decode('utf-8','replace')
    s=re.sub(r'(?is)<(script|style|noscript)[^>]*>.*?</\1>',' ',s)
    s=re.sub(r'(?i)<a [^>]*href="([^"]+)"[^>]*>',r' [\1] ',s)
    s=re.sub(r'(?i)<br\s*/?>|</p>|</div>|</tr>|</h\d>|</li>','\n',s)
    s=re.sub(r'(?i)</td>|</th>',' | ',s)
    s=re.sub(r'<[^>]+>',' ',s)
    s=html.unescape(s)
    s=re.sub(r'[ \t\r\f\v]+',' ',s)
    s=re.sub(r'\n\s*\n+','\n',s)
    txt=s
if txt is not None:
    tp=re.sub(r'\.(pdf|html?|PDF)$','',path)+".txt"
    open(tp,"w").write(txt)
    print("txt chars",len(txt), tp)
if "--noappend" not in sys.argv:
    with open(os.path.join(D,"FUENTES.txt"),"a") as f:
        f.write(f"{name} | {os.path.getsize(path)} | {url} | {datetime.date.today().isoformat()} | {desc}\n")
print("bytes",os.path.getsize(path))
