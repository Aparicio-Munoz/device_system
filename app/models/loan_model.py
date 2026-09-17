from datetime import datetime, timezone

from sqlalchemy import CheckConstraint, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..database.connection import Base


class Loan(Base):
    __tablename__ = "loans"

    __table_args__ = (
        CheckConstraint(
            "status IN ('active', 'returned', 'overdue')",
            name="ck_loans_status",
        ),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    device_id = Column(
        Integer,
        ForeignKey("devices.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    loan_date = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    return_date = Column(DateTime(timezone=True), nullable=True)
    status = Column(String(20), nullable=False, default="active", index=True)

    user = relationship("User", back_populates="loans")
    device = relationship("Device", back_populates="loans")
