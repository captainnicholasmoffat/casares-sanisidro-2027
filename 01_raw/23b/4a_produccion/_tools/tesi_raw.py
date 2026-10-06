import requests, re, html, json, sys
q=sys.argv[1]; out=sys.argv[2]
s=requests.Session(); s.verify="/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/c23b_raw/z4a_produccion/_tools/ca_si.pem"
r=s.get("https://tesi.sanisidro.gob.ar/boletin",timeout=60)
t=r.text
m=re.search(r'wire:snapshot="([^"]+)"',t); snap=html.unescape(m.group(1))
tok=re.search(r'data-csrf="([^"]+)"',t) or re.search(r'name="csrf-token" content="([^"]+)"',t)
tok=tok.group(1)
body={"_token":tok,"components":[{"snapshot":snap,"updates":{"buscar":q},"calls":[]}]}
rr=s.post("https://tesi.sanisidro.gob.ar/livewire/update",json=body,headers={"X-Livewire":"true","Content-Type":"application/json"},timeout=60)
open(out,'w').write(rr.json()["components"][0]["effects"].get("html",""))
