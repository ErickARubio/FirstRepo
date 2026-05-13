# Brief de Voz — La geografía invisible del subsidio migrante
**Proyecto:** 2026-05-remesas-mx
**Agente:** A4 Director de Voz
**Fecha:** 2026-05-13
**Estado:** Borrador v1.0
**Input:** script_draft.md v1.0 (aprobado)

---

## Estadísticas

| Métrica | Valor |
|---------|-------|
| Chunks totales | 11 |
| Duración estimada | 6:30 |
| Palabras limpias | ~901 |
| Velocidad de síntesis | 0.90 (escala ElevenLabs) |
| Voz recomendada | Masculino es-MX, tono periodístico profundo |
| Modelo ElevenLabs | eleven_multilingual_v2 |
| Caracteres estimados | ~4,800 (dentro del límite gratuito de 10,000/mes) |

---

## Perfil de voz seleccionada

### Casting: voz masculina, periodístico de profundidad, es-MX

**Perfil objetivo:** El narrador de un documental económico de investigación — no el locutor de un noticiario, no el presentador de un podcast de negocios. La referencia es el periodismo de largo aliento latinoamericano: Carlos Monsiváis leyendo datos, no un conductor de televisión. Autoritativo, cálido, sin reverencia hacia el poder.

**Cómo seleccionar la voz en el panel ElevenLabs:**
1. Ir a elevenlabs.io → Voice Library
2. Filtrar por idioma: `Spanish` o `es-MX` / `es-419`
3. Buscar descriptores: "documentary", "deep", "journalist", "narrative"
4. Probar con el Chunk 01 del script antes de producir todos los chunks
5. Verificar que las pausas `[...]` sean respetadas — si la voz las ignora, ajustar `stability` a 0.60

**Alternativa femenina:** Una voz femenina periodística rompería la convención del narrador masculino en economía — si el usuario prefiere este enfoque, buscar `es-LAT` con descriptor "analytical" o "documentary". El guion funciona igualmente bien con voz femenina.

**Parámetros ElevenLabs:**

```python
from elevenlabs.types import VoiceSettings

voice_settings = VoiceSettings(
    stability=0.55,
    similarity_boost=0.75,
    style=0.30,
    use_speaker_boost=True,
    speed=0.90,
)
model_id = "eleven_multilingual_v2"
```

> **Nota técnica SDK v1.x:** El campo es `speed`, no `speaking_rate`. Rango: 0.7 (muy lento) – 1.2 (rápido). Para video-ensayo analítico: 0.85–0.95.

**Para el Chunk 11 (implicación final):** bajar `speed` a 0.85 y `stability` a 0.48 — más variabilidad natural en la voz ayuda al tono reflexivo del cierre.

---

## Instrucciones de dirección por acto

### Acto 1 — Gancho (Chunk 01, 00:00–00:45)
**Tono:** Directo. Sin suspenso artificial. Como si acabaras de revisar un reporte del Banco Mundial y compartes lo que encontraste. No es una pregunta retórica — es un hallazgo.
**Velocidad:** Ligeramente más lenta que el resto. El número de $67,637 millones necesita espacio. La pausa después de él es dramática.
**Énfasis:** En "TODO el petróleo", "MAYOR fuente de divisas", "los MISMOS de hace sesenta años", "Es una TRAMPA".
**Pausa crítica:** La pausa `[...]` después de "sesenta y siete mil millones de dólares" debe sentirse como un beat de 1.5 segundos. Es el momento en que el espectador procesa la escala del número.

### Acto 2 — Contexto histórico (Chunks 02–03, 00:45–02:00)
**Tono:** Periodístico, objetivo. El narrador establece los hechos históricos sin juicio. Los años son puntos de quiebre, no datos de relleno.
**Velocidad:** Normal en narración histórica. Bajar al leer nombres geográficos: "Mi-choa-cán, Gua-na-jua-to y Ja-lis-co" — darles sus sílabas.
**Énfasis:** En "Los circuitos, NO" (el giro central del Chunk 02). En "SESENTA AÑOS después" — peso de tiempo. En "NIETOS de los braceros" (Chunk 03).
**Pausa crítica:** Después de "El programa terminó en mil novecientos sesenta y cuatro." — 1.5 segundos antes de "Los circuitos, NO." Esta pausa hace el contraste.

### Acto 3 — Anatomía (Chunks 04–08, 02:00–04:30)
**Tono:** Analítico, preciso. Cada oración es una pieza de evidencia. El narrador no opina — describe con exactitud quirúrgica.
**Velocidad:** Ligeramente más lenta en datos cuantitativos. "entre el CINCO y el QUINCE por ciento" — cada número pronunciado con peso. No apresurar.
**Énfasis:** En los contrastes: "NO provee" (Chunk 04), "TAMBIÉN la sostienen" (Chunk 06), "OTRO país" (Chunk 07), "El MISMO ciclo. El MISMO mapa." (Chunk 08).
**Pausa crítica:** En Chunk 06, la pausa antes de "TAMBIÉN la sostienen" — el giro de que las remesas no solo tapan la ausencia del Estado sino que la perpetúan — necesita 1.5 segundos de silencio.

### Acto 4 — Tensión (Chunks 09–10, 04:30–05:45)
**Tono:** Más íntimo. El narrador reconoce una complicación genuina, no la descarta. El espectador debe sentir que el video es intelectualmente honesto.
**Velocidad:** Más lenta. Los `[...]` importan especialmente aquí. La honestidad del contraargumento necesita su tiempo.
**Énfasis:** En "completamente REAL" y "ÚNICO plan" (Chunk 09) — el primero con reconocimiento, el segundo con peso crítico. En "PUNTO DE FALLA" y "FRÁGIL" (Chunk 10).
**Pausa crítica:** En Chunk 09, pausa larga después de "Ese argumento es completamente REAL." — 2 segundos — antes de "Y es INSUFICIENTE." La honestidad intelectual requiere ese espacio.

