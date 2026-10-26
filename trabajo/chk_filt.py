import re,sys,collections,glob
base=sys.argv[1]
txt=open(base+'/compr/C.txt',encoding='utf-8').read()
norm=lambda s: re.sub(r'\s+',' ',s).strip()
T=norm(txt)
src=''
for f in glob.glob(base+'/repo/doc/content_*.py'):
    src+=open(f,encoding='utf-8').read()
S=norm(re.sub(r'<[^>]+>','',src))
lines=[l for l in open(base+'/compr/filt_C.md',encoding='utf-8').read().splitlines() if l.strip()]
c=collections.Counter()
for i,l in enumerate(lines,1):
    p=[x.strip() for x in l.split(' | ')]
    tag=p[0]; c[tag]+=1
    if tag in('KEEP','VERIFY','NICK'):
        o=p[2]; prop=p[3]
        inT=o in T; inS=o in S
        if not(inT and inS): print(i,tag,'C.txt' if inT else 'NO-C', 'src' if inS else 'NO-SRC', o[:70])
        for s in re.split(r'(?<=[.:!?])\s+',prop):
            if re.match(r'^(Y|Que|E)\b',s): print(i,'STARTS',s[:40])
        for w in ['plata','mafia','sobreprecio','en castellano','actualizados al']:
            if w in prop.lower(): print(i,'FORBIDDEN',w)
    if tag=='DROP':
        o=p[2]
        if o not in T and o not in S: print(i,'DROP-orig not found',o)
print(c, len(lines))
