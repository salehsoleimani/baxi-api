from typing import Any, Callable, Set

from pydantic import (
    AliasChoices,
    AmqpDsn,
    BaseModel,
    Field,
    ImportString,
    PostgresDsn,
    RedisDsn,
)

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    port: int = 80
    DATABASE_URL: str
    REDIS_URL: str
    SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_EXPIRE_MINUTES: int = 900
    SESSION_EXPIRE_MINUTES: int = 24 * 60 * 30
    OTP_EXPIRE_SECONDS: int = 60 * 5
    OTP_RESEND_SECONDS: int = 60 * 2
    SMS_KEY: str
    SMS_LINE: str

    class Config:
        env_file = ".env"


settings = Settings()
