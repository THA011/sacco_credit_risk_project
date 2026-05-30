from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import Member
from app.schemas import MemberRead

router = APIRouter(prefix="/api/v1/members", tags=["members"])


@router.get("/search", response_model=List[MemberRead])
def search_members(q: str = Query(..., min_length=2), db: Session = Depends(get_db)):
    term = f"%{q}%"
    members = (
        db.query(Member)
        .filter(
            or_(
                Member.member_no.ilike(term),
                Member.full_name.ilike(term),
                Member.mobile_no.ilike(term),
            )
        )
        .all()
    )
    if not members:
        raise HTTPException(status_code=404, detail="No members match search query")
    return members


@router.get("/{member_no}", response_model=MemberRead)
def get_member(member_no: str, db: Session = Depends(get_db)):
    member = db.query(Member).filter(Member.member_no == member_no).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return member
