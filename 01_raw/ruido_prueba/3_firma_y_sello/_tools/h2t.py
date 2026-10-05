import re,html,sys
b=open(sys.argv[1],'rb').read()
try:
    t=b.decode('utf-8')
except UnicodeDecodeError:
    t=b.decode('cp1252',errors='replace')
t=re.sub(r'<script.*?</script>','',t,flags=re.S|re.I)
t=re.sub(r'<style.*?</style>','',t,flags=re.S|re.I)
t=re.sub(r'<br\s*/?>','\n',t,flags=re.I)
t=re.sub(r'</(p|div|h\d|li|tr)>','\n',t,flags=re.I)
t=re.sub(r'<a [^>]*href="([^"]+)"[^>]*>',r' [\1] ',t)
t=re.sub(r'<[^>]+>',' ',t)
t=html.unescape(t)
t=re.sub(r'[ \t\xa0]+',' ',t)
t=re.sub(r'\n\s*\n+','\n',t)
print(t)
