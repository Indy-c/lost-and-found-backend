import asyncio

from app.shared.infrastructure.db import AsyncSessionLocal
from app.modules.auth.infrastructure.orm.models import UserModel, pwd_context
from sqlalchemy import text


async def seed_users():
    async with AsyncSessionLocal() as session:

        # Clear existing users
        await session.execute(text("DELETE FROM users"))

        user = UserModel(
            email="admin@example.com",
            password_hash=pwd_context.hash("123456"),
            role="ADMIN",
        )

        session.add(user)
        await session.commit()

        print("Seeded user: admin@example.com / 123456")


if __name__ == "__main__":
    asyncio.run(seed_users())