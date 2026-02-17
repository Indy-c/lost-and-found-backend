from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from datetime import datetime
from typing import List

from ...domain.repositories.claim_repo import ClaimRepository
from ...domain.entities.claim import Claim
from ...domain.value_objects.claim_status import ClaimStatus

from ..orm.models import ClaimModel, ClaimAnswerModel
from ..orm.mappers import map_claim_model_to_domain


class ClaimRepositorySQL(ClaimRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, claim_id: UUID):

        stmt = select(ClaimModel).where(
            ClaimModel.id == str(claim_id)
        )

        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()

        if not model:
            return None

        return map_claim_model_to_domain(model)

    async def create(
        self,
        claim_id: UUID,
        item_id: UUID,
        claimant_user_id: UUID,
        answers: List[str],
        submitted_at: datetime,
    ) -> None:

        model = ClaimModel(
            id=str(claim_id),
            item_id=str(item_id),
            claimant_user_id=str(claimant_user_id),
            status=ClaimStatus.SUBMITTED.value,
            submitted_at=submitted_at,
        )

        for a in answers:
            model.answers.append(
                ClaimAnswerModel(answer=a)
            )

        self.session.add(model)

        await self.session.flush()

    async def save(self, claim: Claim) -> None:

        model = await self.session.get(
            ClaimModel,
            str(claim.id),
        )

        if not model:
            raise ValueError("Claim not found")

        model.status = claim.status.value

        await self.session.flush()