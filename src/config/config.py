from pydantic import BaseSettings


class Settings(BaseSettings):
    port: int = 80
    DATABASE_URL: str
    REDIS_URL: str
    SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_EXPIRE_MINUTES: int = 900
    SESSION_EXPIRE_MINUTES: int = 24 * 60 * 30

    class Config:
        env_file = ".env"


settings = Settings()
