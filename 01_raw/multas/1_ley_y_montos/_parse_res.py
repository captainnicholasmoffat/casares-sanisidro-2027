import re,html,glob,subprocess,sys
seen={}
for f in sys.argv[1:]:
    t=subprocess.run(['python3','_h2t.py',f],capture_output=True,text=True).stdout
    blocks=re.split(r'\n\s*\[(/ar-b/[^\]]+)\]',t)
    for i in range(1,len(blocks),2):
        url=blocks[i]; body=blocks[i+1]
        fe=re.search(r'Fecha de publicaci\S*:\s*([0-9/]+)',body)
        body=re.sub(r'\s+',' ',body)
        body=body.split('Última actualizacion')[0]
        seen[url]=((fe.group(1) if fe else '??/??/????'),body[:260])
for k,v in sorted(seen.items(),key=lambda x:x[1][0][-4:]+x[1][0][3:5]+x[1][0][:2]):
    print(v[0],k,v[1])
