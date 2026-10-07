# Cuentas del reporte v1 (inspectores de Habilitaciones y de obra; banco que paga los sueldos)
# Correr: python3 -I calculo.py > calculo_salida.txt
import json, datetime, collections, os
D = os.path.dirname(os.path.abspath(__file__))

IPC_DIC25 = 10121.3715
IPC_JUL26 = 12076.3937          # último mes disponible: se usa para precios posteriores
F = IPC_DIC25 / IPC_JUL26        # factor a pesos de dic-2025
def dic25(x): return x * F
def M(x): return f"{x/1e6:,.2f} M"
print(f"Factor a pesos de dic-2025 (IPC dic-25 / jul-26) = {F:.5f}")

# ---------------- 1. Habilitaciones: F6 2026 (transcripción propia, pág. 24 de 31) ----------------
hab = {"Superior DG": 1, "Jerárquico c13": 2, "Jerárquico c14": 1,
       "Técnico c9": 1, "Técnico c10": 2, "Técnico c12": 1,
       "Admin c8": 3, "Admin c9": 7, "Admin c10": 4, "Admin c11": 3, "Mensualizado": 4}
print("\n== 1. Habilitaciones y Permisos (F6 2026) ==")
print("total cargos:", sum(hab.values()), "(F6 dice 29)")
tec = sum(v for k, v in hab.items() if k.startswith("Técnico"))
adm = sum(v for k, v in hab.items() if k.startswith("Admin"))
jef = sum(v for k, v in hab.items() if k.startswith(("Superior", "Jerárquico")))
print(f"técnicos {tec}, administrativos {adm}, mensualizados {hab['Mensualizado']}, jefes {jef}")
print(f"costo anual mensualizados 50.434.579 / 4 = {50434579/4:,.0f} por cargo (13 sueldos: {50434579/4/13:,.0f} por mes)")

# Carga de trabajo: disposiciones de la DG Habilitaciones y Permisos en el índice del Boletín
d = json.load(open(os.path.join(D, "tmp", "dghp_disposiciones.json")))
def dt(s):
    try: return datetime.datetime.strptime(s, "%d/%m/%Y").date()
    except Exception: return None
cnt = collections.Counter()
for k, v in d.items():
    x = dt(v[1])
    if x and datetime.date(2025, 8, 1) <= x <= datetime.date(2026, 7, 31):
        cnt[v[2]] += 1
print("disposiciones firmadas ago-2025 a jul-2026 (12 meses), por tipo:", dict(cnt))
lic = cnt["LICENCIA"]; exp_ = cnt["EXPRES"]
print(f"licencias (nivel 2, con inspección previa) por año: {lic}; exprés: {exp_}; parte de licencias: {lic/(lic+exp_):.1%}")
dias_habiles = 220
for por_dia in (1.5, 3):
    print(f"  con {por_dia} inspecciones por día y por inspector: {lic/dias_habiles/por_dia:.2f} inspectores de tiempo completo")
hab_piso, hab_central, hab_techo = 2, 4, 8
print(f"rango adoptado Habilitaciones: piso {hab_piso} (carga + cobertura de licencias), central {hab_central} (técnicos), techo {hab_techo} (técnicos + mensualizados)")

# ---------------- 2. Obras: F6 2026 Planeamiento Urbano (pág. 25 de 31) ----------------
plan = {"Superior DG": 2, "Superior Subsecretario": 2, "Superior Secretario": 1,
        "Jerárquico c14": 4, "Jerárquico c15": 1,
        "Profesional c9": 5, "Profesional c11": 4, "Profesional c13": 4, "Profesional c14": 1,
        "Técnico c9": 5, "Técnico c12": 5,
        "Admin c7": 3, "Admin c8": 7, "Admin c9": 8, "Admin c10": 6, "Admin c11": 1, "Admin c13": 3,
        "Servicio c7": 1, "Servicio c8": 1, "Servicio c9": 4, "Mensualizado": 23}
