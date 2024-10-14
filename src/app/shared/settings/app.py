from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


env_path = Path(__file__).parent.parent.parent.parent.parent.joinpath(".env")


class AppSettings(BaseSettings):

    # Logging
    DB_ECHO: bool = False

    # HTTP API prefixes
    ROOT_URL: str = "/root"
    API_PREFIX: str = "/api"
    WEB_PREFIX: str = "/web"

    # Database connection
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str
    POSTGRES_SCHEME: str

    model_config = SettingsConfigDict(env_file=env_path, extra="ignore")

    def get_db_url(self):
        return (
            f"{self.POSTGRES_SCHEME}://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )
