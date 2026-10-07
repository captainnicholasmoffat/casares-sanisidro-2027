# Extrae de las Estadísticas Climatológicas Normales 1991-2020 del SMN los promedios mensuales
# de días con precipitación >=1 mm, >=0,1 mm, tormenta, granizo y viento fuerte para 3 estaciones.
import sys, re, pymupdf
pdf = sys.argv[1]
d = pymupdf.open(pdf)
def promedios(pi):
    lines = [l.strip() for l in d[pi].get_text().split('\n')]
    out = []; titles = [l for l in lines if l.startswith('Frecuencia') or l.startswith('Precipitaci') or l.startswith('Velocidad') or l.startswith('Nubosidad') or l.startswith('Viento')]
    for i, l in enumerate(lines):
        if l == 'Promedio':
            vals = lines[i+1:i+14]
            out.append(vals)
    return out, titles
# primera página de cada estación (índice PDF 1-based)
est = {'SAN FERNANDO AERO': 189, 'AEROPARQUE AERO': 277, 'BUENOS AIRES OBSERVATORIO': 285}
for n, p0 in est.items():
    print('==', n)
    for off in (1, 4, 5, 6):
        prom, titles = promedios(p0 + off - 1)
        print(' pág PDF', p0 + off, 'títulos:', titles)
        for v in prom:
            print('   Promedio:', ' '.join(v))
