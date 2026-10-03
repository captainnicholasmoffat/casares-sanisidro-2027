import pymupdf,subprocess,sys,os
os.environ['OMP_THREAD_LIMIT']='1'
src,outdir,dpi=sys.argv[1],sys.argv[2],int(sys.argv[3])
first=int(sys.argv[4]) if len(sys.argv)>4 else 1
last=int(sys.argv[5]) if len(sys.argv)>5 else None
os.makedirs(outdir,exist_ok=True)
d=pymupdf.open(src); last=last or len(d)
for pn in range(first,last+1):
    fn=os.path.join(outdir,f'p{pn:03d}.png')
    d[pn-1].get_pixmap(dpi=dpi).save(fn)
    r=subprocess.run(['tesseract',fn,'-','-l','spa','--psm','6'],capture_output=True,text=True,env=dict(os.environ,OMP_THREAD_LIMIT='1'))
    open(os.path.join(outdir,f'p{pn:03d}.txt'),'w').write(r.stdout)
    os.remove(fn)
print('done',src)
