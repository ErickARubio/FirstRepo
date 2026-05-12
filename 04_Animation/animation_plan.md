# Plan de Animación — El impuesto que no regresa

**Proyecto:** 2026-05-edomex-cdmx
**Agente:** A5 Director Técnico de Motion Graphics
**Fecha:** 2026-05-10
**Estado:** Borrador v1.0

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

## Reglas globales de motion

| Tipo de movimiento | Easing | Duración |
|-------------------|--------|----------|
| Entrada de elemento principal | ease-out cubic | 700ms |
| Salida de elemento | ease-in cubic | 500ms |
| Transición entre escenas (mismo acto) | Cut duro | 0ms |
| Transición entre actos | Fade negro | 700ms |
| Count-up de número | ease-out expo | 1500ms |
| Aparición de texto editorial | fade + slide-up 30px | 400ms |
| Revelado de mapa (choropleth) | ease-out progresivo | 800ms |
| Líneas de flujo (flow map) | draw-on secuencial | 2000ms |
| Highlight de región | scale 100→105% + glow | 300ms |

---

## Storyboard técnico por escena

---

### ESCENA 01 — Mapa de apertura nocturno
**Chunk:** CHUNK_01 | **Inicio:** 00:00 | **Fin:** 00:15 | **Duración:** 15s
**Visual:** MAP-FLOW nocturno | **Comp AE:** SC01_APERTURA

#### Animación de entrada
- **Tipo:** Fade desde negro
- **Duración:** 1200ms
- **Easing:** ease-out cubic
- El mapa aparece en estado "noche" (fondo `#0D1117`)

#### Elementos y comportamiento
| Elemento | Aparece en | Animación | Sale en | Notas |
|----------|-----------|-----------|---------|-------|
| Fondo mapa ZMVM (oscuro) | 00:00 | Fade-in 1200ms | 00:15 | Base estática |
| Líneas de flujo ámbar Edomex→CDMX | 00:02 | draw-on secuencial desde origen, 2000ms, ease-out expo | loop suave | Grosor proporcional al volumen del flujo |
| Texto "La frontera invisible" | 00:10 | fade + slide-up 20px, 400ms | 00:15 | Inter ExtraBold, `#F4F6F9`, centrado inferior |

#### Animación de salida
- **Tipo:** Cut duro a ESCENA 02
- El mapa sigue corriendo en fondo oscuro — la escena 2 entra encima con un fade rápido del fondo claro

#### Sincronización con voz
- Las líneas de flujo empiezan a dibujarse en cuanto comienza el audio (00:02)
- "La frontera invisible" aparece en 00:10, coincidiendo con la pausa dramática del CHUNK_01

---

### ESCENA 02 — Diagrama mecanismo ISN
**Chunk:** CHUNK_02 | **Inicio:** 00:15 | **Fin:** 00:45 | **Duración:** 30s
**Visual:** DIAGRAM animado | **Comp AE:** SC02_ISN_MECANISMO

#### Animación de entrada
- **Tipo:** Fade blanco desde negro (transición de noche a día)
- **Duración:** 700ms
- Fondo cambia a `#FFFFFF`

#### Elementos y comportamiento
| Elemento | Aparece en | Animación | Sale en | Notas |
|----------|-----------|-----------|---------|-------|
| Ícono empresa CDMX (centro) | 00:16 | scale 0→100% + fade, 600ms, ease-out | — | Azul `#0072B5` |
| Ícono trabajador A (Condesa) | 00:19 | slide desde abajo-izq, 500ms | — | Color neutro `#4A6274` |
| Ícono trabajador B (Ecatepec) | 00:21 | slide desde abajo-der, 500ms | — | Naranja `#E8520A` |
| Flecha ISN 4% → erario | 00:25 | draw-on hacia arriba, 700ms | — | Aparece cuando voz dice "cuatro pesos de cada cien" |
| Texto "ISN: 4% sobre nómina total" | 00:28 | fade + slide-up, 400ms | — | Inter ExtraBold 72px |
| Caja "Erario CDMX" | 00:30 | scale + fade, 500ms | — | `#0D1B2A` con texto blanco |

