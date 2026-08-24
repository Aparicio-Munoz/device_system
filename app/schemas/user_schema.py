from enum import Enum
from typing import Generic, TypeVar

from pydantic import BaseModel, EmailStr, Field


class UserRole(str, Enum):
    admin = "admin"
    support = "support"
    user = "user"


class UserBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    role: UserRole
    is_active: bool


class User(UserBase):
    id: int = Field(..., gt=0)


class UserCreate(User):
    pass


class UserResponse(User):
    pass


T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    message: str
    data: T
