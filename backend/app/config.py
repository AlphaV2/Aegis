from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from pydantic import field_validator


class Settings(BaseSettings):
    app_name: str = "Aegis Layer"
    app_env: str = "dev"
    app_port: int = 8000

    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/aegis"
    redis_url: str = "redis://localhost:6379/0"

    hmac_max_age_seconds: int = 300
    rate_limit_per_minute: int = 60
    velocity_limit_5_min: int = 10
    max_request_body_bytes: int = 1048576
    cors_origins: str = "http://localhost:3000"

    admin_api_key: str = ""

    model_config = ConfigDict(env_file=".env", env_file_encoding="utf-8")

    @field_validator("database_url")
    @classmethod
    def validate_database_url(cls, value: str) -> str:
        if not value.startswith("postgresql"):
            raise ValueError("DATABASE_URL must use PostgreSQL for production deployment")
        return value

    @field_validator("redis_url")
    @classmethod
    def validate_redis_url(cls, value: str) -> str:
        if not value.startswith("redis://") and not value.startswith("rediss://"):
            raise ValueError("REDIS_URL must use Redis for production deployment")
        return value


settings = Settings()
