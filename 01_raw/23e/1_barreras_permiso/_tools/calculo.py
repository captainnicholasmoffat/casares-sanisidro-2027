# Cálculos U1 · barreras flotantes en Perú y Alto Perú. Pesos de dic-2025.
# Correr: python3 -I calculo.py > calculo_salida.txt
import csv, math, os
IPCF='/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/ch/wt/data/ipc_indec_mensual.csv'
ipc={}
for r in csv.DictReader(open(IPCF,encoding='utf-8')):
    ipc[(int(r['anio']),int(r['mes']))]=float(r['indice'])
D25=ipc[(2025,12)]; J26=ipc[(2026,7)]
def a_dic25(monto,anio,mes):
    k=(anio,mes)
    if k not in ipc: k=(2026,7)   # precios posteriores a jul-2026: se usa jul-2026 (regla)
    return monto*D25/ipc[k]
USD=1447.84
M=1e6
def fm(x): return f"{x/M:,.1f} M".replace(',','X').replace('.',',').replace('X','.')
def fp(x): return f"{x:,.0f}".replace(',','.')
out=[]
def p(*a): print(*a)

p("=== 0. Índices usados")
for k in [(2018,12),(2020,6),(2021,8),(2024,11),(2025,3),(2025,12),(2026,1),(2026,7)]:
    p("  IPC",k,ipc[k])
p("  Dólar dic-2025 (BCRA A3500 promedio):",USD)

p("\n=== 1. Precio por metro de barrera (pesos dic-2025)")
numaco20 = a_dic25(283140/20,2020,6)   # OSSE CD 66/2020: 2 tramos de 10 m, pollera de red
sincerar18= a_dic25(379300/140,2018,12) # OSSE CP 64/18: lona, si fueran 140 m
ecoBRV1520= a_dic25(980089,2026,10)     # EcoWay lista oct-2026 (aguas tranquilas)
ecoBRV1014= a_dic25(487424,2026,10)
ecoBR1018 = a_dic25(458598,2026,10)
ecoBR1014 = a_dic25(432393,2026,10)
for n,v in [("NUMACO 2020 dinámica con pollera de red (OSSE)",numaco20),("SINCERAR 2018 lona (OSSE, si 140 m)",sincerar18),
            ("EcoWay BRV1520 valla (lista oct-26)",ecoBRV1520),("EcoWay BRV1014 valla",ecoBRV1014),("EcoWay BR1018 antiderrame",ecoBR1018),("EcoWay BR1014 antiderrame",ecoBR1014)]:
    p(f"  {n}: {fp(v)} $/m")
P_LO, P_HI = numaco20, ecoBRV1520
P_MID=(P_LO+P_HI)/2
p(f"  Rango adoptado tipo 'corriente y residuos grandes': {fp(P_LO)} a {fp(P_HI)} $/m; medio {fp(P_MID)}")
osse26=a_dic25(36960000,2026,8); osse26pres=a_dic25(37443450,2026,8)
p(f"  OSSE CP 87/26 (NUMACO, largo no publicado): {fm(osse26)}; presupuesto oficial {fm(osse26pres)}")
for L in (40,60,80,100,140):
    p(f"     si midiera {L} m: {fp(osse26/L)} $/m")

p("\n=== 2. Largo de barrera")
casos={'Perú':dict(W=13,Wlo=10,Whi=18),'Alto Perú':dict(W=23,Wlo=18,Whi=30)}
POCKET=6.0; SLACK=1.10; SPARE=0.25
def largos(W):
    r={}
    r['diag45']=W/math.sin(math.radians(45))
    r['diag30']=W/math.sin(math.radians(30))
    r['J37.5']=W/math.sin(math.radians(37.5))+POCKET
    r['U_bandalong(2W)']=2*W
    r['U_semicirculo(pi*W/2)']=math.pi*W/2
    return r