#### Animación de salida
- **Tipo:** Cross dissolve 600ms hacia ESCENA 03

#### Sincronización con voz
- Empresa: cuando voz dice "Cada empresa con domicilio..."
- Flecha ISN: cuando voz dice "cuatro pesos de cada cien"
- Ícono Ecatepec (naranja) aparece cuando voz dice "trabajadores que viven en el Estado de México"

---

### ESCENA 03 — PIB nacional + pastel CDMX
**Chunk:** CHUNK_03 | **Inicio:** 00:45 | **Fin:** 01:05 | **Duración:** 20s
**Visual:** MAP-COR (10s) → CHART-PIE (10s) | **Comp AE:** SC03_PIB

#### Parte A: Mapa PIB (00:45–00:55)
| Elemento | Aparece en | Animación | Sale en |
|----------|-----------|-----------|---------|
| Mapa México por entidad | 00:45 | revelado coroplético ease-out, 800ms | 00:55 |
| Resaltado CDMX | 00:47 | scale 100→103% + glow, 300ms | 00:55 |
| Counter "14.8% del PIB nacional" | 00:50 | count-up 0→14.8, 1500ms | 00:55 |
| Fuente en pie "INEGI, PIBE 2023" | 00:46 | fade, 300ms | 00:55 |

#### Parte B: Pastel servicios (00:55–01:05)
| Elemento | Aparece en | Animación | Sale en |
|----------|-----------|-----------|---------|
| Gráfico pastel CDMX | 00:55 | pie sweep ease-out, 1000ms | 01:05 |
| Segmento "83.5% servicios" resaltado | 01:00 | scale 100→108% + saturación, 400ms | 01:05 |
| Etiqueta "83.5% servicios" | 01:01 | fade + slide, 400ms | 01:05 |

#### Transición: Cross dissolve 600ms entre parte A y parte B
#### Salida: Cut a ESCENA 04

---

### ESCENA 04 — Crecimiento Ecatepec + expansión urbana
**Chunk:** CHUNK_04 | **Inicio:** 01:05 | **Fin:** 01:30 | **Duración:** 25s
**Visual:** CHART-BAR (12s) + MAP expansión (13s) | **Comp AE:** SC04_CRECIMIENTO

#### Parte A: Barras Ecatepec (01:05–01:17)
| Elemento | Aparece en | Animación | Sale en |
|----------|-----------|-----------|---------|
| Eje Y (escala) | 01:05 | fade, 300ms | 01:17 |
| Barras 1970→2020 (secuencial) | 01:06 | grow-up desde base, ease-out, 200ms/barra | 01:17 |
| Etiqueta final "1.65M hoy" | 01:14 | fade + slide, 400ms | 01:17 |
| Fuente "INEGI, Censos 1970-2020" | 01:06 | fade, 300ms | 01:17 |

**Nota:** Las barras crecen de izquierda a derecha, una por una, con delay de 150ms entre cada una para que el crecimiento temporal se lea como proceso histórico.

#### Parte B: Mapa expansión urbana (01:17–01:30)
| Elemento | Aparece en | Animación | Sale en |
|----------|-----------|-----------|---------|
| Mapa base ZMVM | 01:17 | fade, 500ms | 01:30 |
| Anillo 1970 (núcleo CDMX) | 01:18 | fill radial ease-out, 600ms | 01:30 |
| Anillo 1980 | 01:20 | fill radial ease-out, 600ms | 01:30 |
| Anillo 1990 | 01:22 | fill radial, naranja | 01:30 |
| Anillo 2000-2020 (Edomex) | 01:24 | fill radial, rojo, más rápido | 01:30 |

#### Salida: Cut a ESCENA 05

---

### ESCENA 05 — Pantalla tipográfica editorial
**Chunk:** CHUNK_05 | **Inicio:** 01:30 | **Fin:** 01:50 | **Duración:** 20s
**Visual:** TYPO dos columnas | **Comp AE:** SC05_SISTEMA

