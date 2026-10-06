import pymupdf, subprocess, sys, os
pdf=sys.argv[1]; out=sys.argv[2]
env=dict(os.environ, OMP_THREAD_LIMIT="1")
d=pymupdf.open(pdf)
for i,p in enumerate(d):
    base=os.path.join(out,f"p{i+1:03d}")
    if os.path.exists(base+".txt") and os.path.getsize(base+".txt")>0: continue
    x=d.extract_image(p.get_images()[0][0]); img=base+"."+x["ext"]
    open(img,"wb").write(x["image"])
    subprocess.run(["tesseract",img,base,"-l","spa","--psm","6"],capture_output=True,env=env,timeout=120)
    os.remove(img)
print("done")
