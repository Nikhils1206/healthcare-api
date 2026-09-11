from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.members import Member
from app.schemas.member import MemberCreate, MemberUpdate


def create_member(
    db: Session,
    member_data: MemberCreate,
    user_id: UUID,
):
    existing_member = db.query(Member).filter(
        Member.user_id == user_id
    ).first()

    if existing_member:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Member profile already exists for this user",
        )

    member = Member(
        user_id=user_id,
        date_of_birth=member_data.date_of_birth,
        gender=member_data.gender,
        phone=member_data.phone,
        blood_group=member_data.blood_group,
        address=member_data.address,
        emergency_contact=member_data.emergency_contact,
    )

    db.add(member)
    db.commit()
    db.refresh(member)

    return member

def get_member(
    db: Session,
    member_id: UUID,
):
    member = db.query(Member).filter(
        Member.id == member_id
    ).first()

    if member is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found",
        )

    return member

def get_member_by_user_id(
    db: Session,
    user_id: UUID,
):
    member = db.query(Member).filter(
        Member.user_id == user_id
    ).first()

    if member is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member profile not found",
        )

    return member

def update_member(
    db: Session,
    user_id: UUID,
    member_data: MemberUpdate,
):
    member = db.query(Member).filter(
        Member.user_id == user_id
    ).first()

    if member is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member profile not found",
        )

    update_data = member_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(member, field, value)

    db.commit()
    db.refresh(member)

    return member

def delete_member(
    db: Session,
    user_id: UUID,
):
    member = db.query(Member).filter(
        Member.user_id == user_id
    ).first()

    if member is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found",
        )

    db.delete(member)
    db.commit()

    return {
        "message": "Member deleted successfully"
    }