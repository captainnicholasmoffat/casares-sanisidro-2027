import sys, zipfile, re, html
p=sys.argv[1]
z=zipfile.ZipFile(p)
x=z.read('word/document.xml').decode('utf-8','replace')
x=re.sub(r'</w:p>','\n',x); x=re.sub(r'</w:tc>',' | ',x); x=re.sub(r'<w:tab/>','\t',x)
x=re.sub(r'<[^>]+>','',x); x=html.unescape(x)
open(p+'.txt','w').write(x)
print(len(x))
