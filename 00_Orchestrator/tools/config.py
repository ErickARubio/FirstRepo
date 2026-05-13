"""
Gestión centralizada de credenciales para APIs externas.
Carga variables desde .env en la raíz del proyecto.

Uso rápido:
    from tools.config import get_credential, check_all_credentials
    key = get_credential("ELEVENLABS_API_KEY")
    check_all_credentials()
"""

import os
from pathlib import Path

# Buscar .env en la raíz del proyecto (dos niveles arriba de tools/)
_ROOT = Path(__file__).resolve().parent.parent.parent
_ENV_FILE = _ROOT / ".env"

# Cargar .env si existe (sin fallar si no está)
try:
    from dotenv import load_dotenv
    load_dotenv(_ENV_FILE)
    _DOTENV_AVAILABLE = True
except ImportError:
    _DOTENV_AVAILABLE = False

# Todas las credenciales del proyecto con metadata
CREDENTIAL_REGISTRY = {
    "ELEVENLABS_API_KEY": {
        "service":     "ElevenLabs",
        "use":         "Síntesis de voz IA",
        "required":    True,
        "guide_url":   "https://elevenlabs.io → Profile → API Keys",
    },
    "GOOGLE_API_KEY": {
        "service":     "Google AI Studio",
        "use":         "Generación de imágenes IA (Imagen 3 + Gemini 2.0 Flash)",
        "required":    True,
        "guide_url":   "https://aistudio.google.com/app/apikey → Create API Key",
    },
    "PEXELS_API_KEY": {
        "service":     "Pexels",
        "use":         "Banco de imágenes",
        "required":    False,
        "guide_url":   "https://www.pexels.com/api/",
    },
    "PIXABAY_API_KEY": {
        "service":     "Pixabay",
        "use":         "Banco de imágenes CC0",
        "required":    False,
        "guide_url":   "https://pixabay.com/api/docs/",
    },
    "UNSPLASH_ACCESS_KEY": {
        "service":     "Unsplash",
        "use":         "Banco de imágenes",
        "required":    False,
        "guide_url":   "https://unsplash.com/developers",
    },
    "UNSPLASH_SECRET_KEY": {
        "service":     "Unsplash (secret)",
        "use":         "Banco de imágenes (autenticación OAuth)",
        "required":    False,
        "guide_url":   "https://unsplash.com/developers",
    },
    "BANXICO_TOKEN": {
        "service":     "Banxico SIE",
        "use":         "Series económicas del Banco de México",
        "required":    True,
        "guide_url":   "https://www.banxico.org.mx/SieAPIRest/service/v1/token",
    },
    "INEGI_TOKEN": {
        "service":     "INEGI API",
        "use":         "Indicadores nacionales México",
        "required":    True,
        "guide_url":   "https://www.inegi.org.mx/servicios/api_indicadores.html",
    },
    "DATAWRAPPER_TOKEN": {
        "service":     "Datawrapper",
        "use":         "Publicación de mapas y gráficos",
        "required":    False,
        "guide_url":   "https://app.datawrapper.de/account/api-tokens",
    },
}


class MissingCredentialError(Exception):
    """Se lanza cuando falta una credencial requerida en .env"""
    pass


def get_credential(name: str) -> str:
    """
    Devuelve el valor de una credencial por nombre.
    Lanza MissingCredentialError con instrucciones claras si no existe.

    Args:
        name: Nombre de la variable de entorno (ej: "ELEVENLABS_API_KEY")

    Returns:
        El valor de la credencial como string.

    Raises:
        MissingCredentialError: Si la variable no está definida o está vacía.
    """
    if not _DOTENV_AVAILABLE:
        raise ImportError(
            "python-dotenv no está instalado.\n"
            "Ejecuta: pip install -r 00_Orchestrator/tools/requirements.txt"
        )

    value = os.environ.get(name, "").strip()

    if not value:
        meta = CREDENTIAL_REGISTRY.get(name, {})
        service = meta.get("service", name)
        guide   = meta.get("guide_url", "Ver 00_Orchestrator/CREDENTIALS_GUIDE.md")
        raise MissingCredentialError(
            f"\n"
            f"❌  Credencial faltante: {name}\n"
            f"    Servicio: {service}\n"
            f"    Cómo obtenerla: {guide}\n"
            f"    Luego agrega en .env:  {name}=tu_clave_aquí\n"
        )

    return value


def get_credential_optional(name: str) -> str | None:
    """
    Igual que get_credential pero devuelve None en lugar de lanzar error.
    Usar para credenciales opcionales (imágenes, Datawrapper, etc.)
    """
    try:
        return get_credential(name)
    except MissingCredentialError:
        return None


def check_all_credentials() -> dict:
    """
    Verifica todas las credenciales registradas e imprime un reporte.

    Returns:
        dict con keys "ok", "missing", "empty" — listas de nombres de variables.
    """
    if not _DOTENV_AVAILABLE:
        print("⚠️  python-dotenv no instalado. Ejecuta pip install python-dotenv")
        return {"ok": [], "missing": [], "empty": []}

    ok      = []
    missing = []

    print("\n" + "─" * 55)
    print(f"  Verificación de credenciales")
    print(f"  .env: {_ENV_FILE}")
    print("─" * 55)

    for name, meta in CREDENTIAL_REGISTRY.items():
        value   = os.environ.get(name, "").strip()
        service = meta["service"]
        req_tag = " [REQUERIDA]" if meta["required"] else ""

        if value:
            print(f"  ✅  {service:<22} {name}")
            ok.append(name)
        else:
            print(f"  ❌  {service:<22} {name}{req_tag}")
            missing.append(name)

    # World Bank no requiere token
    print(f"  ✅  {'World Bank':<22} (sin token — acceso libre)")

    print("─" * 55)
    total   = len(CREDENTIAL_REGISTRY) + 1  # +1 World Bank
    ok_count = len(ok) + 1
    print(f"  {ok_count} de {total} APIs configuradas correctamente.\n")

    if missing:
        required_missing = [n for n in missing if CREDENTIAL_REGISTRY[n]["required"]]
        if required_missing:
            print("  ⚠️  Credenciales requeridas faltantes:")
            for n in required_missing:
                print(f"     • {n} → {CREDENTIAL_REGISTRY[n]['guide_url']}")
        print()

    return {"ok": ok, "missing": missing}


if __name__ == "__main__":
    check_all_credentials()
