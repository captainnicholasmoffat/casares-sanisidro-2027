# -*- coding: utf-8 -*-
# Arma FUENTES.txt: una línea por archivo (archivo | bytes | URL | fecha de consulta | qué es), más lo leído y no guardado y los errores.
# Uso: python3 -I fuentes.py
import os
SCR = '/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad'
V = SCR + '/c23d_raw/v4_volumen'
RUIDO = SCR + '/ch/wt/01_raw/ruido_prueba'
W3A = SCR + '/c23c_raw/w3a_shows_calidad_alquiler'
Y7 = SCR + '/c23_raw/y7_espectaculos'
meta = {}
for l in open(V + '/_tmp/FUENTES_log_get.txt', encoding='utf-8'):
    c = [x.strip() for x in l.split(' | ')]
    if len(c) >= 5:
        meta[c[0]] = (c[2], c[3], ' | '.join(c[4:]))
# metadatos de copias de material previo (tomados de los FUENTES.txt de origen)
def load(fu, pref=''):
    d = {}
    if not os.path.exists(fu): return d
    for l in open(fu, encoding='utf-8', errors='replace'):
        c = [x.strip() for x in l.split(' | ')]
        if len(c) >= 5:
            d[os.path.basename(c[0])] = (c[2], c[3], ' | '.join(c[4:]))
    return d
prev = {}
for fu in (RUIDO + '/1_estaciones/FUENTES.txt', RUIDO + '/2_og27_y_faltas/FUENTES.txt', W3A + '/FUENTES.txt', Y7 + '/FUENTES.txt'):
    prev.update(load(fu))
manual = {
 'guias_afuera/australia_victoria_EPA_1826_protocolo_ruido.docx': ('https://www.epa.vic.gov.au/sites/default/files/2025-09/Noise-limit-and-assessment-protocol-commercial%2C-industrial-and-trade-premises-and-entertainment-venues.docx', '2026-10-07', 'EPA Victoria (Australia), publicación 1826: Noise limit and assessment protocol (Parte II: 65 dB(A) afuera para eventos al aire libre), versión 2025-09'),
 'copias_previas/w3a_calculo_salida_kits_23ter.txt': ('(copia de c23c_raw/w3a_shows_calidad_alquiler/_tools/calculo_salida.txt)', '2026-10-07', 'Salida del cálculo del c23c/w3a: composición y precio del kit de show de 29,5 M y del kit de callejeros de 4,9 M'),
 '_tools/calculo.py': ('(propio)', '2026-10-07', '[cálculo propio] topes, volumen por público, distancias a la fachada, graves, precios y kits'),
 '_tools/calculo_salida.txt': ('(propio)', '2026-10-07', 'salida de calculo.py'),
 '_tools/get.py': ('(propio)', '2026-10-07', 'descarga con curl (TLS verificado), guarda original y .txt, anota en FUENTES'),
 '_tools/hx.py': ('(propio)', '2026-10-07', 'lista productos de la API pública de Hendrix'),
 '_tools/tm.py': ('(copia del c23c/w3a)', '2026-10-07', 'lista productos de búsquedas de Todo Música'),
 '_tools/fuentes.py': ('(propio)', '2026-10-07', 'arma este FUENTES.txt'),
 '_tools/fuentes_cola.txt': ('(propio)', '2026-10-07', 'texto de las secciones finales de FUENTES.txt (leído y no guardado, errores)'),
 '_tools/ca_sanisidro_bundle.pem': ('(armado con /etc/ssl/certs + puestos_raw/d1_terreno/work/ca_plus_ov_dv.pem, según las reglas)', '2026-10-07', 'cadena de certificados para sanisidro.gob.ar (TLS verificado)'),
}
rows = []
for root, dirs, files in os.walk(V):
    dirs[:] = [d for d in dirs if d != '_tmp']
    for fn in sorted(files):
        full = os.path.join(root, fn); rel = os.path.relpath(full, V)
        if rel == 'FUENTES.txt': continue
        b = os.path.getsize(full)
        base = rel[:-4] if rel.endswith('.txt') and not rel.startswith('_tools') else rel
        if rel in manual:
            u, f, q = manual[rel]
        elif rel.endswith('.docx.txt') and base in manual:
            u, f, q = manual[base]; q = '[texto extraído] ' + q
        elif rel in meta:
            u, f, q = meta[rel]
        elif base in meta:
            u, f, q = meta[base]; q = '[texto extraído] ' + q
        elif rel.startswith('copias_previas/'):
            n = os.path.basename(rel); nb = os.path.basename(base)
            if n in prev:
                u, f, q = prev[n]
            elif nb in prev:
                u, f, q = prev[nb]; q = '[texto extraído] ' + q
            else:
                u, f, q = ('(material previo del repo; ver FUENTES de origen)', '2026-10-05', 'copia de material previo')
            q = '[copia de material previo] ' + q
        else:
            u, f, q = ('?', '?', '?')
        rows.append(f'{rel} | {b} | {u} | {f} | {q}')
hdr = ['FUENTES · c23d / v4 · Tope de volumen para shows municipales al aire libre y el equipo · consultado el 07/10/2026',
       'Formato: archivo | bytes | URL | fecha de consulta | qué es. Las copias de material previo traen la URL y la fecha de su FUENTES de origen.', '']
tail = open(V + '/_tools/fuentes_cola.txt', encoding='utf-8').read() if os.path.exists(V + '/_tools/fuentes_cola.txt') else ''
open(V + '/FUENTES.txt', 'w', encoding='utf-8').write('\n'.join(hdr + rows) + '\n\n' + tail)
print(len(rows), 'líneas;', sum(1 for r in rows if '| ? |' in r), 'sin metadatos')
