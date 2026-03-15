import os
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


def find_env_file(filename: str = ".env", max_levels: int = 5) -> Optional[str]:
    """
    Ищет файл .env в текущей папке и max_levels уровней выше.
    Возвращает абсолютный путь, если найден, иначе None.
    """
    path = os.path.dirname(os.path.abspath(__file__))
    for _ in range(max_levels + 1):
        candidate = os.path.join(path, filename)
        if os.path.exists(candidate):
            return candidate
        path = os.path.dirname(path)
    return None


env_path = find_env_file()


class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str

    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    model_config = SettingsConfigDict(env_file=env_path, extra="ignore", env_file_encoding="utf-8", env_prefix="")


settings = Settings()


def get_db_url() -> str:
    return settings.DATABASE_URL


def get_redis_url() -> str:
    return settings.REDIS_URL


def get_jwt_secret() -> str:
    return settings.JWT_SECRET


def get_jwt_algorithm() -> str:
    return settings.JWT_ALGORITHM


def get_access_expire_minutes() -> int:
    return settings.ACCESS_TOKEN_EXPIRE_MINUTES


def get_refresh_expire_days() -> int:
    return settings.REFRESH_TOKEN_EXPIRE_DAYS
