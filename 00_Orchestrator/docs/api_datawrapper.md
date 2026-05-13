# API Reference — Datawrapper

**Verificado:** 2026-05-12  
**Estado:** Operacional  
**Cuenta:** erick_-182@hotmail.com  
**Credencial:** `DATAWRAPPER_TOKEN` en `.env` (64 chars)

---

## Autenticacion

```
Header: Authorization: Bearer {DATAWRAPPER_TOKEN}
```

---

## Base URL

```
https://api.datawrapper.de/v3/
```

---

## Tipos de charts disponibles

| ID | Tipo | Uso en el proyecto |
|----|------|--------------------|
| `d3-lines` | Linea | Series de tiempo (remesas por ano) |
| `d3-bars` | Barras verticales | Comparacion por estado |
| `d3-bars-stacked` | Barras apiladas | Composicion (transferencias electronicas vs cash) |
| `d3-area` | Area | Tendencia acumulada |
| `d3-maps-choropleth` | Mapa coroplético | Remesas por entidad federativa |
| `d3-maps-symbols` | Mapa de simbolos | Flujos/puntos |
| `tables` | Tabla | Datos de referencia |

---

## Flujo de trabajo: crear chart y exportar PNG

```python
import requests, os, time
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.environ['DATAWRAPPER_TOKEN']
HEADERS = {'Authorization': f'Bearer {TOKEN}', 'Content-Type': 'application/json'}
BASE = 'https://api.datawrapper.de/v3'


def crear_chart(titulo, tipo, datos_csv):
    """Crea un chart, sube datos y devuelve chart_id."""

    # 1. Crear el chart
    r = requests.post(f'{BASE}/charts',
        headers=HEADERS,
        json={'title': titulo, 'type': tipo}
    )
    chart_id = r.json()['id']

    # 2. Subir datos CSV
    requests.put(f'{BASE}/charts/{chart_id}/data',
        headers={**HEADERS, 'Content-Type': 'text/csv'},
        data=datos_csv.encode('utf-8')
    )

    # 3. Publicar
    requests.post(f'{BASE}/charts/{chart_id}/publish', headers=HEADERS)

    return chart_id


def exportar_png(chart_id, output_path, width=1920, height=1080):
    """Exporta chart publicado como PNG."""
    time.sleep(2)   # esperar a que se publique
    r = requests.get(
        f'{BASE}/charts/{chart_id}/export/png',
        headers=HEADERS,
        params={'width': width, 'height': height, 'plain': False},
    )
    if r.status_code == 200:
        with open(output_path, 'wb') as f:
            f.write(r.content)
        return output_path
    raise Exception(f'Export failed: {r.status_code} {r.text[:200]}')


# --- Ejemplo: grafica de remesas por ano ---

csv_remesas = """Year,Remesas (millones USD)
2020,43977
2021,55067
2022,61457
2023,66237
2024,67637"""

chart_id = crear_chart(
    titulo='Remesas a Mexico 2020-2024',
    tipo='d3-lines',
    datos_csv=csv_remesas,
)
print(f'Chart creado: {chart_id}')
exportar_png(chart_id, '03_Assets/charts/remesas_serie.png')
```

---

## Endpoints clave

| Metodo | Endpoint | Descripcion |
|--------|----------|-------------|
| GET | `/v3/me` | Info de cuenta |
| GET | `/v3/charts` | Listar charts |
| POST | `/v3/charts` | Crear chart |
| PUT | `/v3/charts/{id}/data` | Subir datos CSV |
| POST | `/v3/charts/{id}/publish` | Publicar |
| GET | `/v3/charts/{id}/export/png` | Exportar PNG |
| DELETE | `/v3/charts/{id}` | Eliminar |

---

## Mapa coropletico de Mexico por estado

Para el mapa de remesas por entidad federativa:

```python
# tipo: 'd3-maps-choropleth'
# El CSV debe tener columna con nombre del estado + columna de valor
csv_mapa = """State,Remesas (millones USD)
Michoacan,1249
Guanajuato,1248
Jalisco,1193
Ciudad de Mexico,1153
Guerrero,820"""

chart_id = crear_chart(
    'Remesas por estado Q1 2026',
    'd3-maps-choropleth',
    csv_mapa
)
```

Datawrapper reconoce los nombres de estados en espanol automaticamente.

---

## Exportar para After Effects

Los PNG exportados van directamente a `03_Assets/charts/` y se importan en AE via `ae_script.jsx`.

Resolucion recomendada: `width=1920, height=1080`

---

## Recursos
- API Reference: https://developer.datawrapper.de/reference
- Getting started: https://developer.datawrapper.de/docs/getting-started
- Tipos de chart: https://developer.datawrapper.de/docs/chart-types
