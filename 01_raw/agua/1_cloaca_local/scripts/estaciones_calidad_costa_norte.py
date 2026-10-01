# -*- coding: utf-8 -*-
"""
Recalcula, estación por estación, la calidad bacteriológica de la costa norte del Río de la Plata
(Tigre, San Fernando, San Isidro, Vicente López y CABA norte como referencia) a partir de los CSV
publicados por el CIAM / Subsecretaría de Ambiente de la Nación (red de monitoreo del Río de la Plata,
campañas 2004, 2010, 2016-2025). Consultados: 2026-09-29 (copia local) y verificados 2026-10-01.

Reglas de limpieza (documentadas):
 - Separador de campos ';'. Encabezados distintos por año: se normalizan por patrón.
 - Números con punto de miles (ej. "2.000.000", "1.100", "41.000") -> se quitan los puntos.
   Sólo se aplica si el valor coincide con ^\d{1,3}(\.\d{3})+$ (las bacterias se informan como enteros).
 - Valores censurados "<10", "<100": se guardan como el límite y se marcan; nunca cuentan como > 126.
 - "no se midió", "s/m", "s/i", "en obra", "no muestreó", "sin muestra", "-": sin dato.
 - Unidades según el encabezado: 2004 y 2010 NMP/100 ml; 2016-2023 UFC/100 ml; 2024 y 2025 el
   encabezado no trae unidad (se asume UFC/100 ml, ver informe).
 - Valor guía: 126 E. coli /100 ml (Res. ADA 42/2006, media geométrica; Directrices MSAL 2017, NGR).
   Aquí se cuenta cuántas MUESTRAS individuales superan 126 (indicador simple, no es la evaluación
   normativa, que usa media geométrica de varias muestras).
"""
import csv, glob, re, statistics, math, os, json, collections

SRC = '/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/ch/wt/01_raw/costa/c_arena/'
OUT = '/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/agua_raw/w1_cloaca_local/'
PREF = ('TI', 'SF', 'SI', 'VL', 'CA')
CABA_NORTE = {'CA041', 'CA043', 'CA044', 'CA046'}
MISSING = re.compile(r'^(no se midi[oó]|no se muestre[oó]|no muestre[oó]|sin muestra|en obra|s/m|s/i|-|)$', re.I)

def parse(v):
    v = (v or '').strip()
    if MISSING.match(v):
        return None, ''
    cens = ''
    if v.startswith('<'):
        cens = '<'; v = v[1:].strip()
    if re.fullmatch(r'\d{1,3}(\.\d{3})+', v):
        v = v.replace('.', '')
    v2 = v.replace(',', '.')
    try:
        return float(v2), cens
    except ValueError:
        return None, 'NO_NUM:' + v

def unit_for(col, year):
    c = col.lower()
    if 'nmp' in c: return 'NMP/100 ml'
    if 'ufc' in c: return 'UFC/100 ml'
    return 'sin unidad en encabezado (se asume UFC/100 ml)'

# Coordenadas publicadas (CIAM dt_id=412). Se corrige el formato (puntos de miles mal puestos).
coords = {}
for r in csv.DictReader(open(SRC + 'CIAM_RdP_estaciones_monitoreo_dt412.csv', encoding='utf-8-sig'), delimiter=';'):
    code = r['código_de_estación'].strip()
    def fix(s):
        s = s.replace('.', '')
        neg = s.startswith('-'); d = s.lstrip('-')
        val = float(d[:2] + '.' + d[2:])
        return -val if neg else val
    lat_raw, lon_raw = r['latitud'], r['longitud']
    coords[code] = (fix(lat_raw), fix(lon_raw), lat_raw, lon_raw)

