from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from ..database.connection import Base


class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    serial_number = Column(String(100), unique=True, nullable=False, index=True)
    device_type = Column(String(50), nullable=False, index=True)
    brand = Column(String(100), nullable=True, index=True)
    is_available = Column(Boolean, nullable=False, default=True)
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    loans = relationship("Loan", back_populates="device")
