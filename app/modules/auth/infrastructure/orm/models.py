from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String
from uuid import uuid4
from app.shared.infrastructure.db import Base

class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(
        primary_key=True, 
        default=lambda:str(uuid4()),
        
    )
    email: Mapped[str] = mapped_column(
        String(255), 
        unique=True, 
        index=True
    )

    password_hash: Mapped[str] = mapped_column(
        String(255), 
        nullable=False
    )

    role: Mapped[str] = mapped_column(
        String(20), 
        nullable=False
    )


