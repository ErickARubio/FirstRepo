# Sistema Orquestador de Video-Ensayos Cartográficos

Sistema de agentes IA para producir video-ensayos de datos económicos de México
al estilo Vox / Bloomberg Originals / The Economist Films.

---

## Inicio rápido

### 1. Inicia un nuevo video

Abre una conversación con Claude y carga el prompt maestro de `orchestrator.md`.
Luego escribe:

```
Nuevo proyecto: [TU TEMA AQUÍ]
```

Ejemplo:
```
Nuevo proyecto: Las remesas como primer ingreso de divisas en México y su impacto regional
```

El orquestador tomará el control y ejecutará las 5 fases con tus aprobaciones en cada checkpoint.

### 2. Sigue el flujo de 5 fases

```
Tema → [CP1: Tesis] → [CP2: Guion] → [CP3: Visuals] → [CP4: Voz] → [CP5: Animación]
```

Cada `CP` es un checkpoint donde debes aprobar o solicitar cambios antes de continuar.

---

## Estructura del sistema

```
00_Orchestrator/
├── orchestrator.md          ← Prompt maestro. Cárgalo primero siempre.
├── agents/
│   ├── 01_research.md       ← Agente A1: Investigador económico
│   ├── 02_script.md         ← Agente A2: Guionista de video-ensayo
│   ├── 03_visuals.md        ← Agente A3: Director visual y de arte
│   ├── 04_voice.md          ← Agente A4: Director de voz y audio
│   └── 05_animation.md      ← Agente A5: Director técnico de animación
├── tools/
│   └── (scripts Python irán aquí: descarga de datos, generación de mapas)
├── templates/
│   ├── thesis_template.md   ← Plantilla para las 3 tesis candidatas
│   ├── script_template.md   ← Plantilla para el guion narración/visual
│   └── sources_template.md  ← Plantilla para el registro de fuentes
├── state.json               ← Estado del proyecto en curso
└── README.md                ← Este archivo
```

---

## Qué hace cada agente

### A1 — Investigador (`01_research.md`)
Genera 3 tesis candidatas debatibles y contraintuitivas, levanta 8-12 fuentes
Tier 1 (INEGI, Banxico, Banco Mundial, OCDE, etc.) y produce un documento de
hallazgos con los datos clave para el video.

**Output:** `tesis_candidatas.md`, `sources.md`, `findings.md`
**Checkpoint:** El usuario aprueba UNA tesis.

### A2 — Guionista (`02_script.md`)
Escribe el guion completo en formato tabla (narración + visual + duración + fuente)
siguiendo el framework de 5 actos: Gancho → Contexto → Anatomía → Tensión → Implicación.

**Output:** `script_draft.md`
**Checkpoint:** El usuario aprueba el guion escena por escena.

### A3 — Director Visual (`03_visuals.md`)
Define el tipo de visual por escena (mapa coroplético, gráfico, imagen documental,
tipografía), especifica paleta de colores, tipografía y genera queries para bancos
de imágenes gratuitos.

**Output:** `visual_brief.md`
**Checkpoint:** El usuario aprueba el brief visual y la paleta.

### A4 — Director de Voz (`04_voice.md`)
Prepara el guion para ElevenLabs: limpia números y abreviaturas, segmenta en chunks
por escena, define parámetros de voz y produce la tabla de timing para sincronización.

**Output:** `voice_brief.md`, `script_for_elevenlabs.txt`
**Checkpoint:** El usuario aprueba el script limpio y la voz seleccionada.

### A5 — Director de Animación (`05_animation.md`)
Genera el storyboard técnico con timing exacto, define todas las transiciones y
produce un script ExtendScript (.jsx) para automatizar la creación del proyecto
en After Effects.

**Output:** `animation_plan.md`, `ae_script.jsx`
**Checkpoint:** El usuario aprueba el plan y declara el proyecto listo para producción.

---

## Dónde están los checkpoints

| Checkpoint | Fase | Pregunta al usuario |
|-----------|------|---------------------|
| CP1 | Investigación | ¿Cuál de las 3 tesis apruebas? |
| CP2 | Guion | ¿Apruebas el guion completo? |
| CP3 | Visuals | ¿Apruebas el brief visual y la paleta? |
| CP4 | Voz | ¿Apruebas el script para ElevenLabs? |
| CP5 | Animación | ¿Apruebas el plan de animación? |

