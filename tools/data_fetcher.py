"""
Fetches live economic data from Banxico SIE and INEGI BISE for map generation.

M01 — Remesas familiares por entidad federativa (Banxico SIE, annual)
M02 — PIB por entidad federativa, crecimiento % (INEGI BISE)

Falls back to caller-supplied hardcoded dicts if any API call fails.
"""

import json
import urllib.request
import urllib.error

BANXICO_BASE = "https://www.banxico.org.mx/SieAPIRest/service/v1"
INEGI_BASE   = "https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR"

# ─── Banxico: series de remesas familiares anuales por entidad ───────────────
# IDs en el SIE: Sector Externo → Remesas familiares → Por entidad federativa
# Si un ID devuelve error o "N/E", ese estado usará el valor hardcodeado de fallback.
BANXICO_REMESAS_BY_STATE = {
    "Aguascalientes":        "SE55093",
    "Baja California":       "SE55094",
    "Baja California Sur":   "SE55095",
    "Campeche":              "SE55096",
    "Coahuila":              "SE55097",
    "Colima":                "SE55098",
    "Chiapas":               "SE55099",
    "Chihuahua":             "SE55100",
    "Ciudad de México":      "SE55101",
    "Durango":               "SE55102",
    "Guanajuato":            "SE55103",
    "Guerrero":              "SE55104",
    "Hidalgo":               "SE55105",
    "Jalisco":               "SE55106",
    "Estado de México":      "SE55107",
    "Michoacán":             "SE55108",
    "Morelos":               "SE55109",
    "Nayarit":               "SE55110",
    "Nuevo León":            "SE55111",
    "Oaxaca":                "SE55112",
    "Puebla":                "SE55113",
    "Querétaro":             "SE55114",
    "Quintana Roo":          "SE55115",
    "San Luis Potosí":       "SE55116",
    "Sinaloa":               "SE55117",
    "Sonora":                "SE55118",
    "Tabasco":               "SE55119",
    "Tamaulipas":            "SE55120",
    "Tlaxcala":              "SE55121",
    "Veracruz":              "SE55122",
    "Yucatán":               "SE55123",
    "Zacatecas":             "SE55124",
}

# ─── INEGI: PIB por entidad federativa ───────────────────────────────────────
# Indicador BISE para PIB estatal (millones de pesos corrientes).
# Alternativas si falla: 6207020001, 6200033148.
# INEGI BISE no soporta batch de áreas; las llamadas son secuenciales.
INEGI_PIB_INDICATOR = "6207020003"

# Claves de área INEGI (2 dígitos, estándar geoid 2020)
INEGI_STATE_AREAS = {
    "Aguascalientes":        "01",
    "Baja California":       "02",
    "Baja California Sur":   "03",
    "Campeche":              "04",
    "Coahuila":              "05",
    "Colima":                "06",
    "Chiapas":               "07",
    "Chihuahua":             "08",
    "Ciudad de México":      "09",
    "Durango":               "10",
    "Guanajuato":            "11",
    "Guerrero":              "12",
    "Hidalgo":               "13",
    "Jalisco":               "14",
    "Estado de México":      "15",
    "Michoacán":             "16",
    "Morelos":               "17",
    "Nayarit":               "18",
    "Nuevo León":            "19",
    "Oaxaca":                "20",
    "Puebla":                "21",
    "Querétaro":             "22",
    "Quintana Roo":          "23",
    "San Luis Potosí":       "24",
    "Sinaloa":               "25",
    "Sonora":                "26",
    "Tabasco":               "27",
    "Tamaulipas":            "28",
    "Tlaxcala":              "29",
    "Veracruz":              "30",
    "Yucatán":               "31",
    "Zacatecas":             "32",
}


# ─── HTTP helpers ─────────────────────────────────────────────────────────────

