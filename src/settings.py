from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

env_file = f"{Path(__file__).parent.parent}/.env"


class Settings(BaseSettings):
    TOKEN: SecretStr
    WEBHOOK_SECRET: SecretStr
    WEBHOOK_PATH: str
    WEB_SERVER_HOST: str
    WEB_SERVER_PORT: int
    BASE_WEBHOOK_URL: str
    DB_PATH: str

    model_config = SettingsConfigDict(env_file=env_file, env_file_encoding="utf-8")


settings = Settings()
