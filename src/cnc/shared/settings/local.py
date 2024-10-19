from typing import Self
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


env_path = Path(__file__).parent.parent.parent.parent.parent.joinpath(".env")


class LocalDevSettings(BaseSettings):

    model_config = SettingsConfigDict(env_file=env_path, extra="ignore")

    # Local development variables
    PORT: int = 8000
    AUTO_RELOAD: bool = True

    @classmethod
    def create_dev_settings(cls) -> Self:
        return cls()
