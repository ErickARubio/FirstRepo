# Brief Visual — El impuesto que no regresa

**Proyecto:** 2026-05-edomex-cdmx
**Agente:** A3 Director Visual
**Fecha:** 2026-05-10
**Estado:** Borrador v1.0
**Input:** script_draft.md v1.0 (aprobado)

---

## Resumen ejecutivo

| Métrica | Valor |
|---------|-------|
| Escenas totales | 14 |
| Mapas a producir | 7 |
| Gráficos y diagramas | 5 |
| Pantallas tipográficas | 3 |
| Imágenes documentales | 0 — video 100% datos |
| Paleta seleccionada | Institucional Moderno (variante ZMVM) |
| Tipografía Display | Inter ExtraBold |
| Tipografía Body | Inter Regular / Medium |
| Tipografía Mono | JetBrains Mono |

**Decisión de dirección:** El video no usa imágenes documentales de personas. Toda la carga visual recae en datos y mapas. Esto refuerza el tono analítico y evita riesgos de licencia o sesgo representacional. La única excepción posible son íconos vectoriales abstractos (trabajador, edificio, casa) para los diagramas.

---

## Sistema de identidad visual

### Paleta — Institucional Moderno (variante ZMVM)

Basada en la Opción B del sistema, con ajuste de acento para el mapa de pobreza y una excepción de fondo oscuro para la escena de apertura (gancho nocturno).

```
Fondo principal:     #FFFFFF    (blanco puro)
Fondo secundario:    #F4F6F9    (gris muy claro — para frames de transición)
Fondo oscuro:        #0D1117    (casi negro — SOLO Escenas 1 y 14, gancho nocturno)
Texto primario:      #0D1B2A    (navy casi negro)
Texto secundario:    #4A6274    (azul gris — labels, fuentes de pie)
Acento principal:    #0072B5    (azul Bloomberg — CDMX, datos centrales)
Acento secundario:   #E8520A    (naranja dato — Edomex, periferia, contraste)
Acento alerta:       #C0392B    (rojo oscuro — pobreza, dato de impacto)
Acento positivo:     #27AE60    (verde — solo si se necesita contraste terciario)
```

**Escalas cromáticas para mapas:**

| Mapa | Escala | Justificación |
|------|--------|---------------|
| PIB por entidad (Escena 3) | Secuencial `#F4F6F9` → `#0072B5` | Variable unidireccional (más PIB = más azul) |
| Flujos Edomex→CDMX (Escenas 1, 6, 14) | Líneas `#E8520A` sobre fondo `#0D1117` (apert.) / `#F4F6F9` (Esc. 6) | Ámbar/naranja sobre oscuro = lectura inmediata |
| Pobreza municipal (Escena 10) | Secuencial `#FFF3CD` → `#C0392B` | Más pobreza = rojo más intenso |
| Tasas ISN (Escena 11) | Divergente `#0072B5` (CDMX 4%) ↔ `#93C6E4` (Edomex 2-3%) | Diferencia de tasa visible a primera vista |
| Precios vivienda (Escena 12) | Secuencial `#FFF3CD` → `#0D1B2A` | Más caro = más oscuro (inversión paleta pobreza) |
| Expansión urbana (Escena 4) | Series temporales: gris (1970) → naranja (1990) → rojo (2020) | Crecimiento como amenaza visual |
| Metro ZMVM (Escena 9) | Líneas con colores oficiales STC sobre fondo gris Edomex | Convención de legibilidad metro |

---

## Sistema tipográfico

### Display — Inter ExtraBold (peso 800)
- **Uso:** números de impacto, títulos de acto, datos en TYPO screens
- **Tamaño en video 1080p:** mínimo 72px para datos grandes, 48px para subtítulos de acto
- **Descarga:** Google Fonts — fonts.google.com/specimen/Inter
- **Ejemplo de uso:** "7,770,000" en Escena 6; "43.5%" en Escena 10

### Body — Inter Regular / Medium (pesos 400 y 500)
- **Uso:** labels de gráficos, notas de fuente en pie de mapa, texto de contexto en diagramas
- **Tamaño en video 1080p:** 28–34px para labels; 22px para fuentes de pie
- **Regla:** texto de fuente siempre en Inter Medium, color `#4A6274`, esquina inferior derecha del frame

