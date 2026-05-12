"""
Verificador de conexiones a APIs externas.

Uso:
    python 00_Orchestrator/tools/test_connections.py

Requisitos previos:
    1. .env con las claves configuradas
    2. pip install -r 00_Orchestrator/tools/requirements.txt
"""

import sys
import os
from pathlib import Path

# Asegurar que el directorio raíz esté en el path
ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

try:
    import httpx
except ImportError:
    print("❌ httpx no instalado. Ejecuta: pip install -r 00_Orchestrator/tools/requirements.txt")
    sys.exit(1)

sys.path.insert(0, str(ROOT / "00_Orchestrator"))
from tools.config import get_credential_optional, CREDENTIAL_REGISTRY  # noqa

# ─── TESTERS POR API ──────────────────────────────────────────────────────────

def test_elevenlabs() -> tuple[bool, str]:
    key = get_credential_optional("ELEVENLABS_API_KEY")
    if not key:
        return False, "FALTA ELEVENLABS_API_KEY en .env"
    try:
        # /v1/voices no requiere permiso user_read — funciona con cualquier key valida
        r = httpx.get(
            "https://api.elevenlabs.io/v1/voices",
            headers={"xi-api-key": key},
            timeout=8,
        )
        if r.status_code == 200:
            voices = r.json().get("voices", [])
            return True, f"Conectado — {len(voices)} voces disponibles"
        elif r.status_code == 401:
            detail = r.json().get("detail", {})
            if isinstance(detail, dict) and detail.get("status") == "missing_permissions":
                return True, "Conectado (key valida, scope limitado)"
            return False, "API key invalida (401)"
        else:
            return False, f"Error {r.status_code}"
    except httpx.TimeoutException:
        return False, "Timeout"
    except Exception as e:
        return False, str(e)


def test_pexels() -> tuple[bool, str]:
    key = get_credential_optional("PEXELS_API_KEY")
    if not key:
        return False, "FALTA PEXELS_API_KEY en .env"
    try:
        r = httpx.get(
            "https://api.pexels.com/v1/search?query=city&per_page=1",
            headers={"Authorization": key},
            timeout=8,
        )
        if r.status_code == 200:
            remaining = r.headers.get("X-Ratelimit-Remaining", "?")
            return True, f"Requests restantes este mes: {remaining}"
        elif r.status_code == 401:
            return False, "API key inválida (401)"
        else:
            return False, f"Error {r.status_code}"
    except httpx.TimeoutException:
        return False, "Timeout"
    except Exception as e:
        return False, str(e)


def test_unsplash() -> tuple[bool, str]:
    key = get_credential_optional("UNSPLASH_ACCESS_KEY")
    if not key:
        return False, "FALTA UNSPLASH_ACCESS_KEY en .env"
    try:
        r = httpx.get(
            "https://api.unsplash.com/me",
            headers={"Authorization": f"Client-ID {key}"},
            timeout=8,
        )
        if r.status_code == 200:
            return True, "Conectado"
        elif r.status_code == 401:
            return False, "Access key inválida (401)"
        else:
            return False, f"Error {r.status_code}"
    except httpx.TimeoutException:
        return False, "Timeout"
    except Exception as e:
        return False, str(e)


def test_banxico() -> tuple[bool, str]:
    token = get_credential_optional("BANXICO_TOKEN")
    if not token:
        return False, "FALTA BANXICO_TOKEN en .env"
    try:
        # Serie SF43718 = tipo de cambio USD/MXN — serie pública de prueba
        url = f"https://www.banxico.org.mx/SieAPIRest/service/v1/series/SF43718/datos/oportuno"
        r = httpx.get(
            url,
            headers={"Bmx-Token": token},
            timeout=10,
        )
        if r.status_code == 200:
            return True, "Conectado (serie SF43718 tipo de cambio OK)"
        elif r.status_code == 400:
            return False, "Token inválido (400)"
        elif r.status_code == 401:
            return False, "Token inválido (401 Unauthorized)"
        else:
            return False, f"Error {r.status_code}"
    except httpx.TimeoutException:
        return False, "Timeout — Banxico puede ser lento"
    except Exception as e:
        return False, str(e)


