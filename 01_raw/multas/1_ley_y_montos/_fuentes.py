import os,re,glob
B='/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/multas_raw/m1_ley_y_montos/'
NG='https://normas.gba.gob.ar'
IL='https://servicios.infoleg.gob.ar/infolegInternet/anexos/'
D='2026-10-02'
m={
'ngba_ley13927_ficha.html':(NG+'/ar-b/ley/2008/13927/2954','Ficha SINDMA de la Ley 13.927 (Código de Tránsito PBA): datos de publicación (BO 26041, 30/12/2008) y normas relacionadas'),
'ley13927_texto_actualizado.html':(NG+'/documentos/0YqDnfd0.html','Ley 13.927 texto actualizado (con Leyes 14246, 14331, 14393, 14774, 15002, 15078, 15139, 15143, 15225, 15321, 15402 y 15613)'),
'ley13927_texto_actualizado.txt':(NG+'/documentos/0YqDnfd0.html','Conversión a texto plano del archivo anterior'),
'ley13927_texto_original.pdf':(NG+'/documentos/VmKgeIdx.pdf','Ley 13.927 copia del texto original (PDF escaneado)'),
'ley13927_fundamentos.html':(NG+'/documentos/xqq5vfrx.html','Ley 13.927, página de fundamentos (casi vacía)'),
'ngba_ley15402_ficha.html':(NG+'/ar-b/ley/2023/15402/334888','Ficha SINDMA Ley 15.402 (alcohol cero; crea fondo PROSEVITRA), BO 29420 del 05/01/2023'),
'ley15402_texto_actualizado.html':(NG+'/documentos/VrlrpQhO.html','Ley 15.402 texto actualizado'),
'ley15402_texto_actualizado.txt':(NG+'/documentos/VrlrpQhO.html','Texto plano de la Ley 15.402'),
'ngba_dec532_09_ficha.html':(NG+'/ar-b/decreto/2009/532/36346','Ficha SINDMA Decreto 532/09 (reglamentación de la Ley 13.927)'),
'dec532_09_texto_actualizado.html':(NG+'/documentos/B3yPzhj0.html','Decreto 532/09 texto actualizado SINDMA (incluye Anexos I a V)'),
'dec532_09_texto_actualizado.txt':(NG+'/documentos/B3yPzhj0.html','Texto plano del Decreto 532/09'),
'dec532_09_anexoV_extracto.txt':(NG+'/documentos/B3yPzhj0.html','Extracto: Anexo V (Régimen general de contravenciones y sanciones) tal como figura en el texto actualizado SINDMA (OJO: no incorpora las sustituciones del Decreto 1350/18)'),
'ngba_ley15002_ficha.html':(NG+'/ar-b/ley/2018/15002/2461','Ficha SINDMA Ley 15.002 (modifica Ley 13.927: fotomultas, notificaciones)'),
'ngba_dec1350_18_ficha.html':(NG+'/ar-b/decreto/2018/1350/17729','Ficha SINDMA Decreto 1350/18 (modifica Decreto 532/09)'),
'dec1350_18_texto.html':(NG+'/documentos/0noe7uMx.html','Decreto 1350/18 texto (sustituye arts. 8,10,17,18,29,30,35,36,38,40 e incorpora art. 41 del Anexo V del Dec. 532/09; art. 33 Anexo I: UF y pago voluntario)'),
'dec1350_18_texto.txt':(NG+'/documentos/0noe7uMx.html','Texto plano del Decreto 1350/18'),
'ley24449_infoleg_texact.htm':(IL+'0-4999/818/texact.htm','Ley nacional 24.449 de Tránsito, texto actualizado InfoLEG (con notas sobre DNU 461/2025 rechazado y Decreto 627/2025)'),
'ley24449_infoleg_texact.txt':(IL+'0-4999/818/texact.htm','Texto plano de la Ley 24.449'),
'ley24449_argentinagob_actualizacion.html':('https://www.argentina.gob.ar/normativa/nacional/ley-24449-818/actualizacion','Ley 24.449 texto actualizado en argentina.gob.ar (copia de respaldo)'),
'dec779_95_infoleg_parte_dispositiva.htm':(IL+'30000-34999/30389/texact.htm','Decreto nacional 779/95 (reglamentación Ley 24.449), parte dispositiva e índice de anexos con modificaciones (Dec. 196/2025, 689/2026, 242/2022)'),
'dec779_95_infoleg_parte_dispositiva.txt':(IL+'30000-34999/30389/texact.htm','Texto plano del anterior'),
'dec779_95_anexo1_infoleg.htm':(IL+'30000-34999/30389/texactdto779-1995-anexo1.htm','Decreto 779/95 Anexo 1: reglamentación general (arts. 70, 83, 84, 85: UF nacional y pago voluntario 25%)'),
'dec779_95_anexo1_infoleg.txt':(IL+'30000-34999/30389/texactdto779-1995-anexo1.htm','Texto plano del anterior'),
'dec779_95_anexo2_infoleg.htm':(IL+'30000-34999/30389/texactdto779-1995-anexo2.htm','Decreto 779/95 Anexo 2 (texto según Dec. 242/2022): régimen nacional de sanciones en UF (para comparar)'),
'dec779_95_anexo2_infoleg.txt':(IL+'30000-34999/30389/texactdto779-1995-anexo2.htm','Texto plano del anterior'),
'infoleg_ficha_dec196_2025.htm':('https://servicios.infoleg.gob.ar/infolegInternet/verNorma.do?id=410682','Ficha InfoLEG del Decreto nacional 196/2025 (modifica reglamentación Ley 24.449; no toca multas)'),
'ngba_dl8751_77_ficha.html':(NG+'/ar-b/decreto-ley/1977/8751/1239','Ficha SINDMA Decreto-Ley 8751/77 (Código de Faltas Municipales)'),
'dl8751_77_texto_actualizado.html':(NG+'/documentos/DxaMGF4x.html','Código de Faltas Municipales, texto actualizado'),
'dl8751_77_texto_actualizado.txt':(NG+'/documentos/DxaMGF4x.html','Texto plano del anterior'),
'ngba_dl6769_58_ficha.html':(NG+'/ar-b/decreto-ley/1958/6769/1719','Ficha SINDMA Decreto-Ley 6769/58 (Ley Orgánica de las Municipalidades)'),
'dl6769_58_LOM_texto_actualizado.html':(NG+'/documentos/OVG48SW0.html','Ley Orgánica de las Municipalidades, texto actualizado'),
'dl6769_58_LOM_texto_actualizado.txt':(NG+'/documentos/OVG48SW0.html','Texto plano del anterior'),
'ngba_ley15170_ficha.html':(NG+'/ar-b/ley/2020/15170/209932','Ficha Ley 15.170 (Impositiva 2020); citada en nota del art. 32 de la Ley 13.927; no relevante para montos'),
'ngba_ley15225_ficha.html':(NG+'/ar-b/ley/2020/15225/222266','Ficha Ley 15.225 (Presupuesto 2021), que dio texto actual a los arts. 9, 43 y 44 de la Ley 13.927'),
'ngba_ley15561_ficha.html':(NG+'/ar-b/ley/2025/15561/555340','Ficha Ley 15.561 (Ley de Financiamiento, BO 23/12/2025)'),
'ley15561_texto.html':(NG+'/documentos/xDNvl7fy.html','Ley 15.561 texto: art. 13 afecta 10% de la parte provincial de multas de tránsito al Fondo Especial de Desarrollo Eléctrico (rutas)'),
'ley15561_texto.txt':(NG+'/documentos/xDNvl7fy.html','Texto plano del anterior'),
'infraccionesba_home.html':('https://infraccionesba.gba.gob.ar/','Portal provincial InfraccionesBA (Subsecretaría de Política y Seguridad Vial): inicio'),
'infraccionesba_unidad-fija-detalle.html':('https://infraccionesba.gba.gob.ar/unidad-fija-detalle','InfraccionesBA: valor actual de la UF ($2281,0) y acto que lo fija'),
'infraccionesba_preguntas-frecuentes.html':('https://infraccionesba.gba.gob.ar/preguntas-frecuentes','InfraccionesBA: preguntas frecuentes (pago voluntario 50%, plan de pagos, apremio)'),
'infraccionesba_equiposDeConstatacion.html':('https://infraccionesba.gba.gob.ar/equiposDeConstatacion','InfraccionesBA: mapa de equipos fijos en jurisdicción provincial ("252 equipos", según la página)'),
'infraccionesba_ubicacion-juzgado.html':('https://infraccionesba.gba.gob.ar/ubicacion-juzgado','InfraccionesBA: ubicación de juzgados'),
'infraccionesba_que-hago.html':('https://infraccionesba.gba.gob.ar/que-hago','InfraccionesBA: medios de pago y tabla de juzgados por jurisdicción'),
'valor_unidad_multa_pba_2023_2026.csv':('(elaboración propia a partir de los actos de uf_actos/)','ENTREGABLE: valor de la UF PBA ene-2023 a oct-2026, con acto, fuente y marca'),
'uf_pba_mensual_vs_ipc_2023_2026.csv':('(elaboración propia; IPC de ch/wt/data/ipc_indec_mensual.csv)','Serie mensual UF vs IPC INDEC, base ene-2023=100, UF en pesos de ene-2023 [cálculo propio]'),
'_h2t.py':('(script propio)','Conversor HTML a texto'),'_pdf2txt.py':('(script propio)','Conversor PDF a texto (pymupdf)'),
'_parse_res.py':('(script propio)','Parser de páginas de resultados de normas.gba.gob.ar'),'_get_actos.py':('(script propio)','Descarga fichas y PDF de actos de UF'),
'_get2.py':('(script propio)','Descarga fichas y PDF de otros actos'),'_build_csv.py':('(script propio)','Arma los dos CSV'),'_fuentes.py':('(script propio)','Arma este FUENTES.txt'),
# otros_actos
'otros_actos/disp1_2018_DPPSV_distribucion_ficha.html':(NG+'/ar-b/disposicion/2018/1/203169','Ficha Disposición 1/2018 DPPSV (distribución de multas según art. 42 Ley 13.927 salvo acuerdos complementarios)'),
'otros_actos/disp1_2018_DPPSV_distribucion_texto.html':(NG+'/documentos/BdarMXiD.html','Texto Disposición 1/2018 DPPSV'),
'otros_actos/disp1_2018_DPPSV_distribucion_texto.txt':(NG+'/documentos/BdarMXiD.html','Texto plano del anterior'),
'otros_actos/res601_2021_MIySP_convenio_sanisidro_ficha.html':(NG+'/ar-b/resolucion/2021/601/237962','Ficha Res. 601/2021 MIySP: aprueba Convenio Marco "Plan Integral de Seguridad Vial" DPPSV-Municipalidad de San Isidro'),
'otros_actos/res601_2021_MIySP_convenio_sanisidro_original.pdf':(NG+'/documentos/V9OPAotW.pdf','Res. 601/2021 MIySP (PDF)'),
'otros_actos/res601_2021_MIySP_convenio_sanisidro_original.txt':(NG+'/documentos/V9OPAotW.pdf','Texto del anterior'),
'otros_actos/res601_2021_anexo_convenio_marco_sanisidro.pdf':(NG+'/anexos/descargar/rBM49mxP.pdf','Anexo: CONVE-2021-07824452 Convenio Marco San Isidro (escaneado, 12 págs.; cláusula SEXTA: 80% municipio / 20% Provincia)'),
'otros_actos/res601_2021_anexo_convenio_marco_sanisidro.txt':(NG+'/anexos/descargar/rBM49mxP.pdf','Texto embebido (solo pie de página)'),
'otros_actos/res601_2021_anexo_convenio_marco_sanisidro_OCR.txt':(NG+'/anexos/descargar/rBM49mxP.pdf','OCR propio (tesseract spa) del convenio; verificado visualmente en cláusula SEXTA y fecha de firma'),
'otros_actos/convenio_sanisidro_recortes/p9_sexta.png':(NG+'/anexos/descargar/rBM49mxP.pdf','Recorte de la pág. 9 del convenio: cláusula SEXTA (80/20)'),
'otros_actos/convenio_sanisidro_recortes/p12_firma.png':(NG+'/anexos/descargar/rBM49mxP.pdf','Recorte de la pág. 12 del convenio: fecha de firma manuscrita ("01" de "octubre" de 2020, lectura probable)'),
'otros_actos/res200_2014_MJGM_convenio_sanisidro_ficha.html':(NG+'/ar-b/resolucion/2014/200/201947','Ficha Res. 200/2014 MJGM: convenio previo de seguridad vial con San Isidro (reemplazado por el de 2020/2021, cláusula OCTAVA)'),
'otros_actos/res200_2014_MJGM_convenio_sanisidro_original.pdf':(NG+'/documentos/B3zbk4i7.pdf','Res. 200/2014 (PDF escaneado, no leído en detalle)'),
'otros_actos/res200_2014_MJGM_convenio_sanisidro_original.txt':(NG+'/documentos/B3zbk4i7.pdf','Texto embebido (vacío)'),
'otros_actos/res200_2014_MJGM_convenio_sanisidro_texto.html':(NG+'/documentos/Bjb5eATy.html','Texto HTML (vacío)'),
'otros_actos/res200_2014_MJGM_convenio_sanisidro_texto.txt':(NG+'/documentos/Bjb5eATy.html','Texto plano (vacío)'),
'otros_actos/res67_2023_SSPySV_autoriza_sanisidro_ficha.html':(NG+'/ar-b/resolucion/2023/67/377330','Ficha Res. 67/2023 SSPySV: autoriza a San Isidro cinemómetros fijos en puntos determinados'),
'otros_actos/res67_2023_SSPySV_autoriza_sanisidro_original.pdf':(NG+'/documentos/0nOq4Zsr.pdf','Res. 67/2023 SSPySV (PDF)'),
'otros_actos/res67_2023_SSPySV_autoriza_sanisidro_original.txt':(NG+'/documentos/0nOq4Zsr.pdf','Texto del anterior'),
'otros_actos/disp32_2023_DPACTA_autoriza_sanisidro_ficha.html':(NG+'/ar-b/disposicion/2023/32/391943','Ficha Disp. 32/2023 DPAyCTA-MT: otra autorización de equipos a San Isidro'),
'otros_actos/disp32_2023_DPACTA_autoriza_sanisidro_original.pdf':(NG+'/documentos/Bgm5b2h3.pdf','Disp. 32/2023 (PDF)'),
'otros_actos/disp32_2023_DPACTA_autoriza_sanisidro_original.txt':(NG+'/documentos/Bgm5b2h3.pdf','Texto del anterior'),
'otros_actos/res566_2019_MG_acuerdo_SACIT_sannicolas_ficha.html':(NG+'/ar-b/resolucion/2019/566/205104','Ficha Res. 566/2019 MG: acuerdo SACIT con San Nicolás (modelo de comparación; no leído en detalle)'),
'otros_actos/res566_2019_MG_acuerdo_SACIT_sannicolas_original.pdf':(NG+'/documentos/BjbZQjhw.pdf','Res. 566/2019 (PDF)'),
'otros_actos/res566_2019_MG_acuerdo_SACIT_sannicolas_original.txt':(NG+'/documentos/BjbZQjhw.pdf','Texto del anterior'),
'otros_actos/res238_2016_MG_competencia_juzgados_ficha.html':(NG+'/ar-b/resolucion/2016/238/189203','Ficha Res. 238/2016 MG: competencia territorial de Juzgados Administrativos provinciales (Depto. San Isidro con asiento en Don Torcuato)'),
'otros_actos/res238_2016_MG_competencia_juzgados_texto.html':(NG+'/documentos/BjboL6Fy.html','Texto Res. 238/2016'),
'otros_actos/res238_2016_MG_competencia_juzgados_texto.txt':(NG+'/documentos/BjboL6Fy.html','Texto plano del anterior'),
'otros_actos/dec469_2024_PROSEVITRA_ficha.html':(NG+'/ar-b/decreto/2024/469/434501','Ficha Decreto 469/2024 (reglamenta PROSEVITRA)'),
'otros_actos/dec469_2024_PROSEVITRA_original.pdf':(NG+'/documentos/VryQeACG.pdf','Decreto 469/2024 (PDF)'),
'otros_actos/dec469_2024_PROSEVITRA_original.txt':(NG+'/documentos/VryQeACG.pdf','Texto del anterior'),
'otros_actos/dec114_2023_PROMEI_ficha.html':(NG+'/ar-b/decreto/2023/114/340127','Ficha Decreto 114/2023 (PROMEI)'),
'otros_actos/dec114_2023_PROMEI_original.pdf':(NG+'(PDF enlazado desde la ficha /ar-b/decreto/2023/114/340127)','Decreto 114/2023: art. 20, 10% de multas provinciales al PROMEI (art. 79 Ley 14.393 según Ley 15.310)'),
'otros_actos/dec114_2023_PROMEI_original.txt':(NG+'(idem)','Texto del anterior'),
'otros_actos/disp43_2021_DPPSV_procedimiento_equipos_ficha.html':(NG+'/ar-b/disposicion/2021/43/243098','Ficha Disp. 43/2021 DPPSV: Procedimiento de autorización de emplazamiento, uso y alta de equipos (v.2021)'),
'otros_actos/disp43_2021_DPPSV_procedimiento_equipos_original.pdf':(NG+'/documentos/VmRZEaHd.pdf','Disp. 43/2021 (PDF)'),
'otros_actos/disp43_2021_DPPSV_procedimiento_equipos_original.txt':(NG+'/documentos/VmRZEaHd.pdf','Texto del anterior'),
'otros_actos/disp43_2021_anexoI_procedimiento.pdf':(NG+'/anexos/descargar/D0Y68kxR.pdf','Anexo I de la Disp. 43/2021: procedimiento y formularios (municipal y provincial)'),
'otros_actos/disp43_2021_anexoI_procedimiento.txt':(NG+'/anexos/descargar/D0Y68kxR.pdf','Texto del anterior'),
'otros_actos/disp69_2020_DPPSV_plan_de_pagos_ficha.html':(NG+'/ar-b/disposicion/2020/69/222424','Ficha Disp. 69/2020 DPPSV: Plan de Pagos de regularización (90 días) para infracciones provinciales'),
'otros_actos/disp69_2020_DPPSV_plan_de_pagos_original.pdf':(NG+'/documentos/xAmyR7HR.pdf','Disp. 69/2020 (PDF)'),
'otros_actos/disp69_2020_DPPSV_plan_de_pagos_original.txt':(NG+'/documentos/xAmyR7HR.pdf','Texto del anterior'),
'otros_actos/disp26_2021_DPPSV_prorroga_plan_pagos_ficha.html':(NG+'/ar-b/disposicion/2021/26/233494','Ficha Disp. 26/2021 DPPSV: prórroga del plan de pagos'),
'otros_actos/disp26_2021_DPPSV_prorroga_plan_pagos_original.pdf':(NG+'/documentos/xk2aYJfR.pdf','Disp. 26/2021 (PDF)'),
'otros_actos/disp26_2021_DPPSV_prorroga_plan_pagos_original.txt':(NG+'/documentos/xk2aYJfR.pdf','Texto del anterior'),
}
# uf_actos: build from ficha
uf_urls={
'disp54_2022_DPACTA_MT':'/ar-b/disposicion/2022/54/334886','disp1_2023_DPACTA_MT':'/ar-b/disposicion/2023/1/334894','res11_2023_SSPySV_MT':'/ar-b/resolucion/2023/11/346080','res43_2023_SSPySV_MT':'/ar-b/resolucion/2023/43/357981','res53_2023_SSPySV_MT':'/ar-b/resolucion/2023/53/368480','res257_2023_MT':'/ar-b/resolucion/2023/257/382848','res335_2023_MT':'/ar-b/resolucion/2023/335/395435','res27B_2023_MT':'/ar-b/resolucion/2023/27b/406732','res63_2024_MT':'/ar-b/resolucion/2024/63/419500','res103_2024_MT':'/ar-b/resolucion/2024/103/430796','res146_2024_MT':'/ar-b/resolucion/2024/146/441333','res203_2024_MT':'/ar-b/resolucion/2024/203/454174','res259_2024_MT':'/ar-b/resolucion/2024/259/468108','res320_2024_MT':'/ar-b/resolucion/2024/320/480856','res2_2025_SSPySV_MT':'/ar-b/resolucion/2025/2/497163','res6_2025_SSPySV_MT':'/ar-b/resolucion/2025/6/509183','res7_2025_SSPySV_MT':'/ar-b/resolucion/2025/7/510165','res8_2025_SSPySV_MT':'/ar-b/resolucion/2025/8/519721','res9_2025_SSPySV_MT':'/ar-b/resolucion/2025/9/533427','res10_2025_SSPySV_MT':'/ar-b/resolucion/2025/10/547351','res11_2025_SSPySV_MT':'/ar-b/resolucion/2025/11/558040','res1_2026_SSPySV_MT':'/ar-b/resolucion/2026/1/571005','res2_2026_SSPySV_MT':'/ar-b/resolucion/2026/2/586425','res3_2026_SSPySV_MT':'/ar-b/resolucion/2026/3/602540','res4_2026_SSPySV_MT':'/ar-b/resolucion/2026/4/616499'}
for n,u in uf_urls.items():
    fich=open(B+f'uf_actos/{n}_ficha.html',encoding='utf-8',errors='ignore').read()
    pdf=re.findall(r'href="(/documentos/[^"]+\.pdf)"',fich)[0]
    m[f'uf_actos/{n}_ficha.html']=(NG+u,f'Ficha SINDMA del acto que fija el valor bimestral de la UF ({n})')
    m[f'uf_actos/{n}_original.pdf']=(NG+pdf,f'PDF firmado del acto {n} (valor de la UF)')
    m[f'uf_actos/{n}_original.txt']=(NG+pdf,f'Texto extraído del PDF {n}')
