# Genera FUENTES.txt: archivo | bytes | URL | fecha de consulta | qué es
import os, csv, re
D='/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/costa_viva_raw/v3_transito_hoy/'
F='2026-10-01'
muni={l.split()[0]:l.split()[2] for l in open(D+'muni/fetched.txt') if l.strip()}
bol={}
for l in open(D+'boletin/urls_boletin.tsv'):
    p=l.rstrip('\n').split('\t'); bol[p[0]]=(p[3],p[1],p[2])
edi={}
for l in open(D+'edictos/urls.tsv'):
    p=l.rstrip('\n').split('\t'); edi[p[0]]=(p[3],p[1],p[2])
OV='Overpass API (espejos maps.mail.ru / overpass-api.de / overpass.private.coffee), consulta en scripts/ov.py'
fixed={
'boletin/boletin_0_1158.pdf':('https://boletines.sanisidro.gob.ar/uploads/boletin/boletin_0_1158.pdf','Boletín Oficial Ed. Extra 1158 (04/01/2019): Ordenanza 9051 Sistema Municipal de Estacionamiento Medido'),
'boletin/boletin_1_1129.pdf':('https://boletines.sanisidro.gob.ar/uploads/boletin/boletin_1_1129.pdf','Boletín Oficial #1129 (31/08/2023): Decreto 1759/2023 tarifa playa subterránea Martínez (concesión LP 1/1992)'),
'boletin/boletin_2_1253.pdf':('https://boletines.sanisidro.gob.ar/uploads/boletin/boletin_2_1253.pdf','Boletín Oficial Ed. Extra 1253 (2022): Decreto 1307/2022 tarifa concesión LP 1/1992'),
'boletin/gde_1750793065_DECRE-2025-605.pdf':('https://tesi.sanisidro.gob.ar/nfs-storage/gde/v2/gde_1750793065.pdf','Decreto 605/2025: SI Plan Urbano Costero; 33 Orientales con "dársenas de estacionamiento"'),
'edictos/muni_impacto-ambiental.html':('https://www.sanisidro.gob.ar/impacto-ambiental','Página municipal de Evaluaciones de Impacto Ambiental: sin documentos listados al 01/10/2026'),
'muni/muni_san-isidro-estaciona.html':('https://www.sanisidro.gob.ar/san-isidro-estaciona','Página municipal SIE: zonas, horarios y tarifa progresiva vigente del estacionamiento medido'),
'muni/search_estacionamiento.html':('https://www.sanisidro.gob.ar/search/node?keys=estacionamiento','Buscador municipal (sin resultados útiles)'),
'muni/search_recorridos.html':('https://www.sanisidro.gob.ar/search/node?keys=recorridos','Buscador municipal (sin resultados útiles)'),
'muni/notas_texto.txt':('(derivado)','Texto extraído de las notas municipales muni_*.html'),
'muni/urls_sel.tsv':('(derivado) índice de novedades municipales 2018-2026 (scratchpad/ch/wt/01_raw/costa/a_basura/indice_novedades_sanisidro_2018-2026.tsv)','Notas seleccionadas'),
'muni/fetched.txt':('(derivado)','Lista de notas descargadas con URL'),
'osm/boundary_coast.json':(OV,'OSM: límite del Partido de San Isidro (rel 1769044) y natural=coastline; base OSM 2026-10-01T08:26Z'),
'osm/parking.json':(OV,'OSM: amenity=parking/parking_space/bicycle_parking/rental en bbox costera (centros); base 2026-10-01T08:26Z'),
'osm/parking_geom.json':(OV,'OSM: estacionamientos con geometría en bbox costera; base 2026-10-01T08:53Z'),
'osm/parking_lanes.json':(OV,'OSM: calles con etiquetas parking:* en bbox costera (ninguna dentro de la zona costera); base 2026-10-01T08:26Z'),
'osm/bus_stops_routes.json':(OV,'OSM: paradas de colectivo y relaciones route=bus en bbox costera; base 2026-10-01T08:27Z'),
'osm/cycle.json':(OV,'OSM: ciclovías/bicisendas; base 2026-10-01T08:32Z'),
'osm/clubs.json':(OV+' (espejo private.coffee DESACTUALIZADO: base 2026-07-24)','OSM: clubes, parques, gastronomía en bbox costera (sólo exploratorio, no usado en cifras)'),
'osm/rail_localidades.json':(OV,'OSM: vías (Tren de la Costa, Mitre) y límites de localidades; base 2026-10-01T08:42Z'),
'osm/stations.json':(OV,'OSM: estaciones dentro del Partido de San Isidro; base 2026-10-01T08:24Z'),
'osm/stations_tdlc.json':(OV,'OSM: estaciones de la zona (Mitre, Tren de la Costa, Belgrano); base 2026-10-01T09:00Z'),
'osm/osrm_foot_table.json':('https://routing.openstreetmap.de/routed-foot/table/v1/driving/... (OSRM perfil peatonal FOSSGIS)','Matriz de distancias a pie estaciones -> costa'),
'osm/tiles_all.pkl':('(derivado) de osm/api_tiles/*.osm','OSM unido (nodos, vías, relaciones)'),
'osm/zonas.pkl':('(derivado)','Polígonos: partido, localidades, línea TdlC, zona costera'),
'trenes/www.trenesargentinos.gob.ar_es_lineas_tren-de-la-costa.html':('https://www.trenesargentinos.gob.ar/es/lineas/tren-de-la-costa (redirige a argentina.gob.ar/transporte/trenes-argentinos)','Portal Trenes Argentinos Operaciones: líneas operadas y noticias al 30/09/2026'),
'trenes/ar_transporte_trenes-argentinos_horarios-tarifas-y-recorridos_areametropolitana_tren-de-la-costa.html':('https://www.argentina.gob.ar/transporte/trenes-argentinos/horarios-tarifas-y-recorridos/areametropolitana/tren-de-la-costa','Página oficial Tren de la Costa (Av. Maipú - Delta); horarios no en el HTML'),
'trenes/ar_transporte_trenes-argentinos_horarios-tarifas-y-recorridos_areametropolitana_lineamitre.html':('https://www.argentina.gob.ar/transporte/trenes-argentinos/horarios-tarifas-y-recorridos/areametropolitana/lineamitre','Página oficial línea Mitre'),
'trenes/ar_transporte_trenes-argentinos_primeros-y-ultimos-trenes.html':('https://www.argentina.gob.ar/transporte/trenes-argentinos/primeros-y-ultimos-trenes','Página oficial primeros/últimos trenes (tabla cargada desde planilla Google)'),
'trenes/primeros_ultimos_trenes_hoja2.csv':('https://docs.google.com/spreadsheets/d/1AW4gSkzAv7-rosjlXOjiuR2fjsCT_v5hm7ekbPzs_u8/gviz/tq?tqx=out:csv&sheet=Hoja%202','Planilla oficial (id citado en la página de Trenes Argentinos) de primeros y últimos trenes'),
'trenes/ar_noticias_por-avances-en-la-renovacion-de-vias-el-ramal-tigre-estara-interrumpido-el-26-y-27-de.html':('https://www.argentina.gob.ar/noticias/por-avances-en-la-renovacion-de-vias-el-ramal-tigre-estara-interrumpido-el-26-y-27-de','Trenes Argentinos 22/09/2026: ramal Tigre interrumpido 26-27/09/2026'),
'trenes/ar_noticias_la-linea-mitre-retoma-sus-servicios-luego-de-obras-clave-para-fortalecer-la-seguridad.html':('https://www.argentina.gob.ar/noticias/la-linea-mitre-retoma-sus-servicios-luego-de-obras-clave-para-fortalecer-la-seguridad','Trenes Argentinos 28/09/2026: Mitre retoma servicios'),
'trenes/ar_trenes_preguntas_frecuentes.html':('https://www.argentina.gob.ar/transporte/trenes-argentinos/institucional/preguntasfrecuentes','Trenes Argentinos, preguntas frecuentes: bicicletas (excepción Tren de la Costa); líneas operadas'),
'trenes/cnrt_estadisticas_ferroviarias.html':('https://www.argentina.gob.ar/transporte/cnrt/estadisticas-ferroviarias','CNRT: índice de estadísticas ferroviarias'),
'trenes/ffcc_amba_pax_x_estacion_2026-08_cnrt.zip':('https://www.argentina.gob.ar/sites/default/files/ffcc_amba_pax_x_estacion_2026-08_cnrt.zip','CNRT: pasajeros pagos (boletos) por estación, todas las líneas, hasta ago-2026 (act. 08/09/2026)'),
'trenes/cnrt_boletos/Boletos Tren de la Costa.xlsx':('(extraído del zip anterior)','CNRT: pasajeros pagos por estación - Tren de la Costa'),
'trenes/cnrt_boletos/Boletos Mitre.xlsx':('(extraído del zip anterior)','CNRT: pasajeros pagos por estación - línea Mitre'),
'trenes/ffcc_amba_pax_metropolitanos_2026_08.xlsx':('https://www.argentina.gob.ar/sites/default/files/ffcc_amba_pax_metropolitanos_2026_08.xlsx','CNRT: pasajeros pagos transportados por línea (no usado en cifras)'),
'trenes/ffcc_amba_cumplimiento_de_programa_2026-08_cnrt.xlsx':('https://www.argentina.gob.ar/sites/default/files/ffcc_amba_cumplimiento_de_programa_2026-08_cnrt.xlsx','CNRT: trenes programados/cancelados/corridos por mes y observaciones (act. 17/09/2026)'),
'trenes/aumeto_tarifario_ffcc_mayo_2026.zip':('https://www.argentina.gob.ar/sites/default/files/aumeto_tarifario_ffcc_mayo_2026.zip','Resolución ST-MEC 27/2026 (15/05/2026) y anexos: tarifas trenes metropolitanos jun-sep 2026'),
'sube/trx2025_hexagonos_dia_habil_oct2025.csv':('https://datos.transporte.gob.ar/dataset/254f0d95-2a1e-481d-bbfd-9f98a4d694bf/resource/160a3ece-ccbd-4719-8406-8f28131a25e8/download/trx2025.csv','Secretaría de Transporte: transacciones SUBE de un día hábil promedio (día tipo oct-2025) por hexágono H3, modo y hora'),
'presupuesto/2024_iv_recursos_-_anual.txt':('https://www.sanisidro.gob.ar/transparencia (PDF 2024_iv_recursos_-_anual.pdf, copia en scratchpad/em/01_raw/sanisidro_transparencia/ejecucion_presupuestaria/)','Texto: ejecución presupuestaria de recursos 2024'),
'presupuesto/2025_iv_recursos.txt':('https://www.sanisidro.gob.ar/transparencia (PDF 2025_iv_recursos.pdf, copia en scratchpad/em/01_raw/...)','Texto: ejecución de recursos 2/1-30/12/2025 (fecha 13/4/2026)'),
'presupuesto/2026_ii_recursos.txt':('https://www.sanisidro.gob.ar/transparencia (PDF 2026_ii_recursos.pdf, copia en scratchpad/em/01_raw/...)','Texto: ejecución de recursos 1/4-30/6/2026'),
'presupuesto/ejec2025_estac.png':('(derivado, recorte del PDF 2025_iv_recursos)','Imagen: renglón 1.2.9.05 Tarifa de estacionamiento vía pública 2025'),
'presupuesto/ejec2025_estac_hdr.png':('(derivado)','Imagen: encabezado'),
'presupuesto/ejec2025_derecho.png':('(derivado)','Imagen: renglón 1.2.2.16 Derecho de estacionamiento 2025'),
'presupuesto/ejec2026ii_estac.png':('(derivado, recorte del PDF 2026_ii_recursos)','Imagen: renglón 1.2.9.05, 2º trim. 2026'),
'presupuesto/ejec2026ii_estac_hdr.png':('(derivado)','Imagen: encabezado'),
'presupuesto/ejec2026ii_derecho.png':('(derivado)','Imagen: renglón 1.2.2.16, 2º trim. 2026'),
'estacionamientos_osm_zona_costera.csv':('(cálculo propio, scripts/estacionamientos_osm.py)','Estacionamientos OSM en la zona costera, por tramo, con superficie y estimación de autos'),
'calles_zona_costera.txt':('(cálculo propio, scripts/calles_zona.py)','Km de calles públicas en la zona costera por tramo y cota teórica de lugares en cordón'),
'distancias_estaciones_costa.csv':('(cálculo propio, scripts/distancias_caminando.py)','Distancias a pie y en línea recta estación -> 9 puntos de la costa'),
'paradas_colectivo_cercanas_costa.csv':('(cálculo propio, scripts/paradas_cercanas.py)','Paradas de colectivo OSM más cercanas a cada punto de la costa'),
'colectivos_zona_costera_osm.csv':('(cálculo propio, scripts/colectivos_zona.py)','Relaciones de colectivo OSM que entran en la zona costera'),
'sube_usos_lineas_costa_por_dia.csv':('(cálculo propio, scripts/sube_resumen.py, sobre sube/sube_usos_*.csv)','Usos SUBE diarios por línea (TdlC, Mitre Tigre, colectivos de la zona) en 5 semanas'),
'sube_resumen_semanas.txt':('(cálculo propio)','Promedio hábil vs sábado vs domingo por línea y semana'),
'sube_hexagonos_zona_costera.csv':('(cálculo propio, scripts/hexagonos_costa.py)','Transacciones SUBE día hábil (oct-2025) en hexágonos de la zona costera'),
'sube_hexagonos_estaciones.csv':('(cálculo propio, scripts/hexagonos_estaciones.py)','Transacciones SUBE día hábil (oct-2025) en el hexágono de cada estación'),
'cnrt_resumen.txt':('(cálculo propio, scripts/cnrt_resumen.py)','Resumen anual de pasajeros pagos por estación y trenes programados (CNRT)'),
'boletin/urls_boletin.tsv':('(derivado)','URLs TESI de los actos descargados'),
'edictos/urls.tsv':('(derivado)','URLs TESI de los edictos de impacto ambiental 2025-2026'),
}
rows=[]
for root,dirs,files in os.walk(D):
    for fn in sorted(files):
        full=os.path.join(root,fn); rel=os.path.relpath(full,D)
        if rel=='FUENTES.txt': continue
        size=os.path.getsize(full); url=''; que=''
        base=os.path.splitext(fn)[0].replace('_OCR','')
        if rel in fixed: url,que=fixed[rel]
        elif rel.startswith('muni/muni_20'):
            k=fn if fn.endswith('.html') else None
            url=muni.get(fn,''); que='Nota de prensa del Municipio (según el Municipio)'
        elif rel.startswith('boletin/') and base in bol:
            url,fp,ref=bol[base]; que=f'TESI/Boletín, publ. {fp}: {ref}'+(' [texto]' if fn.endswith('.txt') else '')+(' [OCR tesseract]' if '_OCR' in fn else '')
        elif rel.startswith('boletin/') and base in ('boletin_0_1158','boletin_1_1129','boletin_2_1253','gde_1750793065_DECRE-2025-605'):
            url,que=fixed['boletin/'+base+'.pdf']; que+=' [texto extraído]'
        elif rel.startswith('edictos/') and base in edi:
            url,fp,ref=edi[base]; que=f'TESI/Boletín, publ. {fp}: {ref}'+(' [texto]' if fn.endswith('.txt') else '')
        elif rel.startswith('edictos/muni_impacto'):
            url,que=fixed['edictos/muni_impacto-ambiental.html']
        elif rel.startswith('osm/api_tiles/'):
            m=re.match(r'map_(.+)_(.+)_(.+)_(.+)\.osm',fn); url=f'https://api.openstreetmap.org/api/0.6/map?bbox={m.group(1)},{m.group(2)},{m.group(3)},{m.group(4)}'; que='OSM API: tesela completa de la zona costera (datos al 01/10/2026)'
        elif rel.startswith('sube/sube_usos_'):
            y=fn[10:14]; url=f'https://archivos-datos.transporte.gob.ar/upload/Dat_Ab_Usos/dat-ab-usos-{y}.csv (pedidos HTTP Range, sólo el día)'; que=f'SUBE: usos por línea del día {fn[10:20]} (dataset sube-cantidad-de-transacciones-usos-por-fecha)'
        elif rel.startswith('trenes/tarifas/'):
            url='(extraído de trenes/aumeto_tarifario_ffcc_mayo_2026.zip)'; que='Resolución ST-MEC 27/2026 y anexos'+(' [texto]' if fn.endswith('.txt') else '')+(' [imagen pág.]' if fn.endswith('.png') else '')
        elif rel.startswith('trenes/') and fn.endswith('.txt'):
            k='trenes/'+base+'.html'; url,que=fixed.get(k,('',''));
            que=(que+' [texto]') if que else '[texto]'
        elif rel.startswith('muni/') and fn.endswith('.txt'):
            k='muni/'+base+'.html'; url,que=fixed.get(k,('','')); que+=' [texto]'
        elif rel.startswith('scripts/'):
            url='(script propio)'; que='Script de este informe'
        rows.append((rel,size,url,F,que))
