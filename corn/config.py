from pydantic import BaseSettings


class Settings(BaseSettings):
    database_url: str
    env: str = "dev"

    class Config:
        env_file = ".env"


settings: Settings = Settings()  # type: ignore
