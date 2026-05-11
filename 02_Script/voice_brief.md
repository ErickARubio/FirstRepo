# Brief de Voz — El impuesto que no regresa

**Proyecto:** 2026-05-edomex-cdmx
**Agente:** A4 Director de Voz
**Fecha:** 2026-05-10
**Estado:** Borrador v1.0
**Input:** script_draft.md v1.0 (aprobado)

---

## Estadísticas

| Métrica | Valor |
|---------|-------|
| Chunks totales | 14 |
| Duración estimada | 6:30 |
| Palabras limpias | ~820 |
| Velocidad de síntesis | 0.90 (escala ElevenLabs) |
| Voz recomendada | Mateo (es-MX) |
| Modelo ElevenLabs | Multilingual v2 |

---

## Perfil de voz seleccionada

### Casting: Mateo (ElevenLabs, es-MX)

**Justificación:** Mateo ofrece un registro periodístico de profundidad — autoritativo sin ser corporativo, cálido sin ser informal. Es el registro del periodismo de largo aliento latinoamericano: el narrador de un documental de investigación, no el locutor de un noticiario. Ideal para contenido analítico de 6 minutos donde el espectador debe confiar en quien habla.

**Alternativas a verificar en el panel ElevenLabs:**
- Si Mateo no está disponible: buscar voz masculina en es-MX con "journalist", "documentary", "deep" como descriptores
- Alternativa femenina: Sofia (es-LAT) — verificar disponibilidad; ritmo más ágil, adecuado si se quiere romper con la convención del narrador masculino en economía

**Parámetros ElevenLabs recomendados:**

```json
{
  "model_id": "eleven_multilingual_v2",
  "voice_settings": {
    "stability": 0.55,
    "similarity_boost": 0.75,
    "style": 0.30,
    "use_speaker_boost": true
  },
  "speaking_rate": 0.90
}
```

**Nota técnica:** Si el chunk de cierre (CHUNK_14) suena demasiado conclusivo, bajar `stability` a 0.45 para esa escena específica — más variabilidad natural en la voz ayuda a la apertura reflexiva que necesita el Acto 5.

---

## Instrucciones de dirección por acto

### Acto 1 — Gancho (Chunks 01–02, 00:00–00:45)
**Tono:** Directo, sin reverencia. No es una pregunta retórica — es un hallazgo que se comparte con calma. Algo entre "fíjate en esto" y "nadie te ha contado esto".
**Velocidad:** Ligeramente más lenta que el resto del video. El dato del ISN necesita espacio para que el espectador entienda el mecanismo antes de que la narración lo procese.
**Énfasis:** En "INVISIBLE" (Chunk 01) y en "cuatro pesos de cada cien" y "ciudad DIFERENTE" (Chunk 02). No exagerar — el énfasis es de peso, no de drama.
**Pausas clave:** La pausa después de "Nadie la gobierna" en Chunk 01 es dramática — debe sentirse. La pausa antes de "Trabajadores que regresan..." en Chunk 02 marca el giro emocional.

### Acto 2 — Contexto histórico (Chunks 03–05, 00:45–01:50)
**Tono:** Periodístico, objetivo. El narrador establece los hechos. No hay juicio aquí todavía.
**Velocidad:** Normal. No acelerar. Los números deben aterrizar: "mil novecientos setenta" necesita sus sílabas.
**Énfasis:** En los puntos de quiebre histórico — "mil novecientos setenta", "cincuenta años". En la paradoja de Chunk 05: "Nadie diseñó este arreglo."
**Pausa clave:** Después de los dos puntos en Chunk 05 ("un sistema IMPLÍCITO:") — beat de 0.8 segundos antes de enunciar las dos líneas paralelas.

### Acto 3 — Anatomía (Chunks 06–10, 01:50–04:20)
**Tono:** Analítico, preciso. Cada oración es una pieza de evidencia. El narrador no opina — describe con exactitud.
**Velocidad:** Ligeramente más lenta en los datos cuantitativos. Las cifras grandes necesitan espacio entre sílabas para que el cerebro las registre: "siete millones... setecientos setenta mil".
**Énfasis:** En contrastes y comparaciones. "donde se TRABAJA, no donde se VIVE" (Chunk 08). "NINGUNA cruza hacia el Estado de México" (Chunk 09). "SEGUNDO municipio" (Chunk 10).
**Pausa clave:** La pausa más larga del Acto 3 es antes de "El impuesto sigue al TRABAJO. [...] No al trabajador." — aquí la separación de ambas oraciones debe sentirse como dos golpes distintos.

### Acto 4 — Tensión y contradicción (Chunks 11–12, 04:20–05:35)
**Tono:** Más íntimo. El narrador reconoce una complicación genuina, no la descarta. El espectador debe sentir que el video es intelectualmente honesto.
**Velocidad:** Más lenta que el Acto 3. Las pausas `[...]` importan especialmente aquí.
**Énfasis:** En "diferencia ESTRUCTURAL" (Chunk 11) y en la paradoja de la "elección libre" (Chunk 12). El énfasis en "LIBRE" en Chunk 12 debe sonar levemente irónico — no burlón, sino revelador.
**Pausa clave:** Después de "La economía no es de un solo sentido." — pausa de 1 segundo antes del giro "Pero hay una diferencia ESTRUCTURAL."

