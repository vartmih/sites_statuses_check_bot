from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

env_file = f"{Path(__file__).parent.parent}/.env"


class Settings(BaseSettings):
    TOKEN: SecretStr

    model_config = SettingsConfigDict(env_file=env_file, env_file_encoding="utf-8")


settings = Settings()
