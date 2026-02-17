from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID
from datetime import datetime

from ..entities.claim import Claim

class ClaimRepository(ABC):

    @abstractmethod
    async def get_by_id(self, claim_id: UUID) -> Optional[Claim]:
        pass

    @abstractmethod
    async def create(
        self,
        claim_id: UUID,
        item_id: UUID,
        claimant_user_id: UUID,
        answers: List[str],
        submitted_at: datetime,
    ) -> None:
        pass

    @abstractmethod
    async def save(self, claim: Claim) -> None:
        pass