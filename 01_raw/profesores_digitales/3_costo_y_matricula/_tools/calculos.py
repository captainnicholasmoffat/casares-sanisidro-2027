# Cálculos propios - Pregunta 4 (costo tutor IA San Isidro)
# Todas las fuentes en FUENTES.txt. Supuestos marcados como SUPUESTO.
TC = 1520.0            # BCRA Com. A 3500, 02/10/2026 ($ por US$)
IPC = {'2023-05':1613.5895,'2026-05':11607.3937,'2025-12':10121.3715,'2026-01':10413.0309,'2026-06':11826.4103,'2026-07':12076.3937}
def a_jul26(monto, mes): return monto*IPC['2026-07']/IPC[mes]
def p(usd): return usd*TC

print("== IPC factores ==")
for m in ['2026-01','2026-06']: print(m, round(IPC['2026-07']/IPC[m],4))

# ---------------- MATRÍCULA (DGCyE RA 2025) ----------------
prim_tot, prim_est = 23122, 7980
sec_tot = 24666+2534+511; sec_est = 8607+1615+511
cov_est = prim_est+sec_est; cov_tot = prim_tot+sec_tot
print("\n== Matrícula ==")
print("sec completa tot/est", sec_tot, sec_est, "| cobertura estatal", cov_est, "| total", cov_tot)
# variante amplia (+especial primaria + adultos primaria/secundaria)
cov_est_amp = cov_est+628+479+1036; cov_tot_amp = cov_tot+1073+479+1095
print("amplia est/tot", cov_est_amp, cov_tot_amp)

# ---------------- PRECEDENTES ----------------
print("\n== Precedentes por alumno-año ==")
prec = {
 'ONG EEUU lista con tutor IA': 15.0,
 'Iowa por licencia (3M/200k)': 3e6/200000,
 'Iowa por alumno con acceso (3M/105k)': 3e6/105000,
 'Indiana (1,8M/45.244)': 1.8e6/45244,
 'Indiana (2,0M/45.244)': 2.0e6/45244,
 'Corea min por materia (52.500 KRW/1445,21)': 52500/1445.21,
 'Corea max por materia (90.500 KRW/1445,21)': 90500/1445.21,
 'Estonia por inscripto (4M EUR/20k*1,1255)': 4e6/20000*1.1255,
 'Estonia por activado (4M EUR/7.700*1,1255)': 4e6/7700*1.1255,
 'Goias R$103 (x0,2010)': 103*0.2010, 'Goias R$110 (x0,2010)': 110*0.2010,
 'Nigeria 6 semanas': 48, 'Nigeria año (4 trimestres)': 124, 'Nigeria marginal': 9,
 'Ghana marginal': 5,
}
for k,v in prec.items(): print(f"{k}: US$ {v:,.1f} = $ {p(v):,.0f}")

# ---------------- USO (SUPUESTOS) ----------------
semanas, ses_sem, min_ses = 36, 2, 20           # SUPUESTO base (ref.: Ghana 2x30', Iowa 20-30'/sem)
ses = semanas*ses_sem; minutos = ses*min_ses
turnos, cache_in, nocache_in, out_t = 15, 5000, 1500, 250   # SUPUESTO por turno
rep_in, rep_out = 8000, 600                                 # informe al docente por sesión
C = ses*turnos*cache_in/1e6
U = ses*(turnos*nocache_in+rep_in)/1e6
O = ses*(turnos*out_t+rep_out)/1e6
print(f"\n== Uso == sesiones/año {ses}, minutos/año {minutos}; Mtokens/año: cache {C:.3f} no-cache {U:.3f} salida {O:.4f}")
precios = { # US$ por millón: (entrada, entrada en caché, salida)
 'A chico (0,10/0,01/0,50)': (0.10,0.01,0.50),
 'C bajo costo pico (0,30/0,006/1,20)': (0.30,0.006,1.20),
 'B chico (1/0,10/5)': (1.0,0.10,5.0),
 'A intermedio (2/0,10/10)': (2.0,0.10,10.0),
 'B intermedio (2/0,20/10)': (2.0,0.20,10.0),
 'A grande (10/1/50)': (10.0,1.0,50.0),
}
MOD = 1.10  # SUPUESTO +10% por moderación automática
llm = {}
for k,(i,c,o) in precios.items():
    v = (U*i + C*c + O*o)*MOD; llm[k]=v
    print(f"LLM {k}: US$ {v:.2f}/alumno-año = $ {p(v):,.0f}")

