import sys, pymupdf
d=pymupdf.open(sys.argv[1]); o=[]
for i,p in enumerate(d): o.append(f"=====PAGE {i+1}=====\n"+p.get_text())
open(sys.argv[2],'w').write('\n'.join(o))
