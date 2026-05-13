# Brief Visual — La geografía invisible del subsidio migrante
**Proyecto:** 2026-05-remesas-mx
**Agente:** A3 Director Visual
**Fecha:** 2026-05-12
**Estado:** Borrador v1.0
**Input:** script_draft.md v1.0 (aprobado)

---

## Resumen ejecutivo

| Métrica | Valor |
|---------|-------|
| Escenas totales | 14 |
| Mapas a producir | 4 |
| Gráficos y diagramas | 7 |
| Imágenes documentales | 3 (2 vía Google Imagen 4, 1 dominio público) |
| Paleta seleccionada | Documental Oscuro (variante remesas) |
| Tipografía Display | Bebas Neue Bold |
| Tipografía Body | Barlow Medium / Regular |
| Tipografía Mono | Barlow Condensed |

**Decisión de dirección:** Paleta oscura. El tema —dinero que mueve millones de vidas sin que ningún gobierno lo controle— requiere peso visual. El dorado como acento único no es decorativo: es la representación cromática de la tesis. Las pantallas de datos sobre fondo negro tienen la gravedad de un informe que nadie quiso publicar.

---

## Sistema de identidad visual

### Paleta — Documental Oscuro (variante remesas)

Basada en la Opción C del sistema. El dorado (`#F5C518`) es el único acento cálido y representa siempre el dinero, las remesas, el flujo. El rojo (`#E63946`) aparece solo para datos de alerta (pobreza, riesgo, fragilidad). El azul frío (`#3A86FF`) es para comparativas institucionales (World Bank, datos macro).

```
Fondo principal:     #121212    (casi negro — base de todas las escenas)
Fondo secundario:    #1E1E1E    (gris oscuro — paneles, diagramas)
Texto primario:      #F2F2F0    (blanco roto — narración, datos)
Texto secundario:    #A0A0A0    (gris claro — labels, fuentes en pie)
Acento remesas:      #F5C518    (dorado — dinero, flujo, dato central)
Acento alerta:       #E63946    (rojo — pobreza, riesgo, fragilidad)
Acento comparativo:  #3A86FF    (azul — datos contextuales, World Bank)
Acento neutro:       #4ECDC4    (teal — terciario, solo si necesario)
```

**Escalas cromáticas para mapas:**

| Mapa | Escala | Justificación |
|------|--------|---------------|
| Remesas por estado (M01) | `#1E1E1E` → `#F5C518` | Más remesas = más dorado |
| PIB per cápita por estado (M02) | `#1E1E1E` → `#3A86FF` | Más PIB = más azul |
| Intensidad migratoria (M03) | `#1E1E1E` → `#F2F2F0` | Flujo migratorio = blanco sobre oscuro |
| EE.UU. riesgo (M04) | Base `#3A86FF` con overlay `#E63946` en riesgo | Concentración azul, amenaza roja |

---

## Sistema tipográfico

### Display — Bebas Neue Bold
- **Uso:** números de impacto, datos grandes, títulos de sección, contador animado
- **Tamaño en 1080p:** 120px para datos de gancho; 72px para datos de anatomía; 48px para labels
- **Descarga:** Google Fonts — fonts.google.com/specimen/Bebas+Neue
- **Ejemplo:** "$67,637,000,000" en Escena 1; "60 AÑOS" en Escena 4

### Body — Barlow Medium / Regular (pesos 400 y 500)
- **Uso:** narración en pantalla (si aplica), labels de gráficos, texto de contexto en diagramas, notas de producción
- **Tamaño en 1080p:** 32px para labels; 24px para fuentes de pie
- **Regla:** fuentes siempre en Barlow Regular, color `#A0A0A0`, esquina inferior derecha

### Mono — Barlow Condensed Regular
- **Uso:** años en cronologías, valores en ejes de gráficos, porcentajes secundarios
- **Descarga:** Google Fonts — fonts.google.com/specimen/Barlow+Condensed
- **Justificación:** Diferencia visualmente valores de datos del texto narrativo

