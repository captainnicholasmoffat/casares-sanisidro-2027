import pdfplumber, collections
REF="/root/.claude/uploads/e718506c-f800-59cb-a388-d13f7f594b6c/8e917875-Extra_Time___Investor_Report_Final_3.pdf"
pdf=pdfplumber.open(REF)
fin=collections.Counter()
for p in pdf.pages:
    lin=collections.defaultdict(list)
    for c in p.chars: lin[round(c["top"],0)].append(c)
    for t,cs in lin.items():
        iz=[c for c in cs if c["x1"]<335]
        de=[c for c in cs if c["x0"]>=335]
        if iz and de: fin[round(max(c["x1"] for c in iz))]+=1
print("borde derecho de la columna izquierda:",sorted(fin.items(),key=lambda t:-t[1])[:8])