**Regla:** El sistema nunca avanza sin tu aprobación explícita. En cualquier
checkpoint puedes pedir cambios, ajustes o reiniciar esa fase.

---

## Cómo modificar el estilo de los agentes

### Cambiar el estilo narrativo (A2)
Edita `agents/02_script.md`. Busca la sección **FRAMEWORK NARRATIVO: 5 ACTOS**
y ajusta las instrucciones de cada acto. Por ejemplo, puedes cambiar la duración
del Gancho de 45 a 30 segundos, o pedir que el Acto 4 incluya una entrevista ficticia.

### Cambiar la estética visual (A3)
Edita `agents/03_visuals.md`. En la sección **FASE 2: SISTEMA DE IDENTIDAD VISUAL**
puedes agregar una Opción D con tu propia paleta, o modificar los valores hex de
las opciones existentes.

### Cambiar los parámetros de voz (A4)
Edita `agents/04_voice.md`. En la sección **FASE 1: SELECCIÓN DE VOZ** ajusta los
parámetros JSON de ElevenLabs (stability, similarity_boost, speaking_rate).

### Cambiar la duración objetivo
Edita `state.json` y modifica `target_duration_min` y `target_duration_max`.
El orquestador usará estos valores al invocar al Agente A2.

### Agregar nuevas fuentes a la lista permitida (A1)
Edita `agents/01_research.md`. En la tabla **JERARQUÍA DE FUENTES PERMITIDAS**
agrega la institución en el Tier correspondiente.

---

## Gestión del estado (`state.json`)

El archivo `state.json` registra el proyecto en curso y el historial de videos producidos.

```json
{
  "current_project": {
    "id": "2026-05-remesas",
    "tema": "Remesas en México",
    "fase_actual": 3,
    "tesis_aprobada": "Las remesas como estabilizador del consumo...",
    "checkpoints": {
      "cp1_tesis": true,
      "cp2_guion": true,
      "cp3_visual": false,
      "cp4_voz": false,
      "cp5_animacion": false
    },
    "archivos_generados": ["findings.md", "sources.md", "script_draft.md"],
    "iniciado": "2026-05-10",
    "ultima_actualizacion": "2026-05-11"
  }
}
```

El orquestador actualiza este archivo después de cada checkpoint aprobado.

---

## Carpetas de salida por fase

Los archivos generados se guardan en las carpetas temáticas del proyecto principal:

| Fase | Carpeta destino | Archivos |
|------|----------------|---------|
| 1 — Investigación | `01_Research/` | findings.md, sources.md, tesis_candidatas.md |
| 2 — Guion | `02_Script/` | script_draft.md |
| 3 — Visuals | `03_Assets/` | visual_brief.md |
| 4 — Voz | `02_Script/` | voice_brief.md, script_for_elevenlabs.txt |
| 5 — Animación | `04_Animation/` | animation_plan.md, ae_script.jsx |

---

## Requisitos técnicos

| Herramienta | Uso | Costo |
|------------|-----|-------|
| Claude (Sonnet o superior) | Orquestador + todos los agentes | API Anthropic |
| ElevenLabs | Síntesis de voz narración | Plan Creator+ |
| After Effects | Animación y motion graphics | Adobe CC |
| QGIS (opcional) | Producción de mapas complejos | Gratuito |
| Python + geopandas (opcional) | Automatización de mapas | Gratuito |
| Flourish (opcional) | Gráficos animados sin código | Gratuito/Pro |

---

## Glosario

| Término | Significado en este sistema |
|---------|---------------------------|
| Tesis | La idea central debatible del video, no el tema |
| Gancho | El dato contraintuitivo de los primeros 15 segundos |
| Chunk | Fragmento del guion de máximo 60 segundos para ElevenLabs |
| Brief visual | Documento con todas las especificaciones de arte del video |
| Tier 1 | Fuentes institucionales de máxima autoridad aceptadas |
| CP | Checkpoint: punto de aprobación humana obligatoria |

---

*Sistema diseñado para producir video-ensayos cartográficos con datos económicos de México.*
*Proyecto base: Remesas — CDMX, 2026.*
