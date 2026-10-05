# Cálculos propios y1b - modelo de lenguaje, voz, reconocimiento, fijos y escenarios (sin avatar)
# Fuentes: ../FUENTES.txt. Todo lo que no sale de una fuente está marcado SUPUESTO.
import csv
TC = 1520.0  # regla del cliente: US$ 1 = $ 1.520
IPC = {}
for r in csv.DictReader(open('/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/c23_raw/y1b_modelo_voz_fijos/copia_ipc_indec_mensual.csv')):
    IPC[f"{r['anio']}-{r['mes']}"] = float(r['indice'])
DIC25 = IPC['2025-12']
def a_dic25(monto, mes): return monto * DIC25 / IPC[mes]
print("== IPC ==  dic-25", DIC25, "| factores a dic-25: jun-26", round(DIC25/IPC['2026-06'],6), "jul-26", round(DIC25/IPC['2026-07'],6), "ene-26", round(DIC25/IPC['2026-01'],6))

# ---------------- USO (supuestos del cliente / informe 22) ----------------
SEM, SES_SEM, MIN_SES = 36, 2, 20
SES = SEM*SES_SEM                       # 72 sesiones por alumno-año (dosis plena)
TURNOS, CTX, NUEVO, SAL = 15, 5000, 1500, 250
REP_IN, REP_OUT = 8000, 600
# por sesión: el contexto de 5.000 se escribe 1 vez (1er intercambio) y se lee 14 veces
s_uncached = TURNOS*NUEVO + REP_IN            # 30.500
s_write = CTX                                 # 5.000
s_read = (TURNOS-1)*CTX                       # 70.000
s_out = TURNOS*SAL + REP_OUT                  # 4.350
print(f"\n== Tokens por sesión == sin caché {s_uncached}, escritura caché {s_write}, lectura caché {s_read}, salida {s_out}")
print(f"   por alumno-año (72 ses.): sin caché {SES*s_uncached/1e6:.3f} M, escritura {SES*s_write/1e6:.3f} M, lectura {SES*s_read/1e6:.3f} M, salida {SES*s_out/1e6:.4f} M")
MOD = 1.10  # SUPUESTO: +10% por control de seguridad (moderación) sobre el costo del modelo

# precios US$ por millón: (entrada sin caché, escritura caché, lectura caché, salida). Si no hay precio de escritura, se usa el de entrada.
LLM = {
 'DeepSeek V4.1 Flash, API oficial, fuera de pico': (0.15, 0.15, 0.003, 0.60),
 'DeepSeek V4.1 Flash, API oficial, pico': (0.30, 0.30, 0.006, 1.20),
 'DeepSeek V4.1 Flash en Together (EE.UU.)': (0.30, 0.30, 0.006, 1.20),
 'DeepSeek V4 Flash 0731 en DeepInfra (EE.UU.)': (0.06, 0.06, 0.015, 0.18),
 'Qwen3.8-Flash (Alibaba intl., Singapur)': (0.15, 0.1875, 0.015, 0.47),
 'Qwen3.7-Flash (Alibaba intl., <=32K)': (0.03, 0.0375, 0.003, 0.13),
 'GLM-5.3-Flash (Z.ai)': (0.15, 0.15, 0.03, 0.50),
 'Kimi K2.6 (Moonshot)': (0.95, 0.95, 0.16, 4.00),
 'MiniMax-M3': (0.30, 0.30, 0.06, 1.20),
 'Mistral Small 4': (0.15, 0.15, 0.015, 0.60),
 'Mistral Large 3': (0.50, 0.50, 0.05, 1.50),
 'Gemini 3.8 Flash (precio 2027)': (1.50, 1.50, 0.15, 7.50),
 'Gemini 3.5 Flash-Lite': (0.30, 0.30, 0.03, 2.50),
 'gpt-6-luna (OpenAI)': (0.10, 0.125, 0.01, 0.50),
 'gpt-6-luna con residencia UE (+10%)': (0.11, 0.1375, 0.011, 0.55),
 'gpt-6.1-sol (OpenAI)': (2.00, 2.50, 0.10, 10.00),
 'Claude Haiku 4.5': (1.00, 1.25, 0.10, 5.00),
 'Claude Sonnet 5.5': (2.00, 2.50, 0.20, 10.00),
 'gpt-oss-120b en Together (sin caché)': (0.15, 0.15, 0.15, 0.60),
 'Gemma 4 31B en DeepInfra (sin caché)': (0.20, 0.20, 0.20, 0.40),
}
def llm_ses(p):
    i,w,r,o = p
    return (s_uncached*i + s_write*w + s_read*r + s_out*o)/1e6
