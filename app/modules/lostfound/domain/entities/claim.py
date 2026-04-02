from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from ..value_objects.claim_status import ClaimStatus


@dataclass
class Claim:
    id: UUID
    item_id: UUID
    claimant_user_id: int
    answers: list[str]
    status: ClaimStatus
    submitted_at: datetime

    def approve(self):
        if self.status != ClaimStatus.SUBMITTED:
            raise ValueError("Only submitted claims can be approved.")
        self.status = ClaimStatus.APPROVED

    def reject(self):
        if self.status != ClaimStatus.SUBMITTED:
            raise ValueError("Only submitted claims can be rejected.")
        self.status = ClaimStatus.REJECTED
