from pydantic import BaseSettings


class Settings(BaseSettings):
    database_url: str = ""
    env: str = "dev"

    class Config:
        env_file = ".env"


class PostgresSettings(BaseSettings):
    user: str = "corn"
    password: str = "corn"
    db: str = "corn"
    host: str = "localhost"
    port: int = 5432

    def base_url(self) -> str:
        return \
            f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}"

    def database_url(self, db: str | None = None) -> str:
        database = db if db is not None else self.db
        return self.base_url() + "/" + database

    class Config:
        env_prefix = "POSTGRES_"
        env_file = ".env"


settings: Settings = Settings()
pg_settings: PostgresSettings = PostgresSettings()
