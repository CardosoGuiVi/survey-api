from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseModel):
    host: str = "localhost"
    port: int = 5432
    user: str
    db: str
    password: str

    @property
    def uri(self) -> str:
        return (
            f"postgresql+asyncpg://{self.user}:"
            f"{self.password}@{self.host}:"
            f"{self.port}/{self.db}"
        )


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="SURVEY_API_",
        case_sensitive=False,
        env_nested_delimiter="__",
        extra="ignore",
    )

    # App
    app_name: str = "Survey API"
    debug: bool = False
    environment: str = "development"

    # Database
    database: DatabaseSettings

    # Auth
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60 * 24 * 7  # 7 dias

    # Sentry (opcional em dev)
    sentry_dsn: str = ""


settings = Settings()
