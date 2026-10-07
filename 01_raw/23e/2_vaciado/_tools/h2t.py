import sys,re,html
for f in sys.argv[1:]:
    s=open(f,encoding='utf-8',errors='ignore').read()
    s=re.sub(r'(?is)<(script|style|noscript)[^>]*>.*?</\1>',' ',s)
    s=re.sub(r'(?i)<br\s*/?>|</p>|</div>|</li>|</tr>|</h\d>','\n',s); s=re.sub(r'<[^>]+>',' ',s); s=html.unescape(s)
    s=re.sub(r'[ \t\r\f\v]+',' ',s); s=re.sub(r'\n\s*\n+','\n',s)
    open(f+'.txt','w').write(s)
