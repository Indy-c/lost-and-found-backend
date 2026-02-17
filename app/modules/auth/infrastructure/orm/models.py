from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String
from app.shared.infrastructure.db import Base
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    email: Mapped[str] = mapped_column(
    String(255),
    unique=True,
    index=True,
    nullable=False,
    )

    password_hash: Mapped[str] = mapped_column(
    String(255),
    nullable=False,
    )

    role: Mapped[str] = mapped_column(
    String(30),
    nullable=False,
    )

    # --------------------
    # domain style helper
    # --------------------
    def verify_password(self, raw_password: str) -> bool:
        return pwd_context.verify(raw_password, self.password_hash)