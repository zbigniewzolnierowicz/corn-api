from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    database_url: str
    env: str = "dev"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
