#!/usr/bin/env python3
# W1b · Video de los inspectores: resolución, peso, plan de datos mínimo, subida por wifi y guarda en Europa.
# Pesos de dic-2025. Dólar 1.447,84 (BCRA, Com. A 3500, promedio dic-2025, consigna). Euro: promedio BCRA dic-2025 (API).
# Marcas: [verificado] dato leído en la fuente; [supuesto] decisión mía; [cálculo propio].
import json, math, os

D = os.path.dirname(os.path.abspath(__file__)) + "/../"
out = []
def pr(*a):
    s = " ".join(str(x) for x in a); print(s); out.append(s)
def P(x, n=0):
    s = f"{x:,.{n}f}"; return s.replace(",", "X").replace(".", ",").replace("X", ".")
def M(x): return P(x/1e6, 2) + " M"

# ---------------------------------------------------------------- moneda e IPC
IPC = {"2025-12": 10121.3715, "2026-03": 11077.0608, "2026-04": 11363.0904, "2026-05": 11607.3937,
       "2026-06": 11826.4103, "2026-07": 12076.3937}
def dm(p, mes): return p * IPC["2025-12"] / IPC[mes]
F_OCT = IPC["2025-12"] / IPC["2026-07"]          # precios de oct-2026 -> jul-2026 es el último IPC del repo
USD = 1447.84
eur = json.load(open(D + "bcra_api_cotizaciones_EUR_dic2025.json"))
EUR = sum(r["detalle"][0]["tipoCotizacion"] for r in eur["results"]) / len(eur["results"])
GIB = 1.073741824                                    # GB por GiB
pr(f"Deflactor oct-2026 (IPC jul-2026) -> dic-2025: {F_OCT:.5f}. Dólar {P(USD,2)}. Euro promedio BCRA dic-2025: {P(EUR,2)} ({len(eur['results'])} días hábiles)")
pr("Precios en USD/EUR de 2026 tomados como de dic-2025 sin ajustar por inflación externa [supuesto]")

# ---------------------------------------------------------------- 1. Resolución y tasa de bits
pr("\n== 1. Peso de una hora de video ==")
OVH_MP4 = 1.015                                      # sobrecarga de contenedor MP4 [supuesto]
AUDIO = 0.128                                        # AAC 128 kbps mono 48 kHz [supuesto]
def gbh(vid, aud=AUDIO): return (vid + aud) * 1e6 * 3600 / 8 / 1e9 * OVH_MP4
perfiles = {
    "720p30 H.264 4 Mbps (piso)":            4.0,
    "720p30 H.265 2,5 Mbps (piso)":          2.5,
    "1080p30 H.264 8 Mbps (alternativa)":    8.0,
    "1080p30 H.265 5 Mbps (RECOMENDADO)":    5.0,
    "1440p30 H.265 8 Mbps (opcional)":       8.0,
    "2160p30 H.265 16 Mbps (no recomendado)": 16.0,
}
GBH = {}
for k, v in perfiles.items():
    GBH[k] = gbh(v)
    pr(f"  {k}: video {v} Mbps + audio 0,128 -> {P(GBH[k],2)} GB por hora ({P(GBH[k]/6*1000,0)} MB cada 10 min)")
pr("  Referencias [verificado]: NIJ 2016: VGA 30 fps 0,55-1,1 GB/h; 720p 1,65-3,3 GB/h. CAST 2018: 10 min HD 350-500 MB = "
   f"{P(0.35*6,1)}-{P(0.5*6,1)} GB/h = {P(350e6*8/600/1e6,1)}-{P(500e6*8/600/1e6,1)} Mbps; 10 min 4K 1.000-1.500 MB")
pr("  YouTube (vivo, 30 fps): 1080p H.265 mín 4 / rec 10 Mbps; H.264 mín 5 / rec 14. 720p H.265 2/6; H.264 3/8 [verificado]")

