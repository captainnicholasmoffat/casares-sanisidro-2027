import os,sys
U=sys.argv[1]
H='2026-10-07'
NG='https://normas.gba.gob.ar'
E='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/19/{y}/{x} (mosaico)'
B='https://ecn.t{0-3}.tiles.virtualearth.net/tiles/a{quadkey}.jpeg?g=1 (mosaico)'
ADA='https://ada.gba.gov.ar/web_doc/resoluciones/'
M={
# ADA nuevo régimen
'ada/ADA_Res1746-25_RSC-2025-42185848-GDEBA-ADA.pdf':(ADA+'RSC-2025-42185848-GDEBA-ADA.pdf',H,'Res. ADA RESOC-2025-1746 (18/11/2025): nuevo régimen de prefactibilidad, aptitudes y permisos; DEROGA la Res. 2222/19 (art. 8)'),
'ada/ADA_Res1746-25_IF-2025-33228050-GDEBA-DLYEADA.pdf':(ADA+'IF-2025-33228050-GDEBA-DLYEADA.pdf',H,'Res. 1746/25 Anexo I: calificación hídrica; CHi3 hidráulica = lindero o atravesado por curso o cuerpo de agua'),
'ada/ADA_Res1746-25_IF-2025-33229276-GDEBA-DLYEADA.pdf':(ADA+'IF-2025-33229276-GDEBA-DLYEADA.pdf',H,'Res. 1746/25 Anexo II: procesos; Aptitud Hidráulica de Obra y documentación CHi3 (estudio hidrológico-hidráulico, contrato visado, capítulo EIA)'),
'ada/ADA_Res1746-25_IF-2025-33229664-GDEBA-DLYEADA.pdf':(ADA+'IF-2025-33229664-GDEBA-DLYEADA.pdf',H,'Res. 1746/25 Anexo IV: aptitudes y permisos especiales (no trata cauces ni flotantes)'),
'ada/ADA_Res1746-25_IF-2025-33229815-GDEBA-DLYEADA.pdf':(ADA+'IF-2025-33229815-GDEBA-DLYEADA.pdf',H,'Res. 1746/25 Anexo V: TASAS (CPH 100 l gasoil grado 3; Aptitud Hidráulica CHi2/3 1,8%; Constancia CHi2/3 1,5%)'),
'ada/ADA_Res1746-25_IF-2025-33229943-GDEBA-DLYEADA.pdf':(ADA+'IF-2025-33229943-GDEBA-DLYEADA.pdf',H,'Res. 1746/25 Anexo VI: formulario de migración de régimen'),
'ada/ADA_Res1746-25_IF-2025-42003218-GDEBA-DALADA.pdf':(ADA+'IF-2025-42003218-GDEBA-DALADA.pdf',H,'Res. 1746/25 Anexo III: formularios DDJJ inicial y resumen de proyecto'),
'ada/ada_guia-permiso-de-aptitud-hidraulica-de-obra.html':('https://ada.gba.gov.ar/guia-permiso-de-aptitud-hidraulica-de-obra/',H,'ADA: guía del Permiso de Aptitud Hidráulica de Obra (remite a Res. 1746/25)'),
'ada/ada_home.html':('https://ada.gba.gov.ar/',H,'ADA: página de inicio (enlaces a guías)'),
# normas
'normas/ADA_ResConj_320-2023_BMDZv2Ia.pdf':(NG+'/documentos/BMDZv2Ia.pdf',H,'Res. conj. ADA 320/2023: convenio de exención de tasas de la Res. 2222/19 para la Subsecretaría de Hábitat (muestra que un organismo público paga salvo convenio)'),
'normas/ADA_Res_338-2012_xk2OKpUA.html':(NG+'/documentos/xk2OKpUA.html',H,'Res. ADA 338/2012: tasas 3% + 4% para vuelco de efluentes (NO aplica a la barrera; régimen viejo)'),
'normas/ADA_Res_355-2015_B3zjwasj.html':(NG+'/documentos/B3zjwasj.html',H,'Res. ADA 355/2015: recupero de inspección 83 l gasoil (régimen anterior, superado)'),
'normas/ADA_Res_355-2015_ficha.html':(NG+'/ar-b/resolucion/2015/355/191702',H,'Ficha SINDMA de Res. ADA 355/2015'),
'normas/PBA_Dec_3233-2025_B3GR2Ahj.html':(NG+'/documentos/B3GR2Ahj.html',H,'Decreto PBA 3233/2025 (31/12/2025): canon por USO de agua (art. 43); no fija canon por ocupación de cauce'),
'normas/PBA_Dec_3233-2025_ficha.html':(NG+'/ar-b/decreto/2025/3233/568302',H,'Ficha SINDMA del Decreto 3233/2025'),
'normas/PBA_Ley15558_Impositiva2026_Bd5moXfD.html':(NG+'/documentos/Bd5moXfD.html',H,'Ley PBA 15.558, Impositiva 2026: UT=$275; art. 66 pto. 4.1 arancel EIA Ley 11.723 (1.484,90 UT + 5 por mil sobre el excedente de 20.000 UT); no hay tasas de la ADA'),
}
for q,ph in [('q_RESFC20192222GDEBAADA','RESFC-2019-2222-GDEBA-ADA'),('q_Resolucin222219','Resolución 2222/19'),('q_canonporocupacin','canon por ocupación'),('q_ley_impositiva_2026','Ley Impositiva para el ejercicio fiscal 2026'),('q_litrosdegasoil','litros de gasoil'),('q_ocupacindecauce','ocupación de cauce'),('q_permisoprecario','permiso precario'),('q_tasasAutoridaddelAgua','tasas Autoridad del Agua'),('q_tasasAutoridaddelAgua_p2','tasas Autoridad del Agua (pág. 2)')]:
    M['normas/'+q+'.html']=(NG+'/resultados?q[phrase]='+ph,H,'Búsqueda en normas.gba.gob.ar: «'+ph+'»')
