import uuid

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.auth.dependency import get_current_user
from app.auth.roles import require_reviewer
from app.database import get_db
from app.models.claim import ClaimStatus
from app.models.user import User
from app.schemas.claims import (
    ClaimApproval,
    ClaimCreate,
    ClaimResponse,
)
from app.services.claim_service import (
    approve_claim,
    create_claim,
    get_claim,
    get_claims,
    reject_claim,
)


router = APIRouter(
    prefix="/claims",
    tags=["Claims"],
)


# ---------------------------------------------------------
# Create Claim
# ---------------------------------------------------------

@router.post(
    "",
    response_model=ClaimResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_claim_endpoint(
    claim: ClaimCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return create_claim(
        db=db,
        claim_data=claim,
        user_id=current_user.id,
    )


# ---------------------------------------------------------
# Get My Claims
# ---------------------------------------------------------

@router.get(
    "",
    response_model=list[ClaimResponse],
)
def get_claims_endpoint(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    status_filter: ClaimStatus | None = Query(
        None,
        alias="status",
    ),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_claims(
        db=db,
        user_id=current_user.id,
        page=page,
        limit=limit,
        status=status_filter,
    )


# ---------------------------------------------------------
# Get Single Claim
# ---------------------------------------------------------

@router.get(
    "/{claim_id}",
    response_model=ClaimResponse,
)
def get_claim_endpoint(
    claim_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_claim(
        db=db,
        claim_id=claim_id,
        user_id=current_user.id,
    )


# ---------------------------------------------------------
# Approve Claim
# ADMIN / PROVIDER only
# ---------------------------------------------------------

@router.patch(
    "/{claim_id}/approve",
    response_model=ClaimResponse,
)
def approve_claim_endpoint(
    claim_id: uuid.UUID,
    approval: ClaimApproval,
    current_user: User = Depends(require_reviewer),
    db: Session = Depends(get_db),
):
    return approve_claim(
        db=db,
        claim_id=claim_id,
        approved_amount=approval.approved_amount,
    )


# ---------------------------------------------------------
# Reject Claim
# ADMIN / PROVIDER only
# ---------------------------------------------------------

@router.patch(
    "/{claim_id}/reject",
    response_model=ClaimResponse,
)
def reject_claim_endpoint(
    claim_id: uuid.UUID,
    current_user: User = Depends(require_reviewer),
    db: Session = Depends(get_db),
):
    return reject_claim(
        db=db,
        claim_id=claim_id,
    )