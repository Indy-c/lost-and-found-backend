import asyncio

from sqlalchemy import text

from app.modules.auth.infrastructure.orm.models import UserModel, pwd_context
from app.shared.infrastructure.db import AsyncSessionLocal


async def seed_users():
    async with AsyncSessionLocal() as session:
        await session.execute(text("DELETE FROM users"))

        admin = UserModel(
            email="admin@example.com",
            password_hash=pwd_context.hash("123456"),
            role="ADMIN",
        )
        owner = UserModel(
            email="owner@example.com",
            password_hash=pwd_context.hash("123456"),
            role="OWNER",
        )
        finder = UserModel(
            email="finder@example.com",
            password_hash=pwd_context.hash("123456"),
            role="FINDER",
        )

        session.add_all([admin, owner, finder])
        await session.commit()

        print("Seeded users:")
        print("  admin@example.com / 123456")
        print("  owner@example.com / 123456")
        print("  finder@example.com / 123456")


if __name__ == "__main__":
    asyncio.run(seed_users())
