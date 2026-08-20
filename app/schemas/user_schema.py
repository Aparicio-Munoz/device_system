from enum import Enum
from pydantic import BaseModel, EmailStr, Field

class UserRole(str, Enum):
    Admin = "admin"
    Support = "support"
    user = "user"

class User(BaseModel):
    id: int
    name: str = Field(..., min_length=3)
    email: EmailStr
    role: UserRole 
    is_active: bool


class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    email: EmailStr
    age: int = Field(ge=18, le=100)


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    age: int