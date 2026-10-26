import re,html,sys
t=open(sys.argv[1],encoding='utf-8',errors='ignore').read()
t=re.sub(r'<script.*?</script>',' ',t,flags=re.S);t=re.sub(r'<style.*?</style>',' ',t,flags=re.S);t=re.sub(r'<[^>]+>',' ',t); t=html.unescape(t); t=re.sub(r'\s+',' ',t)
s=sys.argv[2] if len(sys.argv)>2 else ''
i=t.find(s) if s else 0
n=int(sys.argv[3]) if len(sys.argv)>3 else 3000
print(t[max(i,0):max(i,0)+n])
