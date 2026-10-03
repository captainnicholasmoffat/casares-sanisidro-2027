# Estimación [cálculo propio] de actas de tránsito PAGADAS a partir de la recaudación del rubro 1.2.6 MULTAS de San Isidro.
# Supuestos explícitos (ver informe). Ningún rubro separa tránsito.
uf = {  # UF PBA vigente por bimestre (m1_ley_y_montos/valor_unidad_multa_pba_2023_2026.csv)
 2024: [771,771,1010,1010,1137,1137,1230,1230,1299,1299,1336,1336],
 2025: [1398,1398,1452,1452,1416,1416,1435,1435,1606,1606,1711,1711],
}
uf_media = {a: sum(v)/12 for a,v in uf.items()}
recaud = {  # millones de pesos, percibido (m2 presupuesto)
 2024: {'total_126': 4128.0, 'sub_04_via_publica': 2207.9, 'sub_01_contravenciones': 280.3},
 2025: {'total_126': 7857.0, 'sub_04_via_publica': 3361.8, 'sub_01_contravenciones': 535.7},
}
montos_uf = {'bajo (25 UF: senda peatonal, pago voluntario)':25, 'medio (75 UF: velocidad, pago voluntario)':75, 'alto (150 UF: semáforo en rojo, pago voluntario)':150}
partes = {'registro neto 32% (UNSAM/UNSO desde ago-2022)':0.32, 'registro 80% (convenio SACIT 80/20)':0.80, 'registro bruto 100%':1.0}
out=[]
for a in (2024,):
    for base_nom in ('sub_04_via_publica','total_126'):
        base = recaud[a][base_nom]*1e6
        for mn,m in montos_uf.items():
            for pn,p in partes.items():
                por_acta = m*uf_media[a]*p
                n = base/por_acta
                out.append((a,base_nom,mn,pn,round(uf_media[a],1),round(por_acta),round(n)))
print('UF media', {k:round(v,1) for k,v in uf_media.items()})
print('anio|base|monto medio|parte municipal|UF media|$ por acta al Municipio|actas pagadas estimadas')
for r in out: print('|'.join(map(str,r)))
# Escenario central y actas labradas con cobrabilidad 1/3 (Disp. 69/2020 DPPSV: ~1/3 de las actas provinciales 2016-2019 se pagaron)
central = recaud[2024]['sub_04_via_publica']*1e6/(75*uf_media[2024]*0.32)
print('central 2024 pagadas:', round(central), ' labradas si se paga 1/3:', round(central*3))