### Mono — JetBrains Mono Regular
- **Uso:** fechas en cronologías, valores numéricos en ejes de gráficos, etiquetas de coordenadas
- **Descarga:** Google Fonts — fonts.google.com/specimen/JetBrains+Mono
- **Justificación:** Distingue valores de datos de texto narrativo; mejora legibilidad de números en gráficos

---

## Especificaciones por escena

---

### Escena 1 — Mapa de apertura nocturno

**Tipo:** MAP-FLOW (animado)
**Descripción:** Mapa de la ZMVM en modo nocturno (fondo oscuro). Líneas de flujo en ámbar emergen de los cinco municipios de mayor emigración laboral en Edomex y fluyen hacia las cuatro alcaldías centrales de CDMX. Sin etiquetas de municipio durante la animación. Texto "La frontera invisible" aparece al final del loop.

**Región:** ZMVM (Edomex + CDMX)
**Variable mapeada:** Flujos de viajes por trabajo, origen Edomex → destino CDMX
**Fuente del dato:** EOD 2017, INEGI — tabla de viajes origen-destino por municipio y propósito
**Granularidad:** Municipal
**Paleta:** Fondo `#0D1117`. Territorio Edomex `#1A2035`. Territorio CDMX `#1E2D45`. Líneas de flujo `#E8860A` (ámbar, opacidad 60-100% según volumen). Límite fronterizo CDMX-Edomex: línea punteada `#4A6274`.
**Elementos de UI:** Sin leyenda en esta escena. Sin fuente en pie (se identifica en Escena 6 que tiene el mismo dato con más contexto). Texto overlay: "La frontera invisible" en Inter ExtraBold `#F4F6F9`.
**Animación:** Las líneas de flujo se dibujan desde Edomex hacia CDMX durante 10 seg. Luego el texto aparece con fade-in. Duración total: 15 seg.
**Herramienta sugerida:** Python (geopandas + matplotlib con Basemap) o Flourish Maps. Para animación: After Effects o Motion Bro.
**Shapes necesarios:** Shapefile ZMVM (D7) + tabla EOD 2017 origen-destino (D1)

---

### Escena 2 — Diagrama ISN mecanismo

**Tipo:** DIAGRAM animado (combinación COUNTER + TYPO)
**Descripción:** Diagrama de flujo estático animado. Muestra el mecanismo del ISN: empresa en CDMX paga 4% de nómina al erario capitalino, por todos los trabajadores independientemente de su municipio de residencia.

**Composición del frame:**
- Centro: ícono de edificio de oficinas con etiqueta "Empresa, CDMX"
- Flechas entrantes (abajo): dos íconos de trabajador
  - Trabajador A: casa en "Condesa, CDMX"
  - Trabajador B: casa en "Ecatepec, Edomex"
- Flecha saliente (arriba): "4% ISN" → caja "Erario CDMX"
- Texto en pantalla: "ISN: 4% sobre nómina total" en Inter ExtraBold 72px
- Subtext: "Independientemente del municipio de residencia del trabajador" en Inter Regular 28px

**Animación:** Primero aparece la empresa. Luego los dos trabajadores. Luego la flecha del ISN al erario. Trabajador B tiene línea adicional de puntos que regresa a "Edomex" (para uso en Escena 8).
**Colores:** Empresa en `#0072B5`. Erario CDMX en `#0D1B2A` con texto blanco. Trabajador Condesa en `#4A6274`. Trabajador Ecatepec en `#E8520A` (acento naranja = periferia).
**Fuente visible:** "SAF CDMX / Ley de Hacienda 2025" en pie, Inter Medium 22px, `#4A6274`
**Herramienta sugerida:** Figma (diseño estático) → After Effects (animación de flechas)

---

### Escena 3 — PIB nacional + pastel servicios CDMX

**Tipo:** MAP-COR + CHART-PIE (dos momentos secuenciales, misma escena de 20 seg)
**Descripción parte A (10 seg):** Mapa coroplético de México por entidad, variable PIB 2023. CDMX resaltada. Texto en pantalla con el dato central.

