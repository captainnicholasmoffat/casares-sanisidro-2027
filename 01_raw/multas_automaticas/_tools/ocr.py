import sys,pymupdf,subprocess,os,tempfile
d=pymupdf.open(sys.argv[1]); out=[]
for i,p in enumerate(d):
    pix=p.get_pixmap(dpi=300); f=tempfile.mktemp(suffix='.png'); pix.save(f)
    t=subprocess.run(['tesseract',f,'-','-l','spa'],capture_output=True,text=True).stdout
    out.append(f'--- p{i+1} (OCR)\n'+t); os.remove(f)
open(sys.argv[2],'w').write('\n'.join(out)); print('ok',len(d))
