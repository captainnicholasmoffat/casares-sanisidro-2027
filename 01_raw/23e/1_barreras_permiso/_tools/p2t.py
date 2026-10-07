import sys,pymupdf
d=pymupdf.open(sys.argv[1]); out=sys.argv[2] if len(sys.argv)>2 else sys.argv[1]+'.txt'
with open(out,'w',encoding='utf-8') as f:
    for i,p in enumerate(d):
        f.write(f"\n=== p{i+1}\n"); f.write(p.get_text())
print(out, d.page_count)
