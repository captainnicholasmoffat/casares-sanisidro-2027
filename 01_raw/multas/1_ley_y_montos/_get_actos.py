import re,subprocess,os,html,sys
urls="""/ar-b/disposicion/2022/54/334886 disp54_2022_DPACTA_MT
/ar-b/disposicion/2023/1/334894 disp1_2023_DPACTA_MT
/ar-b/resolucion/2023/11/346080 res11_2023_SSPySV_MT
/ar-b/resolucion/2023/43/357981 res43_2023_SSPySV_MT
/ar-b/resolucion/2023/53/368480 res53_2023_SSPySV_MT
/ar-b/resolucion/2023/257/382848 res257_2023_MT
/ar-b/resolucion/2023/335/395435 res335_2023_MT
/ar-b/resolucion/2023/27b/406732 res27B_2023_MT
/ar-b/resolucion/2024/63/419500 res63_2024_MT
/ar-b/resolucion/2024/103/430796 res103_2024_MT
/ar-b/resolucion/2024/146/441333 res146_2024_MT
/ar-b/resolucion/2024/203/454174 res203_2024_MT
/ar-b/resolucion/2024/259/468108 res259_2024_MT
/ar-b/resolucion/2024/320/480856 res320_2024_MT
/ar-b/resolucion/2025/2/497163 res2_2025_SSPySV_MT
/ar-b/resolucion/2025/6/509183 res6_2025_SSPySV_MT
/ar-b/resolucion/2025/7/510165 res7_2025_SSPySV_MT
/ar-b/resolucion/2025/8/519721 res8_2025_SSPySV_MT
/ar-b/resolucion/2025/9/533427 res9_2025_SSPySV_MT
/ar-b/resolucion/2025/10/547351 res10_2025_SSPySV_MT
/ar-b/resolucion/2025/11/558040 res11_2025_SSPySV_MT
/ar-b/resolucion/2026/1/571005 res1_2026_SSPySV_MT
/ar-b/resolucion/2026/2/586425 res2_2026_SSPySV_MT
/ar-b/resolucion/2026/3/602540 res3_2026_SSPySV_MT
/ar-b/resolucion/2026/4/616499 res4_2026_SSPySV_MT"""
for line in urls.splitlines():
    u,name=line.split()
    fich=f'{name}_ficha.html'
    if not os.path.exists(fich):
        subprocess.run(['curl','-sS','-L','-m','60','-o',fich,'https://normas.gba.gob.ar'+u])
    t=open(fich,encoding='utf-8',errors='ignore').read()
    pdfs=re.findall(r'href="(/documentos/[^"]+\.pdf)"',t)
    pub=re.search(r'Fecha de publicaci\S*:\s*</?[^>]*>?\s*([0-9/]+)',t)
    pubs=re.findall(r'([0-9]{2}/[0-9]{2}/[0-9]{4})',t)
    bo=re.search(r'Boletín Oficial:\s*(?:<[^>]+>\s*)*([0-9]+)',t)
    print(name,u,pdfs,pubs[:2],bo.group(1) if bo else '')
    if pdfs:
        pdf=f'{name}_original.pdf'
        if not os.path.exists(pdf):
            subprocess.run(['curl','-sS','-L','-m','90','-o',pdf,'https://normas.gba.gob.ar'+pdfs[0]])
