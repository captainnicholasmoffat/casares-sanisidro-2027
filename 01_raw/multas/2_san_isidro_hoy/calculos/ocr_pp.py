import pymupdf, subprocess, os, sys
from concurrent.futures import ThreadPoolExecutor
src,outdir,a,b=sys.argv[1],sys.argv[2],int(sys.argv[3]),int(sys.argv[4])
os.makedirs(outdir,exist_ok=True)
doc=pymupdf.open(src)
def ocr(i):
    out=f'{outdir}/p{i+1:03d}'
    if os.path.exists(out+'.txt'): return
    doc2=pymupdf.open(src); doc2[i].get_pixmap(dpi=110).save(out+'.png')
    subprocess.run(['tesseract',out+'.png',out,'-l','spa','--psm','6'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    os.remove(out+'.png')
with ThreadPoolExecutor(4) as ex: list(ex.map(ocr,range(a-1,min(b,len(doc)))))
print('done')
