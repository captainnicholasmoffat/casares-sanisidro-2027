# uso: python3 -I sibom.py "consulta" [city_id] [desde dd/mm/aaaa] [hasta] [page] [tipo]
import sys,re,html,urllib.parse,subprocess,os
B='/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/c23c_raw/w3a_shows_calidad_alquiler/_tmp/sibom/'
os.makedirs(B,exist_ok=True)
a=sys.argv[1:]+['']*6
q,city,gte,lte,page,typ=a[0],a[1],a[2],a[3],a[4] or '1',a[5]
params=[('utf8','✓'),('q[simple_query_string]',q)]
if typ: params.append(('q[terms][type]',typ))
if city: params.append(('q[terms][bulletin.city_id]',city))
if gte: params.append(('q[date_ranges][bulletin.published_at][gte]',gte))
if lte: params.append(('q[date_ranges][bulletin.published_at][lte]',lte))
if page!='1': params.append(('page',page))
url='https://sibom.slyt.gba.gob.ar/'+('advanced_search' if (city or gte or typ) else 'search')+'?'+urllib.parse.urlencode(params)
out=B+re.sub(r'[^A-Za-z0-9]+','_',q+'_'+city+'_'+gte)[:80]+'_p'+page+'.html'
code=''
for attempt in range(4):
    r=subprocess.run(['curl','-sS','-g','-L','--max-time','90','-o',out,'-w','%{http_code}',url],capture_output=True,text=True)
    code=r.stdout
    if code=='200': break
print('HTTP',code,url)
t=open(out,encoding='utf-8',errors='ignore').read() if os.path.exists(out) else ''
m=re.search(r'([\d\.]+)\s+resultado',t)
print('total:',m.group(1) if m else '0')
for blk in t.split('class="search-result"')[1:]:
    a=re.search(r'href="(/bulletins/\d+/contents/\d+)"',blk)
    snip=re.sub(r'\s+',' ',html.unescape(re.sub('<[^>]+>',' ',blk)))
    print('*','https://sibom.slyt.gba.gob.ar'+a.group(1) if a else '','|',snip[:700])
