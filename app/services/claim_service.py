import uuid

from sqlalchemy.orm import Session

from app.models.claim import Claim, ClaimStatus
from app.models.members import Member
from app.schemas.claims import ClaimCreate
from app.exceptions.custom import (
    NotFoundException,
    BadRequestException,
)


def get_member_for_user(
    db: Session,
    user_id: uuid.UUID,
):
    member = (
        db.query(Member)
        .filter(Member.user_id == user_id)
        .first()
    )

    if not member:
        raise NotFoundException("Member profile not found")

    return member


def create_claim(
    db: Session,
    claim_data: ClaimCreate,
    user_id: uuid.UUID,
):
    member = get_member_for_user(db, user_id)

    claim = Claim(
        member_id=member.id,
        claim_number=f"CLM-{uuid.uuid4().hex[:8].upper()}",
        service_date=claim_data.service_date,
        description=claim_data.description,
        diagnosis=claim_data.diagnosis,
        billed_amount=claim_data.billed_amount,
        approved_amount=None,
        status=ClaimStatus.PENDING,
    )

    db.add(claim)
    db.commit()
    db.refresh(claim)

    return claim


def get_claims(
    db: Session,
    user_id: uuid.UUID,
    page: int = 1,
    limit: int = 10,
    status: ClaimStatus | None = None,
):
    member = get_member_for_user(db, user_id)

    query = (
        db.query(Claim)
        .filter(Claim.member_id == member.id)
    )

    if status is not None:
        query = query.filter(Claim.status == status)

    offset = (page - 1) * limit

    return (
        query
        .order_by(Claim.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )


def get_claim(
    db: Session,
    claim_id: uuid.UUID,
    user_id: uuid.UUID,
):
    member = get_member_for_user(db, user_id)

    claim = (
        db.query(Claim)
        .filter(
            Claim.id == claim_id,
            Claim.member_id == member.id,
        )
        .first()
    )

    if not claim:
        raise NotFoundException("Claim not found")

    return claim


def approve_claim(
    db: Session,
    claim_id: uuid.UUID,
    approved_amount,
):
    claim = (
        db.query(Claim)
        .filter(Claim.id == claim_id)
        .first()
    )

    if not claim:
        raise NotFoundException("Claim not found")

    if claim.status != ClaimStatus.PENDING:
        raise BadRequestException(
            "Only pending claims can be approved"
        )

    if approved_amount > claim.billed_amount:
        raise BadRequestException(
            "Approved amount cannot be greater than billed amount"
        )

    claim.status = ClaimStatus.APPROVED
    claim.approved_amount = approved_amount

    db.commit()
    db.refresh(claim)

    return claim


def reject_claim(
    db: Session,
    claim_id: uuid.UUID,
):
    claim = (
        db.query(Claim)
        .filter(Claim.id == claim_id)
        .first()
    )

    if not claim:
        raise NotFoundException("Claim not found")

    if claim.status != ClaimStatus.PENDING:
        raise BadRequestException(
            "Only pending claims can be rejected"
        )

    claim.status = ClaimStatus.REJECTED
    claim.approved_amount = None

    db.commit()
    db.refresh(claim)

    return claim