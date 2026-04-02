from dataclasses import dataclass
from datetime import datetime


@dataclass
class UserSummaryDTO:
    id: int
    email: str
    role: str
    is_active: bool
    created_at: datetime


def to_user_summary_dto(user) -> UserSummaryDTO:
    return UserSummaryDTO(
        id=user.id,
        email=user.email,
        role=user.role,
        is_active=user.is_active,
        created_at=user.created_at,
    )
