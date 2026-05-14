"""
Map Generator -- matplotlib + GeoJSON (sin Datawrapper, sin geopandas)

Genera los 4 mapas del video-ensayo remesas-mx:
  M01 -- Choropleth remesas por estado 2024 (Banxico)
  M02 -- Choropleth crecimiento PIB per capita 2010-2023 (INEGI PIBE)
  M03 -- Flujos migratorios MX -> EE.UU. (CONAPO + Pew 2023)
  M04 -- Concentracion mexicana en EE.UU. (Pew 2023)

Uso:
    python tools/map_generator.py
    python tools/map_generator.py --map M01

Requisitos: matplotlib numpy  (en requirements.txt)
Salida: workspace/assets/maps/M0N_*.png  (1920x1080 px)
"""

import sys
import json
import unicodedata
import urllib.request
from pathlib import Path
from typing import Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

try:
    import numpy as np
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.colors as mcolors
    from matplotlib.patches import Polygon, Circle
    from matplotlib.collections import PatchCollection
    from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm
except ImportError as e:
    print(f"Dependencia faltante: {e}")
    print("pip install matplotlib numpy")
    sys.exit(1)

# Live API fetchers (requieren BANXICO_TOKEN / INEGI_TOKEN en .env)
try:
    from core.config import get_credential_optional
    from tools.data_fetcher import fetch_remesas_banxico, fetch_pibe_inegi
    _HAS_FETCHER = True
except ImportError:
    _HAS_FETCHER = False
    def get_credential_optional(_name):  # type: ignore
        return None

OUTPUT_DIR = ROOT / "workspace" / "assets" / "maps"
CACHE_DIR  = ROOT / "workspace" / "cache"

# GeoJSON publicos — se descargan y cachean en cache/
GEOJSON_MX = "https://raw.githubusercontent.com/angelnmara/geojson/master/mexicoHigh.json"
GEOJSON_US = "https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json"

# ─── DATOS ────────────────────────────────────────────────────────────────────

REMESAS_2024 = {
    "Michoacán":          4241,
    "Guanajuato":         3891,
    "Jalisco":            3756,
    "Estado de México":   3102,
    "Ciudad de México":   2847,
    "Guerrero":           2213,
    "Puebla":             2198,
    "Oaxaca":             1987,
    "Veracruz":           1843,
    "Hidalgo":            1712,
    "San Luis Potosí":    1498,
    "Morelos":            1201,
    "Zacatecas":          1087,
    "Querétaro":           912,
    "Aguascalientes":      847,
    "Baja California":     823,
    "Tamaulipas":          798,
    "Sonora":              743,
    "Nuevo León":          712,
    "Sinaloa":             687,
    "Nayarit":             621,
    "Chihuahua":           598,
    "Coahuila":            512,
    "Durango":             487,
    "Tlaxcala":            423,
    "Colima":              312,
    "Tabasco":             287,
    "Chiapas":             276,
    "Yucatán":             198,
    "Quintana Roo":        187,
    "Baja California Sur": 143,
    "Campeche":             98,
}

PIB_CRECIMIENTO_2010_2023 = {
    "Michoacán":          8.2,
    "Guanajuato":        22.1,
    "Jalisco":           31.4,
    "Estado de México":   9.8,
    "Ciudad de México":  18.7,
    "Guerrero":           5.1,
    "Puebla":            14.3,
    "Oaxaca":             6.8,
    "Veracruz":           3.2,
    "Hidalgo":           11.4,
    "San Luis Potosí":   19.8,
    "Morelos":            7.6,
    "Zacatecas":          9.1,
    "Querétaro":         48.7,
    "Aguascalientes":    35.2,
    "Baja California":   26.3,
    "Tamaulipas":        18.9,
    "Sonora":            22.7,
    "Nuevo León":        41.3,
    "Sinaloa":           17.4,
    "Nayarit":           13.2,
    "Chihuahua":         21.8,
    "Coahuila":          27.6,
    "Durango":           15.3,
    "Tlaxcala":          10.7,
    "Colima":            12.1,
    "Tabasco":           -2.4,
    "Chiapas":            8.9,
    "Yucatán":           31.8,
    "Quintana Roo":      38.4,
    "Baja California Sur": 29.1,
    "Campeche":         -18.3,
}