# ---------------- VOZ ----------------
min_tutor_habla, min_alumno_habla, chars_min = 8, 6, 900   # SUPUESTO por sesión
chars = ses*min_tutor_habla*chars_min; stt_min = ses*min_alumno_habla
print(f"\n== Voz == caracteres TTS/año {chars:,}; minutos STT/año {stt_min}")
tts = {'TTS estándar 4/M': 4, 'TTS neural 15/M': 15, 'TTS neural 16/M': 16, 'TTS premium 30/M': 30, 'TTS proveedor D 40/M': 40, 'TTS proveedor D 80/M': 80}
for k,v in tts.items(): print(f"{k}: US$ {chars/1e6*v:.2f}")
stt = {'STT 0,003/min': 0.003*stt_min, 'STT 0,006/min': 0.006*stt_min, 'STT tiempo real 0,017/min': 0.017*stt_min, 'STT nube 3 1 US$/h': stt_min/60*1.0}
for k,v in stt.items(): print(f"{k}: US$ {v:.2f}")
print(f"Voz por minuto de sesión 0,05 US$/min: US$ {0.05*minutos:.1f}; pipeline de voz 0,08 US$/min: US$ {0.08*minutos:.1f}")
voz_base = chars/1e6*15 + 0.017*stt_min
voz_baja = chars/1e6*4 + 0.003*stt_min
voz_alta = 0.08*minutos
print(f"VOZ baja {voz_baja:.2f} base {voz_base:.2f} alta {voz_alta:.2f}")

# ---------------- AVATAR ----------------
min_avatar_habla = ses*min_tutor_habla
print(f"\n== Avatar == minutos/año si se cobra sólo cuando habla: {min_avatar_habla}; si se cobra toda la sesión: {minutos}")
for k,v in {'proveedor F 0,32':0.32,'proveedor F 0,37':0.37,'nube 3 estándar 0,50':0.50,'nube 3 0,625':0.625,'nube 3 HD 0,70':0.70,'nube 3 HD custom 0,80':0.80}.items():
    print(f"avatar {k}: habla US$ {v*min_avatar_habla:,.0f} | sesión completa US$ {v*minutos:,.0f}")
av_baja = 0.0            # avatar 2D animado en el dispositivo (sin costo por minuto; costo fijo de desarrollo)
av_base = 0.50*min_avatar_habla
av_alta = 0.80*minutos

# ---------------- INFRA ----------------
INFRA = 0.15  # SUPUESTO: +15% sobre IA+voz por hosting, base de datos, registros, monitoreo
def esc(llmv, vozv, avv):
    var = (llmv+vozv)*(1+INFRA) + avv
    return var
llm_base = llm['A intermedio (2/0,10/10)']; llm_baja = llm['A chico (0,10/0,01/0,50)']; llm_alta = llm['A grande (10/1/50)']
E = {
 '1 Texto':        (esc(llm_baja,0,0), esc(llm_base,0,0), esc(llm_alta,0,0)),
 '2 Texto+voz':    (esc(llm_baja,voz_baja,0), esc(llm_base,voz_base,0), esc(llm_alta,voz_alta,0)),
 '3 Avatar video': (esc(llm_baja,voz_baja,av_baja), esc(llm_base,voz_base,av_base), esc(llm_alta,voz_alta,av_alta)),
}
print("\n== Costo variable por alumno-año (US$) baja/base/alta ==")
for k,(a,b,c) in E.items(): print(f"{k}: {a:,.2f} / {b:,.2f} / {c:,.2f}  | pesos base $ {p(b):,.0f}")

# ---------------- EQUIPO FIJO ----------------
sipa_jun26 = 2184021.058534571   # promedio s/estacionalidad jun-2026
fte_mes = a_jul26(sipa_jun26,'2026-06')*2       # SUPUESTO perfil técnico = 2x promedio
fte_anio = fte_mes*13*1.24                       # SUPUESTO 13 sueldos + 24% contribuciones
FTE = 11
equipo = FTE*fte_anio
print(f"\n== Equipo fijo == FTE/año $ {fte_anio:,.0f} (US$ {fte_anio/TC:,.0f}); {FTE} FTE = $ {equipo:,.0f} (US$ {equipo/TC:,.0f})")

# ---------------- CAPACITACIÓN ----------------
hc_mes = 19996.73+8113.27+7898.71 + 0.54*19996.73   # hora cátedra semanal secundaria, ene-2026, 10 años antig.
hora_reloj = hc_mes/(52/12)*1.5                      # 4,33 semanas/mes; 1 h reloj = 1,5 h cátedra (40')
hora_reloj_jul = a_jul26(hora_reloj,'2026-01')*1.24
horas_cap = 20
costo_doc = horas_cap*hora_reloj_jul*1.08           # +8% capacitadores (1 cada 25, 20 h a 2x)
doc_tot = 1087 + 3*1213; doc_est = 431 + 3*(459+79+24)
print(f"\n== Capacitación == hora reloj ene-26 $ {hora_reloj:,.0f}; jul-26 c/contrib $ {hora_reloj_jul:,.0f}; por docente $ {costo_doc:,.0f} (US$ {costo_doc/TC:,.0f})")
print(f"docentes estimados: estatal {doc_est}, total {doc_tot}; costo estatal $ {doc_est*costo_doc:,.0f}; total $ {doc_tot*costo_doc:,.0f}")

