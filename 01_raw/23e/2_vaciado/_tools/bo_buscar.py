# Busca en el Boletín Oficial de San Isidro (tesi.sanisidro.gob.ar/boletin) vía Livewire (copia adaptada del script de c23_raw/y4)
import sys; sys.path.append("/root/.local/lib/python3.11/site-packages")
import requests, re, html, sys, os
CA=os.path.join(os.path.dirname(os.path.abspath(__file__)),'ca_all.pem')
q=sys.argv[1]; pages=int(sys.argv[2]) if len(sys.argv)>2 else 1
s=requests.Session(); s.verify=CA
r=s.get("https://tesi.sanisidro.gob.ar/boletin",timeout=60)
t=r.text
m=re.search(r'wire:snapshot="([^"]+)"',t); snap=html.unescape(m.group(1))
tok=re.search(r'data-csrf="([^"]+)"',t) or re.search(r'name="csrf-token" content="([^"]+)"',t)
tok=tok.group(1)
def parse(h):
    out=[]
    for row in re.split(r'<tr class="hover',h)[1:]:
        pdf=re.findall(r'href="(https://tesi.sanisidro.gob.ar/(?:boletin/pdf|nfs-storage)/[^"]+)"',row)
        x=re.sub(r'<!--.*?-->','',row,flags=re.S); x=re.sub(r'<[^>]+>','|',x); x=html.unescape(x)
        x=re.sub(r'\s*\|[\s|]*',' | ',x).strip(' |'); x=x.split('>',1)[-1].strip(' |')
        out.append(x.replace("| Ver","").strip()+" || "+" ".join(pdf))
    return out
upd={"buscar":q}
for p in range(pages):
    body={"_token":tok,"components":[{"snapshot":snap,"updates":upd,"calls":[] if p==0 else [{"path":"","method":"nextPage","params":["page"]}]}]}
    rr=s.post("https://tesi.sanisidro.gob.ar/livewire/update",json=body,headers={"X-Livewire":"true","Content-Type":"application/json"},timeout=60)
    j=rr.json(); c=j["components"][0]; snap=c["snapshot"]; h=c["effects"].get("html","")
    res=parse(h)
    for line in res: print(line)
    if not res: break
    upd={}
