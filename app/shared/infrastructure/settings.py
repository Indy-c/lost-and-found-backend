from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="LOSTFOUND_",
        extra="ignore",
    )

    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/lostfound"
    db_echo: bool = False
    jwt_secret_key: str = "SECRET_KEY"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30
    auth_login_rate_limit: int = 10
    auth_login_rate_window_seconds: int = 60
    auth_register_rate_limit: int = 5
    auth_register_rate_window_seconds: int = 300
    item_write_rate_limit: int = 20
    item_write_rate_window_seconds: int = 60
    claim_submit_rate_limit: int = 10
    claim_submit_rate_window_seconds: int = 300
    claim_decision_rate_limit: int = 20
    claim_decision_rate_window_seconds: int = 60
    auto_create_schema_on_startup: bool = True
    repair_schema_on_startup: bool = True


settings = Settings()
