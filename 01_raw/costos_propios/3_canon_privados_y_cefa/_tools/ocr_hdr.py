import pymupdf,subprocess,sys
d=pymupdf.open(sys.argv[1]); a,b=int(sys.argv[2]),int(sys.argv[3])
png='/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/c23_raw/y2_canon_privados/_tools/ocr_hdr.png'
for i in range(a-1,b):
    p=d[i]; r=p.rect
    # en la página sin rotar, el encabezado del cuadro (rotado) está en la franja izquierda
    clip=pymupdf.Rect(r.x0, r.y0, r.x0+r.width*0.45, r.y1)
    m=pymupdf.Matrix(130/72,130/72).prerotate(90)
    p.get_pixmap(matrix=m,clip=clip).save(png)
    t=subprocess.run(['tesseract',png,'-','-l','spa','--psm','6'],capture_output=True,text=True,timeout=120).stdout
    lines=[l for l in t.splitlines() if any(k in l for k in ('Jurisdic','Programa','Unidad','Página','Pá'))]
    print(i+1,' || '.join(lines)[:300], flush=True)
