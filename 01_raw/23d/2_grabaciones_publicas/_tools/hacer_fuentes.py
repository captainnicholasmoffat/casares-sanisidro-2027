# Arma FUENTES.txt: una línea por archivo (archivo | bytes | URL | fecha de consulta | qué es). Uso: python3 -I hacer_fuentes.py
import os, re
D = '/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/c23d_raw/v2_grabaciones_publicas'
log = {}
for line in open(os.path.join(D, '_tools', 'bajadas.log'), encoding='utf-8'):
    p = [x.strip() for x in line.split('|')]
    if len(p) >= 5 and p[3] == '200':
        log[p[1]] = (p[4], p[0][:10])

desc = {
 'nac_ley27275_acceso_informacion_infoleg_texact.htm': 'Ley 27.275 de acceso a la información pública (texto actualizado): art. 1 principio de disociación; art. 7 sujetos (Nación); art. 8 i) y j) excepciones; arts. 32-34 transparencia activa; art. 36 invita a provincias',
 'nac_dec206_2017_reglamento_ley27275_infoleg.htm': 'Decreto 206/2017 reglamentario de la Ley 27.275: art. 8 inc. i) la excepción de datos personales no rige para datos relacionados con las funciones de los funcionarios públicos; prueba de daño',
 'nac_ccyc_ley26994_infoleg_texact.htm': 'Código Civil y Comercial (Ley 26.994) texto actualizado: arts. 52 (dignidad, imagen, intimidad), 53 (imagen y voz: consentimiento salvo actos públicos o interés general) y 1770 (vida privada)',
 'nac_ley26061_ninos_infoleg.htm': 'Ley 26.061 de protección integral de niñas, niños y adolescentes: art. 22 prohíbe difundir imágenes que los identifiquen contra su voluntad cuando lesionen su dignidad o su intimidad',
 'pba_ley15502_normasgba.html': 'Ley 15.502 de la Provincia de Buenos Aires: NO es de acceso a la información (declara personalidad destacada del deporte). Guardada para descartar la referencia',
 'pba_ley12475_normasgba.html': 'Ficha de la Ley 12.475 PBA (acceso a documentos administrativos) con normas relacionadas: Decreto 2549/2004 (reglamento) y Ley 14.214 (hábeas data)',
 'pba_ley12475_texto_actualizado.html': 'Ley 12.475 PBA, texto actualizado: interés legítimo, solicitud fundada, art. 6 deniega acceso si perjudica la privacidad de terceros',
 'pba_constitucion_provincial_normasgba.html': 'Página de normas.gba.gob.ar de la Constitución provincial (enlace al PDF)',
 'pba_constitucion_provincial_1994.pdf': 'Constitución de la Provincia de Buenos Aires 1994 (Boletín Oficial escaneado). El .txt es transcripción manual de la página 2 (OCR falló): arts. 12, 13, 20 inc. 3, 24 (allanamiento por autoridad municipal sólo para salubridad), 26, 27',
 'gcp_video_intelligence_precios.html': 'Google Cloud Video Intelligence API, precios por minuto: detección de rostros US$0,10 (0,09 y 0,08 con planes de ahorro), texto US$0,15, seguimiento de objetos US$0,15; primeros 1.000 min/mes gratis',
 'deface_README.md': 'deface (ORB-HD), README: anonimiza caras con CenterFace; opciones --scale, --thresh; GPU con onnxruntime-gpu; descarta el audio por defecto',
 'lic_deface_LICENSE.txt': 'Licencia de deface: MIT',
 'pypi_deface.json': 'PyPI, metadatos de deface: última versión 1.5.0 (15/10/2023), licencia MIT, dependencias',
 'aws_pricing_rekognition_us-east-1_index.json': 'AWS Price List API, Amazon Rekognition us-east-1 (publicado 11/09/2026): video archivado US$0,10 por minuto',
 'aws_pricing_rekognition_eu-west-1_index.json': 'AWS Price List API, Amazon Rekognition eu-west-1 (Irlanda): video archivado US$0,10 por minuto',
 'azure_retail_prices_video_indexer_westeurope.json': 'Azure Retail Prices API, Azure Video Indexer West Europe: Standard Video Indexing US$0,09/min, Video Modification (incluye redacción de caras) US$0,01/min, Basic 0,045, Advanced 0,15',
 'azure_retail_prices_video_indexer_brazilsouth.json': 'Azure Retail Prices API, Azure Video Indexer Brazil South: mismos precios',
 'azure_docs_video_indexer_face_redaction.html': 'Microsoft Learn: redacción de caras con Azure AI Video Indexer (requiere análisis Standard o Advanced; dos trabajos facturables; acceso a Face limitado por elegibilidad; incluir o excluir caras por ID)',
 'azure_precios_video_indexer_pagina.html': 'Página de precios de Azure Video Indexer: describe presets y que Video Modification incluye la redacción de caras (los importes cargan con JavaScript; se tomaron de la API)',
 'azure_retail_prices_vm_gpu_cpu_eastus.json': 'Azure Retail Prices API, máquinas virtuales East US: NC4as T4 v3 US$0,526/h, F16s v2 US$0,677/h, F4s v2 US$0,169/h (y spot)',
 'azure_retail_prices_vm_gpu_cpu_westeurope.json': 'Azure Retail Prices API, máquinas virtuales West Europe: NC4as T4 v3 US$0,658/h (spot 0,2925), F16s v2 US$0,776/h (spot 0,1434), F4s v2 US$0,194/h',
 'sighthound_redactor_precios.html': 'Sighthound Redactor, precios oficiales: Pro US$2.500/año (1 usuario, escritorio), Server US$3.500/año (+US$500 por usuario hasta 5), Enterprise a medida; detecta cabezas, personas, patentes, vehículos, documentos de identidad, pantallas y documentos; audio; local u offline; no cobra por minuto',
 'lic_centerface_LICENSE.txt': 'Licencia de CenterFace (detector que usa deface): MIT',
 'lic_egoblur_LICENSE.txt': 'Licencia de EgoBlur (Meta): Apache 2.0',
 'egoblur_README.md': 'EgoBlur README: modelos de caras y patentes; «The model is licensed under the Apache 2.0 license»; modelos se bajan del sitio de Project Aria',
 'lic_understandai_anonymizer_LICENSE.txt': 'Licencia de understand.ai anonymizer (caras y patentes): Apache 2.0',
 'lic_opencv_zoo_yunet_LICENSE.txt': 'Licencia del detector de caras YuNet (OpenCV Zoo): MIT',
 'insightface_README.md': 'InsightFace README: código MIT, pero los modelos entrenados son sólo para investigación no comercial (descartado)',
 'lic_ultralytics_LICENSE.txt': 'Licencia de Ultralytics YOLO: AGPL-3.0 (descartado por licencia)',
 'arxiv_2308.13093_egoblur_resumen.html': 'arXiv 2308.13093, resumen de EgoBlur: anonimiza caras y patentes en video de anteojos con cámara',
 'arxiv_1911.03599_centerface_resumen.html': 'arXiv 1911.03599, resumen de CenterFace: tiempo real en un núcleo de CPU a VGA; WIDER FACE Hard 0,875 (pierde caras difíciles)',
 'ogp_2023_ojos_en_alerta_ficha.pdf': 'Ficha de compromiso de gobierno abierto de la Ciudad de Mendoza (no San Martín) sobre el programa «Ojos en Alerta»',
 'prensa_lanacion_2018_ojos_en_alerta_san_martin.html': 'La Nación 2018: «Ojos en Alerta» nació en San Miguel (PBA); vecinos avisan por WhatsApp al centro de monitoreo [prensa]',
 'prensa_noticiasnqn_2025_ojos_en_alerta.html': 'NoticiasNQN 2025: «Ojos en Alerta» en casi 80 municipios; los demás usuarios no ven las alertas [prensa]',
 'uy_uaip_res2698_2026.pdf': 'Uruguay, UAIP Res. 98/026 (11/03/2026): revisa la reserva por 15 años de grabaciones de cámaras del Ministerio del Interior',
 'uy_uaip_res2589_2025.pdf': 'Uruguay, UAIP Res. 89/025 (02/07/2025): idem, grabación de cámaras de seguridad de un choque',
 'us_wa_rcw_42.56.240.html': 'Washington, RCW 42.56.240(14): pedidos de video de cámaras corporales (identificar persona, caso, fecha y lugar u oficial); presunciones de intimidad (interior de viviendas, salud, menores, etc.); cobro del costo de difuminar; 60 días de guarda',
 'us_seattle_spd_body_worn_video_pagina.html': 'Policía de Seattle, página del programa de cámaras corporales: aviso de grabación; consentimiento antes de entrar a una vivienda; qué se difumina y qué no (transeúntes en la vía pública no)',
 'us_seattle_spd_policy_bja.pdf': 'Manual de la Policía de Seattle 16.091, borrador del piloto (29/01/2014), copia en BJA: capacitación, uso, equipos sólo oficiales',
 'us_wa_mrsc_s42camera.pdf': 'Manual de la Policía de Seattle 16.091, piloto vigente desde 01/04/2015 (copia en MRSC): en viviendas se pide consentimiento para grabar y, si se niega, se deja de grabar; acuerdo con el sindicato policial; marcar videos con menores, salud, entrada a vivienda',
 'us_lapd_politica_publicacion_videos_incidentes_criticos_2018.html': 'LAPD, política de publicación de videos de incidentes críticos (2018): 45 días; difuminar caras e imágenes que identifiquen; proteger menores y víctimas; no publicar si no se puede difuminar',
 'us_wi_legislatura_ab837_testimonios_2024.pdf': 'Legislatura de Wisconsin, testimonios sobre AB 837 (31/01/2024): difuminar lleva 1,5 horas por hora de video',
 'prensa_fox6_wisconsin_costo_bodycam.html': 'FOX6 (Wisconsin): 1,5 h por hora de video; puesto de US$80.000/año sólo para difuminar [prensa]',
 'prensa_knpr_washoe_costo_redaccion_2020.html': 'KNPR (Nevada) 2020: el sheriff de Washoe tarda una hora por cada 10 minutos de video y propuso cobrar US$200 la hora [prensa]',
 'prensa_abogados_csjn_acordada29_2008.html': 'abogados.com.ar: Acordada CSJN 29/2008 sobre difusión de juicios orales (se transmiten inicio, alegatos y sentencia; no la prueba ni testimonios) [secundaria]',
 'uk_college_of_policing_app_imagenes_y_videos.html': 'College of Policing (Reino Unido), práctica profesional autorizada «Images and footage»: publicar video de cámaras corporales caso por caso; alternativa de verlo sin difundir (copia del sitio de producción; el principal dio 403)',
 'uk_merseyside_police_politica_bwv_v1.pdf': 'Policía de Merseyside, política de video corporal 2014: intrusión colateral y viviendas privadas',
 'us_scotus_camara_v_municipal_court_1967_lii.html': 'Corte Suprema de EE. UU., 387 U.S. 523 (1967): la inspección municipal de una vivienda sin consentimiento requiere orden (estándar administrativo)',
 'us_scotus_wilson_v_layne_1999_lii.html': 'Corte Suprema de EE. UU., 526 U.S. 603 (1999): llevar prensa o terceros a una vivienda durante un allanamiento viola la 4.a Enmienda',
 'tedh_44647-98_2003_sentencia.pdf': 'Tribunal Europeo de Derechos Humanos, demanda 44647/98, sentencia 28/01/2003: un municipio difundió video de sus cámaras sin difuminar a la persona; violación del art. 8',
 'csjn_fallos_306-1892_1984_texto_unlp.pdf': 'CSJN, Fallos 306:1892 (1984), texto alojado por la UNLP: el art. 19 CN protege la imagen; sólo por ley puede justificarse la intromisión',
 'mx_nl_congreso_2026-05_camaras_inspectores.html': 'Congreso de Nuevo León (México), mayo 2026: aprobó en primera vuelta cámaras corporales obligatorias para inspectores municipales; la parte inspeccionada puede pedir la grabación',
 'mx_nl_congreso_2026-08_camaras_inspectores.html': 'Congreso de Nuevo León, agosto 2026: iniciativa para que contralorías auditen videos al azar y sancionar la edición o el borrado',
 'prensa_tvn_panama_camaras_inspectores.html': 'TVN Panamá: el Municipio de Panamá da cámaras corporales a inspectores, monitoreadas en tiempo real [prensa]',
 'prensa_cnnchile_934_camaras_inspectores.html': 'CNN Chile: 934 cámaras corporales para inspectores municipales de la Región Metropolitana [prensa]',
 'us_fl_statute_119.071.html': 'Florida, Estatuto 119.071(2)(l): grabación de cámara corporal dentro de una vivienda privada, centro de salud o lugar privado es confidencial; se entrega a la persona grabada y al morador',
 'aaip_node443099.html': 'AAIP, 27/09/2024: Guía para un uso responsable de la inteligencia artificial (evaluación de impacto, explicabilidad); programa de la Res. 161/2023',
 'caba_ley2602_videocamaras_digesto.pdf': 'Ley 2602 de la Ciudad de Buenos Aires (videocámaras del Ejecutivo): no filmar interiores sin orden judicial; acceso restringido; prohibida la cesión; destrucción a los 60 días',
}
copias = {
 'copias_previas/ley25326_datos_personales_infoleg_texact.htm': ('https://servicios.infoleg.gob.ar/infolegInternet/anexos/60000-64999/64790/texact.htm', '2026-10-02/05 (repo)', 'Ley 25.326: arts. 1, 2, 4, 5, 6, 7.4, 9, 11, 12, 22, 44'),
 'copias_previas/dnpdp_disp10_2015_videovigilancia_texact.html': ('https://www.argentina.gob.ar/normativa/nacional/disposici%C3%B3n-10-2015-243335/actualizacion', '2026-10-02/05 (repo)', 'Disposición DNPDP 10/2015, Anexo I arts. 1 a 7 (art. 2: difusión al público)'),
 'copias_previas/aaip_res4_2019_anexoI.pdf': ('https://www.argentina.gob.ar/normativa/318874_res4AAIP_pdf/archivo', '2026-10-02/05 (repo)', 'AAIP Res. 4/2019 Anexo I: criterio 1 (acceso a imágenes, disociar a terceros), criterio 3 (persona determinable), criterio 5 (menores)'),
 'copias_previas/aaip_videovigilancia_responsables.html': ('https://www.argentina.gob.ar/aaip/datospersonales/responsables/videovigilancia', '2026-10-02/05 (repo)', 'AAIP: inscripción de bases de videovigilancia y contenido del manual'),
 'copias_previas/dl8751_77_codigo_faltas_municipales_normasgba.html': ('https://normas.gba.gob.ar/documentos/DxaMGF4x.html', '2026-10-02/05 (repo)', 'Decreto-Ley 8751/77: no tiene reglas de allanamiento ni de grabación'),
 'copias_previas/SI_digesto_1.50.2.1._Ordenanza_nº_5182_Codigo_Contravencional.pdf': ('https://boletines.sanisidro.gob.ar/digesto/ (rubro 1.50.2.1)', '2026-10-06 (Z2)', 'Ordenanza 5182 de San Isidro, Código Contravencional'),
 'copias_previas/caba_ley1217_procedimiento_faltas_juristeca.html': ('https://juristeca.jusbaires.gob.ar/compilacion-normativa-juristeca/ley-1217/', '2026-10-06 (Z2)', 'Ley 1217 de la Ciudad de Buenos Aires (procedimiento de faltas)'),
 'copias_previas/constitucion_nacional_infoleg.htm': ('https://servicios.infoleg.gob.ar/infolegInternet/anexos/0-4999/804/norma.htm', '2026-10-02', 'Constitución Nacional: arts. 18 y 19'),
 'copias_previas/dl6769_58_LOM_texto_actualizado.html': ('https://normas.gba.gob.ar/documentos/OVG48SW0.html', '2026-10-02', 'Ley Orgánica de las Municipalidades: art. 26 (ordenanzas pueden prever inspecciones y allanamientos según el art. 24 de la Constitución provincial) y art. 108 incs. 4, 5 y 18'),
 'copias_previas/SI_BO1235_Dec782-2026_Anexo_IF-2026-00262469.pdf': ('https://tesi.sanisidro.gob.ar/boletin/pdf/... (Boletín 1235, ver FUENTES de ruido_raw/x2)', '2026-10-05', 'Decreto 782/2026 de San Isidro, escala salarial julio 2026 (categorías 6 y 8, 40 h)'),
 'copias_previas/pba_ley13927_transito_normasgba.html': ('https://normas.gba.gob.ar/documentos/0YqDnfd0.html', '2026-10-02', 'Ley 13.927 PBA (tránsito): art. 32 g) se notifica al causante con copia del acta'),
}