def test_inegi() -> tuple[bool, str]:
    token = get_credential_optional("INEGI_TOKEN")
    if not token:
        return False, "FALTA INEGI_TOKEN en .env"
    try:
        # Indicador 1002000001 = Poblacion total — banco BISE, area 00 (nacional)
        url = (
            f"https://www.inegi.org.mx/app/api/indicadores/desarrolladores/"
            f"jsonxml/INDICATOR/1002000001/es/00/false/BISE/2.0/{token}?type=json"
        )
        r = httpx.get(url, timeout=10)
        if r.status_code == 200:
            return True, "Conectado (indicador poblacion OK)"
        elif r.status_code == 400:
            return False, f"Error de consulta: {r.text[:80]}"
        elif r.status_code == 401:
            return False, "Token invalido (401)"
        else:
            return False, f"Error {r.status_code}"
    except httpx.TimeoutException:
        return False, "Timeout"
    except Exception as e:
        return False, str(e)


def test_datawrapper() -> tuple[bool, str]:
    token = get_credential_optional("DATAWRAPPER_TOKEN")
    if not token:
        return False, "FALTA DATAWRAPPER_TOKEN en .env"
    try:
        r = httpx.get(
            "https://api.datawrapper.de/v3/me",
            headers={"Authorization": f"Bearer {token}"},
            timeout=8,
        )
        if r.status_code == 200:
            data = r.json()
            name = data.get("data", {}).get("name", "usuario")
            return True, f"Conectado como: {name}"
        elif r.status_code == 401:
            return False, "Token inválido (401)"
        else:
            return False, f"Error {r.status_code}"
    except httpx.TimeoutException:
        return False, "Timeout"
    except Exception as e:
        return False, str(e)


def test_worldbank() -> tuple[bool, str]:
    try:
        r = httpx.get(
            "https://api.worldbank.org/v2/country/MX/indicator/NY.GDP.MKTP.CD"
            "?format=json&per_page=1&mrv=1",
            timeout=8,
        )
        if r.status_code == 200:
            return True, "Sin token requerido — acceso libre OK"
        else:
            return False, f"Error {r.status_code}"
    except httpx.TimeoutException:
        return False, "Timeout"
    except Exception as e:
        return False, str(e)


# ─── RUNNER PRINCIPAL ─────────────────────────────────────────────────────────

TESTS = [
    ("ElevenLabs",  "ELEVENLABS_API_KEY",   test_elevenlabs,  True),
    ("Pexels",      "PEXELS_API_KEY",        test_pexels,      False),
    ("Unsplash",    "UNSPLASH_ACCESS_KEY",   test_unsplash,    False),
    ("Banxico",     "BANXICO_TOKEN",         test_banxico,     True),
    ("INEGI",       "INEGI_TOKEN",           test_inegi,       True),
    ("Datawrapper", "DATAWRAPPER_TOKEN",     test_datawrapper, False),
    ("World Bank",  "(sin token)",           test_worldbank,   False),
]


def run_all_tests():
    SEP  = "=" * 60
    SEP2 = "-" * 60
    print("\n" + SEP)
    print("  Test de conexiones - Video-Ensayos Cartograficos")
    print(SEP)

    results = []
    for name, var, tester, required in TESTS:
        print(f"\n  Probando {name}...", end=" ", flush=True)
        ok, detail = tester()
        req_tag = " [REQUERIDA]" if required and not ok else ""
        icon = "[OK]" if ok else "[--]"
        print(f"\r  {icon}  {name:<15} {detail}{req_tag}")
        results.append((name, ok, required))

    # Resumen
    total    = len(results)
    ok_count = sum(1 for _, ok, _ in results if ok)
    req_fail = [(n, r) for n, ok, r in results if not ok and r]

    print("\n" + SEP2)
    print(f"  {ok_count} de {total} APIs configuradas correctamente.")

    if req_fail:
        print(f"\n  ATENCION: {len(req_fail)} credencial(es) REQUERIDA(S) faltante(s):")
        for name, _ in req_fail:
            print(f"     -> Registrarte en {name} (ver CREDENTIALS_GUIDE.md)")

    if ok_count == total:
        print("\n  LISTO. Puedes conectar los clientes de API.")
    print(SEP + "\n")


if __name__ == "__main__":
    run_all_tests()
