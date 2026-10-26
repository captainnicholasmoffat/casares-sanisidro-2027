import re,html,sys
t=open(sys.argv[1],encoding='utf-8',errors='ignore').read()
t=re.sub(r'<script.*?</script>|<style.*?</style>','',t,flags=re.S|re.I)
t=re.sub(r'<br\s*/?>|</p>|</div>|</tr>|</li>|</h\d>','\n',t,flags=re.I)
t=html.unescape(re.sub(r'<[^>]+>',' ',t))
t=re.sub(r'[ \t\r\f\v]+',' ',t)
t=re.sub(r'\n\s*\n+','\n',t)
print(t)
