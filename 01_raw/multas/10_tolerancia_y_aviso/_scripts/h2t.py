import sys,re
from bs4 import BeautifulSoup
for p in sys.argv[1:]:
    s=BeautifulSoup(open(p,'rb').read(),'html.parser')
    for x in s(['script','style','noscript','svg']): x.decompose()
    t=re.sub(r'\n\s*\n+','\n',s.get_text('\n'))
    open(p.rsplit('.',1)[0]+'.txt','w').write(t)
