import re,sys,html
t=open(sys.argv[1],encoding='utf-8',errors='ignore').read()
t=re.sub(r'(?is)<(script|style|noscript).*?</\1>',' ',t)
t=re.sub(r'(?i)<br\s*/?>|</p>|</li>|</h\d>|</tr>|</div>','\n',t)
t=re.sub(r'<[^>]+>',' ',t); t=html.unescape(t)
t=re.sub(r'[ \t\r\f\v]+',' ',t); t=re.sub(r'\n\s*\n+','\n',t)
print(t)
