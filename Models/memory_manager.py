from pathlib import Path
import json
from typing import List, Dict


class MemoryManager:
    def __init__(self, assets_memory_path: Path) -> None:
        self.assets_memory_path = assets_memory_path

        self.core_memory = {}
        self.contextual_memory = {}
        self.temporal_memory = {}

        self.load_memory()

    def load_memory(self) -> None:
        self.core_memory = self._load_json("core.json")
        self.contextual_memory = self._load_json("contextual.json")
        self.temporal_memory = self._load_json("temporal.json")

    def get_relevant_memory(self, intent: str) -> List[str]:
        relevant_memory: List[str] = []

        if intent == "personal":
            relevant_memory.extend(self._get_core_memory())

        elif intent == "project":
            relevant_memory.extend(self._get_core_memory(limit=1))
            relevant_memory.extend(self._get_contextual_memory())

        elif intent == "emotional":
            relevant_memory.extend(self._get_core_memory(limit=1))
            relevant_memory.extend(self._get_temporal_memory())

        return relevant_memory

    def apply_memory_updates(self, updates: Dict) -> None:
        # validate and apply updates
        pass

    def cleanup_temporal_memory(self) -> None:
        # remove expired temporal entries
        pass

    def _load_json(self, filename: str) -> Dict:
        file_path = self.assets_memory_path / filename

        if not file_path.exists():
            return {}

        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def _save_json(self, filename: str, data: Dict) -> None:
        file_path = self.assets_memory_path / filename

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)


    def _get_core_memory(self, limit: int | None = None) -> List[str]:
        memory: List[str] = []

        user = self.core_memory.get("user", {})

        if user.get("name"):
            memory.append(f"{user['name']} is the user")

        if user.get("studies"):
            memory.append(f"Pablo studies {user['studies']}")

        if user.get("music_taste"):
            memory.append("Pablo enjoys music genres like " + ", ".join(user["music_taste"]))

        if limit is not None:
            return memory[:limit]

        return memory

    def _get_contextual_memory(self) -> List[str]:
        memory: List[str] = []

        projects = self.contextual_memory.get("projects", [])

        for project in projects:
            if project.get("status") == "activo":
                memory.append(f"Pablo is working on the {project['name']} project")

                if project.get("focus"):
                    memory.append(f"The current focus is {project['focus']}")

        return memory

    def _get_temporal_memory(self) -> List[str]:
        memory: List[str] = []

        entries = self.temporal_memory.get("entries", [])

        if not entries:
            return memory

        latest_entry = entries[-1]

        entry_type = latest_entry.get("type")
        value = latest_entry.get("value")

        if entry_type and value:
            memory.append(f"Pablo is currently feeling {value}")

        return memory

