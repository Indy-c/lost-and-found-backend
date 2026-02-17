from dataclasses import dataclass

from ..domain.repositories import UserRepository
from ..infrastructure.security.password import verify_password
from ..infrastructure.security.jwt import create_access_token

@dataclass
class LoginCommand:
    email: str
    password: str

class LoginHandler:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo
    
    async def handle(self, cmd: LoginCommand) -> str:
        user = await self.user_repo.get_by_email(cmd.email)

        if not user:
            raise ValueError("Invalid email or password.")

        if not verify_password(cmd.password, user.password_hash):
            raise ValueError("Invalid email or password.")

        token = create_access_token(
            subject=str(user.id),
            role=user.role.value,
        )

        return token