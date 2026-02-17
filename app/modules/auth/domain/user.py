from dataclasses import dataclass
from uuid import UUID

from .user_role import UserRole


@dataclass
class User:
    id: UUID
    email: str
    password_hash: str
    role: UserRole