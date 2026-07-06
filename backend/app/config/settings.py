from typing import List, Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    app_name: str = "WiSense Backend"
    environment: str = "development"
    debug: bool = False
    version: str = "0.1.0"
    description: str = "AI-powered WiFi sensing platform backend."

    database_url: str
    api_v1_prefix: str = "/api/v1"
    cors_origins: List[str] = ["http://127.0.0.1:8000", "http://localhost:8000"]
    cors_allow_methods: List[str] = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]
    cors_allow_headers: List[str] = ["Authorization", "Content-Type", "Accept"]

    def get_cors_origins(self) -> List[str]:
        """Return CORS origins for exact domain matching."""

        if self.debug or self.environment == "development":
            return ["*"]
        return list(self.cors_origins)

    def get_cors_origin_regex(self) -> Optional[str]:
        """Return regex pattern for CORS origin matching (ngrok, localhost, etc)."""

        if self.debug or self.environment == "development":
            return r"https://.*\.ngrok.*\.app|http://localhost.*"
        return None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )
