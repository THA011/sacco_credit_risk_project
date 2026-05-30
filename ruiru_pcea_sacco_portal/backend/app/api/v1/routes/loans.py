from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import Loan, Member
from app.schemas import LoanRead

router = APIRouter(prefix="/api/v1/loans", tags=["loans"])


@router.get("/{loan_id}", response_model=LoanRead)
def get_loan(loan_id: int, db: Session = Depends(get_db)):
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    return loan


@router.get("/member/{member_no}", response_model=List[LoanRead])
def get_loans_by_member(member_no: str, db: Session = Depends(get_db)):
    member = db.query(Member).filter(Member.member_no == member_no).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return db.query(Loan).filter(Loan.member_id == member.id).all()
