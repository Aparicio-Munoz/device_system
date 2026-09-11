from typing import Literal

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from ..dependencies.database_dependency import get_db
from ..schemas.user_schema import UserCreate, UserPatch, UserResponse, UserRole, UserUpdate
from ..services import user_service


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return user_service.create_user(db, user)


@router.get("", response_model=list[UserResponse])
def list_users(
    role: UserRole | None = Query(default=None),
    is_active: bool | None = Query(default=None),
    sort_by: Literal["name", "created_at"] = Query(default="created_at"),
    sort_order: Literal["asc", "desc"] = Query(default="asc"),
    db: Session = Depends(get_db),
):
    return user_service.list_users(db, role, is_active, sort_by, sort_order)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return user_service.get_user(db, user_id)


@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    return user_service.update_user(db, user_id, user)


@router.patch("/{user_id}", response_model=UserResponse)
def patch_user(user_id: int, user: UserPatch, db: Session = Depends(get_db)):
    return user_service.patch_user(db, user_id, user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user_service.delete_user(db, user_id)
    return None
