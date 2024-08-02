from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, env_file_encoding='utf-8', extra='ignore'
    )
    SQLALCHEMY_DATABASE_URL: str
    REDIS_BROKER_URL: str
    REDIS_BACKEND_URL: str

settings = Settings()