records = []
for f in sorted(glob.glob(SRC + 'CIAM_RdP_monitoreo_*.csv')):
    year_file = re.search(r'monitoreo_(\d{4})', f).group(1)
    rows = [r for r in csv.reader(open(f, encoding='utf-8-sig', newline=''), delimiter=';') if r]
    h = [c.strip() for c in rows[0]]
    ci = [i for i, c in enumerate(h) if c.startswith('cód') or c.startswith('cod')][0]
    si = [i for i, c in enumerate(h) if c.startswith('sitio')][0]
    fi = h.index('fecha')
    ec = [i for i, c in enumerate(h) if re.search(r'escher', c)]
    fc = [i for i, c in enumerate(h) if re.search(r'colif_fecales', c)]
    en = [i for i, c in enumerate(h) if re.search(r'enteroc', c)]
    for r in rows[1:]:
        if len(r) <= ci: continue
        code = r[ci].strip()
        if not code.startswith(PREF): continue
        if code.startswith('CA') and code not in CABA_NORTE: continue
        rec = dict(archivo=os.path.basename(f), anio=year_file, codigo=code, sitio=r[si].strip(), fecha=r[fi].strip())
        for key, idx in (('ecoli', ec), ('colif_fec', fc), ('enteroc', en)):
            if idx:
                v, cens = parse(r[idx[0]])
                rec[key] = v; rec[key + '_cens'] = cens; rec[key + '_raw'] = r[idx[0]].strip()
                rec[key + '_unidad'] = unit_for(h[idx[0]], year_file)
            else:
                rec[key] = None; rec[key + '_cens'] = ''; rec[key + '_raw'] = ''; rec[key + '_unidad'] = ''
        records.append(rec)

# Muestras individuales (para auditoría)
with open(OUT + 'estaciones_calidad_costa_norte_muestras.csv', 'w', newline='', encoding='utf-8') as fo:
    keys = ['archivo', 'anio', 'codigo', 'sitio', 'fecha', 'ecoli_raw', 'ecoli', 'ecoli_cens', 'ecoli_unidad',
            'colif_fec_raw', 'colif_fec', 'colif_fec_unidad', 'enteroc_raw', 'enteroc', 'enteroc_cens', 'enteroc_unidad']
    w = csv.DictWriter(fo, fieldnames=keys, extrasaction='ignore'); w.writeheader(); w.writerows(records)

partido = {'TI': 'Tigre', 'SF': 'San Fernando', 'SI': 'San Isidro', 'VL': 'Vicente López', 'CA': 'CABA (norte, referencia)'}
asociado = {
 'SI023': 'Desagüe pluvial de calle Perú ("canal aliviador del arroyo Pavón superior", según el Municipio 2017; "Desagüe Dardo Rocha" en OSM)',
 'SI022': 'Reserva Ecológica Ribera Norte (sin conducto identificado en la fuente)',
 'SI021': 'Espigón La Farola (sin conducto identificado en la fuente)',
 'SI024': 'Playa Espigón de Pacheco (sin conducto identificado en la fuente)',
 'SF015': 'Del Arca (sin conducto identificado en la fuente)',
 'VL031': 'Costa y Melo (sin conducto identificado en la fuente)',
 'VL032': 'Puerto de Olivos, espigón (sin conducto identificado en la fuente)',
 'VL033': 'Reserva Barrio El Ceibo (sin conducto identificado en la fuente)',
 'TI001': 'Canal Villanueva / Río Luján (según nombre del sitio)',
 'TI002': 'Canal Aliviador / Río Luján (según nombre del sitio)',
 'TI003': 'Río Carapachay / Arroyo Gallo Fiambre (según nombre del sitio)',
 'TI004': 'Río Reconquista / Río Luján (según nombre del sitio)',
 'TI005': 'Río Tigre antes del Luján (según nombre del sitio)',
 'TI006': 'Río Luján / Arroyo Caraguatá (según nombre del sitio)',
 'TI007': 'Río Luján / Canal San Fernando (según nombre del sitio)',
 'TI008': 'Río Capitán / Río San Antonio (según nombre del sitio)',
 'TI009': 'Arroyo Abra Vieja / Santa Rosa (según nombre del sitio)',
 'CA041': 'Parque de los Niños (sin conducto identificado en la fuente)',
 'CA043': 'Frente a la toma de agua de AySA (según nombre del sitio)',
 'CA044': 'Costanera Norte, espigón Abanico (sin conducto identificado en la fuente)',
 'CA046': 'Club de Pescadores (sin conducto identificado en la fuente)',
}

def stats(vals):
    nums = [v for v, c in vals if v is not None]
    if not nums: return {}
    gm = math.exp(sum(math.log(max(v, 1)) for v in nums) / len(nums))
    return dict(n=len(nums), mediana=statistics.median(nums), maximo=max(nums), media_geom=round(gm),
                n_sup126=sum(1 for v, c in vals if v is not None and c != '<' and v > 126))