**Región:** México nacional
**Variable mapeada:** PIB por entidad federativa, 2023 (millones de pesos corrientes)
**Fuente del dato:** INEGI, PIBE 2023
**Granularidad:** Estatal
**Paleta parte A:** Secuencial `#F4F6F9` → `#0072B5`. CDMX en `#003D6B` (más oscuro para destacar). Resto de estados en escala proporcional.
**Elementos de UI:** Leyenda de escala (5 intervalos). Texto overlay: "14.8% del PIB nacional" en Inter ExtraBold 72px sobre CDMX. Fuente: "INEGI, PIBE 2023" en pie.
**Shapes necesarios:** Shapefile estatal INEGI (marco geoestadístico) + tabla PIBE 2023

**Descripción parte B (10 seg):** Transición suave a gráfico de pastel. Torta del PIB de CDMX por sector de actividad. Sector servicios iluminado/resaltado.

**Tipo:** CHART-PIE
**Variable:** Composición sectorial del PIB de CDMX 2023
**Series:** Servicios (83.5%), Industria (~13%), Primario (~0.5%) — verificar % exactos en INEGI PIBE 2023
**Colores:** Servicios en `#0072B5` (acento principal). Resto en `#F4F6F9` con borde `#4A6274`. Etiqueta "83.5% servicios" en Inter ExtraBold.
**Anotación:** Flecha o resaltado hacia el segmento de servicios con el porcentaje.
**Herramienta:** Flourish o Datawrapper (más rápido para iteraciones)

---

### Escena 4 — Crecimiento Ecatepec + expansión urbana

**Tipo:** CHART-BAR + MAP animado (dos momentos secuenciales)
**Descripción parte A (12 seg):** Gráfico de barras verticales, población de Ecatepec por año censal.

**Eje X:** Año censal (1970, 1980, 1990, 2000, 2010, 2020)
**Eje Y:** Habitantes (en millones)
**Serie:** Ecatepec de Morelos, Estado de México
**Valores:** 1970: 0.4M | 1980: 0.78M | 1990: 1.22M | 2000: 1.62M | 2010: 1.66M | 2020: 1.65M — verificar con INEGI Censo 2020
**Colores:** Barras en degradado `#93C6E4` (1970) → `#E8520A` (2020). La barra 2020 con etiqueta explícita "1.65M".
**Anotaciones:** Línea horizontal en 400K con etiqueta "1970". Flecha de crecimiento ×4.
**Fuente:** INEGI, Censos de Población 1970-2020.

**Descripción parte B (13 seg):** Mapa estilizado de la ZMVM mostrando expansión de la mancha urbana. Anillos concéntricos desde el centro de CDMX hacia afuera, con años marcados.

**Región:** ZMVM
**Variable:** Expansión de la mancha urbana construida por décadas
**Paleta:** Capas por décadas: núcleo CDMX = `#0D1B2A`, 1970 = `#4A6274`, 1980 = `#0072B5`, 1990 = `#E8520A`, 2000–2020 = `#C0392B`
**Herramienta:** QGIS con datos de uso de suelo histórico (INEGI/CONABIO); alternativa simplificada: ilustración vectorial en Figma

---

### Escena 5 — Pantalla tipográfica editorial

**Tipo:** TYPO
**Descripción:** Pantalla limpia, fondo blanco, dos columnas de texto con contraste conceptual. No hay datos numéricos. Es la única pantalla sin fuente en pie — es una síntesis editorial, no un dato.

**Composición:**
```
[Columna izquierda, color #0072B5]     [Columna derecha, color #E8520A]
CDMX                                   EDOMEX
─────────────────                      ─────────────────
Produce el empleo                      Produce los trabajadores
Se queda con el producto               Se queda con los costos
```

**Tipografía:** Inter ExtraBold para encabezados (CDMX / EDOMEX), 72px. Inter Medium para las líneas de descripción, 36px.
**Elemento gráfico:** Flecha horizontal doble (`→ ←`) en el centro del frame, en `#0D1B2A`. Indica el flujo de extracción.
**Nota:** El texto no aparece de golpe. La columna izquierda entra primero, luego la flecha, luego la columna derecha. 20 seg total.