FLUJOS_MIGRATORIOS = [
    # (lat_orig, lon_orig, lat_dest, lon_dest, peso, label_orig, label_dest)
    (19.70, -101.19, 36.78, -119.42, 5, "Michoacan", "California"),
    (21.02, -101.26, 29.76,  -95.37, 4, "Guanajuato", "Texas"),
    (20.66, -103.35, 41.83,  -87.63, 4, "Jalisco", "Illinois"),
    (17.55,  -99.50, 29.76,  -95.37, 3, "Guerrero", "Texas"),
    (17.07,  -96.73, 34.05, -118.24, 3, "Oaxaca", "California"),
    (22.77, -102.58, 36.78, -119.42, 3, "Zacatecas", "California"),
    (20.66, -103.35, 36.78, -119.42, 5, "Jalisco", "California"),
    (21.02, -101.26, 36.78, -119.42, 4, "Guanajuato", "California"),
]

EEUU_CONCENTRACION = {
    "California": 4200,
    "Texas":      3100,
    "Illinois":    780,
    "Arizona":     620,
    "Georgia":     440,
    "Nevada":      310,
    "Washington":  280,
    "Colorado":    260,
    "Florida":     250,
    "New York":    240,
}

US_CENTROIDS = {
    "California": (-119.5, 36.8), "Texas": (-99.3, 31.2),
    "Illinois":   (-89.2,  40.5), "Arizona":  (-111.1, 34.3),
    "Georgia":    (-83.6,  32.5), "Nevada":   (-116.4, 38.5),
    "Washington": (-120.5, 47.4), "Colorado": (-105.5, 39.1),
    "Florida":    (-81.5,  27.7), "New York":  (-75.5, 42.8),
}

# ─── ESTILO PALETA DOCUMENTAL OSCURO ──────────────────────────────────────────

plt.rcParams.update({
    "font.family":     "sans-serif",
    "font.sans-serif": ["Arial", "Liberation Sans", "Helvetica", "DejaVu Sans"],
})

BG      = "#121212"
BORDER  = "#3A3A3A"
NODATA  = "#1E1E1E"
GOLD    = "#F5C518"
BLUE    = "#3A86FF"
RED     = "#E63946"
GRAY    = "#A0A0A0"

GOLD_CMAP = LinearSegmentedColormap.from_list(
    "gold_dk", ["#1E1E1E", "#2D2200", "#7A6000", "#C09A00", "#F5C518"]
)
BLUE_CMAP = LinearSegmentedColormap.from_list(
    "blue_dk", ["#1E1E1E", "#061020", "#0D3060", "#1A5CB0", "#3A86FF"]
)
DIVG_CMAP = LinearSegmentedColormap.from_list(
    "divg_dk", ["#E63946", "#5A1010", "#1E1E1E", "#0D2040", "#3A86FF"]
)

# Aliases para nombres de estados en GeoJSON (normalizados)
MX_ALIASES = {
    "mexico":                               "estado de mexico",
    "michoacan de ocampo":                  "michoacan",
    "coahuila de zaragoza":                 "coahuila",
    "veracruz de ignacio de la llave":      "veracruz",
    "veracruz-llave":                       "veracruz",
    "queretaro de arteaga":                 "queretaro",
    "distrito federal":                     "ciudad de mexico",
}

# ─── UTILIDADES ───────────────────────────────────────────────────────────────

def normalize(s: str) -> str:
    s = unicodedata.normalize("NFD", s.lower().strip())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