#### Animación de entrada
- **Tipo:** Fade desde negro, 700ms — marca cambio de tono
- Fondo `#FFFFFF` limpio

#### Elementos y comportamiento
| Elemento | Aparece en | Animación | Sale en |
|----------|-----------|-----------|---------|
| Columna izq. "CDMX / Empleo / Producto" | 01:31 | slide desde izquierda, 600ms, ease-out | 01:50 |
| Flecha doble central "←→" | 01:35 | fade + scale 0→100%, 400ms | 01:50 |
| Columna der. "EDOMEX / Trabajadores / Costos" | 01:37 | slide desde derecha, 600ms, ease-out | 01:50 |

**Timing preciso:** La columna izquierda entra con "la capital produce el empleo", la flecha con "y se queda con el producto", la columna derecha con "La periferia produce los trabajadores".

#### Animación de salida
- **Tipo:** Fade a negro, 700ms — cierre de Acto 2, apertura del Acto 3

---

### ESCENA 06 — Mapa flujos EOD 2017 (detallado)
**Chunk:** CHUNK_06 | **Inicio:** 01:50 | **Fin:** 02:20 | **Duración:** 30s
**Visual:** MAP-FLOW diurno | **Comp AE:** SC06_FLUJOS_EOD

#### Animación de entrada
- **Tipo:** Fade desde negro, 500ms → fondo `#F4F6F9`

#### Elementos y comportamiento
| Elemento | Aparece en | Animación | Sale en |
|----------|-----------|-----------|---------|
| Mapa base ZMVM (fondo claro) | 01:50 | fade, 500ms | 02:20 |
| Límite CDMX-Edomex (línea punteada roja) | 01:52 | draw-on, 600ms | 02:20 |
| Etiquetas municipios Edomex | 01:53 | fade secuencial, 200ms cada uno | 02:20 |
| Flechas de flujo (7 rutas principales) | 01:56 | draw-on secuencial desde origen, ease-out, 250ms/flecha | 02:10 |
| Counter "7,770,000 viajes/día" | 02:05 | count-up 0→7,770,000, 1500ms ease-out expo | 02:20 |
| Sub-texto "22.5% de todos los viajes" | 02:08 | fade + slide-up, 400ms | 02:20 |
| Fuente "INEGI, EOD 2017" | 01:52 | fade, 300ms | 02:20 |

#### Sincronización con voz
- El contador empieza cuando la voz dice "El número es este:"
- Las flechas terminan de dibujarse antes de que la voz diga "El veintidós punto cinco..."

#### Salida: Cut duro a ESCENA 07

---

### ESCENA 07 — Timeline jornada laboral
**Chunk:** CHUNK_07 | **Inicio:** 02:20 | **Fin:** 02:50 | **Duración:** 30s
**Visual:** INFOGRAPH timeline horizontal | **Comp AE:** SC07_JORNADA

#### Elementos y comportamiento
| Elemento | Aparece en | Animación | Sale en |
|----------|-----------|-----------|---------|
| Eje horizontal (línea de tiempo) | 02:20 | draw-on izq→der, 800ms | 02:50 |
| Hito 5:30 AM "Sale de Ecatepec" | 02:23 | drop-in desde arriba + fade, 400ms | 02:50 |
| Hito 7:00 AM "Cruza frontera" | 02:25 | drop-in, 400ms | 02:50 |
| Hito 9:00 AM "Llega al trabajo" | 02:27 | drop-in, 400ms | 02:50 |
| Barra naranja "traslado" | 02:29 | fill izq→der, 600ms | 02:50 |
| Hito 6:00 PM / 8:00 PM | 02:32 | drop-in secuencial, 400ms c/u | 02:50 |
| Texto "14 HORAS fuera de casa" | 02:38 | fade + scale, 600ms | 02:50 |

**Regla de sincronización:** Cada hito aparece 0.5 seg antes de que la voz lo mencione (el ojo prepara al oído).

#### Salida: Cut duro a ESCENA 08

---

