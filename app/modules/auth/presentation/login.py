from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.shared.infrastructure.db import get_session
from app.modules.auth.infrastructure.repositories.user_repo_sql import UserRepository
from app.modules.auth.application.login import LoginHandler, LoginCommand

router = APIRouter(prefix="/auth", tags=["auth"])


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

@router.post("/login", response_model=LoginResponse)
async def login(
    request: LoginRequest,
    session: AsyncSession = Depends(get_session),
):
    user_repo = UserRepository(session)
    handler = LoginHandler(user_repo)

    try:
        token = await handler.handle(
            LoginCommand(
                email=request.email,
                password=request.password,
            )
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    return LoginResponse(access_token=token)