pr("\n  Densidad de píxeles (px por metro de escena, horizontal) con el teléfono en el pecho [cálculo propio]")
pr("  Umbrales IEC 62676-4 (vía Axis, [probable]): 2014 identificar 250 px/m; 2025 caracterizar 250, validar 500 (verificar personas conocidas, leer patente), escrutar 1.500 (identidad con alta certeza, leer patente)")
pr("  Documento: letra de 2,5 mm con 6 px de alto -> 2.400 px/m [supuesto]")
anchos = {"720p": 1280, "1080p": 1920, "1440p": 2560, "2160p": 3840}
for fov in (70, 100):
    for d in (0.4, 1, 2, 3):
        fila = []
        for k, w in anchos.items():
            pxm = w / (2 * d * math.tan(math.radians(fov / 2)))
            fila.append(f"{k} {P(pxm)}")
        pr(f"   lente {fov}° horizontal, a {d} m: " + " | ".join(fila))

# ---------------------------------------------------------------- 2. Turno, memoria y bloques
pr("\n== 2. Turno completo, memoria libre y bloques de 10 minutos ==")
TURNOS = {6: 22, 8: 22, 12: 15}                      # turnos por mes [supuesto: 5 por semana; 12 h en régimen 12x36]
REC = "1080p30 H.265 5 Mbps (RECOMENDADO)"; ALT = "1080p30 H.264 8 Mbps (alternativa)"; MIN = "720p30 H.265 2,5 Mbps (piso)"
BLOQUE_MIN = 10
for h, tm in TURNOS.items():
    for k in (MIN, REC, ALT):
        g = GBH[k] * h
        libre = 2 * g * 1.10 + 5                     # 2 turnos de margen +10% + 5 GB de sistema [supuesto]
        nb = h * 60 // BLOQUE_MIN
        pr(f"  {h} h | {k}: {P(g,1)} GB por turno; {nb} bloques de {BLOQUE_MIN} min de {P(GBH[k]/6*1000)} MB; memoria libre recomendada {P(libre)} GB; por mes ({tm} turnos) {P(g*tm/1000,2)} TB")

# ---------------------------------------------------------------- 3. Datos móviles
pr("\n== 3. Datos móviles fuera de la base ==")
man = os.path.getsize(D + "_tools/muestra_huella/manifiesto.json")
firma = os.path.getsize(D + "_tools/muestra_huella/firma_ecdsa_p256.b64")
cuerpo = man + firma + 30
pr(f"  Medido con openssl: manifiesto JSON {man} B (dos huellas SHA-256 y SHA-512, hora, GPS, huella del bloque anterior) + firma ECDSA P-256 en base64 {firma} B -> cuerpo {cuerpo} B")
HUELLA_CAL = 2_000                                   # B por bloque con conexión abierta (encabezados HTTP/2, TLS, TCP/IP, acuse) [supuesto]
HUELLA_FRIA = 8_000                                  # B por bloque si hay que abrir la conexión TLS de nuevo [supuesto]
LATIDO = 1_000                                       # B por mensaje de control cada 60 s [supuesto]
esc = {
    "A mínimo (huellas + control)":                          dict(ia_txt=0, ia_voz=0, actas=0, fotos=0, foto_kb=0, margen=0.5),
    "B típico (+10 consultas, 6 actas, 18 fotos reducidas)": dict(ia_txt=5, ia_voz=5, actas=6, fotos=18, foto_kb=250, margen=5),
    "C alto (+30 consultas de voz, 15 actas, 60 fotos)":     dict(ia_txt=0, ia_voz=30, actas=15, fotos=60, foto_kb=400, margen=20),
}
IA_TXT_KB, IA_VOZ_KB, ACTA_KB = 10, 150, 170          # [supuesto]
MB_TURNO = {}
for nombre, e in esc.items():
    for h, tm in TURNOS.items():
        nb = h * 60 // BLOQUE_MIN
        huellas = nb * HUELLA_CAL / 1e6
        huellas_peor = nb * HUELLA_FRIA / 1e6
        control = h * 60 * LATIDO / 1e6
        resto = (e["ia_txt"] * IA_TXT_KB + e["ia_voz"] * IA_VOZ_KB + e["actas"] * ACTA_KB + e["fotos"] * e["foto_kb"]) / 1000 + e["margen"]
        tot = huellas + control + resto
        MB_TURNO[(nombre, h)] = tot
        pr(f"  {nombre} | {h} h: huellas {P(huellas,2)} MB (peor caso {P(huellas_peor,2)}), control {P(control,2)} MB, resto {P(resto,1)} MB -> {P(tot,1)} MB por turno; {P(tot*tm,0)} MB por mes ({tm} turnos)")
