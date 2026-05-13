# Hallazgos de Investigación — Las remesas en México
**Proyecto:** 2026-05-remesas-mx
**Tesis seleccionada:** Tesis 2 — La geografía invisible del subsidio migrante
**Agente:** A1 Investigador Económico
**Fecha:** 2026-05-12

---

## Tesis seleccionada

Las remesas no distribuyen riqueza equitativamente: la concentran en los mismos estados expulsores de migrantes desde hace 60 años — Michoacán, Guanajuato, Jalisco, Guerrero — perpetuando una geografía de dependencia que desacopla el consumo local del desarrollo regional. Los estados que más reciben remesas no son los que más crecen económicamente.

---

## Hallazgos principales

### H1 — La misma geografía desde 1964: el circuito se calcificó
El Programa Bracero (1942–1964) movilizó a 4.5 millones de trabajadores mexicanos hacia California, Texas e Illinois — casi todos provenientes de Michoacán, Guanajuato, Jalisco y Zacatecas. El programa terminó. Los circuitos migratorios que generó, no. Hoy, 60 años después, los mismos estados encabezan la lista de receptores de remesas: Michoacán (~$4,273M USD, 2024), Jalisco (~$4,081M), Guanajuato (~$4,071M). La geografía de la migración mexicana lleva seis décadas sin cambiar estructuralmente.

- **Implicación para el video:** El mapa de remesas de 2024 es casi idéntico al mapa de envíos de braceros de 1955. Eso es el gancho visual central.
- **Fuentes:** CONAPO, Índice de Intensidad Migratoria 2020; Banxico SIE, remesas por entidad 2024; National Archives (EEUU), Bracero Program records
- **Estado:** Patrón geográfico verificado; montos exactos 2024 pendientes de confirmar en descarga oficial Banxico

### H2 — El dinero llega pero la economía no despega: correlación inversa
Los estados con mayor dependencia de remesas como porcentaje de su ingreso disponible — Michoacán, Guerrero, Oaxaca, Zacatecas — están consistentemente entre los de menor crecimiento del PIB per cápita. Michoacán tiene un PIB per cápita de aproximadamente 60% de la media nacional (INEGI PIBE 2023). La correlación no es casual: hay literatura académica (CEPAL, BID) que documenta un "efecto trampa" donde las remesas estabilizan el consumo lo suficiente para que la presión de cambio estructural se disipe.

- **Implicación para el video:** Este es el argumento central. Requiere gráfico scatter plot: eje X = remesas/PIB estatal, eje Y = crecimiento PIB per cápita 2010–2023.
- **Fuentes:** INEGI PIBE 2023; Banxico remesas por entidad; CEPAL estudios LAC; BID evaluaciones de impacto
- **Estado:** Relación documentada en literatura; gráfico requiere procesamiento de datos PIBE + Banxico

### H3 — El gasto de las remesas: consumo, no inversión
La ENIGH 2022 permite desagregar el gasto de hogares receptores de remesas. Los estudios basados en ENIGH consistentemente muestran que la mayor parte del ingreso por remesas se destina a consumo básico (alimentación, vivienda, salud, educación básica). La fracción destinada a ahorro o inversión productiva (negocios, tierra, maquinaria) es minoritaria — estimaciones en literatura académica oscilan entre 5–15% dependiendo del estado y año.

No es irresponsabilidad de las familias: las remesas llegan para cubrir lo que el Estado y el mercado local no proveen. Son el sustituto privado de servicios públicos ausentes.

- **Fuentes:** INEGI ENIGH 2022; BID "Remittances as development tool"; CEPAL
- **Estado:** Patrón verificado en literatura; porcentaje exacto requiere procesamiento microdatos ENIGH 2022
- **Nota:** Usar rango conservador (5–15%) y citarlo como "estudios basados en ENIGH", no como cifra puntual propia

### H4 — El efecto de sustitución: remesas como anestesia de la demanda pública
Cuando el flujo de remesas es constante y predecible, reduce la presión que los ciudadanos ejercen sobre sus gobiernos para proveer servicios. Las familias que pueden pagar una clínica privada gracias a las remesas no marchan exigiendo clínicas públicas. Los estados con mayor dependencia de remesas muestran menor inversión pública en infraestructura per cápita que la media nacional — aunque la dirección de causalidad es objeto de debate académico.

- **Fuentes:** SHCP, presupuesto ejercido por entidad; BID estudios de sustitución fiscal; CEPAL "Remesas y gasto público"
- **Estado:** Mecanismo documentado teóricamente; dato empírico específico de Michoacán vs. media nacional requiere cálculo con datos SHCP
- **Nota para el video:** Presentar como mecanismo establecido en literatura, no como hallazgo propio, para mantener rigor sin sobreafirmar

### H5 — El drenaje demográfico: se van los que construirían la economía local
El Censo 2020 (INEGI) muestra que los estados de alta emigración tienen pirámides de edad visiblemente más angostas en el rango 20–40 años (la cohorte más migratoria) que el promedio nacional. Michoacán tiene una de las tasas de emigración internacional más altas del país. Lo que queda en las comunidades de alta emigración son principalmente mujeres, niños y adultos mayores — una estructura demográfica que dificulta la formación de capital humano local y la creación de economías productivas endógenas.

- **Fuentes:** INEGI Censo 2020, pirámides de edad por entidad; CONAPO Índice de Intensidad Migratoria 2020
- **Estado:** Verificable con tabulados del Censo 2020 disponibles en portal INEGI

