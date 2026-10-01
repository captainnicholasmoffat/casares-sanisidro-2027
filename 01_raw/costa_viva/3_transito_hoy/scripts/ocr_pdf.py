# OCR (tesseract, español) de PDFs escaneados del Boletín. Salida: <nombre>_OCR.txt
import sys, pymupdf, subprocess, os, tempfile
for src in sys.argv[1:]:
    d=pymupdf.open(src); out=[]
    for i,p in enumerate(d):
        pix=p.get_pixmap(dpi=200); fn=tempfile.mktemp(suffix='.png'); pix.save(fn)
        t=subprocess.run(['tesseract',fn,'-','-l','spa'],capture_output=True,text=True).stdout
        out.append(f'\n=== PAGE {i+1} ===\n'+t); os.remove(fn)
    open(os.path.splitext(src)[0]+'_OCR.txt','w').write(''.join(out)); print(src,'ok')
