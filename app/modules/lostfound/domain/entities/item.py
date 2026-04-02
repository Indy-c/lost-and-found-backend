from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import List, Optional
from uuid import UUID, uuid4

from ..value_objects.item_status import ItemStatus
from ..value_objects.report_type import ReportType


@dataclass
class VerificationQuestion:
    question: str


@dataclass
class Item:
    id: UUID
    report_type: ReportType
    title: str
    description_public: str
    category: str
    location_text: str
    happened_at: datetime
    posted_by_user_id: int
    status: ItemStatus = ItemStatus.OPEN
    verification_questions: List[VerificationQuestion] = field(default_factory=list)
    active_claim_id: Optional[UUID] = None

    @staticmethod
    def create(
        report_type: ReportType | str,
        title: str,
        description_public: str,
        category: str,
        location_text: str,
        happened_at: datetime,
        posted_by_user_id: int,
        verification_questions: List[str],
    ) -> "Item":
        normalized_questions = [
            question.strip()
            for question in verification_questions
            if question.strip()
        ]

        if not title.strip():
            raise ValueError("Title is required.")

        if not description_public.strip():
            raise ValueError("Description is required.")

        if not category.strip():
            raise ValueError("Category is required.")

        if not location_text.strip():
            raise ValueError("Location is required.")

        if not normalized_questions:
            raise ValueError("At least one verification question is required.")

        normalized_happened_at = happened_at
        if normalized_happened_at.tzinfo is not None:
            normalized_happened_at = normalized_happened_at.astimezone(UTC).replace(
                tzinfo=None
            )

        return Item(
            id=uuid4(),
            report_type=ReportType(report_type),
            title=title.strip(),
            description_public=description_public.strip(),
            category=category.strip(),
            location_text=location_text.strip(),
            happened_at=normalized_happened_at,
            posted_by_user_id=posted_by_user_id,
            status=ItemStatus.OPEN,
            verification_questions=[
                VerificationQuestion(question)
                for question in normalized_questions
            ],
            active_claim_id=None,
        )

    def mark_pending(self, claim_id: UUID) -> None:
        if self.status != ItemStatus.OPEN:
            raise ValueError("Item must be OPEN to accept a claim.")
        self.status = ItemStatus.PENDING
        self.active_claim_id = claim_id

    def mark_returned(self) -> None:
        if self.status != ItemStatus.PENDING:
            raise ValueError("Item must be PENDING to be marked RETURNED.")
        self.status = ItemStatus.RETURNED

    def reopen(self) -> None:
        if self.status != ItemStatus.PENDING:
            raise ValueError("Item must be PENDING to reopen.")
        self.status = ItemStatus.OPEN
        self.active_claim_id = None
