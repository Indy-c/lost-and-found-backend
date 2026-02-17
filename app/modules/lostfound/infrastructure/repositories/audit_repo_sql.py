from sqlalchemy.ext.asyncio import AsyncSession
from ..orm.models import AuditLogModel


class AuditLogRepositorySQL:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(
        self,
        actor_user_id: str,
        action: str,
        target_type: str,
        target_id: str,
    ):
        self.session.add(
            AuditLogModel(
                actor_user_id=actor_user_id,
                action=action,
                target_type=target_type,
                target_id=target_id,
            )
        )