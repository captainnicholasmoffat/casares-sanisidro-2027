import re,html,sys
for f in sys.argv[1:]:
    t=open(f,encoding='utf-8',errors='ignore').read()
    t=re.sub(r'<script.*?</script>','',t,flags=re.S|re.I)
    t=re.sub(r'<style.*?</style>','',t,flags=re.S|re.I)
    t=re.sub(r'<(nav|header|footer)\b.*?</\1>','',t,flags=re.S|re.I)
    x=html.unescape(re.sub(r'<[^>]+>',' ',t))
    x=re.sub(r'\s+',' ',x)
    print('=====',f); print(x)
