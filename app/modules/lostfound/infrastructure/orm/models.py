from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, ForeignKey
from uuid import uuid4
from datetime import datetime
from typing import List

from app.shared.infrastructure.db import Base


class ItemModel(Base):
    __tablename__ = "items"

    id: Mapped[str] = mapped_column(
        primary_key=True,
        default=lambda: str(uuid4()),
    )

    title: Mapped[str] = mapped_column(String(255))
    description_public: Mapped[str] = mapped_column(String(1000))
    category: Mapped[str] = mapped_column(String(100))
    location_text: Mapped[str] = mapped_column(String(255))
    happened_at: Mapped[datetime] = mapped_column(DateTime)
    posted_by_user_id: Mapped[str] = mapped_column(String(36))

    status: Mapped[str] = mapped_column(String(20))
    active_claim_id: Mapped[str | None] = mapped_column(String(36), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    verification_questions: Mapped[List["VerificationQuestionModel"]] = relationship(
        back_populates="item",
        cascade="all, delete-orphan",
    )


class VerificationQuestionModel(Base):
    __tablename__ = "verification_questions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    item_id: Mapped[str] = mapped_column(
        ForeignKey("items.id", ondelete="CASCADE"),
    )

    question: Mapped[str] = mapped_column(String(255))

    item = relationship(back_populates="verification_questions")


class ClaimModel(Base):
    __tablename__ = "claims"

    id: Mapped[str] = mapped_column(primary_key=True)
    item_id: Mapped[str] = mapped_column(
        ForeignKey("items.id", ondelete="CASCADE")
    )

    claimant_user_id: Mapped[str] = mapped_column(String(36))
    status: Mapped[str] = mapped_column(String(20))
    submitted_at: Mapped[datetime] = mapped_column(DateTime)

    answers: Mapped[List["ClaimAnswerModel"]] = relationship(
        back_populates="claim",
        cascade="all, delete-orphan",
    )


class ClaimAnswerModel(Base):
    __tablename__ = "claim_answers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    claim_id: Mapped[str] = mapped_column(
        ForeignKey("claims.id", ondelete="CASCADE")
    )

    answer: Mapped[str] = mapped_column(String(255))

    claim = relationship(back_populates="answers")


class AuditLogModel(Base):
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    actor_user_id: Mapped[str] = mapped_column(String(36))
    action: Mapped[str] = mapped_column(String(100))
    target_type: Mapped[str] = mapped_column(String(50))
    target_id: Mapped[str] = mapped_column(String(36))

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )