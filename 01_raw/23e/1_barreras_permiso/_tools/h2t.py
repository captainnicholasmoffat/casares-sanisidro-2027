import sys,re,html
src=sys.argv[1]; dst=sys.argv[2] if len(sys.argv)>2 else src+'.txt'
t=open(src,encoding='utf-8',errors='replace').read()
t=re.sub(r'(?s)<script.*?</script>|<style.*?</style>|<!--.*?-->','',t)
t=re.sub(r'(?i)<br\s*/?>|</p>|</div>|</tr>|</h\d>|</li>',"\n",t)
t=re.sub(r'<[^>]+>',' ',t); t=html.unescape(t)
t=re.sub(r'[ \t\r\f\v]+',' ',t); t=re.sub(r'\n\s*\n+',"\n",t)
open(dst,'w',encoding='utf-8').write(t)
print(dst,len(t))
