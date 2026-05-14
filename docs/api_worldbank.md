# API Reference — World Bank Open Data

**Verificado:** 2026-05-12  
**Estado:** Operacional  
**Autenticacion:** Ninguna — acceso libre, sin API key

---

## Endpoint base

```
https://api.worldbank.org/v2/country/{PAIS}/indicator/{INDICADOR}
```

Parametros utiles:
- `format=json` — respuesta en JSON (default es XML)
- `mrv=N` — "most recent values", los N ultimos datos
- `date=2010:2024` — rango de anos

---

## Estructura de respuesta

```json
[
  { "page": 1, "pages": 1, "total": 5 },
  [
    { "date": "2024", "value": 67637913797.0, "country": {"id": "MX"} },
    { "date": "2023", "value": 66237847600.0 }
  ]
]
```

El indice `[1]` contiene los datos. `[0]` es metadata de paginacion.

---

## Indicadores verificados para el proyecto

### Remesas Mexico
| Indicador | Descripcion | Ultimo valor verificado |
|-----------|-------------|------------------------|
| `BX.TRF.PWKR.CD.DT` | Remesas recibidas — total USD corrientes | $67,637,913,797 (2024) |
| `BX.TRF.PWKR.DT.GD.ZS` | Remesas como % del PIB | 3.64% (2024) |

**Serie historica 2020-2024 (BX.TRF.PWKR.CD.DT):**
| Ano | Monto (USD) | Variacion |
|-----|-------------|-----------|
| 2024 | $67,637M | — |
| 2023 | $66,237M | +2.1% |
| 2022 | $61,457M | +9.0% |
| 2021 | $55,067M | +24.1% |
| 2020 | $43,977M | — |

Crecimiento 2020→2024: **+54%**

### Economia Mexico
| Indicador | Descripcion | Ultimo valor |
|-----------|-------------|--------------|
| `NY.GDP.MKTP.CD` | PIB Mexico — USD corrientes | $1,856,365M (2024) |
| `FP.CPI.TOTL.ZG` | Inflacion % anual | 4.72% (2024) |
| `SM.POP.NETM` | Migracion neta | -108,037 personas (2025) |

### Comparativas regionales
```
Sustituir MX por el codigo ISO del pais:
US = Estados Unidos
GT = Guatemala  
SV = El Salvador
HN = Honduras
CO = Colombia
```

---

## Ejemplo de uso en Python

```python
import requests

def get_worldbank(pais, indicador, anos=5):
    r = requests.get(
        f'https://api.worldbank.org/v2/country/{pais}/indicator/{indicador}',
        params={'format': 'json', 'mrv': anos},
        timeout=15
    )
    r.raise_for_status()
    data = r.json()
    if not data[1]:
        return []
    return [
        {'ano': d['date'], 'valor': d['value']}
        for d in data[1] if d.get('value') is not None
    ]

# Uso
remesas = get_worldbank('MX', 'BX.TRF.PWKR.CD.DT', anos=10)
for r in remesas:
    print(f"{r['ano']}: ${r['valor']/1e9:.1f}B USD")
```

---

## Recursos
- Explorador de indicadores: https://data.worldbank.org/indicator
- API docs: https://datahelpdesk.worldbank.org/knowledgebase/articles/889392
- Busqueda de indicadores: https://api.worldbank.org/v2/indicator?format=json&q=remittances
