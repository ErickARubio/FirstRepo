"""
Generador automatico de assets visuales con IA — Google Imagen 3 / Gemini 2.0 Flash

Uso:
    python tools/ai_asset_generator.py --visual-brief workspace/research/visual_brief.md

Requisitos previos:
    1. GOOGLE_API_KEY en .env  (https://aistudio.google.com/app/apikey)
    2. pip install -r 00_Orchestrator/tools/requirements.txt

Flujo:
    parse visual_brief.md
    -> genera con Imagen 3 (fallback: Gemini 2.0 Flash)
    -> post-procesa: contraste + saturacion + resize 1920x1080
    -> guarda en workspace/assets/images/
"""

import sys
import re
import time
import urllib.request
import urllib.parse
from pathlib import Path
from typing import Dict, Tuple, Optional

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

try:
    from google import genai
    from google.genai import types as gtypes
    from PIL import Image, ImageEnhance
    import io
except ImportError:
    print("Dependencias faltantes. Ejecuta: pip install -r 00_Orchestrator/tools/requirements.txt")
    sys.exit(1)

from core.config import get_credential

# --- CONFIGURACION -----------------------------------------------------------

VISUAL_BRIEF_FILE = ROOT / "03_Assets" / "visual_brief.md"
OUTPUT_DIR        = ROOT / "03_Assets" / "ai_generated"

# Modelos verificados en la cuenta (2026-05-12)
# Primario:  Imagen 4 — mejor calidad disponible
# Fallback:  Gemini 2.5 Flash imagen — si Imagen 4 falla
MODEL_IMAGEN  = "imagen-4.0-generate-001"
MODEL_GEMINI  = "gemini-3.1-flash-image-preview"

BRAND_IDENTITY = {
    "style":     "Bloomberg Originals, The Economist Films, editorial data visualization",
    "palette":   "#1a1a1a, #FFD700, #E74C3C, #3498db, #FFFFFF",
    "tone":      "data-driven, minimalist, high contrast, no text overlays",
    "format":    "16:9 widescreen, no watermarks, professional quality",
}

# --- PARSER DEL VISUAL BRIEF -------------------------------------------------

def parse_visual_brief(brief_path: Path) -> Dict:
    """Extrae especificaciones de escena del visual_brief.md."""
    if not brief_path.exists():
        print(f"Error: {brief_path} no existe. Ejecuta primero el Agente A3.")
        return {}

    content = brief_path.read_text(encoding="utf-8")
    visuals = {}

    # Formato real del brief: "### Escena N — Título" (minúsculas, sin ESCENA)
    pattern = r"### Escena (\d+)[^\n]*\n(.*?)(?=### Escena |\Z)"
    for match in re.finditer(pattern, content, re.DOTALL | re.IGNORECASE):
        num  = int(match.group(1))
        body = match.group(2)

        tipo_m  = re.search(r"\*\*Tipo:\*\*\s*(.*?)\n", body)
        desc_m  = re.search(r"\*\*Descripci[oó]n:\*\*\s*(.*?)\n", body)
        # El prompt está en un bloque de código después de "**Prompt para Google Imagen 4..."
        prompt_m = re.search(
            r"\*\*Prompt para Google Imagen 4[^*]*\*\*\s*\n```[^\n]*\n(.*?)\n```",
            body, re.DOTALL
        )
        # person_generation viene del campo **Parámetros:**
        person_m = re.search(r"person_generation\s*[`']?(\w+)[`']?", body)

        visuals[num] = {
            "type":              tipo_m.group(1).strip()   if tipo_m   else "conceptual",
            "description":       desc_m.group(1).strip()   if desc_m   else "",
            "prompt_ia":         prompt_m.group(1).strip() if prompt_m else "",
            "person_generation": person_m.group(1).strip() if person_m else "dont_allow",
            "raw":               body,
        }

    return visuals


# --- CONSTRUCCION DEL PROMPT -------------------------------------------------

