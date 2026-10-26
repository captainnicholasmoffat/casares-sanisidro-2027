import re, subprocess, sys
from collections import defaultdict
def col(x):
    if x<=445: return 'est'
    if x<=505: return 'mod'
    if x<=565: return 'vig'
    if x<=615: return 'dev'
    if x<=675: return 'dvd'
    if x<=725: return 'perc'
    if x<=785: return 'ddp'
    return 'dvp'
pdf=sys.argv[1]
out=subprocess.run(['pdftotext','-bbox',pdf,'-'],capture_output=True,text=True).stdout
pages=out.split('<page ')[1:]
agg=defaultdict(lambda: defaultdict(float)); unknown=[]
rowsout=[]
for pi,pg in enumerate(pages,1):
    ws=re.findall(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">([^<]*)</word>',pg)
    rows={}
    for x0,y0,x1,y1,w in ws:
        k=None
        for yy in rows:
            if abs(yy-float(y0))<=2: k=yy;break
        if k is None: k=float(y0); rows[k]=[]
        rows[k].append((float(x0),float(x1),w))
    ys=sorted(rows)
    for i,y in enumerate(ys):
        r=sorted(rows[y]); 
        label=' '.join(w for a,b,w in r if not re.match(r'^-?[\d,]+\.\d\d$',w))
        if not re.match(r'^\d+\.\d+\.\d+\.\d+',label): continue
        nums={col(b):float(w.replace(',','')) for a,b,w in r if re.match(r'^-?[\d,]+\.\d\d$',w)}
        if not nums: continue
        # if dev present but perc missing and dvd present, keep as is
        proc=None
        for p in ['ORIGEN MUNICIPAL','ORIGEN PROVINCIAL','ORIGEN NACIONAL','OTROS ORIGENES']:
            if p in label: proc=p
        if proc is None:
            # look at next/prev line
            for j in (i-1,i+1):
                if 0<=j<len(ys):
                    l2=' '.join(w for a,b,w in rows[ys[j]])
                    for p in ['ORIGEN MUNICIPAL','ORIGEN PROVINCIAL','ORIGEN NACIONAL','OTROS ORIGENES']:
                        if p in l2 and not re.match(r'^\d+\.\d+',l2): proc=p
        if proc is None: proc='?'; unknown.append(label[:60])
        code=label.split()[0]
        for k in ('dev','perc'): agg[proc][k]+=nums.get(k,0.0)
        agg[proc]['n']+=1
        rowsout.append((code,proc,nums.get('dev'),nums.get('perc')))
for p,v in agg.items(): print(f"{p:20s} n={int(v['n']):3d} dev={v['dev']:,.2f} perc={v['perc']:,.2f}")
tot_dev=sum(v['dev'] for v in agg.values()); tot_perc=sum(v['perc'] for v in agg.values())
print(f"SUM rows dev={tot_dev:,.2f} perc={tot_perc:,.2f}")
print('unknown:',unknown)
if len(sys.argv)>2:
    for r in rowsout: print(r)