busq={'ngba_busqueda_UF_frase_unidades_fijas.html':'q[phrase]=Unidades Fijas, desde 01/01/2022','ngba_busqueda_UF_s1_1.html':'q[phrase]=valor bimestral, desde 01/10/2022','ngba_busqueda_UF_s2_1.html':'q[phrase]=Unidades Fijas, desde 01/10/2022','ngba_busqueda_UF_s3_1.html':'q[phrase]=Unidad Fija (p.1)','ngba_busqueda_UF_s3_2.html':'q[phrase]=Unidad Fija (p.2)','ngba_busqueda_UF_s4_1.html':'q[with_some_words]=UF UFs multas bimestral','ngba_busqueda_UF_s5_1.html':'q[phrase]=nafta de mayor octanaje','ngba_busqueda_art42_ley13927.html':'q[phrase]=artículo 42 de la Ley N° 13.927','ngba_busqueda_distribucion_ingreso_multa.html':'q[phrase]=distribución del ingreso por multa','ngba_busqueda_SACIT.html':'q[phrase]=SACIT','ngba_busqueda_municipalidad_san_isidro_p1.html':'q[phrase]=Municipalidad de San Isidro + palabras tránsito/infracciones (p.1)','ngba_busqueda_municipalidad_san_isidro_p2.html':'idem p.2','ngba_busqueda_2023plus_planes_pago.html':'q[phrase]=infracciones de tránsito + cuotas/plan de pagos, desde 2023','ngba_busqueda_2023plus_multas_infracciones.html':'q[phrase]=multas por infracciones de tránsito, desde 2023','ngba_busqueda_plan_de_pagos.html':'q[phrase]=plan de pagos + infracciones tránsito multas'}
for k,v in busq.items():
    m['busquedas/'+k]=(NG+'/resultados?'+v,'Página de resultados de búsqueda en normas.gba.gob.ar (GET): '+v)
