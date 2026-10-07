import sys, pymupdf
pdf, page, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
y0, y1 = float(sys.argv[4]), float(sys.argv[5])  # fractions of page height
dpi = int(sys.argv[6]) if len(sys.argv)>6 else 220
doc = pymupdf.open(pdf); p = doc[page-1]; r = p.rect
clip = pymupdf.Rect(r.x0, r.y0 + r.height*y0, r.x1, r.y0 + r.height*y1)
p.get_pixmap(dpi=dpi, clip=clip).save(out)
print(out, r)
