from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4
from typing import List

from ...domain.repositories.item_repo import ItemRepository
from ...domain.repositories.claim_repo import ClaimRepository


@dataclass
class SubmitClaimCommand:
    item_id: UUID
    claimant_user_id: UUID
    answers: List[str]


class SubmitClaimHandler:

    def __init__(
        self,
        item_repo: ItemRepository,
        claim_repo: ClaimRepository,
    ):
        self.item_repo = item_repo
        self.claim_repo = claim_repo

    async def handle(self, cmd: SubmitClaimCommand) -> UUID:
        item = await self.item_repo.get_by_id(cmd.item_id)

        if not item:
            raise ValueError("Item not found")

        if item.status.value != "OPEN":
            raise ValueError("Item is not open for claims")

        if len(cmd.answers) != len(item.verification_questions):
            raise ValueError("Answers count mismatch")

        claim_id = uuid4()

        await self.claim_repo.create(
            claim_id=claim_id,
            item_id=item.id,
            claimant_user_id=cmd.claimant_user_id,
            answers=cmd.answers,
            submitted_at=datetime.utcnow(),
        )

        item.mark_pending(claim_id)

        await self.item_repo.save(item)

        return claim_id