def get_geojson(url: str) -> dict:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_file = CACHE_DIR / url.split("/")[-1]
    if cache_file.exists():
        return json.loads(cache_file.read_text(encoding="utf-8"))
    print(f"    Descargando {cache_file.name}...", end=" ", flush=True)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
    cache_file.write_bytes(data)
    print("OK")
    return json.loads(data)


def get_coords(feat) -> List[np.ndarray]:
    geom = feat.get("geometry")
    if geom is None:
        return []
    result = []
    if geom["type"] == "Polygon":
        result.append(np.array(geom["coordinates"][0])[:, :2])
    elif geom["type"] == "MultiPolygon":
        for poly in geom["coordinates"]:
            result.append(np.array(poly[0])[:, :2])
    return result


def find_mx_key(props: dict, norm_lookup: dict) -> Optional[str]:
    for val in props.values():
        if not isinstance(val, str) or len(val) < 3:
            continue
        n = normalize(val)
        n = MX_ALIASES.get(n, n)
        if n in norm_lookup:
            return norm_lookup[n]
    return None


def find_us_key(props: dict, data_dict: dict) -> Optional[str]:
    name = str(props.get("name") or props.get("NAME") or "")
    if name in data_dict:
        return name
    n = normalize(name)
    for k in data_dict:
        if normalize(k) == n:
            return k
    return None


def setup_ax(bounds: Tuple, dpi: int = 100) -> Tuple:
    fig, ax = plt.subplots(figsize=(19.2, 10.8), dpi=dpi)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(bounds[0], bounds[1])
    ax.set_ylim(bounds[2], bounds[3])
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def add_title_block(ax, title: str, subtitle: str, source: str):
    ax.text(0.02, 0.97, title, transform=ax.transAxes,
            fontsize=17, fontweight="bold", color=GOLD,
            va="top", ha="left", zorder=10)
    ax.text(0.02, 0.91, subtitle, transform=ax.transAxes,
            fontsize=9, color=GRAY, va="top", ha="left", zorder=10)
    ax.text(0.02, 0.03, f"Fuente: {source}", transform=ax.transAxes,
            fontsize=7.5, color=GRAY, va="bottom", ha="left",
            alpha=0.7, zorder=10)


def add_colorbar(fig, ax, cmap, norm, label: str):
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=ax, orientation="vertical",
                        fraction=0.016, pad=0.01, aspect=22, shrink=0.55)
    cbar.ax.yaxis.set_tick_params(color=GRAY)
    cbar.outline.set_edgecolor(BORDER)
    plt.setp(cbar.ax.yaxis.get_ticklabels(), color=GRAY, fontsize=8)
    cbar.set_label(label, color=GRAY, fontsize=8)


def render_choropleth(ax, features, data_dict: dict, cmap, norm, is_mx: bool):
    norm_lookup = {normalize(k): k for k in data_dict}
    patches = []
    colors  = []
    for feat in features:
        props = feat.get("properties") or {}
        key   = find_mx_key(props, norm_lookup) if is_mx else find_us_key(props, data_dict)
        value = data_dict.get(key) if key else None
        color = cmap(norm(value)) if value is not None else NODATA
        for coords in get_coords(feat):
            patches.append(Polygon(coords, closed=True))
            colors.append(color)
    pc = PatchCollection(patches, facecolors=colors,
                         edgecolors=BORDER, linewidths=0.5, zorder=2)
    ax.add_collection(pc)


def render_outlines(ax, features, facecolor: str = "#1A1A1A"):
    patches = []
    for feat in features:
        for coords in get_coords(feat):
            patches.append(Polygon(coords, closed=True))
    pc = PatchCollection(patches, facecolors=facecolor,
                         edgecolors="#2A2A2A", linewidths=0.4, zorder=1)
    ax.add_collection(pc)


def save_fig(fig, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=100, bbox_inches="tight", facecolor=BG, format="png")
    plt.close(fig)
    return path


# ─── BEZIER PARA FLUJOS ───────────────────────────────────────────────────────

