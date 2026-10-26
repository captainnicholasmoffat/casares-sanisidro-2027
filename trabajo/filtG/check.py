import re,sys
d='/tmp/claude-0/-home-claude/ac2c9a6e-772e-5575-a5d3-16a61434e961/scratchpad/compr/'
t=open(d+'G.txt',encoding='utf-8').read()
norm=re.sub(r'\s+',' ',t)
for i,l in enumerate(open(d+'out_G.md',encoding='utf-8'),1):
    l=l.rstrip('\n')
    if not l.strip(): continue
    parts=[p.strip() for p in l.split(' | ')]
    orig=parts[1]
    ok = orig in norm
    if not ok:
        print(i, 'NOT FOUND:', orig[:120])