### ESCENA 08 — Diagrama flujo fiscal diferencial
**Chunk:** CHUNK_08 | **Inicio:** 02:50 | **Fin:** 03:20 | **Duración:** 30s
**Visual:** DIAGRAM fiscal A vs B | **Comp AE:** SC08_FLUJO_FISCAL

#### Elementos y comportamiento
| Elemento | Aparece en | Animación | Sale en |
|----------|-----------|-----------|---------|
| Trabajador A (Condesa) + ruta completa | 02:51 | build secuencial: ícono → flecha → empresa → ISN → servicio, 500ms por elemento | 03:03 |
| Trabajador B (Ecatepec) + ruta incompleta | 03:03 | mismo build, pero la flecha de "servicio" no cierra — cut animado en la flecha | 03:18 |
| Texto "El impuesto sigue al TRABAJO" | 03:10 | fade + slide-up, 400ms | 03:20 |
| Texto "No al trabajador." | 03:14 | fade (separado, 1 seg después), 400ms | 03:20 |

**Momento crítico:** El "corte" en la flecha de servicios del Trabajador B se anima como un dash animado que se disuelve — visualmente la conexión existe pero está rota. Sincronizado con la pausa dramática del chunk: "El impuesto sigue al TRABAJO. [...] No al trabajador."

#### Salida: Cut duro a ESCENA 09

---

### ESCENA 09 — Mapa Metro CDMX vs. límite ZMVM
**Chunk:** CHUNK_09 | **Inicio:** 03:20 | **Fin:** 03:50 | **Duración:** 30s
**Visual:** MAP esquemático Metro | **Comp AE:** SC09_METRO

#### Elementos y comportamiento
| Elemento | Aparece en | Animación | Sale en |
|----------|-----------|-----------|---------|
| Mapa base ZMVM (fondo gris Edomex) | 03:20 | fade, 500ms | 03:50 |
| Líneas Metro (12 líneas colores oficiales) | 03:22 | draw-on simultáneo desde estación Pantitlán/centro, 1500ms | 03:50 |
| Estaciones (puntos) | 03:23 | appear secuencial, 15ms por estación | 03:50 |
| Límite CDMX-Edomex (línea punteada roja) | 03:26 | draw-on, 600ms, gruesa — se impone sobre el mapa | 03:50 |
| Zona Edomex → gris oscuro + texto "SIN COBERTURA" | 03:28 | fill + fade, 700ms | 03:50 |
| Texto "195 estaciones. 0 en Edomex." | 03:32 | fade + slide-up, 500ms | 03:50 |

**El argumento visual:** Las líneas de Metro se dibujan confiadas y coloridas, luego la línea fronteriza roja aparece y las corta. El Edomex "se oscurece" después de ver el límite. La secuencia cuenta la historia sin narración.

#### Sincronización con voz
- La frontera roja aparece cuando la voz dice "porque el Metro de Ciudad de México tiene..."
- El texto "0 en Edomex" aparece en la pausa antes de "La red de transporte masivo..."

#### Salida: Cut duro a ESCENA 10

---

### ESCENA 10 — Mapa de pobreza municipal
**Chunk:** CHUNK_10 | **Inicio:** 03:50 | **Fin:** 04:20 | **Duración:** 30s
**Visual:** MAP-COR pobreza | **Comp AE:** SC10_POBREZA

#### Elementos y comportamiento
| Elemento | Aparece en | Animación | Sale en |
|----------|-----------|-----------|---------|
| Mapa coroplético ZMVM (pobreza) | 03:50 | revelado coroplético, 800ms | 04:20 |
| Leyenda escala de colores | 03:51 | fade, 300ms | 04:20 |
| Highlight Ecatepec (pulso rojo) | 03:56 | scale 100→106% + glow, 400ms, ease-out; loop 2 veces | 04:10 |
| Counter "43.5% en pobreza" | 03:58 | count-up 0→43.5, 1500ms, ease-out expo | 04:10 |
| Counter "786,000 personas" | 04:02 | count-up 0→786000, 1500ms | 04:10 |
| Texto "2° municipio más pobre de México" | 04:06 | fade + slide-up, 500ms | 04:20 |
| Fuente "CONEVAL 2020" | 03:51 | fade, 300ms | 04:20 |

