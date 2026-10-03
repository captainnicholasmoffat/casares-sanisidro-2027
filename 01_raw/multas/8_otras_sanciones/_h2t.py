import re,html,sys
src=sys.argv[1]; dst=sys.argv[2] if len(sys.argv)>2 else None
raw=open(src,'rb').read()
enc='utf-8'
try: raw.decode('utf-8')
except UnicodeDecodeError: enc='latin-1'
t=raw.decode(enc,errors='ignore')
t=re.sub(r'(?is)<script.*?</script>|<style.*?</style>','',t)
t=re.sub(r'(?i)<br\s*/?>|</p>|</div>|</li>|</h\d>|</tr>','\n',t)
t=html.unescape(re.sub(r'<[^>]+>',' ',t)); t=re.sub(r'[ \t\r]+',' ',t); t=re.sub(r'\n\s*\n+','\n',t)
if dst: open(dst,'w',encoding='utf-8').write(t)
else: print(t)
