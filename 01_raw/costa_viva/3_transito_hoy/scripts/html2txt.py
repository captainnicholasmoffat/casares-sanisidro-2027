import sys,re,html
for f in sys.argv[1:]:
    s=open(f,encoding='utf-8',errors='ignore').read()
    s2=re.sub(r'(?s)<script.*?</script>|<style.*?</style>','',s)
    s2=re.sub(r'(?i)<(br|/p|/li|/tr|/h\d|/div)[^>]*>','\n',s2)
    t=html.unescape(re.sub(r'<[^>]+>',' ',s2)); t=re.sub(r'[ \t]+',' ',t); t=re.sub(r'\n\s*\n+','\n',t)
    open(f.rsplit('.',1)[0]+'.txt','w').write(t)
    print('#####',f,len(t))