pr("  Con bloques de 1 minuto las huellas se multiplican por 10 (8 h: 0,96 MB por turno) [cálculo propio]")

pr("\n  Planes (por línea y mes, pesos de dic-2025):")
planes = {
    "Ciudad, convenio LPU25 renglón 21, M2M 1 GB (AMX, abr-2026)":           (dm(7444.00, "2026-04"), dm(7991.87, "2026-04"), 1),
    "Ciudad, renglón 43, M2M 1 GB asistencia a distancia (Telefónica, jul-2026)": (dm(11163.00, "2026-07"), dm(12876.37, "2026-07"), 1),
    "Ciudad, renglón 6, voz+SMS+5 GB (Telecom, jul-2026)":                 (dm(22423.80, "2026-07"), dm(23933.17, "2026-07"), 5),
    "Ciudad, renglón 20, M2M 5 GB (Telefónica, mar-2026)":                  (dm(24341.10, "2026-03"), dm(27274.00, "2026-03"), 5),
    "Ciudad, renglón 5, voz+SMS+10 GB (Telecom, may-2026)":                 (dm(38636.00, "2026-05"), dm(42802.33, "2026-05"), 10),
    "Movistar Empresas, Plan Control 2 GB, lista 2026 + impuestos x1,235":  (24175 * 1.235 * F_OCT,) * 2 + (2,),
    "Movistar Empresas, Plan Control 4 GB, lista 2026 + impuestos x1,235":  (30300 * 1.235 * F_OCT,) * 2 + (4,),
}
for k, (a, b, gb) in planes.items():
    pr(f"   {k}: {P(a)} a {P(b)} por mes -> {P(a*12)} a {P(b*12)} por año")
DATOS_MIN = planes["Ciudad, convenio LPU25 renglón 21, M2M 1 GB (AMX, abr-2026)"]
DATOS_VOZ = planes["Ciudad, renglón 6, voz+SMS+5 GB (Telecom, jul-2026)"]
DATOS_LISTA = planes["Movistar Empresas, Plan Control 2 GB, lista 2026 + impuestos x1,235"]

# ---------------------------------------------------------------- 4. Subida por wifi
pr("\n== 4. Subida por wifi en la base ==")
EF = 0.85                                            # rendimiento útil de la conexión [supuesto]
for h in TURNOS:
    g = GBH[REC] * h; g2 = GBH[ALT] * h
    fila = " | ".join(f"{x} Mbps: {P(g*8000/(x*EF)/60)} min (H.264: {P(g2*8000/(x*EF)/60)})" for x in (20, 50, 100, 300))
    pr(f"  Turno de {h} h ({P(g,1)} GB H.265): {fila}")
pr("  Ancho de banda para N agentes que vuelven juntos (Mbps útiles) [cálculo propio]")
for h in TURNOS:
    g = GBH[REC] * h
    for N in (50, 150, 450):
        vent = " | ".join(f"en {w} h: {P(N*g*8000/(w*3600)/EF)}" for w in (0.5, 1, 8, 24))
        pr(f"   {h} h H.265, {N} agentes ({P(N*g/1000,2)} TB): {vent}")
pr("  Con H.264 multiplicar por " + P(GBH[ALT]/GBH[REC], 2))