def bezier_arc(p0: Tuple, p1: Tuple, arc: float = 7, n: int = 120) -> Tuple:
    mx = (p0[0] + p1[0]) / 2
    my = (p0[1] + p1[1]) / 2 + arc
    t  = np.linspace(0, 1, n)
    x  = (1 - t)**2 * p0[0] + 2 * (1 - t) * t * mx + t**2 * p1[0]
    y  = (1 - t)**2 * p0[1] + 2 * (1 - t) * t * my + t**2 * p1[1]
    return x, y


def _unwrap_result(result: Optional[dict], fallback_data: dict,
                   fallback_periodo: str, fallback_source: str) -> Tuple:
    """Extracts (data, periodo, source, live_tag) from a fetcher result."""
    if result is None:
        return fallback_data, fallback_periodo, fallback_source, " (estimación)"
    n        = len(result.get("states_from_api", []))
    live_tag = f" — {n}/32 en vivo" if result.get("is_live") else " (estimación)"
    return result["data"], result["periodo"], result["source_name"], live_tag


# ─── M01 — Remesas por estado 2024 ───────────────────────────────────────────

def create_M01(features_mx, _, remesas_result: dict = None) -> Path:
    out = OUTPUT_DIR / "M01_remesas_estados.png"
    if out.exists():
        print(f"  [SKIP] M01 ya existe ({out.stat().st_size // 1024} KB)")
        return out

    data, periodo, source, live_tag = _unwrap_result(
        remesas_result, REMESAS_2024, "2024",
        "Banco de México (Banxico), Balanza de Pagos 2024",
    )
    print(f"  M01 Remesas por estado {periodo}...", end=" ", flush=True)

    norm = mcolors.Normalize(vmin=min(data.values()), vmax=max(data.values()))
    fig, ax = setup_ax((-118, -86, 14, 33))
    render_choropleth(ax, features_mx, data, GOLD_CMAP, norm, is_mx=True)
    add_colorbar(fig, ax, GOLD_CMAP, norm, "Millones USD")

    top3 = sorted(data, key=data.get, reverse=True)[:3]
    add_title_block(ax,
        f"Remesas recibidas por estado — {periodo}",
        f"Top 3: {', '.join(top3)}{live_tag}",
        source)

    save_fig(fig, out)
    print(f"OK ({out.stat().st_size // 1024} KB)")
    return out


# ─── M02 — Crecimiento PIB per capita 2010-2023 ───────────────────────────────

def create_M02(features_mx, _, pibe_result: dict = None) -> Path:
    out = OUTPUT_DIR / "M02_pib_crecimiento.png"
    if out.exists():
        print(f"  [SKIP] M02 ya existe ({out.stat().st_size // 1024} KB)")
        return out

    data, periodo, source, live_tag = _unwrap_result(
        pibe_result, PIB_CRECIMIENTO_2010_2023, "2010–2023",
        "INEGI, Producto Interno Bruto por Entidad Federativa (PIBE) 2023",
    )
    print(f"  M02 Crecimiento PIB {periodo}...", end=" ", flush=True)

    vmin    = min(data.values())
    vmax    = max(data.values())
    vcenter = 0.0 if vmin < 0 else vmin + (vmax - vmin) * 0.1
    norm = TwoSlopeNorm(vmin=vmin, vcenter=vcenter, vmax=vmax)
    fig, ax = setup_ax((-118, -86, 14, 33))
    render_choropleth(ax, features_mx, data, DIVG_CMAP, norm, is_mx=True)
    add_colorbar(fig, ax, DIVG_CMAP, norm, "% crecimiento acumulado")

    top_s = max(data, key=data.get)
    bot_s = min(data, key=data.get)
    add_title_block(ax,
        f"Crecimiento PIB estatal — {periodo}",
        f"{top_s} +{data[top_s]:.1f}% vs {bot_s} {data[bot_s]:.1f}%  |  Estados remeseros: crecimiento lento{live_tag}",
        source)

    save_fig(fig, out)
    print(f"OK ({out.stat().st_size // 1024} KB)")
    return out


