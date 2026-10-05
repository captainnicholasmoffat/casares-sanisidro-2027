import pymupdf,subprocess,sys,os
pdf,a,b,pat=sys.argv[1],int(sys.argv[2]),int(sys.argv[3]),sys.argv[4]
d=pymupdf.open(pdf)
out=open(sys.argv[5],'a')
for i in range(a-1,b):
    png=f'/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/c23_raw/y2_canon_privados/_tools/ocr_tmp.png'
    d[i].get_pixmap(dpi=150).save(png)
    t=subprocess.run(['tesseract',png,'-','-l','spa','--psm','6'],capture_output=True,text=True).stdout
    out.write(f'=== p{i+1}\n{t}\n'); out.flush()
    if any(p.lower() in t.lower() for p in pat.split('|')): print('HIT page',i+1, flush=True)
