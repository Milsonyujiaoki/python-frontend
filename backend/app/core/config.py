"""Configuration settings."""
from pydantic_settings import BaseSettings
from typing import Optional, List
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings with environment variable support."""

    # Application
    PROJECT_NAME: str = "✂️ Barbershop SaaS"
    DEBUG: bool = True
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "Modern barbershop management platform"

    # Server
    API_V1_PREFIX: str = "/api/v1"
    ALLOWED_HOSTS: List[str] = ["localhost", "127.0.0.1", "*"]

    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:8080",  # Solara
        "http://localhost:8081",  # Streamlit
        "http://localhost:8082",  # FastUI
        "http://localhost:3000",  # React/Next.js
        "http://localhost:5173",  # Vite
    ]

    # Security
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./barbershop.db"

    # Branding (customizable identity)
    BRAND_NAME: str = "BarberPro"
    BRAND_COLOR_PRIMARY: str = "#6366f1"  # Modern indigo (like Nubank)
    BRAND_COLOR_SECONDARY: str = "#10b981"  # Emerald green
    BRAND_COLOR_DARK: str = "#1e293b"  # Slate dark
    BRAND_COLOR_LIGHT: str = "#f8fafc"  # Light background
    BRAND_FONT: str = "Inter, system-ui, sans-serif"

    # Redis (optional for caching)
    REDIS_URL: Optional[str] = None

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


settings = get_settings()