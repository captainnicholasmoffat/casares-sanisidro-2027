# Informe 23 quáter: 200 shows todo el año; mayo a agosto bajo techo (criterio central del investigador de invierno);
# al aire libre cancela sólo la alerta que cubre el horario; si se cancela la nueva fecha, otro 70%; la tercera bajo techo.
# Pesos de dic-2025. Insumos: cachet promedio y % de días con alerta por mes del informe 23 ter (3_shows_calidad_alquiler);
# factor 0,6 «sólo la alerta del horario» (supuesto del mismo investigador); costo de salas del investigador de invierno.
CACHET=0.980112  # M por show (piso SADEM + 25%, mezcla 40/30/30)
alerta={'central':[13,14,10,10,6,4,4,8,7,12,11,13],'bajo':[5,7,5,5,4,1,1,3,3,4,3,4],'alto':[20,21,14,14,8,7,6,13,11,19,19,22]}
HORARIO=0.6
techo={4,5,6,7}  # mayo a agosto (índices 0=ene)
por_mes=200/12
for esc,a in alerta.items():
    afuera=[m for m in range(12) if m not in techo]
    extra=0; 
    for m in afuera:
        p=a[m]/100*HORARIO
        extra+=por_mes*CACHET*(0.7*p+0.7*p*p)   # 70% por la 1.ª cancelación; otro 70% si cae también la 2.ª; la 3.ª va bajo techo
    base=200*CACHET
    print(f"{esc}: shows al aire libre {por_mes*len(afuera):.0f}, bajo techo {por_mes*len(techo):.0f}; cachets base {base:.1f} M + pagos por cancelación {extra:.1f} M = {base+extra:.1f} M por año")
print("Salas en invierno (S1 del investigador): 13,8 M por año (rango 10,5 a 17,6). Producción con 3 equipos: 106,8 M por año. Control contra robos: 2,0 a 2,7 M por año.")