---

### Escena 6 — Mapa de flujos EOD 2017 (detallado)

**Tipo:** MAP-FLOW (animado, versión diurna con más información)
**Descripción:** Versión expandida del mapa de apertura, ahora con etiquetas de municipios de origen y destino, fondo claro, y contador animado visible.

**Región:** ZMVM
**Variable mapeada:** Viajes diarios laborales por municipio origen (Edomex) → alcaldía destino (CDMX). Propósito: trabajo. Fuente: EOD 2017.
**Granularidad:** Municipal
**Municipios de origen a etiquetar:** Ecatepec, Naucalpan, Tlalnepantla, Nezahualcóyotl, Chimalhuacán, Tultitlán, Ixtapaluca
**Alcaldías destino a etiquetar:** Cuauhtémoc, Miguel Hidalgo, Benito Juárez, Venustiano Carranza
**Paleta:** Fondo `#F4F6F9`. Edomex en `#E8E4DC`. CDMX en `#F4F6F9`. Límite en `#0D1B2A` (línea más gruesa que otros límites). Flechas de flujo en `#E8520A` con opacidad proporcional al volumen (escala logarítmica recomendada).
**Contador animado:** "7,770,000 viajes/día" en Inter ExtraBold 96px, `#0D1B2A`. Aparece después de que se dibujan los flujos.
**Leyenda:** Escala de grosor de flecha con 3 niveles (alto / medio / bajo volumen).
**Fuente en pie:** "INEGI, Encuesta Origen-Destino 2017" — Inter Medium 22px, `#4A6274`
**Herramienta:** Python geopandas + matplotlib (flowmap) o QGIS + complemento FlowMapper. Para animación: After Effects.
**Dataset necesario:** D1 (EOD 2017 microdatos o dataset ajustado WRI F12)

---

### Escena 7 — Timeline jornada laboral

**Tipo:** INFOGRAPH (línea de tiempo horizontal)
**Descripción:** Representación visual del día completo de un trabajador que vive en Ecatepec y trabaja en el Centro Histórico. Muestra cómo el tiempo de traslado come el día.

**Composición:**
- Eje horizontal: 4:00 AM a 10:00 PM (18 horas)
- Hitos con íconos vectoriales y etiquetas:
  - 5:30 AM — ícono de casa (Ecatepec) — "Sale de casa"
  - 7:00 AM — ícono de frontera (línea punteada) — "Cruza a CDMX"
  - 9:00 AM — ícono de edificio (CDMX) — "Llega al trabajo"
  - 6:00 PM — ícono de puerta — "Sale del trabajo"
  - 8:00 PM — ícono de casa — "Regresa a Ecatepec"
- Barras de color debajo del eje:
  - Traslado (5:30–9:00 AM y 6:00–8:00 PM): color `#E8520A` — "3 hrs/día en traslado"
  - Trabajo (9:00 AM–6:00 PM): color `#0072B5` — "9 hrs trabajo"
  - Casa/descanso (8:00 PM–5:30 AM): color `#F4F6F9` con borde — "8.5 hrs"
  - Texto destacado: "14 hrs fuera de casa" en Inter ExtraBold, `#C0392B`
- Texto al pie: "* Estimación basada en tiempo promedio de traslado EOD 2017 y horarios típicos"

**Paleta:** Fondo `#FFFFFF`. Íconos en `#0D1B2A`. Barras como descritas.
**Fuente en pie:** "EOD 2017, INEGI; SEMOVI, Diagnóstico PIM 2019"
**Herramienta:** Figma (diseño) → After Effects (animación de entrada de elementos)

---

### Escena 8 — Diagrama flujo fiscal ISN

**Tipo:** DIAGRAM animado (versión ampliada de Escena 2)
**Descripción:** Diagrama de dos caminos que ilustra el destino diferencial de los impuestos según el municipio de residencia del trabajador.

