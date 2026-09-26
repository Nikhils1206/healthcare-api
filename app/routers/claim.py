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
from app.services.ai_service import (
    analyze_claim,
    save_claim_analysis,
)


router = APIRouter(
    prefix="/claims",
    tags=["Claims"],
)


# CREATE CLAIM
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


# GET CLAIMS
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


# GET SINGLE CLAIM
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


# APPROVE CLAIM
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


# REJECT CLAIM
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


# AI CLAIM ANALYSIS
@router.post(
    "/{claim_id}/analyze",
)
def analyze_claim_endpoint(
    claim_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    claim = get_claim(
        db=db,
        claim_id=claim_id,
        user_id=current_user.id,
    )

    analysis = analyze_claim(claim)

    saved_analysis = save_claim_analysis(
        db=db,
        claim_id=claim.id,
        analysis=analysis,
    )

    return {
        "claim_id": claim.id,
        "claim_number": claim.claim_number,
        "analysis": {
            "id": saved_analysis.id,
            "risk_score": saved_analysis.risk_score,
            "risk_level": saved_analysis.risk_level,
            "flags": saved_analysis.flags,
            "summary": saved_analysis.summary,
            "analyzed_at": saved_analysis.analyzed_at,
        },
    }