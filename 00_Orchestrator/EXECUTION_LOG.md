# EJECUCIÓN DE PRUEBA END-TO-END

**Estado:** LISTO PARA COMENZAR  
**Proyecto de Prueba:** 2026-05-AI-tech  
**Tema:** Impacto de la IA en empleos técnicos en México

---

## PASO 1: VERIFICACIÓN PRE-EJECUCIÓN

### 1.1 Revisar estructura limpia
```bash
ls -la 00_Orchestrator/
ls -la 01_Research/
ls -la 02_Script/
ls -la 03_Assets/
ls -la 04_Animation/
```

**Esperado:** Todos los directorios existen, sin carpetas vacías de placeholder.

### 1.2 Verificar archivos críticos
```bash
cat 00_Orchestrator/state.json
# Esperado: current_project es null
```

### 1.3 Instalar dependencias
```bash
pip install -r 00_Orchestrator/tools/requirements.txt
python -c "from elevenlabs.client import ElevenLabs; print('OK')"
```

---

## PASO 2: INICIAR PROYECTO EN CLAUDE

**Acción:** Abre Claude y carga el prompt maestro:

```
[Cargar contenido de 00_Orchestrator/orchestrator.md]

Luego escribe:
Nuevo proyecto: Impacto de la IA en empleos técnicos en México
```

**Sistema debe responder con:**
```
## FASE 1 — INVESTIGACIÓN
Agente: A1 Investigador
Estado: En progreso

[Invocando agents/01_research.md...]

[Output: 3 tesis candidatas + 8-12 fuentes]

---
⏸ CHECKPOINT 1: ¿Cuál de las 3 tesis apruebas?
```

**Tu respuesta:** `Apruebo la Tesis 2`

---

## PASO 3: CHECKPOINT 1 → FASE 2

**Sistema debe:**
- Actualizar `state.json`: `checkpoints.cp1_tesis = true`
- Guardar archivos en `01_Research/`:
  - `tesis_candidatas.md`
  - `sources.md`
  - `findings.md`

**Verificar:**
```bash
ls -la 01_Research/
# Esperado: 3 archivos .md
cat 01_Research/tesis_candidatas.md | head -20
# Esperado: Formato markdown, 3 tesis con argumentos
```

**Continuación en Claude:**
```
Siguiente: Ejecutar Fase 2
```

---

## PASO 4: FASE 2 — GUION + VOZ PREP

**Sistema debe:**
- Invocar `agents/02_script.md` → genera `script_draft.md`
- Invocar `agents/04_voice.md` → genera `script_for_elevenlabs.txt`
- Guardar en `02_Script/`

**Verificar:**
```bash
ls -la 02_Script/
# Esperado: script_draft.md, script_for_elevenlabs.txt
wc -w 02_Script/script_draft.md
# Esperado: ~800–900 palabras
```

**Tu respuesta:** `Apruebo el guion`

**Sistema debe:**
- Actualizar `state.json`: `checkpoints.cp2_guion = true`

---

## PASO 5: FASE 3 — VISUALS

**Sistema debe:**
- Invocar `agents/03_visuals.md`
- Generar `visual_brief.md`
- Guardar en `03_Assets/`

**Verificar:**
```bash
ls -la 03_Assets/
# Esperado: visual_brief.md
grep -A5 "Paleta A" 03_Assets/visual_brief.md
# Esperado: hex codes y descripción
```

**Tu respuesta:** `Apruebo Paleta B. Visuals OK`

**Sistema debe:**
- Actualizar `state.json`: `checkpoints.cp3_visual = true`

---

## PASO 6: FASE 4 — VOZ (GENERACIÓN DE AUDIO)

**Acción en terminal:**
```bash
cd c:\Users\erick\Projects\Proyecto_01_Remesas
python 00_Orchestrator/tools/voice_gen.py Rachel
```

**Esperado:**
```
===========================================================
  Voice Generator — El impuesto que no regresa
  Modelo: eleven_multilingual_v2
===========================================================

  Buscando voz 'Rachel'... OK
  
  Voces en tu cuenta (X):
     >>> Rachel                    [voice_id]
  
  Script cargado: 14 chunks  |  820 chars totales
  Cuota plan gratuito ElevenLabs: 10,000 chars/mes
  OK — dentro del plan gratuito (9180 chars sobraran)
  
  Output: 03_Assets/audio

  Generando chunk 01/14  (45 chars)... OK — 2.3s — 45 KB
  Generando chunk 02/14  (60 chars)... OK — 2.8s — 52 KB
  ...
  [SKIP]  Chunk 05/14 — chunk_05.wav ya existe (48 KB)
  ...
  Generando chunk 14/14  (25 chars)... OK — 1.2s — 32 KB

  ---------------------------------------------------------
  14/14 chunks completados
  Caracteres consumidos en esta sesion: ~820
  Tiempo total: 45.2s
  
  Todos los WAV en: 03_Assets/audio
  Siguiente paso: abrir After Effects y ejecutar ae_script.jsx
===========================================================
```

**Verificar:**
```bash
ls -la 03_Assets/audio/
# Esperado: chunk_01.wav ... chunk_14.wav (14 archivos)
# Cada uno: 30–60 KB
```

**Sistema debe:**
- Actualizar `state.json`: `checkpoints.cp4_voz = true`

---

## PASO 7: FASE 5 — ANIMACIÓN

**Sistema debe:**
- Invocar `agents/05_animation.md`
- Generar `animation_plan.md` + `ae_script.jsx`
- Guardar en `04_Animation/`

**Verificar:**
```bash
ls -la 04_Animation/
# Esperado: animation_plan.md, ae_script.jsx
head -30 04_Animation/ae_script.jsx
# Esperado: sintaxis ExtendScript válida
```

**Tu respuesta:** `Proyecto listo para producción`

**Sistema debe:**
- Actualizar `state.json`:
  - `fase_actual = "COMPLETADO"`
  - `checkpoints.cp5_animacion = true`
  - `estado = "ENTREGA_FINAL"`

---

## PASO 8: VALIDACIÓN FINAL

### 8.1 Revisar estado final
```bash
cat 00_Orchestrator/state.json | jq .
# Esperado: todos los checkpoints en true, lista de archivos_generados
```

### 8.2 Contar archivos generados
```bash
find 01_Research 02_Script 03_Assets 04_Animation -type f | wc -l
# Esperado: ~25 archivos (3+2+1+14+5)
```

### 8.3 Verificar integridad
```bash
du -sh 03_Assets/audio/
# Esperado: ~600–800 KB (14 WAVs)

du -sh 01_Research 02_Script 03_Assets 04_Animation
# Esperado: total ~1–2 MB
```

---

## RESULTADOS ESPERADOS

✅ **Fase 1:** 3 archivos en `01_Research/`  
✅ **Fase 2:** 2 archivos en `02_Script/`  
✅ **Fase 3:** 1 archivo en `03_Assets/`  
✅ **Fase 4:** 14 WAVs en `03_Assets/audio/`  
✅ **Fase 5:** 2 archivos en `04_Animation/`  
✅ **Total:** 22 archivos generados  
✅ **state.json:** Completamente actualizado con todos los checkpoints en true  

---

## NOTAS

- Si una fase falla, la prueba se detiene y se reporta el error.
- No hay rollback automático; revisar logs y reintenta paso 5 en adelante.
- ElevenLabs requiere credencial válida en `.env`.
- Los archivos WAV se cachean; si existen, se omiten (útil para reintento).

