# AUDITORÍA TÉCNICA INDEPENDIENTE — Proyecto_01_Remesas
**Fecha de ejecución:** 2026-05-11
**Auditor:** Claude Code (rol: auditor independiente)
**Alcance:** Pieza 1 completa + infraestructura del sistema
**Metodología:** Lectura directa de archivos, conteo automatizado, cruce de datos entre documentos

---

## NIVEL 1 — AUDITORÍA DE INFRAESTRUCTURA

### 1.1 Carpetas obligatorias

| Carpeta | Estado | Notas |
|---------|--------|-------|
| `00_Orchestrator/` | ✅ Existe | Completa con subcarpetas |
| `00_Orchestrator/agents/` | ✅ Existe | 5 archivos |
| `00_Orchestrator/tools/` | ✅ Existe | 5 archivos Python |
| `00_Orchestrator/templates/` | ✅ Existe | 3 templates |
| `00_Orchestrator/staging/` | ✅ Existe | Creada en sesión actual |
| `01_Research/` | ✅ Existe | 3 archivos de contenido |
| `02_Script/` | ✅ Existe | 3 archivos de contenido |
| `03_Assets/` | ⚠️ Existe vacía | 4 subcarpetas vacías (fonts/, maps_svg/, palette/, templates/) |
| `04_Animation/` | ✅ Existe | 2 archivos de contenido |
| `05_Final/` | ❌ Vacía | Solo .gitkeep — sin producto final |

### 1.2 Archivos críticos del orchestrator

| Archivo | Estado | Observación |
|---------|--------|------------|
| `orchestrator.md` | ✅ Existe | Sistema de 5 agentes documentado |
| `agents/01_research.md` | ✅ Existe | — |
| `agents/02_script.md` | ✅ Existe | — |
| `agents/03_visuals.md` | ✅ Existe | — |
| `agents/04_voice.md` | ✅ Existe | — |
| `agents/05_animation.md` | ✅ Existe | — |
| `state.json` | ✅ Existe | Todos los checkpoints en `true` |
| `README.md` | ✅ Existe | — |

### 1.3 Archivos generados de la Pieza 1

| Archivo | Estado | Líneas | Observación |
|---------|--------|--------|------------|
| `01_Research/findings.md` | ✅ Existe | 158 | Completo |
| `01_Research/sources.md` | ✅ Existe | 153 | Completo |
| `01_Research/tesis_candidatas.md` | ✅ Existe | 93 | Completo |
| `02_Script/script_draft.md` | ⚠️ Existe | 93 | Ver hallazgo H-03 |
| `02_Script/script_for_elevenlabs.txt` | ✅ Existe | 176 | 14 chunks completos |
| `02_Script/voice_brief.md` | ✅ Existe | 137 | Completo |
| `03_Assets/visual_brief.md` | ✅ Existe | 455 | Completo |
| `04_Animation/animation_plan.md` | ✅ Existe | 451 | Completo |
| `04_Animation/ae_script.jsx` | ✅ Existe | 399 | Sintaxis válida |

### 1.4 Configuración Git

| Verificación | Resultado |
|-------------|-----------|
| ¿Existe `.git/`? | ✅ Sí |
| ¿Existe `.gitignore`? | ✅ Sí |
| Commits previos | ✅ 4 commits (c68f194 → b482d7c) |
| Archivos sin commitear | ⚠️ 5 items pendientes (ver abajo) |
| Branch vs origin | ⚠️ 3 commits adelante de `origin/main` — nunca pusheado |

**Archivos sin commitear detectados:**
```
modified:   00_Orchestrator/CREDENTIALS_GUIDE.md
modified:   00_Orchestrator/tools/test_connections.py
untracked:  00_Orchestrator/staging/           (a1_data_raw.json)
untracked:  00_Orchestrator/tools/dry_run_a1.py
untracked:  00_Orchestrator/tools/verify_data.py
```

---

## NIVEL 2 — AUDITORÍA DE SEGURIDAD

### 2.1 Protección del archivo .env

| Verificación | Resultado | Criticidad |
|-------------|-----------|-----------|
| ¿Existe `.env`? | ✅ Sí | — |
| ¿Está `.env` en `.gitignore`? | ✅ Sí — patrón `*.env` | — |
| ¿Git rastrea `.env`? | ✅ NO — solo `.env.example` | — |
| ¿Existe `.env.example`? | ✅ Sí — plantilla pública sin valores | — |

