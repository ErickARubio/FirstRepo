"""
Manages checkpoint state for a project.

State is persisted in workspace/state.json.
Each checkpoint has: status ("pending" | "approved"), timestamp, and free-form meta.
"""

import json
from pathlib import Path
from datetime import datetime, timezone


class StateManager:

    CHECKPOINTS = ["research", "script", "visuals", "voice", "animation"]

    def __init__(self, project_root: Path):
        self._path  = Path(project_root) / "workspace" / "state.json"
        self._state = self._load()

    # ── public ──────────────────────────────────────────────────────────────

    def mark_done(self, checkpoint: str, meta: dict | None = None) -> None:
        self._state.setdefault("checkpoints", {})[checkpoint] = {
            "status":    "approved",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            **(meta or {}),
        }
        self._save()

    def mark_pending(self, checkpoint: str) -> None:
        self._state.setdefault("checkpoints", {})[checkpoint] = {"status": "pending"}
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
        return "\n".join(lines)

    # ── private ─────────────────────────────────────────────────────────────

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
