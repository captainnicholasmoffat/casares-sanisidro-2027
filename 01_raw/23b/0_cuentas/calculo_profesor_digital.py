# Profesor digital: costo a dólar $1.447,84 (BCRA Com. A 3500, promedio dic-2025), pesos de dic-2025.
# Componentes tomados de los cálculos del informe 23 (modelo, voz y fijos; avatar). Separa lo que está en pesos de lo que está en dólares.
D=1447.84; N=50833
# escenario: pesos sin equipo (conectividad, internet de centros, capacitación), US$ fijos (netbooks amortizadas + servidores), US$ variable (IA y voz), avatar min/max, equipo del informe 23 (M)
E={'c) uso esperado 15%':(8.4+1.93+4.7, 20824+12334, 86811, 65600, 109799, 361.6),
   'd) uso pleno':        (56.1+1.93+4.7, 110971+24668, 409645, 437500, 731995, 482.1)}
EQ27=269.7  # equipo del tutor con los sueldos del cuadro 27 (informe 23, A4 bis)
gratis={'públicas (18.713) + parroquiales y diocesanas (5.595)':18713+5595,
        'públicas (18.713) + sólo parroquiales (3.384)':18713+3384}
priv={'privados que pagan, 2026 (31.234 - 5.595)':31234-5595, 'privados que pagan, sólo parroquiales gratis (31.234 - 3.384)':31234-3384}
for k,(p,uf,uv,a0,a1,eq) in E.items():
    lo=p+(uf+uv+a0)*D/1e6; hi=p+(uf+uv+a1)*D/1e6
    print(f"\n{k}")
    print(f"  sin equipo de personas: {lo:,.1f} a {hi:,.1f} M/año; por alumno inscripto ${lo*1e6/N:,.0f} a ${hi*1e6/N:,.0f}/año (${lo*1e5/N:,.0f} a ${hi*1e5/N:,.0f} por mes, 10 meses)")
    for g,n in gratis.items(): print(f"  gratis {g} = {n:,}: {n*lo/N:,.1f} a {n*hi/N:,.1f} M/año")
    for g,n in priv.items(): print(f"  ingreso si pagan {g} = {n:,}: {n*lo/N:,.1f} a {n*hi/N:,.1f} M/año")
    print(f"  con el equipo del cuadro 27 ({EQ27} M): {lo+EQ27:,.1f} a {hi+EQ27:,.1f} M/año; por alumno ${(lo+EQ27)*1e6/N:,.0f} a ${(hi+EQ27)*1e6/N:,.0f}")
    print(f"  con el equipo del informe 23 ({eq} M): {lo+eq:,.1f} a {hi+eq:,.1f} M/año; por alumno ${(lo+eq)*1e6/N:,.0f} a ${(hi+eq)*1e6/N:,.0f}")
# informes a los docentes
rep=(8000*0.11+600*0.55)/1e6*72*1.10  # US$ por alumno-año: 8.000 tokens de entrada y 600 de salida por sesión, gpt-6-luna con datos en la UE, +10% de control
print(f"\nInformes al docente: tokens US$ {rep:.4f} = ${rep*D:,.0f} por alumno y por año (ya dentro del variable)")
h=19528; print(f"Capacitación paga de 4 h por docente: ${4*h:,} una vez (hora reloj docente $19.528, informe 23); con los cursos gratuitos de Educ.ar: $0")
print(f"4 docentes revisores (cuadro 27, Educación): 93,8 M/año = ${93.8e6/N:,.0f} por alumno y por año (va en el cuadro 27)")