def build_prompt(visual: Dict) -> str:
    """Construye prompt optimizado para Imagen 3 / Gemini con identidad visual."""
    base = visual.get("prompt_ia") or visual.get("description") or "data visualization"

    return (
        f"{base}. "
        f"Style: {BRAND_IDENTITY['style']}. "
        f"Color palette: {BRAND_IDENTITY['palette']}. "
        f"Tone: {BRAND_IDENTITY['tone']}. "
        f"Format: {BRAND_IDENTITY['format']}."
    )


# --- GENERACION CON GOOGLE IMAGEN 3 ------------------------------------------

def generate_with_imagen(client, prompt: str, scene_num: int, person_generation: str = "dont_allow") -> Optional[Path]:
    """Genera imagen con Imagen 4 (mejor calidad disponible, aspecto 16:9)."""
    try:
        response = client.models.generate_images(
            model=MODEL_IMAGEN,
            prompt=prompt,
            config=gtypes.GenerateImagesConfig(
                number_of_images=1,
                aspect_ratio="16:9",
                safety_filter_level="block_low_and_above",
                person_generation=person_generation,
            ),
        )
        if not response.generated_images:
            return None

        img_bytes = response.generated_images[0].image.image_bytes
        out = OUTPUT_DIR / f"scene_{scene_num:02d}_generated.png"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(img_bytes)
        return out

    except Exception as e:
        print(f"(Imagen 4 fallo: {e} — intentando Gemini Flash)")
        return None


# --- FALLBACK: GEMINI 2.0 FLASH ----------------------------------------------

def generate_with_gemini_flash(client, prompt: str, scene_num: int) -> Optional[Path]:
    """Genera imagen con Gemini 2.0 Flash (fallback si Imagen 3 no esta disponible)."""
    try:
        response = client.models.generate_content(
            model=MODEL_GEMINI,
            contents=prompt,
            config=gtypes.GenerateContentConfig(
                response_modalities=["Text", "Image"],
            ),
        )
        for part in response.candidates[0].content.parts:
            if part.inline_data and part.inline_data.mime_type.startswith("image/"):
                img_bytes = part.inline_data.data
                out = OUTPUT_DIR / f"scene_{scene_num:02d}_generated.png"
                out.parent.mkdir(parents=True, exist_ok=True)
                out.write_bytes(img_bytes)
                return out
        return None

    except Exception as e:
        print(f"(Gemini Flash tambien fallo: {e})")
        return None


def generate_with_pollinations(prompt: str, scene_num: int) -> Optional[Path]:
    """Fallback gratuito: Pollinations.ai con modelo Flux. Sin API key."""
    try:
        encoded = urllib.parse.quote(prompt)
        url = (
            f"https://image.pollinations.ai/prompt/{encoded}"
            f"?width=1920&height=1080&model=flux&nologo=true&enhance=true"
        )
        out = OUTPUT_DIR / f"scene_{scene_num:02d}_generated.png"
        out.parent.mkdir(parents=True, exist_ok=True)
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=90) as resp:
            out.write_bytes(resp.read())
        return out
    except Exception as e:
        print(f"(Pollinations.ai fallo: {e})")
        return None


def generate_image(client, prompt: str, scene_num: int, person_generation: str = "dont_allow") -> Optional[Path]:
    """Cadena de fallbacks: Imagen 4 -> Gemini Flash -> Pollinations.ai (gratis)."""
    path = generate_with_imagen(client, prompt, scene_num, person_generation)
    if path:
        return path
    path = generate_with_gemini_flash(client, prompt, scene_num)
    if path:
        return path
    print("(intentando Pollinations.ai — gratis, sin API key)")
    return generate_with_pollinations(prompt, scene_num)


# --- POST-PROCESADO ----------------------------------------------------------

