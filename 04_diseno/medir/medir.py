import pdfplumber, collections, statistics, json, sys
REF="/root/.claude/uploads/e718506c-f800-59cb-a388-d13f7f594b6c/8e917875-Extra_Time___Investor_Report_Final_3.pdf"
pdf=pdfplumber.open(REF)
print("paginas:",len(pdf.pages))
tam=collections.Counter((round(p.width,1),round(p.height,1)) for p in pdf.pages)
print("tamanos:",tam.most_common())
# fuentes y tamanos
f=collections.Counter()
for p in pdf.pages:
    for c in p.chars:
        f[(c["fontname"],round(c["size"],1))]+=1
for k,v in f.most_common(30):
    print("  %-46s %6.1f  %6d"%(k[0],k[1],v))
