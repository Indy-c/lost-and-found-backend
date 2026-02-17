from dataclasses import dataclass
from uuid import UUID

from ...domain.repositories.item_repo import ItemRepository


@dataclass
class RemoveItemCommand:
    item_id: UUID


class RemoveItemHandler:

    def __init__(self, item_repo: ItemRepository):
        self.item_repo = item_repo

    async def handle(self, cmd: RemoveItemCommand):
        item = await self.item_repo.get_by_id(cmd.item_id)

        if not item:
            raise ValueError("Item not found")

        # will implement delete in repository later
        await self.item_repo.delete(item.id)