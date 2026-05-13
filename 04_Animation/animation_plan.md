# Plan de Animación — La geografía invisible del subsidio migrante

**Proyecto:** 2026-05-remesas-mx
**Agente:** A5 Director Técnico de Motion Graphics
**Fecha:** 2026-05-13
**Estado:** Borrador v1.0
**Input:** script_draft.md v1.0 + visual_brief.md v1.0 (ambos aprobados)

---

## Resumen técnico

| Parámetro | Valor |
|-----------|-------|
| Composición | 1920 × 1080 px |
| Frame rate | 24 fps |
| Duración total | 6:30 (390 seg) |
| Escenas | 14 |
| Composiciones AE | 15 (14 escenas + 1 maestra) |
| Software | After Effects 2024+ |
| Script JSX | ae_script.jsx (incluido) |
| Preset de exportación | H.264, 16 Mbps, AAC 320 kbps, sRGB |

---

## Paleta — Documental Oscuro

| Rol | Hex | Uso |
|-----|-----|-----|
| Fondo principal | `#121212` | Todas las escenas oscuras (default) |
| Acento dorado (remesas) | `#F5C518` | Contadores, cifras clave, nodos del ciclo |
| Rojo alerta | `#E63946` | Datos negativos, riesgo, cohorte demográfica perdida |
| Azul comparativo | `#3A86FF` | Datos de referencia, promedio nacional, serie remesas |
| Gris editorial | `#A0A0A0` | Fuentes en pie, texto secundario |
| Blanco editorial | `#F2F2F0` | Texto principal sobre fondos oscuros |

---

## Tipografía

| Rol | Familia | Uso en AE |
|-----|---------|-----------|
| Display | Bebas Neue Bold | Números grandes, títulos de acto |
| Body | Barlow Medium | Narración de apoyo, listas |
| Mono | Barlow Condensed | Fuentes en pie, etiquetas técnicas |

> **Antes de ejecutar ae_script.jsx:** instalar Bebas Neue y Barlow (Google Fonts) en el sistema.

---

## Reglas globales de motion

| Tipo de movimiento | Easing | Duración |
|-------------------|--------|----------|
| Entrada de elemento principal | ease-out cubic | 700ms |
| Salida de elemento | ease-in cubic | 500ms |
| Transición entre escenas (mismo acto) | Cut duro | 0ms |
| Transición entre actos | Fade a negro | 700ms |
| Count-up de número | ease-out expo | 1500ms |
| Aparición de texto editorial | fade + slide-up 30px | 400ms |
| Revelado de mapa coroplético | ease-out progresivo | 800ms |
| Líneas de flujo (flow map) | draw-on secuencial | 2000ms |
| Highlight de región/nodo | scale 100→105% + glow | 300ms |
| Sweep de gráfico dona | ease-out, sentido horario | 1000ms |
| Grow de barra vertical | grow desde base, ease-out | 600ms |
| Aparición de nodo de ciclo | scale 0→100% + fade | 500ms |

---

## Storyboard técnico por escena

---

### ESCENA 01 — Contador tipográfico $67.6B
**Chunk:** CHUNK_01 | **Inicio:** 00:00 | **Fin:** 00:25 | **Duración:** 25s
**Visual:** COUNTER animado | **Comp AE:** SC01_CONTADOR_REMESAS

#### Animación de entrada
- **Tipo:** Fade desde negro
- **Duración:** 800ms
- Fondo `#121212` — permanece hasta el final del video

#### Elementos y comportamiento
| Elemento | Aparece en | Animación | Sale en | Notas |
|----------|-----------|-----------|---------|-------|
| Fondo sólido `#121212` | 00:00 | — | 00:25 | Base permanente |
| Counter "$67,637,000,000" en dorado | 00:02 | count-up 0→67,637,000,000, 1500ms, ease-out expo | 00:25 | Bebas Neue 120px, `#F5C518` |
| Texto "USD" debajo del número | 00:04 | fade, 400ms | 00:25 | Barlow Condensed 36px, `#A0A0A0` |
| Línea 1: "Mayor que los ingresos petroleros" | 00:08 | fade + slide-up 30px, 400ms | 00:25 | `#F2F2F0`, 36px, entrada secuencial |
| Línea 2: "Mayor que la IED" | 00:12 | fade + slide-up 30px, 400ms | 00:25 | delay 0.5s respecto a línea 1 |
| Línea 3: "Primera fuente de divisas" | 00:16 | fade + slide-up 30px, 400ms | 00:25 | delay 0.5s respecto a línea 2 |
| Fuente: "Banco Mundial, 2024" | 00:03 | fade, 300ms | 00:25 | `#A0A0A0`, Barlow Condensed 24px, pie derecho |

**Momento crítico:** El counter llega a su valor final al mismo tiempo que la voz dice "sesenta y siete mil millones de dólares." Las tres líneas comparativas entran durante la pausa dramática `[...]`.

