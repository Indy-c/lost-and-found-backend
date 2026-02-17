from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.shared.infrastructure.db import get_session
from app.modules.auth.presentation.deps import get_current_user
from app.modules.auth.presentation.deps import require_roles
from app.modules.auth.domain.user_role import UserRole

from ...application.commands.decide_claim import (
    DecideClaimHandler,
    DecideClaimCommand,
)

from ...infrastructure.repositories.claim_repo_sql import ClaimRepositorySQL
from ...infrastructure.repositories.item_repo_sql import ItemRepositorySQL


router = APIRouter()


class DecideRequest(BaseModel):
    decision: str   # APPROVE or REJECT


@router.post("/claims/{claim_id}/decision")
async def decide_claim(
    claim_id: UUID,
    req: DecideRequest,
    user=Depends(require_roles([UserRole.OWNER])),
    session: AsyncSession = Depends(get_session),
):

    handler = DecideClaimHandler(
        item_repo=ItemRepositorySQL(session),
        claim_repo=ClaimRepositorySQL(session),
    )

    try:
        await handler.handle(
            DecideClaimCommand(
                claim_id=claim_id,
                decision=req.decision,
                actor_user_id=user.id,
            )
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"status": "ok"}