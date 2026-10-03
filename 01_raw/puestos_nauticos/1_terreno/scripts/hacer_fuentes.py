import os
D='/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/puestos_raw/d1_terreno/'
F='2026-10-03'
OSMAPI='https://api.openstreetmap.org/api/0.6/map?bbox='
E=[
# OSM
('osm/osmapi_1_aguila.osm',OSMAPI+'-58.4925,-34.4815,-58.4815,-34.4705','OpenStreetMap (ODbL), datos vivos API 0.6 alrededor del Parque del Águila. Primaria colaborativa, no oficial'),
('osm/osmapi_2_saenzpena.osm',OSMAPI+'-58.5035,-34.4700,-58.4925,-34.4590','OSM API 0.6 alrededor de Roque Sáenz Peña y el río'),
('osm/osmapi_3_centenera.osm',OSMAPI+'-58.5085,-34.4685,-58.4975,-34.4575','OSM API 0.6 alrededor del final de Del Barco Centenera'),
('osm/osmapi_4_puerto.osm',OSMAPI+'-58.5115,-34.4645,-58.5005,-34.4535','OSM API 0.6 alrededor de la dársena del Puerto de San Isidro'),
('osm/osmapi_5_33orientales.osm',OSMAPI+'-58.5240,-34.4565,-58.5130,-34.4455','OSM API 0.6 alrededor del Paseo 33 Orientales'),
('osm/osmapi_6_pacheco.osm',OSMAPI+'-58.4865,-34.4905,-58.4755,-34.4795','OSM API 0.6 alrededor de General Pacheco y el río'),
('osm/osmapi_rel_3623442_full.osm','https://api.openstreetmap.org/api/0.6/relation/3623442/full','OSM: espejo de agua leisure=marina (canal/dársenas del Puerto a 33 Orientales), 24,1 ha [cálculo propio]'),
('osm/osmapi_rel_10343661_full.osm','https://api.openstreetmap.org/api/0.6/relation/10343661/full','OSM: espejo de agua natural=water junto a Roque Sáenz Peña (5,9 ha), donde está el Muelle Público'),
('osm/osmapi_rel_6603491_full.osm','https://api.openstreetmap.org/api/0.6/relation/6603491/full','OSM: leisure=park "Paseo Público Costero" (Martínez)'),
('osm/osmapi_rel_10343663_full.osm','https://api.openstreetmap.org/api/0.6/relation/10343663/full','OSM: boundary=protected_area "Parque Natural Municipal Ribera Norte"'),
('osm/osmapi_rel_19648933_full.osm','https://api.openstreetmap.org/api/0.6/relation/19648933/full','OSM: leisure=park (Parque Público del Puerto, 3,3 ha en OSM)'),
('osm/nominatim/nominatim_Del_Barco_Centenera__San_Isidro__Buenos_Aires.json','https://nominatim.openstreetmap.org/search?q=Del Barco Centenera, San Isidro, Buenos Aires&format=jsonv2','Geocodificación OSM: calle Del Barco Centenera (Bajo de San Isidro)'),
('osm/nominatim/nominatim_Barco_Centenera__Martiinez__Buenos_Aires.json','https://nominatim.openstreetmap.org/search?q=Barco Centenera, Martínez, Buenos Aires&format=jsonv2','Geocodificación OSM: sin resultados (no hay Del Barco Centenera en Martínez)'),
('osm/nominatim/nominatim_Juan_Diiaz_de_Soliis__Martiinez__Buenos_Aires.json','https://nominatim.openstreetmap.org/search?q=Juan Díaz de Solís, Martínez, Buenos Aires&format=jsonv2','Geocodificación OSM: Juan Díaz de Solís en Martínez (sale de General Pacheco hacia el sur)'),
('osm/nominatim/nominatim_Juan_Diiaz_de_Soliis__San_Isidro__Buenos_Aires.json','https://nominatim.openstreetmap.org/search?q=Juan Díaz de Solís, San Isidro, Buenos Aires&format=jsonv2','Geocodificación OSM: Juan Díaz de Solís en Martínez y en Acassuso (Barrio Parque Aguirre)'),
# ARBA
('arba/arba_wfs_idera_capabilities.xml','https://geo.arba.gov.ar/geoserver/idera/wfs?service=WFS&version=1.0.0&request=GetCapabilities','ARBA: capacidades del WFS público idera (capas Parcela, Manzana, etc.)'),
]
for s,b in [('1_aguila','-58.4915,-34.4805,-58.4825,-34.4715'),('2_saenzpena','-58.5025,-34.4690,-58.4935,-34.4600'),('3_centenera','-58.5075,-34.4675,-58.4985,-34.4585'),('4_puerto','-58.5105,-34.4635,-58.5015,-34.4545'),('5_33orientales','-58.5230,-34.4555,-58.5140,-34.4465'),('6_pacheco','-58.4855,-34.4895,-58.4765,-34.4805')]:
    for L in ('Parcela','Manzana'):
        E.append((f'arba/arba_{L}_{s}.json',f'https://geo.arba.gov.ar/geoserver/idera/wfs?service=WFS&version=1.0.0&request=GetFeature&typeName=idera:{L}&outputFormat=application/json&srsName=EPSG:4326&bbox={b},EPSG:4326',f'ARBA catastro público (capa idera:{L}) alrededor del puesto {s}'))
