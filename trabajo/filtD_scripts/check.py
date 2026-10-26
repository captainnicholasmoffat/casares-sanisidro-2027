import re,sys
d=open(sys.argv[1]).read()
norm=re.sub(r'\s+',' ',d)
for i,line in enumerate(open(sys.argv[2]),1):
    line=line.rstrip('\n')
    if not line.strip(): continue
    parts=line.split(' | ')
    orig=parts[1].strip()
    ok = orig in norm
    if not ok:
        print(i, 'NOTFOUND', orig[:120])
