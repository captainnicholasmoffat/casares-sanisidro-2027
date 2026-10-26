import re,collections
base='/tmp/claude-0/-home-claude/ac2c9a6e-772e-5575-a5d3-16a61434e961/scratchpad/compr/'
out=[l for l in open(base+'filt_F.md',encoding='utf-8').read().split('\n') if l.strip()]
items=[l for l in out if l.split(' | ')[0] in ('KEEP','VERIFY','NICK')]
stop=set('desde entre sobre donde cuando porque también además sólo según hasta para como pero más menos todo toda todos todas este esta esto estos estas ese esa eso esos esas cada mismo misma'.split())
n=0
for l in out:
    p=l.split(' | ')
    if p[0] not in ('KEEP','VERIFY','NICK'): continue
    n+=1
    prop=p[3]
    for s in re.split(r'(?<=[.!?])\s+',prop):
        ws=[w.lower() for w in re.findall(r'[A-Za-zÁÉÍÓÚÑáéíóúñü]+',s) if len(w)>=4]
        cnt=collections.Counter(w for w in ws if w not in stop)
        reps=[w for w,k in cnt.items() if k>1]
        if reps: print(p[0],p[1],reps,'::',s[:110])
