import sys, pymupdf
p=sys.argv[1]
d=pymupdf.open(p)
t="\n".join(f"=== p{i+1} ===\n"+pg.get_text() for i,pg in enumerate(d))
open(p+'.txt','w').write(t); print(len(t))
