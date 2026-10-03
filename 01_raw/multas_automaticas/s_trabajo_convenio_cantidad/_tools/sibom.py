import sys,re,html,urllib.parse,subprocess,os
B='/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/multas_raw/s_trabajo_convenio_cantidad/_tmp/sibom/'
q=sys.argv[1]; page=sys.argv[2] if len(sys.argv)>2 else '1'
out=re.sub(r'[^A-Za-z0-9]+','_',q)[:60]+'_p'+page+'.html'
url='https://sibom.slyt.gba.gob.ar/search?q%5Bsimple_query_string%5D='+urllib.parse.quote(q)+('&page='+page if page!='1' else '')
for attempt in range(3):
    r=subprocess.run(['curl','-sS','-g','-L','--max-time','90','-o',B+out,'-w','%{http_code}',url],capture_output=True,text=True)
    if r.stdout=='200': break
print('HTTP',r.stdout,r.stderr[:200],url)
t=open(B+out,encoding='utf-8',errors='ignore').read() if os.path.exists(B+out) else ''
m=re.search(r'([\d\.]+)\s+resultado',t)
print('total?',m.group(1) if m else '')
for blk in t.split('class="search-result"')[1:]:
    a=re.search(r'href="(/bulletins/\d+/contents/\d+)">(.*?)</a>',blk,re.S)
    snip=re.sub(r'\s+',' ',html.unescape(re.sub('<[^>]+>',' ',blk)))
    print('*',a.group(1) if a else '','|',snip[:500])
