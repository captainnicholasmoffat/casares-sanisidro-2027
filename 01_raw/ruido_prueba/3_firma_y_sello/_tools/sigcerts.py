import sys, pymupdf, subprocess, binascii, os, re
T=os.path.dirname(os.path.abspath(__file__))
raw=open(sys.argv[1],'rb').read()
d = pymupdf.open(sys.argv[1])
for x in range(1, d.xref_length()):
    try: o=d.xref_object(x, compressed=False)
    except Exception: continue
    if "/ByteRange" not in o: continue
    g=lambda k: d.xref_get_key(x,k)[1]
    br=[int(v) for v in re.findall(r'\d+', g("ByteRange"))]
    print("== xref",x,"SubFilter",g("SubFilter"),"Name",g("Name"),"M",g("M"),"Loc",g("Location"))
    seg=raw[br[0]+br[1]:br[2]].strip().strip(b"<>")
    der=binascii.unhexlify(seg)
    if der[1]==0x82: L=4+int.from_bytes(der[2:4],'big')
    elif der[1]==0x83: L=5+int.from_bytes(der[2:5],'big')
    else: L=len(der)
    der=der[:L]
    p=os.path.join(T,"sig.der"); open(p,"wb").write(der)
    out=subprocess.run(["openssl","pkcs7","-inform","DER","-in",p,"-print_certs","-noout"],capture_output=True,text=True)
    print(out.stdout.strip()[:2500], out.stderr.strip()[:300])
    print("RFC3161 timestamp token presente:", b"\x2a\x86\x48\x86\xf7\x0d\x01\x09\x10\x02\x0e" in der)
