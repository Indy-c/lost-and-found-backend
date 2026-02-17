from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from ..entities.item import Item

class ItemRepository(ABC):

    @abstractmethod
    async def get_by_id(self, item_id: UUID) -> Optional[Item]:
        pass

    @abstractmethod
    async def save(self, item: Item) -> None:
        pass