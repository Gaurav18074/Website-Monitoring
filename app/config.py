from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "postgresql://monitor:monitor@db:5432/monitor"
    smtp_host: str = ""
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_pass: str = ""
    alert_email_to: str = ""
    slack_webhook_url: str = ""
    telegram_bot_token: str = ""
    telegram_chat_id: str = ""
    check_interval_seconds: int = 60

    class Config:
        env_file = ".env"

settings = Settings()
