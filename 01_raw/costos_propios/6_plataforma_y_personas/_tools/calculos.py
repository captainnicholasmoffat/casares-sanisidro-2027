# Cálculos propios A4 / A4 bis. Pesos de diciembre de 2025; US$1 = $1.520 (regla del encargo).
TC=1520
M=lambda usd: usd*TC/1e6   # US$ -> millones de pesos
IPC_dic25=10121.3715; IPC_jul26=12076.3937

# ---------- Población (Censo 2022, data/censo2022_sanisidro_por_radio.csv + otros_niveles) ----------
pob_part=295978; pob_col=1304; pob=pob_part+pob_col
menores15=51388; g15_19=21139
adultos16=pob_part-menores15-g15_19/5+pob_col     # supone edad uniforme en 15-19
print(f"Población 2022: {pob:,}; 16 años o más ≈ {adultos16:,.0f}")

# ---------- Precedentes de uso (conversaciones por habitante y por año) ----------
boti=32422082/3121707
cba=437459*365/268/1505250          # 437.459 gestiones al 24/09/2024 (día 268), anualizado
print(f"Boti 2025: {boti:.2f} conversaciones/hab/año; Córdoba (todos los canales, 2024 anualizado): {cba:.2f}")
esc={'bajo':0.40,'medio':3.0,'alto':round(boti,2)}
PREG_POR_CONV=2.5
preg={k:pob*v*PREG_POR_CONV for k,v in esc.items()}
for k in esc: print(f"  {k}: {pob*esc[k]:,.0f} conversaciones -> {preg[k]:,.0f} preguntas/año")

# ---------- Costo por pregunta ----------
# Supuesto por pregunta: 2 llamadas; 10.000 tokens de entrada sin caché (documentos + historial),
# 6.000 en caché (instrucciones fijas), 2.000 de salida (razonamiento + respuesta).
def costo(pin,pcache,pout,unc=10000,cac=6000,out=2000): return unc*pin/1e6+cac*pcache/1e6+out*pout/1e6
glm=costo(0.15,0.03,0.50)
ds_off=costo(0.15,0.003,0.60); ds_peak=costo(0.30,0.006,1.20); ds=0.9*ds_off+0.1*ds_peak
ds_verb=0.9*costo(0.15,0.003,0.60,out=3000)+0.1*costo(0.30,0.006,1.20,out=3000)
gem=costo(0.75,0.075,3.75)
filtro=1000*0.15/1e6+100*0.5/1e6            # filtro de datos personales / ruteo, modelo chico
dificil=0.05*(20000*1.4/1e6+3000*4.4/1e6)   # 5% de preguntas a GLM-5.3 (grande)
por_preg=glm+filtro+dificil
print(f"\nPor pregunta: GLM-5.3-Flash US$ {glm:.5f}; DeepSeek V4.1 Flash (90% fuera de pico) {ds:.5f} (verborrágico {ds_verb:.5f}); Gemini 3.8 Flash {gem:.5f}")
print(f"  + filtro {filtro:.5f} + 5% difícil {dificil:.5f} = US$ {por_preg:.5f} por pregunta")

# ---------- WhatsApp (utility fuera de la ventana de 24 h: US$0,026; servicio gratis) ----------
reclamos_hoy=36500+37000      # 147 (>100/día) + Centro de Atención al Vecino (37.000 en 2025), según el Municipio
susc=0.05*adultos16
wa_medio=reclamos_hoy*2*2 + susc*24 + 244000*1.0 + 0.10*244000*12 + susc*12
def wa_cost(n_anual):
    m=n_anual/12; tiers=[(100000,0.026),(1000000,0.0247),(4500000,0.0234)]; c=0; prev=0
    for top,p in tiers:
        q=max(0,min(m,top)-prev); c+=q*p; prev=top
    return c*12
wa={'bajo':0.3*wa_medio,'medio':wa_medio,'alto':2.5*wa_medio}
for k,v in wa.items(): print(f"WhatsApp {k}: {v:,.0f} mensajes/año -> US$ {wa_cost(v):,.0f} = $ {M(wa_cost(v)):.1f} M")

