# -*- coding: utf-8 -*-
# Arma ../FUENTES.txt: una línea por archivo (archivo | bytes | URL | fecha de consulta | qué es),
# con lo bajado hoy (FUENTES_log.txt), las copias, las búsquedas, los scripts, y al final lo leído y no guardado y los errores.
import os
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def sz(f):
    return os.path.getsize(os.path.join(D, f)) if os.path.exists(os.path.join(D, f)) else 0

L = []
L.append('FUENTES · c23b_raw/z1_redes (redes y rejas en los desagües de la costa, sin que tapen ni inunden)')
L.append('Consulta: 06/10/2026. Nada pago, sin registros, sin contactar a nadie. El repo ch/wt sólo se leyó (lo copiado de ahí dice "copia").')
L.append('Formato: archivo | bytes | URL | fecha de consulta | qué es. Cada original va con su .txt al lado (pymupdf para PDF; HTML sin etiquetas).')
L.append('Montos: pesos de dic-2025 con ch/wt/data/ipc_indec_mensual.csv; dólar $1.274. Cuentas: _tools/calculo.py -> calculo.txt.')
L.append('')
L.append('== 1. DESCARGADO HOY (06/10/2026) ==')
for line in open(os.path.join(D, 'FUENTES_log.txt')):
    line = line.rstrip('\n')
    if line.strip():
        L.append(line + ' (+ .txt)')