---

## Especificaciones por escena

---

### Escena 1 — Contador de impacto

**Tipo:** COUNTER + TYPO
**Descripción:** Pantalla negra. El número de las remesas aparece primero en dorado. Luego tres líneas de comparación van apareciendo, estableciendo la escala del fenómeno antes de que cualquier imagen llegue.

**Composición (secuencia de 25 seg):**
1. (0–8 seg) Animación de contador: empieza en $0 y sube hasta "$67,637,000,000 USD" en Bebas Neue 120px, dorado `#F5C518`. Fondo `#121212`.
2. (8–15 seg) Aparecen tres líneas de comparación en Barlow 32px, `#A0A0A0`:
   - "Mayor que todos los ingresos petroleros de México"
   - "Mayor que la inversión extranjera directa"
   - "Primera fuente de divisas del país"
3. (15–25 seg) Transición suave al mapa de Escena 2.

**Fuente visible:** "Banco Mundial, BX.TRF.PWKR.CD.DT, 2024" — Barlow Regular 22px, `#A0A0A0`, esquina inferior derecha.
**Herramienta:** After Effects (animación de contador con expresión Math.round)

---

### Escena 2 — Mapa doble: remesas vs. crecimiento económico

**Tipo:** MAP-COR (dos mapas superpuestos en secuencia)
**Descripción:** El argumento visual central del video. Primero el mapa de remesas por estado (dorado). Luego, en transición suave, el mapa de crecimiento del PIB per cápita (azul). Los mismos estados dominan ambas escalas — pero en sentidos opuestos. El texto final es el punch: "El mapa del dinero es el mapa del estancamiento."

**Mapa A — Remesas por estado 2024:**
- **Región:** México nacional (32 estados)
- **Variable:** Monto de remesas recibidas 2024 (millones USD)
- **Fuente del dato:** Banxico SIE, series por entidad, 2024
- **Granularidad:** Estatal
- **Paleta:** Secuencial `#1E2020` (mínimo) → `#F5C518` (máximo). Los 5 estados top (Michoacán, Jalisco, Guanajuato, CDMX, Edomex) en el extremo dorado.
- **Elementos de UI:** Leyenda 5 intervalos. Etiquetas de los 5 estados top con monto aproximado. Título: "Remesas recibidas 2024 (USD)" en Barlow Medium 32px.
- **Herramienta:** Python geopandas + matplotlib / Datawrapper Maps

**Mapa B — Crecimiento PIB per cápita 2010–2023:**
- **Región:** México nacional
- **Variable:** Crecimiento % PIB per cápita 2010–2023 (o tasa anual promedio)
- **Fuente del dato:** INEGI PIBE 2023
- **Paleta:** Secuencial `#1E2020` (mínimo crecimiento) → `#3A86FF` (máximo). Los mismos 5 estados del mapa A aparecen en el extremo oscuro (bajo crecimiento).
- **Transición:** Crossfade de 2 segundos entre Mapa A y Mapa B. El espectador ve que los estados dorados se vuelven oscuros.
- **Texto final:** "El mapa del dinero es el mapa del estancamiento." — Bebas Neue 72px, `#F2F2F0`, centrado, fade-in.
- **Fuente visible:** "Banxico SIE 2024 / INEGI PIBE 2023"
- **Dataset necesario:** D1 (Banxico remesas por estado) + D3 (PIBE 2023) + shapefile estatal INEGI

---

### Escena 3 — Imagen histórica: Programa Bracero

**Tipo:** IMG-DOC (imagen histórica, dominio público)
**Descripción:** Imagen de época blanco y negro del Programa Bracero: trabajadores mexicanos en campo agrícola de California o Texas, 1940s–1960s. Sobreimpresión de datos del programa.