#### Animación de salida
- **Tipo:** Cut duro a ESCENA 02 (misma paleta oscura, sin necesidad de transición)

---

### ESCENA 02 — Mapa coroplético dual (remesas vs. PIB)
**Chunk:** CHUNK_01 cont. | **Inicio:** 00:25 | **Fin:** 00:45 | **Duración:** 20s
**Visual:** MAP-COR (10s) → OVERLAY MAP-COR (10s) | **Comp AE:** SC02_MAPA_DUAL

#### Parte A: Mapa remesas (00:25–00:35)
| Elemento | Aparece en | Animación | Sale en |
|----------|-----------|-----------|---------|
| Mapa coroplético México (remesas 2024) | 00:25 | revelado progresivo ease-out, 800ms | 00:35 |
| Paleta gris claro → amarillo `#F5C518` | simultáneo | fill por intensidad, norte→sur | 00:35 |
| Top 5 estados iluminados en secuencia | 00:28 | scale 100→104% + glow, 300ms c/u, delay 400ms | 00:35 |
| Etiqueta nombre+monto de cada estado | simultáneo al highlight | fade + bubble, 300ms | 00:35 |
| Fuente "Banxico SIE, 2024" | 00:26 | fade, 300ms | 00:35 |

#### Parte B: Overlay crecimiento PIB (00:35–00:45)
| Elemento | Aparece en | Animación | Sale en |
|----------|-----------|-----------|---------|
| Overlay transparencia 60% sobre mapa A | 00:35 | cross dissolve 600ms | 00:45 |
| Escala de color PIB (azul frío = bajo crecimiento) | simultáneo | revelado progresivo, 800ms | 00:45 |
| Mismos 5 estados — ahora en azul oscuro | 00:38 | transición de color, ease-out, 500ms | 00:45 |
| Texto: "El mapa del dinero es el mapa del estancamiento." | 00:40 | fade + slide-up, 400ms | 00:45 | `#F2F2F0`, Barlow Medium 36px |

**El argumento visual:** el mapa A (dorado = remesas) y el mapa B (azul = bajo PIB) muestran exactamente los mismos estados coloreados. El espectador lo entiende sin narración.

#### Animación de salida
- **Tipo:** Fade a negro, 700ms — cambio de Acto 1 a Acto 2

---

### ESCENA 03 — Imagen documental Programa Bracero
**Chunk:** CHUNK_02 | **Inicio:** 00:45 | **Fin:** 01:15 | **Duración:** 30s
**Visual:** IMG-DOC B&W | **Comp AE:** SC03_BRACERO

#### Animación de entrada
- **Tipo:** Fade desde negro, 600ms
- Asset: imagen editorial dominio público (Library of Congress) — blanco y negro, trabajadores agrícolas 1940s–1960s

#### Elementos y comportamiento
| Elemento | Aparece en | Animación | Sale en | Notas |
|----------|-----------|-----------|---------|-------|
| Foto Bracero (full bleed) | 00:45 | fade, 600ms | 01:15 | Ajuste de brillo: -15%, contraste: +10% para profundidad |
| Overlay sólido negro 30% | 00:45 | — | 01:15 | Mejora legibilidad de texto |
| Bloque datos sobreimpuesto | 00:48 | fade + slide-up, 400ms, ease-out | 01:10 | Esquina inferior izquierda |
| "Programa Bracero / 1942–1964" | — | — en bloque — | — | Bebas Neue 64px, `#F5C518` |
| "4,500,000 mexicanos" | — | — | — | Bebas Neue 48px, `#F2F2F0` |
| "Michoacán — Guanajuato — Jalisco" | — | — | — | Barlow Medium 36px, `#A0A0A0` |
| "→ California — Texas — Illinois" | — | — | — | Barlow Medium 36px, `#A0A0A0` |
| Fuente "National Archives / CONAPO" | 00:47 | fade, 300ms | 01:10 | Pie inferior derecho |

**Instrucción de producción:** La foto actúa como telón de fondo estático. El bloque de datos entra como unidad sólida (no elemento por elemento). No aplicar motion a la foto — la estabilidad contrasta con las animaciones de datos del resto del video.

#### Animación de salida
- **Tipo:** Cut duro a ESCENA 04

---

### ESCENA 04 — Mapa de flujos migratorios (líneas que crecen)
**Chunk:** CHUNK_02 cont. | **Inicio:** 01:15 | **Fin:** 01:40 | **Duración:** 25s
**Visual:** MAP-FLOW | **Comp AE:** SC04_FLUJOS_MIG

#### Animación de entrada
- **Tipo:** Cut directo desde ESCENA 03, fondo `#121212`

