from fastapi import APIRouter, HTTPException, Query, status

from app.schemas.user_schema import (
    APIResponse,
    User,
    UserCreate,
    UserResponse,
    UserRole,
)

router = APIRouter(prefix="/users", tags=["Users"])

users = [
    User(
        id=1,
        name="Daniel Munoz",
        email="daniel@example.com",
        role=UserRole.admin,
        is_active=True,
    ),
    User(
        id=2,
        name="Laura Gomez",
        email="laura@example.com",
        role=UserRole.support,
        is_active=True,
    ),
    User(
        id=3,
        name="Carlos Perez",
        email="carlos@example.com",
        role=UserRole.user,
        is_active=False,
    ),
]


@router.get("", response_model=APIResponse[list[UserResponse]])
def get_users(
    role: UserRole | None = Query(
        default=None,
        description="Filtra por rol: admin, support o user.",
    ),
    is_active: bool | None = Query(
        default=None,
        description="Filtra por estado activo o inactivo.",
    ),
):
    result = users.copy()

    if role is not None:
        result = [user for user in result if user.role == role]

    if is_active is not None:
        result = [user for user in result if user.is_active == is_active]

    return {
        "message": "Usuarios obtenidos correctamente",
        "data": result,
    }


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=APIResponse[UserResponse],
)
def create_user(user: UserCreate):
    user_exists = any(existing_user.id == user.id for existing_user in users)

    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un usuario con este ID",
        )

    email_exists = any(
        str(existing_user.email).casefold() == str(user.email).casefold()
        for existing_user in users
    )

    if email_exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El correo ya está registrado",
        )

    new_user = User.model_validate(user)
    users.append(new_user)

    return {
        "message": "Usuario creado correctamente",
        "data": new_user,
    }


@router.get("/{user_id}", response_model=APIResponse[UserResponse])
def get_user_by_id(user_id: int):
    user = next((user for user in users if user.id == user_id), None)

    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return {
        "message": "Usuario obtenido correctamente",
        "data": user,
    }
