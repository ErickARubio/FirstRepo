"""
Pre-flight check para el piloto.

Uso:
    python run_pilot.py

Verifica dependencias, archivos criticos, credenciales y state.json.
Si todo pasa: imprime instrucciones de inicio.
Si hay problemas: indica exactamente que falta y como resolverlo.
"""

import sys
import os
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

SEP  = "=" * 65
SEP2 = "-" * 65

REQUIRED_DEPS = {
    "dotenv":     "python-dotenv",
    "requests":   "requests",
    "elevenlabs": "elevenlabs",
    "google.genai": "google-genai",
    "PIL":        "pillow",
}

OPTIONAL_DEPS = {
    "pandas":     "pandas",
    "numpy":      "numpy",
}

CRITICAL_FILES = [
    "00_Orchestrator/orchestrator.md",
    "00_Orchestrator/state.json",
    "00_Orchestrator/agents/01_research.md",
    "00_Orchestrator/agents/02_script.md",
    "00_Orchestrator/agents/03_visuals.md",
    "00_Orchestrator/agents/04_voice.md",
    "00_Orchestrator/agents/05_animation.md",
    "00_Orchestrator/tools/config.py",
    "00_Orchestrator/tools/voice_gen.py",
    "00_Orchestrator/tools/ai_asset_generator.py",
]

REQUIRED_CREDENTIALS = [
    ("ELEVENLABS_API_KEY",   "ElevenLabs (voz IA)",          "https://elevenlabs.io -> Profile -> API Keys"),
    ("GOOGLE_API_KEY",        "Google AI Studio (Imagen 3 + Gemini)", "https://aistudio.google.com/app/apikey"),
    ("BANXICO_TOKEN",        "Banxico SIE (datos MX)",        "https://www.banxico.org.mx/SieAPIRest/service/v1/token"),
    ("INEGI_TOKEN",          "INEGI API (indicadores MX)",    "https://www.inegi.org.mx/servicios/api_indicadores.html"),
]

OPTIONAL_CREDENTIALS = [
    ("DATAWRAPPER_TOKEN",   "Datawrapper (mapas publicables)"),
    ("PEXELS_API_KEY",      "Pexels (banco imagenes)"),
    ("UNSPLASH_ACCESS_KEY", "Unsplash (banco imagenes)"),
    ("PIXABAY_API_KEY",     "Pixabay (banco imagenes CC0)"),
]

OUTPUT_FOLDERS = ["01_Research", "02_Script", "03_Assets", "04_Animation", "05_Final"]


def section(title):
    print(f"\n  {title}")
    print(f"  {'-' * len(title)}")


def ok(msg):
    print(f"  [OK]  {msg}")


def warn(msg):
    print(f"  [??]  {msg}")


def fail(msg):
    print(f"  [!!]  {msg}")


# --- 1. DEPENDENCIAS ----------------------------------------------------------

def check_dependencies():
    section("DEPENDENCIAS PYTHON")
    missing = []
    for module, pkg in REQUIRED_DEPS.items():
        try:
            __import__(module)
            ok(pkg)
        except (ImportError, Exception):
            fail(f"{pkg}  <- falta o incompatible")
            missing.append(pkg)

    for module, pkg in OPTIONAL_DEPS.items():
        try:
            __import__(module)
            ok(f"{pkg}  [opcional]")
        except (ImportError, Exception):
            warn(f"{pkg}  [opcional - no disponible]")

    if missing:
        print(f"\n     Instalar requeridas con:")
        print(f"     pip install -r 00_Orchestrator/tools/requirements.txt")
        return False
    return True


# --- 2. ARCHIVOS CRITICOS -----------------------------------------------------

def check_files():
    section("ARCHIVOS CRITICOS DEL SISTEMA")
    missing = []
    for rel in CRITICAL_FILES:
        path = ROOT / rel
        if path.exists():
            ok(rel)
        else:
            fail(f"{rel}  <- FALTA")
            missing.append(rel)

    if missing:
        print(f"\n     {len(missing)} archivo(s) faltante(s). El repositorio puede estar incompleto.")
        return False
    return True


