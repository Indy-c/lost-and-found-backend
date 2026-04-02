from uuid import UUID

from sqlalchemy import delete, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ...domain.entities.item import Item
from ...domain.repositories.item_repo import ItemListFilters, ItemRepository
from ..orm.mappers import map_item_model_to_domain
from ..orm.models import ItemModel, VerificationQuestionModel


class ItemRepositorySQL(ItemRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, item_id: UUID):
        stmt = (
            select(ItemModel)
            .options(selectinload(ItemModel.verification_questions))
            .where(ItemModel.id == str(item_id))
        )

        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()

        if not model:
            return None

        return map_item_model_to_domain(model)

    async def get_by_id_for_update(self, item_id: UUID):
        stmt = (
            select(ItemModel)
            .options(selectinload(ItemModel.verification_questions))
            .where(ItemModel.id == str(item_id))
            .with_for_update()
        )

        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()

        if not model:
            return None

        return map_item_model_to_domain(model)

    async def save(self, item: Item) -> None:
        model = await self.session.get(ItemModel, str(item.id))

        if not model:
            model = ItemModel(id=str(item.id))
            self.session.add(model)
        else:
            await self.session.refresh(
                model,
                attribute_names=["verification_questions"],
            )

        model.report_type = item.report_type.value
        model.title = item.title
        model.description_public = item.description_public
        model.category = item.category
        model.location_text = item.location_text
        model.happened_at = item.happened_at
        model.posted_by_user_id = item.posted_by_user_id
        model.status = item.status.value
        model.active_claim_id = str(item.active_claim_id) if item.active_claim_id else None

        model.verification_questions.clear()
        for question in item.verification_questions:
            model.verification_questions.append(
                VerificationQuestionModel(question=question.question)
            )

        await self.session.flush()

    async def delete(self, item_id: UUID) -> None:
        stmt = delete(ItemModel).where(ItemModel.id == str(item_id))
        await self.session.execute(stmt)
        await self.session.flush()

    async def list(self, filters: ItemListFilters) -> list[Item]:
        stmt = (
            select(ItemModel)
            .options(selectinload(ItemModel.verification_questions))
            .order_by(ItemModel.created_at.desc())
        )

        if filters.query:
            pattern = f"%{filters.query.strip()}%"
            stmt = stmt.where(
                or_(
                    ItemModel.title.ilike(pattern),
                    ItemModel.description_public.ilike(pattern),
                    ItemModel.location_text.ilike(pattern),
                )
            )

        if filters.category:
            stmt = stmt.where(ItemModel.category == filters.category)

        if filters.status:
            stmt = stmt.where(ItemModel.status == filters.status.value)

        if filters.report_type:
            stmt = stmt.where(ItemModel.report_type == filters.report_type.value)

        if filters.posted_by_user_id is not None:
            stmt = stmt.where(ItemModel.posted_by_user_id == filters.posted_by_user_id)

        stmt = stmt.limit(filters.limit).offset(filters.offset)

        result = await self.session.execute(stmt)
        models = result.scalars().unique().all()
        return [map_item_model_to_domain(model) for model in models]
