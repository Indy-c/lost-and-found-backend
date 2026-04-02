from contextlib import asynccontextmanager
from datetime import UTC, datetime

from fastapi import FastAPI
from sqlalchemy import inspect, text

from app.shared.infrastructure.db import Base, engine

from app.modules.auth.infrastructure.orm import models as auth_models  # noqa: F401
from app.modules.auth.presentation.routes import admin_router as admin_routes_router
from app.modules.auth.presentation.routes import router as auth_routes_router
from app.modules.lostfound.infrastructure.orm import models as lostfound_models  # noqa: F401
from app.modules.lostfound.presentation.routes.claims import router as claims_router
from app.modules.lostfound.presentation.routes.items import router as items_router
from app.shared.infrastructure.settings import settings

LOSTFOUND_TABLES = (
    "claim_answers",
    "claims",
    "verification_questions",
    "audit_logs",
    "items",
)

EXPECTED_LOSTFOUND_COLUMNS = {
    "items": {
        "id",
        "report_type",
        "title",
        "description_public",
        "category",
        "location_text",
        "happened_at",
        "posted_by_user_id",
        "status",
        "active_claim_id",
        "created_at",
    },
    "verification_questions": {"id", "question", "item_id"},
    "claims": {"id", "item_id", "claimant_user_id", "status", "submitted_at"},
    "claim_answers": {"id", "answer", "claim_id"},
    "audit_logs": {"id", "actor_user_id", "action", "target_type", "target_id", "created_at"},
}


def _has_legacy_lostfound_schema(sync_conn) -> bool:
    inspector = inspect(sync_conn)
    existing_tables = set(inspector.get_table_names())

    for table_name, required_columns in EXPECTED_LOSTFOUND_COLUMNS.items():
        if table_name not in existing_tables:
            continue

        existing_columns = {
            column["name"]
            for column in inspector.get_columns(table_name)
        }

        if not required_columns.issubset(existing_columns):
            return True

    return False


def _archive_legacy_lostfound_tables(sync_conn) -> None:
    inspector = inspect(sync_conn)
    existing_tables = set(inspector.get_table_names())

    if not _has_legacy_lostfound_schema(sync_conn):
        return

    suffix = datetime.now(UTC).strftime("%Y%m%d%H%M%S")

    for table_name in LOSTFOUND_TABLES:
        if table_name in existing_tables:
            sync_conn.execute(
                text(
                    f'ALTER TABLE "{table_name}" RENAME TO "{table_name}_legacy_{suffix}"'
                )
            )


def _repair_users_schema(sync_conn) -> None:
    inspector = inspect(sync_conn)
    existing_tables = set(inspector.get_table_names())

    if "users" not in existing_tables:
        return

    existing_columns = {
        column["name"]
        for column in inspector.get_columns("users")
    }

    if "is_active" not in existing_columns:
        sync_conn.execute(
            text(
                'ALTER TABLE "users" ADD COLUMN "is_active" BOOLEAN NOT NULL DEFAULT TRUE'
            )
        )

    if "created_at" not in existing_columns:
        sync_conn.execute(
            text(
                'ALTER TABLE "users" ADD COLUMN "created_at" TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP'
            )
        )


async def startup():
    async with engine.begin() as conn:
        if settings.repair_schema_on_startup:
            await conn.run_sync(_archive_legacy_lostfound_tables)
            await conn.run_sync(_repair_users_schema)

        if settings.auto_create_schema_on_startup:
            await conn.run_sync(Base.metadata.create_all)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await startup()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(auth_routes_router)
app.include_router(admin_routes_router)
app.include_router(items_router)
app.include_router(claims_router)
