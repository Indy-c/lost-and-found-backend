from fastapi import FastAPI

from app.shared.infrastructure.db import engine, Base

from app.modules.auth.presentation.login import router as auth_login_router
from app.modules.auth.presentation.routes import router as auth_routes_router

app = FastAPI()

app.include_router(auth_login_router)
app.include_router(auth_routes_router)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)