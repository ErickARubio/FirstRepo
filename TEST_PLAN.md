# PLAN DE PRUEBA END-TO-END — Sistema Limpio

**Fecha:** 2026-05-11  
**Objetivo:** Validar que el sistema de orquestación y 5 agentes funciona de cero sin dependencias rotas.

---

## SETUP INICIAL

### 1.1 Verificar estructura crítica

```bash
✓ 00_Orchestrator/orchestrator.md — Prompt maestro
✓ 00_Orchestrator/state.json — Estado (limpio, null)
✓ 00_Orchestrator/agents/01_research.md — A1
✓ 00_Orchestrator/agents/02_script.md — A2
✓ 00_Orchestrator/agents/03_visuals.md — A3
✓ 00_Orchestrator/agents/04_voice.md — A4
✓ 00_Orchestrator/agents/05_animation.md — A5
✓ 00_Orchestrator/tools/voice_gen.py — Script de voz (refactorizado)
✓ 00_Orchestrator/templates/ — Todas las plantillas
✓ .env — Contiene ELEVENLABS_API_KEY
✓ 01_Research/, 02_Script/, 03_Assets/, 04_Animation/ — Directorios output
```

### 1.2 Verificar dependencias Python

```bash
pip install -r 00_Orchestrator/tools/requirements.txt
# Debe instalar: python-dotenv, requests, pandas, elevenlabs

python -c "from elevenlabs.client import ElevenLabs; print('✓ ElevenLabs OK')"
```

---

## TEST CASE 1: FASE 1 — INVESTIGACIÓN (Checkpoint 1)

**Descripción:** Ejecutar Agente A1 (Investigador) con un tema de prueba.

### Entrada:
```
Tema: Impacto de la inteligencia artificial en empleos de nivel técnico en México
```

### Proceso:
1. Cargar `orchestrator.md` como prompt maestro
2. Escribir: "Nuevo proyecto: [tema]"
3. Sistema debe:
   - Crear entrada en `state.json` con ID único (2026-05-IA-tech)
   - Invocar `agents/01_research.md`
   - Generar 3 tesis candidatas con 8-12 fuentes Tier 1
   - Guardar en `01_Research/`:
     - `tesis_candidatas.md`
     - `sources.md`
     - `findings.md`

### Validación (Output esperado):
```
✓ findings.md contiene: contexto histórico, 3 tesis debatibles, 8-12 fuentes INEGI/Banxico/BM/OCDE
✓ sources.md contiene: tabla de fuentes con URL, autor, fecha, Tier
✓ tesis_candidatas.md contiene: 3 opciones contradictorias, cada una con argumento/contraargumento
✓ state.json actualizado: fase_actual=1, archivos_generados=[], checkpoints.cp1_tesis=false
```

### Checkpoint 1:
```
USER RESPONSE EXPECTED:
"Apruebo la Tesis 2"

STATE UPDATE:
- state.json.tesis_aprobada = [contenido de Tesis 2]
- state.json.checkpoints.cp1_tesis = true
- Fase pasa a 2
```

---

## TEST CASE 2: FASE 2 — GUION (Checkpoint 2)

**Descripción:** Ejecutar Agente A2 (Guionista) con tesis aprobada.

### Entrada:
```
Tesis aprobada (de CP1) + archivos: findings.md, sources.md
```

### Proceso:
1. Sistema invoca `agents/02_script.md`
2. A2 escribe guion de 6–7 minutos en formato tabla:
   - Narración + Visual + Duración + Fuente
   - 5 actos: Gancho → Contexto → Anatomía → Tensión → Implicación
3. Guarda en `02_Script/script_draft.md`
4. Luego invoca `agents/04_voice.md` (preparación para voz)
5. Genera `02_Script/script_for_elevenlabs.txt` (guion limpio en chunks)

### Validación (Output esperado):
```
✓ script_draft.md contiene: tabla 14-16 escenas, ~820 palabras, 390 seg (6:30)
✓ Cada fila: narración coherente, visual descriptivo, duración en segundos, fuente citada
✓ script_for_elevenlabs.txt contiene: texto limpio en [CHUNK_01]...[CHUNK_14] con separadores ====
✓ state.json.archivos_generados incluye: script_draft.md, script_for_elevenlabs.txt
```

### Checkpoint 2:
```
USER RESPONSE EXPECTED:
"Apruebo el guion. Escena 7: cambiar duración de 30 a 25 seg"

STATE UPDATE:
- A2 integra cambio menor (no reinicia fase)
- state.json.checkpoints.cp2_guion = true
- Fase pasa a 3
```

---

## TEST CASE 3: FASE 3 — DIRECCIÓN VISUAL (Checkpoint 3)

**Descripción:** Ejecutar Agente A3 (Director Visual) con guion.

### Entrada:
```
script_draft.md + sources.md
```

### Proceso:
1. Sistema invoca `agents/03_visuals.md`
2. A3 produce `visual_brief.md`:
   - Tipo visual por escena (mapa, gráfico, imagen, tipografía)
   - Paleta de colores (3 opciones)
   - Tipografía
   - Queries para bancos de imágenes gratuitos
3. Guarda en `03_Assets/visual_brief.md`

### Validación (Output esperado):
```
✓ visual_brief.md contiene:
  - Para cada escena: visual type + descripción + paleta + tipografía
  - 3 opciones de paleta (Opción A/B/C) con hex codes
  - Queries de búsqueda (Unsplash, Pexels, Pixabay) para cada visual
  - Referencia a iconografía/datasets (geopandas, Flourish)
✓ state.json.archivos_generados incluye: visual_brief.md
```

