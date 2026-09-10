import pdfplumber, collections, statistics as st
REF="/root/.claude/uploads/e718506c-f800-59cb-a388-d13f7f594b6c/8e917875-Extra_Time___Investor_Report_Final_3.pdf"
pdf=pdfplumber.open(REF)
P=72/25.4
izq=[];der=[];arr=[];x0s=collections.Counter();x1s=collections.Counter()
for p in pdf.pages:
    cs=[c for c in p.chars]
    if not cs: continue
    izq.append(min(c["x0"] for c in cs)); der.append(p.width-max(c["x1"] for c in cs))
    arr.append(min(c["top"] for c in cs))
    for c in cs: x0s[round(c["x0"])]+=1; x1s[round(c["x1"])]+=1
print("margen izq min %.1fpt (%.1fmm)  moda %s"%(min(izq),min(izq)/P,sorted(x0s.items(),key=lambda t:-t[1])[:6]))
print("margen der min %.1fpt (%.1fmm)"%(min(der),min(der)/P))
print("margen sup min %.1fpt (%.1fmm)"%(min(arr),min(arr)/P))
# columnas: los x0 mas frecuentes
print("x0 frecuentes:",[k for k,v in sorted(x0s.items(),key=lambda t:-t[1])[:8]])
print("x1 frecuentes:",[k for k,v in sorted(x1s.items(),key=lambda t:-t[1])[:8]])
# interlineado del cuerpo 9.7
tops=collections.defaultdict(list)
for i,p in enumerate(pdf.pages):
    for c in p.chars:
        if abs(c["size"]-9.7)<0.15 and "Regular" in c["fontname"]:
            tops[i].append(round(c["top"],1))
saltos=collections.Counter()
for i,v in tops.items():
    u=sorted(set(v))
    for a,b in zip(u,u[1:]):
        d=round(b-a,1)
        if 5<d<40: saltos[d]+=1
print("interlineado cuerpo:",saltos.most_common(6))
# reglas: rects y lines finos
gr=collections.Counter(); anchos=collections.Counter()
for p in pdf.pages:
    for r in p.rects:
        h=r["y1"]-r["y0"]; w=r["x1"]-r["x0"]
        if h<3 and w>40: gr[round(h,2)]+=1
        if h>=3: anchos[round(h,1)]+=1
    for l in p.lines:
        gr[round(l.get("linewidth") or 0,2)]+=1
print("grosor de reglas:",gr.most_common(8))
print("alto de bandas (rects>=3pt):",anchos.most_common(10))
