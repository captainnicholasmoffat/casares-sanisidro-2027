import sys,re,html,urllib.parse,subprocess
B='/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/educ_raw/w2_competencia_datos/_busquedas/'
q=sys.argv[1]; out=sys.argv[2]; page=sys.argv[3] if len(sys.argv)>3 else '1'
city=sys.argv[4] if len(sys.argv)>4 else ''
url='https://sibom.slyt.gba.gob.ar/search?q%5Bsimple_query_string%5D='+urllib.parse.quote(q)+('&page='+page if page!='1' else '')+('&q%5Bterms%5D%5Bbulletin.city_id%5D='+city if city else '')
r=subprocess.run(['curl','-sS','-g','-L','--max-time','90','-o',B+out,'-w','%{http_code}',url],capture_output=True,text=True)
print('HTTP',r.stdout,r.stderr[:200],url)
t=open(B+out,encoding='utf-8',errors='ignore').read()
m=re.search(r'([\d\.]+)\s+resultados?',t)
print('total?',(m.group(0) if m else ''))
for blk in t.split('class="search-result"')[1:]:
    a=re.search(r'href="(/bulletins/\d+/contents/\d+)">(.*?)</a>',blk,re.S)
    d=re.search(r'text-muted">([^<]+)<',blk)
    snip=re.sub(r'\s+',' ',html.unescape(re.sub('<[^>]+>','',blk)))
    print('*',a.group(1) if a else '',re.sub(r'\s+',' ',a.group(2)) if a else '','|',d.group(1) if d else '','|',snip[:500])
