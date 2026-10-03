# Calculos propios - Programa San Isidro 2027 - n1_cuanto (2026-10-03)
import math
print("=== FINLANDIA (RL 2a:1-3; Asetus 609/1999; TLL 729/2018; tabla policial segun Kaila B.1) ===")
def df(y, dep=0):
    return max(6, math.floor((y-255)/60) - 3*dep)
cases = [("Vel +<=10 (lim<=60) fija",100,None),("Vel +16-20 (lim<=60) fija",200,None),
         ("Vel +21-23 (lim<=60) 12 DF",None,12),("Vel +30-32 (lim<=60) 18 DF",None,18),
         ("Vel +45-47 (lim<=60) 28 DF",None,28),("Vel +21-23 (lim>60) 10 DF",None,10),
         ("Celular (TLL) fija",100,None),("Semaforo rojo sin peligro (TLL) fija",100,None)]
for y in [1000,2000,4000,10000]:
    d=df(y); print(f"Ingreso neto {y} EUR: dia-multa {d} EUR ({100*d/y:.2f}% del ingreso mensual)")
    for name,fixed,n in cases:
        if fixed: amt=fixed
        else:
            amt=n*d
            if 'Vel' in name: amt=max(amt,200)
        print(f"   {name}: {amt} EUR = {100*amt/y:.1f}%")
print("Con 2 hijos a cargo, ingreso 2000:", df(2000,2), "EUR/dia")
print()
print("=== INGLATERRA Y GALES ===")
for w in [120,300,440,1000,2000]:
    m=w*52/12
    print(f"RWI {w} GBP/sem = {m:.0f} GBP/mes")
    for band,p in [("A",0.5),("B",1.0),("C",1.5)]:
        f=w*p; fc=min(f,1000); fm=min(f,2500)
        print(f"   Banda {band}: {f:.0f} (tope 1000 -> {fc:.0f} = {100*fc/m:.1f}% mes; autopista tope 2500 -> {fm:.0f} = {100*fm/m:.1f}%); con 1/3 culpabilidad: {fc*2/3:.0f} = {100*fc*2/3/m:.1f}%")
    for name,a in [("FPN velocidad",100),("FPN celular",200),("FPN semaforo",100)]:
        print(f"   {name} {a} = {100*a/m:.1f}% mes")
print("Tabla de cuotas: ", [(w,c,f"{100*c/w:.1f}%") for w,c in [(60,5),(120,10),(200,25),(300,50),(400,80)]])
print()
print("=== CALIFORNIA (UBPS 2026; FPL 2026) ===")
fpl1=15960/12; fpl4=33000/12
incs={"125% FPL 1 pers":1.25*fpl1,"125% FPL 4 pers":1.25*fpl4,"10000 USD":10000}
fines={"Vel 1-15 mph":234,"Vel 16-25":363,"Vel>=26 / Rojo":486,"Celular":158}
for k,v in incs.items():
    print(f"{k}: {v:.2f}/mes")
    for f,a in fines.items():
        print(f"   {f} {a}: {100*a/v:.1f}% | con -50%: {100*a*0.5/v:.1f}% | con -61%: {100*a*0.39/v:.1f}%")
    print(f"   cuota 25 USD = {100*25/v:.2f}%; FFJC 2% = {0.02*v:.0f} USD")
print()
print("=== ALEMANIA (BKatV) ===")
for y in [1000,2000,4000,10000]:
    print(y, {k:f"{100*a/y:.1f}%" for k,a in [("21-25 km/h urbano 115",115),("31-40 urbano 260",260),("rojo 90",90),("rojo>1s 200",200),("celular 100",100)]})
print()
print("=== SUECIA (SFS 2025:917 Bilaga 1A) SEK ===")
for y in [15000,30000,60000,150000]:
    print(y, {k:f"{100*a/y:.1f}%" for k,a in [("21-25 lim<=50 3200",3200),("31+ 4000",4000),("rojo 3000",3000),("celular 1500",1500)]})
print("dagsbot anual 400000: ", 400000/1000-50)
print()
print("=== SUIZA ===")
for y in [3000,6000,12000,30000]:
    ts=y/30
    print(f"neto {y} CHF/mes: TS ~{ts:.0f} (tope 3000; min 30). OB 250 = {100*250/y:.1f}%; Busse 400 = {100*400/y:.1f}% ; 10 TS = {10*min(ts,3000):.0f} ({100*10*min(ts,3000)/y:.0f}%); 20 TS = {20*min(ts,3000):.0f} ({100*20*min(ts,3000)/y:.0f}%)")
print()
print("=== DINAMARCA alcohol ===")
for g in [200000,400000,1000000]:
    for p in [0.6,1.0,2.0]:
        print(g,p, round(g*p/25))
print()
print("=== ARGENTINA ===")
UF=2281.0
smvm=391200; jub=435748.51; cbt_ae=519578.43; cbt_h2=1605497.35; cba_h2=726469.38
d1=136480; d5=827837; d10=3466554; med=900000
anchors={"SMVM":smvm,"Jub min":jub,"CBT adulto eq":cbt_ae,"CBT hogar 4":cbt_h2,"Decil1":d1,"Mediana":med,"Decil10":d10}
for name,uf in [("Vel min 150UF pago vol 50%",75),("Vel min 150UF",150),("Vel max 1000UF",1000),("Rojo/celular min 300 pago vol",150),("Rojo/celular min 300",300)]:
    a=uf*UF
    print(name, f"${a:,.0f}", {k:f"{100*a/v:.1f}%" for k,v in anchors.items()})
print()
print("=== ARBA patente (Ley 15.558 art 33 A) ===")
def pat(v):
    tr=[(0,14.1e6,0,0.01),(14.1e6,18.7e6,141000,0.02),(18.7e6,26.1e6,233000,0.03),(26.1e6,53.9e6,455000,0.04),(53.9e6,1e18,1567000,0.045)]
    for lo,hi,fx,al in tr:
        if lo<v<=hi: return fx+al*(v-lo)
for v in [10e6,20e6,30e6,60e6,100e6]:
    p=pat(v); print(f"valuacion {v:,.0f}: patente {p:,.0f} ({100*p/v:.2f}%); mensual {p/12:,.0f}; % SMVM anual {100*p/(12*smvm):.1f}%")
print()
print("=== CABA proyecto IdDoc215871 (UF CABA 1173.08 [prensa]) ===")
ufc=1173.08
for v in [10e6,60e6]:
    for name,uf,pc in [("hasta 30% 150UF+0.05%",150,0.0005),(">30% 250UF+0.10%",250,0.001),("estac 100UF+0.05%",100,0.0005)]:
        base=uf*ufc; add=pc*v
        print(f"val {v:,.0f} {name}: base {base:,.0f} + adic {add:,.0f} (+{100*add/base:.1f}%)")
print()
print("=== BRASIL PL 78/2025 (umbral de valor del vehiculo donde se iguala multa actual) ===")
for name,cur,p in [("gravissima",293.47,0.0035),("grave",195.23,0.002),("media",130.16,0.0015),("leve",88.38,0.001)]:
    print(name, f"R$ {cur/p:,.0f}", "; auto R$ 60.000 ->", round(60000*p,2), "; R$ 500.000 ->", round(500000*p,2))
