from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Security
    secret_key: str = "dev-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 480

    # Database
    database_url: str = "sqlite:///./infrapilot.db"

    # Agent
    agent_name: str = "production-server-1"
    collect_interval: int = 30

    # Alerts
    alert_cpu_threshold: float = 80.0
    alert_memory_threshold: float = 85.0
    alert_disk_threshold: float = 90.0
    telegram_bot_token: str = ""
    telegram_chat_id: str = ""
    smtp_server: str = ""
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    alert_email_to: str = ""

    # Logging
    log_level: str = "INFO"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()