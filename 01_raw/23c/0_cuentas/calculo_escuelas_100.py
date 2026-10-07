# Informe 23 ter, punto 2: profesor digital gratis en públicas y en privadas con aporte del 100%; el resto paga lo que usa, con su parte del equipo.
# Dólar $1.447,84 (BCRA Com. A 3500, promedio dic-2025); pesos de dic-2025. Componentes: informe 23 (modelo, voz y fijos; avatar) e informe 23 bis.
import csv,sys
D=1447.84; EQ=269.7e6  # equipo del tutor con sueldos del cuadro 27
padron=sys.argv[1]
rows=[r for r in csv.DictReader(open(padron,encoding='utf-8')) if r['sector']=='Privado' and r['nivel'] in ('Nivel Primario','Nivel Secundario') and r['modalidad'] in ('Educación Común','Educación Técnico Profesional')]
cien=[r for r in rows if r['subvencion'].strip()=='Subvención Total 100%']
print('Unidades privadas con aporte del 100% (primaria y secundaria, padrón 28/09/2026):')
for r in sorted(cien,key=lambda x:(x['nivel'],x['establecimiento_nombre'])): print(f"  {r['clave']} | {r['establecimiento_nombre']} | {r['nivel']} | {r['matricula']}")
n100=sum(int(r['matricula']) for r in cien); npriv=sum(int(r['matricula']) for r in rows)
PUB=18713  # estatales de primaria y secundaria 2025 (informe 22)
gratis=PUB+n100; pagan=npriv-n100
print(f"Privados con 100%: {n100:,}; privados total: {npriv:,}; pagan: {pagan:,}; gratis (públicas 2025 + 100%): {gratis:,}")
# componentes por escenario (informe 23): usuarios, US$ variable, avatar min/max, US$ servidores, US$ netbooks amortizadas, pesos conectividad+internet centros+capacitación
E={'c) uso esperado 15%':(0.15, 86811,65600,109799, 12334, 20824, (8.4+1.93+4.7)*1e6, 7625),
   'd) uso pleno':(1.0, 409645,437500,731995, 24668, 110971, (56.1+1.93+4.7)*1e6, 50833)}
for k,(u,var,a0,a1,srv,net,pes,uso) in E.items():
    por_uso=[(var+a)/uso*D + srv/uso*D for a in (a0,a1)]   # $ por alumno que lo usa: IA, voz, avatar y servidores
    eq_u=EQ/uso
    print(f"\n{k}")
    print(f"  uso por alumno que lo usa (IA, voz, avatar, servidores): ${por_uso[0]:,.0f} a ${por_uso[1]:,.0f} por año")
    print(f"  parte del equipo por alumno que lo usa: ${eq_u:,.0f} por año (269,7 M / {uso:,} usuarios)")
    pp=[x+eq_u for x in por_uso]
    print(f"  PAGA cada alumno privado que lo usa: ${pp[0]:,.0f} a ${pp[1]:,.0f} por año = ${pp[0]/10:,.0f} a ${pp[1]/10:,.0f} por mes (10 meses) = ${pp[0]/72:,.0f} a ${pp[1]/72:,.0f} por sesión de 20 min (72 sesiones)")
    up=round(pagan*u); ug=round(gratis*u)
    print(f"  privados que lo usan y pagan: {up:,}; ingreso por año: {up*pp[0]/1e6:,.1f} a {up*pp[1]/1e6:,.1f} M (de eso, equipo {up*eq_u/1e6:,.1f} M)")
    fijo=net*D+pes
    cg=[ug*x+fijo for x in por_uso]
    print(f"  COSTO para el Municipio de los gratuitos (sin equipo): usuarios {ug:,} x uso + netbooks, datos, internet de centros y capacitación ({fijo/1e6:,.1f} M) = {cg[0]/1e6:,.1f} a {cg[1]/1e6:,.1f} M por año")
    print(f"  parte del equipo de los gratuitos (va en el cuadro 27): {ug*eq_u/1e6:,.1f} M")
