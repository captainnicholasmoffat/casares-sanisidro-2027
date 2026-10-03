import sys, os
from bs4 import BeautifulSoup
def ext(p):
    if p.lower().endswith('.pdf'):
        import fitz
        d = fitz.open(p)
        return "\n".join(f"\n=== PAGINA {i+1} ===\n" + pg.get_text() for i, pg in enumerate(d))
    raw = open(p, 'rb').read()
    s = BeautifulSoup(raw, 'html.parser')
    for t in s(['script','style','noscript']): t.decompose()
    return s.get_text("\n")
for p in sys.argv[1:]:
    out = sys.argv[-1] if False else None
    t = ext(p)
    import re
    t = re.sub(r'\n\s*\n+', '\n\n', t)
    dest = os.environ.get('DEST')
    if dest:
        op = os.path.join(dest, os.path.basename(p).rsplit('.',1)[0] + '.txt')
    else:
        op = p.rsplit('.',1)[0] + '.txt'
    open(op,'w').write(t)
    print(op, len(t))
