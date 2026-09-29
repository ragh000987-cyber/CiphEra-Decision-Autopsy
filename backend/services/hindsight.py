import os
from typing import Any, Optional

from backend.models.decision import Decision


class HindsightService:
    """Wrapper around the Hindsight client for retain / recall / reflect."""

    def __init__(self) -> None:
        self.base_url = os.getenv("HINDSIGHT_BASE_URL", "http://localhost:8888")
        self.default_bank = os.getenv("HINDSIGHT_BANK_ID", "ciph-era-decisions")
        self._client: Optional[Any] = None

    @property
    def client(self) -> Any:
        if self._client is None:
            try:
                from hindsight_client import Hindsight

                self._client = Hindsight(base_url=self.base_url)
            except ImportError as exc:
                raise RuntimeError(
                    "hindsight-client is not installed. Run: pip install hindsight-client"
                ) from exc
        return self._client

    def is_available(self) -> bool:
        try:
            self.client
            return True
        except RuntimeError:
            return False

    def format_decision_content(self, decision: Decision) -> str:
        assumptions = "\n".join(f"- {a}" for a in decision.assumptions)
        evidence = "\n".join(f"- {e}" for e in decision.evidence)
        return (
            f"Decision: {decision.title}\n"
            f"Date: {decision.timestamp.isoformat()}\n"
            f"Context: {decision.context}\n"
            f"Reasoning: {decision.reasoning}\n"
            f"Assumptions:\n{assumptions or '- (none recorded)'}\n"
            f"Outcome ({decision.outcome_status.value}): {decision.outcome or 'pending'}\n"
            f"Evidence:\n{evidence or '- (none recorded)'}\n"
            f"Tags: {', '.join(decision.tags) if decision.tags else 'none'}"
        )

    def retain(self, decision: Decision, bank_id: Optional[str] = None) -> dict[str, Any]:
        bank = bank_id or self.default_bank
        content = self.format_decision_content(decision)
        result = self.client.retain(bank_id=bank, content=content)
        return {"bank_id": bank, "decision_id": decision.id, "result": result}

    def recall(self, query: str, bank_id: Optional[str] = None) -> dict[str, Any]:
        bank = bank_id or self.default_bank
        result = self.client.recall(bank_id=bank, query=query)
        return {"bank_id": bank, "query": query, "result": result}

    def reflect(self, query: str, bank_id: Optional[str] = None) -> dict[str, Any]:
        bank = bank_id or self.default_bank
        result = self.client.reflect(bank_id=bank, query=query)
        return {"bank_id": bank, "query": query, "result": result}


hindsight_service = HindsightService()