with open(D+'FUENTES.txt','w') as f:
    f.write('archivo | bytes | URL | fecha de consulta | qué es\n')
    for r in sorted(rows): f.write(' | '.join(str(x) for x in r)+'\n')
    f.write('\n# PÁGINAS LEÍDAS Y NO GUARDADAS (consulta 2026-10-01)\n')
    for u,q in [
     ('https://www.lanacion.com.ar/sociedad/en-san-isidro-hay-calles-exclusivas-para-los-vecinos-nid877099/','La Nación 21/01/2007: estacionamiento exclusivo para vecinos en Manuel A. Aguirre y Almafuerte (Acassuso) por congestión de fin de semana cerca de estación Barrancas (leída con WebFetch)'),
     ('https://www.quepasaweb.com.ar/espacio-vecino-estacionamiento-restringido/','Que Pasa Web 13/05/2017: queja por estacionamiento restringido (zona Fondo de la Legua-Márquez, no costera)'),
     ('https://enelsubte.com/noticias/tren-de-la-costa-mejoran-la-frecuencia-en-fines-de-semana-y-feriados/','EnElSubte 12/2021: frecuencias TdlC fines de semana (dato viejo)'),
     ('https://wwwcronicaferroviaria.blogspot.com/2025/12/tren-de-la-costa-nuevo-cronograma-de.html','Crónica Ferroviaria 12/2025: reproduce aviso de Trenes Argentinos de nuevo cronograma TdlC desde 02/01/2026'),
     ('https://www.argentina.gob.ar/noticias/el-tren-de-la-costa-suma-frecuencias-y-ahora-circula-cada-20-minutos','Noticia oficial: devolvió 403/500, no se pudo leer'),
     ('https://www.lanacion.com.ar/sociedad/desde-el-sabado-cierra-por-50-dias-un-ramal-ferroviario-de-la-linea-mitre-nid06012026/','La Nación 06/01/2026 (vía resultado de búsqueda): cierre ramal Tigre 10/01-28/02/2026'),
     ('https://enelsubte.com/noticias/linea-mitre-desde-enero-el-ramal-tigre-estara-interrumpido-por-50-dias/','EnElSubte (vía resultado de búsqueda): ídem'),
     ('https://enelsubte.com/noticias/se-demora-el-retorno-del-tren-de-la-costa-continuara-suspendido-hasta-el-8-de-mayo-inclusive/','EnElSubte (vía resultado de búsqueda): suspensión TdlC abril-mayo 2026'),
     ('https://zonales.com/san-isidro-colectivos-recorridos-314-343-228-338/','Zonales (vía resultado de búsqueda): nuevos recorridos 228/314/338/343, junio 2026'),
     ('https://www.lanoticiaweb.com.ar/la-linea-228-absorberia-el-recorrido-de-la-ex-437-entre-san-isidro-boulogne-y-garin/','La Noticia Web (vía resultado de búsqueda): 228 absorbe ex 437'),
     ('https://datos.transporte.gob.ar/api/3/action/package_list','CKAN Secretaría de Transporte: 48 datasets; ninguno de pasajeros por estación ni GTFS'),
     ('https://datos.gob.ar/api/3/action/package_search?q=gtfs (y otras)','CKAN datos.gob.ar: sin GTFS ni pasajeros por estación'),
     ('https://catalogo.datos.gba.gob.ar/api/3/action/package_search?q=tmda|aforo|conteo vehicular|transito medio diario','CKAN Provincia de Buenos Aires: 0 resultados'),
     ('https://datos.transporte.gob.ar/api/3/action/package_show?id=tmda','TMDA 2017-18 sólo rutas nacionales (no calles costeras)'),
     ('https://archivos-datos.transporte.gob.ar/upload/Dat_Ab_Usos/dat-ab-usos-2026.csv y -2025.csv','Archivos completos de 52 y 65 MB: NO se descargaron enteros (regla de 20 MB); se tomaron sólo los días citados por HTTP Range'),
    ]: f.write(f'(no guardada) | - | {u} | {F} | {q}\n')
    f.write('\n# ARCHIVOS DEL PROYECTO LEÍDOS (sólo lectura, no copiados)\n')
    for p,q in [('scratchpad/ch/wt/informes/16_agua_y_costa.md (secc. 4)','ubicación de espacios costeros'),('scratchpad/ch/wt/informes/14_parques_y_costa.md','obras costeras'),
                ('scratchpad/ch/wt/informes/07_asuntos_hcd_2018_2021.csv','asuntos entrados HCD 2018-2021 (de órdenes del día https://hcd.sanisidro.gob.ar/)'),
                ('scratchpad/ch/wt/informes/08_asuntos_hcd_2024_2026.csv','asuntos entrados HCD 2024-2026'),('scratchpad/ch/wt/informes/06_presentaciones_hcd_san_isidro.csv','presentaciones HCD dic-2023/sep-2026 con estado (https://www.sanisidroabierto.com.ar/presentaciones)'),
                ('scratchpad/ch/wt/informes/05_resenas_app_reclamos.csv y 05_que_dicen_los_vecinos.md','reclamos vecinales'),
                ('scratchpad/em/01_raw/boletin_oficial/*.json.gz','índice TESI 2024-2026 (15.464 actos) y archivo 2002-2024 (37.132 actos)'),
                ('scratchpad/urbanismo_raw/u3_marco_legal/Ordenanza_Impositiva_2026-Nro_9415-2025_OCR.txt','Ordenanza Impositiva 2026, arts. 16, 37, 38 (URL: https://arsi.gob.ar/pdf/ordenanzas/Ordenanza_Impositiva_2026-Nro_9415-2025.pdf)'),
                ('scratchpad/ch/wt/01_raw/urbanismo/b_marco_legal/Ordenanza_Fiscal_2026-Nro_9414-2025_OCR.txt','Ordenanza Fiscal 2026, arts. 182-199 (URL: https://arsi.gob.ar/pdf/ordenanzas/Ordenanza_Fiscal_2026-Nro_9414-2025.pdf)'),
                ('scratchpad/pres_presupuesto_2025_msi.txt','Cálculo de recursos 2025 (URL: https://www.sanisidro.gob.ar/sites/default/files/img/presupuesto_2025_msi.pdf)'),
                ('scratchpad/ch/wt/01_raw/costa/a_basura/indice_novedades_sanisidro_2018-2026.tsv','índice de 3.884 notas municipales 2018-2026'),
                ('scratchpad/ch/wt/01_raw/agua/5_parques/work/plan_manejo_rn_2012.txt','Plan de Manejo Ribera Norte 2012 (sin datos de estacionamiento)')]:
        f.write(f'{p} | - | (archivo local) | {F} | {q}\n')
print(len(rows))
