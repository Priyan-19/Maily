from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Maily API"
    debug: bool = True

    google_client_id: str
    google_client_secret: str
    google_redirect_uri: str = (
        "http://127.0.0.1:8000/api/auth/google/callback"
    )

    google_scopes: str = (
        "https://www.googleapis.com/auth/gmail.readonly"
    )

    database_url: str = ""

    groq_api_key: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def scopes(self) -> list[str]:
        return [
            scope.strip()
            for scope in self.google_scopes.split(",")
            if scope.strip()
        ]


import os

@lru_cache
def get_settings() -> Settings:
    s = Settings()
    if os.environ.get("DATABASE_URL"):
        s.database_url = os.environ["DATABASE_URL"]
    return s


settings = get_settings()