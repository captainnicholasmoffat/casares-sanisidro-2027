import sys,subprocess,re,html,urllib.parse
q=sys.argv[1]; extra=sys.argv[2] if len(sys.argv)>2 else ''
url="https://normas.gba.gob.ar/resultados?"+urllib.parse.urlencode({'q[phrase]':q,'q[sort]':'by_publication_date_desc'})+extra
t=subprocess.run(["curl","-sS","-g","-m","60","-A","Mozilla/5.0",url],capture_output=True,text=True).stdout
m=re.search(r'Página \d+ de [\d]+ resultados',t); print(url); print(m.group(0) if m else 'no count')
for m in re.finditer(r'<a href="(/ar-b/[^"]+)">\s*(.*?)</a>(.*?)Fecha de publicación:\s*([\d/]+)',t,re.S):
    s=re.sub(r'\s+',' ',html.unescape(re.sub('<[^>]+>',' ',m.group(3)))).strip()
    print(m.group(4), m.group(1), re.sub(r'\s+',' ',m.group(2)).strip(),'|',s[:300])