**Composición:**
- Trabajador A (Condesa): vive en CDMX → trabaja en CDMX → empresa paga ISN 4% a CDMX → usa Metro, Metrobús, servicios CDMX. Flujo: azul `#0072B5`. Círculo completo cerrado.
- Trabajador B (Ecatepec): vive en Edomex → trabaja en CDMX → empresa paga ISN 4% a CDMX → usa servicios de Edomex. Flujo: naranja `#E8520A` para el tramo Edomex; azul para el tramo CDMX. El círculo queda ABIERTO: la flecha del ISN va a CDMX, pero la flecha de uso de servicios regresa a Edomex. Brecha visual explícita.
- Texto central: "El impuesto sigue al trabajo / no al trabajador" en dos líneas, Inter ExtraBold 48px.

**Animación:** Primero se muestra el Trabajador A (flujo completo, azul, círculo cerrado). Luego el Trabajador B (flujo incompleto, la brecha aparece con un "corte" visual animado en la flecha de servicios).
**Herramienta:** After Effects (mejor control de la animación de la brecha)

---

### Escena 9 — Mapa red Metro vs. límite ZMVM

**Tipo:** MAP-FLOW / SCHEME (mapa esquemático)
**Descripción:** Mapa esquemático del STC Metro de CDMX superpuesto sobre el mapa político de la ZMVM. El argumento visual es que las líneas del Metro no cruzan el límite político. El municipio de Edomex que más se acerca al Metro (Ecatepec, Neza) aparece en gris, sin red.

**Región:** ZMVM, zoom en el área de contacto CDMX-Edomex norte y oriente
**Variable mapeada:** Red de estaciones STC Metro (punto) y líneas (segmento) vs. límite político CDMX-Edomex
**Paleta:**
- Fondo CDMX: `#F4F6F9`
- Fondo Edomex: `#E8E4DC` (más gris, más "vacío")
- Líneas Metro: colores oficiales del STC (Línea 1 rosa, Línea 2 azul, etc.) — convención que el espectador reconoce
- Límite CDMX-Edomex: línea punteada gruesa `#C0392B`, 3px — visualmente prominente
- Estaciones: puntos `#0D1B2A`, radio 4px
- Texto sobre Edomex: "SIN COBERTURA DE METRO" en Inter ExtraBold, `#4A6274`, fondo transparente

**Elementos de UI:** Etiqueta "STC Metro" con escala de colores de líneas (leyenda pequeña). Etiquetas de municipios clave de Edomex más cercanos: Ecatepec, Neza. Texto central: "195 estaciones. 0 en Edomex." en Inter ExtraBold 72px, `#C0392B`.
**Fuente en pie:** "STC Metro CDMX; SEDATU, Delimitación ZMVM 2018"
**Herramienta:** QGIS (shapefile Metro disponible en datos.cdmx.gob.mx) + shapefile ZMVM (D7)
**Dataset necesario:** Red vectorizada STC Metro (datos.cdmx.gob.mx/dataset/metro-lineas) + D7

---

### Escena 10 — Mapa de pobreza municipal

**Tipo:** MAP-COR + COUNTER animado
**Descripción:** Mapa coroplético de municipios de la ZMVM, variable porcentaje de población en pobreza (CONEVAL 2023). El contraste visual entre Ecatepec/Neza (rojo oscuro) y alcaldías de CDMX (tono claro) es el argumento.

**Región:** ZMVM (zoom que excluya municipios periféricos de baja densidad demográfica)
**Variable mapeada:** % de población en situación de pobreza, 2023
**Fuente del dato:** CONEVAL, Medición de pobreza municipal 2020 (verificar disponibilidad 2023)
**Granularidad:** Municipal
**Paleta:** Secuencial `#FFF3CD` (0-10% pobreza) → `#F39C12` (20-30%) → `#C0392B` (40%+). Ecatepec y Nezahualcóyotl deben quedar en el extremo rojo.
**Elementos de UI:**
- Leyenda con 5 intervalos y porcentajes
- COUNTER animado que aparece sobre Ecatepec: "43.5% | 786,000 personas | 2° municipio más pobre de México" — en tres líneas, Inter ExtraBold, `#0D1B2A` con fondo blanco semi-transparente
- Comparador en esquina: mini-barra "CDMX promedio: ~27%" vs "Ecatepec: 43.5%"
**Fuente en pie:** "CONEVAL, Medición de pobreza 2020/2023 — verificar año disponible"
**Herramienta:** QGIS o Python geopandas + shapefile municipal INEGI
**Dataset necesario:** D4 (CONEVAL pobreza municipal shapefile)

