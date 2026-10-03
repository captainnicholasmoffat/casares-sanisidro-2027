import csv
base='/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/multas_raw/m1_ley_y_montos/'
NG='https://normas.gba.gob.ar'
# (desde, hasta, valor, acto, gde, bo_pub, bo_num, url_ficha, url_pdf, nota)
rows=[
('2023-01-01','2023-02-28',204.20,'Disposición 54/2022 DPAyCTA-MT, rectificada por Disposición 1/2023 DPAyCTA-MT (período enero-febrero 2023)','DISPO-2022-54 / DISPO-2023-1-GDEBA-DPAYCTAMTRAGP','05/01/2023','29420','/ar-b/disposicion/2022/54/334886 ; /ar-b/disposicion/2023/1/334894','/documentos/0vQNyvhz.pdf ; /documentos/xkdLvquR.pdf','La Disp. 54/2022 decía nov-dic 2022 por error; la Disp. 1/2023 la corrige a ene-feb 2023. Valor según ACA sede La Plata.'),
('2023-03-01','2023-04-30',229.50,'Resolución 11/2023 SSPySV-MT','RESO-2023-11-GDEBA-SSPYSVMTRAGP','06/03/2023','29460','/ar-b/resolucion/2023/11/346080','/documentos/0Pr3o9c7.pdf','Según ACA sede La Plata.'),
('2023-05-01','2023-06-30',256.80,'Resolución 43/2023 SSPySV-MT','RESO-2023-43-GDEBA-SSPYSVMTRAGP','05/05/2023','29500','/ar-b/resolucion/2023/43/357981','/documentos/B1Q6M5tz.pdf','Según ACA sede La Plata.'),
('2023-07-01','2023-08-31',290.10,'Resolución 53/2023 SSPySV-MT','RESO-2023-53-GDEBA-SSPYSVMTRAGP','04/07/2023','29538','/ar-b/resolucion/2023/53/368480','/documentos/0PrXXqh7.pdf','Según ACA sede La Plata.'),
('2023-09-01','2023-10-31',290.10,'Resolución 257/2023 MT (prórroga del valor de la Res. 53/2023)','RESO-2023-257-GDEBA-MTRAGP','05/09/2023','29582','/ar-b/resolucion/2023/257/382848','/documentos/BjNJqNuw.pdf','Prórroga: congelamiento nacional de combustibles hasta 31/10/2023 y límite de 6 dígitos del sistema de cobro del Banco Provincia (considerandos).'),
('2023-11-01','2023-12-31',290.10,'Resolución 335/2023 MT (segunda prórroga)','RESO-2023-335-GDEBA-MTRAGP','01/11/2023','29621','/ar-b/resolucion/2023/335/395435','/documentos/BO47LRCy.pdf','Mismos fundamentos que la Res. 257/2023.'),
('2024-01-01','2024-02-29',771.00,'Resolución 27 B/2023 MT','RESOB-2023-27-GDEBA-MTRAGP','02/01/2024','29661','/ar-b/resolucion/2023/27b/406732','/documentos/0XzvR6Hd.pdf','Vuelve a seguir el precio ACA La Plata ($771/litro según considerandos).'),
('2024-03-01','2024-04-30',1010.00,'Resolución 63/2024 MT','RESO-2024-63-GDEBA-MTRAGP','01/03/2024','29702','/ar-b/resolucion/2024/63/419500','/documentos/04zojzHN.pdf',''),
('2024-05-01','2024-06-30',1137.00,'Resolución 103/2024 MT','RESO-2024-103-GDEBA-MTRAGP','30/04/2024','29740','/ar-b/resolucion/2024/103/430796','/documentos/VWXWAlHY.pdf',''),
('2024-07-01','2024-08-31',1230.00,'Resolución 146/2024 MT','RESO-2024-146-GDEBA-MTRAGP','01/07/2024','29780','/ar-b/resolucion/2024/146/441333','/documentos/VR5DpQfy.pdf',''),
('2024-09-01','2024-10-31',1299.00,'Resolución 203/2024 MT','RESO-2024-203-GDEBA-MTRAGP','30/08/2024','29823','/ar-b/resolucion/2024/203/454174','/documentos/0ndR2ehr.pdf',''),
('2024-11-01','2024-12-31',1336.00,'Resolución 259/2024 MT','RESO-2024-259-GDEBA-MTRAGP','31/10/2024','29866','/ar-b/resolucion/2024/259/468108','/documentos/VWXJvlHY.pdf',''),
('2025-01-01','2025-02-28',1398.00,'Resolución 320/2024 MT','RESO-2024-320-GDEBA-MTRAGP','31/12/2024','29907','/ar-b/resolucion/2024/320/480856','/documentos/xqQD2Esj.pdf',''),
('2025-03-01','2025-04-30',1452.00,'Resolución 2/2025 SSPySV-MT','RESO-2025-2-GDEBA-SSPYSVMTRAGP','06/03/2025','29951','/ar-b/resolucion/2025/2/497163','/documentos/Bo71zQhl.pdf',''),
('2025-05-01','2025-05-05',1506.00,'Resolución 6/2025 SSPySV-MT','RESO-2025-6-GDEBA-SSPYSVMTRAGP','07/05/2025','29989','/ar-b/resolucion/2025/6/509183','/documentos/BKayMrfn.pdf','Rectificada desde el 06/05/2025 por la Res. 7/2025 (baja del precio ACA).'),
('2025-05-06','2025-06-30',1416.00,'Resolución 7/2025 SSPySV-MT (rectifica la Res. 6/2025)','RESO-2025-7-GDEBA-SSPYSVMTRAGP','12/05/2025','29992','/ar-b/resolucion/2025/7/510165','/documentos/Byv7ekil.pdf','ACA La Plata informó baja del precio a $1.416 (considerandos).'),
('2025-07-01','2025-08-31',1435.00,'Resolución 8/2025 SSPySV-MT','RESO-2025-8-GDEBA-SSPYSVMTRAGP','01/07/2025','30026','/ar-b/resolucion/2025/8/519721','/documentos/BydQ82Fl.pdf',''),
('2025-09-01','2025-10-31',1606.00,'Resolución 9/2025 SSPySV-MT','RESO-2025-9-GDEBA-SSPYSVMTRAGP','03/09/2025','30070','/ar-b/resolucion/2025/9/533427','/documentos/B71W9KCK.pdf',''),
('2025-11-01','2025-12-31',1711.00,'Resolución 10/2025 SSPySV-MT','RESO-2025-10-GDEBA-SSPYSVMTRAGP','05/11/2025','30114','/ar-b/resolucion/2025/10/547351','/documentos/056KZLFj.pdf',''),
('2026-01-01','2026-02-28',1807.00,'Resolución 11/2025 SSPySV-MT','RESO-2025-11-GDEBA-SSPYSVMTRAGP','06/01/2026','30153','/ar-b/resolucion/2025/11/558040','/documentos/xajEePt3.pdf',''),
('2026-03-01','2026-04-30',1896.00,'Resolución 1/2026 SSPySV-MT','RESO-2026-1-GDEBA-SSPYSVMTRAGP','04/03/2026','30192','/ar-b/resolucion/2026/1/571005','/documentos/VN34Pwi6.pdf',''),
('2026-05-01','2026-06-30',2215.00,'Resolución 2/2026 SSPySV-MT','RESO-2026-2-GDEBA-SSPYSVMTRAGP','06/05/2026','30232','/ar-b/resolucion/2026/2/586425','/documentos/BEQa1lun.pdf','ACA La Plata: $2.215/litro (considerandos).'),
('2026-07-01','2026-08-31',2271.00,'Resolución 3/2026 SSPySV-MT','RESO-2026-3-GDEBA-SSPYSVMTRAGP','03/07/2026','30272','/ar-b/resolucion/2026/3/602540','/documentos/xaGgeZc3.pdf',''),
('2026-09-01','2026-10-31',2281.00,'Resolución 4/2026 SSPySV-MT','RESO-2026-4-GDEBA-SSPYSVMTRAGP','03/09/2026','30313','/ar-b/resolucion/2026/4/616499','/documentos/0Y2rEOFv.pdf','Valor vigente al 02/10/2026; coincide con https://infraccionesba.gba.gob.ar/unidad-fija-detalle (consultado 02/10/2026).'),
]
with open(base+'valor_unidad_multa_pba_2023_2026.csv','w',newline='') as f:
    w=csv.writer(f)
    w.writerow(['fecha','valor_en_pesos','acto','fuente','marca'])
    for r in rows:
        fuente='; '.join(NG+u.strip() for u in r[7].split(';'))+' | PDF: '+'; '.join(NG+u.strip() for u in r[8].split(';'))+f' | BO PBA N° {r[6]} del {r[5]} | consultado 2026-10-02'
        acto=f'{r[3]} [{r[4]}]; vigencia {r[0]} a {r[1]}'+(f'. Nota: {r[9]}' if r[9] else '')
        w.writerow([r[0],f'{r[2]:.2f}',acto,fuente,'[verificado]'])