M.update({
'guias/ITOPF_TIP03_Use_of_Booms_2011.pdf':('https://www.itopf.org/fileadmin/uploads/itopf/data/Documents/TIPS_TAPS_new/TIP_3_Use_of_Booms_in_Oil_Pollution_Response.pdf',H,'ITOPF TIP 3: fórmula de fuerza F=100·A·V², tabla de ángulos máximos según corriente, muertos de hormigón 3x la carga, amarres deslizantes para la marea'),
'osse/osse_2019-05-21_barco_optima_barrera.html':('https://www.osmgp.gov.ar/osse/desague-pluvial-arroyo-del-barco-optima-funcionalidad-de-la-reja-de-contencion-y-barrera-flotante-luego-de-las-primeras-lluvias-con-la-obra-finalizada/',H,'OSSE (21/05/2019): malla flotante de 140 m en PVC, encierro de la boca del Arroyo del Barco'),
'osse/osse_busqueda_barrera_flotante.html':('https://www.osmgp.gov.ar/osse/?s=barrera+flotante',H,'OSSE: búsqueda «barrera flotante» en su sitio'),
'precios_afuera/doee_dc_2009_bandalong_anacostia.html':('https://doee.dc.gov/release/fenty-unveils-first-western-hemisphere-trash-removal-system-anacostia-river',H,'DOEE Washington DC (2009): Bandalong en Watts Branch, unos US$55.000 instalado'),
'precios_afuera/connection_2020-05_little_hunting_creek_bandalong.html':('https://connectionnewspapers.com/news/2020/may/13/litter-trap-installed-little-hunting-creek',H,'Prensa (Fairfax County, 2020): trampa US$104.500; diseño, permisos, accesos y obra US$587.000; mantenimiento US$45.000/año (cita al condado)'),
'precios/ecoway_barreras_flotantes_products.json':('https://ecoway.com.ar/collections/barreras-flotantes/products.json?limit=250',H,'EcoWay: catálogo JSON con precios de lista por metro (BRV1014 $487.424; BRV1520 $980.089; BR1014 $432.393; BR1018 $458.598); «para aguas tranquilas»; IVA no informado'),
'precios/easy_cadena_galvanizada.json':('https://www.easy.com.ar/api/catalog_system/pub/products/search?ft=cadena%20galvanizada',H,'Easy (VTEX): cadenas galvanizadas por metro (máx. 7 mm)'),
'precios/easy_cadena_10mm_busqueda.json':('https://www.easy.com.ar/api/catalog_system/pub/products/search?ft=cadena%2010%20mm',H,'Easy: cadena galvanizada 7 mm x 1 m $19.930'),
'precios/easy_grillete_busqueda.json':('https://www.easy.com.ar/api/catalog_system/pub/products/search?ft=grillete',H,'Easy: grilletes (1/2" $4.360)'),
'precios/easy_cano_estructural_busqueda.json':('https://www.easy.com.ar/api/catalog_system/pub/products/search?ft=ca%C3%B1o%20estructural',H,'Easy: caño estructural 100x100x1,6 mm 3 m $64.190 (base del $/kg de acero)'),
'precios/se_precios_surtidor_vigentes.csv':('http://datos.energia.gob.ar/dataset/1c181390-5045-475e-94dc-410429be4b17/resource/80ac25de-a44a-4445-9215-090cf55cfda5/download/precios-en-surtidor-resolucin-3142016.csv',H,'Secretaría de Energía, precios en surtidor (Res. 314/2016), precios vigentes por estación con fecha'),
'precios/se_gasoil_g2_BA_por_mes.txt':('(cálculo propio sobre el CSV anterior)',H,'Mediana gasoil grado 2, provincia de Buenos Aires, por mes de vigencia (dic-25: $1.723)'),
'precios/se_gasoil_g3_por_mes.txt':('(cálculo propio sobre el CSV anterior)',H,'Mediana gasoil grado 3 (país y PBA) por mes de vigencia (dic-25: $1.972,5 país; $1.949 PBA)'),
'precios/se_precios_surtidor_resumen.txt':('(cálculo propio sobre el CSV anterior)',H,'Resumen por producto (todas las fechas mezcladas; no usar)'),
'osm/osm_map_peru.xml':('https://api.openstreetmap.org/api/0.6/map?bbox=-58.4980,-34.4760,-58.4860,-34.4660',H,'OSM (ODbL): datos alrededor de la boca de Perú; desagüe «Dardo Rocha» (culvert 5,9 km) termina en -34.47164,-58.49158; muelle 435902874'),
'osm/osm_map_altoperu.xml':('https://api.openstreetmap.org/api/0.6/map?bbox=-58.5280,-34.4560,-58.5120,-34.4440',H,'OSM (ODbL): Bajo de Beccar; calle de servicio «Dársena Gauto y Pavón» (way 64376475), Treinta y Tres Orientales, desagüe 1505789325'),
'osm/overpass_q_nombres_gauto.json':('https://overpass.private.coffee/api/interpreter (consulta name~Gauto|Dársena)',H,'Overpass: «Dársena Gauto y Pavón» es una calle de servicio (way 64376475)'),
'mapainv/_contacto_fotos.jpg':('(elaboración propia)',H,'Hoja de contacto de las 10 fotos oficiales de la obra Alto Perú'),
'mapainv/FOTOS.txt':('(elaboración propia)',H,'Descripción de las fotos de MapaInversiones'),
'img/IMAGENES.txt':('(elaboración propia)',H,'Descripción y mediciones de las imágenes satelitales'),
})
for i in range(1,11):
    M[f'mapainv/fotos_1003116908_{i}.jpg']=(f'https://mapainversiones.obraspublicas.gob.ar/Images/1003116908_{i}_XL093439.jpg',H,'Foto oficial obra «Desagües pluviales cuenca Alto Perú» (BAPIN 130705): túnel, sin la desembocadura')
