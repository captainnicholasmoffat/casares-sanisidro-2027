import sys, re
from bs4 import BeautifulSoup
for f in sys.argv[1:]:
    s = BeautifulSoup(open(f,'rb').read(), 'html.parser')
    d = s.find(id='codeLawSectionNoHead') or s.find(id='display_code_many_law_sections')
    t = d.get_text('\n') if d else ''
    t = re.sub(r'\n\s*\n+', '\n', t); t = re.sub(r'[ \t]+', ' ', t)
    open(f.rsplit('.',1)[0]+'.txt','w').write(t)
    print(f, len(t))
