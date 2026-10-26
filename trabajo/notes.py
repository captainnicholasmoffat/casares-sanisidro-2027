import re
L=open('p5.txt').read().split('\n')
page=1;label=None;res=[];i=0
while i<len(L):
    l=L[i]
    m=re.search(r'Página (\d+) de 46',l)
    if m: page=int(m.group(1))+1
    m=re.match(r'^\s*(CUADRO|GRÁFICO|GR ÁFICO)\s+(\d+)\s*$',l)
    if m: label=f"{m.group(1).replace(' ','')[0]}{m.group(2)}"
    if re.match(r'^(Fuente|Nota)',l) and label:
        j=i;n=0;chars=0
        while j<len(L) and L[j].strip() and not re.search(r'Página \d+ de 46',L[j]):
            n+=1;chars+=len(L[j].strip());j+=1
        res.append((label,page,n,chars));label=None;i=j;continue
    i+=1
for r in res: print(*r)