#### Elementos y comportamiento
| Elemento | Aparece en | Animación | Sale en | Notas |
|----------|-----------|-----------|---------|-------|
| Mapa base América del Norte (oscuro) | 01:15 | fade, 500ms | 01:40 | Fondo `#121212`, contornos `#A0A0A0` delgados |
| Líneas de flujo 1964 (delgadas) | 01:17 | draw-on desde origen, 800ms, ease-out | 01:40 | `#F5C518` 1px, Michoacán/GTO/JAL → CA/TX/IL |
| Líneas de flujo 1990 (medianas) | 01:20 | draw-on, 600ms | 01:40 | `#F5C518` 3px, grosor crece |
| Líneas de flujo 2010 (gruesas) | 01:23 | draw-on, 600ms | 01:40 | `#F5C518` 5px |
| Líneas de flujo 2024 (muy gruesas) | 01:26 | draw-on, 800ms | 01:40 | `#F5C518` 8px + glow suave |
| Texto: "Las rutas no cambiaron. Solo crecieron." | 01:32 | fade + slide-up, 400ms | 01:40 | Barlow Medium 36px, `#F2F2F0` |
| Fuente "CONAPO, Índice de Intensidad Migratoria 2020" | 01:16 | fade, 300ms | 01:40 | `#A0A0A0`, pie |

**Momento crítico:** Las 4 capas de líneas (1964/1990/2010/2024) deben dibujarse en el mismo recorrido geográfico, diferenciadas solo por grosor. El resultado muestra el mismo mapa engordando a lo largo del tiempo — la geografía "se calcifica."

**Sincronización con voz:** El draw-on de las líneas 2024 comienza cuando la voz dice "La geografía se REPITE."

#### Animación de salida
- **Tipo:** Fade a negro, 700ms — fin de contexto histórico

---

### ESCENA 05 — Imagen documental: hogar rural
**Chunk:** CHUNK_03 | **Inicio:** 01:40 | **Fin:** 02:00 | **Duración:** 20s
**Visual:** IMG-DOC | **Comp AE:** SC05_HOGAR_RURAL

#### Animación de entrada
- **Tipo:** Fade desde negro, 600ms
- Asset: imagen generada con Google Imagen 4 (prompt en visual_brief.md — I02)

#### Elementos y comportamiento
| Elemento | Aparece en | Animación | Sale en | Notas |
|----------|-----------|-----------|---------|-------|
| Foto hogar rural (full bleed) | 01:40 | fade, 600ms | 02:00 | Tono cálido, luz de tarde |
| Overlay sólido negro 35% | 01:40 | — | 02:00 | Legibilidad |
| Bloque texto sobreimpuesto | 01:44 | fade + slide-up, 400ms | 01:57 | Centro inferior |
| "67,637 millones de dólares anuales" | — | — en bloque — | — | Bebas Neue 48px, `#F5C518` |
| "sin banco central" | — | — | — | Barlow Medium 30px, `#F2F2F0` |
| "sin política pública" | — | — | — | Barlow Medium 30px, `#F2F2F0` |
| "sin plan" | — | — | — | Barlow Medium 30px, `#E63946` |

**Sincronización con voz:** El bloque de texto entra cuando la voz dice "México construyó, sin planearlo, una economía paralela de transferencias."

#### Animación de salida
- **Tipo:** Cut duro a ESCENA 06 — inicio del Acto 3

---

### ESCENA 06 — Gráfico de dona: gasto de hogares receptores
**Chunk:** CHUNK_04 | **Inicio:** 02:00 | **Fin:** 02:30 | **Duración:** 30s
**Visual:** CHART-DONUT | **Comp AE:** SC06_DONA_GASTO

#### Animación de entrada
- **Tipo:** Cut directo, fondo `#121212`

#### Elementos y comportamiento
| Elemento | Aparece en | Animación | Sale en | Notas |
|----------|-----------|-----------|---------|-------|
| Gráfico dona (base) | 02:02 | sweep ease-out, 1000ms, sentido horario | 02:20 | Centro vacío, ancho de anillo 60px |
| Segmento Alimentación (mayor) | primero en sweep | `#3A86FF` | — | ~35% del círculo |
| Segmento Vivienda/Renta | en sweep | `#A0A0A0` | — | ~25% |
| Segmento Salud | en sweep | `#A0A0A0` | — | ~20% |
| Segmento Educación | en sweep | `#A0A0A0` | — | ~15% |
| Segmento Ahorro/Inversión | último en sweep | `#F5C518` resaltado | — | 5–15% — el más pequeño |
| Etiquetas de segmento | 02:06 | fade secuencial + leader line, 300ms c/u | 02:25 | Barlow Condensed 28px |
| Highlight segmento Ahorro | 02:15 | scale 100→110% + glow dorado, 300ms | 02:25 | Llama la atención sobre el más pequeño |
| Texto "Solo 5–15% se ahorra o invierte" | 02:18 | fade + slide-up, 400ms | 02:28 | Bebas Neue 48px, `#F5C518`, centro dona |
| Fuente "INEGI, ENIGH 2022" | 02:02 | fade, 300ms | 02:28 | Pie izq. |

