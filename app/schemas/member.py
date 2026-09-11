from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel


class MemberCreate(BaseModel):
    date_of_birth: date
    gender: str
    phone: str
    blood_group: str | None = None
    address: str | None = None
    emergency_contact: str | None = None


class MemberUpdate(BaseModel):
    date_of_birth: date | None = None
    gender: str | None = None
    phone: str | None = None
    blood_group: str | None = None
    address: str | None = None
    emergency_contact: str | None = None


class MemberResponse(BaseModel):
    id: UUID
    user_id: UUID
    date_of_birth: date
    gender: str
    phone: str
    blood_group: str | None
    address: str | None
    emergency_contact: str | None
    created_at: datetime
    updated_at: datetime | None

    class Config:
        from_attributes = True