**Búsqueda de imagen:**
- **Fuente primaria:** Library of Congress (loc.gov) — búsqueda: "Bracero Program Mexican workers California" — dominio público, sin restricción
- **Alternativa:** National Archives (archives.gov) — colección Bracero Program
- **Lo que DEBE mostrar:** trabajadores en campo, herramientas agrícolas, contexto rural, época 1940-1960
- **Lo que NO debe mostrar:** imágenes de detención, cruces ilegales, violencia — el Bracero fue un programa legal
- **Tratamiento:** Convertir a BN si no lo está. Leve viñeta en bordes.

**Sobreimpresión:**
- Título: "PROGRAMA BRACERO" — Bebas Neue 72px, `#F5C518`
- Datos: "1942–1964 / 4,500,000 mexicanos / Michoacán · Guanajuato · Jalisco → California · Texas · Illinois" — Barlow Medium 32px, `#F2F2F0`

**Licencia:** Dominio público (obras del gobierno de EE.UU. pre-1928 o con copyright expirado)

---

### Escena 4 — Mapa de flujos migratorios históricos

**Tipo:** MAP-FLOW (animado, perspectiva global MX→EE.UU.)
**Descripción:** Mapa que muestra los circuitos de migración desde los estados de alta emigración en México hacia los estados de alta concentración en EE.UU. Las líneas se engrosan progresivamente para mostrar que los circuitos no se debilitaron — crecieron.

**Región:** México + EE.UU. (vista continental, norte de México + sur de EE.UU.)
**Variable mapeada:** Flujo migratorio acumulado por estado de origen (Mx) → estado de destino (EE.UU.)
**Fuente del dato:** CONAPO, Índice de Intensidad Migratoria 2020; Pew Research Center 2023 (distribución en EE.UU.)
**Granularidad:** Estatal (ambos países)

**Orígenes (México, estados de alta emisión):** Michoacán, Guanajuato, Jalisco, Guerrero, Oaxaca, Zacatecas
**Destinos (EE.UU., estados de alta concentración):** California, Texas, Illinois, Arizona, Georgia

**Animación (25 seg):**
1. (0–5 seg) El mapa aparece vacío. Solo los contornos.
2. (5–12 seg) Líneas de 1964: delgadas, ámbar tenue. Label: "1964"
3. (12–18 seg) Líneas se engrosan: "1990"
4. (18–23 seg) Líneas en máximo grosor: "2024"
5. (23–25 seg) Texto emergente: "Las rutas no cambiaron. Solo crecieron." — Bebas Neue 48px.

**Paleta:** Fondo `#0A0E14` (azul marino muy oscuro — océano/continental). Territorio MX: `#1A2020`. Territorio EE.UU.: `#1A1A28`. Líneas: `#F5C518` con opacidad creciente (40% → 100%) conforme aumenta el grosor.
**Herramienta:** Python (geopandas + cartopy para proyección correcta) o After Effects con capas de mapa base

---

### Escena 5 — Imagen documental: hogar de alta emigración

**Tipo:** IMG-DOC (generada con Google Imagen 4)
**Descripción:** Interior de hogar rural en zona de alta emigración (Michoacán / Guerrero). Mesa familiar, mujer mayor, niños. Ausencia implícita de hombres jóvenes. Luz cálida de tarde. Tono documental, no dramático.

**Prompt para Google Imagen 4 (en inglés):**
```
Interior of a modest rural home in Michoacan Mexico, older woman and children sitting at a wooden table, warm afternoon light through a window, empty chairs visible, simple decor, documentary photography style, realistic, no men present, cinematic, editorial quality, no text overlays, no watermarks, 16:9 aspect ratio
```

**Parámetros:** modelo `imagen-4.0-generate-001`, aspect_ratio `16:9`, person_generation `allow_adult`, safety `block_only_high`
**Post-proceso:** +10% contraste, +10% saturación, resize 1920×1080

