"""
API Inspector — Formato real de respuestas de Banxico, INEGI y World Bank.

Ejecuta llamadas reales y muestra el JSON crudo + análisis de estructura
para saber exactamente cómo normalizar cada campo antes de armar datasets.

Uso:
    python tools/api_inspector.py
    python tools/api_inspector.py --only banxico
    python tools/api_inspector.py --only inegi
    python tools/api_inspector.py --only worldbank
"""

import sys
import json
import os
import urllib.request
import urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

try:
    from dotenv import load_dotenv
    load_dotenv(ROOT / ".env")
except ImportError:
    pass

BANXICO_TOKEN = os.environ.get("BANXICO_TOKEN", "")
INEGI_TOKEN   = os.environ.get("INEGI_TOKEN", "")

BANXICO_BASE  = "https://www.banxico.org.mx/SieAPIRest/service/v1"
INEGI_BASE    = "https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR"
WB_BASE       = "https://api.worldbank.org/v2"

SEP  = "=" * 72
SEP2 = "-" * 72


# ─── HTTP helpers ─────────────────────────────────────────────────────────────

def http_get(url: str, headers: dict = None, label: str = "") -> dict | list | None:
    req = urllib.request.Request(url, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            raw = resp.read()
            return json.loads(raw)
    except urllib.error.HTTPError as e:
        body = e.read().decode()[:300]
        print(f"  ✗ HTTP {e.code} — {body}")
        return None
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return None


def banxico_get(path: str) -> dict | None:
    return http_get(
        f"{BANXICO_BASE}{path}",
        headers={"Bmx-Token": BANXICO_TOKEN, "Accept": "application/json"},
    )


def inegi_get(indicator: str, area: str) -> dict | None:
    url = f"{INEGI_BASE}/{indicator}/es/{area}/false/BISE/2.0/{INEGI_TOKEN}?type=json"
    return http_get(url)


def wb_get(path: str, params: str = "") -> list | None:
    url = f"{WB_BASE}{path}?format=json"
    if params:
        url += f"&{params}"
    result = http_get(url)
    if isinstance(result, list) and len(result) > 1:
        return result
    return None


# ─── Análisis de campos ───────────────────────────────────────────────────────

def analyze_date_field(value: str) -> str:
    """Detecta el formato de un campo de fecha."""
    if not value:
        return "vacío"
    parts = value.split("/")
    if len(parts) == 3:
        return f"DD/MM/YYYY → '{value}' → año = '{value.split('/')[-1]}'"
    if len(parts) == 2:
        return f"MM/YYYY → '{value}' → año = '{value.split('/')[-1]}'"
    if len(value) == 4:
        return f"YYYY → '{value}'"
    if "-" in value and len(value) >= 7:
        return f"ISO → '{value}'"
    return f"desconocido → '{value}'"


def analyze_number_field(value: str) -> str:
    """Detecta formato y convierte campo numérico."""
    if not value:
        return "vacío"
    if value in ("N/E", "N/D", "NA"):
        return f"valor faltante = '{value}'"
    try:
        n = float(value)
        return f"string → float OK → {n:,.2f}"
    except ValueError:
        return f"no convertible → '{value}'"


# ─── BLOQUE 1: Banxico ────────────────────────────────────────────────────────

def inspect_banxico():
    print(f"\n{SEP}")
    print("  BANXICO SIE — Inspección de formatos")
    print(SEP)

    if not BANXICO_TOKEN:
        print("  ✗ BANXICO_TOKEN no configurado en .env")
        return

    # 1a. Serie de referencia — tipo de cambio (confirmada funcional)
    print(f"\n{SEP2}")
    print("  [B1] Serie de referencia: SF43878 (tipo de cambio USD/MXN)")
    print(SEP2)
    data = banxico_get("/series/SF43878/datos/oportuno")
    if data:
        series = data.get("bmx", {}).get("series", [{}])[0]
        print(f"\n  Campos disponibles en 'series[0]':")
        for k in series:
            v = series[k]
            if k != "datos":
                print(f"    {k:20s} = {repr(v)}")
        datos = series.get("datos", [])
        print(f"\n  Número de datos: {len(datos)}")
        if datos:
            d = datos[-1]
            print(f"  Último dato (raw): {d}")
            print(f"  · fecha: {analyze_date_field(d.get('fecha',''))}")
            print(f"  · dato:  {analyze_number_field(d.get('dato',''))}")

    # 1b. Remesas familiares — total nacional
    print(f"\n{SEP2}")
    print("  [B2] Remesas familiares total nacional — probando series candidatas")
    print(SEP2)

    candidates_national = ["SE27813", "SE27814", "SE4758", "SE4759"]
    for sid in candidates_national:
        print(f"\n  Probando {sid}...", end=" ")
        d = banxico_get(f"/series/{sid}/datos/oportuno")
        if d:
            s = d.get("bmx", {}).get("series", [{}])[0]
            titulo = s.get("titulo", "?")
            datos  = s.get("datos", [])
            if datos:
                ultimo = datos[-1]
                print(f"OK")
                print(f"    titulo:    {titulo}")
                print(f"    fecha:     {analyze_date_field(ultimo.get('fecha',''))}")
                print(f"    dato:      {analyze_number_field(ultimo.get('dato',''))}")
                print(f"    unidad:    {s.get('unidad','?')}")
                print(f"    cifra:     {s.get('cifra','?')}")
            else:
                print(f"OK (sin datos recientes — titulo: {titulo})")
        else:
            print("ERROR")

    # 1c. Remesas por estado — probar primeras 4 series del rango estimado
    print(f"\n{SEP2}")
    print("  [B3] Remesas por estado — probando rango SE55093–SE55096")
    print("  (si es correcto, el título de la serie debe mencionar el estado)")
    print(SEP2)

    for sid in ["SE55093", "SE55094", "SE55095", "SE55096"]:
        print(f"\n  Probando {sid}...", end=" ")
        d = banxico_get(f"/series/{sid}/datos/oportuno")
        if d:
            s = d.get("bmx", {}).get("series", [{}])[0]
            titulo = s.get("titulo", "?")
            datos  = s.get("datos", [])
            if datos:
                ultimo = datos[-1]
                print(f"OK")
                print(f"    titulo: {titulo}")
                print(f"    fecha:  {analyze_date_field(ultimo.get('fecha',''))}")
                print(f"    dato:   {analyze_number_field(ultimo.get('dato',''))}")
                print(f"    unidad: {s.get('unidad','?')}")
            else:
                print(f"OK — sin datos (titulo: {titulo})")
        else:
            print("ERROR o ID no existe")

    # 1d. Batch: ver si funcionan múltiples series en una sola llamada
    print(f"\n{SEP2}")
    print("  [B4] Batch de series (coma-separadas): SE55093,SE55094,SE55095")
    print(SEP2)
    d = banxico_get("/series/SE55093,SE55094,SE55095/datos/oportuno")
    if d:
        series_list = d.get("bmx", {}).get("series", [])
        print(f"  Respuesta: {len(series_list)} series devueltas")
        for s in series_list:
            titulo = s.get("titulo", "?")
            datos  = s.get("datos", [])
            sid    = s.get("idSerie", "?")
            ultimo = datos[-1] if datos else {}
            dato   = analyze_number_field(ultimo.get("dato", ""))
            print(f"    {sid}: '{titulo[:50]}' | dato: {dato}")

    # 1e. Historial completo de una serie — cuántos años regresa
    print(f"\n{SEP2}")
    print("  [B5] Historial completo de SE27813 (últimas 10 observaciones)")
    print(SEP2)
    d = banxico_get("/series/SE27813/datos")
    if d:
        s    = d.get("bmx", {}).get("series", [{}])[0]
        all_datos = s.get("datos", [])
        titulo = s.get("titulo", "?")
        print(f"  Titulo: {titulo}")
        print(f"  Total observaciones: {len(all_datos)}")
        if all_datos:
            print(f"  Primera: {all_datos[0]}")
            print(f"  Última:  {all_datos[-1]}")
            # Mostrar últimas 10
            print(f"\n  Últimas 10 observaciones:")
            for obs in all_datos[-10:]:
                fecha = obs.get("fecha", "")
                dato  = obs.get("dato", "")
                print(f"    {fecha:15s} | {dato}")


# ─── BLOQUE 2: INEGI BISE ─────────────────────────────────────────────────────

def inspect_inegi():
    print(f"\n{SEP}")
    print("  INEGI BISE — Inspección de formatos")
    print(SEP)

    if not INEGI_TOKEN:
        print("  ✗ INEGI_TOKEN no configurado en .env")
        return

    # 2a. Serie de referencia — Población total
    print(f"\n{SEP2}")
    print("  [I1] Serie de referencia: 1002000001 (Población total, área 00)")
    print(SEP2)
    data = inegi_get("1002000001", "00")
    if data:
        series = data.get("Series", [{}])[0]
        print(f"\n  Campos disponibles en 'Series[0]':")
        for k in series:
            if k != "OBSERVATIONS":
                print(f"    {k:25s} = {repr(series[k])}")
        obs = series.get("OBSERVATIONS", [])
        print(f"\n  Total observaciones: {len(obs)}")
        if obs:
            print(f"  Primera: {obs[0]}")
            print(f"  Última:  {obs[-1]}")
            print(f"\n  Análisis del último dato:")
            print(f"  · TIME_PERIOD: {analyze_date_field(obs[-1].get('TIME_PERIOD',''))}")
            print(f"  · OBS_VALUE:   {analyze_number_field(obs[-1].get('OBS_VALUE',''))}")
            if len(obs) >= 5:
                print(f"\n  Muestra de 5 observaciones:")
                for o in obs[-5:]:
                    tp  = o.get("TIME_PERIOD", "?")
                    val = o.get("OBS_VALUE", "?")
                    print(f"    {tp:12s} | {val}")

    # 2b. PIB por entidad — probar varios indicadores para Michoacán (área 16)
    print(f"\n{SEP2}")
    print("  [I2] PIB/PIBE por entidad — probando indicadores candidatos (área 16 = Michoacán)")
    print(SEP2)

    pib_candidates = [
        ("6207020003", "PIB estatal — candidato 1"),
        ("6207020001", "PIB estatal — candidato 2"),
        ("6207020004", "PIB estatal — candidato 3"),
        ("6200033148", "PIB estatal — candidato 4"),
        ("6207020002", "PIB estatal — candidato 5"),
    ]

    for indicator, label in pib_candidates:
        print(f"\n  Probando {indicator} ({label})...", end=" ")
        data = inegi_get(indicator, "16")
        if data:
            series = data.get("Series", [{}])[0]
            obs = series.get("OBSERVATIONS", [])
            if obs:
                print(f"OK — {len(obs)} observaciones")
                print(f"    UNIT_MULT:  {series.get('UNIT_MULT','?')}")
                print(f"    FREQ:       {series.get('FREQ','?')}")
                print(f"    Periodo:    {obs[0].get('TIME_PERIOD','?')} → {obs[-1].get('TIME_PERIOD','?')}")
                print(f"    Último val: {analyze_number_field(obs[-1].get('OBS_VALUE',''))}")
                print(f"    Última obs: {obs[-1]}")
            else:
                print(f"OK — sin observaciones (vacío)")
                print(f"    Respuesta: {str(data)[:200]}")
        else:
            print("ERROR")

    # 2c. Probar PIB nacional (área 00) para ver qué devuelve
    print(f"\n{SEP2}")
    print("  [I3] PIB estatal — área 00 (nacional) para ver si da total")
    print(SEP2)
    for indicator, label in pib_candidates[:2]:
        print(f"\n  Probando {indicator}, área 00...", end=" ")
        data = inegi_get(indicator, "00")
        if data:
            series = data.get("Series", [{}])[0]
            obs = series.get("OBSERVATIONS", [])
            if obs:
                print(f"OK — {len(obs)} obs | último: {obs[-1]}")
            else:
                print(f"OK — vacío")
        else:
            print("ERROR")

    # 2d. Probar índice de intensidad migratoria si existe en BISE
    print(f"\n{SEP2}")
    print("  [I4] Exploración: INEGI ENIGH / microdatos remesas — 6xxxxxxx")
    print(SEP2)
    enigh_candidates = ["6500095380", "6500095379", "1002000004", "3104000040"]
    for indicator in enigh_candidates:
        print(f"  Probando {indicator}...", end=" ")
        data = inegi_get(indicator, "00")
        if data:
            series = data.get("Series", [{}])[0]
            obs = series.get("OBSERVATIONS", [])
            print(f"OK — {len(obs)} obs" if obs else "OK — vacío")
        else:
            print("ERROR")


# ─── BLOQUE 3: World Bank ─────────────────────────────────────────────────────

def inspect_worldbank():
    print(f"\n{SEP}")
    print("  WORLD BANK — Inspección de formatos")
    print(SEP)

    # 3a. Remesas como % del PIB (BX.TRF.PWKR.DT.GD.ZS)
    print(f"\n{SEP2}")
    print("  [W1] Remesas México como % del PIB (BX.TRF.PWKR.DT.GD.ZS)")
    print(SEP2)
    data = wb_get("/country/MX/indicator/BX.TRF.PWKR.DT.GD.ZS", "mrv=5&per_page=5")
    if data and len(data) > 1:
        meta = data[0]
        obs  = data[1]
        print(f"  Metadata: {meta}")
        print(f"\n  Observaciones (últimas 5):")
        for o in obs:
            print(f"    {o}")
        if obs:
            o = obs[0]
            print(f"\n  Análisis del campo 'date':  {analyze_date_field(str(o.get('date','?')))}")
            val = o.get("value")
            print(f"  Análisis del campo 'value': {type(val).__name__} → {val}")

    # 3b. Remesas totales (valor absoluto)
    print(f"\n{SEP2}")
    print("  [W2] Remesas México totales en USD (BX.TRF.PWKR.CD.DT)")
    print(SEP2)
    data = wb_get("/country/MX/indicator/BX.TRF.PWKR.CD.DT", "mrv=10&per_page=10")
    if data and len(data) > 1:
        obs = data[1]
        print(f"  Total observaciones: {len(obs)}")
        print(f"\n  Todas las observaciones disponibles:")
        for o in obs:
            date = o.get("date", "?")
            val  = o.get("value")
            formatted = f"{val/1e9:.2f}B USD" if val else "N/A"
            print(f"    {date} | raw: {val} | {formatted}")

    # 3c. Serie histórica larga
    print(f"\n{SEP2}")
    print("  [W3] Serie histórica 2000-2024 (date range)")
    print(SEP2)
    data = wb_get("/country/MX/indicator/BX.TRF.PWKR.CD.DT", "date=2000:2024&per_page=30")
    if data and len(data) > 1:
        obs = sorted(data[1], key=lambda x: x.get("date", ""), reverse=False)
        print(f"  Total observaciones: {len(obs)}")
        print(f"  Rango: {obs[0].get('date') if obs else '?'} — {obs[-1].get('date') if obs else '?'}")
        print(f"\n  Serie completa:")
        for o in obs:
            date = o.get("date", "?")
            val  = o.get("value")
            if val:
                print(f"    {date} | {val/1e9:6.2f}B USD")
            else:
                print(f"    {date} | N/A (sin dato)")


# ─── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    only = None
    if "--only" in sys.argv:
        idx = sys.argv.index("--only")
        if idx + 1 < len(sys.argv):
            only = sys.argv[idx + 1].lower()

    print(f"\n{SEP}")
    print("  API Inspector — Proyecto remesas-mx")
    print("  Propósito: documentar formatos reales antes de normalizar")
    print(SEP)
    print(f"\n  Tokens configurados:")
    print(f"    BANXICO_TOKEN: {'✓ configurado' if BANXICO_TOKEN else '✗ FALTA en .env'}")
    print(f"    INEGI_TOKEN:   {'✓ configurado' if INEGI_TOKEN else '✗ FALTA en .env'}")
    print(f"    World Bank:    ✓ sin token (acceso libre)")

    if only is None or only == "banxico":
        inspect_banxico()
    if only is None or only == "inegi":
        inspect_inegi()
    if only is None or only == "worldbank":
        inspect_worldbank()

    print(f"\n{SEP}")
    print("  Inspección completa.")
    print("  Usa la salida arriba para actualizar data_fetcher.py y visual_standards.py")
    print(SEP + "\n")


if __name__ == "__main__":
    main()