L_inst={}
for b,c in casos.items():
    p(f"  {b}: ancho W={c['W']} m (rango {c['Wlo']}-{c['Whi']})")
    for Wk in ('Wlo','W','Whi'):
        r=largos(c[Wk])
        p(f"    W={c[Wk]:>4} m: "+"; ".join(f"{k} {v:.1f} m" for k,v in r.items()))
    Ls=[largos(c[Wk])['J37.5']*SLACK for Wk in ('Wlo','W','Whi')]
    L_inst[b]=Ls
    p(f"    Recomendado J a ~37,5° + bolsillo {POCKET:.0f} m + {int((SLACK-1)*100)}% uniones/holgura: {Ls[0]:.0f} / {Ls[1]:.0f} / {Ls[2]:.0f} m instalados; con {int(SPARE*100)}% de repuesto (ACUMAR): {Ls[0]*(1+SPARE):.0f} / {Ls[1]*(1+SPARE):.0f} / {Ls[2]*(1+SPARE):.0f} m")
p("  Alternativa Alto Perú si la boca diera a canal abierto (~70 m): encierro semicircular radio 15 m = %.0f m" % (math.pi*15))
p("  Referencia OSSE Arroyo del Barco: reja 3,70 x 7,40 m y barrera de 140 m (encierro en el puerto)")
p("  Referencia Bandalong: canal de 200 pies con 400 pies de brazos = 2,0 x ancho")

p("\n=== 3. Recorrido vertical (m sobre el Cero del Riachuelo, SHN en Plan de Manejo 2012)")
niveles={'1 año':2.55,'2,5 años':3.05,'10 años':3.55,'45 años':4.05,'90 años':4.40}
minimo=-0.70
for k,v in niveles.items(): p(f"  recurrencia {k}: max {v:.2f} m -> rango desde el mínimo anual ({minimo}) = {v-minimo:.2f} m")
p("  Marea astronómica: M2 0,27 m de amplitud en Buenos Aires (rango ~0,5-0,6 m); sudestada 09/08/2021: 2,80 m (según el Municipio)")
GUIA=3.55+0.6+0.5   # nivel de diseño 10 años + alto de barrera + margen
p(f"  Tope de guía recomendado ~ +{GUIA:.2f} m CdR (10 años + 0,6 m de barrera + 0,5 m de margen) [supuesto]; por encima: se suelta por alerta")

p("\n=== 4. Fuerzas (ITOPF TIP 3: F[kgf]=100*A*V^2; viento: V/40)")
SK=0.6; FB=0.4; THETA=math.radians(37.5)
anch={}
for b in casos:
    L=L_inst[b][1]; A=L*SK
    for v in (0.5,1.0,1.5):
        Fc=100*A*(v*math.sin(THETA))**2
        p(f"  {b} L={L:.0f} m, pollera {SK} m, v={v} m/s a 37,5°: corriente {Fc:,.0f} kgf")
    Fc=100*A*(1.0*math.sin(THETA))**2; Fw=100*(L*FB)*(15/40)**2; Ft=(Fc+Fw)*1.3
    Fperp=100*A*(2.0)**2
    anch[b]=Ft
    p(f"   -> diseño v=1,0 m/s + viento 15 m/s + 30% por basura: {Ft:,.0f} kgf; caso extremo v=2 m/s perpendicular: {Fperp:,.0f} kgf (por eso: eslabón fusible/suelta rápida)")
    p(f"   -> muerto (3x carga en aire, ITOPF) si toma 1/3: {3*Ft/3/1000:.2f} t = {3*Ft/3/1000/2.4:.2f} m3 de hormigón; se adopta 1,0 m3 por muerto [supuesto]")