---

### Escena 11 — Tasas ISN comparativas + valor agregado

**Tipo:** MAP-COR + CHART-BAR (dos momentos secuenciales, 40 seg)
**Descripción parte A (20 seg):** Mapa de tasas ISN por estado/municipio. Dos colores dominantes: CDMX (4%) vs. Edomex (2-3%).

**Región:** Foco en CDMX + municipios limítrofes Edomex
**Variable mapeada:** Tasa ISN vigente 2025
**Fuente:** EY, Matriz ISN 2025; legislación local de cada entidad
**Paleta parte A:** Divergente simplificado. CDMX: `#0072B5` (4%). Edomex: `#93C6E4` (2-3%). Texto en pantalla: "CDMX: 4% | Edomex: 2-3% sobre nómina" en Inter ExtraBold.

**Descripción parte B (20 seg):** Gráfico de barras comparativo de valor agregado promedio por trabajador formal, por sector económico y entidad.

**Eje X:** Sector económico (Servicios financieros CDMX / Servicios profesionales CDMX / Manufactura Edomex / Comercio Edomex)
**Eje Y:** Valor agregado bruto por trabajador (miles de pesos, 2023)
**Paleta parte B:** Barras CDMX en `#0072B5`. Barras Edomex en `#E8520A`. Línea horizontal marcando el promedio nacional.
**Anotación clave:** Flecha indicando "Mayor valor → Mayor ISN → Recaudado por CDMX"
**Fuente:** INEGI, PIBE 2023 por actividad; IMSS datos de empleo formal
**Nota:** Si no hay dato desagregado de valor agregado por trabajador por municipio, usar aproximación sectorial con PIBE estatal / IMSS asegurados.
**Herramienta:** Datawrapper (parte A — mapa) + Flourish (parte B — barras)

---

### Escena 12 — Mapa de precios de vivienda ZMVM

**Tipo:** MAP-COR
**Descripción:** Mapa de precio promedio por m² de vivienda en la ZMVM, por alcaldía/municipio. El gradiente visual desde el centro (caro) hacia la periferia (barato) es el argumento de por qué la gente "elige" vivir en Edomex.

**Región:** ZMVM
**Variable mapeada:** Precio promedio por m² de vivienda, datos recientes (2023-2024)
**Fuente del dato:** SHF (Sociedad Hipotecaria Federal) — Índice de Precios de la Vivienda; INFONAVIT datos de créditos; alternativa: portales inmobiliarios con geocodificación (Lamudi, Inmuebles24) — si se usa, declararlo en pie como "fuente no institucional, referencial"
**Granularidad:** Alcaldía (CDMX) / Municipal (Edomex)
**Paleta:** Secuencial invertida `#F4F6F9` (precio bajo, periferia) → `#0D1B2A` (precio alto, centro CDMX). Benito Juárez y Miguel Hidalgo deben estar en el extremo oscuro.
**Elementos de UI:**
- Leyenda con rangos de precio en pesos/m²
- Marcadores de texto para 2 puntos de referencia: "Benito Juárez: ~$70,000/m²" y "Ecatepec: ~$15,000/m²"
- Ratio en pantalla: "4.5x diferencia de precio" en Inter ExtraBold
**Fuente en pie:** "SHF / INFONAVIT, datos de precio de vivienda — verificar año exacto"
**Herramienta:** QGIS + datos SHF
**Nota de producción:** Este es el dato que requiere mayor verificación antes de Fase 4. Los rangos indicados en el guion son aproximados.

---

### Escena 13 — Pantalla tipográfica "El dato que no existe"

**Tipo:** TYPO (pantalla oscura, texto aparece línea a línea)
**Descripción:** Pantalla negra. Texto aparece progresivamente con pausas dramáticas. Es el momento de mayor tensión narrativa del video. Sin datos, sin fuente, sin gráfico. Solo la pregunta.