E+=[
('ign/ign_geoserver_wms_capabilities.xml','https://imagenes.ign.gob.ar/geoserver/wms?service=WMS&request=GetCapabilities','IGN: capacidades WMS; existe el MDE 5 m "mde_5m_amba_1.3_2013" que cubre San Isidro, pero el WMS sólo devuelve colores y el WCS está deshabilitado: no se pudo leer la cota'),
# Municipio
('muni/muni_noticia196_modernizan_bombeo_bajo_sudestada.html','https://www.sanisidro.gob.ar/noticia/196','Municipio, 05/10/2016: albardón de 4.300 m y casi 5 m de alto, de Rondeau (Beccar, Colegio Marín) a Estación Las Barrancas; 6 estaciones de bombeo pluvial (España y Mitre; Leloir; Martín y Omar; Roque Sáenz Peña; Los Álamos)'),
('muni/muni_noticia236_sistema_hidraulico_respondio.html','https://www.sanisidro.gob.ar/noticia/236','Municipio, 20/10/2016: sudestada de 2,80 m sin anegamientos en el Bajo; compuertas que se cierran con río alto; estaciones España y Mitre, Chile, Leloir, Martín y Omar, R. Sáenz Peña, Los Álamos'),
('muni/muni_nueva_estacion_bombeo_bajo.html','https://www.sanisidro.gob.ar/novedades/nueva-estacion-de-bombeo-en-el-bajo-de-san-isidro','Municipio, 01/12/2023: nueva estación pluvial Discépolo y Héroes de Malvinas; descarga en la estación de Chile y el río'),
('muni/muni_recuperacion_6_estaciones_bombeo.html','https://www.sanisidro.gob.ar/novedades/avanza-la-recuperaci%C3%B3n-de-seis-estaciones-de-bombeo-para-prevenir-inundaciones','Municipio, 09/06/2026: puesta en valor de 6 estaciones (España, Chile, Leloir, Martín y Omar, Sáenz Peña, Los Álamos); relleno de sectores del albardón "por debajo del nivel adecuado"'),
('muni/muni_acceso_principal_parque_publico_puerto.html','https://www.sanisidro.gob.ar/novedades/se-inauguro-el-acceso-principal-del-parque-publico-del-puerto','Municipio, 16/08/2021: Parque Público del Puerto, 7 ha; "Contará con sanitarios"; calle nueva que bordea el parque para evitar autos dentro; rotonda Mitre-Primera Junta-Tiscornia'),
('muni/muni_noticia1096_parque_publico_puerto_banos.html','https://www.sanisidro.gob.ar/noticia/1096/en-el-puerto-de-san-isidro-avanza-la-creacion-del-parque-publico','Municipio, 20/09/2017: tablestacado del muelle; predio provincial de casi 7 ha cuya administración la Provincia transfirió al Municipio por acta'),
('muni/muni_noticia76_obras_puerto_libre_banos.html','https://www.sanisidro.gob.ar/noticia/76','Municipio, 01/09/2016: Puerto Libre (5 ha): baños para personas con discapacidad y 4 sanitarios con duchas'),
('muni/muni_renovacion_paseo_publico_costero.html','https://www.sanisidro.gob.ar/novedades/el-municipio-renueva-el-paseo-publico-costero','Municipio, 08/04/2021: puente peatonal y de bicicletas en Pacheco y el río; miradores Alvear y Paraná'),
('muni/muni_nautica.html','https://www.sanisidro.gob.ar/nautica','Municipio: página de Náutica (inscripción por Tramitador); no da lugares'),
('muni/muni_urbanismo_planointeractivo.html','https://www.sanisidro.gob.ar/urbanismo/planointeractivo','Municipio: enlace al plano interactivo de zonificación (gemelodigital.sanisidro.gob.ar), que no abrió (ver abajo)'),
# AySA
('aysa/aysa_2024-07_rehabilitacion_colector_cloacal_costanero.html','https://www.aysa.com.ar/usuarios/Novedades/2024/07/avanza_rehabilitacion_Colector_Cloacal_Costanero','AySA, julio 2024: el Colector Costanero "nace con otro nombre –Colector Ribereño– del lado de provincia, con un diámetro de 400 mm en San Isidro y atraviesa Vicente López". No da traza'),
# Normas
('normas/CCyC_Ley26994_arts_235_237_1960_1974_extracto_infoleg.txt','https://servicios.infoleg.gob.ar/infolegInternet/anexos/235000-239999/235975/texact.htm','Código Civil y Comercial (InfoLEG): arts. 235 (río y línea de ribera), 237, 1960 y 1974 (camino de sirga, 15 m). Extracto textual'),
('normas/normasgba_Res_MIVSP_705-2007_linea_de_ribera.html','https://normas.gba.gob.ar/documentos/VJJ42mHJ.html','Provincia: Res. 705/2007 (Infraestructura): procedimiento de la ADA para definir y demarcar la línea de ribera'),
# SHN y prensa
('shn/shn_AACRIOPLA_avisos_alertas_rio_de_la_plata.html','https://www.hidro.gov.ar/oceanografia/AACRIOPLA.asp','Servicio de Hidrografía Naval: avisos y alertas del Río de la Plata (03/10/2026: ninguno vigente)'),
('shn/shn_pronostico_mareologico_rio_de_la_plata.html','https://www.hidro.gov.ar/oceanografia/pronostico.asp','SHN: pronóstico mareológico 02-03/10/2026 (San Fernando, Buenos Aires, La Plata); alturas sobre el cero de las tablas, no IGN'),
('prensa/infobae_2026-01-08_sudestada_supero_3m.html','https://www.infobae.com/sociedad/2026/01/08/alerta-por-una-nueva-crecida-del-rio-de-la-plata-que-llevaria-el-nivel-del-agua-por-encima-de-los-3-metros/','Prensa (secundaria), 08/01/2026: según el mapa de Prefectura, en San Isidro el río subió hasta 3,40 m (San Fernando 2,90 m)'),
('prensa/infobae_2026-02-25_crecida_rio_de_la_plata_supero_3m.html','https://www.infobae.com/sociedad/2026/02/25/alerta-por-una-crecida-del-rio-de-la-plata-la-altura-supero-los-tres-metros-y-hubo-anegamientos-en-el-conurbano/','Prensa (secundaria), 25/02/2026: alerta del SHN; 3,10 m en La Plata y Buenos Aires; pico previsto 3,20 m en San Fernando'),
# Cálculos
('calculos/CALCULO_PROPIO_puestos_terreno.json','elaboración propia (scripts/analisis_puestos.py) con OSM, ARBA y Censo 2022','[cálculo propio] Por puesto: punto náutico, parcela ARBA, calles, playones, ciclovías, parques, baños OSM, locales, radios censales'),
('calculos/analisis_puestos_salida.txt','elaboración propia','[cálculo propio] Salida legible del script anterior'),
('calculos/CALCULO_PROPIO_anchos_via_publica_ARBA.csv','elaboración propia (scripts/anchos.py) con OSM + ARBA','[cálculo propio] Ancho de la vía pública entre parcelas ARBA (línea municipal a línea municipal), cada 10 m, y distancia del eje al canal'),
('calculos/CALCULO_PROPIO_distancias_lugares_candidatos.csv','elaboración propia (scripts/distancias_clave.py)','[cálculo propio] Distancia de cada calle/playón candidato al punto náutico y a la orilla OSM (franja de 15 m)'),
('calculos/CALCULO_PROPIO_poligono_Dec910-2012_Bosque_Alegre.geojson','elaboración propia con las 6 coordenadas del Dec. 910/2012 (repo: 01_raw/agua/5_parques/Ediciones-Extras-645-2012-04-01.pdf)','[cálculo propio] Polígono del Paisaje Protegido Bosque Alegre: 34.906 m2'),
]
for s in ('1_aguila','2_saenzpena','3_centenera','4_puerto','5_33orientales','6_pacheco'):
    E.append((f'mapas/mapa_{s}.png','elaboración propia (scripts/mapa.py) con OSM (ODbL) + ARBA',f'[cálculo propio] Mapa de trabajo del puesto {s}: punto náutico, franja de 15 m, parcelas del convenio'))