**Sobreimpresión:**
- "$67,637,000,000 USD anuales" — Bebas Neue 48px, `#F5C518`, esquina superior derecha
- "Sin banco central. Sin política pública. Sin plan." — Barlow Medium 28px, `#A0A0A0`, abajo

**Si la imagen es rechazada por safety:** usar imagen de banco de fotos.
- **Unsplash query:** "rural Mexico home interior woman family documentary"
- **Pexels query:** "Mexican rural family home kitchen table warm"
- **Licencia requerida:** Unsplash License / CC0

---

### Escena 6 — Gráfico de dona: composición del gasto

**Tipo:** CHART-DONUT (animado)
**Descripción:** Gráfico de dona que muestra cómo los hogares receptores de remesas distribuyen su ingreso adicional. El segmento de "Ahorro e inversión" es el más pequeño y se ilumina al final — ese es el argumento.

**Variable:** Composición del gasto de hogares receptores de remesas
**Fuente:** INEGI, ENIGH 2022 (procesar microdatos o usar estudios publicados basados en ENIGH)
**Categorías y estimaciones orientativas** (verificar con microdatos ENIGH 2022):
- Alimentación: ~35%
- Vivienda y renta: ~20%
- Salud: ~15%
- Educación: ~15%
- Ahorro e inversión productiva: ~5–15%

**Paleta:**
- Alimentación: `#3D3D3D`
- Vivienda: `#4A4A4A`
- Salud: `#575757`
- Educación: `#636363`
- Ahorro e inversión: `#F5C518` (dorado — el único que se ilumina)

**Animación:** Los segmentos se dibujan en sentido horario uno por uno (2 seg cada uno). Al llegar al segmento dorado, se agranda ligeramente con una animación de "pop" y aparece el label en grande: "5–15% / Ahorro e inversión".

**Elementos de UI:** Título "¿A dónde va el dinero?" en Bebas Neue 48px. Leyenda con categorías. Label central de la dona: "Hogares receptores / ENIGH 2022".
**Fuente visible:** "INEGI, ENIGH 2022 / Estudios BID-CEPAL"
**Herramienta:** Datawrapper (d3-pie) → exportar PNG → After Effects para animación

---

### Escena 7 — Barra de progreso: el porcentaje que no invierte

**Tipo:** TYPO + INFOGRAPH
**Descripción:** Barra de progreso horizontal. Fondo oscuro. La barra se llena hasta 85–95% en gris oscuro (consumo). El 5–15% final en dorado con label: "Ahorro e inversión". El argumento en un solo visual.

**Composición (30 seg):**
1. (0–8 seg) Barra vacía aparece. Label a la izquierda: "Ingreso por remesas" en Barlow Medium.
2. (8–20 seg) La barra se llena de izquierda a derecha. Segmento gris oscuro `#3D3D3D` (consumo).
3. (20–25 seg) El último 10% se llena en dorado `#F5C518`. Pop animation.
4. (25–30 seg) Texto grande centrado aparece: "5–15% SE INVIERTE" en Bebas Neue 96px, `#F5C518`.
   Subtext: "El resto: consumo básico" en Barlow 28px, `#A0A0A0`.

**Nota:** Presentar como rango (5–15%), no como cifra puntual. Label "Fuente: estudios basados en ENIGH 2022, BID, CEPAL" en pie.
**Herramienta:** After Effects (animación de relleno de barra con expresión de velocidad)

---

### Escena 8 — Gráfico de barras: inversión pública comparativa

**Tipo:** CHART-BAR (comparativo, animado)
**Descripción:** Dos barras verticales. La diferencia en altura es el argumento. Estados con alta dependencia de remesas invierten menos en infraestructura pública por habitante que el promedio nacional.