# ---------------------------------------------------------------- 5. Nube en Europa
pr("\n== 5. Guarda en Europa: 6 meses de acceso inmediato + 18 meses de archivo ==")
# precio por GB-mes (decimal) en USD o EUR; ops por objeto; recuperación por GB; mínimo de días
def g(p_gib): return p_gib / GIB
prov = {
 # nombre: (moneda, rápido, archivo, PUT por op (capa rápida), transición por op, recup. rápida/GB, recup. archivo/GB, salida/GB, min rápido, min archivo, demora archivo)
 "Azure Suecia Central (Cold -> Archive)":         ("USD", 0.0036, 0.00099, 0.18/1e4, 0.12/1e4, 0.03, 0.024, 0.087, 90, 180, "hasta 15 h"),
 "Azure Europa Occidental (Cold -> Archive)":      ("USD", 0.0045, 0.0018, 0.18/1e4, 0.12/1e4, 0.03, 0.024, 0.087, 90, 180, "hasta 15 h"),
 "AWS Estocolmo o Irlanda (Glacier IR -> Deep Archive)": ("USD", 0.004, 0.00099, 0.02/1e3, 0.055/1e3, 0.03, 0.02, 0.09, 90, 180, "horas (estándar) [sin confirmar el plazo]"),
 "AWS Fráncfort (Glacier IR -> Deep Archive)":     ("USD", 0.005, 0.0018, 0.02/1e3, 0.06/1e3, 0.03, 0.024, 0.09, 90, 180, "horas [sin confirmar el plazo]"),
 "Google Cloud Bélgica/Finlandia/Países Bajos (Coldline -> Archive)": ("USD", g(0.004), g(0.0012), 0.02/1e3, 0.05/1e3, g(0.02), g(0.05), g(0.12), 90, 365, "milisegundos"),
 "Google Cloud Fráncfort/Estocolmo (Coldline -> Archive)": ("USD", g(0.006), g(0.0025), 0.02/1e3, 0.05/1e3, g(0.02), g(0.05), g(0.12), 90, 365, "milisegundos"),
 "OVHcloud París 3 zonas (Infrequent Access -> Cold Archive)": ("EUR", g(0.0094973), g(0.0016644), 0, 0, g(0.004), g(0.009), 0.0, 30, 180, "[sin confirmar]"),
 "OVHcloud una zona IA -> Cold Archive 3 zonas":   ("EUR", g(0.0040004), g(0.0016644), 0, 0, g(0.004), g(0.009), 0.0, 30, 180, "[sin confirmar]"),
 "Scaleway París (One Zone -> Glacier)":           ("EUR", 0.00803, 0.00254, 0, 0, 0.0, 0.009, 0.01, 0, 0, "[sin confirmar]"),
 "Hetzner Alemania/Finlandia (una sola clase, 24 meses)": ("EUR", 0.00626, 0.00626, 0, 0, 0.0, 0.0, 0.001, 0, 0, "inmediato"),
}
OBJ_MB = GBH[REC] / 6 * 1000                         # MB por bloque de 10 min
OPS_POR_OBJ = math.ceil(OBJ_MB / 16.777216) + 2      # subida en partes de 16 MiB [supuesto]
pr(f"  Bloque de 10 min H.265: {P(OBJ_MB)} MB -> {OPS_POR_OBJ} operaciones de escritura por objeto (partes de 16 MiB) [supuesto]")
LEE_RAP, LEE_ARCH = 0.05, 0.005                      # fracción del video que se baja a la Argentina [supuesto]
def ars(x, mon): return x * (USD if mon == "USD" else EUR)
RES = {}
for nombre, (mon, pf, pa, put, tr, rr, ra, eg, mf, ma, demora) in prov.items():
    ciclo = 6 * pf + 18 * pa                         # por GB producido, en toda su vida
    ops_gb = (OPS_POR_OBJ * put + tr) / (OBJ_MB / 1000)
    lect = LEE_RAP * (rr + eg) + LEE_ARCH * (ra + eg)
    por_tb = (ciclo + ops_gb + lect) * 1000
    RES[nombre] = (mon, ciclo, ops_gb, lect, por_tb, pf, pa)
    pr(f"  {nombre} [{mon}]: rápido {pf:.5f}/GB-mes, archivo {pa:.5f}/GB-mes; ciclo de 24 meses {P(ciclo*1000,1)} por TB; escritura y paso de capa {P(ops_gb*1000,2)} por TB; "
       f"lecturas (5% rápido + 0,5% archivo, con salida a la Argentina) {P(lect*1000,2)} por TB -> TOTAL {P(por_tb,1)} {mon} por TB producido = {P(ars(por_tb, mon))} $ por TB; demora del archivo: {demora}; mínimos {mf}/{ma} días")

