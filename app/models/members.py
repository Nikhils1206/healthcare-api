import uuid
from datetime import date, datetime

from sqlalchemy import String, Date, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Member(Base):
    __tablename__ = "members"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False
    )

    date_of_birth: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    gender: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    phone: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    blood_group: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True
    )

    address: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    emergency_contact: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True
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

    user = relationship(
        "User",
        back_populates="member"
    )
 