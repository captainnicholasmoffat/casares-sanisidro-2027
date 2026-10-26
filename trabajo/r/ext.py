import re,html,sys
f=sys.argv[1]; keys=sys.argv[2:]
t=open(f,encoding='utf-8',errors='ignore').read()
t=re.sub(r'<script.*?</script>',' ',t,flags=re.S);t=re.sub(r'<style.*?</style>',' ',t,flags=re.S);t=re.sub(r'<[^>]+>',' ',t); t=html.unescape(t); t=re.sub(r'\s+',' ',t)
for k in keys:
  n=0
  for m in re.finditer(k,t,flags=re.I):
    print('['+k+']',t[max(0,m.start()-150):m.start()+200]); n+=1
    if n>=3: break
