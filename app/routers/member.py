from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.member import MemberCreate, MemberResponse
from app.auth.dependency import get_current_user
from app.models.user import User
from app.services.member_services import create_member, get_member_by_user_id, update_member,delete_member


router = APIRouter(
    prefix="/members",
    tags=["Members"]
)


@router.post(
    "",
    response_model=MemberResponse,
    status_code=status.HTTP_201_CREATED
)
def create_member_profile(
    member: MemberCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return create_member(
        db=db,
        member_data=member,
        user_id=current_user.id,
    )

@router.get("/me", response_model=MemberResponse)
def get_member_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_member_by_user_id(
        db=db,
        user_id=current_user.id,
    )

@router.patch("/me", response_model=MemberResponse)
def update_member_profile(
    member: MemberCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return update_member(
        db=db,
        member_data=member,
        user_id=current_user.id,
    )

@router.delete("/me")
def delete_member_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return delete_member(
        db=db,
        user_id=current_user.id,
    )