print("\n== Modelo de lenguaje: US$ por sesión y por alumno-año (72 sesiones), con y sin +10% de moderación ==")
for k,p in LLM.items():
    v = llm_ses(p)
    print(f"{k}: sesión US$ {v:.5f} | año US$ {v*SES:.3f} | año c/moder. US$ {v*SES*MOD:.3f} = $ {v*SES*MOD*TC:,.0f}")

# ---------------- VOZ ----------------
MIN_TUTOR, MIN_ALUMNO, CH_MIN = 8, 6, 900   # CH_MIN: SUPUESTO del informe 22 (rango de proveedores 750-1.000)
ch_ses = MIN_TUTOR*CH_MIN
print(f"\n== Síntesis de voz == caracteres por sesión {ch_ses}; por alumno-año {ch_ses*SES:,}; minutos de tutor por año {MIN_TUTOR*SES}")
TTS = {  # US$ por millón de caracteres
 'Azure Neural (es-AR Elena/Tomás), lista': 15, 'Azure Neural compromiso 400M/mes': 9.75, 'Azure Neural compromiso 2000M/mes (excedente)': 7.5,
 'Azure Neural HD': 22, 'Google Chirp 3 HD (sin es-AR)': 30, 'Google Neural2': 16, 'Amazon Polly Neural (sin es-AR)': 16, 'Amazon Polly Generative': 30,
 'ElevenLabs v4 Turbo / Flash (lista)': 40, 'ElevenLabs v3 / v2 Multilingual': 80, 'Cartesia (plan Scale 299/8M)': 299/8,
 'MiniMax speech-2.8-turbo': 60, 'MiniMax speech-2.8-hd': 100, 'Mistral Voxtral TTS': 16, 'Deepgram Aura-2': 30,
 'Alibaba qwen3-tts-flash (intl.)': 10, 'Alibaba qwen3-tts-instruct-flash': 11.5,
}
for k,v in TTS.items(): print(f"{k}: US$ {v:.2f}/M -> sesión US$ {ch_ses*v/1e6:.4f} | año US$ {ch_ses*SES*v/1e6:.2f}")
# Gemini TTS por audio (25 tokens/s): 3.8 Flash-Lite TTS 2027 US$6/M audio + US$0,50/M texto (aprox. 1 token cada 4 caracteres - SUPUESTO)
g_audio = MIN_TUTOR*60*25*6/1e6; g_text = ch_ses/4*0.5/1e6
print(f"Gemini 3.8 Flash-Lite TTS (2027): sesión US$ {g_audio+g_text:.4f} | año US$ {(g_audio+g_text)*SES:.2f}  (excluido por términos <18)")

