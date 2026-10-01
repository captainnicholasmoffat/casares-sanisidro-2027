import sys,re,html
from html.parser import HTMLParser
class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.t=[]; s.skip=0
    def handle_starttag(s,tag,a):
        if tag in('script','style','noscript'): s.skip+=1
        if tag in('p','br','div','li','h1','h2','h3','tr'): s.t.append('\n')
    def handle_endtag(s,tag):
        if tag in('script','style','noscript'): s.skip-=1
    def handle_data(s,d):
        if not s.skip: s.t.append(d)
p=P(); p.feed(open(sys.argv[1],encoding='utf-8',errors='replace').read())
t=re.sub(r'\n\s*\n+','\n',''.join(p.t))
print(t)
