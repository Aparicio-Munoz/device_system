from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..dependencies.auth_dependency import get_current_active_user
from ..dependencies.database_dependency import get_db
from ..middlewares.request_middleware import limiter
from ..schemas.auth_schema import Token, UserRegister
from ..schemas.user_schema import UserResponse
from . import auth_service
from .security import create_access_token


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar usuario",
)
@limiter.limit("3/minute")
def register(
    request: Request,
    user: UserRegister,
    db: Session = Depends(get_db),
):
    return auth_service.register_user(db, user)


@router.post(
    "/login",
    response_model=Token,
    summary="Iniciar sesión",
)
@limiter.limit("5/minute")
def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = auth_service.authenticate_user(
        db,
        form_data.username,
        form_data.password,
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token({"sub": str(user.id), "role": user.role})
    return {"access_token": token, "token_type": "bearer"}


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Consultar usuario autenticado",
)
def me(current_user=Depends(get_current_active_user)):
    return current_user