for f,url,d in [('esri_z19_peru_boca.png',E,'Esri, boca de Perú, z19'),('esri_z19_peru_boca_zoom_grid5m.png',E,'Esri, boca de Perú, recorte con grilla de 5 m (medición del ancho)'),('bing_z19_peru_boca.png',B,'Bing, boca de Perú, z19'),('bing_z19_peru_boca_grid5m.png',B,'Bing, boca de Perú, grilla 5 m'),('esri_z18_altoperu_zona.png',E.replace('/19/','/18/'),'Esri, Bajo de Beccar z18: dársena y canal'),('esri_z18_altoperu_darsena_grid10m.png',E.replace('/19/','/18/'),'Esri, dársena con grilla de 10 m (medición del ancho)'),('esri_z19_altoperu_cabecera.png',E,'Esri, cabecera de la dársena z19'),('esri_z19_altoperu_cabecera_grid5m.png',E,'Esri, cabecera con grilla de 5 m'),('bing_z19_altoperu_cabecera.png',B,'Bing, cabecera (copas tapan el canal)'),('esri_z19_altoperu_osm_drain_sur.png',E,'Esri, desagüe OSM 1505789325 que llega a canal de barrio privado (segundo candidato)')]:
    M['img/'+f]=(url,H,d)
for q in ['barreradecontencinderesiduos','hincadodepilotes','muertodehormign','pilotesmetlicosmuelle']:
    M['sibom/q_'+q+'.html']=('https://sibom.slyt.gba.gob.ar/search?q[simple_query_string]=...',H,'Búsqueda SIBOM «'+q+'» (sin precios útiles)')