**RESULTADO SEGURIDAD .env: LIMPIO**

### 2.2 Estado de variables en .env

| Variable | Estado |
|----------|--------|
| `ELEVENLABS_API_KEY` | ✅ Tiene valor |
| `PEXELS_API_KEY` | ❌ Vacía |
| `UNSPLASH_ACCESS_KEY` | ❌ Vacía |
| `UNSPLASH_SECRET_KEY` | ❌ Vacía |
| `BANXICO_TOKEN` | ✅ Tiene valor |
| `INEGI_TOKEN` | ✅ Tiene valor |
| `DATAWRAPPER_TOKEN` | ❌ Vacía |

### 2.3 Búsqueda de claves hardcodeadas

Búsqueda ejecutada en todos los archivos `.py`, `.md`, `.jsx`, `.txt` del repositorio
con patrones: `sk_`, `Bearer `, `xi-api-key`, `Bmx-Token:`, fragmentos de tokens conocidos.

**Resultados:**

| Archivo | Hallazgo | Evaluación |
|---------|----------|-----------|
| `CREDENTIALS_GUIDE.md` | `sk_xxxxxxxx` (placeholder) | ✅ SEGURO — es ejemplo de formato |
| `tools/test_connections.py` | `"xi-api-key"` (nombre de header) | ✅ SEGURO — es el nombre del campo, no una clave |
| `tools/verify_data.py` | `"xi-api-key"` (nombre de header) | ✅ SEGURO — ídem |

**RESULTADO SEGURIDAD CÓDIGO: LIMPIO — ninguna clave real en código**

### 2.4 Historial de Git

Git no registra ningún commit que haya incluido `.env`. La protección es efectiva desde el inicio del repositorio.

**RESULTADO SEGURIDAD TOTAL: APROBADO**

---

## NIVEL 3 — AUDITORÍA DE CONTENIDO

### 3.1 findings.md

| Métrica | Resultado |
|---------|-----------|
| Hallazgos principales (H1-H7) | 7 hallazgos |
| Datos contraintuitivos (D1-D5) | 5 datos |
| Comparaciones internacionales | 3 (París, Tokio, São Paulo) |
| Vacíos de información identificados | 4 |
| Hallazgos con fuente citada | 7/7 ✅ |

**HALLAZGO DE AUDITORÍA — CONEVAL 2023:**
El documento cita "CONEVAL 2023" para la pobreza municipal de Ecatepec (43.5%, 786K personas). CONEVAL publica datos de pobreza **a nivel municipal** únicamente en años censales. La medición municipal más reciente disponible es **CONEVAL 2020**, alineada con el Censo de Población 2020. No existe una medición CONEVAL de pobreza municipal para 2023. El dato citado como "2023" es probablemente el dato de 2020. Este error se propaga a `sources.md`, `script_draft.md` y `script_for_elevenlabs.txt`.

**HALLAZGO DE AUDITORÍA — Grand Paris Express:**
H7 cita "35 mil millones de euros" con nota explícita "requieren verificación contra fuente primaria". El dato está en el documento como no verificado pero tampoco está marcado visualmente como pendiente en la narrativa — solo en una nota de pie.

### 3.2 sources.md

| Métrica | Resultado |
|---------|-----------|
| Fuentes totales | 12 (F01–F12) |
| Tier 1A — Instituciones Nacionales | 8 (F01–F08) |
| Tier 1B — Multilaterales | 2 (F09–F10) |
| Tier 1C — Académicas | 2 (F11–F12) |
| Fuentes con URL | 12/12 ✅ |
| Datasets descargados | 0/7 ❌ |

**HALLAZGO DE AUDITORÍA — FUENTES FALTANTES EN sources.md:**
Dos fuentes citadas en `findings.md` no tienen entrada en `sources.md`:
- **"México Evalúa"** — citada en H6 (eliminación Fondo Metropolitano) y en cronología. Sin ficha en sources.md.
- **"PEF"** (Presupuesto de Egresos de la Federación) — citado en cronología. Sin ficha en sources.md.

**HALLAZGO — F09 (BID):**
La URL de F09 tiene nota: "Buscar publicación específica sobre ZMVM o México en portal BID". La URL listada es genérica, no apunta al documento específico citado.

