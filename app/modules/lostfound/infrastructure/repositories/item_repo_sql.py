from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from uuid import UUID

from ...domain.repositories.item_repo import ItemRepository
from ...domain.entities.item import Item
from ..orm.models import ItemModel, VerificationQuestionModel
from ..orm.mappers import map_item_model_to_domain


class ItemRepositorySQL(ItemRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, item_id: UUID):

        stmt = (
            select(ItemModel)
            .where(ItemModel.id == str(item_id))
        )

        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()

        if not model:
            return None

        await self.session.refresh(
            model,
            attribute_names=["verification_questions"],
        )

        return map_item_model_to_domain(model)

    async def save(self, item: Item) -> None:

        model = await self.session.get(ItemModel, str(item.id))

        if not model:
            model = ItemModel(
                id=str(item.id),
            )
            self.session.add(model)

        model.title = item.title
        model.description_public = item.description_public
        model.category = item.category
        model.location_text = item.location_text
        model.happened_at = item.happened_at
        model.posted_by_user_id = str(item.posted_by_user_id)
        model.status = item.status.value
        model.active_claim_id = (
            str(item.active_claim_id)
            if item.active_claim_id
            else None
        )

        # replace verification questions
        model.verification_questions.clear()

        for q in item.verification_questions:
            model.verification_questions.append(
                VerificationQuestionModel(
                    question=q.question
                )
            )

        await self.session.flush()

    async def delete(self, item_id: UUID) -> None:

        stmt = delete(ItemModel).where(
            ItemModel.id == str(item_id)
        )
        await self.session.execute(stmt)