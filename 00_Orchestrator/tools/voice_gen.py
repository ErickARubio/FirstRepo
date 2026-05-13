"""
Generador de audio con ElevenLabs TTS.

Uso:
    python 00_Orchestrator/tools/voice_gen.py [NombreDeVoz]

Requisitos previos:
    1. ELEVENLABS_API_KEY en .env
    2. pip install -r 00_Orchestrator/tools/requirements.txt

Lee 02_Script/script_for_elevenlabs.txt y genera WAVs en 03_Assets/audio/.
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
    from elevenlabs.client import ElevenLabs
    from elevenlabs.types import VoiceSettings
except ImportError:
    print("elevenlabs no instalado. Ejecuta: pip install -r 00_Orchestrator/tools/requirements.txt")
    sys.exit(1)

from tools.config import get_credential  # noqa

# ─── CONFIGURACION ─────────────────────────────────────────────────────────────

SCRIPT_FILE = ROOT / "02_Script" / "script_for_elevenlabs.txt"
OUTPUT_DIR  = ROOT / "03_Assets" / "audio"
VOICE_NAME  = sys.argv[1] if len(sys.argv) > 1 else "Rachel"
MODEL_ID    = "eleven_multilingual_v2"

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

def find_voice_id(client: ElevenLabs, voice_name: str):
    """Busca una voz por nombre. Retorna voice_id o None si no existe."""
    try:
        voices = client.voices.get_all()
        # Búsqueda exacta
        for v in voices.voices:
            if v.name.lower() == voice_name.lower():
                return v.voice_id
        # Búsqueda parcial
        for v in voices.voices:
            if voice_name.lower() in v.name.lower():
                return v.voice_id
        return None
    except Exception as e:
        print(f"Error al buscar voces: {e}")
        return None


def get_all_voices(client: ElevenLabs) -> list:
    """Retorna lista de todas las voces disponibles."""
    try:
        voices = client.voices.get_all()
        return [
            {"name": v.name, "voice_id": v.voice_id, "labels": getattr(v, 'labels', {})}
            for v in voices.voices
        ]
    except Exception as e:
        print(f"Error al obtener voces: {e}")
        return []


def generate_chunk(client: ElevenLabs, voice_id: str, text: str, out_path: Path) -> dict:
    """Genera un chunk de audio usando ElevenLabs."""
    start = time.time()
    try:
        audio_iter = client.text_to_speech.convert(
            voice_id=voice_id,
            text=text,
            model_id="eleven_multilingual_v2",
            voice_settings=VoiceSettings(
                stability=0.55,
                similarity_boost=0.75,
                style=0.30,
                use_speaker_boost=True,
                speed=0.90,
            ),
        )
        audio_bytes = b"".join(audio_iter)
    except Exception as e:
        error_str = str(e).lower()
        if "401" in error_str or "unauthorized" in error_str:
            return {"ok": False, "error": "API key invalida (401) — verifica ELEVENLABS_API_KEY en .env"}
        elif "422" in error_str:
            return {"ok": False, "error": f"Parametros invalidos (422): {e}"}
        elif "429" in error_str:
            return {"ok": False, "error": "CUOTA AGOTADA (429) — plan gratuito: 10,000 chars/mes"}
        elif "timeout" in error_str:
            return {"ok": False, "error": "Timeout — reintenta este chunk"}
        else:
            return {"ok": False, "error": str(e)}

    elapsed = time.time() - start

    try:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_bytes(audio_bytes)
        return {"ok": True, "elapsed": elapsed, "bytes": len(audio_bytes), "chars": len(text)}
    except Exception as e:
        return {"ok": False, "error": f"Error al guardar archivo: {e}"}


# ─── RUNNER ────────────────────────────────────────────────────────────────────

def run():
    SEP  = "=" * 65
    SEP2 = "-" * 65
    print("\n" + SEP)
    print("  Voice Generator — ElevenLabs TTS")
    print(f"  Modelo: {MODEL_ID}")
    print(SEP)

    api_key = get_credential("ELEVENLABS_API_KEY")
    client = ElevenLabs(api_key=api_key)

    # Verificar voz
    all_voices = get_all_voices(client)
    if not all_voices:
        print("\n  Error: no se pudieron obtener voces de la cuenta. Verifica tu API key.")
        sys.exit(1)

    print(f"\n  Buscando voz '{VOICE_NAME}'...", end=" ", flush=True)
    voice_id   = find_voice_id(client, VOICE_NAME)
    voice_used = VOICE_NAME

    if not voice_id:
        print("no encontrada — usando primera disponible")
        voice_id   = all_voices[0]["voice_id"]
        voice_used = all_voices[0]["name"]
    else:
        print("OK")

    print(f"\n  Voces en tu cuenta ({len(all_voices)}):")
    for v in all_voices:
        marker = "  >>>" if v["voice_id"] == voice_id else "     "
        print(f"  {marker} {v['name']:<28} {v['voice_id']}")
    print(f"\n  Usando: '{voice_used}'  (pasa otro nombre como argumento: voice_gen.py \"Nombre\")")

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

    if len(chunks) == 0:
        print(f"\n  ERROR: no se encontraron chunks en el script. Verifica el formato [CHUNK_XX].")
        sys.exit(1)

    print(f"\n  Output: {OUTPUT_DIR.relative_to(ROOT)}\n")

    # Generar
    total_start = time.time()
    chars_used  = 0
    ok_count    = 0
    errors      = []

    for chunk in chunks:
        num      = chunk["number"]
        out_path = OUTPUT_DIR / chunk["filename"]

        total_chunks = len(chunks)
        if out_path.exists():
            sz = out_path.stat().st_size // 1024
            print(f"  [SKIP]  Chunk {num:02d}/{total_chunks} — {chunk['filename']} ya existe ({sz} KB)")
            ok_count   += 1
            chars_used += chunk["chars"]
            continue

        print(f"  Generando chunk {num:02d}/{total_chunks}  ({chunk['chars']} chars)...", end=" ", flush=True)
        result = generate_chunk(client, voice_id, chunk["text"], out_path)

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