print(f"\n== Reconocimiento de voz == minutos de alumno por sesión {MIN_ALUMNO}; por año {MIN_ALUMNO*SES}")
STT = {  # US$ por minuto
 'Azure tiempo real lista (1 US$/h)': 1/60, 'Azure compromiso 2K h (0,80/h)': 0.80/60, 'Azure compromiso 50K h (0,50/h)': 0.50/60,
 'Deepgram Nova-3 multilingüe streaming (promo)': 0.0058, 'Deepgram Nova-3 multilingüe streaming (regular)': 0.0092,
 'Deepgram Nova-3 monolingüe streaming (regular)': 0.0077, 'Deepgram Flux multilingüe': 0.0078,
 'AssemblyAI Universal-Streaming multilingüe (0,15/h)': 0.15/60, 'AssemblyAI Universal-3.6 Pro Realtime (0,45/h)': 0.45/60,
 'ElevenLabs Scribe v2 Realtime (0,39/h)': 0.39/60, 'OpenAI gpt-live-transcribe / realtime-whisper': 0.017,
 'OpenAI gpt-transcribe (no tiempo real)': 0.0045, 'OpenAI gpt-4o-mini-transcribe': 0.003,
 'Google STT V2 estándar (<=500K min/mes)': 0.016, 'Google STT V2 (>2M min/mes)': 0.004,
 'Mistral Voxtral Mini Transcribe Realtime': 0.006, 'Groq whisper-large-v3 (0,111/h)': 0.111/60, 'Groq whisper-large-v3-turbo (0,04/h)': 0.04/60,
 'MiniMax ASR (0,38/h)': 0.38/60, 'Alibaba qwen3-asr-flash (0,000035/s)': 0.000035*60,
}
for k,v in STT.items(): print(f"{k}: US$ {v:.5f}/min -> sesión US$ {v*MIN_ALUMNO:.4f} | año US$ {v*MIN_ALUMNO*SES:.2f}")
print(f"Comparación voz a voz por minuto: gpt-live-1 0,05 US$/min x {MIN_SES*SES} min = US$ {0.05*MIN_SES*SES:.0f} por alumno-año, más el modelo")

# ---------------- PILA RECOMENDADA ----------------
def pila(tts_m, stt_h):
    llm = llm_ses(LLM['gpt-6-luna con residencia UE (+10%)'])*MOD
    tts = ch_ses*tts_m/1e6
    stt = MIN_ALUMNO*stt_h/60
    return llm, tts, stt
for nom,(t,s) in {'lista (pruebas y centros)':(15,1.0),'escala c (400M/mes y 2K h)':(9.75,0.80),'escala d (2000M/mes y 50K h)':(7.5,0.50)}.items():
    l,tt,ss = pila(t,s)
    print(f"\nPila recomendada {nom}: por sesión LLM {l:.4f} + TTS {tt:.4f} + STT {ss:.4f} = US$ {l+tt+ss:.4f}; por alumno-año US$ {(l+tt+ss)*SES:.2f}")
# alternativa abierta/barata: DeepSeek fuera de pico + Groq turbo + TTS propio (costo de servidor aparte)
alt = llm_ses(LLM['DeepSeek V4.1 Flash, API oficial, fuera de pico'])*MOD + MIN_ALUMNO*0.04/60
print(f"Alternativa barata (DeepSeek fuera de pico + Groq turbo, TTS propio aparte): sesión US$ {alt:.4f}; año US$ {alt*SES:.2f}")

# ---------------- CAPACIDAD (para servidor propio) ----------------
VENTANA_H_SEM = 30  # SUPUESTO: uso concentrado 6 h por día hábil
for nom,n in [('c (15%)',50833*0.15),('d (100%)',50833)]:
    h_sem = n*SES_SEM*MIN_SES/60
    conc = h_sem/VENTANA_H_SEM
    print(f"\nConcurrencia {nom}: horas-sesión/semana {h_sem:,.0f}; promedio en ventana {conc:,.0f}; pico x2 {2*conc:,.0f}")
    min_stt = n*MIN_ALUMNO*SES; seg = min_stt*60
    for m,rtf in [('whisper-large-v3',386.26),('whisper-large-v3-turbo',660.78)]:
        gpu_h = seg/rtf/3600
        print(f"   STT {m}: {min_stt:,.0f} min/año; horas-GPU puras (RTFx {rtf}) {gpu_h:,.0f}")
# precios de GPU
print("\nGPU: AWS São Paulo p5.4xlarge (1 H100) 11,5584 US$/h; g4dn.xlarge (T4) 0,894; DeepInfra H100 2,20; Together H100 5,49")
for nom,pr in [('AWS SP H100',11.5584),('DeepInfra H100',2.20)]:
    print(f"   1 GPU sólo en ventana (30 h x 36 sem = {30*36} h): US$ {pr*30*36:,.0f}/año | 24x7: US$ {pr*8760:,.0f}/año")
print(f"   g4dn.xlarge 24x7 6 meses: US$ {0.894*8760/2:,.0f}")

