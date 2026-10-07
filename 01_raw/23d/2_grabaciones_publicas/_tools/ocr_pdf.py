# OCR de páginas de un PDF escaneado. Uso: python3 -I ocr_pdf.py PDF PAG_DESDE PAG_HASTA SALIDA_TXT DIR_TMP
import sys, subprocess, pymupdf, os
pdf, a, b, out, tmp = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], sys.argv[5]
doc = pymupdf.open(pdf)
res = []
for i in range(a - 1, min(b, len(doc))):
    png = os.path.join(tmp, 'p%03d.png' % (i + 1))
    doc[i].get_pixmap(dpi=200).save(png)
    t = subprocess.run(['tesseract', png, '-', '-l', 'spa'], capture_output=True).stdout.decode('utf-8', 'replace')
    res.append('\n=== PAGINA %d ===\n%s' % (i + 1, t))
open(out, 'w', encoding='utf-8').write(''.join(res))
print(len(doc), 'paginas en total')
