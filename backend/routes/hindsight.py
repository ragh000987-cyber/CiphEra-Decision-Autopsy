from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.services.hindsight import hindsight_service

router = APIRouter(prefix="/hindsight", tags=["hindsight"])


class RecallBody(BaseModel):
    query: str
    bank_id: str = "ciph-era-decisions"


@router.get("/status")
def hindsight_status():
    return {
        "available": hindsight_service.is_available(),
        "base_url": hindsight_service.base_url,
        "default_bank": hindsight_service.default_bank,
    }


@router.post("/recall")
def recall_memories(body: RecallBody):
    if not hindsight_service.is_available():
        raise HTTPException(status_code=503, detail="Hindsight client unavailable")

    try:
        return hindsight_service.recall(query=body.query, bank_id=body.bank_id)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
