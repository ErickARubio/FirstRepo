"""
Verificacion funcional de APIs — fetcha datos reales y muestra valores.
Uso: python 00_Orchestrator/tools/verify_data.py

A diferencia de test_connections.py (que solo verifica autenticacion),
este script confirma que el pipeline de datos funciona de extremo a extremo.
"""

import sys
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

try:
    import httpx
except ImportError:
    print("httpx no instalado. Ejecuta: pip install -r 00_Orchestrator/tools/requirements.txt")
    sys.exit(1)

sys.path.insert(0, str(ROOT / "00_Orchestrator"))
from tools.config import get_credential_optional  # noqa


# ─── VERIFICACIONES POR API ───────────────────────────────────────────────────

def verify_banxico_remesas() -> tuple:
    token = get_credential_optional("BANXICO_TOKEN")
    if not token:
        return False, "FALTA BANXICO_TOKEN", None
    try:
        # SE27803 = Remesas Familiares Total (millones de dolares, mensual)
        r = httpx.get(
            "https://www.banxico.org.mx/SieAPIRest/service/v1/series/SE27803/datos/oportuno",
            headers={"Bmx-Token": token},
            timeout=12,
        )
        if r.status_code == 200:
            datos = r.json().get("bmx", {}).get("series", [{}])[0].get("datos", [])
            if datos:
                last = datos[-1]
                return True, f"SE27803 remesas: {last.get('fecha', '?')} = ${last.get('dato', '?')} MDD", last
            return False, "Sin datos en la respuesta", None
        return False, f"Error {r.status_code}", None
    except httpx.TimeoutException:
        return False, "Timeout", None
    except Exception as e:
        return False, str(e), None


def verify_banxico_tipo_cambio() -> tuple:
    token = get_credential_optional("BANXICO_TOKEN")
    if not token:
        return False, "FALTA BANXICO_TOKEN", None
    try:
        r = httpx.get(
            "https://www.banxico.org.mx/SieAPIRest/service/v1/series/SF43718/datos/oportuno",
            headers={"Bmx-Token": token},
            timeout=12,
        )
        if r.status_code == 200:
            datos = r.json().get("bmx", {}).get("series", [{}])[0].get("datos", [])
            if datos:
                last = datos[-1]
                return True, f"SF43718 USD/MXN: {last.get('fecha', '?')} = {last.get('dato', '?')} MXN", last
            return False, "Sin datos", None
        return False, f"Error {r.status_code}", None
    except httpx.TimeoutException:
        return False, "Timeout", None
    except Exception as e:
        return False, str(e), None


def verify_inegi_poblacion() -> tuple:
    token = get_credential_optional("INEGI_TOKEN")
    if not token:
        return False, "FALTA INEGI_TOKEN", None
    try:
        url = (
            f"https://www.inegi.org.mx/app/api/indicadores/desarrolladores/"
            f"jsonxml/INDICATOR/1002000001/es/00/false/BISE/2.0/{token}?type=json"
        )
        r = httpx.get(url, timeout=12)
        if r.status_code == 200:
            series = r.json().get("Series", [{}])
            obs = series[0].get("OBSERVATIONS", []) if series else []
            if obs:
                # Las observaciones vienen de mas reciente a mas antigua
                latest = obs[0]
                val = int(float(latest.get("OBS_VALUE", 0)))
                return True, f"Poblacion MX: {latest.get('TIME_PERIOD', '?')} = {val:,} hab.", latest
            return False, "Sin observaciones en la respuesta", None
        return False, f"Error {r.status_code}: {r.text[:60]}", None
    except Exception as e:
        return False, str(e), None


def verify_worldbank_remesas() -> tuple:
    try:
        r = httpx.get(
            "https://api.worldbank.org/v2/country/MX/indicator/BX.TRF.PWKR.CD.DT"
            "?format=json&mrv=3",
            timeout=10,
        )
        if r.status_code == 200:
            raw = r.json()
            if len(raw) >= 2 and raw[1]:
                data = [d for d in raw[1] if d.get("value") is not None]
                if data:
                    d = data[0]
                    val_b = d["value"] / 1e9
                    return True, f"Remesas MX {d['date']}: USD {val_b:.1f}B (corrientes)", d
            return False, "Sin datos", None
        return False, f"Error {r.status_code}", None
    except Exception as e:
        return False, str(e), None


def verify_worldbank_remesas_pct() -> tuple:
    try:
        r = httpx.get(
            "https://api.worldbank.org/v2/country/MX/indicator/BX.TRF.PWKR.DT.GD.ZS"
            "?format=json&mrv=3",
            timeout=10,
        )
        if r.status_code == 200:
            raw = r.json()
            if len(raw) >= 2 and raw[1]:
                data = [d for d in raw[1] if d.get("value") is not None]
                if data:
                    d = data[0]
                    return True, f"Remesas % PIB {d['date']}: {d['value']:.2f}% del PIB", d
            return False, "Sin datos", None
        return False, f"Error {r.status_code}", None
    except Exception as e:
        return False, str(e), None


def verify_elevenlabs_cuota() -> tuple:
    key = get_credential_optional("ELEVENLABS_API_KEY")
    if not key:
        return False, "FALTA ELEVENLABS_API_KEY", None
    try:
        r = httpx.get(
            "https://api.elevenlabs.io/v1/user/subscription",
            headers={"xi-api-key": key},
            timeout=8,
        )
        if r.status_code == 200:
            data = r.json()
            used  = data.get("character_count", 0)
            limit = data.get("character_limit", 0)
            return True, f"Cuota: {limit - used:,} chars disponibles / {limit:,} limite", data
        elif r.status_code == 401:
            detail = r.json().get("detail", {})
            if isinstance(detail, dict) and detail.get("status") == "missing_permissions":
                # Key valida, solo scope limitado — no bloquea la produccion
                return None, "Key valida (scope user_read no asignado — no bloquea produccion)", None
            return False, "Key invalida (401)", None
        return False, f"Error {r.status_code}", None
    except Exception as e:
        return False, str(e), None


# ─── RUNNER ───────────────────────────────────────────────────────────────────

VERIFICATIONS = [
    ("Banxico   CE81   remesas familiares",  verify_banxico_remesas),
    ("Banxico   SF43718 tipo de cambio",     verify_banxico_tipo_cambio),
    ("INEGI     poblacion total",            verify_inegi_poblacion),
    ("WorldBank remesas MX (USD)",           verify_worldbank_remesas),
    ("WorldBank remesas MX (% PIB)",         verify_worldbank_remesas_pct),
    ("ElevenLabs cuota de caracteres",       verify_elevenlabs_cuota),
]


def run_verification():
    SEP  = "=" * 70
    SEP2 = "-" * 70
    print("\n" + SEP)
    print("  Verificacion funcional — datos reales por API")
    print(SEP)

    ok_count = 0
    for name, fn in VERIFICATIONS:
        print(f"  Consultando {name}...", end="\r", flush=True)
        ok, detail, _ = fn()
        if ok is True:
            icon = "[OK]"
            ok_count += 1
        elif ok is None:
            icon = "[~~]"
            ok_count += 1
        else:
            icon = "[--]"
        print(f"  {icon}  {name:<38} {detail}")

    print("\n" + SEP2)
    print(f"  {ok_count} de {len(VERIFICATIONS)} verificaciones exitosas.")
    if ok_count == len(VERIFICATIONS):
        print("  Todos los datos fluyen correctamente. Listo para produccion.")
    print(SEP + "\n")


if __name__ == "__main__":
    run_verification()