**Eje X:** Categoría (2 barras: "Estados alta dependencia remesas" / "Promedio nacional")
**Eje Y:** Inversión pública en infraestructura por habitante (pesos, 2018–2023 promedio)
**Fuente:** SHCP, presupuesto ejercido por entidad + INEGI población; literatura BID sobre efecto sustitución
**Nota de producción:** Si el dato exacto no está disponible con el tiempo de producción, usar gráfico ilustrativo con rango estimado y declararlo en pie como "estimación basada en datos SHCP/literatura BID"

**Colores:**
- Barra "Alta dependencia": `#E63946` (roja — indica déficit)
- Barra "Promedio nacional": `#3A86FF` (azul — referencia)
- Diferencia marcada con bracket: "–X%" en `#F5C518`

**Animación:** Las barras crecen desde abajo simultáneamente. Al alcanzar su altura final, aparece el bracket de diferencia con un flash.
**Texto central:** "Las remesas no solo cubren la ausencia del Estado. También la sostienen." — Barlow Medium 28px, `#A0A0A0`
**Fuente visible:** "SHCP, presupuesto ejercido 2018–2023 / Literatura BID"
**Herramienta:** Datawrapper (d3-bars) → After Effects para animación adicional

---

### Escena 9 — Pirámide demográfica doble

**Tipo:** SPLIT (dos pirámides lado a lado)
**Descripción:** Comparación directa de la pirámide de edad de Michoacán versus el promedio nacional de México. La cohorte 20–40 años marcada en rojo en ambas pirámides — pero en Michoacán esa cohorte es visiblemente más angosta.

**Variable:** Distribución de la población por grupo de edad y sexo, 2020
**Fuente:** INEGI, Censo de Población y Vivienda 2020 — tabulados por entidad (disponibles sin microdatos)
**Granularidad:** Estatal

**Composición:**
- Pirámide izquierda: "MICHOACÁN 2020" — Bebas Neue 48px label
- Pirámide derecha: "MÉXICO PROMEDIO 2020" — Bebas Neue 48px label
- Cohortes 20–40 años: resaltadas en `#E63946` en ambas pirámides
- En Michoacán: un bracket apunta a la cohorte 20–40 con texto: "Los que construirían la economía local"

**Paleta:**
- Barras masculinas: `#3A86FF`
- Barras femeninas: `#4ECDC4`
- Cohorte migratoria (20–40): `#E63946` (override de ambos sexos)
- Fondo: `#121212`
- Eje y labels: `#A0A0A0`

**Animación:** Las barras crecen de adentro hacia afuera (del centro del eje Y) simultáneamente en ambas pirámides. Las barras 20–40 aparecen 0.5 seg después que el resto — énfasis.
**Fuente visible:** "INEGI, Censo de Población y Vivienda 2020"
**Herramienta:** Python (matplotlib) o Datawrapper — Datawrapper no soporta pirámidas nativas, usar Python

---

### Escena 10 — Diagrama de ciclo trágico

**Tipo:** DIAGRAM + TYPO (ciclo cerrado animado)
**Descripción:** Diagrama circular con cuatro nodos conectados por flechas. El ciclo rota lentamente. No hay fecha, no hay fuente — es la síntesis de la anatomía.

**Nodos (en sentido horario, Bebas Neue 36px, `#F2F2F0`):**
1. "ECONOMÍA LOCAL ESTANCADA"
2. "JÓVENES MIGRAN"
3. "REMESAS LLEGAN"
4. "ESTADO NO INVIERTE"

**Flechas:** `#F5C518` — las flechas tienen un efecto de flujo (partículas que se mueven en la dirección de la flecha, velocidad moderada)

**Centro del diagrama:** "60 AÑOS / EL MISMO CICLO / EL MISMO MAPA" — Bebas Neue 48px, `#F5C518`, aparece después de que el ciclo da la primera vuelta completa.

**Animación (30 seg):**
1. (0–5 seg) Aparecen los 4 nodos con fade-in
2. (5–15 seg) Aparecen las flechas y empiezan a fluir. El ciclo da una vuelta completa.
3. (15–20 seg) El texto central aparece con fade-in
4. (20–30 seg) El ciclo continúa rotando. La escena termina con el ciclo en movimiento.

