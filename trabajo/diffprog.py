import json,sys
def load(p):
    d=json.load(open(p))
    return d if isinstance(d,list) else d.get('entradas') or d.get('items') or d
a=load(sys.argv[1]); b=load(sys.argv[2])
print(type(a), len(a))
def idx(x):
    if isinstance(x,dict): return x
    return {e['id']:e for e in x}
A=idx(a);B=idx(b)
SKIP={'hoja_a4','hoja_a4_fin','fuentes_hojas_a4','hoja','hojas'}
def strip(v):
    if isinstance(v,dict): return {k:strip(w) for k,w in v.items() if k not in SKIP}
    if isinstance(v,list): return [strip(w) for w in v]
    return v
for k in sorted(set(A)|set(B)):
    if k not in A: print('NEW',k); continue
    if k not in B: print('GONE',k); continue
    ea,eb=strip(A[k]),strip(B[k])
    if ea!=eb:
        for f in sorted(set(ea)|set(eb)):
            if ea.get(f)!=eb.get(f): print('CHANGED',k,f)
