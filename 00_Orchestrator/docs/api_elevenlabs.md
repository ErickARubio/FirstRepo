# API Reference — ElevenLabs TTS

**Verificado:** 2026-05-12  
**Estado:** Operacional (22 voces disponibles)  
**Credencial:** `ELEVENLABS_API_KEY` en `.env` (51 chars)  
**SDK:** `elevenlabs` v1.x (pip install elevenlabs>=1.0.0)

---

## Autenticacion

```
Header REST: xi-api-key: {ELEVENLABS_API_KEY}
SDK: ElevenLabs(api_key=os.environ['ELEVENLABS_API_KEY'])
```

**Importante:** Los permisos deben estar activados en el panel:
elevenlabs.io → Profile → API Keys → Edit → activar todos los permisos

---

## Modelos de TTS

| Modelo | Descripcion | Uso |
|--------|-------------|-----|
| `eleven_multilingual_v2` | **RECOMENDADO** — 29 idiomas, alta calidad | Produccion |
| `eleven_turbo_v2_5` | Mas rapido, menor latencia | Si hay prisa |
| `eleven_monolingual_v1` | Solo ingles, legacy | No usar |

---

## SDK — Uso correcto (v1.x)

```python
from elevenlabs.client import ElevenLabs
from elevenlabs.types import VoiceSettings
import os
from dotenv import load_dotenv

load_dotenv()
client = ElevenLabs(api_key=os.environ['ELEVENLABS_API_KEY'])

# Listar voces
voices = client.voices.get_all()
for v in voices.voices:
    print(v.voice_id, v.name)

# Generar audio
audio_iter = client.text_to_speech.convert(
    voice_id='voice_id_aqui',
    text='Texto a sintetizar',
    model_id='eleven_multilingual_v2',
    voice_settings=VoiceSettings(
        stability=0.55,
        similarity_boost=0.75,
        style=0.30,
        use_speaker_boost=True,
        speed=0.90,       # 0.7=lento, 1.0=normal, 1.2=rapido
    ),
)
audio_bytes = b''.join(audio_iter)   # CRITICO: es Iterator, no bytes directos
with open('chunk_01.wav', 'wb') as f:
    f.write(audio_bytes)
```

---

## Parametros de VoiceSettings

| Campo | Rango | Recomendado para video-ensayo |
|-------|-------|-------------------------------|
| `stability` | 0.0–1.0 | 0.55 (expresivo pero consistente) |
| `similarity_boost` | 0.0–1.0 | 0.75 (fiel a la voz original) |
| `style` | 0.0–1.0 | 0.30 (ligero, no exagerado) |
| `use_speaker_boost` | bool | True |
| `speed` | 0.7–1.2 | 0.90 (media-lenta, analitica) |

---

## Voces disponibles en la cuenta (verificado 2026-05-12)

22 voces disponibles. Para video-ensayo en espanol buscar voces con:
- Idioma: `es-MX` o `es-419` (latin america)
- Tono: periodistico, autoritativo, no comercial

Buscar via SDK:
```python
voices = client.voices.get_all()
espanol = [v for v in voices.voices 
           if any('es' in str(l).lower() for l in getattr(v, 'labels', {}).values())]
```

---

## Formato del script para TTS

El archivo `02_Script/script_for_elevenlabs.txt` debe seguir este formato:

```
[CHUNK_01 — ACT: Gancho]
Texto del chunk uno. Una idea por oracion.
Los numeros escritos en letras: doscientos cuarenta y tres mil.
Las pausas marcadas con puntos suspensivos...

================================================================================
[CHUNK_02 — ACT: Contexto]
Texto del chunk dos...

================================================================================
FIN DEL SCRIPT
```

Separador: exactamente 80 signos `=`  
Maximo por chunk: 60 segundos (~140 palabras)

---

## Limites del plan gratuito

- 10,000 caracteres / mes
- Script tipico de 6 min: ~900 palabras ≈ ~5,400 caracteres
- Un piloto completo cabe en el plan gratuito

---

## Recursos
- API docs: https://elevenlabs.io/docs/api-reference
- Panel de voces: https://elevenlabs.io/app/voice-library
- Modelos: https://elevenlabs.io/docs/speech-synthesis/models
