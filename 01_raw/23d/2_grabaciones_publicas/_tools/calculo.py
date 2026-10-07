# V2 · Costo de difuminar las grabaciones de inspecciones (Programa San Isidro 2027)
# Correr con: python3 -I calculo.py > calculo_salida.txt
# Montos en pesos de diciembre de 2025. Dólar 1.447,84 (BCRA, Com. A 3500, promedio dic-2025).
# Precios en pesos de jul-2026 se deflactan con el IPC del repo (dic-2025 = 10121.3715; jul-2026 = 12076.3937).

USD = 1447.84
DEFL_JUL26 = 10121.3715 / 12076.3937

def ars(usd):
    return usd * USD

def M(x):
    return '%.1f M' % (x / 1e6)

def miles(x):
    return '{:,.0f}'.format(x).replace(',', '.')

print('=== 0. Constantes ===')
print('Dólar: %.2f $; deflactor jul-2026 -> dic-2025: %.5f' % (USD, DEFL_JUL26))

# ---------------------------------------------------------------
print('\n=== 1. Costo de una hora de trabajo municipal (revisión humana) ===')
# Decreto 782/2026 (Anexo IF-2026-00262469-SI-SSRH, art. 6): sueldo básico julio 2026, régimen de 40 h
basico_40h = {'cat 6 administrativo (40 h)': 625405, 'cat 8 administrativo (40 h)': 719501}
FACTOR_COSTO = (13 / 12) * 1.25   # aguinaldo + contribuciones patronales (25%) [supuesto]
HORAS_MES = 40 * 52 / 12
costo_hora = {}
for k, v in basico_40h.items():
    h = v * FACTOR_COSTO / HORAS_MES * DEFL_JUL26
    costo_hora[k] = h
    print('%s: básico jul-26 %s $ -> costo por hora dic-25 %s $ (factor %.3f, %.1f h/mes)' % (k, miles(v), miles(h), FACTOR_COSTO, HORAS_MES))
H_LO = min(costo_hora.values()); H_HI = max(costo_hora.values())
H_MID = (H_LO + H_HI) / 2
print('Rango usado: %s a %s $ por hora (centro %s)' % (miles(H_LO), miles(H_HI), miles(H_MID)))
HORAS_ANIO_FTE = 1760  # horas efectivas por persona y año [supuesto]

# ---------------------------------------------------------------
print('\n=== 2. Volumen de video de inspecciones ===')
DIAS = 22 * 12   # días hábiles por año [supuesto, igual que Z2 y W1b]
esc = {
    'bajo':    dict(agentes=200, insp_dia=4,  minutos=5.0),
    'central': dict(agentes=250, insp_dia=8,  minutos=12.5),
    'alto':    dict(agentes=300, insp_dia=12, minutos=20.0),
}
vol = {}
for k, e in esc.items():
    insp = e['agentes'] * e['insp_dia'] * DIAS
    mins = insp * e['minutos']
    vol[k] = dict(insp=insp, mins=mins, horas=mins / 60, min_por=e['minutos'])
    print('%-8s %d agentes x %d inspecciones/día x %.1f min x %d días = %s inspecciones/año, %s min/año (%s h)' % (
        k, e['agentes'], e['insp_dia'], e['minutos'], DIAS, miles(insp), miles(mins), miles(mins / 60)))

pedidos = {'bajo': 1000, 'central': 10000, 'alto': 50000}   # pedidos de vecinos por año [supuesto]
print('Pedidos a demanda por año [supuesto]:', pedidos, '; duración media 12,5 min')
for k, p in pedidos.items():
    print('  %s: %s pedidos = %.1f%% de las inspecciones del escenario central' % (k, miles(p), 100 * p / vol['central']['insp']))

# ---------------------------------------------------------------
print('\n=== 3. Medición propia de deface 1.5.0 (CPU, onnxruntime 1.30) ===')
# Video sintético 1080p 30 fps de 60 s (caras de una foto de dominio público de la NASA), máquina de 4 vCPU Xeon 2,1 GHz
seg_video = 60.0
medido = {'detección a 1080p (sin --scale)': 455.22, 'detección a 720p (--scale 1280x720)': 216.97,
          'detección a 540p (--scale 960x540)': 152.86, 'detección a 360p (--scale 640x360)': 98.64,
          'sólo recodificar con libx264 (sin detección)': 26.90}
