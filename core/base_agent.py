"""
Abstract base class for all production agents.

Every agent (Researcher, Scriptwriter, …) inherits from this,
gets access to mapping_rules.json automatically, and uses a
shared StateManager to mark its checkpoint as done.
"""

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

    # ── public interface ────────────────────────────────────────────────────

    @abstractmethod
    def run(self) -> dict:
        """Execute the agent. Must return a metadata dict on success."""
        ...

    def checkpoint_name(self) -> str:
        """Override to return a custom checkpoint key; default = class name."""
        return self.__class__.__name__.lower()

    def done(self, meta: dict | None = None) -> dict:
        """Call at the end of run() to mark the checkpoint approved."""
        self.state.mark_done(self.checkpoint_name(), meta or {})
        return meta or {}

    def load_prompt(self, filename: str) -> str:
        """Read a .md prompt file from prompts/."""
        return (self.prompts / filename).read_text(encoding="utf-8")

    def dataset_for(self, visual_id: str) -> dict | None:
        """Return the dataset spec whose visual_destination matches visual_id."""
        for ds in self.mapping.get("datasets", []):
            if ds.get("visual_destination") == visual_id:
                return ds
        return None

    # ── private ─────────────────────────────────────────────────────────────

    def _load_mapping(self) -> dict:
        path = self.root / "mapping_rules.json"
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
        return {}
