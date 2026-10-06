import sys, openpyxl, csv
src, out = sys.argv[1], sys.argv[2]
wb = openpyxl.load_workbook(src, read_only=True)
print(wb.sheetnames)
ws = wb[wb.sheetnames[0]]
rows = ws.iter_rows(values_only=True)
hdr=None; n=0; keep=[]
for i,r in enumerate(rows):
    if hdr is None:
        if r and any(isinstance(c,str) and 'CUE' in c.upper() for c in r if c):
            hdr=[str(c).strip() if c else f'c{j}' for j,c in enumerate(r)]
            print(i, hdr)
        elif i<15: print('pre',i,r[:8])
        continue
    n+=1
    d=dict(zip(hdr,r))
    s=' '.join(str(v) for v in r if v)
    if 'Buenos Aires' in s and 'San Isidro' in s:
        keep.append(r)
print('total rows',n,'kept',len(keep))
with open(out,'w',newline='',encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(hdr); w.writerows(keep)