for f,d in [('scripts/osmlib.py','carga OSM y proyecta a UTM 21S'),('scripts/analisis_puestos.py','análisis por puesto'),('scripts/anchos.py','anchos entre parcelas'),('scripts/distancias_clave.py','distancias a lugares candidatos'),('scripts/mapa.py','mapas'),('scripts/calles.py','listado de calles cercanas'),('scripts/contiene.py','polígonos que contienen un punto'),('scripts/explorar.py','exploración de OSM'),('scripts/tiles_buscar.py','búsqueda en los tiles OSM del repo (solo lectura)'),('scripts/h2t.py','HTML a texto'),('scripts/get.sh','descarga con TLS verificado'),('scripts/ov.sh','consulta Overpass (falló, ver abajo)'),('scripts/hacer_fuentes.py','arma este archivo'),('scripts/fuentes_cola.txt','cola de este archivo (material del repo y consultas fallidas)'),('work/ov_r36.pem','certificado intermedio público Sectigo OV R36 (http://crt.sectigo.com/SectigoPublicServerAuthenticationCAOVR36.crt) para validar *.sanisidro.gob.ar; la verificación TLS siguió activa'),('work/dv_r36.pem','certificado intermedio público Sectigo DV R36 (http://crt.sectigo.com/SectigoPublicServerAuthenticationCADVR36.crt) para validar aysa.com.ar'),('work/ca_plus_ov_dv.pem','CA del proxy + los dos intermedios (herramienta)')]:
    E.append((f,'herramienta',d))
out=['# FUENTES · d1_terreno (puestos náuticos) · 03/10/2026','# archivo | bytes | URL | fecha de consulta | descripción','# Las páginas .html tienen al lado su .txt (texto extraído con scripts/h2t.py).','']
for f,u,d in E:
    p=D+f
    b=os.path.getsize(p) if os.path.exists(p) else 'NO EXISTE'
    out.append(f'{f} | {b} | {u} | {F} | {d}')
    t=p.rsplit('.',1)[0]+'.txt'
    if f.endswith('.html') and os.path.exists(t): out.append(f'{f.rsplit(".",1)[0]}.txt | {os.path.getsize(t)} | (texto de la anterior) | {F} | texto extraído')
out+=open(D+'scripts/fuentes_cola.txt').read().splitlines()
open(D+'FUENTES.txt','w').write('\n'.join(out)+'\n')
print('\n'.join(out[:5]),len(out))