### H6 — El circuito se autoalimenta: más pobreza → más migración → más remesas
Los municipios con mayor intensidad migratoria (CONAPO) son también los de menor acceso a servicios públicos y mercados laborales locales (CONEVAL). Las remesas no rompen ese ciclo: lo sostienen. Son suficientes para evitar el colapso, pero insuficientes para generar las condiciones que harían innecesaria la migración. El resultado es un equilibrio bajo: ni colapso ni despegue. La trampa se mantiene generación tras generación.

- **Fuentes:** CONAPO Índice de Intensidad Migratoria 2020; CONEVAL Pobreza municipal 2020; literatura académica sobre migración circular
- **Estado:** Marco establecido en literatura; mapa de coincidencia geográfica verificable cruzando shapefile CONAPO + CONEVAL

---

## Cronología relevante

| Año | Evento | Impacto cuantitativo | Fuente |
|-----|--------|---------------------|--------|
| 1942 | Inicia el Programa Bracero EE.UU.-México | 4.5M trabajadores movilizados 1942–1964 | National Archives EE.UU. / CONAPO |
| 1964 | Termina el Programa Bracero | Circuitos migratorios permanecen activos | CONAPO, historia migración |
| 1986 | IRCA (Immigration Reform and Control Act) | Regularización de ~3M mexicanos en EE.UU.; refuerza circuitos establecidos | Pew Research Center |
| 1994 | TLCAN entra en vigor | Migración aumenta por disrupción económica rural; quiebra de pequeños agricultores | CEPAL; CONAPO |
| 2000 | Remesas México superan los $6,500M USD | Primera vez que superan la IED en varios años | Banxico / Banco Mundial |
| 2006 | Crisis financiera EE.UU. se aproxima | Pico de migración indocumentada; remesas en máximo relativo pre-crisis | Pew Research Center |
| 2008–2009 | Recesión EE.UU. | Remesas caen ~15% (única caída importante en la serie) | Banco Mundial WDI |
| 2019 | Remesas superan ingresos petroleros | Primera vez que remesas > petróleo como fuente de divisas | Banxico / SHCP |
| 2020 | Pandemia COVID-19, PIB México -8.5% | Remesas crecen +11% (comportamiento anticíclico) | Banco Mundial; INEGI |
| 2024 | Remesas: $67,637M USD, 3.64% PIB | Máximo histórico | Banco Mundial WDI (verificado) |

---

## Datos para mapas

| Variable | Granularidad | Año | Institución | Acceso |
|----------|-------------|-----|-------------|--------|
| Remesas recibidas por estado (USD) | Estatal | 2024 | Banxico SIE | Descarga manual portal SIE |
| Índice de intensidad migratoria | Municipal | 2020 | CONAPO | Excel + shapefile público |
| PIB per cápita estatal | Estatal | 2023 | INEGI PIBE | Excel tabulados |
| % hogares en pobreza | Municipal | 2020 | CONEVAL | Excel + shapefile público |
| Pirámide de edad cohorte 20-40 | Estatal | 2020 | INEGI Censo | Tabulados portal INEGI |
| % hogares receptores de remesas | Estatal | 2022 | INEGI ENIGH | Microdatos (requieren procesamiento) |

---

## Contraargumentos a anticipar

**Objeción 1: "Las remesas reducen la pobreza, eso es positivo"**
Respuesta con datos: Sí, reducen la pobreza de los hogares individuales — el Banco Mundial documenta que un dólar de remesas reduce la pobreza local más eficientemente que un dólar de gasto gubernamental en contextos débiles. Pero el argumento de la tesis no es que las remesas sean dañinas: es que son el único plan. No hay evidencia de que los estados con alta dependencia de remesas hayan reducido su pobreza estructural más rápido que los estados sin esa dependencia. El bienestar individual no es lo mismo que el desarrollo regional.

**Objeción 2: "La gente puede hacer lo que quiere con su dinero"**
Respuesta: Correcto, y las familias toman decisiones racionales dado su contexto. El problema no es la decisión individual sino la arquitectura de incentivos que el Estado construyó (o dejó de construir) alrededor de ese dinero. El Programa 3x1 Para Migrantes intentó canalizar remesas a proyectos de infraestructura — con resultados mixtos y recursos mínimos comparados con el total del flujo.

**Objeción 3: "Es que Michoacán tiene otros problemas (inseguridad, corrupción)"**
Respuesta: Correcto, y esos problemas son en parte causa y en parte consecuencia del mismo ciclo. La inseguridad en Michoacán empuja a migrar; la dependencia de remesas reduce la base fiscal local para combatir la inseguridad; el ciclo se refuerza. La tesis no afirma que las remesas sean la única causa del estancamiento, sino que son un mecanismo que lo perpetúa.

---

## Vacíos de información

1. **Datos exactos de remesas por estado 2024:** Los montos citados (Michoacán $4,273M) son de referencia periodística; los datos oficiales Banxico requieren descarga del portal SIE y pueden diferir marginalmente.

2. **Correlación remesas/PIB estatal:** La correlación inversa está documentada en literatura pero el cálculo exacto para México 2010–2023 requiere cruzar datasets PIBE + Banxico, lo cual es trabajo de análisis de datos no disponible sin procesamiento.

3. **Composición del gasto ENIGH:** El porcentaje exacto destinado a inversión productiva varía por estudio; usar rango conservador (5–15%) y no afirmar cifra puntual sin procesamiento propio.

4. **Efecto Cherán y otros municipios:** El caso de municipios donde la emigración está disminuyendo (Cherán, algunos municipios de Oaxaca con economías locales autónomas) es real pero requiere datos específicos por municipio que no son fácilmente accesibles.
