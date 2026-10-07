# Informe 23 ter, punto 1: teléfonos por etapa (sin transmisión en vivo; video por wifi; guarda 6 meses rápida + 18 archivo).
# Pesos de dic-2025, dólar $1.447,84. Insumos verificados en los reportes de agentes/turnos (W1a) y de video/datos/nube (W1b).
GBH=2.34          # GB por hora, 1080p H.265 5 Mbps + audio (W1b)
TB=74186          # $ por TB producido, Google Cloud Bélgica, 6 meses Coldline + 18 Archive (W1b)
DATOS=82495       # $ por agente y año, M2M 1 GB del convenio de la Ciudad (W1b)
KIT=98327         # soporte de pecho + batería 10.000 mAh (W1b)
REPO=KIT/2        # reposición del kit cada 2 años
grupos={ # nombre: (agentes min, max, horas por turno, turnos por mes)
 'Inspectores (Fiscalización)':(81,103,7,22),
 'Tránsito (Jefatura de Inspectores)':(120,167,8,26),
 'Patrulla (calle)':(300,359,7,22)}
tot={}
for g,(a0,a1,h,t) in grupos.items():
    tbano=GBH*h*t*12/1000; guarda=tbano*TB; anual=guarda+DATOS+REPO
    print(f"{g}: {h} h x {t} turnos/mes -> {tbano:.2f} TB/año por agente; guarda ${guarda:,.0f}; datos ${DATOS:,}; reposición ${REPO:,.0f}; total ${anual:,.0f} por agente y año (régimen)")
    print(f"   {a0}-{a1} agentes: compra {a0*KIT/1e6:.1f} a {a1*KIT/1e6:.1f} M; por año {a0*anual/1e6:.1f} a {a1*anual/1e6:.1f} M")
    tot[g]=(a0*KIT,a1*KIT,a0*anual,a1*anual)
e1=[tot['Inspectores (Fiscalización)'][i]+tot['Tránsito (Jefatura de Inspectores)'][i] for i in range(4)]
print(f"\nPRIMERA ETAPA (inspectores + tránsito): compra {e1[0]/1e6:.1f} a {e1[1]/1e6:.1f} M; por año en régimen {e1[2]/1e6:.1f} a {e1[3]/1e6:.1f} M")
p=tot['Patrulla (calle)']; print(f"SEGUNDA ETAPA (Patrulla): compra {p[0]/1e6:.1f} a {p[1]/1e6:.1f} M; por año en régimen {p[2]/1e6:.1f} a {p[3]/1e6:.1f} M")
print("Aparte: estación de descarga por base (QNAP 12 bahías con 4 discos de 22 TB, unos 40 TB útiles): 9,47 M cada una [W1b, supuesto el armado]")
print("El primer año la guarda cuesta menos (se acumula): según W1b, unos dos tercios del régimen por agente.")
