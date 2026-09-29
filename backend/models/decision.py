from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class OutcomeStatus(str, Enum):
    SUCCESS = "success"
    PARTIAL = "partial"
    FAILURE = "failure"
    UNKNOWN = "unknown"


class Decision(BaseModel):
    id: str
    title: str
    context: str
    reasoning: str
    assumptions: list[str] = Field(default_factory=list)
    outcome: Optional[str] = None
    outcome_status: OutcomeStatus = OutcomeStatus.UNKNOWN
    timestamp: datetime
    tags: list[str] = Field(default_factory=list)
    evidence: list[str] = Field(default_factory=list)


class AutopsyRequest(BaseModel):
    decision_id: str
    focus: Optional[str] = None


class AutopsyReport(BaseModel):
    decision_id: str
    title: str
    root_causes: list[str]
    premise_drift: list[str]
    lessons: list[str]
    recommendations: list[str]
    summary: str


class ReflectRequest(BaseModel):
    query: str
    bank_id: str = "ciph-era-decisions"


class RetainRequest(BaseModel):
    bank_id: str = "ciph-era-decisions"
