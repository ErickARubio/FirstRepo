#!/usr/bin/env python3
"""
setup_new_project.py — Crea un nuevo proyecto de video-ensayo cartográfico.

Genera la estructura profesional completa con todos los archivos base listos
para empezar a producir sin modificar el proyecto anterior.

Uso:
    python setup_new_project.py Proyecto_02_Inflacion
    python setup_new_project.py Proyecto_03_Desigualdad --parent C:/Users/erick/Projects
    python setup_new_project.py Proyecto_04_TLCAN --dry-run
"""

import sys
import argparse
import json
import textwrap
from pathlib import Path
from datetime import date


# ─── ESTRUCTURA DE CARPETAS ────────────────────────────────────────────────────

FOLDERS = [
    "core",
    "agents",
    "tools",
    "prompts",
    "prompts/templates",
    "workspace/research",
    "workspace/script",
    "workspace/assets/maps",
    "workspace/assets/charts",
    "workspace/assets/images",
    "workspace/assets/audio",
    "workspace/cache",
    "animation/src/compositions/scenes",
    "docs",
]


# ─── CONTENIDO DE ARCHIVOS BASE ────────────────────────────────────────────────

def _content_core_init():
    return "from .base_agent import BaseAgent\nfrom .state_manager import StateManager\n\n__all__ = ['BaseAgent', 'StateManager']\n"


def _content_base_agent():
    return textwrap.dedent("""\
    \"\"\"
    Abstract base class for all production agents.
    \"\"\"
    from abc import ABC, abstractmethod
    from pathlib import Path
    import json
    from .state_manager import StateManager


    class BaseAgent(ABC):

        def __init__(self, project_root: Path):
            self.root      = Path(project_root)
            self.workspace = self.root / "workspace"
            self.prompts   = self.root / "prompts"
            self.mapping   = self._load_mapping()
            self.state     = StateManager(self.root)

        @abstractmethod
        def run(self) -> dict:
            \"\"\"Execute the agent. Returns metadata dict on success.\"\"\"
            ...

        def checkpoint_name(self) -> str:
            return self.__class__.__name__.lower()

        def done(self, meta: dict | None = None) -> dict:
            \"\"\"Mark this agent's checkpoint as approved.\"\"\"
            self.state.mark_done(self.checkpoint_name(), meta or {})
            return meta or {}

        def load_prompt(self, filename: str) -> str:
            return (self.prompts / filename).read_text(encoding="utf-8")

        def dataset_for(self, visual_id: str) -> dict | None:
            for ds in self.mapping.get("datasets", []):
                if ds.get("visual_destination") == visual_id:
                    return ds
            return None

        def _load_mapping(self) -> dict:
            path = self.root / "mapping_rules.json"
            if path.exists():
                return json.loads(path.read_text(encoding="utf-8"))
            return {}
    """)


def _content_state_manager():
    return textwrap.dedent("""\
    \"\"\"
    Checkpoint state manager — persisted in workspace/state.json.
    \"\"\"
    import json
    from pathlib import Path
    from datetime import datetime, timezone


    class StateManager:

        CHECKPOINTS = ["research", "script", "visuals", "voice", "animation"]

        def __init__(self, project_root: Path):
            self._path  = Path(project_root) / "workspace" / "state.json"
            self._state = self._load()

        def mark_done(self, checkpoint: str, meta: dict | None = None) -> None:
            self._state.setdefault("checkpoints", {})[checkpoint] = {
                "status":    "approved",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                **(meta or {}),
            }
            self._save()

        def is_done(self, checkpoint: str) -> bool:
            return (
                self._state.get("checkpoints", {})
                .get(checkpoint, {})
                .get("status") == "approved"
            )

        def status(self) -> dict:
            return self._state.get("checkpoints", {})

        def reset(self) -> None:
            self._state["checkpoints"] = {}
            self._save()

        def summary(self) -> str:
            lines = [f"  Project: {self._state.get('project', '?')}"]
            for cp in self.CHECKPOINTS:
                info   = self._state.get("checkpoints", {}).get(cp, {})
                status = info.get("status", "pending")
                mark   = "[OK]" if status == "approved" else "[ ]"
                lines.append(f"  {mark}  {cp}")
            return "\\n".join(lines)

        def _load(self) -> dict:
            if self._path.exists():
                return json.loads(self._path.read_text(encoding="utf-8"))
            return {"project": self._path.parent.parent.name, "checkpoints": {}}

        def _save(self) -> None:
            self._path.parent.mkdir(parents=True, exist_ok=True)
            self._path.write_text(
                json.dumps(self._state, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
    """)


