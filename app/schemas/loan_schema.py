from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from .device_schema import DeviceSummary


LoanStatus = Literal["active", "returned", "overdue"]


class LoanCreate(BaseModel):
    user_id: int = Field(..., gt=0)
    device_id: int = Field(..., gt=0)
    loan_date: datetime | None = None
    status: Literal["active"] = "active"

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "user_id": 1,
                "device_id": 1,
                "status": "active",
            }
        }
    )


class LoanUpdate(BaseModel):
    status: LoanStatus


class LoanResponse(BaseModel):
    id: int
    user_id: int
    device_id: int
    loan_date: datetime
    return_date: datetime | None
    status: LoanStatus

    model_config = ConfigDict(from_attributes=True)


class UserSummary(BaseModel):
    id: int
    name: str
    email: str

    model_config = ConfigDict(from_attributes=True)


class LoanDetailResponse(LoanResponse):
    user: UserSummary
    device: DeviceSummary