by = collections.defaultdict(list)
for r in records: by[r['codigo']].append(r)
order = sorted(by, key=lambda c: (['VL', 'SI', 'SF', 'TI', 'CA'].index(c[:2]), c))
rows_out = []
for code in order:
    rs = by[code]
    name = collections.Counter(r['sitio'] for r in rs).most_common(1)[0][0]
    ec_vals = [(r['ecoli'], r['ecoli_cens']) for r in rs if r['ecoli'] is not None]
    ec_years = sorted({r['anio'] for r in rs if r['ecoli'] is not None})
    ec_units = sorted({r['ecoli_unidad'] for r in rs if r['ecoli'] is not None})
    s = stats(ec_vals)
    s21 = stats([(r['ecoli'], r['ecoli_cens']) for r in rs if r['ecoli'] is not None and int(r['anio']) >= 2021])
    fc_vals = [(r['colif_fec'], r['colif_fec_cens']) for r in rs if r['colif_fec'] is not None]
    sf = stats(fc_vals)
    en_vals = [(r['enteroc'], r['enteroc_cens']) for r in rs if r['enteroc'] is not None]
    se = stats(en_vals)
    lat, lon, latr, lonr = coords.get(code, (None, None, '', ''))
    maxrec = max((r for r in rs if r['ecoli'] is not None), key=lambda r: r['ecoli'], default=None)
    rows_out.append(dict(
        partido=partido[code[:2]], codigo=code, sitio=name,
        lat_publicada=latr, lon_publicada=lonr,
        lat=round(lat, 6) if lat else '', lon=round(lon, 6) if lon else '',
        conducto_o_curso_asociado=asociado.get(code, ''),
        campanias_total=len(rs),
        ecoli_n=s.get('n', 0), ecoli_anios=(ec_years[0] + '-' + ec_years[-1]) if ec_years else '',
        ecoli_mediana=s.get('mediana', ''), ecoli_max=s.get('maximo', ''),
        ecoli_max_fecha=maxrec['fecha'] if maxrec else '',
        ecoli_media_geom=s.get('media_geom', ''), ecoli_n_sup126=s.get('n_sup126', ''),
        ecoli_2021_2025_n=s21.get('n', 0), ecoli_2021_2025_mediana=s21.get('mediana', ''),
        ecoli_2021_2025_n_sup126=s21.get('n_sup126', ''),
        ecoli_unidades=' | '.join(ec_units),
        colif_fec_n=sf.get('n', 0), colif_fec_mediana=sf.get('mediana', ''), colif_fec_max=sf.get('maximo', ''),
        enteroc_n=se.get('n', 0), enteroc_mediana=se.get('mediana', ''), enteroc_max=se.get('maximo', ''),
        enteroc_n_sup33=sum(1 for v, c in en_vals if c != '<' and v > 33),
    ))
with open(OUT + 'estaciones_calidad_costa_norte.csv', 'w', newline='', encoding='utf-8') as fo:
    w = csv.DictWriter(fo, fieldnames=list(rows_out[0].keys())); w.writeheader(); w.writerows(rows_out)
for r in rows_out:
    print(r['codigo'], r['sitio'][:28], '| n', r['ecoli_n'], r['ecoli_anios'], '| med', r['ecoli_mediana'], '| max', r['ecoli_max'], r['ecoli_max_fecha'], '| gm', r['ecoli_media_geom'], '| >126', r['ecoli_n_sup126'], '| 21-25 n', r['ecoli_2021_2025_n'], 'med', r['ecoli_2021_2025_mediana'], '>126', r['ecoli_2021_2025_n_sup126'], '| CF n', r['colif_fec_n'], 'med', r['colif_fec_mediana'], '| Ent n', r['enteroc_n'], 'med', r['enteroc_mediana'], 'max', r['enteroc_max'], '>33', r['enteroc_n_sup33'], '|', r['lat'], r['lon'])
print('NO_NUM:', [ (r['codigo'],r['fecha'],k,r[k+'_raw']) for r in records for k in ('ecoli','colif_fec','enteroc') if str(r.get(k+'_cens','')).startswith('NO_NUM')])