# ---------- Audios (25% de preguntas, 30 s; gpt-transcribe US$0,0045/min) ----------
aud={k:preg[k]*0.25*0.5*0.0045 for k in preg}
# ---------- Trabajo de fondo: ingesta, auditoría, escucha, transcripción de 2.000 h de asambleas y sesiones ----------
fondo=2000*60*0.0045 + 300e6*0.15/1e6 + 30e6*0.5/1e6 + 600
print(f"Fondo US$ {fondo:,.0f}")

# ---------- Servidores (Azure Suecia Central, lista, pago por uso) ----------
h=8760
vm=6*0.204*h                    # 6 VM D4s v5: 2 web/API, 2 trabajos/ingesta/embeddings, 1 prueba, 1 respaldo
pg=2*0.374*h                    # PostgreSQL flexible 4 vCore + réplica de alta disponibilidad
pg_disco=1024*0.115*12          # 1 TB (precio de disco no bajado: supuesto similar al de respaldo 0,103)
blob=10240*0.0184*12            # 10 TB caliente
resp=2048*0.103*12              # 2 TB de respaldos
egr=(2400*0.08)*12              # 2,5 TB/mes de salida (100 GB gratis)
cf=200*12                       # Cloudflare Business
video=(60000/1000*5)*12/2 + 3.6e6/1000*1   # Stream: 1.000 h guardadas (promedio medio año) + 3,6 M min vistos
infra=vm+pg+pg_disco+blob+resp+egr+cf+video
print(f"Infra: VM {vm:,.0f} PG {pg:,.0f}+{pg_disco:,.0f} blob {blob:,.0f} resp {resp:,.0f} egr {egr:,.0f} CF {cf:,.0f} video {video:,.0f} = US$ {infra:,.0f} = $ {M(infra):.1f} M")

# ---------- Licencias del equipo (Claude Team: premium US$100, estándar US$20, anual) ----------
lic=34*100*12+15*20*12
print(f"Licencias equipo US$ {lic:,.0f} = $ {M(lic):.1f} M")

# ---------- Cupos ----------
p_txt=10000*0.15/1e6+2000*0.03/1e6+3000*0.5/1e6   # pregunta de asociación (redacción): US$
p_img=0.0389; p_render=0.0389+1000*8/1e6; p_hq=0.2107; p_dat=(60000*1.4+8000*4.4)/1e6+0.03; gb=0.0184
cupo_asoc=3000*p_txt+300*p_img+100*p_render+20*p_hq+60*p_dat+50*gb
print(f"\nPregunta asociación US$ {p_txt:.4f}; análisis US$ {p_dat:.3f}; render {p_render:.4f}")
print(f"Cupo asociación lleno: US$ {cupo_asoc:.2f}/mes = US$ {cupo_asoc*12:,.0f}/año = $ {M(cupo_asoc*12):.2f} M")
tok_dia=lambda t: (0.8*t*0.03+0.15*t*0.15+0.05*t*0.5)/1e6
alum=tok_dia(2e6)*22+100*22*glm      # 2 M tokens/día de agente + 100 preguntas/día con GLM-5.3-Flash, 22 días
emp=tok_dia(10e6)*22+500*p_img+200*p_dat
vec=600*por_preg
print(f"Cupo vecino lleno US$ {vec:.2f}/mes; alumno US$ {alum:.2f}/mes; empresa US$ {emp:.2f}/mes")
N_asoc=70; N_alum=928; N_emp=20; uso=0.4; uso_alum=0.25
asoc_tot=N_asoc*cupo_asoc*12*uso; alum_tot=N_alum*alum*12*uso_alum*(10/12); emp_tot=N_emp*emp*12*uso
print(f"Asociaciones {N_asoc} al 40%: US$ {asoc_tot:,.0f} = $ {M(asoc_tot):.1f} M (lleno $ {M(asoc_tot/uso):.1f} M)")
print(f"Alumnos {N_alum} al 25%, 10 meses: US$ {alum_tot:,.0f} = $ {M(alum_tot):.1f} M")
print(f"Semillero {N_emp} al 40%: US$ {emp_tot:,.0f} = $ {M(emp_tot):.1f} M")

