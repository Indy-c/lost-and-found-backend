from fastapi import Depends, APIRouter, HTTPException
from pydantic import BaseModel
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.shared.infrastructure.db import get_session
from app.modules.auth.presentation.deps import get_current_user

from ...application.commands.submit_claim import (
    SubmitClaimHandler,
    SubmitClaimCommand,
)
from ...infrastructure.repositories.item_repo_sql import ItemRepositorySQL
from ...infrastructure.repositories.claim_repo_sql import ClaimRepositorySQL


router = APIRouter()


class SubmitClaimRequest(BaseModel):
    answers: list[str]


@router.post("/items/{item_id}/claims")
async def submit_claim(
    item_id: UUID,
    req: SubmitClaimRequest,
    user=Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):

    handler = SubmitClaimHandler(
        ItemRepositorySQL(session),
        ClaimRepositorySQL(session),
    )

    try:
        claim_id = await handler.handle(
            SubmitClaimCommand(
                item_id=item_id,
                claimant_user_id=user.id,
                answers=req.answers,
            )
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"claim_id": claim_id}