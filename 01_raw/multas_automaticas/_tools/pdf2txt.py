import sys,pymupdf
d=pymupdf.open(sys.argv[1])
out=[]
for i,p in enumerate(d):
    out.append(f'--- p{i+1}\n'+p.get_text())
t='\n'.join(out)
open(sys.argv[2],'w').write(t)
print(len(d),'pages',len(t),'chars')
