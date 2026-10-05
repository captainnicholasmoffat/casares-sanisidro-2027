import re,html,sys
t=open(sys.argv[1],encoding='utf-8',errors='ignore').read()
if 'charset=windows-1252' in t[:3000].lower() or 'charset=iso-8859-1' in t[:3000].lower():
    try: t=open(sys.argv[1],encoding='cp1252',errors='ignore').read()
    except: pass
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