**Herramienta:** After Effects (shapes + trim paths para las flechas animadas)

---

### Escena 11 — Gráfico de líneas doble: remesas y pobreza

**Tipo:** CHART-LINE (dos series, eje Y dual)
**Descripción:** Serie temporal 2000–2024. Línea 1: remesas totales México (en aumento sostenido). Línea 2: % de la población en pobreza extrema (en descenso lento). El argumento: las remesas sí ayudan, pero 60 años no son suficientes para transformar la estructura.

**Eje X:** Año (2000, 2002, 2004... 2024)
**Eje Y izquierdo:** Remesas (miles de millones USD)
**Eje Y derecho:** % población en pobreza extrema (CONEVAL)
**Fuentes:**
- Remesas: Banco Mundial WDI, BX.TRF.PWKR.CD.DT (API verificada)
- Pobreza extrema: CONEVAL, medición bienal 2000–2022

**Series:**
- Línea 1 (remesas): `#F5C518` — sube de $6.6B (2000) a $67.6B (2024)
- Línea 2 (pobreza extrema): `#E63946` — baja de ~24% (2000) a ~8% (2022)

**Anotaciones:**
- Punto marcado en 2020: "COVID / –8.5% PIB / +11% Remesas" con bracket doble en `#F2F2F0`
- Punto marcado en 2008: "Recesión EE.UU. / única caída de remesas" con nota en `#A0A0A0`
- Texto de cierre: "Las remesas sí funcionan. Pero 60 años no son suficientes para salir de la trampa." — Barlow 28px, `#A0A0A0`

**Herramienta:** Datawrapper (d3-lines) — exportar PNG → After Effects para animación de trace
**Dataset necesario:** World Bank API (ya verificada) + datos CONEVAL históricos

---

### Escena 12 — Mapa de riesgo: EE.UU. + fragilidad

**Tipo:** MAP-DOT + TYPO (mapa EE.UU. con overlay)
**Descripción:** Mapa de EE.UU. mostrando la concentración de población mexicana por estado. Sobre el mapa, tres iconos de riesgo aparecen en secuencia. El mensaje: el punto de falla está lejos y el remitente no lo controla.

**Región:** EE.UU. continental (48 estados)
**Variable:** Concentración de población de origen mexicano por estado
**Fuente:** Pew Research Center, 2023; American Community Survey (Census Bureau)
**Granularidad:** Estatal

**Paleta base:** Secuencial `#1E1E2E` (poca concentración) → `#3A86FF` (alta: California, Texas, Illinois)

**Overlay de riesgo (aparecen en secuencia sobre el mapa):**
1. Ícono 1: Gráfico de recesión + texto "RECESIÓN EN EE.UU." — `#E63946`
2. Ícono 2: Documento/ley + texto "POLÍTICA MIGRATORIA" — `#E63946`
3. Ícono 3: Avión/persona + texto "DEPORTACIONES MASIVAS" — `#E63946`

**Efecto:** A medida que aparecen los íconos de riesgo, el mapa de EE.UU. va perdiendo intensidad de color (fade a oscuro). Simultáneamente, un mini-mapa de México en la esquina inferior izquierda muestra los estados de alta dependencia de remesas oscureciéndose en `#E63946`.

**Texto de cierre:** "UN SOLO PUNTO DE FALLA" — Bebas Neue 96px, `#E63946`, centrado.
**Fuente visible:** "Pew Research Center 2023; CONAPO"
**Herramienta:** After Effects (composición con dos mapas + animación de iconos)

---

### Escena 13 — Imagen documental: pueblo en transición

**Tipo:** IMG-DOC (generada con Google Imagen 4)
**Descripción:** Calle de un pueblo pequeño en zona de alta emigración. Casas de colores, algunas con puertas cerradas. Ambiente quieto, sin actividad económica visible. Tarde. No dramático — solo ausencia.