print(len(rows),'rows')
# monthly series
import datetime
ipc={}
for d in csv.DictReader(open('/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/ch/wt/data/ipc_indec_mensual.csv')):
    ipc[(int(d['anio']),int(d['mes']))]=float(d['indice'])
def val_at(y,m,day=1):
    dt=datetime.date(y,m,day)
    for r in rows:
        a=datetime.date.fromisoformat(r[0]); b=datetime.date.fromisoformat(r[1])
        if a<=dt<=b: return r[2],r[3].split(' (')[0]
mon=[]
y,m=2023,1
while (y,m)<=(2026,10):
    v,a=val_at(y,m,15)  # valor a mitad de mes (mayo 2025: $1416 desde el 6/5)
    i=ipc.get((y,m))
    mon.append((y,m,v,a,i))
    m+=1
    if m==13: y+=1;m=1
b_uf=mon[0][2]; b_ipc=mon[0][4]
with open(base+'uf_pba_mensual_vs_ipc_2023_2026.csv','w',newline='') as f:
    w=csv.writer(f)
    w.writerow(['anio_mes','uf_pesos_dia15','acto','indice_uf_ene2023_100','ipc_indec_indice','indice_ipc_ene2023_100','uf_real_pesos_de_ene2023','marca'])
    for (y,m,v,a,i) in mon:
        iu=v/b_uf*100
        if i:
            ii=i/b_ipc*100; real=v/(i/b_ipc)
            w.writerow([f'{y}-{m:02d}',f'{v:.2f}',a,f'{iu:.1f}',f'{i:.4f}',f'{ii:.1f}',f'{real:.2f}','[cálculo propio]'])
        else:
            w.writerow([f'{y}-{m:02d}',f'{v:.2f}',a,f'{iu:.1f}','','','','[cálculo propio] (IPC no disponible en el archivo)'])
for (y,m,v,a,i) in mon:
    if i: print(y,m,v,round(v/b_uf*100,1),round(i/b_ipc*100,1),round(v/(i/b_ipc),2))
    else: print(y,m,v,round(v/b_uf*100,1),'--')
