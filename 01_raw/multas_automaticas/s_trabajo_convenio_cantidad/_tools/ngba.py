import sys,re,html,urllib.parse,subprocess
W='/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/multas_raw/s_trabajo_convenio_cantidad/busquedas/'
params=sys.argv[1]; out=sys.argv[2]
url='https://normas.gba.gob.ar/resultados?'+'&'.join(k+'='+urllib.parse.quote(v) for k,v in [p.split('=',1) for p in params.split('&')])
r=subprocess.run(['curl','-sS','-g','-L','--max-time','90','-o',W+out,'-w','%{http_code}',url],capture_output=True,text=True)
print('HTTP',r.stdout,r.stderr[:200],url)
t=open(W+out,encoding='utf-8',errors='ignore').read()
m=re.search(r'([\d\.]+)\s+resultados',t); print('total:',m.group(1) if m else '?')
t2=re.sub(r'(?is)<script.*?</script>|<style.*?</style>','',t)
for blk in t2.split('rule-card')[1:]:
    a=re.search(r'href="(/ar-b/[^"]+)"',blk)
    s=re.sub(r'\s+',' ',html.unescape(re.sub('<[^>]+>',' ',blk))).strip()
    print('*',a.group(1) if a else '','|',s[:330])