### Acto 5 — Implicación abierta (Chunks 13–14, 05:35–06:30)
**Tono:** Reflexivo, abierto. La voz baja un registro. Como si el narrador también se estuviera preguntando esto por primera vez.
**Velocidad:** La más lenta del video. "Ningún gobierno lo ha pedido. Y ningún presupuesto lo ha considerado." — cada cláusula necesita su propio espacio.
**Énfasis:** Minimal en Chunk 14. La pregunta final no se enfatiza — se declara con calma. El peso lo carga el silencio después de ella.
**Pausa crítica:** Antes de la pregunta final ("¿cuánto le debe la ciudad...") — 2 segundos completos de silencio. Es la pausa más larga del video. No recortar.

---

## Guía de pronunciación

| Término | Pronunciación correcta | Nota |
|---------|------------------------|------|
| INEGI | "i-NE-gi" (no "INEGI" como acrónimo) | Ya expandido como "Instituto Nacional de Estadística y Geografía" en Chunk 06 |
| IMSS | "i-ME-ese-ese" | Expandido como "Instituto Mexicano del Seguro Social" en Chunk 13 |
| ISN | Siempre pronunciar como "Impuesto Sobre Nóminas" | No usar la sigla en narración |
| PIB | Pronunciar letra por letra: "pi-i-be" | Ya expandido como "producto interno bruto" en Chunk 03 |
| Ecatepec | "e-ca-TE-pec" | Acento en la tercera sílaba |
| Chimalhuacán | "chi-mal-hua-CÁN" | Acento en última sílaba |
| Tlalnepantla | "tla-ne-PAN-tla" | No omitir la "tl" inicial |
| Metrobús | "me-tro-BÚS" | Acento en última sílaba |
| Mexiquenses | "me-xi-KUEN-ses" | Pronunciación natural en mexicano |
| EOD | No mencionar la sigla en voz — ya expandida en el texto | — |
| CONEVAL | No mencionado en narración | — |

---

## Tabla de timing completa

| Chunk | Acto | Texto (primeras 10 palabras) | Inicio | Fin | Dur. (seg) | Notas de dirección |
|-------|------|-------------------------------|--------|-----|------------|---------------------|
| 01 | Gancho | "Cada lunes, millones de personas cruzan una frontera..." | 00:00 | 00:15 | 15 | Pausa dramática después de "Nadie la gobierna" |
| 02 | Gancho | "Hay un mecanismo fiscal que casi nadie conoce..." | 00:15 | 00:45 | 30 | Pausa antes de "Trabajadores que regresan..." |
| 03 | Contexto | "Ciudad de México genera el catorce punto ocho..." | 00:45 | 01:05 | 20 | Velocidad normal; énfasis en "SERVICIOS" al final |
| 04 | Contexto | "Esos servicios necesitan personas. Pero vivir..." | 01:05 | 01:30 | 25 | Bajar velocidad en "cuatrocientos mil... mil novecientos setenta" |
| 05 | Contexto | "Se construyó así un sistema implícito..." | 01:30 | 01:50 | 20 | Pausa de 0.8 seg después de los dos puntos en "implícito:" |
| 06 | Anatomía | "El número es este: siete millones setecientos..." | 01:50 | 02:20 | 30 | "siete millones setecientos setenta mil" — muy lento y separado |
| 07 | Anatomía | "El tiempo promedio de ese viaje es ochenta..." | 02:20 | 02:50 | 30 | Pausa de 1.5 seg después de "cinco y media" |
| 08 | Anatomía | "Y aquí está el mecanismo: el Impuesto Sobre..." | 02:50 | 03:20 | 30 | "TRABAJA... VIVE" — énfasis separado; pausa larga antes de "No al trabajador" |
| 09 | Anatomía | "Con ese impuesto, Ciudad de México financia..." | 03:20 | 03:50 | 30 | Énfasis en "NINGUNA"; pausa antes de "La red de transporte..." |
| 10 | Anatomía | "Mientras tanto, el municipio que envía esos..." | 03:50 | 04:20 | 30 | Leer Ecatepec a la mexicana; pausa de 1 seg antes de "Casi ochocientas mil" |
| 11 | Tensión | "Hay un argumento en contra. El Estado..." | 04:20 | 05:00 | 40 | Pausa de 1 seg antes de "Pero hay una diferencia estructural" |
| 12 | Tensión | "El contraargumento más honesto es otro..." | 05:00 | 05:35 | 35 | "LIBRE" con ironía leve, no burlona |
| 13 | Implicación | "Hay un número que no existe todavía..." | 05:35 | 06:05 | 30 | Voz más baja; cada oración como afirmación separada |
| 14 | Implicación | "Quizás, porque calcular ese número obligaría..." | 06:05 | 06:30 | 25 | 2 seg de silencio antes de la pregunta final; no enfatizar |

**Total: 390 segundos (6:30)**

---

## Flujo de producción sugerido

1. **Generar chunks individualmente** en ElevenLabs (no el texto completo de una vez — los chunks individuales permiten regenerar escenas sin regrabar todo)
2. **Orden de prioridad para revisión:** Chunks 01, 14, 08 primero — son los momentos de mayor carga narrativa
3. **Regenerar hasta 3 veces** por chunk si el timing o el énfasis no es correcto antes de ajustar parámetros
4. **Exportar en WAV 44.1kHz** para edición en Adobe Premiere o DaVinci Resolve
5. **Guardar cada chunk con nomenclatura:** `chunk_01_v1.wav`, `chunk_01_v2.wav` — nunca sobrescribir

---
*Generado por Agente A4 — Sistema de Video-Ensayos Cartográficos*
