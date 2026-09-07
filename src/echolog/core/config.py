from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    database_url: str = "sqlite:///echolog.db"

    GEMINI_API_KEY: str

    RESEND_API_KEY: str

    # JWT Configuration
    ACCESS_TOKEN_SECRET_KEY: str

    ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


config = Config()
