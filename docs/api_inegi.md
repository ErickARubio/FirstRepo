# API Reference — INEGI Indicadores

**Verificado:** 2026-05-12  
**Estado:** Operacional  
**Credencial:** `INEGI_TOKEN` en `.env` (36 chars)  
**Token en URL** (no en header)

---

## URL exacta (CRITICO)

```
https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/{ID}/es/00/false/BISE/2.0/{TOKEN}?type=json
```

Parametros que NO cambian:
- `es` — idioma
- `00` — area geografica nacional (no 0700, no otro)
- `false` — sin unidades dobles
- `BISE` — banco correcto (NO usar `BIE` — devuelve 400)
- `2.0` — version del API
- `?type=json` — formato JSON (obligatorio)

---

## Estructura de respuesta

```json
{
  "Series": [{
    "INDICADOR": "1002000001",
    "OBSERVATIONS": [
      {
        "TIME_PERIOD": "1910",
        "OBS_VALUE": "15160369.00000000000000000000",
        "OBS_STATUS": "3",
        "COBER_GEO": "0"
      }
    ]
  }]
}
```

`OBS_VALUE` viene como string con decimales. Convertir: `float(obs['OBS_VALUE'])`

---

## Indicadores verificados

### Verificado con llamada real

| ID | Descripcion | Ultimo dato |
|----|-------------|-------------|
| `1002000001` | Poblacion total | 15,160,369 (1910) |

### Indicadores candidatos para remesas (pendiente verificacion)

| ID | Descripcion probable |
|----|---------------------|
| `444319` | Remesas familiares (por verificar) |
| `6207019526` | PIB a precios de mercado (por verificar con BISE) |

Para verificar un indicador:
```bash
python -c "
from dotenv import load_dotenv; load_dotenv('.env'); import os, requests
token = os.environ['INEGI_TOKEN']
r = requests.get(f'https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/TU_ID/es/00/false/BISE/2.0/{token}?type=json', timeout=15)
print(r.status_code, r.text[:300])
"
```

---

## Como encontrar IDs de indicadores

1. Ve a https://www.inegi.org.mx/app/indicadores/
2. Busca el indicador (ej: "remesas")
3. Abre el indicador → la URL contiene el ID

O usa el catalogo de indicadores:
```
https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATORS/es/BISE/2.0/{TOKEN}?type=json
```

---

## Indicadores relevantes para el proyecto (por buscar)

- Remesas familiares recibidas
- Poblacion en estados con alta emigracion (Michoacan, Guanajuato, Jalisco)
- PIB por entidad federativa
- Indice de marginacion
- Hogares que reciben remesas (ENIGH)

**Fuente alternativa para remesas:** World Bank API — ya verificada, ver `api_worldbank.md`

---

## Ejemplo de uso en Python

```python
import requests, os
from dotenv import load_dotenv
load_dotenv()

def get_inegi(indicador_id):
    token = os.environ['INEGI_TOKEN']
    url = (
        f'https://www.inegi.org.mx/app/api/indicadores/desarrolladores/'
        f'jsonxml/INDICATOR/{indicador_id}/es/00/false/BISE/2.0/{token}?type=json'
    )
    r = requests.get(url, timeout=15)
    r.raise_for_status()
    data = r.json()
    obs = data['Series'][0]['OBSERVATIONS']
    return [
        {'periodo': o['TIME_PERIOD'], 'valor': float(o['OBS_VALUE'])}
        for o in obs if o.get('OBS_VALUE')
    ]

# Uso
pob = get_inegi('1002000001')
print(f"Poblacion Mexico: {pob[-1]}")
```

---

## Recursos
- Portal de indicadores: https://www.inegi.org.mx/app/indicadores/
- Documentacion API: https://www.inegi.org.mx/servicios/api_indicadores.html
- Solicitar token: https://www.inegi.org.mx/app/api/indicadores/desarrolladores/
