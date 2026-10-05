import sys, pymupdf, subprocess, os, tempfile
for f in sys.argv[1:]:
    d=pymupdf.open(f); out=[]
    for i,p in enumerate(d):
        pix=p.get_pixmap(dpi=250)
        tmp=tempfile.mktemp(suffix=".png"); pix.save(tmp)
        r=subprocess.run(["tesseract",tmp,"-","-l","spa"],capture_output=True,text=True)
        out.append(f"=== página {i+1} (OCR) ===\n"+r.stdout); os.remove(tmp)
    o=f[:-4]+"_OCR.txt"; open(o,"w").write("\n".join(out)); print(o)
