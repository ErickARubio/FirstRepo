"""
Auditoría de arquitectura del proyecto — verifica archivos críticos y términos prohibidos.

Uso:
    python 00_Orchestrator/tools/system_audit.py
"""

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

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
    "00_Orchestrator/tools/requirements.txt",
    ".env.example",
]

FORBIDDEN_TERMS = [
    "Banana.dev",
    "banana_api_key",
    "BANANA_API_KEY",
    "hardcoded",
]

SEP = "=" * 60


def check_files():
    print(f"\n{'ARCHIVOS CRÍTICOS':^60}")
    print(SEP)
    ok = missing = 0
    for file in CRITICAL_FILES:
        path = ROOT / file
        if path.exists():
            size_kb = path.stat().st_size / 1024
            print(f"  OK      {file:<50} ({size_kb:.1f} KB)")
            ok += 1
        else:
            print(f"  FALTA   {file}")
            missing += 1
    print(f"\n  {ok} presentes / {missing} faltantes")
    return missing == 0


def check_forbidden_terms():
    print(f"\n{'TÉRMINOS PROHIBIDOS EN .md':^60}")
    print(SEP)
    found = []
    for md_file in ROOT.rglob("*.md"):
        try:
            content = md_file.read_text(encoding="utf-8")
            for term in FORBIDDEN_TERMS:
                if term.lower() in content.lower():
                    rel = md_file.relative_to(ROOT)
                    print(f"  WARN    '{term}' en {rel}")
                    found.append((str(rel), term))
        except Exception as e:
            print(f"  ERROR   No se pudo leer {md_file}: {e}")
    if not found:
        print("  OK      Ningún término prohibido encontrado")
    return len(found) == 0


def check_output_folders():
    print(f"\n{'CARPETAS DE SALIDA':^60}")
    print(SEP)
    folders = ["01_Research", "02_Script", "03_Assets", "04_Animation", "05_Final"]
    for folder in folders:
        path = ROOT / folder
        if path.exists():
            files = [f for f in path.iterdir() if f.name != ".gitkeep"]
            print(f"  OK      {folder:<20} ({len(files)} archivos generados)")
        else:
            print(f"  FALTA   {folder}")


def check_env():
    print(f"\n{'CREDENCIALES (.env)':^60}")
    print(SEP)
    env_path = ROOT / ".env"
    if not env_path.exists():
        print("  ERROR   .env no existe — crea uno desde .env.example")
        return False
    try:
        from dotenv import load_dotenv
        load_dotenv(env_path)
    except ImportError:
        print("  WARN    python-dotenv no instalado")

    required = ["ELEVENLABS_API_KEY", "BANXICO_TOKEN", "INEGI_TOKEN", "REPLICATE_API_TOKEN"]
    optional = ["PEXELS_API_KEY", "UNSPLASH_ACCESS_KEY", "DATAWRAPPER_TOKEN", "PIXABAY_API_KEY"]
    all_ok = True
    for key in required:
        val = os.environ.get(key, "").strip()
        if val:
            print(f"  OK      {key}")
        else:
            print(f"  FALTA   {key}  [REQUERIDA]")
            all_ok = False
    for key in optional:
        val = os.environ.get(key, "").strip()
        status = "OK" if val else "vacía"
        print(f"  {status:<6}  {key}  [opcional]")
    return all_ok


def main():
    print("\n" + SEP)
    print(f"{'PROJECT ARCHITECTURE AUDIT':^60}")
    print(f"{'Root: ' + str(ROOT):^60}")
    print(SEP)

    files_ok = check_files()
    terms_ok = check_forbidden_terms()
    check_output_folders()
    env_ok = check_env()

    print(f"\n{SEP}")
    if files_ok and terms_ok and env_ok:
        print("  RESULTADO: SISTEMA LISTO PARA PRODUCCIÓN")
    else:
        print("  RESULTADO: HAY PROBLEMAS — revisa los items marcados arriba")
    print(SEP + "\n")


if __name__ == "__main__":
    main()
