# El flujo de caja de San Isidro, en tres párrafos

Pesos constantes de diciembre de 2025. Todo lo que sigue sale de
`data/modelo_flujo_caja.csv` y está explicado en `data/METODOLOGIA_MODELO.md`.

## Qué pasa si no se cambia nada

San Isidro cerró 2025 con un **déficit financiero de 6.051 millones**: gastó
309.236 e ingresó 303.185. No es una crisis —el ahorro corriente fue positivo, de
49.751 millones, y la deuda es de apenas 8.960 millones, el 2,9% del gasto anual—
pero es el primer año en rojo después de un 2024 con superávit de 27.154
millones. Debajo hay dos fuerzas que empujan en direcciones opuestas: los
recursos propios, que son el 68% de los ingresos y crecen al 1,95% real anual
desde 2010, y la coparticipación provincial, que es el 29% y viene perdiendo
peso: la participación de San Isidro en el reparto a los 135 municipios cayó de
1,9378% en 2021 a 1,7731% en 2025, un −2,2% anual compuesto que en los datos
preliminares de 2026 se acelera. Con el gasto real quieto, la primera fuerza gana
y el resultado vuelve a positivo hacia 2028. Pero el margen es fino y depende
enteramente del crecimiento propio: **si los recursos propios crecen un punto
menos por año, el mandato termina en rojo** (−2.946 millones en 2031 en vez de
+10.375). En el escenario adverso —dos puntos menos de crecimiento propio y una
coparticipación que cae al 3,5% anual— el déficit llega a **−20.484 millones en
2031 y −32.257 en 2037**, y ahí ya no alcanza con administrar.

## Qué cuesta el programa

Hoy el Municipio destina a empleo y vivienda **505,7 millones al año**: 170,3 al
programa "Apoyo y promoción al empleo" y 335,4 a "Infraestructura habitacional".
Es el **0,164% del gasto**. Llevarlo al 2,5% del gasto total de forma gradual en
cuatro años cuesta **7.225 millones por año** en régimen —5.680 si el objetivo es
2%, 8.771 si es 3%—. Para dimensionarlo: es el **8,3% del gasto flexible**, que
en 2025 fue de 87.326 millones. No toca personal (34,4% del gasto), ni el
servicio de la deuda (4,6%), ni los contratos plurianuales de servicios (34,1%):
esos tres bloques son el 73,1% del presupuesto y no se mueven dentro de un
ejercicio. El programa entra entero en el 26,9% restante. Dicho de otro modo:
**multiplicar por quince lo que San Isidro gasta hoy en empleo y vivienda cuesta
menos de un peso de cada diez de los que el Municipio sí puede reasignar.**

## De dónde sale la plata

Hay tres caminos y ninguno está elegido acá; los tres están cuantificados en
`data/financiamiento_opciones.csv`. **Reasignar** desde el gasto flexible cubre
el 100% del costo y no cambia el resultado financiero: cambia la composición del
gasto, no su nivel. **Cobrar mejor** es el camino más potente y el que no le saca
nada a nadie: en 2025 quedaron **35.994 millones sin cobrar** —se devengaron
337.149 y se percibieron 301.155, una percepción del 89,3%—, así que subir la
cobranza apenas tres puntos, al 92%, aporta 9.036 millones y **ya cubre el
programa entero con 25% de sobra**; al 95% aporta 19.150 millones y al 97%,
25.893. **Endeudarse** también cubre el costo, pero es el peor de los tres: como
no hay ningún dato en el repo sobre a qué tasa se financia el Municipio, el
modelo corre tres tasas reales (0%, 5% y 10%) y en todas el aporte neto al
resultado cae rápido a medida que entra el servicio de la deuda —de 7.225
millones de crédito tomado, el efecto neto en régimen queda entre 2.529 y 723
millones según la tasa—. La conclusión práctica: **la combinación de reasignación
y mejora de cobranza financia el programa completo sin tomar un peso de deuda y
sin subir una sola alícuota**, y deja además margen para mejorar el resultado
financiero del ejercicio.
