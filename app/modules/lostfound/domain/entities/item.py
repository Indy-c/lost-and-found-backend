from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4

from ..value_objects.item_status import ItemStatus


@dataclass
class VerificationQuestion:
    question: str


@dataclass
class Item:
    id: UUID
    title: str
    description_public: str
    category: str
    location_text: str
    happened_at: datetime
    posted_by_user_id: UUID

    status: ItemStatus = ItemStatus.OPEN
    verification_questions: List[VerificationQuestion] = field(default_factory=list)
    active_claim_id: Optional[UUID] = None

    @staticmethod
    def create(
        title: str,
        description_public: str,
        category: str,
        location_text: str,
        happened_at: datetime,
        posted_by_user_id: UUID,
        verification_questions: List[str],
    ) -> "Item":
        item = Item(
            id=uuid4(),
            title=title,
            description_public=description_public,
            category=category,
            location_text=location_text,
            happened_at=happened_at,
            posted_by_user_id=posted_by_user_id,
            status=ItemStatus.OPEN,
            verification_questions=[VerificationQuestion(q) for q in verification_questions],
            active_claim_id=None,
        )
        return item

    def mark_pending(self, claim_id: UUID) -> None:
        if self.status != ItemStatus.OPEN:
            raise ValueError("Item must be OPEN to accept a claim.")
        self.status = ItemStatus.PENDING
        self.active_claim_id = claim_id

    def mark_returned(self) -> None:
        if self.status != ItemStatus.PENDING:
            raise ValueError("Item must be PENDING to be marked RETURNED.")
        self.status = ItemStatus.RETURNED