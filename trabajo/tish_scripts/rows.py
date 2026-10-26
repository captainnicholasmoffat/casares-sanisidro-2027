import re, subprocess, sys
pdf = sys.argv[1]
keys = sys.argv[2].split('|')
out = subprocess.run(['pdftotext','-bbox',pdf,'-'],capture_output=True,text=True).stdout
pages = out.split('<page ')[1:]
for pi, pg in enumerate(pages, 1):
    ws = re.findall(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">([^<]*)</word>', pg)
    rows = {}
    for x0,y0,x1,y1,w in ws:
        y = round(float(y0))
        k = None
        for yy in rows:
            if abs(yy-float(y0))<=2: k=yy;break
        if k is None: k=y; rows[k]=[]
        rows[k].append((float(x0),float(x1),w))
    for y in sorted(rows):
        r = sorted(rows[y])
        label = ' '.join(w for x0,x1,w in r if not re.match(r'^-?[\d,]+\.\d\d$',w))
        if any(k.lower() in label.lower() for k in keys):
            nums = [(round(x1),w) for x0,x1,w in r if re.match(r'^-?[\d,]+\.\d\d$',w)]
            print(f'p{pi} y{y} | {label[:70]} | {nums}')