### Acto 5 — Implicación abierta (Chunk 11, 05:45–06:30)
**Tono:** Reflexivo, abierto. La voz baja un registro. Como si el narrador también estuviera procesando la pregunta por primera vez. No concluyente.
**Velocidad:** La más lenta del video. 0.85 en lugar de 0.90.
**Énfasis:** Mínimo. La pregunta final no se énfatiza — se declara con calma. El silencio después de ella carga el peso.
**Pausa crítica:** Antes de "¿quién paga la deuda de SESENTA AÑOS...?" — 2 segundos completos. Es la pausa más larga del video. No recortar.

---

## Guía de pronunciación

| Término | Pronunciación | Nota |
|---------|--------------|------|
| Michoacán | "mi-choa-CÁN" | Acento en última sílaba |
| Guanajuato | "gua-na-JÚA-to" | La "j" como aspirada mexicana |
| Guerrero | "gue-RRE-ro" | Doble r suave |
| Oaxaca | "ua-HA-ca" | La x es como "j" en español mexicano |
| INEGI | Expandido en texto como "Instituto Nacional de Estadística y Geografía" | No pronunciar como sigla |
| CONEVAL | No aparece en la narración | — |
| ENIGH | Expandido como "Encuesta Nacional de Ingresos y Gastos de los Hogares" | No pronunciar como sigla |
| Banco Mundial | "BAN-co mun-DIAL" | Sin siglas, siempre expandido |
| per cápita | "per CÁ-pi-ta" | Pronunciación correcta en español |
| bracero/braceros | "bra-CE-ro" | Acento en segunda sílaba |
| remesas | "re-ME-sas" | Término clave — pronunciar con claridad, sin apresurar |

---

## Tabla de timing completa

| Chunk | Acto | Texto (primeras 8 palabras) | Inicio | Fin | Dur. (seg) | Escenas | Nota de dirección |
|-------|------|------------------------------|--------|-----|------------|---------|-------------------|
| 01 | Gancho | "Cada año, los mexicanos que viven en..." | 00:00 | 00:45 | 45 | 1–2 | Pausa 1.5s después de "sesenta y siete mil millones"; "Es una trampa" — contundente |
| 02 | Contexto | "Todo empieza en mil novecientos cuarenta y dos..." | 00:45 | 01:40 | 55 | 3–4 | Pausa 1.5s después de "Los circuitos, NO"; bajar velocidad en nombres geográficos |
| 03 | Contexto | "Las familias que dependen hoy del dinero..." | 01:40 | 02:00 | 20 | 5 | Tono puente — conecta el contexto histórico con la anatomía |
| 04 | Anatomía | "¿Adónde va ese dinero cuando llega?..." | 02:00 | 02:30 | 30 | 6 | Pausa 1s después de la pregunta inicial; énfasis en "NO provee" |
| 05 | Anatomía | "Los estudios basados en esa encuesta muestran..." | 02:30 | 03:00 | 30 | 7 | "entre el CINCO y el QUINCE" — deliberado; pausa antes de "Son el precio" |
| 06 | Anatomía | "Y aquí viene la consecuencia más silenciosa..." | 03:00 | 03:30 | 30 | 8 | Pausa 1.5s antes de "TAMBIÉN la sostienen" |
| 07 | Anatomía | "El circuito de migración no extrae..." | 03:30 | 04:00 | 30 | 9 | "CONSTRUIRÍA" — con peso condicional; pausa antes de "de OTRO país" |
| 08 | Anatomía | "El resultado es un equilibrio trágico..." | 04:00 | 04:30 | 30 | 10 | Últimas tres oraciones solas, con pausa entre cada una |
| 09 | Tensión | "Aquí está el contraargumento que merece..." | 04:30 | 05:10 | 40 | 11 | Pausa 2s después de "completamente REAL"; "ÚNICO plan" — énfasis final |
| 10 | Tensión | "El riesgo de depender de un solo mecanismo..." | 05:10 | 05:45 | 35 | 12 | Cada riesgo en línea separada: "Se llama X. / Se llama Y." |
| 11 | Implicación | "En varias comunidades de Michoacán y Oaxaca..." | 05:45 | 06:30 | 45 | 13–14 | Speed 0.85; pausa 2s antes de la pregunta final; no enfatizar — dejar sonar |

**Total: 11 chunks | ~390 segundos (6:30)**

---

## Flujo de producción

1. **Orden de grabación recomendado:** Chunk 01 primero (el gancho define el tono de todo). Si queda bien, grabar en orden.
2. **Máximo 3 intentos por chunk** antes de ajustar parámetros. Si el timing falla en el intento 3, revisar el texto del chunk (puede ser muy denso).
3. **Chunks prioritarios para revisión humana:** 01 (gancho), 09 (contraargumento), 11 (cierre). Son los momentos de mayor carga emocional.
4. **Formato de exportación:** WAV, 44.1 kHz — compatible con Adobe Premiere y DaVinci Resolve.
5. **Nomenclatura:** `chunk_01_v1.wav`, `chunk_01_v2.wav` — nunca sobrescribir tomas.
6. **Usar `voice_gen.py`:** El script `00_Orchestrator/tools/voice_gen.py` ya está configurado para ElevenLabs SDK v1.x. Pasar cada chunk como string.

---
*Generado por Agente A4 — Sistema de Video-Ensayos Cartográficos*
