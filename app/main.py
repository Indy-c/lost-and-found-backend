from fastapi import FastAPI

from app.shared.infrastructure.db import engine, Base

import app.modules.auth.infrastructure.orm.models
import app.modules.lostfound.infrastructure.orm.models

app = FastAPI()


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)