**Sincronización con voz:** El highlight dorado del segmento de ahorro coincide con "lo que el Estado NO provee en esas regiones."

#### Animación de salida
- **Tipo:** Cut duro a ESCENA 07

---

### ESCENA 07 — Barra de progreso tipográfica: 5–15%
**Chunk:** CHUNK_05 | **Inicio:** 02:30 | **Fin:** 03:00 | **Duración:** 30s
**Visual:** TYPO + barra horizontal | **Comp AE:** SC07_BARRA_INVERSION

#### Animación de entrada
- **Tipo:** Cut directo, fondo `#121212`

#### Elementos y comportamiento
| Elemento | Aparece en | Animación | Sale en | Notas |
|----------|-----------|-----------|---------|-------|
| Barra horizontal fondo gris | 02:32 | fade, 300ms | 02:58 | Rect. 1600×80px, `#A0A0A0` 30% opacidad |
| Relleno azul (consumo) | 02:34 | fill ease-out izq→der, 1200ms, hasta 85–95% | 02:58 | `#3A86FF` |
| Relleno dorado (ahorro/inversión) | 02:36 | fill ease-out desde posición 85%, hasta 100%, 600ms | 02:58 | `#F5C518` — el tramo pequeño |
| Texto "85–95%" | 02:38 | fade, 400ms | 02:58 | Bebas Neue 96px, `#3A86FF`, centrado sobre tramo azul |
| Texto "consumo básico" | 02:41 | fade + slide-up, 400ms | 02:58 | Barlow Medium 36px, `#F2F2F0` bajo el "85–95%" |
| Texto "5–15%" | 02:44 | fade, 400ms | 02:58 | Bebas Neue 96px, `#F5C518`, sobre tramo dorado |
| Texto "ahorro e inversión" | 02:47 | fade + slide-up, 400ms | 02:58 | Barlow Medium 36px, `#A0A0A0` |
| Línea separadora vertical en el quiebre | 02:37 | draw-on top→bottom, 400ms | 02:58 | Blanco 1px |
| Texto final: "Las remesas no son capital de desarrollo." | 02:52 | fade + slide-up, 400ms | 02:58 | Barlow Medium 32px, `#F2F2F0` |
| Texto final: "Son el precio de vivir donde el Estado decidió no invertir." | 02:55 | fade + slide-up, 400ms | 02:58 | Barlow Medium 32px, `#E63946` |
| Fuente "Estudios basados en ENIGH 2022, BID, CEPAL" | 02:32 | fade, 300ms | 02:58 | `#A0A0A0`, pie |

**Sincronización con voz:** La línea en rojo entra en la pausa antes de "Son el precio..." — 1.5s de silencio visual antes del texto.

#### Animación de salida
- **Tipo:** Cut duro a ESCENA 08

---

### ESCENA 08 — Barras comparativas: inversión pública
**Chunk:** CHUNK_06 | **Inicio:** 03:00 | **Fin:** 03:30 | **Duración:** 30s
**Visual:** CHART-BAR comparativo | **Comp AE:** SC08_BARRAS_INV

#### Animación de entrada
- **Tipo:** Cut directo, fondo `#121212`

#### Elementos y comportamiento
| Elemento | Aparece en | Animación | Sale en | Notas |
|----------|-----------|-----------|---------|-------|
| Eje Y con escala | 03:02 | fade, 300ms | 03:28 | `#A0A0A0`, Barlow Condensed 24px |
| Título: "Inversión pública en infraestructura / por habitante" | 03:02 | fade, 300ms | 03:28 | Barlow Medium 32px, `#F2F2F0` |
| Subtítulo: "Promedio 2018–2023" | 03:03 | fade, 300ms | 03:28 | `#A0A0A0`, 24px |
| Barra izq.: "Estados alta dependencia de remesas" | 03:06 | grow desde base, ease-out, 800ms | 03:28 | `#E63946`, más baja |
| Etiqueta barra izq. | 03:09 | fade, 300ms | 03:28 | Barlow Condensed 24px, bajo la barra |
| Barra der.: "Promedio nacional" | 03:10 | grow desde base, ease-out, 800ms | 03:28 | `#3A86FF`, más alta |
| Etiqueta barra der. | 03:13 | fade, 300ms | 03:28 | — |
| Anotación diferencia (línea + número) | 03:16 | draw-on vertical + fade, 500ms | 03:28 | `#F5C518`, marca el gap |
| Texto: "Las remesas no solo cubren la ausencia del Estado." | 03:22 | fade + slide-up, 400ms | 03:28 | Barlow Medium 32px, `#F2F2F0` |
| Texto: "TAMBIÉN la sostienen." | 03:26 | fade, 400ms | 03:28 | Bebas Neue 48px, `#E63946` |
| Fuente "SHCP + BID" | 03:02 | fade, 300ms | 03:28 | `#A0A0A0`, pie |