#### Animación de salida
- **Tipo:** Fade a negro, 700ms — fin del Acto 3, inicio del Acto 4

---

### ESCENA 11 — Tasas ISN + valor agregado
**Chunk:** CHUNK_11 | **Inicio:** 04:20 | **Fin:** 05:00 | **Duración:** 40s
**Visual:** MAP-COR tasas (20s) + CHART-BAR valor agregado (20s) | **Comp AE:** SC11_TENSION_ISN

#### Parte A: Mapa tasas ISN (04:20–04:40)
| Elemento | Aparece en | Animación | Sale en |
|----------|-----------|-----------|---------|
| Mapa bicolor CDMX (4%) vs Edomex (2-3%) | 04:20 | fill entidades, 700ms | 04:40 |
| Etiqueta "CDMX: 4%" | 04:23 | fade, 400ms | 04:40 |
| Etiqueta "Edomex: 2-3%" | 04:25 | fade, 400ms | 04:40 |
| Texto "Mayor valor → Mayor ISN → CDMX" | 04:30 | fade + slide-up, 400ms | 04:40 |

#### Parte B: Barras valor agregado (04:40–05:00)
| Elemento | Aparece en | Animación | Sale en |
|----------|-----------|-----------|---------|
| Ejes X e Y | 04:40 | fade, 300ms | 05:00 |
| Barras CDMX (azul, más altas) | 04:42 | grow-up desde base, 600ms, ease-out | 05:00 |
| Barras Edomex (naranja, más bajas) | 04:45 | grow-up, 600ms | 05:00 |
| Flecha anotación "→ Mayor ISN" | 04:50 | draw-on, 400ms | 05:00 |

#### Sincronización con voz
- Mapa entra con "Hay un argumento en contra"
- Transición a barras cuando voz dice "Pero hay una diferencia ESTRUCTURAL"

#### Salida: Cut duro a ESCENA 12

---

### ESCENA 12 — Mapa precios de vivienda
**Chunk:** CHUNK_12 | **Inicio:** 05:00 | **Fin:** 05:35 | **Duración:** 35s
**Visual:** MAP-COR precios vivienda | **Comp AE:** SC12_VIVIENDA

#### Elementos y comportamiento
| Elemento | Aparece en | Animación | Sale en |
|----------|-----------|-----------|---------|
| Mapa ZMVM precio/m² | 05:00 | revelado coroplético, 800ms | 05:35 |
| Marcador Benito Juárez "~$70,000/m²" | 05:05 | fade + bubble, 400ms | 05:35 |
| Marcador Ecatepec "~$15,000/m²" | 05:08 | fade + bubble, 400ms | 05:35 |
| Texto "4.5x diferencia de precio" | 05:15 | fade + scale, 600ms, ease-out | 05:35 |
| Leyenda gradiente precio | 05:01 | fade, 300ms | 05:35 |

#### Sincronización con voz
- Los marcadores de precio aparecen cuando la voz dice "entre tres y CINCO VECES mayor"
- El ratio "4.5x" aparece en la pausa antes de "La periferia no es una elección LIBRE"

#### Animación de salida
- **Tipo:** Fade a negro, 900ms — transición al Acto 5 (pausa visual más larga)

---

### ESCENA 13 — Pantalla oscura "El dato que no existe"
**Chunk:** CHUNK_13 | **Inicio:** 05:35 | **Fin:** 06:05 | **Duración:** 30s
**Visual:** TYPO pantalla oscura | **Comp AE:** SC13_EL_DATO

#### Animación de entrada
- **Tipo:** Ya en negro desde transición ESCENA 12
- Fondo `#0D1117` — mismo de la apertura

