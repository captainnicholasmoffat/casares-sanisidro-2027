import sys,re,html
from html.parser import HTMLParser
class P(HTMLParser):
    def __init__(s): super().__init__(); s.o=[]; s.skip=0
    def handle_starttag(s,t,a):
        if t in('script','style','noscript'): s.skip+=1
        if t in('p','br','div','li','h1','h2','h3','h4','tr','td','th'): s.o.append('\n')
    def handle_endtag(s,t):
        if t in('script','style','noscript'): s.skip-=1
    def handle_data(s,d):
        if s.skip<=0: s.o.append(d)
p=P(); p.feed(open(sys.argv[1],encoding='utf-8',errors='replace').read())
t=re.sub(r'\n\s*\n+','\n',''.join(p.o)); t=re.sub(r'[ \t]+',' ',t)
open(sys.argv[2],'w').write(t) if len(sys.argv)>2 else print(t)
