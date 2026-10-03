# Modelo de costo por puesto [cálculo propio]. Pesos ~jul-oct 2026.
IPC={'2022-10':1028.7060,'2025-05':8714.4871,'2025-06':8855.5681,'2025-11':9841.3581,'2025-12':10121.3715,'2026-01':10413.0309,'2026-02':10714.6255,'2026-07':12076.3937}
f=lambda m: IPC['2026-07']/IPC[m]
print("factores a jul-2026:", {k:round(f(k),4) for k in IPC})
# Precedentes por m2 y por artefacto
casos={'Reserva PO':(697289904.28,'2025-05',175,22),'Reserva contrato':(557832240,'2025-06',175,22),
       'Botanico PO':(399778429.18,'2025-06',105,16),'Botanico contrato':(319880718,'2025-06',105,16),
       'MdP LP48 PO':(27998240,'2022-10',103,9)}
for k,(m,mes,m2,art) in casos.items():
    a=m*f(mes); print(f"{k}: {a/1e6:.1f} M jul26; {a/m2/1e6:.2f} M/m2; {a/art/1e6:.1f} M/artefacto")
# AySA conexion con K oct-2026
K=2376.5912
con_lo=(284.25+24.22+445.81)*K; con_hi=(426.53+24.22+709.34)*K
print("AySA conexion", round(con_lo), round(con_hi))
# CABA LP16/26 unit prices ajustados (supuesto mes base ene-feb 2026 -> x1.13..1.16)
adj=(1.13+1.16)/2
pp110=118766.60*adj; cam=1356435.63*adj; exc=16254.65*adj; rell=117425.83*adj; ag40=65338.65*adj; contrap=70212.39*adj
grav_hi=pp110+0.8*exc+0.7*rell*0.5+cam/30+0.6*0.5*contrap
osse=108621226/(355+234)
print("grav per m: hi", round(grav_hi), " osse blend", round(osse), " agua40", round(ag40))
grav=(185000,275000); agua=(65000,90000); imp=(90000,130000); eb=(15e6,30e6)
modulo=(45e6,95e6); con=(con_lo,con_hi); fact_otros=(1.0e6,3.0e6)  # tramites, proyecto, empalmes [supuesto]
# Operacion mensual
rem=510234+104053+62094; nrem=303863+190039; conf=rem+nrem
contrib=0.31*rem; sac=(rem+0.31*rem)/12; fte=(conf+contrib+sac)*1.08
hora=fte/200
print("SOM conformado",conf," costo FTE empleador",round(fte)," por hora",round(hora))
margen=(1.5,1.9)
h_lim=60  # 2 pasadas diarias x 1 h x 30 dias
limp=(h_lim*hora*margen[0], h_lim*hora*margen[1])
h_enc=300 # 10 h/dia x 30
enc=(h_enc*hora*margen[0], h_enc*hora*margen[1])
print("limpieza 2 pasadas/dia",[round(x) for x in limp]," encargado 10h/dia",[round(x) for x in enc])
insumos=(150000,350000)
m3=(30,90); pm3=2*0.686*K*1.21
agua_mes=(m3[0]*pm3+2*0.0716*K*30*1.21, m3[1]*pm3+2*0.0716*K*30*1.21)
print("precio m3 agua+cloaca c/IVA",round(pm3)," agua/mes",[round(x) for x in agua_mes])
def fila(dist,bombeo):
    if not bombeo:
        tramo=(dist*grav[0]+dist*agua[0], dist*grav[1]+dist*agua[1]); ebc=(0,0)
    else:
        tramo=(dist*imp[0]+dist*agua[0], dist*imp[1]+dist*agua[1]); ebc=eb
    obra=tuple(modulo[i]+con[i]+fact_otros[i]+tramo[i]+ebc[i] for i in (0,1))
    mant=tuple(obra[i]*0.04/12 for i in (0,1))   # 4%/año de la obra
    mb=(200000,400000) if bombeo else (0,0)
    op=tuple(limp[i]+insumos[i]+agua_mes[i]+mant[i]+mb[i] for i in (0,1))
    am=tuple(obra[i]/120 for i in (0,1))
    tot=tuple(op[i]+am[i] for i in (0,1))
    return tramo,ebc,obra,op,am,tot
print("\n| Distancia | Bombeo | Tramo agua+cloaca | Estación de bombeo | OBRA total | Operación/mes | Amortización/mes (10 años) | TOTAL/mes |")
for d in (50,150,300):
    for b in (False,True):
        tramo,ebc,obra,op,am,tot=fila(d,b)
        M=lambda t: f"{t[0]/1e6:.1f}–{t[1]/1e6:.1f}"
        print(f"| {d} m | {'sí' if b else 'no'} | {M(tramo)} | {M(ebc) if b else '—'} | {M(obra)} | {M(op)} | {M(am)} | {M(tot)} |")
# con encargado: diferencia
d_enc=(enc[0]-limp[0], enc[1]-limp[1])
print("\nextra por encargado 10h/dia:", [round(x/1e6,2) for x in d_enc])
# 6 puestos
for d in (50,150,300):
    tramo,ebc,obra,op,am,tot=fila(d,False)
    print(d,"x6 total/mes sin bombeo:", round(6*tot[0]/1e6,1), round(6*tot[1]/1e6,1), " obra x6:", round(6*obra[0]/1e6), round(6*obra[1]/1e6))
