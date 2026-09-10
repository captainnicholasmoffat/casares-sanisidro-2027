import pdfplumber, collections
REF="/root/.claude/uploads/e718506c-f800-59cb-a388-d13f7f594b6c/8e917875-Extra_Time___Investor_Report_Final_3.pdf"
pdf=pdfplumber.open(REF); P=72/25.4
# lineas de texto agrupadas por top -> ver donde arrancan y terminan
ini=collections.Counter(); fin=collections.Counter()
for p in pdf.pages:
    lin=collections.defaultdict(list)
    for c in p.chars: lin[round(c["top"],0)].append(c)
    for t,cs in lin.items():
        ini[round(min(c["x0"] for c in cs))]+=1
        fin[round(max(c["x1"] for c in cs))]+=1
print("arranques de linea:",sorted(ini.items(),key=lambda t:-t[1])[:6])
print("finales de linea  :",sorted(fin.items(),key=lambda t:-t[1])[:6])
izq=[k for k,v in ini.items() if v>20 and k<200]
der=[k for k,v in fin.items() if v>20]
print("col izq arranca en",sorted(izq)[:4],"  col der arranca en",sorted([k for k,v in ini.items() if v>20 and k>300])[:4])
print("finales >20:",sorted(der))