print("\n== 2. Planeamiento Urbano (F6 2026) ==")
print("total cargos:", sum(plan.values()), "(F6 dice 91)")
serv = sum(v for k, v in plan.items() if k.startswith("Servicio"))
tecp = sum(v for k, v in plan.items() if k.startswith("Técnico"))
print(f"personal de servicio {serv}, técnicos {tecp}, profesionales {sum(v for k,v in plan.items() if k.startswith('Profesional'))}")
print(f"costo por mensualizado: 440.184.043 / 23 = {440184043/23:,.0f} por año ({440184043/23/13:,.0f} por mes) -> por encima del básico de cat. 15 (1.382.572): no son inspectores [inferencia]")
print(f"comparación Fiscalización: 526.621.797 / 49 = {526621797/49/13:,.0f} por mes por mensualizado")
ob_piso, ob_c1, ob_c2, ob_techo = 3, 3, 6, serv + tecp
print(f"rango adoptado obras particulares: piso {ob_piso} (Dto. 1218/2025: eran los únicos), central {ob_c1} a {ob_c2} (personal de servicio del programa), techo {ob_techo} (servicio + técnicos)")
print("meta 2026 del Programa 53 (Agencia de Control): 610 fiscalizaciones de obras por año =",
      f"{610/dias_habiles:.1f} por día hábil (las hacen los inspectores de Fiscalización, ya contados)")

# ---------------- 5. Costo de sumar a la primera etapa ----------------
COMPRA = 98327; ANUAL = 452463
print("\n== 5. Costo de sumar Habilitaciones y obras (valores por agente del 23 ter: compra 98.327; por año 452.463, 7 h x 22) ==")
def fila(nombre, n):
    print(f"{nombre:42} {n:>3} agentes | compra {n*COMPRA:>12,.0f} | por año {n*ANUAL:>13,.0f}")
for nombre, n in [("Habilitaciones piso", hab_piso), ("Habilitaciones central", hab_central), ("Habilitaciones techo", hab_techo),
                  ("Obras piso = central bajo", ob_piso), ("Obras central alto", ob_c2), ("Obras techo", ob_techo)]:
    fila(nombre, n)
tot_c = (hab_central + ob_c1, hab_central + ob_c2)
tot_x = (hab_piso + ob_piso, hab_techo + ob_techo)
print(f"TOTAL central {tot_c[0]} a {tot_c[1]} agentes: compra {M(tot_c[0]*COMPRA)} a {M(tot_c[1]*COMPRA)}; por año {M(tot_c[0]*ANUAL)} a {M(tot_c[1]*ANUAL)}")
print(f"TOTAL extremos {tot_x[0]} a {tot_x[1]} agentes: compra {M(tot_x[0]*COMPRA)} a {M(tot_x[1]*COMPRA)}; por año {M(tot_x[0]*ANUAL)} a {M(tot_x[1]*ANUAL)}")
# primera etapa anterior (23 ter): 201 a 270 agentes; 19,8 a 26,5 M compra; 104,4 a 141,0 M por año
pe_ag = (201, 270); pe_c = (19.8e6, 26.5e6); pe_a = (104.4e6, 141.0e6)
print(f"Primera etapa nueva (central): {pe_ag[0]+tot_c[0]} a {pe_ag[1]+tot_c[1]} agentes; compra {M(pe_c[0]+tot_c[0]*COMPRA)} a {M(pe_c[1]+tot_c[1]*COMPRA)}; por año {M(pe_a[0]+tot_c[0]*ANUAL)} a {M(pe_a[1]+tot_c[1]*ANUAL)}")
print(f"Primera etapa nueva (extremos): {pe_ag[0]+tot_x[0]} a {pe_ag[1]+tot_x[1]} agentes; compra {M(pe_c[0]+tot_x[0]*COMPRA)} a {M(pe_c[1]+tot_x[1]*COMPRA)}; por año {M(pe_a[0]+tot_x[0]*ANUAL)} a {M(pe_a[1]+tot_x[1]*ANUAL)}")
print(f"aumento sobre la primera etapa (central): {tot_c[0]*ANUAL/pe_a[1]:.1%} a {tot_c[1]*ANUAL/pe_a[0]:.1%} del costo anual")