# ─── M03 — Flujos migratorios MX -> EE.UU. ───────────────────────────────────

def create_M03(features_mx, features_us) -> Path:
    out = OUTPUT_DIR / "M03_flujos_migratorios.png"
    if out.exists():
        print(f"  [SKIP] M03 ya existe ({out.stat().st_size // 1024} KB)")
        return out
    print("  M03 Flujos migratorios MX -> EE.UU....", end=" ", flush=True)

    fig, ax = setup_ax((-135, -60, 13, 55))

    # Fondo: contornos de MX y EE.UU.
    render_outlines(ax, features_mx + features_us)

    # Lineas de flujo con arco Bezier
    for flow in FLUJOS_MIGRATORIOS:
        lat0, lon0, lat1, lon1, peso, _, _ = flow
        lw    = 0.7 + peso * 0.55
        alpha = 0.30 + peso * 0.10
        bx, by = bezier_arc((lon0, lat0), (lon1, lat1), arc=6)
        ax.plot(bx, by, color=GOLD, linewidth=lw, alpha=alpha,
                zorder=3, solid_capstyle="round")

    # Puntos origen (MX) y destino (EE.UU.)
    seen_orig = set()
    seen_dest = set()
    for flow in FLUJOS_MIGRATORIOS:
        lat0, lon0, lat1, lon1, peso, lbl0, lbl1 = flow
        key0, key1 = (lon0, lat0), (lon1, lat1)
        if key0 not in seen_orig:
            seen_orig.add(key0)
            ax.scatter(lon0, lat0, s=60, color=GOLD, zorder=5,
                      edgecolors="#FFFFFF", linewidths=0.6)
            ax.text(lon0 + 0.9, lat0 + 0.7, lbl0, fontsize=7.5, color=GOLD,
                   zorder=6, fontweight="bold")
        if key1 not in seen_dest:
            seen_dest.add(key1)
            ax.scatter(lon1, lat1, s=70, color=BLUE, zorder=5,
                      edgecolors="#FFFFFF", linewidths=0.6)
            ax.text(lon1 + 0.9, lat1 + 0.7, lbl1, fontsize=7.5, color=BLUE,
                   zorder=6, fontweight="bold")

    # Leyenda minima
    ax.scatter([], [], s=60, color=GOLD, label="Origen (Mexico)")
    ax.scatter([], [], s=60, color=BLUE, label="Destino (EE.UU.)")
    leg = ax.legend(loc="lower right", framealpha=0.35, facecolor=BG,
                    edgecolor=BORDER, fontsize=9)
    for t in leg.get_texts():
        t.set_color(GRAY)

    add_title_block(ax,
        "Circuitos de migracion Mexico -> Estados Unidos",
        "Grosor de linea = intensidad del flujo (CONAPO IIM 2020 + Pew 2023)",
        "CONAPO, Indice de Intensidad Migratoria 2020 / Pew Research Center 2023")

    save_fig(fig, out)
    print(f"OK ({out.stat().st_size // 1024} KB)")
    return out


# ─── M04 — Concentracion mexicana en EE.UU. ──────────────────────────────────

