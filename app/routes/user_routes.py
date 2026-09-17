from typing import Literal

from fastapi import APIRouter, Depends, Query, Request, status
from sqlalchemy.orm import Session

from ..dependencies.auth_dependency import (
    get_current_active_user,
    require_admin,
)
from ..dependencies.database_dependency import get_db
from ..middlewares.request_middleware import limiter
from ..schemas.user_schema import UserCreate, UserPatch, UserResponse, UserRole, UserUpdate
from ..services import user_service


router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_admin)],
)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return user_service.create_user(db, user)


@router.get(
    "",
    response_model=list[UserResponse],
    dependencies=[Depends(get_current_active_user)],
)
@limiter.limit("30/minute")
def list_users(
    request: Request,
    role: UserRole | None = Query(default=None),
    is_active: bool | None = Query(default=None),
    sort_by: Literal["name", "created_at"] = Query(default="created_at"),
    sort_order: Literal["asc", "desc"] = Query(default="asc"),
    db: Session = Depends(get_db),
):
    return user_service.list_users(db, role, is_active, sort_by, sort_order)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    dependencies=[Depends(get_current_active_user)],
)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return user_service.get_user(db, user_id)


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    dependencies=[Depends(require_admin)],
)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    return user_service.update_user(db, user_id, user)


@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    dependencies=[Depends(require_admin)],
)
def patch_user(user_id: int, user: UserPatch, db: Session = Depends(get_db)):
    return user_service.patch_user(db, user_id, user)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_admin)],
)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user_service.delete_user(db, user_id)
    return None