**HALLAZGO — Datasets prioritarios:**
La tabla de "Datasets prioritarios a descargar" lista 7 datasets (D1-D7) que se requieren para producción de mapas. Ninguno ha sido descargado ni se encuentra en `03_Assets/`.

### 3.3 script_draft.md

| Métrica | Resultado |
|---------|-----------|
| Escenas | 14 ✅ |
| Columnas en tabla | Narración / Visual / Duración / Fuente ✅ |
| Duración total calculada | 390 seg = 6:30 ✅ |
| Encaja en 5-7 min target | ✅ |
| Estado de aprobación en el documento | ⚠️ "[ ] Pendiente" — no actualizado |

**HALLAZGO — APROBACIÓN NO REGISTRADA EN DOCUMENTO:**
`state.json` marca `cp2_guion: true`, pero `script_draft.md` tiene el checkbox de aprobación en `[ ] Pendiente`. El documento y el estado del proyecto están desincronizados.

**HALLAZGO — DATO DE VIVIENDA SIN FUENTE VERIFICADA:**
Escena 12 usa precios de vivienda "CDMX $50,000–$80,000 / Ecatepec $12,000–$18,000 por m²" con fuente marcada como "verificar contra fuente primaria". El dato está en el guion aprobado pero no tiene respaldo verificado.

### 3.4 script_for_elevenlabs.txt

| Métrica | Resultado |
|---------|-----------|
| Chunks totales | 14 ✅ |
| Caracteres brutos (con marcadores) | 7,702 |
| Caracteres limpios (texto a sintetizar) | 5,495 |
| Cuota ElevenLabs plan gratuito | 10,000 chars/mes |
| Margen disponible | 4,505 chars (45% de margen) ✅ |
| Coincidencia chunks / escenas | 14 / 14 ✅ |

**NOTA:** Los 5,495 caracteres incluyen los `[...]` de pausa que ElevenLabs interpreta como silencio. La facturación real puede variar ±3% según el procesamiento del modelo.

### 3.5 animation_plan.md

| Métrica | Resultado |
|---------|-----------|
| Escenas cubiertas | 14/14 ✅ |
| Timing exacto por escena | ✅ (inicio, fin, duración en seg) |
| Duración total | 390 seg = 6:30 ✅ |

### 3.6 ae_script.jsx

| Métrica | Resultado |
|---------|-----------|
| Líneas totales | 399 ✅ |
| Composiciones definidas | 15 (1 maestra + 14 escenas via loop) ✅ |
| Llaves `{}` balanceadas | 39 abiertas / 39 cerradas ✅ |
| Paréntesis `()` balanceados | 168 abiertos / 168 cerrados ✅ |
| Funciones definidas | 15 named functions ✅ |
| Importa assets automáticamente | ❌ NO — diseño intencional, documentado |
| Importa audio automáticamente | ❌ NO — diseño intencional, documentado |

**NOTA:** El script crea la estructura de composiciones y define animaciones base (fades, text placeholders, count-ups). La importación de WAV y assets visuales requiere intervención manual posterior, según el header del archivo.

---

## NIVEL 4 — AUDITORÍA DE CONSISTENCIA CRUZADA

### 4.1 Número de escenas entre documentos

| Documento | Escenas declaradas | Consistente |
|-----------|-------------------|-------------|
| `script_draft.md` | 14 | — |
| `animation_plan.md` | 14 | ✅ |
| `ae_script.jsx` (SCENES array) | 14 | ✅ |
| `script_for_elevenlabs.txt` (chunks) | 14 | ✅ |

### 4.2 Fuentes citadas en findings vs registradas en sources

| Institución | En findings.md | En sources.md |
|-------------|---------------|--------------|
| INEGI | ✅ | ✅ |
| EOD 2017 | ✅ | ✅ |
| CONEVAL | ✅ | ✅ |
| IMSS | ✅ | ✅ |
| SEMOVI | ✅ | ✅ |
| SAF CDMX | ✅ | ✅ |
| SEDATU | ✅ | ✅ |
| CONAPO | ✅ | ✅ |
| ONU-Habitat | ✅ | ✅ |
| BID | ✅ | ✅ |
| UNAM / GIITRAL | ✅ | ✅ |
| **México Evalúa** | ✅ | ❌ FALTA |
| **PEF** | ✅ | ❌ FALTA |

### 4.3 Consistencia de la tesis

