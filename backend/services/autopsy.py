import json
import re
from typing import Optional

from backend.models.decision import AutopsyReport, Decision
from backend.services.llm import llm_service


AUTOPSY_SYSTEM = """You are an engineering post-mortem analyst for agentic AI systems.
Given a past decision and its outcome, produce a structured autopsy.

Respond ONLY with valid JSON matching this schema:
{
  "root_causes": ["..."],
  "premise_drift": ["assumptions that changed or were wrong"],
  "lessons": ["..."],
  "recommendations": ["..."],
  "summary": "one paragraph executive summary"
}"""


class AutopsyService:
    def run(self, decision: Decision, focus: Optional[str] = None) -> AutopsyReport:
        focus_line = f"\nFocus area: {focus}" if focus else ""
        user_prompt = (
            f"Analyze this decision and its outcome.{focus_line}\n\n"
            f"Title: {decision.title}\n"
            f"Context: {decision.context}\n"
            f"Reasoning: {decision.reasoning}\n"
            f"Assumptions: {json.dumps(decision.assumptions)}\n"
            f"Outcome status: {decision.outcome_status.value}\n"
            f"Outcome: {decision.outcome or 'unknown'}\n"
            f"Evidence: {json.dumps(decision.evidence)}"
        )

        raw = llm_service.complete(AUTOPSY_SYSTEM, user_prompt)
        parsed = self._parse_response(raw)

        return AutopsyReport(
            decision_id=decision.id,
            title=decision.title,
            **parsed,
        )

    def _parse_response(self, raw: str) -> dict:
        match = re.search(r"\{[\s\S]*\}", raw)
        if not match:
            return self._fallback(raw)

        try:
            data = json.loads(match.group())
            return {
                "root_causes": data.get("root_causes", []),
                "premise_drift": data.get("premise_drift", []),
                "lessons": data.get("lessons", []),
                "recommendations": data.get("recommendations", []),
                "summary": data.get("summary", raw[:500]),
            }
        except json.JSONDecodeError:
            return self._fallback(raw)

    def _fallback(self, raw: str) -> dict:
        return {
            "root_causes": ["Unable to parse structured autopsy — see summary"],
            "premise_drift": [],
            "lessons": [],
            "recommendations": ["Re-run autopsy with OPENAI_API_KEY configured"],
            "summary": raw[:1000],
        }


autopsy_service = AutopsyService()