for k, s in medido.items():
    print('%-48s %6.1f s -> %.2f veces la duración del video (4 vCPU)' % (k, s, s / seg_video))
ratio_720_4v = medido['detección a 720p (--scale 1280x720)'] / seg_video
ratio_full_4v = medido['detección a 1080p (sin --scale)'] / seg_video
ratio_enc_4v = medido['sólo recodificar con libx264 (sin detección)'] / seg_video

# ---------------------------------------------------------------
print('\n=== 4. Precio por minuto de video de cada opción (USD) ===')
# Precios oficiales [verificado]: Azure Retail Prices API (West Europe), AWS Price List API (eu-west-1), página de Google
AZ_F16 = 0.776; AZ_F16_SPOT = 0.143405; AZ_F4 = 0.194; AZ_T4 = 0.658; AZ_T4_SPOT = 0.292547   # USD por hora, West Europe
# CPU de 16 vCPU: se supone escala lineal desde la medición de 4 vCPU [supuesto]
cpu16_720 = ratio_720_4v / 4
cpu16_full = ratio_full_4v / 4
# GPU T4 con 4 vCPU: la detección deja de pesar y manda decodificar/difuminar/codificar; se supone 0,5 a 1,0 veces la duración [inferencia]
gpu_lo, gpu_hi = 0.5, 1.0
blur_post = ratio_enc_4v * AZ_F4 / 60   # aplicar el difuminado tras una API de detección: recodificar en 4 vCPU
opciones = {
    'Google Video Intelligence, caras (+ recodificar)': 0.10 + blur_post,
    'Google, caras + texto (pantallas/documentos)': 0.10 + 0.15 + blur_post,
    'AWS Rekognition Video, caras (+ recodificar)': 0.10 + blur_post,
    'AWS Rekognition, caras + texto [inferencia: se cobra por API]': 0.20 + blur_post,
    'Azure Video Indexer (análisis estándar 0,09 + modificación 0,01)': 0.09 + 0.01,
    'deface en CPU 16 vCPU, detección 720p (Azure F16s v2)': cpu16_720 * AZ_F16 / 60,
    'deface en CPU 16 vCPU, detección 720p, spot': cpu16_720 * AZ_F16_SPOT / 60,
    'deface en CPU 16 vCPU, detección 1080p': cpu16_full * AZ_F16 / 60,
    'deface en GPU T4 (Azure NC4as T4 v3), 0,5x': gpu_lo * AZ_T4 / 60,
    'deface en GPU T4, 1,0x': gpu_hi * AZ_T4 / 60,
    'deface en GPU T4 spot, 1,0x': gpu_hi * AZ_T4_SPOT / 60,
}
for k, v in opciones.items():
    print('%-66s US$ %.4f/min = %7.2f $/min = %9s $ por hora de video' % (k, v, ars(v), miles(ars(v) * 60)))
print('Recodificar tras una API (4 vCPU F4s v2): US$ %.5f/min' % blur_post)
print('Google: primeros 1.000 min por mes sin cargo (se descuentan 12.000 min/año)')

# Sighthound Redactor (precio oficial, oct-2026): Pro 2.500 USD/año (1 usuario, escritorio, sin límite de duración);
# Server 3.500 USD/año con 1 usuario, +500 USD por usuario hasta 5
def sighthound(usuarios):
    if usuarios <= 1:
        return 2500
    tramos = (usuarios + 4) // 5     # un servidor cada 5 usuarios [supuesto: Enterprise sin precio publicado]
    return tramos * 3500 + (usuarios - tramos) * 500
print('Sighthound Redactor: 1 usuario %s $/año; 2 usuarios %s $; 5 usuarios %s $' % (
    miles(ars(sighthound(1))), miles(ars(sighthound(2))), miles(ars(sighthound(5)))))

