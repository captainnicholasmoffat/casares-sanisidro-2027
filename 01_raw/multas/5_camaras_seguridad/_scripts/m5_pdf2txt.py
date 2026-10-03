import sys, pymupdf
for f in sys.argv[1:]:
    doc = pymupdf.open(f)
    out = f.rsplit('.',1)[0] + '.txt'
    with open(out,'w',encoding='utf8') as o:
        for i,p in enumerate(doc):
            o.write(f"\n=== p.{i+1} ===\n"); o.write(p.get_text())
    print(out, len(open(out,encoding='utf8').read().split()))
