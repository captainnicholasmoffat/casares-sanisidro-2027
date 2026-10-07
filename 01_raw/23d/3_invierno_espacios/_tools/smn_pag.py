# Vuelca el texto de un rango de páginas (1-based) de un PDF a stdout
import sys, pymupdf
d = pymupdf.open(sys.argv[1])
a, b = int(sys.argv[2]), int(sys.argv[3])
for p in range(a-1, b):
    print('=====PAGE', p+1)
    print(d[p].get_text())
