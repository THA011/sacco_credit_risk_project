from fastapi import APIRouter

from app.schemas import LoanBase

router = APIRouter(prefix="/api/v1/risk", tags=["risk"])


@router.post("/calculator")
def calculate_risk(payload: LoanBase):
    # Simple echo for now — frontend can call and we will extend logic
    return {"emi": 0, "ltd": 0, "annual_rate": 0, "risk_score": 0, "verdict": "TBD", "advice": "TBD"}
