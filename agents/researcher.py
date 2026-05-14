"""
Researcher — wrapper Python para el agente de produccion.
La logica de prompts vive en prompts/researcher.md.
"""
from pathlib import Path
from core.base_agent import BaseAgent


class Researcher(BaseAgent):

    def checkpoint_name(self) -> str:
        return "research"

    def run(self) -> dict:
        prompt = self.load_prompt("researcher.md")
        # TODO: invocar Claude API con el prompt y los inputs correspondientes
        # Datasets disponibles desde mapping_rules.json:
        #   for ds in self.mapping.get("datasets", []):
        #       print(ds["id"], ds["visual_destination"])
        raise NotImplementedError("Researcher.run() pendiente de implementar")