# ---------------- DISPOSITIVOS Y CONECTIVIDAD ----------------
sin_comp = 64917/295978; sin_int = 26963/295978; sin_nada = 9257/295978
laptop = 472.38; laptop_iva = 505.45; vida = 4
arpu = 1094928670.19*1000/13768437/3     # ingreso por acceso fijo por mes, 2T2026
arpu = a_jul26(arpu,'2026-05')          # 2T2026 centrado en mayo -> julio 2026
conect_anual = arpu*10                   # SUPUESTO 10 meses de ciclo lectivo
print(f"\n== Brecha == sin compu/tablet {sin_comp:.3%}; sin internet vivienda {sin_int:.3%}; sin internet ni celular c/internet {sin_nada:.3%}")
print(f"ARPU internet fijo 2T2026 (a jul-26) $ {arpu:,.0f}/mes; anual (10 meses) $ {conect_anual:,.0f} (US$ {conect_anual/TC:,.0f})")
print(f"laptop anualizada US$ {laptop/vida:,.0f}-{laptop_iva/vida:,.0f} = $ {p(laptop/vida):,.0f}")
for nom,n in [('estatal',cov_est),('total',cov_tot)]:
    nd = n*sin_comp; ni = n*sin_int
    disp_inicial = nd*laptop_iva; disp_anual = nd*laptop_iva/vida; con = ni*conect_anual
    print(f"{nom}: alumnos sin compu {nd:,.0f} sin internet {ni:,.0f}; dispositivos inicial US$ {disp_inicial:,.0f} (anualizado US$ {disp_anual:,.0f}); conectividad $ {con:,.0f}/año (US$ {con/TC:,.0f})")

# ---------------- TOTALES ----------------
print("\n== TOTAL ANUAL (millones de $ y miles de US$) ==")
for nom,n,ndoc in [('Estatal prim+sec',cov_est,doc_est),('Todos prim+sec',cov_tot,doc_tot)]:
    disp_anual = n*sin_comp*laptop_iva/vida*TC; con = n*sin_int*conect_anual; cap = ndoc*costo_doc
    for k,(a,b,c) in E.items():
        ia = [x*n*TC for x in (a,b,c)]
        tot_base = ia[1]+equipo
        tot_base_full = tot_base + cap + disp_anual + con
        print(f"{nom} | {k} | IA variable baja/base/alta $M {ia[0]/1e6:,.1f}/{ia[1]/1e6:,.1f}/{ia[2]/1e6:,.1f} | +equipo base $M {tot_base/1e6:,.1f} (US$k {tot_base/TC/1e3:,.0f}) | +capac+disp+conect $M {tot_base_full/1e6:,.1f} (US$k {tot_base_full/TC/1e3:,.0f}) | por alumno base c/equipo US$ {tot_base/TC/n:,.1f}")
    print(f"   {nom}: capacitación (año 1) $M {cap/1e6:,.1f}; dispositivos anualizados $M {disp_anual/1e6:,.1f}; conectividad $M {con/1e6:,.1f}; equipo $M {equipo/1e6:,.1f}")
    # rangos con equipo
    for k,(a,b,c) in E.items():
        lo = a*n*TC+equipo; hi = c*n*TC+equipo
        print(f"   {k} rango c/equipo: $M {lo/1e6:,.0f} - {hi/1e6:,.0f} | US$k {lo/TC/1e3:,.0f} - {hi/TC/1e3:,.0f}")

print("\n== COSTO TOTAL POR ALUMNO-AÑO (base; capacitación anualizada en 3 años) ==")
for nom,n,ndoc in [('Estatal prim+sec',cov_est,doc_est),('Todos prim+sec',cov_tot,doc_tot)]:
    disp_anual = n*sin_comp*laptop_iva/vida*TC; con = n*sin_int*conect_anual; cap3 = ndoc*costo_doc/3
    for k,(a,b,c) in E.items():
        tot = b*n*TC + equipo + cap3 + disp_anual + con
        print(f"{nom} | {k} | total $M {tot/1e6:,.0f} (US$k {tot/TC/1e3:,.0f}) | por alumno $ {tot/n:,.0f} (US$ {tot/TC/n:,.0f})")