**Composición (secuencia de entrada):**
1. (0-5 seg) Pantalla negra
2. (5-15 seg) Aparece: "¿Cuánto del ISN de Ciudad de México viene de trabajo mexiquense?" — Inter ExtraBold 48px, `#F4F6F9`, centrado
3. (15-20 seg) Pausa
4. (20-23 seg) Aparece debajo: "Ese dato no existe." — Inter ExtraBold 72px, `#E8520A`
5. (23-27 seg) Pausa
6. (27-30 seg) Aparece debajo: "Podría calcularse." — Inter Medium 48px, `#93C6E4`

**Fondo:** `#0D1117` (mismo que apertura — cierre visual del círculo)
**Animación:** Fade-in texto. Sin transiciones rápidas. El silencio visual importa.
**Sin fuente en pie en esta escena** — es una observación editorial, no un dato.

---

### Escena 14 — Cierre: mapa de apertura con interrogante

**Tipo:** MAP-FLOW (reutilización de Escena 1 con variaciones)
**Descripción:** El mapa de apertura nocturno regresa. Los flujos de trabajadores siguen ahí. Pero ahora, sobre la línea fronteriza entre CDMX y Edomex, aparece un signo de interrogación grande y pulsante. Fade a negro con texto final.

**Región:** ZMVM (mismo encuadre que Escena 1)
**Cambios respecto a Escena 1:**
- El signo "?" aparece sobre la línea fronteriza (límite CDMX-Edomex) en `#E8520A`, Inter ExtraBold 120px, animación de pulso suave (scale 100% → 105% → 100% en loop)
- Los flujos de traslado siguen activos en el fondo (loop del mismo mapa)
- Texto final aparece en fade lento: "La frontera invisible tiene precio. Nadie lo ha cobrado todavía." — Inter Medium 36px, `#F4F6F9`, centrado en la parte inferior del frame
- Fade a negro en los últimos 5 segundos

**Herramienta:** Reutilizar composición After Effects de Escena 1. Agregar capa de "?" y texto.

---

## Lista de assets a producir

### Mapas (7)

| ID | Escena | Descripción | Dataset necesario | Herramienta |
|----|--------|-------------|-------------------|-------------|
| M01 | 1, 14 | MAP-FLOW ZMVM nocturno — apertura/cierre | D1 (EOD 2017), D7 (shapefile ZMVM) | Python / AE |
| M02 | 3 | MAP-COR PIB por entidad México 2023 | D2 (PIBE 2023) + shapefile estatal INEGI | QGIS / Datawrapper |
| M03 | 4 | MAP estilizado expansión urbana ZMVM (series temporales) | INEGI uso de suelo histórico / vectorial simplificado | QGIS / Figma |
| M04 | 6 | MAP-FLOW ZMVM diurno (detallado, con etiquetas) | D1 (EOD 2017), D7 | Python / AE |
| M05 | 9 | MAP esquemático Metro CDMX vs. límite ZMVM | Red STC Metro vectorizada + D7 | QGIS |
| M06 | 10 | MAP-COR pobreza municipal ZMVM | D4 (CONEVAL), shapefile municipal INEGI | QGIS / Python |
| M07 | 12 | MAP-COR precios de vivienda ZMVM | SHF / INFONAVIT datos vivienda | QGIS / Datawrapper |

### Gráficos (4)

| ID | Escena | Tipo | Dataset | Herramienta |
|----|--------|------|---------|-------------|
| G01 | 3 | CHART-PIE composición PIB CDMX por sector | D2 (PIBE 2023) | Flourish / Datawrapper |
| G02 | 4 | CHART-BAR crecimiento poblacional Ecatepec 1970-2020 | INEGI Censos | Flourish |
| G03 | 11a | MAP-COR tasas ISN por entidad | EY Matriz ISN 2025 + legislación local | Datawrapper |
| G04 | 11b | CHART-BAR valor agregado por trabajador por sector/entidad | D2 (PIBE) + IMSS asegurados | Flourish |

### Diagramas / Infografías (3)

