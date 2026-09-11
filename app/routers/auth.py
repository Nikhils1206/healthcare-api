from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.auth.dependency import get_current_user
from app.models.user import User
from app.database import get_db

from app.schemas.user import (
    UserCreate,
    UserResponse,
    UserLogin,
    Token,
)

from app.services.user_service import (
    create_user,
    authenticate_user,
)

from app.auth.jwt import create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    return create_user(db, user)


@router.post(
    "/login",
    response_model=Token,
)
def login(
    user: UserLogin,
    db: Session = Depends(get_db),
):
    authenticated_user = authenticate_user(
        db=db,
        email=user.email,
        password=user.password,
    )

    access_token = create_access_token(
        data={
            "sub": str(authenticated_user.id),
            "role": authenticated_user.role.value,
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
@router.get("/me")
def get_me(
    current_user: User = Depends(get_current_user),
):
    return current_user