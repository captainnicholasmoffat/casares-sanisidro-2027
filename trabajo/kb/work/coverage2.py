import json,re,unicodedata,sys
S='/tmp/claude-0/-home-claude/ac2c9a6e-772e-5575-a5d3-16a61434e961/scratchpad'
P=json.load(open(sys.argv[1]))
def words(s):
    s=unicodedata.normalize('NFKD',s.lower()); s=''.join(c for c in s if not unicodedata.combining(c))
    return re.findall(r'[a-z0-9]+',s)
HEAD=re.compile(r"^P R O G R A M A D E G O B I E R N O · PA R T I D O D E S A N I S I D R O\s*$",re.M)
FOOT=re.compile(r"^(Programa de gobierno · San Isidro 2027|Página \d+ de \d+)\s*$",re.M)
K=5
JS=set()
for e in P:
    w=words(e['titulo']+' '+e['texto']+' '+' '.join(c['titulo']+' '+c['texto'] for c in e['cuadros'])+' '+e['fuentes'])
    for i in range(len(w)-K+1): JS.add(tuple(w[i:i+K]))
total=0;unc=0
for i in range(5,141):
    t=open(f'{S}/v21/t/{i}.txt').read(); t=HEAD.sub('',t); t=FOOT.sub('',t)
    w=words(t); cov=[False]*len(w)
    for j in range(len(w)-K+1):
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
        if len(alpha)>=3: print(f'p{i}: {" ".join(run)[:200]}')
        j=k
print('palabras A4:',total,'sin cubrir:',unc)
