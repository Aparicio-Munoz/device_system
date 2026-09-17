from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from .user_schema import UserRole


def _clean_name(value: str) -> str:
    return value.strip() if isinstance(value, str) else value


def _clean_email(value: str) -> str:
    return value.strip().lower() if isinstance(value, str) else value


def _validate_password(value: str) -> str:
    if any(character.isspace() for character in value):
        raise ValueError("La contraseña no puede contener espacios")
    if not any(character.isupper() for character in value):
        raise ValueError("La contraseña debe incluir una mayúscula")
    if not any(character.islower() for character in value):
        raise ValueError("La contraseña debe incluir una minúscula")
    if not any(character.isdigit() for character in value):
        raise ValueError("La contraseña debe incluir un número")
    if len(value.encode("utf-8")) > 72:
        raise ValueError("La contraseña no puede superar 72 bytes")
    return value


class UserRegister(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=72)
    role: UserRole = "user"
    is_active: bool = True

    _clean_name = field_validator("name", mode="before")(_clean_name)
    _clean_email = field_validator("email", mode="before")(_clean_email)
    _validate_password = field_validator("password")(_validate_password)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Ana Pérez",
                "email": "ana@sena.edu.co",
                "password": "Segura2026",
                "role": "user",
                "is_active": True,
            }
        }
    )


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=1, max_length=72)

    _clean_email = field_validator("email", mode="before")(_clean_email)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: int
    role: UserRole | None = None

    model_config = ConfigDict(from_attributes=True)
