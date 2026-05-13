"""
Prueba de conectividad real para todas las APIs del proyecto.
Hace una llamada minima a cada endpoint para confirmar que las credenciales funcionan.

Uso:
    python 00_Orchestrator/tools/test_apis.py
"""

import sys
import os
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "00_Orchestrator"))

from dotenv import load_dotenv
load_dotenv(ROOT / ".env")

try:
    import requests
except ImportError:
    print("FALTA: pip install requests")
    sys.exit(1)

SEP = "=" * 65

results = {}


def test(name):
    def decorator(fn):
        def wrapper():
            try:
                msg = fn()
                results[name] = ("OK", msg)
                print(f"  [OK]  {name}")
                print(f"        {msg}")
            except AssertionError as e:
                results[name] = ("FAIL", str(e))
                print(f"  [!!]  {name}")
                print(f"        {e}")
            except Exception as e:
                results[name] = ("ERROR", str(e))
                print(f"  [ERR] {name}")
                print(f"        {e}")
        return wrapper
    return decorator


# --- ELEVENLABS ---------------------------------------------------------------

@test("ElevenLabs — listar voces")
def test_elevenlabs():
    key = os.environ.get("ELEVENLABS_API_KEY", "")
    assert key, "ELEVENLABS_API_KEY vacia en .env"
    r = requests.get(
        "https://api.elevenlabs.io/v1/voices",
        headers={"xi-api-key": key},
        timeout=10,
    )
    assert r.status_code == 200, f"HTTP {r.status_code}: {r.text[:200]}"
    data = r.json()
    voices = data.get("voices", [])
    names = [v["name"] for v in voices[:5]]
    return f"{len(voices)} voces disponibles. Primeras: {', '.join(names)}"


# --- BANXICO ------------------------------------------------------------------

@test("Banxico SIE — tipo de cambio USD/MXN (SF43878)")
def test_banxico():
    token = os.environ.get("BANXICO_TOKEN", "")
    assert token, "BANXICO_TOKEN vacio en .env"
    url = f"https://www.banxico.org.mx/SieAPIRest/service/v1/series/SF43878/datos/oportuno"
    r = requests.get(
        url,
        headers={"Bmx-Token": token},
        timeout=10,
    )
    assert r.status_code == 200, f"HTTP {r.status_code}: {r.text[:200]}"
    data = r.json()
    series = data.get("bmx", {}).get("series", [{}])[0]
    datos = series.get("datos", [])
    assert datos, "Sin datos en la respuesta"
    ultimo = datos[-1]
    return f"Ultimo dato: {ultimo.get('fecha')} = {ultimo.get('dato')} MXN/USD"


# --- INEGI --------------------------------------------------------------------

@test("INEGI BISE — Poblacion total (indicador 1002000001)")
def test_inegi():
    token = os.environ.get("INEGI_TOKEN", "")
    assert token, "INEGI_TOKEN vacio en .env"
    # IMPORTANTE: banco=BISE (no BIE), area=00 (nacional), ?type=json al final
    indicator = "1002000001"
    url = (
        f"https://www.inegi.org.mx/app/api/indicadores/desarrolladores/"
        f"jsonxml/INDICATOR/{indicator}/es/00/false/BISE/2.0/{token}?type=json"
    )
    r = requests.get(url, timeout=15)
    assert r.status_code == 200, f"HTTP {r.status_code}: {r.text[:200]}"
    data = r.json()
    obs = data.get("Series", [{}])[0].get("OBSERVATIONS", [])
    assert obs, f"Sin observaciones. Respuesta: {str(data)[:300]}"
    ultimo = obs[-1]
    return f"Ultimo dato: periodo {ultimo.get('TIME_PERIOD')} = {float(ultimo.get('OBS_VALUE', 0)):,.0f} habitantes"


# --- DATAWRAPPER --------------------------------------------------------------

@test("Datawrapper — info de cuenta")
def test_datawrapper():
    token = os.environ.get("DATAWRAPPER_TOKEN", "")
    assert token, "DATAWRAPPER_TOKEN vacio en .env -- configurar en .env"
    r = requests.get(
        "https://api.datawrapper.de/v3/me",
        headers={"Authorization": f"Bearer {token}"},
        timeout=10,
    )
    assert r.status_code == 200, f"HTTP {r.status_code}: {r.text[:200]}"
    data = r.json()
    email = data.get("email", "?")
    plan = data.get("activeProduct", {}).get("name", "?")
    return f"Cuenta: {email} | Plan: {plan}"


# --- GOOGLE AI (IMAGEN 3 / GEMINI) -------------------------------------------

