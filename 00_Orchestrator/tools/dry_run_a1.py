"""
Simulacro del Agente A1 — fetcha todas las series economicas del video de remesas.
Uso: python 00_Orchestrator/tools/dry_run_a1.py

Replica exactamente lo que A1 (Investigador) hara cuando el Orquestador le asigne
la Pieza 2 del megaREGION ZMVM. Guarda los datos crudos en:
    00_Orchestrator/staging/a1_data_raw.json

Los datos quedan listos para que A1 los analice y redacte el reporte de investigacion.
"""

import sys
import os
import json
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

try:
    import httpx
except ImportError:
    print("httpx no instalado. Ejecuta: pip install -r 00_Orchestrator/tools/requirements.txt")
    sys.exit(1)

sys.path.insert(0, str(ROOT / "00_Orchestrator"))
from tools.config import get_credential_optional  # noqa

STAGING_DIR = ROOT / "00_Orchestrator" / "staging"
OUTPUT_FILE = STAGING_DIR / "a1_data_raw.json"


# ─── FETCHERS ─────────────────────────────────────────────────────────────────

def fetch_banxico_serie(token: str, serie: str, titulo: str, anios: int = 5) -> dict:
    from datetime import date
    fecha_fin = date.today().strftime("%Y-%m-%d")
    fecha_ini = f"{date.today().year - anios}-01-01"
    url = (
        f"https://www.banxico.org.mx/SieAPIRest/service/v1/series/{serie}"
        f"/datos/{fecha_ini}/{fecha_fin}"
    )
    try:
        r = httpx.get(url, headers={"Bmx-Token": token}, timeout=15)
        if r.status_code == 200:
            raw  = r.json().get("bmx", {}).get("series", [{}])[0]
            datos = raw.get("datos", [])
            return {
                "status": "ok",
                "serie":  serie,
                "titulo": titulo,
                "rango":  f"{fecha_ini} / {fecha_fin}",
                "n_obs":  len(datos),
                "ultimo": datos[-1] if datos else None,
                "datos":  datos,
            }
        return {"status": "error", "serie": serie, "titulo": titulo,
                "http": r.status_code, "body": r.text[:120]}
    except Exception as e:
        return {"status": "error", "serie": serie, "titulo": titulo, "exc": str(e)}


def fetch_inegi_indicador(token: str, indicador: str, titulo: str) -> dict:
    url = (
        f"https://www.inegi.org.mx/app/api/indicadores/desarrolladores/"
        f"jsonxml/INDICATOR/{indicador}/es/00/false/BISE/2.0/{token}?type=json"
    )
    try:
        r = httpx.get(url, timeout=15)
        if r.status_code == 200:
            series = r.json().get("Series", [{}])
            obs    = series[0].get("OBSERVATIONS", []) if series else []
            # Las observaciones vienen de mas reciente a mas antigua
            return {
                "status":    "ok",
                "indicador": indicador,
                "titulo":    titulo,
                "n_obs":     len(obs),
                "ultimo":    obs[0] if obs else None,
                "datos":     obs,
            }
        return {"status": "error", "indicador": indicador, "titulo": titulo,
                "http": r.status_code, "body": r.text[:120]}
    except Exception as e:
        return {"status": "error", "indicador": indicador, "titulo": titulo, "exc": str(e)}


def fetch_worldbank(indicator: str, titulo: str, mrv: int = 10) -> dict:
    url = (
        f"https://api.worldbank.org/v2/country/MX/indicator/{indicator}"
        f"?format=json&mrv={mrv}"
    )
    try:
        r = httpx.get(url, timeout=12)
        if r.status_code == 200:
            raw  = r.json()
            data = []
            if len(raw) >= 2 and raw[1]:
                data = [d for d in raw[1] if d.get("value") is not None]
            return {
                "status":    "ok",
                "indicator": indicator,
                "titulo":    titulo,
                "n_obs":     len(data),
                "ultimo":    data[0] if data else None,
                "datos":     data,
            }
        return {"status": "error", "indicator": indicator, "titulo": titulo,
                "http": r.status_code}
    except Exception as e:
        return {"status": "error", "indicator": indicator, "titulo": titulo, "exc": str(e)}


# ─── RUNNER PRINCIPAL ─────────────────────────────────────────────────────────

