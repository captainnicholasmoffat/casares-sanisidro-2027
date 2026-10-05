import sys,re,html,urllib.parse,subprocess
q=sys.argv[1]; out=sys.argv[2]
url='https://sibom.slyt.gba.gob.ar/search?q[simple_query_string]='+urllib.parse.quote(q)
if len(sys.argv)>3: url+='&page='+sys.argv[3]
subprocess.run(['curl','-g','-sS','-L','-m','90','-A','Mozilla/5.0','-o',out,url])
s=open(out,'rb').read().decode('utf-8','ignore')
print('URL',url)
links=re.findall(r'href="(/bulletins/\d+/contents/\d+)"[^>]*>\s*(.*?)\s*</a>',s,flags=re.S)
i=s.find('Búsqueda Avanzada'); body=s[i:]
t=html.unescape(re.sub(r'<[^>]+>',' ',body)); t=re.sub(r'\s+',' ',t)
parts=re.split(r'(?=(?:Ordenanza|Decreto|Resoluci[oó]n|Disposici[oó]n|Comunicaci[oó]n|Minuta|Edicto|Licitaci[oó]n|Convenio|Declaraci[oó]n|Aviso|Otro|Promulgaci[oó]n)[^ ]* N?º?\s*\S* en el bolet[ií]n)',t)
m=dict((re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>','',b))).strip(),a) for a,b in links)
for p in parts[1:]:
    title=p.split(' en el bol')[0]
    key=[k for k in m if p.startswith(k)]
    print('-',(m[key[0]] if key else ''),p[:330])