L.append('')
L.append('== 2. COPIAS (de ch/wt/01_raw/costa/ o de c23_raw/y4_redes_desagues/; consultadas de nuevo el 06/10/2026, bajadas originalmente el 29/09 o el 05/10/2026) ==')
copias = [
 ('copias/muni_2026-09-08_el_nino_desembocaduras.html', 'https://www.sanisidro.gob.ar/novedades/el-ni%C3%B1o-se-refuerzan-los-operativos-de-prevenci%C3%B3n', 'Municipio de San Isidro, 08/09/2026: plan El Niño; limpieza de más de 4.300 sumideros y conductos y más de 540 m de desembocaduras (según el Municipio). Copia de ch/wt/01_raw/costa/a_basura/'),
 ('copias/muni_2021-08-09_sudestada_2m80.html', 'https://www.sanisidro.gob.ar/novedades/nuevamente-el-sistema-hidraulico-evito-inundaciones', 'Municipio de San Isidro, 09/08/2021: sudestada con pico de 2,80 m, 42 mm de lluvia, 8 bombas (según el Municipio). Copia del repo'),
 ('copias/osm_desembocaduras_costa_san_isidro.csv', 'https://api.openstreetmap.org/api/0.6/map (recortes) + nominatim', 'Elaboración del repo con OpenStreetMap: 14 puntos finales de desagües en la costa, sin medidas. Copia del repo'),
 ('copias/PLIEG-2026-51028121-APN-DGAACUMAR.pdf', 'https://www.acumar.gob.ar/wp-content/uploads/2026/05/PLIEG-2026-51028121-APN-DGAACUMAR.pdf', 'ACUMAR, pliego LP 318-0001-LPU26: barreras de 250 m (pollera hasta 1 m, francobordo 0,40 m), "no deberán contener más de 10 m2 de residuos acumulados". Copia del repo'),
 ('copias/Marin_MCSTOPPP_2022_pp7-10_25_48-49.pdf', 'https://eoainc.com/trash_impracticability/Appendix_B-12_-_MCSTOPPP_FTC_FeasibilityStudy_June22.pdf', 'Marin County (Schaaf & Wheeler, jun-2022), páginas 7-10, 25, 48-49: costos unitarios (red US$2.500/pie3/s, separador US$3.000/pie3/s, connector pipe screen US$2.500), reja con vertedero de 6 pulgadas "para evitar inundaciones", desenganche rápido "para prevenir inundaciones", criterios de captura total de California. Extracto propio del PDF del repo'),
 ('copias/SI_DECRE-2025-1077_LP62-2024_anexos_precios.pdf', 'https://tesi.sanisidro.gob.ar/nfs-storage/gde/v2/gde_1758140813.pdf', 'San Isidro, Decreto 1077/2025, LP 62/2024: precios unitarios redeterminados al 01/03/2025 (reja, hormigón, excavación, jornal). Copia de c23_raw/y4'),
 ('copias/SI_DECRE-2024-1238_Volmat_camion_hora.pdf', 'https://tesi.sanisidro.gob.ar/nfs-storage/gde/v2/gde_1726157343.pdf', 'San Isidro, Decreto 1238/2024: camión volcador 5 m3 con chofer $33.114/h. Copia de c23_raw/y4'),
 ('copias/SI_BO1235_Dec782-2026_Anexo_IF-2026-00262469.pdf', 'https://tesi.sanisidro.gob.ar/boletin/pdf/eyJpdiI6IkdaSHcwaFltUjRUQ015M0tBYlFaYlE9PSIs... (URL completa en c23_raw/y4_redes_desagues/FUENTES.txt)', 'San Isidro, anexo del Decreto 782/2026: escala salarial de obreros desde jul-2026. Copia de c23_raw/y4'),
 ('copias/SI_Ord9415_Impositiva2026_p4_art3_tasas_camion_peon.pdf', 'https://arsi.gob.ar/pdf/ordenanzas/Ordenanza_Impositiva_2026-Nro_9415-2025.pdf (página 4)', 'San Isidro, Ordenanza Impositiva 2026, art. 3 b): hora de camión $135.400, peón $12.070. Copia de c23_raw/y4'),
 ('copias/lanus_servicio_limpieza_desagues_pliego.pdf', 'https://www.lanus.gob.ar/documentos-oficiales/1161/servicio-integral-de-limpieza-de-desagues-pluviales-del-distrito/descargar', 'Lanús, pliego del servicio integral de limpieza de desagües pluviales. Copia de c23_raw/y4'),
 ('copias/ecoway_barrera-flotante-tipo-valla-por-metro-brv1014.js', 'https://ecoway.com.ar/products/barrera-flotante-tipo-valla-por-metro-brv1014.js', 'EcoWay (Argentina): precio de lista por metro, barrera BRV1014. Copia de c23_raw/y4'),
 ('copias/ecoway_barrera-flotante-tipo-valla-por-metro-brv1520.js', 'https://ecoway.com.ar/products/barrera-flotante-tipo-valla-por-metro-brv1520.js', 'EcoWay (Argentina): precio de lista por metro, barrera BRV1520. Copia de c23_raw/y4'),
 ('copias/OSSE_barreras_flotantes_extractos.txt', 'https://sibom.slyt.gba.gob.ar/bulletins/2300/contents/1335926 y otros (ver c23_raw/y4_redes_desagues/FUENTES.txt)', 'OSSE Mar del Plata: extractos de resoluciones sobre barreras flotantes 2018-2026 (precios, "tramos muy deteriorados"). Copia de c23_raw/y4'),
 ('copias/osse_mdp_arroyo_del_barco_reja.html', 'https://www.osmgp.gov.ar/osse/desague-pluvial-arroyo-del-barco-marcada-efectividad-de-la-reja-de-contencion-de-residuos/', 'OSSE Mar del Plata, 18/06/2019: reja de contención en la desembocadura del Arroyo del Barco, limpieza con herramientas de mano y camiones después de cada lluvia. Copia de c23_raw/y4'),
 ('copias/sannicolas_2026-07_barreras_desagues.html', 'https://www.opinandosannicolas.ar/2026/07/san-nicolas-instalaron-barreras-en-desagues-pluviales-y-evitaron-que-mas-de-350-kilos-de-residuos-llegaran-al-rio/', 'San Nicolás, jul-2026: rejas y barreras en 4 desagües, 350 kg en 2 meses (prensa). Copia de c23_raw/y4'),
 ('copias/parana_2025-09_barrera_antonico.html', 'https://www.miradorprovincial.com/2025/09/17/colocaron-una-barrera-de-contencion-de-residuos-y-limpiaron-el-arroyo-antonico/', 'Paraná, sep-2025: barrera en el arroyo Antoñico, vaciado cada 10 días (prensa). Copia de c23_raw/y4'),
 ('copias/comirec_nuevas_barreras_tigre.html', 'https://www.gba.gob.ar/comirec/noticias/nuevas_barreras_de_contenci%C3%B3n_de_residuos_en_tigre', 'COMIREC, 27/07/2020: reposición de barreras de contención en Tigre (Larralde y El Taurita) por convenio con CEAMSE. Copia del repo'),
 ('copias/noticiasambientales_tigre_barreras_reconquista.html', 'https://noticiasambientales.com/medio-ambiente/tigre-pide-reponer-las-barreras-del-rio-reconquista-para-cuidar-la-naturaleza-y-el-deporte-local-de-la-basura/', 'Noticias Ambientales, 14/05/2025: Tigre pide reponer las mangas flotantes retiradas en la Pista Nacional de Remo (prensa). Copia del repo'),
 ('copias/letrap_2020-07-02_ceamse_flotantes_reconquista.html', 'https://www.letrap.com.ar/nota/2020-7-2-11-20-0-ceamse-continua-con-la-recoleccion-de-residuos-flotantes-del-rio-reconquista', 'Letra P, 02/07/2020: CEAMSE retira más de 150.000 kg por mes de flotantes del Reconquista (prensa). Copia del repo'),
 ('copias/scielo_moreira_simionato_2019_RdlP_hydrology_circulation.html', 'https://www.scielo.org.ar/scielo.php?script=sci_arttext&pid=S1850-468X2019000100001', 'Moreira y Simionato (2019), Meteorologica: Río de la Plata micromareal, marea media 0,6 m y máxima 1 m en Buenos Aires; sudestada récord 4,44 m (1940); ondas de tormenta varias veces por año. Copia del repo'),
]
for f, u, q in copias:
    L.append(f'{f} | {sz(f)} | {u} | 2026-10-06 (copia) | {q} (+ .txt)')
