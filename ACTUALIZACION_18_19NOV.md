# Actualización del 18 y 19 de noviembre de 2026

Qué cambió en el programa de San Isidro después de la revisión completa del 17/11, por qué, y dónde está. Sirve para
Luján: el método y el código se reusan; los datos, los nombres y las propuestas de San Isidro, no.

Ramas: web, cuentas y plan en `web-sanisidro` (desde el commit 46c68e2); documento en PDF y A4 en
`claude/cool-hopper-3hdk58` (desde a20f59e). Cada cambio tiene su script en `trabajo/` (apply_18nov_a a g,
apply_19nov_a, chat_18nov*, chat_19nov, cuentas_18nov*, cuentas_19nov, despl/apply_plan_18nov*, despl/apply_plan_19nov),
con el texto viejo y el nuevo y la fuente de cada cifra.

## Decisiones de Nick (por id en proyecto/web/data/programa.json)

1. Votación (4.6, Ordenanza 1, cuadros 42 y 44): la primera ronda de asambleas (mes 3) ya se vota con la inteligencia
   artificial del Municipio: módulo de votación con identidad validada por el RENAPER (DNI y prueba de vida, convenio
   por TAD) y tablets con personal del Municipio en cada asamblea y en la delegación de la zona o la más cercana. Si
   falla el RENAPER, el personal mira el DNI contra el padrón. El primer año convoca el Municipio.
2. Funciones nuevas de la IA (4.11, cuadros 14, 28, 42 a 44, 3.4): cada una con su costo, con precios públicos (70,7 M
   por año en el escenario medio, 210,1 en el alto) y su fecha (denuncias e historias, meses 6–9; power users y
   contratos, 7–12; salud mental, 12–18; consulta de lugares, 18–24). La arquitectura y el esqueleto de la IA se
   preparan antes de asumir: eso acorta los plazos.
3. Auditoría en dos contratos (4.11, metodo-notas-4): la de la plataforma y la certificación de cada escalón de la
   partida vecinal (de 15,7 a 62,7 M por año). Las denuncias sobre la obra van a la de la obra; las demás, a la de la
   plataforma.
4. Garantía de alquiler (5.4): lo ya garantizado se paga sólo con el fondo, en orden, nunca con otro dinero.
5. Terrenos sin uso (5.4-r3, Ordenanzas 20 y 21): cuatro trabas y nada de expropiación. Tasa de 4 veces lo que paga una
   casa en un terreno igual (6 si no está mantenido; precedentes: Pilar y Avellaneda), recargo de la Ley 14.449 encima
   para quien no construye, nada de planes ni perdones, cobro judicial con remate (Ley 13.406) y venta sin base si el
   segundo remate queda desierto. Si lo compra el mismo dueño, no se salva: la obligación de construir sigue anotada.
6. Salud mental (5.3, 5.6-r5): acompañante es una opción entre varias para los empleados cuyas tareas libera la IA; el
   primer año es de absorción. La formación es gratis en institutos públicos de la Provincia, dura un año lectivo y pide
   el secundario completo: los primeros acompañan desde el mes 37. Hasta entonces la IA le pasa el resumen sólo al
   profesional.
7. Power users (4.11-r5): tercera fórmula por productividad, sólo para propuestas bien armadas; las multas cuentan, pero
   el vecino cobra un porcentaje sólo de lo efectivamente cobrado.
8. La IA siempre neutral (4.11, gráfico 25, chat): pros y contras; si piden recomendación, sólo mejores prácticas, nunca
   una conclusión propia.
9. Los 60 agentes de seguridad de marzo de 2026 se cuentan desde 2026 (842,8 M en 2026, 1.011,4 M en 2027) en el
   modelo, la planilla y el gráfico 13.
10. Tránsito (5.11): el reductor que elige la zona es obra y lo paga el dinero de obra de la zona; las cámaras, el fondo
    de seguridad vial. La revisión anual puede mudar una cámara, pero la cantidad nunca baja.
11. Seguridad (5.7, 5.9): la patrulla sólo previene y busca el delito; deja los controles de tránsito desde el mes 1.
    Los agentes de tránsito pasan a la patrulla con formación en los meses 4 a 6 (de 40 a 100), y cobran lo mismo que
    sus compañeros de la patrulla (de 62,3 a 504,7 M por año, presupuesto de Seguridad). Nada de retener vehículos por
    faltas menores.
12. El titular del punto 2 de «Qué proponemos hacer» queda como está.

## Lecciones de método (para Luján)

- La web muestra sólo los párrafos que figuran en «orden» de cada apartado. Un script que agrega párrafos tiene que
  agregarlos a «orden»; si no, no se ven y los títulos caen en otro párrafo. Control y arreglo: trabajo/orden_18nov.py.
- Los gráficos de la web son imágenes hechas desde los SVG del documento (trabajo/raster_charts.py): cuando cambian los
  datos, hay que rehacer los SVG (doc/charts.py) y después las imágenes. El 17/11 la web mostró un gráfico viejo.
- El código del modelo tiene que dar lo mismo que los datos parchados: si se cambian datos a mano, se cambia el código
  (03_scripts/modelo.py), o la próxima corrida los pisa.
- Dos revisores independientes (uno de texto, uno de números y plan) encontraron 7 problemas medios y uno grave que
  quien escribió no vio. Revisar siempre con alguien que no escribió.
- El documento se trae de la web con 03_scripts/web_a_doc.py; después hay que mirar a mano filas de cuadros, clases de
  los bloques, recuadros fuera de las columnas y marcas de corte de página.
- Nick, 18/11: nada de mensajes para copiar y pegar entre chats para trabajar; el trabajo lo hacen ayudantes propios.
  Las preguntas, de a una, en texto, sin opciones múltiples, con contexto, lo malo de cada camino y una recomendación.
  Nunca volver a preguntar lo que ya decidió. Las funciones de la IA no llevan nombre propio.