pr("\n  Por agente y por año, en régimen (año 3 en adelante) y en el año 1 (pesos de dic-2025):")
def anual(nombre, gb_mes):
    mon, ciclo, ops_gb, lect, por_tb, pf, pa = RES[nombre]
    reg = 12 * gb_mes * (ciclo + ops_gb + lect)
    a1 = 0
    for m in range(1, 13):
        rap = min(m, 6) * gb_mes; arch = max(0, m - 6) * gb_mes
        a1 += rap * pf + arch * pa
    a1 += 12 * gb_mes * (ops_gb + lect)
    return ars(reg, mon), ars(a1, mon)
GUARDA = {}
for h, tm in TURNOS.items():
    for k in (REC, ALT):
        gb_mes = GBH[k] * h * tm
        pr(f"  {h} h, {k}: {P(gb_mes*12/1000,2)} TB por año por agente; en régimen se guardan {P(gb_mes*24/1000,1)} TB por agente")
        for nombre in prov:
            reg, a1 = anual(nombre, gb_mes)
            GUARDA[(h, k, nombre)] = (reg, a1)
            pr(f"     {nombre}: régimen {P(reg)} $/año; año 1 {P(a1)} $")

pr("\n  Costo de borrar antes de tiempo (por GB) [cálculo propio]:")
pr(f"   Google Archive (mínimo 365 días): un bloque que pasó al archivo a los 6 meses y se borra a los 12 paga 6 meses más: {g(0.0012)*6:.5f} USD/GB")
pr(f"   Azure Archive Suecia (mínimo 180 días): borrado a los 9 meses (3 en archivo) paga 3 meses: {0.00099*3:.5f} USD/GB")
pr(f"   AWS Deep Archive Estocolmo (mínimo 180 días): igual, {0.00099*3:.5f} USD/GB")
pr("   Con el plan de 6 + 18 meses no hay cargo: los mínimos (90 días en la capa rápida; 180 o 365 en archivo) se cumplen")
pr("  Recuperar 1 TB del archivo y bajarlo a la Argentina:")
for nombre, (mon, pf, pa, put, tr, rr, ra, eg, mf, ma, demora) in prov.items():
    pr(f"   {nombre}: {P((ra+eg)*1000,1)} {mon} = {P(ars((ra+eg)*1000, mon))} $ ({demora})")

# ---------------------------------------------------------------- 6. Cuenta final por agente
pr("\n== 6. Cuenta final por agente (pesos de dic-2025) ==")
SOPORTE = 25.98 * USD * 1.5                          # Telesin chaleco + pinza, EE. UU., x1,5 importación [supuesto]
BAT10 = 49999 * F_OCT; BAT20 = 54999 * F_OCT         # Cetrogar oct-2026 [verificado]
SD256 = 89000 * F_OCT                                # SanDisk Ultra 256 GB, Carrefour oct-2026 [verificado]
pr(f"  Soporte de pecho {P(SOPORTE)}; batería 10.000 mAh {P(BAT10)}; 20.000 mAh {P(BAT20)}; microSD 256 GB {P(SD256)} (sólo si falta memoria)")
NUBE_REC = "Google Cloud Bélgica/Finlandia/Países Bajos (Coldline -> Archive)"
NUBE_BAR = "Azure Suecia Central (Cold -> Archive)"
NUBE_UE = "OVHcloud una zona IA -> Cold Archive 3 zonas"
for h, tm in TURNOS.items():
    bat = BAT20 if h == 12 else BAT10
    compra = SOPORTE + bat
    compra_sd = compra + SD256
    repos = compra / 2                               # kit cada 2 años [supuesto]
    for k in (REC, ALT):
        for nube in (NUBE_REC, NUBE_BAR, NUBE_UE):
            reg, a1 = GUARDA[(h, k, nube)]
            for dn, (da, db, _) in (("M2M 1 GB", DATOS_MIN), ("voz+5 GB", DATOS_VOZ), ("lista Movistar 2 GB", DATOS_LISTA)):
                datos = (da + db) / 2 * 12
                pr(f"  {h} h | {k.split(' (')[0]} | {nube.split(' (')[0]} | datos {dn}: compra {P(compra)} (con microSD {P(compra_sd)}); por año: datos {P(datos)} + guarda {P(reg)} (año 1: {P(a1)}) + reposición {P(repos)} = {P(datos+reg+repos)}")

