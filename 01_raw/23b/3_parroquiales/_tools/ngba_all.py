import sys,subprocess,re,html,urllib.parse,time,json
q=sys.argv[1]; maxp=int(sys.argv[2]) if len(sys.argv)>2 else 20
out=[]
for p in range(1,maxp+1):
    url="https://normas.gba.gob.ar/resultados?"+urllib.parse.urlencode({'page':p,'q[phrase]':q,'q[sort]':'by_publication_date_desc'})
    t=subprocess.run(["curl","-sS","-g","-m","60","-A","Mozilla/5.0",url],capture_output=True,text=True).stdout
    s=re.sub(r'(?is)<(script|style)[^>]*>.*?</\1>',' ',t)
    items=re.split(r'(?=<a href="/ar-b/)',s)[1:]
    if not items: break
    for it in items:
        m=re.match(r'<a href="(/ar-b/[^"]+)"',it)
        txt=re.sub(r'\s+',' ',html.unescape(re.sub('<[^>]+>',' ',it))).strip()
        k=txt.find('Última actualizacion'); txt=txt[:k] if k>0 else txt[:800]
        out.append((m.group(1),txt))
    time.sleep(0.5)
for u,t in out: print('https://normas.gba.gob.ar'+u,'|',t[:600])
