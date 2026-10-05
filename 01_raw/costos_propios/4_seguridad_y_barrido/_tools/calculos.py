# Cálculos propios A2/A5. Pesos de diciembre de 2025 (IPC del repo, dic-2025 = 10121,3715). Dólar $1.520.
import csv
IPC={}
for r in csv.DictReader(open('/tmp/claude-0/-home-user-casares-sanisidro-2027/19687d82-9b19-5a6f-8ec4-f8d897955d9f/scratchpad/ch/wt/data/ipc_indec_mensual.csv')):
    IPC[(int(r['anio']),int(r['mes']))]=float(r['indice'])
D=IPC[(2025,12)]; USD=1520
f=lambda y,m: D/IPC[(y,m)]
M=1e6
print("factores: nov25 %.6f oct24 %.6f jun23 %.6f abr26 %.6f jun26 %.6f jul26(proxy sep26) %.6f ene26 %.6f"%(f(2025,11),f(2024,10),f(2023,6),f(2026,4),f(2026,6),f(2026,7),f(2026,1)))
# Lo de hoy
print("Hoy: 1.200 M; 22%% -> %.1f M/año; cámaras 168,7 M = %.0f $/u dic25; licencia 3.825.756/80 = %.0f"%(1200*0.22,168737624/80,3825756/80))
print("Oracle: 10450/47500 = %.4f"%(10450/47500))
print("Milestone MSRP 2022: Care Plus DL 63/345 = %.4f"%(63/345))
# LP 45/2025 analítica (EXANET): 188.179.200 nov-2025 por 100 licencias + 3 años de soporte
lp45=188179200; amp45=18817920
print("LP45 unit nominal %.0f; dic25 %.0f; total dic25 %.1f M; ampliación 10 jun26 -> dic25 %.1f M"%(lp45/100, lp45/100*f(2025,11), lp45*f(2025,11)/M, amp45*f(2026,6)/M))
extra=40*lp45/100
print("Ampliar 40 (tope 50%%): nominal %.2f M; dic25 %.1f M; techo soporte año 4+: %.1f M/año (1/3 del paquete)"%(extra/M, extra*f(2025,11)/M, extra*f(2025,11)/3/M))
print("LP45 por cámara y año (paquete/3): %.0f $ = US$ %.0f"%(lp45/100*f(2025,11)/3, lp45/100*f(2025,11)/3/USD))
# LP 25/2025 VMS
vms=1083878028; ampvms=351045650.80
print("VMS: adj %.1f M (dic25) + ampl %.1f M (abr26->dic25 %.1f M) = %.1f M; por cámara (2.650) %.0f $"%(vms/M, ampvms/M, ampvms*f(2026,4)/M, (vms+ampvms*f(2026,4))/M, (vms+ampvms*f(2026,4))/2650))
# LP 76/2024 cámaras
lp76=4982871400
print("LP76 presupuesto oficial oct24 %.1f M -> dic25 %.1f M; por cámara (1.788) dic25 %.0f $"%(lp76/M, lp76*f(2024,10)/M, lp76*f(2024,10)/1788))
# Cámaras corporales
print("Mendoza jun-2023: 40 M/200 = 200.000 -> dic25 %.0f $/u"%(200000*f(2023,6)))
s13=200506558.26; s14=138813510.96
print("Salta LP13 (40 cám): %.1f M sep26 -> dic25 (proxy jul26) %.1f M = %.2f M/cám; LP14 (25 cám): %.1f M -> %.1f M = %.2f M/cám"%(s13/M, s13*f(2026,7)/M, s13*f(2026,7)/40/M, s14/M, s14*f(2026,7)/M, s14*f(2026,7)/25/M))
print("Techo llave en mano 80 cámaras: %.0f a %.0f M"%(80*s13*f(2026,7)/40/M, 80*s14*f(2026,7)/25/M))
print("Doc: 2.170.000 ene26 -> dic25 %.0f; x80 = %.1f M"%(2170000*f(2026,1), 80*2170000*f(2026,1)/M))
for anios in (3,4,5):
    print(" reposición cada %d años: %.1f M/año"%(anios,168.737624/anios))
# Mar del Plata mantenimiento (NEC, 24 meses, sep-2026)
mdp=3696e6
print("MdP: %.0f M/año nominal; por cámara-año (1.383) %.0f nominal; dic25 (proxy) %.0f"%(mdp/2/M, mdp/2/1383, mdp/2/1383*f(2026,7)))
# Nube
gmin=30*24*60
print("Google VI etiquetas 24/7: %d min/mes x 0,10 = US$ %.0f/mes = US$ %.0f/año = %.1f M $/cámara/año"%(gmin, gmin*0.10, gmin*0.10*12, gmin*0.10*12*USD/M))
print("AWS streaming events (sólo clips por evento): US$0,00817/min; 24/7 sería US$ %.0f/mes por cámara"%(gmin*0.00817))
# Volumen de video de cámaras corporales (supuestos)
for mbps,h in ((1.5,4),(2.0,6)):
    gbh=mbps*3600/8/1000
    gbm=gbh*h*22
    print("  %.1f Mbps, %d h/día, 22 días: %.2f GB/h, %.0f GB/mes por cámara, %.1f TB/mes y %.0f TB/año las 80"%(mbps,h,gbh,gbm,gbm*80/1000,gbm*80*12/1000))
# WhatsApp (informe 17)
print("WhatsApp: US$2.600/mes = US$31.200/año = %.1f M $/año"%(31200*USD/M))
# Sensores (doc 5.5 vs informe 16)
print("Sensores: 20x500 = US$10.000 = %.1f M (a 1.447,84) / %.1f M (a 1.520); 20x25 = US$500 = %.2f M; diferencia %.1f M"%(10000*1447.84/M, 10000*USD/M, 500*1447.84/M, 9500*1447.84/M))
print("Diag Perú: (5.000+10.000)x1.447,84 = %.1f M ; (15.000+10.000)x1.447,84 = %.1f M"%(15000*1447.84/M, 25000*1447.84/M))
# Nuevos totales
inv_piso=168.737624+extra*f(2025,11)/M
inv_techo=80*s14*f(2026,7)/25/M+extra*f(2025,11)/M
print("Inversión nueva: piso %.1f M, techo %.1f M; diferencia con 1.200: %.1f a %.1f M"%(inv_piso,inv_techo,inv_piso-1200,inv_techo-1200))
for anios in (5,3):
    a=168.737624/anios
    print("Anual nuevo (reposición cada %d años) %.1f M + datos móviles s/p; diferencia con 264: %.1f M"%(anios,a,a-264))
