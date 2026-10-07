# Busca en el Boletín Oficial de San Isidro (tesi.sanisidro.gob.ar/boletin) vía Livewire (stdlib)
import urllib.request, ssl, re, html, json, sys, http.cookiejar
q=sys.argv[1]; pages=int(sys.argv[2]) if len(sys.argv)>2 else 1
ctx=ssl.create_default_context(cafile="/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/c23c_raw/w3b_robos_spotify/_tools/ca_si.pem")
cj=http.cookiejar.CookieJar()
op=urllib.request.build_opener(urllib.request.HTTPSHandler(context=ctx),urllib.request.HTTPCookieProcessor(cj),urllib.request.ProxyHandler())
op.addheaders=[('User-Agent','Mozilla/5.0')]
t=op.open("https://tesi.sanisidro.gob.ar/boletin",timeout=60).read().decode('utf-8','replace')
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
    req=urllib.request.Request("https://tesi.sanisidro.gob.ar/livewire/update",data=json.dumps(body).encode(),headers={"X-Livewire":"true","Content-Type":"application/json"})
    j=json.loads(op.open(req,timeout=60).read())
    c=j["components"][0]; snap=c["snapshot"]; h=c["effects"].get("html","")
    if len(sys.argv)>3: open(sys.argv[3]+f'_p{p+1}.html','w').write(h)
    for line in parse(h): print(line)
    upd={}