L.append('')
L.append('== 3. BÚSQUEDAS GUARDADAS ==')
for f in sorted(os.listdir(os.path.join(D, 'sibom'))):
    if f.startswith('q_') and f.endswith('.html'):
        L.append(f'sibom/{f} | {sz("sibom/"+f)} | https://sibom.slyt.gba.gob.ar/search?q[simple_query_string]=... (consulta en el nombre; ver _tools/sibom_search.py) | 2026-10-06 | Búsqueda en SIBOM (boletines municipales bonaerenses)')
L.append(f'_bo_busquedas_z1.txt | {sz("_bo_busquedas_z1.txt")} | https://tesi.sanisidro.gob.ar/boletin (búsqueda Livewire con _tools/bo_buscar.py) | 2026-10-06 | Boletín de San Isidro: "cooperativa de trabajo", "hidrocinético", "sumideros" (sin resultados), "conductos pluviales"')
L.append(f'_tools/_bo_full.txt | {sz("_tools/_bo_full.txt")} | ídem | 2026-10-06 | Salida completa de las búsquedas anteriores (los enlaces GDE de los decretos se tomaron de c23b_raw/z4a y agua_raw/w1 del scratchpad, índices propios previos)')
L.append('')
L.append('== 4. CUENTAS Y SCRIPTS ==')
L.append(f'calculo.txt | {sz("calculo.txt")} | (propio) | 2026-10-06 | Salida de _tools/calculo.py [cálculo propio]')
for f in ['calculo.py', 'get.py', 'grep.py', 'sibom_search.py', 'bo_buscar.py', 'hacer_fuentes.py', '_ca_combo.pem']:
    L.append(f'_tools/{f} | {sz("_tools/"+f)} | (propio) | 2026-10-06 | ' + {
        'calculo.py': 'Cuentas de instalación y operación (pesos de dic-2025)',
        'get.py': 'Descarga con curl (verificación TLS activa), extrae .txt y anota en FUENTES_log.txt',
        'grep.py': 'Búsqueda de pasajes en los .txt',
        'sibom_search.py': 'Búsqueda en SIBOM (copia del script de c23_raw/y4)',
        'bo_buscar.py': 'Búsqueda en el Boletín de San Isidro (copia del script de c23_raw/y4)',
        'hacer_fuentes.py': 'Arma este FUENTES.txt',
        '_ca_combo.pem': 'Certificados públicos: sistema + intermedio de sanisidro.gob.ar (puestos_raw/d1_terreno/work/ca_plus_ov_dv.pem) + proxy (/root/.ccr/ca-bundle.crt); no se desactivó la verificación TLS'}[f])
L.append('FUENTES_log.txt y _errores_log.txt | - | (propio) | 2026-10-06 | Registros de descarga y de errores que alimentan este archivo')
L.append('')
L.append('== 5. LEÍDO Y NO GUARDADO ==')
L.append('- Resultados del buscador web (no se guardan): EA trash screen guide; "Section 19 flood investigation trash screen"; Melbourne Water GPT; EPA trash capture; "reja tapada basura entubamiento"; canastos en sumideros Argentina; Ludueña; CABA sumideros. Sirvieron sólo para encontrar URL.')
L.append('- Bloxham (Oxfordshire), informe Sección 19 de 2025: según el resumen del buscador, una reja de alcantarilla tapada agravó la inundación de hasta 35 viviendas el 24/11/2024. No pude abrir el PDF (captcha) ni con la herramienta de lectura web: [sin confirmar].')
L.append('- Chester (Storm Christoph) y Rutland (Barleythorpe Brook): sólo el resumen del buscador menciona rejas de alcantarilla a revisar. No abiertos: [sin confirmar].')
L.append('- CIRIA C786 "Culvert, screen and outfall manual" (2019), que reemplazó a la guía de la Environment Agency: es de pago o pide registro; no se abrió.')
L.append('- Fresh Creek / StormTrap "Netting TrashTrap": el sitio redirige a stormtrap.com y devuelve 403.')
L.append('- Lista 2025 de dispositivos certificados de California (waterboards.ca.gov): 404. Se usó el extracto de la lista 2021 que trae el estudio de Marin.')
L.append('')
L.append('== 6. ERRORES ==')
for line in open(os.path.join(D, '_errores_log.txt')):
    if line.strip():
        L.append(line.rstrip('\n'))
L.append('Nota: el primer intento de sibom/CArecco_Dec1438-2026_zanjas.html falló (conexión cortada); el segundo intento funcionó y está guardado.')
open(os.path.join(D, 'FUENTES.txt'), 'w').write('\n'.join(L) + '\n')
print('\n'.join(L))
