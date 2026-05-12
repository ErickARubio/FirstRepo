"""
Generador de audio para ElevenLabs — Pieza 1 "El impuesto que no regresa"

Uso:
    python 00_Orchestrator/tools/voice_gen.py

Requisitos previos:
    1. ELEVENLABS_API_KEY en .env
    2. pip install -r 00_Orchestrator/tools/requirements.txt

Genera 14 archivos WAV en 03_Assets/audio/ (chunk_01.wav ... chunk_14.wav).
Si un archivo ya existe lo omite — permite reanudar si se interrumpe.
"""

import sys
import re
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "00_Orchestrator"))

try:
    import httpx
except ImportError:
    print("httpx no instalado. Ejecuta: pip install -r 00_Orchestrator/tools/requirements.txt")
    sys.exit(1)

from tools.config import get_credential  # noqa

# ─── CONFIGURACION ─────────────────────────────────────────────────────────────

SCRIPT_FILE = ROOT / "02_Script" / "script_for_elevenlabs.txt"
OUTPUT_DIR  = ROOT / "03_Assets" / "audio"
VOICE_NAME  = "Mateo"
MODEL_ID    = "eleven_multilingual_v2"

VOICE_SETTINGS = {
    "stability":        0.55,
    "similarity_boost": 0.75,
    "style":            0.30,
    "use_speaker_boost": True,
    "speed":            0.90,
}

# ─── PARSER DEL SCRIPT ─────────────────────────────────────────────────────────

def parse_chunks(script_path: Path) -> list:
    text     = script_path.read_text(encoding="utf-8")
    segments = text.split("=" * 80)
    chunks   = []

    for seg in segments:
        seg = seg.strip()
        if not seg:
            continue
        match = re.match(r"\[CHUNK_(\d+)[^\]]*\]", seg)
        if not match:
            continue

        num = int(match.group(1))

        # Eliminar encabezado del chunk
        body = re.sub(r"^\[CHUNK_[^\]]+\]\s*", "", seg).strip()
        # Reemplazar marcadores de pausa con puntos suspensivos naturales
        body = body.replace("[...]", "...")
        # Quitar línea FIN DEL SCRIPT si la hay
        body = re.sub(r"FIN DEL SCRIPT.*", "", body, flags=re.DOTALL).strip()

        if body:
            chunks.append({
                "number":   num,
                "filename": f"chunk_{num:02d}.wav",
                "text":     body,
                "chars":    len(body),
            })

    return sorted(chunks, key=lambda x: x["number"])


# ─── API ELEVENLABS ─────────────────────────────────────────────────────────────

def find_voice_id(api_key: str, voice_name: str):
    r = httpx.get(
        "https://api.elevenlabs.io/v1/voices",
        headers={"xi-api-key": api_key},
        timeout=10,
    )
    if r.status_code != 200:
        return None
    voices = r.json().get("voices", [])
    for v in voices:
        if v["name"].lower() == voice_name.lower():
            return v["voice_id"]
    for v in voices:
        if voice_name.lower() in v["name"].lower():
            return v["voice_id"]
    return None


def list_spanish_voices(api_key: str) -> list:
    r = httpx.get(
        "https://api.elevenlabs.io/v1/voices",
        headers={"xi-api-key": api_key},
        timeout=10,
    )
    if r.status_code != 200:
        return []
    out = []
    for v in r.json().get("voices", []):
        labels = v.get("labels", {})
        lang   = (labels.get("language", "") + labels.get("accent", "")).lower()
        if any(k in lang for k in ("spanish", "espanol", "mexico", "mexican", "es-")):
            out.append({"name": v["name"], "voice_id": v["voice_id"], "labels": labels})
    return out


def generate_chunk(api_key: str, voice_id: str, text: str, out_path: Path) -> dict:
    start = time.time()
    try:
        r = httpx.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
            headers={
                "xi-api-key":   api_key,
                "Content-Type": "application/json",
                "Accept":       "audio/wav",
            },
            json={
                "text":           text,
                "model_id":       MODEL_ID,
                "voice_settings": VOICE_SETTINGS,
            },
            timeout=90,
        )
    except httpx.TimeoutException:
        return {"ok": False, "error": "Timeout (90s) — reintenta este chunk"}
    except Exception as e:
        return {"ok": False, "error": str(e)}

    elapsed = time.time() - start

    if r.status_code == 200:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_bytes(r.content)
        return {"ok": True, "elapsed": elapsed, "bytes": len(r.content), "chars": len(text)}

    if r.status_code == 401:
        return {"ok": False, "error": "API key invalida (401) — verifica ELEVENLABS_API_KEY en .env"}
    if r.status_code == 422:
        detail = r.json().get("detail", "parametros invalidos")
        return {"ok": False, "error": f"Parametros invalidos (422): {detail}"}
    if r.status_code == 429:
        return {"ok": False, "error": "CUOTA AGOTADA (429) — plan gratuito: 10,000 chars/mes"}
    try:
        err = r.json()
    except Exception:
        err = r.text[:120]
    return {"ok": False, "error": f"Error HTTP {r.status_code}: {err}"}


