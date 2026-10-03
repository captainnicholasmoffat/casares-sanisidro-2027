# OCR rápido de un PDF escaneado probando rotaciones 0/90/270; guarda la mejor por página
import pymupdf, subprocess, os, sys, re
from concurrent.futures import ThreadPoolExecutor
os.environ['OMP_THREAD_LIMIT']='1'
src,outdir=sys.argv[1],sys.argv[2]
os.makedirs(outdir,exist_ok=True)
n=len(pymupdf.open(src))
def score(t): return len(re.findall(r'\b(de|la|DE|LA|el|EL|del|DEL|y|Y|en|EN)\b',t))
def ocr(i):
    out=f'{outdir}/p{i+1:03d}.txt'
    if os.path.exists(out): return
    d=pymupdf.open(src); best=('',-1)
    for rot in (0,90,270):
        png=f'{outdir}/tmp{i}_{rot}.png'
        d[i].get_pixmap(matrix=pymupdf.Matrix(100/72,100/72).prerotate(rot)).save(png)
        r=subprocess.run(['tesseract',png,'stdout','-l','spa','--psm','6'],capture_output=True,text=True)
        os.remove(png)
        s=score(r.stdout)
        if s>best[1]: best=(r.stdout,s)
        if s>40: break
    open(out,'w').write(best[0])
with ThreadPoolExecutor(4) as ex: list(ex.map(ocr,range(n)))
print('done',n)
