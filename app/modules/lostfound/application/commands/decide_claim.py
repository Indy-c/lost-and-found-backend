from dataclasses import dataclass
from uuid import UUID

from ...domain.repositories.claim_repo import ClaimRepository
from ...domain.repositories.item_repo import ItemRepository


@dataclass
class DecideClaimCommand:
    claim_id: UUID
    decision: str
    actor_user_id: int


class DecideClaimHandler:
    def __init__(
        self,
        item_repo: ItemRepository,
        claim_repo: ClaimRepository,
        audit_repo=None,
    ):
        self.item_repo = item_repo
        self.claim_repo = claim_repo
        self.audit_repo = audit_repo

    async def handle(self, cmd: DecideClaimCommand):
        claim = await self.claim_repo.get_by_id_for_update(cmd.claim_id)

        if not claim:
            raise ValueError("Claim not found")

        item = await self.item_repo.get_by_id_for_update(claim.item_id)

        if not item:
            raise ValueError("Item not found")

        if item.posted_by_user_id != cmd.actor_user_id:
            raise ValueError("Only item owner can decide this claim")

        if item.active_claim_id != claim.id:
            raise ValueError("Only the active claim can be decided")

        decision = cmd.decision.upper()

        if decision == "APPROVE":
            claim.approve()
            item.mark_returned()
        elif decision == "REJECT":
            claim.reject()
            item.reopen()
        else:
            raise ValueError("Invalid decision")

        await self.claim_repo.save(claim)
        await self.item_repo.save(item)

        if self.audit_repo is not None:
            await self.audit_repo.add(
                actor_user_id=cmd.actor_user_id,
                action=f"CLAIM_{decision}",
                target_type="claim",
                target_id=str(claim.id),
            )
