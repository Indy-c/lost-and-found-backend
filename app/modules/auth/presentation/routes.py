from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.shared.infrastructure.db import get_session
from ..application.login import LoginHandler, LoginCommand
from ..infrastructure.repositories.user_repo_sql import UserRepositorySQL

router = APIRouter(prefix="/auth", tags=["auth"])

class LoginRequest(BaseModel):
    email: str
    password: str   

@router.post("/login")
async def login(
    req: LoginRequest,
    session: AsyncSession = Depends(get_session),
):
    handler = LoginHandler(UserRepositorySQL(session))

    try:
        token = await handler.handle(LoginCommand(
            email=req.email,
            password=req.password,
        ))
    
    except ValueError:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password.",
        )
    
    return {"access_token": token, "token_type": "bearer"}