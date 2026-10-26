import json,re,unicodedata,sys
S=sys.argv[2]
P=json.load(open(sys.argv[1],encoding="utf-8"))
def words(s):
    s=unicodedata.normalize('NFKD',s.lower()); s=''.join(c for c in s if not unicodedata.combining(c))
    return re.findall(r'[a-z0-9]+',s)
HEAD=re.compile(r"^P R O G R A M A D E G O B I E R N O · PA R T I D O D E S A N I S I D R O\s*$",re.M)
FOOT=re.compile(r"^(Programa de gobierno · San Isidro 2027|Página \d+ de \d+)\s*$",re.M)
K=5
def alltext(e):
    parts=[e['id'] if re.match(r'^\d',e['id']) else '', e['titulo'], e['texto'], e['fuentes'], ' '.join(e.get('etiquetas',[])), ' '.join(e.get('pies_de_foto',[]))]
    for c in e['cuadros']: parts += [c['titulo'], c['texto'], c.get('texto_del_grafico','')]
    return ' '.join(parts)
JS=set()
for e in P:
    w=words(alltext(e))
    for i in range(len(w)-K+1): JS.add(tuple(w[i:i+K]))
total=0;unc=0; A4=set()
for i in range(5,141):
    t=open(f'{S}/v21/t/{i}.txt',encoding='utf-8').read(); t=HEAD.sub('',t); t=FOOT.sub('',t)
    w=words(t); cov=[False]*len(w)
    for j in range(len(w)-K+1):
        A4.add(tuple(w[j:j+K]))
        if tuple(w[j:j+K]) in JS:
            for k in range(j,j+K): cov[k]=True
    total+=len(w)
    j=0
    while j<len(w):
        if cov[j]: j+=1; continue
        k=j
        while k<len(w) and not cov[k]: k+=1
        run=w[j:k]; unc+=len(run)
        alpha=[x for x in run if len(x)>2 and not x.isdigit()]
        if len(alpha)>=3: print(f'A4 p{i}: {" ".join(run)[:220]}')
        j=k
print('palabras A4 (hojas 5-140):',total,'sin cubrir:',unc)
bad=0
for e in P:
    blocks=[e['titulo']]+e['texto'].split('\n\n')+[c['titulo'] for c in e['cuadros']]+[x for c in e['cuadros'] for x in c['texto'].split('\n')]+e['fuentes'].split('\n\n')
    for b in blocks:
        w=words(b); s=[tuple(w[i:i+K]) for i in range(len(w)-K+1)]
        m=[x for x in s if x not in A4]
        if s and len(m)/len(s)>0.2:
            bad+=1; print(f'JSON {e["id"]}: {len(m)}/{len(s)} :: {b[:140]!r}')
print('bloques JSON con >20% no hallado en A4:',bad)