out = []
for root, dirs, files in os.walk(D):
    dirs[:] = [x for x in dirs if x not in ('venv', 'ocr_cpba', '__pycache__')]
    for f in sorted(files):
        rel = os.path.relpath(os.path.join(root, f), D)
        if rel == 'FUENTES.txt':
            continue
        size = os.path.getsize(os.path.join(root, f))
        base = rel
        if rel.startswith('copias_previas/'):
            orig = re.sub(r'\.txt$', '', rel)
            for k, v in copias.items():
                if orig == k or orig + '.html' == k or orig + '.htm' == k or orig + '.pdf' == k or rel == k:
                    if rel == k:
                        out.append('%s | %d | %s | %s | COPIA de material previo: %s' % (rel, size, v[0], v[1], v[2]))
                    else:
                        out.append('%s | %d | (texto derivado de %s) | %s | texto extraído' % (rel, size, k, v[1]))
                    break
            else:
                out.append('%s | %d | (derivado) | - | texto extraído' % (rel, size))
            continue
        if rel.startswith('_tools/'):
            out.append('%s | %d | (propio) | 2026-10-07 | herramienta o salida propia' % (rel, size))
            continue
        b = re.sub(r'\.txt$', '', rel) if rel.endswith('.txt') and os.path.exists(os.path.join(D, re.sub(r'\.txt$', '', rel))) else None
        if b and b in log:
            out.append('%s | %d | (texto derivado de %s) | %s | texto extraído' % (rel, size, b, log[b][1]))
        elif rel in log:
            out.append('%s | %d | %s | %s | %s' % (rel, size, log[rel][0], log[rel][1], desc.get(rel, '(sin descripción)')))
        else:
            out.append('%s | %d | ? | ? | %s' % (rel, size, desc.get(rel, '(sin descripción)')))

extra = open(os.path.join(D, '_tools', 'fuentes_final.txt'), encoding='utf-8').read()
with open(os.path.join(D, 'FUENTES.txt'), 'w', encoding='utf-8') as fh:
    fh.write('FUENTES · V2 grabaciones públicas de inspecciones · consultado el 07/10/2026\n')
    fh.write('archivo | bytes | URL | fecha de consulta | qué es\n')
    fh.write('\n'.join(out) + '\n\n' + extra)
print(len(out), 'líneas')