**Momento crítico:** "TAMBIÉN la sostienen" aparece en la pausa más larga antes del final del chunk. El rojo en Bebas Neue contrasta con el tono analítico del resto de la escena.

#### Animación de salida
- **Tipo:** Cut duro a ESCENA 09

---

### ESCENA 09 — Pirámide de edad doble: Michoacán vs. México
**Chunk:** CHUNK_07 | **Inicio:** 03:30 | **Fin:** 04:00 | **Duración:** 30s
**Visual:** SPLIT pirámide demográfica | **Comp AE:** SC09_PIRAMIDE

#### Animación de entrada
- **Tipo:** Cut directo, fondo `#121212`

#### Elementos y comportamiento
| Elemento | Aparece en | Animación | Sale en | Notas |
|----------|-----------|-----------|---------|-------|
| Eje central Y (edades) | 03:32 | draw-on top→bottom, 600ms | 03:58 | `#F2F2F0`, etiquetas cohortes cada 10 años |
| Pirámide derecha: "México promedio 2020" | 03:34 | grow desde eje central, ease-out, 1200ms | 03:58 | `#3A86FF`, barras horizontales |
| Pirámide izquierda: "Michoacán 2020" | 03:36 | grow desde eje, ease-out, 1200ms | 03:58 | `#A0A0A0`, visiblemente más angosta |
| Highlight cohorte 20–40 (ambas pirámides) | 03:42 | fill `#E63946`, ease-out, 500ms | 03:56 | La más angosta en Michoacán salta a la vista |
| Texto: "Los que construirían la economía local ya no están." | 03:48 | fade + slide-up, 400ms | 03:58 | Barlow Medium 32px, `#F2F2F0`, centrado inferior |
| Fuente "INEGI, Censo de Población 2020" | 03:32 | fade, 300ms | 03:58 | `#A0A0A0`, pie |

**El argumento visual:** Las dos pirámides son espejadas. La de Michoacán muestra la cohorte 20–40 visiblemente menor que el promedio nacional. El highlight rojo hace la comparación obvia sin necesidad de narración.

**Sincronización con voz:** El highlight rojo en la cohorte 20–40 aparece cuando la voz dice "A los hombres en edad productiva."

#### Animación de salida
- **Tipo:** Fade a negro, 700ms — fin del Acto 3, inicio del clímax

---

### ESCENA 10 — Diagrama de ciclo cerrado
**Chunk:** CHUNK_08 | **Inicio:** 04:00 | **Fin:** 04:30 | **Duración:** 30s
**Visual:** DIAGRAM ciclo | **Comp AE:** SC10_CICLO

#### Animación de entrada
- **Tipo:** Fade desde negro, 700ms. Fondo `#121212`.

#### Elementos y comportamiento (construcción secuencial del ciclo)
| Elemento | Aparece en | Animación | Sale en | Notas |
|----------|-----------|-----------|---------|-------|
| Nodo 1: "Economía local estancada" | 04:02 | scale 0→100% + fade, 500ms | 04:28 | Círculo `#F5C518`, texto interior Barlow 28px |
| Flecha 1→2 (draw-on curva) | 04:04 | draw-on, 600ms, ease-out | 04:28 | Blanca 2px, arco superior |
| Nodo 2: "Jóvenes migran" | 04:06 | scale 0→100% + fade, 500ms | 04:28 | Círculo `#E63946` |
| Flecha 2→3 | 04:08 | draw-on, 600ms | 04:28 | — |
| Nodo 3: "Remesas llegan" | 04:10 | scale 0→100% + fade, 500ms | 04:28 | Círculo `#3A86FF` |
| Flecha 3→4 | 04:12 | draw-on, 600ms | 04:28 | — |
| Nodo 4: "Estado no invierte" | 04:14 | scale 0→100% + fade, 500ms | 04:28 | Círculo `#A0A0A0` |
| Flecha 4→1 (cierra el ciclo) | 04:16 | draw-on, 800ms, ease-out | 04:28 | `#F5C518` 3px — la flecha de cierre en dorado |
| El ciclo da una vuelta completa (loop) | 04:20 | recorrido de luz/glow por las flechas, 2000ms | 04:28 | Loop suave, 2 veces |
| Texto "Sesenta años. El mismo ciclo." | 04:24 | fade, 400ms | 04:28 | Bebas Neue 64px, `#F2F2F0`, centrado inferior |

**Instrucción de producción:** Los 4 nodos forman un cuadrado con flechas curvas entre ellos. La última flecha (4→1) en dorado señala que el ciclo regresa al inicio. No añadir texto adicional — los nodos son auto-explicativos.

#### Animación de salida
- **Tipo:** Cut duro a ESCENA 11 — el ciclo sigue en pantalla pero corta abruptamente (refuerza la trampa)

---