p("\n=== 5. Precios de anclaje (pesos dic-2025)")
HA_m3=a_dic25(416219.43,2025,3)       # LP 62/2024 banco H°A° in situ, redeterminado 1/3/2025
p(f"  H°A° in situ por m3 (LP 62/2024, mar-25): {fp(HA_m3)} $/m3; premoldeado con ojal (+20% supuesto): {fp(HA_m3*1.2)}")
acero_kg=a_dic25(64190/(0.4*0.0016*7850*3),2026,10)  # Easy caño 100x100x1,6 3 m
p(f"  Acero (minorista Easy, caño 100x100x1,6 mm 3 m $64.190, oct-26): {fp(acero_kg)} $/kg")
c7=a_dic25(19930,2026,10); c13=c7*(13/7)**2
p(f"  Cadena galvanizada 7 mm (Easy, oct-26): {fp(c7)} $/m; 13 mm extrapolada por peso (x(13/7)^2): {fp(c13)} $/m [cálculo propio]")
hora=a_dic25(133100,2024,11)
p(f"  Hora de equipo con cuadrilla (LP 60/2024, $133.100, nov-24): {fp(hora)} $/h")
gas3=1972.5   # mediana país, estaciones con precio vigente fechado dic-2025 (SE Res. 314/2016)
gas2=1723.0
p(f"  Gasoil grado 3 dic-25 (mediana SE): {gas3} $/l; grado 2: {gas2} $/l")

# Poste guía en la orilla: caño 273x9,3 mm x 9 m = 60,5 kg/m
kg_poste=60.5*9
def poste(f): return kg_poste*acero_kg*f + 2.0*HA_m3
p(f"  Poste guía en orilla (caño 273x9,3 x 9 m, {kg_poste:.0f} kg, x1,5-2,5 por fabricar/galvanizar/collar/colocar + 2 m3 de base): {fm(poste(1.5))} a {fm(poste(2.5))}; medio {fm(poste(2.0))}")
muerto=1.0*HA_m3*1.2; cadena_m=16; boya_herr=0.3*M
def muertoset(): return muerto+cadena_m*c13+boya_herr
p(f"  Muerto 1 m3 + 16 m de cadena 13 mm + boya y grilletes: {fm(muertoset())}")

p("\n=== 6. Compra por boca (barrera + anclaje + instalación + proyecto + permisos)")
cfg={'Perú':dict(muertos=(1,1,2),horas=(16,24,32),herr=(0.6*M,1.0*M,1.5*M)),
     'Alto Perú':dict(muertos=(2,2,3),horas=(24,32,48),herr=(0.8*M,1.5*M,2.0*M))}
UT26=275.0
def eia_prov(inv_d25):
    inv_nom=inv_d25*J26/D25; base=1484.90*UT26; tope=148484.70*UT26
    ar=base+max(0,inv_nom-20000*UT26)*0.005
    return min(ar,tope)*D25/J26
tot={}
for b,c in cfg.items():
    res=[]
    for i,esc in enumerate(('bajo','medio','alto')):
        Lbuy=L_inst[b][1]*(1+SPARE) if esc!='alto' else L_inst[b][2]*(1+SPARE)
        if esc=='bajo': Lbuy=L_inst[b][0]*(1+SPARE)
        precio=(P_LO,P_MID,P_HI)[i]
        barrera=Lbuy*precio
        postes=2*poste((1.5,2.0,2.5)[i])
        muertos=c['muertos'][i]*muertoset()
        herr=c['herr'][i]
        inst=c['horas'][i]*hora+1.0*M
        obra=barrera+postes+muertos+herr+inst
        proy=max(8*M,obra*(0.15,0.20,0.25)[i]) if esc!='bajo' else max(8*M,obra*0.15)
        cph=100*gas3
        aho=0.018*obra; cah=0.015*obra
        eia=eia_prov(obra)
        perm_min=cph+aho+cah          # municipal EIA sin arancel
        perm_max=cph+aho+cah+eia       # EIA provincial
        total_min=obra+proy+perm_min; total_max=obra+proy+perm_max
        res.append((esc,Lbuy,barrera,postes,muertos,herr,inst,obra,proy,cph,aho,cah,eia,total_min,total_max))
        p(f"  {b} [{esc}] compra {Lbuy:.0f} m a {fp(precio)} $/m: barrera {fm(barrera)}; postes {fm(postes)}; muertos {c['muertos'][i]} = {fm(muertos)}; herrajes/señales {fm(herr)}; instalación {fm(inst)} -> OBRA {fm(obra)}")
        p(f"      proyecto {fm(proy)}; ADA: CPH {fm(cph)} + aptitud hidráulica 1,8% {fm(aho)} + constancia 1,5% {fm(cah)}; EIA provincial (si corresponde) {fm(eia)}")
        p(f"      TOTAL {fm(total_min)} (EIA municipal) a {fm(total_max)} (EIA provincial)")
    tot[b]=res