#### Elementos y comportamiento (secuencia de texto progresivo)
| Elemento | Aparece en | Animación | Sale en | Notas |
|----------|-----------|-----------|---------|-------|
| Línea 1: "¿Cuánto del ISN de CDMX viene de trabajo mexiquense?" | 05:38 | fade, 600ms, Inter ExtraBold 48px `#F4F6F9` | — | |
| [silencio visual 2 seg] | 05:44 | — | — | No mover nada |
| Línea 2: "Ese dato no existe." | 05:46 | fade, 500ms, Inter ExtraBold 72px `#E8520A` | — | Tamaño mayor = peso mayor |
| [silencio visual 2 seg] | 05:51 | — | — | |
| Línea 3: "Podría calcularse." | 05:53 | fade, 500ms, Inter Medium 48px `#93C6E4` | — | Tono más suave = apertura |
| Diagrama mínimo IMSS+EOD | 05:57 | fade, 500ms | 06:05 | Pequeño, bajo el texto |

#### Salida: Fade progresivo a negro, 1000ms

---

### ESCENA 14 — Cierre: mapa con interrogante
**Chunk:** CHUNK_14 | **Inicio:** 06:05 | **Fin:** 06:30 | **Duración:** 25s
**Visual:** MAP-FLOW apertura (reutilizado) + "?" | **Comp AE:** SC14_CIERRE

**Estrategia de producción:** SC14 anida SC01 como pre-comp y añade capas encima. No re-renderizar el mapa.

#### Elementos y comportamiento
| Elemento | Aparece en | Animación | Sale en |
|----------|-----------|-----------|---------|
| Mapa apertura (pre-comp SC01) | 06:05 | fade desde negro, 800ms | 06:30 |
| Signo "?" sobre la frontera CDMX-Edomex | 06:10 | scale 0→100% + fade, 600ms, ease-out; luego pulso scale 100→104→100%, loop | 06:25 |
| Texto "La frontera invisible tiene precio. Nadie lo ha cobrado todavía." | 06:14 | fade, 700ms, Inter Medium 36px `#F4F6F9` | 06:28 |
| Fade final a negro | 06:25 | fade total, 1200ms | 06:30 |

#### Sincronización con voz
- El "?" aparece en la pausa de 2 seg antes de la pregunta final ("¿cuánto le debe...")
- El texto de cierre aparece mientras la voz formula la pregunta
- El fade a negro comienza en el último beat de la pregunta

---

## Tabla maestra de timing

| # | Escena | Inicio | Fin | Dur (s) | Visual | Trans. entrada | Trans. salida |
|---|--------|--------|-----|---------|--------|---------------|---------------|
| 01 | Apertura nocturna | 00:00 | 00:15 | 15 | MAP-FLOW oscuro | Fade negro →  | Cut |
| 02 | Diagrama ISN mecanismo | 00:15 | 00:45 | 30 | DIAGRAM | Fade blanco | Cross dissolve |
| 03 | PIB + pastel servicios | 00:45 | 01:05 | 20 | MAP-COR + PIE | Cross dissolve | Cut |
| 04 | Crecimiento Ecatepec | 01:05 | 01:30 | 25 | BAR + MAP | Cut | Cut |
| 05 | Sistema implícito (typo) | 01:30 | 01:50 | 20 | TYPO | Fade negro | Fade negro |
| 06 | Flujos EOD 2017 | 01:50 | 02:20 | 30 | MAP-FLOW claro | Fade negro → | Cut |
| 07 | Timeline jornada | 02:20 | 02:50 | 30 | INFOGRAPH | Cut | Cut |
| 08 | Flujo fiscal diferencial | 02:50 | 03:20 | 30 | DIAGRAM | Cut | Cut |
| 09 | Metro vs. límite ZMVM | 03:20 | 03:50 | 30 | MAP esquemático | Cut | Cut |
| 10 | Pobreza municipal | 03:50 | 04:20 | 30 | MAP-COR | Cut | Fade negro |
| 11 | Tasas ISN + valor agregado | 04:20 | 05:00 | 40 | MAP + BAR | Fade negro → | Cut |
| 12 | Precios de vivienda | 05:00 | 05:35 | 35 | MAP-COR | Cut | Fade negro |
| 13 | El dato que no existe | 05:35 | 06:05 | 30 | TYPO oscura | Fade negro → | Fade negro |
| 14 | Cierre con "?" | 06:05 | 06:30 | 25 | MAP-FLOW (pre-comp) | Fade negro → | Fade negro |