### ESCENA 11 — Gráfico de líneas doble: remesas + pobreza extrema
**Chunk:** CHUNK_09 | **Inicio:** 04:30 | **Fin:** 05:10 | **Duración:** 40s
**Visual:** CHART-LINE doble | **Comp AE:** SC11_LINEAS_DUAL

#### Animación de entrada
- **Tipo:** Cut directo, fondo `#121212`

#### Elementos y comportamiento
| Elemento | Aparece en | Animación | Sale en | Notas |
|----------|-----------|-----------|---------|-------|
| Ejes X (2000–2024) e Y (escala doble) | 04:32 | fade, 300ms | 05:08 | `#A0A0A0`, Barlow Condensed 22px |
| Línea 1: "Remesas México (mmd USD)" | 04:34 | draw-on izq→der, 1500ms, ease-out | 05:08 | `#3A86FF`, crece sostenidamente |
| Línea 2: "% Pobreza extrema (CONEVAL)" | 04:36 | draw-on izq→der, 1500ms, ease-out | 05:08 | `#E63946`, baja pero lentamente |
| Leyenda (2 líneas) | 04:35 | fade, 300ms | 05:08 | Esquina superior derecha |
| Anotación texto en gráfico | 04:48 | fade + slide-up, 400ms | 05:08 | "Las remesas sí funcionan. / Pero 60 años no son suficientes." |
| Highlight punto 2008 (crisis) | 04:52 | punto rojo pulsante, scale 100→120%, 300ms | 05:04 | Señala la resistencia de las remesas |
| Fuente "Banco Mundial WDI; CONEVAL 2000–2022" | 04:32 | fade, 300ms | 05:08 | `#A0A0A0`, pie |

**Sincronización con voz:** La anotación aparece cuando la voz dice "Ese argumento es completamente REAL." La pausa de 2s antes de "Y es INSUFICIENTE" se produce sobre el gráfico estático — silencio visual deliberado.

#### Animación de salida
- **Tipo:** Cut duro a ESCENA 12

---

### ESCENA 12 — Mapa de riesgo EE.UU. (puntos de falla)
**Chunk:** CHUNK_10 | **Inicio:** 05:10 | **Fin:** 05:45 | **Duración:** 35s
**Visual:** MAP-DOT | **Comp AE:** SC12_RIESGO_EEUU

#### Animación de entrada
- **Tipo:** Cut directo, fondo `#121212`

#### Elementos y comportamiento
| Elemento | Aparece en | Animación | Sale en | Notas |
|----------|-----------|-----------|---------|-------|
| Mapa base EE.UU. (oscuro) | 05:10 | fade, 500ms | 05:43 | Contornos `#A0A0A0` delgados |
| Estados alta concentración mexicanos iluminados | 05:12 | fill `#F5C518` ease-out, 700ms | 05:43 | California, Texas, Illinois, NY |
| Mapa espejo de México (derecha) | 05:13 | fade, 500ms | 05:43 | Escala reducida 40%, estados dependientes en `#3A86FF` |
| Ícono riesgo 1: "Recesión" | 05:18 | scale 0→100% + fade, 400ms | 05:43 | `#E63946`, sobre California |
| Ícono riesgo 2: "Política migratoria" | 05:22 | scale 0→100% + fade, 400ms | 05:43 | `#E63946`, sobre Texas |
| Ícono riesgo 3: "Deportaciones masivas" | 05:26 | scale 0→100% + fade, 400ms | 05:43 | `#E63946`, sobre Illinois |
| Flechas riesgo EE.UU. → México | 05:28 | draw-on, 600ms c/u, ease-out | 05:43 | `#E63946` punteadas — cada ícono tiene su flecha |
| Estados mexicanos se oscurecen progresivamente | 05:30 | fill `#1A1A1A`, 800ms, ease-out | 05:43 | Michoacán, GTO, JAL, GRO |
| Texto: "Si el flujo se interrumpe, no tienen alternativa." | 05:36 | fade + slide-up, 400ms | 05:43 | Barlow Medium 32px, `#F2F2F0` |
| Fuente "Pew Research Center 2023; CONAPO" | 05:11 | fade, 300ms | 05:43 | `#A0A0A0`, pie |

**Sincronización con voz:** Cada ícono de riesgo aparece cuando la voz dice "Se llama X." — tres veces, una por riesgo. Los estados mexicanos se oscurecen durante la pausa después de "Si el flujo se interrumpe."

#### Animación de salida
- **Tipo:** Fade a negro, 700ms — inicio de Acto 5 (implicación)

---

### ESCENA 13 — Imagen documental: pueblo en silencio
**Chunk:** CHUNK_11 | **Inicio:** 05:45 | **Fin:** 06:10 | **Duración:** 25s
**Visual:** IMG-DOC | **Comp AE:** SC13_PUEBLO_VACIO

#### Animación de entrada
- **Tipo:** Fade desde negro, 700ms
- Asset: imagen generada con Google Imagen 4 (prompt en visual_brief.md — I03)

