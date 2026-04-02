from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from ...domain.entities.item import Item
from ...domain.repositories.item_repo import ItemRepository
from ...domain.value_objects.report_type import ReportType


@dataclass
class CreateItemCommand:
    report_type: ReportType
    title: str
    description_public: str
    category: str
    location_text: str
    happened_at: datetime
    posted_by_user_id: int
    verification_questions: list[str]


class CreateItemHandler:
    def __init__(self, item_repo: ItemRepository, audit_repo=None):
        self.item_repo = item_repo
        self.audit_repo = audit_repo

    async def handle(self, cmd: CreateItemCommand) -> UUID:
        item = Item.create(
            report_type=cmd.report_type,
            title=cmd.title,
            description_public=cmd.description_public,
            category=cmd.category,
            location_text=cmd.location_text,
            happened_at=cmd.happened_at,
            posted_by_user_id=cmd.posted_by_user_id,
            verification_questions=cmd.verification_questions,
        )

        await self.item_repo.save(item)

        if self.audit_repo is not None:
            await self.audit_repo.add(
                actor_user_id=cmd.posted_by_user_id,
                action="ITEM_CREATED",
                target_type="item",
                target_id=str(item.id),
            )

        return item.id