def _content_config():
    return textwrap.dedent("""\
    \"\"\"
    Centralised credential management — reads from .env at project root.
    \"\"\"
    import os
    from pathlib import Path

    _ROOT     = Path(__file__).resolve().parent.parent
    _ENV_FILE = _ROOT / ".env"

    try:
        from dotenv import load_dotenv
        load_dotenv(_ENV_FILE)
    except ImportError:
        pass


    class MissingCredentialError(Exception):
        pass


    REGISTRY = {
        "ELEVENLABS_API_KEY":  {"service": "ElevenLabs",        "required": True},
        "GOOGLE_API_KEY":      {"service": "Google AI Studio",   "required": True},
        "BANXICO_TOKEN":       {"service": "Banxico SIE",        "required": True},
        "INEGI_TOKEN":         {"service": "INEGI BISE",         "required": True},
        "DATAWRAPPER_TOKEN":   {"service": "Datawrapper",        "required": False},
        "PEXELS_API_KEY":      {"service": "Pexels",             "required": False},
        "UNSPLASH_ACCESS_KEY": {"service": "Unsplash",           "required": False},
        "PIXABAY_API_KEY":     {"service": "Pixabay",            "required": False},
    }


    def get(name: str) -> str:
        value = os.environ.get(name, "").strip()
        if not value:
            meta = REGISTRY.get(name, {})
            raise MissingCredentialError(
                f"Credencial faltante: {name} ({meta.get('service', '?')})\\n"
                f"Agregar en .env:  {name}=tu_clave_aqui"
            )
        return value


    def get_optional(name: str) -> str | None:
        try:
            return get(name)
        except MissingCredentialError:
            return None


    def check_all() -> None:
        print("\\n--- Credenciales del proyecto ---")
        for name, meta in REGISTRY.items():
            val = os.environ.get(name, "").strip()
            tag = "[REQUERIDA]" if meta["required"] else "[opcional]"
            status = "OK" if val else "FALTA"
            print(f"  [{status}]  {meta['service']:<22}  {name}  {tag}")
        print()
    """)


def _content_agent_stub(class_name: str, checkpoint: str, prompt_file: str) -> str:
    return textwrap.dedent(f"""\
    \"\"\"
    {class_name} — wrapper Python para el agente de producción.
    La lógica de prompts vive en prompts/{prompt_file}.
    \"\"\"
    from pathlib import Path
    from core.base_agent import BaseAgent


    class {class_name}(BaseAgent):

        def checkpoint_name(self) -> str:
            return "{checkpoint}"

        def run(self) -> dict:
            prompt = self.load_prompt("{prompt_file}")
            # TODO: invocar Claude API con el prompt y los inputs correspondientes
            # Consultar mapping_rules.json para saber qué datasets/APIs usar:
            #   datasets = self.mapping.get("datasets", [])
            raise NotImplementedError("{class_name}.run() no implementado aún")
    """)


def _content_tools_init():
    return textwrap.dedent("""\
    from .data_fetcher import fetch_remesas_banxico, fetch_pibe_inegi
    from .map_generator import run as generate_maps

    __all__ = ["fetch_remesas_banxico", "fetch_pibe_inegi", "generate_maps"]
    """)


def _content_data_fetcher_stub():
    return textwrap.dedent("""\
    \"\"\"
    Fetches live economic data from Banxico SIE and INEGI BISE.
    Reads series IDs from mapping_rules.json — no hardcoded IDs here.
    Falls back to caller-supplied dicts if any API call fails.
    \"\"\"
    # TODO: copy implementation from Proyecto_01_Remesas/00_Orchestrator/tools/data_fetcher.py
    # and update imports to use core.config instead of tools.config.

    def fetch_remesas_banxico(banxico_token: str, fallback: dict) -> dict:
        raise NotImplementedError("Copy from Proyecto_01_Remesas")


    def fetch_pibe_inegi(inegi_token: str, fallback: dict, base_year: str = "2010") -> dict:
        raise NotImplementedError("Copy from Proyecto_01_Remesas")
    """)


