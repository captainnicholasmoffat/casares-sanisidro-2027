import re,sys
base='/tmp/claude-0/-home-claude/ac2c9a6e-772e-5575-a5d3-16a61434e961/scratchpad/compr/'
txt=open(base+'F.txt',encoding='utf-8').read()
norm=re.sub(r'\s+',' ',txt)
lines=[l for l in open(base+'out_F.md',encoding='utf-8').read().split('\n') if l.strip()]
for i,l in enumerate(lines,1):
    parts=[p.strip() for p in l.split(' | ')]
    orig=parts[1]
    ok = orig in norm
    if not ok:
        print(i,'NOTFOUND',repr(orig[:100]))
print(len(lines))
