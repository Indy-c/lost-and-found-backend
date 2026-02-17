from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.shared.infrastructure.db import get_session
from ..application.login import LoginHandler, LoginCommand
from ..infrastructure.repositories.user_repo_sql import UserRepository 

from .role_guard import require_roles
from ..domain.user_role import UserRole

router = APIRouter(prefix="/auth", tags=["auth"])

class LoginRequest(BaseModel):
    email: str
    password: str   

@router.post("/login")
async def login(
    req: LoginRequest,
    session: AsyncSession = Depends(get_session),
):
    handler = LoginHandler(UserRepository(session))

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

@router.get("/protected")
async def protected_test(user=Depends(require_roles([UserRole.ADMIN]))):
    return {
        "message": "Only Admin can access this endpoint",
        "user": {
            "id": user.id,
            "email": user.email,
            "role": user.role,
        }
    }