def _content_map_generator_stub():
    return textwrap.dedent("""\
    \"\"\"
    Generates map PNGs using matplotlib + GeoJSON.
    Output: workspace/assets/maps/M01_*.png (1920x1080)
    \"\"\"
    # TODO: copy implementation from Proyecto_01_Remesas/00_Orchestrator/tools/map_generator.py
    # Update CACHE_DIR to point to workspace/cache/

    def run(maps: list[str] | None = None) -> None:
        raise NotImplementedError("Copy from Proyecto_01_Remesas")
    """)


def _content_chart_generator_stub():
    return textwrap.dedent("""\
    \"\"\"
    Creates and publishes charts to Datawrapper.
    Reads chart specs from mapping_rules.json datasets[].datawrapper_type.
    Output: workspace/assets/charts/G01_*.png
    \"\"\"
    import json
    from pathlib import Path


    def publish_chart(dataset_spec: dict, csv_data: str, dw_token: str) -> str:
        \"\"\"
        Creates a Datawrapper chart from a dataset spec and CSV data.
        Returns the chart URL.
        \"\"\"
        # TODO: implement using Datawrapper API v3
        # POST /v3/charts → PUT /v3/charts/{id}/data → POST /v3/charts/{id}/publish
        raise NotImplementedError("chart_generator not implemented yet")


    def run(mapping: dict, dw_token: str) -> None:
        for ds in mapping.get("datasets", []):
            if ds.get("datawrapper_type"):
                print(f"  [{ds['id']}] {ds['name']} → {ds['datawrapper_type']}")
                # publish_chart(ds, csv_data, dw_token)
    """)


def _content_voice_gen_stub():
    return textwrap.dedent("""\
    \"\"\"
    Synthesises narration audio using ElevenLabs.
    Input:  workspace/script/script_for_elevenlabs.txt (chunked)
    Output: workspace/assets/audio/chunk_NN.mp3
    \"\"\"
    # TODO: copy implementation from Proyecto_01_Remesas/00_Orchestrator/tools/voice_gen.py

    def run(script_path: str, output_dir: str, api_key: str) -> list[str]:
        raise NotImplementedError("Copy from Proyecto_01_Remesas")
    """)


def _content_ai_asset_stub():
    return textwrap.dedent("""\
    \"\"\"
    Generates editorial images using Google Imagen 3 (via google-genai).
    Output: workspace/assets/images/I01_*.png
    \"\"\"
    # TODO: copy implementation from Proyecto_01_Remesas/00_Orchestrator/tools/ai_asset_generator.py

    def run(prompts: list[dict], output_dir: str, api_key: str) -> list[str]:
        raise NotImplementedError("Copy from Proyecto_01_Remesas")
    """)


def _content_main(project_name: str) -> str:
    return textwrap.dedent(f"""\
    \"\"\"
    main.py — Pre-flight check y entry point del pipeline.

    Uso:
        python main.py           # verifica dependencias y credenciales
        python main.py --run     # ejecuta el pipeline completo
    \"\"\"
    import sys
    import argparse
    from pathlib import Path

    ROOT = Path(__file__).resolve().parent

    sys.path.insert(0, str(ROOT))

    from core.config import check_all
    from core.state_manager import StateManager


    def preflight():
        print("\\n{'=' * 60}")
        print(f"  {project_name}")
        print(f"{'=' * 60}")
        check_all()
        sm = StateManager(ROOT)
        print("\\n--- Estado de checkpoints ---")
        print(sm.summary())
        print()


    def run_pipeline():
        from agents.researcher       import Researcher
        from agents.scriptwriter     import Scriptwriter
        from agents.visual_director  import VisualDirector
        from agents.voice_director   import VoiceDirector
        from agents.animation_director import AnimationDirector

        sm = StateManager(ROOT)

        agents = [
            Researcher(ROOT),
            Scriptwriter(ROOT),
            VisualDirector(ROOT),
            VoiceDirector(ROOT),
            AnimationDirector(ROOT),
        ]

        for agent in agents:
            cp = agent.checkpoint_name()
            if sm.is_done(cp):
                print(f"  [SKIP] {{cp}} ya aprobado")
                continue
            print(f"  [RUN ] {{cp}}")
            agent.run()


    if __name__ == "__main__":
        parser = argparse.ArgumentParser()
        parser.add_argument("--run", action="store_true", help="Ejecutar pipeline")
        args = parser.parse_args()

        preflight()
        if args.run:
            run_pipeline()
    """)