### Checkpoint 3:
```
USER RESPONSE EXPECTED:
"Apruebo Paleta B. Tipografía: mantener recomendación. Visuals: OK"

STATE UPDATE:
- state.json.checkpoints.cp3_visual = true
- Fase pasa a 4
```

---

## TEST CASE 4: FASE 4 — VOZ Y AUDIO (Checkpoint 4)

**Descripción:** Preparar y generar audio con ElevenLabs.

### Entrada:
```
script_for_elevenlabs.txt (chunks del guion)
```

### Proceso:
1. Sistema invoca `agents/04_voice.md`
2. A4 produce `voice_brief.md`:
   - Voz seleccionada (ej: Rachel)
   - Parámetros ElevenLabs (stability, similarity_boost, style)
   - Tabla de timing por chunk
3. Ejecutar `python 00_Orchestrator/tools/voice_gen.py`
4. Script descarga `script_for_elevenlabs.txt` y genera 14 WAV en `03_Assets/audio/`

### Validación (Output esperado):
```
✓ voice_brief.md contiene: voz, parámetros JSON, timing tabla
✓ 03_Assets/audio/ contiene: chunk_01.wav, chunk_02.wav, ..., chunk_14.wav (14 archivos)
✓ Cada WAV: ~3-6 MB, duración correspondiente a chunk
✓ state.json.archivos_generados incluye: voice_brief.md, script_for_elevenlabs.txt, chunk_*.wav
```

### Checkpoint 4:
```
USER RESPONSE EXPECTED:
"Voz OK. Audio suena natural. Adelante a animación"

STATE UPDATE:
- state.json.checkpoints.cp4_voz = true
- Fase pasa a 5
```

---

## TEST CASE 5: FASE 5 — ANIMACIÓN (Checkpoint 5)

**Descripción:** Generar plan de animación y script After Effects.

### Entrada:
```
script_draft.md + visual_brief.md + timing del audio
```

### Proceso:
1. Sistema invoca `agents/05_animation.md`
2. A5 produce:
   - `animation_plan.md`: storyboard técnico con timing exacto
   - `ae_script.jsx`: script ExtendScript para After Effects (automatización)
3. Guarda en `04_Animation/`

### Validación (Output esperado):
```
✓ animation_plan.md contiene:
  - Timeline con timing exacto por escena
  - Definición de todas las transiciones
  - Especificación de layers, efectos, keyframes
✓ ae_script.jsx contiene:
  - Sintaxis ExtendScript válida
  - Crea composition, establece duración, importa assets
  - Automatiza setup de layers y transiciones
✓ state.json.archivos_generados incluye: animation_plan.md, ae_script.jsx
```

### Checkpoint 5 (Final):
```
USER RESPONSE EXPECTED:
"Proyecto listo para producción. Confirmado en After Effects"

STATE UPDATE:
- state.json.checkpoints.cp5_animacion = true
- state.json.fase_actual = "COMPLETADO"
- state.json.estado = "ENTREGA_FINAL"
- history.append(project_data)
```

---

## VALIDACIONES GLOBALES

### Estructura de directorios (post-ejecución):
```
01_Research/
  ├── tesis_candidatas.md ✓
  ├── sources.md ✓
  └── findings.md ✓

02_Script/
  ├── script_draft.md ✓
  ├── script_for_elevenlabs.txt ✓
  └── voice_brief.md ✓

03_Assets/
  ├── visual_brief.md ✓
  └── audio/
      ├── chunk_01.wav ✓
      ├── chunk_02.wav ✓
      └── ... (14 archivos)

04_Animation/
  ├── animation_plan.md ✓
  └── ae_script.jsx ✓

00_Orchestrator/
  ├── state.json (actualizado) ✓
  └── README.md (sin cambios) ✓
```

### state.json (estado final esperado):
```json
{
  "current_project": {
    "id": "2026-05-IA-tech",
    "tema": "Impacto de la IA en empleos técnicos en México",
    "tesis_aprobada": "[contenido]",
    "fase_actual": "COMPLETADO",
    "checkpoints": {
      "cp1_tesis": true,
      "cp2_guion": true,
      "cp3_visual": true,
      "cp4_voz": true,
      "cp5_animacion": true
    },
    "archivos_generados": [
      "01_Research/tesis_candidatas.md",
      "01_Research/sources.md",
      "01_Research/findings.md",
      "02_Script/script_draft.md",
      "02_Script/script_for_elevenlabs.txt",
      "02_Script/voice_brief.md",
      "03_Assets/visual_brief.md",
      "03_Assets/audio/chunk_01.wav",
      ... (todos los chunks)
      "04_Animation/animation_plan.md",
      "04_Animation/ae_script.jsx"
    ],
    "iniciado": "2026-05-11",
    "ultima_actualizacion": "2026-05-11",
    "estado": "ENTREGA_FINAL"
  },
  "history": [
    { "id": "2026-05-IA-tech", "completado": true, "fecha": "2026-05-11" }
  ],
  "settings": { ... }
}
```

---

## CRITERIOS DE ÉXITO

✓ Todos los 5 checkpoints aprobados sin rollback  
✓ 9 archivos críticos generados (3+1+1+2+2)  
✓ 14 archivos WAV descargados exitosamente  
✓ state.json actualizado correctamente en cada fase  
✓ Ningún archivo huérfano o corrupción  
✓ Rutas relativas correctas en todos los links internos  
✓ Formato de salida coherente (Markdown, JSON, WAV)  

---

## PRÓXIMOS PASOS DESPUÉS DE PRUEBA

Si la prueba es exitosa:
1. Archivar este TEST_PLAN.md en referencia
2. Crear nuevo proyecto real (tema diferente)
3. Ejecutar workflow de nuevo
4. Si hay errores, debuggear con los logs de state.json