#### Elementos y comportamiento
| Elemento | Aparece en | Animación | Sale en | Notas |
|----------|-----------|-----------|---------|-------|
| Foto calle pueblo rural (full bleed) | 05:45 | fade, 700ms | 06:08 | Casas de colores, negocios cerrados, luz de tarde |
| Overlay negro 40% | 05:45 | — | 06:08 | Lecturabilidad |
| Texto 1: "Las comunidades donde la emigración baja" | 05:52 | fade + slide-up, 400ms | 06:08 | Barlow Medium 30px, `#F2F2F0`, centro inferior |
| Texto 2: "aún no tienen economía local que las reciba." | 05:56 | fade + slide-up, 400ms | 06:08 | Barlow Medium 30px, `#F2F2F0` |
| Fuente "CONAPO" | 05:47 | fade, 300ms | 06:05 | `#A0A0A0`, pie |

**Sincronización con voz (Chunk 11, speed=0.85):** El texto 1 entra cuando la voz dice "Las remesas que llegaban están disminuyendo." La pausa larga antes de la pregunta final ocurre sobre el pueblo vacío estático — máximo silencio visual.

#### Animación de salida
- **Tipo:** Fade a negro, 1000ms — la más lenta del video. Prepara el cierre.

---

### ESCENA 14 — Pantalla negra: pregunta final
**Chunk:** CHUNK_11 cont. | **Inicio:** 06:10 | **Fin:** 06:30 | **Duración:** 20s
**Visual:** TYPO sobre negro | **Comp AE:** SC14_PREGUNTA_FINAL

#### Animación de entrada
- **Tipo:** Ya en negro desde ESCENA 13. Nada aparece hasta 06:13 — 3 segundos de silencio total.

#### Elementos y comportamiento
| Elemento | Aparece en | Animación | Sale en | Notas |
|----------|-----------|-----------|---------|-------|
| Silencio visual | 06:10–06:13 | — ninguno — | — | La voz hace la pausa de 2s antes de la pregunta |
| Línea 1: "¿Quién paga la deuda" | 06:13 | fade, 600ms — aparece sola | — | Bebas Neue 72px, `#F2F2F0`, centrado |
| Línea 2: "de sesenta años" | 06:16 | fade, 500ms | — | Bebas Neue 72px, `#F5C518` — dorado |
| Línea 3: "de desarrollo postergado?" | 06:19 | fade, 500ms | — | Bebas Neue 72px, `#F2F2F0` |
| Fade final a negro total | 06:25 | fade, 1200ms | 06:30 | Sin texto adicional. Sin logo. Sólo negro. |

**Instrucción de producción:** Esta es la escena más restringida. Nada se mueve. Ningún elemento tiene slide-up. Las tres líneas aparecen en silencio absoluto, una por una. El fade final comienza antes de que termine el audio — el último sonido de voz se apaga en negro.

**Sincronización con voz:** Línea 1 aparece justo cuando la voz comienza "¿quién paga la deuda". Línea 2 en "de sesenta años". Línea 3 en "de desarrollo postergado". La voz termina. El negro permanece 5 segundos antes de cortar.

---

## Tabla maestra de timing

| # | Escena | Inicio | Fin | Dur (s) | Chunk | Visual | Trans. entrada | Trans. salida |
|---|--------|--------|-----|---------|-------|--------|---------------|---------------|
| 01 | Contador tipográfico $67.6B | 00:00 | 00:25 | 25 | C01 | COUNTER | Fade negro → | Cut |
| 02 | Mapa coroplético dual | 00:25 | 00:45 | 20 | C01 | MAP-COR | Cut | Fade negro |
| 03 | Bracero B&W (IMG-DOC) | 00:45 | 01:15 | 30 | C02 | IMG-DOC | Fade negro → | Cut |
| 04 | Flujos migratorios (MAP-FLOW) | 01:15 | 01:40 | 25 | C02 | MAP-FLOW | Cut | Fade negro |
| 05 | Hogar rural (IMG-DOC) | 01:40 | 02:00 | 20 | C03 | IMG-DOC | Fade negro → | Cut |
| 06 | Dona gasto hogares | 02:00 | 02:30 | 30 | C04 | CHART-DONUT | Cut | Cut |
| 07 | Barra inversión 5–15% | 02:30 | 03:00 | 30 | C05 | TYPO+BAR | Cut | Cut |
| 08 | Barras inversión pública | 03:00 | 03:30 | 30 | C06 | CHART-BAR | Cut | Cut |
| 09 | Pirámide demográfica doble | 03:30 | 04:00 | 30 | C07 | SPLIT | Cut | Fade negro |
| 10 | Ciclo cerrado (DIAGRAM) | 04:00 | 04:30 | 30 | C08 | DIAGRAM | Fade negro → | Cut |
| 11 | Gráfico líneas dual | 04:30 | 05:10 | 40 | C09 | CHART-LINE | Cut | Cut |
| 12 | Mapa riesgo EE.UU. | 05:10 | 05:45 | 35 | C10 | MAP-DOT | Cut | Fade negro |
| 13 | Pueblo vacío (IMG-DOC) | 05:45 | 06:10 | 25 | C11 | IMG-DOC | Fade negro → | Fade negro |
| 14 | Pregunta final (TYPO) | 06:10 | 06:30 | 20 | C11 | TYPO | (en negro) | Fade negro |