def _content_mapping_rules(slug: str, title: str) -> str:
    data = {
        "project": {
            "slug":                    slug,
            "title":                   title,
            "language":                "es-MX",
            "target_duration_seconds": 390,
            "created":                 str(date.today()),
            "entry_point":             "main.py",
        },
        "visual_standard": {
            "palette":    "editorial_nordico",
            "resolution": [1920, 1080],
            "fps":        30,
            "fonts": {
                "display": "Playfair Display",
                "body":    "Source Sans Pro",
                "mono":    "Source Code Pro",
            },
            "colors": {
                "bg_primary":    "#FAFAF8",
                "bg_secondary":  "#F0EDE6",
                "text_primary":  "#1A1A1A",
                "text_secondary":"#5A5A5A",
                "accent_1":      "#C41E3A",
                "accent_2":      "#2B4C8C",
            },
        },
        "datasets": [
            {
                "id":                "D01",
                "name":              "COMPLETAR — dataset principal",
                "institution":       "COMPLETAR — Banxico / INEGI / World Bank / ENIGH",
                "api":               "COMPLETAR — banxico_sie / inegi_bise / world_bank / manual_download",
                "series_ids":        "COMPLETAR — ej: SE55093",
                "granularity":       "COMPLETAR — nacional / estatal / municipal",
                "frequency":         "COMPLETAR — anual / trimestral / mensual",
                "unit":              "COMPLETAR — ej: millones USD",
                "visual_destination":"M01",
                "datawrapper_type":  "d3-maps-choropleth",
                "basemap":           "mexico-estados",
                "csv_schema": {
                    "columns": ["COMPLETAR_col1", "COMPLETAR_col2"],
                    "types":   ["string", "float"],
                    "example": ["Estado ejemplo", 1234.5],
                },
                "palette_config": {
                    "variable":           "COMPLETAR_col2",
                    "scale":              "sequential",
                    "range_min":          0,
                    "range_max":          1000,
                    "datawrapper_palette":"OrRd",
                },
            }
        ],
        "assets": {
            "maps":   ["M01", "M02"],
            "charts": ["G01", "G02", "G03"],
            "images": ["I01", "I02"],
        },
        "apis_required": ["elevenlabs", "google_ai"],
        "apis_optional": ["banxico", "inegi", "datawrapper", "pexels", "unsplash"],
        "agent_sequence": [
            {"step": 1, "agent": "researcher",         "checkpoint": "research"},
            {"step": 2, "agent": "scriptwriter",        "checkpoint": "script"},
            {"step": 3, "agent": "visual_director",     "checkpoint": "visuals"},
            {"step": 4, "agent": "voice_director",      "checkpoint": "voice"},
            {"step": 5, "agent": "animation_director",  "checkpoint": "animation"},
        ],
    }
    return json.dumps(data, ensure_ascii=False, indent=2)


def _content_requirements() -> str:
    return (
        "python-dotenv>=1.0.0\n"
        "requests>=2.31.0\n"
        "elevenlabs>=1.0.0\n"
        "google-genai>=1.0.0\n"
        "pillow>=10.0.0\n"
        "numpy>=1.24.0\n"
        "pandas>=2.0.0\n"
        "matplotlib>=3.8.0\n"
    )


def _content_env_example() -> str:
    return (
        "# Credenciales del proyecto\n"
        "# Copia este archivo a .env y llena tus claves\n\n"
        "# Requeridas\n"
        "ELEVENLABS_API_KEY=\n"
        "GOOGLE_API_KEY=\n"
        "BANXICO_TOKEN=\n"
        "INEGI_TOKEN=\n\n"
        "# Opcionales\n"
        "DATAWRAPPER_TOKEN=\n"
        "PEXELS_API_KEY=\n"
        "UNSPLASH_ACCESS_KEY=\n"
        "PIXABAY_API_KEY=\n"
    )


def _content_gitignore() -> str:
    return (
        ".env\n"
        "__pycache__/\n"
        "*.pyc\n"
        "workspace/cache/\n"
        "workspace/assets/\n"
        "node_modules/\n"
        "animation/out/\n"
    )


def _content_remotion_root(project_name: str) -> str:
    return textwrap.dedent(f"""\
    import {{ Composition }} from 'remotion';
    import {{ MainVideo }} from './compositions/MainVideo';

    export const RemotionRoot: React.FC = () => {{
      return (
        <>
          <Composition
            id="MainVideo"
            component={{MainVideo}}
            durationInFrames={{30 * 390}}
            fps={{30}}
            width={{1920}}
            height={{1080}}
          />
        </>
      );
    }};
    """)


