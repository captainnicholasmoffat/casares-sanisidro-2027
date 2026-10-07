# Extrae de las Estadísticas Climatológicas Normales 1991-2020 (SMN, 2023) las filas "Promedio"
# de cada cuadro, para San Fernando Aero, Aeroparque Aero y Buenos Aires Observatorio.
# Uso: python3 -I smn_extrae.py <pdf> > salida.csv
import sys, pymupdf
d = pymupdf.open(sys.argv[1])
EST = {'SAN FERNANDO AERO': 189, 'AEROPARQUE AERO': 277, 'BUENOS AIRES OBSERVATORIO': 285}
TIT = ('Temperatura', 'Heliofania', 'Precipitaci', 'Frecuencia de d', 'Nubosidad', 'Humedad',
       'Tensión', 'Presión', 'Velocidad del Viento', 'Viento máximo', 'Frecuencia (')
print('estacion;pagina;cuadro;Ene;Feb;Mar;Abr;May;Jun;Jul;Ago;Sep;Oct;Nov;Dic;Anual')
for n, p0 in EST.items():
    for p in range(p0 - 1, p0 + 7):
        lines = [l.strip() for l in d[p].get_text().split('\n')]
        tits = [l for l in lines if l.startswith(TIT)]
        tits = [t for t in tits if not t.startswith('Frecuencia (')]
        proms = []
        for i, l in enumerate(lines):
            if l == 'Promedio':
                vals = lines[i + 1:i + 14]
                ok = lambda v: v in ('S/D', '< 0.1') or v.replace('.', '').replace('-', '').isdigit()
                if len(vals) == 13 and all(ok(v) for v in vals):
                    proms.append(vals)
        # en la página de viento la tabla de frecuencias por dirección no tiene 13 valores
        tt = [t for t in tits if not t.startswith('Viento máximo')]
        # Correcciones manuales: en estas páginas el texto de los títulos sale en otro orden que los cuadros
        # (revisado a ojo: el promedio anual de una frecuencia es suma; el de una velocidad, promedio).
        FIX = {('AEROPARQUE AERO', 279): ['Humedad relativa (%)', 'Temperatura de rocío (°C)', 'Temperatura de bulbo húmedo (°C)'],
               ('AEROPARQUE AERO', 281): ['Velocidad del Viento (km/h) (2011-2020)', 'Frecuencia de días con Viento fuerte (2011-2020)']}
        tt = FIX.get((n, p + 1), tt)
        for k, v in enumerate(proms):
            t = tt[k] if k < len(tt) else '?'
            print(';'.join([n, str(p + 1), t] + v))
