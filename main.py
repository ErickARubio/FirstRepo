"""
main.py — Pre-flight check y entry point del pipeline.

Uso:
    python main.py           # verifica sistema
    python main.py --run     # ejecuta pipeline completo
    python main.py --status  # muestra checkpoints
"""

import sys
import os
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv
load_dotenv(ROOT / ".env")

SEP = "=" * 65

REQUIRED_DEPS = {
    "dotenv":       "python-dotenv",
    "requests":     "requests",
    "elevenlabs":   "elevenlabs",
    "google.genai": "google-genai",
    "PIL":          "pillow",
}

OPTIONAL_DEPS = {
    "pandas": "pandas",
    "numpy":  "numpy",
    "matplotlib": "matplotlib",
}

CRITICAL_FILES = [
    "prompts/orchestrator.md",
    "prompts/researcher.md",
    "prompts/scriptwriter.md",
    "prompts/visual_director.md",
    "prompts/voice_director.md",
    "prompts/animation_director.md",
    "core/base_agent.py",
    "core/state_manager.py",
    "core/config.py",
    "tools/data_fetcher.py",
    "tools/map_generator.py",
    "tools/voice_gen.py",
    "mapping_rules.json",
]

REQUIRED_CREDS = [
    ("ELEVENLABS_API_KEY", "ElevenLabs (voz IA)"),
    ("GOOGLE_API_KEY",     "Google AI Studio (Imagen 3 + Gemini)"),
    ("BANXICO_TOKEN",      "Banxico SIE (datos MX)"),
    ("INEGI_TOKEN",        "INEGI API (indicadores MX)"),
]

OPTIONAL_CREDS = [
    ("DATAWRAPPER_TOKEN",   "Datawrapper"),
    ("PEXELS_API_KEY",      "Pexels"),
    ("UNSPLASH_ACCESS_KEY", "Unsplash"),
    ("PIXABAY_API_KEY",     "Pixabay"),
]


# ─── checks ───────────────────────────────────────────────────────────────────

def check_deps() -> bool:
    print("\n  Dependencias Python")
    print("  " + "-" * 30)
    missing = []
    for mod, pkg in REQUIRED_DEPS.items():
        try:
            __import__(mod)
            print(f"  [OK]  {pkg}")
        except ImportError:
            print(f"  [!!]  {pkg}  <- falta")
            missing.append(pkg)
    for mod, pkg in OPTIONAL_DEPS.items():
        try:
            __import__(mod)
            print(f"  [OK]  {pkg}  [opcional]")
        except ImportError:
            print(f"  [??]  {pkg}  [opcional - no instalado]")
    if missing:
        print(f"\n     pip install -r requirements.txt")
    return not missing


def check_files() -> bool:
    print("\n  Archivos criticos")
    print("  " + "-" * 30)
    missing = []
    for rel in CRITICAL_FILES:
        p = ROOT / rel
        if p.exists():
            print(f"  [OK]  {rel}")
        else:
            print(f"  [!!]  {rel}  <- FALTA")
            missing.append(rel)
    return not missing


def check_creds() -> bool:
    print("\n  Credenciales (.env)")
    print("  " + "-" * 30)
    all_ok = True
    for key, service in REQUIRED_CREDS:
        val = os.environ.get(key, "").strip()
        if val:
            print(f"  [OK]  {service}")
        else:
            print(f"  [!!]  {service}  <- {key} vacia")
            all_ok = False
    for key, service in OPTIONAL_CREDS:
        val = os.environ.get(key, "").strip()
        mark = "[OK]" if val else "[??]"
        print(f"  {mark}  {service}  [opcional]")
    return all_ok


def check_state() -> bool:
    from core.state_manager import StateManager
    sm = StateManager(ROOT)
    print("\n  Checkpoints del proyecto")
    print("  " + "-" * 30)
    print(sm.summary())
    return True


def ensure_workspace() -> None:
    for folder in [
        "workspace/research", "workspace/script",
        "workspace/assets/maps", "workspace/assets/charts",
        "workspace/assets/images", "workspace/assets/audio",
        "workspace/cache",
    ]:
        (ROOT / folder).mkdir(parents=True, exist_ok=True)


# ─── pipeline ─────────────────────────────────────────────────────────────────

def run_pipeline() -> None:
    from core.state_manager import StateManager
    from agents.researcher         import Researcher
    from agents.scriptwriter       import Scriptwriter
    from agents.visual_director    import VisualDirector
    from agents.voice_director     import VoiceDirector
    from agents.animation_director import AnimationDirector

    sm = StateManager(ROOT)

    for AgentCls in [Researcher, Scriptwriter, VisualDirector, VoiceDirector, AnimationDirector]:
        agent = AgentCls(ROOT)
        cp    = agent.checkpoint_name()
        if sm.is_done(cp):
            print(f"  [SKIP] {cp} (ya aprobado)")
            continue
        print(f"\n  [RUN ] {cp}")
        agent.run()


# ─── main ─────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run",    action="store_true", help="Ejecutar pipeline")
    parser.add_argument("--status", action="store_true", help="Ver checkpoints")
    args = parser.parse_args()

    print(f"\n{SEP}")
    print(f"  Proyecto_01_Remesas — Video-Ensayos Cartograficos")
    print(SEP)

    ensure_workspace()

    if args.status:
        check_state()
        return

    results = {
        "deps":  check_deps(),
        "files": check_files(),
        "creds": check_creds(),
    }
    check_state()

    all_ok = all(results.values())
    print(f"\n{SEP}")

    if all_ok:
        print("  [OK] SISTEMA LISTO")
        if args.run:
            run_pipeline()
        else:
            print("""
  Iniciar pipeline:
    python main.py --run

  O en Claude Code:
    /read prompts/orchestrator.md
""")
    else:
        failed = [k for k, v in results.items() if not v]
        print(f"  [!!] PROBLEMAS EN: {', '.join(failed)}")
        print("       Resuelve los items [!!] y vuelve a correr: python main.py")

    print(SEP + "\n")


if __name__ == "__main__":
    main()
