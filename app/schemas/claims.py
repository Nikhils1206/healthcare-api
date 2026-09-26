from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel

from app.models.claim import ClaimStatus


class ClaimCreate(BaseModel):
    service_date: date
    description: str
    diagnosis: str
    billed_amount: Decimal


class ClaimApproval(BaseModel):
    approved_amount: Decimal


class ClaimResponse(BaseModel):
    id: UUID
    member_id: UUID
    claim_number: str
    service_date: date
    description: str
    diagnosis: str
    billed_amount: Decimal
    approved_amount: Decimal | None
    status: ClaimStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True