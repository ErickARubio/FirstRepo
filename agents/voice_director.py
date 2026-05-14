"""
VoiceDirector — wrapper Python para el agente de produccion.
La logica de prompts vive en prompts/voice_director.md.
"""
from pathlib import Path
from core.base_agent import BaseAgent


class VoiceDirector(BaseAgent):

    def checkpoint_name(self) -> str:
        return "voice"

    def run(self) -> dict:
        prompt = self.load_prompt("voice_director.md")
        # TODO: invocar Claude API con el prompt y los inputs correspondientes
        # Datasets disponibles desde mapping_rules.json:
        #   for ds in self.mapping.get("datasets", []):
        #       print(ds["id"], ds["visual_destination"])
        raise NotImplementedError("VoiceDirector.run() pendiente de implementar")
