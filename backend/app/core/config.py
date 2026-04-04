from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "GigProtect AI API"
    environment: str = "dev"
    debug: bool = True
    api_v1_prefix: str = "/api/v1"
    secret_key: str = "super-secret-change-me"
    access_token_expire_minutes: int = 60 * 24 * 7

    mongodb_uri: str = "mongodb://localhost:27017"
    mongodb_db: str = "gigprotect_ai"

    # Comma-separated CORS origins from env, e.g. "http://localhost:3000,http://127.0.0.1:3000"
    allowed_origins: str = "http://localhost:3000"

    scheduler_enabled: bool = True
    scheduler_interval_minutes: int = 15

    openweather_api_key: str = ""
    openweather_base_url: str = "https://api.openweathermap.org/data/2.5/weather"
    aqi_api_key: str = ""
    aqi_base_url: str = "https://api.waqi.info/feed"
    google_maps_api_key: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def allowed_origins_list(self) -> list[str]:
        return [item.strip() for item in self.allowed_origins.split(",") if item.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