def _banxico_get(path: str, token: str) -> dict:
    req = urllib.request.Request(
        f"{BANXICO_BASE}{path}",
        headers={"Bmx-Token": token, "Accept": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=12) as resp:
        return json.loads(resp.read())


def _inegi_get(indicator: str, area: str, token: str) -> dict:
    url = f"{INEGI_BASE}/{indicator}/es/{area}/false/BISE/2.0/{token}?type=json"
    with urllib.request.urlopen(urllib.request.Request(url), timeout=12) as resp:
        return json.loads(resp.read())


# ─── Shared status helper ─────────────────────────────────────────────────────

def _build_status(states_live, all_states, label, periodo, live_source, est_source):
    """Prints fetch summary, returns (is_live, byline, source_name)."""
    n     = len(states_live)
    total = len(all_states)
    if n:
        print(f"    [{label}] {n}/{total} estados con datos en vivo ({periodo})")
        missing = total - n
        if missing:
            print(f"    [fallback] {missing} estados usan valor hardcodeado")
        return True, f"{label} {periodo} — {n}/{total} estados en vivo", live_source
    print(f"    [{label}] API no disponible — usando datos hardcodeados")
    return False, f"{label}, {periodo} (estimación)", est_source


# ─── Banxico: remesas por estado ──────────────────────────────────────────────

def fetch_remesas_banxico(banxico_token: str, fallback: dict) -> dict:
    """
    Fetches remesas familiares (millones USD) per state from Banxico SIE
    using a single batch request for all 32 states.

    Returns:
        data, periodo, fuente, is_live, states_from_api, byline, source_name
    """
    data        = dict(fallback)
    states_live = []
    periodo     = "2024"
    id_to_state = {v: k for k, v in BANXICO_REMESAS_BY_STATE.items()}

    try:
        ids  = ",".join(BANXICO_REMESAS_BY_STATE.values())
        resp = _banxico_get(f"/series/{ids}/datos/oportuno", banxico_token)
        for serie in resp.get("bmx", {}).get("series", []):
            estado = id_to_state.get(serie.get("idSerie", ""))
            if not estado:
                continue
            datos = serie.get("datos", [])
            if not datos:
                continue
            ultimo = datos[-1]
            fecha  = ultimo.get("fecha", "")
            valor  = ultimo.get("dato", "")
            if not valor or valor == "N/E":
                continue
            try:
                data[estado] = round(float(valor), 1)
            except ValueError:
                continue
            states_live.append(estado)
            if "/" in fecha:
                periodo = fecha.split("/")[-1]
            elif len(fecha) >= 4:
                periodo = fecha[:4]
    except Exception:
        pass  # all states fall back to hardcoded

    is_live, byline, source_name = _build_status(
        states_live, BANXICO_REMESAS_BY_STATE, "Banxico", periodo,
        "Banco de México (Banxico), Balanza de Pagos",
        "Banco de México (Banxico)",
    )
    return {
        "data":            data,
        "periodo":         periodo,
        "fuente":          "Banco de México (Banxico), SIE",
        "is_live":         is_live,
        "states_from_api": states_live,
        "byline":          byline,
        "source_name":     source_name,
    }


# ─── INEGI: crecimiento PIB por estado ───────────────────────────────────────

def fetch_pibe_inegi(inegi_token: str, fallback: dict, base_year: str = "2010") -> dict:
    """
    Fetches PIB by state from INEGI BISE and calculates accumulated growth
    from base_year to most recent available year.

    periodo reflects the actual min/max years across all successful states,
    not an arbitrary last-iterated value.
    """
    data        = dict(fallback)
    states_live = []
    yr_bases    = []
    yr_lasts    = []

    for estado, area in INEGI_STATE_AREAS.items():
        try:
            resp = _inegi_get(INEGI_PIB_INDICATOR, area, inegi_token)
            obs  = resp.get("Series", [{}])[0].get("OBSERVATIONS", [])
            if not obs:
                continue

            by_year = {}
            for o in obs:
                try:
                    by_year[o["TIME_PERIOD"][:4]] = float(o["OBS_VALUE"])
                except (KeyError, ValueError, TypeError):
                    pass

            years  = sorted(by_year)
            if len(years) < 2:
                continue

            yr_base = base_year if base_year in by_year else years[0]
            yr_last = years[-1]
            v_base  = by_year[yr_base]
            if v_base <= 0:
                continue

            data[estado] = round((by_year[yr_last] - v_base) / v_base * 100, 1)
            states_live.append(estado)
            yr_bases.append(yr_base)
            yr_lasts.append(yr_last)
        except Exception:
            pass

    periodo_ini = min(yr_bases) if yr_bases else base_year
    periodo_fin = max(yr_lasts) if yr_lasts else ""
    periodo     = f"{periodo_ini}–{periodo_fin}" if periodo_fin else f"{base_year} (estimación)"

    is_live, byline, source_name = _build_status(
        states_live, INEGI_STATE_AREAS, "INEGI", periodo,
        "Instituto Nacional de Estadística y Geografía (INEGI)",
        "INEGI, Producto Interno Bruto por Entidad Federativa (PIBE)",
    )
    return {
        "data":            data,
        "periodo":         periodo,
        "fuente":          "INEGI, PIBE — Crecimiento PIB por entidad",
        "is_live":         is_live,
        "states_from_api": states_live,
        "byline":          byline,
        "source_name":     source_name,
    }
