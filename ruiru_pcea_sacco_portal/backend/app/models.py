from datetime import date
from sqlalchemy import Date, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Member(Base):
    __tablename__ = "members"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    member_no: Mapped[str] = mapped_column(String(16), unique=True, index=True, nullable=False)
    full_name: Mapped[str | None] = mapped_column(String(255))
    mobile_no: Mapped[str | None] = mapped_column(String(32))

    loans: Mapped[list["Loan"]] = relationship(back_populates="member")


class Loan(Base):
    __tablename__ = "loans"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    member_id: Mapped[int] = mapped_column(ForeignKey("members.id"))
    loan_name: Mapped[str | None] = mapped_column(String(128))
    balance: Mapped[Numeric | None] = mapped_column(Numeric(18, 2))

    member: Mapped[Member] = relationship(back_populates="loans")