def create_M04(_, features_us) -> Path:
    out = OUTPUT_DIR / "M04_riesgo_eeuu.png"
    if out.exists():
        print(f"  [SKIP] M04 ya existe ({out.stat().st_size // 1024} KB)")
        return out
    print("  M04 Concentracion mexicana EE.UU....", end=" ", flush=True)

    norm = mcolors.Normalize(vmin=240, vmax=4200)
    # CONUS: crop a 48 estados contiguos
    fig, ax = setup_ax((-130, -65, 23, 52))
    render_choropleth(ax, features_us, EEUU_CONCENTRACION, GOLD_CMAP, norm, is_mx=False)

    # Dots proporcionales al tamano
    max_c = max(EEUU_CONCENTRACION.values())
    for state, conc in EEUU_CONCENTRACION.items():
        cx, cy = US_CENTROIDS.get(state, (None, None))
        if cx is None:
            continue
        radius = 0.6 + (conc / max_c) ** 0.45 * 2.5
        circle = Circle((cx, cy), radius=radius,
                        color=GOLD, alpha=0.55, zorder=5)
        ax.add_patch(circle)
        if conc >= 780:  # etiqueta solo top 3
            ax.text(cx, cy + radius + 0.3, f"{conc}k",
                   fontsize=8, color=GOLD, ha="center", zorder=6)

    add_colorbar(fig, ax, GOLD_CMAP, norm, "Miles de migrantes mx")
    add_title_block(ax,
        "Concentracion de migrantes mexicanos en EE.UU. — 2023",
        "California (4.2M) y Texas (3.1M) concentran el 70% del total nacional",
        "Pew Research Center, 2023")

    save_fig(fig, out)
    print(f"OK ({out.stat().st_size // 1024} KB)")
    return out


# ─── RUNNER ───────────────────────────────────────────────────────────────────

MAP_FUNCS = {
    "M01": create_M01,
    "M02": create_M02,
    "M03": create_M03,
    "M04": create_M04,
}


def run():
    SEP  = "=" * 65
    SEP2 = "-" * 65

    only = None
    if "--map" in sys.argv:
        idx = sys.argv.index("--map")
        if idx + 1 < len(sys.argv):
            only = sys.argv[idx + 1].upper()

    print("\n" + SEP)
    print("  Map Generator -- matplotlib + GeoJSON")
    print("  Proyecto: 2026-05-remesas-mx")
    print(SEP)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("\n  Cargando GeoJSON...")
    gj_mx = get_geojson(GEOJSON_MX)
    gj_us = get_geojson(GEOJSON_US)
    features_mx = gj_mx.get("features", [])
    features_us = gj_us.get("features", [])
    print(f"  MX: {len(features_mx)} entidades / US: {len(features_us)} estados\n")

    # Fetch live data from APIs only when the PNG doesn't exist yet
    remesas_result = None
    pibe_result    = None

    if _HAS_FETCHER:
        needs_m01 = not (OUTPUT_DIR / "M01_remesas_estados.png").exists()
        needs_m02 = not (OUTPUT_DIR / "M02_pib_crecimiento.png").exists()

        if needs_m01 and (only is None or only == "M01"):
            tok = get_credential_optional("BANXICO_TOKEN")
            if tok:
                print("  Obteniendo remesas por estado de Banxico SIE...")
                remesas_result = fetch_remesas_banxico(tok, REMESAS_2024)

        if needs_m02 and (only is None or only == "M02"):
            tok = get_credential_optional("INEGI_TOKEN")
            if tok:
                print("  Obteniendo PIB por estado de INEGI BISE...")
                pibe_result = fetch_pibe_inegi(tok, PIB_CRECIMIENTO_2010_2023)

    target = {k: v for k, v in MAP_FUNCS.items() if only is None or k == only}
    ok     = []
    errors = []

    extra_kwargs = {
        "M01": {"remesas_result": remesas_result},
        "M02": {"pibe_result":    pibe_result},
    }

    for name, fn in target.items():
        try:
            out = fn(features_mx, features_us, **extra_kwargs.get(name, {}))
            ok.append(f"{name} -> {out.name} ({out.stat().st_size // 1024} KB)")
        except Exception as e:
            import traceback
            print("ERROR")
            traceback.print_exc()
            errors.append((name, str(e)))

    print("\n" + SEP2)
    print(f"  {len(ok)}/{len(target)} mapas generados")
    for line in ok:
        print(f"    OK  {line}")
    if errors:
        print(f"\n  Errores ({len(errors)}):")
        for name, err in errors:
            print(f"    {name}: {err}")
    else:
        print(f"\n  PNGs en: workspace/assets/maps/")
        print("  Siguiente: importar en layer 03_MAPS del proyecto After Effects")
    print(SEP + "\n")


if __name__ == "__main__":
    run()
