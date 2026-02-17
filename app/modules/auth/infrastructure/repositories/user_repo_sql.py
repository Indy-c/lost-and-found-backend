from uuid import UUID
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ...domain.repositories import UserRepository
from ...domain.user import User
from ..orm.models import UserModel
from ...domain.user_role import UserRole


class UserRepositorySQL(UserRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_email(self, email: str) -> Optional[User]:
        stmt = select(UserModel).where(UserModel.email == email)
        result = await self.session.execute(stmt)
        row = result.scalar_one_or_none()

        if not row:
            return None

        return User(
            id=UUID(row.id),
            email=row.email,
            password_hash=row.password_hash,
            role=UserRole(row.role),
        )

    async def get_by_id(self, user_id: UUID) -> Optional[User]:
        stmt = select(UserModel).where(UserModel.id == str(user_id))
        result = await self.session.execute(stmt)
        row = result.scalar_one_or_none()

        if not row:
            return None

        return User(
            id=UUID(row.id),
            email=row.email,
            password_hash=row.password_hash,
            role=UserRole(row.role),
        )