# ─── RUNNER ────────────────────────────────────────────────────────────────────

def run():
    SEP  = "=" * 65
    SEP2 = "-" * 65
    print("\n" + SEP)
    print("  Voice Generator — El impuesto que no regresa")
    print(f"  Modelo: {MODEL_ID}  |  Voz objetivo: {VOICE_NAME}")
    print(SEP)

    api_key = get_credential("ELEVENLABS_API_KEY")

    # Verificar voz
    print(f"\n  Buscando voz '{VOICE_NAME}' en tu cuenta...", end=" ", flush=True)
    voice_id = find_voice_id(api_key, VOICE_NAME)

    if not voice_id:
        print("NO ENCONTRADA")
        print(f"\n  La voz '{VOICE_NAME}' no esta disponible en tu cuenta.")
        spanish = list_spanish_voices(api_key)
        if spanish:
            print("\n  Voces en espanol disponibles:")
            for v in spanish:
                print(f"    - {v['name']:<25} ID: {v['voice_id']}")
        print("\n  Opciones:")
        print("    1. Anade 'Mateo' desde: elevenlabs.io → Voices → Add Voice → busca Mateo")
        print("    2. Edita VOICE_NAME en este script con el nombre de una voz disponible")
        sys.exit(1)

    print(f"OK  (voice_id: {voice_id})")

    # Parsear script
    if not SCRIPT_FILE.exists():
        print(f"\n  Error: no se encontro {SCRIPT_FILE}")
        sys.exit(1)

    chunks     = parse_chunks(SCRIPT_FILE)
    total_chars = sum(c["chars"] for c in chunks)

    print(f"\n  Script cargado: {len(chunks)} chunks  |  {total_chars} chars totales")
    print(f"  Cuota plan gratuito ElevenLabs: 10,000 chars/mes")
    if total_chars > 10000:
        print(f"  ADVERTENCIA: {total_chars} chars supera el plan gratuito")
    else:
        print(f"  OK — dentro del plan gratuito ({10000 - total_chars} chars sobraran)")

    if len(chunks) != 14:
        print(f"\n  ADVERTENCIA: se esperaban 14 chunks, se encontraron {len(chunks)}")

    print(f"\n  Output: {OUTPUT_DIR.relative_to(ROOT)}\n")

    # Generar
    total_start = time.time()
    chars_used  = 0
    ok_count    = 0
    errors      = []

    for chunk in chunks:
        num      = chunk["number"]
        out_path = OUTPUT_DIR / chunk["filename"]

        if out_path.exists():
            sz = out_path.stat().st_size // 1024
            print(f"  [SKIP]  Chunk {num:02d}/14 — {chunk['filename']} ya existe ({sz} KB)")
            ok_count   += 1
            chars_used += chunk["chars"]
            continue

        print(f"  Generando chunk {num:02d}/14  ({chunk['chars']} chars)...", end=" ", flush=True)
        result = generate_chunk(api_key, voice_id, chunk["text"], out_path)

        if result["ok"]:
            kb = result["bytes"] / 1024
            print(f"OK — {result['elapsed']:.1f}s — {kb:.0f} KB")
            ok_count   += 1
            chars_used += result["chars"]
        else:
            print(f"ERROR")
            print(f"         {result['error']}")
            errors.append((num, result["error"]))
            if "CUOTA AGOTADA" in result["error"]:
                print("\n  Deteniendo para evitar cargos adicionales.")
                break

        # Pausa breve entre llamadas para no saturar la API
        time.sleep(0.5)

    elapsed_total = time.time() - total_start

    print("\n" + SEP2)
    print(f"  {ok_count}/{len(chunks)} chunks completados")
    print(f"  Caracteres consumidos en esta sesion: ~{chars_used}")
    print(f"  Tiempo total: {elapsed_total:.1f}s")
    if errors:
        print(f"\n  Errores ({len(errors)}):")
        for num, err in errors:
            print(f"    Chunk {num:02d}: {err}")
        print(f"\n  Para reintentar chunks fallidos, eliminá el archivo WAV y corre de nuevo.")
    else:
        print(f"\n  Todos los WAV en: {OUTPUT_DIR.relative_to(ROOT)}")
        print("  Siguiente paso: abrir After Effects y ejecutar ae_script.jsx")
    print(SEP + "\n")


if __name__ == "__main__":
    run()
