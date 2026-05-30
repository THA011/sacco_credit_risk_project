from typing import List, Optional
from pydantic import BaseModel


class LoanBase(BaseModel):
    loan_name: Optional[str]
    balance: Optional[float]


class LoanRead(LoanBase):
    id: int

    class Config:
        orm_mode = True


class MemberBase(BaseModel):
    member_no: str
    full_name: Optional[str]
    mobile_no: Optional[str]


class MemberRead(MemberBase):
    id: int
    loans: List[LoanRead] = []

    class Config:
        orm_mode = True
