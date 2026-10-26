import re,collections
base='/tmp/claude-0/-home-claude/ac2c9a6e-772e-5575-a5d3-16a61434e961/scratchpad/compr/'
norm=re.sub(r'\s+',' ',open(base+'F.txt',encoding='utf-8').read())
inp=[l for l in open(base+'out_F.md',encoding='utf-8').read().split('\n') if l.strip()]
out=[l for l in open(base+'filt_F.md',encoding='utf-8').read().split('\n') if l.strip()]
items=[l for l in out if l.split(' | ')[0] in ('KEEP','VERIFY','NICK','DROP')]
print('items',len(items),'input',len(inp))
c=collections.Counter(l.split(' | ')[0] for l in items); print(c)
nf={'KEEP':4,'VERIFY':5,'NICK':5,'DROP':4}
for i,(a,b) in enumerate(zip(inp,items),1):
    p=b.split(' | ')
    if len(p)!=nf[p[0]]: print(i,'FIELDS',len(p))
    pin=a.split(' | ')[0].strip()
    if p[1]!=pin: print(i,'PAGE',p[1],pin)
    orig=p[2]
    if p[0]=='DROP':
        if not (orig in norm): print(i,'DROP prefix not found',orig)
        # check prefix of reader original
        ro=a.split(' | ')[1].strip()
        if not ro.startswith(orig): print(i,'DROP not prefix of reader orig',orig,'|',ro[:60])
    else:
        if orig not in norm: print(i,'ORIG NOT FOUND',orig[:80])
        prop=p[3]
        for s in re.split(r'(?<=[.!?»])\s+',prop):
            w=s.strip().split(' ')[0] if s.strip() else ''
            if w in ('Y','Que','E') or w.startswith('Y,'): print(i,'STARTS',s[:50])
        for bad in ['plata','mafia','sobreprecio','en castellano','actualizados al','dudoso','(?)']:
            if bad in prop.lower(): print(i,'BAD',bad)
        if re.search(r'inteligencia artificial(?! del Municipio)',prop): print(i,'IA sin del Municipio')
print('TOTAL line:',out[-1])