@test("Google AI Studio — Gemini 2.0 Flash (modelos disponibles)")
def test_google():
    key = os.environ.get("GOOGLE_API_KEY", "")
    assert key, "GOOGLE_API_KEY vacio en .env -- ver https://aistudio.google.com/app/apikey"
    r = requests.get(
        "https://generativelanguage.googleapis.com/v1beta/models",
        params={"key": key},
        timeout=10,
    )
    assert r.status_code == 200, f"HTTP {r.status_code}: {r.text[:300]}"
    data = r.json()
    models = [m["name"].split("/")[-1] for m in data.get("models", [])]
    imagen = [m for m in models if "imagen" in m.lower()]
    gemini = [m for m in models if "gemini-2" in m.lower()][:3]
    return f"Imagen models: {imagen[:3]} | Gemini 2.x: {gemini}"


# --- PEXELS -------------------------------------------------------------------

@test("Pexels — busqueda de prueba ('mexico')")
def test_pexels():
    key = os.environ.get("PEXELS_API_KEY", "")
    assert key, "PEXELS_API_KEY vacio en .env -- ver https://www.pexels.com/api/"
    r = requests.get(
        "https://api.pexels.com/v1/search",
        headers={"Authorization": key},
        params={"query": "mexico", "per_page": 1},
        timeout=10,
    )
    assert r.status_code == 200, f"HTTP {r.status_code}: {r.text[:200]}"
    data = r.json()
    total = data.get("total_results", 0)
    return f"{total} fotos disponibles para 'mexico'"


# --- UNSPLASH -----------------------------------------------------------------

@test("Unsplash — busqueda de prueba ('remesas')")
def test_unsplash():
    key = os.environ.get("UNSPLASH_ACCESS_KEY", "")
    assert key, "UNSPLASH_ACCESS_KEY vacio en .env -- ver https://unsplash.com/developers"
    r = requests.get(
        "https://api.unsplash.com/search/photos",
        headers={"Authorization": f"Client-ID {key}"},
        params={"query": "remesas", "per_page": 1},
        timeout=10,
    )
    assert r.status_code == 200, f"HTTP {r.status_code}: {r.text[:200]}"
    data = r.json()
    total = data.get("total", 0)
    return f"{total} fotos disponibles para 'remesas'"


# --- PIXABAY ------------------------------------------------------------------

@test("Pixabay — busqueda de prueba ('economia')")
def test_pixabay():
    key = os.environ.get("PIXABAY_API_KEY", "")
    assert key, "PIXABAY_API_KEY vacio en .env -- ver https://pixabay.com/api/docs/"
    r = requests.get(
        "https://pixabay.com/api/",
        params={"key": key, "q": "economia", "per_page": 3, "lang": "es"},
        timeout=10,
    )
    assert r.status_code == 200, f"HTTP {r.status_code}: {r.text[:200]}"
    data = r.json()
    total = data.get("totalHits", 0)
    return f"{total} fotos disponibles para 'economia'"


# --- WORLD BANK (sin token) ---------------------------------------------------

@test("World Bank Open Data — remesas Mexico (BX.TRF.PWKR.DT.GD.ZS)")
def test_worldbank():
    url = "https://api.worldbank.org/v2/country/MX/indicator/BX.TRF.PWKR.DT.GD.ZS"
    r = requests.get(url, params={"format": "json", "mrv": 1}, timeout=15)
    assert r.status_code == 200, f"HTTP {r.status_code}"
    data = r.json()
    obs = data[1]
    assert obs, "Sin datos"
    ultimo = obs[0]
    return f"Remesas/PIB Mexico: {ultimo.get('date')} = {ultimo.get('value'):.2f}%"


# --- MAIN ---------------------------------------------------------------------

def main():
    print("\n" + SEP)
    print("  TEST DE APIs -- Conexion y autenticacion real")
    print(SEP)

    test_elevenlabs()
    test_banxico()
    test_inegi()
    test_worldbank()
    test_datawrapper()
    test_google()
    test_pexels()
    test_unsplash()
    test_pixabay()

    ok_count   = sum(1 for s, _ in results.values() if s == "OK")
    fail_count = sum(1 for s, _ in results.values() if s in ("FAIL", "ERROR"))

    print(f"\n{SEP}")
    print(f"  RESULTADO: {ok_count}/{len(results)} APIs funcionando")

    if fail_count:
        print(f"\n  APIs con problemas:")
        for name, (status, msg) in results.items():
            if status != "OK":
                print(f"    [{status}] {name}: {msg[:80]}")

    print(SEP + "\n")


if __name__ == "__main__":
    main()
