import json,re,unicodedata,sys
S='/tmp/claude-0/-home-claude/ac2c9a6e-772e-5575-a5d3-16a61434e961/scratchpad'
P=json.load(open(sys.argv[1]))
def words(s):
    s=unicodedata.normalize('NFKD',s.lower()); s=''.join(c for c in s if not unicodedata.combining(c))
    return re.findall(r'[a-z0-9]+',s)
HEAD=re.compile(r"^P R O G R A M A D E G O B I E R N O · PA R T I D O D E S A N I S I D R O\s*$",re.M)
FOOT=re.compile(r"^(Programa de gobierno · San Isidro 2027|Página \d+ de \d+)\s*$",re.M)
pages={}
for i in range(1,141):
    t=open(f'{S}/v21/t/{i}.txt').read(); t=HEAD.sub('',t); t=FOOT.sub('',t); pages[i]=words(t)
K=6
def sh(w): return {' '.join(w[i:i+K]) for i in range(len(w)-K+1)}
# json stream
js=[]
for e in P:
    js.append(words(e['titulo'])); 
    for p in e['texto'].split('\n\n'): js.append(words(p))
    for c in e['cuadros']:
        js.append(words(c['titulo']))
        for p in re.split(r'\n\n|\n| \| ',c['texto']): js.append(words(p))
    for p in e['fuentes'].split('\n\n'): js.append(words(p))
JS=set()
for w in js: JS|=sh(w)
A4=set()
for i in range(5,141): A4|=sh(pages[i])
# direction A4 -> json: uncovered runs per page
tot=0
for i in range(5,141):
    w=pages[i]; miss=[j for j in range(len(w)-K+1) if ' '.join(w[j:j+K]) not in JS]
    # group into runs
    runs=[];
    for j in miss:
        if runs and j<=runs[-1][1]+1: runs[-1][1]=j
        else: runs.append([j,j])
    for a,b in runs:
        frag=' '.join(w[a:b+K])
        if sum(len(x)>1 for x in w[a:b+K])<4: continue
        tot+=1
        print(f'A4 p{i}: {frag[:160]}')
print('runs A4 no cubiertos:',tot)
# direction json -> A4
bad=0
for e in P:
    blocks=[e['titulo']]+e['texto'].split('\n\n')+[c['texto'] for c in e['cuadros']]+[e['fuentes']]
    for b in blocks:
        w=words(b); s=[' '.join(w[i:i+K]) for i in range(len(w)-K+1)]
        m=[x for x in s if x not in A4]
        if s and len(m)/len(s)>0.15:
            bad+=1; print(f'JSON {e["id"]}: {len(m)}/{len(s)} :: {b[:120]!r}')
print('bloques JSON con >15% no hallado en A4:',bad)
