# API Reference — Google AI Studio (Imagen 4 + Gemini)

**Verificado:** 2026-05-12  
**Estado:** Operacional  
**Credencial:** `GOOGLE_API_KEY` en `.env` (39 chars)  
**SDK:** `google-genai` (pip install google-genai)

---

## Modelos disponibles en esta cuenta

### Imagen (generacion de imagenes — mejor calidad)
| Modelo | Uso recomendado |
|--------|----------------|
| `imagen-4.0-generate-001` | **PRIMARIO** — balance calidad/velocidad |
| `imagen-4.0-ultra-generate-001` | Calidad maxima, mas lento |
| `imagen-4.0-fast-generate-001` | Mas rapido, calidad ligeramente menor |

### Gemini con imagen (fallback)
| Modelo | Uso |
|--------|-----|
| `gemini-2.5-flash-image` | **FALLBACK** — si Imagen 4 falla |
| `gemini-3.1-flash-image-preview` | Preview — no usar en produccion |
| `gemini-3-pro-image-preview` | Preview — no usar en produccion |

---

## Generacion de imagenes con Imagen 4

```python
from google import genai
from google.genai import types as gtypes
import os
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.environ['GOOGLE_API_KEY'])

response = client.models.generate_images(
    model='imagen-4.0-generate-001',
    prompt='Your prompt here',
    config=gtypes.GenerateImagesConfig(
        number_of_images=1,
        aspect_ratio='16:9',           # Para video 1920x1080
        safety_filter_level='block_only_high',
        person_generation='dont_allow', # Para contenido editorial
    ),
)

# Acceder a los bytes de la imagen
img_bytes = response.generated_images[0].image.image_bytes
with open('output.png', 'wb') as f:
    f.write(img_bytes)
```

### Parametros de GenerateImagesConfig
| Parametro | Opciones | Recomendado para el proyecto |
|-----------|---------|------------------------------|
| `aspect_ratio` | `'1:1'`, `'16:9'`, `'9:16'`, `'4:3'`, `'3:4'` | `'16:9'` para video |
| `number_of_images` | 1-4 | `1` para ahorrar quota |
| `safety_filter_level` | `'block_low_and_above'`, `'block_medium_and_above'`, `'block_only_high'` | `'block_only_high'` |
| `person_generation` | `'dont_allow'`, `'allow_adult'`, `'allow_all'` | `'dont_allow'` para datos |

---

## Fallback con Gemini 2.5 Flash

```python
response = client.models.generate_content(
    model='gemini-2.5-flash-image',
    contents='Generate an image: ' + prompt,
    config=gtypes.GenerateContentConfig(
        response_modalities=['Text', 'Image'],
    ),
)

# Extraer imagen de la respuesta multimodal
for part in response.candidates[0].content.parts:
    if part.inline_data and part.inline_data.mime_type.startswith('image/'):
        img_bytes = part.inline_data.data
        break
```

---

## Listar modelos disponibles (para verificar)

```python
import requests, os
r = requests.get(
    'https://generativelanguage.googleapis.com/v1beta/models',
    params={'key': os.environ['GOOGLE_API_KEY']},
    timeout=15
)
models = [m['name'].split('/')[-1] for m in r.json().get('models', [])]
imagen_models = [m for m in models if 'imagen' in m.lower()]
```

---

## Estructura del prompt para el proyecto

```
{descripcion del visual}

Style: Bloomberg Originals, The Economist Films, editorial data visualization.
Color palette: #1a1a1a, #FFD700, #E74C3C, #3498db.
Tone: data-driven, minimalist, high contrast, no text overlays.
Format: 16:9 widescreen, no watermarks, professional quality.
```

**Buenas practicas de prompt:**
- Escribir en ingles (mejores resultados)
- Especificar paleta con hex codes
- Incluir "no text", "no watermark", "editorial quality"
- Para mapas: "no labels", "clean minimal design"

---

## Post-procesamiento recomendado

Imagen 4 genera en resolucion nativa del modelo. Siempre redimensionar a 1920x1080 en post-proceso:

```python
from PIL import Image, ImageEnhance

img = Image.open('output.png').convert('RGB')
img = ImageEnhance.Contrast(img).enhance(1.15)   # +15% contraste
img = ImageEnhance.Color(img).enhance(1.10)       # +10% saturacion
img = img.resize((1920, 1080), Image.LANCZOS)
img.save('output_final.png', format='PNG')
```

---

## Recursos
- Google AI Studio: https://aistudio.google.com
- SDK docs: https://googleapis.github.io/python-genai/
- Modelos disponibles: https://ai.google.dev/gemini-api/docs/models
