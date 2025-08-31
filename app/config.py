import os
from typing import Optional
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Intercom API Configuration
    INTERCOM_ACCESS_TOKEN: str = os.getenv("INTERCOM_ACCESS_TOKEN", "")
    INTERCOM_WEBHOOK_SECRET: Optional[str] = os.getenv(
        "INTERCOM_WEBHOOK_SECRET")
    INTERCOM_WORKSPACE_ID: Optional[str] = os.getenv("INTERCOM_WORKSPACE_ID")

    # OpenAI Configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    OPENAI_MAX_TOKENS: int = int(os.getenv("OPENAI_MAX_TOKENS", "1000"))
    OPENAI_TEMPERATURE: float = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))

    # Application Configuration
    APP_NAME: str = "Intercom AI Support"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    # Server Configuration
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))

    # Database Configuration (if needed in the future)
    DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL")

    # Logging Configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # AI Configuration
    AI_ENABLED: bool = os.getenv("AI_ENABLED", "True").lower() == "true"
    AUTO_ESCALATION_ENABLED: bool = os.getenv(
        "AUTO_ESCALATION_ENABLED", "True").lower() == "true"
    SENTIMENT_ANALYSIS_ENABLED: bool = os.getenv(
        "SENTIMENT_ANALYSIS_ENABLED", "True").lower() == "true"

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))

    # Security
    SECRET_KEY: str = os.getenv(
        "SECRET_KEY", "your-secret-key-change-in-production")
    ALLOWED_HOSTS: str = os.getenv("ALLOWED_HOSTS", "*")

    class Config:
        env_file = ".env"
        case_sensitive = True


# Create settings instance
settings = Settings()

# Validation


def validate_settings():
    """Validate that required settings are present"""
    required_settings = [
        ("INTERCOM_ACCESS_TOKEN", settings.INTERCOM_ACCESS_TOKEN),
        ("OPENAI_API_KEY", settings.OPENAI_API_KEY),
    ]

    missing_settings = []
    for name, value in required_settings:
        if not value:
            missing_settings.append(name)

    if missing_settings:
        raise ValueError(
            f"Missing required environment variables: {', '.join(missing_settings)}")


# Validate settings on import
try:
    validate_settings()
except ValueError as e:
    print(f"Configuration Error: {e}")
    print("Please check your .env file and ensure all required variables are set.")
