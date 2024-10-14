from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

env_path = Path(__file__).parent.parent.parent.parent.parent.joinpath(".env")


class AlembicSettings(BaseSettings):

    DEPLOYMENT_ONLY: bool = False

    # Development variables (for DEPLOYMENT_ONLY="false")
    SCHEMA_NAME: str = "public"
    META_PATH: str = "entrypoints.alembic_meta"
    META_NAME: str = "metadata"

    # Database connection
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str

    model_config = SettingsConfigDict(env_file=env_path, extra="ignore")

    def get_db_url(self):
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )
