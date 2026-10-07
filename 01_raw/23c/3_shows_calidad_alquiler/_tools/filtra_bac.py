# Lee un CSV OCDS de Buenos Aires Compras por stdin y guarda las filas cuyo texto menciona sonido.
import sys, csv, re
csv.field_size_limit(10**9)
out = open(sys.argv[1], 'w', newline='')
r = csv.reader(sys.stdin)
w = csv.writer(out)
h = next(r); w.writerow(h)
pat = re.compile(r'(?i)\bsonido|sonorizaci|audio para evento|amplificaci')
n = k = 0
for row in r:
    n += 1
    txt = ' '.join(row[1:4] + row[11:13]) if len(row) > 13 else ' '.join(row)
    if pat.search(txt):
        w.writerow(row); k += 1
print('filas', n, 'coinciden', k)
