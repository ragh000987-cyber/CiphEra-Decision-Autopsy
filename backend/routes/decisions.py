from fastapi import APIRouter, HTTPException

from backend.models.decision import AutopsyRequest, AutopsyReport, ReflectRequest, RetainRequest
from backend.services.autopsy import autopsy_service
from backend.services.decisions import decision_store
from backend.services.hindsight import hindsight_service

router = APIRouter(prefix="/decisions", tags=["decisions"])


@router.get("")
def list_decisions():
    return decision_store.get_all()


@router.get("/{decision_id}")
def get_decision(decision_id: str):
    decision = decision_store.get_by_id(decision_id)
    if not decision:
        raise HTTPException(status_code=404, detail="Decision not found")
    return decision


@router.post("/{decision_id}/retain")
def retain_decision(decision_id: str, body: RetainRequest):
    decision = decision_store.get_by_id(decision_id)
    if not decision:
        raise HTTPException(status_code=404, detail="Decision not found")
    if not hindsight_service.is_available():
        raise HTTPException(status_code=503, detail="Hindsight client unavailable")

    try:
        return hindsight_service.retain(decision, bank_id=body.bank_id)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@router.post("/{decision_id}/reflect")
def reflect_on_decision(decision_id: str, body: ReflectRequest):
    decision = decision_store.get_by_id(decision_id)
    if not decision:
        raise HTTPException(status_code=404, detail="Decision not found")
    if not hindsight_service.is_available():
        raise HTTPException(status_code=503, detail="Hindsight client unavailable")

    query = body.query or f"What can we learn from the decision '{decision.title}'?"
    try:
        return hindsight_service.reflect(query=query, bank_id=body.bank_id)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@router.post("/{decision_id}/autopsy", response_model=AutopsyReport)
def autopsy_decision(decision_id: str, body: AutopsyRequest | None = None):
    decision = decision_store.get_by_id(decision_id)
    if not decision:
        raise HTTPException(status_code=404, detail="Decision not found")

    focus = body.focus if body else None
    return autopsy_service.run(decision, focus=focus)
