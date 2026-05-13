# GUÍA DE INTEGRACIÓN IA — Generación Automática de Assets Visuales

**Versión:** 2.0  
**Actualizado:** 2026-05-12  
**Agentes afectados:** A3 (Director Visual), A5 (Director de Animación)

---

## Proveedor de imágenes IA

| Modelo | Uso | Calidad | Costo |
|--------|-----|---------|-------|
| **Google Imagen 3** (`imagen-3.0-generate-001`) | Primario — fondos, conceptuales, ilustraciones editoriales | Máxima | Gratis (tier) |
| **Gemini 2.0 Flash** (imagen) | Fallback automático si Imagen 3 no disponible | Alta | Gratis (tier) |
| **Runway ML Gen-3** | Transiciones animadas y fondos en movimiento | Video | $0.05–0.10/seg |

**Una sola credencial para todo:** `GOOGLE_API_KEY` desde [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)

---

## Configuración requerida

### .env

```env
# Google AI Studio — Imagen 3 + Gemini 2.0 Flash
GOOGLE_API_KEY=AIzaSy...
```

### Obtener la clave

1. Ir a https://aistudio.google.com/app/apikey
2. Iniciar sesión con cuenta Google
3. Clic en **Create API Key**
4. Copiar y pegar en `.env` como `GOOGLE_API_KEY`

Sin tarjeta de crédito requerida para el tier gratuito.

### Instalar SDK

```
pip install google-genai pillow
```

---

## Flujo de trabajo

### Rol del Agente A3

El Agente A3 (Director Visual) debe marcar en `visual_brief.md` qué escenas requieren generación IA:

```markdown
### ESCENA 1 — Mapa de flujos de remesas

**Tipo visual:** conceptual
**Descripción:** Mapa estilizado de México con flechas que salen de EEUU hacia estados
receptores de remesas. Fondo oscuro, flechas en dorado. Estilo Bloomberg Originals.
**Prompt IA:** Stylized map of Mexico showing remittance flow arrows from USA,
dark background #1a1a1a, golden arrows #FFD700, minimal editorial style,
no text, no watermark, 16:9 format
```

Tipos que activan generación IA: `conceptual`, `illustration`, `background`, `fondo`, `mapa`, `diagrama`.  
Tipos que NO usan IA: `CHART-LINE`, `CHART-BAR`, `COUNTER`, `TYPO` (se generan con Python o After Effects nativo).

### Rol del Agente A5

Antes de construir el proyecto en After Effects:

```bash
# Generar assets visuales con IA
python 00_Orchestrator/tools/ai_asset_generator.py

# Salida esperada:
#   AI Asset Generator
#   Proveedor: Google Imagen 3 / Gemini 2.0 Flash
#   14 escenas en el brief
#   4 requieren generacion IA
#   Escena 01 (conceptual)... OK -> scene_01_generated_branded.png
#   Escena 05 (mapa)...       OK -> scene_05_generated_branded.png
#   4/4 assets generados
#   Listos para importar en After Effects via ae_script.jsx
```

---

## Uso paso a paso

### Paso 1: Preparar visual_brief.md (Agente A3)

Formato requerido para que el script pueda parsear cada escena:

```markdown
### ESCENA [N] — [Nombre descriptivo]

**Tipo visual:** [tipo — ver tabla arriba]
**Descripción:** [descripción detallada de lo que debe mostrar]
**Prompt IA:** [prompt optimizado para Imagen 3, en inglés para mejor calidad]
```

Si no hay `**Prompt IA:**`, el script usa `**Descripción:**` como prompt.

### Paso 2: Ejecutar el generador

```bash
python 00_Orchestrator/tools/ai_asset_generator.py
```

El script:
1. Lee `03_Assets/visual_brief.md`
2. Filtra escenas con tipos que requieren IA
3. Genera con Google Imagen 3 (fallback: Gemini 2.0 Flash)
4. Post-procesa: contraste +15%, saturación +10%, resize a 1920x1080
5. Guarda en `03_Assets/ai_generated/scene_NN_generated_branded.png`

Si un archivo ya existe, lo omite (permite reanudar sin re-generar).

