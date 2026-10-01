import sys,re,html,glob
for f in sys.argv[1:]:
    s=open(f,encoding='utf-8',errors='ignore').read()
    m=re.findall(r'article:published_time" content="([^"]+)"',s)
    s2=re.sub(r'(?s)<script.*?</script>|<style.*?</style>','',s)
    t=html.unescape(re.sub(r'<[^>]+>',' ',s2)); t=re.sub(r'\s+',' ',t)
    i=t.find('Agencia de Recaudación ×'); t=t[i+24:] if i>0 else t
    j=t.find('147 Atención al vecino'); t=t[:j] if j>0 else t
    # cut related news block: first occurrence of pattern 'YYYY-MM-DD 00:00:00'
    k=re.search(r'\S+ [^.]{0,200}\d{4}-\d{2}-\d{2} 00:00:00',t)
    if k: t=t[:k.start()]
    print('#####',f.split('/')[-1],m[:1]); print(t.strip()[:4000]); print()
