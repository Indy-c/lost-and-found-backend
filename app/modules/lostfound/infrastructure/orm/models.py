from datetime import datetime
from typing import List

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.infrastructure.db import Base


class ItemModel(Base):
    __tablename__ = "items"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    report_type: Mapped[str] = mapped_column(String(10), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description_public: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    location_text: Mapped[str] = mapped_column(String(255), nullable=False)
    happened_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    posted_by_user_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    active_claim_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    verification_questions: Mapped[List["VerificationQuestionModel"]] = relationship(
        back_populates="item",
        cascade="all, delete-orphan",
    )
    claims: Mapped[List["ClaimModel"]] = relationship(
        back_populates="item",
        cascade="all, delete-orphan",
    )


class VerificationQuestionModel(Base):
    __tablename__ = "verification_questions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    question: Mapped[str] = mapped_column(Text, nullable=False)
    item_id: Mapped[str] = mapped_column(
        ForeignKey("items.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    item: Mapped["ItemModel"] = relationship(back_populates="verification_questions")


class ClaimModel(Base):
    __tablename__ = "claims"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    item_id: Mapped[str] = mapped_column(
        ForeignKey("items.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    claimant_user_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    submitted_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    item: Mapped["ItemModel"] = relationship(back_populates="claims")
    answers: Mapped[List["ClaimAnswerModel"]] = relationship(
        back_populates="claim",
        cascade="all, delete-orphan",
    )


class ClaimAnswerModel(Base):
    __tablename__ = "claim_answers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    answer: Mapped[str] = mapped_column(Text, nullable=False)
    claim_id: Mapped[str] = mapped_column(
        ForeignKey("claims.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    claim: Mapped["ClaimModel"] = relationship(back_populates="answers")


class AuditLogModel(Base):
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    actor_user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    action: Mapped[str] = mapped_column(String(100), nullable=False)
    target_type: Mapped[str] = mapped_column(String(50), nullable=False)
    target_id: Mapped[str] = mapped_column(String(36), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
