import sys, os, re
p = sys.argv[1]
base, ext = os.path.splitext(p)
out = base + ".txt"
data = open(p,'rb').read()
txt = ""
if data[:4] == b'%PDF':
    import pymupdf
    try:
        doc = pymupdf.open(p)
        txt = "\n".join(f"\n===== PAG {i+1} =====\n" + pg.get_text() for i, pg in enumerate(doc))
    except Exception as e:
        txt = "ERROR PDF: %s" % e
else:
    from bs4 import BeautifulSoup
    try:
        s = data.decode('utf-8')
    except UnicodeDecodeError:
        s = data.decode('latin-1')
    soup = BeautifulSoup(s, 'html.parser')
    for t in soup(['script','style','noscript','svg']): t.decompose()
    txt = soup.get_text("\n")
    txt = re.sub(r'\n\s*\n+', '\n\n', txt)
open(out,'w').write(txt)
print("txt chars", len(txt), "->", os.path.basename(out))