# ---------- Totales por escenario ----------
print("\nTOTAL por escenario (millones de pesos dic-2025)")
for k in ['bajo','medio','alto']:
    llm=preg[k]*por_preg
    var=llm+aud[k]+fondo+wa_cost(wa[k])
    sub=var+infra+lic+asoc_tot+alum_tot+emp_tot
    cont=0.15*(var+infra)
    tot=sub+cont
    nucleo=var+infra+cont
    print(f"   {k} NÚCLEO vecinos (IA+WhatsApp+infra+contingencia) {M(nucleo):.1f} M; + licencias {M(nucleo+lic):.1f} M")
    print(f"{k}: LLM {M(llm):.1f} | audios {M(aud[k]):.1f} | fondo {M(fondo):.1f} | WhatsApp {M(wa_cost(wa[k])):.1f} | infra {M(infra):.1f} | licencias {M(lic):.1f} | asoc {M(asoc_tot):.1f} | alumnos {M(alum_tot):.1f} | semillero {M(emp_tot):.1f} | contingencia {M(cont):.1f} | TOTAL {M(tot):.1f} M vs 193,2 M -> {M(tot)-193.2:+.1f}")

# ---------- Abuso sin límites ----------
print("\nABUSO sin límites (por día y por año)")
for rps in [1,10]:
    d=rps*86400*por_preg; print(f"  robot a {rps} preg/s: US$ {d:,.0f}/día = $ {M(d):.1f} M/día; $ {M(d*365):,.0f} M/año")
for nom,p in [('Muse Image',0.01),('MAI-Image-2.6',0.0389),('GPT Image 2.5',0.2107)]:
    d=150*1440*p; print(f"  imágenes a 150 por minuto con {nom}: US$ {d:,.0f}/día = $ {M(d):.1f} M/día")
d=1000*vec/30; print(f"  1.000 cuentas falsas de vecino al tope: US$ {d*30:,.0f}/mes = $ {M(d*365):.1f} M/año")
d=100000*vec/30; print(f"  100.000 cuentas falsas al tope: $ {M(d*365):.1f} M/año")

# ---------- Personas ----------
Sr,SSr,Jr,Pas=53.10,37.96,23.44,3.16625
print(f"\nInforme 22: 11 FTE = 790,9 M de jul-2026 -> {790.913*IPC_dic25/IPC_jul26:.1f} M de dic-2025; por FTE {71.901*IPC_dic25/IPC_jul26:.1f} M")
filas={'Profesor digital (plataforma: 1 Sr, 2 SSr, 2 Jr)':Sr+2*SSr+2*Jr,'Profesor digital (Educación: 4 docentes revisores, a sueldo Jr)':4*Jr,
'Sellado y cadena de custodia (1 SSr, Seguridad)':SSr,'Multas: módulo aliado del vecino (1 Jr, Servicios)':Jr,
'Multas: operación pública (1 SSr + 3 Jr egresados, Tránsito)':SSr+3*Jr,'Analítica: auditoría de algoritmos (1 SSr, opcional)':SSr,
'Puente con laboratorios (1 SSr)':SSr,'IA que escucha (1 SSr + 1 Jr)':SSr+Jr}
for k,v in filas.items(): print(f"  {k}: {v:.1f} M")
plat=filas['Profesor digital (plataforma: 1 Sr, 2 SSr, 2 Jr)']+SSr+Jr+SSr+SSr+Jr
print(f"  Nuevos en la plataforma (sin analítica): {plat:.1f} M; con analítica {plat+SSr:.1f} M")
print(f"  Nuevos en áreas: {4*Jr+SSr+3*Jr:.1f} M")
# validación de actas
for seg in [30,60,120]:
    hs=244000*seg/3600; print(f"  actas 244.000 a {seg}s: {hs:,.0f} h = {hs/1600:.1f} personas (1.600 h/año)")
