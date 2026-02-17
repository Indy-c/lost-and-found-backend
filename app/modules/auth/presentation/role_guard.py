from fastapi import Depends, HTTPException
from typing import Iterable

from .deps import get_current_user
from ..domain.user_role import UserRole


def require_roles(roles: Iterable[UserRole]):

    async def checker(user=Depends(get_current_user)):
        if user.role not in roles:
            raise HTTPException(
                status_code=403,
                detail="Not enough permissions",
            )
        return user

    return checker