def _content_remotion_constants() -> str:
    return textwrap.dedent("""\
    export const FPS    = 30;
    export const WIDTH  = 1920;
    export const HEIGHT = 1080;

    export const PALETTE = {
      bgPrimary:    '#FAFAF8',
      bgSecondary:  '#F0EDE6',
      textPrimary:  '#1A1A1A',
      textSecondary:'#5A5A5A',
      accent1:      '#C41E3A',
      accent2:      '#2B4C8C',
    };

    export const FONTS = {
      display: 'Playfair Display',
      body:    'Source Sans Pro',
      mono:    'Source Code Pro',
    };

    /** Convierte segundos a frames */
    export const s = (sec: number) => sec * FPS;
    """)


def _content_remotion_main_video() -> str:
    return textwrap.dedent("""\
    import { AbsoluteFill } from 'remotion';

    // TODO: importar escenas generadas por AnimationDirector
    // import { SceneMap } from './scenes/SceneMap';

    export const MainVideo: React.FC = () => {
      return (
        <AbsoluteFill>
          {/* Las secuencias se generan automáticamente por el Agente A5 */}
        </AbsoluteFill>
      );
    };
    """)


def _content_package_json(project_slug: str) -> str:
    data = {
        "name":    project_slug.lower().replace("_", "-"),
        "version": "0.1.0",
        "scripts": {
            "start":  "npx remotion preview src/Root.tsx",
            "render": "npx remotion render src/Root.tsx MainVideo ../workspace/assets/video_final.mp4 --codec=h264",
            "build":  "npx remotion render src/Root.tsx MainVideo out/video.mp4",
        },
        "dependencies": {
            "remotion":        "^4.0.0",
            "@remotion/core":  "^4.0.0",
            "@remotion/cli":   "^4.0.0",
            "@remotion/easing":"^4.0.0",
        },
        "devDependencies": {
            "typescript":  "^5.0.0",
            "@types/react":"^18.0.0",
        },
    }
    return json.dumps(data, indent=2)


# ─── PROMPT STUBS ──────────────────────────────────────────────────────────────

def _prompt_stub(agent_role: str, phase_count: int) -> str:
    return textwrap.dedent(f"""\
    # AGENTE — {agent_role.upper()}

    ## ROL
    [Describir el rol específico de este agente para este proyecto]

    ## INPUT REQUERIDO
    [Listar los archivos/datos de entrada necesarios]

    {"".join(f"## FASE {i}: [NOMBRE DE LA FASE]{chr(10)}[Describir la tarea de esta fase]{chr(10)}{chr(10)}" for i in range(1, phase_count + 1))}
    ## OUTPUT FINAL
    [Listar los archivos que produce este agente]
    """)


# ─── BUILDER ───────────────────────────────────────────────────────────────────

FILES = {}  # populated in build_file_map()


