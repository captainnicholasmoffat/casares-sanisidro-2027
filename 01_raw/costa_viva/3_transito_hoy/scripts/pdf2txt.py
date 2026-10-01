import sys, pymupdf, os
for src in sys.argv[1:]:
    dst = os.path.splitext(src)[0] + '.txt'
    d = pymupdf.open(src)
    out = []
    for i, p in enumerate(d):
        out.append(f'\n=== PAGE {i+1} ===\n' + p.get_text())
    open(dst, 'w').write(''.join(out))
    print(os.path.basename(src), len(d), 'pages', sum(len(x.split()) for x in out), 'words')
