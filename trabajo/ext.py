import re,html,sys
t=open(sys.argv[1],encoding='utf-8',errors='ignore').read()
t=re.sub(r'<script.*?</script>|<style.*?</style>|<header.*?</header>|<footer.*?</footer>|<nav.*?</nav>','',t,flags=re.S)
print('TITLE:',re.findall(r'<title>(.*?)</title>',t,re.S)[:1])
for m in re.findall(r'datetime="([^"]+)"',t)[:2]: print('DT',m)
s=html.unescape(re.sub(r'<[^>]+>','\n',t))
lines=[re.sub(r'\s+',' ',l).strip() for l in s.split('\n')]
lines=[l for l in lines if len(l)>25]
n=int(sys.argv[2]) if len(sys.argv)>2 else 5000
print('\n'.join(lines)[:n])