p("\n  DOS BOCAS:")
for i,esc in enumerate(('bajo','medio','alto')):
    a=tot['Perú'][i]; c=tot['Alto Perú'][i]
    p(f"   [{esc}] obra {fm(a[7]+c[7])}; proyecto {fm(a[8]+c[8])}; permisos {fm(a[9]+a[10]+a[11]+c[9]+c[10]+c[11])} (+EIA prov. {fm(a[12]+c[12])}); TOTAL {fm(a[13]+c[13])} a {fm(a[14]+c[14])}")

p("\n=== 7. Reposición por año (sin vaciado)")
for b in cfg:
    for i,esc in enumerate(('bajo','medio','alto')):
        r=tot[b][i]; Linst=L_inst[b][i]
        precio=(P_LO,P_MID,P_HI)[i]
        frac=(0.15,0.20,0.25)[i]
        barrera_anual=Linst*frac*precio
        cadena_herr=(r[4]*0.5+r[5])*0.25   # 25%/año de cadenas y herrajes (~mitad del set de muerto es cadena)
        civil=(r[3]+r[4]*0.5)*0.05
        p(f"  {b} [{esc}]: barrera {int(frac*100)}%/año {fm(barrera_anual)} + cadenas/herrajes {fm(cadena_herr)} + postes/muertos 5% {fm(civil)} = {fm(barrera_anual+cadena_herr+civil)} por año")

p("\n=== 8. Referencias importadas (dólares históricos a $1.447,84, sin ajustar por inflación de EE. UU.)")
for n,v in [("Bandalong Watts Branch, DC (2009) instalado",55000),("Bandalong Fairfax (2020) trampa sola",104500),("Fairfax (2020) diseño, permisos, accesos, obra",587000),("Fairfax total",691500),("Fort Worth (Lake Como) total",226000),("Fairfax mantenimiento estimado por año",45000)]:
    p(f"  {n}: US$ {fp(v)} = {fm(v*USD)}")

p("\n=== 9. Velocidad en el canal en la crecida de diseño (río bajo)")
Qap=4e6/1000/60
p(f"  Alto Perú: Q = 4 millones de litros por minuto (según el Municipio) = {Qap:.1f} m3/s")
for h in (1.5,2.0,3.0):
    p(f"    dársena 23 m x {h} m de agua: v = {Qap/(23*h):.2f} m/s")
p(f"    túnel 4,40 m lleno: v = {Qap/(math.pi*4.4**2/4):.2f} m/s")
Aperu=2*3.2*3.2
for vb in (1.5,2.0,2.5):
    Q=Aperu*vb
    p(f"  Perú: dos bocas 3,2x3,2 m ({Aperu:.1f} m2) a {vb} m/s [supuesto] -> Q={Q:.0f} m3/s; canal 13 m x 1,5-3 m: v = {Q/(13*3):.2f} a {Q/(13*1.5):.2f} m/s")
p("  MSMA: la basura escapa por debajo desde ~1 m/s. ITOPF tabla 2 (petróleo): 0,5 m/s -> 45°; 0,75 -> 28°; 1,0 -> 20°.")
p("\n=== 10. Canon posible si la ADA aplicara la fórmula del Decreto 3233/2025 con Q=0 (sólo cargo fijo) [inferencia]")
p(f"  8 l de gasoil grado 3 por mes = {fp(8*gas3)} $/mes = {fm(12*8*gas3)} por año y por permiso")
p(f"  Arancel EIA provincial mínimo (1.484,90 UT x $275, a pesos dic-25 con IPC jul-26): {fm(1484.9*275*D25/J26)}")