**Prompt para Google Imagen 4 (en inglés):**
```
Small town street in rural Michoacan or Oaxaca Mexico, colorful houses with some closed doors and shuttered windows, late afternoon light, quiet empty street, no people visible, some overgrown vegetation, a closed small shop, documentary photography style, cinematic, 16:9 widescreen, no text, no watermarks, editorial quality
```

**Parámetros:** modelo `imagen-4.0-generate-001`, aspect_ratio `16:9`, person_generation `dont_allow`, safety `block_only_high`
**Post-proceso:** +15% contraste, +10% saturación, resize 1920×1080

**Si rechazada por safety:** usar banco de fotos.
- **Unsplash query:** "small town Mexico street empty afternoon"
- **Pexels query:** "rural Mexican village street houses colorful"
- **Licencia:** Unsplash License / CC0

**Sobreimpresión (aparece 10 seg después del inicio de la imagen):**
- "Las comunidades donde la emigración baja" — Barlow Medium 32px, `#F2F2F0`
- "aún no tienen economía local que las reciba." — Barlow Medium 32px, `#A0A0A0`

---

### Escena 14 — Pregunta final: pantalla negra

**Tipo:** TYPO (pantalla negra, texto progresivo)
**Descripción:** La escena más austera del video. Pantalla negra total. El texto aparece en tres fragmentos con pausas que dan peso a cada parte. Sin música de impacto. El silencio visual hace el trabajo.

**Composición y timing (20 seg):**
1. (0–2 seg) Pantalla negra. Silencio.
2. (2–8 seg) Aparece: "¿Quién paga la deuda" — Bebas Neue 72px, `#F2F2F0`, centrado. Fade-in 1 seg.
3. (8–13 seg) Aparece en línea siguiente: "de sesenta años" — misma tipografía.
4. (13–18 seg) Aparece en línea siguiente: "de desarrollo postergado?" — misma tipografía. Al completar esta línea, la última palabra `postergado?` tiene un leve glow dorado `#F5C518` de 0.5 seg.
5. (18–20 seg) La pregunta completa permanece. Fade lento a negro total.

**Regla de producción:** No usar música stinger al final. El silencio o una nota de piano sostenida muy baja es lo correcto. La pregunta debe resonar, no ser aplastada por la música.
**Sin fuente en pie** — es una pregunta editorial, no un dato.
**Herramienta:** After Effects (text animators + glow effect en la última palabra)

---

## Lista de assets a producir

### Mapas (4)

| ID | Escena | Descripción | Dataset | Herramienta |
|----|--------|-------------|---------|-------------|
| M01 | 2 | MAP-COR dual remesas vs PIB per cápita por estado | D1 (Banxico) + D3 (PIBE) + shapefile estatal | Python / Datawrapper |
| M02 | 4 | MAP-FLOW circuitos migratorios MX→EE.UU. animado | D2 (CONAPO intensidad migratoria) + shapefiles | Python + AE |
| M03 | 11 | CHART-LINE remesas + pobreza extrema 2000–2024 | World Bank API + CONEVAL histórico | Datawrapper |
| M04 | 12 | MAP-DOT EE.UU. concentración mexicana + riesgo overlay | Pew Research Center + shapefiles EE.UU. | AE |

### Gráficos y diagramas (7)

| ID | Escena | Tipo | Dataset | Herramienta |
|----|--------|------|---------|-------------|
| G01 | 1 | COUNTER animado $67.6B | — | After Effects |
| G02 | 6 | CHART-DONUT composición gasto hogares receptores | INEGI ENIGH 2022 | Datawrapper → AE |
| G03 | 7 | TYPO barra de progreso 5–15% inversión | — | After Effects |
| G04 | 8 | CHART-BAR comparación inversión pública infraestructura | SHCP + literatura BID | Datawrapper → AE |
| G05 | 9 | SPLIT pirámide demográfica doble | INEGI Censo 2020 | Python (matplotlib) |
| G06 | 10 | DIAGRAM ciclo cerrado trágico | — | After Effects |
| G07 | 14 | TYPO pantalla negra pregunta final | — | After Effects |

