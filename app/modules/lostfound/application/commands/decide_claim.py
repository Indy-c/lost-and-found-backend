from dataclasses import dataclass
from uuid import UUID


from ...domain.repositories.item_repo import ItemRepository
from ...domain.repositories.claim_repo import ClaimRepository

@dataclass
class DecideClaimCommand:
    claim_id: UUID
    decision: str  # "approve" or "reject"
    actor_user_id: UUID


class DecideClaimHandler:

    def __init__(
            self, 
            item_repo: ItemRepository, 
            claim_repo: ClaimRepository
    ):
            self.item_repo = item_repo
            self.claim_repo = claim_repo
    
    async def handle(self, cmd: DecideClaimCommand):

        claim = await self.claim_repo.get_by_id(cmd.claim_id)

        if not claim:
            raise ValueError("Claim not found")

        item = await self.item_repo.get_by_id(claim.item_id)

        if not item:
            raise ValueError("Item not found")
        
        # -----------------------------------
        # BUSINESS RULE: only item owner 
        # -----------------------------------
        if item.posted_by_user_id != cmd.actor_user_id:
             raise ValueError("Only item owner can decide this claim")
        
        if cmd.decision == "APPROVE":
            claim.approve()
            item.mark_returned()

        elif cmd.decision == "REJECT":
            claim.reject()
            
            # allow new cliams again
            item.active_claim_id = None
            item.status = item.status.OPEN
        
        else:
            raise ValueError("Invalid decision")
        
        await self.claim_repo.update(claim)
        await self.item_repo.update(item)