---

## Assets — checklist de producción

### Mapas
- [ ] M01 — MAP-FLOW ZMVM nocturno (Esc. 1, 14) — EOD 2017 + shapefile ZMVM
- [ ] M02 — MAP-COR PIB México por entidad (Esc. 3) — INEGI PIBE 2023 + MGE estatal
- [ ] M03 — MAP expansión urbana ZMVM décadas (Esc. 4) — INEGI uso de suelo histórico
- [ ] M04 — MAP-FLOW ZMVM diurno detallado (Esc. 6) — EOD 2017 + shapefile ZMVM
- [ ] M05 — MAP esquemático Metro CDMX + límite (Esc. 9) — STC Metro GeoJSON + shapefile ZMVM
- [ ] M06 — MAP-COR pobreza municipal ZMVM (Esc. 10) — CONEVAL 2020 + shapefile municipal
- [ ] M07 — MAP-COR precios vivienda ZMVM (Esc. 12) — SHF / INFONAVIT

### Gráficos
- [ ] G01 — PIE composición PIB CDMX por sector (Esc. 3) — INEGI PIBE 2023
- [ ] G02 — BAR crecimiento Ecatepec 1970-2020 (Esc. 4) — INEGI Censos
- [ ] G03 — MAP bicolor tasas ISN (Esc. 11a) — EY Matriz ISN 2025
- [ ] G04 — BAR valor agregado por sector/entidad (Esc. 11b) — INEGI PIBE + IMSS

### Fuentes tipográficas (instalar en AE antes de ejecutar JSX)
- [ ] Inter (todos los pesos: 400, 500, 800) — Google Fonts
- [ ] JetBrains Mono Regular — Google Fonts

### Audio
- [ ] chunk_01_v1.wav (00:00–00:15)
- [ ] chunk_02_v1.wav (00:15–00:45)
- [ ] chunk_03_v1.wav (00:45–01:05)
- [ ] chunk_04_v1.wav (01:05–01:30)
- [ ] chunk_05_v1.wav (01:30–01:50)
- [ ] chunk_06_v1.wav (01:50–02:20)
- [ ] chunk_07_v1.wav (02:20–02:50)
- [ ] chunk_08_v1.wav (02:50–03:20)
- [ ] chunk_09_v1.wav (03:20–03:50)
- [ ] chunk_10_v1.wav (03:50–04:20)
- [ ] chunk_11_v1.wav (04:20–05:00)
- [ ] chunk_12_v1.wav (05:00–05:35)
- [ ] chunk_13_v1.wav (05:35–06:05)
- [ ] chunk_14_v1.wav (06:05–06:30)
- [ ] Música ambiente (opcional, 0-3dB, ambiental electroacústica) — buscar en Epidemic Sound / Artlist

---

## Checklist pre-render

- [ ] Ejecutar ae_script.jsx en After Effects — crear estructura de composiciones
- [ ] Instalar Inter y JetBrains Mono antes de ejecutar el script
- [ ] Importar todos los WAV de voz y sincronizar con timeline
- [ ] Importar todos los mapas (SVG/PNG exportados de QGIS/Python)
- [ ] Importar todos los gráficos (SVG exportados de Flourish/Datawrapper)
- [ ] Verificar sincronización voz-imagen en puntos críticos (chunks 01, 06, 08, 14)
- [ ] Color profile: sRGB (para YouTube — no usar Display P3)
- [ ] Resolución: 1920×1080, 24fps
- [ ] Exportar en H.264, 16 Mbps, AAC 320 kbps
- [ ] Exportar versión corta 9:16 (1080×1920) para IG/TikTok — crop + scale de los mapas

---
*Generado por Agente A5 — Sistema de Video-Ensayos Cartográficos*
