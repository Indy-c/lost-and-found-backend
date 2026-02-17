from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError

from ..infrastructure.security.jwt import SECRET_KEY, ALGORITHM
from ..infrastructure.repositories.user_repo_sql import UserRepository
from app.shared.infrastructure.db import get_session
from sqlalchemy.ext.asyncio import AsyncSession


# This tells FastAPI to read:
# Authorization: Bearer <token>
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: AsyncSession = Depends(get_session),
):
    # credentials.credentials = the raw JWT string
    token = credentials.credentials

    try:
        # decode JWT
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        # "sub" is what to put in create_access_token(subject=...)
        user_id = payload.get("sub")

        user = await repo.get_by_id(int(user_id))

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    # DB id is INT, not UUID
    repo = UserRepository(session)
    user = await repo.get_by_id(int(user_id))

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user