pr("\n  TABLA FINAL (1080p H.265; datos M2M 1 GB a precio de la Ciudad; guarda en la nube indicada; reposición del kit cada 2 años):")
for h in TURNOS:
    bat = BAT20 if h == 12 else BAT10
    compra = SOPORTE + bat; repos = compra / 2
    datos = (DATOS_MIN[0] + DATOS_MIN[1]) / 2 * 12
    datos_voz = (DATOS_VOZ[0] + DATOS_VOZ[1]) / 2 * 12
    for nube in (NUBE_REC, NUBE_BAR, NUBE_UE):
        reg, a1 = GUARDA[(h, REC, nube)]
        reg264, a1264 = GUARDA[(h, ALT, nube)]
        pr(f"   {h} h | {nube.split(' (')[0]}: compra {P(compra)}; año 1 {P(datos+a1+repos)}; régimen {P(datos+reg+repos)}; régimen con voz+5 GB {P(datos_voz+reg+repos)}; régimen con H.264 {P(datos+reg264+repos)}")

pr("\n  Batería: consumo de una videollamada 679 a 1.345 mAh por hora (Scientific Reports 2023, material z2) como techo; grabar con la pantalla apagada debería gastar menos [inferencia]")
for nombre, extra in (("solo el teléfono (5.000 mAh)", 0), ("+ batería de 10.000 mAh (60% útil)", 6000), ("+ batería de 20.000 mAh (60% útil)", 12000)):
    pr(f"   {nombre}: {P((5000+extra)/1345,1)} a {P((5000+extra)/679,1)} h")

pr("\n  Guarda por TB [cálculo propio]: el costo de vida completa por TB producido se paga en 2 años; en régimen, cada TB guardado cuesta la mitad por año")
for nombre in (NUBE_REC, NUBE_BAR, "AWS Estocolmo o Irlanda (Glacier IR -> Deep Archive)", NUBE_UE, "Hetzner Alemania/Finlandia (una sola clase, 24 meses)"):
    mon, ciclo, ops_gb, lect, por_tb, pf, pa = RES[nombre]
    pr(f"   {nombre}: {P(ars(por_tb, mon))} $ por TB producido; {P(ars(por_tb, mon)/2)} $ por TB guardado y por año")

pr("\n  Escala (combinación recomendada: 8 h, 1080p H.265, Google Cloud Bélgica, M2M 1 GB) [cálculo propio]")
reg8, a18 = GUARDA[(8, REC, NUBE_REC)]
compra8 = SOPORTE + BAT10
datos8 = (DATOS_MIN[0] + DATOS_MIN[1]) / 2 * 12
for N in (50, 150, 450):
    pr(f"   {N} agentes: compra {M(N*compra8)}; por año en régimen {M(N*(datos8+reg8+compra8/2))} (año 1: {M(N*(datos8+a18+compra8/2))}); video guardado en régimen {P(N*GBH[REC]*8*22*24/1000)} TB")

pr("\n  Estación de descarga en la base (opcional, no por agente): servidor de almacenamiento intermedio [referencia de precios z2, oct-2026]")
NAS = 4699999 * F_OCT; HDD = 1649999 * F_OCT
pr(f"   QNAP 12 bahías {P(NAS)} + 4 discos de 22 TB {P(4*HDD)} = {P(NAS+4*HDD)} (unos 40 TB útiles en RAID 6) [supuesto el armado]")

open(D + "_tools/calculo_salida.txt", "w").write("\n".join(out) + "\n")
