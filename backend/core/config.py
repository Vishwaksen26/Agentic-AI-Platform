"""
AgentForge AI – Core Configuration
Reads from environment variables / .env file.
All connections degrade gracefully when not configured.
"""

from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # App
    app_name: str = "AgentForge AI"
    app_version: str = "1.0.0"
    debug: bool = True
    demo_mode: bool = True  # When True, agents use simulated data

    # API
    api_prefix: str = "/api/v1"
    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:5173", "http://127.0.0.1:3000"]

    # Security
    secret_key: str = "agentforge-super-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24 * 7  # 7 days

    # LLM
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    default_llm_model: str = "gpt-4o"
    default_llm_temperature: float = 0.1

    # Database
    postgres_url: Optional[str] = None
    database_url: str = "sqlite+aiosqlite:///./agentforge.db"

    # Redis
    redis_url: Optional[str] = None

    # ChromaDB
    chromadb_host: str = "localhost"
    chromadb_port: int = 8001

    # Clerk Auth
    clerk_secret_key: Optional[str] = None
    clerk_publishable_key: Optional[str] = None

    @property
    def effective_database_url(self) -> str:
        return self.postgres_url or self.database_url

    @property
    def llm_available(self) -> bool:
        return bool(self.openai_api_key or self.anthropic_api_key)


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
