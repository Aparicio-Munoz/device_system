from fastapi import APIRouter, HTTPException, status

from app.schemas.user_schema import UserCreate, UserResponse


router = APIRouter(prefix="/users", tags=["Users"])

users_db: list[UserResponse] = []
next_id = 1


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def create_user(user: UserCreate):
    global next_id

    email = str(user.email).lower()

    for existing_user in users_db:
        if str(existing_user.email).lower() == email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El correo ya está registrado"
            )

    new_user = UserResponse(
        id=next_id,
        name=user.name,
        email=email,
        age=user.age
    )

    users_db.append(new_user)
    next_id += 1

    return new_user