# --- 3. CREDENCIALES ----------------------------------------------------------

def load_env():
    env_path = ROOT / ".env"
    if not env_path.exists():
        return False
    try:
        from dotenv import load_dotenv
        load_dotenv(env_path)
        return True
    except ImportError:
        return False


def check_credentials():
    section("CREDENCIALES (.env)")

    env_path = ROOT / ".env"
    if not env_path.exists():
        fail(".env no encontrado")
        print(f"\n     Crea el archivo copiando la plantilla:")
        print(f"     copy .env.example .env")
        print(f"     Luego llena las claves requeridas.")
        return False

    load_env()

    all_ok = True
    for key, service, guide in REQUIRED_CREDENTIALS:
        val = os.environ.get(key, "").strip()
        if val:
            ok(service)
        else:
            fail(f"{service}  <- {key} vacia")
            print(f"       Obtener en: {guide}")
            all_ok = False

    for key, service in OPTIONAL_CREDENTIALS:
        val = os.environ.get(key, "").strip()
        if val:
            ok(f"{service}  [opcional]")
        else:
            warn(f"{service}  [opcional - no configurada]")

    return all_ok


# --- 4. CARPETAS DE SALIDA ----------------------------------------------------

def check_output_folders():
    section("CARPETAS DE SALIDA")
    for folder in OUTPUT_FOLDERS:
        path = ROOT / folder
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            ok(f"{folder}/  (creada)")
        else:
            files = [f for f in path.iterdir() if f.name != ".gitkeep"]
            ok(f"{folder}/  ({len(files)} archivos generados)")


# --- 5. STATE.JSON ------------------------------------------------------------

def check_state():
    section("ESTADO DEL PROYECTO (state.json)")
    state_path = ROOT / "00_Orchestrator" / "state.json"
    if not state_path.exists():
        fail("state.json no encontrado")
        return False
    try:
        state = json.loads(state_path.read_text(encoding="utf-8"))
        project = state.get("current_project")
        if project is None:
            ok("state.json valido - sin proyecto activo (listo para nuevo piloto)")
        else:
            fase = project.get("fase_actual", "?")
            tema = project.get("tema", "?")
            ok(f"Proyecto activo: '{tema}' - Fase {fase}")
        return True
    except json.JSONDecodeError as e:
        fail(f"state.json corrupto: {e}")
        return False


# --- MAIN ---------------------------------------------------------------------

def main():
    print("\n" + SEP)
    print("  PRE-FLIGHT CHECK -- Video-Ensayos Cartograficos")
    print(f"  Proyecto: {ROOT.name}")
    print(SEP)

    results = {
        "deps":        check_dependencies(),
        "files":       check_files(),
        "credentials": check_credentials(),
        "state":       check_state(),
    }
    check_output_folders()

    all_ok = all(results.values())

    print(f"\n{SEP}")
    if all_ok:
        print("  [OK] SISTEMA LISTO PARA PRODUCCION")
        print(SEP)
        print("""
  COMO INICIAR EL PILOTO:

  1. Abre Claude Code (nueva sesion)
  2. Escribe:
       /read 00_Orchestrator/orchestrator.md
  3. Claude confirmara que cargo el rol de Orquestador.
  4. Luego escribe tu tema:
       Nuevo proyecto: las remesas en Mexico

  El Orquestador toma el control. Cada fase termina con un
  checkpoint -- tu apruebas antes de avanzar a la siguiente.
""")
    else:
        failed = [k for k, v in results.items() if not v]
        print(f"  [!!] NO LISTO -- {len(failed)} seccion(es) con problemas: {', '.join(failed)}")
        print("     Resuelve los items con [!!] arriba y vuelve a correr:")
        print("     python run_pilot.py")
    print(SEP + "\n")


if __name__ == "__main__":
    main()