---

## Assets — checklist de producción

### Mapas (exportar como SVG o PNG 1920×1080 desde QGIS/Python)
- [ ] M01 — MAP-COR: México remesas por estado 2024 (Esc. 2a) — Banxico SIE + shapefile INEGI estatal
- [ ] M02 — MAP-COR: México PIB estatal per cápita 2010–2023 (Esc. 2b) — INEGI PIBE 2023 + shapefile
- [ ] M03 — MAP-FLOW: América del Norte + líneas migratorias 4 épocas (Esc. 4) — CONAPO IIM 2020
- [ ] M04 — MAP-DOT: EE.UU. estados + México estados (Esc. 12) — shapefiles ambos países

### Gráficos/Diagramas (exportar como SVG desde Datawrapper o Python matplotlib)
- [ ] G01 — CHART-DONUT: Composición gasto hogares receptores (Esc. 6) — INEGI ENIGH 2022
- [ ] G02 — TYPO+BAR: Barra progreso 85–95% / 5–15% (Esc. 7) — crear en AE directamente
- [ ] G03 — CHART-BAR: Inversión pública infraestructura por habitante (Esc. 8) — SHCP + INEGI
- [ ] G04 — SPLIT: Pirámide demográfica doble Michoacán vs. México (Esc. 9) — INEGI Censo 2020
- [ ] G05 — DIAGRAM: Ciclo 4 nodos (Esc. 10) — crear en AE directamente
- [ ] G06 — CHART-LINE: Remesas USD + % pobreza extrema 2000–2024 (Esc. 11) — WB API + CONEVAL

### Imágenes documentales (generación y descarga)
- [ ] I01 — Bracero Program B&W (Esc. 3) — Library of Congress (dominio público, descarga directa)
- [ ] I02 — Hogar rural interior (Esc. 5) — Google Imagen 4 (prompt en visual_brief.md)
- [ ] I03 — Calle pueblo rural (Esc. 13) — Google Imagen 4 (prompt en visual_brief.md)

### Fuentes tipográficas (instalar ANTES de ejecutar ae_script.jsx)
- [ ] Bebas Neue Bold — Google Fonts
- [ ] Barlow Medium (400, 500) — Google Fonts
- [ ] Barlow Condensed Regular — Google Fonts

### Audio (voz sintetizada con ElevenLabs via voice_gen.py)
- [ ] chunk_01_v1.wav (00:00–00:45)
- [ ] chunk_02_v1.wav (00:45–01:40)
- [ ] chunk_03_v1.wav (01:40–02:00)
- [ ] chunk_04_v1.wav (02:00–02:30)
- [ ] chunk_05_v1.wav (02:30–03:00)
- [ ] chunk_06_v1.wav (03:00–03:30)
- [ ] chunk_07_v1.wav (03:30–04:00)
- [ ] chunk_08_v1.wav (04:00–04:30)
- [ ] chunk_09_v1.wav (04:30–05:10)
- [ ] chunk_10_v1.wav (05:10–05:45)
- [ ] chunk_11_v1.wav (05:45–06:30) — speed=0.85, stability=0.48
- [ ] Música ambiente (opcional, 0–3dB, drone electroacústico ambiental) — Epidemic Sound / Artlist

---

## Checklist pre-render

- [ ] Ejecutar `ae_script.jsx` en After Effects (File > Scripts > Run Script File...)
- [ ] Instalar Bebas Neue y Barlow antes de ejecutar el script
- [ ] Importar WAV de voz en carpeta `04_VOICE` del proyecto AE
- [ ] Sincronizar cada WAV con su escena correspondiente en el timeline maestro
- [ ] Importar mapas (SVG/PNG) en carpeta `02_MAPS`
- [ ] Importar gráficos en carpeta `03_CHARTS`
- [ ] Importar imágenes documentales en carpeta `01_IMAGES`
- [ ] Verificar sincronización voz–imagen en momentos críticos: SC01 (counter), SC04 (flujos), SC10 (ciclo), SC14 (pregunta final)
- [ ] Revisar que ESCENA 14 no tenga ningún movimiento — solo fade de opacidad
- [ ] Color profile: sRGB (YouTube — no usar Display P3)
- [ ] Resolución: 1920×1080, 24fps
- [ ] Exportar H.264, 16 Mbps, AAC 320 kbps
- [ ] Nombre de exportación: `remesas_mx_v1_MASTER.mp4`

---

*Generado por Agente A5 — Sistema de Video-Ensayos Cartográficos*