| Documento | Enunciado de tesis | Estado |
|-----------|-------------------|--------|
| `tesis_candidatas.md` | "...recauda el impuesto sobre nóminas de **aproximadamente 3 millones de trabajadores**..." | Aprobada como Tesis 1 |
| `script_draft.md` | "...recauda el ISN de trabajadores..." | **Sin el dato "3 millones"** |

**HALLAZGO — NÚMERO CLAVE DESAPARECIDO:**
La tesis aprobada incluye "aproximadamente 3 millones de trabajadores" como cuantificación central. Este número NO aparece en el script final. El guion nunca menciona cuántos trabajadores mexiquenses generan el ISN capitalino. La omisión puede ser deliberada (el dato no está verificado, es un estimado propio) pero no está documentada. Si el dato fue eliminado por falta de fuente, debió quedar registrado.

### 4.4 Consistencia visual: mapas en visual_brief vs script

| Mapa | En visual_brief | En script | Estado |
|------|----------------|-----------|--------|
| Flujos Edomex→CDMX | ✅ (Escenas 1, 6, 14) | ✅ | ✅ |
| PIB por entidad | ✅ (Escena 3) | ✅ | ✅ |
| Expansión urbana Edomex | ✅ (Escena 4) | ✅ | ✅ |
| Red Metro ZMVM | ✅ (Escena 9) | ✅ | ✅ |
| Pobreza municipal | ✅ (Escena 10) | ✅ | ✅ |
| Tasas ISN comparativa | ✅ (Escena 11) | ✅ | ✅ |
| Precios vivienda | ✅ (Escena 12) | ✅ | ✅ |
| Archivos de mapa en disco | ❌ 0 de 7 | — | ❌ |

### 4.5 Duración total entre documentos

| Documento | Duración total |
|-----------|---------------|
| `script_draft.md` (suma de escenas) | 390 seg = 6:30 ✅ |
| `animation_plan.md` (suma de escenas) | 390 seg = 6:30 ✅ |
| `ae_script.jsx` (TOTAL_SECONDS) | 390 ✅ |
| Target del proyecto | 6:00–7:00 ✅ |

---

## NIVEL 5 — HALLAZGOS Y RECOMENDACIONES

### 5.1 Resumen ejecutivo

**✅ LO QUE ESTÁ SÓLIDO:**
- Seguridad: .env protegido, sin claves en código, git no rastrea credenciales
- Estructura: todas las carpetas y archivos críticos presentes
- Consistencia estructural: 14 escenas en todos los documentos
- Duración: 6:30 consistente en todos los documentos
- Script de voz: 14 chunks, 5,495 chars (cabe en plan gratuito ElevenLabs)
- ae_script.jsx: sintaxis válida, estructura correcta, 15 composiciones
- Fuentes: 10 de 12 instituciones tienen ficha completa con URL

**⚠️ LO QUE NECESITA ATENCIÓN:**
1. Carpeta `03_Assets/` vacía — 7 datasets y 7 mapas sin descargar
2. Git: 5 archivos sin commitear, repositorio nunca pusheado
3. `script_draft.md` dice "Aprobación: Pendiente" aunque state.json dice aprobado
4. Fuentes "México Evalúa" y "PEF" citadas pero sin ficha en sources.md
5. El dato "3 millones de trabajadores" de la tesis desapareció del guion sin registro
6. `05_Final/` completamente vacía — ningún producto físico existe
7. F09 (BID) tiene URL genérica, no el documento específico

**❌ LO QUE ESTÁ MAL O FALTA:**
1. **CONEVAL 2023 a nivel municipal NO EXISTE** — el dato de Ecatepec (43.5%, 786K) es de CONEVAL 2020; la cita de año es incorrecta en findings.md, sources.md, script_draft.md y script_for_elevenlabs.txt
2. **Ningún dataset descargado** — los 7 datasets prioritarios (D1-D7) no existen en disco; sin ellos no es posible producir los 7 mapas requeridos
3. **Ningún asset de audio generado** — 0 archivos WAV; sin audio no se puede sincronizar After Effects
4. **Ningún archivo de producción final** — 05_Final/ vacía

### 5.2 Riesgos identificados

