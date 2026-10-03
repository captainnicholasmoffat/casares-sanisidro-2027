import sys,pymupdf,subprocess,os,tempfile
d=pymupdf.open(sys.argv[1]); out=[]
for i,p in enumerate(d):
    txt=p.get_text()
    if len(txt.strip())>200:
        out.append(f'--- p{i+1}\n'+txt); continue
    pix=p.get_pixmap(dpi=200); f=tempfile.mktemp(suffix='.png'); pix.save(f)
    t=subprocess.run(['tesseract',f,'-','-l','spa'],capture_output=True,text=True).stdout
    out.append(f'--- p{i+1} (OCR)\n'+t); os.remove(f)
open(sys.argv[2],'w').write('\n'.join(out)); print('ok',len(d))
