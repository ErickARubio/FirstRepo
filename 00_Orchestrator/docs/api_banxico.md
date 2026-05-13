# API Reference — Banxico SIE

**Verificado:** 2026-05-12  
**Estado:** Operacional  
**Token:** `BANXICO_TOKEN` en `.env` (64 chars)

---

## Autenticacion

```
Header: Bmx-Token: {BANXICO_TOKEN}
```

No uses `Authorization: Bearer`. El header exacto es `Bmx-Token`.

---

## Endpoints

### Dato mas reciente de una serie
```
GET https://www.banxico.org.mx/SieAPIRest/service/v1/series/{ID}/datos/oportuno
```

### Rango de fechas
```
GET https://www.banxico.org.mx/SieAPIRest/service/v1/series/{ID}/datos/{INICIO}/{FIN}
Ejemplo: /series/SF43878/datos/2020-01-01/2024-12-31
```

### Multiples series (separadas por coma)
```
GET https://www.banxico.org.mx/SieAPIRest/service/v1/series/SF43878,SF63528/datos/oportuno
```

### Metadatos de una serie
```
GET https://www.banxico.org.mx/SieAPIRest/service/v1/series/{ID}
```

---

## Estructura de respuesta

```json
{
  "bmx": {
    "series": [{
      "idSerie": "SF43878",
      "titulo": "...",
      "fechaInicio": "DD/MM/YYYY",
      "periodicidad": "Mensual|Diaria|Trimestral|Anual",
      "cifra": "Millones de dolares",
      "datos": [
        { "fecha": "DD/MM/YYYY", "dato": "12345.67" }
      ]
    }]
  }
}
```

**Nota:** `dato` viene como string, no numero. Convertir con `float(dato.replace(',',''))`.

---

## Series verificadas y utiles para el proyecto

### Tipo de cambio
| ID | Descripcion | Periodicidad | Ultimo valor |
|----|-------------|-------------|--------------|
| `SF43878` | TIIE 91 dias / Tipo cambio historico | Diaria | 6.81 MXN/USD (2026-05-13) |
| `SF63528` | Tipo de cambio peso-dolar desde 1954 | Diaria | 17.25 MXN/USD |
| `SF60649` | TIIE a 91 dias | Diaria | 6.81% (2026-05-13) |
| `SF60648` | TIIE a 28 dias | Diaria | 6.78% (2026-05-13) |

### Remesas — como encontrar las series
Las series de remesas familiares en Banxico no estan en formato SF/SE accesible directamente via API con nombre legible. Para encontrarlas:

1. Ve al portal SIE: https://www.banxico.org.mx/SieInternet/
2. Navega: Sector Externo → Balanza de Pagos → Remesas familiares
3. Abre el cuadro **CE100** o **CE81**
4. Los IDs de serie aparecen en la URL o al exportar

**Cuadros relevantes identificados:**
- `CA79` — Remesas por entidad federativa (resumen)
- `CE81` — Ingresos por remesas (estructura mensual)
- `CE100` — Distribucion por entidad federativa

**Alternativa confirmada via World Bank** (ver `api_worldbank.md`):
- Remesas totales Mexico 2024: **$67,637 millones USD**
- Remesas / PIB 2024: **3.64%**

### Inflacion y economia
| ID | Descripcion |
|----|-------------|
| `SF46410` | Serie historica tipo cambio controlado |

---

## Formatos de ID de serie

- `SF#####` — Series financieras (tipo cambio, tasas, indices)
- `SE#####` — Series economicas (balanza de pagos, cuentas nacionales)
- `SP#####` — Series de precios

---

## Ejemplo de uso en Python

```python
import requests, os
from dotenv import load_dotenv
load_dotenv()

token = os.environ['BANXICO_TOKEN']

def get_serie(serie_id, tipo='oportuno'):
    r = requests.get(
        f'https://www.banxico.org.mx/SieAPIRest/service/v1/series/{serie_id}/datos/{tipo}',
        headers={'Bmx-Token': token},
        timeout=15
    )
    r.raise_for_status()
    serie = r.json()['bmx']['series'][0]
    datos = serie['datos']
    return {
        'titulo': serie['titulo'],
        'periodicidad': serie['periodicidad'],
        'datos': [(d['fecha'], float(d['dato'].replace(',',''))) 
                  for d in datos if d['dato'] not in ('N/E', '', None)]
    }

# Uso
tc = get_serie('SF43878')
print(f"Tipo cambio: {tc['datos'][-1]}")
```

---

## Recursos
- Documentacion API: https://www.banxico.org.mx/SieAPIRest/
- Portal SIE (busqueda de series): https://www.banxico.org.mx/SieInternet/
- Catalogo de remesas: https://www.banxico.org.mx/publicaciones-y-prensa/balanza-de-pagos/remesas.html