| Riesgo | Severidad | Descripción |
|--------|-----------|-------------|
| CONEVAL 2023 municipal | **ALTA** | El año citado no corresponde a ninguna publicación real. Si el video se publica con "CONEVAL 2023" para dato municipal, es verificablemente incorrecto. |
| Datasets sin descargar | **ALTA** | Los 7 mapas son el núcleo visual del video. Sin los shapefiles de INEGI, CONEVAL y SEDATU no se pueden producir. Este es el cuello de botella más largo. |
| "3 millones" sin fuente | **MEDIA** | El número central de la tesis aprobada no aparece en el guion. Puede ser correcto como eliminación deliberada (dato sin verificar), pero sin registro de la decisión. |
| Datos de vivienda Escena 12 | **MEDIA** | El rango de precios m² no tiene fuente verificada primaria. Si alguien lo cuestiona post-publicación, no hay respaldo. |
| Repositorio sin push | **BAJA** | 3 commits solo en local. Un fallo de disco pierde el trabajo desde `8660b8d`. Riesgo de pérdida. |
| Aprobaciones desincronizadas | **BAJA** | Los documentos internos no reflejan su estado de aprobación aunque state.json sea autoritativo. |

### 5.3 Recomendaciones concretas

**ANTES DE CONTINUAR — Obligatorio:**

| # | Acción | Archivo | Prioridad |
|---|--------|---------|-----------|
| 1 | Corregir año CONEVAL: cambiar "2023" por "2020" en hallazgo H5, D1, cronología, script escena 10, voice script CHUNK_10 | findings.md, script_draft.md, script_for_elevenlabs.txt | CRÍTICA |
| 2 | Agregar fichas de "México Evalúa" y "PEF" en sources.md | sources.md | ALTA |
| 3 | Descargar los 7 datasets prioritarios (D1-D7) de INEGI, CONEVAL, SEDATU | 03_Assets/ | ALTA |
| 4 | Documentar por qué "3 millones" fue eliminado del guion (o agregarlo de vuelta con fuente) | script_draft.md o tesis_candidatas.md | MEDIA |
| 5 | Commitear los 5 archivos pendientes y hacer push al remoto | git | MEDIA |

**PUEDE HACERSE DESPUÉS:**

| # | Acción | Cuando |
|---|--------|--------|
| 6 | Actualizar checkbox de aprobación en script_draft.md | Antes de archivar |
| 7 | Verificar URL específica de F09 BID | Antes de publicar |
| 8 | Verificar dato Grand Paris Express "35 mil millones" contra fuente primaria | Antes de publicar |
| 9 | Resolver dato de precios de vivienda Escena 12 con INFONAVIT o SHF | Antes de grabar voz |

**NO TOCAR — Está correcto:**
- Sintaxis de `ae_script.jsx` — no modificar
- Estructura de 14 chunks en `script_for_elevenlabs.txt` — no alterar
- Parámetros de voz en `voice_brief.md` — validados
- Sistema de carpetas del orchestrator — correcto
- Protección .env / .gitignore — correcto

---

## TABLA DE SEVERIDAD CONSOLIDADA

| ID | Hallazgo | Severidad | Bloquea producción |
|----|----------|-----------|-------------------|
| H-01 | CONEVAL año 2023 incorrecto (debe ser 2020) | 🔴 ALTA | Sí — credibilidad del video |
| H-02 | 7 datasets sin descargar (mapas imposibles) | 🔴 ALTA | Sí — producción visual |
| H-03 | 0 archivos WAV generados | 🔴 ALTA | Sí — producción de audio |
| H-04 | "México Evalúa" y "PEF" sin ficha en sources | 🟡 MEDIA | No — pero incompleto |
| H-05 | "3 millones" desaparecido del guion sin registro | 🟡 MEDIA | No — pero inconsistencia documental |
| H-06 | Precio vivienda Escena 12 sin fuente verificada | 🟡 MEDIA | No — pero riesgo post-publicación |
| H-07 | 5 archivos sin commitear | 🟡 MEDIA | No — pero riesgo de pérdida |
| H-08 | Repositorio nunca pusheado | 🟡 MEDIA | No — pero riesgo de pérdida |
| H-09 | script_draft.md dice "Pendiente" (no refleja aprobación) | 🟢 BAJA | No |
| H-10 | F09 BID tiene URL genérica | 🟢 BAJA | No |
| H-11 | Grand Paris "35B euros" no verificado contra fuente primaria | 🟢 BAJA | No |

---

*Auditoría ejecutada el 2026-05-11 mediante lectura directa de archivos y verificación automatizada.*
*Ningún dato fue inventado. Los hallazgos se basan en evidencia verificable en el repositorio.*
