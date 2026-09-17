from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator, model_validator


UserRole = Literal["admin", "support", "user"]


def _clean_name(value: str) -> str:
    if isinstance(value, str):
        return value.strip()
    return value


def _clean_email(value: str) -> str:
    if isinstance(value, str):
        return value.strip().lower()
    return value


class UserCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    role: UserRole
    is_active: bool = True

    _name_validator = field_validator("name", mode="before")(_clean_name)
    _email_validator = field_validator("email", mode="before")(_clean_email)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Ana Pérez",
                "email": "ana@sena.edu.co",
                "role": "user",
                "is_active": True,
            }
        }
    )


class UserUpdate(UserCreate):
    pass


class UserPatch(BaseModel):
    name: str | None = Field(default=None, min_length=3, max_length=100)
    email: EmailStr | None = None
    role: UserRole | None = None
    is_active: bool | None = None

    _name_validator = field_validator("name", mode="before")(_clean_name)
    _email_validator = field_validator("email", mode="before")(_clean_email)

    @model_validator(mode="after")
    def reject_explicit_nulls(self):
        for field in self.model_fields_set:
            if getattr(self, field) is None:
                raise ValueError(f"El campo '{field}' no puede ser null")

        return self


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: UserRole
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
