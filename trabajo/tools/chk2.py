import sys,re,collections
txt=open(sys.argv[1],encoding='utf-8').read(); norm=re.sub(r'\s+',' ',txt)
lines=[l.rstrip('\n') for l in open(sys.argv[2],encoding='utf-8') if l.strip()]
cnt=collections.Counter(); items=0
stop=set("el la los las de del a al y o en que con por para un una unos unas se su sus lo le les es no sí si ya más como sólo solo cada este esta ese esa eso hay va van ser son está están hoy también además cuando donde entre desde hasta sin sobre tiene puede qué cuál cómo".split())
ban=['mafia','plata','sobreprecio','en castellano','datos actualizados al','aplicación','plataforma','asistente']
for i,l in enumerate(lines,1):
    p=[x.strip() for x in l.split(' | ')]
    lab=p[0]
    if lab in('KEEP','VERIFY','NICK','DROP'):
        cnt[lab]+=1; items+=1
        if lab!='DROP':
            for s in [x.strip() for x in p[2].split(' / ')]:
                if s not in norm and not s.startswith('La primera ronda informa'): print(i,'ORIG NOT FOUND',s[:60])
            prop=p[3]
            for b in ban:
                if b in prop.lower(): print(i,'BANNED',b)
            for sent in re.split(r'(?<=[.:])\s+|\s/\s',prop):
                s2=re.sub(r'^\d+ · ','',sent.strip())
                if re.match(r'^(Y|Que|E)\b',s2): print(i,'STARTS',s2[:40])
                if '(en lista)' in sent: continue
                w=[x for x in re.findall(r'[a-záéíóúñü]+',sent.lower()) if x not in stop and len(x)>3]
                d=[k for k,v in collections.Counter(w).items() if v>1]
                if d: print(i,'REPEAT',d,'|',sent[:90])
        else:
            o=p[2]
            if not norm.startswith(o) and o not in norm and not o.startswith('La primera'): print(i,'DROP ORIG?',o)
print(items,dict(cnt))
