import sys, os, subprocess, pymupdf
from concurrent.futures import ThreadPoolExecutor
pdf, out = sys.argv[1], sys.argv[2]
pages = None
if len(sys.argv) > 3:
    a,b = sys.argv[3].split('-'); pages = range(int(a)-1, int(b))
d = pymupdf.open(pdf)
tmp = os.path.join(os.path.dirname(out), 'work', 'ocrtmp_' + os.path.basename(pdf))
os.makedirs(tmp, exist_ok=True)
idx = list(pages) if pages else list(range(d.page_count))
def do(i):
    png = os.path.join(tmp, f'p{i+1:03d}.png')
    d2 = pymupdf.open(pdf)
    d2[i].get_pixmap(dpi=220).save(png)
    r = subprocess.run(['tesseract', png, '-', '-l', 'spa', '--psm', '6'], capture_output=True, text=True, env=dict(os.environ, OMP_THREAD_LIMIT='1'))
    return i, r.stdout
res = {}
with ThreadPoolExecutor(3) as ex:
    for i, t in ex.map(do, idx):
        res[i] = t
with open(out, 'w') as f:
    for i in sorted(res):
        f.write(f"\n===== PAG {i+1} (OCR tesseract spa) =====\n{res[i]}")
print("done", len(res))
