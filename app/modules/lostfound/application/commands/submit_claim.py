from dataclasses import dataclass
from datetime import UTC, datetime
from typing import List
from uuid import UUID, uuid4

from ...domain.repositories.claim_repo import ClaimRepository
from ...domain.repositories.item_repo import ItemRepository


@dataclass
class SubmitClaimCommand:
    item_id: UUID
    claimant_user_id: int
    answers: List[str]


class SubmitClaimHandler:
    def __init__(
        self,
        item_repo: ItemRepository,
        claim_repo: ClaimRepository,
        audit_repo=None,
    ):
        self.item_repo = item_repo
        self.claim_repo = claim_repo
        self.audit_repo = audit_repo

    async def handle(self, cmd: SubmitClaimCommand) -> UUID:
        item = await self.item_repo.get_by_id_for_update(cmd.item_id)

        if not item:
            raise ValueError("Item not found")

        if item.posted_by_user_id == cmd.claimant_user_id:
            raise ValueError("You cannot claim your own item")

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
            submitted_at=datetime.now(UTC).replace(tzinfo=None),
        )

        item.mark_pending(claim_id)
        await self.item_repo.save(item)

        if self.audit_repo is not None:
            await self.audit_repo.add(
                actor_user_id=cmd.claimant_user_id,
                action="CLAIM_SUBMITTED",
                target_type="claim",
                target_id=str(claim_id),
            )

        return claim_id