# ---------------- FIJOS ----------------
sipa_jun26 = 2184021.058534571                     # promedio s/est jun-2026 (provisorio)
sipa_dic25 = a_dic25(sipa_jun26,'2026-06')
FTE = sipa_dic25*2*13*1.24                         # SUPUESTO informe 22: perfil técnico = 2x promedio; 13 sueldos; +24% contribuciones
print(f"\n== Equipo == SIPA jun-26 $ {sipa_jun26:,.0f} -> dic-25 $ {sipa_dic25:,.0f}; FTE-año $ {FTE:,.0f} (US$ {FTE/TC:,.0f})")
hc_mes = 19996.73+8113.27+7898.71+0.54*19996.73   # hora cátedra semanal secundaria ene-2026 (informe 22)
hora_reloj = hc_mes/(52/12)*1.5
hora_dic25 = a_dic25(hora_reloj,'2026-01')*1.24
print(f"== Hora docente == ene-26 $ {hora_reloj:,.0f} -> dic-25 con contribuciones $ {hora_dic25:,.0f}")
NET = 10874142/50000                                # San Juan, adenda 2 UNOPS (2026)
print(f"== Netbook == San Juan adenda 2: US$ {NET:,.2f} por unidad; 1ra etapa (alumnos+docentes): US$ {8111036/(25000+5423):,.2f}; adenda 1: US$ {5540929/(19000+1500):,.2f}")
sin_comp = 64917/295978; sin_comp_ni_cel = (2460+8902)/295978; sin_nada = 9257/295978; sin_int = 26963/295978
print(f"== Brecha (Censo 2022, personas) == sin compu/tablet {sin_comp:.3%}; sin compu/tablet NI celular c/internet {sin_comp_ni_cel:.3%}; sin internet en casa {sin_int:.3%}; sin internet NI celular c/internet {sin_nada:.3%}")
pase = 585; pase_dic25 = a_dic25(pase,'2026-07')  # ENACOM sept-2026; se usa el IPC de jul-26 (último disponible)
conect_alumno = SES*pase_dic25
print(f"== Conectividad == pase 50 MB/día $ {pase} (sept-26) -> dic-25 aprox. $ {pase_dic25:,.0f}; por alumno-año (72 días) $ {conect_alumno:,.0f} (US$ {conect_alumno/TC:,.1f})")
inet_centro = a_dic25(31998,'2026-07')*12
print(f"== Internet fijo de centro (300 MB nominal $31.998 sept-26) == $ {inet_centro:,.0f}/año dic-25 (US$ {inet_centro/TC:,.0f})")
srv = {'t3.xlarge':0.3091,'m5.2xlarge':0.704}
print(f"== Servidores app en AWS Buenos Aires == t3.xlarge 24x7 US$ {0.3091*8760:,.0f}/año; m5.2xlarge 24x7 US$ {0.704*8760:,.0f}/año")

