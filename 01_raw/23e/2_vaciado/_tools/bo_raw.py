import sys; sys.path.append("/root/.local/lib/python3.11/site-packages")
import requests, re, html, os
CA=os.path.join(os.path.dirname(os.path.abspath(__file__)),'ca_all.pem')
q=sys.argv[1]
s=requests.Session(); s.verify=CA
r=s.get("https://tesi.sanisidro.gob.ar/boletin",timeout=60); t=r.text
snap=html.unescape(re.search(r'wire:snapshot="([^"]+)"',t).group(1))
tok=(re.search(r'data-csrf="([^"]+)"',t) or re.search(r'name="csrf-token" content="([^"]+)"',t)).group(1)
body={"_token":tok,"components":[{"snapshot":snap,"updates":{"buscar":q},"calls":[]}]}
rr=s.post("https://tesi.sanisidro.gob.ar/livewire/update",json=body,headers={"X-Livewire":"true","Content-Type":"application/json"},timeout=60)
print(rr.json()["components"][0]["effects"].get("html",""))
