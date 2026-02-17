from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.modules.auth.infrastructure.orm.models import UserModel


class UserRepository:

    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_email(self, email: str) -> UserModel | None:

        stmt = (
            select(UserModel)
            .where(UserModel.email == email)
            .limit(1)
        )

        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()


    async def get_by_id(self, user_id: int) -> UserModel | None:

        stmt = (
            select(UserModel)
            .where(UserModel.id == user_id)
            .limit(1)
        )

        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()