### Paso 3: Verificar assets generados

```bash
# Windows PowerShell
dir 03_Assets\ai_generated\

# Esperado (un branded.png por escena generada):
# scene_01_generated_branded.png
# scene_05_generated_branded.png
```

### Paso 4: After Effects import automático

El script JSX generado por el Agente A5 importa automáticamente los assets:

```javascript
var IA_ASSETS = {
    "scene_01": ASSETS_FOLDER + "ai_generated/scene_01_generated_branded.png",
    "scene_05": ASSETS_FOLDER + "ai_generated/scene_05_generated_branded.png",
};
var layer = importAIGeneratedAsset(IA_ASSETS["scene_01"]);
```

---

## Identidad visual en los prompts

Cada prompt se amplía automáticamente con la identidad del proyecto:

```
{prompt del visual_brief}

Style: Bloomberg Originals, The Economist Films, editorial data visualization.
Color palette: #1a1a1a, #FFD700, #E74C3C, #3498db, #FFFFFF.
Tone: data-driven, minimalist, high contrast, no text overlays.
Format: 16:9 widescreen, no watermarks, professional quality.
```

Post-procesamiento automático:
- Contraste: +15%
- Saturación: +10%
- Resize final: 1920×1080 px (LANCZOS)

---

## Troubleshooting

### Error: "GOOGLE_API_KEY vacio en .env"

```env
GOOGLE_API_KEY=AIzaSy_tu_clave_aqui
```

Verificar: `python -c "from dotenv import load_dotenv; load_dotenv('.env'); import os; print(bool(os.environ.get('GOOGLE_API_KEY','')))" `

### Error: "Imagen 3 fallo — intentando Gemini Flash"

Normal si tu región no tiene Imagen 3 disponible. El fallback a Gemini 2.0 Flash es automático.
Si Gemini Flash también falla, verifica que la API key tenga acceso a modelos de imagen en AI Studio.

### El asset se ve diferente a lo esperado

Refina el `**Prompt IA:**` en `visual_brief.md`. Inglés genera mejores resultados que español.

**Prompt débil:**
```
Mapa de México con colores
```

**Prompt sólido:**
```
Choropleth map of Mexico, states colored by remittance income intensity,
dark navy background, gold-to-white gradient scale, Bloomberg Originals editorial style,
clean minimal design, no text labels, no watermark, high contrast
```

### Asset generado pero tamaño incorrecto

El post-procesamiento redimensiona automáticamente a 1920×1080. No requiere acción manual.

---

## Qué generar con IA vs. otras herramientas

| Tipo de visual | Herramienta correcta |
|----------------|---------------------|
| Mapa coroplético con datos reales | Python + geopandas/matplotlib (datos precisos) |
| Mapa estilizado/conceptual/de fondo | **Google Imagen 3** |
| Gráfica de series de tiempo | Python + matplotlib o **Datawrapper** |
| Gráfica interactiva exportable | **Datawrapper** (export PNG/SVG) |
| Contador animado | After Effects nativo (count-up expression) |
| Ilustración editorial/conceptual | **Google Imagen 3** |
| Fondo abstracto o textura | **Google Imagen 3** |
| Texto tipográfico en pantalla | After Effects nativo |
| Fotos documentales/reportaje | Unsplash / Pexels / Pixabay (APIs configuradas) |

---

## Costo estimado

| Operación | Costo |
|-----------|-------|
| Google Imagen 3 (tier gratuito) | $0 hasta el límite del tier |
| Gemini 2.0 Flash imagen | $0 hasta el límite del tier |
| Post-procesamiento Python (local) | $0 |
| Proyecto típico (4–6 imágenes IA) | $0 en tier gratuito |

Para proyectos con muchas imágenes IA fuera del tier gratuito:
- Imagen 3: ~$0.04/imagen
- Gemini 2.0 Flash: ~$0.01/imagen

---

**Para dudas sobre motion design y timing:** consultar agente A5 (`agents/05_animation.md`)  
**Para dudas sobre el brief visual:** consultar agente A3 (`agents/03_visuals.md`)
