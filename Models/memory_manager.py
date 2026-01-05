# PABLO BOTELLA JIMÉNEZ
# Vega AI Assistant Application

# Manages the memory system for the Vega AI assistant.
# Handles loading, retrieving, and updating different types of memory: core, contextual, and temporal.
# Memory is stored in JSON files within the specified assets memory directory.
# Provides methods to get relevant memory based on intent and to clean up old temporal memory entries.
# Memory updates can be applied based on new information received during interactions.


## LIBRARY IMPORTS
from pathlib import Path
import json
from typing import List, Dict
from datetime import datetime, timedelta

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

        #if user.get("name"):
        #    memory.append(f"{user['name']} is the user")

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

        if entry_type == "mood" and value:
            memory.append(f"Pablo is currently feeling {value}")

        return memory
    
    def apply_memory_updates(self, updates: Dict) -> None:
        if not isinstance(updates, dict):
            return
        
        self.cleanup_temporal_memory()
        self._apply_core_updates(updates.get("core", {}))
        self._apply_contextual_updates(updates.get("contextual", {}))
        self._apply_temporal_updates(updates.get("temporal", {}))

        self._save_json("core.json", self.core_memory)
        self._save_json("contextual.json", self.contextual_memory)
        self._save_json("temporal.json", self.temporal_memory)

    def _apply_core_updates(self, core_updates: Dict) -> None:
        additions = core_updates.get("add", [])

        traits = self.core_memory.setdefault("traits", {}).setdefault("personality", [])

        for item in additions:
            if item not in traits:
                traits.append(item)


    def _apply_contextual_updates(self, contextual_updates: Dict) -> None:
        additions = contextual_updates.get("add", [])

        if not additions:
            return

        topics = self.contextual_memory.setdefault("recurring_topics", [])

        for item in additions:
            normalized = item.lower().strip()

            # If there is already a topic, it normalizes it
            if topics:
                topics[0] = normalized
            else:
                topics.append(normalized)

            # We only keep one topic at a time
            break


    def _apply_temporal_updates(self, temporal_updates: dict) -> None:
        additions = temporal_updates.get("add", [])

        if not additions:
            return

        entries = self.temporal_memory.setdefault("entries", [])
        today = datetime.now().strftime("%Y-%m-%d")

        for item in additions:
            # Delete any mood entry for today to avoid duplicates
            entries[:] = [
                entry for entry in entries
                if entry.get("date") != today
            ]

            entries.append({
                "type": "mood",
                "value": item,
                "date": today
            })

    def cleanup_temporal_memory(self, max_age_days: int = 7) -> None:
        entries = self.temporal_memory.get("entries", [])

        if not entries:
            return

        cutoff_date = datetime.now() - timedelta(days=max_age_days)

        cleaned_entries = []

        for entry in entries:
            entry_date_str = entry.get("date")
            if not entry_date_str:
                continue

            try:
                entry_date = datetime.strptime(entry_date_str, "%Y-%m-%d")
            except ValueError:
                continue

            if entry_date >= cutoff_date:
                cleaned_entries.append(entry)

        self.temporal_memory["entries"] = cleaned_entries


    def _is_duplicate_temporal_entry(
        self,
        new_value: str,
        existing_entries: list[dict],
        lookback: int = 5,
    ) -> bool:
        normalized_new = new_value.lower().strip()

        for entry in existing_entries[-lookback:]:
            existing_value = entry.get("value", "").lower().strip()
            if normalized_new == existing_value:
                return True

        return False