out=['archivo | bytes | URL | fecha de consulta | qué es']
missing=[]
for root,dirs,files in os.walk(B):
    for f in sorted(files):
        p=os.path.relpath(os.path.join(root,f),B)
        if p=='FUENTES.txt': continue
        if p not in m: missing.append(p); continue
        u,d=m[p]
        out.append(f'{p} | {os.path.getsize(B+p)} | {u} | {D} | {d}')
out.append('')
out.append('PÁGINAS LEÍDAS Y NO GUARDADAS (consultadas 2026-10-02):')
for u,d in [
('https://www.lanacion.com.ar/sociedad/radares-bajo-sospecha-que-pasara-con-las-fotomultas-emitidas-por-equipos-sin-homologacion-y-por-que-nid28052026/','La Nación 28/05/2026: relevamiento ANSV de radares en rutas nacionales (526 autorizados, 152 sin autorización), fallo CSJN caso Darwin (Río Negro). Leída vía WebFetch.'),
('https://www.infobae.com/economia/2026/05/29/polemica-por-cientos-de-radares-de-velocidad-no-autorizados-que-hacer-si-se-recibe-una-fotomulta-de-uno-de-ellos/','Infobae 29/05/2026: mismo tema. WebFetch.'),
('https://diputadosbsas.com.ar/de-leo-terminar-negocio-fotomultas/','Nota 29/09/2026 sobre proyecto en Diputados PBA (Coalición Cívica) que modifica la Ley 13.927 (cinemómetros). WebFetch. Sin número de expediente.'),
('https://informenorte.com.ar/diputado-bonaerense-propone-regularizar-las-fotomultas-en-la-provincia/','Nota 30/09/2026 sobre el mismo proyecto. WebFetch.'),
('https://www.infoplatense.com.ar/multas-y-registro-proyecto-libertario-para-que-las-deudas-de-transito-dejen-de-bloquear-la-renovacion-en-la-provincia/','Nota 05/08/2026: proyecto en Diputados PBA (La Libertad Avanza) contra el "libre deuda" de multas para licencias. WebFetch.'),
('https://www.diariodemocracia.com/provinciales/336802-piden-informes-por-rarezas-en-el-cobro/','Nota 12/04/2026: pedido de informes en el Senado PBA sobre fotomultas. WebFetch.'),
('https://infocielo.com/politica-y-economia/un-senador-pone-la-lupa-las-fotomultas-n798724','Proyecto de un senador PBA (02/01/2025) sobre señalización de fotomultas. WebFetch devolvió 403; contenido solo por el resumen del buscador (El Día 04/01/2025, MDZ 27/01/2025, Minuto Neuquén 09/01/2025).'),
('https://www.eldia.com/nota/2025-1-4-2-43-37-un-proyecto-para-limitar-abusos-de-las-fotomultas-politica-y-economia','Solo visto en resultados de búsqueda (no abierta).'),
('https://hcdiputados-ba.gov.ar/index.php?alcance=0&numero=777&origen=D+++&page=proyectos&periodo=26-27&search=proyecto','Ficha de un proyecto D-777/26-27 (no relacionado: Ley 13.928 amparo). Se descartó. El buscador general de la HCD es un formulario POST: no se usó.'),
]:
    out.append(f'- {u} | {d}')
out.append('')
out.append('Búsquedas web (WebSearch) realizadas: (1) fotomultas rutas nacionales ANSV 2025; (2) proyecto de ley Legislatura bonaerense fotomultas 2025 Ley 13.927; (3) hcdiputados-ba.gov.ar cinemómetros 13927 2026; (4) fotomultas Senado bonaerense expediente 3000 metros.')
open(B+'FUENTES.txt','w').write('\n'.join(out)+'\n')
print('missing:',missing)
print(len(out))
