import re,sys,html
t=open(sys.argv[1],encoding='utf-8',errors='ignore').read()
m=re.search(r'<h1[^>]*>(.*?)</h1>',t,re.S)
t2=re.sub(r'(?is)<(script|style|noscript).*?</\1>',' ',t)
body=re.search(r'field-name-body.*?field-item even"[^>]*>(.*?)</div>\s*</div>',t2,re.S)
b=body.group(1) if body else ''
b=re.sub(r'(?i)<br\s*/?>|</p>|</li>','\n',b); b=html.unescape(re.sub('<[^>]+>',' ',b)); b=re.sub(r'[ \t]+',' ',b); b=re.sub(r'\n\s*\n+','\n',b)
print(b.strip())
