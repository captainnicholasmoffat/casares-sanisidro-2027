import re,subprocess,os,sys
for line in sys.stdin.read().strip().splitlines():
    u,name=line.split()
    fich=f'{name}_ficha.html'
    if not os.path.exists(fich):
        subprocess.run(['curl','-sS','-L','-m','60','-o',fich,'https://normas.gba.gob.ar'+u])
    t=open(fich,encoding='utf-8',errors='ignore').read()
    pdfs=re.findall(r'href="(/documentos/[^"]+\.pdf)"',t)
    htmls=re.findall(r'href="(/documentos/[^"]+\.html)"',t)
    pubs=re.findall(r'([0-9]{2}/[0-9]{2}/[0-9]{4})',t)
    print(name,u,pdfs,htmls,pubs[:2])
    if pdfs:
        pdf=f'{name}_original.pdf'
        if not os.path.exists(pdf):
            subprocess.run(['curl','-sS','-L','-m','120','-o',pdf,'https://normas.gba.gob.ar'+pdfs[0]])
        subprocess.run(['python3','../_pdf2txt.py',pdf,pdf.replace('.pdf','.txt')])
