class IntentClassifier:
    def __init__(self) -> None:
        self.project_keywords = {
            "vega", "project", "code", "memory", "architecture", "bug"
        }

        self.emotional_keywords = {
            "tired", "frustrated", "motivated", "angry", "happy"
        }

        self.personal_keywords = {
            "i like", "i enjoy", "my friends", "i study"
        }

    def classify(self, text: str) -> str:
        text_lower = text.lower()

        if self._contains_any(text_lower, self.project_keywords):
            return "project"

        if self._contains_any(text_lower, self.emotional_keywords):
            return "emotional"

        if self._contains_any(text_lower, self.personal_keywords):
            return "personal"

        return "casual"

    def _contains_any(self, text: str, keywords: set[str]) -> bool:
        return any(keyword in text for keyword in keywords)
