import sys,re,html,subprocess
path=sys.argv[1]; out=sys.argv[2]
url='https://sibom.slyt.gba.gob.ar'+path
subprocess.run(['curl','-g','-sS','-L','-m','90','-A','Mozilla/5.0','-o',out,url])
s=open(out,'rb').read().decode('utf-8','ignore')
s2=re.sub(r'<script.*?</script>|<style.*?</style>','',s,flags=re.S|re.I)
t=html.unescape(re.sub(r'<[^>]+>','\n',s2)); t=re.sub(r'[ \t\r]+',' ',t); t=re.sub(r'\n\s*\n+','\n',t)
i=t.find('Boletines/'); j=t.find('Redes Sociales')
t=t[i:j] if i>=0 else t
open(out.rsplit('.',1)[0]+'.txt','w').write('URL: '+url+'\n'+t)
print(url, len(s)); print(t[:int(sys.argv[3]) if len(sys.argv)>3 else 6000])
