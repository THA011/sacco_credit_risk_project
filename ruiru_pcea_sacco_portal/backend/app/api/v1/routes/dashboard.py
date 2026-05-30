from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import Loan
from app.schemas import MemberRead

router = APIRouter(prefix="/api/v1/dashboard", tags=["dashboard"])


@router.get("/summary")
def portfolio_summary(db: Session = Depends(get_db)):
    total_balance = db.query(func.coalesce(func.sum(Loan.balance), 0)).scalar() or 0
    total_loans = db.query(func.count(Loan.id)).scalar() or 0
    active_members = db.query(func.count(func.distinct(Loan.member_id))).scalar() or 0

    return {
        "total_balance": float(total_balance),
        "active_members": int(active_members),
        "total_loans": int(total_loans),
        "average_loan_balance": float(total_balance) / (total_loans or 1),
    }