def build_file_map(project_name: str, project_dir: Path) -> dict[str, str]:
    slug  = project_name.lower().replace(" ", "_")
    title = project_name.replace("_", " ").replace("Proyecto ", "")

    return {
        # ── core ──────────────────────────────────────────────────────────
        "core/__init__.py":       _content_core_init(),
        "core/base_agent.py":     _content_base_agent(),
        "core/state_manager.py":  _content_state_manager(),
        "core/config.py":         _content_config(),

        # ── agents ────────────────────────────────────────────────────────
        "agents/__init__.py": (
            "from .researcher         import Researcher\n"
            "from .scriptwriter       import Scriptwriter\n"
            "from .visual_director    import VisualDirector\n"
            "from .voice_director     import VoiceDirector\n"
            "from .animation_director import AnimationDirector\n"
        ),
        "agents/researcher.py":
            _content_agent_stub("Researcher",        "research",  "researcher.md"),
        "agents/scriptwriter.py":
            _content_agent_stub("Scriptwriter",       "script",    "scriptwriter.md"),
        "agents/visual_director.py":
            _content_agent_stub("VisualDirector",     "visuals",   "visual_director.md"),
        "agents/voice_director.py":
            _content_agent_stub("VoiceDirector",      "voice",     "voice_director.md"),
        "agents/animation_director.py":
            _content_agent_stub("AnimationDirector",  "animation", "animation_director.md"),

        # ── tools ─────────────────────────────────────────────────────────
        "tools/__init__.py":           _content_tools_init(),
        "tools/data_fetcher.py":       _content_data_fetcher_stub(),
        "tools/map_generator.py":      _content_map_generator_stub(),
        "tools/chart_generator.py":    _content_chart_generator_stub(),
        "tools/voice_gen.py":          _content_voice_gen_stub(),
        "tools/ai_asset_generator.py": _content_ai_asset_stub(),

        # ── prompts (stubs — copiar de Proyecto_01 y adaptar) ─────────────
        "prompts/researcher.md":        _prompt_stub("Investigador Económico", 5),
        "prompts/scriptwriter.md":      _prompt_stub("Guionista de Video-Ensayo", 3),
        "prompts/visual_director.md":   _prompt_stub("Director Visual y de Arte", 4),
        "prompts/voice_director.md":    _prompt_stub("Director de Voz y Audio", 5),
        "prompts/animation_director.md":_prompt_stub("Director Técnico de Motion Graphics", 5),

        # ── animation (Remotion) ──────────────────────────────────────────
        "animation/src/Root.tsx":
            _content_remotion_root(project_name),
        "animation/src/constants.ts":
            _content_remotion_constants(),
        "animation/src/compositions/MainVideo.tsx":
            _content_remotion_main_video(),
        "animation/package.json":
            _content_package_json(slug),

        # ── root ──────────────────────────────────────────────────────────
        "main.py":           _content_main(project_name),
        "mapping_rules.json":_content_mapping_rules(slug, title),
        "requirements.txt":  _content_requirements(),
        ".env.example":      _content_env_example(),
        ".gitignore":        _content_gitignore(),
    }


# ─── MAIN ──────────────────────────────────────────────────────────────────────

def create_project(project_name: str, parent: Path, dry_run: bool) -> None:
    project_dir = parent / project_name

    if project_dir.exists() and not dry_run:
        print(f"  [!!]  La carpeta ya existe: {project_dir}")
        print(f"        Usa un nombre diferente o elimínala primero.")
        sys.exit(1)

    mode = "DRY RUN — " if dry_run else ""
    sep  = "=" * 65
    print(f"\n{sep}")
    print(f"  {mode}Creando: {project_name}")
    print(f"  Destino: {project_dir}")
    print(sep)

    # ── carpetas ──────────────────────────────────────────────────────────
    print("\n  Carpetas:")
    for folder in FOLDERS:
        path = project_dir / folder
        print(f"    {folder}/")
        if not dry_run:
            path.mkdir(parents=True, exist_ok=True)
            (path / ".gitkeep").touch()

    # ── archivos ──────────────────────────────────────────────────────────
    file_map = build_file_map(project_name, project_dir)
    print(f"\n  Archivos ({len(file_map)}):")
    for rel_path, content in file_map.items():
        print(f"    {rel_path}")
        if not dry_run:
            full = project_dir / rel_path
            full.parent.mkdir(parents=True, exist_ok=True)
            full.write_text(content, encoding="utf-8")

    # ── resumen ───────────────────────────────────────────────────────────
    print(f"\n{sep}")
    if dry_run:
        print(f"  DRY RUN completo. Nada fue escrito.")
    else:
        print(f"  [OK]  {project_name} creado exitosamente.")
        print(f"\n  Siguientes pasos:")
        print(f"    1. cd {project_dir}")
        print(f"    2. cp .env.example .env   # llena tus claves")
        print(f"    3. pip install -r requirements.txt")
        print(f"    4. Edita mapping_rules.json con los datasets de tu tema")
        print(f"    5. Copia los prompts de Proyecto_01 y adapta el texto")
        print(f"    6. python main.py")
    print(sep + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Crea un nuevo proyecto de video-ensayo cartográfico."
    )
    parser.add_argument(
        "project_name",
        help='Nombre del proyecto (ej: "Proyecto_02_Inflacion")',
    )
    parser.add_argument(
        "--parent",
        default=str(Path(__file__).resolve().parent.parent),
        help="Carpeta padre donde crear el proyecto (default: carpeta hermana del actual)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Muestra qué se crearía sin escribir nada",
    )
    args = parser.parse_args()
    create_project(args.project_name, Path(args.parent), args.dry_run)


if __name__ == "__main__":
    main()