# ---------------------------------------------------------------
print('\n=== 5. Revisión humana (lo que manda en el costo) ===')
REV = {'piso (1,0x)': 1.0, 'central (1,5x, Wisconsin)': 1.5, 'techo (6,0x, Washoe)': 6.0}
for k, r in REV.items():
    print('%-28s por minuto de video: %.0f a %.0f $; inspección de 12,5 min: %s a %s $' % (
        k, r * H_LO / 60, r * H_HI / 60, miles(12.5 * r * H_LO / 60), miles(12.5 * r * H_HI / 60)))

# ---------------------------------------------------------------
print('\n=== 6. Escenario A: difuminar TODAS las inspecciones al subirlas ===')
for k in ['bajo', 'central', 'alto']:
    mins = vol[k]['mins']
    print('-- %s: %s min/año (%s h)' % (k, miles(mins), miles(mins / 60)))
    for nombre in ['Google Video Intelligence, caras (+ recodificar)', 'Azure Video Indexer (análisis estándar 0,09 + modificación 0,01)',
                   'deface en CPU 16 vCPU, detección 720p (Azure F16s v2)', 'deface en GPU T4, 1,0x']:
        m = mins - (12000 if nombre.startswith('Google') else 0)
        print('   %-66s %s por año' % (nombre, M(ars(opciones[nombre] * max(m, 0)))))
    horas_rev = mins / 60 * 1.5
    print('   + revisión humana 1,5x: %s h/año = %.0f personas; %s a %s por año' % (
        miles(horas_rev), horas_rev / HORAS_ANIO_FTE, M(horas_rev * H_LO), M(horas_rev * H_HI)))

# ---------------------------------------------------------------
print('\n=== 7. Escenario B: difuminar A DEMANDA (sólo lo que un vecino pide), con revisión humana ===')
MIN_MEDIA = 12.5
for k, p in pedidos.items():
    mins = p * MIN_MEDIA
    hv = mins / 60
    comp_cpu = ars(opciones['deface en CPU 16 vCPU, detección 720p (Azure F16s v2)'] * mins)
    comp_api = ars(opciones['Google, caras + texto (pantallas/documentos)'] * max(mins - 12000, 0))
    print('-- %s: %s pedidos, %s min de video (%s h)' % (k, miles(p), miles(mins), miles(hv)))
    print('   cómputo: deface CPU %s $; Google caras+texto %s $; Azure %s $' % (
        miles(comp_cpu), miles(comp_api), miles(ars(0.10 * mins))))
    for rk, r in REV.items():
        h = hv * r
        personas = h / HORAS_ANIO_FTE
        usuarios = max(1, int(-(-personas // 1)))
        lic = ars(sighthound(usuarios))
        print('   revisión %-26s %s h = %.2f personas -> trabajo %s a %s; Sighthound (%d usuario/s) %s; total %s a %s' % (
            rk, miles(h), personas, M(h * H_LO), M(h * H_HI), usuarios, M(lic), M(h * H_LO + lic + comp_cpu), M(h * H_HI + lic + comp_cpu)))

# ---------------------------------------------------------------
print('\n=== 8. Costo por inspección pedida (12,5 min), opción recomendada ===')
lic_central = ars(sighthound(2))
rev_c = 12.5 * 1.5 * H_MID / 60
comp_c = ars(opciones['deface en CPU 16 vCPU, detección 720p (Azure F16s v2)'] * 12.5)
print('Revisión 1,5x a costo medio: %s $; cómputo: %s $; licencia prorrateada (2 usuarios, 10.000 pedidos): %s $; total ~%s $' % (
    miles(rev_c), miles(comp_c), miles(lic_central / 10000), miles(rev_c + comp_c + lic_central / 10000)))

# ---------------------------------------------------------------
print('\n=== 9. Ver la inspección: salida de datos desde la nube ===')
GB_H_720 = 1.20      # 720p H.265 2,5 Mbps (W1b)
EGRESS = 0.087       # USD por GB (informe 23b) [verificado allí]
gb = GB_H_720 * MIN_MEDIA / 60
print('Una vista de 12,5 min a 720p: %.2f GB -> US$ %.4f = %.0f $' % (gb, gb * EGRESS, ars(gb * EGRESS)))
for k, p in pedidos.items():
    print('  %s pedidos x 3 vistas cada uno: %s por año' % (miles(p), M(ars(gb * EGRESS * p * 3))))
