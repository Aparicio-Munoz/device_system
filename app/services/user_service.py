from typing import Literal

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..auth.security import DISABLED_PASSWORD_HASH
from ..models.user_model import User
from ..schemas.user_schema import UserCreate, UserPatch, UserUpdate


SortField = Literal["name", "created_at"]
SortOrder = Literal["asc", "desc"]


def _values(data: UserCreate | UserUpdate | UserPatch) -> dict:
    values = data.model_dump(exclude_unset=True)

    if "email" in values:
        values["email"] = str(values["email"]).lower()

    return values


def _find_by_email(db: Session, email: str, user_id: int | None = None) -> User | None:
    statement = select(User).where(User.email == email)

    if user_id is not None:
        statement = statement.where(User.id != user_id)

    return db.scalar(statement)


def _commit(db: Session, user: User) -> User:
    try:
        db.commit()
        db.refresh(user)
    except IntegrityError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado",
        ) from error

    return user


def create_user(db: Session, data: UserCreate) -> User:
    values = _values(data)
    values["hashed_password"] = DISABLED_PASSWORD_HASH

    if _find_by_email(db, values["email"]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado",
        )

    user = User(**values)
    db.add(user)
    return _commit(db, user)


def list_users(
    db: Session,
    role: str | None = None,
    is_active: bool | None = None,
    sort_by: SortField = "created_at",
    sort_order: SortOrder = "asc",
) -> list[User]:
    statement = select(User)

    if role is not None:
        statement = statement.where(User.role == role)

    if is_active is not None:
        statement = statement.where(User.is_active == is_active)

    order_column = User.name if sort_by == "name" else User.created_at

    if sort_order == "desc":
        order_column = order_column.desc()

    statement = statement.order_by(order_column, User.id)
    return list(db.scalars(statement).all())


def get_user(db: Session, user_id: int) -> User:
    user = db.get(User, user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )

    return user


def update_user(db: Session, user_id: int, data: UserUpdate) -> User:
    user = get_user(db, user_id)
    values = _values(data)

    if _find_by_email(db, values["email"], user_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado",
        )

    for field, value in values.items():
        setattr(user, field, value)

    return _commit(db, user)


def patch_user(db: Session, user_id: int, data: UserPatch) -> User:
    user = get_user(db, user_id)
    values = _values(data)

    if not values:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debes enviar al menos un campo para actualizar",
        )

    if "email" in values and _find_by_email(db, values["email"], user_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado",
        )

    for field, value in values.items():
        setattr(user, field, value)

    return _commit(db, user)


def delete_user(db: Session, user_id: int) -> None:
    user = get_user(db, user_id)

    if user.loans:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se puede eliminar un usuario con historial de préstamos",
        )

    db.delete(user)

    try:
        db.commit()
    except IntegrityError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se puede eliminar el usuario porque tiene préstamos",
        ) from error