| ID | Escena | Descripción | Herramienta |
|----|--------|-------------|-------------|
| D01 | 2 | Diagrama mecanismo ISN (empresa → ISN → erario) | Figma → AE |
| D02 | 7 | Timeline jornada laboral día típico Ecatepec→CDMX | Figma → AE |
| D03 | 8 | Diagrama flujo fiscal diferencial (Trabajador A vs. B) | After Effects |

### Pantallas tipográficas (3)

| ID | Escena | Descripción | Herramienta |
|----|--------|-------------|-------------|
| T01 | 1 | Texto overlay "La frontera invisible" | AE |
| T02 | 5 | Pantalla dos columnas CDMX / EDOMEX | Figma → AE |
| T03 | 13 | Pantalla oscura "El dato que no existe" (texto progresivo) | After Effects |

---

## Datos a descargar para mapas

| ID | Nombre | Institución | URL | Formato | Prioritario |
|----|--------|-------------|-----|---------|-------------|
| D1 | EOD 2017 microdatos (o dataset ajustado WRI) | INEGI / WRI | inegi.org.mx/programas/eod/2017/ | CSV / shapefile | SÍ — M01, M04 |
| D2 | PIBE 2023 por entidad y sector | INEGI | PIBEF2023.pdf + tabulados | Excel / CSV | SÍ — M02, G01, G04 |
| D3 | Shapefile marco geoestadístico estatal | INEGI | inegi.org.mx (MGE) | Shapefile | SÍ — M02 |
| D4 | Pobreza municipal 2020/2023 | CONEVAL | coneval.org.mx | Excel + shapefile | SÍ — M06 |
| D5 | Red STC Metro vectorizada | Datos CDMX | datos.cdmx.gob.mx | GeoJSON / KML | SÍ — M05 |
| D6 | Shapefile ZMVM (límites municipales) | SEDATU/CONAPO | conapo.gob.mx | Shapefile | SÍ — todos los mapas |
| D7 | Índice precios de vivienda por municipio | SHF / INFONAVIT | shf.gob.mx | Excel | SÍ — M07 |
| D8 | Matriz ISN 2025 por estado | EY (referencia) | ey.com (PDF público) | PDF → manual | SÍ — G03 |

---

## Herramientas de producción recomendadas

| Herramienta | Uso | Por qué |
|-------------|-----|---------|
| QGIS 3.x | Mapas coropléticos y esquemáticos | Gratuito, maneja shapefiles INEGI directamente |
| Python (geopandas + matplotlib) | Mapas de flujo (flow maps) | Mejor control de arcos y opacidades para EOD 2017 |
| Flourish / Datawrapper | Gráficos de barras y pastel | Rapidez de iteración; exporta SVG/PNG de alta calidad |
| Figma | Diagramas, pantallas tipográficas, sistema de diseño | Control pixel-perfect; exporta a AE con plugin |
| After Effects | Animación de todos los assets | Compatibilidad con el flujo AE del Agente A5 |

---

## Notas finales del Director Visual

1. **El metro es el visual más poderoso del video** (Escena 9). Si hay un mapa que vale la pena invertir más tiempo, es ese. El argumento es puramente espacial: las líneas se detienen en una línea invisible y el mapa lo hace irrefutable.

2. **Las Escenas 1 y 14 son el marco visual** — apertura y cierre con el mismo mapa. El "?" en el cierre es la única diferencia. Crear una sola composición AE y reutilizarla reduce el tiempo de producción.

3. **La Escena 13 (pantalla oscura) no tiene datos** — es el momento de mayor riesgo de perder al espectador. El timing de cada línea de texto debe probarse con varios revisores antes de aprobar. Recomiendo 2 segundos de pausa entre cada línea como mínimo.

4. **Verificación prioritaria antes de producir:** El precio de vivienda (Escena 12) y el dato de pobreza 2023 vs. 2020 (Escena 10) deben confirmarse con fuente primaria antes de diseñar los mapas. No producir M06 ni M07 hasta tener los datos verificados.

---

## Registro de revisiones

| Versión | Fecha | Cambio | Solicitado por |
|---------|-------|--------|----------------|
| v1.0 | 2026-05-10 | Borrador inicial | Agente A3 |

---
*Generado por Agente A3 — Sistema de Video-Ensayos Cartográficos*