# ---------------- 3. Banco que paga los sueldos: saldos de las cuentas 'SUELDOS' (SEF) ----------------
print("\n== 3. Cuentas 'SUELDOS' en la Situación Económico-Financiera (saldos al cierre) ==")
sueldos = [("31/12/2024", 766070.33, 36957.05, 40486.32), ("31/12/2025", 10585445022.26, 36957.05, 40486.32),
           ("31/03/2026", 106419979.16, 388.27, 40486.32), ("30/06/2026", 11518277769.47, None, None)]
for f_, bp, san, hg in sueldos:
    tot = bp + (san or 0) + (hg or 0)
    print(f"{f_}: Banco Provincia Sueldos 34545/1 = {bp:>18,.2f} | Santander Sueldos = {san} | HSBC/Galicia Sueldos = {hg} | parte Banco Provincia {bp/tot:.4%}")

# ---------------- 4. Teléfono en Provincia Compras y alternativas de crédito ----------------
print("\n== 4. Teléfono propio: Provincia Compras (07/10/2026) en pesos de dic-2025 ==")
ofertas = [("Galaxy A27 5G 8/256 (Diggit), 24 cuotas tasa 0", 925999, 24),
           ("Galaxy A27 5G 8/256 (Dinatech), 24 cuotas tasa 0", 921999, 24),
           ("Galaxy A27 5G 256 (tienda Samsung), 9 cuotas tasa 0", 799999, 9),
           ("Moto G85 5G 8/256 OIS (Newsan), 24 cuotas tasa 0", 761925, 24),
           ("Galaxy A37 8/256 OIS (Vstore), 24 cuotas tasa 0", 1149999, 24),
           ("Redmi Note 15 Pro 8/256 OIS (Diggit), 24 cuotas tasa 0", 1069999, 24)]
basicos = {7: 499710, 8: 524675, 9: 550902, 10: 578468, 11: 607363, 12: 637790}  # Dto. 782/2026, 35 h, julio 2026
for n, p, c in ofertas:
    cuota = p / c
    print(f"{n:58} precio {p:>10,.0f} (= {dic25(p):>9,.0f} dic-25) | cuota {cuota:>9,.0f} (= {dic25(cuota):>7,.0f}) | "
          + " ".join(f"c{k}:{cuota/b:.1%}" for k, b in basicos.items()))
print("(cuota / básico de julio 2026 de 35 h; el agente cobra además bonificaciones, así que el peso real es menor)")

def cuota_frances(P, tna, n):
    i = tna / 12
    return P * i / (1 - (1 + i) ** -n)
P = 799999
for tna, nombre in [(0.651, "Préstamo personal precalificado agentes públicos (TNA 65,10%)"), (0.855, "Público en general (TNA 85,50%)")]:
    c = cuota_frances(P, tna, 24)
    print(f"{nombre}: por {P:,} en 24 meses, cuota {c:,.0f}, total {c*24:,.0f} ({c*24/P-1:.0%} más que el contado)")

# tasa implícita de las 24 cuotas (925.999) contra el precio de la tienda Samsung en 9 cuotas sin interés (799.999)
def pv(c, r, n): return c * (1 - (1 + r) ** -n) / r
c24 = 925999 / 24
lo, hi = 1e-6, 0.2
for _ in range(200):
    mid = (lo + hi) / 2
    if pv(c24, mid, 24) > 799999: lo = mid
    else: hi = mid
print(f"tasa implícita de pagar 24 x {c24:,.0f} en vez de 799.999: {mid:.3%} mensual = TNA {mid*12:.1%}")
for infl in (0.015, 0.02, 0.0211):
    print(f"  valor actual de las 24 cuotas con inflación de {infl:.2%} mensual: {pv(c24, infl, 24):,.0f} (contra 799.999)")
print(f"sobreprecio de las 24 cuotas sobre el precio Samsung/Naldo: {925999/799999-1:.1%}")
