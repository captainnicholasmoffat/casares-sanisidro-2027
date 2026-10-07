# OCR de páginas de un PDF con pymupdf + tesseract (spa). Uso: python3 -I ocr.py pdf pag_desde pag_hasta salida.txt
import sys, pymupdf, subprocess, os, tempfile
pdf, a, b, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
d = pymupdf.open(pdf)
res = []
with tempfile.TemporaryDirectory() as td:
    for p in range(a - 1, min(b, d.page_count)):
        png = os.path.join(td, f'p{p+1}.png')
        d[p].get_pixmap(dpi=250).save(png)
        r = subprocess.run(['tesseract', png, '-', '-l', 'spa'], capture_output=True, text=True)
        res.append(f'=== OCR página {p+1} ===\n' + r.stdout)
open(out, 'w').write('\n'.join(res))
print(out, sum(len(x) for x in res))
