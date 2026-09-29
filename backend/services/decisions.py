import json
from pathlib import Path
from typing import Optional

from backend.models.decision import Decision


class DecisionStore:
    def __init__(self, data_path: Optional[Path] = None) -> None:
        if data_path is None:
            data_path = Path(__file__).resolve().parents[2] / "data" / "decisions.json"
        self.data_path = data_path
        self._cache: list[Decision] = []

    def load(self) -> list[Decision]:
        with open(self.data_path, encoding="utf-8") as f:
            raw = json.load(f)
        self._cache = [Decision.model_validate(item) for item in raw]
        return self._cache

    def get_all(self) -> list[Decision]:
        if not self._cache:
            self.load()
        return self._cache

    def get_by_id(self, decision_id: str) -> Optional[Decision]:
        for decision in self.get_all():
            if decision.id == decision_id:
                return decision
        return None


decision_store = DecisionStore()
