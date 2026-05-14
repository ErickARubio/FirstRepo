# Proyecto 01 — Video-Ensayos Cartográficos

Sistema de producción automatizada de video-ensayos económicos con datos cartográficos para YouTube.

## Qué hace

Toma un tema económico (ej. remesas en México) y produce todos los assets del video: investigación con fuentes verificadas, guion, mapas, imágenes IA, narración de voz y plan de animación.

## Arquitectura

```
main.py                  # Entry point y pre-flight check
prompts/orchestrator.md  # Instrucciones del Orquestador Maestro (leer en Claude Code)
│
├── agents/              # 5 agentes especializados
│   ├── researcher.py        # A1 — Investigación y fuentes
│   ├── scriptwriter.py      # A2 — Guion narrativo
│   ├── visual_director.py   # A3 — Mapas y gráficos
│   ├── voice_director.py    # A4 — Script ElevenLabs
│   └── animation_director.py# A5 — Storyboard y Remotion
│
├── core/                # Base del sistema
│   ├── base_agent.py        # Clase padre de los agentes
│   ├── state_manager.py     # Checkpoints del pipeline
│   └── config.py            # Configuración global
│
├── tools/               # Herramientas de producción
│   ├── data_fetcher.py      # INEGI, Banxico, World Bank
│   ├── map_generator.py     # Generación de mapas con matplotlib
│   ├── voice_gen.py         # ElevenLabs TTS
│   └── ai_asset_generator.py# Google Imagen 3
│
├── prompts/             # Prompts de cada agente
└── docs/                # Documentación de APIs
```

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env    # completar con tus API keys
python main.py          # verifica dependencias y credenciales
```

## Credenciales requeridas (.env)

| Variable | API | Uso |
|---|---|---|
| `ELEVENLABS_API_KEY` | ElevenLabs | Narración de voz |
| `GOOGLE_AI_API_KEY` | Google AI Studio | Gemini + Imagen 3 |
| `BANXICO_TOKEN` | Banxico SIE | Datos económicos MX |
| `INEGI_TOKEN` | INEGI BISE | Indicadores nacionales MX |
| `DATAWRAPPER_TOKEN` | Datawrapper | Gráficos publicables (opcional) |

## Uso

```bash
# Verificar sistema
python main.py

# Ejecutar pipeline completo (modo Claude Code)
/read prompts/orchestrator.md

# Ejecutar pipeline por código
python main.py --run

# Ver checkpoints del proyecto activo
python main.py --status
```

## Flujo de producción

```
Tema del usuario
    → A1 Investigador  (tesis + fuentes)
    → A2 Guionista     (narrativa)
    → A3 Visual        (mapas + imágenes IA)
    → A4 Voz           (script ElevenLabs)
    → A5 Animación     (storyboard + Remotion)
```

Cada fase requiere aprobación explícita antes de continuar.