### Imágenes documentales (3)

| ID | Escena | Descripción | Fuente | Licencia |
|----|--------|-------------|--------|----------|
| I01 | 3 | Bracero Program B&N 1940s–1960s | Library of Congress / National Archives | Dominio público |
| I02 | 5 | Hogar rural zona emigración | Google Imagen 4 (prompt en brief) | Generada — uso libre |
| I03 | 13 | Pueblo pequeño calles vacías | Google Imagen 4 (prompt en brief) | Generada — uso libre |

---

## Datasets a descargar

| ID | Nombre | Institución | Formato | Prioritario |
|----|--------|-------------|---------|-------------|
| D1 | Remesas por entidad federativa 2024 | Banxico SIE | Excel/CSV (descarga portal SIE) | SÍ — M01 |
| D2 | Índice de Intensidad Migratoria 2020 | CONAPO | Excel + shapefile | SÍ — M02 |
| D3 | PIBE 2023 por entidad | INEGI | Excel tabulados | SÍ — M01 |
| D4 | Censo 2020 — pirámide edad Michoacán | INEGI | Tabulados web (portal INEGI) | SÍ — G05 |
| D5 | ENIGH 2022 — hogares receptores de remesas | INEGI | CSV microdatos o tabulados | SÍ — G02 |
| D6 | Pobreza extrema 2000–2022 serie histórica | CONEVAL | Excel del sitio CONEVAL | SÍ — M03 |
| D7 | Shapefiles estados México (marco geoestadístico) | INEGI | Shapefile | SÍ — todos los mapas MX |
| D8 | Shapefiles estados EE.UU. | Census Bureau | Shapefile / GeoJSON | SÍ — M04 |
| D9 | Remesas 2000–2024 serie histórica | Banco Mundial API | JSON (API verificada) | SÍ — M03 |

---

## Herramientas de producción

| Herramienta | Uso | Por qué |
|-------------|-----|---------|
| Python (geopandas + matplotlib + cartopy) | MAP-FLOW y pirámide demográfica | Control total de proyección y estilos |
| Datawrapper | Gráficos de barras, líneas, dona | Rápido, exporta PNG/SVG de alta calidad |
| After Effects | Animación de todos los assets | Requerido para Agente A5 (AE script) |
| Google Imagen 4 (`ai_asset_generator.py`) | I02 e I03 | API verificada y operacional en el sistema |
| QGIS (opcional) | Verificación de shapefiles | Útil para inspeccionar datos antes de scripting |

---

## Notas del Director Visual

1. **El visual más importante es M01** (mapa doble remesas vs. crecimiento): es el corazón del argumento de la Tesis 2. Si hay un mapa que vale la pena refinar, es ese.

2. **I01 (Bracero Program)** es la única imagen que no se genera — se busca en Library of Congress. Buscar bajo dominio público, etiqueta "Bracero". Preferir imágenes horizontales para formato 16:9.

3. **G06 (ciclo cerrado)** es la escena de mayor riesgo de producción — un diagrama animado de ciclo puede quedar genérico si no se trabaja el timing. El ciclo debe sentirse lento y pesado, no ágil.

4. **La pantalla G07 (Escena 14)** es deliberadamente austera. Resistir la tentación de agregar gráficos, música intensa o efectos. La pregunta sola, en negro, es el visual.

---

## Registro de revisiones

| Versión | Fecha | Cambio | Solicitado por |
|---------|-------|--------|----------------|
| v1.0 | 2026-05-12 | Borrador inicial — proyecto remesas-mx | Agente A3 |

---
*Generado por Agente A3 — Sistema de Video-Ensayos Cartográficos*
