import sys, os, re
import pymupdf
W='/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/agua_raw/w6_plan_provincia'
for f in sys.argv[1:]:
    p=os.path.join(W,f) if not f.startswith('/') else f
    out=os.path.join(W,'_txt',os.path.basename(p)+'.txt')
    if p.lower().endswith('.pdf'):
        try:
            d=pymupdf.open(p); t=''.join(f'\n=== PAGE {i+1} ===\n'+pg.get_text() for i,pg in enumerate(d)); n=len(d)
        except Exception as e:
            print('ERR',f,e); continue
    else:
        b=open(p,'rb').read()
        try: h=b.decode('utf-8')
        except UnicodeDecodeError: h=b.decode('latin-1')
        h=re.sub(r'(?is)<(script|style).*?</\1>',' ',h); t=re.sub(r'<[^>]+>',' ',h)
        import html; t=html.unescape(t); t=re.sub(r'[ \t\r]+',' ',t); t=re.sub(r'\n\s*\n+','\n',t); n=0
    open(out,'w').write(t); print(os.path.basename(p), n, 'pages', len(t.split()), 'words')