# copias (material previo reusado)
C={
'Ley_PBA_12257_Codigo_de_Aguas_texto_actualizado.html':('https://normas.gba.gob.ar/documentos/xbROJHGx.html','2026-09-29','Ley 12.257 (arts. 34, 43, 44, 102) — copia de ch/wt/01_raw/costa'),
'Resolucion_ADA_2222-2019_BgArqOc3.pdf':('https://normas.gba.gob.ar/documentos/BgArqOc3.pdf','2026-09-29','Res. ADA 2222/19 (DEROGADA por Res. 1746/25) — copia'),
'Decreto_PBA_8282-1987_consulta_riberas.html':('https://normas.gba.gob.ar/documentos/VJZOMqHJ.html','2026-09-29','Decreto 8282/87: consulta previa, 45 días, silencio = asentimiento — copia'),
'Ley_PBA_11723_texto_actualizado.html':('normas.gba.gob.ar (ver ch/wt/01_raw/costa/a_diagnostico/FUENTES.txt)','2026-09-29','Ley 11.723 arts. 10-19 y Anexo II — copia'),
'msi_aliviador_alto_peru_2026-04-06.html':('https://www.sanisidro.gob.ar/novedades/para-evitar-inundaciones-avanzan-los-trabajos-del-aliviador-alto-per%C3%BA','2026-09-29','Municipio (06/04/2026): traza hasta Dársena Gauto y Pavón — copia'),
'msi_alto_peru_cortes_2026-02-23.html':('https://www.sanisidro.gob.ar/novedades/avanza-la-obra-del-aliviador-alto-per%C3%BA-habr%C3%A1-cortes-y-desv%C3%ADos-en-el-bajo-de-beccar','2026-09-29','Municipio (23/02/2026): conductos hacia la desembocadura — copia'),
'msi_alto_peru_convenio_2021-02-26.html':('https://www.sanisidro.gob.ar/novedades/la-obra-hidraulica-que-beneficiara-los-vecinos','2026-09-29','Municipio (26/02/2021): 2.300 m, túnel 4,40 m y cajón 4,20 x 2,60 m — copia'),
'msi_alto_peru_primera_etapa_2023-12-05.html':('https://www.sanisidro.gob.ar/novedades/finalizo-la-primera-etapa-de-la-mega-obra-del-alto-peru','2026-09-29','Municipio (05/12/2023): 51,5 ha, más de 4 millones de litros por minuto — copia'),
'mapainversiones_desagues_cuenca_alto_peru.html':('https://mapainversiones.obraspublicas.gob.ar/Proyecto/PerfilProyecto/1003116908','2026-09-29','Ficha nacional BAPIN 130705: $7.018 M, 78,2%, desemboca por tramo existente del Colector Alto Perú — copia'),
'osm_desembocaduras_costa_san_isidro.csv':('OSM API + Nominatim (elaboración del repo)','2026-09-29','Puntos finales de desagües en la costa — copia'),
'lanacion_2007-01-08_demolieron_casa_reparto_canal_Peru_nid873557.html':('https://www.lanacion.com.ar/sociedad/demolieron-la-casa-del-reparto-de-dinero-nid873557/','2026-10-01','La Nación 2007: canal de 5,50 m, dos bocas de 3,20 x 3,20 m en Perú (sólo el dato técnico) — copia'),
'lanacion_2017-05-07_acassuso_costa_contaminada_nid2021344.html':('https://www.lanacion.com.ar/buenos-aires/acassuso-parte-de-su-costa-una-de-las-mas-contaminadas-del-rio-de-la-plata-nid2021344/','2026-10-01','La Nación 2017: comunicado del Municipio, «puente de madera que cruza el desagüe» — copia'),
'plan-de-manejo-ribera-norte.pdf':('https://www.losquesevan.com/archivos/plan-de-manejo-ribera-norte.pdf','2026-10-01','Plan de Manejo Ribera Norte 2012: tabla SHN de niveles por recurrencia; Proyecto 17 barrera en Perú — copia'),
'MY_JPS_MSMA_cap34_Gross_Pollutant_Traps.pdf':('https://www.water.gov.my/jps/resources/auto%20download%20images/58464d541b50e.pdf','2026-10-06','Malasia MSMA cap. 34: booms, holgura para marea, escape desde 1 m/s — copia'),
'fab_StormWaterSystems_Bandalong_pagina.html':('https://www.stormwatersystems.com/bandalong-litter-trap','2026-10-06','Bandalong: canal de 200 pies con 400 pies de brazos; pilotes de 35 pies; compuerta de marea; garantía 10 años — copia'),
'fab_StormWaterSystems_folleto.pdf':('https://cdn.prod.website-files.com/64f9e19ddf90ba1af22019d2/66bfaae48efe611b95db8875_StormWaterSystems%20Brochure_compressed.pdf','2026-10-06','Folleto Storm Water Systems: tamaños Bandalong — copia'),
'OSSE_barreras_flotantes_extractos.txt':('SIBOM, resoluciones OSSE (ver c23_raw/y4 FUENTES.txt)','2026-10-05','Extractos OSSE: CP 64/18, CD 66/2020, CP 67/21, CP 10/20, Res. 609/2026 — copia'),
'GP_OSSE_R595-617_2026_anexo_OCR.txt':('SIBOM General Pueyrredon 2026 (ver c23_raw/y4 FUENTES.txt)','2026-10-05','OCR del anexo con Res. OSSE 609/2026 (CP 87/26 NUMACO $36.960.000) — copia'),
'GP_OSSE_Res609-2026_p36.png':('SIBOM General Pueyrredon 2026','2026-10-05','Imagen de la página 36 (Res. 609/2026) — copia'),
'PLIEG-2026-51028121-APN-DGAACUMAR.pdf':('ACUMAR 318-0001-LPU26 (ver ch/wt/01_raw/costa)','2026-09-29','Pliego ACUMAR 2026: 200 m + 25% = 250 m de barrera, pollera hasta 1 m, francobordo 0,40 m, 10 m2 máx. — copia'),
'SI_DECRE-2025-1077_LP62-2024_anexos_precios.pdf':('boletín oficial San Isidro (ver c23_raw/y4 FUENTES.txt)','2026-10-05','San Isidro LP 62/2024: banco H°A° in situ $416.219,43/m3 (mar-25) — copia'),
'SI_DECRE-2025-124_LP60-2024_desobstruccion_pluviales.pdf':('boletín oficial San Isidro (ver c23b_raw/z1 FUENTES.txt)','2026-10-06','San Isidro LP 60/2024: $133.100 por hora de servicio con equipo — copia'),
'muni_2021-08-09_sudestada_2m80.html':('https://www.sanisidro.gob.ar (ver ch/wt/01_raw/costa FUENTES.txt)','2026-09-29','Municipio: sudestada 2,80 m (09/08/2021) — copia'),
'scielo_moreira_simionato_2019_RdlP_hydrology_circulation.html':('scielo (ver ch/wt/01_raw/costa FUENTES.txt)','2026-09-29','Moreira y Simionato 2019: M2 0,27 m en Buenos Aires; ondas de tormenta — copia'),
}
for k,v in C.items(): M['copias/'+k]=v
lines=[]
for root,dirs,files in os.walk(U):
    dirs.sort()
    for f in sorted(files):
        rel=os.path.relpath(os.path.join(root,f),U)
        if rel.startswith('_tools') or rel=='FUENTES.txt': continue
        size=os.path.getsize(os.path.join(root,f))
        base=rel[:-4] if rel.endswith('.txt') and rel[:-4] in M else rel
        if rel in M: url,fecha,que=M[rel]
        elif base in M and base!=rel: url,fecha,que=M[base][0],M[base][1],'Texto extraído de '+os.path.basename(base)
        else: url,fecha,que='?',H,'(sin descripción)'
        lines.append(f"{rel} | {size} | {url} | {fecha} | {que}")
open(os.path.join(U,'FUENTES.txt'),'w').write("archivo | bytes | URL | fecha de consulta | qué es\n"+"\n".join(lines)+"\n")
print(len(lines)); print("\n".join(l for l in lines if '(sin descripción)' in l))