def post_process(img_path: Path) -> Path:
    """Ajusta contraste/saturacion y redimensiona a 1920x1080."""
    try:
        img = Image.open(img_path).convert("RGB")
        img = ImageEnhance.Contrast(img).enhance(1.15)
        img = ImageEnhance.Color(img).enhance(1.10)
        img = img.resize((1920, 1080), Image.LANCZOS)

        out = img_path.parent / f"{img_path.stem}_branded.png"
        img.save(out, format="PNG")
        return out
    except Exception as e:
        print(f"    Warn post-proceso: {e}")
        return img_path


# --- VALIDACION --------------------------------------------------------------

def validate(img_path: Path) -> Tuple[bool, str]:
    """Verifica que el archivo es una imagen valida y tiene resolucion minima."""
    try:
        if img_path.suffix.lower() not in (".png", ".jpg", ".jpeg"):
            return False, f"Formato no soportado: {img_path.suffix}"
        img = Image.open(img_path)
        img.load()
        w, h = img.size
        if w < 512 or h < 288:
            return False, f"Resolucion insuficiente: {w}x{h}"
        return True, f"OK {w}x{h}"
    except Exception as e:
        return False, f"Error: {e}"


# --- TIPOS QUE REQUIEREN IA --------------------------------------------------

def requiere_ia(visual: Dict) -> bool:
    """Solo escenas IMG-DOC con prompt para Google Imagen 4 requieren generación IA."""
    tipo = visual.get("type", "").lower()
    raw  = visual.get("raw", "").lower()
    return "img-doc" in tipo and "google imagen" in raw and bool(visual.get("prompt_ia"))


# --- RUNNER ------------------------------------------------------------------

def run():
    SEP  = "=" * 65
    SEP2 = "-" * 65

    print("\n" + SEP)
    print("  AI Asset Generator")
    print("  Proveedor: Google Imagen 4 / Gemini 2.5 Flash")
    print(SEP)

    api_key = get_credential("GOOGLE_API_KEY")
    client  = genai.Client(api_key=api_key)

    print(f"\n  Leyendo: {VISUAL_BRIEF_FILE.relative_to(ROOT)}")
    visuals = parse_visual_brief(VISUAL_BRIEF_FILE)

    if not visuals:
        print("  Sin escenas encontradas. Verifica el formato del visual_brief.md.")
        sys.exit(1)

    print(f"  {len(visuals)} escenas en el brief")

    ia_scenes = {k: v for k, v in visuals.items() if requiere_ia(v)}
    print(f"  {len(ia_scenes)} requieren generacion IA\n")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    ok_count = 0
    errors   = []

    for num, visual in ia_scenes.items():
        existing = OUTPUT_DIR / f"scene_{num:02d}_generated_branded.png"
        if existing.exists():
            sz = existing.stat().st_size // 1024
            print(f"  [SKIP] Escena {num:02d} — ya existe ({sz} KB)")
            ok_count += 1
            continue

        prompt = build_prompt(visual)
        print(f"  Escena {num:02d} ({visual['type']})...", end=" ", flush=True)

        person_gen = visual.get("person_generation", "dont_allow")
        img_path = generate_image(client, prompt, num, person_gen)

        if img_path:
            is_ok, msg = validate(img_path)
            if is_ok:
                final = post_process(img_path)
                print(f"OK -> {final.name}")
                ok_count += 1
            else:
                print(f"Fallo validacion: {msg}")
                errors.append((num, msg))
        else:
            print("Generacion fallida")
            errors.append((num, "Sin output de la API"))

        time.sleep(1)

    print("\n" + SEP2)
    print(f"  {ok_count}/{len(ia_scenes)} assets generados")
    print(f"  Ubicacion: {OUTPUT_DIR.relative_to(ROOT)}")
    if errors:
        print(f"\n  Errores:")
        for num, err in errors:
            print(f"    Escena {num:02d}: {err}")
    else:
        print("  Listos para importar en After Effects via ae_script.jsx")
    print(SEP + "\n")


if __name__ == "__main__":
    run()
