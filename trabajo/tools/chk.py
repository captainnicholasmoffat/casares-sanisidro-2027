import sys,re
txt=open(sys.argv[1],encoding='utf-8').read()
norm=re.sub(r'\s+',' ',txt)
for i,l in enumerate(open(sys.argv[2],encoding='utf-8'),1):
    parts=[p.strip() for p in l.split(' | ')]
    if len(parts)<3: continue
    orig=parts[1]
    segs=[s.strip() for s in orig.split(' / ')]
    bad=[s for s in segs if s not in norm]
    if bad: print(i,'NOT FOUND:',bad[:2])
