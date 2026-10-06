import sys, xlrd
p=sys.argv[1]
b=xlrd.open_workbook(p)
out=[]
for sh in b.sheets():
    out.append(f"[hoja {sh.name}]")
    for r in range(sh.nrows):
        row=[str(c.value) for c in sh.row(r)]
        if any(x.strip() for x in row): out.append(" | ".join(row))
open(p+'.txt','w').write("\n".join(out)); print(len(out))