def run_dry_run():
    SEP  = "=" * 70
    SEP2 = "-" * 70
    print("\n" + SEP)
    print("  DRY RUN A1 — Simulacro de recopilacion de datos (remesas ZMVM)")
    print(SEP)

    banxico_token = get_credential_optional("BANXICO_TOKEN")
    inegi_token   = get_credential_optional("INEGI_TOKEN")

    resultados = {}
    errores    = []

    # ── Banxico ───────────────────────────────────────────────────────────────
    print("\n  [Banxico] Fetching series economicas...")

    series_banxico = [
        ("SE27803", "Remesas familiares total (MDD)",                5),
        ("SE27806", "Remesas — transferencias electronicas (MDD)",   5),
        ("SE27808", "Remesas familiares total (numero de operaciones)", 5),
        ("SF43718", "Tipo de cambio USD/MXN fix",                    3),
    ]
    if banxico_token:
        for serie, titulo, anios in series_banxico:
            print(f"    -> {serie} {titulo}...", end=" ", flush=True)
            res = fetch_banxico_serie(banxico_token, serie, titulo, anios)
            resultados[f"banxico_{serie.lower()}"] = res
            if res["status"] == "ok":
                ult = res["ultimo"]
                print(f"OK ({res['n_obs']} obs) | ultimo: {ult}")
            else:
                print(f"ERROR: {res.get('http', res.get('exc', '?'))}")
                errores.append(f"Banxico {serie}")
    else:
        print("    SKIP — BANXICO_TOKEN no configurado")

    # ── INEGI ─────────────────────────────────────────────────────────────────
    print("\n  [INEGI] Fetching indicadores nacionales...")

    indicadores_inegi = [
        ("1002000001", "Poblacion total nacional"),
    ]
    if inegi_token:
        for ind, titulo in indicadores_inegi:
            print(f"    -> {ind} {titulo}...", end=" ", flush=True)
            res = fetch_inegi_indicador(inegi_token, ind, titulo)
            resultados[f"inegi_{ind}"] = res
            if res["status"] == "ok":
                ult = res["ultimo"]
                print(f"OK ({res['n_obs']} obs) | ultimo: {ult}")
            else:
                print(f"ERROR: {res.get('http', res.get('body', res.get('exc', '?')))}")
                errores.append(f"INEGI {ind}")
    else:
        print("    SKIP — INEGI_TOKEN no configurado")

    # ── World Bank ────────────────────────────────────────────────────────────
    print("\n  [World Bank] Fetching indicadores Mexico...")

    indicadores_wb = [
        ("BX.TRF.PWKR.CD.DT",    "Remesas recibidas (USD corrientes)",    10),
        ("BX.TRF.PWKR.DT.GD.ZS", "Remesas como % del PIB",               10),
        ("NY.GDP.MKTP.CD",        "PIB Mexico (USD corrientes)",           10),
        ("NY.GDP.PCAP.CD",        "PIB per capita Mexico (USD)",           10),
    ]
    for ind, titulo, mrv in indicadores_wb:
        print(f"    -> {ind}...", end=" ", flush=True)
        res = fetch_worldbank(ind, titulo, mrv)
        resultados[f"worldbank_{ind.replace('.', '_').lower()}"] = res
        if res["status"] == "ok":
            ult = res["ultimo"]
            print(f"OK ({res['n_obs']} obs) | ultimo: {ult.get('date')} = {ult.get('value')}")
        else:
            print(f"ERROR: {res.get('http', res.get('exc', '?'))}")
            errores.append(f"WorldBank {ind}")

    # ── Guardar JSON ──────────────────────────────────────────────────────────
    STAGING_DIR.mkdir(parents=True, exist_ok=True)
    output = {
        "generated_at": datetime.now().isoformat(),
        "topic":        "remesas_zmvm_pieza_2",
        "errores":      errores,
        "fuentes":      resultados,
    }
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    # ── Resumen ───────────────────────────────────────────────────────────────
    total  = len(resultados)
    ok_cnt = sum(1 for v in resultados.values() if v.get("status") == "ok")
    print("\n" + SEP2)
    print(f"  {ok_cnt} de {total} fuentes descargadas correctamente.")
    if errores:
        print(f"  Errores: {', '.join(errores)}")
    print(f"  Datos guardados en: {OUTPUT_FILE.relative_to(ROOT)}")
    if ok_cnt == total:
        print("  A1 tiene todos los datos para iniciar el analisis.")
    print(SEP + "\n")


if __name__ == "__main__":
    run_dry_run()
