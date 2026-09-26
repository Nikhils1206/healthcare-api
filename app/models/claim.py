import uuid
from datetime import date, datetime
from enum import Enum

from sqlalchemy import String, Date, DateTime, ForeignKey, Numeric, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

class ClaimStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

class Claim(Base):
    __tablename__ = "claims"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    member_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("members.id", ondelete="CASCADE"),
        nullable=False
    )

    claim_number: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True
    )

    service_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    description: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    diagnosis: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    billed_amount: Mapped[float] = mapped_column(
        Numeric(12, 2),
        nullable=False
    )

    approved_amount: Mapped[float | None] = mapped_column(
        Numeric(12, 2),
        nullable=True
    )

    status: Mapped[ClaimStatus] = mapped_column(
        SQLEnum(ClaimStatus),
        default=ClaimStatus.PENDING,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    member = relationship(
        "Member",
        back_populates="claims"
    )

    