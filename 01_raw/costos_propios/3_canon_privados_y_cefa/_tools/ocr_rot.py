import pymupdf,subprocess,sys
pdf,a,b,out,rot=sys.argv[1],int(sys.argv[2]),int(sys.argv[3]),sys.argv[4],int(sys.argv[5])
d=pymupdf.open(pdf); f=open(out,'a')
png='/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/c23_raw/y2_canon_privados/_tools/ocr_tmp3.png'
for i in range(a-1,b):
    m=pymupdf.Matrix(150/72,150/72).prerotate(rot)
    d[i].get_pixmap(matrix=m).save(png)
    t=subprocess.run(['tesseract',png,'-','-l','spa','--psm','6'],capture_output=True,text=True).stdout
    f.write(f'=== p{i+1}\n{t}\n'); f.flush()
