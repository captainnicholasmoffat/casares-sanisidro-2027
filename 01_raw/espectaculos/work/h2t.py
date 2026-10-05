import sys, re, html
from html.parser import HTMLParser
class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.out=[]; s.skip=0
    def handle_starttag(s,t,a):
        if t in ("script","style","noscript"): s.skip+=1
        if t in ("p","div","br","li","tr","h1","h2","h3","h4","h5","table","section","article","td","th","dt","dd"): s.out.append("\n")
    def handle_endtag(s,t):
        if t in ("script","style","noscript"): s.skip=max(0,s.skip-1)
    def handle_data(s,d):
        if not s.skip: s.out.append(d)
for f in sys.argv[1:]:
    raw=open(f,"rb").read().decode("utf-8","replace")
    p=P(); p.feed(raw)
    t="".join(p.out)
    t=re.sub(r"[ \t\r\f\v]+"," ",t); t=re.sub(r"\n\s*\n+","\n",t)
    out=re.sub(r"\.html?$","",f)+".txt"
    open(out,"w").write(t.strip()+"\n"); print(out, len(t))
