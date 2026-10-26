import re,html,sys
t=open(sys.argv[1],encoding='utf-8',errors='ignore').read()
t=re.sub(r'<script.*?</script>','',t,flags=re.S|re.I)
t=re.sub(r'<style.*?</style>','',t,flags=re.S|re.I)
t=re.sub(r'<[^>]+>','\n',t)
t=html.unescape(t)
t=re.sub(r'[ \t]+',' ',t)
t=re.sub(r'\n\s*\n+','\n',t)
open(sys.argv[2],'w').write(t)