# ---------------- ESCENARIOS ----------------
ALUM = 50833
def esc(nombre, inscriptos, activos, ses_activo, fte_anios, n_net_centros, n_net_casa, n_conect, n_centros_inet, educ_cap, h_cap, servers_usd, meses, tts_m, stt_h, cap_opcional=0):
    l,tt,ss = pila(tts_m, stt_h)
    var_usd = activos*ses_activo*(l+tt+ss)
    equipo = fte_anios*FTE
    disp_compra_usd = (n_net_centros+n_net_casa)*NET
    disp_anual_usd = disp_compra_usd/4*(meses/12)            # SUPUESTO: vida útil 4 años
    conect = n_conect*pase_dic25*ses_activo
    inet = n_centros_inet*inet_centro*(meses/12)
    cap = educ_cap*h_cap*hora_dic25
    fijo_ars = equipo + conect + inet + cap + (servers_usd+disp_anual_usd)*TC
    tot_ars = var_usd*TC + fijo_ars
    print(f"\n### {nombre}")
    print(f"  variable (IA+voz) US$ {var_usd:,.0f} = $ {var_usd*TC/1e6:,.1f} M")
    print(f"  equipo {fte_anios} FTE-año $ {equipo/1e6:,.1f} M (US$ {equipo/TC:,.0f})")
    print(f"  dispositivos: compra {n_net_centros+n_net_casa} netbooks US$ {disp_compra_usd:,.0f}; amortizado en el período US$ {disp_anual_usd:,.0f} = $ {disp_anual_usd*TC/1e6:,.1f} M")
    print(f"  conectividad {n_conect:,.0f} chicos $ {conect/1e6:,.1f} M; internet centros $ {inet/1e6:,.2f} M; capacitación {educ_cap} x {h_cap} h $ {cap/1e6:,.1f} M; servidores US$ {servers_usd:,.0f}")
    print(f"  FIJO del período $ {fijo_ars/1e6:,.1f} M (US$ {fijo_ars/TC:,.0f})")
    print(f"  TOTAL del período $ {tot_ars/1e6:,.1f} M (US$ {tot_ars/TC:,.0f})")
    print(f"  por alumno inscripto ({inscriptos:,}) US$ {tot_ars/TC/inscriptos:,.1f} = $ {tot_ars/inscriptos:,.0f} | por alumno activo ({activos:,.0f}) US$ {tot_ars/TC/activos:,.1f} = $ {tot_ars/activos:,.0f}")
    print(f"     de eso variable por activo US$ {var_usd/activos:,.2f}; fijo por activo US$ {fijo_ars/TC/activos:,.1f}")
    if cap_opcional:
        c2 = cap_opcional*4*hora_dic25
        print(f"  opcional: capacitar {cap_opcional:,} docentes de escuela x 4 h = $ {c2/1e6:,.0f} M (US$ {c2/TC:,.0f}) -> + US$ {c2/TC/inscriptos:,.1f} por inscripto")
    return tot_ars

# (a) prueba 6 meses, 2 centros x 100 chicos; 18 semanas x 2 sesiones = 36; 3 FTE x 0,5 año; 2x15 netbooks; 8 educadores x 10 h; 1 t3.xlarge medio año
esc('a) Prueba 6 meses, 2 centros (200 chicos)', 200, 200, 36, 1.5, 30, 0, 0, 2, 8, 10, 0.3091*8760/2, 6, 15, 1.0)
# (b) 6 centros x 100 chicos, año completo; 4 FTE; 90 netbooks; 24 educadores x 10 h; 1 t3.xlarge
esc('b) Los 6 centros (600 chicos), 1 año', 600, 600, 72, 4, 90, 0, 0, 6, 24, 10, 0.3091*8760, 12, 15, 1.0)
# (c) en casa, todos con acceso; 15% usa con dosis plena; 6 FTE; netbooks para el 15% de los que no tienen compu NI celular; conectividad 15% de los sin nada; 2 m5.2xlarge
n_c = round(ALUM*0.15)
esc('c) En casa, todos, uso realista 15%', ALUM, n_c, 72, 6, 90, round(ALUM*sin_comp_ni_cel*0.15), round(ALUM*sin_nada*0.15), 6, 24, 10, 2*0.704*8760, 12, 9.75, 0.80, cap_opcional=4726)
# (d) en casa, todos, dosis plena; 8 FTE; netbooks para todos los sin compu NI celular; conectividad sin nada; 4 m5.2xlarge
esc('d) En casa, todos, uso pleno', ALUM, ALUM, 72, 8, 90, round(ALUM*sin_comp_ni_cel), round(ALUM*sin_nada), 6, 24, 10, 4*0.704*8760, 12, 7.5, 0.50, cap_opcional=4726)
# sensibilidad: netbooks para todo el 21,9% sin compu/tablet en (d)
extra = (round(ALUM*sin_comp)-round(ALUM*sin_comp_ni_cel))*NET
print(f"\nSensibilidad d): netbooks para todo el 21,9% ({round(ALUM*sin_comp):,}) en vez de {round(ALUM*sin_comp_ni_cel):,}: compra extra US$ {extra:,.0f}; anualizado US$ {extra/4:,.0f} (+US$ {extra/4/ALUM:,.1f} por alumno)")
